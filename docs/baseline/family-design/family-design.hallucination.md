---
baseline_schema: "2.0"
pack: "family-design"
document: "hallucination"
status: "active"
updated: "2026-08-28"
code_ref: "0cb913f"
---

# Family Design: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more: never its reasoning, never the justification behind its outcome, never a summary that could be mistaken for the entry. An answer that turns on an entry whose full text was not read is unbacked, and must be reported that way rather than derived from a row.

Required by `contract/pack-contract.md` above 40 KB or 20 entries. This document holds 32.

Every identifier in this initiative carries its pack's prefix: `FD-` here, `SC-` in `skill-consolidation`. It is written that way everywhere, inside the pack as well as across packs, so a reference is unambiguous wherever it is read and greppable across the whole repository. FD-D30 records the decision.

| Entry | About | Status | Related |
|---|---|---|---|
| FD-D1 | which skills a host may fire on its own, and how the rest stay deliberate | current | FD-D9, FD-Q1 |
| FD-D2 | the move from a fixed five-document pack to three core plus two conditional | current | FD-D22, FD-D25 |
| FD-D3 | what `code_ref` records, and what it cannot record | current | FD-D18 |
| FD-D4 | what a phase checkpoint contains and which document holds it | current | FD-D5, FD-D21 |
| FD-D5 | the boundary between what `run` checkpoints and what `save` writes | current | FD-D4, FD-D8 |
| FD-D6 | how much the checkpoint hook is allowed to work out for itself | current | FD-D4, FD-D26 |
| FD-D7 | which instruction surface carries a rule's pointer and which carries its content | current | FD-D2, FD-D21 |
| FD-D8 | writing the family's intended order down, and where `save` sits in it | current | FD-D5, FD-D9, FD-D19 |
| FD-D9 | what the README leads with | current | FD-D1, FD-D8 |
| FD-D10 | how `onboard` avoids reading half a pack and believing it read all of it | current | FD-D11, FD-D17 |
| FD-D11 | what `onboard` loads when the target is an initiative rather than one pack | current | FD-D10, FD-D12, FD-D24 |
| FD-D12 | when `onboard` may skip asking which sub-pack to load | current | FD-D11 |
| FD-D13 | what `onboard` does when an initiative has sub-packs and no index | current | FD-D11, FD-D24 |
| FD-D14 | what a dependency edge tells a reader, and what it does not | current | FD-D11, FD-D24 |
| FD-D15 | what `onboard` does about a loaded pack leaning on one that was not loaded | current | FD-D10, FD-D13 |
| FD-D16 | what happens when the index and a pack disagree about status | current | FD-D24 |
| FD-D17 | what `onboard` reports first | current | FD-D10 |
| FD-D18 | whether the source document an adopted pack came from is loaded with the pack | current | FD-D3, FD-D10 |
| FD-D19 | dissolving the `resume-*` family, and what replaced `resume-continue` | current | FD-D8, FD-D20 |
| FD-D20 | deleting the last three `resume-*` skills with nothing in their place | current | FD-D19 |
| FD-D21 | which evidence an active document keeps and which it drops | current | FD-D4, FD-D29 |
| FD-D22 | what `useguide` means and when the file is omitted | current | FD-D2, FD-D25, FD-D29 |
| FD-D23 | whether `run` may choose an approval or commit policy in silence | current | FD-D4 |
| FD-D24 | what an initiative index holds and what it must not hold | current | FD-D11, FD-D13, FD-D16 |
| FD-D25 | why this pack has no `useguide` | current | FD-D22, FD-D9 |
| FD-D26 | writing a checkpoint from a transcript or from repository-wide candidates | current, rejected and still rejected | FD-D6 |
| FD-D27 | what happens to `DESIGN.md` now that this pack exists | current, carried out. The file is deleted | FD-D7, FD-D28 |
| FD-D28 | a coverage ledger routed seven sections to another pack without checking that pack carried them | current, repaired | FD-D27, FD-D7 |
| FD-D29 | whether the contract carries the retention and `useguide` detail in full or in summary, closing FD-Q3 | current | FD-D21, FD-D22, FD-D7 |
| FD-D30 | how an identifier is named once an initiative holds more than one pack, closing FD-Q4 | current | FD-D24, FD-D27 |
| FD-Q1 | hiding internal helpers at package level rather than by naming convention | open, deferred on a missing platform feature | FD-D1 |
| FD-Q2 | installing checkpoint hooks across more than one repository | open, deferred | FD-D6 |

## FD-D1: six entrypoints stay deliberate, and the rest stay agent-selectable

**Decided.** Six user entrypoints, `init`, `adopt`, `save`, `run`, `onboard`, and `brief`, plus the one-time `setup-hooks` utility, set `allow_implicit_invocation: false` in `agents/openai.yaml`. The eight lifecycle skills keep it enabled. Alongside that, lifecycle skills prefix their UI name with `Baseline Docs Internal:`, their descriptions state the automatic trigger context, and the README teaches the entrypoints and never the lifecycle skills.

**Why.** An entrypoint is a decision the user makes: loading a pack, running a roadmap, writing state down. A lifecycle skill is a repair the agent should be able to reach for when it notices the condition. Firing an entrypoint implicitly spends the user's context on their behalf; requiring an explicit call for a lifecycle skill means the repair happens only when a user already knows the skill exists.

