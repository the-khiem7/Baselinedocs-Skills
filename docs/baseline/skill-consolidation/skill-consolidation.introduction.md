---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "introduction"
status: "active"
updated: "2026-10-05"
code_ref: "uncommitted"
---

# Skill Consolidation

## Scope

Reduce the `baselinedocs` skill family by removing skills whose operation duplicates another, and repair the selection surface where two skills claim overlapping triggers but produce different outcomes.

In scope: skill folders in this repository, `contract/pack-contract.md` and its packaged copies, `tests/`, `README.md`, and `AGENTS.md`. `DESIGN.md` was in scope while this pack ran and was deleted once `family-design` took over its record (`family-design` FD-D27).

Out of scope: the pack schema, which is unchanged apart from the one enum removal SC-D11 records, and hook behavior.

## Current truth

| Fact | State |
|---|---|
| skills on disk | every `baselinedocs-*` folder, none counted here. Entrypoints: `init`, `adopt`, `save`, `run`, `onboard`, `load`, `brief`, `callout`; every other skill is lifecycle. 18 skills at `cded242`, before SC-P1; `callout`, `load`, and `recall` were added after this pack closed (`family-design` FD-D38, FD-D39, FD-D40) |
| skills shipping `references/pack-contract.md` | byte-identical, one per skill in `CONTRACT_SKILLS` (`tests/test_references.py`): every writer, `onboard`, `load`, `recall`. Absent from `brief`, `audit-drift`, `audit-claims`. 13 at `cded242`, 10 at `c6eb29a` |
| criterion for shipping it | a full read of the pack, not the act of writing. SC-D16. `recall` ships it under a third criterion, `family-design` FD-D40 |
| skills shipping `references/report-style.md` | byte-identical, every skill outside `REPORT_STYLE_EXEMPT`, which holds `load` (`family-design` FD-D39). SC-D17, SC-D22 |
| `contract/pack-contract.md` | size not recorded here. 74 lines at `cded242` before the SC-P2 `Disproven claims` section, 84 before the SC-P12 entry-index and SC-P13 misfiled-content sections; later `family-design` phases widened it further |
| entry kinds in `hallucination` | at least 3, and never enumerated: a closed decision with four required parts, a disproven-claim relocation with a different shape, and an open question. SC-Q8 |
| installed copies, any machine | per-machine state, not tracked here. SC-P8 replaced every host copy on this machine from this clone, SC-P9 reopened the gap one phase later, and every later repository edit reopens it. The standing remedy is in the `family-design` roadmap, Risks |
| `AGENTS.md` claim about the pack-writing skill count | stated once, pinned against `WRITER_SKILLS` by `test_agents_md_states_the_skill_count_once_and_correctly`. It said 14 in all four places at `cded242`, when the real figure was 13; SC-P5 corrected four and SC-P6 found only two of them |
| `status: archived` | removed from the enum by SC-P5. No producer, no consumer |
| test command | `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q` |
| `hallucination` entry index | required by the contract from the first entry (FD-D42 removed the 40 KB / 20 entry threshold). Present here, and no skill consumes it yet. SC-D19 |
| existing baseline packs | none before this one |

## Target

| Change | Result |
|---|---|
| `sync-decision` folded into `sync-decisions` | one decision-propagation skill |
| `maintain-prune` deleted | journal content in `hallucination` stops being removable by design |
| `audit-verify` renamed `audit-claims` | audit pair separated on unit of analysis |
| `maintain-archive` deleted | with `status: archived` and `onboard`'s exclusion, so no orphaned affordance is left behind |
| `maintain-compact` gains a revert gate | compaction is lossless or it is reverted |
| merge criterion recorded | SC-D1 carries a testable rule instead of a pointer heuristic, and `AGENTS.md` points at it |
| contract shipped on a full read, not on writing | `onboard` could report content sitting in a document whose role does not cover it. It no longer does: `family-design` FD-D34 deleted the check, and FD-Q5 asks who owns it |
| report style shipped to every reporting skill | an element identifier is glossed in conversation regardless of whose machine the skill runs on |

End state reached at SC-P14: 14 skills, 11 packaged contract copies, 14 packaged report-style copies. Later changes belong to `family-design`.

## Constraints

- Frontmatter schema must not change, with one deliberate exception: SC-D11 removes `archived` from the `status` enum, because its only producer was deleted. Every other field and value is untouched.
- Removal is a direct folder delete. No deprecation stub.
- ASCII hyphen only. `test_no_typographic_dashes` covers every `.md`, `.yaml`, `.yml`, `.txt`, `.py`, and `.ini` file Git lists for this repository, this pack included.
- A skill may rely only on files inside its own folder. The contract is copied into each skill that ships it, never referenced across folders.
- A `baselinedocs` skill invoked in a later thread reads its own installed copy, not this repository's. An install is therefore a snapshot: this repository and any machine drift apart from the next repository edit onward. Treat `contract/pack-contract.md` here as authoritative and verify any pack file written through an installed skill against it. SC-D15 records the generation gap that held on this machine until SC-P8 closed it.
