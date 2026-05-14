# Baseline Docs Skill Refactor Plan

## Goal

Refactor the current monolith `baseline-docs` skill into a family of 15 focused micro-skills.

The current skill is valuable but too broad. It mixes multiple responsibilities in one place:

- baseline initialization
- documentation synchronization after code changes
- decision propagation after hallucination-risk resolution
- resumable task recovery after long inactivity
- baseline cleanup and maintenance
- drift detection and trust verification

This makes the trigger surface ambiguous and causes a naming problem in the skill library. The user or agent may know the desired action, but the current skill name does not communicate whether the task is:

- creating a new baseline
- syncing an existing baseline
- resuming a stale task
- auditing trust and drift
- compacting or archiving old baseline state

The refactor should solve both problems:

1. split one broad skill into smaller purpose-specific skills
2. standardize naming so related skills stay grouped together in the library

## Naming Strategy

### Display Naming Pattern

All skills follow this display pattern:

`Baseline Docs <Family> <Variant>`

Examples:

- `Baseline Docs Sync Codebase`
- `Baseline Docs Resume Snapshot`
- `Baseline Docs Maintain Compact`

### Frontmatter Naming Pattern

All `name` values in `SKILL.md` frontmatter stay in snake-case:

`baseline_docs_<family>_<variant>`

Examples:

- `baseline_docs_sync_codebase`
- `baseline_docs_resume_snapshot`
- `baseline_docs_maintain_compact`

### Exception

The initialization skill is intentionally shorter:

- display name: `Baseline Docs Init`
- frontmatter name: `baseline_docs_init`

This is the entrypoint skill for creating a baseline pack from scratch.

## Why Refactor

### Current Monolith Problems

The current `baseline-docs` skill behaves like a lifecycle skill even though it is named like a single-purpose skill.

It currently overlaps several phases:

- initialize docs for a new task
- update docs after code changes
- apply closed decisions into downstream baseline files
- help agents resume work after context loss
- keep roadmap and pack consistent over time

This creates several issues:

| Problem | Effect |
|---|---|
| Too much scope in one skill | Triggering is ambiguous |
| Naming too broad | Skills become hard to discover later |
| Docs lifecycle mixed with init flow | Hard to maintain clean prompts |
| Resume and sync behaviors mixed | Agent may choose the wrong behavior |
| Cleanup actions not explicit | Baseline entropy grows over time |

### Design Target

The new design should make each skill answer one clear question:

- Are we creating?
- Are we syncing?
- Are we resuming?
- Are we auditing?
- Are we maintaining?

The skill family should feel like a small operating system for baseline docs, not one giant catch-all instruction file.

## Final Skill Set

This refactor keeps the previously agreed 15 skills.

| # | Display name | Frontmatter name |
|---|---|---|
| 1 | `Baseline Docs Init` | `baseline_docs_init` |
| 2 | `Baseline Docs Sync Codebase` | `baseline_docs_sync_codebase` |
| 3 | `Baseline Docs Sync Decisions` | `baseline_docs_sync_decisions` |
| 4 | `Baseline Docs Sync Reconcile` | `baseline_docs_sync_reconcile` |
| 5 | `Baseline Docs Sync Decision` | `baseline_docs_sync_decision` |
| 6 | `Baseline Docs Resume Continue` | `baseline_docs_resume_continue` |
| 7 | `Baseline Docs Resume Snapshot` | `baseline_docs_resume_snapshot` |
| 8 | `Baseline Docs Resume Next Step` | `baseline_docs_resume_next_step` |
| 9 | `Baseline Docs Resume Handoff` | `baseline_docs_resume_handoff` |
| 10 | `Baseline Docs Audit Drift` | `baseline_docs_audit_drift` |
| 11 | `Baseline Docs Audit Verify` | `baseline_docs_audit_verify` |
| 12 | `Baseline Docs Maintain Compact` | `baseline_docs_maintain_compact` |
| 13 | `Baseline Docs Maintain Archive` | `baseline_docs_maintain_archive` |
| 14 | `Baseline Docs Maintain Split` | `baseline_docs_maintain_split` |
| 15 | `Baseline Docs Maintain Prune` | `baseline_docs_maintain_prune` |

## Skill Families

### `Init`

Purpose: create the first baseline pack for a task, feature, or topic.

Skills:

- `Baseline Docs Init`

### `Sync`

