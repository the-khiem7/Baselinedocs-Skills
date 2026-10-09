---
baseline_schema: "2.0"
pack: "family-design"
document: "introduction"
status: "active"
updated: "2026-10-10"
code_ref: "uncommitted"
---

# Baseline Docs Family Design

## Scope

The design of the `baselinedocs` skill family as a whole: which skills exist and how a host selects them, what a pack is and what its frontmatter means, how a phase checkpoint is produced, the order the skills are meant to be used in, and how a reader loads a pack without loading too much.

In scope: the trigger architecture, the pack schema and its frontmatter semantics, the checkpoint model, rule placement across the three instruction surfaces, the workflow sequence and the README shape that teaches it, the onboard scope gate, the dissolution of the `resume-*` family, evidence retention, the `useguide` role, run's execution policies, and multi-pack routing.

Out of scope, and owned elsewhere:

| Subject | Owner | Why not here |
|---|---|---|
| Which skills were merged, deleted, or renamed, and the criterion that decided each | `docs/baseline/skill-consolidation/` | That initiative has its own pack, with its own execution history and decisions. Restating any of it here would create a second copy that drifts |
| The definitive rules a running agent obeys | `contract/pack-contract.md` and `contract/report-style.md` | Those files ship into skill folders. This pack records why they say what they say, never what they say |
| How a user is taught to use the family | `README.md` | This pack records the decision that the README leads with the workflow, not the workflow itself |
| Repository conventions for a contributor | `AGENTS.md` | Same boundary: the convention ships in `AGENTS.md`, the argument for it lives here or in `skill-consolidation` |

## Current truth

Verified against the working tree at `0cb913f`, not read off `DESIGN.md`.

| Fact | State |
|---|---|
| skills on disk | every `baselinedocs-*` folder. No count is kept here: `tests/helpers.py` enumerates them and each test classifies every one |
| user entrypoints | `init`, `adopt`, `save`, `run`, `onboard`, `load`, `brief`, `callout`, `help`, `adr`, `self-upgrade`. All set `allow_implicit_invocation: false`. Pinned by `ENTRYPOINTS` in `tests/test_skill_metadata.py` |
| one-time administration | none |
| lifecycle skills, agent-selected | every other skill, all `true`. Includes `recall`, FD-D40 |
| pack schema | `2.0`. Three core documents, two conditional |
| packaged `pack-contract.md` copies | one per skill in `CONTRACT_SKILLS` (`tests/test_references.py`). Absent from `audit-claims`, `audit-drift`, `brief` |
| packaged `report-style.md` copies | every skill outside `REPORT_STYLE_EXEMPT`. Absent from `load` |
| checkpoint hook | none. Automated Stop hook adapter retired and removed in FD-P8 |
| skill version | top-level `version:` in every `SKILL.md`, one value for the family, `0.0.0` until the first tag. A pushed `vX.Y.Z` tag makes `.github/workflows/release.yml` stamp it onto `main`. FD-D45 |
| checkpoint model | in-thread phase checkpointing by `run` |
| `resume-*` skills | none on disk |
| execution policies | `approval_policy` and `commit_policy`, defined in `baselinedocs-run/references/execution-contract.md`, gated by `tests/test_run_policy.py` |
| test command and result | `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q`, green. The pass count is not recorded: it changes with every skill added |
| commit skills | `commit-composer` and `commit-composer-max`: user entrypoints outside the `baselinedocs-*` naming, so the family tests and the release stamp skip them. Tested by `tests/test_commit_skills.py` and `tests/test_commitkit.py`. FD-D48 |
| installed-skill upgrade | `baselinedocs-self-upgrade`: a family skill that upgrades the installed baselinedocs skills in every agent on a machine, never a pack. Its read-only `scripts/upgradekit.sh` is the one script a single family skill owns. Tested by `tests/test_upgradekit.py`. FD-D49 |
| README illustrations | light and dark WebP pairs under `assets/`, rendered from `assets/source/*.html`; the README selects them with `<picture>` and has no Mermaid. `banner.png` is the one PNG and has no dark variant. Tested by `tests/test_readme_assets.py` against the family map source only. FD-D50 |
| baseline packs in this repository | this one and `skill-consolidation`, routed by `docs/baseline/baselinedocs.index.md` |
| source of this pack | `DESIGN.md`, 495 lines, 60,743 bytes. Deleted 2026-08-28 after coverage was verified, and recoverable at `git show 0cb913f:DESIGN.md`. FD-D27 |

## Target

The family's design is shipped, not planned. This pack exists so the reasoning behind it survives without `DESIGN.md` having to be read end to end, and so the parts still undecided are visible as questions rather than as gaps.

| Design area | Intended end state | Reached |
|---|---|---|
| Trigger architecture | Deliberate entrypoints stay explicit; lifecycle skills stay selectable by an agent | yes |
| Pack schema | Three core documents plus two conditional, transitioning additively from the fixed five | yes |
| Checkpoint model | A phase checkpoint is written by `run` itself; no automated hook adapter | yes |
| Rule placement | A rule's pointer lives in `SKILL.md`, its content in exactly one file | yes |
| Workflow sequence | The intended order is written down and taught by the README | yes |
| Onboard scope gate | A reader either knows what it holds or knows it holds nothing; never a silent partial read | yes |
| Resume family | Dissolved, with one owner per question it used to claim | yes |
| Installation profiles | Internal helpers hidden at package level | no, deferred. FD-Q1 |
| Hook rollout | Retired in FD-P8; hook mechanism removed | yes |

## Constraints

- A skill may rely only on files inside its own folder. `npx skills add --skill <name>` installs one folder and nothing else travels with it, so a canonical asset reaches a skill as a byte-identical packaged copy or it does not reach it at all.
- `README.md`, `AGENTS.md`, `contract/`, `tests/`, and this pack do not ship. No installed agent can open any of them, so nothing may be cut from a `SKILL.md` on the grounds that it is written down here.
- ASCII hyphen only. `test_no_typographic_dashes` covers every `.md`, `.yaml`, `.yml`, `.txt`, `.py`, and `.ini` file Git lists for this repository, this pack included.
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
