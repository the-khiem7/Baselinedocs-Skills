import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
ENTRYPOINTS = {
    "baselinedocs-init",
    "baselinedocs-save",
    "baselinedocs-run",
    "baselinedocs-setup-hooks",
}


class SkillMetadataTests(unittest.TestCase):
    def skill_dirs(self):
        return sorted(
            path for path in ROOT.glob("baselinedocs-*") if path.is_dir()
        )

    def test_skill_ids_match_folders(self):
        for folder in self.skill_dirs():
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            match = re.search(r"^name:\s*(\S+)$", text, re.MULTILINE)
            self.assertIsNotNone(match, folder.name)
            self.assertEqual(folder.name, match.group(1))
            self.assertNotIn("_", match.group(1))

    def test_openai_prompts_name_the_skill(self):
        for folder in self.skill_dirs():
            text = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"${folder.name}", text)

    def test_only_user_entrypoints_disable_implicit_invocation(self):
        for folder in self.skill_dirs():
            text = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
            expected = "false" if folder.name in ENTRYPOINTS else "true"
            self.assertIn(f"allow_implicit_invocation: {expected}", text)


if __name__ == "__main__":
    unittest.main()
