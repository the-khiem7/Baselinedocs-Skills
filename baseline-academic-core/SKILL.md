---
name: baseline-academic-core
description: Load, recall, reload, or re-read the baselinedocs lesson rules - how a lesson built from baseline pack documents is formatted, cited and anonymized - together with the pack contract and the report style, into working context without composing a lesson. Use before free-form work on an anonymized lesson that no baselinedocs academic skill covers, after a context compaction during lesson work, or when the user says the agent forgot the lesson, citation or anonymization rules. Every baselinedocs academic skill also reads it from this folder.
version: "3.4.0"
---

# Baseline Academic Core

The single home of what every `baselinedocs-academic-*` skill reads: `references/academic-contract.md` (the lesson format, the citation rule, and the anonymization rules). The academic skills read it from this folder and ship no copy. Pack documents themselves are read through `baseline-core`, not here.

Selected by an agent or by the user, load the rules and stop. Nothing is read from a pack and nothing is written.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `references/academic-contract.md` beside this SKILL.md in full now, every time.

Read `<core-dir>/references/pack-contract.md` in full now, every time.

Read `<core-dir>/references/report-style.md` in full now, every time.

## Workflow

1. Read the three files above in full. Do not skim headings, sample sections, or substitute a search for a read. Do not rely on a summary's paraphrase: the anonymization rules are checked against their wording, and a lesson that leaks a name cannot be recalled once shared.
2. Do not read a pack or a lesson, and do not reconstruct lesson state from a summary.
3. When a baselinedocs academic skill is running and its instructions are still in context, return to it once the files are read; steps 4 and 5 do not apply. When its instructions were compacted, name it as the skill to invoke again; do not continue its work from the summary.
4. Respond strictly with "Sẵn sàng." (or "Ready." in English environments), plus the one line from step 3 when it applies.
5. Stop. Do not resume, propose, or plan work unless asked.

## Non-Goals

- not a lesson; `baselinedocs-academic-compose` builds one
- does not modify or write files
- does not resume interrupted work
- not self-contained when moved: every `baselinedocs-academic-*` skill expects this folder beside its own, and this folder expects `baseline-core` beside it
