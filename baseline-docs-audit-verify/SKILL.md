---
name: baseline_docs_audit_verify
description: Verify whether claims in the baseline pack are supported by code or explicit user decisions. Use when documentation trust is low and claims need evidence review.
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

## Primary Output

- claim verification report

## Non-Goals

- not for broad syncing or pack maintenance