**What breaks if ignored.** Without the split, either every skill fires on its own, so `onboard` can consume a context window unasked, or none does, so the sync and audit skills become dead weight that only an expert invokes.

**This is progressive disclosure, not a hidden registry.** `allow_implicit_invocation` is a Codex field. It is not portable, it does not remove a skill from every picker, and on other hosts `description` is the real selection surface. The naming prefix and the README's silence are what carry the intent elsewhere. Claiming that every host can maintain two physically separate skill registries would be false, so the design does not claim it.

**Rejected: rely on the policy field alone.** It would have been one field and no convention. Rejected because on a non-Codex host the field is inert, and an entrypoint would then be indistinguishable from a helper at exactly the surface that selects it.

## FD-D2: the pack is three core documents plus two conditional

**Decided.** Schema `2.0` replaces the fixed five-file contract with `introduction`, `roadmap`, and `hallucination` as core, and `sourcecode` and `useguide` as conditional. The transition is additive: existing five-file packs stay valid, and no skill deletes an existing conditional document merely because a new pack would not create one.

**Why.** Three of the five files answered a question every pack has. The other two answered questions some packs do not have, and a mandatory file with no content to put in it gets filled with `not applicable` filler, which costs a read on every load and tells the reader nothing.

**What breaks if ignored.** Made mandatory, the two conditional files become filler. Made freely deletable, a lifecycle skill prunes a `sourcecode` a later phase needed, and the information is gone rather than relocated.

**Rejected: keep the fixed five.** Simpler to describe and impossible to get wrong. Rejected because the filler cost is paid by every reader of every pack, forever, while the ambiguity cost of a conditional file is paid once by the author.

## FD-D3: `code_ref` is code provenance, not the document's commit

**Decided.** `updated` records the date the document was last edited. `code_ref` records the state of the code that was actually inspected while writing it, expressed as a commit, `uncommitted`, or `unknown`.

**Why.** A document cannot carry its own Git commit hash, because writing the hash into the file changes the file and therefore changes the commit. The field a reader actually needs is different anyway: not when the document was written, but what the writer was looking at.

**What breaks if ignored.** A drift audit that reads `code_ref` as a document version compares the wrong two things. Treating a newer repository commit as automatic proof of drift is the other half of the same error: the commit may not have touched anything the document describes, so the audit must compare the scoped changes against the claim body before declaring drift. A newer commit is a signal, not a verdict.

**Rejected: record nothing and compare dates.** An `updated` date tells a reader when someone typed, which correlates with code state only by accident.

## FD-D4: a phase checkpoint holds outcome, not reasoning

**Decided.** A semantic checkpoint lives in `roadmap` and contains the phase outcome and status, the final evidence, the affected files, the open risk, and the exact next action. It does not contain a defect's cause or a rejected alternative; those live in `hallucination`, and the checkpoint links to them rather than repeating them.

**Why.** The two documents have different lifetimes. An outcome is superseded by the next phase; a reason is not, and a reason repeated in both places has to be corrected twice on every later change.

**What breaks if ignored.** The roadmap grows into a narrative, and the same reasoning drifts between two documents until they disagree about why something was done.

## FD-D5: `run` writes its own checkpoint, so `save` is not the step after `run`

**Decided.** `baselinedocs-run` writes the phase checkpoint itself after every phase. `baselinedocs-save` owns what a checkpoint does not: a decision that closed, a question that opened, a scope that moved.

**Why.** Everything a phase checkpoint holds lives in `roadmap`, and `run` already puts it there. Stated the other way round: after a clean run the roadmap is current and the other two core documents may not be, and closing that gap is the whole job of a save that follows a run.

**What breaks if ignored.** Calling `save` the step after `run` teaches the user that a run leaves the pack incomplete, so they either run a redundant save that finds nothing to write, or they skip save entirely on the phases where a decision actually closed.

## FD-D6: the checkpoint hook infers nothing about the repository

**Decided.** The command adapter performs no roadmap discovery, no Git inspection, no timestamp comparison, and no semantic completion check. On the first Stop event of a turn it returns a fixed prompt to the same thread. The agent identifies a pack only from that thread and makes no change when the pack is absent, ambiguous, or already current. Each host's stop-loop field prevents a second continuation.

**Why.** A hook sees a repository, not a conversation. It cannot tell which pack owns the work, and a shared working tree may hold changes from other threads, so any ownership it inferred would be a guess applied automatically. Putting the judgment in a prompt returned to the thread moves the decision to the only place that holds the context needed to make it.

**What breaks if ignored.** A hook that guesses writes a checkpoint into somebody else's pack, or attributes another thread's changes to this one, and it does so silently on every turn.

**Accepted cost.** At most one extra continuation per turn, spent to avoid global roadmap guesses and shared runtime markers. Parallel threads keep separate conversation context, and the prompt warns explicitly that the working tree does not.

**Rejected: detect the active roadmap in the hook and check whether it is current.** The obvious design, and the one the adapter is written to make impossible. Rejected because ownership is not derivable from repository state, and a wrong automatic write is more expensive than a prompt that turns out to be unnecessary.

## FD-D7: the pointer lives in `SKILL.md`, the content lives in one file

**Decided.** A rule a running agent must obey is stated in exactly one file. The sentence sending the agent to read that file is restated in every `SKILL.md` that needs it, and is the only thing restated.

