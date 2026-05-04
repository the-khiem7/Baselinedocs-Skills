# Baselinedocs Skills

Skills.sh-compatible repository for the `baseline-docs` skill.

`baseline-docs` helps agents create and continuously sync a baseline documentation pack for a codebase. The goal is to keep docs aligned with the actual implementation, business decisions, API contracts, diagrams, and current roadmap so work can resume without prior conversation memory.

## Install

Install from GitHub:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baseline-docs
```

Install globally without prompts:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git --skill baseline-docs --global --yes
```

Install from the default branch without selecting a skill:

```bash
npx skills add https://github.com/the-khiem7/Baselinedocs-Skills.git
```

## Local Install

From a cloned copy of this repository:

```bash
npx skills add . --skill baseline-docs
```

List available skills:

```bash
npx skills add . --list
```

## Skill: `baseline-docs`

Use this skill when you need to:

- create a baseline documentation pack for a codebase
- sync docs after code changes
- make an implementation roadmap that can be resumed later
- document unresolved business or technical decisions
- write source-code diagrams for implemented or planned behavior
- write API contracts for frontend or mobile developers

The docs pack contains:

- `<prefix>.introduction.md` - target, current status, implementation direction
- `<prefix>.roadmap.md` - progress tracker, evidence, next resume step
- `<prefix>.hallucination.md` - unresolved decisions and closed decision records
- `<prefix>.sourcecode.md` - class diagrams and sequence diagrams
- `<prefix>.useguide.md` - API contracts, request/response examples, black-box usage notes

## Repository Layout

```text
baseline-docs/
  SKILL.md
  agents/
    openai.yaml
README.md
```

## Compatibility

This repository is structured for the Skills.sh CLI. The skill folder contains a `SKILL.md` file with `name` and `description` frontmatter, which is the format detected by:

```bash
npx skills add . --list
```
