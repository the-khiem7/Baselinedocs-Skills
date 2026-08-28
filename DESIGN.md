# Baseline Docs Workflow Design

## Decision Summary

This version separates deliberate user workflow starts, one-time administration, and lifecycle behavior that an agent can select automatically.

| Concern | Decision |
|---|---|
| Skill overload | Expose six user entrypoints and visually label lifecycle skills as internal |
| Brownfield capture | Add `baselinedocs-save` |
| Non-baseline source material | Add `baselinedocs-adopt` so an existing document becomes a pack without losing information |
| Loading a pack before work | Add `baselinedocs-onboard` as the read-side entrypoint |
| Rule placement | Put an enforceable rule in `SKILL.md`, not in a referenced file |
| Long-running execution | Add `baselinedocs-run` with phase checkpoints |
| Context compaction | Add a prompt-centric Stop continuation with a loop guard |
| Hook administration | Add an explicit per-repository setup skill that safely merges host configuration |
| Pack bloat | Store outcomes and material failures, not attempt history |
| Inconsistent formatting | Add schema, status, date, and code provenance frontmatter |
| Reusable knowledge | Add a separate wiki extraction workflow |
| Redundant useguide | Make it a conditional consumer-contract extension |
| Post-initial feedback | Reopen or revise phases before creating new ones |
| Multi-domain chains | Use a directly linked initiative index and dependency graph |
| Resume family | Dissolve it; `baselinedocs-brief` owns orientation, `baselinedocs-maintain-compact` owns snapshots, the pack itself is the handoff |
| Unwritten sequence | Write the intended workflow down: save before any context branch, and prefer a new thread over staying through a compaction |
| Teaching the workflow | Lead the README with the ordered workflow; the entrypoint table cannot express order or branching |
| Install granularity | Teach only the whole-family install, because the skills route to each other by name |
| Skill fragmentation | Merge only on a two-condition test; delete `sync-decision` and `maintain-prune`, rename `audit-verify` to `audit-claims` |
| Removing a false claim | Relocate it into `hallucination`; nothing in an active pack is deleted for being untrue |
| Compaction correctness | Give `maintain-compact` a pass-or-revert gate instead of a goal |
| Archived material | Delete `maintain-archive`, the `status: archived` enum value, and `onboard`'s exclusion together, rather than keep an affordance nothing performs |
| Sync against audit | Keep all five. The comparison-scope matrix that made them look overlapping was drawn on an axis that does not separate them |
| Renaming for directness | Applies to a new skill, not retroactively. `sync-reconcile` keeps its name because a pointer, not the name, is how it is reached |
| A finished pack | No status value and no `onboard` filter. Routing already declines to load a sub-pack that is not in progress |
| Who ships the contract | A full read of the pack, not the act of writing. The ten writers and `baselinedocs-onboard`; no partial reader |
| Unreadable element codes | Ship `report-style.md` to every reporting skill, so a glossed identifier does not depend on one user's own instructions |
| Hard-wrapped paragraphs | Ban them in the contract. One paragraph is one line; wrapping doubles the line count and buys nothing |
| An oversized journal | A conditional entry index above 40 KB or 20 entries, with a required status column and no test behind the rows |
| True content in the wrong place | Name owners in the contract, as the disproven-claim rule does. No new skill, no widened trigger |

## Trigger Architecture

Codex supports explicit and implicit skill invocation and allows `agents/openai.yaml` to disable implicit invocation per skill. The six user entrypoints and the one-time `baselinedocs-setup-hooks` utility set `allow_implicit_invocation: false`. Lifecycle skills keep it enabled.

This policy does not hide internal skills from every picker and is not a portable Agent Skills field. Therefore:

- UI names mark helpers as `Baseline Docs Internal: ...`
- descriptions state automatic trigger contexts
- the README teaches the workflow and its entrypoints, never the lifecycle skills
- hook administration is documented separately as a one-time utility

This is progressive disclosure rather than a claim that every host can maintain two physically separate skill registries.

## Pack Schema

Schema `2.0` changes the fixed five-file contract into a three-core plus two-extension contract.

Core:

- introduction
- roadmap
- hallucination

Conditional:

- sourcecode
- useguide

The transition is additive. Existing five-file packs remain valid. Agents should not delete an existing extension simply because a new pack would omit it.

## Frontmatter Semantics

`updated` records the document edit date. `code_ref` records the code state inspected while writing.

The document cannot reliably contain its own Git commit hash because changing the file changes the commit. Therefore `code_ref` is code provenance, not the document commit. Drift audits compare later scoped code changes against the claim body before declaring drift.

## Checkpoint Model

A semantic checkpoint belongs in the roadmap and contains:

- phase outcome and status
- final evidence
- affected files
- open risk
- exact next action

Checkpoint evidence names outcomes, not reasoning - a defect's cause or a rejected alternative belongs in `hallucination.md`, referenced from the checkpoint rather than repeated in it.

`baselinedocs-run` writes this checkpoint itself after every phase, which fixes what `baselinedocs-save` is for. Save is not the step after run. A phase checkpoint owns phase outcome, evidence, affected files, open risk, and next action, all of which live in `roadmap`; it does not own a decision that closed, a question that opened, or a scope that moved. Stated the other way round: after a clean run the roadmap is current and the other two core documents may not be, and that gap is the whole job of a save that follows a run.

Hooks cannot safely infer pack ownership or business outcomes from repository-wide Git state. The command adapter therefore performs no roadmap discovery, Git inspection, timestamp comparison, or semantic completion check. On the first Stop event it returns a concise prompt to the same thread; the agent identifies a pack only from that thread and makes no change when the pack is absent, ambiguous, or already current.

This prompt-centric design intentionally spends at most one additional continuation per turn in exchange for avoiding global roadmap guesses and shared runtime markers. Each host's stop-loop field prevents repeated continuation. Parallel threads keep separate conversation context, while the prompt explicitly warns that a shared working tree still contains changes from other threads.

## Rule Placement

