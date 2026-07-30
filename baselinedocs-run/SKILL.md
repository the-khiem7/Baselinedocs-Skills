---
name: baselinedocs-run
description: Execute an initialized baseline roadmap phase by phase with durable checkpoints, optional approval gates, and explicitly authorized phase commits. Use explicitly when the user asks the agent to implement all phases or run a loop-engineering workflow from an existing pack.
---

# Baseline Docs Run

Execute the active roadmap while keeping the pack resumable after every material phase.

## Inputs

Resolve from the current request and pack:

- active pack or initiative index
- phase order and dependencies
- `approval_policy`: `phase` by default; `continuous` only when explicitly requested
- `commit_policy`: `none` by default; `per-phase` only when explicitly authorized in the current request
- verification commands and release gates

Read `references/execution-contract.md` before execution.

## Workflow

1. Validate that the roadmap has executable phases, acceptance criteria, and dependency order.
2. Confirm current repository state and preserve unrelated user changes.
3. Execute the next ready phase.
4. Verify the phase in proportion to risk.
5. Checkpoint the pack before starting another phase:
   - current phase status
   - final evidence and affected files
   - open risks and exact next action
   - document frontmatter
6. If `approval_policy` is `phase`, stop for approval after the checkpoint.
7. If `commit_policy` is `per-phase`, commit only phase-related code and docs after verification. Follow the requested convention and never add co-author trailers unless explicitly requested.
8. Continue until all authorized phases are complete or a real blocker requires the user.

## Revision Policy

Treat post-initial corrections as revisions of an existing phase when they preserve its outcome, acceptance criteria, and dependency boundary. Add a new phase only when the change introduces a distinct outcome, dependency, release gate, or independently reviewable scope.

Aggregate small revisions under a `Revision summary` entry. Do not create one phase per feedback turn.

## Safety

- Selecting this skill is not permission to commit.
- Do not commit unless the current user request explicitly authorizes it.
- Do not mark runtime, deployment, integration, or external-service behavior verified from build or formatting checks alone.
- Do not begin a dependent phase when its prerequisite is unverified.
