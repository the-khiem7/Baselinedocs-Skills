---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "roadmap"
status: "active"
updated: "2026-08-27"
code_ref: "uncommitted"
---

# Skill Consolidation Roadmap

Verification gate for every phase: `uvx pytest tests/ -q` green. The repository has no `pyproject.toml`, so `uv run python -m pytest` does not work. Every checkpoint below met the gate: 20 passed and 23 subtests passed for P1 through P7, 21 passed and 23 subtests for P8 once the test it adds landed, 22 passed and 35 subtests for P9, and 24 passed and 63 subtests for P10 through P14.

Reasoning for each phase lives in `skill-consolidation.hallucination.md` under the decision named in its Basis column. Do not restate it here.

## Phase status

| Phase | Outcome | Basis | Depends on | Status |
|---|---|---|---|---|
| P1 | `sync-decision` folded into `sync-decisions` | D2 | - | complete |
| P2 | `maintain-prune` deleted, relocation rule in the contract | D4, D5 | P1 | complete |
| P3 | `audit-verify` renamed `audit-claims`, both audit descriptions rewritten | D3 | - | complete |
| P4 | `maintain-compact` carries the revert gate | D7 | - | complete |
| P5 | `maintain-archive` deleted, with `status: archived` and its only consumer | D11 | Q1 | complete |
| P6 | `DESIGN.md`, `AGENTS.md`, `README.md` aligned to the end state, and the last duplicate rule statements removed | D1, D8, D9, D10 | P1, P2, P3, P4 | complete |
| P7 | the sync and audit model corrected, and the routing pointers it exposed added | D12 | Q3 | complete |
| P8 | installed skills replaced on this machine, and the stale-count class of defect given a test | D8 | P7 | complete |
| P9 | the contract-shipping criterion changed to a full read, and `onboard` given the copy and a gate of its own | D16 | - | complete |
| P10 | report style shipped to every reporting skill, hard-wrapping banned, Q6 and Q7 opened from measured packs | D17, D18 | - | complete |
| P11 | entry index built on this pack as a Q7 trial | Q7 | P10 | complete |
| P12 | the entry index required by the contract above a threshold | D19 | P11 | complete |
| P13 | misfiled content given named owners in the contract, closing Q5 | D20 | P11 | complete |
| P14 | contract heading repaired, and the thread's uncaptured reasoning written down | D21 | P13 | complete |

## P1: fold sync-decision into sync-decisions

Acceptance criteria:

- one skill covers both the single-decision and the multi-decision case
- no file in the repository names `baselinedocs-sync-decision` except this pack and `DESIGN.md`, which P6 rewrites
- 12 packaged contract copies remain, all byte-identical to `contract/pack-contract.md`

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 17, down from 18 |
| Packaged contract copies | 12, all byte-identical, pinned by `test_packaged_contract_matches_canonical_contract` |
| Residual references | `DESIGN.md` only, deferred to P6 by design |

Changes:

| File | Change |
|---|---|
| `baselinedocs-sync-decision/` | deleted, 3 files |
| `baselinedocs-sync-decisions/SKILL.md` | D2's section-scope constraint added: patch only directly impacted sections, no broad unrelated rewrites. The mutual `Non-Goals` line pointing at the deleted skill removed. `description`, `Purpose`, `Use When`, `Core Behavior` also rewritten |
| `tests/test_references.py` | `"baselinedocs-sync-decision"` removed from `CONTRACT_SKILLS` |
| `README.md` | `Agent-Selected Skills` sync row |

Revision summary: the absorbed skill's trigger vocabulary was carried into the surviving description rather than dropped with the folder. Deleting a folder deletes a selection surface, and on hosts where `description` drives selection the words "atomic", "targeted", and "one specific" were the only route to the narrow case. This is part of the merge, not the separate description batch in D9.

Revision summary: `README.md` is edited by each deletion phase for its own row, while P6 keeps the counts, the criterion, and the deprecation record. P1's acceptance criteria had required a clean repository-wide reference check that P6 alone could not satisfy mid-sequence.

## P2: delete maintain-prune, add the relocation rule

Acceptance criteria:

- the disproven-claim case has a named owner in the contract
- no file names `baselinedocs-maintain-prune` except this pack and the deprecation record P6 adds to `DESIGN.md`
- 11 packaged contract copies remain, all byte-identical

Risk: `maintain-prune` is named by nothing else in the repository, verified at `cded242`, so no pointer needs repair. Re-verify before deleting rather than trusting this line.

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 16, down from 17 |
| Packaged contract copies | 11, all byte-identical, re-synced from canonical after the contract edit |
| Residual references | this pack only. `DESIGN.md` never named `maintain-prune`, so P6 adds a deprecation record rather than repairing one |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | new `Disproven claims` section carrying D5's rule, placed after `Reasoning ownership`. 74 lines to 82 |
| `<skill>/references/pack-contract.md` | all 11 remaining copies re-synced from canonical |
| `baselinedocs-maintain-prune/` | deleted, 3 files |
| `tests/test_references.py` | `"baselinedocs-maintain-prune"` removed from `CONTRACT_SKILLS` |
| `README.md` | `Agent-Selected Skills` maintain row |

