---
name: baseline_docs_sync_decision
description: Apply one specific closed decision to the exact baseline files it affects. Use when a narrow, atomic update is safer than pack-wide synchronization.
---

# Baseline Docs Sync Decision

## Purpose

Apply one specific decision with minimal, targeted changes.

## Use When

- the user just closed one risk
- only a small part of the pack needs updating
- an atomic decision patch is preferable to a wider sync

## Core Behavior

1. Read the chosen decision.
2. Identify only the directly impacted files and sections.
3. Patch those sections without broad unrelated rewrites.

## Primary Output

- targeted baseline updates for one decision

## Non-Goals

- not for pack-wide decision propagation
- not for codebase drift syncing
