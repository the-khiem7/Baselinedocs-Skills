---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "roadmap"
status: "complete"
updated: "2026-08-27"
code_ref: "uncommitted"
---

# Skill Consolidation Roadmap

Verification gate for every phase: `uvx pytest tests/ -q` green. The repository has no `pyproject.toml`, so `uv run python -m pytest` does not work.

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

Deliverables:

- delete `baselinedocs-sync-decision/`
- add the section-scope constraint to `baselinedocs-sync-decisions/SKILL.md`: patch only directly impacted sections, no broad unrelated rewrites
- remove the mutual `Non-Goals` line in `sync-decisions` that points at the deleted skill
- remove `"baselinedocs-sync-decision"` from `CONTRACT_SKILLS` in `tests/test_references.py`

Acceptance criteria:

- one skill covers both the single-decision and the multi-decision case
- no file in the repository names `baselinedocs-sync-decision` except this pack and `DESIGN.md`, which P6 rewrites
- 12 packaged contract copies remain, all byte-identical to `contract/pack-contract.md`

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 17, down from 18 |
| Packaged contract copies | 12, all byte-identical, pinned by `test_packaged_contract_matches_canonical_contract` |
| Residual references | `DESIGN.md` only, deferred to P6 by design |

Affected files:

- deleted `baselinedocs-sync-decision/` (3 files)
- `baselinedocs-sync-decisions/SKILL.md`: description, `Purpose`, `Use When`, `Core Behavior`, `Non-Goals`
- `tests/test_references.py`: `CONTRACT_SKILLS`
- `README.md`: `Agent-Selected Skills` sync row

Revision summary: the absorbed skill's trigger vocabulary was carried into the surviving description rather than dropped with the folder. Deleting a folder deletes a selection surface, and on hosts where `description` drives selection the words "atomic", "targeted", and "one specific" were the only route to the narrow case. This is part of the merge, not the separate description batch in D9.

Revision summary: `README.md` is edited by each deletion phase for its own row, while P6 keeps the counts, the criterion, and the deprecation record. P1's acceptance criteria had required a clean repository-wide reference check that P6 alone could not satisfy mid-sequence.

## P2: delete maintain-prune, add the relocation rule

Deliverables:

- delete `baselinedocs-maintain-prune/`
- add the disproven-claim relocation rule from D5 to `contract/pack-contract.md`
- copy the canonical contract to all remaining pack-writing skills
- remove `"baselinedocs-maintain-prune"` from `CONTRACT_SKILLS`

Acceptance criteria:

- the disproven-claim case has a named owner in the contract
- no file names `baselinedocs-maintain-prune` except this pack and the deprecation record P6 adds to `DESIGN.md`
- 11 packaged contract copies remain, all byte-identical

Risk: `maintain-prune` is named by nothing else in the repository, verified at `cded242`, so no pointer needs repair. Re-verify before deleting rather than trusting this line.

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 16, down from 17 |
| Packaged contract copies | 11, all byte-identical, re-synced from canonical after the contract edit |
| `contract/pack-contract.md` | 74 lines to 82 |
| Residual references | this pack only. `DESIGN.md` never named `maintain-prune`, so P6 adds a deprecation record rather than repairing one |

Affected files:

- `contract/pack-contract.md`: new `Disproven claims` section, placed after `Reasoning ownership`
- all 11 remaining `<skill>/references/pack-contract.md` re-synced
- deleted `baselinedocs-maintain-prune/` (3 files)
- `tests/test_references.py`: `CONTRACT_SKILLS`
- `README.md`: `Agent-Selected Skills` maintain row

The contract rule was written before the folder was deleted, so the disproven-claim case had a named owner at every point in the sequence. Its closing line is the load-bearing one: nothing in an active pack is removed on the grounds that it is no longer true, it is relocated. That is the general prohibition replacing the deleted skill, and it holds whether or not a future reader knows the skill existed.

## P3: rename audit-verify to audit-claims

Deliverables:

- rename the folder to `baselinedocs-audit-claims/`
- update `name:` in `SKILL.md`, plus `display_name`, `short_description`, and `default_prompt` in `agents/openai.yaml`
- rewrite both audit descriptions on the document-versus-claim axis from D3

