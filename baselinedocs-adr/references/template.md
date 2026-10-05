# ADR template (AWS Prescriptive Guidance format)

Source: `https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/appendix.html`

Copy the structure below for every new ADR. Keep every heading even when a section is short - a one-line **Compliance** or **Notes** section is fine, an omitted heading is not.

```markdown
# ADR-NNNN: <Title>

## Status

Proposed | Accepted | Rejected | Superseded by ADR-NNNN

## Date

YYYY-MM-DD

## Context

<The forces at play - technical, business, and team constraints - that make this decision necessary. State the problem and the options that were on the table neutrally. If an alternative was seriously considered and rejected, say so here and give the reason, so it is not re-proposed later.>

## Decision

<The choice made, stated actively: "We will ...". Include enough detail that someone who was not in the discussion understands what changes as a result.>

## Consequences

Positive:
- <benefit>

Negative:
- <cost, risk, or follow-up work created by this decision>

## Compliance

- <A concrete, checkable rule that follows from the decision. Used during code and architecture review to check conformance. Omit this section if there is nothing checkable.>

## Notes

- Author: <name>
- Version: <e.g. 0.1>
- Changelog:
  - 0.1: Initial proposed version
```

## Field definitions

- **Title** - names the decision, not the problem. "We use an adapted GitFlow for ABC application development", not "Branching strategy problem".
- **Status** - one of `Proposed`, `Accepted`, `Rejected`, `Superseded by ADR-NNNN`. See [process.md](process.md) for the state transitions.
- **Date** - the date the status last changed, not the date the file was created.
- **Context** - explains *why* a decision is needed, without arguing for a particular answer. Good context lets a future reader understand the decision even after the original constraints have changed.
- **Decision** - the single sentence-or-paragraph statement of what was decided, written so it can be quoted during a code review ("this violates ADR-0007's decision that...").
- **Consequences** - both positive and negative. An ADR with only positive consequences usually means the trade-offs were not thought through.
- **Compliance** - optional, but valuable when the decision implies rules that can be checked mechanically or in review (e.g. "the main and develop branches must be marked Protected").
- **Notes** - optional metadata: author, version, and a changelog of substantive edits made while the ADR was still `Proposed`. Do not use the changelog to record edits made after acceptance - an accepted ADR does not get edited (see process.md).