Purpose: update baseline docs so they match code, decisions, or internal truth.

Skills:

- `Baseline Docs Sync Codebase`
- `Baseline Docs Sync Decisions`
- `Baseline Docs Sync Reconcile`
- `Baseline Docs Sync Decision`

### `Resume`

Purpose: recover focus, execution context, and next action after context loss or long inactivity.

Skills:

- `Baseline Docs Resume Continue`
- `Baseline Docs Resume Snapshot`
- `Baseline Docs Resume Next Step`
- `Baseline Docs Resume Handoff`

### `Audit`

Purpose: inspect trust, drift, and evidence quality before changing docs.

Skills:

- `Baseline Docs Audit Drift`
- `Baseline Docs Audit Verify`

### `Maintain`

Purpose: keep the baseline pack clean, scalable, and manageable over time.

Skills:

- `Baseline Docs Maintain Compact`
- `Baseline Docs Maintain Archive`
- `Baseline Docs Maintain Split`
- `Baseline Docs Maintain Prune`

## Detailed Micro-Skill Definitions

### 1. `Baseline Docs Init`

**Frontmatter name:** `baseline_docs_init`

**Purpose**

Create a new baseline documentation pack for a task, topic, feature, or initiative.

**Use when**

- the user starts a new task with no baseline pack yet
- the existing baseline files do not exist yet
- the user asks for an implementation roadmap from scratch
- the user wants initial introduction, roadmap, risk log, diagrams, and use guide

**Primary output**

- `<prefix>.introduction.md`
- `<prefix>.roadmap.md`
- `<prefix>.hallucination.md`
- `<prefix>.sourcecode.md`
- `<prefix>.useguide.md`

**Non-goals**

- not the main skill for code drift syncing
- not the main skill for propagating closed decisions
- not the main skill for resume recovery after long inactivity

### 2. `Baseline Docs Sync Codebase`

**Frontmatter name:** `baseline_docs_sync_codebase`

**Purpose**

Synchronize the baseline pack with the current codebase after implementation changed.

**Use when**

- code changed but docs did not
- routes, models, auth, jobs, config, or behavior drifted from baseline docs
- roadmap evidence must reflect new implementation state

**Primary output**

- updated baseline files that reflect actual code state
- roadmap evidence updated with changed files and verification notes

**Core behavior**

- inspect code first
- compare pack vs code
- treat stale docs as bugs
- update every impacted baseline file in one pass when feasible

### 3. `Baseline Docs Sync Decisions`

**Frontmatter name:** `baseline_docs_sync_decisions`

**Purpose**

Propagate already-closed hallucination risks or other decisions across the whole baseline pack.

**Use when**

- the user resolved one or more open risks
- the decision is recorded in `hallucination.md` but not reflected elsewhere
- multiple docs still describe old options or uncertainty

**Primary output**

- closed decisions applied to introduction, roadmap, sourcecode, and useguide
- pack reflects one chosen direction instead of unresolved alternatives

**Difference vs `Sync Decision`**

- `Sync Decisions` is batch-oriented or pack-wide
- `Sync Decision` is a single-decision atomic operation

### 4. `Baseline Docs Sync Reconcile`

**Frontmatter name:** `baseline_docs_sync_reconcile`

**Purpose**

Resolve contradictions between baseline files and re-establish one canonical truth.

**Use when**

- `roadmap.md` says a task is done but `useguide.md` still says planned
- `sourcecode.md` describes outdated architecture
- baseline files disagree about current implementation state

**Primary output**

- consistent baseline pack
- explicit resolution of conflicting statements

**Core behavior**

- compare files inside the pack
- identify contradictions
- prefer code evidence and explicit user decisions
- rewrite conflicting sections to converge on one truth

### 5. `Baseline Docs Sync Decision`

**Frontmatter name:** `baseline_docs_sync_decision`

**Purpose**

Apply one specific decision to the exact baseline files it affects.

**Use when**

- the user just closed one risk
- the agent must patch only targeted sections
- a smaller, safer update is preferable to pack-wide synchronization

**Primary output**

- minimal, targeted updates for one decision

**Difference vs `Sync Decisions`**

- this skill is atomic and narrow
- best for one decision at a time

### 6. `Baseline Docs Resume Continue`

**Frontmatter name:** `baseline_docs_resume_continue`

**Purpose**

Recover where work left off and determine how to continue without prior conversation memory.

