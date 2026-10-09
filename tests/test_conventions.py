import re
import warnings

import pytest

from helpers import (
    ROOT,
    SKILL_NAMES,
    read_text,
    rel,
    repo_files,
    repo_files_matching,
)

# Covers every text file the repo authors, not only markdown. The suffix list is
# the set of text formats present here; an en dash in a skill's openai.yaml or in
# this directory's own Python is as much a convention break as one in a document.
# The set is Git's view of the repo (see helpers.repo_files), so a host skills
# directory installed into this checkout never makes the suite fail on text this
# repo did not author and cannot fix.
TEXT_SUFFIXES = (".md", ".yaml", ".yml", ".txt", ".py", ".ini", ".sh")
# Built from code points so this file does not contain the characters it bans.
TYPOGRAPHIC_DASH = re.compile(f"[{chr(0x2013)}{chr(0x2014)}]")


def test_no_typographic_dashes():
    offenders = []
    for path in repo_files_matching(*TEXT_SUFFIXES):
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            if TYPOGRAPHIC_DASH.search(line):
                offenders.append(f"{rel(path)}:{number}")
    assert offenders == [], (
        f"use the ASCII hyphen, not an en dash or em dash: {', '.join(offenders)}"
    )


# A skill may rely only on its own folder: `npx skills add --skill <name>`
# installs one folder and nothing else travels with it. Naming a sibling skill to
# route a reader to it holds whether or not the sibling is installed; requiring a
# sibling's content does not. So the test bans the ways a prerequisite can be
# written - a path out of the folder, a path into another skill's folder, or an
# instruction to read a sibling - and leaves bare names alone.
def skill_files(name):
    folder = ROOT / name
    return [
        path
        for path in repo_files()
        if folder in path.parents and path.suffix in (".md", ".yaml")
    ]


def sibling_dependencies(name):
    found = []
    for path in skill_files(name):
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            if "../" in line or "..\\" in line:
                found.append((path, number, "a path out of the skill folder"))
            for other in re.findall(
                r"baselinedocs-[a-z-]+(?=/(?:references|agents|SKILL\.md))", line
            ):
                if other != name:
                    found.append((path, number, f"a path into {other}"))
            if re.search(r"\b[Rr]ead\s+(?:the\s+)?`baselinedocs-[a-z-]+`", line):
                found.append((path, number, "an instruction to read a sibling skill"))
    return found


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_skill_depends_on_no_sibling(name):
    found = sibling_dependencies(name)
    assert found == [], (
        f"{name} must run with only its own folder installed; "
        + "; ".join(f"{rel(path)}:{number} has {why}" for path, number, why in found)
    )


# Folder shape from AGENTS.md: SKILL.md, agents/openai.yaml, references/ only
# when needed, and scripts/packtool.sh as the one script. A stray file here ships
# to everyone who installs the skill. The one exception is a script a single skill
# owns outright and no other skill ships, named here so a second one is a decision.
OWN_SCRIPTS = {"baselinedocs-self-upgrade": "scripts/upgradekit.sh"}


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_skill_folder_has_only_the_shipped_shape(name):
    folder = ROOT / name
    relative = {
        path.relative_to(folder).as_posix()
        for path in repo_files()
        if folder in path.parents
    }
    assert "SKILL.md" in relative and "agents/openai.yaml" in relative, (
        f"{name} needs SKILL.md and agents/openai.yaml"
    )
    strays = sorted(
        item
        for item in relative
        if item
        not in (
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/packtool.sh",
            OWN_SCRIPTS.get(name),
        )
        and not (item.startswith("references/") and item.count("/") == 1)
    )
    assert strays == [], f"{name} ships files outside the folder shape: {strays}"


# Never hard-wrap a paragraph: one paragraph is one line. A hard wrap leaves two
# or more consecutive plain lines, which Markdown renders as one paragraph, so any
# such run is a candidate. Tables, lists, headings, quotes, fences, indented lines
# and frontmatter are not paragraphs. Warns rather than fails: a heuristic cannot
# tell a deliberate line break from a wrap, and a false failure would teach the
# suite to be ignored.
UNWRAPPED_SKIP = ("example/",)
BLOCK_START = re.compile(r"^(\s|#|\||>|[-*+]\s|\d+[.)]\s|<|```|---|===)")


def wrapped_runs(text):
    lines = text.splitlines()
    start = 0
    if lines and lines[0] == "---":
        start = next((i + 1 for i, line in enumerate(lines[1:], 1) if line == "---"), 0)
    runs, current, fenced = [], [], False
    for number, line in enumerate(lines[start:], start=start + 1):
        if line.startswith("```"):
            fenced = not fenced
        plain = bool(line.strip()) and not fenced and not BLOCK_START.match(line)
        if plain:
            current.append(number)
            continue
        if len(current) > 1:
            runs.append(current[0])
        current = []
    if len(current) > 1:
        runs.append(current[0])
    return runs


def test_paragraphs_are_not_hard_wrapped():
    findings = []
    for path in repo_files_matching(".md"):
        if rel(path).startswith(UNWRAPPED_SKIP):
            continue
        findings += [f"{rel(path)}:{line}" for line in wrapped_runs(read_text(path))]
    if findings:
        warnings.warn(
            f"{len(findings)} possible hard-wrapped paragraph(s), first lines: "
            + ", ".join(findings[:20]),
            stacklevel=1,
        )
