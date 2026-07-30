# Phase Checkpoint Hooks

The hook in `hooks/checkpoint.py` is an advisory guardrail. It looks for an active `*.roadmap.md` and implementation changes that are newer than baseline doc changes. When a turn stops, it asks the agent to update the pack with a compact checkpoint.

It does not edit documentation automatically.

## Install in a target repository

1. Copy `hooks/checkpoint.py` to `.baseline/hooks/checkpoint.py`.
2. Copy and adapt one example configuration:
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

- no active roadmap exists
- no implementation files appear newer than baseline docs
- the host already continued the same stop event

When a checkpoint is needed, it asks the agent to record only:

- current phase status
- final evidence
- changed files
- open risks
- exact next action
- refreshed frontmatter

## Strict mode

Add `--strict` to return a continuation or block decision where the host supports it. Strict mode can prevent a turn from finishing until the checkpoint is written.

Do not enable strict `PreCompact` blocking by default. Both Codex and Claude Code expose compaction lifecycle hooks, but interrupting automatic compaction near the context limit can cause the active request to fail. A Stop checkpoint plus post-compaction resume metadata is safer for general use.

## Host boundaries

- Codex loads project hooks from `.codex/hooks.json` after trust review. `Stop` can create one continuation prompt.
- Claude Code supports `Stop`, `TaskCompleted`, and `PreCompact`; the example uses `Stop` for portable semantics.
- Cursor uses lowercase `stop` and a `followup_message`.

Hook schemas evolve independently. Treat the examples as versioned templates and verify them against the installed agent version before organization-wide rollout.
