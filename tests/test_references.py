import re

import pytest

from helpers import ROOT, SKILL_NAMES, read_skill, read_text, rel

CORE = ROOT / "baseline-core"
CORE_ASSETS = [
    "references/pack-contract.md",
    "references/report-style.md",
    "scripts/packtool.sh",
]
CORE_SENTENCE = (
    "`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md "
    "sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the "
    "user to install `baseline-core`; never write or report on a pack from memory instead."
)

# Report style is gated in every skill that names a pack element in its output.
# `baselinedocs-load` is exempt because it operates silently and outputs only a single
# confirmation word ("Sẵn sàng." / "Ready.") with no pack elements cited.
REPORT_STYLE_EXEMPT = {
    "baselinedocs-load",
}

REPORT_GATE = (
    "Read `<core-dir>/references/report-style.md` in full before reporting to the user, "
    "every time."
)

# Every skill that writes into a pack gates on the contract, which lives once in
# `baseline-core`. The gate fails closed when that folder is missing, so a skill
# installed without it stops instead of writing from memory.
WRITER_SKILLS = {
    "baselinedocs-init",
    "baselinedocs-adopt",
    "baselinedocs-save",
    "baselinedocs-run",
    "baselinedocs-sync-codebase",
    "baselinedocs-sync-decisions",
    "baselinedocs-sync-reconcile",
    "baselinedocs-maintain-compact",
    "baselinedocs-maintain-split",
    "baselinedocs-extract-wiki",
    "baselinedocs-callout",
}

# A skill that writes nothing still needs the role list to report content sitting
# in a document whose role does not cover it. The qualifier is a full read, not
# the absence of writes: a skill that reads part of a pack and owns the role list
# would report conformance it never checked, which is worse than not reporting it.
# `baselinedocs-brief` reads no document in full, and neither `audit` skill
# compares placement, so none of them gate on it.
READER_SKILLS = {
    "baselinedocs-onboard",
}

# A silent loader reads the pack in full and holds the contract to understand
# baseline document roles and schemas, but produces no explanatory report.
LOADER_SKILLS = {
    "baselinedocs-load",
}

RECALL_SKILLS = {
    "baselinedocs-recall",
}

CONTRACT_SKILLS = WRITER_SKILLS | READER_SKILLS | LOADER_SKILLS | RECALL_SKILLS

# One gate per skill, worded for what that skill does with the contract. Both are
# pinned: an unpinned second wording is how the family ends up with two
# definitions of when the file must be read.
WRITE_GATE = (
    "Read `<core-dir>/references/pack-contract.md` in full before creating or editing any pack "
    "file, every time."
)
READ_GATE = (
    "Read `<core-dir>/references/pack-contract.md` in full before reporting the pack state, "
    "every time."
)
LOAD_GATE = (
    "Read `<core-dir>/references/pack-contract.md` in full before loading a pack, "
    "every time."
)
RECALL_CONTRACT_GATE = "Read `<core-dir>/references/pack-contract.md` in full now, every time."
GATES = {name: WRITE_GATE for name in WRITER_SKILLS}
GATES.update({name: READ_GATE for name in READER_SKILLS})
GATES.update({name: LOAD_GATE for name in LOADER_SKILLS})
GATES.update({name: RECALL_CONTRACT_GATE for name in RECALL_SKILLS})

# `baseline-core/scripts/packtool.sh` checks pack structure mechanically:
# duplicate identifiers, index rows against entry headings, entries filed under
# the wrong section. A writer runs it after every write, because the failures it
# catches report success when made; a full reader or an audit runs it before
# reporting, so the report rests on a check rather than on a read.
TOOL_SKILLS = WRITER_SKILLS | READER_SKILLS | {
    "baselinedocs-audit-claims",
    "baselinedocs-audit-drift",
}
TOOL_WRITE_GATE = (
    "Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` after every pack write "
    "and before reporting it, and allocate every new identifier with "
    "`sh <core-dir>/scripts/packtool.sh next-id <pack-dir> <D|Q|P> [PREFIX]`, never "
    "from memory. A new pack's first identifier needs its PREFIX."
)
TOOL_REPORT_GATE = (
    "Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` before reporting the "
    "pack state, and report its FAIL and WARN lines as findings; it reports, it never "
    "fixes."
)
CLOSE_PLAN_SKILLS = {"baselinedocs-sync-decisions", "baselinedocs-save"}
TOOL_GATES = {name: TOOL_WRITE_GATE for name in WRITER_SKILLS}
TOOL_GATES.update({name: TOOL_REPORT_GATE for name in TOOL_SKILLS - WRITER_SKILLS})

RECALL_REPORT_GATE = "Read `<core-dir>/references/report-style.md` in full now, every time."
REPORT_GATES = {name: RECALL_REPORT_GATE for name in RECALL_SKILLS}

REPORTERS = [name for name in SKILL_NAMES if name not in REPORT_STYLE_EXEMPT]
READ_ONLY_SKILLS = sorted(READER_SKILLS | LOADER_SKILLS | RECALL_SKILLS)

@pytest.mark.parametrize("asset", CORE_ASSETS)
def test_baseline_core_holds_the_shared_asset(asset):
    assert (CORE / asset).is_file(), f"baseline-core/{asset} is missing"


# `baseline-academic-core` holds the lesson rules the academic skills read. It is a
# second core, kept apart from `baseline-core` so a pack-writing skill never loads
# rules only a lesson needs.
ACADEMIC_CORE = ROOT / "baseline-academic-core"
ACADEMIC_ASSETS = ["references/academic-contract.md"]


