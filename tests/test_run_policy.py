import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class RunPolicyContractTests(unittest.TestCase):
    def test_every_ambiguous_invocation_requires_policy_questions(self):
        skill = (ROOT / "baselinedocs-run" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Apply this gate to every invocation style.", skill)
        self.assertIn("is only one example", skill)
        self.assertIn("missing or ambiguous", skill)
        self.assertIn("Do not silently apply defaults", skill)
        self.assertIn("Ask in the user's language", skill)
        self.assertIn("Do not expose internal policy identifiers", skill)

    def test_execution_contract_has_no_silent_defaults(self):
        contract = (
            ROOT / "baselinedocs-run" / "references" / "execution-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("For every invocation style", contract)
        self.assertIn("does not clearly determine one or both choices", contract)
        self.assertNotIn("This is the default.", contract)


if __name__ == "__main__":
    unittest.main()