Acceptance criteria:

- neither audit description can be satisfied by the other skill's question
- `test_skill_ids_match_folders` and `test_openai_prompts_name_the_skill` pass
- `allow_implicit_invocation: true` preserved, since this is not a user entrypoint

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 16, unchanged. A rename, not a deletion |
| Dangling pointers | none. All three inbound pointers, in `onboard` and `brief`, name `audit-drift`, which kept its name. `audit-verify` was named by nothing |
| Residual references | this pack only |

Affected files:

- `baselinedocs-audit-verify/` renamed to `baselinedocs-audit-claims/`
- `baselinedocs-audit-claims/SKILL.md`: `name`, description, H1, `Core Behavior` step 3, new provenance rule, `Non-Goals`
- `baselinedocs-audit-claims/agents/openai.yaml`: all three interface fields
- `baselinedocs-audit-drift/SKILL.md`: description, `Non-Goals`
- `README.md`: `Agent-Selected Skills` audit row

Each description now names the other skill for the question it does not answer. A routing pointer placed in the description reaches the selection surface itself, which is where the wrong choice was being made; the same sentence in the body would only be read after the choice was already wrong.

`Core Behavior` step 3 classified a claim as "false/outdated" before this phase. "Outdated" is drift vocabulary: it implies a claim was true and stopped being true, when an unsupported claim was never true at all. Changed to "contradicted by evidence", and a rule was added forbidding this skill from ranking claims by `code_ref` at all. Without that rule the two audit skills sit on one axis at two zoom levels, which is the state D3 rejected.

## P4: give compact its revert gate

Deliverables:

- write the D7 gate into `baselinedocs-maintain-compact/SKILL.md` with its WHY clause

Acceptance criteria:

- the body states the revert condition and the cost comparison, not only the goal
- the gate is stated as a pass or revert test, not as advice

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 16, unchanged |
| Packaged contract copies | 11, re-synced after the second contract edit, `cmp` clean |
| `contract/pack-contract.md` | 82 lines, unchanged in count. One sentence rewritten, not added |

Affected files:

- `contract/pack-contract.md`: the lesson-entry rule now binds writing and later compaction in one sentence, absorbing the wording that lived in `maintain-compact`
- all 11 `<skill>/references/pack-contract.md` re-synced
- `baselinedocs-maintain-compact/SKILL.md`: description, `Core Behavior` step 1, new `Gate` section, deleted lesson-entry restatement, new `Non-Goals` pointer

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

Deliverables:

- delete `baselinedocs-maintain-archive/`
- remove `archived` from the `status` enum in `contract/pack-contract.md`, then re-copy to all remaining pack-writing skills
- remove `"baselinedocs-maintain-archive"` from `CONTRACT_SKILLS`
- remove the archived-material exclusion from `baselinedocs-onboard/SKILL.md`, and make the retained-source-material rule beside it self-standing, since it read "on the same terms" and its terms are being deleted
- replace `maintain-compact`'s `not for archiving completed phases` non-goal with a direct prohibition on moving content out of the active pack, so the deletion does not silently grant compact the relocation right D11 rejected
- `README.md`, `AGENTS.md`, `DESIGN.md` aligned

Acceptance criteria:

- no file in the repository names `baselinedocs-maintain-archive` except this pack and the `DESIGN.md` record
- no producer and no consumer of `status: archived` remains, and the value is gone from the enum
- 10 packaged contract copies, all byte-identical
- `maintain-compact` still forbids relocation after the skill that owned it is gone

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 15, down from 16 |
| Packaged contract copies | 10, `cmp` clean after the fourth contract edit |
| `contract/pack-contract.md` | 82 lines. One enum value removed, no line count change |
| `status: archived` | no producer, no consumer, not in the enum |
| Residual references | this pack and `DESIGN.md`'s deletion record only |

Affected files:

- deleted `baselinedocs-maintain-archive/` (3 files)
- `contract/pack-contract.md`: `status` enum
- all 10 `<skill>/references/pack-contract.md` re-synced
- `tests/test_references.py`: `CONTRACT_SKILLS`
- `baselinedocs-onboard/SKILL.md`: `Inputs`, and two `Reading Rules` lines merged into one
- `baselinedocs-maintain-compact/SKILL.md`: `Non-Goals`
- `README.md`: `Agent-Selected Skills` maintain row
- `AGENTS.md`: pack-writing count in four places, not two
- `DESIGN.md`: `Decision Summary` row, `Onboard Scope Gate` paragraph removed and its principle moved to the source-material rule, `Skill Consolidation` count and table row, `Why archive was kept` replaced by `Why archive was deleted`, `Deferred Work` bullet replaced

Revision summary: `AGENTS.md` still said 14 in two further places, at `The pack contract` bullets "copy it to all 14" and "Each of the 14". P6 corrected the two prose mentions and missed these, because it searched for the sentence it knew about rather than for the number. All four now read 10.

Revision summary: the compact non-goal was replaced rather than deleted. It had named `maintain-archive` to mark a boundary, and deleting the line with the skill would have removed the prohibition along with the pointer, silently handing compact the relocation right D11 records as rejected. Same shape as the P6 pointer replacements: when a line names something being deleted, check whether the line is a pointer or a rule wearing a pointer's clothes.

### Finding: the last mention of archiving in shipped text

`baselinedocs-adopt/SKILL.md` lines 17 and 51 use the word "archive" for the source artifact, not for pack status: a source-retention choice of retain, archive separately, or remove. Unrelated to `status: archived` and left as written. Recorded so a later reference sweep does not read it as a missed deletion.

## P6: align the repository documents

Deliverables:

- `contract/pack-contract.md`: widen the lesson-entry sentence to say the entry stays even after the mistake is resolved, then re-copy to all 11 skills. This is the one idea the two duplicates carry that the canonical sentence does not
- delete the duplicate lesson-entry statement in `baselinedocs-run/references/execution-contract.md`
- delete the duplicate lesson-entry statement in `baselinedocs-save/SKILL.md`
- `DESIGN.md`: replace the pointer criterion in `Deferred Work` with D1, record every decision in `skill-consolidation.hallucination.md` with its rejected alternatives, add deprecation records for `sync-decision` and `maintain-prune`, and correct line 190, which credits `maintain-compact` with a prohibition P4 moved into the contract
- `AGENTS.md`: correct the pack-writing skill count, stated as 14 in two places at `cded242`, actually 13 then and 11 now
- `README.md`: check the sections the per-phase edits did not touch. The `Agent-Selected Skills` table was updated by P1, P2, and P3 as each landed

Acceptance criteria:

- no document states a skill count that disagrees with `CONTRACT_SKILLS`
- `test_no_typographic_dashes` passes across every `*.md`, this pack included
- no document points at a deleted skill outside the deprecation records
- the lesson-entry rule is stated once outside the 11 pinned copies, in `contract/pack-contract.md`, and that one statement covers writing an entry, compacting it later, and keeping it after the mistake is resolved

Revision summary: the duplicate removals were added here rather than given their own phase, per D10. The contract edit must land and be re-copied before either deletion, because both duplicates carry the after-resolution clause that the canonical sentence currently lacks.

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 16 |
| Packaged contract copies | 11, `cmp` clean after the third contract edit |
| `contract/pack-contract.md` | 82 lines |
| `DESIGN.md` | 261 to 366 lines |
| Deleted skills still named outside `DESIGN.md` and this pack | none |
| `README.md` | already correct. The per-phase table edits in P1, P2, and P3 had covered it, and no count or skill name elsewhere was stale |

Affected files:

- `contract/pack-contract.md`: lesson-entry sentence now also covers keeping the entry after the mistake is resolved
- all 11 `<skill>/references/pack-contract.md` re-synced
- `baselinedocs-run/references/execution-contract.md`: duplicate replaced with a pointer
- `baselinedocs-save/SKILL.md`: duplicate replaced with a pointer
- `DESIGN.md`: three rows added to `Decision Summary`, the `resume-snapshot` justification corrected, the `Deferred Work` bullet replaced, and two new sections, `Skill Consolidation` and `Detect And Repair`
- `AGENTS.md`: the pack-writing count corrected in two places, and one pointer added to `Conventions`

