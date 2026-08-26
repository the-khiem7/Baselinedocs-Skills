---
name: baselinedocs-maintain-archive
description: Archive completed baseline phases or tasks to preserve history without cluttering active operational memory. Use automatically when live docs should focus on unfinished work.
---

# Baseline Docs Maintain Archive

## Purpose

Move completed history out of the active baseline flow.

## Use When

- an epic or phase is complete
- old execution history is valuable but should not clutter active docs
- the active pack should focus only on live work

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

## Core Behavior

1. Identify completed sections.
2. Preserve them in an archive-friendly form.
3. Clean the active pack so only current work remains emphasized.
4. Set archived documents or sections to `status: archived` and keep direct links from the active roadmap when history is still relevant.

## Primary Output

- archived historical state
- cleaner active baseline

## Non-Goals

- not for deleting misleading leftovers without preserving history
