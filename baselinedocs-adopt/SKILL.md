---
name: baselinedocs-adopt
description: Adopt an existing document, proposal, specification, wiki, export, or other non-baseline format into an adaptive baseline documentation pack. Use when the source material must be distributed into a durable, resumable baselinedocs structure without losing its information, decisions, assumptions, risks, provenance, or open questions.
---

# Baselinedocs Adopt

Adopt source material into a baseline pack that is collectively equivalent in information, but easier to navigate, update, audit, and resume. Do not reconstruct the source as a replacement god document.

## Inputs

Determine or confirm:

- the source artifact or source set
- the target baseline root and pack prefix
- whether a suitable pack already exists
- the source-retention decision: retain, archive separately, or remove after validation
- the source's authority and the meaning of its claims

Read `baselinedocs-init` when creating a new pack. Read the relevant lifecycle skill when updating an existing pack.

## Workflow

1. Inspect the complete source before editing. Record its scope, headings, decisions, requirements, workflows, assumptions, risks, open questions, and explicit exclusions.
2. Inspect the repository, canonical documentation, existing baseline pack, and worktree state. Do not treat source-document claims as implementation evidence.
3. Choose the target layout: extend a suitable existing domain pack; create one bounded-domain pack; or create an initiative index with linked domain packs for independent or dependent domains.
4. Create or update the pack documents so their combined content preserves the source information. Distribute material by purpose; do not add a replacement catch-all document.
5. Preserve provenance for every adopted claim, including the source artifact and the point-in-time interpretation where useful.
6. Mark each claim accurately as `implemented`, `planned`, `decided`, `unverified`, or historical. Resolve contradictions only with repository evidence or an explicit decision.
7. Write a coverage ledger mapping every source section or requirement to its destination baseline document. Include exclusions and intentionally consolidated material.
8. Validate that the pack answers the same substantive questions as the source: why, scope, behavior, architecture, users/operations, decisions, risks, verification state, roadmap, and next action.
9. If source removal was authorized, remove it only after coverage validation succeeds. If retention was required, follow the agreed retention method. Never infer either choice.
10. Report changed paths, coverage result, unresolved gaps, source-retention result, and the next executable action.

## Document Roles

Use the smallest applicable set:

- `*.introduction.md`: purpose, scope, stakeholders, boundaries, vocabulary, decisions, and known risks.
- `*.sourcecode.md`: code-inspected architecture, integrations, data/control flow, and evidence boundaries.
- `*.useguide.md`: user and operator workflows, expected behavior, limitations, and operational guidance.
- `*.roadmap.md`: ordered work, dependencies, acceptance criteria, verification gates, unresolved decisions, and one exact next action.
- `*.index.md`: initiative navigation and cross-domain relationships when multiple packs are necessary.

Do not force content into a file whose role does not fit. Add a narrowly scoped domain pack when separation improves discoverability without duplicating truth.

## Coverage Rules

- Preserve information, not paragraph shape or source-file structure.
- Keep exact requirements, constraints, names, state transitions, ownership boundaries, and negative requirements traceable.
- Preserve open questions as open; do not silently decide them during conversion.
- Preserve explicit unknowns and unsupported claims as unverified.
- Distinguish proposal intent from code, test, deployment, and runtime evidence.
- Do not claim builds, formatting, static inspection, or documentation review prove live behavior.
- Do not delete, archive, commit, or otherwise alter the source artifact unless the user explicitly authorizes that action.
- If lossless retention is required, verify raw-byte identity; a normalized hash or matching headings is insufficient.

## Output

Produce a baseline pack that is collectively equivalent in information to the adopted source while being easier to navigate, update, audit, and resume.
