# Adaptive Pack Contract

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

`updated` is the last document edit date. `code_ref` is the code state actually inspected, not the document's own commit. A newer commit is a drift signal, not automatic proof of drift.

## Required documents

- `introduction`: scope, current truth, target, constraints
- `roadmap`: phases, dependencies, status, final evidence, next action
- `hallucination`: open questions and closed decisions

## Conditional documents

- `sourcecode`: include when architecture, code topology, or execution flow will help later work
- `useguide`: include when another consumer needs an API contract, method usage, migration procedure, operator instructions, or black-box behavior

Omit a conditional document when it would contain only `not applicable` filler. Preserve an existing conditional document until its useful content is migrated or pruning is explicitly safe.

## Evidence density

Record final evidence and material unresolved failures. Do not retain every failed fixture run, retry, or intermediate command.

## Multi-pack initiatives

For work spanning dependent domains, keep every domain pack first-class and add `<initiative>/<initiative>.index.md`. The index contains direct links, owners or scopes, status, and dependency edges. It is routing metadata, not a general pack that repeats child content.

Example dependency table:

| Pack | Scope | Depends on | Status | Next checkpoint |
|---|---|---|---|---|
| `identity-api` | Backend contract | - | active | Schema verified |
| `avatar-ui` | Frontend rendering | `identity-api` | blocked | Consume signed URL |

Use a Mermaid dependency graph only when it makes alternating cross-domain order clearer.