The contract rule was written before the folder was deleted, so the disproven-claim case had a named owner at every point in the sequence. Its closing line is the load-bearing one: nothing in an active pack is removed on the grounds that it is no longer true, it is relocated. That is the general prohibition replacing the deleted skill, and it holds whether or not a future reader knows the skill existed.

## P3: rename audit-verify to audit-claims

Acceptance criteria:

- neither audit description can be satisfied by the other skill's question
- `test_skill_ids_match_folders` and `test_openai_prompts_name_the_skill` pass
- `allow_implicit_invocation: true` preserved, since this is not a user entrypoint

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 16, unchanged. A rename, not a deletion |
| Dangling pointers | none. All three inbound pointers, in `onboard` and `brief`, name `audit-drift`, which kept its name. `audit-verify` was named by nothing |
| Residual references | this pack only |

Changes:

| File | Change |
|---|---|
| `baselinedocs-audit-verify/` | renamed to `baselinedocs-audit-claims/` |
| `baselinedocs-audit-claims/SKILL.md` | `name`, description rewritten on D3's document-versus-claim axis, H1, `Core Behavior` step 3, new provenance rule, `Non-Goals` |
| `baselinedocs-audit-claims/agents/openai.yaml` | all three interface fields: `display_name`, `short_description`, `default_prompt` |
| `baselinedocs-audit-drift/SKILL.md` | description rewritten on the same axis, `Non-Goals` |
| `README.md` | `Agent-Selected Skills` audit row |

Each description now names the other skill for the question it does not answer. A routing pointer placed in the description reaches the selection surface itself, which is where the wrong choice was being made; the same sentence in the body would only be read after the choice was already wrong.

`Core Behavior` step 3 classified a claim as "false/outdated" before this phase. "Outdated" is drift vocabulary: it implies a claim was true and stopped being true, when an unsupported claim was never true at all. Changed to "contradicted by evidence", and a rule was added forbidding this skill from ranking claims by `code_ref` at all. Without that rule the two audit skills sit on one axis at two zoom levels, which is the state D3 rejected.

## P4: give compact its revert gate

Acceptance criteria:

- the body states the revert condition and the cost comparison, not only the goal
- the gate is stated as a pass or revert test, not as advice

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 16, unchanged |
| Packaged contract copies | 11, re-synced after the second contract edit, `cmp` clean |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | the lesson-entry rule now binds writing and later compaction in one sentence, absorbing the wording that lived in `maintain-compact`. 82 lines, unchanged in count: one sentence rewritten, not added |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `baselinedocs-maintain-compact/SKILL.md` | D7's gate written in with its WHY clause as a new `Gate` section. Also description, `Core Behavior` step 1, deleted lesson-entry restatement, new `Non-Goals` pointer |

Three changes beyond the gate itself, each closing a hole P2 opened or exposed:

`Core Behavior` step 1 said "repeated and low-value content". With `maintain-prune` deleted, "low-value" was the only phrase left in the family authorizing removal on grounds other than redundancy, which is the permission P2 revoked at contract level. Now "repeated and redundant".

The description promised "preserving factual truth", a weaker standard than the gate it now carries. Factual truth survives while detail is lost and a passage becomes ambiguous, which is exactly the failure the gate rejects. The description is the selection surface, so it states the real standard.

The lesson-entry restatement was deleted rather than kept, and the canonical sentence was widened first so nothing was lost in the trade. The contract had framed the rule under evidence density, which reads as guidance for writing an entry; an agent shrinking an existing document could have read it as not applying. Now it names both cases.

### Finding: the lesson-entry rule is still stated twice more

Outside the pinned contract copies, the rule appears in two further wordings, both in files the reading skill already has:

| Location | Why it is a duplicate |
|---|---|
| `baselinedocs-run/references/execution-contract.md:42` | `run` reads both of its reference files on the same run, so the rule is stated twice to one reader |
| `baselinedocs-save/SKILL.md:39` | `save` ships a contract copy, so the rule is in a file it already reads |

Neither has the host-boundary excuse that justifies the 11 contract copies: those exist because a skill cannot reach a sibling's folder, while these are second statements inside one folder. `test_references.py` cannot see them drift, because it only compares contract copies against the canonical file.

P4 also invalidated one sentence in `DESIGN.md:190`, which credits `maintain-compact` with forbidding lesson-entry compression. The prohibition still exists and still holds; it now lives in the contract. P6 owns that correction.

## P5: delete maintain-archive and its orphaned consumers

Scope changed after Q1 was answered. The phase was written as "specify the destination"; specifying it disproved D6, and D11 replaced it. Reasoning is in D11, not here.

Acceptance criteria:

- no file in the repository names `baselinedocs-maintain-archive` except this pack and the `DESIGN.md` record
- no producer and no consumer of `status: archived` remains, and the value is gone from the enum
- 10 packaged contract copies, all byte-identical
- `maintain-compact` still forbids relocation after the skill that owned it is gone

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 15, down from 16 |
| Packaged contract copies | 10 |
| `status: archived` | no producer, no consumer, not in the enum |
| Residual references | this pack and `DESIGN.md`'s deletion record only |

