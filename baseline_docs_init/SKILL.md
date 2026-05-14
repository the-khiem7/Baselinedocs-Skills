---
name: baseline_docs_init
description: Create the first baseline documentation pack for a codebase, task, feature, or initiative. Use when no baseline pack exists yet and you need an initial introduction, roadmap, hallucination log, sourcecode doc, and use guide.
---

# Baseline Docs Init

## Purpose

Create a new baseline documentation pack from scratch.

This skill is the initialization entrypoint for the Baseline Docs skill family. It should be used when a task, feature, or initiative does not yet have a baseline pack.

## Use When

- the user starts a new task and no baseline pack exists yet
- the user wants an initial implementation roadmap
- the user wants a first-pass introduction, decision log, code diagrams, and API/use guide
- the existing baseline is missing most or all required files

## Inputs

Extract these from the user request, existing repo docs, or nearby context:

- `topic`: business or implementation topic; infer it when possible
- `task_list`: requested tasks; create a starter roadmap if missing
- `business_target`: desired outcome and constraints
- `docs_dir`: folder where the pack should live; default to `docs/baseline` if unspecified and no pack exists
- `prefix`: filename prefix; default to a short kebab-case slug from `topic`, fallback to `baseline`

## File Contract

Create exactly this English documentation pack inside `docs_dir`:

- `<prefix>.introduction.md`
- `<prefix>.roadmap.md`
- `<prefix>.hallucination.md`
- `<prefix>.sourcecode.md`
- `<prefix>.useguide.md`

## Initialization Workflow

1. Confirm that a suitable baseline pack does not already exist.
2. Inspect the current codebase before writing.
3. Identify current implemented state relevant to the topic.
4. Generate the five baseline files with factual, dated content.
5. Make the roadmap resumable from a cold start.
6. Record unresolved decisions only when the code and business context do not support a safe choice.

## Writing Rules

- Keep all docs factual and tied to observed code or explicit user decisions.
- Use Mermaid when diagrams improve understanding.
- Mark planned or unknown behavior explicitly.
- Do not present guesses as implemented facts.

## Non-Goals

This init skill is not the primary owner for:

- syncing docs after later code changes
- propagating closed decisions into an existing pack
- reconciling contradictions inside an existing pack
- compacting, pruning, splitting, or archiving an existing pack
- resuming a stale task after long inactivity

Use the other Baseline Docs micro-skills for those lifecycle tasks.

## Output Behavior

When asked to create a plan for a new task, create or initialize the baseline pack instead of only replying in chat. In the final response, report the docs path, files created, open risks, and the first next step.
