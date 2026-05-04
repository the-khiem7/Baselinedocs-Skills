---
name: baseline-docs
description: Create and maintain resumable baseline documentation packs for a codebase. Use when asked to make implementation plans, sync docs after code changes, document API contracts, write class or sequence diagrams, track progress, or record unresolved business decisions/hallucination risks.
---

# Baseline Docs

## Overview

Maintain a baseline documentation pack that mirrors the actual codebase state and can be resumed without conversation memory. Update the pack whenever code, requirements, APIs, architecture, or implementation progress changes.

## Inputs

Extract these from the user request, existing repo docs, or nearby context:

- `topic`: business/implementation topic. If blank, infer the nearest feature or ask only when multiple unrelated topics are possible.
- `task list`: requested tasks. If blank, create a roadmap skeleton from the business target and current codebase.
- `business target`: desired business outcome and constraints.
- `docs_dir`: folder where the pack lives. If unspecified and no existing pack is found, use `docs/baseline`.
- `prefix`: filename prefix. If unspecified, use a short kebab-case slug from `topic`; fallback to `baseline`.

## File Contract

Create or update exactly this English documentation pack inside `docs_dir`:

- `<prefix>.introduction.md`: target, current codebase status, implementation direction.
- `<prefix>.roadmap.md`: resumable implementation tracker with status, tasks, decisions, changed files, verification, next actions.
- `<prefix>.hallucination.md`: unresolved choices that require the user's decision because code or business requirements support multiple valid options.
- `<prefix>.sourcecode.md`: class diagrams and sequence diagrams for relevant implemented or desired functions.
- `<prefix>.useguide.md`: API contracts for frontend/mobile developers, including endpoint behavior, request examples, response examples, errors, auth, and black-box usage notes.

Use Mermaid for diagrams when useful. Keep all docs factual, dated, and tied to observed code or explicit user decisions.

## Discovery Workflow

1. Locate the existing baseline pack by searching for the five filenames, then infer `docs_dir` and `prefix`.
2. Inspect the current codebase before writing. Prefer code graph/MCP tools when available; use `rg` for literals, configs, routes, schemas, docs, and unsupported languages.
3. Identify actual implemented state: entry points, modules, API routes, data models, auth, config, jobs, tests, and known gaps.
4. Compare docs against code and requirements. Treat stale docs as bugs.
5. Update every affected baseline file in the same turn when feasible.
6. Run relevant verification commands if docs reference generated contracts, routes, schemas, or tests.

## Roadmap Rules

Make `<prefix>.roadmap.md` sufficient to resume work cold:

- Include topic, business target, docs pack location, current date, current status, scope, out-of-scope items.
- Track each task with `Pending`, `In Progress`, `Blocked`, or `Done`.
- For each completed task, include evidence: files changed, behavior implemented, tests/commands run, and remaining risks.
- End with `Next Resume Step`: the exact next action an agent should take without prior chat memory.
- When code changes, update the roadmap in the same change set.

## Hallucination Risk Rules

Use `<prefix>.hallucination.md` only for decisions that cannot be safely chosen from code/business evidence.

For each open risk, record:

- stable risk id, title, status `Open`
- why the decision is required
- impact if guessed wrong
- concrete options with tradeoffs
- recommended option only when evidence supports it
- required user decision

When the user decides:

1. Change status to `Closed`.
2. Keep the original option list.
3. Add a decision record with date, chosen option, user rationale if provided, and implementation/doc impact.
4. Merge the decision into the affected baseline docs.
5. Update the roadmap with the closed risk and next implementation step.

Do not delete closed risks; they are decision history.

## Sourcecode Doc Rules

In `<prefix>.sourcecode.md`:

- Separate `Observed Current Code` from `Desired/Planned Code`.
- Include diagrams only for relevant flows, not the whole repo by default.
- Document classes/modules, major functions, route handlers, data flow, sequence flows, persistence, external services, error paths, and auth boundaries.
- Mark unknown or planned elements explicitly; do not present guesses as implemented facts.

## Use Guide Rules

In `<prefix>.useguide.md`:

- Write for mobile/frontend developers treating the backend as a black box.
- For each endpoint or callable interface, include method/path, auth, headers, params, request body, success response, error responses, validation rules, side effects, idempotency/retry notes, and sample calls.
- If no API exists yet, document planned contracts under `Planned API` and mark them as not implemented.
- Keep examples minimal but valid JSON.

## Output Behavior

When asked to make a plan, create or update the baseline pack instead of only replying in chat. In the final response, report docs path, files changed, open risks, and next resume step.

When a codebase changed, sync baseline docs before claiming completion.
