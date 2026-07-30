# Execution Contract

## Approval policies

| Policy | Behavior |
|---|---|
| `phase` | Implement and verify one phase, update the pack, then wait for approval. |
| `continuous` | Continue through ready phases, checkpointing after each one. |

## Commit policies

| Policy | Behavior |
|---|---|
| `none` | Leave changes uncommitted. |
| `per-phase` | After verification and the docs checkpoint, commit only files belonging to that phase. Requires explicit authorization in the current request. |

## Selection gate

Both policies must be unambiguous before implementation begins. For every invocation style, when the user's request does not clearly determine one or both choices, ask for the unclear choices instead of applying defaults.

For example, `$baselinedocs-run @docpack` leaves both choices unclear, so ask naturally in the user's language:

- whether to pause for approval after each phase or continue through every ready phase
- whether to leave changes uncommitted or create a commit after each verified phase

Do not present internal policy identifiers as a configuration form unless the user requests technical details. Do not infer policy from earlier turns. A reply requesting a commit after each phase provides explicit commit authorization for that run.

## Phase checkpoint

Keep one compact record:

- outcome and status
- final evidence
- changed files
- unresolved risk
- next ready phase

Do not keep a diary of every fixture or command attempt. Preserve an intermediate failure only when it remains actionable or explains the final design.

## Post-initial revisions

Keep a change in the current phase when it adjusts implementation under the same acceptance criteria. Reopen the phase if needed and summarize the revision.

Create a new phase only when at least one condition applies:

- new user-visible or system outcome
- new cross-domain dependency
- new release or approval gate
- separately deployable scope
- enough work to merit independent verification and rollback