**Why.** The surfaces do not offer the same guarantee, as `family-design.sourcecode.md` sets out: `description` is always in context, a `SKILL.md` body loads whenever the skill runs, and a `references/*.md` file loads only if the body says to read it and the agent complies. So the gate requiring the contract to be read cannot itself live in the contract, because an agent that skipped the file never reaches the sentence telling it not to skip the file.

**What breaks if ignored.** Two copies of a rule disagree from the day they are written, and a test comparing copies of the same block cannot see it. That is not hypothetical: an earlier revision embedded the document role list into every pack-writing `SKILL.md` as well as into the contract, and the two descriptions of `hallucination` disagreed immediately.

**Rejected: embed the role list in every `SKILL.md` as well.** The arrangement above, and the reason it failed is above.

**Rejected: keep the role list inline and strip roles out of the contract.** The mirror image, and it does not separate cleanly. The contract still has to name the five documents to give their filenames and inclusion criteria, so both files would keep discussing the same five things, divided only by a line between "what it holds" and "when to create it" that is too fine to survive editing.

**Who ships which asset is a different question.** It is decided in `skill-consolidation` SC-D16 for the contract and SC-D17 for report style, on a criterion this entry does not restate.

## FD-D8: the intended sequence is written down, and `save` comes before any branch

**Decided.** The family has one intended order, and it is recorded rather than left implicit. Its load-bearing step is `baselinedocs-save` before any context branch.

**Why the sequence is written at all.** Every skill was individually correct while the order connecting them lived only in its author's head. Walking that order through out loud surfaced four defects at once: `brief` placed at a node it is built to refuse, `save` described as the step after `run` when run already checkpoints, one entry door named out of three, and no return edge closing the loop. None was a skill defect. An unwritten sequence cannot be checked against anything, which is the reason to write it down even though every part of it was already true.

**Why `save` is the load-bearing step.** Both branches lose the thread. Staying keeps a lossy summary of it and leaving keeps none, so the pack is the only thing that survives either. Saving first is what makes a lost context ordinary rather than an incident.

**The two branches are not equivalent, and the difference is a count of sources.**

| Branch | Sources of truth afterwards | Consequence |
|---|---|---|
| Stay in the thread, then host `/compact` | two: the pack, and a compaction summary that can disagree with it | the disagreement has to be managed, which is what `brief` reports |
| New thread, then `onboard` | one: the pack | nothing can disagree, at the cost of re-reading |

A new thread is the default once the pack is current, which after a save it is. Staying is for the case where the thread still holds something that could not be written down, a half-formed approach or a debugging session in flight.

**Where `brief` sits.** Before the expensive choice, not in place of it. It is a diagnostic: it reports whether the pack has fallen behind the thread, which is what tells the user to carry on, to run `save`, or to pay for a full `onboard`. Using it as the recovery step itself is the error FD-D9 records, and it is the error the skill's own first rule refuses.

**What breaks if ignored.** Branching before saving loses whatever the thread held and the pack did not, and no later skill can recover it, because the only copy was the conversation.

## FD-D9: the README leads with the ordered workflow

**Decided.** `README.md` opens with the workflow as a Mermaid flowchart, followed by a branch comparison table and a trap table. The entrypoint table comes after it. Per-skill install commands were removed.

**Why.** The entrypoint table answers "I want X, which skill do I call", which is the question a reader has once they already know the shape of the work. It cannot answer "X is finished, what now", because a table carries no ordering and no branch. The flowchart is used because the two branch points are the whole content and any linear format buries them, and the two tables under it are used because branch against branch is a comparison and the traps are a lookup, and a reader should not have to extract either from prose.

**What breaks if ignored, and it already did.** The author of this family placed `brief` at the node meaning "make sure no detail was forgotten after a compaction", which is the one thing brief is built to refuse, its first rule being to state that it is not a load. A structure that lets its own author put a skill in the wrong place will not teach anyone else the right one.

**Why the install commands went.** The skills route to each other by name, so a partial install turns a pointer into a dead end that surfaces only after the user has already asked for something. This is a teaching decision, not an enforcement one: `npx skills add --skill <name>` still works and is merely no longer advertised.

## FD-D10: `onboard` enumerates before it reads, and narrows in the open

**Decided.** `onboard` promises a complete read of the selected scope. It enumerates the files and reports line counts before reading, states what the scope excludes, and when it cannot say with confidence that the scope fits, it stops, presents the total, proposes a narrower scope, and waits.

**Why the gate is worded on the agent's own uncertainty.** An agent cannot measure its share of a context window, so a threshold phrased that way is settled by guess. "Can you state with confidence that this fits" is a question it can answer, and it resolves toward asking.

**What breaks if ignored.** Silent truncation is the designed-out failure. An agent that read half a pack and believes it is loaded gives confidently wrong answers, which is worse than an agent that knows it has read nothing.

**Rejected: a percentage-of-context threshold.** Precise-sounding and unmeasurable from inside the agent, so in practice it becomes a guess wearing a number.

## FD-D11: an initiative routes before it loads, and one pack is the default scope

**Decided.** An index is routing metadata. `onboard` reads the index, stops, and selects one sub-pack. It does not treat the index as a manifest of everything to pull in, and one domain pack is the default scope.

**Why.** Loading a whole initiative by default would spend exactly the context an index exists to conserve, and it would trip the size gate on nearly every real initiative, which turns the gate into noise the agent learns to talk past.

**What breaks if ignored.** The index becomes a table of contents for a load nobody asked for, and the size gate stops meaning anything because it fires every time.

