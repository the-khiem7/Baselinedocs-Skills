---
baseline_schema: "2.0"
pack: "academy"
document: "introduction"
status: "draft"
updated: "2026-10-25"
code_ref: "d26f99f"
---

# Academy

## Scope

Design a new sub-family of the `baselinedocs` skill family, branded `academic`, that reads the baseline packs of many projects and composes a knowledge base of lessons from them. The purpose is to learn from operating projects and to hand that knowledge to another person.

In scope: the `baselinedocs-academic-*` skills, the core skill `baseline-academic-core`, their tests, and the repository files that list the family (`AGENTS.md`, `README.md`, `scripts/stamp_version.py`, the sets in `tests/`).

Out of scope: any change to the pack schema or to `baseline-core`; any write into a project that is read; publishing the output outside the local machine.

## Current truth

| Fact | State |
|---|---|
| `baseline-academic-core` | exists, holding `references/academic-contract.md`; stamped with the family version |
| any `baselinedocs-academic-*` skill | none exists yet |
| source projects | every folder under `C:\.repos\Work\` that holds `docs/baseline/`; not enumerated here, because the set changes |
| external course-building skill | none installed; ACA-D7 records what was read and rejected |
| `baseline-core` | holds `pack-contract.md`, `report-style.md` and `packtool.sh` once, reached as `<skill-dir>/../baseline-core` (`baselinedocs` BLD-D54) |

## Target

One skill, `baselinedocs-academic-compose`, works in three modes (ACA-D10): project scoped inside one project repo, a named topic across several projects, or topics suggested across several projects. It reads packs read-only and writes a standalone local HTML knowledge base of lessons; project-scoped output is written inside that project repo (ACA-D12). Every point in a lesson cites the pack entry it came from, project names and account or host identifiers are replaced with neutral labels, and nothing in a source project is modified.

`baseline-academic-core` holds the rules that only the lesson product needs: the lesson format, the anonymization rules, the citation rule. It is a skill that is not a workflow, like `baseline-core`.

## Constraints

| Constraint | Source |
|---|---|
| output is local HTML only, never published to a hosted service | ACA-D6 |
| source packs are read, never written | ACA-D4 |
| output is anonymized before it is written | ACA-D5 |
| every claim in a lesson cites a source entry; a gap is marked, not filled | ACA-D7, ACA-D8 |
| no external skill is installed; reused `teach` text keeps its MIT notice | ACA-D7, ACA-D15 |
| the anonymizer's mapping file lives outside every repository | ACA-D13 |
| HTML is written in the directory the skill is called from | ACA-D14 |
| user is a standard Windows account; no step may need elevation | machine privileges rule in the user's global instructions |