Both duplicates were replaced by a one-line pointer rather than deleted outright. Each sat immediately after an instruction it qualified: "a lesson entry is not a diary entry" follows "do not keep a diary", and "not a transcript of an attempt" follows "store outcomes, not a transcript of attempts". Deleting the qualifier would have left the neighbouring instruction over-applied, which is a different defect from the duplication being removed. The pointer carries no rule text, so there is nothing left to drift.

Revision summary: the acceptance criterion requiring the rule to be stated once outside the pinned copies needed one qualification. `DESIGN.md` states it as well, under `Evidence Retention`, and that is correct rather than a violation: `DESIGN.md` does not ship and no agent can open it, so it explains rules instead of enforcing them. The criterion constrains files a running agent reads.

`AGENTS.md` gained a pointer beyond the stated deliverables. Two of the alternatives rejected in D1 are the kind a contributor would propose again on sight, and `AGENTS.md` is what a contributor reads before touching a skill folder, so a one-line pointer there is what makes the rejection reachable at the moment it matters.

## P7: correct the sync and audit model, add the pointers it exposed

Opened when Q3 was answered. No skill is merged, added, or renamed; the change is to the model and to four routing pointers. Reasoning is in D12.

Deliverables:

- replace the comparison-scope matrix in `DESIGN.md` and in this pack's `sourcecode` with the two-axis model
- `audit-drift` step 5 names the repair skill for each finding
- `sync-codebase`, `sync-decisions`, `sync-reconcile` non-goals name the skill they route to
- `audit-drift` description widened to match its own body, which already compares decision records

Acceptance criteria:

- no document describes the five skills as one axis across comparison scopes
- every empty cell has a recorded reason it stays empty, and the reasons are not the same reason
- `sync-codebase` and `sync-decisions` are named in shipped text by at least one other skill
- no skill folder is added or removed

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 20 passed, 23 subtests passed |
| Skills on disk | 15, unchanged |
| Packaged contract copies | 10, untouched. No contract edit in this phase |
| Inbound pointers, shipped text | `sync-codebase` and `sync-decisions` went from none to one each, both from `audit-drift` |
| Q3 | closed by D12. The namespace half of Q2 closed with it |

Affected files:

- `baselinedocs-audit-drift/SKILL.md`: description, `Core Behavior` step 5, new provenance limit after the drift-signal line
- `baselinedocs-sync-codebase/SKILL.md`: `Non-Goals`
- `baselinedocs-sync-decisions/SKILL.md`: `Non-Goals`
- `baselinedocs-sync-reconcile/SKILL.md`: `Non-Goals`
- `DESIGN.md`: `Decision Summary` row, `Detect And Repair` rewritten, `Deferred Work` bullet replaced
- `skill-consolidation.sourcecode.md`: matrix section replaced

The `audit-drift` description said the skill audits documents that have fallen behind "the code", while its own second step compares decision records and its own second sentence names decisions. The body was right and the first sentence was narrow. Widening it also fills the matrix cell that looked empty, which is why the model correction and the description fix belong in one phase.

The added provenance limit is the reason that fix is not cosmetic: a document whose `code_ref` is current can still describe an option a decision rejected, and it sorts to the bottom of a provenance-ordered list. Ranking by `code_ref` would therefore hide exactly the drift the widened description promises to find.

### Finding: one flagged defect was not a defect

`sync-reconcile` was flagged for not pointing back at `onboard` and `brief`, which both point at it. Checked and left alone. A pointer earns its place at the surface where a wrong choice is made, and nobody who has already selected `sync-reconcile` needs sending to `onboard`. The asymmetry is correct: `onboard` writes nothing so it must hand off, while `sync-reconcile` detects and repairs in one pass, so it has nothing to hand off. Recorded so the same flag is not raised again by the next reference sweep.

## P8: replace the installed skills, and pin the count

Two unrelated items, joined because both are what a repository change does not reach on its own: one is outside the repository, the other is prose the tests could not see.

Deliverables:

- delete every `baselinedocs-*` folder from each host skills directory, then install from the local clone
- state the pack-writing skill count in one sentence in `AGENTS.md` and phrase the rest count-free
- add a test pinning that sentence against `CONTRACT_SKILLS`, failing on a second sentence as well as on a wrong number
- record the rule in `AGENTS.md` conventions, where a contributor meets it before writing a second count

Acceptance criteria:

- every host directory holds exactly the 15 skills this repository defines, with no deleted skill remaining
- installed contract copies are byte-identical to `contract/pack-contract.md`
- the new test fails when the count is wrong, verified by making it wrong on purpose
- skills belonging to other families in those directories are untouched

### Checkpoint: complete

| Item | Result |
|---|---|
| Evidence | `uvx pytest tests/ -q`: 21 passed, 23 subtests passed. Negative check run: setting the count to 99 failed the new test, then restored |
| Host directories updated | `.claude`, `.agents`, `.kilocode`, `.kiro`, each independently holding a full copy. `.codex/skills` exists but was empty before and after |
| Installed before | 19 baselinedocs skills per directory, including all four `resume-*` and the four deleted here. Missing `adopt`, `onboard`, `brief`, `audit-claims`. Contract 46 lines |
| Installed after | 15 per directory, contract 82 lines, `cmp` identical to canonical |
| Preserved | the `terraform-*` skills in each directory, untouched |

The installed set was worse than the recorded risk described. It was not one generation behind: it predated the dissolution of the `resume` family, which `DESIGN.md` had recorded as finished before this pack opened, and it was missing two of the six user entrypoints entirely. `onboard` and `brief` could not have fired on this machine at all.

Two host quirks worth recording. The directories are independent copies, not symlinks into a shared store, so each needed its own delete; `--copy` versus the default made no difference to that. Global install is refused by two hosts the installer knows about, which is reported per skill and is not a failure of the others.

Deleting before installing was deliberate. The installer adds and overwrites but does not remove, so an install alone would have left all eight deleted skills in place, still competing for selection. That is the D8 cost made concrete: a repository delete cannot reach an installed machine, and only an explicit delete on that machine can.

Revision summary: the pack was set to `status: complete` in this phase. Q2 and Q4 remain open and do not block it, because neither is in this pack's scope: Q2 is a naming question the pack narrowed but never owned, and Q4 was surfaced by P5 as a consequence to record rather than a deliverable. A pack whose declared scope is delivered is complete even while it names questions for someone else.

## Risks

| Risk | Detail |
|---|---|
| Installed skills are stale | Closed by P8 on this machine, all four host directories. It stays live everywhere else, and it returns here the moment the repository changes again: an install is a snapshot, so this repository and any machine drift apart from the next edit onward. |
| Direct delete cannot reach installed machines | Accepted under D8, and confirmed by P8, which had to delete eight obsolete folders by hand in each of four directories because the installer adds and overwrites but never removes. |
| Uncommitted work is the only copy | Every change in this pack lives in one working tree, per the commit policy chosen for this run, and P8 installed from that working tree rather than from a commit. Losing the tree loses the repository state and leaves four machines running skills that no source matches. |
| The separate description batch closed empty | D9 split description sharpening into its own batch. Its last candidate pair was `sync-codebase` against `audit-drift`, and D12 established the two are not on one axis. P7 gave each side a pointer to the other instead of rewriting either description to compete. No batch remains. |

## Next action

Commit. Every change this pack made lives in one uncommitted working tree, and P8 installed four machine copies from it, so the tree is now the only source those installs match. That was the policy chosen when the run started and it has outlived its purpose.

All eight phases are complete. 15 skills, 10 packaged contract copies, 21 tests passing.

Nothing is blocked. Two questions stay open, both narrow and neither belonging to this pack's scope:

| | Question | Size |
|---|---|---|
| Q2 | rename `sync-reconcile` to name what it reconciles | one skill, and the rename cost in D8 is the whole argument |
| Q4 | a pack-level finished marker `onboard` can skip | three lines plus a contract re-copy, and it only pays off on a multi-pack initiative |

The D9 description batch closes empty. It existed for pairs sharing triggers while producing different outcomes; the last candidate was `sync-codebase` against `audit-drift`, and D12 established they are not on one axis and gave each a pointer to the other side of the work.
