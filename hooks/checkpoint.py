#!/usr/bin/env python3
"""Prompt-centric Baseline Docs checkpoint hook adapter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROMPT_PATH = Path(__file__).parent / "prompts" / "checkpoint.md"


def load_payload() -> dict[str, Any] | None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def already_continued(payload: dict[str, Any]) -> bool:
    if payload.get("stop_hook_active"):
        return True
    try:
        return int(payload.get("loop_count", 0) or 0) > 0
    except (TypeError, ValueError):
        return True


def load_prompt(path: Path = PROMPT_PATH) -> str | None:
    try:
        prompt = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return prompt or None


def output_for(agent: str, event: str, prompt: str) -> dict[str, Any]:
    if agent == "cursor":
        return {"followup_message": prompt}
    if event.lower() == "stop":
        return {"decision": "block", "reason": prompt}
    return {"systemMessage": prompt}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=("codex", "claude", "cursor"), required=True)
    parser.add_argument("--event", default="Stop")
    parser.add_argument("--strict", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    payload = load_payload()
    if (
        payload is None
        or not isinstance(payload.get("hook_event_name"), str)
        or not payload["hook_event_name"].strip()
        or already_continued(payload)
    ):
        print("{}")
        return 0

    prompt = load_prompt()
    if prompt is None:
        print("{}")
        return 0

    print(json.dumps(output_for(args.agent, args.event, prompt)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
