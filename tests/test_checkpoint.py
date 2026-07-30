import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "hooks" / "checkpoint.py"
SPEC = importlib.util.spec_from_file_location("checkpoint", SCRIPT)
CHECKPOINT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECKPOINT)


class CheckpointTests(unittest.TestCase):
    def make_repo(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        roadmap = root / "docs" / "baseline" / "sample" / "sample.roadmap.md"
        roadmap.parent.mkdir(parents=True)
        roadmap.write_text(
            '---\nbaseline_schema: "2.0"\nstatus: "active"\n---\n',
            encoding="utf-8",
        )
        return temporary, root, roadmap

    def test_detects_newer_implementation_change(self):
        temporary, root, roadmap = self.make_repo()
        self.addCleanup(temporary.cleanup)
        code = root / "src" / "feature.py"
        code.parent.mkdir()
        code.write_text("enabled = True\n", encoding="utf-8")
        os.utime(roadmap, (100, 100))
        os.utime(code, (200, 200))

        self.assertTrue(CHECKPOINT.needs_checkpoint(root, [roadmap]))

    def test_stays_silent_after_newer_doc_checkpoint(self):
        temporary, root, roadmap = self.make_repo()
        self.addCleanup(temporary.cleanup)
        code = root / "src" / "feature.py"
        code.parent.mkdir()
        code.write_text("enabled = True\n", encoding="utf-8")
        os.utime(code, (100, 100))
        os.utime(roadmap, (200, 200))

        self.assertFalse(CHECKPOINT.needs_checkpoint(root, [roadmap]))

    def test_ignores_inactive_roadmap(self):
        temporary, root, roadmap = self.make_repo()
        self.addCleanup(temporary.cleanup)
        roadmap.write_text('---\nstatus: "complete"\n---\n', encoding="utf-8")

        self.assertEqual([], CHECKPOINT.active_roadmaps(root))


if __name__ == "__main__":
    unittest.main()
