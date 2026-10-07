import shutil
import subprocess
import sys

import pytest

from helpers import ROOT

# `contract/commitkit.sh` ships to skills as a byte-identical copy, so testing the
# canonical file tests every copy. Each case builds a small git repository in a
# temporary directory and asserts one behaviour of one command.
TOOL = (ROOT / "contract" / "commitkit.sh").as_posix()
SH = shutil.which("sh")

pytestmark = pytest.mark.skipif(SH is None, reason="needs a POSIX sh on PATH")


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", *args], cwd=repo, check=check, capture_output=True, text=True
    )


def kit(repo, *args):
    return subprocess.run(
        [SH, TOOL, *args], cwd=repo, capture_output=True, text=True
    )


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q", ".")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    git(tmp_path, "config", "core.autocrlf", "false")
    return tmp_path


def commit_all(repo, message="init"):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)


def units(repo):
    out = kit(repo, "hunks")
    assert out.returncode == 0, out.stderr
    return [line.split("\t") for line in out.stdout.splitlines()]


def stage_units(repo, *ids):
    # Bytes, not text: text mode rewrites newlines on Windows and corrupts the patch.
    patch = subprocess.run([SH, TOOL, "patch", *ids], cwd=repo, capture_output=True)
    assert patch.returncode == 0, patch.stderr
    applied = subprocess.run(
        ["git", "apply", "--cached", "--unidiff-zero"],
        cwd=repo,
        input=patch.stdout,
        capture_output=True,
    )
    assert applied.returncode == 0, applied.stderr.decode()


def three_hunk_file(repo):
    """Edit line 3, insert two lines after line 12, delete line 25 of a 30-line file."""
    (repo / "f.txt").write_text("".join(f"{n}\n" for n in range(1, 31)))
    commit_all(repo)
    lines = [f"{n}\n" for n in range(1, 31)]
    lines[2] = "three\n"
    lines.insert(12, "ins1\nins2\n")
    lines.remove("25\n")
    (repo / "f.txt").write_text("".join(lines))


def ids_of(rows, name):
    return [row[0] for row in rows if row[1] == name]


# --- hunks -----------------------------------------------------------------


def test_hunks_lists_each_changed_region_as_its_own_unit(repo):
    three_hunk_file(repo)
    rows = units(repo)
    assert len(ids_of(rows, "f.txt")) == 3
    assert all(row[2] == "hunk" for row in rows)


def test_hunks_lists_untracked_file_as_a_new_file_unit(repo):
    (repo / "keep.txt").write_text("x\n")
    commit_all(repo)
    (repo / "new.txt").write_text("a\nb\n")
    rows = units(repo)
    assert [(row[1], row[2], row[3]) for row in rows] == [("new.txt", "hunk", "-0,0")]


def test_hunks_skips_ignored_files(repo):
    (repo / ".gitignore").write_text("ignored.txt\n")
    commit_all(repo)
    (repo / "ignored.txt").write_text("x\n")
    assert units(repo) == []


def test_hunks_lists_a_deleted_file(repo):
    (repo / "d.txt").write_text("x\n")
    commit_all(repo)
    (repo / "d.txt").unlink()
    rows = units(repo)
    assert [(row[1], row[4]) for row in rows] == [("d.txt", "+0,0")]


def test_hunks_makes_a_binary_file_one_whole_unit(repo):
    (repo / "keep.txt").write_text("x\n")
    commit_all(repo)
    (repo / "b.bin").write_bytes(b"\x00\x01\x02bin")
    rows = units(repo)
    assert [(row[1], row[2], row[6]) for row in rows] == [("b.bin", "whole", "binary")]


@pytest.mark.skipif(sys.platform == "win32", reason="file modes are not tracked on Windows")
def test_hunks_makes_a_mode_change_one_whole_unit(repo):
    (repo / "run.sh").write_text("x\n")
    commit_all(repo)
    git(repo, "config", "core.fileMode", "true")
    (repo / "run.sh").chmod(0o755)
    rows = units(repo)
    assert [(row[1], row[2], row[6]) for row in rows] == [("run.sh", "whole", "mode-change")]


def test_hunks_works_before_the_first_commit(repo):
    (repo / "a.txt").write_text("a\n")
    rows = units(repo)
    assert [(row[1], row[2]) for row in rows] == [("a.txt", "hunk")]


