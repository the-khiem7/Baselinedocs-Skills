---
name: baselinedocs-audit-drift
description: Audit drift between code, baseline docs, frontmatter provenance, and decisions without modifying files by default. Use automatically when staleness or alignment is uncertain.
---

# Baseline Docs Audit Drift

## Purpose

Report where baseline truth drift exists.

## Use When

- the user wants an audit before syncing
- the team wants to know what is stale first
- trust in alignment between code and docs is uncertain

## Core Behavior

1. Read `status`, `updated`, and `code_ref` frontmatter to prioritize likely stale documents.
2. Compare scoped code changes after `code_ref`, document claims, and decision records.
3. Identify mismatch categories.
4. Report affected files and likely impact.
5. Recommend follow-up actions.

Treat a newer commit as a drift signal, not automatic proof that every document is stale.

## Primary Output

- drift report

## Non-Goals

- audit-first, not auto-fix-first
