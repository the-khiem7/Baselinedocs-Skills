import re

import pytest

from helpers import ROOT, SKILL_NAMES, read_skill, read_text, split_frontmatter

# The Agent Skills format bounds these; a host may truncate or reject beyond them.
MAX_NAME = 64
MAX_DESCRIPTION = 1024

# The core skills double as rule loaders an agent selects on its own and a user
# calls by name; each carries the family version so the release can stamp it.
CORE_SKILLS = ("baseline-core", "baseline-academic-core")


@pytest.mark.parametrize("name", CORE_SKILLS)
def test_core_skills_are_selectable_rule_loaders(name):
    frontmatter, _ = split_frontmatter(read_text(ROOT / name / "SKILL.md"))
    assert frontmatter.get("name") == name
    assert re.fullmatch(r"\d+\.\d+\.\d+", frontmatter.get("version", "")), (
        f"{name}/SKILL.md carries no family version, so the release cannot stamp it"
    )
    assert len(frontmatter.get("description", "")) <= MAX_DESCRIPTION


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
