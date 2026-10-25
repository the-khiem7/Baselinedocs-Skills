---
name: baselinedocs-audit-claims
description: Check whether individual claims in a baseline pack are supported by code or an explicit decision, and classify each as verified, unverified, or contradicted. Reports without modifying files. Use automatically when documentation trust or evidence quality is low, including in a document whose provenance is current. For whether a whole document has fallen behind the code, use `baselinedocs-audit-drift` instead.
version: "3.3.0"
---

# Baseline Docs Audit Claims

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` before reporting the pack state, and report its FAIL and WARN lines as findings; it reports, it never fixes. Without `sh`, say the checks were not run.

## Purpose

Check whether baseline claims are actually supported.

## Use When

- the user wants to know which claims are proven versus assumed
- roadmap or useguide statements need evidence review
- the baseline is suspected to contain unsupported assertions

## Core Behavior

1. Collect factual claims from the pack.
2. Compare each with code and explicit decisions.
3. Classify each as verified, unverified, or contradicted by evidence.
4. Update no files unless the user also asks for synchronization.

Do not rank or filter claims by `code_ref`. A current `code_ref` does not make a claim supported, and a stale one does not make it false: an unsupported claim was never true, so it did not go stale. Reaching for provenance here answers the neighbouring skill's question instead of this one.

## Primary Output

- claim verification report, one verdict per claim

## Non-Goals

- not for broad syncing or pack maintenance
- not a document-level staleness check; `baselinedocs-audit-drift` does that
