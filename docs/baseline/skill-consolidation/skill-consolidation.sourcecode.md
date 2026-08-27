---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "sourcecode"
status: "complete"
updated: "2026-08-27"
code_ref: "c6eb29a"
---

# Skill Family Topology

The shape the consolidation acts on. Baseline measured at `cded242`; counts below track the working tree and are marked where a phase moved them.

## Folder shape

```text
<skill>/
  SKILL.md
  agents/
    openai.yaml
  references/     # only when the skill writes into a pack
```

A skill may rely only on files inside its own folder, because `npx skills add --skill <name>` installs one folder and nothing else travels with it. `contract/`, `hooks/`, `tests/`, and the repository documents do not ship.

## Classification

| Class | Count | Skills | `allow_implicit_invocation` |
|---|---|---|---|
| User entrypoints | 6 | `init`, `adopt`, `save`, `run`, `onboard`, `brief` | false |
| One-time administration | 1 | `setup-hooks` | false |
| Lifecycle, agent-selected | 8 | 3 sync, 2 audit, 2 maintain, `extract-wiki`. 11 at `cded242` | true |

`tests/test_skill_metadata.py` pins this: the 7 names in `ENTRYPOINTS` must disable implicit invocation and every other skill must enable it.

## Contract fanout

`contract/pack-contract.md` is the only definition of which baseline document owns which content. 10 pack-writing skills each ship a byte-identical copy at `<skill>/references/pack-contract.md`, pinned by `tests/test_references.py`, because a skill cannot reach a sibling's files. 13 at `cded242`.

| Carries a copy | Does not |
|---|---|
| `init`, `adopt`, `save`, `run`, `sync-codebase`, `sync-decisions`, `sync-reconcile`, `maintain-compact`, `maintain-split`, `extract-wiki` | `onboard`, `brief`, `setup-hooks`, `audit-drift`, `audit-claims` |

Skills that only read a pack carry no copy. Each of the 10 also carries one gate sentence sending the agent to read the contract; that gate cannot live in the contract, because an agent that skipped the file never reaches the sentence telling it not to skip the file.

Editing the canonical file means re-copying it to all 10. P2 added a section, P4 rewrote a sentence, and P5 removed an enum value, so any copy predating this pack is stale on three counts.

`baselinedocs-run` additionally ships `references/execution-contract.md`, which has no second copy anywhere.

## The sync and audit skills

Two groups on two different axes, not one detect/repair axis across comparison scopes. The earlier comparison-scope matrix is recorded as disproven in D12; what follows is the shape the bodies actually have.

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

## Pointer graph

Which skills are named inside another skill's shipped text. Recorded as topology only. Per D1 this is not evidence about whether a skill is needed; a skill nothing points at may be missing a pointer, and its description can still be uncontested.

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
| `init`, `run`, `setup-hooks`, `maintain-compact`, `extract-wiki` | nothing |

`sync-codebase` and `sync-decisions` moved out of the last row in P7. Both were named by nothing, which under D1 is a signal that a pointer is missing rather than that a skill is unnecessary, and P7 acted on it that way: `audit-drift` now names all three repair skills when it recommends follow-up actions, and the write trio names whichever sibling owns the case it refuses.

At `cded242` the deleted `sync-decision` appeared here too, named only by `sync-decisions` in a mutual `Non-Goals` reference between the pair being merged.

The audit pair now carries a mutual reference of its own, added by P3, and it does not mean the same thing. `sync-decision` and `sync-decisions` pointed at each other because neither description could settle which one applied; the pointers were a symptom of an undecidable pair. `audit-drift` and `audit-claims` point at each other to state the boundary in the surface that selects them, so the pointers are what makes the pair decidable. Same shape, opposite meaning: read a mutual disclaimer as a merge signal only when neither description states what separates the two.

`README.md` names `maintain-compact` in its trap table, but the README does not ship, so that reference does not exist at runtime.

## Frontmatter producers and consumers

| Value | Written by | Read by |
|---|---|---|
| `code_ref` | every pack-writing skill | `audit-drift`, `onboard` |

`status: archived` was the second row here, written by `maintain-archive` only and read by `onboard` only, as a default scope exclusion. That single-producer, single-consumer shape is what D6 turned on and what D11 removed: P5 deleted the producer, the consumer, and the value together, so no orphaned half remains for a later contributor to complete.

`audit-claims` is absent from the `code_ref` row by rule, not by omission. P3 forbids it from ranking or filtering claims by provenance, because a current `code_ref` does not make a claim supported and a stale one does not make it false. That rule is what keeps the audit pair on separate axes rather than on the same axis at two zoom levels.

## Test surface

| File | Pins |
|---|---|
| `test_references.py` | contract copies byte-identical to canonical, the gate sentence present in each, the pack-writing skill count stated once in `AGENTS.md` and matching `CONTRACT_SKILLS`, no typographic dashes in any `*.md` under the root |
| `test_skill_metadata.py` | skill id matches folder name, `openai.yaml` names its own skill, only entrypoints disable implicit invocation |
| `test_checkpoint.py` | the Stop hook adapter contains no repository detection logic, and the prompt keeps its thread boundaries |
| `test_install_hooks.py` | packaged hook assets match canonical, installs are idempotent, existing host configuration preserved |
| `test_run_policy.py` | `baselinedocs-run` policy selection gate |

`test_no_typographic_dashes` globs every `*.md` under the repository root, so it covers this pack.
