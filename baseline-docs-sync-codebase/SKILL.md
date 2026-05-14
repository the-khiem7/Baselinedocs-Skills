---
name: baseline_docs_sync_codebase
description: Synchronize an existing baseline documentation pack with the current codebase after implementation changes. Use when code changed but the related baseline docs were not updated.
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

## Primary Output

- synced baseline docs
- refreshed roadmap evidence

## Non-Goals

- not for creating a brand new pack
- not for atomic one-decision propagation
- not for long-gap resume recovery
