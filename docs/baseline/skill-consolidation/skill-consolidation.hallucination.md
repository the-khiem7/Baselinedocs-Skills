---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "hallucination"
status: "complete"
updated: "2026-08-27"
code_ref: "c6eb29a"
---

# Skill Consolidation: Decisions and Open Questions

## D1: merge criterion is a two-condition test

**Decided.** Two skills merge only when both hold: their trigger space overlaps in a way that survives a good-faith rewrite of both descriptions, and their bodies produce the same post-state.

**Why.** The first condition needs the rewrite clause or the criterion fires on a description defect. `audit-drift` and `audit-verify` read as near-synonyms today, but that overlap is sloppy wording, not shared identity, and renaming separates them. `sync-decision` and `sync-decisions` cannot be separated by any rewrite, because "one specific closed decision" sits literally inside "one or more". Nested concepts merge; nested wording gets rewritten.

**What breaks if ignored.** Without the rewrite clause, any two carelessly described skills look mergeable, and a real distinction gets destroyed to fix a text problem. Without the post-state condition, a read-only reporter gets merged into a writer, erasing a safety boundary the user can see.

**Rejected: pointer reachability.** `DESIGN.md` previously held that a skill absent from the documented workflow should be reached by a pointer rather than by competing for a description match. Rejected because description match is a first-class host selection mechanism, not a fallback, while pointer reachability is a convention local to this repository. It measures only whether some other skill's prose happens to name the skill, which is an artifact of who wrote what. `extract-wiki` is the counterexample: nothing points at it, and no other skill contests its trigger vocabulary. Under the rejected criterion it looked endangered; under D1 it is one of the healthiest skills present. The pointer observation keeps one narrow use, as a signal that a pointer is missing, never that a skill is unnecessary.

**Rejected: merging by family prefix.** Grouping the sync, audit, and maintain families into one skill each was proposed and rejected. A prefix is a naming artifact, not a property of the operation. `maintain-split` produces new packs plus an index; `maintain-archive` relocates content and sets a status `onboard` depends on. Neither shares a post-state with `maintain-compact`, so neither satisfies D1.

## D2: sync-decision merges into sync-decisions

**Decided.** Delete `baselinedocs-sync-decision`. Its scope constraint, that only directly impacted sections are patched with no broad unrelated rewrites, becomes a rule in `baselinedocs-sync-decisions`.

**Why.** The descriptions are strictly nested and the post-states are identical: patch the affected sections, refresh frontmatter in the documents that changed. No situation exists in which an agent should load one and not the other.

**What breaks if ignored.** Selection is undecidable. An agent holding one closed decision matches both descriptions, and "one or more" includes one.

**Rejected name: `baselinedocs-sync`.** `sync-codebase` and `sync-reconcile` remain separate skills, so a bare `sync` name would attract every request to sync docs against code through the name alone, recreating the undecidability being removed. The deferred detect/repair research may also need that namespace for the code-sync skill.

## D3: the audit pair stays separate, audit-verify is renamed

**Decided.** Keep both. Rename `baselinedocs-audit-verify` to `baselinedocs-audit-claims`. Rewrite both descriptions on the axis that separates them.

**Why.** They differ by unit of analysis, and the two questions are independent.

| Skill | Unit | Question | Driven by |
|---|---|---|---|
| `audit-drift` | document | is this document behind the code? | provenance, `code_ref` against current state |
| `audit-claims` | claim | is this statement supported by evidence? | evidence quality, no provenance |

A document with a current `code_ref` can still be full of claims that were never true; those did not go stale. A document stale by provenance can hold claims that are all still accurate.

**What breaks if ignored.** Merging folds a provenance-free question into a provenance-driven one, so a claim that was never supported gets reported as stale, which points the reader at the wrong repair. `audit-drift` keeps its name because "drift" is precise and both `onboard` and `brief` name it in shipped text.

**Rejected: merging the pair.** Recommended earlier on the strength of near-identical descriptions, then withdrawn. That overlap is exactly the description defect D1's rewrite clause exists to exclude.

