---
baseline_schema: "2.0"
pack: "family-design"
document: "roadmap"
status: "active"
updated: "2026-09-16"
code_ref: "uncommitted"
---

# Family Design Roadmap

Reasoning for every row below lives in `family-design.hallucination.md` under the entry named in its Basis column. Do not restate it here.

**Provenance, and a limit on how this document may be read.** This pack was adopted from `DESIGN.md`, which is a decision log and records no execution history for the family design: no phases, no dates, no checkpoints. The area rows below are therefore a status view built by verifying each design claim against the working tree at `0cb913f`. They are not a recorded sequence, and nobody should read them as one. FD-P1 is the only real phase in this pack, because it is the only work this pack watched happen.

## Design area status

Verified against the repository, not against `DESIGN.md`.

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Trigger architecture | FD-D1, FD-D38, FD-D39 | implemented | 8 `agents/openai.yaml` files set `allow_implicit_invocation: false`, exactly the 8 user entrypoints; the other 8 set `true`. Pinned by `tests/test_skill_metadata.py` |
| Pack schema 2.0 | FD-D2 | implemented | `contract/pack-contract.md` defines 3 required and 2 conditional documents; the `status` enum holds `draft`, `active`, `blocked`, `complete` |
| Frontmatter semantics | FD-D3 | implemented | contract states `updated` as the edit date and `code_ref` as the inspected code state, with `uncommitted` and `unknown` as valid values |
| Checkpoint contents | FD-D4 | implemented | `baselinedocs-run/references/execution-contract.md`, `Phase checkpoint`, lists outcome, evidence, changed files, unresolved risk, next phase, and routes reasoning to `hallucination` |
| Run and save boundary | FD-D5 | implemented | `README.md` trap table states it; `run` checkpoints each phase |
| Hook infers nothing | FD-D6, FD-D37 | retired | Hook adapter retired and removed in FD-P8. Checkpoint execution handled in-thread by `run` |
| Rule placement | FD-D7 | implemented | 13 byte-identical `pack-contract.md` copies and 15 `report-style.md` copies with `baselinedocs-load` exempt, each with a gate sentence in its `SKILL.md`. Pinned by `tests/test_references.py` |
| Workflow sequence written down | FD-D8 | implemented | `README.md` Mermaid flowchart plus the branch table |
| README leads with the workflow | FD-D9 | implemented | `README.md` order is Install, Workflow, Six User Entrypoints; no per-skill install command present |
| Onboard scope gate | FD-D10 | implemented | `baselinedocs-onboard/SKILL.md` steps 4 and 5, and its first two Reading Rules |
| Initiative routing | FD-D11, FD-D12, FD-D13 | implemented | `onboard` steps 2 and 3; `Never write the index` in step 2 |
| Dependency edges and coupling | FD-D14, FD-D15, FD-D16 | implemented | `onboard` Reading Rules, four consecutive rules covering edges, collected references, unresolved references, and the index-status contradiction |
| Output leads with state | FD-D17 | implemented | `onboard` step 11 and the `Output` section, whose two parts are `I. Pack status` then `II. Read record` |
| Source material excluded | FD-D18 | implemented | `onboard` Reading Rules, retained-source-material rule keyed on absent baseline frontmatter |
| Resume family dissolved | FD-D19, FD-D20 | implemented | no `resume-*` folder on disk; `baselinedocs-brief` present and set to `false` |
| Evidence retention | FD-D21, FD-D29 | implemented | `contract/pack-contract.md`, `Evidence density`, carries both lists, the resolved-mistake distinction, and the external-log permission. 11 packaged copies re-synced |
| `useguide` role | FD-D22, FD-D29 | implemented | contract, `Conditional documents`, carries the criterion, the five valid forms, and the wiki routing rule |
| Execution policy gate | FD-D23 | implemented | `execution-contract.md`, `Selection gate`. Pinned by `tests/test_run_policy.py` |
| Multi-pack routing | FD-D24 | implemented | contract, `Multi-pack initiatives`; and `docs/baseline/baselinedocs.index.md` now exercises it |
| Report structure | FD-D31, FD-D32, FD-D33, FD-D34, FD-D35 | implemented | `contract/report-style.md` at 43 lines carries 8 rules plus the four-column exception; 14 packaged copies `cmp` clean; `baselinedocs-onboard/SKILL.md` `Output` is five flat sections, `Read record` removed |
| Decision entry register | FD-D36 | implemented | `contract/pack-contract.md`, `Register`, a standalone section after `Required documents`, states the compact form for a decision's four required parts and the loss-verification step; 11 packaged copies `cmp` clean |
| Installation profiles | FD-Q1 | deferred | no platform mechanism exists to build against |
| Organization-wide hook rollout | FD-Q2, FD-D37 | closed | Hook mechanism removed from repository in FD-P8; rollout no longer applicable |
| Silent loader entrypoint | FD-D39 | implemented | `baselinedocs-load` implemented as a silent pack loader with single-word confirmation output; exempt from `report-style.md` in `tests/test_references.py` |