Changes:

| File | Change |
|---|---|
| `baselinedocs-maintain-archive/` | deleted, 3 files |
| `contract/pack-contract.md` | `archived` removed from the `status` enum. 82 lines, no line count change |
| `<skill>/references/pack-contract.md` | all 10 copies re-synced, `cmp` clean after the fourth contract edit |
| `tests/test_references.py` | `"baselinedocs-maintain-archive"` removed from `CONTRACT_SKILLS` |
| `baselinedocs-onboard/SKILL.md` | `Inputs`, and the archived-material exclusion removed from `Reading Rules`. Two `Reading Rules` lines merged into one, because the retained-source-material rule beside the exclusion read "on the same terms" and its terms were being deleted, so it had to be made self-standing |
| `baselinedocs-maintain-compact/SKILL.md` | `Non-Goals`: `not for archiving completed phases` replaced with a direct prohibition on moving content out of the active pack, so the deletion does not silently grant compact the relocation right D11 rejected |
| `README.md` | `Agent-Selected Skills` maintain row |
| `AGENTS.md` | pack-writing count in four places, not two |
| `DESIGN.md` | `Decision Summary` row, `Onboard Scope Gate` paragraph removed and its principle moved to the source-material rule, `Skill Consolidation` count and table row, `Why archive was kept` replaced by `Why archive was deleted`, `Deferred Work` bullet replaced |

Revision summary: `AGENTS.md` still said 14 in two further places, at `The pack contract` bullets "copy it to all 14" and "Each of the 14". P6 corrected the two prose mentions and missed these, because it searched for the sentence it knew about rather than for the number. All four now read 10.

Revision summary: the compact non-goal was replaced rather than deleted. It had named `maintain-archive` to mark a boundary, and deleting the line with the skill would have removed the prohibition along with the pointer, silently handing compact the relocation right D11 records as rejected. Same shape as the P6 pointer replacements: when a line names something being deleted, check whether the line is a pointer or a rule wearing a pointer's clothes.

### Finding: the last mention of archiving in shipped text

`baselinedocs-adopt/SKILL.md` lines 17 and 51 use the word "archive" for the source artifact, not for pack status: a source-retention choice of retain, archive separately, or remove. Unrelated to `status: archived` and left as written. Recorded so a later reference sweep does not read it as a missed deletion.

## P6: align the repository documents

Acceptance criteria:

- no document states a skill count that disagrees with `CONTRACT_SKILLS`
- `test_no_typographic_dashes` passes across every `*.md`, this pack included
- no document points at a deleted skill outside the deprecation records
- the lesson-entry rule is stated once outside the 11 pinned copies, in `contract/pack-contract.md`, and that one statement covers writing an entry, compacting it later, and keeping it after the mistake is resolved

Revision summary: the removal of the two duplicates P4 found was added here rather than given its own phase, per D10. The contract edit must land and be re-copied before either deletion, because both duplicates carry the after-resolution clause that the canonical sentence lacked.

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 16 |
| Packaged contract copies | 11 |
| Deleted skills still named outside `DESIGN.md` and this pack | none |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | lesson-entry sentence widened to say the entry stays even after the mistake is resolved. That is the one idea the two duplicates carried and the canonical sentence did not, which is why it had to land first. 82 lines |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced, `cmp` clean after the third contract edit |
| `baselinedocs-run/references/execution-contract.md` | duplicate lesson-entry statement replaced with a pointer |
| `baselinedocs-save/SKILL.md` | duplicate lesson-entry statement replaced with a pointer |
| `skill-consolidation.hallucination.md` | every decision recorded with its rejected alternatives |
| `AGENTS.md` | pack-writing skill count corrected in two places, stated as 14 at `cded242` when the real figure was 13, and 11 as at this phase. One pointer added to `Conventions` |
| `DESIGN.md` | 261 to 366 lines. Three rows added to `Decision Summary`, the `resume-snapshot` justification corrected, the pointer criterion in `Deferred Work` replaced with D1, deprecation records added for `sync-decision` and `maintain-prune`, line 190 corrected where it credited `maintain-compact` with a prohibition P4 moved into the contract, and two new sections added, `Skill Consolidation` and `Detect And Repair` |
| `README.md` | already correct. The `Agent-Selected Skills` table had been updated by P1, P2, and P3 as each landed, and the sections those edits did not touch carried no stale count or skill name |

Both duplicates were replaced by a one-line pointer rather than deleted outright. Each sat immediately after an instruction it qualified: "a lesson entry is not a diary entry" follows "do not keep a diary", and "not a transcript of an attempt" follows "store outcomes, not a transcript of attempts". Deleting the qualifier would have left the neighbouring instruction over-applied, which is a different defect from the duplication being removed. The pointer carries no rule text, so there is nothing left to drift.