## D4: maintain-prune is deprecated

**Decided.** Delete `baselinedocs-maintain-prune`.

**Why.** `hallucination` is a journal. It has to keep rejected options and failed approaches so a later agent does not repeat a defeated approach. Prune's success test is "is this still relevant?", and on a journal that test returns remove for exactly the content the journal exists to hold: a rejected alternative is obsolete by construction, because it was rejected, and a closed question reads as resolved and therefore removable.

The lesson-entry exception already in the skill body does not patch this. The conflict is with the operation's success test, not with its edge-case list, and the exception covers only content written in the shape of a lesson entry. A rejected alternative or a closed question written any other way is unprotected.

**What breaks if ignored.** The journal erodes one prune pass at a time, and agents repeat mistakes the pack once recorded. That is the failure the journal exists to prevent, so a skill whose success test attacks it cannot be kept behind an exception clause.

**Consequence requiring D5.** Prune served one legitimate case that now needs an owner: a disproven assumption still asserted as current truth in `introduction`.

## D5: a disproven claim is relocated, not deleted

**Decided.** A claim disproven by code or closed by a decision moves into `hallucination` as a closed entry recording what was believed and what disproved it. The document whose role is current truth stops asserting it. The claim is never deleted. Owners: `sync-codebase` when code disproved it, `sync-decisions` when a decision closed it, `save` when the thread established it. The rule goes into `contract/pack-contract.md`, which every pack-writing skill already reads.

**Why.** This keeps the journal complete while removing the false current-truth claim, which is what prune was reached for.

**What breaks if ignored.** Deleting prune with no replacement leaves a misleading claim with no owner, and the gap gets closed later by re-adding prune, reversing D4.

## D6: maintain-archive is kept, with a defined destination

**Decided.** Keep the skill. Specify its destination path and naming convention in its body.

**Why.** It is not only a status flag. Three of its four steps relocate content: identify completed sections, preserve them in an archive-friendly form, clean the active pack. But the body never says where the archive goes, so what it produces has never been settled. That exact defect is on record in `DESIGN.md` as the reason `resume-snapshot` was deleted, which makes it a known-fatal gap rather than an untidy one.

**What breaks if ignored.** Two runs archive to two different places, and `onboard`, which excludes archived material from its default scope, cannot predict what it is excluding. `maintain-archive` is also the only producer of `status: archived` and `onboard` its only consumer, so the exclusion rule dies with the skill.

**Rejected: deprecate archive and give the relocation right to compact.** Relocation is legal under compact's information-preservation gate, since moving a completed phase into a linked file leaves the active document shorter with nothing lost, so this alternative was real. Rejected because it gives `maintain-compact` two mechanisms and an escape hatch from its own revert gate: an agent unable to compress far enough could relocate content instead, satisfying "shorter" without doing the work the gate asks for. Cost accepted in exchange: one more skill in a family being trimmed.

## D7: compact carries an explicit revert gate

**Decided.** `maintain-compact` succeeds only when the document is shorter and its informational performance is unchanged. If any detail is lost, or a passage becomes open to more than one reading, revert. A long file costs less than hallucination from a short one.

**Why.** An agent compacting always has a reason to cut one more line, and the cut always looks locally harmless. Without the cost comparison stated in the body, the gate reads as advice.

**What breaks if ignored.** A pack that reads shorter and answers wrong, which is more expensive than the length it saved.

## D8: removal is a direct delete

**Decided.** Delete removed skill folders outright. No stub, no deprecation shim.

**Known cost, accepted.** Skills install one folder at a time and users delete manually, so a `baselinedocs-sync-decision` already installed on someone's machine stays there and keeps competing for selection. Deleting from this repository cannot reach it.

**Rejected: a one-version stub.** A stub whose description redirects to the merged skill is the only thing that could reach an already-installed machine. Rejected in favor of a clean tree.

## D9: description sharpening is a separate batch

**Decided.** Rewriting descriptions for pairs that share triggers but differ in outcome is its own batch, not part of this one. The audit rename in D3 is excluded from that split, because a rename cannot be done without writing the new description.

