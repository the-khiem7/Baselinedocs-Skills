---
name: baseline_docs_resume_continue
description: Recover where work left off and determine how to continue from an existing baseline pack. Use when the user returns after a long gap and the agent no longer has prior conversation memory.
---

# Baseline Docs Resume Continue

## Purpose

Determine the current state and the correct continuation point.

## Use When

- the user returns after weeks or months
- the agent lost context
- the pack exists but it is unclear what is current versus old

## Core Behavior

1. Read the baseline pack as operational memory.
2. Identify current truth, unresolved items, and stale sections.
3. Summarize status, blockers, and risks.
4. End with an exact continuation path.

## Primary Output

- current-state resume brief
- exact continuation point

## Non-Goals

- not for creating a new pack
- not primarily for compacting or cleaning the pack