Revision summary: the acceptance criterion requiring the rule to be stated once outside the pinned copies needed one qualification. `DESIGN.md` states it as well, under `Evidence Retention`, and that is correct rather than a violation: `DESIGN.md` does not ship and no agent can open it, so it explains rules instead of enforcing them. The criterion constrains files a running agent reads.

`AGENTS.md` gained a pointer beyond the stated deliverables. Two of the alternatives rejected in D1 are the kind a contributor would propose again on sight, and `AGENTS.md` is what a contributor reads before touching a skill folder, so a one-line pointer there is what makes the rejection reachable at the moment it matters.

## P7: correct the sync and audit model, add the pointers it exposed

Opened when Q3 was answered. No skill is merged, added, or renamed; the change is to the model and to four routing pointers. Reasoning is in D12.

Acceptance criteria:

- no document describes the five skills as one axis across comparison scopes
- every empty cell has a recorded reason it stays empty, and the reasons are not the same reason
- `sync-codebase` and `sync-decisions` are named in shipped text by at least one other skill
- no skill folder is added or removed

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills on disk | 15, unchanged |
| Packaged contract copies | 10, untouched. No contract edit in this phase |
| Inbound pointers, shipped text | `sync-codebase` and `sync-decisions` went from none to one each, both from `audit-drift` |
| Q3 | closed by D12. The namespace half of Q2 closed with it |

Changes:

| File | Change |
|---|---|
| `baselinedocs-audit-drift/SKILL.md` | description widened to match its own body, `Core Behavior` step 5 now names the repair skill for each finding, new provenance limit after the drift-signal line |
| `baselinedocs-sync-codebase/SKILL.md` | `Non-Goals` names the skill it routes to |
| `baselinedocs-sync-decisions/SKILL.md` | `Non-Goals` names the skill it routes to |
| `baselinedocs-sync-reconcile/SKILL.md` | `Non-Goals` names the skill it routes to |
| `DESIGN.md` | `Decision Summary` row, `Detect And Repair` rewritten with the two-axis model in place of the comparison-scope matrix, `Deferred Work` bullet replaced |
| `skill-consolidation.sourcecode.md` | matrix section replaced with the two-axis model |

The `audit-drift` description said the skill audits documents that have fallen behind "the code", while its own second step compares decision records and its own second sentence names decisions. The body was right and the first sentence was narrow. Widening it also fills the matrix cell that looked empty, which is why the model correction and the description fix belong in one phase.

The added provenance limit is the reason that fix is not cosmetic: a document whose `code_ref` is current can still describe an option a decision rejected, and it sorts to the bottom of a provenance-ordered list. Ranking by `code_ref` would therefore hide exactly the drift the widened description promises to find.

### Finding: one flagged defect was not a defect

`sync-reconcile` was flagged for not pointing back at `onboard` and `brief`, which both point at it. Checked and left alone. A pointer earns its place at the surface where a wrong choice is made, and nobody who has already selected `sync-reconcile` needs sending to `onboard`. The asymmetry is correct: `onboard` writes nothing so it must hand off, while `sync-reconcile` detects and repairs in one pass, so it has nothing to hand off. Recorded so the same flag is not raised again by the next reference sweep.

## P8: replace the installed skills, and pin the count

Two unrelated items, joined because both are what a repository change does not reach on its own: one is outside the repository, the other is prose the tests could not see.

Deliverables, each with the criterion it had to satisfy:

| Deliverable | Acceptance criterion |
|---|---|
| delete every `baselinedocs-*` folder from each host skills directory, then install from the local clone | every host directory holds exactly the 15 skills this repository defines, with no deleted skill remaining; installed contract copies byte-identical to `contract/pack-contract.md`; skills belonging to other families in those directories untouched |
| state the pack-writing skill count in one sentence in `AGENTS.md` and phrase the rest count-free | enforced by the test below, which fails on a second sentence as well as on a wrong number |
| add a test pinning that sentence against `CONTRACT_SKILLS`, failing on a second sentence as well as on a wrong number | the new test fails when the count is wrong, verified by making it wrong on purpose |
| record the rule in `AGENTS.md` conventions, where a contributor meets it before writing a second count | - |

### Checkpoint: complete

| Item | Result |
|---|---|
| Negative check | setting the count to 99 failed the new test, then restored |
| Host directories updated | `.claude`, `.agents`, `.kilocode`, `.kiro`, each independently holding a full copy. `.codex/skills` exists but was empty before and after |
| Installed before | 19 baselinedocs skills per directory, including all four `resume-*` and the four deleted here. Missing `adopt`, `onboard`, `brief`, `audit-claims`. Contract 46 lines |
| Installed after | 15 per directory, contract 82 lines, `cmp` identical to canonical |
| Preserved | the `terraform-*` skills in each directory, untouched |

The installed set was worse than the recorded risk described. It was not one generation behind: it predated the dissolution of the `resume` family, which `DESIGN.md` had recorded as finished before this pack opened, and it was missing three of the six user entrypoints entirely. `adopt`, `onboard`, and `brief` could not have fired on this machine at all.

Two host quirks worth recording. The directories are independent copies, not symlinks into a shared store, so each needed its own delete; `--copy` versus the default made no difference to that. Global install is refused by two hosts the installer knows about, which is reported per skill and is not a failure of the others.

