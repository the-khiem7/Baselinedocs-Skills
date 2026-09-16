import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CANONICAL_CONTRACT = ROOT / "contract" / "pack-contract.md"
CANONICAL_REPORT_STYLE = ROOT / "contract" / "report-style.md"

# Report style ships to every skill that names a pack element in its output, which
# is now every skill in the family. It is a separate asset from the contract on
# purpose: the contract's audience is skills that write or fully read a pack, and
# `brief` is a conversational skill that must not carry the role list (see D16),
# yet it cites element identifiers in every report it produces. Folding the two
# would force the wrong audience on one of them.
REPORT_STYLE_EXEMPT = set()

REPORT_GATE = (
    "Read `references/report-style.md` in full before reporting to the user, "
    "every time."
)

# Every skill that writes into a pack ships the contract, because skills install
# one folder at a time and cannot reach a sibling skill's files. The copies are
# packaged assets of one canonical file, and they are pinned for the same reason:
# a drifted copy reaches whoever installed that one skill, and nothing in their
# install says it is stale.
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
# compares placement, so none of them carry a copy.
READER_SKILLS = {
    "baselinedocs-onboard",
}

CONTRACT_SKILLS = WRITER_SKILLS | READER_SKILLS

# One gate per skill, worded for what that skill does with the contract. Both are
# pinned: an unpinned second wording is how the family ends up with two
# definitions of when the file must be read.
WRITE_GATE = (
    "Read `references/pack-contract.md` in full before creating or editing any pack "
    "file, every time."
)
READ_GATE = (
    "Read `references/pack-contract.md` in full before reporting the pack state, "
    "every time."
)
GATES = {name: WRITE_GATE for name in WRITER_SKILLS}
GATES.update({name: READ_GATE for name in READER_SKILLS})


class ContractCopyTests(unittest.TestCase):
    def test_packaged_contract_matches_canonical_contract(self):
        canonical = CANONICAL_CONTRACT.read_bytes()
        packaged = sorted(ROOT.glob("baselinedocs-*/references/pack-contract.md"))
        self.assertEqual(
            {path.parents[1].name for path in packaged}, CONTRACT_SKILLS
        )
        for path in packaged:
            self.assertEqual(
                path.read_bytes(),
                canonical,
                f"{path.relative_to(ROOT)} drifted from contract/pack-contract.md",
            )

    def test_contract_skills_gate_on_reading_the_contract(self):
        for name in sorted(CONTRACT_SKILLS):
            with self.subTest(skill=name):
                text = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(
                    GATES[name],
                    text,
                    f"{name} ships the contract but never requires reading it",
                )

    def test_packaged_report_style_matches_canonical_and_reaches_every_reporter(self):
        canonical = CANONICAL_REPORT_STYLE.read_bytes()
        expected = {
            path.name for path in ROOT.glob("baselinedocs-*") if path.is_dir()
        } - REPORT_STYLE_EXEMPT
        packaged = sorted(ROOT.glob("baselinedocs-*/references/report-style.md"))
        self.assertEqual({path.parents[1].name for path in packaged}, expected)
        for path in packaged:
            with self.subTest(copy=path.parents[1].name):
                self.assertEqual(
                    path.read_bytes(),
                    canonical,
                    f"{path.relative_to(ROOT)} drifted from contract/report-style.md",
                )

    def test_every_reporter_gates_on_report_style(self):
        for name in sorted(
            {path.name for path in ROOT.glob("baselinedocs-*") if path.is_dir()}
            - REPORT_STYLE_EXEMPT
        ):
            with self.subTest(skill=name):
                text = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(
                    REPORT_GATE,
                    text,
                    f"{name} ships report style but never requires reading it",
                )

    def test_read_only_skills_are_not_gated_on_writing(self):
        for name in sorted(READER_SKILLS):
            with self.subTest(skill=name):
                text = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn(
                    WRITE_GATE,
                    text,
                    f"{name} writes no pack file, so the write gate can never fire in it",
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
    def test_agents_md_states_the_skill_count_once_and_correctly(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        stated = re.findall(r"The (\d+) pack-writing skills", text)
        self.assertEqual(
            len(stated),
            1,
            "state the pack-writing skill count in exactly one sentence in AGENTS.md",
        )
        self.assertEqual(
            int(stated[0]),
            len(WRITER_SKILLS),
            "AGENTS.md disagrees with WRITER_SKILLS about how many skills write into a pack",
        )
        strays = re.findall(r"\ball (\d+)\b|\bEach of the (\d+)\b", text)
        self.assertEqual(
            strays,
            [],
            "phrase these count-free: the count belongs in one sentence, checked above",
        )

    # Scoped to this repository's own markdown. A dot-directory under the root is
    # never repo content: it is `.git`, a tool cache, or a host skills directory
    # someone installed into this checkout, and `.gitignore` already excludes those.
    # Sweeping them makes a convention test fail on text this repo did not author
    # and cannot fix, which is how a green suite turns into a permanently red one.
    def test_no_typographic_dashes(self):
        offenders = []
        for path in sorted(ROOT.rglob("*.md")):
            if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if re.search("[–—]", line):
                    offenders.append(f"{path.relative_to(ROOT)}:{number}")
        self.assertEqual(offenders, [], "use the ASCII hyphen, not an en dash or em dash")


if __name__ == "__main__":
    unittest.main()
