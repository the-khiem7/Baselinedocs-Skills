---
name: baselinedocs-load
description: Silently load or prime an existing adaptive baseline documentation pack into working context completely, replying with a one-word confirmation. Also does smart (dynamic) loading - give it only one or more initiative index files, or say smartloading, and it routes by the task to the packs, and the decision entries of an oversized journal, that the task needs. Use when the user asks to load or prime a doc pack and wants zero conversational overhead.
version: "3.4.0"
---

# Baseline Docs Load

Load a pack into working context silently and confirm readiness. The deliverable is a loaded agent holding the pack state in context, without explanatory commentary or status reporting. Nothing is written.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/pack-contract.md` in full before loading a pack, every time. It is the only definition of which document owns which content, the entry-index shape, and what a phase or an open question records; do not infer any of it from a filename, from an earlier session, or from memory.

## Inputs

Determine or confirm:

- the pack roots or initiative index paths. More than one is allowed, including indexes in different repositories
- the mode. Direct: the user names one or more packs. Smart: the user says smartloading or dynamic loading, or gives only initiative index files and names no pack
- the task, in the user's words, for smart mode. A restriction the user states, such as one environment of an index, removes packs from the candidates before any matching
- the scope. For an initiative the default is one domain pack, not the whole set
- whether linked wiki articles are in scope
- whether retained source material is in scope

## Workflow

1. Classify each target: a single pack, an initiative with an index, or an initiative whose sub-packs have no index. Classify each index on its own; a pack does not join the scope because it sits in a request beside another.
2. Direct mode: load the named packs and go to step 4. Packs of one initiative, or of several, are all loaded as named.
3. Smart mode: read each index, stop, and read no sub-pack content yet. Select a pack only on a sentence the index records that ties it to the task: its scope cell, a routing table such as `Reading this initiative`, a callout group row (a group may point into another repository), or its next checkpoint. Quote the sentence for the manifest. Match the task, never which pack looks more important. A dependency edge never selects a pack. With no task stated, only the index selecting exactly one sub-pack as in progress counts as evidence, and you name it. Several candidates or none: present the routing table and ask. With no index, build the same view from each sub-pack's frontmatter and next action, report the missing index, and name `baselinedocs-maintain-split`.
4. Per selected pack, take `introduction`, `roadmap` and `hallucination`. Add `sourcecode` or `useguide` only when the task touches what it holds.
5. Apply the size gate to the whole selection. When you cannot say with confidence that it fits in remaining context, stop and narrow before reading. The narrowing, in this order: fewer packs; then, for an oversized `hallucination` only, entry scope. Entry scope reads the `## Entry index` in full, picks the entries whose row ties to the task, adds every entry a picked row's status names as amending, superseding or reversing it, and reads each picked entry in full, located with `sh <core-dir>/scripts/bldh.sh outline <file>`. Do not pick entries by guessing from a subject. In direct mode the gate asks first and entry scope is offered as the narrower option; in smart mode apply it and say so in the manifest. Still too large: present the total and wait. Uncertainty resolves toward asking, not toward starting.
6. Read every file in the agreed scope in full; for a document in entry scope, the index and every picked entry in full. Do not truncate, skim headings, sample sections, or substitute a search for a read.
7. Follow links out of the pack. Read a wiki article when it is in scope; otherwise leave it unread and do not treat it as loaded.
8. Confirm readiness: the word, then in smart mode the manifest from `Output`. Stop. Do not propose, plan, or begin work unless asked.

## Reading Rules

- Complete means complete for the selected scope, not for everything reachable. Narrow openly before reading starts; never read part of what was then selected. Entry scope is a scope: a picked entry is read whole, and an entry not picked is unread, so an answer that turns on it is unbacked. A row is a locator, not a source.
- A dependency edge is status, not reading order. Do not reorder reads around edges, and do not pull in an excluded upstream pack.
- Retained source material is out of scope unless the user includes it: a `sources/` directory, or any file in the pack without baseline frontmatter.
- A pack that holds a `<prefix>.cowork.md` is co-worked: its configuration and every journal are baseline documents in scope. Resolve the current author from `git config user.email` against the `Authors` table and hold it silently.
- Writes no files. Do not update frontmatter, dates, or status.

## Output

Direct mode: respond strictly with a single confirmation word, "Sẵn sàng." (or "Ready."). No headings, tables, open questions, roadmaps, or follow-up proposals.

Smart mode: the same word, then one table of the selection and nothing else, so the user can see what the agent chose and what it left unread.

| Pack | Loaded | Why |
|---|---|---|
| pack name, and its index when several | `full`, `entry scope` (the picked entries by identifier with a few words of gloss, and the count read against the count in the journal), or `not loaded` | the quoted index sentence that selected it; for entry scope the task word each row matched; for `not loaded` the reason |

List every pack of every index the user gave, the unloaded ones included. An agent that believes it is loaded and is not is worse than one that knows it read nothing.

## Non-Goals

- not an explanatory review or status report; `baselinedocs-brief` reports status without loading, and `baselinedocs-onboard` loads with a full five-section report
- does not modify or write files
- does not propose or begin work automatically
