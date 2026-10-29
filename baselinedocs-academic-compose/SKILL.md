---
name: baselinedocs-academic-compose
description: Compose an anonymized local HTML lesson series from the baseline packs of one or more internal projects, so what operating projects taught can be learned from or handed to another person. Use explicitly when the user wants a lesson, course, tutorial or knowledge base built from baseline pack decisions and lessons, for one project, for a named topic across projects, or from topics suggested out of many projects. Not for writing papers or articles from outside sources.
version: "3.4.0"
---

# Baseline Docs Academic Compose

Turn what baseline packs recorded into lessons another person can learn from. A lesson is derived: the packs stay the record and are only read. Output is local HTML and is never published.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

`<academic-dir>` is the folder `baseline-academic-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-academic-core`). When it is not there, stop and tell the user to install `baseline-academic-core`; never write a lesson from memory instead.

Read `<core-dir>/references/pack-contract.md` in full before reading a pack for a lesson, every time. It is the only definition of what each document holds and how an entry is headed, which a citation depends on.

Read `<academic-dir>/references/academic-contract.md` in full before composing a lesson, every time. It owns the lesson format, the citation form, the integrity markers and the anonymization rules; this skill does not restate them.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Inputs

Determine or confirm before reading anything beyond frontmatter:

- the mode, from where the skill was called and what the user asked
- the topic, in the first two modes
- the projects folder for the two multi-project modes, default `C:\.repos\Work\`; the projects are every folder under it that holds `docs/baseline/`
- for project-scoped mode, whether the page will be shared

## Modes

| Mode | When | Reading |
|---|---|---|
| project scoped | called inside one project repo, lesson for that repo only | that repo's pack only |
| named topic | the user names a topic across several projects | entries located with `<core-dir>/scripts/packtool.sh outline` and `find`, then read in full; no whole pack is loaded |
| suggested topics | the user wants candidate topics from many projects | one explorer subagent per project runs `baselinedocs-load` on that pack and returns only a topic list; the user picks one, then the named-topic reading applies |

- In suggested mode, when `baselinedocs-load` is not installed, stop and name it. Never load whole packs yourself as a fallback: that spends the main context the mode exists to spare.
- A topic list from a subagent is a locator, not a source. Read each entry a point rests on yourself before citing it.
- Project-scoped output is anonymized only when the user says it will be shared. Edit nothing of the project except the one mapping-file ignore entry below, and only when anonymizing.

## Workflow

1. Resolve the three inputs. In a multi-project mode called from inside a project repo, warn that cross-project content would be written into that project, and continue only on the user's word.
2. State the outcomes first: what the learner must be able to do after the lesson. Choose topics and points from them, not the reverse.
3. Locate and read. For each point keep its project, document and entry heading, and whether it came from one pack or several.
4. Mark integrity as the academic contract defines: single source, disagreement shown with both sides, missing, inferred.
5. Anonymize when it applies. Collect candidates while reading: project names (folder names and `pack:` values too), 12-digit account IDs, host names, customer names, person names, including inside profile names, ARNs, paths and URLs. Reuse the labels already in the series mapping file without printing it.
6. Write the mapping file `academic-mapping.json` in the calling directory only after `git check-ignore -q academic-mapping.json` passes there. When it fails, append `/academic-mapping.json` to that directory's `.gitignore` and check again. When it still fails, including when the directory is not inside a git repository or the file is already tracked, stop without writing and say why.
7. Scan every page's text for private key blocks, access key IDs, bearer tokens, `password=` or `secret=` assignments and connection strings with embedded credentials. On a finding, stop and name the file and the rule, never the value.
8. Write `academic-index.html`, `academic-reference.html` and `academic-<nn>-<slug>.html` per lesson in the calling directory. Each carries `<meta name="generator" content="baselinedocs-academic-compose">`. Overwrite only a file that carries it; when another file holds the name, stop and ask.
9. Report what was written, the point counts by marker, and, when anonymized, the replacement count per class with the statement that replacement is a heuristic not proven complete and the page needs the user's review before it leaves the machine.

## Rules

- Never fill a gap from memory or the web, and never smooth a disagreement into one claim. A lesson that looks complete beats one that admits a gap only until the first reader acts on the invented part.
- Never publish. Do not use an artifact tool, a hosted service or an upload: pack content is internal, and a publish sends it to a third party that may cache it.
- Never print the mapping file or copy it into a page. It holds exactly what the anonymizer hides.
- Never write a pack or any file of a source project. New `academic-*` pages and the mapping file are the only writes.
- Write only in the directory the skill was called from. Never choose another folder.
- Do not add quizzes that record answers or progress tracking; the contract defers them.

## Output

- the mode and the projects read, with what was read in full against what was only located
- the pages written, with paths
- points by marker: single source, disagreement, missing, inferred
- when anonymized: replacement count per class, and the review request
- what is not verified: anonymizer completeness, and that a plain copy of the folder carries the mapping with the pages

## Non-Goals

- not a paper, article or report writer; it uses no source outside the packs
- not a pack writer; `baselinedocs-save` records what a thread established
- not a publisher; the output stays on the machine
- not an installer of other course skills
