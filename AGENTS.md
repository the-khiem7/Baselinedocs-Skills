# Working in this repository

This repo is the source of the `baselinedocs` skill family. Everything here is authored to be installed elsewhere, one skill at a time.

## What ships and what does not

`npx skills add <repo> --skill <name>` installs a single skill folder. Nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/references/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `tests/`, `scripts/`, `.github/`, `assets/`, `docs/baseline/` | no | whoever works in this repo |

Consequences:

- **A skill may rely on anything inside its own folder.** That is what `<skill>/references/` is for, and it ships. The one exception is `baseline-core`, below. The boundary is the folder, not the act of reading a file.
- **Name a sibling skill for routing.** "`baselinedocs-maintain-split` creates one" tells the reader where to go next and holds whether or not that skill is installed. The `Non-Goals` sections across the family are built on this.
- **Never make a sibling's content a prerequisite, except `baseline-core`.** Not "read `baselinedocs-init`", not a path through `../`, not a sibling's `references/`. `baseline-core` is the single exception (BLD-D54): it is installed with the family, every reading skill fails closed without it, and no other sibling may be read this way. Naming a skill is routing; requiring its content is a dependency that resolves to nothing when the skill is installed alone. That is the historical bug here: `baselinedocs-adopt` shipped with "Read `baselinedocs-init` when creating a new pack", and the folder it named was usually absent. Note that the broken line contained no path at all, so "avoid paths" is not the test - "does this run need another folder present" is.
- Do not justify cutting something from a `SKILL.md` on the grounds that it is written down in `docs/baseline/`. No installed agent can open a doc pack.

## Where reasoning goes

`docs/baseline/` is the decision log: the full argument, the alternatives that were rejected, and why. Record decisions there, including what breaks if one is ignored. Two packs, routed by `docs/baseline/baseline-gateway.index.md`:

| Pack | Owns |
|---|---|
| `docs/baseline/baselinedocs/` | the design of the family as a whole: trigger architecture, pack schema, checkpoint model, rule placement, workflow sequence, the onboard scope gate, evidence retention, `useguide`, execution policy, multi-pack routing |
| `docs/baseline/skill-consolidation/` | which skills were merged, deleted, or renamed, and the criterion that decided each |

Identifiers carry their pack prefix, `BLD-` or `SC-`, so a reference is unambiguous wherever it is read. `baselinedocs.hallucination.md` BLD-D30 records why.

A `SKILL.md` is an instruction executed fresh on every run, not a decision log. It carries a WHY clause only where the agent has a plausible reason to break the rule and would otherwise talk itself out of it.

| Line | WHY? |
|---|---|
| `Report the line counts read` | no. Nobody argues with it |
| `Read every file in the agreed scope in full` | no |
| `Never write the index` | yes. The agent wants to be helpful |
| `Do not answer around the gap as though it were closed` | yes. The agent wants to look competent |

A bare prohibition with an appealing counter-argument gets overridden mid-run. A self-evident instruction padded with justification protects nothing and costs tokens on every invocation. `SKILL.md` length is not cosmetic: the whole body loads each time the skill runs, and for a skill whose job is to conserve context, its own bulk works against it.

## The shared core

`baseline-core` is a skill that holds the three assets every `baselinedocs-*` skill reads: `references/pack-contract.md`, `references/report-style.md` and `scripts/packtool.sh`. Nothing else holds a copy. `baselinedocs-brief`, `audit-claims`, `audit-drift` and the rest read it from the sibling folder, `<skill-dir>/../baseline-core`, written `<core-dir>` in every `SKILL.md`. `docs/baseline/baselinedocs/` BLD-D54 records why this replaced byte-identical copies, and what a lone install now loses.

- Edit the file in `baseline-core/` and nothing else. There is no copy to resync.
- `baseline-core` is not a workflow: it carries `allow_implicit_invocation: false`, the `Baseline Docs Internal:` display prefix, and the family `version:`, stamped by the release with the rest.
- Every `SKILL.md` that reads any of the three assets carries one sentence defining `<core-dir>` that fails closed: when the folder is missing the skill stops and names `baseline-core`. A skill that guessed instead would write or report a pack from memory, which is the failure the contract exists to prevent.
- Never restate the document roles anywhere else.

### The pack contract

`pack-contract.md` is the only definition of which baseline document owns which content. The 11 pack-writing skills gate on it before a write, and `baselinedocs-onboard` before reporting pack state, because it reads every document in full and reports content sitting in the wrong one.

- A skill gates on the contract when it writes pack files, or when it reads every document in full and reports placement. The test is a full read, not the absence of writes: `baselinedocs-brief` reads nothing in full and neither `audit` skill compares placement, so a gate there would let a skill report conformance it never checked.
- One exception reads no pack at all: `baselinedocs-recall` re-reads the contract and report style after a context compaction, because restoring them is its whole job. It reports nothing about a pack, so the conformance objection does not reach it.
- Each gate sentence in a `SKILL.md` is worded for what the skill does with the file: before a write, or before reporting pack state. Both wordings are pinned. That gate cannot live in the contract: an agent that skipped the file never reaches the sentence telling it not to skip the file.
- A skill without a gate is not missing one. An onboard run once reported the absent contract in a read-only skill as a defect and concluded that future pack writes were blocked; no write routes through a read-only skill, and adding the gate to one fails `test_references.py`.

`tests/test_references.py` pins the gates, the `<core-dir>` sentence and the absence of copies.

### Report style

`report-style.md` governs what the agent says to the user, not what it writes into a pack. It covers two things: how a pack element or a quotation is named so the reader can act on it, and how a report is shaped so the reader can scan it. Every skill gates on reading it, because every one of them produces a report that cites pack elements.