**Use when**

- the user returns after weeks or months
- the agent lost context
- the baseline exists but it is unclear what is current and what is old

**Primary output**

- current state summary
- open blockers and risks
- exact recommended continuation point

**Core behavior**

- read the pack as operational memory
- identify current truth, outdated sections, and unresolved items
- end with a concrete next continuation path

### 7. `Baseline Docs Resume Snapshot`

**Frontmatter name:** `baseline_docs_resume_snapshot`

**Purpose**

Create a clean, canonical snapshot from a long or messy baseline so future resume becomes easier.

**Use when**

- the baseline is chat-driven and noisy
- too much old and new content is mixed together
- future agents will struggle to identify the active state

**Primary output**

- a concise resume-ready snapshot
- a stable summary of what is true now

**Difference vs `Resume Continue`**

- `Resume Snapshot` creates a cleaner artifact for future use
- `Resume Continue` focuses on continuing work now

### 8. `Baseline Docs Resume Next Step`

**Frontmatter name:** `baseline_docs_resume_next_step`

**Purpose**

Reduce a large baseline state into one immediately actionable next move.

**Use when**

- the user asks “what should we do next?”
- the full resume context is unnecessary
- the task only needs one precise next action

**Primary output**

- one exact next action
- optional short rationale and prerequisite note

### 9. `Baseline Docs Resume Handoff`

**Frontmatter name:** `baseline_docs_resume_handoff`

**Purpose**

Prepare a concise handoff for another agent or another person to continue work safely.

**Use when**

- ownership changes
- another agent will continue implementation
- the user wants a short operational handoff instead of full baseline reading

**Primary output**

- handoff summary
- current truth
- open risks
- next expected action

### 10. `Baseline Docs Audit Drift`

**Frontmatter name:** `baseline_docs_audit_drift`

**Purpose**

Audit drift between codebase, baseline docs, and decisions without necessarily changing files.

**Use when**

- the user wants to inspect drift before syncing
- the user asks what is stale or inconsistent
- the team wants an audit report first

**Primary output**

- drift report
- impacted files and mismatch categories
- recommended follow-up actions

**Non-goal**

- this skill is audit-first, not update-first

### 11. `Baseline Docs Audit Verify`

**Frontmatter name:** `baseline_docs_audit_verify`

**Purpose**

Verify whether claims in the baseline pack are supported by code or explicit user decisions.

**Use when**

- trust in the docs is low
- the user wants to know which claims are proven vs assumed
- roadmap or use guide statements need evidence review

**Primary output**

- verified claims
- unverified claims
- false or outdated claims

### 12. `Baseline Docs Maintain Compact`

**Frontmatter name:** `baseline_docs_maintain_compact`

**Purpose**

Reduce repetition and verbosity while preserving factual truth and operational usefulness.

**Use when**

- the pack became too long
- multiple sections repeat the same information
- resume cost is too high because the baseline is bloated

**Primary output**

- shorter, denser baseline docs
- preserved evidence and canonical state

### 13. `Baseline Docs Maintain Archive`

**Frontmatter name:** `baseline_docs_maintain_archive`

**Purpose**

Close out a finished phase or task and preserve history without cluttering the active baseline.

**Use when**

- an epic or phase is complete
- the active pack should focus only on live work
- old execution history is still valuable but should move out of the main flow

**Primary output**

- archived snapshot of completed state
- cleaner active baseline

### 14. `Baseline Docs Maintain Split`

**Frontmatter name:** `baseline_docs_maintain_split`

**Purpose**

Split one overloaded baseline pack into multiple smaller packs by topic, feature, or workstream.

**Use when**

- one pack covers too many unrelated tasks
- roadmap scope became too large
- resume quality is low because multiple streams are mixed together

**Primary output**

- multiple scoped baseline packs
- clearer ownership and resume boundaries

### 15. `Baseline Docs Maintain Prune`

**Frontmatter name:** `baseline_docs_maintain_prune`

**Purpose**

Remove obsolete, superseded, or misleading content from the active baseline pack.

**Use when**

- old planned sections are no longer relevant
- assumptions were invalidated
- outdated content causes confusion during sync or resume

**Primary output**

- reduced noise
- active pack contains fewer misleading leftovers

## Refactor Scope

### What Changes

