# Phase Checkpoint Hooks

The hook in `hooks/checkpoint.py` is a prompt-centric Stop adapter. On the first Stop event for a turn, it sends the instruction in `hooks/prompts/checkpoint.md` back to the agent so the agent can decide from the current thread whether one clearly identified pack needs a checkpoint.

Python does not search for roadmaps, inspect Git state, compare timestamps, select a pack, or edit documentation.

## Install in a target repository

Install `baselinedocs-setup-hooks`, then ask the agent:

```text
Use $baselinedocs-setup-hooks to install the checkpoint hook for Codex in this repository.
```

The skill detects the repository, copies the handler, safely merges the selected host configuration, validates JSON, and checks that a repeated install makes no changes. Run it once for every repository that needs checkpoint reminders.

For a preview:

```text
Use $baselinedocs-setup-hooks to preview installing the checkpoint hook for Codex in this repository. Do not change files.
```

Manual fallback:

1. Copy `hooks/checkpoint.py` to `.baseline/hooks/checkpoint.py` and `hooks/prompts/checkpoint.md` to `.baseline/hooks/prompts/checkpoint.md`.
2. Merge and adapt one example configuration:
   - Codex: `hooks/examples/codex.hooks.json` to `.codex/hooks.json`
   - Claude Code: merge `hooks/examples/claude.settings.json` into `.claude/settings.json`
   - Cursor: `hooks/examples/cursor.hooks.json` to `.cursor/hooks.json`
3. Confirm `python` is available.
4. Review and trust project-local hooks in the agent UI when required.
5. Test with:

```bash
python .baseline/hooks/checkpoint.py --agent codex --event Stop < sample-event.json
```

Use a JSON payload containing `cwd`, `hook_event_name`, and the host stop-loop field.

## Behavior

The hook stays silent when:

- the host already continued the same stop event
- the event payload is invalid
- the prompt file is missing or empty

Otherwise it creates at most one continuation and asks the agent to:

- identify a pack only from the current thread
- avoid global roadmap discovery
- make no changes when the pack is absent, ambiguous, or already current
- checkpoint only work attributable to the current thread
- avoid changes owned by parallel threads in a shared working tree
- leave all changes uncommitted

This adds one model continuation to each initial Stop event in a repository where the hook is installed. The loop marker prevents a second continuation for the same turn.

## Compatibility

The command still accepts `--strict` for compatibility with existing local configurations, but the flag has no separate behavior and is no longer part of the public setup instructions.

## Host boundaries

- Codex loads project hooks from `.codex/hooks.json` after trust review. The command returns a JSON continuation reason because plain text is invalid for `Stop`.
- Claude Code uses the same prompt through its `Stop` command handler.
- Cursor uses lowercase `stop` and a `followup_message`.

Hook schemas evolve independently. Treat the examples as versioned templates and verify them against the installed agent version before organization-wide rollout.
