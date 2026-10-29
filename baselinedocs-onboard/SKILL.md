---
name: baselinedocs-onboard
description: Load, ingest, or absorb an existing adaptive baseline pack or initiative into working context completely, reading every document in full before any planning or implementation discussion. Use when the user asks for a doc pack to be loaded before work starts, and wants the agent to hold the pack's entire state rather than a forward-looking summary.
version: "3.3.0"
---

# Baseline Docs Onboard

Load a pack into working context and show the user what is going on: what the project is, how far it has got, and what waits on them. The deliverable is a loaded agent and a report that can be read at a glance, not a new document. Nothing is written, except the page `Output` describes when the user asks for one.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/pack-contract.md` in full before reporting the pack state, every time. It is the only definition of which document owns which content, the entry-index shape, and what a phase or an open question records; do not infer any of it from a filename, from an earlier session, or from memory.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` before reporting the pack state, and report its FAIL and WARN lines as findings; it reports, it never fixes. Without `sh`, say the checks were not run.

## Inputs

Determine or confirm:

- the pack root or the initiative index path
- the scope. For an initiative the default is one domain pack, not the whole set
- whether linked wiki articles are in scope
- whether retained source material is in scope

## Workflow

1. Classify the target: a single pack, an initiative with an index, or an initiative whose sub-packs have no index.
2. Route before loading. A single pack needs no routing: go to step 4. For an initiative, read the index, stop, and read no sub-pack content yet. With no index, build the same view from each sub-pack's frontmatter and next action, report the missing index, and name `baselinedocs-maintain-split`. Never write the index: a reader can only record links it inferred, not the edges an author supplies.
3. Select the scope. When the routing evidence names exactly one sub-pack in progress, load it and state what named it. Otherwise present the routing table and ask. Bypass the question only on stated evidence, never on which pack looks more important.
4. Enumerate the selected scope and keep the list; do not report it.
5. Apply the size gate. When you cannot say with confidence that the scope fits in remaining context, stop, present the total, propose a narrower scope, and wait. Uncertainty resolves toward asking, not toward starting.
6. Read every file in the agreed scope in full. Do not truncate, skim headings, sample sections, or substitute a search for a read.
7. Record provenance per document: `status`, `updated`, `code_ref`. `uncommitted` and `unknown` are provenance, not commits. A newer commit than a document's `code_ref` is the drift signal the contract describes, not a verdict to investigate here.
8. Follow links out of the pack. Read a wiki article when it is in scope; otherwise leave it unread and do not treat it as loaded.
9. Note every point where a loaded document leans on something outside the scope: a decision cited without its content, a term used undefined, a link into another pack.
10. Report the sections `Output` defines, in that order. Omit `Pack map` and `Caveats` when their stated condition does not hold; render the others every time and say so when one has nothing to show.
11. Stop. Do not propose, plan, or begin work unless asked.

## Reading Rules

- Complete means complete for the selected scope, not for everything reachable. Narrow openly before reading starts; never read part of what was then selected. An agent that believes it is loaded and is not is worse than one that knows it read nothing.
- Never summarize a document from its headings.
- Report state as the documents record it. Onboard describes; it does not assess progress, revise a status, or invent a next action. Counting recorded statuses is describing; a percentage, a forecast, or "on track" is assessing.
- A dependency edge is status, not reading order. Report edges as stated; do not reorder reads around them, and do not pull in an excluded upstream pack.
- Take references from the text, not from the edges: an edge can be purely operational, and a pack can lean on one it has no edge to.
- A reference left unread is a gap even when the report does not list it. An answer touching it is unbacked: say so and offer to load what it names. Do not load unasked, and do not answer around the gap as though it were closed.
- Dependency edges and the cross-pack checkpoint live only in the index. Without one they are missing, not derivable: do not infer them from directory names, alphabetical order, or the import graph.
- Do not resolve a contradiction found while reading; report it. `baselinedocs-sync-reconcile` owns the repair. Index status disagreeing with a pack's own `status` is one of these: do not treat the index as authoritative and do not prefer the newer `updated`.
- Retained source material is out of scope unless the user includes it: a `sources/` directory, or any file in the pack without baseline frontmatter. `baselinedocs-adopt` already distributed its information into the documents, so reading both loads the same content twice, and the source is usually the largest file present.
- A link, token, or credential in a pack is never reproduced: name what it is and write a placeholder. A work ticket line is the exception: its key and URL identify a task, not access, so report them as recorded.
- Do not update frontmatter, dates, or status. Onboard writes no pack file, including the index it just reported missing.

## Output

Six named sections, each its own heading, in this order: `Needs you now`, `Progress`, `Doc pack introduction`, `Next actions`, `Pack map`, `Caveats`. The reader should know what is going on from the first two without reading further. Show a fact as a visual, a table, or a bullet, never as a paragraph; a paragraph is for an argument that must be followed in order, and a report is not one. A visual states only what the documents record: counts of recorded statuses, never a percentage, a forecast, or a verdict.

Chips are fixed, so a report reads the same every run. Classify by the word the pack records. A word that matches none gets `❔` with the pack's own word beside it.

| Chip | Recorded status |
|---|---|
| ✅ | complete |
| 🔄 | active, in progress |
| ⛔ | blocked |
| 📝 | draft |
| ⬜ | planned, not started |
| ❔ | any other word |

