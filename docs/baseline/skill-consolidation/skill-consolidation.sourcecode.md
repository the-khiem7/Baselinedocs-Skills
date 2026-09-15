---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "sourcecode"
status: "active"
updated: "2026-08-27"
code_ref: "uncommitted"
---

# Skill Family Topology

The shape the consolidation acts on. Baseline measured at `cded242`; counts below track the working tree and are marked where a phase moved them.

## Folder shape

```text
<skill>/
  SKILL.md
  agents/
    openai.yaml
  references/     # report-style.md in every reporting skill; pack-contract.md when it writes or fully reads
```

A skill may rely only on files inside its own folder, because `npx skills add --skill <name>` installs one folder and nothing else travels with it. `contract/`, `hooks/`, `tests/`, and the repository documents do not ship.

## Classification

| Class | Count | Skills | `allow_implicit_invocation` |
|---|---|---|---|
| User entrypoints | 6 | `init`, `adopt`, `save`, `run`, `onboard`, `brief` | false |
| One-time administration | 0 | none (`setup-hooks` deleted in SC-D22) | - |
| Lifecycle, agent-selected | 8 | 3 sync, 2 audit, 2 maintain, `extract-wiki`. 11 at `cded242` | true |

`tests/test_skill_metadata.py` pins this: the 6 names in `ENTRYPOINTS` must disable implicit invocation and every other skill must enable it.

## Contract fanout

`contract/pack-contract.md` is the only definition of which baseline document owns which content. 11 skills each ship a byte-identical copy at `<skill>/references/pack-contract.md`, pinned by `tests/test_references.py`, because a skill cannot reach a sibling's files. 13 at `cded242`, 10 at `c6eb29a`.

| Carries a copy | Does not |
|---|---|
| `init`, `adopt`, `save`, `run`, `sync-codebase`, `sync-decisions`, `sync-reconcile`, `maintain-compact`, `maintain-split`, `extract-wiki`, `onboard` | `brief`, `audit-drift`, `audit-claims` |

The criterion is a full read of the pack, not the act of writing: the 10 writers qualify, and so does `onboard`, which writes nothing but reads every document and reports content sitting in a document whose role does not cover it. `brief` reads nothing in full and neither `audit` skill compares placement, so a copy there would let a skill report conformance it never checked.

Each of the 11 carries one gate sentence sending the agent to read the contract, in one of two pinned wordings: the writers trigger before creating or editing a pack file, `onboard` before reporting the pack state. `test_read_only_skills_are_not_gated_on_writing` asserts `onboard` does not carry the write wording, whose precondition it can never meet. That gate cannot live in the contract, because an agent that skipped the file never reaches the sentence telling it not to skip the file.

Editing the canonical file means re-copying it to all of them. SC-P2 added a section, SC-P4 rewrote a sentence, and SC-P5 removed an enum value, so any copy predating this pack is stale on three counts.

## Report style fanout

`contract/report-style.md` governs what the agent says to the user, and nothing about what goes inside a document. 14 skills ship a byte-identical copy at `<skill>/references/report-style.md`, every single skill in the family without exception.

Its audience is deliberately wider than the contract's, and the two sets are not nested the same way: `brief`, `audit-claims`, and `audit-drift` carry report style without carrying the contract, because each produces a user-facing report that cites identifiers while none of them writes a pack or reads one in full. SC-D17 records why merging the two files would force the wrong audience on one of them.

Each of the 14 carries a gate sentence triggering before it reports, pinned by `test_every_reporter_gates_on_report_style`, and the copies are pinned by `test_packaged_report_style_matches_canonical_and_reaches_every_reporter`, which also asserts the audience set rather than only comparing whatever copies happen to exist.

`baselinedocs-run` additionally ships `references/execution-contract.md`, which has no second copy anywhere.

## The sync and audit skills

Two groups on two different axes, not one detect/repair axis across comparison scopes. The earlier comparison-scope matrix is recorded as disproven in SC-D12; what follows is the shape the bodies actually have.

Report-only, separated by unit of analysis:

| Skill | Unit | Sources consulted |
|---|---|---|
| `audit-drift` | document | code changes after `code_ref`, document claims, decision records |
| `audit-claims` | claim | code, explicit decisions. Forbidden from using `code_ref` |

Writes, separated by trigger, which fixes blast radius:

| Skill | Triggered by | Touches | Sources consulted |
|---|---|---|---|
| `sync-codebase` | code changed | whole pack, one pass | code, inspected first |
| `sync-decisions` | a decision closed | only sections that decision reaches | the closed decisions |
| `sync-reconcile` | pack contradicts itself | only conflicting sections | the pack, with code and decisions as tiebreak |

