#!/usr/bin/env python3
"""Advisory Baseline Docs checkpoint hook for Codex, Claude Code, and Cursor."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


DOC_PARTS = (".introduction.md", ".roadmap.md", ".hallucination.md", ".sourcecode.md", ".useguide.md", ".index.md")


def run_git(cwd: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def is_baseline_doc(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    return "/docs/wiki/" in f"/{normalized}" or any(normalized.endswith(part) for part in DOC_PARTS)


def active_roadmaps(cwd: Path) -> list[Path]:
    roadmaps: list[Path] = []
    for path in cwd.rglob("*.roadmap.md"):
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:2000].lower()
        except OSError:
            continue
        if "status: \"active\"" in head or "status: active" in head:
            roadmaps.append(path)
    return roadmaps


def changed_paths(cwd: Path) -> list[str]:
    paths: list[str] = []
    for line in run_git(cwd, "status", "--porcelain", "--untracked-files=all"):
        value = line[3:] if len(line) > 3 else ""
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        if value:
            paths.append(value.strip('"'))
    return paths


def needs_checkpoint(cwd: Path, roadmaps: list[Path]) -> bool:
    changed = changed_paths(cwd)
    implementation = [path for path in changed if not is_baseline_doc(path)]
    if not implementation:
        return False

    doc_times = [path.stat().st_mtime for path in roadmaps if path.exists()]
    implementation_times: list[float] = []
    for relative in implementation:
        path = cwd / relative
        if path.exists():
            implementation_times.append(path.stat().st_mtime)

    if not implementation_times:
        return True
    if not doc_times:
        return True
    return max(implementation_times) > max(doc_times)


def checkpoint_message(roadmaps: list[Path], cwd: Path) -> str:
    names = ", ".join(str(path.relative_to(cwd)) for path in roadmaps[:3])
    return (
        "Baseline Docs checkpoint required before stopping. "
        f"Update the active roadmap ({names}) with the current phase status, final evidence, "
        "changed files, open risks, exact next action, and refreshed frontmatter. "
        "Record outcomes rather than every failed attempt."
    )


def emit(agent: str, event: str, message: str, strict: bool) -> None:
    if agent == "cursor":
        print(json.dumps({"followup_message": message}))
        return

    if strict:
        print(json.dumps({"decision": "block", "reason": message}))
        return

    if event.lower() == "stop":
        print(json.dumps({"decision": "block", "reason": message}))
        return

    print(json.dumps({"systemMessage": message}))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=("codex", "claude", "cursor"), required=True)
    parser.add_argument("--event", default="Stop")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}

    if payload.get("stop_hook_active") or int(payload.get("loop_count", 0) or 0) > 0:
        print("{}")
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd()).resolve()
    roadmaps = active_roadmaps(cwd)
    if not roadmaps or not needs_checkpoint(cwd, roadmaps):
        print("{}")
        return 0

    emit(args.agent, args.event, checkpoint_message(roadmaps, cwd), args.strict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
