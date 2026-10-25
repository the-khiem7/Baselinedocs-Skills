---
baseline_schema: "2.0"
pack: "academy"
document: "hallucination"
status: "draft"
updated: "2026-10-25"
code_ref: "d26f99f"
---

# Academy: Decisions and Open Questions

## Entry index

| Entry | About | Status | Related |
|---|---|---|---|
| ACA-D1 | the brand word `academic` and the names built on it | current | ACA-D3 |
| ACA-D2 | where the skills live and starting with one skill | current | ACA-D1 |
| ACA-D3 | two cores: `baseline-core` and `baseline-academic-core` | current | ACA-D1, ACA-D9 |
| ACA-D4 | which projects are read, and read-only | current | ACA-D5 |
| ACA-D5 | anonymizing the output automatically | current | ACA-D4, ACA-D6, ACA-Q2 |
| ACA-D6 | local HTML only, interactivity deferred as debt | current | ACA-D5, ACA-Q3 |
| ACA-D7 | external course skills read and rejected, structure borrowed from `teach` | current, new-words clause amended by ACA-D15 | ACA-D8, ACA-D15, ACA-Q4 |
| ACA-D8 | integrity rules for a lesson built from many packs | current | ACA-D7 |
| ACA-D9 | giving the new skills the same family treatment as `baseline-core` | current, taken by default | ACA-D3 |
| ACA-D10 | three ways to choose topics: project scoped, named topic across projects, suggested topics across projects | current | ACA-D4, ACA-D12, ACA-Q5 |
| ACA-D11 | keeping the pack folder `academy` beside the brand `academic` | current | ACA-D1, ACA-Q1 |
| ACA-D12 | running inside one project repo and writing its HTML there | current | ACA-D4, ACA-D10, ACA-Q7 |
| ACA-D13 | the anonymizer: five classes, counts reported, mapping kept outside every repository | current | ACA-D5, ACA-Q2 |
| ACA-D14 | writing the HTML where the skill is called | current | ACA-D6, ACA-D12, ACA-Q3 |
| ACA-D15 | reusing `teach` text under its MIT licence | current | ACA-D7, ACA-Q4 |
| ACA-D16 | suggest mode stops when `baselinedocs-load` is missing | current | ACA-D10, ACA-Q6 |
| ACA-D17 | anonymizing project-scoped output only when it will be shared | current | ACA-D5, ACA-D12, ACA-Q7 |
| ACA-Q8 | where the anonymizer's mapping file lives | open | ACA-D13 |

## Closed decisions

### ACA-D1: the brand word is `academic`

