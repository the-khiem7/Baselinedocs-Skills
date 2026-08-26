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
| P3 | `audit-verify` renamed `audit-claims`, both audit descriptions rewritten | D3 | - | planned |
| P4 | `maintain-compact` carries the revert gate | D7 | - | planned |
| P5 | `maintain-archive` destination specified | D6 | Q1 | blocked |
| P6 | `DESIGN.md`, `AGENTS.md`, `README.md` aligned to the end state | D1, D8, D9 | P1, P2, P3 | planned |

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

## P4: give compact its revert gate

Deliverables:

- write the D7 gate into `baselinedocs-maintain-compact/SKILL.md` with its WHY clause

Acceptance criteria:

- the body states the revert condition and the cost comparison, not only the goal
- the gate is stated as a pass or revert test, not as advice

## P5: specify the archive destination

Blocked on Q1. Do not start by choosing a path.

Deliverables:

- state the destination path and naming convention in `baselinedocs-maintain-archive/SKILL.md`

Acceptance criteria:

- two independent runs would archive the same content to the same location
- the destination is readable from the skill body without inference

## P6: align the repository documents

Deliverables:

- `DESIGN.md`: replace the pointer criterion in `Deferred Work` with D1, and record every decision in `skill-consolidation.hallucination.md` with its rejected alternatives
- `AGENTS.md`: correct the pack-writing skill count, stated as 14 in two places at `cded242` and actually 13 before this work
- `README.md`: update the `Agent-Selected Skills` table

Acceptance criteria:

- no document states a skill count that disagrees with `CONTRACT_SKILLS`
- `test_no_typographic_dashes` passes across every `*.md`, this pack included
- no document points at a deleted skill outside the deprecation record

## Risks

| Risk | Detail |
|---|---|
| Installed skills are stale | The skills installed on this machine are an older generation than this repository. The installed `baselinedocs-init` routes to a `resume` family that no longer exists here and ships a 44-line contract against this repository's 74-line canonical file. A `baselinedocs` skill invoked in a later thread reads the installed copy. Verify any pack file written that way against `contract/pack-contract.md` here. |
| Direct delete cannot reach installed machines | Accepted under D8. A removed skill already installed elsewhere keeps competing for selection there. |
| The separate description batch may be empty | D9 splits description sharpening into its own batch. After P2 deletes `maintain-prune`, the only overlapping-trigger pair left is `sync-codebase` against `audit-drift`, which Q3 covers. Revisit after P6 rather than assuming the batch still has content. |

## Next action

Execute P3. Rename `baselinedocs-audit-verify/` to `baselinedocs-audit-claims/`, update `name:` in its `SKILL.md` and all three fields in its `agents/openai.yaml`, rewrite both audit descriptions on the document-versus-claim axis from D3, update the `README.md` audit row, then run `uvx pytest tests/ -q`.

`audit-drift` is named in shipped text by `onboard` and `brief`; `audit-verify` is named by nothing. Verify both before editing, because the rename must not leave a pointer dangling and the description rewrite touches a skill two others reference by name.