## FD-P1: adopt `DESIGN.md` into this pack

Acceptance criteria:

- every section of `DESIGN.md` maps to a named destination, including the sections that map to the existing `skill-consolidation` pack rather than to a new file
- nothing `skill-consolidation` already owns is restated here
- `DESIGN.md` is unchanged, byte for byte
- `uvx pytest tests/ -q` stays green, including `test_no_typographic_dashes`, which globs this pack

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| Source | `DESIGN.md`, 495 lines, 60,743 bytes, unchanged at this phase. `git status` reported it clean |
| Files created | 5: 4 pack documents and the initiative index |
| Source sections mapped | 22 of 22 |
| Sections deferred to `skill-consolidation` rather than restated | 7 |
| Entries written here | 30: FD-D1 to FD-D26, FD-Q1 to FD-Q4 |
| Entry index | required and present. 30 entries, above the 20-entry threshold |
| Content dropped | none |

Changes:

| File | Change |
|---|---|
| `docs/baseline/family-design/family-design.introduction.md` | new. Scope, the out-of-scope table naming each other owner, verified current truth, target, constraints, platform basis |
| `docs/baseline/family-design/family-design.roadmap.md` | new. This document |
| `docs/baseline/family-design/family-design.hallucination.md` | new. 30 entries with an entry index |
| `docs/baseline/family-design/family-design.sourcecode.md` | new. Instruction surfaces, checkpoint hook execution flow, execution policy, pack layout |
| `docs/baseline/baselinedocs.index.md` | new. Routes the two packs, carries the dependency edge and the cross-pack checkpoint |
| `DESIGN.md` | untouched. Retention was not authorized either way, so the source is retained as it stands |

### Coverage ledger

Every section of `DESIGN.md` at `0cb913f`, with its destination. A destination naming `skill-consolidation` means the information is already recorded there in fuller form and was deliberately not copied.

| Source section | Lines | Destination |
|---|---|---|
| Decision Summary | 3-38 | split by row. Rows about the family design became entries FD-D1 to FD-D26 here; rows about the consolidation are already `skill-consolidation` SC-D1 to SC-D21. The table's own function is served by the entry index in each `hallucination` |
| Trigger Architecture | 40-51 | FD-D1. Mechanics in `family-design.sourcecode.md`, `Instruction surfaces`; counts in `family-design.introduction.md`, `Current truth` |
| Pack Schema | 53-68 | FD-D2 |
| Frontmatter Semantics | 70-74 | FD-D3 |
| Checkpoint Model | 76-92 | FD-D4, FD-D5, FD-D6. Execution flow in `family-design.sourcecode.md`, `Checkpoint hook` |
| Rule Placement | 94-124 | FD-D7, and the surface table in `family-design.sourcecode.md`. The criterion for which skill ships which asset is `skill-consolidation` SC-D16 and SC-D17, cited and not restated |
| Report Style As A Shipped Asset | 126-136 | `skill-consolidation` SC-D17 |
| Hard-Wrapped Paragraphs | 138-146 | `skill-consolidation` SC-D18 |
| Entry Index | 148-164 | `skill-consolidation` SC-D19 |
| Misfiled Content | 166-178 | `skill-consolidation` SC-D20 |
| Workflow Sequence | 180-195 | FD-D8 |
| README Shape | 197-205 | FD-D9 |
| Onboard Scope Gate | 207-237 | FD-D10, FD-D11, FD-D12, FD-D13, FD-D14, FD-D15, FD-D16, FD-D17, FD-D18 |
| Resume Family Dissolved | 239-272 | FD-D19, FD-D20 |
| Skill Consolidation, all subsections | 274-379 | `skill-consolidation` SC-D1 to SC-D14 and SC-D21, and its roadmap SC-P1 to SC-P14 |
| Detect And Repair | 381-430 | `skill-consolidation` SC-D12, and `skill-consolidation.sourcecode.md`, `The sync and audit skills` |
| Evidence Retention | 432-451 | FD-D21, and the shipping gap as FD-Q3 |
| Useguide Role | 453-463 | FD-D22, and the shipping gap as FD-Q3 |
| Loop Engineering | 465-469 | FD-D23. Policy tables in `family-design.sourcecode.md`, `Execution policy` |
| Multi-Pack Routing | 471-480 | FD-D24. Layout in `family-design.sourcecode.md`, `Pack layout on disk`; instantiated by `docs/baseline/baselinedocs.index.md` |
| Deferred Work | 482-487 | FD-Q1, FD-Q2, and FD-D26. The closing line that nothing about the skill family remains deferred is carried by the Risks table below |
| Research Basis | 489-495 | `family-design.introduction.md`, `Platform basis`. All five links preserved |