Deleting before installing was deliberate. The installer adds and overwrites but does not remove, so an install alone would have left all eight deleted skills in place, still competing for selection. That is the D8 cost made concrete: a repository delete cannot reach an installed machine, and only an explicit delete on that machine can.

The install was made from an uncommitted working tree, which was the state of the repository at the time. That tree became `c6eb29a`, and every installed skill folder was diffed against the repository afterwards to confirm the two agree: they do, the only difference being a gitignored `__pycache__` that the installer does not copy. The check was worth running rather than assuming, because the edits made after the install touched `AGENTS.md`, `tests/`, and this pack, none of which ship inside a skill folder, and that is the reason the two still match.

Revision summary: the pack was set to `status: complete` in this phase, while Q2 and Q4 were still open, on the grounds that neither was in its scope. Both were closed afterwards in D13 and D14 without touching a skill file, so the status needed no revisiting.

## P9: ship the contract to the pack's only full reader

Opened by a real `onboard` run against an unrelated pack, which reported `onboard`'s absent contract copy as an unreadable file and concluded that future writes into that pack were blocked. Both halves were wrong, and the wrong conclusion was reachable because nothing recorded why the copy was absent. D16 carries the argument.

Acceptance criteria:

- the criterion for shipping the contract is recorded as a full read of the pack, not the act of writing
- `onboard` ships a byte-identical copy and gates on it with a wording whose precondition it can actually meet
- a read-only skill carrying the write gate fails a test
- `AGENTS.md` still states the pack-writing count in one sentence, and that count still means writers only
- 11 packaged contract copies, all byte-identical

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 22 passed, 35 subtests passed |
| Packaged contract copies | 11, `cmp` clean against canonical |
| Negative check, copy drift | appending a line to `onboard`'s copy failed `test_packaged_contract_matches_canonical_contract`, then restored |
| Negative check, wrong gate | injecting the write gate into `onboard` failed `test_read_only_skills_are_not_gated_on_writing`, then restored |
| Skills on disk | 15, unchanged. No skill added, deleted, or renamed |
| Installed copies, this machine | still 10 per host directory. Not reinstalled in this phase |

Changes:

| File | Change |
|---|---|
| `baselinedocs-onboard/references/pack-contract.md` | new, byte-identical to canonical. The 11th copy |
| `baselinedocs-onboard/SKILL.md` | read gate added above `Inputs`; new `Workflow` step 10 checking placement against the contract, with the old steps 10 and 11 renumbered; the drift-signal half of step 7 folded into a citation; `Output` gains a placement-findings line and the statement that a skill without a copy is not missing one |
| `tests/test_references.py` | `CONTRACT_SKILLS` split into `WRITER_SKILLS` and `READER_SKILLS`, both gate wordings pinned, new test that a reader carries no write gate, `AGENTS.md` count test repinned to `WRITER_SKILLS`, `test_no_typographic_dashes` scoped away from dot-directories |
| `AGENTS.md` | `The pack contract` states the criterion and both gate wordings and records that an absent copy is a decision; the folder-boundary bullet and the count convention repinned |
| `DESIGN.md` | `Decision Summary` row, and `Rule Placement` extended with the criterion, the per-use gate, three rejected alternatives, and what breaks if it is ignored |

The gate wording had to change with the copy. `onboard` never creates or edits a pack file, so the writers' sentence names a precondition it cannot meet, and an instruction that can never fire teaches the agent to read the gate as decoration. Its wording triggers on reporting the pack state instead, and the test asserts the write wording is absent rather than merely that some gate is present.

### Finding: the promised de-duplication was one sentence, not a sweep

The case for shipping the copy included an argument that `onboard`'s `SKILL.md` was paraphrasing the contract in several places and could shrink to pointers. Reading both texts side by side reduced that to one sentence: `onboard`'s "a moved repository is a signal" restated the contract's "a newer commit is a drift signal, not automatic proof of drift", and only the "not a verdict to investigate here" half was `onboard`'s own. That half is kept and the restated half now cites the contract.

The `Output` section's document names survived on purpose. They read as reporting order rather than as a second role list, and stripping them would have made the instruction vaguer without removing a fact. Recorded because the de-duplication argument was the strongest-sounding one on the table and it was the weakest in fact; the criterion argument in D16 is what carried the phase.

### Finding: the convention test swept content the repository does not own

`test_no_typographic_dashes` failed on 73 lines across more than twenty skill folders under `.agents/`, a host skills directory installed into this checkout and already excluded by `.gitignore`. None of it is authored here and none of it can be fixed here. The test skipped only `.git` and `.pytest_cache` by name, so anything else hidden at the root swept in. It now skips every dot-directory component, which is exact for this repository: all 38 of its own markdown files sit outside one.

Found while running P9's gate, unrelated to P9's change. Left in this phase rather than given its own, because a convention test that fails on foreign text is not a finding a later phase would inherit in a usable state.

## P10: report style shipped, hard-wrapping banned, and two questions opened from measured packs

