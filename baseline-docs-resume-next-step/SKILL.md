---
name: baseline_docs_resume_next_step
description: Reduce an existing baseline state into one precise next action. Use when the user asks what to do next and does not need a full resume analysis.
---

# Baseline Docs Resume Next Step

## Purpose

Extract one immediately actionable next move.

## Use When

- the user asks what to do next
- a full resume report is unnecessary
- the task only needs one exact action to proceed

## Core Behavior

1. Inspect the active baseline state.
2. Identify the highest-value executable next move.
3. Return one action with minimal rationale.

## Primary Output

- one exact next step

## Non-Goals

- not a full pack rewrite
- not a detailed handoff
