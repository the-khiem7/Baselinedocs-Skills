---
name: baselinedocs-setup-hooks
description: Install or update Baseline Docs checkpoint hooks safely in one repository for Codex, Claude Code, or Cursor. Use explicitly when the user asks to enable automatic phase checkpoints without manually copying hook files or merging agent configuration.
---

# Baseline Docs Setup Hooks

## Overview

Install the portable checkpoint handler and merge the selected host configuration without overwriting unrelated hooks. This is a one-time administrative action for each repository.

## Inputs

- target repository; default to the current repository
- agent host: `codex`, `claude`, or `cursor`
- optional dry-run request

Prefer an agent host named explicitly by the user. Otherwise infer it only when the current host or one existing host configuration makes the choice unambiguous. If multiple host configurations exist and the target is unclear, ask one concise question before writing.

## Workflow

1. Resolve and verify the repository root.
2. Inspect the selected host configuration before changing it.
3. Run the bundled installer:

   ```text
   python <skill-directory>/scripts/install_hooks.py --agent <codex|claude|cursor> --repo <repository>
   ```

   Add `--dry-run` when the user requests a preview.

4. Validate the resulting JSON and run the installer a second time to confirm it reports no changes.
5. Inspect the scoped diff. Report:
   - handler and configuration paths
   - whether existing configuration was preserved
   - validation result
   - any trust or restart action required by the host

## Installer Contract

The installer:

- copies `assets/checkpoint.py` to `.baseline/hooks/checkpoint.py`
- merges one handler into `.codex/hooks.json`, `.claude/settings.json`, or `.cursor/hooks.json`
- preserves unknown keys and existing hook entries
- refuses invalid existing JSON before making any change
- writes atomically and avoids duplicate handlers
- uses only the Python standard library

## Safety

- Do not overwrite the entire configuration.
- Do not install for multiple hosts unless the user asks.
- Do not commit unless the current request explicitly authorizes it.
- Treat project-local hook trust or restart prompts as user-controlled actions.