@pytest.mark.parametrize("asset", ACADEMIC_ASSETS)
def test_baseline_academic_core_holds_the_lesson_asset(asset):
    assert (ACADEMIC_CORE / asset).is_file(), f"baseline-academic-core/{asset} is missing"


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_no_skill_ships_a_copy_of_an_academic_core_asset(name):
    copies = [asset for asset in ACADEMIC_ASSETS if (ROOT / name / asset).exists()]
    assert copies == [], (
        f"{name} ships {copies}; the only copy lives in baseline-academic-core"
    )


def test_baseline_academic_core_ships_no_core_asset_of_baseline_core():
    copies = [asset for asset in CORE_ASSETS if (ACADEMIC_CORE / asset).exists()]
    assert copies == [], (
        f"baseline-academic-core ships {copies}; those live only in baseline-core"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_no_skill_ships_a_copy_of_a_core_asset(name):
    copies = [asset for asset in CORE_ASSETS if (ROOT / name / asset).exists()]
    assert copies == [], (
        f"{name} ships {copies}; the only copy lives in baseline-core (BLD-D54)"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_every_skill_defines_core_dir_and_fails_closed(name):
    assert CORE_SENTENCE in read_skill(name), (
        f"{name} reads baseline-core but never defines <core-dir> and stops without it"
    )


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_no_skill_points_at_a_local_copy_of_a_core_asset(name):
    text = read_skill(name)
    for stale in (
        "`references/pack-contract.md`",
        "`references/report-style.md`",
        "<skill-dir>/scripts/packtool.sh",
    ):
        assert stale not in text, f"{name} still points at {stale}, which no longer ships"


@pytest.mark.parametrize("name", sorted(CONTRACT_SKILLS))
def test_contract_skills_gate_on_reading_the_contract(name):
    assert GATES[name] in read_skill(name), (
        f"{name} is classified as reading the contract but never requires reading it"
    )


@pytest.mark.parametrize("name", sorted(TOOL_SKILLS))
def test_tool_skills_gate_on_running_the_check(name):
    assert TOOL_GATES[name] in read_skill(name), (
        f"{name} is classified as running packtool.sh but never requires running it"
    )


@pytest.mark.parametrize("name", sorted(CLOSE_PLAN_SKILLS))
def test_skills_that_close_questions_run_close_plan(name):
    assert "packtool.sh close-plan <pack-dir> <Q-ID> <D-ID>" in read_skill(name), (
        f"{name} closes questions but never routes the closing edits through close-plan"
    )


def test_no_skill_calls_the_tool_from_the_current_directory():
    for name in sorted(TOOL_SKILLS):
        assert "`sh scripts/packtool.sh" not in read_skill(name), (
            f"{name} writes a cwd-relative tool path; the host does not run from the skill folder"
        )


@pytest.mark.parametrize("name", REPORTERS)
def test_every_reporter_gates_on_report_style(name):
    assert REPORT_GATES.get(name, REPORT_GATE) in read_skill(name), (
        f"{name} reports to the user but never requires reading the report style"
    )


@pytest.mark.parametrize("name", READ_ONLY_SKILLS)
def test_read_only_skills_are_not_gated_on_writing(name):
    assert WRITE_GATE not in read_skill(name), (
        f"{name} writes no pack file, so the write gate can never fire in it"
    )


# The count of pack-writing skills is stated in prose in AGENTS.md, and prose
# is not re-derived when CONTRACT_SKILLS changes. It went stale twice: it read
# 14 when the real figure was 13, and a later pass corrected two of the four
# mentions because it searched for the sentence it remembered instead of for
# the number. The cure is one statement, pinned. Keep the count in the
# `The N pack-writing skills` sentence only; say "every pack-writing skill"
# everywhere else, so there is nothing else to update and nothing to disagree.
# That count is `WRITER_SKILLS`, not `CONTRACT_SKILLS`: since a full reader also
# ships the contract, the two differ, and pinning the prose to the wrong one
# would make AGENTS.md call a read-only skill a pack-writing skill.
def test_agents_md_states_the_skill_count_once_and_correctly():
    text = read_text(ROOT / "AGENTS.md")
    stated = re.findall(r"The (\d+) pack-writing skills", text)
    assert len(stated) == 1, (
        "state the pack-writing skill count in exactly one sentence in AGENTS.md"
    )
    assert int(stated[0]) == len(WRITER_SKILLS), (
        "AGENTS.md disagrees with WRITER_SKILLS about how many skills write into a pack"
    )
    strays = re.findall(r"\ball (\d+)\b|\bEach of the (\d+)\b", text)
    assert strays == [], (
        "phrase these count-free: the count belongs in one sentence, checked above"
    )


# `baselinedocs-help` ships its own guide because the README does not ship. A
# skill added without a row would be invisible to anyone asking which skill to use.
@pytest.mark.parametrize("name", SKILL_NAMES)
def test_help_guide_names_every_skill(name):
    guide = read_text(ROOT / "baselinedocs-help" / "references" / "guide.md")
    assert f"`{name}`" in guide, (
        f"baselinedocs-help/references/guide.md has no row for {name}; add one"
    )


# `baselinedocs-adr` ships the AWS template unmodified, so its headings are the
# AWS ones. A pointer into a pack would leave the repository inside a promoted ADR.
ADR_HEADINGS = [
    "# ADR-NNNN: <Title>",
    "## Status",
    "## Date",
    "## Context",
    "## Decision",
    "## Consequences",
    "## Compliance",
    "## Notes",
]


def test_adr_template_carries_the_aws_headings_and_no_pack_pointer():
    template = read_text(ROOT / "baselinedocs-adr" / "references" / "template.md")
    missing = [heading for heading in ADR_HEADINGS if heading not in template]
    assert missing == [], f"baselinedocs-adr template is missing {missing}"
    assert "docs/baseline" not in template, "the ADR template must not point into a pack"
