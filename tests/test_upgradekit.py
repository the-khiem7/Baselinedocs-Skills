import os
import shutil
import subprocess

import pytest

from helpers import ROOT

# `baselinedocs-self-upgrade/scripts/upgradekit.sh` is the only copy, so this tests
# the shipped file. Each case builds a fake home directory in a temporary
# directory and passes it as the root, so no case reads the real machine.
TOOL = (ROOT / "baselinedocs-self-upgrade" / "scripts" / "upgradekit.sh").as_posix()
SH = shutil.which("sh")


def install(root, agent, skill, version='"3.1.0"', body="", newline="\n"):
    # `agent` is the path under the root, for example ".claude/skills".
    folder = root / agent / skill
    folder.mkdir(parents=True, exist_ok=True)
    lines = ["---", f"name: {skill}", "description: fixture"]
    if version is not None:
        lines.append(f"version: {version}")
    lines += ["---", body]
    (folder / "SKILL.md").write_text(
        newline.join(lines), encoding="utf-8", newline=""
    )
    return folder


def run(*args, env=None):
    assert SH, (
        "no `sh` on PATH; upgradekit.sh needs a POSIX shell (Git for Windows provides one)"
    )
    return subprocess.run(
        [SH, TOOL, *args], capture_output=True, text=True, encoding="utf-8", env=env
    )


def rows(result):
    return [line.split("\t") for line in result.stdout.splitlines() if "\t" in line]


def inventory(root):
    result = run("inventory", root.as_posix())
    assert result.returncode == 0, result.stdout + result.stderr
    prefix = len(root.as_posix()) + 1
    return result, {(r[0], r[3][prefix:].rsplit("/", 2)[0]): r[1] for r in rows(result)}


def statuses(result):
    return {(r[1], r[4]): r[0] for r in rows(result)}


def test_inventory_finds_installs_at_both_depths(tmp_path):
    install(tmp_path, ".claude/skills", "baselinedocs-help")
    install(tmp_path, ".gemini/config/skills", "baselinedocs-help")
    install(tmp_path, ".config/crush/skills", "baselinedocs-save")
    result, found = inventory(tmp_path)
    assert found == {
        ("baselinedocs-help", ".claude"): "3.1.0",
        ("baselinedocs-help", ".gemini/config"): "3.1.0",
        ("baselinedocs-save", ".config/crush"): "3.1.0",
    }, result.stdout
    assert result.stdout.rstrip().endswith("OK 3 install(s)")


def test_inventory_ignores_skills_that_are_not_baselinedocs(tmp_path):
    install(tmp_path, ".claude/skills", "baselinedocs-help")
    install(tmp_path, ".claude/skills", "archify")
    result, found = inventory(tmp_path)
    assert list(found) == [("baselinedocs-help", ".claude")], result.stdout


# `.*` also matches `..`, which would scan the parent of the root.
def test_inventory_does_not_scan_the_parent_of_the_root(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    install(tmp_path, "skills", "baselinedocs-help")
    result = run("inventory", home.as_posix())
    assert result.stdout.strip() == "NONE no baselinedocs install found", result.stdout


def test_inventory_reports_none_when_nothing_is_installed(tmp_path):
    result = run("inventory", tmp_path.as_posix())
    assert result.returncode == 0
    assert result.stdout.strip() == "NONE no baselinedocs install found"


def test_roots_default_to_home(tmp_path):
    install(tmp_path, ".kiro/skills", "baselinedocs-help")
    env = {**os.environ, "HOME": tmp_path.as_posix()}
    result = run("inventory", env=env)
    assert result.returncode == 0 and "OK 1 install(s)" in result.stdout, result.stdout


def test_several_roots_are_all_scanned(tmp_path):
    first, second = tmp_path / "a", tmp_path / "b"
    install(first, ".claude/skills", "baselinedocs-help")
    install(second, ".kiro/skills", "baselinedocs-help", version='"3.0.0"')
    result = run("inventory", first.as_posix(), second.as_posix())
    assert [r[1] for r in rows(result)] == ["3.1.0", "3.0.0"], result.stdout


VERSIONS = {
    "double quoted": ('"3.1.0"', "3.1.0"),
    "single quoted": ("'3.1.0'", "3.1.0"),
    "bare": ("3.1.0", "3.1.0"),
    "trailing space": ('"3.1.0"  ', "3.1.0"),
    "absent": (None, "-"),
    "prerelease": ('"3.1.0-rc1"', "-"),
    "two components": ('"3.1"', "-"),
    "empty": ('""', "-"),
}


@pytest.mark.parametrize("label", VERSIONS)
def test_version_is_read_from_the_frontmatter(tmp_path, label):
    declared, expected = VERSIONS[label]
    install(tmp_path, ".claude/skills", "baselinedocs-help", version=declared)
    result = run("inventory", tmp_path.as_posix())
    assert rows(result)[0][1] == expected, result.stdout


def test_crlf_frontmatter_is_read(tmp_path):
    install(tmp_path, ".claude/skills", "baselinedocs-help", newline="\r\n")
    assert rows(run("inventory", tmp_path.as_posix()))[0][1] == "3.1.0"


# A `version:` in the body, or indented under another key, is not the skill's.
def test_a_version_outside_the_top_level_frontmatter_is_ignored(tmp_path):
    folder = install(
        tmp_path, ".claude/skills", "baselinedocs-help", version=None,
        body='version: "9.9.9"',
    )
    path = folder / "SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "description: fixture", "metadata:\n  version: \"8.8.8\""
        ),
        encoding="utf-8",
        newline="",
    )
    assert rows(run("inventory", tmp_path.as_posix()))[0][1] == "-"