## FD-D12: the routing question is skipped only on evidence

**Decided.** When the index marks exactly one sub-pack in progress, `onboard` loads that pack and names the evidence that selected it. Two candidates, or none, means asking.

**Why.** Asking the user to repeat what the index already states wastes a turn, and naming the evidence leaves the user able to redirect. But "which pack looks most important" is not evidence; it is the guess this rule exists to block.

**What breaks if ignored.** An agent that selects on judgement loads the wrong pack and reports it as routed, so the user finds out only when an answer comes back about the wrong domain.

## FD-D13: `onboard` reconstructs a missing index but never writes one

**Decided.** When an initiative has several sub-packs and no index, `onboard` builds the routing view in memory from each sub-pack's frontmatter and next action, reports the missing index, and names `baselinedocs-maintain-split` as the skill that creates one. It does not create it.

**Why.** A pack set grows by hand faster than anyone runs a split, so this state is normal rather than broken. But `onboard` writes nothing, and an index composed by a reader would record links and statuses it inferred rather than the dependency edges and cross-pack checkpoint only an author can supply. Those two fields are reported missing rather than guessed, because inferring order from directory names or an import graph produces an ordering that looks authoritative and is not.

**What breaks if ignored.** A reader-written index is indistinguishable from an author-written one, so the next reader trusts inferred edges as declared ones.

**A consequence worth stating.** The index is itself a document with its own frontmatter, so it takes its own manifest row, and an initiative has several next actions, one per pack in scope plus the index's cross-pack checkpoint. That is why the output is plural.

## FD-D14: a dependency edge is status, not reading order

**Decided.** A dependency edge records why a pack is blocked. It does not assert that one pack's documents cannot be understood before another's. `onboard` reports the edges and reads in no particular order.

**Why.** Ordering reads by dependency gains nothing once one domain pack is the default scope, and it implies a comprehension dependency between packs that the contract never claims.

**What breaks if ignored.** A reader who treats edges as reading order pulls in an upstream pack it was never asked to load, which is the scope expansion FD-D11 exists to prevent, arriving through a different door.

**Rejected: order the reads by dependency.** Considered and dropped for the two reasons above.

## FD-D15: cross-pack coupling is resolved by evidence, not by policy

**Decided.** `onboard` collects the references the text actually makes, quotes each with its source, and offers to load what they name. It does not auto-load, and it does not refuse to look.

**Why both fixed policies were rejected.** Loading one pack risks answering from a neighbour that was never read. Loading every neighbour spends the context an index exists to conserve. Both decide before reading, while the question is only answerable during it: a dependency edge can be purely operational with no coupling between the documents at all, and a pack can lean on another it has no edge to, because edges are declared by hand and get forgotten.

**Why this is safe.** The hallucination risk is not the unread pack. It is answering from an unread pack without knowing it went unread. An agent holding an explicit list of what it could not resolve cannot make that mistake silently, which is the same principle the whole skill rests on: knowing you have read nothing is safer than believing you read everything.

**What breaks if ignored.** An answer that turns on an unquoted, unread reference is unbacked and reads exactly like a backed one.

**Rejected: auto-load on a non-empty reference list.** It reinstates the scope expansion the routing default exists to prevent, and the offer costs one turn.

## FD-D16: an index-versus-pack status disagreement is reported, never resolved

**Decided.** Index status is routing metadata that restates a status each pack also owns. When the two disagree, `onboard` reports a contradiction. It does not prefer the index, and it does not prefer the newer `updated` date. `baselinedocs-sync-reconcile` owns the repair.

**Why.** Duplication the contract accepts for routing still drifts, and a reader that silently picks a winner destroys the evidence that the two ever disagreed.

**What breaks if ignored.** The drift is resolved invisibly on every read and never repaired at source, so it recurs indefinitely and nobody sees it.

## FD-D17: the output leads with pack state, not with the manifest

**Decided.** `onboard` reports what the documents record first: what the project is, its target, phase status, the recorded next action quoted verbatim, open questions, and unresolved references. The load manifest follows as the check on the read.

**Why, from a real run.** The first use returned a correct file-by-file manifest and none of what the reader wanted. The documents onboard had just read exist precisely to carry the state: `introduction` owns scope and target, `roadmap` owns phase status. The skill was reporting metadata about the files instead of the state inside them. A manifest proves the read happened; it is not what anyone loads a pack to find out.

**What this does not turn onboard into.** A brief. `onboard` reports what the documents record from a complete read; `brief` reports position from a deliberately partial one. The rule keeping onboard descriptive is explicit because a skill that has just read everything is well placed to start assessing progress and recommending action, which is a different job on a different reading strategy.

**What breaks if ignored.** The reader gets bookkeeping and has to ask a second question to get the answer they came for, which spends the turn the manifest was supposed to save.

## FD-D18: retained source material is out of scope by default

**Decided.** Material retained from an adoption is excluded from `onboard`'s default scope and the exclusion is reported. Files without baseline frontmatter identify this material, so no naming convention is needed.

**Why.** `baselinedocs-adopt` promises a pack collectively equivalent in information to its source, so loading both loads the same information twice. It is not a marginal cost: in the first real run, `sources/PROPOSAL.md` was 2,415 of the 3,460 lines read, seventy percent of the budget spent on content the pack already carried.

