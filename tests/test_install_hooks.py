import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "baselinedocs-setup-hooks" / "scripts" / "install_hooks.py"
SPEC = importlib.util.spec_from_file_location("install_hooks", SCRIPT)
INSTALL_HOOKS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(INSTALL_HOOKS)


class InstallHooksTests(unittest.TestCase):
    def test_packaged_hook_matches_canonical_hook(self):
        canonical = (ROOT / "hooks" / "checkpoint.py").read_bytes()
        packaged = (
            ROOT / "baselinedocs-setup-hooks" / "assets" / "checkpoint.py"
        ).read_bytes()
        self.assertEqual(canonical, packaged)

        canonical_prompt = (
            ROOT / "hooks" / "prompts" / "checkpoint.md"
        ).read_bytes()
        packaged_prompt = (
            ROOT
            / "baselinedocs-setup-hooks"
            / "assets"
            / "prompts"
            / "checkpoint.md"
        ).read_bytes()
        self.assertEqual(canonical_prompt, packaged_prompt)

    def test_installs_each_host_and_is_idempotent(self):
        cases = {
            "codex": Path(".codex/hooks.json"),
            "claude": Path(".claude/settings.json"),
            "cursor": Path(".cursor/hooks.json"),
        }
        for agent, relative_config in cases.items():
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as directory:
                repo = Path(directory)
                result = INSTALL_HOOKS.install(agent, repo)
                self.assertEqual(3, len(result["changes"]))

                config = json.loads((repo / relative_config).read_text(encoding="utf-8"))
                self.assertTrue(INSTALL_HOOKS.contains_handler(config, agent))
                self.assertTrue((repo / ".baseline/hooks/checkpoint.py").exists())
                self.assertTrue(
                    (repo / ".baseline/hooks/prompts/checkpoint.md").exists()
                )

                repeated = INSTALL_HOOKS.install(agent, repo)
                self.assertEqual([], repeated["changes"])
                self.assertEqual(3, len(repeated["unchanged"]))

    def test_preserves_existing_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            path = repo / ".codex/hooks.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "custom": {"keep": True},
                        "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "existing"}]}]},
                    }
                ),
                encoding="utf-8",
            )

            INSTALL_HOOKS.install("codex", repo)
            config = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual({"keep": True}, config["custom"])
            self.assertEqual(2, len(config["hooks"]["Stop"]))

    def test_invalid_json_aborts_without_partial_install(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            path = repo / ".claude/settings.json"
            path.parent.mkdir(parents=True)
            path.write_text("{ invalid", encoding="utf-8")

            with self.assertRaises(ValueError):
                INSTALL_HOOKS.install("claude", repo)
            self.assertFalse((repo / ".baseline/hooks/checkpoint.py").exists())
            self.assertEqual("{ invalid", path.read_text(encoding="utf-8"))

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            result = INSTALL_HOOKS.install("cursor", repo, dry_run=True)
            self.assertEqual(3, len(result["changes"]))
            self.assertFalse((repo / ".baseline").exists())
            self.assertFalse((repo / ".cursor").exists())


if __name__ == "__main__":
    unittest.main()
