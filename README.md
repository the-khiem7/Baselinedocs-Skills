![Baselinedocs](logo.png)

**Adaptive operational memory for agent-assisted software work.**

Baseline Docs stores current implementation truth, decisions, evidence, dependencies, and the exact continuation point so another conversation or agent can resume without relying on chat history.

## Install

Install one user entrypoint:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baselinedocs-init
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baselinedocs-save
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baselinedocs-run
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baselinedocs-setup-hooks
```

List or install the complete family:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --list
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git
```

From a local clone, replace the repository URL with `.`.

## Three User Entrypoints

| User intent | Skill | Outcome |
|---|---|---|
| Start durable docs with a new workflow | `baselinedocs-init` | Create an adaptive pack or multi-pack initiative |
| Capture work already in progress | `baselinedocs-save` | Save current brownfield context without restarting |
| Execute an initialized roadmap | `baselinedocs-run` | Run phases with checkpoints and requested approval policy |

These entrypoints set `policy.allow_implicit_invocation: false` for Codex so they remain deliberate user actions. Use `$baselinedocs-init`, `$baselinedocs-save`, or `$baselinedocs-run`.

When `$baselinedocs-run` is invoked without both execution policies, it asks naturally whether to pause after each phase and whether to commit each verified phase. It does not silently choose defaults or expose configuration-style identifiers unless requested.

`baselinedocs-setup-hooks` is a separate one-time administration utility. Invoke it explicitly in each repository where automatic checkpoint reminders are wanted; it is not part of the daily three-entrypoint workflow.

The remaining lifecycle skills are agent-selected helpers. Their UI names start with `Baseline Docs Internal:` and implicit invocation remains enabled. Other agent hosts may not enforce the Codex-specific policy, so the classification is also documented in each skill description.

## Agent-Selected Skills

| Family | Skills |
|---|---|
| Sync | `sync-codebase`, `sync-decision`, `sync-decisions`, `sync-reconcile` |
| Resume | `resume-continue`, `resume-snapshot`, `resume-next-step`, `resume-handoff` |
| Audit | `audit-drift`, `audit-verify` |
| Maintain | `maintain-compact`, `maintain-archive`, `maintain-split`, `maintain-prune` |
| Knowledge | `extract-wiki` |

All skill IDs use lowercase kebab-case, for example `baselinedocs-sync-codebase`.

## Adaptive Pack Contract

Every pack has three core documents:

- `<prefix>.introduction.md`: scope, current truth, target, constraints
- `<prefix>.roadmap.md`: phases, dependencies, evidence, risks, next action
- `<prefix>.hallucination.md`: open questions and closed decisions

Two extensions are conditional:

- `<prefix>.sourcecode.md`: architecture and implementation flow
- `<prefix>.useguide.md`: consumer contract, API or method usage, migration procedure, or operator guidance

Do not create conditional files that would contain only filler. Existing five-file packs remain compatible; lifecycle skills preserve useful content and prune only when safe.

Each document carries frontmatter:

```yaml
---
baseline_schema: "2.0"
pack: "avatar-rollout"
document: "roadmap"
status: "active"
updated: "2026-07-30"
code_ref: "2d0bf83"
---
```

`updated` is the last document edit date. `code_ref` is the code state actually inspected. A newer commit is a drift signal, not proof by itself.

## Writing Policy

Baseline packs are current operational memory, not command transcripts.

- Record final verification evidence.
- Keep an intermediate failure only when it remains actionable, explains a design change, or reproduces a defect.
- Aggregate small post-initial corrections under the phase they refine.
- Create a new phase only for a distinct outcome, dependency, release gate, or independently reviewable scope.

## Wiki Boundary

Use `docs/wiki/<topic>.md` for reusable patterns such as migrations, conversions, integrations, and method usage.

- Baseline pack: task-specific state, decisions, evidence, roadmap.
- Wiki: task-independent instructions that can be injected into later work.

`baselinedocs-extract-wiki` removes task chronology and links the reusable article back from the pack.

## Multi-Domain Work

Do not hide child packs behind a duplicated general pack. Keep every domain pack directly addressable and add an initiative index:

```text
docs/baseline/avatar-modernization/
  avatar-modernization.index.md
  identity-api/
    identity-api.introduction.md
    identity-api.roadmap.md
    identity-api.hallucination.md
  avatar-ui/
    avatar-ui.introduction.md
    avatar-ui.roadmap.md
    avatar-ui.hallucination.md
```

The index contains direct links, status, and dependency edges. It routes work without repeating child content.

## Phase Checkpoint Hooks

The repository includes a portable advisory hook and configuration examples for Codex, Claude Code, and Cursor. It detects changed implementation files while an active baseline roadmap exists and asks the agent to checkpoint before stopping.

Use `$baselinedocs-setup-hooks` to install or update it without copying files or replacing existing hook configuration. See [HOOKS.md](HOOKS.md) for behavior and manual fallback instructions. Hooks are a safety net; the roadmap workflow remains the source of truth.

## Design Notes

See [DESIGN.md](DESIGN.md) for the decisions, tradeoffs, migration behavior, and host capability boundaries behind this version.

## Compatibility

Each skill follows the Agent Skills folder shape:

```text
<skill>/
  SKILL.md
  agents/
    openai.yaml
  references/     # only when needed
```

The repository is compatible with Skills.sh discovery. Codex-specific invocation policy lives in `agents/openai.yaml`; other hosts can still use the portable `name` and `description` frontmatter.
