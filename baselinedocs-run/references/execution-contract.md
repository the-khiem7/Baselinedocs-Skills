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

A phase commit follows the repository's existing commit message convention and must be indistinguishable in form from the repository's own commits. Do not add authorship, attribution, or tool-generated trailers that the repository's history does not already use. A trailer nobody asked for turns every phase commit into a permanent, unremovable record of how the work was produced rather than what it changed.

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

A lesson entry - a mistake, why it looked reasonable, what disproved it, and the fix - is not a diary entry. Preserve it in full even after the mistake is resolved; it is what prevents the same mistake recurring.

When a checkpoint's evidence includes a defect's cause or a rejected alternative, record that reasoning in `hallucination.md` and link to it from the checkpoint. Do not restate it in the roadmap - a phase checkpoint reports outcome and evidence, not the reasoning behind them.

## Post-initial revisions

Keep a change in the current phase when it adjusts implementation under the same acceptance criteria. Reopen the phase if needed and summarize the revision.

Create a new phase only when at least one condition applies:

- new user-visible or system outcome
- new cross-domain dependency
- new release or approval gate
- separately deployable scope
- enough work to merit independent verification and rollback