Four items reported from real use of the family against unrelated packs. Two were decided and implemented here, D17 and D18; two were opened as questions rather than answered, Q6 and Q7, because both need a wider sample or a design not yet argued.

Acceptance criteria:

- every skill that names a pack element in its output ships `references/report-style.md` and gates on reading it
- the contract forbids hard-wrapping a paragraph
- both new fanouts fail a test when a copy drifts or a gate is missing
- the identifier scheme is recorded as an open question, not guessed at

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `report-style.md` copies | 14, `cmp` clean. Every skill except `setup-hooks`, which names no pack element |
| Contract copies | 11, re-synced after the hard-wrap edit, `cmp` clean |
| Negative check, copy drift | appending a line to `brief`'s copy failed `test_packaged_report_style_matches_canonical_and_reaches_every_reporter`, then restored |
| Negative check, missing gate | deleting the gate line from `brief` failed `test_every_reporter_gates_on_report_style`, then restored |
| Packs surveyed | 2 repositories, 16 documents, 12,932 lines. Read for structure and size only; nothing written to either |

Changes:

| File | Change |
|---|---|
| `contract/report-style.md` | new, 4 rules. Governs conversation only, and says so in its first line to keep the boundary with the contract explicit |
| `<skill>/references/report-style.md` | 14 copies, byte-identical |
| 14 `SKILL.md` files | one gate sentence each, placed above the first section, or directly under the contract gate where one exists |
| `contract/pack-contract.md` | hard-wrap prohibition added to the writing rules. 82 lines to 84 |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `tests/test_references.py` | two tests for the report-style fanout, one on byte-identity and audience, one on the gate |
| `AGENTS.md` | new `Report style` section stating the audience rule and why the asset is separate |
| `DESIGN.md` | two `Decision Summary` rows, and two new sections, `Report Style As A Shipped Asset` and `Hard-Wrapped Paragraphs` |

`setup-hooks` is the one exemption. It merges host configuration and never names a pack element, so a report-style copy there would be an asset nothing in the skill can act on.

### Finding: the survey disproved its own hypothesis

The survey was run to test a cheap explanation for oversized journals, that a large fraction was content the contract already forbids and that enforcement alone would shrink them. It is not there: across the two large journals, zero changelog-style revision notes, zero retry or attempt logs, zero `UPDATE:` or `EDIT:` markers, zero superseded markers. The bulk is journal content the contract requires be kept.

Recorded because the hypothesis was mine and it was wrong, and because its failure is what makes Q7 a structural question rather than an enforcement one. The measurements and the structural root cause both live in Q7; they are not restated here.

## P11: build the entry index on this pack as a Q7 trial

Approved as a trial only. The index goes into this pack's `hallucination` and nowhere else: the contract does not require one, no other pack gets one, and `onboard`'s reading rules are unchanged, so nothing yet consumes it. The point was to produce real numbers for a question that could not be settled on argument.

Acceptance criteria:

- one row per entry, stating what the entry is about and never its reasoning
- the table declares itself a trial under Q7, so a later reader does not mistake it for a contract requirement
- the before-and-after token cost of a scoped read is measured, not estimated

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| Rows | 21: D1 through D18, Q5 through Q7 |
| File cost, index alone | 317 lines and 41.8 KB to 347 lines and 44.3 KB. Plus 623 tokens. The document passed 370 lines once the trial write-up in Q7 landed, and a figure measured inside the document it measures cannot stay exact |
| Scoped read, table and open questions only | about 3,322 tokens, 28 percent of a full read, measured after the write-up landed |
| Scoped read, plus the four entries a contract-fanout task needs | about 5,842 tokens, 50 percent of a full read |
| Contract | unchanged. No new fanout, no new test |

Changes:

| File | Change |
|---|---|
| `skill-consolidation.hallucination.md` | `Entry index` section added above D1, with the rule that a row carries subject only and the note that it is a Q7 trial |
| `skill-consolidation.hallucination.md`, Q7 | trial result, the closed-to-open ratio measured across three journals, and the sequencing consequence it exposed |

The measurements and the reasoning both live in Q7. Not restated here.

### Finding: what decides the payoff is placement, not size

The trial's useful output was not the saving on this pack. It was that the saving depends on the ratio of closed decisions to open questions, because only a closed entry can be deferred to a row, and that ratio varies from 86 percent closed to 46 percent closed across three real journals. The pack that most needs the mechanism benefits least, and its ratio is bad because settled material sits under its open-questions heading. That is Q5 presenting as Q7, and it changes the order the two should be answered in. Recorded in Q7 with the numbers.

## P12: the entry index enters the contract

The trial in P11 produced numbers, and the numbers carried the decision. D19 records the argument, the threshold's calibration, and the three rejected alternatives, one of which was this phase's own recommendation.

Acceptance criteria:

