# Adaptive Pack Contract

## Before writing

The gate that requires reading this file lives in each skill's `SKILL.md`, because a rule that exists only inside a file the agent may not open cannot enforce opening that file. This section records why the gate exists.

Content written into a document whose role does not cover it does not stay contained - it gets duplicated once the correct owner also turns out to need the same fact, and the copies drift as later corrections land in only one of them. This happened: execution status and evidence landed in the decisions and architecture documents instead of `roadmap`, which already had an established pattern for that exact content and was never opened.

Decide placement from the role lists below, every time. Do not infer it from a filename, from an earlier session, or from memory of this contract.

## Frontmatter

Every baseline document starts with:

```yaml
---
baseline_schema: "2.0"
pack: "<kebab-case-pack>"
document: "<introduction|roadmap|hallucination|sourcecode|useguide|index>"
status: "<draft|active|blocked|complete>"
updated: "YYYY-MM-DD"
code_ref: "<commit|uncommitted|unknown>"
---
```

`updated` is the last document edit date. `code_ref` is the code state actually inspected, not the document's own commit. Use `uncommitted` for an inspected working tree and `unknown` when provenance cannot be established. A newer commit is a drift signal, not automatic proof of drift.

## Required documents

- `introduction` (`<prefix>.introduction.md`): scope, current truth, target, constraints
- `roadmap` (`<prefix>.roadmap.md`): phases, dependencies, status, final evidence, risks, next action
- `hallucination` (`<prefix>.hallucination.md`): the why - open questions, closed decisions, a defect's cause, rejected alternatives

A closed decision records four things: what was decided, why, what breaks if it is ignored, and which alternatives were rejected with their reasons. A decision recorded without its reasoning is one the next reader optimizes away, because nothing tells them what it was protecting. A rejected alternative that is not written down gets proposed again.

## Register

A `hallucination` entry is read by an agent every time the pack loads, not by a person reading once. State its four required parts above in a fixed compact form, never as narrative prose.

- Decision: one imperative or declarative sentence.
- Why: a trailing clause after a dash, expanded to a full sentence only when it carries a measurement or mechanism a clause cannot hold. Drop it entirely once the harm is self-evident from the decision.
- What breaks if ignored: the concrete failure, not a description of how it would feel.
- Rejected alternative: what it was plus the one reason it lost, not the deliberation that led to trying it.

Cut on sight: a rhetorical question used as a section lead-in, narration of how this entry's own wording was arrived at, a lead-in phrase carrying no content beyond `Why:` or `Rejected:` themselves, a dated anecdote beyond what the lesson-entry form under `Evidence density` already keeps.

Compression must not delete a fact. Before shortening an existing entry, confirm every identifier, filename, number, and rejected alternative the original named is still present somewhere in the result.

## Entry index

Conditional, like the documents below. Add an index at the top of `hallucination` once that document exceeds 40 KB or holds more than 20 entries, whichever comes first. Below that, omit it: the maintenance burden is per entry and does not scale down, while a reader can hold a short journal without help.

The index is one table, one row per entry, four columns: the entry's identifier, what the entry is about, its status, and the identifiers of related entries. Status is required, not decorative, because it is the only place a reader learns an entry was later reversed without reading the entry that reversed it.

A row states what an entry is about and nothing more. Never its reasoning, never the justification behind its outcome, never a summary that could be mistaken for the entry. A row that carries reasoning is a second copy of the entry, and the two drift.

Nothing verifies a row against its entry. Every other duplicated file in this system is byte-identical and machine-compared; a row is a different text by design, so there is nothing to compare it to. This one is upheld by discipline: when an entry changes status or subject, its row changes in the same edit. A stale row asserting an entry is current when a later entry reversed it is worse than no index at all.

An answer that turns on an entry whose full text was not read is unbacked. Say so and offer to read the entry. A row is a locator, not a source.

The index presumes each entry is delimited by its own heading carrying its identifier. Where a journal is not yet structured that way, delimiting it is the first step of adding the index and is the author's work: no skill performs that restructuring, and bold text at the start of a line does not count, because it is not an anchor, not a table-of-contents row, and not a citable target.

## Reasoning ownership

`roadmap` records the outcome: what happened, the final evidence, and the next action. `hallucination` records the why: a defect's cause, rejected alternatives, the reasoning behind a fix. When a roadmap entry needs to explain why something happened, link to the matching hallucination entry instead of restating its reasoning. Duplicating the same narrative in both documents means every later correction has to be made twice, and they drift when it isn't.

## Disproven claims

A claim that code or an explicit decision has disproven moves into `hallucination` as a closed entry recording what was believed and what disproved it. The document whose role is current truth stops asserting it. The claim is not deleted.

Owners: `sync-codebase` when code disproved it, `sync-decisions` when a decision closed it, `save` when the current thread established it.