**Why the exclusion is reported rather than applied quietly.** An unreported exclusion fails the same way a silent truncation does: the user cannot tell what the agent is actually holding.

**What breaks if ignored.** Either the largest file in the pack is read for nothing, or it is skipped without the user knowing the pack had a source at all.

**Related provenance rule.** Provenance is recorded, not adjudicated. `code_ref` may be a commit, `uncommitted`, or `unknown`, and only the first is comparable; even then a moved repository is reported as a signal. An onboard that starts investigating drift stops being a bounded read and turns into `baselinedocs-audit-drift` without its scope limit.

## FD-D19: the `resume-*` family is dissolved, and `brief` replaced `resume-continue`

**Decided.** `baselinedocs-resume-continue` is deleted and `baselinedocs-brief` takes its place. The audit method was to take each situation the old skill claimed and ask which skill already owned it.

| Situation the old skill claimed | Outcome |
|---|---|
| Returning after weeks | An anti-pattern. The point of a pack is resuming without chat history, so the correct path is a fresh thread and `onboard`. A partial-recovery skill earns its place only if the pack cannot be trusted, which is a different problem |
| Deciding whether the pack has gone stale | Owned twice over: `audit-drift` answers the question, `save` and `sync-codebase` close it. `save` even ends by reporting where work should resume |
| Orienting mid-task | A real need the skill served weakly, now `brief` |
| Recovering after a compaction | Its stated reason to exist, and the case it handled worst |

**Why the compaction case failed, which is what `brief` is built around.** After a compaction the summary in context can hold hours of work that was never written into the pack, so the pack is behind the thread. The old skill read the pack and reported it, never comparing the two, and returned a continuation point stale by exactly the amount of unrecorded work, with nothing marking it as such. It also read selectively with no definition of what it read and no obligation to say what it skipped, so the reader could not tell how much of the pack the brief rested on.

**What `brief` carries that the old skill lacked.** Three rules: state that this is not a load, report what was read against what was skipped, and compare the thread against the pack and report the delta. The last is the job nothing else in the family does. Writing the delta down stays with `save`; brief only surfaces it, because a skill that detected a gap and closed it in the same breath would be writing to a pack it only partially read.

**What breaks if ignored.** A recovery skill that does not compare thread against pack hands back a stale continuation point that looks current, which is the single most expensive wrong answer this family can give.

**Rejected: make `onboard` the successor.** It is explicit-only by policy, so on Codex nothing would fire after a compaction, which is exactly when the user is least likely to remember to invoke anything. More fundamentally, onboard is bound to report the state the documents record and forbidden to assess it, so after a compaction it would load a stale picture completely and confidently, arriving at onboard's own designed-out failure through a different door.

**Rejected: keep the old skill alongside the new one.** Two skills answering "where are we" from overlapping reads is how an agent picks the wrong one, and the old skill's weaknesses are not additive with the new one's guarantees.

**Accepted cost.** `brief` is a user entrypoint, so it sets `allow_implicit_invocation: false` like the others. On Codex that costs the automatic firing the compaction case wants. The field is Codex-only and on other hosts `description` still reaches the skill without it being typed, so the cost is bounded to one host and is the price of keeping the entrypoint classification meaningful.

## FD-D20: the last three `resume-*` skills are deleted with no replacement

**Decided.** `resume-snapshot`, `resume-next-step`, and `resume-handoff` are deleted. Nothing takes their place.

| Skill | Why it went |
|---|---|
| `resume-snapshot` | `maintain-compact` covers it and covers it better. Same trigger, a long noisy chat-driven pack; same steps, distill what is true now and drop attempt-by-attempt narration; and compact carries a pass-or-revert gate that snapshot never had. Snapshot also never said where the snapshot goes, while carrying a contract gate that only makes sense for a skill writing pack files, so what it produced was never settled |
| `resume-next-step` | `brief` reports the recorded next action verbatim. What next-step added was permission to substitute its own judgment for what the pack records, with no way to know the recorded action was stale and no obligation to say it had substituted, which is the failure brief's delta rule exists to prevent. It was also the least guarded skill in the repository, with no contradiction handling, no read-against-skipped disclosure, and no statement that it is not a load, while producing the most command-shaped output of any of them |
| `resume-handoff` | A pack that needs a separate handoff artifact is a pack failing at its stated purpose. Baseline Docs exists so another conversation or agent can resume without chat history, so the pack is the handoff and a fresh thread with `onboard` is how it gets read |

**What breaks if ignored.** Each retained skill is a description competing for selection against a neighbour that answers the same question better, which is what the fragmentation problem is made of.

**Rejected: keep `resume-handoff` for the reader who will not run an agent at all.** The only skill in the family whose output was meant to leave the thread, which is a real distinction. Rejected because the only rule it carried that an agent would not have followed anyway was a single line about linking wiki guidance rather than copying it, and a skill that exists to carry one line still spends a whole description competing for selection.

**What remains is one owner per question.** `brief` answers where the work stands, `onboard` loads the pack, `save` writes the delta down, and `maintain-compact` cleans the pack up.

## FD-D21: what an active document keeps as evidence, and what it drops

**Decided.** The standard itself lives in `contract/pack-contract.md` under `Evidence density`: a keep list, a discard list, the distinction between a resolved mistake and a routine failed attempt, and the permission to link an external log rather than paste it. FD-D29 put it there. This entry holds the reasoning and deliberately carries no second copy of the rule.

