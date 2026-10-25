import importlib.util
import re

import pytest

from helpers import ROOT, SKILL_NAMES, read_skill, split_frontmatter

VERSIONED = [*SKILL_NAMES, "baseline-core", "baseline-academic-core"]

spec = importlib.util.spec_from_file_location(
    "stamp_version", ROOT / "scripts" / "stamp_version.py"
)
stamp_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stamp_version)

SAMPLE = '---\nname: x\ndescription: y\n---\n\n# Body\n'


def versions():
    return {
        name: split_frontmatter(read_skill(name))[0].get("version")
        for name in VERSIONED
    }


@pytest.mark.parametrize("name", VERSIONED)
def test_skill_declares_a_semver_string(name):
    version = versions()[name]
    assert isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version), (
        f"{name}/SKILL.md has version {version!r}; it must be a quoted "
        "MAJOR.MINOR.PATCH string, written by scripts/stamp_version.py"
    )


def test_every_skill_carries_the_same_version():
    found = versions()
    assert len(set(found.values())) == 1, (
        f"skills disagree on version: {found}; run scripts/stamp_version.py "
        "once with the release version rather than editing one file"
    )


def test_stamp_inserts_then_replaces_without_touching_the_body():
    first = stamp_version.stamp_text(SAMPLE, "1.2.3")
    assert first == '---\nname: x\ndescription: y\nversion: "1.2.3"\n---\n\n# Body\n'
    second = stamp_version.stamp_text(first, "1.2.4")
    assert second == first.replace("1.2.3", "1.2.4")
    assert stamp_version.stamp_text(second, "1.2.4") == second


def test_stamp_keeps_crlf_line_endings():
    crlf = SAMPLE.replace("\n", "\r\n")
    assert stamp_version.stamp_text(crlf, "1.0.0") == (
        '---\r\nname: x\r\ndescription: y\r\nversion: "1.0.0"\r\n---\r\n\r\n# Body\r\n'
    )


@pytest.mark.parametrize("raw", ["1.2", "v1.2.3.4", "latest", "v1.2.x", ""])
def test_stamp_rejects_a_tag_that_is_not_semver(raw):
    with pytest.raises(ValueError):
        stamp_version.parse_version(raw)


def test_stamp_accepts_a_leading_v():
    assert stamp_version.parse_version("v1.2.3") == "1.2.3"


def test_check_reports_a_skill_that_differs_and_writes_nothing(capsys):
    current = next(iter(set(versions().values())))
    assert stamp_version.main(["stamp_version.py", "--check", f"v{current}"]) == 0
    assert stamp_version.main(["stamp_version.py", "--check", "v99.0.0"]) == 1
    assert "version is not 99.0.0" in capsys.readouterr().out
    assert set(versions().values()) == {current}


def test_check_needs_a_version_argument():
    assert stamp_version.main(["stamp_version.py", "--check"]) == 2
