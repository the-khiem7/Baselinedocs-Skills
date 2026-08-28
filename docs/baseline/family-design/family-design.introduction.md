---
baseline_schema: "2.0"
pack: "family-design"
document: "introduction"
status: "active"
updated: "2026-08-28"
code_ref: "0cb913f"
---

# Baseline Docs Family Design

## Scope

The design of the `baselinedocs` skill family as a whole: which skills exist and how a host selects them, what a pack is and what its frontmatter means, how a phase checkpoint is produced, the order the skills are meant to be used in, and how a reader loads a pack without loading too much.

In scope: the trigger architecture, the pack schema and its frontmatter semantics, the checkpoint model and its hook adapter, rule placement across the three instruction surfaces, the workflow sequence and the README shape that teaches it, the onboard scope gate, the dissolution of the `resume-*` family, evidence retention, the `useguide` role, run's execution policies, and multi-pack routing.

Out of scope, and owned elsewhere:

| Subject | Owner | Why not here |
|---|---|---|
| Which skills were merged, deleted, or renamed, and the criterion that decided each | `docs/baseline/skill-consolidation/` | That initiative has its own pack, with fourteen phases of execution history and twenty-one decisions. Restating any of it here would create a second copy that drifts |
| The definitive rules a running agent obeys | `contract/pack-contract.md` and `contract/report-style.md` | Those files ship into skill folders. This pack records why they say what they say, never what they say |
| How a user is taught to use the family | `README.md` | This pack records the decision that the README leads with the workflow, not the workflow itself |
| Repository conventions for a contributor | `AGENTS.md` | Same boundary: the convention ships in `AGENTS.md`, the argument for it lives here or in `skill-consolidation` |

## Current truth

Verified against the working tree at `0cb913f`, not read off `DESIGN.md`.

| Fact | State |
|---|---|
| skills on disk | 15 |
| user entrypoints | 6: `init`, `adopt`, `save`, `run`, `onboard`, `brief`. All set `allow_implicit_invocation: false` |
| one-time administration | 1: `setup-hooks`, also `false` |
| lifecycle skills, agent-selected | 8, all `true` |
| pack schema | `2.0`. Three core documents, two conditional |
| packaged `pack-contract.md` copies | 11. Absent from `audit-claims`, `audit-drift`, `brief`, `setup-hooks` |
| packaged `report-style.md` copies | 14. Absent from `setup-hooks` only |
| checkpoint hook | `hooks/checkpoint.py`, 78 lines, plus `hooks/prompts/checkpoint.md` and three host config examples |
| hook repository inspection | none. The adapter reads stdin, checks a loop guard, and emits a fixed prompt |
| `resume-*` skills | none on disk |
| execution policies | `approval_policy` and `commit_policy`, defined in `baselinedocs-run/references/execution-contract.md`, gated by `tests/test_run_policy.py` |
| test command and result | `uvx pytest tests/ -q`: 24 passed, 63 subtests passed |
| baseline packs in this repository | 2: this one and `skill-consolidation`, routed by `docs/baseline/baselinedocs.index.md` |
| source of this pack | `DESIGN.md`, 495 lines, 60,743 bytes. Deleted 2026-08-28 after coverage was verified, and recoverable at `git show 0cb913f:DESIGN.md`. FD-D27 |

## Target

The family's design is shipped, not planned. This pack exists so the reasoning behind it survives without `DESIGN.md` having to be read end to end, and so the parts still undecided are visible as questions rather than as gaps.

| Design area | Intended end state | Reached |
|---|---|---|
| Trigger architecture | Deliberate entrypoints stay explicit; lifecycle skills stay selectable by an agent | yes |
| Pack schema | Three core documents plus two conditional, transitioning additively from the fixed five | yes |
| Checkpoint model | A phase checkpoint is written by `run` itself; the hook only prompts and never inspects the repository | yes |
| Rule placement | A rule's pointer lives in `SKILL.md`, its content in exactly one file | yes |
| Workflow sequence | The intended order is written down and taught by the README | yes |
| Onboard scope gate | A reader either knows what it holds or knows it holds nothing; never a silent partial read | yes |
| Resume family | Dissolved, with one owner per question it used to claim | yes |
| Installation profiles | Internal helpers hidden at package level | no, deferred. FD-Q1 |
| Hook rollout | More than one repository at a time | no, deferred. FD-Q2 |

## Constraints

- A skill may rely only on files inside its own folder. `npx skills add --skill <name>` installs one folder and nothing else travels with it, so a canonical asset reaches a skill as a byte-identical packaged copy or it does not reach it at all.
- `README.md`, `AGENTS.md`, `HOOKS.md`, `contract/`, `hooks/`, `tests/`, and this pack do not ship. No installed agent can open any of them, so nothing may be cut from a `SKILL.md` on the grounds that it is written down here.
- ASCII hyphen only. `test_no_typographic_dashes` globs every `*.md` outside a dot-directory, this pack included.
- The frontmatter schema is fixed at `2.0`. Extending it is a schema change, not a convention change.
- An install is a snapshot. An installed skill reads its own packaged copy, so this repository and any machine drift apart from the next edit onward.

### Platform basis

The trigger architecture and the checkpoint model are constrained by what the hosts actually support. These are the sources the design was argued from, and they are the reason the policy field is treated as Codex-only rather than portable.

| Source | What it establishes |
|---|---|
| [OpenAI Codex skills](https://developers.openai.com/codex/skills) | explicit and implicit invocation, and `allow_implicit_invocation` as a per-skill field |
| [OpenAI Codex hooks](https://developers.openai.com/codex/hooks) | project hook discovery, trust review, Stop, and compaction events |
| [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | Stop, task, and compaction lifecycle behavior |
| [Cursor agent best practices](https://cursor.com/blog/agent-best-practices) | dynamic skills and the `stop` continuation pattern |
| [Skills.sh CLI](https://www.skills.sh/docs/cli) | the installation and discovery surface, including the absence of a portable hidden-skill category |
