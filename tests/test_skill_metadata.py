import re

import pytest
import yaml

from helpers import ROOT, SKILL_NAMES, read_skill, read_text, split_frontmatter

ENTRYPOINTS = {
    "baselinedocs-init",
    "baselinedocs-adopt",
    "baselinedocs-onboard",
    "baselinedocs-load",
    "baselinedocs-brief",
    "baselinedocs-save",
    "baselinedocs-run",
    "baselinedocs-callout",
    "baselinedocs-help",
    "baselinedocs-adr",
}

# Lifecycle skills are agent-selected and say so in their display name. The one
# exception is a lifecycle skill a user also calls by hand as often as an agent
# selects it, which drops `Internal` so the name does not read as off-limits.
LIFECYCLE_PREFIX = "Baseline Docs Internal: "
ENTRYPOINT_PREFIX = "Baseline Docs "
DISPLAY_NAME_EXCEPTIONS = {
    "baselinedocs-recall": "Baseline Docs: Recall",
}

# The Agent Skills format bounds these; a host may truncate or reject beyond them.
MAX_NAME = 64
MAX_DESCRIPTION = 1024

ENTRYPOINT_HINT = (
    "add it to ENTRYPOINTS in tests/test_skill_metadata.py if it is a user "
    "entrypoint, otherwise set allow_implicit_invocation to true"
)


def load_openai(name):
    return yaml.safe_load(read_text(ROOT / name / "agents" / "openai.yaml"))


def test_entrypoints_are_real_skill_folders():
    assert ENTRYPOINTS <= set(SKILL_NAMES), (
        f"ENTRYPOINTS names folders that do not exist: "
        f"{sorted(ENTRYPOINTS - set(SKILL_NAMES))}"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_skill_frontmatter(name):
    frontmatter, _ = split_frontmatter(read_skill(name))
    assert isinstance(frontmatter, dict), f"{name}/SKILL.md has no frontmatter block"
    assert frontmatter.get("name") == name, (
        f"{name}/SKILL.md declares name {frontmatter.get('name')!r}, not its folder"
    )
    assert re.fullmatch(r"[a-z0-9-]+", name) and len(name) <= MAX_NAME, (
        f"{name}: lowercase letters, digits and hyphens only, at most {MAX_NAME}"
    )
    description = frontmatter.get("description")
    assert isinstance(description, str) and description.strip(), (
        f"{name}/SKILL.md has no description, which is the selection surface on "
        "every host"
    )
    assert len(description) <= MAX_DESCRIPTION, (
        f"{name}/SKILL.md description is {len(description)} characters, "
        f"over {MAX_DESCRIPTION}"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_openai_yaml_shape(name):
    data = load_openai(name)
    assert isinstance(data, dict), f"{name}/agents/openai.yaml is not a mapping"
    interface = data.get("interface")
    policy = data.get("policy")
    assert isinstance(interface, dict), f"{name}: openai.yaml has no interface block"
    assert isinstance(policy, dict), f"{name}: openai.yaml has no policy block"
    for key in ("display_name", "short_description", "default_prompt"):
        assert isinstance(interface.get(key), str) and interface[key].strip(), (
            f"{name}: interface.{key} is missing or empty"
        )
    assert f"${name}" in interface["default_prompt"], (
        f"{name}: default_prompt must name the skill as ${name}"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_only_user_entrypoints_disable_implicit_invocation(name):
    allowed = load_openai(name)["policy"].get("allow_implicit_invocation")
    expected = name not in ENTRYPOINTS
    assert allowed is expected, (
        f"{name}: policy.allow_implicit_invocation is {allowed!r}, expected "
        f"{expected!r}; {ENTRYPOINT_HINT}"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_display_name_marks_entrypoints_and_lifecycle_skills(name):
    display = load_openai(name)["interface"]["display_name"]
    if name in DISPLAY_NAME_EXCEPTIONS:
        assert display == DISPLAY_NAME_EXCEPTIONS[name], (
            f"{name}: display_name must stay {DISPLAY_NAME_EXCEPTIONS[name]!r}"
        )
    elif name in ENTRYPOINTS:
        assert display.startswith(ENTRYPOINT_PREFIX) and not display.startswith(
            LIFECYCLE_PREFIX
        ), f"{name}: a user entrypoint is named {ENTRYPOINT_PREFIX!r}..., not Internal"
    else:
        assert display.startswith(LIFECYCLE_PREFIX), (
            f"{name}: a lifecycle skill's display_name starts {LIFECYCLE_PREFIX!r}"
        )
