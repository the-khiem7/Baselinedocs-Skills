import re
import shutil
import subprocess

import pytest

from helpers import ROOT

# `contract/packtool.sh` ships to skills as a byte-identical copy, so testing the
# canonical file tests every copy. Each case builds a small pack in a temporary
# directory, breaks exactly one rule, and asserts the rule code that names it.
TOOL = (ROOT / "contract" / "packtool.sh").as_posix()
SH = shutil.which("sh")


def frontmatter(pack, document, code_ref="uncommitted"):
    return (
        "---\n"
        'baseline_schema: "2.0"\n'
        f'pack: "{pack}"\n'
        f'document: "{document}"\n'
        'status: "active"\n'
        'updated: "2026-10-05"\n'
        f'code_ref: "{code_ref}"\n'
        "---\n"
    )


HALLUCINATION = """
# TB: Decisions

## Entry index

| Entry | About | Status | Related |
|---|---|---|---|
| TB-D1 | broker disk size | current | TB-Q1 |
| TB-D2 | telemetry TTL | current | TB-D1 |
| TB-Q1 | broker-2 disk growth | open | TB-D1 |

## TB-D1: broker disk size

Decided: grow the volume.

## TB-D2: telemetry TTL

Decided: expire telemetry after 30 days.

## Open questions

### TB-Q1: why does broker-2 use more disk?

Unanswered.
"""

ROADMAP = """
# TB: Roadmap

## TB-P1: size the brokers

Done. TB-D1 holds the reasoning.
"""

INTRODUCTION = """
# TB: Introduction

Scope: the broker fleet.
"""


def write_pack(root, name="tb", hallucination=HALLUCINATION, roadmap=ROADMAP, code_ref="uncommitted"):
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    docs = {"introduction": INTRODUCTION, "roadmap": roadmap, "hallucination": hallucination}
    for document, body in docs.items():
        (folder / f"{name}.{document}.md").write_text(
            frontmatter(name, document, code_ref) + body, encoding="utf-8", newline="\n"
        )
    return folder


