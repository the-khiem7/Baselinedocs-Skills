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

Skills install one folder at a time and cannot reach a sibling skill's files, so every pack-writing skill ships its own copy of the contract. Those copies are packaged assets of `contract/pack-contract.md`, the same arrangement `hooks/checkpoint.py` already uses, and they are pinned by a test for the same reason: a copy that drifts reaches whoever installed that one skill, and nothing in their install tells them it is stale.

The README now documents only the whole-family install, and that does not relax this boundary or permit collapsing the copies into one shared file. `npx skills add --skill <name>` still works and is merely no longer advertised, and a host's skills directory is a place users delete from as well as install into, so a skill can still end up alone next to nothing. The boundary is what a folder can be relied on to contain, not what one install command happened to fetch. Pointing a skill at a sibling's `references/` would work on the maintainer's machine and fail silently on a user's.

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

Archived material sits outside the default scope. `baselinedocs-maintain-archive` exists to move finished history out of the active flow, so reading it straight back in spends the context budget the active pack needs and undoes that maintenance. The exclusion is reported rather than applied quietly, because an unreported exclusion fails the same way a silent truncation does: the user cannot tell what the agent is actually holding.

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

Retained source material is excluded by default, on the same reasoning as archived content. `baselinedocs-adopt` promises a pack collectively equivalent in information to its source, so loading both loads the same information twice. It is not a marginal cost: in the first real run, `sources/PROPOSAL.md` was 2415 of the 3460 lines read, seventy percent of the budget spent on content the pack already carried. Files without baseline frontmatter identify this material without needing a naming convention.

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
| `resume-snapshot` | `baselinedocs-maintain-compact` covers it and covers it better. The triggers were the same (a long, noisy, chat-driven pack), the steps were the same (distill what is true now, drop attempt-by-attempt narration), and compact additionally forbids compressing a lesson entry away, which snapshot never mentioned. Snapshot also never said where the snapshot goes, while carrying the contract gate that only makes sense for a skill that writes pack files, so what it actually produced was never settled |
| `resume-next-step` | `baselinedocs-brief` reports the recorded next action verbatim. What next-step added on top of that was permission to substitute its own judgment for what the pack records, with no way to know the recorded action was stale and no obligation to say it had substituted, which is the failure `brief`'s delta rule exists to prevent. It was also the least guarded skill in the repository, with no contradiction handling, no read-against-skipped disclosure, and no statement that it is not a load, while producing the most command-shaped output of any of them |
| `resume-handoff` | A pack that needs a separate handoff artifact is a pack failing at its stated purpose. Baseline Docs exists so another conversation or agent can resume without chat history, so the pack is the handoff and a fresh thread with `baselinedocs-onboard` is how it gets read. This is the same reasoning that made "returning after weeks" an anti-pattern in the table above, applied to a second reader rather than the same one |

Keeping `resume-handoff` for the reader who will not run an agent at all was considered and rejected. It was the only skill in the family whose output was meant to leave the thread, which is a real distinction, but the only rule it carried that an agent would not have followed anyway was a single line about linking wiki guidance rather than copying it. A skill that exists to carry one line still spends a whole description competing for selection against every neighbor, which is what the fragmentation problem is made of.

What remains is one owner per question: `brief` answers where the work stands, `onboard` loads the pack, `save` writes the delta down, and `maintain-compact` cleans the pack up.

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
- Collapsing the `sync`, `maintain`, and `audit` families into one skill each remains under review. Skill selection happens with only descriptions in context, so near neighbors can be undecidable at the moment of choice: `sync-decision` claims "one specific closed decision" and `sync-decisions` claims "one or more", which logically includes one. Moving the choice inside a single loaded skill would put it where the full text of every mode is visible, which is also what stops the choice from depending on how strong the selecting agent is. The cost is that one description then has to cover several operations, trading precision between families for precision within one. A second piece of evidence: the intended workflow, drawn out in full, invokes exactly the seven entrypoints and none of the eleven lifecycle skills. That is not proof the eleven are unnecessary, since `baselinedocs-onboard` and `baselinedocs-brief` reach `sync-reconcile` and `audit-drift` by naming them in already-loaded text, but it does say a skill absent from the workflow should be reached by a pointer rather than by competing for a description match.

## Research Basis

- [OpenAI Codex skills](https://developers.openai.com/codex/skills): explicit and implicit invocation plus `allow_implicit_invocation`
- [OpenAI Codex hooks](https://developers.openai.com/codex/hooks): project hook discovery, trust review, Stop, and compaction events
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks): Stop, task, and compaction lifecycle behavior
- [Cursor agent best practices](https://cursor.com/blog/agent-best-practices): dynamic skills and the `stop` continuation pattern
- [Skills.sh CLI](https://www.skills.sh/docs/cli): installation and discovery surface
