import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "hooks" / "checkpoint.py"
PROMPT = ROOT / "hooks" / "prompts" / "checkpoint.md"


class CheckpointTests(unittest.TestCase):
    def run_hook(self, agent, payload, *extra_args, script=SCRIPT):
        input_text = payload if isinstance(payload, str) else json.dumps(payload)
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agent",
                agent,
                "--event",
                "Stop",
                *extra_args,
            ],
            input=input_text,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_normal_stop_emits_prompt_for_each_host(self):
        prompt = PROMPT.read_text(encoding="utf-8").strip()
        for agent in ("codex", "claude"):
            with self.subTest(agent=agent):
                self.assertEqual(
                    {"decision": "block", "reason": prompt},
                    self.run_hook(agent, {"hook_event_name": "Stop"}),
                )
        self.assertEqual(
            {"followup_message": prompt},
            self.run_hook("cursor", {"hook_event_name": "stop"}),
        )

    def test_loop_markers_prevent_another_continuation(self):
        cases = (
            ("codex", {"hook_event_name": "Stop", "stop_hook_active": True}),
            ("claude", {"hook_event_name": "Stop", "stop_hook_active": True}),
            ("cursor", {"hook_event_name": "stop", "loop_count": 1}),
        )
        for agent, payload in cases:
            with self.subTest(agent=agent):
                self.assertEqual({}, self.run_hook(agent, payload))

    def test_invalid_or_incomplete_payload_fails_safely(self):
        for payload in ("{ invalid", "[]", "{}"):
            with self.subTest(payload=payload):
                self.assertEqual({}, self.run_hook("codex", payload))

    def test_missing_prompt_fails_safely(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "checkpoint.py"
            script.write_bytes(SCRIPT.read_bytes())
            self.assertEqual(
                {},
                self.run_hook(
                    "codex",
                    {"hook_event_name": "Stop"},
                    script=script,
                ),
            )

    def test_deprecated_strict_flag_is_a_no_op(self):
        payload = {"hook_event_name": "Stop"}
        self.assertEqual(
            self.run_hook("codex", payload),
            self.run_hook("codex", payload, "--strict"),
        )

    def test_prompt_enforces_thread_boundaries(self):
        prompt = PROMPT.read_text(encoding="utf-8")
        for phrase in (
            "current thread",
            "Do not search the repository for active roadmaps",
            "more than one pack is plausible",
            "finish without modifying files",
            "Do not infer ownership from global Git status",
            "Do not commit",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, prompt)

    def test_adapter_has_no_repository_detection_logic(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for forbidden in (
            "subprocess",
            "rglob",
            "st_mtime",
            "active_roadmaps",
            "changed_paths",
            "needs_checkpoint",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
