---
name: baselinedocs-audit-drift
description: Audit which baseline documents have fallen behind the code, ranked by `code_ref` frontmatter provenance, and report without modifying files. Use automatically when staleness or alignment between docs, code, and decisions is uncertain. For whether an individual statement is supported by evidence, use `baselinedocs-audit-claims` instead.
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
- not a claim-level evidence check; `baselinedocs-audit-claims` does that