A rule is only as strong as its chance of being read. Three surfaces carry instructions, and they do not offer the same guarantee:

| Surface | Guarantee | Carries |
|---|---|---|
| `description` frontmatter | always in context | one line, enough to select the skill |
| `SKILL.md` body | loaded whenever the skill runs | the gate that sends the agent to the contract |
| `references/*.md` | only if `SKILL.md` says to read it and the agent complies | the contract itself: roles, frontmatter, evidence rules, incidents |

Therefore the *pointer* belongs in `SKILL.md` and the *content* belongs in one file. The rule requiring the pack contract to be read cannot itself live in the pack contract: an agent that skipped the file never reaches the sentence telling it not to skip the file. That is the only part of the contract that has to be restated per skill.

The content stays in one place. `pack-contract.md` is the single definition of which document owns which content, and nothing else in the repository states it a second time. An earlier revision embedded the role list into every pack-writing `SKILL.md` as well, which put the same fact in two places at once; the two descriptions of `hallucination` disagreed from the day they were written, and the test pinning the embedded copies to each other could not see the disagreement because it only compared copies of the same block. Rejected for that reason.

The opposite arrangement - keeping the role list inline and stripping roles out of the contract - was also rejected. The contract still has to name the five documents to give their filenames and their inclusion criteria, so both files would keep discussing the same five things, separated only by a distinction between "what it holds" and "when to create it" that is too fine to survive editing.

Skills install one folder at a time and cannot reach a sibling skill's files, so every skill that ships the contract ships its own copy. Those copies are packaged assets of `contract/pack-contract.md`, the same arrangement `hooks/checkpoint.py` already uses, and they are pinned by a test for the same reason: a copy that drifts reaches whoever installed that one skill, and nothing in their install tells them it is stale.

The criterion for shipping it is a full read of the pack, not the act of writing. Ten writers qualify, and so does `baselinedocs-onboard`, which writes nothing. `Detect And Repair` already assigns the pack-against-itself detection cell to `onboard` and `brief`, and a detector without the role list can only see two statements that literally disagree. It cannot see content sitting in a document whose role does not cover it, which is the failure the contract's opening section calls the damaging one, because that content gets duplicated once the correct owner needs the same fact and the copies then drift. `onboard` reads every document in full, so it is the one read-only skill that can check placement against the standard rather than against a sibling pack that happens to be shaped differently.

The gate is worded per use. A writer reads before creating or editing a pack file; `onboard` reads before reporting the pack state. Both wordings are pinned by `tests/test_references.py`, and that test also asserts `onboard` does not carry the write wording. Reusing the write sentence there was rejected: its precondition can never be met in a skill that writes nothing, and an instruction that never fires teaches the agent to read the gate as decoration.

**Rejected: leave `onboard` without a copy, on the grounds that it writes nothing.** The arrangement this replaces. It reads the criterion off the wrong axis. Writing is what makes placement a *decision*; a full read is what makes it *checkable*. Keeping the old criterion leaves the family's only full reader unable to report the misplacement the contract exists to prevent.

**Rejected: give the contract to every read-only skill.** `baselinedocs-brief` deliberately reads no document in full, so it would report conformance it never checked, which is worse than reporting none. Neither `audit` skill compares placement: `audit-drift` compares documents against code and decisions, `audit-claims` compares a claim against its evidence. `baselinedocs-setup-hooks` never opens a pack.

**Rejected: add a placement-audit skill instead.** Rejected on the grounds already recorded under `Why the matrix is not completed`. The detect cell for a pack against itself is occupied, and a new skill there would serve only "show placement findings without loading the pack", which nothing has asked for and which no partial read can answer.

**What breaks if this is ignored.** An onboard run against a real pack reported the absent copy in a read-only skill as an unreadable file, and concluded that every future write into that pack was blocked. Both halves were wrong: ten skills carried the copy at the time, and no write routes through a read-only skill. The two repairs that reading invites are adding copies to skills that must not have one, which fails `test_references.py`, and concluding the contract is missing everywhere and skipping the gate. Recording the criterion is what makes an absent copy legible as a decision rather than as damage.

The README now documents only the whole-family install, and that does not relax this boundary or permit collapsing the copies into one shared file. `npx skills add --skill <name>` still works and is merely no longer advertised, and a host's skills directory is a place users delete from as well as install into, so a skill can still end up alone next to nothing. The boundary is what a folder can be relied on to contain, not what one install command happened to fetch. Pointing a skill at a sibling's `references/` would work on the maintainer's machine and fail silently on a user's.

## Report Style As A Shipped Asset

A rule about how the agent talks cannot live only in a user's own instruction file. That file is per-user, so a rule placed there produces one user's experience and leaves every other user with whatever the model defaults to, which is the drift this repository exists to remove from the skill family. `contract/report-style.md` therefore ships to every skill that names a pack element in its output, which is all of them except `setup-hooks`.

It stays a separate file from the contract because the two have different correct audiences. The contract goes to skills that write a pack or read one in full. `brief` is neither, and `Rule Placement` records why it must not hold the role list: a partial reader that owns the placement standard reports conformance it never checked. Yet `brief` produces a user-facing report on every run and cites identifiers in it. Merging the files would either hand `brief` the contract, reversing that decision, or leave the family's cheapest conversational skill outside the conversation rule. Two files, two audiences, two pinning tests.

The rule the file carries is one line of substance: an identifier gets a gloss the first time a message names it. The reader of a terminal cannot recover a meaning the message never carried, so a bare code is not brevity, it is a deferred question. This was reported from real use, where a suggestion phrased as three bare codes could not be evaluated without scrolling back.

**Rejected: state it in the user's global instructions only.** It works, for one user, on one machine. The point of a shipped skill is that its behavior does not depend on who installed it.

**Rejected: add it as a section of `pack-contract.md`.** Cheaper by one file and one test, and wrong on audience, for the reason above.

## Hard-Wrapped Paragraphs

The contract now forbids inserting a newline inside a paragraph. One paragraph is one line however long; the reader's editor wraps it.