Two entries here are not in the source. FD-Q3 and FD-Q4 were found during this adoption and are marked as such in their own text, so a later reader does not attribute them to `DESIGN.md`.

### Finding: seven sections were already owned, and copying them would have been the easy mistake

`DESIGN.md` reads as one document, so the obvious adoption is one pack holding all of it. Seven of its twenty-two sections are already recorded in `skill-consolidation` in fuller form, with rejected alternatives and measured numbers this file only summarizes. Copying them would have produced two descriptions of the same twenty-one decisions with nothing pinning them together, which is the drift the family's own rule-placement decision exists to prevent, reproduced inside the documentation about it.

The check that caught it was reading the existing pack in full first, all 1,254 lines, before deciding the layout. Reading it by headings would have shown a pack named for consolidation and would not have shown that it already owns the report-style, hard-wrap, entry-index, and misfiled-content decisions, none of which is about consolidating a skill.

## FD-P2: close the coverage gaps a planned deletion exposes

Opened when FD-D27 settled that `DESIGN.md` is deleted rather than retained. A ledger row routing a section to another pack was sufficient while the source stayed on disk; it is not sufficient once the source goes. FD-D28 carries the reasoning.

Acceptance criteria:

- every fact in the seven sections FD-P1 routed to `skill-consolidation` is present in the pack that owns it, checked at fact granularity rather than section granularity
- each addition lands in the entry whose subject already covers it, with no new entry and no new document
- `DESIGN.md` still unchanged, byte for byte
- `uvx pytest tests/ -q` stays green

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| Method | every numeric token and every capitalised term in the 225 deferred lines of `DESIGN.md`, checked for presence across `skill-consolidation` |
| Facts checked | all tokens in the seven deferred sections |
| Gaps found | 2 |
| Gaps closed | 2 |
| Entries or documents added | none. Both facts belonged inside an entry that already existed |
| `DESIGN.md` | unchanged. `git status` reports it clean |

| Gap | Where it belonged | Source |
|---|---|---|
| Terraform separating `plan` from `apply` as the same shape of argument for keeping a detect skill apart from a repair skill | `skill-consolidation` SC-D12, its rejected one-skill-per-comparison-scope alternative | `DESIGN.md:424` |
| the entry index breaking even at about five percent of entries deferred, and its projected saving near 35,000 tokens per load on a 342 KB journal | `skill-consolidation` SC-D19, `Why conditional rather than mandatory` | `DESIGN.md:152` |

Changes:

| File | Change |
|---|---|
| `skill-consolidation.hallucination.md` | two facts added to SC-D12 and SC-D19; frontmatter `updated` to 2026-08-28 and `code_ref` to `0cb913f`, the state inspected |
| `family-design.hallucination.md` | FD-D27 records the replacement decision and its prerequisites; FD-D28 records the ledger-versus-coverage lesson; two index rows added |

`skill-consolidation`'s roadmap still states that its phases SC-P9 through SC-P14 are uncommitted, and that is left alone here. It is a pack that has fallen behind the code, which `baselinedocs-sync-codebase` owns, and repairing it in passing would mix an unrelated correction into a coverage phase.

## FD-P3: close both open questions and finish the handover

Three deliverables, joined because all three were unblocked by the same round of user decisions. Reasoning is in FD-D29 and FD-D30; the `AGENTS.md` work is the last prerequisite FD-D27 listed.

Acceptance criteria:

- `contract/pack-contract.md` carries the retention standard and the `useguide` definition in full, and all 11 packaged copies are byte-identical to it
- the contract's section structure is verified by reading the whole file, not the diff
- no identifier anywhere in `docs/baseline/` is written without its pack prefix, and no cross-pack reference points at a heading that does not exist
- no file outside `docs/baseline/` names `DESIGN.md`
- `uvx pytest tests/ -q` stays green

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `contract/pack-contract.md` | 108 lines to 129 |
| Packaged contract copies | 11, re-synced, `cmp` clean against canonical |
| Contract structure | all 12 headings present and all 5 role bullets under the correct heading, checked by listing each bullet with the heading above it rather than by eye |
| Identifiers renamed | 34 in this pack, 43 in `skill-consolidation`, and every reference to them |
| Unprefixed identifiers left | 0 in both packs |
| Dangling cross-pack references | 0. Every `SC-` reference in this pack resolves to a heading in `skill-consolidation` |
| `DESIGN.md` references outside `docs/baseline/` | 0 |
| `DESIGN.md` | still unchanged, byte for byte |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | `Evidence density` gains the keep and discard lists, the resolved-mistake distinction, and the external-log permission; `Conditional documents` gains the `useguide` definition, its five valid forms, and the wiki routing rule |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `family-design.hallucination.md` | FD-D29 and FD-D30 added; FD-D21 and FD-D22 reduced to reasoning now that the contract carries the rule; FD-Q3 and FD-Q4 closed and their analysis carried into the decisions; every identifier prefixed |
| `skill-consolidation.hallucination.md` | every identifier prefixed; SC-Q6 records which of its clauses FD-D30 settled and which stay open |
| `skill-consolidation.roadmap.md`, `skill-consolidation.sourcecode.md`, `skill-consolidation.introduction.md` | every identifier prefixed |
| `AGENTS.md` | four references to `DESIGN.md` rewired to the packs: the ships table, the rule against citing a non-shipping file to justify a cut, `Where reasoning goes` with a pack-ownership table, and the merge pointer under `Conventions` |
| `baselinedocs.index.md` | identifier rule, dependency edge, and cross-pack checkpoint updated |

### Finding: the contract edit was verified by reading the whole file, and that is why it can be trusted

`skill-consolidation` SC-D21 records an earlier contract edit that destroyed the `## Conditional documents` heading, passed `cmp` across all 11 copies, and kept the suite green, because every check available measures whether the copies agree rather than whether the source is still correct. This phase touched the same two regions of the same file. The structure check above is that lesson applied rather than restated: the heading list and the bullet-to-heading mapping were both produced mechanically after the edit, before the copies were made.

### Finding: closing FD-Q3 moved a rule, so a duplicate had to be removed in a fixed order

FD-D21 and FD-D22 each carried the full text of a rule the contract only summarized. Once the contract carried it, those two entries held a second copy, and a second copy of a rule is the thing this repository spends the most effort removing. The order was forced: widen the contract, re-copy to all 11, verify, then trim the pack entries. Trimming first would have dropped the rule for as long as it took to notice, which is the sequencing `skill-consolidation` SC-D10 already records. What is left in FD-D21 and FD-D22 is reasoning, which the contract deliberately does not carry.

## FD-P4: delete the source

The last step of the adoption, kept as its own phase because it is the one act in this sequence the repository cannot undo by editing a file. FD-D27 carries the decision and the prerequisites it had to clear.

Acceptance criteria:

- the full-file coverage check runs once more, over all 22 sections rather than the 7 FD-P2 checked, and every apparent gap is either closed or shown to be a formatting difference
- `DESIGN.md` is recoverable from Git history after the deletion, and the exact command is recorded
- no file outside `docs/baseline/` names `DESIGN.md`
- `uvx pytest tests/ -q` stays green

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| Coverage check scope | every numeric token and every capitalised term in all 495 lines, against both packs |
| Apparent gaps | 5 |
| Real gaps | 0. All five were false positives, listed below |
| Recovery command | `git show 0cb913f:DESIGN.md`, verified to return 495 lines before the deletion |
| `DESIGN.md` references outside `docs/baseline/` | 0 |
| File state | deleted from the working tree. `git status` reports ` D DESIGN.md` |

The five apparent gaps, each checked rather than waved through:

| Flagged | Verdict |
|---|---|
| `2415` and `3460` | present as `2,415` and `3,460` in FD-D18. The source wrote them without thousands separators; this pack writes them with. Same fact |
| `Concern` | a column header in the source's decision-summary table, not a fact |
| `Consequences` | a section heading in the source's detect-and-repair section. Its content is in `skill-consolidation` SC-D12 and `skill-consolidation.sourcecode.md` |
| `Inconsistent` | the label on a decision-summary row. The decision on that row, adding schema, status, date, and code provenance frontmatter, is FD-D2 and FD-D3 |

Changes:

| File | Change |
|---|---|
| `DESIGN.md` | deleted |
| `family-design.introduction.md` | the source row now records the deletion and the recovery command; `DESIGN.md` removed from the does-not-ship constraint, since it no longer exists to not ship |
| `family-design.roadmap.md` | this phase; next action; the line-count figure corrected from 496 to the 495 Git reports |
| `family-design.hallucination.md` | FD-D27 records the deletion as done |
| `baselinedocs.index.md` | cross-pack checkpoint updated |

### Finding: the line count in FD-P1 was wrong by one, and only the deletion exposed it

