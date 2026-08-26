# Adaptive Pack Contract

## Before writing

The gate that requires reading this file lives in each skill's `SKILL.md`, because a rule that exists only inside a file the agent may not open cannot enforce opening that file. This section records why the gate exists.

Content written into a document whose role does not cover it does not stay contained. It gets duplicated once the correct owner also turns out to need the same fact, and the copies drift as later corrections land in only one of them. In the recorded incident, execution status and evidence were written into two documents whose roles are decisions and architecture, while the document whose role actually covers evidence and next action already existed, already had an established pattern for that exact content, and was never opened.

Decide placement from the role lists below, every time. Do not infer it from a filename, from an earlier session, or from memory of this contract.

## Frontmatter

Every baseline document starts with:

```yaml
---
baseline_schema: "2.0"
pack: "<kebab-case-pack>"
document: "<introduction|roadmap|hallucination|sourcecode|useguide|index>"
status: "<draft|active|blocked|complete|archived>"
updated: "YYYY-MM-DD"
code_ref: "<commit|uncommitted|unknown>"
---
```

`updated` is the last document edit date. `code_ref` is the code state actually inspected, not the document's own commit. Use `uncommitted` for an inspected working tree and `unknown` when provenance cannot be established. A newer commit is a drift signal, not automatic proof of drift.

## Required documents

- `introduction` (`<prefix>.introduction.md`): scope, current truth, target, constraints
- `roadmap` (`<prefix>.roadmap.md`): phases, dependencies, status, final evidence, risks, next action
- `hallucination` (`<prefix>.hallucination.md`): the why - open questions, closed decisions, a defect's cause, rejected alternatives

A closed decision records four things: what was decided, why, what breaks if it is ignored, and which alternatives were rejected with their reasons. A decision recorded without its reasoning is one the next reader optimizes away, because nothing tells them what it was protecting. A rejected alternative that is not written down gets proposed again.

## Reasoning ownership

`roadmap` records the outcome: what happened, the final evidence, and the next action. `hallucination` records the why: a defect's cause, rejected alternatives, the reasoning behind a fix. When a roadmap entry needs to explain why something happened, link to the matching hallucination entry instead of restating its reasoning. Duplicating the same narrative in both documents means every later correction has to be made twice, and they drift when it isn't.

## Disproven claims

A claim that code or an explicit decision has disproven moves into `hallucination` as a closed entry recording what was believed and what disproved it. The document whose role is current truth stops asserting it. The claim is not deleted.

Owners: `sync-codebase` when code disproved it, `sync-decisions` when a decision closed it, `save` when the current thread established it.

Deleting the claim loses the only record that the belief was ever held, and a later agent re-derives it from the same evidence that produced it the first time. `hallucination` is a journal, and a defeated approach kept beside what defeated it is what stops that approach being proposed again. Nothing in an active pack is removed on the grounds that it is no longer true. It is relocated.

## Conditional documents

- `sourcecode` (`<prefix>.sourcecode.md`): architecture, code topology, execution flow. Include when that shape will help later work.
- `useguide` (`<prefix>.useguide.md`): consumer contract, API or method usage, migration procedure, operator guidance. Include when a consumer outside this pack depends on the behavior.

Omit a conditional document when it would contain only `not applicable` filler. Preserve an existing conditional document until its useful content is migrated or pruning is explicitly safe.

## Evidence density

Record final evidence and material unresolved failures. Do not retain every failed fixture run, retry, or intermediate command.

A lesson entry - a mistake with why it looked reasonable, what disproved it, and the fix applied - is not a retry or an intermediate command. Keep it in full even after the mistake is resolved, both when writing it and when compacting the document later. Trimming it to its final state, or dropping it because it is fixed, discards the reason it exists, which is what prevents the same mistake recurring.

Do not present a build, a formatter, a static check, or a documentation review as proof of live runtime, integration, or deployment behavior. Record what was observed running.

Write terse. Use a table for options, comparisons, and status. Do not add changelog-style notes about what was just corrected, and do not create a side file to explain an edit; edit the target document only. A pack that accumulates edit commentary becomes the transcript this policy exists to prevent. Use the ASCII hyphen. Do not emit an en dash or an em dash.

## Boundary with code

A pack is internal operational memory. Never reference a pack filename or a pack section from inside code, configuration, infrastructure resource descriptions, or anything else that ships outside the repository. State the technical reason in place instead.

This has happened: infrastructure resource descriptions cited a pack's `hallucination` document by filename, and those descriptions were visible in a cloud provider console to everyone with account access, where the referenced filename means nothing.

## Multi-pack initiatives

For work spanning dependent domains, keep every domain pack first-class and add `<initiative>/<initiative>.index.md`. The index contains direct links, owners or scopes, status, dependency edges, and the current cross-pack checkpoint. It is routing metadata, not a general pack that repeats child content.

Example dependency table:

| Pack | Scope | Depends on | Status | Next checkpoint |
|---|---|---|---|---|
| `identity-api` | Backend contract | - | active | Schema verified |
| `avatar-ui` | Frontend rendering | `identity-api` | blocked | Consume signed URL |

Use a Mermaid dependency graph only when it makes alternating cross-domain order clearer.