- the current monolith skill is renamed and narrowed into `Baseline Docs Init`
- responsibilities are separated into 14 additional micro-skills
- naming becomes family-based and consistent
- `openai.yaml` metadata should align with the new initial skill positioning
- repository layout should evolve from one skill folder to a multi-skill layout

### What Does Not Change

- the baseline pack contract still centers on the same five doc types
- code inspection remains mandatory before writing factual docs
- stale docs are still treated as bugs
- diagrams, roadmap evidence, hallucination tracking, and use guides remain core outputs where relevant

## Proposed Repository Evolution

### Current State

```text
baseline_docs_init/
  SKILL.md
  agents/
    openai.yaml
```

### Target State

```text
baseline-docs-init/
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
```

## Recommended Refactor Phases

### Phase 1 — Freeze Taxonomy

Goal: lock the naming, family structure, and responsibility boundaries.

Tasks:

- confirm all 15 names
- confirm display naming and snake-case frontmatter convention
- confirm which responsibilities leave the current monolith skill

### Phase 2 — Narrow the Existing Skill

Goal: convert current `baseline-docs` into `Baseline Docs Init`.

Tasks:

- update frontmatter name to `baseline_docs_init`
- rewrite description to init-only scope
- remove lifecycle behaviors better owned by sync/resume/maintain skills
- update `openai.yaml` wording to init-oriented language

### Phase 3 — Create Skeleton Micro-Skills

Goal: add the remaining 14 skills as minimal but valid skill folders.

Tasks:

- create folder per micro-skill
- add `SKILL.md` with frontmatter and focused description
- ensure naming consistency across all folders

### Phase 4 — Distribute Behaviors

Goal: move instructions from monolith logic into the right skills.

Tasks:

- move code drift logic into `Sync Codebase`
- move decision propagation logic into `Sync Decisions` and `Sync Decision`
- move contradiction repair logic into `Sync Reconcile`
- move resume recovery logic into `Resume Continue`
- move snapshot and handoff logic into resume family
- move cleanup/archive/split/prune logic into maintain family
- move trust inspection logic into audit family

### Phase 5 — Align Docs and Metadata

Goal: make repository docs reflect the new multi-skill architecture.

Tasks:

- update `README.md`
- update installation examples if needed
- document all 15 skills and their purpose
- clarify which skill is the default entrypoint

### Phase 6 — Validate Skill Boundaries

Goal: reduce overlap and ambiguous triggering.

Validation questions:

- can the user tell which skill to use from the name?
- does each skill solve one clear job?
- are there hidden overlaps that should be merged or renamed?
- does each skill have a clear non-goal section?

## Boundary Rules

To avoid reintroducing monolith behavior, each skill should declare:

- what it is for
- when to trigger it
- what files or outputs it should affect
- what it explicitly does not own

Especially important boundaries:

| Skill | Must avoid becoming |
|---|---|
| `Baseline Docs Init` | a generic catch-all updater |
| `Baseline Docs Sync Codebase` | a resume skill |
| `Baseline Docs Sync Decisions` | a code drift skill |
| `Baseline Docs Resume Continue` | a full compaction skill |
| `Baseline Docs Maintain Compact` | a sync skill |
| `Baseline Docs Audit Drift` | an auto-fix skill |

## Recommended Implementation Order

1. `Baseline Docs Init`
2. `Baseline Docs Sync Codebase`
3. `Baseline Docs Sync Decisions`
4. `Baseline Docs Resume Continue`
5. `Baseline Docs Resume Snapshot`
6. `Baseline Docs Sync Reconcile`
7. `Baseline Docs Audit Drift`
8. `Baseline Docs Maintain Compact`
9. remaining supporting skills

This order prioritizes the most common user pain:

- new baseline creation
- code/docs drift
- decision propagation
- returning to stale work
- reducing entropy over time

## Success Criteria

The refactor is successful when:

- the old monolith behavior is decomposed into 15 clear skills
- the current `baseline-docs` skill becomes init-focused only
- naming is consistent and grouped in the library
- users can pick a skill by intent without reading all skill bodies
- resume, sync, audit, and maintain tasks no longer depend on a single catch-all skill

## Final Recommendation

Do not stop at renaming.

The correct direction is:

1. rename the monolith entrypoint to `Baseline Docs Init`
2. rewrite its body to init-only behavior
3. create the other 14 skills with focused scope
4. update repository docs to present the system as a skill family

This preserves the original value of the project while making the skill library far easier to use, scale, and maintain.
