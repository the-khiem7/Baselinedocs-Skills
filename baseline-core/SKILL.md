---
name: baseline-core
description: Load, recall, reload, or re-read the baselinedocs rules - the pack contract, the report style, and the pack check script - into working context, without running a workflow or reading a pack. Use before free-form work on a baseline pack that no other baselinedocs skill covers, after a context compaction or summary before the next pack write or report, or when the user says the agent forgot the baselinedocs rules. Every baselinedocs skill also reads these files from this folder.
version: "3.4.0"
---

# Baseline Core

The single home of what every `baselinedocs-*` skill reads: `references/pack-contract.md` (which document owns which content), `references/report-style.md` (how a report names pack elements), `references/cowork-contract.md` (who writes where on a pack several people write), and `scripts/bldh.sh` (`outline`, `find`, `next-id`, `close-plan`, `check`). The other skills read them from this folder and ship no copy.

Selected by an agent or by the user, load the rules and stop. Nothing is read from a pack and nothing is written.

Read `references/pack-contract.md` beside this SKILL.md in full now, every time.

Read `references/report-style.md` beside this SKILL.md in full now, every time.

When the work is on a pack that holds a `<prefix>.cowork.md`, read `references/cowork-contract.md` beside this SKILL.md in full now as well.

## Workflow

1. Read the files above in full. Do not skim headings, sample sections, or substitute a search for a read. Do not rely on a summary's paraphrase of either file: a summary keeps that a rule existed, not its wording, and the wording is what a pack write is checked against.
2. Resolve the absolute path of `scripts/bldh.sh` beside this SKILL.md. For the rest of the session, run `sh <that path> check <pack-dir>` after every pack write and before reporting it, allocate every new identifier with `sh <that path> next-id <pack-dir> <D|Q|P> [PREFIX]`, and never report a write as done while `check` prints a FAIL line. Free-form work runs no workflow skill that would hold this rule.
3. Do not read the pack, and do not reconstruct pack state from a summary. `baselinedocs-load` or `baselinedocs-onboard` load a pack; `baselinedocs-brief` reports whether the thread holds work the pack does not.
4. When a baselinedocs skill is running and its instructions are still in context, return to it once the files are read; steps 5 and 6 do not apply. When its instructions were compacted, such as a `baselinedocs-run` phase, name it as the skill to invoke again; do not continue its work from the summary.
5. Respond strictly with "Sẵn sàng." (or "Ready." in English environments), then the absolute `bldh.sh` path, plus the one line from step 4 when it applies.
6. Stop. Do not resume, propose, or plan work unless asked.

## Non-Goals

- not a pack load; `baselinedocs-load` and `baselinedocs-onboard` read the pack
- not a status report; `baselinedocs-brief` reports position
- does not modify or write files
- does not resume interrupted work
- not self-contained when moved: every `baselinedocs-*` skill expects this folder beside its own
