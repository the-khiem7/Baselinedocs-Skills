import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class RunPolicyContractTests(unittest.TestCase):
    def test_minimal_invocation_requires_both_policy_choices(self):
        skill = (ROOT / "baselinedocs-run" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            'For a minimal invocation such as `$baselinedocs-run @docpack`, ask for both policies.',
            skill,
        )
        self.assertIn("Do not silently apply defaults", skill)

    def test_execution_contract_has_no_silent_defaults(self):
        contract = (
            ROOT / "baselinedocs-run" / "references" / "execution-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Both policies must be selected before implementation begins.", contract)
        self.assertNotIn("This is the default.", contract)


if __name__ == "__main__":
    unittest.main()
