---
name: baselinedocs-onboard
description: Load, ingest, or absorb an existing adaptive baseline pack or initiative into working context completely, reading every document in full before any planning or implementation discussion. Use when the user asks for a doc pack to be loaded before work starts, and wants the agent to hold the pack's entire state rather than a forward-looking summary.
---

# Baseline Docs Onboard

Load a pack into working context and report the state it records. The deliverable is a loaded agent, not a new document. Nothing is written.

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
4. Enumerate the selected scope. Report the file list with line counts before reading anything, and name what the scope excludes.
5. Apply the size gate. When you cannot say with confidence that the scope fits in remaining context, stop, present the total, propose a narrower scope, and wait. Uncertainty resolves toward asking, not toward starting.
6. Read every file in the agreed scope in full. Do not truncate, skim headings, sample sections, or substitute a search for a read.
7. Record provenance per document: `status`, `updated`, `code_ref`. When `code_ref` names a commit, report whether the repository moved past it. `uncommitted` and `unknown` are provenance, not commits: report them as stated and compare nothing. A moved repository is a signal, not a verdict to investigate here.
8. Follow links out of the pack. Read a wiki article when it is in scope; otherwise list it unread.
9. Collect unresolved references: every point where a loaded document leans on something outside the scope, quoted with its location. A decision cited without its content, a term used undefined, a link into another pack.
10. Report the pack state first, then the manifest. The state is what a reader needs; the manifest is how they check the read happened.
11. Stop. Do not propose, plan, or begin work unless asked.

## Reading Rules

- Complete means complete for the selected scope, not for everything reachable. Narrow openly before reading starts; never read part of what was then selected. An agent that believes it is loaded and is not is worse than one that knows it read nothing.
- Report the line counts read. Never summarize a document from its headings.
- Report state as the documents record it. Onboard describes; it does not assess progress, revise a status, or invent a next action.
- A dependency edge is status, not reading order. Report edges as stated; do not reorder reads around them, and do not pull in an excluded upstream pack.
- Collect references from the text, not from the edges: an edge can be purely operational, and a pack can lean on one it has no edge to.
- An unresolved reference is a stated gap. Report it, say that an answer touching it is unbacked, and offer to load what it names. Do not load unasked, and do not answer around the gap as though it were closed.
- Dependency edges and the cross-pack checkpoint live only in the index. Without one they are missing, not derivable: do not infer them from directory names, alphabetical order, or the import graph.
- Do not resolve a contradiction found while reading; report it. `baselinedocs-sync-reconcile` owns the repair. Index status disagreeing with a pack's own `status` is one of these: do not treat the index as authoritative and do not prefer the newer `updated`.
- Retained source material is out of scope unless the user includes it: a `sources/` directory, or any file in the pack without baseline frontmatter. `baselinedocs-adopt` already distributed its information into the documents, so reading both loads the same content twice, and the source is usually the largest file present.
- List anything excluded rather than dropping it silently, so the user can pull it in.
- Do not update frontmatter, dates, or status. Onboard writes nothing, including the index it just reported missing.

## Output

State first:

- what the pack is: its scope and target, as `introduction` records them
- phase status from `roadmap`: what is complete, what is in progress, what is blocked, and on what
- the recorded next action for each pack in scope, quoted verbatim; for an initiative, the index's cross-pack checkpoint as well
- open questions still open
- unresolved references, quoted with location, and the offer to load what they name

Then the record of the read:

- the routing view: every sub-pack, its status, and which was selected on what evidence
- load manifest: path, `status`, `updated`, `code_ref`, lines read, grouped by pack, with the index as its own row
- dependency edges as recorded, and any excluded pack an in-scope pack depends on
- anything missing, unreadable, or excluded by scope

## Non-Goals

- not a quick brief; onboard loads the pack in full, `baselinedocs-brief` reports position without loading
- not a drift audit; `baselinedocs-audit-drift` does that
- does not create the missing index; `baselinedocs-maintain-split` does that
- writes no files
