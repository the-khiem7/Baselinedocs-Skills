---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "introduction"
status: "active"
updated: "2026-08-27"
code_ref: "uncommitted"
---

# Skill Consolidation

## Scope

Reduce the `baselinedocs` skill family by removing skills whose operation duplicates another, and repair the selection surface where two skills claim overlapping triggers but produce different outcomes.

In scope: skill folders in this repository, `contract/pack-contract.md` and its packaged copies, `tests/`, and `README.md` / `DESIGN.md` / `AGENTS.md`.

Out of scope: the pack schema (`2.0` is unchanged), hook behavior, and the detect/repair architecture question, which is deferred to its own research.

## Current truth

| Fact | State |
|---|---|
| skills on disk | 15: 7 entrypoints, 8 lifecycle. 18 at `cded242`, before P1 |
| pack-writing skills shipping `references/pack-contract.md` | 10, byte-identical, pinned by `tests/test_references.py`. 13 at `cded242` |
| `contract/pack-contract.md` | 82 lines. 74 at `cded242`, before the P2 `Disproven claims` section |
| `AGENTS.md` claim about that count | corrected to 10 in four places by P5. It said 14 in all four at `cded242`, when the real figure was 13; P6 found only two of them |
| `status: archived` | removed from the enum by P5. No producer, no consumer |
| test command | `uvx pytest tests/ -q` |
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

End state: 15 skills, 10 packaged contract copies.

## Constraints

- Frontmatter schema must not change, with one deliberate exception: D11 removes `archived` from the `status` enum, because its only producer was deleted. Every other field and value is untouched.
- Removal is a direct folder delete. No deprecation stub.
- ASCII hyphen only. `test_no_typographic_dashes` globs every `*.md` under the repository root, this pack included.
- A skill may rely only on files inside its own folder. The contract is copied into each pack-writing skill, never referenced across folders.
- The skills installed on this machine are an older generation than this repository: the installed `baselinedocs-init` still routes to a `resume` family and ships a 44-line contract against this repository's 74-line canonical file. A `baselinedocs` skill invoked in a later thread reads the installed copy, not this repository's. Treat `contract/pack-contract.md` here as authoritative and verify any pack file written through an installed skill against it.
