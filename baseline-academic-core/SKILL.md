---
name: baseline-academic-core
description: Shared rules for the baselinedocs academic skills - how a lesson built from baseline pack documents is formatted, cited and anonymized. Installed beside every baselinedocs academic skill, which reads it. Not a workflow and not for direct use.
version: "3.4.0"
---

# Baseline Academic Core

The single home of what every `baselinedocs-academic-*` skill reads: `references/academic-contract.md` (the lesson format, the citation rule, and the anonymization rules). The academic skills point here and ship no copy. Pack documents themselves are read through `baseline-core`, not here.

If the user invoked this skill directly, there is nothing to run: name the `baselinedocs` skill that fits their request, or `baselinedocs-help` when unsure.

## Non-Goals

- not a workflow: it reads and writes no pack and produces no lesson
- not self-contained when moved: every `baselinedocs-academic-*` skill expects this folder beside its own