## D10: the remaining duplicate rule statements are removed inside P6

**Decided.** The two further wordings of the lesson-entry rule, in `baselinedocs-run/references/execution-contract.md` and `baselinedocs-save/SKILL.md`, are removed as part of P6 rather than in a phase of their own.

**Why.** Both are one sentence in one file, and P6 is already the phase that makes the repository's written rules agree with each other.

**What breaks if ignored.** A rule stated three times in three wordings drifts on the next edit, and `test_references.py` cannot see it: that test only compares contract copies against the canonical file, so a fourth paraphrase written somewhere else passes.

**Rejected: a separate P7.** It would have given the removal its own verification step, and mixing skill-body edits into a documentation phase does put two kinds of change in one place. Rejected as too small a scope to justify the phase.

**Order, carried from D7's execution.** Both duplicates state one thing the canonical sentence does not: a lesson entry stays even after the mistake is resolved. Widen the canonical sentence to cover that, re-copy it, and only then delete the two. Deleting first drops the rule for as long as it takes to notice.

## D11: maintain-archive is deleted, reversing D6

**Decided.** Delete `baselinedocs-maintain-archive`. Remove `archived` from the `status` enum in `contract/pack-contract.md`, remove `onboard`'s archived-material exclusion rule, and replace `maintain-compact`'s `not for archiving completed phases` non-goal with a direct prohibition on moving content out of the active pack. Closes Q1.

**Why.** D6 kept the skill on condition that its destination be specified. Specifying it forced the prior question of what may be moved, and the answer left almost nothing.

| Document | Archivable | Reason |
|---|---|---|
| `hallucination` | no | the journal. Moving it outside `onboard`'s default scope reproduces the failure D4 deleted `maintain-prune` for: content a fresh agent cannot reach by default is, for that agent, content that was removed |
| `introduction`, `sourcecode`, `useguide` | no | current state, not history |
| `roadmap` | completed phase history only | and the contract already keeps reasoning out of a checkpoint, so what is movable is evidence tables and affected-file lists |

The flag does not survive either. `onboard` excludes by document, while every proposal for `status: archived` was a per-section marker, so a marked section inside an active document is still read in full and the exclusion does nothing.

**What breaks if ignored.** Keeping the enum value with no producer and no consumer leaves an affordance that invites the next contributor to supply the missing producer, which is how a deleted skill returns. Keeping the skill with an unspecified destination leaves two runs archiving to two different places, which is the defect that deleted `resume-snapshot`.

**Accepted cost.** A long-running single-domain pack now has no way to shed history. `maintain-compact` cannot, because D7's gate forbids losing detail, and its "low-value" wording, the phrase an agent used to cut old phase narration, was removed in the same round. `maintain-split` divides by domain, and a one-domain pack has nothing to divide. Onboard cost for such a pack grows monotonically and nothing mitigates it.

**Supersedes one constraint.** The introduction recorded that the frontmatter schema must not change and that `status: archived` stays in the enum, carried from the original instruction. That constraint was set while D6 held. Removing the value is a deliberate exception to it, not an oversight; the rest of the schema is untouched.

**Rejected: keep archive and specify `<pack>/archive/`.** One file per archived phase, `status: archived` frontmatter, linked from the active roadmap, with archiving forbidden on `hallucination` and a promote-the-reasoning-first step before any relocation. Coherent, and it is the only option that closes the accepted cost above. Rejected because the operation it protects is thin once `hallucination` is excluded, and because no skill routes to it, so it fires only when a user remembers a maintenance chore.

**Rejected: move the flag into the write-able skills and drop relocation.** The first proposal on the table. It collapses: with relocation gone the flag is only ever a per-section marker, and `onboard` excludes by document, so the marker is inert. It would have retired the skill while appearing to keep the feature.

**D1 and D6 are left as written.** Both cite `maintain-archive` as a live skill, D1 using it as an example of a post-state `maintain-compact` does not share. That is what was argued at the time and the journal keeps it. Read those two entries as history; D11 is the current position. `DESIGN.md` carries the corrected version, because it states current design rather than recording a sequence.