FD-P1 recorded the source as 496 lines. `git show 0cb913f:DESIGN.md | wc -l` returns 495. The figure came from a reader that numbers a trailing blank line; `wc -l` counts newline characters. One line is not a consequential error, but the way it survived is: it was written into a checkpoint, carried into the introduction, and read back twice without being questioned, because a number in a table looks like a measurement whether or not anything measured it. Corrected in both places to the figure a command returns.

## FD-P5: give `report-style.md` the shape of a report, and reinstall

Opened 2026-08-29 by a user review of a real `onboard` run in an unrelated repository. Four of the findings were layout, one reversed a shipped rule, and one proposed removing the load manifest. FD-D31, FD-D32, and FD-D33 carry the reasoning; the reinstall is the next action FD-P3 left standing, and it is in this phase because a rule that does not reach a machine changes nothing on it.

Acceptance criteria:

- `contract/report-style.md` carries the layout rules and all 14 packaged copies are byte-identical to it
- a general rule lives in `report-style.md` and a report's own section names live in that skill's `SKILL.md`, with neither restating the other
- the load manifest is compressed rather than removed, and still reports lines read
- all four host skill directories match this repository, contract and report style included
- `uvx pytest tests/ -q` stays green

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `contract/report-style.md` | 25 lines to 41. 4 rules to 8 |
| Packaged report-style copies | 14, re-synced, `cmp` clean against canonical |
| Contract copies | 11, untouched. No contract edit in this phase |
| Host directories updated | 4: `.claude`, `.agents`, `.kilocode`, `.kiro`. Each holds 15 skills, 11 contract copies, 14 report-style copies |
| Installed state verified | every skill folder diffed against this repository. The only difference is a gitignored `scripts/__pycache__` in `setup-hooks` that the installer does not copy |
| Entries written | 3: FD-D31, FD-D32, FD-D33 |

Changes:

| File | Change |
|---|---|
| `contract/report-style.md` | 4 rules added: gloss a quotation, structure a report rather than narrate it, a three-column table budget, and state the default answer set when asking. The next-action rule rewritten from verbatim quotation to structure-preserving restructure |
| `<skill>/references/report-style.md` | all 14 copies re-synced |
| `baselinedocs-onboard/SKILL.md` | `Output` rewritten into two named parts with a section per document role and a compressed manifest; step 11 rewired to point at `Output` instead of restating it; step 9 now requires a reference be said in the agent's own words before it is quoted |
| `AGENTS.md` | `Report style` now states that the asset governs report shape as well as element naming |
| `family-design.hallucination.md` | FD-D31, FD-D32, FD-D33 added; 3 index rows; entry count 32 to 35 |
| `family-design.roadmap.md` | this phase, the design area row, the installed-skills risk row, and the next action |
| `baselinedocs.index.md` | cross-pack checkpoint updated now that the reinstall is done |

### Finding: the reviewed report was produced with no report-style rules at all

The run under review came from an installed `baselinedocs-onboard` whose folder held no `report-style.md`, and a `pack-contract.md` at 82 lines against this repository's 129. So every formatting quality the reviewer praised was emergent model behavior with nothing behind it, and every formatting defect broke no rule. That is why the reinstall belongs in the same phase as the rule: without it the next run on this machine would have reproduced both, and the fix would have looked ineffective rather than undelivered.

### Finding: three of the six layout complaints were one defect

The load manifest, the unresolved-reference list, and one of the two phase tables all degraded into vertical dumps of field names. All three were tables with more columns than the terminal could render; a two-column table in the same report rendered correctly. The reviewer described the symptom as a wall of text and proposed deleting the manifest. Diagnosing the mechanism is what turned one of those three into a column budget rather than a deletion, and FD-D33 records why the deletion would have cost a guarantee rather than a table.

### Finding: the installer splits neither `--skill` nor `--agent` on commas

A comma-separated list is treated as one literal name. `-s a,b,c` reports `No matching skills found` and prints the available list, which reads like a discovery failure rather than a syntax error, and `-a` fails the same way with `Invalid agents`. Repeating the flag works: `-a claude-code -a universal -a kilo -a kiro-cli`. Recorded because the first attempt appeared to succeed at a glance, exited non-zero without anything obviously wrong in the visible output, and left all four hosts unchanged. Any later reinstall loops one skill per invocation with the agent flag repeated.

## FD-P6: narrow `onboard`'s report to pack status only, and extend the table-width exception

Opened 2026-09-04 when this session's own `baselinedocs-onboard` run against this repository's two packs, exactly the exercise FD-P5's next action called for, returned a report the user judged too wall-of-text and too heavy on bookkeeping. FD-D34 and FD-D35 carry the reasoning; FD-Q5 opens on the gap the change leaves behind.