Measured on a real pack before the rule existed: 2,396 of 2,610 prose lines fell in the 40-to-89-character band and only 20 lines exceeded 90 characters. No natural paragraph distributes that way, so the file had been wrapped at a column. Two packs written without wrapping put the majority of their prose lines above 200 characters, which is what unwrapped prose looks like.

What wrapping costs: the paragraph reads as a list of unrelated statements, the line count roughly doubles so every line-number reference drifts and the document looks twice its real size, and a diff of a one-word change re-flows a whole block.

What it does not cost is tokens, which track bytes rather than lines. That distinction is load-bearing, because a wrapped document looks like a size problem and is not one. Unwrapping the measured pack would cut its line count by roughly half and its token cost by almost nothing. Do not offer this rule as a remedy for a pack that is genuinely too large.

## Entry Index

A large `hallucination` is a real cost and the contract now answers it with an index at the top of the document, one row per entry, conditional on the document exceeding 40 KB or holding more than 20 entries.

The arithmetic is favourable and was measured, not assumed. A row costs about 87 bytes; the average closed entry it defers is about 1,850 bytes, in two separate packs. That is roughly 21 to 1, so an index pays for itself once more than about five percent of entries can be deferred, which is every realistic read. On a 342 KB journal the projection is a saving near 35,000 tokens per load.

It is conditional rather than mandatory for one reason that has nothing to do with tokens: the maintenance burden is per entry and does not scale down. A journal of six entries can be held whole by any reader and an index there is upkeep with no return. Mandating it everywhere would also have made three real packs non-conformant the day the rule landed, and the restructuring that would fix them is the author's work rather than any skill's: relocating misfiled content now has named owners, but delimiting an undelimited journal into entries is not a relocation, and the contract says outright that no skill performs it.

Both threshold numbers are stated because they measure different costs. Bytes measure what a read costs. Entry count measures what the index costs to maintain. Neither alone is the trigger, and both are calibrated against measured points rather than derived: at 21 entries and 47 KB a scoped read came to 28 to 50 percent of a full read, while a 2.9 KB journal would carry an index larger than its saving.

**The index is the first duplication here that no test can pin, and that was accepted deliberately.** Every other duplicated file in this repository is byte-identical and machine-compared, which is exactly why the fanout is safe. A row is a different text from its entry by design, so there is nothing to compare it against, and no test can establish that a row still describes what it points at. The rule therefore rests on discipline: when an entry changes subject or status, its row changes in the same edit. The specific worst case is a row asserting an entry is current after a later entry reversed it, which is the disproven-claim failure the contract's relocation rule exists to prevent, reappearing inside the index.

**Rejected: mandatory in every pack.** Three measured journals, at 2,796, 2,008, and 1,110 lines, delimit entries with bold text or with nothing. For them the index is a restructuring, not an addition.

**Rejected: pin the structural half while accepting the unverifiable text.** Tests for a missing row, a row pointing at no entry, and a row exceeding one line are cheap, and this was the recommendation. Not taken; the mechanism rests on discipline by decision. They remain cheap to add, and what they would not have caught is the only thing that matters, which is whether a row's text is still true.

**Rejected: drop the status column.** The defensive option, since status is the column most likely to go stale and the only one that can assert something false. Kept because its value showed on the first build, where it made a reversed decision visible without reading the entry that reversed it, and because without it the table is a locator that no longer answers whether an entry still holds.

## Misfiled Content

Content that is accurate but sitting where the role lists do not put it now has named owners in the contract: `sync-decisions` when a decision settled what it was filed under, `sync-reconcile` when the misplacement has already produced a contradiction, `save` when the current thread established where it belongs. A reporting skill names the owner and moves nothing. The move is verbatim, because shortening on the way is a different operation with a different gate.

No skill repaired this before, and the reason was structural rather than an oversight. `sync-reconcile` fires on a contradiction, and correctly-stated content in the wrong file is not one yet; it becomes one only once the correct owner also states the fact, which is the drift the contract's opening section warns about. The only available repair therefore arrived one step after the damage. `maintain-compact` shortens and never moves. The write skills add rather than reorganize. The read skills report.

The commonest form is inside one document rather than across two: settled material accumulating under a heading that says it is unsettled. Measured in a real pack, an open-questions section held 88 entries while 7 questions were actually open. Nothing in it was untrue, so neither audit skill reports it: one asks whether a claim has evidence, the other whether a document trails the code, and misfiling fails neither test.

It costs twice, and the second cost is invisible. A reader cannot tell which questions are live, which is the only thing that section exists to answer. And every reader pays tokens for it, because the section that must always be read in full is exactly the section that filled with material an index could have deferred. On the measured pack the difference was about 21,000 tokens per load, more than the entry index itself returns there.

**Rejected: widen `sync-reconcile` to treat a heading disagreeing with its own content as a contradiction.** Coherent, and cheaper by one contract section. Rejected on blast radius: that skill's guarantee is that it touches only what conflicts, and a heading-versus-content trigger makes any section reorganizable under it.

**Rejected: add a skill for it.** Refused on the grounds recorded under `Why the matrix is not completed`. Naming owners is the pattern the disproven-claims rule already set, it costs no folder, and this family had eight phases of trimming behind it.

## Workflow Sequence

The family has one intended sequence, and until this revision it was written down nowhere. Every skill was individually correct while the order connecting them lived only in its author's head, which is why walking that order through out loud surfaced four defects at once: `baselinedocs-brief` placed at a node it is built to refuse, `baselinedocs-save` described as the step after `baselinedocs-run` when run already checkpoints, one entry door named out of three, and no return edge closing the loop. None of those were skill defects. An unwritten sequence cannot be checked against anything, which is the reason to write it down even though every part of it was already true.

`baselinedocs-save` before a context branch is the load-bearing step. Both branches lose the thread, staying keeps a lossy summary of it and leaving keeps none, so the pack is the only thing that survives either. Saving first is what makes a lost context ordinary rather than an incident.

