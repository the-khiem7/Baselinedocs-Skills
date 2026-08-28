---
baseline_schema: "2.0"
pack: "family-design"
document: "roadmap"
status: "active"
updated: "2026-08-28"
code_ref: "0cb913f"
---

# Family Design Roadmap

Reasoning for every row below lives in `family-design.hallucination.md` under the entry named in its Basis column. Do not restate it here.

**Provenance, and a limit on how this document may be read.** This pack was adopted from `DESIGN.md`, which is a decision log and records no execution history for the family design: no phases, no dates, no checkpoints. The area rows below are therefore a status view built by verifying each design claim against the working tree at `0cb913f`. They are not a recorded sequence, and nobody should read them as one. FD-P1 is the only real phase in this pack, because it is the only work this pack watched happen.

## Design area status

Verified against the repository, not against `DESIGN.md`.

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Trigger architecture | FD-D1 | implemented | 7 `agents/openai.yaml` files set `allow_implicit_invocation: false`, exactly the 6 entrypoints plus `setup-hooks`; the other 8 set `true`. Pinned by `tests/test_skill_metadata.py` |
| Pack schema 2.0 | FD-D2 | implemented | `contract/pack-contract.md` defines 3 required and 2 conditional documents; the `status` enum holds `draft`, `active`, `blocked`, `complete` |
| Frontmatter semantics | FD-D3 | implemented | contract states `updated` as the edit date and `code_ref` as the inspected code state, with `uncommitted` and `unknown` as valid values |
| Checkpoint contents | FD-D4 | implemented | `baselinedocs-run/references/execution-contract.md`, `Phase checkpoint`, lists outcome, evidence, changed files, unresolved risk, next phase, and routes reasoning to `hallucination` |
| Run and save boundary | FD-D5 | implemented | `README.md` trap table states it; `run` checkpoints each phase |
| Hook infers nothing | FD-D6 | implemented | `hooks/checkpoint.py` at 76 lines contains no Git, filesystem-search, or timestamp call; the loop guard reads `stop_hook_active` and `loop_count`. Pinned by `tests/test_checkpoint.py` |
| Rule placement | FD-D7 | implemented | 11 byte-identical `pack-contract.md` copies and 14 byte-identical `report-style.md` copies, each with a gate sentence in its `SKILL.md`. Pinned by `tests/test_references.py` |
| Workflow sequence written down | FD-D8 | implemented | `README.md` Mermaid flowchart plus the branch table |
| README leads with the workflow | FD-D9 | implemented | `README.md` order is Install, Workflow, Six User Entrypoints; no per-skill install command present |
| Onboard scope gate | FD-D10 | implemented | `baselinedocs-onboard/SKILL.md` steps 4 and 5, and its first two Reading Rules |
| Initiative routing | FD-D11, FD-D12, FD-D13 | implemented | `onboard` steps 2 and 3; `Never write the index` in step 2 |
| Dependency edges and coupling | FD-D14, FD-D15, FD-D16 | implemented | `onboard` Reading Rules, four consecutive rules covering edges, collected references, unresolved references, and the index-status contradiction |
| Output leads with state | FD-D17 | implemented | `onboard` step 11 and the `Output` section, which opens `State first` |
| Source material excluded | FD-D18 | implemented | `onboard` Reading Rules, retained-source-material rule keyed on absent baseline frontmatter |
| Resume family dissolved | FD-D19, FD-D20 | implemented | no `resume-*` folder on disk; `baselinedocs-brief` present and set to `false` |
| Evidence retention | FD-D21, FD-D29 | implemented | `contract/pack-contract.md`, `Evidence density`, carries both lists, the resolved-mistake distinction, and the external-log permission. 11 packaged copies re-synced |
| `useguide` role | FD-D22, FD-D29 | implemented | contract, `Conditional documents`, carries the criterion, the five valid forms, and the wiki routing rule |
| Execution policy gate | FD-D23 | implemented | `execution-contract.md`, `Selection gate`. Pinned by `tests/test_run_policy.py` |
| Multi-pack routing | FD-D24 | implemented | contract, `Multi-pack initiatives`; and `docs/baseline/baselinedocs.index.md` now exercises it |
| Installation profiles | FD-Q1 | deferred | no platform mechanism exists to build against |
| Organization-wide hook rollout | FD-Q2 | deferred | `baselinedocs-setup-hooks` handles one repository per invocation |

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

## Risks

| Risk | Detail |
|---|---|
| `AGENTS.md` points four times at a file that is being retired | FD-D27 made this pack canonical and scheduled `DESIGN.md` for deletion, so `AGENTS.md` is already wrong where it tells a contributor to record decisions in `DESIGN.md`. The file is still on disk, so nothing is broken yet, but a contributor reading `AGENTS.md` today would write a new decision into the file being deleted. The rewire is the next action below |
| `skill-consolidation` records its own state as uncommitted | Its roadmap states that SC-P9 through SC-P14 are uncommitted at the user's request. Those changes are now committed, at `959617b`, `b857216`, and `0cb913f`. This adoption did not repair it: `baselinedocs-sync-codebase` owns a pack that has fallen behind the code, and the repair belongs in that pack, not this one |
| Installed skills are behind this repository | Measured on one host directory only, `C:\Users\STYLVN\.claude\skills`: the installed `baselinedocs-adopt` carries an 82-line `pack-contract.md` and no `report-style.md`, against this repository's 108-line contract and 14 report-style copies. The other three host directories `skill-consolidation` names were not re-checked in this run |
| A reference written before 2026-08-28 names an identifier that no longer exists | FD-D30 renamed every identifier in both packs to carry a pack prefix. Anything citing a bare `D16` or `P8`, in a commit message or an earlier thread, now resolves to nothing. That is the intended failure mode, chosen over a bare number that resolves silently to the wrong entry, but it is a real cost to anyone holding an old reference |
| Nothing about the skill family itself is deferred | The rename sweep and the finished-pack marker were closed rather than postponed, in `skill-consolidation` SC-D13 and SC-D14. The only deferred items in this pack, FD-Q1 and FD-Q2, are blocked on a platform capability and on a rollout mechanism, neither of which is a skill-family question |

## Next action

Reinstall the family on this machine. `contract/pack-contract.md` moved from 108 lines to 129 in FD-P3, so every host skill directory now holds a contract at least one generation behind this repository, and an installed skill reads its own packaged copy rather than this one. Installing is a deliberate machine action, never a side effect of a repository edit, which is why it is stated as the next action rather than performed as part of a phase.

The adoption itself is finished. Nothing in this pack is waiting on a user decision.

One repair is outstanding and belongs to another pack: `skill-consolidation.roadmap.md` states that SC-P9 through SC-P14 are uncommitted, and they are committed at `959617b`, `b857216`, and `0cb913f`. `baselinedocs-sync-codebase` owns a pack that has fallen behind the code, and the repair belongs in that pack rather than here.

Two open questions remain in this pack, both deferred on something outside it: FD-Q1 waits on a portable hidden-skill mechanism that no installer provides, and FD-Q2 waits on a hook rollout design. Neither is a decision anyone can take today. `skill-consolidation` still carries SC-Q6, SC-Q7, and SC-Q8, and SC-Q6 is the one this pack touched: FD-D30 settled its uniqueness clause and left the rest of it open.