Acceptance criteria:

- `baselinedocs-onboard/SKILL.md`'s `Output` section reports pack state only, in five named sections, with no `Read record` half
- `contract/report-style.md` states the four-column exception in the section it qualifies, and all 14 packaged copies are byte-identical to it
- both gate sentences, for `pack-contract.md` and for `report-style.md`, survive unchanged in `baselinedocs-onboard/SKILL.md`
- `uvx pytest tests/ -q` stays green

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `contract/report-style.md` | 41 lines to 43. 1 exception added to the existing table-width rule |
| Packaged report-style copies | 14, re-synced, `cmp` clean against canonical |
| `baselinedocs-onboard/SKILL.md` | 79 lines to 69. `Output` from two parts, 6 plus 5 items, to 5 flat sections |
| Workflow steps removed | 1: the placement check, since nothing reports its result now |
| Contract copies | 11, untouched. No contract edit in this phase |
| Host directories updated | 0. Reinstall not carried out in this phase |
| Entries written | 3: FD-D34, FD-D35, FD-Q5 |
| Commit | `0d30867`, present on disk with the 16-file change already staged and committed under that hash. No `git commit` was invoked in this session; the commit's origin was not investigated here and was flagged to the user instead |

Changes:

| File | Change |
|---|---|
| `contract/report-style.md` | `Keep a table inside the terminal's width` gains the four-column exception |
| `<skill>/references/report-style.md` | all 14 copies re-synced |
| `baselinedocs-onboard/SKILL.md` | opening paragraph, steps 7 and 8, and one Reading Rules bullet trimmed of promises `Read record` no longer keeps; step 10 (placement check) deleted and the rest renumbered; `Output` rewritten into 5 flat sections |
| `family-design.hallucination.md` | FD-D34, FD-D35, FD-Q5 added; FD-D33's index status marked reversed by FD-D34; entry count 35 to 38 |
| `family-design.roadmap.md` | this phase, the design area row, the installed-skills risk row, and the next action |

### Finding: the checkpoint FD-P5 left standing returned the opposite verdict from what it was written expecting

FD-P5's next action asked for the report shape to be exercised on a real pack and reported on. It was, this session, against this repository's own two-pack initiative, and the report it produced was the one FD-P5 itself had just finished making readable: headed sections, budgeted tables, a restructured next action. The verdict was not that the shape held; it was that the shape it replaced, `I. Pack status` plus `II. Read record`, was still too much report for what the user wanted, independent of whether each part inside it was well formatted. A layout fix and a scope fix are different corrections, and FD-P5 only made the first one available to notice.

## FD-P7: state a compact register for `hallucination` entries in the contract

Opened 2026-09-04, in the same onboard session as FD-P6, when the user named the pain point directly: this pack's own entries burn context on every `onboard` because they are written as narrative prose rather than for the agent that reads them. The user pointed at two candidates already present on this machine, the `deprose` skill and the `.agents/skills/caveman*` family, and asked which fit. FD-D36 carries the reasoning and the rejection.

Acceptance criteria:

- `contract/pack-contract.md` states the compact register for a decision entry's four required parts, and all 11 packaged copies are byte-identical to it
- the rule changes wording only; the four required parts `Required documents` already mandates are not reduced
- the change is scoped to future entries; no existing entry in either pack is rewritten in this phase
- `uvx pytest tests/ -q` stays green

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `contract/pack-contract.md` | 129 lines to 140. New `Register` section added directly after `Required documents`, not folded into `Evidence density`: the compact four-part form plus the loss-verification step. Two standalone narrative-incident paragraphs, in `Before writing` and `Boundary with code`, compressed into a trailing clause on the directive each one justified; verified by grep that every term either named survived the compression |
| Packaged contract copies | 11, re-synced, `cmp` clean against canonical |
| Report-style copies | 14, untouched. No `report-style.md` edit in this phase |
| Host directories updated | 0. Reinstall not carried out in this phase |
| Entries written | 1: FD-D36 |
| Commit | `5bb5e7f`, present on disk with this phase's 14-file change already staged and committed under that hash. No `git commit` was invoked in this session; the commit's origin was not investigated here and is flagged to the user instead |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | new `Register` section, after `Required documents`: the compact four-part form, the cut-on-sight list, and the loss-verification sentence. `Before writing` and `Boundary with code` each lose one standalone narrative-incident paragraph, folded into the directive above it as a trailing clause |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `family-design.hallucination.md` | FD-D36 added; 1 index row; entry count 38 to 39 |
| `family-design.roadmap.md` | this phase, the design area row, the risk row, and the next action |