The two branches are not equivalent, and the difference is a count of sources:

| Branch | Sources of truth afterwards | Consequence |
|---|---|---|
| Stay in the thread, then host `/compact` | two: the pack, and a compaction summary that can disagree with it | the disagreement has to be managed, which is what `baselinedocs-brief` reports |
| New thread, then `baselinedocs-onboard` | one: the pack | nothing can disagree, at the cost of re-reading |

A new thread is therefore the default once the pack is current, which after a save it is. Staying is for the case where the thread still holds something that could not be written down, a half-formed approach or a debugging session in flight.

`baselinedocs-brief` sits before the expensive choice rather than in place of it. It is a diagnostic: it reports whether the pack has fallen behind the thread, which is what tells the user to carry on, to run `baselinedocs-save`, or to pay for a full `baselinedocs-onboard`. Using it as the recovery step itself is the error recorded in the next section, and it is the error the skill's own first rule exists to refuse.

## README Shape

The README leads with the ordered workflow rather than the entrypoint table. The table answers "I want X, which skill do I call", which is the question a reader has once they already know the shape of the work. It cannot answer "X is finished, what now", because a table carries no ordering and no branch.

That gap produced a real error, which is why the section exists. The author of this family placed `baselinedocs-brief` at the node meaning "make sure no detail was forgotten after a compaction" - the one thing brief is built to refuse, its first rule being to state that it is not a load. `baselinedocs-onboard` is the skill for detail; brief's value at that node is as a diagnostic that reports whether the pack has fallen behind and therefore which of the two is needed. A structure that lets its own author put a skill in the wrong place will not teach anyone else the right one.

The section renders as a mermaid flowchart, because the two branch points are the whole content and any linear format buries them. What sits under it is two tables rather than paragraphs for the same reason: branch A against branch B is a comparison, and the traps are a lookup, and a reader should not have to extract either from prose.

Per-skill install commands were removed for a related reason. The skills route to each other by name, so a partial install turns a pointer into a dead end that surfaces only after the user has already asked for something. Removing the commands from the README is a teaching decision, not an enforcement one.

## Onboard Scope Gate

`baselinedocs-onboard` promises a complete read. That promise conflicts with a large initiative, so the skill enumerates files and reports line counts before reading, and narrows the scope in the open when the full set will not fit.

Silent truncation is the failure being designed out: an agent that read half a pack and believes it is loaded gives confidently wrong answers, which is worse than an agent that knows it has read nothing.

The gate fires on the agent's own uncertainty rather than on a share of the context window. An agent cannot measure that share, so a threshold phrased that way is settled by guess; "can you state with confidence that this fits" is a question it can answer, and it resolves toward asking.

An initiative routes before it loads. An index is routing metadata, so onboard reads the index, stops, and selects one sub-pack; it does not treat the index as a manifest of everything to pull in. Loading a whole initiative by default would spend the context an index exists to conserve, and it would trip the size gate on nearly every real initiative, turning the gate into noise. One domain pack is therefore the default scope.

The routing question is skipped only on evidence, never on judgement. When the index marks exactly one sub-pack in progress, asking the user to repeat what the index already states wastes a turn, so onboard loads that pack and names the evidence that selected it, which leaves the user able to redirect. Two candidates, or none, means asking. "Which pack looks most important" is not evidence and is exactly the guess this rule exists to block.

An initiative can also have several sub-packs and no index, because a pack set grows by hand faster than anyone runs `baselinedocs-maintain-split`. Onboard reconstructs the routing view in memory from each sub-pack's frontmatter and next action, reports the missing index, and names the skill that creates one. It does not create the index itself: onboard writes nothing, and an index composed by a reader would record links and statuses it inferred rather than the dependency edges and cross-pack checkpoint only an author can supply. Those two fields are reported missing rather than guessed, since inferring order from directory names or an import graph produces an ordering that looks authoritative and is not.

The index is also a document with its own frontmatter, so it gets its own manifest row, and an initiative has several next actions - one per pack in scope, plus the index's cross-pack checkpoint - which is why the output is plural.

A dependency edge is status, not reading order. It records why a pack is blocked; it does not assert that one pack's documents cannot be understood before another's. Onboard therefore reports the edges and reads in no particular order. Ordering the reads by dependency was considered and rejected: it gains nothing once one domain pack is the default scope, and it implies a comprehension dependency between packs that the contract never claims, which would push a reader toward pulling in an upstream pack it was never asked to load.

Cross-pack coupling is then resolved by evidence rather than by policy. Loading one pack risks answering from a neighbour that was never read; loading every neighbour spends the context an index exists to conserve. Both fixed policies were rejected because both decide before reading, while the question is only answerable during it: a dependency edge can be purely operational, with no coupling between the documents at all, and a pack can lean on another it has no edge to, since edges are declared by hand and get forgotten. Onboard instead collects the references the text actually makes, quotes each with its source, and offers to load what they name.

This holds because the hallucination risk is not the unread pack. It is answering from an unread pack without knowing it went unread. An agent holding an explicit list of what it could not resolve cannot make that mistake silently, which is the same principle the whole skill rests on: knowing you have read nothing is safer than believing you read everything. Auto-loading on a non-empty list was rejected as well, since it reinstates the scope expansion the routing default exists to prevent, and the offer costs one turn.

Index status is routing metadata that restates a status each pack also owns. Duplication that the contract accepts for routing still drifts, so a disagreement between the two is reported as a contradiction rather than resolved by preferring the index or the newer date. Onboard does not repair; `baselinedocs-sync-reconcile` does.

The output leads with state, not with bookkeeping. First real use returned a correct file-by-file manifest and none of what the reader wanted: what the project is, its target, what is finished. The documents onboard had just read exist precisely to carry that - `introduction` owns scope and target, `roadmap` owns phase status - so the skill was reporting metadata about the files instead of the state inside them. A manifest proves the read happened; it is not what anyone loads a pack to find out. State comes first now and the manifest follows as the check on it.