It is a second asset rather than a section of the contract on purpose. The contract's audience is skills that write a pack or read one in full, and `baselinedocs-brief` is neither: it must not be gated on the role list, because a partial reader holding it would report conformance it never checked. It still cites element identifiers in every report it produces. Folding the two files would force the wrong audience on one of them, so they stay separate and are pinned separately.

### The pack tool

`packtool.sh` is the only implementation of the mechanical pack check: `outline`, `find`, `next-id`, `close-plan`, `check`. Every pack-writing skill, `baselinedocs-onboard`, and both `audit` skills run it from `<core-dir>/scripts/packtool.sh`.

- `tests/test_references.py` pins the gate sentences (`TOOL_SKILLS`).
- POSIX sh and POSIX awk only: no gawk extensions, no regex intervals, no `find(1)`. CI runs it under mawk, BWK awk, and Git for Windows gawk.
- It never writes, never touches the network, and runs git read-only. Keep it that way: an installed skill executes it inside other teams' repositories.
- `tests/test_packtool.py` holds one case per rule. A new rule needs a case.

## The self-upgrade skill

`baselinedocs-self-upgrade` upgrades the installed skills, not a pack. It is a family skill (`baselinedocs-*`, shared `version:`, stamped by the release) so it can compare and upgrade itself.

- It ships `scripts/upgradekit.sh` (`inventory`, `compare`), the one script a family skill owns outright. It lives in `baselinedocs-self-upgrade` rather than `baseline-core`: it has a single consumer. `tests/test_conventions.py` names it in `OWN_SCRIPTS`, and `tests/test_upgradekit.py` is its test surface and builds a fake home in a temporary directory.
- `upgradekit.sh` obeys the `packtool.sh` rules: POSIX sh and awk only, never writes, never touches the network, does not run git. The agent runs `git ls-remote`, `npx skills update`, the clone, and every write, so the script stays safe to run inside any machine.
- It finds installs by globbing `$HOME/.<agent>/skills` and `$HOME/.<agent>/<sub>/skills`, not from a list of agents. A list goes stale with every new agent; `.config/devin`, `.config/goose`, and `.gemini/skills` were found only because the scan is a glob.
- The `kind` column is a hint. Git for Windows `[ -L ]` reads a junction as a plain directory, so the skill checks the link type itself before it replaces or deletes a path. Writing through a junction would damage the shared copy every agent reads.

## Conventions

- ASCII hyphen only. No en dash, no em dash. Enforced by `test_no_typographic_dashes` across every `.md`, `.yaml`, `.yml`, `.txt`, `.py`, and `.ini` file Git lists for the repo.
- State the pack-writing skill count in one sentence only, the one under `The pack contract`. Everywhere else say "every pack-writing skill". `test_references.py` pins that sentence against `WRITER_SKILLS` and fails on a second one, because a count repeated in prose goes stale the next time a skill is added or removed. It is pinned to `WRITER_SKILLS` rather than `CONTRACT_SKILLS` because a full reader ships the contract too, so the two counts differ and the prose is about writing.
- Before merging or deleting a skill, read `docs/baseline/skill-consolidation/skill-consolidation.hallucination.md` SC-D1. The merge test is two conditions, not one, and two plausible-looking alternatives are recorded there as rejected so they are not proposed again.
- Skill folder shape: `SKILL.md`, `agents/openai.yaml`, `references/` only when needed, and no copy of the shared assets. `baselinedocs-self-upgrade` also owns `scripts/upgradekit.sh`. `baseline-core` holds `references/` and `scripts/packtool.sh` only.
- User entrypoints set `allow_implicit_invocation: false`. Lifecycle skills keep it enabled and prefix their display name with `Baseline Docs Internal:`. `baselinedocs-recall` is the one lifecycle skill named `Baseline Docs: Recall` without `Internal`, because a user calls it by hand as often as an agent selects it.
- That policy field is Codex-only. On other hosts the `description` frontmatter is the real selection surface, so it must carry the vocabulary a user would actually type.

## Releases

Every `SKILL.md` carries one top-level `version:`, shared by the whole family. Never edit it by hand: commit the work to `main`, then run `uv run scripts/release.py vMAJOR.MINOR.PATCH`. It stamps every `SKILL.md`, runs the suite, commits `release: vX.Y.Z`, and tags that commit, so the tag holds the stamped tree. It never pushes: run the two `git push` commands it prints. `.github/workflows/release.yml` only verifies, with `stamp_version.py --check`, that every `SKILL.md` carries the tag's version, and holds read-only permission. Tags up to `v3.2.1` were cut the earlier way, on the commit before the stamp. `tests/test_version.py` fails when the skills disagree.

## Tests

```bash
uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q
```

pytest is pinned because bare `uvx pytest` takes whatever is newest. PyYAML is test-only: it parses `SKILL.md` frontmatter, `agents/openai.yaml`, and pack frontmatter. The repo has no `pyproject.toml`, so `uv run python -m pytest` does not work; `pytest.ini` holds the config.

Adding a skill fails a test that names the set to update: `WRITER_SKILLS`, `READER_SKILLS`, `LOADER_SKILLS`, `RECALL_SKILLS`, or `REPORT_STYLE_EXEMPT` in `tests/test_references.py`, and `ENTRYPOINTS` in `tests/test_skill_metadata.py`. Shared helpers live in `tests/helpers.py`.

`.gitattributes` forces LF on text assets, because `sh` cannot run `baseline-core/scripts/packtool.sh` with CRLF endings.