## D12: the sync and audit skills all stay, and the matrix that questioned them was wrong

**Decided.** Keep all five. Merge nothing, add nothing, rename nothing. Replace the detect/repair matrix in this pack and in `DESIGN.md` with the model below. Closes Q3, and closes the namespace half of Q2.

**Why the old model was wrong.** It assumed four distinct comparison scopes. The bodies say otherwise: `audit-drift` compares code changes, document claims and decision records; `audit-claims` compares each claim against code and explicit decisions; `sync-reconcile` prefers code evidence and explicit user decisions to break a tie. Three of five consult the same two sources, so scope does not separate them, and a matrix on that axis reports holes that are artifacts of the axis.

**The two real axes.**

| Group | Separated by | Members |
|---|---|---|
| report-only | unit of analysis | `audit-drift` document, `audit-claims` claim |
| writes | trigger event, which fixes blast radius | `sync-codebase` whole pack, `sync-decisions` only sections the decision reaches, `sync-reconcile` only conflicting sections |

**Why each empty cell stays empty.** Different reason per cell, which is itself the evidence that the matrix was not describing one phenomenon.

| Cell | Verdict |
|---|---|
| repair for claim against evidence | occupied by the contract. D5 names three owners. A skill here is a fourth owner of a rule that names three |
| detect for pack against itself | occupied by `onboard` and `brief`, which report contradictions and route to `sync-reconcile` without repairing. A separate skill serves only "show contradictions without loading the pack", which nothing has asked for |
| detect for decision against pack | occupied by `audit-drift` step 2, which already compares decision records |

**What breaks if ignored.** Completing the matrix adds up to three skills to a family being trimmed, and each would either duplicate a contract rule or claim work an existing skill already does. Collapsing it costs the cheap screen, below.

**Rejected: one skill per comparison scope, detect as a report-only mode.** Rejected on cost asymmetry, a stronger objection than the boundary-visibility one recorded when Q3 was framed. `audit-drift` is doc-first: read frontmatter, narrow, then compare scoped code changes. `sync-codebase` is code-first and unscoped, opening with "inspect the codebase first". Report-only mode on the merged skill still pays the full inspection cost, so the family trades a cheap screen plus an expensive fix for one expensive skill with a flag, and the screen is the half used most often.

**Rejected: complete the matrix.** See the cell table above. A matrix with holes is a diagnostic, not a specification, and this one was drawn on the wrong axis.

**Consequence for D2.** `baselinedocs-sync` is not needed as a namespace, because no merge happens. `sync-decisions` keeps its longer name for the original reason: a bare `sync` would attract every code-sync request through the name alone.

## D13: the rename sweep stops at the audit pair, closing Q2

**Decided.** No skill outside D3's rename is renamed. `sync-reconcile` keeps its name. Closes Q2.

**Why.** Three findings, in increasing weight.

The name is not the surface that selects this skill. Both `onboard` and `brief` name `baselinedocs-sync-reconcile` in shipped text, and each does so at the moment a contradiction is found, which is exactly when the choice is made. Routing already works without the name carrying its object, so a rename would pay for an improvement to a surface that is not the main entry path.

The family has no single naming convention to conform to. `sync-codebase` names the source of truth it compares against; `sync-decisions` names the thing it propagates. Two skills already considered direct, two different patterns. "Name the object" therefore has no one target here, and `sync-contradictions`, the best candidate, would parallel one of them while diverging from the other.

The cost is higher than D8 recorded, measured in P8. A machine carries several independent host skill directories, four on this one, each a real copy rather than a link into a shared store, and the installer adds and overwrites but never removes. A rename leaves the old name in every one of them until someone deletes it by hand.

**What breaks if ignored.** Renaming on a naming principle the family does not consistently follow buys a marginal clarity gain and pays it in stale duplicate skills competing for selection on every installed machine.