### Finding: compressing two narrative anecdotes does not reopen FD-D29

FD-D29 rejected shipping only the two sentences an agent cannot derive and kept the contract's reasoning in full, on the ground that "derivable" is the writer's judgement, not the agent's. This phase's anecdote compression is a narrower operation: each incident's fact set survives, moved from a standalone paragraph into a trailing clause on the directive it justifies, and checked afterward by grep for every term the original named. Nothing was judged derivable and cut; the words describing it were shortened. FD-D29's own boundary, keep the reasoning, not necessarily its longest phrasing, was never in question.

### Finding: two commits landed on this repository between this session's own `onboard` read and this phase, from the same user, under identifiers this phase could have collided with

This session's `onboard` read `family-design.hallucination.md` at 35 decision entries, `FD-D33` newest. Before this phase started editing, commits `0d30867` and `0d1cc02` had already landed on `main`, adding `FD-D34`, `FD-D35`, `FD-Q5`, and this roadmap's own `FD-P6`, none of it visible to the session that read the pack minutes earlier. Re-reading both files immediately before writing was what caught it; writing from the onboard read alone would have produced a second `FD-D34` naming an unrelated decision, the exact silent-collision failure `FD-D30` names as the reason every identifier carries a pack prefix, reproduced one level down inside a single pack's own counter instead of across packs.

## FD-P8: remove hook mechanism and setup-hooks skill

Opened 2026-09-11 when the user requested complete removal of hooks from the family. FD-D37 carries the reasoning and rejected alternatives.

Acceptance criteria:

- `baselinedocs-setup-hooks/`, `hooks/`, and `HOOKS.md` removed from the repository
- `tests/test_checkpoint.py` and `tests/test_install_hooks.py` removed; remaining test suite passes cleanly
- `contract/pack-contract.md` updated to remove "hooks" from line 36 and all 11 packaged copies re-synced
- `tests/test_skill_metadata.py` updated to 6 user entrypoints; `tests/test_references.py` updated to empty exemption
- Host installations in `.gemini`, `.agents`, and `.claude` cleaned up
- `uvx pytest tests/ -q` stays green, including `test_no_typographic_dashes`

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 12 passed, 40 subtests passed |
| Hook files removed | `baselinedocs-setup-hooks/` (5 files), `hooks/` (5 files), `HOOKS.md` |
| Test files removed | 2: `tests/test_checkpoint.py`, `tests/test_install_hooks.py` |
| Contract copies | 11, re-synced, `cmp` clean against canonical |
| Host directories cleaned | 3: `.gemini`, `.agents`, `.claude` |
| Entries written | 1: FD-D37; FD-D6 retired; FD-Q2 closed |
| Commit | uncommitted |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | line 36 removes "hooks" from the downstream tools sentence |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `tests/test_skill_metadata.py` | `baselinedocs-setup-hooks` removed from `ENTRYPOINTS` |
| `tests/test_references.py` | `REPORT_STYLE_EXEMPT` set to empty |
| `AGENTS.md` | `HOOKS.md` and `hooks/` removed from untracked list; report-style exemption note removed |
| `family-design.introduction.md` | counts updated to 14 skills and 6 entrypoints; hooks removed from scope and truth |
| `family-design.sourcecode.md` | `Checkpoint hook` replaced with `Checkpoint model` |
| `family-design.hallucination.md` | FD-D37 added; FD-D6 marked retired; FD-Q2 closed |
| `family-design.roadmap.md` | this phase, design area status, and risks updated |

## FD-P9: implement baselinedocs-load silent pack loader

Opened 2026-09-16 when the user requested a silent onboard variant that loads a pack into working context with zero conversational explanation, responding strictly with a single confirmation word. FD-D39 carries the reasoning and rejected alternatives.

Acceptance criteria:

- `baselinedocs-load` created as a user entrypoint with `allow_implicit_invocation: false`
- `baselinedocs-load/references/pack-contract.md` carries a byte-identical copy of `contract/pack-contract.md`
- `tests/test_references.py` exempts `baselinedocs-load` from `report-style.md` and gates on `LOAD_GATE`
- `tests/test_skill_metadata.py` adds `baselinedocs-load` to `ENTRYPOINTS`
- `uvx pytest tests/ -q` stays green, including `test_no_typographic_dashes`

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 12 passed, 45 subtests passed |
| Files created | `baselinedocs-load/SKILL.md`, `baselinedocs-load/agents/openai.yaml`, `baselinedocs-load/references/pack-contract.md` |
| Contract copies | 13, re-synced, `cmp` clean against canonical |
| Exemptions | `baselinedocs-load` in `REPORT_STYLE_EXEMPT` |
| Entries written | 1: FD-D39 |
| Commit | uncommitted |

