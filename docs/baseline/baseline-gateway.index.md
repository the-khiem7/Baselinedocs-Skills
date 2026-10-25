---
baseline_schema: "2.0"
pack: "baseline-gateway"
document: "index"
status: "active"
updated: "2026-10-25"
code_ref: "02f17f4"
---

# Baselinedocs Initiative Index

Routing metadata for the packs under `docs/baseline/`. It carries links, scope, status, dependency edges, and the current cross-pack checkpoint, and nothing else. It does not summarize child content: a summary here would be a second copy of a document that is one click away, and it would drift.

## Packs

| Pack | Scope | Depends on | Status | Next checkpoint |
|---|---|---|---|---|
| [`baselinedocs`](baselinedocs/baselinedocs.introduction.md) | The design of the skill family as a whole: trigger architecture, pack schema, checkpoint model, rule placement, workflow sequence, onboard scope gate, the dissolved `resume-*` family, evidence retention, `useguide`, execution policy, multi-pack routing, report structure | - | active | Reinstall BLD-P6 to BLD-P14 changes on any machine behind them; confirm the first `release.yml` run (BLD-P16); run `baselinedocs-self-upgrade` once on a stale machine (BLD-P20) |
| [`skill-consolidation`](skill-consolidation/skill-consolidation.introduction.md) | Reducing the family by removing skills whose operation duplicates another, and repairing the selection surface where two skills claim overlapping triggers | - | active | Four decisions waiting on the user, listed in its roadmap under `Next action` |
| [`academy`](academy/academy.introduction.md) | The `academic` sub-family: skills that read the packs of many projects and compose an anonymized local HTML knowledge base of lessons, and its core skill `baseline-academic-core` | `baselinedocs` | draft | No open question; trial-run ACA-P4 once the user approves it |

Status is copied from each pack's own frontmatter. When this table and a pack disagree, that is a contradiction to report, not a conflict to settle here by preferring the index or the newer date. `baselinedocs-sync-reconcile` owns the repair.

## Documents

| Pack | Documents |
|---|---|
| `baselinedocs` | [introduction](baselinedocs/baselinedocs.introduction.md), [roadmap](baselinedocs/baselinedocs.roadmap.md), [hallucination](baselinedocs/baselinedocs.hallucination.md), [sourcecode](baselinedocs/baselinedocs.sourcecode.md) |
| `skill-consolidation` | [introduction](skill-consolidation/skill-consolidation.introduction.md), [roadmap](skill-consolidation/skill-consolidation.roadmap.md), [hallucination](skill-consolidation/skill-consolidation.hallucination.md), [sourcecode](skill-consolidation/skill-consolidation.sourcecode.md) |
| `academy` | [introduction](academy/academy.introduction.md), [roadmap](academy/academy.roadmap.md), [hallucination](academy/academy.hallucination.md) |

No pack carries a `useguide`. `README.md` at the repository root is the consumer-facing surface for this family, so a `useguide` in any pack would restate it in a file that ships nowhere.

## Dependency edges

| Pack | Depends on | Why |
|---|---|---|
| `academy` | `baselinedocs` | its skills join the family and reuse `baseline-core`; building them adds a second exception to the sibling-prerequisite rule that `baselinedocs` BLD-D54 recorded, and that decision belongs in `baselinedocs` |

`baselinedocs` and `skill-consolidation` block neither each other nor `academy`, and no work in them is waiting on another pack.

One cross-pack coupling exists and it is not a blocking edge: `baselinedocs` BLD-D30 amended one clause of `skill-consolidation` SC-Q6, replacing "unique across the pack" with "unique across the initiative, by carrying the pack prefix". SC-Q6 stays open on everything else it asks. A reader touching the identifier scheme has to read both entries; a reader doing anything else does not.

A second coupling: `baselinedocs` BLD-D42 reversed the conditional clause of `skill-consolidation` SC-D19 (the entry index is now required from the first entry) and settled the heading format half of SC-Q6. A reader touching the entry index has to read both entries.

An edge records why something is blocked. It is never a reading order: either pack can be read first, and neither has to be loaded to understand the other.

## Reading this initiative

