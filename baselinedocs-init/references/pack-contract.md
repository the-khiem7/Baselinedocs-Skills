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

`updated` is the document edit date. `code_ref` identifies the code state actually inspected. Use `uncommitted` for an inspected working tree and `unknown` when provenance cannot be established.

## Core documents

- `<prefix>.introduction.md`: scope, current truth, target, and constraints
- `<prefix>.roadmap.md`: phases, dependencies, evidence, risks, and next action
- `<prefix>.hallucination.md`: open questions and closed decisions

## Conditional documents

- `<prefix>.sourcecode.md`: architecture, topology, diagrams, and implementation flow
- `<prefix>.useguide.md`: consumer-facing API or method contract, migration procedure, operator instructions, or black-box usage

Do not create a conditional document that would only contain filler.

## Multi-domain layout

Keep each domain pack directly addressable. Add `<initiative>/<initiative>.index.md` with:

- direct links to every pack
- scope and status
- dependency edges
- current cross-pack checkpoint

The index routes work; it does not duplicate the child packs as a general abstraction layer.

## Evidence density

Store final verification results and material unresolved failures. Omit routine failed attempts that no longer affect current truth.
