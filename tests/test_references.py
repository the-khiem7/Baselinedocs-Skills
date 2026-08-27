import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CANONICAL_CONTRACT = ROOT / "contract" / "pack-contract.md"

# Every skill that writes into a pack ships the contract, because skills install
# one folder at a time and cannot reach a sibling skill's files. The copies are
# packaged assets of one canonical file, the same arrangement `hooks/checkpoint.py`
# already uses, and they are pinned for the same reason: a drifted copy reaches
# whoever installed that one skill, and nothing in their install says it is stale.
CONTRACT_SKILLS = {
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
}

GATE = (
    "Read `references/pack-contract.md` in full before creating or editing any pack "
    "file, every time."
)


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
            text = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(
                GATE, text, f"{name} ships the contract but never requires reading it"
            )

    # The count of pack-writing skills is stated in prose in AGENTS.md, and prose
    # is not re-derived when CONTRACT_SKILLS changes. It went stale twice: it read
    # 14 when the real figure was 13, and a later pass corrected two of the four
    # mentions because it searched for the sentence it remembered instead of for
    # the number. The cure is one statement, pinned. Keep the count in the
    # `The N pack-writing skills` sentence only; say "every pack-writing skill"
    # everywhere else, so there is nothing else to update and nothing to disagree.
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
            len(CONTRACT_SKILLS),
            "AGENTS.md disagrees with CONTRACT_SKILLS about how many skills ship the contract",
        )
        strays = re.findall(r"\ball (\d+)\b|\bEach of the (\d+)\b", text)
        self.assertEqual(
            strays,
            [],
            "phrase these count-free: the count belongs in one sentence, checked above",
        )

    def test_no_typographic_dashes(self):
        offenders = []
        for path in sorted(ROOT.rglob("*.md")):
            if any(part in {".git", ".pytest_cache"} for part in path.parts):
                continue
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if re.search("[–—]", line):
                    offenders.append(f"{path.relative_to(ROOT)}:{number}")
        self.assertEqual(offenders, [], "use the ASCII hyphen, not an en dash or em dash")


if __name__ == "__main__":
    unittest.main()
