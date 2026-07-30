---
name: baselinedocs-audit-verify
description: Verify whether claims in an adaptive baseline pack are supported by code or explicit decisions. Use automatically when documentation trust or evidence quality is low.
---

# Baseline Docs Audit Verify

## Purpose

Check whether baseline claims are actually supported.

## Use When

- the user wants to know which claims are proven versus assumed
- roadmap or useguide statements need evidence review
- the baseline is suspected to contain unsupported assertions

## Core Behavior

1. Collect factual claims from the pack.
2. Compare them with code and explicit decisions.
3. Classify them as verified, unverified, or false/outdated.
4. Update no files unless the user also asks for synchronization.

## Primary Output

- claim verification report

## Non-Goals

- not for broad syncing or pack maintenance
