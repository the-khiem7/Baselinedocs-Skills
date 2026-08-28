---
name: baselinedocs-maintain-compact
description: Compact an existing baseline pack by reducing repetition, retries, and verbosity, keeping its informational performance unchanged. Use automatically when the pack is too noisy to resume efficiently.
---

# Baseline Docs Maintain Compact

## Purpose

Reduce pack size and reading cost without losing truth.

## Use When

- the pack is too long
- multiple sections repeat the same information
- the resume cost became too high because the baseline is bloated

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Core Behavior

1. Detect repeated and redundant content.
2. Merge duplicates.
3. Preserve evidence and canonical truth.
4. Produce a denser, cleaner pack.

Collapse repeated fixture or command attempts into one final evidence entry. Retain only failures that remain actionable or explain a material change in approach.

## Gate

Compaction succeeds only when the document is shorter and its informational performance is unchanged. Before accepting a compacted document, check both:

- is every detail the original carried still recoverable from the shorter text
- can any passage now be read in more than one way

Either check failing means revert, not adjust. A long file costs less than a hallucination produced from a short one, so length is the cheap side of this trade and detail is not.

## Primary Output

- shorter baseline docs with preserved meaning

## Non-Goals

- not for moving content out of the active pack; compaction is compression, and relocating instead satisfies "shorter" while skipping the work the gate above asks for
- not for splitting unrelated workstreams
- not for removing a claim that turned out false; the contract's relocation rule owns that
