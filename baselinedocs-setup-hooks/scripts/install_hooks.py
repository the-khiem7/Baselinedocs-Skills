#!/usr/bin/env python3
"""Install the Baseline Docs checkpoint hook without replacing host config."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any


CONFIG_PATHS = {
    "codex": Path(".codex/hooks.json"),
    "claude": Path(".claude/settings.json"),
    "cursor": Path(".cursor/hooks.json"),
}


def handler_for(agent: str) -> tuple[str, dict[str, Any]]:
    if agent == "codex":
        return (
            "Stop",
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": 'python "$(git rev-parse --show-toplevel)/.baseline/hooks/checkpoint.py" --agent codex --event Stop',
                        "commandWindows": (
                            'powershell.exe -NoProfile -Command "$root = git rev-parse '
                            "--show-toplevel; python (Join-Path $root "
                            "'.baseline/hooks/checkpoint.py') --agent codex --event Stop\""
                        ),
                        "statusMessage": "Checking Baseline Docs checkpoint",
                        "timeout": 10,
                    }
                ]
            },
        )
    if agent == "claude":
        return (
            "Stop",
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python .baseline/hooks/checkpoint.py --agent claude --event Stop",
                        "timeout": 10,
                    }
                ]
            },
        )
    return (
        "stop",
        {
            "command": "python .baseline/hooks/checkpoint.py --agent cursor --event stop"
        },
    )


def contains_handler(value: Any, agent: str) -> bool:
    if isinstance(value, str):
        return ".baseline/hooks/checkpoint.py" in value and f"--agent {agent}" in value
    if isinstance(value, dict):
        return any(contains_handler(item, agent) for item in value.values())
    if isinstance(value, list):
        return any(contains_handler(item, agent) for item in value)
    return False


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def merge_handler(config: dict[str, Any], agent: str) -> bool:
    if contains_handler(config, agent):
        return False

    if agent == "cursor":
        config.setdefault("version", 1)
    elif agent == "codex":
        config.setdefault("description", "Advisory Baseline Docs phase checkpoint.")

    hooks = config.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("Existing 'hooks' value must be a JSON object")

    event, handler = handler_for(agent)
    entries = hooks.setdefault(event, [])
    if not isinstance(entries, list):
        raise ValueError(f"Existing hooks.{event} value must be a JSON array")
    entries.append(handler)
    return True


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def install(agent: str, repo: Path, dry_run: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f"Repository directory does not exist: {repo}")

    skill_root = Path(__file__).parents[1]
    asset_pairs = (
        (
            skill_root / "assets" / "checkpoint.py",
            repo / ".baseline" / "hooks" / "checkpoint.py",
        ),
        (
            skill_root / "assets" / "prompts" / "checkpoint.md",
            repo / ".baseline" / "hooks" / "prompts" / "checkpoint.md",
        ),
    )
    config_path = repo / CONFIG_PATHS[agent]

    asset_contents = [(target, source.read_bytes()) for source, target in asset_pairs]
    config = load_config(config_path)
    config_changed = merge_handler(config, agent)
    asset_changes = [
        (target, not target.exists() or target.read_bytes() != content, content)
        for target, content in asset_contents
    ]

    changes: list[str] = []
    unchanged: list[str] = []
    for path, changed, _ in asset_changes:
        (changes if changed else unchanged).append(str(path.relative_to(repo)))
    (changes if config_changed else unchanged).append(str(config_path.relative_to(repo)))

    if not dry_run:
        for target, changed, content in asset_changes:
            if changed:
                atomic_write_bytes(target, content)
        if config_changed:
            atomic_write(config_path, json.dumps(config, indent=2) + "\n")

    return {
        "agent": agent,
        "repo": str(repo),
        "dry_run": dry_run,
        "changes": changes,
        "unchanged": unchanged,
        "trust_review_required": agent == "codex",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=tuple(CONFIG_PATHS), required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        result = install(args.agent, args.repo, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
