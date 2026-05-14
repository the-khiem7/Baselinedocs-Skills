---
name: baseline_docs_audit_drift
description: Audit drift between the codebase, baseline docs, and decisions without necessarily modifying files. Use when the user wants to inspect staleness or inconsistency before syncing.
---

# Baseline Docs Audit Drift

## Purpose

Report where baseline truth drift exists.

## Use When

- the user wants an audit before syncing
- the team wants to know what is stale first
- trust in alignment between code and docs is uncertain

## Core Behavior

1. Compare code, baseline docs, and decision records.
2. Identify mismatch categories.
3. Report affected files and likely impact.
4. Recommend follow-up actions.

## Primary Output

- drift report

## Non-Goals

- audit-first, not auto-fix-first
