import re

import pytest
import yaml

from helpers import COMMIT_SKILL_NAMES, ROOT, read_text, rel, split_frontmatter

# The `commit-*` skills are not part of the baselinedocs family: `skill_dirs()`
# never lists them, so the family's metadata, version, and reference tests do not
# reach them. This file is their whole test surface, and it pins the same things
# the family tests pin for a baselinedocs skill: the folder shape, the packaged
# copies of two canonical files, and the gate sentence in each SKILL.md.
COMMIT_SKILLS = {
    "commit-composer": "--concise",
    "commit-composer-max": "--max",
}

CANONICAL_CONVENTION = ROOT / "contract" / "commit-convention.md"
CANONICAL_KIT = ROOT / "contract" / "commitkit.sh"

# Each skill ships both files because a skill cannot reach a sibling's folder.
SHIPPED = {
    "references/commit-convention.md": CANONICAL_CONVENTION,
    "scripts/commitkit.sh": CANONICAL_KIT,
}

CONVENTION_GATE = (
    "Read `references/commit-convention.md` in full before grouping or writing any "
    "message, every time."
)


def tool_gate(flag):
    return (
        "Run `sh <skill-dir>/scripts/commitkit.sh scan` on the staged diff before every "
        f"commit, and `sh <skill-dir>/scripts/commitkit.sh lint {flag} <msgfile>` on every "
        "message before `git commit -F`."
    )


def skill_text(name):
    return read_text(ROOT / name / "SKILL.md")


def test_every_commit_skill_is_classified():
    assert set(COMMIT_SKILL_NAMES) == set(COMMIT_SKILLS), (
        f"commit-* folders on disk {sorted(COMMIT_SKILL_NAMES)} differ from COMMIT_SKILLS "
        f"{sorted(COMMIT_SKILLS)}: update COMMIT_SKILLS in tests/test_commit_skills.py"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_skill_frontmatter(name):
    frontmatter, _ = split_frontmatter(skill_text(name))
    assert isinstance(frontmatter, dict), f"{name}/SKILL.md has no frontmatter block"
    assert frontmatter.get("name") == name
    description = frontmatter.get("description")
    assert isinstance(description, str) and description.strip()
    assert len(description) <= 1024, f"{name}: description is {len(description)} characters"
    assert "version" not in frontmatter, (
        f"{name}: the release stamp only reaches baselinedocs-* skills, so a version "
        "here would never be updated and would go stale"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_description_carries_the_words_a_user_would_type(name):
    description = split_frontmatter(skill_text(name))[0]["description"].lower()
    for word in ("commit", "conventional", "hunk"):
        assert word in description, (
            f"{name}: description lacks {word!r}; on a host that is not Codex the "
            "description is the only selection surface"
        )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_openai_yaml_is_an_explicit_entrypoint(name):
    data = yaml.safe_load(read_text(ROOT / name / "agents" / "openai.yaml"))
    interface, policy = data["interface"], data["policy"]
    for key in ("display_name", "short_description", "default_prompt"):
        assert isinstance(interface.get(key), str) and interface[key].strip()
    assert f"${name}" in interface["default_prompt"]
    assert policy.get("allow_implicit_invocation") is False, (
        f"{name}: a skill that commits is something the user calls, never an agent"
    )
    assert not interface["display_name"].startswith("Baseline Docs"), (
        f"{name}: it is not a baselinedocs skill and must not wear that name"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_folder_shape(name):
    held = {
        path.relative_to(ROOT / name).as_posix()
        for path in (ROOT / name).rglob("*")
        if path.is_file()
    }
    assert held == {"SKILL.md", "agents/openai.yaml", *SHIPPED}, (
        f"{name} holds {sorted(held)}"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
@pytest.mark.parametrize("asset", SHIPPED)
def test_packaged_copy_is_byte_identical(name, asset):
    copy = ROOT / name / asset
    assert copy.read_bytes() == SHIPPED[asset].read_bytes(), (
        f"{rel(copy)} drifted from {rel(SHIPPED[asset])}: edit the canonical file, then copy it"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_skill_requires_the_convention_and_the_checks(name):
    text = skill_text(name)
    assert CONVENTION_GATE in text, f"{name} never requires reading the convention"
    assert tool_gate(COMMIT_SKILLS[name]) in text, (
        f"{name} does not gate commits on scan and on lint {COMMIT_SKILLS[name]}"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_skill_stops_when_the_checks_cannot_run(name):
    assert "do not commit unchecked" in skill_text(name), (
        f"{name}: without sh the secret scan cannot run, and committing unscanned is "
        "the failure the gate exists to prevent"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_no_dependency_outside_the_skill_folder(name):
    for path in (ROOT / name).rglob("*"):
        if not path.is_file():
            continue
        text = read_text(path)
        assert "../" not in text, f"{rel(path)} reaches outside its folder"
        assert "baselinedocs-" not in text, (
            f"{rel(path)} names a baselinedocs skill: a commit skill installs without the family"
        )


def test_each_skill_routes_to_the_other_by_name_only():
    assert "`commit-composer-max`" in skill_text("commit-composer")
    assert "`commit-composer`" in skill_text("commit-composer-max")


def test_no_trailer_rule_survives_in_the_convention():
    text = read_text(CANONICAL_CONVENTION)
    assert re.search(r"No trailer of any kind that names an AI tool or a co-author", text)