Deleting the claim loses the only record that the belief was ever held, and a later agent re-derives it from the same evidence that produced it the first time. `hallucination` is a journal, and a defeated approach kept beside what defeated it is what stops that approach being proposed again. Nothing in an active pack is removed on the grounds that it is no longer true. It is relocated.

## Misfiled content

Content that is accurate but sits where the role lists do not put it moves to the document or section that owns it. It moves verbatim: this is a relocation, not a rewrite, and shortening it on the way is a separate operation that needs its own justification.

Owners: `sync-decisions` when a decision settled what the content was filed under, `sync-reconcile` when the misplacement has already produced a contradiction, `save` when the current thread established where it belongs. A skill that only reports names the owner and moves nothing.

The commonest form is not across two documents but inside one: settled material accumulating under a heading that says it is unsettled. Measured in a real pack, an open-questions section held 88 entries while 7 questions were actually open, so more than nine tenths of that section was closed material filed as open. Nothing there is untrue, so no audit reports it and the disproven-claims rule above does not reach it.

Left alone it costs twice. A reader cannot tell which questions are live, which is the one thing that section exists to answer. And every reader pays for it, because the section a reader must always take in full is exactly the section that filled up with material that could have been deferred.

## Conditional documents

- `sourcecode` (`<prefix>.sourcecode.md`): architecture, code topology, execution flow. Include when that shape will help later work.
- `useguide` (`<prefix>.useguide.md`): consumer contract, API or method usage, migration procedure, operator guidance. Include when a consumer outside this pack depends on the behavior.

Omit a conditional document when it would contain only `not applicable` filler. Preserve an existing conditional document until its useful content is migrated or pruning is explicitly safe.

`useguide` means a consumer contract. Valid forms: API request and response behavior; method or library usage; a migration or conversion procedure; an operator workflow; black-box behavior another team needs. If no consumer exists, omit the file.

A procedure that applies across tasks is not a consumer contract, whoever consumes it. It belongs in the wiki, at `docs/wiki/<topic>.md`, because a pack holds task-specific state while a wiki article holds task-independent instruction that can be injected into later work. `baselinedocs-extract-wiki` performs that move.

## Evidence density

Keep:

- the final passing or failing result supporting current status
- unresolved failures
- failures that explain a changed design
- reproduction details for an active defect
- a lesson entry

Discard from an active document:

- routine failed fixture iterations
- repeated commands with the same meaning
- transient syntax or setup mistakes already resolved
- chat chronology that does not affect current truth

A resolved mistake is not the same as a routine failed attempt. The discard list targets attempts carrying no reusable insight, not a documented misjudgment that would otherwise be repeated.

External raw logs may still be linked when auditability requires them. Link them rather than pasting them into the document.

A lesson entry - a mistake with why it looked reasonable, what disproved it, and the fix applied - is not a retry or an intermediate command. Keep it in full even after the mistake is resolved, both when writing it and when compacting the document later. Trimming it to its final state, or dropping it because it is fixed, discards the reason it exists, which is what prevents the same mistake recurring.

Do not present a build, a formatter, a static check, or a documentation review as proof of live runtime, integration, or deployment behavior. Record what was observed running.

Write terse. Use a table for options, comparisons, and status. Do not add changelog-style notes about what was just corrected, and do not create a side file to explain an edit; edit the target document only. A pack that accumulates edit commentary becomes the transcript this policy exists to prevent. Use the ASCII hyphen. Do not emit an en dash or an em dash.

Never hard-wrap a paragraph. One paragraph is one line, however long, and the reader's editor wraps it. Inserting a newline at a column breaks the paragraph into fragments that read as a list of unrelated statements, and it roughly doubles the line count without adding a word, so every later reference to a line number is off and the document looks twice the size it is. Measured on a real pack: 92 percent of its prose lines fell in the 40-to-89-character band, which no natural paragraph produces.

## Boundary with code

A pack is internal operational memory. Never reference a pack filename or a pack section from inside code, configuration, infrastructure resource descriptions, or anything else that ships outside the repository - infrastructure resource descriptions have done exactly that, citing a `hallucination` document by filename in text a cloud provider console showed to everyone with account access, where the filename meant nothing. State the technical reason in place instead.

## Multi-pack initiatives

For work spanning dependent domains, keep every domain pack first-class and add `<initiative>/<initiative>.index.md`. The index contains direct links, owners or scopes, status, dependency edges, and the current cross-pack checkpoint. It is routing metadata, not a general pack that repeats child content.

Example dependency table:

| Pack | Scope | Depends on | Status | Next checkpoint |
|---|---|---|---|---|
| `identity-api` | Backend contract | - | active | Schema verified |
| `avatar-ui` | Frontend rendering | `identity-api` | blocked | Consume signed URL |

Use a Mermaid dependency graph only when it makes alternating cross-domain order clearer.