**Why two lists rather than one instruction.** "Record what matters" is not a test an agent can fail, so it authorizes whatever the agent already wanted to do. Two lists make the boundary something a reader can point at, and the cases on each side were drawn from real packs rather than invented.

**Why the lesson entry is on the keep list.** It is the one item whose value survives its own resolution. Everything else on the keep list is kept because it is still live; a lesson entry is kept precisely because it is finished, since what it prevents is the same mistake being made again by someone who cannot see it was already made once.

**Why the external-log permission is stated at all, rather than left implied.** A rule made only of prohibitions gets read as a prohibition on everything nearby. Without the permission, an agent facing a large log has two visible options, paste it or drop it, and both are wrong. Naming the third option is what makes it reachable.

**What breaks if ignored.** Read one way the pack becomes a command transcript nobody can resume from. Read the other way it loses the record of why a design changed, and the change gets undone by someone who cannot see what it cost to arrive at.

## FD-D22: `useguide` means a consumer contract

**Decided.** The definition, its five valid forms, and the rule sending a cross-task procedure to the wiki live in `contract/pack-contract.md` under `Conditional documents`. FD-D29 put them there. This entry holds the reasoning and carries no second copy of the rule.

**Why the file needs a definition rather than a name.** `useguide` reads like "documentation about using this", which is true of half a pack. Without a stated meaning it becomes a second `sourcecode` written for nobody, or the place content lands when the author is unsure where else it goes. Naming a consumer is what makes the inclusion test answerable: either something outside the pack depends on the behavior or nothing does.

**Why the wiki rule sits beside it rather than somewhere else.** The two are the same question asked twice. A procedure that applies across tasks passes the "someone outside depends on this" test, so a reader applying the inclusion criterion alone would put it in `useguide` and be wrong. The wiki rule is what stops that, and it only works if it is read at the same moment as the criterion it corrects.

**What breaks if ignored.** A `useguide` with no consumer is filler by another name, which is exactly the cost FD-D2 removed by making the file conditional. A reusable procedure buried in a task-specific pack is worse than filler: it is written, correct, and unreachable from the next task that needs it.

## FD-D23: `run` has no silent execution-policy defaults

**Decided.** Before implementation, `baselinedocs-run` asks for any missing `approval_policy` and `commit_policy`. Selecting `per-phase` in the user's reply is explicit commit authorization for that run, and for that run only. Policy is never inferred from an earlier turn.

**Why.** Both policies control something the user cannot undo cheaply. A silent default on `approval_policy` means an agent runs a whole roadmap unattended when the user expected to review each phase; a silent default on `commit_policy` means commits appear in the user's history that they never authorized.

**What breaks if ignored.** An unauthorized commit is the failure with no cheap reversal, and it is the one a default would produce most quietly.

**Related rule on post-initial feedback.** Feedback after initial completion is assigned to the phase whose acceptance criteria it refines, reopening that phase if needed. A new phase requires a new outcome, dependency, release gate, deployable unit, or independently reviewable body of work. Without that test every correction becomes a phase, and the roadmap turns into a change log.

## FD-D24: an initiative index is routing metadata and nothing else

**Decided.** For work spanning dependent domains, every domain pack stays first-class and the initiative gains an index holding direct child links, domain scope, dependency edges, and the current cross-pack checkpoint. It is not a general introduction or roadmap that duplicates child content.

**Why.** Keeping every sub-pack directly queryable is what makes the initiative navigable at all. An index that summarized child content would become a fourth core document per initiative, and the summary would drift from the pack it summarizes.

**What breaks if ignored.** A general parent pack hides its children, so a reader loads the parent, gets a summary, and never reaches the pack that holds the detail. That is the failure this shape exists to prevent.

## FD-D25: this pack carries no `useguide`

**Decided.** `family-design` ships `introduction`, `roadmap`, `hallucination`, and `sourcecode`. No `useguide`.

**Why.** The consumer of this family is a user of the skills, and `README.md` is already the surface written for them, with the workflow, the entrypoint table, the pack contract summary, and the hook instructions. A `useguide` here would restate the README in a file that ships nowhere and that no installed agent can open.

**What breaks if ignored.** Two descriptions of the same workflow, one of which is never read, so the unread one drifts and the next author corrects the wrong copy.

## FD-D26: no blind semantic writing from a transcript or repository-wide candidates

**Decided.** An agent may checkpoint only a pack unambiguously established in its current thread. Writing a checkpoint by scanning the repository for roadmap candidates, or by reconstructing state from a transcript, stays rejected.

**Why.** It is the same argument as FD-D6 applied to the agent rather than to the hook. Repository state does not identify ownership, and a shared working tree may hold another thread's changes.

**What breaks if ignored.** The write lands in a pack that did not ask for it, attributing work to the wrong initiative, and the error is invisible until someone reads that pack expecting their own state.

## FD-D27: this pack replaces `DESIGN.md`, which is deleted once the handover is complete

**Decided, and carried out.** `family-design` and `skill-consolidation` together are the canonical record of the family design. `DESIGN.md` was superseded and then deleted, in FD-P4 on 2026-08-28, rather than kept as a second view. A design decision is written into a pack. The file remains recoverable at `git show 0cb913f:DESIGN.md`, which is the safety net that made an irreversible-looking act reversible in practice, and it is not a reason to relax the coverage check that preceded it: a file recoverable only by someone who knows it existed is not a source anyone will find.