This does not turn onboard into a brief. Onboard reports what the documents record from a complete read; `baselinedocs-brief` reports position from a deliberately partial one. The rule keeping onboard descriptive is explicit, because a skill that has just read everything is well placed to start assessing progress and recommending action, which is a different job on a different reading strategy.

Retained source material is excluded by default. `baselinedocs-adopt` promises a pack collectively equivalent in information to its source, so loading both loads the same information twice. It is not a marginal cost: in the first real run, `sources/PROPOSAL.md` was 2415 of the 3460 lines read, seventy percent of the budget spent on content the pack already carried. Files without baseline frontmatter identify this material without needing a naming convention. The exclusion is reported rather than applied quietly, because an unreported exclusion fails the same way a silent truncation does: the user cannot tell what the agent is actually holding.

Provenance is recorded, not adjudicated. `code_ref` may be a commit, `uncommitted`, or `unknown`, and only the first is comparable; even then a moved repository is reported as a signal. An onboard that starts investigating drift stops being a bounded read and turns into `baselinedocs-audit-drift` without its scope limit.

## Resume Family Dissolved

The `resume-*` family no longer exists. It was removed in two passes, both driven by the same audit: take each situation the skill claimed, and ask which skill already owns it.

`baselinedocs-resume-continue` went first, with `baselinedocs-brief` added in its place. The four situations the old skill claimed were audited one at a time, and none of them survived:

| Situation | Outcome |
|---|---|
| Returning after weeks | An anti-pattern. The point of a pack is resuming without chat history, so the correct path is a fresh thread and `baselinedocs-onboard`. A partial-recovery skill only earns its place if the pack cannot be trusted, and that is a different problem |
| Deciding whether the pack has gone stale | Already owned twice over: `baselinedocs-audit-drift` answers the question, `baselinedocs-save` and `baselinedocs-sync-codebase` close it. `save` even ends by reporting where work should resume |
| Orienting mid-task | A real need the skill served weakly, now `baselinedocs-brief` |
| Recovering after a compaction | Its stated reason to exist, and the case it handled worst |

The compaction case failed for a reason worth recording, because it is what `brief` is built around. After a compaction the summary in context can hold hours of work that was never written into the pack, so the pack is behind the thread. The old skill read the pack and reported it, never comparing the two, and returned a continuation point stale by exactly the amount of unrecorded work, with nothing marking it as such. It also read selectively with no definition of what it read and no obligation to say what it skipped, so the reader could not tell how much of the pack the brief rested on.

`brief` therefore carries three rules the old skill lacked: state that this is not a load, report what was read against what was skipped, and compare the thread against the pack and report the delta. That last one is the job nothing else in the family does. Writing the delta down stays with `baselinedocs-save`; brief only surfaces it, because a skill that detects a gap and closes it in the same breath would be writing to a pack it only partially read.

Making `baselinedocs-onboard` the successor was rejected. It is explicit-only by policy, so on Codex nothing would fire after a compaction, which is exactly when the user is least likely to remember to invoke anything. More fundamentally, onboard is bound to report the state the documents record and forbidden to assess it, so after a compaction it would load a stale picture completely and confidently, arriving at onboard's own designed-out failure through a different door.

Keeping the old skill alongside the new one was also rejected. Two skills answering "where are we" from overlapping reads is how an agent picks the wrong one, and the old skill's weaknesses are not additive with the new one's guarantees.

`brief` is a user entrypoint, so it sets `allow_implicit_invocation: false` like the others. On Codex that costs the automatic firing the compaction case wants. The field is Codex-only, and on hosts where `description` drives selection the skill is still reachable without being typed, so the cost is bounded to one host and is the price of keeping the entrypoint classification meaningful.

The three remaining skills went in a second pass, and nothing replaced them.

| Skill | Why it was deleted |
|---|---|
| `resume-snapshot` | `baselinedocs-maintain-compact` covers it and covers it better. The triggers were the same (a long, noisy, chat-driven pack), the steps were the same (distill what is true now, drop attempt-by-attempt narration), and compact carries a pass-or-revert gate that snapshot never had. Snapshot also never said where the snapshot goes, while carrying the contract gate that only makes sense for a skill that writes pack files, so what it actually produced was never settled |
| `resume-next-step` | `baselinedocs-brief` reports the recorded next action verbatim. What next-step added on top of that was permission to substitute its own judgment for what the pack records, with no way to know the recorded action was stale and no obligation to say it had substituted, which is the failure `brief`'s delta rule exists to prevent. It was also the least guarded skill in the repository, with no contradiction handling, no read-against-skipped disclosure, and no statement that it is not a load, while producing the most command-shaped output of any of them |
| `resume-handoff` | A pack that needs a separate handoff artifact is a pack failing at its stated purpose. Baseline Docs exists so another conversation or agent can resume without chat history, so the pack is the handoff and a fresh thread with `baselinedocs-onboard` is how it gets read. This is the same reasoning that made "returning after weeks" an anti-pattern in the table above, applied to a second reader rather than the same one |

Keeping `resume-handoff` for the reader who will not run an agent at all was considered and rejected. It was the only skill in the family whose output was meant to leave the thread, which is a real distinction, but the only rule it carried that an agent would not have followed anyway was a single line about linking wiki guidance rather than copying it. A skill that exists to carry one line still spends a whole description competing for selection against every neighbor, which is what the fragmentation problem is made of.

What remains is one owner per question: `brief` answers where the work stands, `onboard` loads the pack, `save` writes the delta down, and `maintain-compact` cleans the pack up.

## Skill Consolidation

The family went from 18 skills to 15. What matters more than the count is the test used to get there, because the two tests tried first would each have produced a different and worse answer.

### The criterion

Two skills merge only when both conditions hold: their trigger space overlaps in a way that survives a good-faith rewrite of both descriptions, and their bodies produce the same post-state.

