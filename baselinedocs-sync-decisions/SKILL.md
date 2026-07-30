---
name: baselinedocs-sync-decisions
description: Propagate one or more closed decisions across an existing baseline pack. Use automatically when resolved risks or business decisions have not reached every affected document.
---

# Baseline Docs Sync Decisions

## Purpose

Apply already-closed decisions across the full baseline pack.

## Use When

- one or more hallucination risks were closed
- decisions are recorded but not reflected elsewhere
- multiple baseline files still describe outdated options or uncertainty

## Core Behavior

1. Read the closed decisions.
2. Identify every affected baseline file and section.
3. Propagate the chosen direction into the pack.
4. Preserve decision history while removing active ambiguity.
5. Refresh `updated` and `code_ref` where implementation evidence was rechecked.

## Primary Output

- introduction, roadmap, sourcecode, and useguide aligned to the chosen decisions

## Non-Goals

- not for code drift syncing
- not for a single targeted atomic decision update when a smaller patch is enough