- Decision: the sub-family is branded `academic`; skills are `baselinedocs-academic-<verb>`, the core is `baseline-academic-core`.
- Why: the user wants one word that carries both the `baselinedocs-` and `baseline-` prefixes. Checked 2026-10-25: npm returns 404 for `baselinedocs-academic` and `baseline-academic-core`, and `npx skills find academic` lists no skill of that name.
- What breaks if ignored: a word already used by a same-domain product is confused with it in search and in conversation.
- Known risk: `academic` is the vocabulary of research-paper skills on the registry (`imbad0202/academic-research-skills`, `yuan1z0825/nature-skills`, `paramchoudhary/resumeskills@academic-cv-builder`), so a request to write a paper can select the wrong family. Mitigation: every description names "baseline pack" and internal knowledge; every entrypoint sets `allow_implicit_invocation: false`, which only Codex honors, so on other hosts the description alone protects.
- Rejected: `lyceum` (the agent's first choice, the user picked `academic`); `compendium`, `cairn`, `lectern`, `anthology` (no collision found, not chosen); `lore`, `loom`, `atlas`, `almanac` (existing products in the same domain: theadust/lore, SpecStory Lore, nudoxorg/Loom, Knowledge Atlas, lmnc); `syllabus`, `curriculum` (close to existing course skills such as vahidrostami/syllabus); `primer` (read as a prompt primer); `codex` (clashes with a host named in `AGENTS.md`, never searched).

### ACA-D2: the skills live in this repository, starting with one

- Decision: the sub-family lives in this repository beside the `baselinedocs-*` skills, and starts as one skill, `baselinedocs-academic-compose`; a split into a separate scan skill and a compose skill waits for a trial run.
- Why: the user placed the skill set here. No run exists yet to show where the boundary between scanning and composing falls.
- What breaks if ignored: a boundary drawn without evidence is redrawn after the first trial, moving files and tests twice.
- Rejected: a separate repository standing beside the projects (the user's first idea, replaced by this repository); two skills now.

### ACA-D3: two cores

- Decision: `baseline-core` stays the only home of the pack contract, report style and `packtool.sh`; `baseline-academic-core` holds the lesson format, the anonymization rules and the citation rule. Academic skills reach both as sibling folders and stop when either is missing.
- Why: the user asked for `baseline-core` to serve pack operations and `baseline-academic-core` to serve the sub-family.
- What breaks if ignored: lesson rules in `baseline-core` load into every pack-writing skill that never uses them, and a copy in each academic skill drifts (`baselinedocs` BLD-D54).
- Consequence: a second exception to the rule that a skill never requires a sibling's content, after `baseline-core`. `AGENTS.md` and the test that pins that rule change in the phase that builds the core, and a decision in `baselinedocs` records the second exception then.
- Rejected: lesson rules inside `baseline-core`; a copy of the rules in each academic skill.

### ACA-D4: every project with a pack is read, read-only

- Decision: in the two multi-project modes of ACA-D10, the scan covers every folder under `C:\.repos\Work\` that holds `docs/baseline/`; no mode writes into a pack.
- Why: the user chose all projects over a list. Writing would alter the packs the lessons cite.
- What breaks if ignored: a write mutates a source pack and the lesson cites text that no longer matches.
- Known risk: a project with sensitive content is included by default; ACA-D5 is the only control.
- Rejected: an allowlist file that starts empty (the agent's recommendation, the user chose all).

### ACA-D5: the output is anonymized automatically

- Decision: project names, account IDs, hostnames and customer names are replaced with neutral labels before any HTML is written, with no un-anonymized copy of the output.
- Why: lessons are meant to be shared with other people (the user's choice, option b).
- What breaks if ignored: internal identifiers reach readers outside the project.
- Unverified: automatic replacement is a heuristic and its completeness has not been tested. Confirm with the security or data protection team before the output leaves the company.
- Rejected: raw output for internal use; raw and anonymized copies side by side (the agent's recommendation, the user chose automatic anonymization only).

### ACA-D6: local HTML only, interactivity is debt

- Decision: the output is one standalone local HTML reading page; it is not published to claude.ai or any host; quizzes and progress tracking are recorded as technical debt.
- Why: pack content is internal and publishing sends it to a third-party service. The user chose a reading page first.
- What breaks if ignored: internal knowledge is cached or indexed outside the machine.
- Rejected: a published Artifact; a Next.js site (`salitaba/lecture-site-engine` needs a Node development environment and runs code through `npx`); a course platform (`canvas-course-builder` needs Canvas, `teach-course-builder` needs a backend).

### ACA-D7: no external course skill installed; structure borrowed

- Decision: install none of the course-building skills found; borrow the structure of `mattpocock/skills@teach` (one HTML file per lesson, a reference area, learning records, shared assets, a check at the end of each lesson) and three rules from the others, written in new words: a lesson is derived and never edits its source; design backward from what the learner must be able to do; a missing fact is marked, never invented.
- Why: `teach` takes its facts from the web, serves one learner and sets `disable-model-invocation: true`; this product takes facts from packs and serves many readers. The three rules come from `yujxzjcn/teaching-skills@course-designer` (backward design, `[NEEDS INPUT]` marks) and `salitaba/lecture-skill` (the agent never writes raw source).
- What breaks if ignored: a skill that browses the web for facts mixes unverified claims into lessons that claim to come from operated projects.
- Two more rules come from `suzheng/k2f@k2f-lesson-plan` and `k2f-syllabus`: every lesson point ties to a stated outcome, and a fact shared across lessons is stated once and cited by key, so lessons cannot drift apart.
- Read in full: `teach` (140 lines), `course-designer` by yujxzjcn (156 lines), `edtech-designer` by heymoezy (133 lines), `k2f-lesson-plan` (76 lines), `k2f-syllabus` (78 lines). Read in part: `lecture-site-engine` (140 of 543 lines), `pauljbernard/content@curriculum-develop-content` and `learning-pedagogy` (the visible part of each skills.sh page; the first is truncated at its inputs).
- Not read: `course-designer` by partme-ai (page truncated) and by teachingai (path not found), `course-material-creator` by travisjneuman (no SKILL.md), `lesson-builder`, the Educators Toolkit pack, `curriculum-review-pedagogy`, and about 35 other skills seen only as names in `npx skills find` results.
- Rejected: `teach` unchanged (web-sourced); `course-designer` by yujxzjcn (written for a university semester, seven agents, and its description says six, and it needs `shared/` and `templates/` folders it does not ship alone); `edtech-designer` (general guidance only); `k2f-lesson-plan` and `k2f-syllabus` (K-12 and university classroom documents that need the separate `k2f` skill and engine and export to formats such as PDF, against ACA-D6); `pauljbernard/content` skills (classroom-oriented, the pedagogy one is a flag-driven command with no workflow shown); `lecture-site-engine` (ACA-D6); `canvas-course-builder`; `teach-course-builder`.

### ACA-D8: integrity rules for a lesson built from many packs

- Decision: a point found in one pack is marked single-source; two packs that disagree are both shown with their projects, never merged; every lesson is scanned for keys and credentials before the HTML is written.
- Why: the user wants to learn from operating projects, and a lesson that smooths over a disagreement teaches the wrong thing. Credentials in a pack must not reach a shared page.
- What breaks if ignored: one project's local workaround is taught as a general rule, or a secret is copied into a shared file.
- Rejected: choosing the newer or more common claim automatically (hides the disagreement the lesson exists to show).

### ACA-D9: same family treatment as `baseline-core`

- Decision: `baseline-academic-core` takes the family `version:` and is stamped by the release; the academic skills are added to the test sets and to the install and upgrade paths the way `baseline-core` was.
- Why: the user did not answer the question, so the default offered was taken: `baselinedocs-academic-*` matches the `baselinedocs-*` glob that the stamp and tests use, and `baseline-academic-core` does not, as `baseline-core` did not.
- What breaks if ignored: the core is missing from the release stamp and its version drifts from the skills that need it.
- Rejected: leaving the core outside the family version.

### ACA-D10: three ways to choose topics

- Decision: one skill offers three modes. Project scoped: run inside one project repo, read only that repo's pack. Named topic: the user names a topic across several projects, and the skill finds the matching entries with `packtool.sh outline` and `find` instead of loading whole packs, so the context window is spared. Suggested topics: the user wants candidate topics across several projects, and explorer subagents load whole packs with `baselinedocs-load` and return only a topic list, which the user picks from before composing starts.
- Why: users forget what they did in a long project, so "all topics" means researching which topics are worth a lesson, not dumping every entry. The three modes trade context cost against how much the user already knows.
- What breaks if ignored: a single mode either loads whole packs for a topic the user already named, or leaves a user who does not remember their own project with nothing to choose from.
- Closes ACA-Q5.
- Rejected: building one flat topic list from entry headings (packs name the same subject differently, so one subject splits); loading whole packs into the main context in the suggest mode (explorer subagents return only the list).

### ACA-D11: pack folder `academy`, brand `academic`

- Decision: keep the pack folder `academy` and the prefix `ACA-`; the brand `academic` names the skills.
- Why: the user chose `academy` for the pack.
- What breaks if ignored: a rename moves the folder and rewrites every `ACA-` citation.
- Closes ACA-Q1.
- Rejected: renaming the pack to `academic`.

### ACA-D12: project-scoped use writes inside the project repo

- Decision: in project-scoped mode the skill runs from a project repo, reads only that repo's pack, and writes the HTML inside that repo, for topics in that repo only.
- Why: the user named this use case after the first request: a lesson file for one project that lives with the project.
- What breaks if ignored: the skill reads `C:\.repos\Work\` wide for a user who wanted one project, and the lesson sits away from its project.
- Rejected: writing project-scoped output into this repository.

### ACA-D13: the anonymizer replaces five classes and keeps a mapping outside every repository

- Decision: before any HTML is written, the anonymizer replaces project names, account IDs, hostnames, customer names and person names with neutral labels, reports the count replaced per class, and keeps the real-to-label mapping in one file outside every repository. The path of that file is set when the skill is built.
- Why: the user wants to trace a label back to its real name, which a mapping allows and the no-mapping option does not.
- What breaks if ignored: a mapping inside a repository ships a list of real names with the repository.
- Known risk: the mapping holds exactly what the anonymizer hides, so it is handled like a secret: never printed, never committed, never copied into HTML.
- Closes ACA-Q2.
- Rejected: replacing the five classes and keeping no mapping (cannot trace a label back); replacing only account IDs and hostnames (project and customer names stay visible).

### ACA-D14: HTML is written where the skill is called

- Decision: in every mode the skill writes the HTML into the working directory it was called from, and never chooses another folder.
- Why: the user builds a course series from several projects in a separate repository and calls the skill there; a fixed folder would pull that output away from the series.
- What breaks if ignored: output lands in a folder the user did not choose, such as a repository of the skill set instead of the series repository.
- Known risk: called from inside a project repo in a multi-project mode, the skill would write cross-project content into that project. The skill warns before writing in that case.
- Closes ACA-Q3.
- Rejected: a git-ignored folder in this repository; a fixed folder outside every repository; asking for a path on every run.

### ACA-D15: text of `teach` may be reused under its MIT licence

- Decision: wording from `mattpocock/skills@teach` may be reused, and any reused text carries the MIT copyright notice.
- Why: the user checked the repository licence and found it MIT. The licence file itself was not read in this session.
- What breaks if ignored: reused text without the notice breaks the MIT condition.
- Closes ACA-Q4. Amends ACA-D7, which said the borrowed structure was written in new words.
- Rejected: writing every borrowed part in new words (no longer needed).

### ACA-D16: suggest mode stops when `baselinedocs-load` is missing

- Decision: when `baselinedocs-load` is not installed, suggested-topics mode stops and names `baselinedocs-load`; it never loads whole packs itself.
- Why: naming a sibling skill for routing holds when it is absent, running it does not, and a fallback that loads packs itself spends the main context the mode exists to spare.
- What breaks if ignored: whole packs from several projects fill the main context window.
- Closes ACA-Q6.
- Rejected: reading packs with `packtool.sh outline` as a fallback (suggestions rest on a partial read).

### ACA-D17: project-scoped output is anonymized only when it will be shared

- Decision: in project-scoped mode the skill anonymizes only when the user says the page will be shared, and edits the project's ignore file only when the user asks.
- Why: inside the team the details are the lesson; editing a project file unasked changes a repository the user did not name.
- What breaks if ignored: an unanonymized page is committed and shared, or a project's ignore file changes without its owner knowing.
- Known risk: nothing stops a commit of an unanonymized page when the user forgets to say it will be shared.
- Closes ACA-Q7.
- Rejected: always anonymizing (loses detail the team needs); always adding the HTML folder to the ignore file (edits a project unasked, and the page is not kept with it).

## Open questions

### ACA-Q8: where the anonymizer's mapping file lives

ACA-D13 puts the real-to-label mapping in one file outside every repository but leaves the path open. A per-user folder such as one under `%LOCALAPPDATA%` needs no elevation on the standard account. The mapping must survive between runs for labels to stay stable across lessons of one series, and must never be inside a folder a repository tracks. Default: a per-user folder under `%LOCALAPPDATA%`, one file per series, path printed on first creation and the contents never printed.
