---
baseline_schema: "2.0"
pack: "baselinedocs"
document: "index"
status: "active"
updated: "2026-09-11"
code_ref: "uncommitted"
---

# Baselinedocs Initiative Index

Routing metadata for the packs under `docs/baseline/`. It carries links, scope, status, dependency edges, and the current cross-pack checkpoint, and nothing else. It does not summarize child content: a summary here would be a second copy of a document that is one click away, and it would drift.

## Packs

| Pack | Scope | Depends on | Status | Next checkpoint |
|---|---|---|---|---|
| [`family-design`](family-design/family-design.introduction.md) | The design of the skill family as a whole: trigger architecture, pack schema, checkpoint model, rule placement, workflow sequence, onboard scope gate, the dissolved `resume-*` family, evidence retention, `useguide`, execution policy, multi-pack routing, report structure | - | active | Reinstall FD-P6, FD-P7, and FD-P8 changes to host skill directories |
| [`skill-consolidation`](skill-consolidation/skill-consolidation.introduction.md) | Reducing the family by removing skills whose operation duplicates another, and repairing the selection surface where two skills claim overlapping triggers | - | active | Four decisions waiting on the user, listed in its roadmap under `Next action` |

Status is copied from each pack's own frontmatter. When this table and a pack disagree, that is a contradiction to report, not a conflict to settle here by preferring the index or the newer date. `baselinedocs-sync-reconcile` owns the repair.

## Documents

| Pack | Documents |
|---|---|
| `family-design` | [introduction](family-design/family-design.introduction.md), [roadmap](family-design/family-design.roadmap.md), [hallucination](family-design/family-design.hallucination.md), [sourcecode](family-design/family-design.sourcecode.md) |
| `skill-consolidation` | [introduction](skill-consolidation/skill-consolidation.introduction.md), [roadmap](skill-consolidation/skill-consolidation.roadmap.md), [hallucination](skill-consolidation/skill-consolidation.hallucination.md), [sourcecode](skill-consolidation/skill-consolidation.sourcecode.md) |

Neither pack carries a `useguide`. `README.md` at the repository root is the consumer-facing surface for this family, so a `useguide` in either pack would restate it in a file that ships nowhere.

## Dependency edges

None. Neither pack blocks the other, and no work in either is waiting on the other.

One cross-pack coupling exists and it is not a blocking edge: `family-design` FD-D30 amended one clause of `skill-consolidation` SC-Q6, replacing "unique across the pack" with "unique across the initiative, by carrying the pack prefix". SC-Q6 stays open on everything else it asks. A reader touching the identifier scheme has to read both entries; a reader doing anything else does not.

An edge records why something is blocked. It is never a reading order: either pack can be read first, and neither has to be loaded to understand the other.

## Reading this initiative

The default scope is one pack, not both. Together they are 2,279 lines, 1,023 in `family-design` and 1,256 in `skill-consolidation`, and a reader who needs the consolidation history does not need the family design to get it.

| If the question is | Load |
|---|---|
| why the family is shaped the way it is, what a pack is, how a checkpoint works, how the skills are meant to be used in order | `family-design` |
| why a particular skill exists, was merged, was renamed, or was deleted, and what the merge criterion is | `skill-consolidation` |
| anything touching the identifier scheme, or a change to `contract/pack-contract.md` | both, because the shared open question sits across them |

## Identifiers

Every identifier carries its pack's prefix, everywhere it is written: inside its own pack, across packs, in a heading, in an entry index row, in a roadmap Basis column, and in a commit message.

| Pack | Prefix | Kinds |
|---|---|---|
| `family-design` | `FD-` | `FD-D<n>` closed decision, `FD-Q<n>` open question, `FD-P<n>` phase |
| `skill-consolidation` | `SC-` | `SC-D<n>`, `SC-Q<n>`, `SC-P<n>` |

The prefix is part of the name, not a qualifier added when a citation leaves its pack. Writing `D16` is not a shorter form of `FD-D16`; it is an identifier that does not exist. `family-design` FD-D30 records the decision, including the two rejected alternatives and what the rename cost.

Any reference written before 2026-08-28 uses the old bare numbers and will not resolve. That is deliberate: a stale reference that fails loudly is the reason this scheme was chosen over one that resolves silently to a neighbouring pack's entry.

## Cross-pack checkpoint

`family-design` was adopted from `DESIGN.md` on 2026-08-28 against `0cb913f`, and `DESIGN.md` was deleted the same day once coverage had been verified across all 22 of its sections. These two packs are now the sole record of the family design. `family-design.hallucination.md` FD-D27 carries the decision; the deleted file remains recoverable at `git show 0cb913f:DESIGN.md`.

The adoption is finished. The reinstall FD-P3 left standing was carried out on 2026-08-29 in `family-design` FD-P5, and reopened again on 2026-09-04 by FD-P6: all four host skill directories still hold FD-P5's snapshot, `report-style.md` at 41 lines and `onboard/SKILL.md`'s two-part `Output`, both now stale against this repository.

The previous checkpoint, exercise the new report shape on a real pack, is closed. It was exercised this session against these same two packs, and the verdict was not that the shape held: the user found the report too heavy on bookkeeping regardless of how well each part was formatted, which is what `family-design` FD-P6 acted on. The current checkpoint is reinstalling FD-P6's changes to the four host directories, recorded above.

What each pack still carries:

| Pack | Outstanding | Kind |
|---|---|---|
| `family-design` | FD-Q1, hiding lifecycle skills at package level | deferred on a platform mechanism that does not exist |
| `family-design` | FD-Q5, who owns misfiled-content detection now that `onboard` no longer checks it | open, opened by FD-P6 |
| `skill-consolidation` | SC-Q6, the identifier scheme and whether the contract owns it | open, minus the uniqueness clause FD-D30 settled |
| `skill-consolidation` | SC-Q7, what `baselinedocs-onboard` does with an entry index | open, four options recorded, none chosen |
| `skill-consolidation` | SC-Q8, the label standard inside an entry | open |

One repair is outstanding and it is not a user decision: `skill-consolidation.roadmap.md` states that its phases SC-P9 through SC-P14 are uncommitted, and they are committed at `959617b`, `b857216`, and `0cb913f`. `baselinedocs-sync-codebase` owns bringing that pack back in line with the repository.
