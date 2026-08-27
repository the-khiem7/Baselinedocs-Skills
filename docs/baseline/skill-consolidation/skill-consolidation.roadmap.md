---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "roadmap"
status: "complete"
updated: "2026-08-27"
code_ref: "c6eb29a"
---

# Skill Consolidation Roadmap

Verification gate for every phase: `uvx pytest tests/ -q` green. The repository has no `pyproject.toml`, so `uv run python -m pytest` does not work. Every checkpoint below met the gate: 20 passed and 23 subtests passed for P1 through P7, and 21 passed and 23 subtests for P8 once the test it adds landed.

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
| `AGENTS.md` | pack-writing skill count corrected in two places, stated as 14 at `cded242` when the real figure was 13 and is now 11. One pointer added to `Conventions` |
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

## Risks

| Risk | Detail |
|---|---|
| Installed skills are stale | Closed by P8 on this machine, all four host directories. It stays live everywhere else, and it returns here the moment the repository changes again: an install is a snapshot, so this repository and any machine drift apart from the next edit onward. |
| Direct delete cannot reach installed machines | Accepted under D8, and made concrete by P8's manual deletion of eight obsolete folders in each of four directories. |
| Uncommitted work is the only copy | Closed. The work is committed at `c6eb29a` on `main`, and P8's post-install diff confirms every installed skill folder matches it, so the four machine copies now have a source. |
| The separate description batch closed empty | D9 split description sharpening into its own batch, for pairs sharing triggers while producing different outcomes. Its last candidate pair was `sync-codebase` against `audit-drift`, and D12 established the two are not on one axis. P7 gave each side a pointer to the other side of the work instead of rewriting either description to compete. No batch remains. |

## Next action

None. The pack is closed.

All eight phases are complete, committed at `c6eb29a` on `main`. 15 skills, 10 packaged contract copies, 21 tests passing, and the four installed host copies verified identical to the repository.

No open questions remain. All four were closed by decision, each with its rejected alternatives recorded:

| Question | Closed by | Outcome |
|---|---|---|
| Q1 archive destination | D11 | specifying it disproved the skill; deleted with its enum value and consumer |
| Q3 detect against repair | D12 | the matrix was drawn on an axis that does not separate the five skills; none merged |
| Q2 rename sweep | D13 | stops at the audit pair. `sync-reconcile` is reached by pointer, not by name |
| Q4 pack-level finished marker | D14 | `onboard` step 3 already selects only a sub-pack in progress |

The D9 description batch closes empty as well, for the reason in the Risks table above.

Three of the four closures reduced scope rather than adding it, and D13 and D14 changed no shipped file at all. What each leaves behind is the trigger that would justify reopening it, which is the part a later reader needs and the part a deleted question would not have carried.