def test_hunks_refuses_unmerged_paths(repo):
    (repo / "f.txt").write_text("base\n")
    commit_all(repo)
    git(repo, "checkout", "-q", "-b", "other")
    (repo / "f.txt").write_text("other\n")
    commit_all(repo, "other")
    git(repo, "checkout", "-q", "-")
    (repo / "f.txt").write_text("main\n")
    commit_all(repo, "main")
    git(repo, "merge", "other", check=False)
    out = kit(repo, "hunks")
    assert out.returncode == 1
    assert "unmerged" in out.stderr


def test_hunks_never_touches_the_index(repo):
    three_hunk_file(repo)
    (repo / "new.txt").write_text("n\n")
    before = git(repo, "write-tree").stdout
    status_before = git(repo, "status", "--short").stdout
    units(repo)
    assert git(repo, "write-tree").stdout == before
    assert git(repo, "status", "--short").stdout == status_before


def test_hunks_outside_a_repository_is_a_usage_error(tmp_path):
    out = kit(tmp_path, "hunks")
    assert out.returncode == 2


# --- patch -----------------------------------------------------------------


def test_patch_with_a_skipped_hunk_between_two_chosen_ones_applies(repo):
    three_hunk_file(repo)
    first, _, third = ids_of(units(repo), "f.txt")
    stage_units(repo, first, third)
    cached = git(repo, "diff", "--cached", "-U0").stdout
    assert "+three" in cached
    assert "-25" in cached
    assert "ins1" not in cached


def test_patch_staging_every_unit_matches_the_working_tree(repo):
    three_hunk_file(repo)
    stage_units(repo, *ids_of(units(repo), "f.txt"))
    assert git(repo, "diff").stdout == ""


def test_patch_handles_new_file_deleted_file_and_binary_together(repo):
    (repo / "d.txt").write_text("x\n")
    commit_all(repo)
    (repo / "d.txt").unlink()
    (repo / "n.txt").write_text("brand\nnew\n")
    (repo / "b.bin").write_bytes(b"\x00\x01\x02bin")
    stage_units(repo, *[row[0] for row in units(repo)])
    names = git(repo, "diff", "--cached", "--name-status").stdout.split()
    assert sorted(names) == sorted(["D", "d.txt", "A", "n.txt", "A", "b.bin"])
    assert git(repo, "status", "--short").stdout.count("??") == 0


def test_patch_places_a_pure_insertion_when_an_earlier_hunk_is_skipped(repo):
    # git apply positions a pure insertion by its new-side start, with no line text
    # to search for. Keeping the full diff's start would land it one line early and
    # still exit 0, so the offset must be recomputed for the subset.
    (repo / "f.txt").write_text("".join(f"{n}\n" for n in range(1, 31)))
    commit_all(repo)
    lines = [f"{n}\n" for n in range(1, 31)]
    del lines[2]
    lines.insert(20, "NEWLINE\n")
    (repo / "f.txt").write_text("".join(lines))
    deletion, insertion = ids_of(units(repo), "f.txt")
    stage_units(repo, insertion)
    staged = git(repo, "show", ":f.txt").stdout.splitlines()
    assert staged[staged.index("NEWLINE") - 1] == "21"
    assert "3" in staged, "the skipped deletion must stay unstaged"


def test_unit_ids_survive_a_commit_that_moves_line_numbers(repo):
    three_hunk_file(repo)
    first, middle, third = ids_of(units(repo), "f.txt")
    third_row = [row for row in units(repo) if row[0] == third][0]
    stage_units(repo, middle)
    git(repo, "commit", "-q", "-m", "the insertion")
    git(repo, "reset", "-q")
    after = [row for row in units(repo) if row[1] == "f.txt"]
    survivor = [row for row in after if row[0] == third][0]
    assert survivor[3] != third_row[3], "the old range must have moved for this to test anything"
    assert [row[0] for row in after] == [first, third]


def test_patch_roundtrips_a_crlf_file(repo):
    (repo / "w.txt").write_bytes(b"a\r\nb\r\nc\r\n")
    commit_all(repo)
    (repo / "w.txt").write_bytes(b"a\r\nB\r\nc\r\n")
    stage_units(repo, *ids_of(units(repo), "w.txt"))
    assert git(repo, "diff").stdout == ""


