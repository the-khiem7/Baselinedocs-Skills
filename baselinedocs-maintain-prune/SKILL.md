---
name: baselinedocs-maintain-prune
description: Prune obsolete, superseded, or misleading content from an active adaptive baseline pack. Use automatically when outdated or inapplicable sections cause confusion.
---

# Baseline Docs Maintain Prune

## Purpose

Remove obsolete noise from the active pack.

## Use When

- planned sections are no longer relevant
- assumptions were invalidated
- outdated content is confusing sync or resume work

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

## Core Behavior

1. Detect obsolete or misleading sections.
2. Remove or rewrite them.
3. Keep only content that still serves active truth.
4. Remove an optional `sourcecode` or `useguide` document only after preserving any unique useful content or obtaining sufficient evidence that it is obsolete.

A lesson entry describing a resolved mistake is not obsolete or misleading merely because the mistake is fixed - the mistake happening, and how it was caught, remains true and reusable. Do not prune it.

## Primary Output

- cleaner active baseline with less misleading residue

## Non-Goals

- not for preserving finished history; use archive for that
