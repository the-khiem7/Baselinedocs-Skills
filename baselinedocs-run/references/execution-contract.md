# Execution Contract

## Approval policies

| Policy | Behavior |
|---|---|
| `phase` | Implement and verify one phase, update the pack, then wait for approval. This is the default. |
| `continuous` | Continue through ready phases, checkpointing after each one. Use only when explicitly requested. |

## Commit policies

| Policy | Behavior |
|---|---|
| `none` | Leave changes uncommitted. This is the default. |
| `per-phase` | After verification and the docs checkpoint, commit only files belonging to that phase. Requires explicit authorization in the current request. |

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