def test_patch_with_an_unknown_id_fails_and_names_it(repo):
    three_hunk_file(repo)
    out = kit(repo, "patch", "deadbeef00")
    assert out.returncode == 1
    assert "deadbeef00" in out.stderr


def test_patch_drops_the_index_line_of_a_partial_file(repo):
    three_hunk_file(repo)
    first = ids_of(units(repo), "f.txt")[0]
    assert "\nindex " not in "\n" + kit(repo, "patch", first).stdout


def test_two_identical_units_in_one_file_get_distinct_ids(repo):
    (repo / "f.txt").write_text("a\nx\nb\nc\nd\ne\nf\ng\nh\n")
    commit_all(repo)
    (repo / "f.txt").write_text("a\nx\nb\nNEW\nc\nd\ne\nf\ng\nNEW\nh\n")
    ids = ids_of(units(repo), "f.txt")
    assert len(ids) == 2 and len(set(ids)) == 2


# --- scan ------------------------------------------------------------------
# Fixtures are assembled at run time so this file holds no string a secret
# scanner would match.

PRIVATE_KEY_HEADER = "-----BEGIN " + "RSA PRIVATE KEY-----"
ACCESS_KEY_ID = "AKIA" + "IOSFODNN7EXAMPLE"
FAKE_VALUE = "Zq" * 6
CREDENTIAL_NAME = "db_" + "pass" + "word"
KEY_NAME = "api" + "_key"


def stage_file(repo, name, text):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    git(repo, "add", name)


def test_scan_passes_a_clean_staged_diff(repo):
    stage_file(repo, "a.txt", "nothing secret\n")
    out = kit(repo, "scan")
    assert out.returncode == 0
    assert out.stdout.startswith("OK scan"), "a pass must be visible, not silent"


def test_scan_flags_a_private_key_block_by_location_not_value(repo):
    stage_file(repo, "a.txt", f"x\n{PRIVATE_KEY_HEADER}\nMIIB\n")
    out = kit(repo, "scan")
    assert out.returncode == 1
    assert "FAIL private-key-block a.txt:2" in out.stdout
    assert "MIIB" not in out.stdout


def test_scan_flags_an_access_key_id_without_printing_it(repo):
    stage_file(repo, "conf.txt", f"id = {ACCESS_KEY_ID}\n")
    out = kit(repo, "scan")
    assert out.returncode == 1
    assert "FAIL aws-access-key-id conf.txt:1" in out.stdout
    assert ACCESS_KEY_ID not in out.stdout


def test_scan_flags_a_literal_credential_assignment(repo):
    stage_file(repo, "app.cfg", f'{CREDENTIAL_NAME} = "{FAKE_VALUE}"\n')
    out = kit(repo, "scan")
    assert "FAIL credential-assignment app.cfg:1" in out.stdout
    assert FAKE_VALUE not in out.stdout


def test_scan_ignores_a_placeholder_credential(repo):
    stage_file(repo, "app.cfg", f'{CREDENTIAL_NAME} = "<DB_VALUE>"\n{KEY_NAME} = "changeme"\n')
    assert kit(repo, "scan").returncode == 0


@pytest.mark.parametrize(
    "name",
    ["server.pem", "deploy.key", "id_rsa", "terraform.tfstate", ".env", ".aws/credentials"],
)
def test_scan_flags_a_secret_bearing_file_name(repo, name):
    stage_file(repo, name, "x\n")
    out = kit(repo, "scan")
    assert out.returncode == 1
    assert name in out.stdout


def test_scan_allows_an_env_example(repo):
    stage_file(repo, ".env.example", "X=\n")
    assert kit(repo, "scan").returncode == 0


# --- lint ------------------------------------------------------------------

GOOD = "feat(billing): add proration\n\n- compute credit from remaining days\n- round to the cent\n"


def lint(repo, text, *flags):
    msg = repo / "MSG"
    msg.write_bytes(text.encode("utf-8"))
    return kit(repo, "lint", *flags, str(msg))


def test_lint_accepts_a_conforming_message(repo):
    out = lint(repo, GOOD)
    assert out.returncode == 0, out.stdout
    assert "OK lint" in out.stdout, "a pass must be visible, not silent"


