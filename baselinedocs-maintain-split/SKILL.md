---
name: baselinedocs-maintain-split
description: Split one overloaded baseline pack into directly addressable domain packs with an initiative index. Use automatically when mixed workstreams or cross-domain dependencies reduce resume quality.
version: "3.4.0"
---

# Baseline Docs Maintain Split

## Purpose

Break one overloaded baseline into clearer bounded packs.

## Use When

- one pack covers too many unrelated tasks
- roadmap scope became too large
- multiple workstreams are mixed together and hard to resume

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` after every pack write and before reporting it, and allocate every new identifier with `sh <core-dir>/scripts/packtool.sh next-id <pack-dir> <D|Q|P> [PREFIX]`, never from memory. A new pack's first identifier needs its PREFIX. Never report a write as done while `check` prints a FAIL line: a duplicate identifier or a missing index row resolves citations to the wrong entry, and nothing else detects it. Without `sh`, say the checks were not run.

## Core Behavior

1. Identify natural split boundaries.
2. Group content by topic, feature, or workstream.
3. Produce smaller packs with clearer scope and ownership.
4. Create an initiative index containing direct links, status, and dependency edges.
5. Move shared reusable guidance to the wiki instead of a general wrapper pack.

## Primary Output

- multiple scoped baseline packs

## Non-Goals

- not for simple pruning or compaction alone
- not for hiding child packs behind a duplicated general pack