The default scope is one pack, not all of them. `baselinedocs` and `skill-consolidation` together are 2,279 lines, 1,023 in `baselinedocs` and 1,256 in `skill-consolidation`, and a reader who needs the consolidation history does not need the family design to get it.

| If the question is | Load |
|---|---|
| why the family is shaped the way it is, what a pack is, how a checkpoint works, how the skills are meant to be used in order | `baselinedocs` |
| why a particular skill exists, was merged, was renamed, or was deleted, and what the merge criterion is | `skill-consolidation` |
| anything touching the identifier scheme, or a change to `contract/pack-contract.md` | both, because the shared open question sits across them |
| the `academic` sub-family, its lessons, anonymization, or its core skill | `academy`; add `baselinedocs` when the change touches `baseline-core` or the sibling-prerequisite rule |

## Identifiers

Every identifier carries its pack's prefix, everywhere it is written: inside its own pack, across packs, in a heading, in an entry index row, in a roadmap Basis column, and in a commit message.

| Pack | Prefix | Kinds |
|---|---|---|
| `baselinedocs` | `BLD-` | `BLD-D<n>` closed decision, `BLD-Q<n>` open question, `BLD-P<n>` phase |
| `skill-consolidation` | `SC-` | `SC-D<n>`, `SC-Q<n>`, `SC-P<n>` |
| `academy` | `ACA-` | `ACA-D<n>`, `ACA-Q<n>`, `ACA-P<n>` |

The prefix is part of the name, not a qualifier added when a citation leaves its pack. Writing `D16` is not a shorter form of `BLD-D16`; it is an identifier that does not exist. `baselinedocs` BLD-D30 records the decision, including the two rejected alternatives and what the rename cost.

The heading format and the kinds a `hallucination` holds are stated in `contract/pack-contract.md` (BLD-D42).

Any reference written before 2026-08-28 uses the old bare numbers and will not resolve. That is deliberate: a stale reference that fails loudly is the reason this scheme was chosen over one that resolves silently to a neighbouring pack's entry.

## Cross-pack checkpoint

`baselinedocs` was adopted from `DESIGN.md` on 2026-08-28 against `0cb913f`, and `DESIGN.md` was deleted the same day once coverage had been verified across all 22 of its sections. These two packs are now the sole record of the family design. `baselinedocs.hallucination.md` BLD-D27 carries the decision; the deleted file remains recoverable at `git show 0cb913f:DESIGN.md`.

The adoption is finished. The reinstall BLD-P3 left standing was carried out on 2026-08-29 in `baselinedocs` BLD-P5, and reopened again on 2026-09-04 by BLD-P6: all four host skill directories still hold BLD-P5's snapshot, `report-style.md` at 41 lines and `onboard/SKILL.md`'s two-part `Output`, both now stale against this repository.

The previous checkpoint, exercise the new report shape on a real pack, is closed. It was exercised this session against these same two packs, and the verdict was not that the shape held: the user found the report too heavy on bookkeeping regardless of how well each part was formatted, which is what `baselinedocs` BLD-P6 acted on. The current checkpoint is reinstalling BLD-P6's changes to the four host directories, recorded above.

What each pack still carries:

| Pack | Outstanding | Kind |
|---|---|---|
| `baselinedocs` | BLD-Q1, hiding lifecycle skills at package level | deferred on a platform mechanism that does not exist |
| `baselinedocs` | BLD-Q5, who owns misfiled-content detection now that `onboard` no longer checks it | open, opened by BLD-P6 |
| `skill-consolidation` | SC-Q6, the identifier scheme and whether the contract owns it | open, minus the uniqueness clause BLD-D30 settled and the heading format BLD-D42 settled |
| `skill-consolidation` | SC-Q7, what `baselinedocs-onboard` does with an entry index | open, four options recorded, none chosen |
| `skill-consolidation` | SC-Q8, the label standard inside an entry | open |

One repair is outstanding and it is not a user decision: `skill-consolidation.roadmap.md` states that its phases SC-P9 through SC-P14 are uncommitted, and they are committed at `959617b`, `b857216`, and `0cb913f`. `baselinedocs-sync-codebase` owns bringing that pack back in line with the repository.
