---
name: baselinedocs-sync-codebase
description: Synchronize an existing baseline documentation pack with current implementation evidence. Use automatically after code changes, phase completion, or a checkpoint when related baseline docs may be stale.
---

# Baseline Docs Sync Codebase

## Purpose

Update an existing baseline pack so it reflects the actual current codebase.

## Use When

- code changed but docs did not
- routes, models, config, auth, jobs, or behavior drifted from the baseline pack
- roadmap evidence must reflect recent implementation changes

## Core Behavior

1. Inspect the codebase first.
2. Compare code against the baseline pack.
3. Treat stale docs as bugs.
4. Update every impacted baseline file in one pass when feasible.
5. Add changed files, verification evidence, and remaining risks to the roadmap.
6. Refresh `updated` and `code_ref` frontmatter in every changed document.

## Checkpoint Density

- Record the final result for each claim or phase.
- Omit routine failed attempts that no longer affect current truth.
- Keep a failure only when it remains unresolved, explains a design change, or is needed to reproduce a defect.
- Do not create optional `sourcecode` or `useguide` files when their roles are not applicable.

## Primary Output

- synced baseline docs
- refreshed roadmap evidence

## Non-Goals

- not for creating a brand new pack
- not for atomic one-decision propagation
- not for long-gap resume recovery
