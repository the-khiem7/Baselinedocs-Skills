---
name: baseline_docs_sync_reconcile
description: Reconcile contradictions inside an existing baseline pack. Use when roadmap, useguide, sourcecode, or introduction disagree about the current truth.
---

# Baseline Docs Sync Reconcile

## Purpose

Restore one canonical truth across the baseline pack.

## Use When

- baseline files contradict each other
- one file says implemented while another still says planned
- the pack has internal truth drift even before checking the codebase

## Core Behavior

1. Compare files inside the pack.
2. Detect contradictions.
3. Prefer code evidence and explicit user decisions.
4. Rewrite conflicting sections to converge on one truth.

## Primary Output

- a consistent baseline pack

## Non-Goals

- not for creating a new pack
- not for code-first syncing after implementation changes
