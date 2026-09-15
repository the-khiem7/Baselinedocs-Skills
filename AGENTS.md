# Working in this repository

This repo is the source of the `baselinedocs` skill family. Everything here is authored to be installed elsewhere, one skill at a time.

## What ships and what does not

`npx skills add <repo> --skill <name>` installs a single skill folder. Nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/references/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `contract/`, `tests/`, `docs/baseline/` | no | whoever works in this repo |

Consequences:

- **A skill may rely on anything inside its own folder.** That is what `<skill>/references/` is for, and it ships. Every skill shipping `references/pack-contract.md` reads its own copy on every run and must keep doing so. The boundary is the folder, not the act of reading a file.
- **Name a sibling skill for routing.** "`baselinedocs-maintain-split` creates one" tells the reader where to go next and holds whether or not that skill is installed. The `Non-Goals` sections across the family are built on this.
- **Never make a sibling's content a prerequisite.** Not "read `baselinedocs-init`", not a path through `../`, not a sibling's `references/`. Naming a skill is routing; requiring its content is a dependency that resolves to nothing when the skill is installed alone. That is the historical bug here: `baselinedocs-adopt` shipped with "Read `baselinedocs-init` when creating a new pack", and the folder it named was usually absent. Note that the broken line contained no path at all, so "avoid paths" is not the test - "does this run need another folder present" is.
- Do not justify cutting something from a `SKILL.md` on the grounds that it is written down in `docs/baseline/`. No installed agent can open a doc pack.

## Where reasoning goes

`docs/baseline/` is the decision log: the full argument, the alternatives that were rejected, and why. Record decisions there, including what breaks if one is ignored. Two packs, routed by `docs/baseline/baselinedocs.index.md`:

| Pack | Owns |
|---|---|
| `docs/baseline/family-design/` | the design of the family as a whole: trigger architecture, pack schema, checkpoint model, rule placement, workflow sequence, the onboard scope gate, evidence retention, `useguide`, execution policy, multi-pack routing |
| `docs/baseline/skill-consolidation/` | which skills were merged, deleted, or renamed, and the criterion that decided each |

Identifiers carry their pack prefix, `FD-` or `SC-`, so a reference is unambiguous wherever it is read. `family-design.hallucination.md` FD-D30 records why.

A `SKILL.md` is an instruction executed fresh on every run, not a decision log. It carries a WHY clause only where the agent has a plausible reason to break the rule and would otherwise talk itself out of it.

| Line | WHY? |
|---|---|
| `Report the line counts read` | no. Nobody argues with it |
| `Read every file in the agreed scope in full` | no |
| `Never write the index` | yes. The agent wants to be helpful |
| `Do not answer around the gap as though it were closed` | yes. The agent wants to look competent |

A bare prohibition with an appealing counter-argument gets overridden mid-run. A self-evident instruction padded with justification protects nothing and costs tokens on every invocation. `SKILL.md` length is not cosmetic: the whole body loads each time the skill runs, and for a skill whose job is to conserve context, its own bulk works against it.

## The pack contract

`contract/pack-contract.md` is the only definition of which baseline document owns which content. The 10 pack-writing skills each ship a byte-identical copy at `<skill>/references/pack-contract.md`, because a skill cannot reach a sibling's files. `baselinedocs-onboard` ships the same copy while writing nothing, because it reads every document in full and reports content sitting in the wrong one.

- Edit the canonical file, then copy it to every skill that ships it.
- Never edit a packaged copy directly, and never restate the document roles anywhere else.
- A skill ships a copy when it writes pack files, or when it reads every document in full and reports placement. The test is a full read, not the absence of writes: `baselinedocs-brief` reads nothing in full and neither `audit` skill compares placement, so a copy there would let a skill report conformance it never checked.
- Each carries one gate sentence in its `SKILL.md` sending the agent to read the contract, worded for what it does with the file: before a write, or before reporting pack state. Both wordings are pinned. That gate cannot live in the contract: an agent that skipped the file never reaches the sentence telling it not to skip the file.
- A skill without a copy is not missing one. An onboard run reported the absent copy in a read-only skill as a defect and concluded that future pack writes were blocked; no write routes through a read-only skill, and adding a copy to one fails `test_references.py`.

`tests/test_references.py` pins the copies and fails on drift.

## Report style

`contract/report-style.md` governs what the agent says to the user, not what it writes into a pack. It covers two things: how a pack element or a quotation is named so the reader can act on it, and how a report is shaped so the reader can scan it. Every skill ships a byte-identical copy at `<skill>/references/report-style.md` and gates on reading it, because every one of them produces a report that cites pack elements.

It is a second asset rather than a section of the contract on purpose. The contract's audience is skills that write a pack or read one in full, and `baselinedocs-brief` is neither: it must not carry the role list, because a partial reader holding it would report conformance it never checked. It still cites element identifiers in every report it produces. Folding the two files would force the wrong audience on one of them, so they stay separate and are pinned separately.

## Conventions

- ASCII hyphen only. No en dash, no em dash. Enforced by `test_no_typographic_dashes` across every `*.md` in the repo.
- State the pack-writing skill count in one sentence only, the one under `The pack contract`. Everywhere else say "every pack-writing skill". `test_references.py` pins that sentence against `WRITER_SKILLS` and fails on a second one, because a count repeated in prose goes stale the next time a skill is added or removed. It is pinned to `WRITER_SKILLS` rather than `CONTRACT_SKILLS` because a full reader ships the contract too, so the two counts differ and the prose is about writing.
- Before merging or deleting a skill, read `docs/baseline/skill-consolidation/skill-consolidation.hallucination.md` SC-D1. The merge test is two conditions, not one, and two plausible-looking alternatives are recorded there as rejected so they are not proposed again.
- Skill folder shape: `SKILL.md`, `agents/openai.yaml`, and `references/` only when needed.
- User entrypoints set `allow_implicit_invocation: false`. Lifecycle skills keep it enabled and prefix their display name with `Baseline Docs Internal:`.
- That policy field is Codex-only. On other hosts the `description` frontmatter is the real selection surface, so it must carry the vocabulary a user would actually type.

## Tests

```bash
uvx pytest tests/ -q
```

The repo has no `pyproject.toml`, so `uv run python -m pytest` does not work.