Three of the five consult code and decisions both, which is why a comparison-scope axis cannot separate them.

Detect for a pack against itself has no dedicated skill because `onboard` and `brief` both report contradictions and route to `sync-reconcile`. Repair for a claim against evidence has none because the contract's disproven-claim rule already names its three owners.

SC-P9 added a third finding type, and SC-D20 gave it owners without adding a skill. `onboard` reports content sitting where the role lists do not put it, and the contract's misfiled-content rule names who moves it: `sync-decisions` when a decision settled what it was filed under, `sync-reconcile` when the misplacement already produced a contradiction, `save` when the current thread established where it belongs. The pattern follows the disproven-claims rule, which also names owners rather than occupying a matrix cell with a new skill.

## Pointer graph

Which skills are named inside another skill's shipped text. Recorded as topology only. Per SC-D1 this is not evidence about whether a skill is needed; a skill nothing points at may be missing a pointer, and its description can still be uncontested.

| Skill | Named by |
|---|---|
| `save` | `brief`, `init` |
| `onboard` | `brief`, `sync-codebase` |
| `brief` | `onboard` |
| `adopt` | `onboard` |
| `sync-reconcile` | `brief`, `onboard`, `audit-drift` |
| `sync-codebase` | `audit-drift`, `sync-decisions`, `sync-reconcile` |
| `sync-decisions` | `audit-drift`, `sync-codebase` |
| `audit-drift` | `brief`, `onboard`, `audit-claims` |
| `audit-claims` | `audit-drift` |
| `maintain-split` | `onboard` |
| `init`, `run`, `maintain-compact`, `extract-wiki` | nothing |

`sync-codebase` and `sync-decisions` moved out of the last row in SC-P7. Both were named by nothing, which under SC-D1 is a signal that a pointer is missing rather than that a skill is unnecessary, and SC-P7 acted on it that way: `audit-drift` now names all three repair skills when it recommends follow-up actions, and the write trio names whichever sibling owns the case it refuses.

At `cded242` the deleted `sync-decision` appeared here too, named only by `sync-decisions` in a mutual `Non-Goals` reference between the pair being merged.

The audit pair now carries a mutual reference of its own, added by SC-P3, and it does not mean the same thing. `sync-decision` and `sync-decisions` pointed at each other because neither description could settle which one applied; the pointers were a symptom of an undecidable pair. `audit-drift` and `audit-claims` point at each other to state the boundary in the surface that selects them, so the pointers are what makes the pair decidable. Same shape, opposite meaning: read a mutual disclaimer as a merge signal only when neither description states what separates the two.

`README.md` names `maintain-compact` in its trap table, but the README does not ship, so that reference does not exist at runtime.

## Frontmatter producers and consumers

| Value | Written by | Read by |
|---|---|---|
| `code_ref` | every pack-writing skill | `audit-drift`, `onboard` |

`status: archived` was the second row here, written by `maintain-archive` only and read by `onboard` only, as a default scope exclusion. That single-producer, single-consumer shape is what SC-D6 turned on and what SC-D11 removed: SC-P5 deleted the producer, the consumer, and the value together, so no orphaned half remains for a later contributor to complete.

`audit-claims` is absent from the `code_ref` row by rule, not by omission. SC-P3 forbids it from ranking or filtering claims by provenance, because a current `code_ref` does not make a claim supported and a stale one does not make it false. That rule is what keeps the audit pair on separate axes rather than on the same axis at two zoom levels.

## Test surface

| File | Pins |
|---|---|
| `test_references.py` | contract copies byte-identical to canonical, the right gate wording present in each and the write wording absent from a reader, the pack-writing skill count stated once in `AGENTS.md` and matching `WRITER_SKILLS`, no typographic dashes in any `*.md` this repository owns |
| `test_skill_metadata.py` | skill id matches folder name, `openai.yaml` names its own skill, only entrypoints disable implicit invocation |
| `test_checkpoint.py` | the Stop hook adapter contains no repository detection logic, and the prompt keeps its thread boundaries |
| `test_install_hooks.py` | packaged hook assets match canonical, installs are idempotent, existing host configuration preserved |
| `test_run_policy.py` | `baselinedocs-run` policy selection gate |

`test_no_typographic_dashes` globs every `*.md` under the repository root except those inside a dot-directory, so it covers this pack and skips a host skills directory installed into the checkout.
