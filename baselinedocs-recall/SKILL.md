---
name: baselinedocs-recall
description: Recall, reload, or re-read the baselinedocs rules - the pack contract and the report style - into working context after a context compaction or summary, before the next baseline pack write or report. Use when work on a baseline pack continues past a compaction, when the thread holds only a summary of rules read earlier, or when the user says the agent forgot the baselinedocs rules.
version: "3.1.0"
---

# Baseline Docs Recall

Restore the family's rules into working context and stop. Nothing is read from the pack and nothing is written.

Read `references/pack-contract.md` in full now, every time.

Read `references/report-style.md` in full now, every time.

## Workflow

1. Read both files above in full. Do not skim headings, sample sections, or substitute a search for a read. Do not rely on the summary's paraphrase of either file: a summary keeps that a rule existed, not its wording, and the wording is what a pack write is checked against.
2. Do not reread the pack, and do not reconstruct pack state from the summary. `baselinedocs-load` or `baselinedocs-onboard` reload a pack; `baselinedocs-brief` reports whether the thread holds work the pack does not.
3. When the interrupted work belonged to another baselinedocs skill, such as a `baselinedocs-run` phase, that skill's own instructions and references were compacted too. Name it as the skill to invoke again; do not continue its work from the summary.
4. Respond strictly with "Sẵn sàng." (or "Ready." in English environments), plus the one line from step 3 when it applies.
5. Stop. Do not resume, propose, or plan work unless asked.

## Non-Goals

- not a pack load; `baselinedocs-load` and `baselinedocs-onboard` read the pack
- not a status report; `baselinedocs-brief` reports position
- does not modify or write files
- does not resume interrupted work
