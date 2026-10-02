import pytest

from helpers import ROOT, read_skill, read_text

SKILL_PHRASES = [
    "Apply this gate to every invocation style.",
    "is only one example",
    "missing or ambiguous",
    "Do not silently apply defaults",
    "Ask in the user's language",
    "Do not expose internal policy identifiers",
]


@pytest.mark.parametrize("phrase", SKILL_PHRASES)
def test_every_ambiguous_invocation_requires_policy_questions(phrase):
    assert phrase in read_skill("baselinedocs-run"), (
        f"baselinedocs-run/SKILL.md lost the policy-gate phrase: {phrase!r}"
    )


def test_execution_contract_has_no_silent_defaults():
    path = ROOT / "baselinedocs-run" / "references" / "execution-contract.md"
    contract = read_text(path)
    assert "For every invocation style" in contract
    assert "does not clearly determine one or both choices" in contract
    assert "This is the default." not in contract, (
        "execution-contract.md must not declare a silent default policy"
    )