**Rejected: rename to `sync-contradictions`.** The strongest candidate, and it does name the object. Rejected on the three findings above rather than on the name itself, which is a better name than the one being kept.

**What the question retains.** The naming principle from D3 stands for any *new* skill: name what it operates on. D13 declines a retroactive sweep, not the principle.

## D14: no pack-level finished marker, closing Q4

**Decided.** Do not re-add a `status` value for a finished or parked pack, and do not give `onboard` a status-based scope filter. Closes Q4.

**Why.** The function already exists one layer up. `onboard` does not scan for packs, it is pointed at one, and on an initiative its step 2 reads the index and stops, then step 3 selects the scope when the routing evidence names exactly one sub-pack **in progress**. That phrase is already the filter Q4 proposed to add: a finished pack is not selected, because it is not in progress. Adding a frontmatter value would restate a routing rule as data.

`status: complete` cannot serve the purpose either, and the reason is worth keeping. This pack is `complete` and is precisely what a contributor must read before touching any skill folder, since D1 through D14 are the whole argument for the shape every current skill has. A rule that skipped complete packs would skip the most load-bearing document in the repository. So a finished marker would have to be a value distinct from `complete`, which makes it a schema change rather than a reuse.

**What breaks if ignored.** It would be `onboard`'s first status-based scope filter after P5 deleted the only one, rebuilding the mechanism just removed to obtain a behavior the routing rule already provides. The orphaned-affordance failure in D11 is the same shape.

**Rejected: add a `parked` or `archived` value with `onboard` as its consumer.** Coherent, and unlike the value D11 deleted it would operate at file granularity, so the mechanism would work. Rejected because no initiative index exists yet, so the payoff is zero today, and because step 3 already declines to load what is not in progress.

**If this is reopened.** The trigger to watch for is a real multi-pack initiative where the index's own status proves insufficient for routing. That is the evidence D14 lacks, not an argument it lost.

## D15: the installed generation gap is closed, and the constraint asserting it is disproven

**What was believed.** The introduction carried a constraint stating that the skills installed on this machine were an older generation than this repository: the installed `baselinedocs-init` still routed to a `resume` family and shipped a 44-line contract against this repository's then-74-line canonical file. The operational conclusion drawn from it was that a `baselinedocs` skill invoked in a later thread would read a stale copy.

**What disproved it.** P8 deleted every `baselinedocs-*` folder from each host directory and installed from this clone. Re-measured at `c6eb29a`: each of `.claude`, `.agents`, `.kilocode`, and `.kiro` holds exactly the 15 skills this repository defines, every packaged `references/pack-contract.md` in all four is `cmp`-identical to the 82-line canonical file, and the installed `baselinedocs-init` contains no occurrence of "resume" at all. `.codex/skills` exists and holds no baselinedocs skill, as it did before.

**What survives it.** The mechanism, not the measurement. An installed skill reads its own copy, so an install is a snapshot and this repository drifts from any machine from the next edit onward. The introduction keeps that as a constraint and the roadmap keeps the returning-risk row. Only the claim that this machine is currently behind is withdrawn.

**Unresolved, and now unresolvable.** Two figures exist for the pre-P8 installed contract: 44 lines in the introduction's constraint, measured against `baselinedocs-init` when that constraint was written, and 46 lines in P8's checkpoint, measured across the installed set at delete time. The state both describe has been overwritten, so neither can be re-checked. Both are kept as recorded rather than reconciled to one number, because choosing between them would invent a measurement. The likeliest explanation, if it ever matters: the host directories are independent copies and may simply have held different generations.

**What breaks if this entry is dropped.** The next reader finds a constraint saying installs are snapshots, with no record that the gap was ever real or ever closed, and re-runs P8's delete-and-reinstall against a machine that already matches. P8's own finding is why the record is worth keeping: the installed set was worse than the constraint described, missing three of the six user entrypoints, so the constraint understated a real problem rather than inventing one.

## Open questions

None. Q1 closed in D11, Q3 in D12, Q2 in D13, Q4 in D14. Stated rather than deleted so a reader can tell the section was emptied deliberately.
