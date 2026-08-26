---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "roadmap"
status: "active"
updated: "2026-08-26"
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
| P5 | `maintain-archive` destination specified | D6 | Q1 | blocked |
| P6 | `DESIGN.md`, `AGENTS.md`, `README.md` aligned to the end state, and the last duplicate rule statements removed | D1, D8, D9, D10 | P1, P2, P3, P4 | complete |

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

## P5: specify the archive destination

Blocked on Q1. Do not start by choosing a path.

Deliverables:

- state the destination path and naming convention in `baselinedocs-maintain-archive/SKILL.md`

Acceptance criteria:

- two independent runs would archive the same content to the same location
- the destination is readable from the skill body without inference

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

## Risks

| Risk | Detail |
|---|---|
| Installed skills are stale | The skills installed on this machine are an older generation than this repository. The installed `baselinedocs-init` routes to a `resume` family that no longer exists here and ships a 44-line contract against this repository's 74-line canonical file. A `baselinedocs` skill invoked in a later thread reads the installed copy. Verify any pack file written that way against `contract/pack-contract.md` here. |
| Direct delete cannot reach installed machines | Accepted under D8. A removed skill already installed elsewhere keeps competing for selection there. |
| The separate description batch may be empty | D9 splits description sharpening into its own batch. After P2 deletes `maintain-prune`, the only overlapping-trigger pair left is `sync-codebase` against `audit-drift`, which Q3 covers. Revisit after P6 rather than assuming the batch still has content. |

## Next action

Answer Q1, then execute P5. That is the only work left in this pack.

Q1 asks where an archived phase is written. `maintain-archive` is kept on the condition that this is stated, so until it is answered the skill is documented as incomplete rather than working, and `onboard` excludes a category nothing reliably produces.

The recommendation on file is a subdirectory, `<pack>/archive/`, one file per archived phase, each with `status: archived` frontmatter and a link from the active roadmap. The reason is mechanical: `onboard` excludes archived material by skipping a whole file, so a section marked archived inside an active document is still read, and the exclusion rule does nothing. The alternative to weigh against it is exactly that in-place variant, which costs no new files but gives up the exclusion.

Everything else is finished. P1 through P4 and P6 are complete, all 20 tests pass, and no changes are committed, per the commit policy chosen for this run.