- the contract requires an index above a stated threshold and omits it below
- the threshold cites what it was calibrated against, so it can be argued with rather than guessed at
- the contract states that no test verifies a row against its entry, rather than leaving that unsaid
- this pack's index stops describing itself as a trial

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `contract/pack-contract.md` | 84 lines to 98 |
| Contract copies | 11, re-synced, `cmp` clean |
| Index rows here | 22, after D19 got its own row |
| New tests | none. The one thing worth pinning cannot be pinned, and the structural half was declined |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | new `Entry index` section after the closed-decision rule: threshold, four required columns, the subject-only rule for a row, the unverifiability statement, and the heading-delimited precondition |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `skill-consolidation.hallucination.md` | index header now cites the contract instead of calling itself a trial; D19 added; Q7 narrowed to what `onboard` does with the index |
| `DESIGN.md` | `Decision Summary` row and a new `Entry Index` section |

The threshold is 40 KB or more than 20 entries, whichever comes first, and both numbers are stated because they measure different costs. Bytes measure what a read costs. Entry count measures what the index costs to maintain, which is the cost that does not scale down.

### Finding: the phase went against its own recommendation, on the record

This phase recommended accepting the unverifiable row while still pinning the structural half, since tests for a missing row, a row pointing at no entry, and a row longer than one line are cheap. The user chose discipline alone. Implemented as decided and recorded in D19 as a rejected alternative rather than as a disagreement, because the tests stay cheap to add later and because what they would not have caught is the only thing that matters here: whether a row's text is still true.

## P13: misfiled content gets owners, closing Q5

Q5 had been left open through P9 and P10 on the grounds that answering it needed either a widened skill trigger or a fourth owner clause in the contract, and that neither was in scope. P11's measurement overtook that: the repair returns more on a live pack than the mechanism P12 shipped. D20 carries the argument.

Acceptance criteria:

- the contract names an owner for content that is accurate but misfiled, without adding a skill
- `onboard` stops reporting that the finding has no owner
- the sub-question the rule does not settle is stated as still unsettled rather than quietly covered

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `contract/pack-contract.md` | 98 lines to 106 |
| Contract copies | 11, re-synced, `cmp` clean |
| Skills added or widened | none. Three existing triggers absorbed the case |
| Q5 | closed by D20. Its analysis moved into D20 rather than being deleted with its heading |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | new `Misfiled content` section after `Disproven claims`: owners, verbatim relocation, the inside-one-document form, and what it costs left alone |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `baselinedocs-onboard/SKILL.md` | step 10 now names the owner the contract gives, and covers settled material under an unsettled heading. It previously said the finding had no owner and warned against inventing one, which D20 made false |
| `skill-consolidation.hallucination.md` | D20 added, Q5's section removed with its content carried into D20, three index rows repointed from Q5 to D20 |
| `skill-consolidation.sourcecode.md` | the third finding type now shows its owners |
| `DESIGN.md` | `Decision Summary` row and a new `Misfiled Content` section |

### Finding: closing Q5 invalidated a sentence P9 had deliberately written

`onboard` step 10 carried a warning that a placement finding has no repair owner and that inventing one is how a reader starts moving content no skill was told to move. That was correct when P9 wrote it and false the moment D20 landed. It was found by grepping for the phrase rather than by remembering it, which is the only method that works: a rule written into a shipped skill to describe a gap becomes wrong when the gap closes, and nothing in the pack points from the closing decision back to the skill file that described the gap.

## P14: repair the contract heading, capture what the thread held

A `save` pass. Its first act was the mandatory full read of the contract, which found a structural defect P13 had introduced and shipped to all 11 copies. The rest of the phase captured reasoning that existed only in conversation.

### Checkpoint: complete

| Item | Result |
|---|---|
| Verification gate | 24 passed, 63 subtests passed |
| `## Conditional documents` | restored. It had been destroyed by P13's insertion, leaving `sourcecode` and `useguide` defined under `## Misfiled content` |
| Structure verified | each of the five role bullets listed with the heading above it, rather than checked by eye. All five sit under the correct heading |
| Contract copies | 11, re-synced, `cmp` clean |
| Index rows against entry headings | 24 rows, 24 headings, matched by count |
| Contract size | 106 lines to 108 |

Changes:

| File | Change |
|---|---|
| `contract/pack-contract.md` | `## Conditional documents` heading restored |
| `<skill>/references/pack-contract.md` | all 11 copies re-synced |
| `skill-consolidation.hallucination.md` | D21 records the heading defect as a lesson entry; Q8 opened for the within-entry label standard; Q6 expanded with the full proposed scheme, its seven rules, and its four rejected alternatives |

Nothing else was written. The four decisions the thread reached the edge of are recorded as open, not as decided, because the user has not answered them.

### Finding: every available signal said the broken contract was fine

The defect passed `cmp` across all 11 copies, which was accurate, and passed the suite at 24 tests. Both checks measure whether the copies agree with canonical. Neither can see a defect introduced into what they agree about, and the more copies there are the more reassuring a green result looks. D21 states the class rather than the incident: a byte-identity test protects a fanout, not a source.

It was found by reading the file top to bottom because the gate requires it, not by reading the diff. The diff showed a section correctly added; only the whole file showed a heading gone.

### Finding: one of this phase's own earlier claims was wrong