`Needs you now`: a card, drawn as a code block with a `┃` left rule, of one to three items the pack records as waiting on the user: a next action addressed to the user, or an open question the pack's own next action names as something it cannot proceed past. One line each: the identifier with a gloss of a few words, and the pack. No instruction text: the card names the item and `Next actions` carries what to do, so nothing appears twice. When nothing is recorded as waiting, one line saying so.

An item the pack records without an identifier is named by a short descriptive phrase, never by a code you made up: an invented tag reads as the pack's own. This holds on the card, the board, and `Next actions`.

`Progress`: one sub-heading per pack, ordered by `updated`, newest first. Under each:
- a badge line: status chip, `updated`, `code_ref`, and the count of open questions
- a bar of recorded phase statuses, for example `▓▓▓▓▓▓▓▓░░ 8/10 complete`, then a strip with one chip per phase in recorded order. The strip stays in recorded order because order is meaning
- a phase table of the phases that are not complete, plus the last phase recorded, with no cap on rows: `blocked` and `active` phases first, then the rest in recorded order. Four columns, the phase identifier followed by its work ticket key when one is recorded, a short phrase of what it did, its status chip and word, and the identifiers of every open question recorded against it, or a dash, with no cap per row. `report-style.md`'s stated exception lets this table run to four columns. "Recorded against" means the question is one the phase is recorded as waiting on, in its own text or its `Dependencies`; a question the phase merely cites as evidence does not count. A question no phase waits on is shown on the board only. A phase already in the table is not added again. Completed phases appear in the bar and the strip only
- a board of three columns, `Needs your decision`, `In progress`, `Waiting`: open questions and recorded next-action items. `Waiting` holds only an item whose record says it is blocked on another recorded item or an outside event; with no such record the column shows a dash. An open question goes to `Needs your decision`, an item the pack records as being worked goes to `In progress`. Place an item by what the pack records, never by your own reading of its urgency
- a `Risks` bullet list, one bullet per risk the roadmap records as not yet mitigated, each a single short line. When the roadmap records no state for its risks, write one line saying so instead of listing them all. Omit it when there are none

Glosses go inside the cell, a few words after the identifier, which satisfies the report-style gloss rule. Do not add a bullet block under a table to explain its cells; a table followed by text longer than the table has failed. A meaning too long for a cell is shortened, not moved.

Badge `updated` is the newest `updated` among the pack's documents. Chips follow the recorded word's meaning, so "Not started, deferred" is ⬜ and the word `deferred` stays beside it.

`Doc pack introduction`: one sub-heading per pack in scope, in the same order. Under it, one bullet for scope and one bullet for target, as `introduction` records them. Report what it records; do not reproduce it, and do not fold scope and target into one paragraph.

`Next actions`: one sub-heading per pack in scope. Under it, one bullet per action item, ordered from easiest and least urgent to hardest and most urgent. An item is the pack's recorded `Next action`, its instructions split one per nested bullet, or an open question the pack's own next action names as something it cannot proceed past. A continuation or "next, in order" passage with no `Next action` label counts when it states what to do next; where several dated passages exist, only the newest counts. A recorded `Next action` that the newest passage contradicts is stale: it does not go on the card or in `Next actions`, and the disagreement goes in `Caveats`. Two current next actions that disagree are both shown with their document and phase, neither chosen, and the disagreement goes in `Caveats`. Head each item with what it is and close with its identity tag as inline code; nest its instructions under it, restructured under the report-style next-action rule so what they tell the user to do survives unchanged, none added, none softened. Rank on two recorded signals, never on unstated judgment: whether the pack already records a recommendation for the item, which ranks easier than one with none, since approving a recorded answer is easier than originating one; and how many other recorded items are blocked on it or waiting on it, which ranks more urgent the higher that count. State the signal beside the item, so the ranking is checkable against the pack rather than taken on trust. Items tied on both signals keep the order the pack records them.

`Pack map`: only when the scope sits inside a multi-pack initiative and the index records a dependency edge or a coupling note touching an in-scope pack. Draw the packs as boxes with their status chip, joined by arrows for the recorded edges, in a code block. Below it, bullets pairing the specific coupled entries or phases the index names, for example "`baselinedocs` BLD-D30 amended one clause of `skill-consolidation` SC-Q6," rather than merging both packs' phase tables into one timeline. Phases in different packs run on independent per-pack counters with no shared date at phase granularity, so pairing the named entries is the fusion this section offers, not a unified chronology. A terminal shows Mermaid as source text, so never emit it in the conversation.

`Caveats`: only the lines that apply, each one line, the heading omitted when none does.
- `Not read:` one line, in your own words, naming what a loaded document leans on that is outside the scope, and any retained source material or other exclusion the user may assume was read. Offer to load it.
- one line per contradiction found between documents, such as an index status against a pack's own, or a question closed in one place and open in another; name both places and choose neither
- one line per FAIL or WARN from `packtool.sh check`, as findings

When the user asks for a page, a diagram they can open, or a visual document, render the same sections and the same chips as one HTML file instead, and draw `Pack map` as Mermaid there. Write it where the user names, otherwise in the working repository. Publishing it sends the pack's content to claude.ai: say so and publish only when the user asks.

## Non-Goals

- not a quick brief; onboard loads the pack in full, `baselinedocs-brief` reports position without loading
- not a drift audit; `baselinedocs-audit-drift` does that
- does not create the missing index; `baselinedocs-maintain-split` does that
- writes no pack file