The rewrite clause is what stops the criterion firing on a text problem. `audit-drift` and `audit-verify` read as near-synonyms, but that was sloppy wording rather than shared identity, and renaming separated them. `sync-decision` and `sync-decisions` cannot be separated by any rewrite, because "one specific closed decision" sits literally inside "one or more". Nested concepts merge; nested wording gets rewritten.

The post-state condition keeps a read-only reporter from being merged into a writer. That boundary is visible to the user, and a flag is not the same thing as a name.

**Rejected: pointer reachability.** An earlier revision of this file held that a skill absent from the documented workflow should be reached by a pointer rather than by competing for a description match. Rejected because description match is a first-class host selection mechanism, not a fallback, while pointer reachability is a convention local to this repository: it measures only whether some other skill's prose happens to name the skill, which is an artifact of who wrote what. `extract-wiki` is the counterexample. Nothing points at it and no other skill contests its trigger vocabulary, so under the rejected criterion it looked endangered and under the current one it is among the healthiest skills present. The observation keeps one narrow use, as a signal that a pointer is missing, never that a skill is unnecessary.

**Rejected: merging by family prefix.** Collapsing `sync-*`, `audit-*`, and `maintain-*` into one skill each was proposed and rejected. A prefix is a naming artifact, not a property of the operation. `maintain-split` produces new packs plus an index, which is not a post-state `maintain-compact` shares, so it does not satisfy the criterion. The proposal reached a written plan before the contradiction was caught, which is why it is recorded rather than dropped.

### What changed

| Skill | Outcome | Reason |
|---|---|---|
| `sync-decision` | deleted, folded into `sync-decisions` | descriptions strictly nested, post-states identical |
| `maintain-prune` | deleted, no replacement skill | its success test attacked the journal |
| `audit-verify` | renamed `audit-claims`, kept separate | different unit of analysis |
| `maintain-archive` | deleted, taking `status: archived` with it | specifying the destination showed there was almost nothing to move |
| `maintain-compact` | kept, gained a pass-or-revert gate | had no success test at all |

A deleted folder takes its description with it, so the absorbed skill's trigger vocabulary was carried into the survivor. The words "atomic", "targeted", and "one specific" were the only route to the narrow decision case on hosts where `description` drives selection; dropping them with the folder would have removed a reachable behavior while appearing to remove only a duplicate.

Removal is a direct delete with no deprecation stub. The accepted cost: skills install one folder at a time and users delete manually, so a deleted skill already installed elsewhere stays there and keeps competing for selection. Deleting from this repository cannot reach it.

### Why prune was deleted rather than fixed

`hallucination` is a journal. It holds rejected options and failed approaches so a later agent does not re-propose a defeated one. Prune's success test is "is this still relevant?", and on a journal that test returns remove for exactly the content the journal exists to hold: a rejected alternative is obsolete by construction, because it was rejected, and a closed question reads as resolved and therefore removable.

The skill already carried an exception protecting lesson entries, and the exception was not enough. The conflict is with the operation's success test, not its edge-case list, and the exception covered only content written in the shape of a lesson entry. A rejected alternative written any other way was unprotected. An exception cannot patch a success test that points the wrong way.

The one legitimate case prune served, a disproven assumption still asserted as current truth, is now a contract rule instead of a skill: the claim moves into `hallucination` as a closed entry recording what was believed and what disproved it, and nothing in an active pack is removed on the grounds that it is no longer true. Owners are `sync-codebase` when code disproved it, `sync-decisions` when a decision closed it, and `save` when the current thread established it. Without that rule the deletion would leave the case ownerless, and the gap would be closed later by re-adding prune.

### Why the audit pair stays separate

| Skill | Unit | Question | Driven by |
|---|---|---|---|
| `audit-drift` | document | is this document behind the code? | `code_ref` provenance |
| `audit-claims` | claim | is this statement supported by evidence? | evidence quality, no provenance |

A document with a current `code_ref` can still be full of claims that were never true, and those did not go stale. Merging would fold a provenance-free question into a provenance-driven one, so a claim that was never supported would be reported as stale, pointing the reader at the wrong repair.

`audit-claims` is therefore forbidden from ranking or filtering claims by `code_ref`. Without that rule the two skills sit on one axis at two zoom levels, which is the state the split exists to prevent, and the rename alone would not have separated them. Its verdict vocabulary changed for the same reason: a claim is now "contradicted by evidence" rather than "false or outdated", because "outdated" implies a claim was once true.

Each description names the other skill for the question it does not answer. A routing pointer in the description reaches the surface where the wrong choice is actually made; the same sentence in the body is read only after the choice is already wrong.

That leaves the pair with a mutual reference, the same shape `sync-decision` and `sync-decisions` had, and it does not mean the same thing. That pair pointed at each other because neither description could settle which applied, so the pointers were a symptom. This pair points to state the boundary in the surface that selects them, so the pointers are the cure. Read a mutual disclaimer as a merge signal only when neither description states what separates the two.

### Why archive was deleted

`maintain-archive` survived the first round on the condition that its destination be specified, and writing that specification is what killed it. Naming where content goes forces the question of what may be moved, and the answer left almost nothing.

`hallucination` cannot be archived. It is the journal, and moving it outside `onboard`'s default scope reproduces the failure `maintain-prune` was deleted for: the content is not lost, but a fresh agent cannot reach it by default, which for that agent is the same outcome. `introduction`, `sourcecode`, and `useguide` record current state rather than history, so they hold nothing to archive. That leaves completed phase history in `roadmap`, and since the contract already forbids reasoning from living in a checkpoint, what remains movable is evidence tables and affected-file lists.

Against that, the flag had exactly one producer and one consumer, and the consumer excludes by document while every proposal reached for a per-section marker. `onboard` skips whole files, so a section marked `status: archived` inside an active document is still read in full and the exclusion does nothing.

Deleted with the skill: `status: archived` from the frontmatter enum, `onboard`'s exclusion rule, and `maintain-compact`'s `not for archiving completed phases` non-goal. A status value nothing writes and nothing reads is an affordance that invites someone to supply the missing producer, which is how a deleted skill comes back.

