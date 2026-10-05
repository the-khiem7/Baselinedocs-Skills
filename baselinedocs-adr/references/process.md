# ADR process (AWS Prescriptive Guidance)

Source: `https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html`

## What an ADR is

An ADR records one architecturally significant decision: its context, the decision, and its consequences. The full set of ADRs in a repo is the decision log - skim titles for a project overview, read individual ADRs for implementation detail.

Accepted ADR -> immutable. New insight requires a different decision -> write a new ADR; once that one is accepted, it supersedes the old one.

## Scope - when a decision needs an ADR

Create an ADR for any decision affecting (Richards and Ford, 2020):
- Structure - architectural patterns, e.g. microservices.
- Non-functional requirements - security, high availability, fault tolerance.
- Dependencies - coupling between components.
- Interfaces - APIs and published contracts.
- Construction techniques - libraries, frameworks, tools, processes.

Functional and non-functional requirements are the most common inputs.

## Contents

Write every ADR from the shared template ([template.md](template.md)). At minimum: context, decision, consequences.

Focus each ADR on why, not how - the reasoning is what lets other team members adopt the decision, and stops an architect who was not part of the discussion from overruling it later without engaging that reasoning.

## Ownership

Any team member may create an ADR. Assign one owner per ADR - the owner maintains and communicates its content. Other members may contribute; the owner approves any change made before the ADR is accepted.

## Lifecycle

1. Proposed - owner drafts the ADR, opens it for review.
2. Review - team reads the ADR (10-15 min), then discusses comments as a group. One of:
   - Rework needed -> stays `Proposed`. Owner assigns an action item per comment, re-schedules the review once they are addressed.
   - Rejected -> owner records the rejection reason in Context or Notes so the option is not re-proposed later, sets status `Rejected`.
   - Accepted -> owner adds date, version, and stakeholders, sets status `Accepted`.
3. Accepted / Rejected -> immutable. Required change -> write a new ADR; never edit Decision or Consequences in place.
4. Supersede -> take the new ADR through review and acceptance first, then set the old ADR's status to `Superseded by ADR-NNNN`. Never delete a superseded ADR.

## In use

Every code change goes through peer review with at least one approval. Reviewer finds a change that violates an ADR -> ask the author to update the code, link the ADR. Consult the decision log directly for product-strategy decisions too, not only during review.

## Applying this to the skill's workflow

- Default a freshly drafted ADR to `Proposed` unless the user states the decision is already agreed by the team.
- Treat `Accepted` and `Rejected` as read-only for Decision/Consequences - only status, date, and Notes may change afterward.
- Create the new ADR first when superseding - flip the old ADR's status only once the new one is actually accepted, never while it is still `Proposed`.