def test_lint_prints_no_ok_line_after_a_fail(repo):
    assert "OK lint" not in lint(repo, "add proration\n").stdout


def test_lint_accepts_a_title_only_message_in_default_mode(repo):
    assert lint(repo, "fix(api): reject empty id\n").returncode == 0


@pytest.mark.parametrize(
    "text, rule",
    [
        ("add proration\n", "title-format"),
        ("feat: add proration\n", "title-format"),
        ("feature(billing): add proration\n", "title-format"),
        ("feat(billing): " + "x" * 70 + "\n", "title-length"),
        ("feat(billing): add proration\nbody right away\n", "blank-line"),
        ("feat(billing): add proration\n\nplain sentence\n", "body-not-bullet"),
        ("feat(billing): add proration\n\n- one bullet that\n  wraps onto a second line\n", "body-not-bullet"),
        ("feat(billing): add proration " + chr(0x2013) + " now\n", "typographic-dash"),
        ("feat(billing): add proration " + chr(0x2014) + " now\n", "typographic-dash"),
        ("feat(billing): add proration\n\n- follows FD-D12\n", "pack-identifier"),
        ("feat(billing): add proration\n\n- covers phase 3\n", "phase-number"),
        ("feat(billing): add proration\n\n- see docs/baseline/x\n", "pack-path"),
        ("feat(billing): add proration\n\n- edit billing.roadmap.md\n", "pack-file"),
        ("feat(billing): add proration\n\nCo-Authored-By: Someone <a@example.com>\n", "ai-trailer"),
        ("", "empty-message"),
    ],
)
def test_lint_fails_each_rule(repo, text, rule):
    out = lint(repo, text)
    assert out.returncode == 1
    assert f"FAIL {rule}" in out.stdout


def test_lint_allows_a_breaking_change_footer(repo):
    text = "feat(api)!: drop v1\n\n- remove the v1 routes\n\nBREAKING CHANGE: v1 clients must move to v2\n"
    out = lint(repo, text)
    assert out.returncode == 0, out.stdout


def test_lint_reads_a_crlf_message(repo):
    assert lint(repo, GOOD.replace("\n", "\r\n")).returncode == 0


def test_lint_concise_rejects_a_label_line(repo):
    out = lint(repo, "fix(api): x\n\nWhy:\n- one\n", "--concise")
    assert "FAIL label-in-concise" in out.stdout


def test_lint_concise_rejects_more_than_five_bullets(repo):
    body = "".join(f"- b{n}\n" for n in range(6))
    out = lint(repo, "fix(api): x\n\n" + body, "--concise")
    assert "FAIL too-many-bullets" in out.stdout


def test_lint_concise_warns_past_fifty_characters(repo):
    out = lint(repo, "fix(api): " + "x" * 45 + "\n", "--concise")
    assert out.returncode == 0
    assert "WARN title-length" in out.stdout


def test_lint_max_requires_a_body(repo):
    out = lint(repo, "fix(api): reject empty id\n", "--max")
    assert "FAIL body-missing" in out.stdout


def test_lint_max_accepts_labelled_bullets(repo):
    text = (
        "fix(api): reject empty id\n\n"
        "Why:\n- an empty id reached the database\n\n"
        "Changes:\n- api/handler.go: validate id before lookup, return 400\n\n"
        "Risk and verification:\n- go test ./api passed\n"
    )
    out = lint(repo, text, "--max")
    assert out.returncode == 0, out.stdout


def test_lint_max_warns_on_vague_wording(repo):
    out = lint(repo, "fix(api): x\n\n- various cleanups\n", "--max")
    assert "WARN vague-wording" in out.stdout
    assert out.returncode == 0


def test_lint_warns_on_a_reference_to_a_commit_by_position(repo):
    out = lint(repo, "docs(x): y\n\n- the fix landed just before this commit\n")
    assert "WARN commit-position-reference" in out.stdout
    assert out.returncode == 0


def test_lint_flags_a_pack_wording_as_a_warning(repo):
    out = lint(repo, "docs(x): y\n\n- update the doc pack\n")
    assert "WARN pack-wording" in out.stdout
    assert out.returncode == 0
