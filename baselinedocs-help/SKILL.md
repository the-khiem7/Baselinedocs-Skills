---
name: baselinedocs-help
description: Explain what each baselinedocs skill does and in what order to use them, from a plain question such as which skill to use, what a skill does, what comes after run, or how the workflow goes. Use when the user asks for help, a list of the baselinedocs skills, the workflow, or which skill fits their situation, and does not need a pack read.
version: "0.0.0"
---

# Baseline Docs Help

Tell the user what each `baselinedocs` skill does and which one to call next. This reads no pack and writes nothing.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a skill or a pack element is named in conversation; a name stated without its meaning is a question the user has to ask.

Read `references/guide.md` in full before answering, every time. It is the only source for the skill list and the workflow; do not answer from memory of an earlier session or from the one-line descriptions of whatever skills happen to be installed.

## Workflow

1. Read the guide.
2. When the user describes a situation, name the skill that fits, the step that follows it, and any trap in the guide that applies.
3. When the user names a skill, give its row from the guide and where it sits in the workflow.
4. When the user asks nothing specific, give the workflow diagram and the skill table.
5. When the guide does not cover the question, say so. Do not invent a skill or a step.
6. Stop. Do not run a skill, read a pack, or begin work unless asked.

## Rules

- The guide describes the family, not what is installed on this machine. A skill it names may be absent here; say so rather than implying every row is callable.
- Do not read, summarize, or assess a pack to answer. `baselinedocs-brief` reports where work stands and `baselinedocs-onboard` loads a pack.

## Output

- when a situation was described: the skill to call and the step after it, first
- otherwise: the workflow diagram, then the skill table
- the trap that applies, when one does

## Non-Goals

- not a pack read or status report; `baselinedocs-brief` and `baselinedocs-onboard` do that
- does not run any other skill
- writes no files