**Accepted cost: a long-running single-domain pack has no way to shed history.** `maintain-compact` cannot, because its gate forbids losing detail, and that gate is recent - its first step previously read "repeated and low-value content", and "low-value" was the phrase an agent used to cut old phase narration. `maintain-split` cannot, because it divides by domain and a one-domain pack has nothing to divide. Onboard cost for such a pack therefore grows monotonically. This is the price of the deletion, and nothing mitigates it.

**Rejected: keep archive and specify `<pack>/archive/` as the destination.** One file per archived phase, `status: archived` frontmatter, linked from the active roadmap, with archiving forbidden on `hallucination` and a promote-the-reasoning-first step before any relocation. Coherent, and it closes the cost above. Rejected because the operation it protects is thin once `hallucination` is excluded, and because no skill routes to it, so it fires only when a user remembers a maintenance chore.

**Rejected: move the flag into the write-able skills and drop relocation.** The first proposal, and it collapses. With relocation gone the flag is only ever a per-section marker, and `onboard` excludes by document, so the marker is inert. It would have retired the skill while appearing to keep the feature.

**Rejected earlier, and still the reason compact must not inherit relocation.** Relocation is legal under compact's information-preservation gate, since moving a completed phase into a linked file leaves the active document shorter with nothing lost, so the alternative was real. Rejected because it gives compact two mechanisms and an escape hatch from its own gate: an agent unable to compress far enough could relocate instead, satisfying "shorter" without doing the work the gate asks for. Compact's non-goal now states that prohibition directly rather than naming a skill that no longer exists.

### The compact gate

Compaction succeeds only when the document is shorter and its informational performance is unchanged. Any detail lost, or any passage that can now be read two ways, means revert rather than adjust. A long file costs less than a hallucination produced from a short one, so length is the cheap side of the trade and detail is not.

The gate is stated in the body with that cost comparison because an agent compacting always has a further cut available that looks locally harmless, and a gate without the comparison reads as advice. The description states the same standard: it previously promised to preserve "factual truth", which survives while detail is lost and a passage turns ambiguous, and the description is what selects the skill.

With prune gone, compact is the only skill that reduces an active document, so its own wording had to stop authorizing what prune was deleted for. Its first step said "repeated and low-value content", and "low-value" was the last phrase in the family permitting removal on grounds other than redundancy.

### Why the rename sweep stopped at the audit pair

`audit-verify` became `audit-claims` because the pair had been separated on unit of analysis and the name had to carry that unit. Extending the same principle across the family was considered and declined. Most skills already name what they operate on, and `maintain-compact` and `maintain-split` name an operation whose object is unambiguous because a pack is the only thing they act on. `sync-reconcile` was the one real candidate, and it keeps its name for three reasons.

The name is not the surface that selects it. `onboard` and `brief` both name it in shipped text, each at the moment a contradiction is found, which is when the choice is actually made. A rename would improve a surface that is not the entry path.

The family has no single convention to conform to. `sync-codebase` names the source of truth it compares against; `sync-decisions` names the thing it propagates. Two already-direct names, two different patterns, so "name the object" has no one target. `sync-contradictions` is a better name than the one kept, and it would parallel one of those two while diverging from the other.

The cost is larger than the install boundary above implies, and it was measured rather than estimated. A machine carries several independent host skill directories, four on the one checked, each a real copy rather than a link into a shared store, and the installer adds and overwrites but never removes. A rename leaves the old name in all of them until someone deletes it by hand.

The principle stands for a new skill. What was declined is the retroactive sweep.

### Why there is no finished-pack marker

Deleting `status: archived` raised the question of whether a pack-level equivalent should replace it, and the answer is no, because the behavior already exists a layer up. `onboard` is pointed at a target rather than scanning for one, and on an initiative it reads the index, stops, and selects the scope only when the routing evidence names exactly one sub-pack in progress. A finished pack is already not selected. A frontmatter value would restate a routing rule as data.

`status: complete` cannot be reused for it either. This repository's own consolidation pack is complete and is exactly what a contributor must read before touching a skill folder, since it carries the whole argument for the shape the current skills have. A rule that skipped complete packs would skip the most load-bearing document present. A finished marker would therefore need a value distinct from `complete`, making it a schema change rather than a reuse of one.

**Rejected: add a `parked` value with `onboard` as its consumer.** Unlike the value that was deleted, this one would operate at file granularity, so the mechanism would work. Rejected because no initiative index exists yet, so the payoff is zero, and because it would be `onboard`'s first status-based scope filter after the previous one was removed, rebuilding a mechanism to obtain a behavior routing already provides. The evidence that would justify reopening it is a real multi-pack initiative where index status proves insufficient for routing.

### One rule, one place

The lesson-entry rule was stated in five wordings: once in the contract and four times elsewhere. `tests/test_references.py` could not see them drift, because it compares contract copies against the canonical file and knows nothing about a paraphrase written somewhere else. Each removal followed the same order: widen the canonical sentence to cover what the duplicate uniquely said, re-copy it to every packaged copy, and only then delete. Deleting first drops the rule for as long as it takes to notice.

`maintain-compact` uniquely said "do not compress it", `run` and `save` uniquely said "even after the mistake is resolved", and all three now live in the one canonical sentence. Where a local signpost was doing real work beside a neighbouring instruction it was replaced by a pointer rather than deleted outright: "a lesson entry is not a diary entry" sits next to "do not keep a diary", and removing it entirely would have left the neighbour over-applied.

This file states the rule too, under `Evidence Retention`. That is not the same duplication. `DESIGN.md` does not ship and no agent can open it, so it explains rules rather than enforcing them; the constraint is on files a running agent reads.

## Detect And Repair

All five skills stay, and nothing is merged. The question that framed this as a choice between two architectures was built on a model of the family that reading the five bodies disproved.

### The comparison-scope axis does not exist