def run(cwd, *args):
    assert SH, (
        "no `sh` on PATH; packtool.sh needs a POSIX shell (Git for Windows provides one)"
    )
    return subprocess.run(
        [SH, TOOL, *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8"
    )


def rules(result, level):
    # The location may hold spaces (a folder titled "TB Broker Fleet"), so the rule
    # is the word after the `:<line>` that ends it, not the third field.
    pattern = re.compile(r"^" + level + r" .*:\d+ ([a-z-]+) ")
    return [m.group(1) for m in map(pattern.match, result.stdout.splitlines()) if m]


def edit(folder, document, old, new, name="tb"):
    path = folder / f"{name}.{document}.md"
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture edit did not apply: {old!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def test_clean_pack_passes(tmp_path):
    write_pack(tmp_path)
    result = run(tmp_path, "check", "tb")
    assert result.returncode == 0, result.stdout + result.stderr
    assert rules(result, "FAIL") == [] and rules(result, "WARN") == [], result.stdout
    assert "0 FAIL, 0 WARN in 3 documents" in result.stdout


def test_crlf_pack_passes(tmp_path):
    folder = write_pack(tmp_path)
    for path in folder.iterdir():
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    result = run(tmp_path, "check", "tb")
    assert result.returncode == 0, result.stdout + result.stderr


# The duplicate-identifier mistake: a second TB-Q1 allocated from memory.
def test_duplicate_identifier_fails_with_both_locations(tmp_path):
    folder = write_pack(tmp_path)
    edit(folder, "hallucination", "| TB-Q1 | broker-2", "| TB-Q1 | RDS autoscaling | open | - |\n| TB-Q1 | broker-2")
    edit(folder, "hallucination", "Unanswered.", "Unanswered.\n\n### TB-Q1: RDS storage autoscaling?\n\nOpen.")
    result = run(tmp_path, "check", "tb")
    assert result.returncode == 1
    assert "duplicate-heading" in rules(result, "FAIL")
    assert "duplicate-index-row" in rules(result, "FAIL")
    line = next(line for line in result.stdout.splitlines() if "duplicate-heading" in line)
    assert line.count("tb.hallucination.md:") == 3, line


FAIL_CASES = {
    "entry-without-index-row": ("hallucination", "| TB-D2 | telemetry TTL | current | TB-D1 |\n", ""),
    "index-row-without-entry": ("hallucination", "| TB-Q1 | broker", "| TB-D9 | ghost | current | - |\n| TB-Q1 | broker"),
    "missing-entry-index": ("hallucination", "## Entry index", "## Index"),
    "question-outside-open-questions": ("hallucination", "## TB-D2: telemetry TTL", "## TB-Q2: stray question\n\n## TB-D2: telemetry TTL"),
    "decision-under-open-questions": ("hallucination", "Unanswered.", "Unanswered.\n\n### TB-D3: filed as open"),
    "decision-outside-hallucination": ("roadmap", "Done.", "## TB-D4: decided in the roadmap\n\nDone."),
    "phase-outside-roadmap": ("hallucination", "Unanswered.", "Unanswered.\n\n## TB-P2: a phase in the journal"),
    "bold-heading": ("hallucination", "Decided: grow the volume.", "Decided: grow the volume.\n\n**TB-D5: a bold pseudo-heading**"),
    "typographic-dash": ("introduction", "Scope: the broker fleet.", "Scope: the broker fleet " + chr(0x2014) + " all of it."),
    "frontmatter-key-missing": ("introduction", 'status: "active"\n', ""),
    "frontmatter-value": ("introduction", 'status: "active"', 'status: "done"'),
    "filename-mismatch": ("introduction", 'document: "introduction"', 'document: "sourcecode"'),
    "unterminated-frontmatter": ("introduction", "---\n\n# TB: Introduction", "\n# TB: Introduction"),
}


@pytest.mark.parametrize("rule", sorted(FAIL_CASES))
def test_structural_rule_fails(tmp_path, rule):
    document, old, new = FAIL_CASES[rule]
    folder = write_pack(tmp_path)
    edit(folder, document, old, new)
    result = run(tmp_path, "check", "tb")
    assert result.returncode == 1, result.stdout
    assert rule in rules(result, "FAIL"), result.stdout


def test_missing_frontmatter_fails(tmp_path):
    folder = write_pack(tmp_path)
    (folder / "tb.introduction.md").write_text(INTRODUCTION, encoding="utf-8", newline="\n")
    result = run(tmp_path, "check", "tb")
    assert "missing-frontmatter" in rules(result, "FAIL"), result.stdout


def test_prefix_shared_by_two_packs_fails(tmp_path):
    write_pack(tmp_path, "tb")
    write_pack(tmp_path, "rds")
    result = run(tmp_path, "check", ".")
    assert "prefix-collision" in rules(result, "FAIL"), result.stdout


WARN_CASES = {
    "closed-question-under-open-questions": ("hallucination", "| broker-2 disk growth | open |", "| broker-2 disk growth | closed by TB-D2 |"),
    "unresolved-citation": ("roadmap", "Done.", "Done. See TB-D8."),
    "reasoning-in-roadmap": ("roadmap", "Done. TB-D1 holds the reasoning.", "Done. The root cause was a full volume."),
    "possible-hard-wrap": ("introduction", "Scope: the broker fleet.", "Scope: the broker\nfleet and its disks."),
    "repeated-fact": ("roadmap", "Done.", "Done. Disk grew to 200 GB on 2026-09-12."),
}


@pytest.mark.parametrize("rule", sorted(WARN_CASES))
def test_heuristic_rule_warns_without_failing(tmp_path, rule):
    document, old, new = WARN_CASES[rule]
    folder = write_pack(tmp_path)
    edit(folder, document, old, new)
    if rule == "repeated-fact":
        edit(folder, "hallucination", "Decided: grow the volume.", "Decided: grow the volume to 200 GB on 2026-09-12.")
    result = run(tmp_path, "check", "tb")
    assert result.returncode == 0, result.stdout
    assert rule in rules(result, "WARN"), result.stdout


# The unchecked `code_ref` mistake: code committed, pack still says uncommitted.
def test_code_ref_uncommitted_with_clean_tree_warns(tmp_path):
    write_pack(tmp_path / "docs")
    (tmp_path / "app.txt").write_text("code\n", encoding="utf-8")
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run([*git, "add", "."], cwd=tmp_path, check=True)
    subprocess.run([*git, "commit", "-qm", "init"], cwd=tmp_path, check=True)
    edit(tmp_path / "docs" / "tb", "roadmap", "Done.", "Done, edited after the commit.")
    result = run(tmp_path, "check", "docs/tb")
    assert "code-ref-stale" in rules(result, "WARN"), result.stdout + result.stderr


def test_next_id_counts_citations_of_closed_questions(tmp_path):
    folder = write_pack(tmp_path)
    assert run(tmp_path, "next-id", "tb", "D").stdout.strip() == "TB-D3"
    assert run(tmp_path, "next-id", "tb", "P").stdout.strip() == "TB-P2"
    edit(folder, "roadmap", "Done.", "Done. TB-Q4 was closed by TB-D2.")
    assert run(tmp_path, "next-id", "tb", "Q").stdout.strip() == "TB-Q5"


def test_next_id_on_an_empty_pack_starts_at_one_with_a_prefix(tmp_path):
    (tmp_path / "new").mkdir()
    result = run(tmp_path, "next-id", "new", "D", "NW")
    assert result.returncode == 0 and result.stdout.strip() == "NW-D1", result.stdout + result.stderr
    assert run(tmp_path, "next-id", "new", "Q", "NW").stdout.strip() == "NW-Q1"
    bare = run(tmp_path, "next-id", "new", "D")
    assert bare.returncode == 2 and "pass the prefix" in bare.stderr, bare.stderr


# A readable folder title is not a defect: the existing packs live in such folders.
def test_folder_title_differs_from_pack_id_only_warns(tmp_path):
    folder = write_pack(tmp_path)
    folder.rename(tmp_path / "TB Broker Fleet")
    result = run(tmp_path, "check", "TB Broker Fleet")
    assert result.returncode == 0, result.stdout
    assert "directory-mismatch" in rules(result, "WARN"), result.stdout


def test_check_dot_from_inside_the_pack_folder_resolves_the_folder_name(tmp_path):
    folder = write_pack(tmp_path)
    result = run(folder, "check", ".")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "directory-mismatch" not in rules(result, "WARN"), result.stdout
    assert "0 FAIL, 0 WARN in 3 documents" in result.stdout


def test_consecutive_bold_label_lines_are_not_a_hard_wrap(tmp_path):
    folder = write_pack(tmp_path)
    edit(folder, "roadmap", "Done. TB-D1 holds the reasoning.", "**Dependencies:** none\n**Status:** done. TB-D1 holds the reasoning.")
    assert "possible-hard-wrap" not in rules(run(tmp_path, "check", "tb"), "WARN")
    edit(folder, "roadmap", "**Status:** done.", "**Status:** done,\ncontinued here.")
    assert "possible-hard-wrap" in rules(run(tmp_path, "check", "tb"), "WARN")


def test_next_id_needs_a_prefix_when_none_or_several_exist(tmp_path):
    write_pack(tmp_path, "tb")
    write_pack(tmp_path, "rds", hallucination=HALLUCINATION.replace("TB-", "RD-"), roadmap=ROADMAP.replace("TB-", "RD-"))
    assert run(tmp_path, "next-id", ".", "D").returncode == 2
    assert run(tmp_path, "next-id", ".", "D", "RD").stdout.strip() == "RD-D3"


def test_find_lists_every_occurrence_by_kind(tmp_path):
    write_pack(tmp_path)
    result = run(tmp_path, "find", "tb", "TB-D1")
    kinds = [line.split("\t")[1] for line in result.stdout.splitlines()]
    assert result.returncode == 0
    assert sorted(set(kinds)) == ["citation", "heading", "index-row"], result.stdout
    assert run(tmp_path, "find", "tb", "TB-D99").returncode == 1


def test_find_prints_an_identifier_cited_twice_on_one_line_once(tmp_path):
    folder = write_pack(tmp_path)
    edit(folder, "roadmap", "Done. TB-D1 holds the reasoning.", "Done. TB-D1 holds the reasoning; TB-D1 is current.")
    result = run(tmp_path, "find", "tb", "TB-D1")
    hits = [line for line in result.stdout.splitlines() if line.startswith("tb/tb.roadmap.md:")]
    assert len(hits) == 1, result.stdout


# A question entry holds reasoning as validly as a decision entry does.
def test_reasoning_linked_to_a_question_does_not_warn(tmp_path):
    folder = write_pack(tmp_path)
    edit(folder, "roadmap", "Done. TB-D1 holds the reasoning.", "Done. TB-Q1 carries the rejected options.")
    result = run(tmp_path, "check", "tb")
    assert "reasoning-in-roadmap" not in rules(result, "WARN"), result.stdout


def test_outline_reports_headings_with_current_line_numbers(tmp_path):
    write_pack(tmp_path)
    result = run(tmp_path, "outline", "tb/tb.hallucination.md")
    assert "tb/tb.hallucination.md:24\t## TB-D2: telemetry TTL" in result.stdout, result.stdout


@pytest.mark.parametrize("args", [(), ("check",), ("bogus", "tb"), ("find", "tb", "D1"), ("next-id", "tb", "X")])
def test_bad_usage_exits_2(tmp_path, args):
    write_pack(tmp_path)
    assert run(tmp_path, *args).returncode == 2


# Dogfood: this repository's own packs must carry no structural failure.
def test_repository_packs_have_no_structural_failure():
    result = run(ROOT, "check", "docs/baseline")
    assert result.returncode == 0, result.stdout + result.stderr
