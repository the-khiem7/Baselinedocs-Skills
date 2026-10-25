---
baseline_schema: "2.0"
pack: "academy"
document: "roadmap"
status: "draft"
updated: "2026-10-25"
code_ref: "02f17f4"
---

# Academy Roadmap

Verification gate for every phase that touches code: `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q` green. Reasoning for each phase lives in `academy.hallucination.md` under the decision named in its Basis column.

## Phase status

| Phase | Outcome | Basis | Depends on | Status |
|---|---|---|---|---|
| ACA-P1 | design recorded in this pack and the gateway index | ACA-D1 to ACA-D17 | - | complete |
| ACA-P2 | `baseline-academic-core` created, family files updated | ACA-D3, ACA-D9 | ACA-P1 | complete |
| ACA-P3 | `baselinedocs-academic-compose` written, three modes | ACA-D2, ACA-D7, ACA-D8, ACA-D10, ACA-D12, ACA-D14, ACA-D16, ACA-D18 | ACA-P2 | complete |
| ACA-P4 | trial run in each mode, project scoped first | ACA-D4, ACA-D5, ACA-D6, ACA-D10, ACA-D17 | ACA-P3 | not started |
| ACA-P5 | release of the sub-family | ACA-D9 | ACA-P4 | not started |

## ACA-P1: record the design

Acceptance criteria:

- this pack holds seventeen closed decisions (ACA-D1 to ACA-D17) and no open question
- the gateway index lists the pack

Evidence: pack written 2026-10-25 against `d26f99f`; no code exists to verify. The pack and the gateway index are uncommitted by the user's choice, so ACA-P2 starts from a tree that already carries these changes.

## ACA-P2: baseline-academic-core and the family files

Acceptance criteria:

- `baseline-academic-core/` holds `SKILL.md`, `agents/openai.yaml` and `references/` with the lesson format, the anonymization rules and the citation rule
- `scripts/stamp_version.py` stamps it; `tests/` pin the sibling-folder sentence, the absence of copies and the set membership, as `baseline-core` is pinned
- `AGENTS.md` and `README.md` name the second exception and the install line
- a decision in `baselinedocs` records the second exception to the sibling-prerequisite rule

Evidence: `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q` gave 474 passed and 2 skipped (the two skips need a symbolic link or a preserved `HOME`, unchanged by this phase); `scripts/stamp_version.py --check v3.3.0` reported 0 files differing; `packtool.sh check docs/baseline` gave 0 FAIL and 5 WARN, all in the older packs. Files changed: `baseline-academic-core/` (new), `scripts/stamp_version.py`, `baselinedocs-self-upgrade/SKILL.md` and `scripts/upgradekit.sh`, `tests/test_references.py`, `test_skill_metadata.py`, `test_version.py`, `test_upgradekit.py`, `test_packs.py`, `AGENTS.md`, `README.md`, and the `baselinedocs` pack (a new decision and an introduction edit). The decision is in `baselinedocs` hallucination as BLD-D55 (the second shared core, read only by the academic skills). The sentence that defines the academic core's folder and its gate are not pinned yet: no academic skill exists, so they are pinned in ACA-P3.

Revision summary: the anonymization rules in `academic-contract.md` were changed after the phase was committed, to move the mapping file into the calling directory and require it to be git-ignored (ACA-D18). The acceptance criteria and dependencies are unchanged.

## ACA-P3: the compose skill

Acceptance criteria:

- `baselinedocs-academic-compose/SKILL.md` reads packs through `baseline-core` and the lesson rules through `baseline-academic-core`, and stops when either is missing
- it writes only the local HTML folder and never a source project
- its description names "baseline pack" and internal knowledge, so it is not selected for paper writing
- it scans output for keys and credentials before writing
- it writes the mapping file only after `git check-ignore` confirms git ignores it, and stops otherwise

Evidence: `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q` gave 508 passed and 2 skipped. Files changed: `baselinedocs-academic-compose/` (new), `baselinedocs-help/references/guide.md`, `tests/test_references.py`, `test_conventions.py`, `test_skill_metadata.py`, `README.md`, `AGENTS.md`, `assets/source/family-map.html`. The core-folder sentence and two gates are pinned for `ACADEMIC_SKILLS`. Choices the skill made that no decision names: the mapping file is `academic-mapping.json` and its ignore entry goes in the calling directory's `.gitignore`; outside a git repository, or when the file is already tracked, the check cannot pass and the skill stops; pages are `academic-*.html` and only a file with the generator meta tag is overwritten, so a page never replaces an unrelated file. No run exists in any mode. `family-map.webp` and `family-map-dark.webp` were not re-rendered, so the README picture omits the skill and the added row may overflow the 650 px panel.

## ACA-P4: trial run

Acceptance criteria:

- project scoped: one project repo, one topic from its pack, one HTML file written inside that repo
- named topic: one topic, two or three projects, entries located with `packtool.sh` without loading whole packs
- suggested topics: explorer subagents return a topic list only, the user picks one, one local HTML file results
- every lesson point cites a source entry; single-source points and disagreements are visible
- the anonymizer's replacement count per class is reported and the user reviews the page for leaked identifiers

## ACA-P5: release

Acceptance criteria:

- `uv run scripts/release.py vMAJOR.MINOR.PATCH` run only when the user asks, and the two printed `git push` commands left to the user

## Risks

| Risk | Pointer |
|---|---|
| wrong family selected for paper-writing requests | ACA-D1 |
| anonymizer misses an identifier | ACA-D5, ACA-D13 |
| mapping file leaks the real names | ACA-D18 |
| sensitive project read by default | ACA-D4 |
| multi-project output written into a project repo | ACA-D14 |

## Next action

Start ACA-P4 once the user approves it: run the skill in project-scoped mode first, inside one project repo with one topic, and review the page for leaked identifiers. Re-render the two family-map images before ACA-P5.
