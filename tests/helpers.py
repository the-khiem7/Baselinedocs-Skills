import re
import subprocess
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def skill_dirs():
    return sorted(path for path in ROOT.glob("baselinedocs-*") if path.is_dir())


SKILL_NAMES = [path.name for path in skill_dirs()]


def commit_skill_dirs():
    """The `commit-*` skills. They are not in the baselinedocs family, so `skill_dirs()`
    never sees them and no family test covers them: `tests/test_commit_skills.py` does."""
    return sorted(path for path in ROOT.glob("commit-*") if path.is_dir())


COMMIT_SKILL_NAMES = [path.name for path in commit_skill_dirs()]


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def read_skill(name):
    return read_text(ROOT / name / "SKILL.md")


def split_frontmatter(text):
    """Return (frontmatter dict, body). Only the first `---` block counts."""
    match = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?", text, re.DOTALL)
    if match is None:
        return None, text
    return yaml.safe_load(match.group(1)), text[match.end():]


@lru_cache(maxsize=1)
def repo_files():
    """Files Git knows or would add: tracked plus untracked-not-ignored.

    Asking Git rather than walking the disk keeps a host skills directory
    installed into this checkout, a tool cache, or a nested worktree out of every
    convention test: those are not repo content and this repo cannot fix them.
    """
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    paths = {ROOT / name for name in listed.split("\0") if name}
    return sorted(path for path in paths if path.is_file())


def repo_files_matching(*suffixes):
    return [path for path in repo_files() if path.suffix in suffixes]


def rel(path):
    return Path(path).relative_to(ROOT).as_posix()
