---
name: baseline_docs_resume_snapshot
description: Create a canonical resume-ready snapshot from a long or messy baseline pack. Use when the pack became noisy, mixed, or difficult for future agents to resume from efficiently.
---

# Baseline Docs Resume Snapshot

## Purpose

Produce a cleaner, resume-friendly snapshot from an existing pack.

## Use When

- the baseline is long and chat-driven
- old and new content are mixed together
- future resume quality is low without compaction into a current-state snapshot

## Core Behavior

1. Read the existing pack.
2. Distill what is true now.
3. Separate active truth from historical noise.
4. Produce a concise resume-ready snapshot.

## Primary Output

- a canonical snapshot for future resume work

## Non-Goals

- not just one next action
- not a full archive or split operation
