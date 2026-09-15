---
baseline_schema: "2.0"
pack: "family-design"
document: "sourcecode"
status: "active"
updated: "2026-09-11"
code_ref: "uncommitted"
---

# Design Mechanisms

The parts of the repository that carry the family design rather than the consolidation. Folder shape, the two asset fanouts, the pointer graph, and the test surface are topology this pack does not own: `skill-consolidation.sourcecode.md` holds them, and nothing here restates them.

## Instruction surfaces

Four surfaces reach a running agent, and they do not offer the same guarantee. The whole rule-placement argument, FD-D7, turns on this table.

| Surface | Loaded | Carries | Enforced by |
|---|---|---|---|
| `description` frontmatter | always, on every host, before selection | one line, enough to select the skill | the host's selection mechanism |
| `agents/openai.yaml` | Codex only | `allow_implicit_invocation`, display name, default prompt | `tests/test_skill_metadata.py` |
| `SKILL.md` body | whenever the skill runs | the gate sentence that sends the agent to a reference file | `tests/test_references.py`, both gate wordings |
| `references/*.md` | only if `SKILL.md` says to read it and the agent complies | the contract itself, and the report-style rules | `tests/test_references.py`, byte-identity against canonical |

The consequence that drives the design: a rule requiring a reference file to be read cannot live in that reference file, because an agent that skipped the file never reaches the sentence telling it not to skip it. That one sentence is the only thing restated per skill.

## Checkpoint model

The checkpoint mechanism runs in-thread through `baselinedocs-run`, not through an automated platform hook. The external Stop hook adapter in `hooks/checkpoint.py` and the one-time installer skill `baselinedocs-setup-hooks` were retired and deleted in FD-P8 under FD-D37.

| Path | Role |
|---|---|
| `baselinedocs-run/references/execution-contract.md` | Phase checkpoint schema, policy gates, and verification standards |
| `contract/pack-contract.md` | Required documents (`roadmap`), phase prefix rules, and entry index requirements |

Execution flow:

1. `baselinedocs-run` executes an authorized phase, verifies acceptance criteria, and checkpoints the active roadmap before proceeding to the next phase.
2. The checkpoint records status, evidence, changed files, open risks, and next action in the pack's `<prefix>.roadmap.md`.
3. In conversational or ad-hoc workflows, the operator or agent invokes `baselinedocs-save` or updates `roadmap.md` directly. No background Stop hook intervenes on host turns.

## Execution policy

`baselinedocs-run` ships `references/execution-contract.md`, which has no second copy anywhere because no other skill executes phases.

| Policy | Values | Effect |
|---|---|---|
| `approval_policy` | `phase`, `continuous` | pause after each phase, or continue through every ready phase, checkpointing after each |
| `commit_policy` | `none`, `per-phase` | leave changes uncommitted, or commit only that phase's files after verification and the docs checkpoint |

The selection gate requires both to be unambiguous before implementation begins, and forbids inferring either from an earlier turn. `tests/test_run_policy.py` pins it. FD-D23 records why silence is not a default.

## Pack layout on disk

```text
docs/baseline/
  baselinedocs.index.md           # initiative routing metadata
  family-design/
    family-design.introduction.md
    family-design.roadmap.md
    family-design.hallucination.md
    family-design.sourcecode.md
  skill-consolidation/
    skill-consolidation.introduction.md
    skill-consolidation.roadmap.md
    skill-consolidation.hallucination.md
    skill-consolidation.sourcecode.md
```

Every document filename is `<pack-prefix>.<document>.md`, and the prefix repeats the directory name so a file identifies its pack when it is open alone in an editor. The index sits at the initiative root beside the packs it routes, not inside either of them.

Neither pack carries a `useguide`. `README.md` is the consumer-facing surface for the family, so a `useguide` here would restate it in a file that ships nowhere. FD-D25 records that.
