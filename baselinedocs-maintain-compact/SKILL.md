---
name: baselinedocs-maintain-compact
description: Compact an existing baseline pack by reducing repetition, retries, and verbosity while preserving factual truth. Use automatically when the pack is too noisy to resume efficiently.
---

# Baseline Docs Maintain Compact

## Purpose

Reduce pack size and reading cost without losing truth.

## Use When

- the pack is too long
- multiple sections repeat the same information
- the resume cost became too high because the baseline is bloated

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

## Core Behavior

1. Detect repeated and low-value content.
2. Merge duplicates.
3. Preserve evidence and canonical truth.
4. Produce a denser, cleaner pack.

Collapse repeated fixture or command attempts into one final evidence entry. Retain only failures that remain actionable or explain a material change in approach.

Do not collapse a lesson entry - a mistake with why it looked reasonable, what disproved it, and the fix - into a shorter summary. Compacting it away, or trimming it to just the final state, discards the reason it exists.

## Primary Output

- shorter baseline docs with preserved meaning

## Non-Goals

- not for archiving completed phases
- not for splitting unrelated workstreams