An earlier count in this thread reported D8, D9, and D15 as closed decisions missing required labels. Reading all three showed D15 is not a closed decision at all but a disproven-claim relocation, so the four-part rule does not apply to it and the count had used the wrong standard. D8 carries the consequence under a different label name. D9 is the only clear case. Corrected in Q8, where it changed the shape of the question: a label standard has to enumerate entry kinds before it can be enforced, and it therefore costs more than it first appeared to.

## Risks

| Risk | Detail |
|---|---|
| Installed skills are stale | Reopened by P9, exactly as this row predicted. P8 closed it on this machine; P9 then changed the repository, so all four host directories now hold 15 skills with 10 contract copies against the repository's 11, and their `onboard` carries no copy and no read gate. The drift is one phase wide and known, not discovered later, which is the only difference an install snapshot allows. |
| Direct delete cannot reach installed machines | Accepted under D8, and made concrete by P8's manual deletion of eight obsolete folders in each of four directories. |
| Uncommitted work is the only copy | Reopened for P9 alone. P1 through P8 are committed at `c6eb29a` on `main`; P9's changes sit in the working tree, uncommitted at the user's request. |
| The separate description batch closed empty | D9 split description sharpening into its own batch, for pairs sharing triggers while producing different outcomes. Its last candidate pair was `sync-codebase` against `audit-drift`, and D12 established the two are not on one axis. P7 gave each side a pointer to the other side of the work instead of rewriting either description to compete. No batch remains. |

## Next action

Four decisions are waiting on the user, and nothing else in this pack can proceed past them. They are stated here because a question the user has not answered is not a next action the pack can take on its own.

| Waiting on | Question | Recommendation on record |
|---|---|---|
| Q8 | fix the exact text of the required labels per entry kind in the contract, and test it | yes. It is the first structural rule in `hallucination` a machine could check, and it answers the readability objection that raised Q8 |
| Q8 | allow a compound reference such as `D19 / Rejected: mandatory in every pack` for citing a part of an entry | yes. A text reference fails loudly when the label changes; a renumbered identifier fails silently |
| Q6 | adopt the identifier scheme now, or keep waiting for further pack samples | adopt now. D19 put an index into the contract whose first column is an identifier, and that column has no defined format until this is settled |
| Q7 | which of the four options `onboard` takes for using the index | option four, entry-level scoping as the size gate's third outcome rather than the default read |

D9 also needs a decision that is not a design question: it is the one closed decision in this journal with no why, no consequence, and no rejected alternative. Filling those in means writing reasoning for a decision closed long ago, which the brownfield rule forbids reconstructing from inference, so the choice is repair it from the record or leave it non-conformant and say so. Q8 carries the detail.

Reinstalling the family on this machine remains outstanding. Deferred 2026-08-27 at the user's request, so the drift below is accepted knowingly rather than pending discovery. All four host directories hold P8's snapshot: 15 skills, 10 contract copies, and an `onboard` with neither the copy nor the read gate. Nothing on this machine is broken by that, because the criterion change only adds a capability, but a later `onboard` run here will behave as it did before P9 and will report the absent copy the same way. P9 was not reinstalled because installing is a machine action taken deliberately, not a side effect of a repository edit.

All fourteen phases are complete. P1 through P8 are committed at `c6eb29a` on `main`; P9 through P14 are uncommitted at the user's request. 15 skills, 11 packaged contract copies, 14 packaged report-style copies, 24 tests passing.

Three open questions are live in `skill-consolidation.hallucination.md`. Q5 was closed by D20 in P13. None of the three is answered anywhere else, so a reader looking for a position on them will not find one outside its entry:

| Question | Subject | Why it is open rather than decided |
|---|---|---|
| Q6 | what the element identifier scheme is, and whether the contract owns it | opened to wait for further pack samples. That reason has weakened: the index D19 requires has an identifier as its first column, and waiting leaves that column undefined |
| Q7 | what `onboard` does with the index, now that D19 settled the index itself | changing what `onboard` reads touches its central promise. Four options are recorded in the entry and none is chosen, so the index currently serves a human reader and saves no tokens |
| Q8 | the label standard inside an entry, and how many entry kinds `hallucination` holds | raised against Q6's proposal by the user. Answering it needs the entry kinds enumerated first, which is more work than the standard appeared to be |

The four original questions were all closed by decision, each with its rejected alternatives recorded:

| Question | Closed by | Outcome |
|---|---|---|
| Q1 archive destination | D11 | specifying it disproved the skill; deleted with its enum value and consumer |
| Q3 detect against repair | D12 | the matrix was drawn on an axis that does not separate the five skills; none merged |
| Q2 rename sweep | D13 | stops at the audit pair. `sync-reconcile` is reached by pointer, not by name |
| Q4 pack-level finished marker | D14 | `onboard` step 3 already selects only a sub-pack in progress |

The D9 description batch closes empty as well, for the reason in the Risks table above.

Three of the four closures reduced scope rather than adding it, and D13 and D14 changed no shipped file at all. What each leaves behind is the trigger that would justify reopening it, which is the part a later reader needs and the part a deleted question would not have carried.