**Why.** Keeping both would create two decision logs for one design, and nothing could pin them to each other: they are different texts by design, so no byte-comparison applies, which is the same unverifiable duplication the entry-index rule accepts only because a row is a locator rather than a source. This repository's own standard, that a rule is stated in exactly one place, is FD-D7 applied to instructions; applying it to design rationale is the same argument one level up.

**What breaks if ignored.** The next design change is written into one of the two and not the other, and there is no test, no gate, and no reader who sees both in the same pass. The copies then disagree about why a rule exists, which is worse than either copy alone, because a reader who finds the disagreement cannot tell which side is current.

**What had to be true before the file was deleted.** All four, and none was optional. All four are met, and the deletion landed in FD-P4 on 2026-08-28.

| Prerequisite | State |
|---|---|
| every fact in `DESIGN.md` is reachable in a pack | done in FD-P2. Verified fact by fact, not assumed from the ledger. FD-D28 records what that check found |
| `AGENTS.md` stops naming `DESIGN.md` as the place to record a decision | done in FD-P3. The ships table, the rule against citing a non-shipping file to justify cutting a `SKILL.md`, and `Where reasoning goes` now name `docs/baseline/` and say which pack owns what |
| the `Skill Consolidation` pointer resolves to the pack instead | done in FD-P3. `AGENTS.md` sends a contributor to `skill-consolidation.hallucination.md` SC-D1, which holds the merge test and both rejected alternatives in fuller form than the section it replaced |
| no other file in the repository depends on it | done. No file outside `docs/baseline/` names `DESIGN.md`, and the references inside `docs/baseline/` are adoption provenance, which stays correct after the file is gone |

**Why the file is not deleted in the same breath as the decision.** Deleting it now would leave `AGENTS.md` pointing four times at a file that does not exist, which is a worse state than the duplication being removed. The order is: close the coverage gaps, rewire `AGENTS.md`, then delete.

**Rejected: keep `DESIGN.md` canonical and treat this pack as a read-optimized view.** It costs no `AGENTS.md` edit and it is the cheapest option today. Rejected because every future design change then has to be written twice, and nothing detects the occasion when it is not.

**Rejected: keep both and record which one wins on a disagreement.** Honest, and it removes the ambiguity without removing the duplication. Rejected because a tie-break rule is only consulted by a reader who already noticed the disagreement, and the expensive case is the reader who does not.

## FD-D28: a coverage ledger routed seven sections to another pack without checking that pack carried them

**What was believed.** The adoption's coverage ledger routed seven of `DESIGN.md`'s twenty-two sections to `skill-consolidation` rather than restating them here, on the grounds that the other pack already recorded those decisions in fuller form. The ledger was written from a full read of both documents, and the routing was correct at section granularity.

**What disproved it.** The decision to delete `DESIGN.md` raised the standard from "the other pack covers this subject" to "the other pack carries every fact". Checking fact by fact found two that no pack held: the argument that Terraform separating `plan` from `apply` is the same shape of argument for keeping the detect skill separate from the repair skill, and the entry index's break-even point of about five percent of entries deferred together with its projected saving of near 35,000 tokens per load on a 342 KB journal.

**Why it looked reasonable.** Both packs discuss the same decisions, and `skill-consolidation`'s versions are longer, carry measured numbers, and record rejected alternatives that `DESIGN.md` only summarizes. A longer treatment of the same subject reads as a superset, and for five of the seven sections it was one. It is not one by construction: a summary written later can carry a supporting argument the earlier full version never had.

**The fix.** Both facts were added to the entries that own them, `skill-consolidation` SC-D12 for the Terraform comparison and SC-D19 for the break-even arithmetic. The check itself is now the first prerequisite in FD-D27, because a ledger row is a routing claim and a routing claim is not evidence of coverage.

**The class, which outlives this incident.** It is the same shape as the failure SC-D21 in `skill-consolidation` records about the contract heading: every available signal agreed, and none of them measured the thing that mattered. There the signals compared copies and could not see a defect in what they agreed about. Here the ledger compared subjects and could not see a fact missing inside a subject both packs discuss. A mapping is not a comparison, and a coverage claim that has not been checked at the granularity of the thing being lost is an assertion, not a result.

**What breaks if this entry is dropped.** The next adoption that routes a section to an existing pack writes the ledger row and stops there, and the deletion that follows it takes the unchecked facts with it. That deletion is unrecoverable in a way a wrong ledger row is not.

## FD-D29: the contract absorbs the retention and `useguide` detail in full, closing FD-Q3

**Decided.** `contract/pack-contract.md` carries the whole retention standard and the whole `useguide` definition, not a summary of either. Added: the keep list of five items and the discard list of four, the sentence separating a resolved mistake from a routine failed attempt, the permission to link an external raw log rather than paste it, the five valid `useguide` forms, and the rule sending a cross-task procedure to `docs/wiki/<topic>.md`. All 11 packaged copies were re-synced. FD-D21 and FD-D22 were then reduced to reasoning, so each rule is stated once.

**Why.** The detail existed only in files that do not ship. An agent writing a pack reads its own `references/pack-contract.md` and cannot open `DESIGN.md`, this pack, or `README.md`, so every sentence living outside the contract guided a human and nobody else. Two of those sentences are not derivable from what the contract did say: that an external log may be linked rather than pasted, and that a cross-task procedure goes to the wiki instead of into `useguide`. Both are permissions or routing, and no agent infers a permission from a list of prohibitions.

