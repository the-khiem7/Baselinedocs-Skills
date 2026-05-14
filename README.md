![Baselinedocs](logo.png)

**Skills.sh-compatible repository for the `Baseline Docs` skill family.**

`Baseline Docs` is a family of focused skills for creating, syncing, resuming, auditing, and maintaining baseline documentation packs for a codebase. The goal is to keep docs aligned with the actual implementation, business decisions, API contracts, diagrams, and roadmap so work can resume without prior conversation memory.

## Install

Install from GitHub:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baseline_docs_init
```

Install globally without prompts:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baseline_docs_init --global --yes
```

Install from the default branch without selecting a skill:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git
```

## Local Install

From a cloned copy of this repository:

```bash
npx skills add . --skill baseline_docs_init
```

List available skills:

```bash
npx skills add . --list
```

## What Baseline Docs Solves

Baseline docs are not just documentation. They are operational memory for future work.

This skill family exists to solve recurring problems such as:

- a new task starts but there is no structured baseline yet
- code changes but the docs are not updated
- hallucination risks are resolved but the decision is not propagated into the rest of the pack
- roadmap, use guide, and sourcecode docs start contradicting each other
- the user returns after weeks or months and the agent no longer remembers prior context
- the baseline pack becomes too long, noisy, mixed, or hard to resume from

The skill family turns those situations into explicit workflows instead of forcing one monolith skill to handle every lifecycle stage.

## Baseline Pack Contract

Most skills in this family operate on a baseline documentation pack containing these five files:

- `<prefix>.introduction.md` - target, current status, implementation direction
- `<prefix>.roadmap.md` - progress tracker, evidence, changed files, risks, next resume step
- `<prefix>.hallucination.md` - unresolved decisions and closed decision records
- `<prefix>.sourcecode.md` - class diagrams, sequence diagrams, and implementation flow notes
- `<prefix>.useguide.md` - API contracts, request/response examples, black-box usage notes

The pack is designed to be factual, resumable, and maintainable over time.

## Naming Pattern

### Display Names

Every skill follows this pattern:

`Baseline Docs <Family> <Variant>`

Examples:

- `Baseline Docs Init`
- `Baseline Docs Sync Codebase`
- `Baseline Docs Resume Snapshot`
- `Baseline Docs Maintain Compact`

### Frontmatter Names

Every `SKILL.md` frontmatter `name` stays in snake-case:

- `baseline_docs_init`
- `baseline_docs_sync_codebase`
- `baseline_docs_resume_snapshot`
- `baseline_docs_maintain_compact`

## Skill Families

The skill family is organized into 5 groups:

- `Init` - create the first baseline pack
- `Sync` - align an existing pack with code, decisions, or canonical truth
- `Resume` - recover context and restart execution after inactivity or context loss
- `Audit` - inspect trust, drift, and evidence before changing docs
- `Maintain` - compact, archive, split, or prune baseline state over time

## Full Micro-Skill Catalog

### `Init`

#### `Baseline Docs Init`

**Frontmatter name:** `baseline_docs_init`

**Role**

This is the entrypoint skill for creating the first baseline pack for a task, feature, or initiative.

**Use when**

- no baseline pack exists yet
- the user starts a new task and wants resumable docs from the beginning
- the user needs an initial roadmap, decision log, diagrams, and use guide

**Primary outcome**

- the first complete baseline pack is created

**What it should not become**

- not a catch-all updater for every later lifecycle task

### `Sync`

#### `Baseline Docs Sync Codebase`

**Frontmatter name:** `baseline_docs_sync_codebase`

**Role**

Synchronize an existing baseline pack with the latest codebase state.

**Use when**

- code changed but docs did not
- routes, models, auth, jobs, config, or behavior drifted from the pack
- roadmap evidence needs refresh after implementation work

**Primary outcome**

- docs reflect actual code state again

**Key distinction**

- this is code-driven synchronization

#### `Baseline Docs Sync Decisions`

**Frontmatter name:** `baseline_docs_sync_decisions`

**Role**

Propagate one or more closed decisions across the whole baseline pack.

**Use when**

- hallucination risks were closed successfully
- the decision is stored in `hallucination.md` but not yet merged into other docs
- multiple docs still show outdated uncertainty or old options

**Primary outcome**

- the chosen direction is reflected across the pack

**Key distinction**

- this is pack-wide decision propagation

#### `Baseline Docs Sync Reconcile`

**Frontmatter name:** `baseline_docs_sync_reconcile`

**Role**

Repair contradictions between baseline files and restore one canonical truth.

**Use when**

- `roadmap.md` says done but `useguide.md` still says planned
- `sourcecode.md` describes outdated architecture while other docs do not
- internal docs disagree even before checking the codebase

**Primary outcome**

- one consistent baseline pack

**Key distinction**

- this is internal truth reconciliation

#### `Baseline Docs Sync Decision`

**Frontmatter name:** `baseline_docs_sync_decision`

**Role**

Apply one specific closed decision as a narrow, atomic update.

**Use when**

- the user just closed one risk
- only a few sections need patching
- a small precise change is safer than a pack-wide rewrite

**Primary outcome**

- one decision is applied cleanly to affected sections

**Key distinction**

- this is the atomic form of `Sync Decisions`

### `Resume`

#### `Baseline Docs Resume Continue`

**Frontmatter name:** `baseline_docs_resume_continue`

**Role**

Recover where work left off and determine how to continue now.

**Use when**

- the user returns after a long gap
- the agent lost prior conversation memory
- it is unclear which parts of the pack are current versus stale

**Primary outcome**

- current state, blockers, risks, and continuation point become clear

**Key distinction**

- this is execution recovery for right now

#### `Baseline Docs Resume Snapshot`

**Frontmatter name:** `baseline_docs_resume_snapshot`

**Role**

Create a canonical resume-ready snapshot from a long or messy baseline pack.

**Use when**

- the baseline is chat-driven and noisy
- old and new content are heavily mixed
- future resume quality is poor without a compacted current-state summary

**Primary outcome**

- a cleaner artifact exists for future resume work

**Key distinction**

- this is future-oriented resume preparation

#### `Baseline Docs Resume Next Step`

**Frontmatter name:** `baseline_docs_resume_next_step`

**Role**

Reduce a large baseline state into one exact next action.

**Use when**

- the user asks “what should we do next?”
- a full resume report is unnecessary
- the task only needs one executable move to keep progress going

**Primary outcome**

- one next action is chosen clearly

**Key distinction**

- this is the lightest-weight resume action

#### `Baseline Docs Resume Handoff`

**Frontmatter name:** `baseline_docs_resume_handoff`

**Role**

Prepare a concise operational handoff for another agent or another person.

**Use when**

- ownership changes
- another agent will continue implementation
- the next actor should not need to read the full baseline pack first

**Primary outcome**

- a short handoff brief explains truth, risks, and next action

**Key distinction**

- this is resume optimized for transfer of ownership

### `Audit`

#### `Baseline Docs Audit Drift`

**Frontmatter name:** `baseline_docs_audit_drift`

**Role**

Inspect drift between the codebase, baseline docs, and decisions without necessarily fixing anything yet.

**Use when**

- the user wants to audit staleness first
- the team needs a mismatch report before deciding whether to sync
- trust in code/doc alignment is uncertain

**Primary outcome**

- a drift report lists stale or inconsistent areas

**Key distinction**

- this is audit-first, not auto-fix-first

#### `Baseline Docs Audit Verify`

**Frontmatter name:** `baseline_docs_audit_verify`

**Role**

Verify whether claims in the baseline pack are actually supported by code or explicit user decisions.

**Use when**

- documentation trust is low
- roadmap or use guide statements need evidence review
- the user wants to know which statements are proven, unverified, or outdated

**Primary outcome**

- claims are classified by evidence quality

**Key distinction**

- this is claim verification, not general drift reporting

### `Maintain`

#### `Baseline Docs Maintain Compact`

**Frontmatter name:** `baseline_docs_maintain_compact`

**Role**

Compact an existing baseline pack by reducing repetition and verbosity while preserving truth.

**Use when**

- the pack became too long
- sections repeat the same information
- resume cost is too high because the baseline is bloated

**Primary outcome**

- the pack becomes denser and easier to read

**Key distinction**

- this is cleanup for readability, not archive or split

#### `Baseline Docs Maintain Archive`

**Frontmatter name:** `baseline_docs_maintain_archive`

**Role**

Archive completed phases or tasks while preserving history outside the active flow.

**Use when**

- an epic or phase is complete
- the active pack should emphasize unfinished work only
- old execution history is still valuable but too noisy for day-to-day use

**Primary outcome**

- history is preserved while active docs become cleaner

**Key distinction**

- this preserves old state instead of simply deleting it

#### `Baseline Docs Maintain Split`

**Frontmatter name:** `baseline_docs_maintain_split`

**Role**

Split one overloaded baseline pack into several smaller packs.

**Use when**

- one pack covers too many unrelated tasks
- multiple workstreams are mixed together
- ownership or scope boundaries are no longer clear

**Primary outcome**

- smaller scoped packs improve resume and maintenance quality

**Key distinction**

- this changes structure, not just content density

#### `Baseline Docs Maintain Prune`

**Frontmatter name:** `baseline_docs_maintain_prune`

**Role**

Remove obsolete, misleading, or superseded content from the active pack.

**Use when**

- planned sections are no longer relevant
- assumptions were invalidated
- outdated content is confusing sync or resume work

**Primary outcome**

- active docs contain less misleading residue

**Key distinction**

- this is targeted removal of obsolete content

## Recommended Workflow

The family is designed to work as a lifecycle.

### Workflow 1 — New Task Bootstrap

Use this when no baseline exists yet.

1. `Baseline Docs Init`
2. optional implementation work happens outside the skill family
3. later changes move into `Sync`, `Resume`, `Audit`, or `Maintain`

### Workflow 2 — Code Changed, Docs Stale

Use this when implementation moved but baseline docs did not.

1. `Baseline Docs Audit Drift` if you want a report first
2. `Baseline Docs Sync Codebase`
3. optional `Baseline Docs Audit Verify` if trust is still low

### Workflow 3 — Risk Was Resolved, Docs Not Updated

Use this when a hallucination risk or business decision is already closed but not propagated.

1. `Baseline Docs Sync Decision` for one atomic decision
2. `Baseline Docs Sync Decisions` for broader pack-wide propagation
3. `Baseline Docs Sync Reconcile` if the pack still contains contradictions afterward

### Workflow 4 — Return After Long Inactivity

Use this when the user comes back after weeks or months.

1. `Baseline Docs Resume Continue`
2. `Baseline Docs Resume Next Step` if only one executable move is needed
3. `Baseline Docs Resume Snapshot` if the pack is too messy for future resume quality

### Workflow 5 — Transfer Ownership

Use this when another agent or person must continue the work.

1. `Baseline Docs Resume Handoff`
2. optional `Baseline Docs Resume Snapshot` if the baseline is too noisy

### Workflow 6 — Baseline Entropy Cleanup

Use this when the baseline remains technically useful but operationally messy.

1. `Baseline Docs Maintain Compact` to reduce repetition
2. `Baseline Docs Maintain Prune` to remove obsolete content
3. `Baseline Docs Maintain Archive` to move completed history out of the active path
4. `Baseline Docs Maintain Split` if one pack covers too many unrelated streams

## Which Skill Should I Pick?

Use this quick guide:

| Situation | Skill |
|---|---|
| No baseline exists yet | `Baseline Docs Init` |
| Code changed, docs stale | `Baseline Docs Sync Codebase` |
| One decision must be applied | `Baseline Docs Sync Decision` |
| Many closed decisions must propagate | `Baseline Docs Sync Decisions` |
| Docs disagree with each other | `Baseline Docs Sync Reconcile` |
| Returning after a long gap | `Baseline Docs Resume Continue` |
| Need a clean resume snapshot | `Baseline Docs Resume Snapshot` |
| Need one next action only | `Baseline Docs Resume Next Step` |
| Need a transfer brief | `Baseline Docs Resume Handoff` |
| Want a drift report first | `Baseline Docs Audit Drift` |
| Want evidence validation | `Baseline Docs Audit Verify` |
| Pack is too long and repetitive | `Baseline Docs Maintain Compact` |
| Old history should leave active flow | `Baseline Docs Maintain Archive` |
| One pack covers too many streams | `Baseline Docs Maintain Split` |
| Obsolete content should be removed | `Baseline Docs Maintain Prune` |

## Default Skill

The default entrypoint skill is `baseline_docs_init`.

Use it when there is no existing baseline pack and the work needs its first structured documentation state.

## Repository Layout

```text
baseline_docs_init/
  SKILL.md
  agents/
    openai.yaml
baseline-docs-sync-codebase/
  SKILL.md
baseline-docs-sync-decisions/
  SKILL.md
baseline-docs-sync-reconcile/
  SKILL.md
baseline-docs-sync-decision/
  SKILL.md
baseline-docs-resume-continue/
  SKILL.md
baseline-docs-resume-snapshot/
  SKILL.md
baseline-docs-resume-next-step/
  SKILL.md
baseline-docs-resume-handoff/
  SKILL.md
baseline-docs-audit-drift/
  SKILL.md
baseline-docs-audit-verify/
  SKILL.md
baseline-docs-maintain-compact/
  SKILL.md
baseline-docs-maintain-archive/
  SKILL.md
baseline-docs-maintain-split/
  SKILL.md
baseline-docs-maintain-prune/
  SKILL.md
README.md
REFACTOR.md
```

## Relationship to `REFACTOR.md`

`README.md` is the practical guide for users of the skill family.

`REFACTOR.md` is the design and migration plan explaining why the monolith skill was split into 15 micro-skills and how the refactor should evolve.

## Compatibility

This repository is structured for the Skills.sh CLI. Each skill folder contains a `SKILL.md` file with `name` and `description` frontmatter, which is the format detected by:

```bash
npx skills add . --list
```