An earlier revision here modelled `sync` and `audit` as one detect and repair axis applied across four comparison scopes, with only one row filled. The scopes are not distinct. `audit-drift` compares code changes, document claims, and decision records. `audit-claims` compares each claim against code and explicit decisions. `sync-reconcile` prefers code evidence and explicit user decisions to break a tie. Three of the five consult the same two sources, so scope is not what separates them, and a matrix drawn on that axis reports holes that are artifacts of the axis.

Two axes separate them, and they are not the same axis:

| Group | Separated by | Members |
|---|---|---|
| report-only | unit of analysis | `audit-drift` at document level, `audit-claims` at claim level |
| writes | the event that triggered the write, which fixes the blast radius | `sync-codebase`, `sync-decisions`, `sync-reconcile` |

The first is the split recorded above under the audit pair. The second is stated in each body already, and the three differ:

| Skill | Triggered by | Touches |
|---|---|---|
| `sync-codebase` | code changed | the whole pack in one pass |
| `sync-decisions` | a decision closed | only the sections that decision reaches, under an explicit rule against widening |
| `sync-reconcile` | the pack contradicts itself | only the conflicting sections |

Blast radius is visible to the user and is set by the trigger, which is why an agent cannot pick the wrong one by accident the way it could pick a wrong mode.

### Why the matrix is not completed

Each apparently empty cell was checked, and each turned out occupied or unwanted, for a different reason in each case.

| Cell | Verdict |
|---|---|
| repair for claim against evidence | occupied by the contract. The disproven-claim rule already names three owners: `sync-codebase` when code disproved it, `sync-decisions` when a decision closed it, `save` when the thread established it. A skill here would be a fourth owner of a rule that names three |
| detect for pack against itself | occupied by `onboard` and `brief`. Both report a contradiction and route to `sync-reconcile` without repairing it. A separate skill would serve only "show contradictions without loading the pack", which nothing has asked for |
| detect for decision against pack | occupied by `audit-drift`, whose second step already compares decision records. Its description was narrower than its body and now says so |

A matrix with holes is not evidence that the holes should be filled. It is a diagnostic, and a diagnostic drawn on the wrong axis manufactures work.

### Rejected: one skill per comparison scope, with detect as a report-only mode

Rejected on cost asymmetry, which is a stronger objection than the boundary-visibility one that was recorded first.

`audit-drift` is doc-first: it reads frontmatter to narrow to the documents worth checking, then compares scoped code changes. `sync-codebase` is code-first and unscoped, opening with "inspect the codebase first". Running the merged skill in report-only mode still pays the full inspection cost, so the family would trade a cheap screen plus an expensive fix for one expensive skill with a flag. The screen is the part that gets used most and it is the part that would be lost.

Terraform separating `plan` from `apply` as two commands is the same shape of argument from consequence rather than cost, and it points the same way.

### Consequences

`baselinedocs-sync` is not needed as a namespace, because no merge happens. `baselinedocs-sync-decisions` keeps its longer name for the reason it was given: a bare `sync` would attract every request to sync docs against code through the name alone.

`sync-codebase` and `sync-decisions` were named by nothing in shipped text. That is the one narrow use the pointer observation retains under the merge criterion, a missing pointer rather than an unnecessary skill, and `audit-drift` now names all three repair skills when it recommends follow-up actions. A detect skill naming its repair skill is the pointer at the surface where the reader is actually deciding what to do next.

## Evidence Retention

Keep:

- final passing or failing result supporting current status
- unresolved failures
- failures that explain a changed design
- reproduction details for an active defect
- a lesson entry: a mistake, why it looked reasonable, what disproved it, and the fix - kept in full even after resolution, because this is what stops the mistake recurring

Discard from active docs:

- routine failed fixture iterations
- repeated commands with the same meaning
- transient syntax or setup mistakes already resolved
- chat chronology that does not affect current truth

A resolved mistake is not the same as a routine failed attempt. The discard list above targets attempts that carry no reusable insight, not a documented misjudgment that would otherwise be repeated.

External raw logs may still be linked when auditability requires them.

## Useguide Role

`useguide` means a consumer contract. Valid forms include:

- API request and response behavior
- method or library usage
- migration or conversion procedure
- operator workflow
- black-box behavior needed by another team

If no consumer exists, omit the file. Reusable procedures that apply across tasks should move to the wiki.

## Loop Engineering

`baselinedocs-run` has no silent execution-policy defaults. Before implementation, it asks for any missing `approval_policy` and `commit_policy`. Selecting `per-phase` in the user's reply is explicit commit authorization for that run.

After initial completion, feedback is assigned to the phase whose acceptance criteria it refines. A new phase requires a new outcome, dependency, release gate, deployable unit, or independently reviewable body of work.

## Multi-Pack Routing

An initiative index is routing metadata:

- direct child-pack links
- domain scope
- dependency edges
- current cross-pack checkpoint

It is not a general introduction or roadmap that duplicates child content. This keeps every sub-pack directly queryable while preserving cross-domain order.

## Deferred Work

- Package-level installation profiles could hide internal helpers more completely, but Skills.sh does not currently provide a portable hidden-skill category.
- Organization-wide hook rollout remains deferred. The setup skill handles one repository at a time and preserves unknown configuration rather than replacing it.
- Blind semantic writing from transcript or repository-wide candidates remains rejected. The agent may checkpoint only a pack unambiguously established in its current thread.
Nothing about the skill family remains deferred. The rename sweep and the finished-pack marker were both closed rather than postponed; see `Skill Consolidation` above for each, including the evidence that would justify reopening them.

## Research Basis

- [OpenAI Codex skills](https://developers.openai.com/codex/skills): explicit and implicit invocation plus `allow_implicit_invocation`
- [OpenAI Codex hooks](https://developers.openai.com/codex/hooks): project hook discovery, trust review, Stop, and compaction events
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks): Stop, task, and compaction lifecycle behavior
- [Cursor agent best practices](https://cursor.com/blog/agent-best-practices): dynamic skills and the `stop` continuation pattern
- [Skills.sh CLI](https://www.skills.sh/docs/cli): installation and discovery surface