**What breaks if ignored.** The design and the shipped rule drift, and the drift is invisible because no test compares prose in one file against prose in another. Two concrete failures were already reachable: an agent holding a large log saw only paste-it or drop-it, and an agent holding a reusable procedure had an inclusion criterion that actively pointed it at the wrong file, because a cross-task procedure does satisfy "a consumer outside this pack depends on it".

**Accepted cost, and it is real.** The contract went from 108 lines to 129, and it is loaded on every invocation of 11 skills. That is paid on every run, forever, in exchange for behavior that is correct rather than merely documented somewhere.

**Rejected: ship only the two sentences an agent cannot derive.** The recommendation that was on the table, and cheaper by about 18 lines per run. Rejected by the user in favour of the full text, and the argument against the cheap option is that "derivable" is a judgement made by whoever writes the contract, not by the agent reading it. The keep and discard lists are what make the boundary checkable; an agent asked to derive them derives them differently each time.

**Rejected: leave the contract terse and keep the detail as design rationale.** It holds the per-run cost exactly where it was. Rejected because it holds the failure there too: rationale no agent can open does not change what any agent does.

**The order this had to follow.** Widen the canonical file, re-copy it to all 11 packaged copies, verify byte-identity, and only then remove the duplicate text from FD-D21 and FD-D22. Deleting first drops the rule for as long as it takes to notice, which is the sequencing `skill-consolidation` SC-D10 recorded when the same problem arose there.

## FD-D30: every identifier carries its pack prefix, closing FD-Q4

**Decided.** Every entry, question, and phase identifier in this initiative is written with its pack's prefix, everywhere: `FD-` for `family-design`, `SC-` for `skill-consolidation`. The prefix is part of the identifier, not a qualifier added when citing across packs. `FD-D16` and `SC-D16` are the names themselves, in headings, in entry index rows, in roadmap Basis columns, and in every reference inside or outside the pack.

**Why.** Two packs numbering independently made `D16` name two different entries, and a reader could not see the ambiguity, because `D16` resolves in whichever pack they happen to be reading. That is the expensive kind of ambiguity: not a reference that fails, but one that succeeds and returns the wrong entry.

**What breaks if ignored.** A cross-pack citation silently resolves to the neighbouring pack's entry of the same number. Nothing reports it, no test can see it, and the reader has no signal that they are looking at the wrong text. Adding a third pack multiplies the collisions rather than adding to them.

**What it costs.** Three characters on every identifier, in a repository where identifiers are cited constantly, and a one-time rewrite: 34 identifiers in this pack and 43 in `skill-consolidation`, with every reference to them across nine documents. Any reference written before this decision, in a commit message or an earlier thread, now names an identifier that no longer exists. That is the good failure mode: it fails loudly, which is the property the rejected qualifier convention lacks.

**Rejected: qualify only when citing across packs, as in `skill-consolidation` D16.** The convention this initiative ran on for one day, and it changes no file. Rejected because it fails silently in exactly the case it exists for: an author who forgets the qualifier produces a citation that still resolves, to the wrong entry, and neither the author nor the reader gets a signal. A rule enforced only by memory is not enforced in a repository whose whole premise is that memory is what fails.

**Rejected: one counter running across the whole initiative, so this pack would start at D22.** Unambiguous with no prefix at all, and the shortest identifiers of the three options. Rejected because a pack's numbering would then depend on which other packs exist: adding a pack, or splitting one, forces a renumber somewhere, and a renumbered identifier is the silent-failure case again. Numbers must be a property of the pack that owns them.

**What this settles in `skill-consolidation` SC-Q6, and what it does not.** SC-Q6 asks what the identifier scheme is and whether the contract should own it, and it proposes flat, append-only, per-kind counters unique across the pack. This decision amends one clause of that proposal, replacing "unique across the pack" with "unique across the initiative, by carrying the pack prefix". Everything else in SC-Q6 stays open: the per-kind letters, the ban on encoding hierarchy in a name, the ban on sub-identifiers, and whether the contract should state any of it. `contract/pack-contract.md` is deliberately unchanged by this decision, because the contract owning the scheme is the half SC-Q6 still owns.

## Open questions

### FD-Q1: can internal helpers be hidden at package level?

Package-level installation profiles would hide the lifecycle skills more completely than the naming prefix and the Codex-only policy field manage today. Deferred because Skills.sh does not currently provide a portable hidden-skill category, so there is nothing to build against.

The trigger to reopen: a portable hidden-skill or profile mechanism appearing in the installer or in the Agent Skills format. Until then FD-D1's progressive disclosure is the whole mechanism, and the design says so rather than implying the split is enforced everywhere.

### FD-Q2: can hooks be rolled out across an organization?

`baselinedocs-setup-hooks` handles one repository at a time and preserves unknown configuration rather than replacing it. An organization-wide rollout remains deferred.

What makes it more than a loop over repositories: the installer merges into each host's existing configuration, and the safety property that matters is preserving what it did not write. A rollout mechanism has to hold that property across repositories whose hook configuration nobody has inspected, which is a different problem from installing into one repository a user is looking at.

FD-Q3 closed in FD-D29, FD-Q4 closed in FD-D30. Stated here rather than deleted, so a reader can tell each was settled by a decision rather than dropped. Neither question's analysis was lost with its heading: both sit inside the decision that closed them.