Changes:

| File | Change |
|---|---|
| `baselinedocs-load/SKILL.md` | new skill instructions with `LOAD_GATE` and single-word confirmation output |
| `baselinedocs-load/agents/openai.yaml` | user entrypoint metadata with `allow_implicit_invocation: false` |
| `baselinedocs-load/references/pack-contract.md` | byte-identical copy of canonical contract |
| `tests/test_references.py` | `REPORT_STYLE_EXEMPT` gains `baselinedocs-load`; `LOAD_GATE` and `LOADER_SKILLS` defined |
| `tests/test_skill_metadata.py` | `ENTRYPOINTS` gains `baselinedocs-load` |
| `family-design.introduction.md` | counts updated to 16 skills and 8 entrypoints |
| `family-design.hallucination.md` | FD-D39 added; 1 index row |
| `family-design.roadmap.md` | this phase, design area status, and next action updated |

## Risks

| Risk | Detail |
|---|---|
| `AGENTS.md` points four times at a file that is being retired | FD-D27 made this pack canonical and scheduled `DESIGN.md` for deletion, so `AGENTS.md` is already wrong where it tells a contributor to record decisions in `DESIGN.md`. The file is still on disk, so nothing is broken yet, but a contributor reading `AGENTS.md` today would write a new decision into the file being deleted. The rewire is the next action below |
| `skill-consolidation` records its own state as uncommitted | Its roadmap states that SC-P9 through SC-P14 are uncommitted at the user's request. Those changes are now committed, at `959617b`, `b857216`, and `0cb913f`. This adoption did not repair it: `baselinedocs-sync-codebase` owns a pack that has fallen behind the code, and the repair belongs in that pack, not this one |
| Installed skills are behind this repository | Widened again 2026-09-11 by FD-P8 and 2026-09-16 by FD-P9, on top of the gap FD-P7 reopened. An installed skill reads its own packaged copy, so any given machine's global install drifts from this repository from its next edit onward, and whether a particular machine is current is machine-specific state this pack does not track. Reinstalling from this local clone is the standing remedy, not a one-time phase: `npx skills remove -g -s <the 14 names>` then `npx skills add . -g -a '*' -s <the 14 names>`, run again whenever a machine's copy needs to catch up |
| A reference written before 2026-08-28 names an identifier that no longer exists | FD-D30 renamed every identifier in both packs to carry a pack prefix. Anything citing a bare `D16` or `P8`, in a commit message or an earlier thread, now resolves to nothing. That is the intended failure mode, chosen over a bare number that resolves silently to the wrong entry, but it is a real cost to anyone holding an old reference |
| Nothing about the skill family itself is deferred | The rename sweep and the finished-pack marker were closed rather than postponed, in `skill-consolidation` SC-D13 and SC-D14. The only deferred item in this pack, FD-Q1, is blocked on a platform capability |

## Next action

On any machine whose global install has not picked up FD-P6's, FD-P7's, FD-P8's, and FD-P9's changes, reinstall the family from a local clone of this repository, the same mechanical step FD-P3 and FD-P5 both closed out with: the widened `contract/report-style.md` and its 14 re-synced packaged copies, the rewritten `baselinedocs-onboard/SKILL.md`, the widened `contract/pack-contract.md` and its 11 re-synced packaged copies, the removal of `baselinedocs-setup-hooks`, and the addition of `baselinedocs-load`. This is per-machine state, not a repository-wide fact this pack tracks, so no phase records when a given machine last ran it.

Separately, and explicitly deferred by the user rather than scheduled: rewriting `family-design.hallucination.md`'s and `skill-consolidation.hallucination.md`'s existing entries under FD-D36's compact register is its own piece of work, not a follow-on to this phase.

One open question is new: FD-Q5 asks who, if anyone, now checks a pack for misfiled content, since `onboard`'s placement check was deleted along with the output section that reported it. Nothing else in the pack is waiting on a user decision.

One repair is outstanding and belongs to another pack: `skill-consolidation.roadmap.md` states that SC-P9 through SC-P14 are uncommitted, and they are committed at `959617b`, `b857216`, and `0cb913f`. `baselinedocs-sync-codebase` owns a pack that has fallen behind the code, and the repair belongs in that pack rather than here.

One older open question remains in this pack: FD-Q1 waits on a portable hidden-skill mechanism that no installer provides. `skill-consolidation` still carries SC-Q6, SC-Q7, and SC-Q8, and SC-Q6 is the one this pack touched: FD-D30 settled its uniqueness clause and left the rest of it open.