def test_a_file_without_frontmatter_is_unparsable(tmp_path):
    folder = tmp_path / ".claude" / "skills" / "baselinedocs-help"
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text('version: "3.1.0"\n', encoding="utf-8")
    assert rows(run("inventory", tmp_path.as_posix()))[0][1] == "-"


def test_a_symbolic_link_is_marked_link(tmp_path):
    real = install(tmp_path, ".agents/skills", "baselinedocs-help")
    link = tmp_path / ".claude" / "skills" / "baselinedocs-help"
    link.parent.mkdir(parents=True)
    try:
        os.symlink(real, link, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("this host cannot create a symbolic link without elevation")
    kinds = {r[3].rsplit("/", 3)[-3]: r[2] for r in rows(run("inventory", tmp_path.as_posix()))}
    assert kinds == {".agents": "dir", ".claude": "link"}


def compare(root, latest):
    return run("compare", latest, root.as_posix())


def test_compare_marks_each_status(tmp_path):
    install(tmp_path, ".a/skills", "baselinedocs-current", version='"3.1.0"')
    install(tmp_path, ".a/skills", "baselinedocs-ahead", version='"3.2.0"')
    install(tmp_path, ".a/skills", "baselinedocs-behind", version='"3.0.0"')
    install(tmp_path, ".a/skills", "baselinedocs-old", version=None)
    result = compare(tmp_path, "3.1.0")
    by_skill = {r[1]: r[0] for r in rows(result)}
    assert by_skill == {
        "baselinedocs-current": "current",
        "baselinedocs-ahead": "ahead",
        "baselinedocs-behind": "behind",
        "baselinedocs-old": "unparsable",
    }
    assert result.returncode == 1
    assert "FAIL 2 of 4 install(s) behind 3.1.0 or unparsable" in result.stdout


# A string comparison would put 3.9.0 above 3.10.0.
def test_versions_compare_numerically_not_as_strings(tmp_path):
    install(tmp_path, ".a/skills", "baselinedocs-help", version='"3.10.0"')
    assert [r[0] for r in rows(compare(tmp_path, "3.9.0"))] == ["ahead"]
    install(tmp_path, ".b/skills", "baselinedocs-help", version='"3.9.0"')
    result = compare(tmp_path, "3.10.0")
    assert statuses(result)[("baselinedocs-help", (tmp_path / ".b/skills/baselinedocs-help").as_posix())] == "behind"


def test_compare_passes_when_nothing_is_behind(tmp_path):
    install(tmp_path, ".a/skills", "baselinedocs-help")
    install(tmp_path, ".b/skills", "baselinedocs-help", version='"3.2.0"')
    result = compare(tmp_path, "3.1.0")
    assert result.returncode == 0
    assert result.stdout.rstrip().endswith("OK 2 install(s) at or above 3.1.0")


def test_compare_accepts_a_tag_with_its_v_prefix(tmp_path):
    install(tmp_path, ".a/skills", "baselinedocs-help")
    result = compare(tmp_path, "v3.1.0")
    assert result.returncode == 0 and "at or above 3.1.0" in result.stdout


def test_compare_reports_none_when_nothing_is_installed(tmp_path):
    result = compare(tmp_path, "3.1.0")
    assert result.returncode == 0
    assert result.stdout.strip() == "NONE no baselinedocs install found"


USAGE_ERRORS = {
    "no command": [],
    "unknown command": ["frobnicate"],
    "compare without a version": ["compare"],
    "latest is not semver": ["compare", "latest"],
    "latest is two components": ["compare", "3.1"],
}


@pytest.mark.parametrize("label", USAGE_ERRORS)
def test_usage_errors_exit_2(label):
    result = run(*USAGE_ERRORS[label])
    assert result.returncode == 2 and result.stdout == "", result.stdout + result.stderr


def test_empty_home_with_no_root_exits_2():
    result = run("inventory", env={**os.environ, "HOME": ""})
    if result.returncode == 0:
        pytest.skip("this shell restores an empty HOME before the script runs")
    assert result.returncode == 2 and "HOME" in result.stderr


def test_it_never_writes(tmp_path):
    install(tmp_path, ".a/skills", "baselinedocs-help", version='"3.0.0"')
    install(tmp_path, ".b/skills", "baselinedocs-save", version=None)

    def snapshot():
        return sorted(
            (p.relative_to(tmp_path).as_posix(), p.stat().st_mtime_ns, p.stat().st_size)
            for p in tmp_path.rglob("*")
        )

    before = snapshot()
    run("inventory", tmp_path.as_posix())
    compare(tmp_path, "3.1.0")
    assert snapshot() == before
