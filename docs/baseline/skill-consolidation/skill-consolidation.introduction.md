---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "introduction"
status: "active"
updated: "2026-09-11"
code_ref: "uncommitted"
---

# Skill Consolidation

## Scope

Reduce the `baselinedocs` skill family by removing skills whose operation duplicates another, and repair the selection surface where two skills claim overlapping triggers but produce different outcomes.

In scope: skill folders in this repository, `contract/pack-contract.md` and its packaged copies, `tests/`, and `README.md` / `DESIGN.md` / `AGENTS.md`.

Out of scope: the pack schema, which is unchanged apart from the one enum removal SC-D11 records, and hook behavior.

## Current truth

| Fact | State |
|---|---|
| skills on disk | 14: 6 entrypoints, 8 lifecycle. 18 at `cded242`, before SC-P1 |
| skills shipping `references/pack-contract.md` | 11, byte-identical, pinned by `tests/test_references.py`. The 10 writers plus `onboard`, which reads every document in full. 13 at `cded242`, 10 at `c6eb29a` |
| criterion for shipping it | a full read of the pack, not the act of writing. SC-D16 |
| skills shipping `references/report-style.md` | 14, byte-identical. Every skill in the family, no exceptions. SC-D17, SC-D22 |
| `contract/pack-contract.md` | 108 lines, 11 sections. 84 before the SC-P12 entry-index and SC-P13 misfiled-content sections, 74 at `cded242` before the SC-P2 `Disproven claims` section |
| entry kinds in `hallucination` | at least 3, and never enumerated: a closed decision with four required parts, a disproven-claim relocation with a different shape, and an open question. SC-Q8 |
| installed copies, this machine | 15 skills per host directory in `.claude`, `.agents`, `.kilocode`, `.kiro`, holding SC-P8's snapshot: 10 contract copies at 82 lines, no `report-style.md` anywhere, and an `onboard` with neither the contract copy nor its read gate. `.codex/skills` holds none |
| `AGENTS.md` claim about that count | corrected to 10 in four places by SC-P5. It said 14 in all four at `cded242`, when the real figure was 13; SC-P6 found only two of them |
| `status: archived` | removed from the enum by SC-P5. No producer, no consumer |
| test command | `uvx pytest tests/ -q` |
| `hallucination` entry index | required by the contract above 40 KB or 20 entries, whichever comes first. 22 rows here, and no skill consumes it yet. SC-D19 |
| existing baseline packs | none before this one |

## Target

| Change | Result |
|---|---|
| `sync-decision` folded into `sync-decisions` | one decision-propagation skill |
| `maintain-prune` deleted | journal content in `hallucination` stops being removable by design |
| `audit-verify` renamed `audit-claims` | audit pair separated on unit of analysis |
| `maintain-archive` deleted | with `status: archived` and `onboard`'s exclusion, so no orphaned affordance is left behind |
| `maintain-compact` gains a revert gate | compaction is lossless or it is reverted |
| merge criterion recorded | `DESIGN.md` carries a testable rule instead of a pointer heuristic |

| contract shipped on a full read, not on writing | `onboard` can report content sitting in a document whose role does not cover it |
| report style shipped to every reporting skill | an element identifier is glossed in conversation regardless of whose machine the skill runs on |

End state: 14 skills, 11 packaged contract copies, 14 packaged report-style copies.

## Constraints

- Frontmatter schema must not change, with one deliberate exception: SC-D11 removes `archived` from the `status` enum, because its only producer was deleted. Every other field and value is untouched.
- Removal is a direct folder delete. No deprecation stub.
- ASCII hyphen only. `test_no_typographic_dashes` globs every `*.md` under the repository root, this pack included.
- A skill may rely only on files inside its own folder. The contract is copied into each skill that ships it, never referenced across folders.
- A `baselinedocs` skill invoked in a later thread reads its own installed copy, not this repository's. An install is therefore a snapshot: this repository and any machine drift apart from the next repository edit onward. Treat `contract/pack-contract.md` here as authoritative and verify any pack file written through an installed skill against it. SC-D15 records the generation gap that held on this machine until SC-P8 closed it.
