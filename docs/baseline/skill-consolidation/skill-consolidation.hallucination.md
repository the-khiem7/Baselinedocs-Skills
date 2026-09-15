---
baseline_schema: "2.0"
pack: "skill-consolidation"
document: "hallucination"
status: "active"
updated: "2026-09-11"
code_ref: "uncommitted"
---

# Skill Consolidation: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more: never its reasoning, never its outcome's justification, never a summary that could be mistaken for the entry itself. That restraint is the whole point, because a row that carried reasoning would be a second copy of the entry and the two would drift. An answer that turns on an entry whose full text was not read is unbacked, and must be reported that way rather than derived from a row.

Required by `contract/pack-contract.md` once a journal passes its threshold. SC-D19 records why, and this document is the first to carry one.

| Entry | About | Status | Related |
|---|---|---|---|
| SC-D1 | the two-condition test that decides whether two skills merge | current | SC-D6, SC-D12 |
| SC-D2 | folding `sync-decision` into `sync-decisions` | done in SC-P1 | SC-D1 |
| SC-D3 | keeping the audit pair separate and renaming `audit-verify` | done in SC-P3 | SC-D1, SC-D12, SC-D13 |
| SC-D4 | deleting `maintain-prune` | done in SC-P2 | SC-D5 |
| SC-D5 | where a disproven claim goes instead of being deleted | current, lives in the contract | SC-D4, SC-D15 |
| SC-D6 | keeping `maintain-archive` with a specified destination | **reversed by SC-D11**, kept as history | SC-D11 |
| SC-D7 | the pass-or-revert gate on `maintain-compact` | done in SC-P4 | SC-D11, SC-Q7 |
| SC-D8 | deleting a skill folder outright instead of leaving a stub | current | SC-D15 |
| SC-D9 | treating description sharpening as its own batch | closed empty | SC-D12 |
| SC-D10 | removing the last duplicate rule statements inside SC-P6 | done in SC-P6 | SC-D7 |
| SC-D11 | deleting `maintain-archive`, its enum value, and its consumer | current | SC-D6, SC-D7, SC-Q7 |
| SC-D12 | keeping all five sync and audit skills, and the axis the old matrix got wrong | current | SC-D3, SC-D20 |
| SC-D13 | stopping the rename sweep at the audit pair | current | SC-D3 |
| SC-D14 | declining a pack-level finished marker | current | - |
| SC-D15 | the installed generation gap, and the constraint that asserted it | current | SC-D8 |
| SC-D16 | shipping the contract on a full read rather than on writing | current | SC-D12, SC-D17, SC-D20 |
| SC-D17 | shipping report style as its own asset, separate from the contract | current | SC-D16 |
| SC-D18 | forbidding hard-wrapped paragraphs in pack documents | current | SC-Q7 |
| SC-D19 | putting the entry index into the contract as a conditional section | current | SC-D5, SC-D6, SC-D20, SC-Q7 |
| SC-D20 | who repairs content that is true but sits in the wrong document, closing SC-Q5 | current | SC-D5, SC-D12, SC-D16 |
| SC-D21 | an edit to the contract destroyed a section heading, and every test stayed green | current, repaired | SC-D5, SC-D19 |
| SC-D22 | deleting setup-hooks and removing the report-style exemption | current | SC-D1, SC-D8, SC-D17 |
| SC-Q6 | what the element identifier scheme is, and whether the contract owns it | open, except the uniqueness clause settled by `family-design` FD-D30 | SC-Q7, SC-Q8, SC-D19 |
| SC-Q7 | what `onboard` does with the index, now that the index itself is decided | open, narrowed by SC-D19 | SC-D19, SC-D7, SC-D11 |
| SC-Q8 | the label standard inside an entry, and how many entry kinds `hallucination` holds | open | SC-Q6, SC-D19 |

## SC-D1: merge criterion is a two-condition test

**Decided.** Two skills merge only when both hold: their trigger space overlaps in a way that survives a good-faith rewrite of both descriptions, and their bodies produce the same post-state.

**Why.** The first condition needs the rewrite clause or the criterion fires on a description defect. `audit-drift` and `audit-verify` read as near-synonyms today, but that overlap is sloppy wording, not shared identity, and renaming separates them. `sync-decision` and `sync-decisions` cannot be separated by any rewrite, because "one specific closed decision" sits literally inside "one or more". Nested concepts merge; nested wording gets rewritten.

**What breaks if ignored.** Without the rewrite clause, any two carelessly described skills look mergeable, and a real distinction gets destroyed to fix a text problem. Without the post-state condition, a read-only reporter gets merged into a writer, erasing a safety boundary the user can see.

**Rejected: pointer reachability.** `DESIGN.md` previously held that a skill absent from the documented workflow should be reached by a pointer rather than by competing for a description match. Rejected because description match is a first-class host selection mechanism, not a fallback, while pointer reachability is a convention local to this repository. It measures only whether some other skill's prose happens to name the skill, which is an artifact of who wrote what. `extract-wiki` is the counterexample: nothing points at it, and no other skill contests its trigger vocabulary. Under the rejected criterion it looked endangered; under SC-D1 it is one of the healthiest skills present. The pointer observation keeps one narrow use, as a signal that a pointer is missing, never that a skill is unnecessary.

**Rejected: merging by family prefix.** Grouping the sync, audit, and maintain families into one skill each was proposed and rejected. A prefix is a naming artifact, not a property of the operation. `maintain-split` produces new packs plus an index; `maintain-archive` relocates content and sets a status `onboard` depends on. Neither shares a post-state with `maintain-compact`, so neither satisfies SC-D1.

## SC-D2: sync-decision merges into sync-decisions

**Decided.** Delete `baselinedocs-sync-decision`. Its scope constraint, that only directly impacted sections are patched with no broad unrelated rewrites, becomes a rule in `baselinedocs-sync-decisions`.

**Why.** The descriptions are strictly nested and the post-states are identical: patch the affected sections, refresh frontmatter in the documents that changed. No situation exists in which an agent should load one and not the other.

**What breaks if ignored.** Selection is undecidable. An agent holding one closed decision matches both descriptions, and "one or more" includes one.

**Rejected name: `baselinedocs-sync`.** `sync-codebase` and `sync-reconcile` remain separate skills, so a bare `sync` name would attract every request to sync docs against code through the name alone, recreating the undecidability being removed. The deferred detect/repair research may also need that namespace for the code-sync skill.

## SC-D3: the audit pair stays separate, audit-verify is renamed

**Decided.** Keep both. Rename `baselinedocs-audit-verify` to `baselinedocs-audit-claims`. Rewrite both descriptions on the axis that separates them.

**Why.** They differ by unit of analysis, and the two questions are independent.

| Skill | Unit | Question | Driven by |
|---|---|---|---|
| `audit-drift` | document | is this document behind the code? | provenance, `code_ref` against current state |
| `audit-claims` | claim | is this statement supported by evidence? | evidence quality, no provenance |

A document with a current `code_ref` can still be full of claims that were never true; those did not go stale. A document stale by provenance can hold claims that are all still accurate.

**What breaks if ignored.** Merging folds a provenance-free question into a provenance-driven one, so a claim that was never supported gets reported as stale, which points the reader at the wrong repair. `audit-drift` keeps its name because "drift" is precise and both `onboard` and `brief` name it in shipped text.

**Rejected: merging the pair.** Recommended earlier on the strength of near-identical descriptions, then withdrawn. That overlap is exactly the description defect SC-D1's rewrite clause exists to exclude.

## SC-D4: maintain-prune is deprecated

**Decided.** Delete `baselinedocs-maintain-prune`.

**Why.** `hallucination` is a journal. It has to keep rejected options and failed approaches so a later agent does not repeat a defeated approach. Prune's success test is "is this still relevant?", and on a journal that test returns remove for exactly the content the journal exists to hold: a rejected alternative is obsolete by construction, because it was rejected, and a closed question reads as resolved and therefore removable.

The lesson-entry exception already in the skill body does not patch this. The conflict is with the operation's success test, not with its edge-case list, and the exception covers only content written in the shape of a lesson entry. A rejected alternative or a closed question written any other way is unprotected.

**What breaks if ignored.** The journal erodes one prune pass at a time, and agents repeat mistakes the pack once recorded. That is the failure the journal exists to prevent, so a skill whose success test attacks it cannot be kept behind an exception clause.

**Consequence requiring SC-D5.** Prune served one legitimate case that now needs an owner: a disproven assumption still asserted as current truth in `introduction`.

## SC-D5: a disproven claim is relocated, not deleted

**Decided.** A claim disproven by code or closed by a decision moves into `hallucination` as a closed entry recording what was believed and what disproved it. The document whose role is current truth stops asserting it. The claim is never deleted. Owners: `sync-codebase` when code disproved it, `sync-decisions` when a decision closed it, `save` when the thread established it. The rule goes into `contract/pack-contract.md`, which every pack-writing skill already reads.

**Why.** This keeps the journal complete while removing the false current-truth claim, which is what prune was reached for.

**What breaks if ignored.** Deleting prune with no replacement leaves a misleading claim with no owner, and the gap gets closed later by re-adding prune, reversing SC-D4.

## SC-D6: maintain-archive is kept, with a defined destination

**Decided.** Keep the skill. Specify its destination path and naming convention in its body.

**Why.** It is not only a status flag. Three of its four steps relocate content: identify completed sections, preserve them in an archive-friendly form, clean the active pack. But the body never says where the archive goes, so what it produces has never been settled. That exact defect is on record in `DESIGN.md` as the reason `resume-snapshot` was deleted, which makes it a known-fatal gap rather than an untidy one.

**What breaks if ignored.** Two runs archive to two different places, and `onboard`, which excludes archived material from its default scope, cannot predict what it is excluding. `maintain-archive` is also the only producer of `status: archived` and `onboard` its only consumer, so the exclusion rule dies with the skill.

**Rejected: deprecate archive and give the relocation right to compact.** Relocation is legal under compact's information-preservation gate, since moving a completed phase into a linked file leaves the active document shorter with nothing lost, so this alternative was real. Rejected because it gives `maintain-compact` two mechanisms and an escape hatch from its own revert gate: an agent unable to compress far enough could relocate content instead, satisfying "shorter" without doing the work the gate asks for. Cost accepted in exchange: one more skill in a family being trimmed.

## SC-D7: compact carries an explicit revert gate

**Decided.** `maintain-compact` succeeds only when the document is shorter and its informational performance is unchanged. If any detail is lost, or a passage becomes open to more than one reading, revert. A long file costs less than hallucination from a short one.

**Why.** An agent compacting always has a reason to cut one more line, and the cut always looks locally harmless. Without the cost comparison stated in the body, the gate reads as advice.

**What breaks if ignored.** A pack that reads shorter and answers wrong, which is more expensive than the length it saved.

## SC-D8: removal is a direct delete

**Decided.** Delete removed skill folders outright. No stub, no deprecation shim.

**Known cost, accepted.** Skills install one folder at a time and users delete manually, so a `baselinedocs-sync-decision` already installed on someone's machine stays there and keeps competing for selection. Deleting from this repository cannot reach it.

**Rejected: a one-version stub.** A stub whose description redirects to the merged skill is the only thing that could reach an already-installed machine. Rejected in favor of a clean tree.

## SC-D9: description sharpening is a separate batch

**Decided.** Rewriting descriptions for pairs that share triggers but differ in outcome is its own batch, not part of this one. The audit rename in SC-D3 is excluded from that split, because a rename cannot be done without writing the new description.

## SC-D10: the remaining duplicate rule statements are removed inside SC-P6

**Decided.** The two further wordings of the lesson-entry rule, in `baselinedocs-run/references/execution-contract.md` and `baselinedocs-save/SKILL.md`, are removed as part of SC-P6 rather than in a phase of their own.

**Why.** Both are one sentence in one file, and SC-P6 is already the phase that makes the repository's written rules agree with each other.

**What breaks if ignored.** A rule stated three times in three wordings drifts on the next edit, and `test_references.py` cannot see it: that test only compares contract copies against the canonical file, so a fourth paraphrase written somewhere else passes.

**Rejected: a separate SC-P7.** It would have given the removal its own verification step, and mixing skill-body edits into a documentation phase does put two kinds of change in one place. Rejected as too small a scope to justify the phase.

**Order, carried from SC-D7's execution.** Both duplicates state one thing the canonical sentence does not: a lesson entry stays even after the mistake is resolved. Widen the canonical sentence to cover that, re-copy it, and only then delete the two. Deleting first drops the rule for as long as it takes to notice.

## SC-D11: maintain-archive is deleted, reversing SC-D6

**Decided.** Delete `baselinedocs-maintain-archive`. Remove `archived` from the `status` enum in `contract/pack-contract.md`, remove `onboard`'s archived-material exclusion rule, and replace `maintain-compact`'s `not for archiving completed phases` non-goal with a direct prohibition on moving content out of the active pack. Closes SC-Q1.

**Why.** SC-D6 kept the skill on condition that its destination be specified. Specifying it forced the prior question of what may be moved, and the answer left almost nothing.

| Document | Archivable | Reason |
|---|---|---|
| `hallucination` | no | the journal. Moving it outside `onboard`'s default scope reproduces the failure SC-D4 deleted `maintain-prune` for: content a fresh agent cannot reach by default is, for that agent, content that was removed |
| `introduction`, `sourcecode`, `useguide` | no | current state, not history |
| `roadmap` | completed phase history only | and the contract already keeps reasoning out of a checkpoint, so what is movable is evidence tables and affected-file lists |

The flag does not survive either. `onboard` excludes by document, while every proposal for `status: archived` was a per-section marker, so a marked section inside an active document is still read in full and the exclusion does nothing.

**What breaks if ignored.** Keeping the enum value with no producer and no consumer leaves an affordance that invites the next contributor to supply the missing producer, which is how a deleted skill returns. Keeping the skill with an unspecified destination leaves two runs archiving to two different places, which is the defect that deleted `resume-snapshot`.

**Accepted cost.** A long-running single-domain pack now has no way to shed history. `maintain-compact` cannot, because SC-D7's gate forbids losing detail, and its "low-value" wording, the phrase an agent used to cut old phase narration, was removed in the same round. `maintain-split` divides by domain, and a one-domain pack has nothing to divide. Onboard cost for such a pack grows monotonically and nothing mitigates it.

**Supersedes one constraint.** The introduction recorded that the frontmatter schema must not change and that `status: archived` stays in the enum, carried from the original instruction. That constraint was set while SC-D6 held. Removing the value is a deliberate exception to it, not an oversight; the rest of the schema is untouched.

**Rejected: keep archive and specify `<pack>/archive/`.** One file per archived phase, `status: archived` frontmatter, linked from the active roadmap, with archiving forbidden on `hallucination` and a promote-the-reasoning-first step before any relocation. Coherent, and it is the only option that closes the accepted cost above. Rejected because the operation it protects is thin once `hallucination` is excluded, and because no skill routes to it, so it fires only when a user remembers a maintenance chore.

**Rejected: move the flag into the write-able skills and drop relocation.** The first proposal on the table. It collapses: with relocation gone the flag is only ever a per-section marker, and `onboard` excludes by document, so the marker is inert. It would have retired the skill while appearing to keep the feature.

**SC-D1 and SC-D6 are left as written.** Both cite `maintain-archive` as a live skill, SC-D1 using it as an example of a post-state `maintain-compact` does not share. That is what was argued at the time and the journal keeps it. Read those two entries as history; SC-D11 is the current position. `DESIGN.md` carries the corrected version, because it states current design rather than recording a sequence.

## SC-D12: the sync and audit skills all stay, and the matrix that questioned them was wrong

**Decided.** Keep all five. Merge nothing, add nothing, rename nothing. Replace the detect/repair matrix in this pack and in `DESIGN.md` with the model below. Closes SC-Q3, and closes the namespace half of SC-Q2.

**Why the old model was wrong.** It assumed four distinct comparison scopes. The bodies say otherwise: `audit-drift` compares code changes, document claims and decision records; `audit-claims` compares each claim against code and explicit decisions; `sync-reconcile` prefers code evidence and explicit user decisions to break a tie. Three of five consult the same two sources, so scope does not separate them, and a matrix on that axis reports holes that are artifacts of the axis.

**The two real axes.**

| Group | Separated by | Members |
|---|---|---|
| report-only | unit of analysis | `audit-drift` document, `audit-claims` claim |
| writes | trigger event, which fixes blast radius | `sync-codebase` whole pack, `sync-decisions` only sections the decision reaches, `sync-reconcile` only conflicting sections |

**Why each empty cell stays empty.** Different reason per cell, which is itself the evidence that the matrix was not describing one phenomenon.

| Cell | Verdict |
|---|---|
| repair for claim against evidence | occupied by the contract. SC-D5 names three owners. A skill here is a fourth owner of a rule that names three |
| detect for pack against itself | occupied by `onboard` and `brief`, which report contradictions and route to `sync-reconcile` without repairing. A separate skill serves only "show contradictions without loading the pack", which nothing has asked for |
| detect for decision against pack | occupied by `audit-drift` step 2, which already compares decision records |

**What breaks if ignored.** Completing the matrix adds up to three skills to a family being trimmed, and each would either duplicate a contract rule or claim work an existing skill already does. Collapsing it costs the cheap screen, below.

**Rejected: one skill per comparison scope, detect as a report-only mode.** Rejected on cost asymmetry, a stronger objection than the boundary-visibility one recorded when SC-Q3 was framed. `audit-drift` is doc-first: read frontmatter, narrow, then compare scoped code changes. `sync-codebase` is code-first and unscoped, opening with "inspect the codebase first". Report-only mode on the merged skill still pays the full inspection cost, so the family trades a cheap screen plus an expensive fix for one expensive skill with a flag, and the screen is the half used most often. Terraform separating `plan` from `apply` into two commands is the same shape of argument, made from consequence rather than from cost, and it points the same way.

**Rejected: complete the matrix.** See the cell table above. A matrix with holes is a diagnostic, not a specification, and this one was drawn on the wrong axis.

**Consequence for SC-D2.** `baselinedocs-sync` is not needed as a namespace, because no merge happens. `sync-decisions` keeps its longer name for the original reason: a bare `sync` would attract every code-sync request through the name alone.

## SC-D13: the rename sweep stops at the audit pair, closing SC-Q2

**Decided.** No skill outside SC-D3's rename is renamed. `sync-reconcile` keeps its name. Closes SC-Q2.

**Why.** Three findings, in increasing weight.

The name is not the surface that selects this skill. Both `onboard` and `brief` name `baselinedocs-sync-reconcile` in shipped text, and each does so at the moment a contradiction is found, which is exactly when the choice is made. Routing already works without the name carrying its object, so a rename would pay for an improvement to a surface that is not the main entry path.

The family has no single naming convention to conform to. `sync-codebase` names the source of truth it compares against; `sync-decisions` names the thing it propagates. Two skills already considered direct, two different patterns. "Name the object" therefore has no one target here, and `sync-contradictions`, the best candidate, would parallel one of them while diverging from the other.

The cost is higher than SC-D8 recorded, measured in SC-P8. A machine carries several independent host skill directories, four on this one, each a real copy rather than a link into a shared store, and the installer adds and overwrites but never removes. A rename leaves the old name in every one of them until someone deletes it by hand.

**What breaks if ignored.** Renaming on a naming principle the family does not consistently follow buys a marginal clarity gain and pays it in stale duplicate skills competing for selection on every installed machine.

**Rejected: rename to `sync-contradictions`.** The strongest candidate, and it does name the object. Rejected on the three findings above rather than on the name itself, which is a better name than the one being kept.

**What the question retains.** The naming principle from SC-D3 stands for any *new* skill: name what it operates on. SC-D13 declines a retroactive sweep, not the principle.

## SC-D14: no pack-level finished marker, closing SC-Q4

**Decided.** Do not re-add a `status` value for a finished or parked pack, and do not give `onboard` a status-based scope filter. Closes SC-Q4.

**Why.** The function already exists one layer up. `onboard` does not scan for packs, it is pointed at one, and on an initiative its step 2 reads the index and stops, then step 3 selects the scope when the routing evidence names exactly one sub-pack **in progress**. That phrase is already the filter SC-Q4 proposed to add: a finished pack is not selected, because it is not in progress. Adding a frontmatter value would restate a routing rule as data.

`status: complete` cannot serve the purpose either, and the reason is worth keeping. This pack is `complete` and is precisely what a contributor must read before touching any skill folder, since SC-D1 through SC-D14 are the whole argument for the shape every current skill has. A rule that skipped complete packs would skip the most load-bearing document in the repository. So a finished marker would have to be a value distinct from `complete`, which makes it a schema change rather than a reuse.

**What breaks if ignored.** It would be `onboard`'s first status-based scope filter after SC-P5 deleted the only one, rebuilding the mechanism just removed to obtain a behavior the routing rule already provides. The orphaned-affordance failure in SC-D11 is the same shape.

**Rejected: add a `parked` or `archived` value with `onboard` as its consumer.** Coherent, and unlike the value SC-D11 deleted it would operate at file granularity, so the mechanism would work. Rejected because no initiative index exists yet, so the payoff is zero today, and because step 3 already declines to load what is not in progress.

**If this is reopened.** The trigger to watch for is a real multi-pack initiative where the index's own status proves insufficient for routing. That is the evidence SC-D14 lacks, not an argument it lost.

## SC-D15: the installed generation gap is closed, and the constraint asserting it is disproven

**What was believed.** The introduction carried a constraint stating that the skills installed on this machine were an older generation than this repository: the installed `baselinedocs-init` still routed to a `resume` family and shipped a 44-line contract against this repository's then-74-line canonical file. The operational conclusion drawn from it was that a `baselinedocs` skill invoked in a later thread would read a stale copy.

**What disproved it.** SC-P8 deleted every `baselinedocs-*` folder from each host directory and installed from this clone. Re-measured at `c6eb29a`: each of `.claude`, `.agents`, `.kilocode`, and `.kiro` holds exactly the 15 skills this repository defines, every packaged `references/pack-contract.md` in all four is `cmp`-identical to the 82-line canonical file, and the installed `baselinedocs-init` contains no occurrence of "resume" at all. `.codex/skills` exists and holds no baselinedocs skill, as it did before.

**What survives it.** The mechanism, not the measurement. An installed skill reads its own copy, so an install is a snapshot and this repository drifts from any machine from the next edit onward. The introduction keeps that as a constraint and the roadmap keeps the returning-risk row. Only the claim that this machine is currently behind is withdrawn.

**Unresolved, and now unresolvable.** Two figures exist for the pre-P8 installed contract: 44 lines in the introduction's constraint, measured against `baselinedocs-init` when that constraint was written, and 46 lines in SC-P8's checkpoint, measured across the installed set at delete time. The state both describe has been overwritten, so neither can be re-checked. Both are kept as recorded rather than reconciled to one number, because choosing between them would invent a measurement. The likeliest explanation, if it ever matters: the host directories are independent copies and may simply have held different generations.

**What breaks if this entry is dropped.** The next reader finds a constraint saying installs are snapshots, with no record that the gap was ever real or ever closed, and re-runs SC-P8's delete-and-reinstall against a machine that already matches. SC-P8's own finding is why the record is worth keeping: the installed set was worse than the constraint described, missing three of the six user entrypoints, so the constraint understated a real problem rather than inventing one.

## SC-D16: the contract ships on a full read, not on writing

**Decided.** The criterion for shipping `references/pack-contract.md` is that the skill reads the pack in full, not that it writes into one. `baselinedocs-onboard` gets the copy and a gate wording of its own, and a new `Workflow` step reporting content that sits in a document whose role does not cover it. No other read-only skill gets a copy. Opens SC-Q5.

**Why.** The old criterion answered the wrong question. Writing is what makes placement a *decision*, so a writer must consult the role list before it acts. A full read is what makes placement *checkable*, and that is a different property the criterion never named. SC-D12 had already assigned the detect cell for a pack against itself to `onboard` and `brief`, which report contradictions and route to `sync-reconcile` without repairing. A detector holding no role list can only see two statements that literally disagree; it cannot see correctly-stated content in the wrong file, which the contract's own opening section names as the damaging failure, because that content is duplicated as soon as the correct owner needs the same fact and the copies then drift.

`onboard` is the only read-only skill that qualifies, and the reason is its read guarantee, not its lack of writes. It commits to reading every document in the selected scope in full.

**The gate had to be reworded, not reused.** The writers' sentence names creating or editing a pack file. In a skill that never does either, that precondition can never be met, and an instruction that can never fire teaches the agent to treat the gate as decoration. `onboard`'s wording triggers on reporting the pack state. Both are pinned, and `test_read_only_skills_are_not_gated_on_writing` asserts the write wording is absent from a reader rather than only asserting that some gate is present.

**What breaks if ignored.** A real `onboard` run against an unrelated pack reported `onboard`'s absent contract copy as an unreadable file, and concluded that every future write into that pack was blocked. Both halves were wrong: ten skills carried the copy at the time, and no write routes through a read-only skill. The run was obeying an instruction scoped to skills that "read or write" a pack, so it looked for a file the skill was never meant to have. A reader acting on that report has two repairs available and both are wrong: add copies to skills that must not have one, which fails `test_references.py`, or conclude the contract is missing everywhere and skip the gate. Recording the criterion is what makes an absent copy legible as a decision rather than as damage.

**Rejected: leave `onboard` without a copy because it writes nothing.** The arrangement this replaces, and the reasoning is above. Keeping it leaves the family's only full reader unable to report the misplacement the contract exists to prevent.

**Rejected: give the contract to every read-only skill.** `brief` deliberately reads nothing in full, so it would report conformance it never checked, which is worse than reporting none. `audit-drift` compares documents against code and decisions and `audit-claims` compares a claim against its evidence, so neither examines placement. `setup-hooks` never opens a pack.

**Rejected: add a placement-audit skill instead.** Refused on the grounds already recorded in SC-D12. The detect cell for a pack against itself is occupied, and a new skill there would serve only "show placement findings without loading the pack", which nothing has asked for and which no partial read can answer.

**The de-duplication argument was weak and is recorded as such.** Part of the case for shipping the copy was that `onboard`'s `SKILL.md` paraphrased the contract in several places and could shrink to pointers, which would have made this a net removal of duplicated text. Reading both files side by side reduced that to one sentence: `onboard`'s "a moved repository is a signal" restated the contract's "a newer commit is a drift signal, not automatic proof of drift", and only the "not a verdict to investigate here" half was its own. The `Output` section's document names were left alone deliberately, because they read as reporting order rather than as a second role list, and cutting them would have made the instruction vaguer without removing a fact. Recorded because it was the most persuasive-sounding argument on the table and the weakest in fact; the criterion argument carried the decision on its own. A later reader re-deriving the change from the de-duplication case would conclude it was not worth making.

**Accepted cost.** The installed set on this machine is one phase behind again, exactly as the roadmap's risk row predicted. Ten copies against the repository's eleven, and an `onboard` that will keep reporting the absent copy the old way until the family is reinstalled here.

## SC-D17: report style ships as its own asset, separate from the contract

**Decided.** Add `contract/report-style.md` and copy it to every skill except `setup-hooks`, each gating on reading it before it reports. It carries one substantive rule: the first time a message names a pack element identifier, it must say what that element is. The same rule also goes into the user's own global instructions, and neither placement replaces the other.

**Why.** Reported from real use. A suggestion phrased as three bare identifiers could not be evaluated at all without scrolling back through the conversation to recover what each one meant, which turns every citing sentence into a question the reader has to ask. A bare code is not brevity; it is a deferred question, and the terminal is the one medium where the reader cannot cheaply look back.

**Why it does not live in the user's instruction file alone.** That file is per-user. A rule placed only there produces one user's experience and leaves every other installer with whatever the model defaults to, which is precisely the cross-user inconsistency this repository exists to remove from the family. A shipped skill's behavior must not depend on who installed it.

**Why it is not a section of the contract.** The two files have different correct audiences, and SC-D16 is what makes them different. The contract goes to skills that write a pack or read one in full. `brief` is neither, and SC-D16 records why it must not hold the role list: a partial reader owning the placement standard would report conformance it never checked. Yet `brief` produces a user-facing report on every run and cites identifiers in it. Folding report style into the contract would either hand `brief` the contract and reverse SC-D16, or leave the family's cheapest conversational skill outside the conversation rule. Two files, two audiences, two pinning tests.

**What breaks if ignored.** Every report that cites an identifier costs the reader a scroll or a question, and the cost is invisible to the agent producing it. Left to per-user configuration, the family behaves differently for each installer, and a report written for one user reads as a code dump to the next.

**Rejected: state it in the user's global instructions only.** Works for one user on one machine, and fails the point of shipping a skill.

**Rejected: add it as a section of `pack-contract.md`.** One fewer file and one fewer test, and wrong on audience, for the reason above.

**Accepted cost.** A second packaged asset means a second fanout to keep in sync, 14 copies against the contract's 11, and a second gate sentence loaded on every run of every skill. The file is deliberately short so that per-run cost stays small.

## SC-D18: hard-wrapped paragraphs are forbidden in pack documents

**Decided.** The contract's writing rules now forbid inserting a newline inside a paragraph. One paragraph is one line, however long, and the reader's editor wraps it.

**Why.** Measured, not assumed. In a real pack written by another agent, 2,396 of 2,610 prose lines fell in the 40-to-89-character band and only 20 lines exceeded 90 characters. No natural paragraph distributes that way, so the file had been wrapped at a column. Two packs written without wrapping put most of their prose lines above 200 characters, which is what unwrapped prose looks like. The wrapped paragraph reads as a list of unrelated statements, the line count roughly doubles so the document looks twice its real size and every line-number reference drifts, and a one-word edit re-flows a whole block in the diff.

**What breaks if ignored.** Beyond readability, the line count stops being usable as a size signal, which matters because `onboard` reports line counts as its proof of a complete read and its size gate reasons about scope from them. A wrapped pack reports double the lines for the same content, so the gate over-estimates the cost of loading it and under-estimates how much content a given budget holds.

**The distinction that has to survive.** Wrapping costs almost no tokens, because tokens track bytes rather than lines. Unwrapping the measured pack would halve its line count and change its token cost by almost nothing. A wrapped document therefore *looks* like a size problem and is not one, and this rule must never be offered as the remedy for a pack that is genuinely too large. SC-Q7 owns that problem.

## SC-D19: the entry index enters the contract as a conditional section

**Decided.** `contract/pack-contract.md` now requires an entry index at the top of `hallucination` once that document exceeds 40 KB or holds more than 20 entries, whichever comes first. Below the threshold it is omitted. The `Status` column is required. Nothing verifies a row against its entry, and that is accepted rather than mitigated. This closes the mechanism half of SC-Q7; the half about what `onboard` does with the index stays open.

**Why conditional rather than mandatory.** The index costs 87 bytes a row and defers an average closed entry of about 1,850 bytes, so its token arithmetic is roughly 21 to 1 in favour, which means it pays for itself once more than about five percent of entries can be deferred, and that is every realistic read. On a 342 KB journal the projection is a saving near 35,000 tokens per load. What does not scale down is the maintenance burden, which is per entry regardless of pack size. A journal of six entries can be held whole by any reader, and an index there is pure upkeep. Mandating it everywhere would also make three real packs non-conformant on the day the rule landed, and the restructuring that would fix them is the pack author's work: SC-D20 gave misfiled content named owners, but delimiting an undelimited journal into entries is not a relocation, so no skill performs it and the contract says so outright.

**Why the threshold is 40 KB or 20 entries.** Calibrated to measured points rather than derived. This document at 21 entries and 47 KB shows a scoped read at 28 to 50 percent of a full read, so the mechanism is already earning at that size. A 2.9 KB journal of 58 lines, measured in another repository, would carry an index larger than the saving. Both numbers are stated because they measure different costs: bytes measure what a read costs, entry count measures what the index costs to maintain. Neither alone is the trigger.

**Why `Status` is required.** It is the only column that tells a reader an entry was later reversed without reading the entry that reversed it. Building the index here surfaced exactly that: SC-D6 kept `maintain-archive` with a specified destination, and SC-D11 deleted the skill outright, so a reader working sequentially learns SC-D6 is dead only on reaching SC-D11. The column also carries the sharpest risk in the mechanism, below.

**What breaks if ignored, and it is accepted.** No test can verify a row still describes its entry, because a row is a different text from the entry by design and there is nothing to byte-compare it against. Every other duplicated file in this repository is safe precisely because it is byte-identical and machine-pinned: 11 contract copies, 14 report-style copies, the hook assets. The index is the first duplication here upheld by discipline alone, and the worst case is specific: a row saying an entry is current after a later entry reversed it actively asserts something false, which is the disproven-claim failure SC-D5 exists to prevent, reappearing inside the index. The user accepted this consciously rather than by omission.

**Rejected: mandatory in every pack.** Three real journals, at 2,796, 2,008, and 1,110 lines, delimit their entries with bold text or with nothing at all. For them the index is not an additive edit but a restructuring, and mandating it would create non-conformance with no owner.

**Rejected: accept the unverifiable row but pin the structural half.** Tests are cheap here and would catch a missing row, a row pointing at no entry, and a row longer than one line. Recommended and not taken: the user chose to rest the whole mechanism on discipline. Recorded because the structural tests remain cheap to add later, and because what they would not have caught is the thing that actually matters, which is whether a row's text is still true.

**Rejected: drop the `Status` column to remove the stale-assertion risk.** The defensive option. Rejected because the column's value was demonstrated on the first build while its risk is still hypothetical, and without it the table is a plain locator that no longer answers the question a reader most needs answered, which is whether an entry still holds.

## SC-D20: misfiled content gets named owners in the contract, closing SC-Q5

**Decided.** The contract gains a `Misfiled content` rule beside the disproven-claims rule. Content that is accurate but sits where the role lists do not put it moves, verbatim, to the document or section that owns it. Owners: `sync-decisions` when a decision settled what the content was filed under, `sync-reconcile` when the misplacement has already produced a contradiction, `save` when the current thread established where it belongs. A reporting skill names the owner and moves nothing. `onboard` step 10 is updated to name an owner instead of reporting that none exists.

**Why the contract rather than a widened skill.** Both were on the table. Naming owners follows a precedent already in the contract, where the disproven-claims rule names three owners rather than adding a skill, and it adds no skill to a family this pack spent eight phases trimming. Widening `sync-reconcile` would have grown the blast radius of the one skill whose current guarantee is that it touches only conflicting sections.

**Why the owners land where they do.** `sync-decisions` carries the commonest case, and it fits without stretching: an entry filed under open questions that a decision has since closed is misfiled precisely because a decision settled it, which is already that skill's trigger. `sync-reconcile` takes the case where the misplacement has produced a real contradiction, which is also already its trigger. `save` takes the case where the thread you are in is what established the correct placement.

**The gap this closes, carried from SC-Q5.** No skill repaired this before, and the reason was structural rather than an oversight. `sync-reconcile` fires on a contradiction, and correctly-stated content in the wrong file is not a contradiction yet; it becomes one only once the correct owner also states the fact, which is the drift the contract's opening section describes. So the only available repair arrived one step after the damage. `maintain-compact` shortens and never moves. The write skills add content rather than reorganizing it. The read skills report.

**Measured, not hypothetical.** In one real pack the open-questions section held 88 entries while 7 questions were actually open, so more than nine tenths of that section was settled material filed as unsettled. Nothing in it is untrue, so no audit reports it: `audit-claims` asks whether a claim has evidence and `audit-drift` asks whether a document trails the code, and misfiling fails neither test.

**What breaks if ignored.** Two costs, and the second is the one nobody sees. A reader cannot tell which questions are live, which is the single thing an open-questions section exists to answer. And every reader pays tokens for it, because the section that must always be read in full is exactly the section that filled with material that could have been deferred to an index row. On that pack the difference measured about 21,000 tokens per load, which is more than the entry index itself buys there.

**Still open, and deliberately left so.** Whether an open follow-up recorded inside a closed decision counts as misfiled. The contract lists open questions and closed decisions as `hallucination` content and does not say whether an open item may live inside a closed entry. Two such items exist in a real pack. The rule above does not decide it, because a follow-up sitting beside the decision that spawned it is arguably where it belongs, and guessing would create exactly the kind of relocation this rule is meant to make deliberate.

**Rejected: widen `sync-reconcile` to treat a heading disagreeing with its own content as a contradiction.** Coherent, and cheaper by one contract section. Rejected on blast radius: that skill's value is that it touches only what conflicts, and a heading-versus-content trigger makes any section reorganizable under it.

**Rejected: leave it open until a pack demonstrates the cost.** The position held through SC-P9 and SC-P10. Overtaken by measurement: the cost is now a number on a live pack, and SC-Q7's own sequencing finding showed this repair returns more there than the mechanism SC-Q7 was about.

## SC-D21: an edit to the contract destroyed a section heading, and nothing detected it

**What happened.** SC-P13 inserted the `Misfiled content` section by replacing a block of text that ended at the `## Conditional documents` heading. The replacement text did not carry that heading back. For the length of SC-P13 the contract defined `sourcecode` and `useguide` as bullets under `## Misfiled content`, and that state was copied byte-identically into all 11 packaged copies. Found on the next full read of the contract, which the gate requires before any pack edit, and repaired in the same pass.

**Why it looked safe.** The edit was anchored on a unique string and applied cleanly. Nothing reported a problem: `cmp` confirmed all 11 copies matched canonical, which they did, and the suite stayed green at 24 passed. Every signal available said the change was sound, because every signal measures agreement between copies and none measures whether the canonical file still has the structure it is supposed to have.

**What disproved it.** Reading the file top to bottom, as the gate requires, rather than reading the diff. The diff showed a new section added at the right place; only the whole file showed the heading gone.

**The lesson, and it generalizes past this incident.** A byte-identity test protects a fanout, not a source. The 11 copies were provably correct and provably wrong at the same time: correct as copies, wrong as content. Any check of the form "the copies agree" is blind by construction to a defect introduced in what they agree about, and the more copies there are the more reassuring the green result looks. This is the same shape as the count-in-prose defect SC-P8 pinned, and the same shape as the index rows SC-D19 accepted as unpinnable, so it is worth stating once as a class rather than three times as incidents.

**What breaks if ignored.** Two document roles were silently redefined. An agent reading the contract during that window would have decided that `sourcecode` is misfiled-content guidance, which is exactly the placement error the contract's opening section exists to prevent, injected into the file that prevents it.

**Repaired, and the gate is what caught it.** The heading is restored, the 11 copies re-synced, and the five role bullets verified to sit under the correct headings by listing each bullet with the heading above it rather than by eye. Recorded rather than quietly fixed because the failure mode, not the typo, is the useful part.

**Rejected: add a test asserting the contract's section list.** Tempting and cheap: pin the ordered heading list, fail on a removal. Not taken here because the heading list is edited deliberately in most phases that touch the contract, so the test would need updating in the same commits that break it, which is the pattern that trains a maintainer to update a test rather than read it. Left as a candidate if a second structural break occurs, which would make it a class rather than an incident.

## SC-D22: delete baselinedocs-setup-hooks and remove report-style exemption

**Decided.** Delete the one-time administrative skill `baselinedocs-setup-hooks` outright without a stub, reducing total skills from 15 to 14 and user entrypoints from 7 to 6, eliminating the `REPORT_STYLE_EXEMPT` exemption so 100 percent of remaining skills ship `contract/report-style.md`.

**Why.** `setup-hooks` existed solely to merge host configurations for the external Stop hook adapter retired in `family-design` FD-D37 - removing the hook mechanism eliminates the skill's only purpose and leaves every remaining skill in the family producing reports that cite pack elements under `report-style.md`.

**What breaks if ignored.** Leaving an administrative skill for a decommissioned subsystem creates dead user entrypoints, lingering host configuration dependencies, and preserves an arbitrary exemption in the report-style distribution test.

**Rejected: keep setup-hooks as an optional utility.** Rejected because retaining a skill whose underlying functionality was removed leaves orphaned code and misleads operators into attempting unsupported hook configurations.

## Open questions

### SC-Q8: what is the label standard inside an entry, and how many entry kinds are there?

Raised 2026-08-27 by the user, against the scheme proposed in SC-Q6. The objection: a rule forbidding identifiers for sub-parts leaves a journal that reads as a wall of text, losing the organized shape a human scans, and that cost was not weighed.

The objection is sound and the proposal had conflated two things. Visual structure inside an entry and citable identity across documents are separable, and only the second was ever the problem. Labels give the first without the second: measured here, one `grep '^\*\*Rejected'` finds all 22 rejected alternatives in this journal, so labels are already addressable as a class without any sub-identifier existing.

**Measured drift in this document.** The labels are not holding their wording.

| Standard label | Uses | Competing wordings in use |
|---|---|---|
| `Decided.` | 18 | - |
| `Why.` | 14 | 8, including `Why conditional rather than mandatory.`, `Why Status is required.`, `Why the old model was wrong.` |
| `What breaks if ignored.` | 15 | 3, including `What breaks if ignored, and it is accepted.`, `What breaks if this entry is dropped.` |
| `Rejected:` | 20 | 2 |

**A correction to the first count, which changes what a standard can assert.** The first pass reported SC-D8, SC-D9, and SC-D15 as entries missing required labels. Reading all three disproved part of that. SC-D15 is not a closed decision at all: it is a disproven-claim relocation, and it uses the shape that rule implies, `What was believed` and `What disproved it`. The contract's four-part requirement is written for a closed decision, so SC-D15 is conformant for its kind and the first count applied the wrong rule to it. SC-D8 is arguable: it carries `Known cost, accepted.` doing the work of `What breaks if ignored.`, so its content is present under a different name. SC-D9 is the only clear case, a single paragraph with no why, no consequence, and no rejected alternative.

That correction is the finding, not a footnote. `hallucination` holds at least three entry kinds already: a closed decision, a disproven-claim relocation, and an open question. A test asserting four labels on every `## D<n>:` heading would fail SC-D15 for being correctly written. So a label standard has to name the kinds and give each its own required labels before it can be enforced, and that is more work than the standard first appeared to be.

**Also unresolved: whether SC-D9 gets repaired or left.** Filling in its missing three parts means writing reasoning for a decision closed long ago, which the brownfield rule forbids reconstructing from inference. Leaving it means the journal contains one entry that does not meet the contract. Neither is obviously right, and no one has decided.

**The candidate answer.** The contract fixes the exact text of the required labels per entry kind, in a fixed order, and a variant becomes an additional label after the standard one rather than a replacement. Unlike the index rows SC-D19 accepted as unpinnable, this is testable, which is the strongest argument for it: it would be the first structural rule in `hallucination` a machine can actually check.

**Related, and unresolved with it: citing a part of an entry.** SC-Q6's proposal said promote the part to its own entry, which is heavy for something like one rejected alternative. The alternative on the table is a compound reference by text, `SC-D19 / Rejected: mandatory in every pack`. Its property is the reason to prefer it: if the label text changes, the reference fails loudly, because a search for it returns nothing. A renumbered identifier fails silently, still resolving, now to the wrong thing. That asymmetry, not verbosity, is the real case against sub-identifiers.

### SC-Q6: what is the identifier scheme, and does the contract own it?

**One clause is now settled, and the rest of this entry stands as written.** `family-design` FD-D30 replaced "unique across the pack" with "unique across the initiative, by carrying the pack prefix", which is why every identifier in this journal now reads `SC-D<n>`, `SC-Q<n>`, or `SC-P<n>`. That change was forced by a second pack appearing beside this one: two independent counters made `D16` name two different entries with no signal to the reader. Everything else below remains open, including the per-kind letters, the ban on encoding hierarchy in a name, the ban on sub-identifiers, and the question in this entry's own title of whether `contract/pack-contract.md` should state any of it. The contract was deliberately left untouched by FD-D30 for that reason.

Raised 2026-08-27, after the user reported that the prefix and its hierarchy vary by whichever agent last wrote the pack. Confirmed at the source: the contract says nothing about identifiers. No mention of numbering, of a prefix, or of an ID anywhere in its 84 lines. It defines document roles, the frontmatter schema, evidence density, and writing rules, and leaves element naming blank. So every agent invents a scheme and none of them is wrong by the standard that exists.

Schemes observed in use: `D<n>` for a closed decision, `Q<n>` for an open question and `P<n>` for a phase in this pack; `T1a` meaning decision `a` inside topic 1, and `T-A` meaning topic A, reported from elsewhere; `Phase` against `Milestone` against bare `P` or `M` at roadmap level one, and `Task` against `Point` against `Node` at level two.

The position to be argued when this is decided, recorded now so it is not lost: **hierarchy must not be encoded in the identifier.** Both `T1a` and `T-A` encode which topic a decision belongs to, and topic membership is the most mutable property a decision has. A decision often relates to two topics, and topics get merged and split as the document grows. Encoding a mutable relation into an immutable name guarantees that reorganizing the document breaks every reference to it. Concretely: if `SC-D16` had been named `T3b`, then grouping it with `SC-D11` today would force a rename, and every citation of it in `roadmap`, `sourcecode`, and `introduction` would silently become wrong. Flat append-only identifiers plus an explicit topic field inside the entry cost nothing to reorganize.

The second half of the proposal, also unargued yet: only pack-wide identifiers may be cited across documents, and anything numbered inside a single document is local detail. A real pack cites "Phase 3 Step 11" from its Phase 4 section; inserting a step or moving that one to another phase breaks the citation with nothing to report it. Under the rule, a step that needs citing from elsewhere has to be promoted to an entry with its own identifier.

**The proposed scheme, in full, so it can be argued with rather than re-derived.** One letter for the kind plus an integer. Flat, append-only, unique across the pack.

| Kind | Identifier | Written as |
|---|---|---|
| closed decision | `D<n>` | `## SC-D19: <title>` |
| open question | `Q<n>` | `### SC-Q7: <title>` |
| roadmap phase | `P<n>` | `## SC-P12: <title>` |
| step inside a phase | `Step <n>` | local detail, not citable from another document |

Seven rules go with it. A separate counter per kind, which this pack already proves out: SC-Q1 through SC-Q4 were closed by SC-D11 through SC-D14, each decision naming the question it closed, so the question keeps its number and the decision takes a new one. Append-only, never renumbered, never reusing a retired number, so a gap in the sequence is information rather than untidiness. The identifier sits in the heading text, which is what makes it greppable and gives it an anchor. No sub-identifiers. Grouping or topic goes in a field inside the entry or in the index's related column, never in the name. Only pack-wide identifiers may be cited between documents. One level-one concept in `roadmap`, named phase, prefixed `P`, with no parallel milestone or `M`, because two names for one level is where the reported drift began.

**Rejected alternatives, with the reason each fails.**

| Scheme | Why not |
|---|---|
| `T1a`, `T-A`, grouped by topic | encodes topic membership, the most mutable property an entry has, into a name that must not change. Concretely: grouping SC-D16 with SC-D11 today would force a rename, and every citation of it in `roadmap`, `sourcecode`, and `introduction` would silently become wrong |
| spelled out, `Decision 16` | verbose at every citation, and the readability problem it addresses is already solved by the gloss rule in `report-style.md`, which costs nothing per identifier |
| dated, `D-2026-08-27-1` | never collides and sorts chronologically, but long, and the date already sits inside the entry |
| one global counter, `E1` upward | loses the kind signal, and the kind is what tells a reader whether an item is settled or still open |

**A citation observed breaking in a real pack.** One pack cites "Phase 3 Step 11" from its Phase 4 section. Inserting a step before it, or moving that step to another phase, breaks the citation with nothing to report it. Under the rule above a step that needs citing from elsewhere has to be promoted to an entry with its own identifier, which is the cost the rule accepts in exchange.

Deliberately not decided in SC-P10. The user was supplying further pack output from other repositories to widen the sample first, and a naming rule written from two samples would be re-litigated the moment a third arrived. That reason has since weakened: SC-D19 put an index into the contract whose first column is an identifier, so the key of a contract-required table currently has no defined format, and waiting leaves it that way. SC-Q8 also has to be answered alongside this one, because the two together decide what is addressable and what is only readable.

### SC-Q7: what does `onboard` do with the index?

Narrowed by SC-D19, which decided the index itself: it is in the contract, conditional on a threshold, with a required `Status` column and no verification of a row against its entry. What is left open is the half that changes a skill rather than a document. The index exists and nothing consumes it, so today it serves a human reader and buys no token saving at all.

The options, none chosen: leave `onboard` reading everything, so the index is documentation only; read the table plus every open question and only the closed entries the task touches, taking the full saving and the audit risk with it; do that but ask the user which closed entries to load, listing them, which is slower and auditable; or keep reading everything by default and engage entry-level scoping only where the size gate would otherwise stop the run.

The last option deserves the most weight and was not obvious at first. `onboard`'s size gate already stops and asks when a scope may not fit, and today its only outcomes are load less or stop. Entry-level scoping turns that stop into a graded read, so the mechanism engages exactly where the alternative was already failing, and the default read is untouched. That answers the objection recorded below about auditability, because the narrowing only happens at a point where the user was going to be asked anyway.

Raised 2026-08-27 from measured real packs. SC-D11 predicted this exact cost and accepted it; the difference now is that it has a number.

| Document | Lines | Bytes | Tokens, approximate |
|---|---|---|---|
| `poc-provisioning.hallucination.md` | 2,796 | 180,066 | 45,000 |
| `poc-provisioning.roadmap.md` | 2,985 | 175,957 | 44,000 |
| second repository, `uat-provisioning/hallucination.md` | 2,008 | 342,029 | **85,500** |
| that pack, all five documents | 3,990 | 625,551 | **156,000** |
| this pack's `hallucination`, for scale | 251 | 30,908 | 7,700 |

Two corrections to how the problem was first stated. Byte count, not line count, is the size signal, because a wrapped document inflates lines and not bytes: the first pack above is wrapped, so its 2,796 lines hold roughly what 1,400 unwrapped lines would. And the figure that matters is per-document as much as per-pack: one 85,500-token `hallucination` is the hard case, while a 156,000-token whole-pack load is already mitigated by `onboard`'s default of one domain pack.

**The hypothesis that a cheap fix existed is disproven.** The survey looked for content the contract already forbids, on the theory that enforcement alone would shrink these files. It is not there. Across both large journals: zero changelog-style revision notes, zero retry or attempt logs, zero `UPDATE:` or `EDIT:` markers, zero superseded-entry markers. The bulk is legitimate journal content that the contract requires be kept. So the size is real, and no enforcement pass reduces it.

**What the survey did find, and it is the root cause of SC-Q6 as well.** These journals have almost no addressable structure. The 2,796-line file carries one `##` heading and three `###` headings in total. The 2,008-line file carries two `##` headings and no `###` at all, delimiting its 172 entries with bold text at the start of a line instead. A third, 1,110 lines, puts every closed decision between line 13 and line 965 as one undelimited section. Bold text is invisible to every tool: not an anchor, not a table of contents row, not a greppable structure, not a citable target.

That single fact explains both open questions. An entry that is not delimited cannot carry a stable identifier, which is SC-Q6, and cannot be read selectively, which is SC-Q7. The contract never requires `hallucination` to be a sequence of individually headed entries, and both symptoms follow from that omission.

**The candidate answer, unagreed.** Give `hallucination` a header table of one row per entry - identifier, one-line statement of what it is about, status, related identifiers - and let `onboard` narrow to it: read the table and every open question in full always, read a closed entry in full when the work touches it, and report in the manifest exactly which entries were read in full against which were read as a row. This attacks the token cost rather than the file size and deletes nothing, and `onboard` already sanctions the mechanism, since its rules require narrowing openly before reading rather than truncating during it. What it lacks today is granularity below one whole document.

Two risks to answer before adopting it. A summary row is a second statement of the entry's content, which is the duplication this repository fights hardest; the mitigation is that a row may state only what the entry is about and never its reasoning, pinned to one line by a test. And the agent will be tempted to answer from rows alone, which is the unbacked-answer failure `onboard` already has vocabulary for: an answer turning on an entry whose full text was not read is unbacked, and must be reported as such with an offer to read it.

**Rejected already, and why the rejections still hold.** Compaction gets ten to fifteen percent, which does not touch 2,796 lines, and SC-D7's gate forbids buying more by losing detail. Splitting by domain does nothing for a single-domain pack, as SC-D11 recorded. Reviving archival to `<pack>/archive/` was rejected in SC-D11 on grounds that still apply to this document specifically: content a fresh agent cannot reach by default is, for that agent, content that was deleted.

**Trial result, measured on this document in SC-P11.** The entry index was built here first, as the cheapest place to find out whether the shape works.

Two things are measured below and they must not be confused. The first is what the mechanism costs the file, measured on the index alone. The second is what a scoped read costs, measured against the file as it stands after this write-up was added, because that is what a run would actually read.

| Measure | Value |
|---|---|
| Cost of the index itself | 317 lines and 41.8 KB to 347 lines and 44.3 KB. Plus 623 tokens, or 6 percent |
| Index table alone | 2,493 bytes, about 623 tokens for 21 entries |
| Document at the time of measurement | 370 lines, 46.6 KB, about 11,644 tokens for a full read. It has grown since, because this table is inside the document it measures |
| Read the table plus every open question, no closed entry | about 3,322 tokens, 28 percent of a full read |
| Read the table, the open questions, and the four entries a contract-fanout task needs | about 5,842 tokens, 50 percent of a full read |

So the shape works and the saving here is real but moderate, between 50 and 72 percent depending on how many closed entries the task touches. The file grows, which is the correct trade only because what a run reads is what costs.

Writing this trial up moved the numbers, which is worth noticing rather than hiding. The write-up is a long open question, so it landed in the always-read half and pushed the minimum scoped read from 24 up to 28 percent. A journal that documents its own mechanics pays for them in the section it can never defer.

**The trial also found what decides the payoff, and it is not size.** It is the ratio of closed decisions to open questions, because open questions must always be read in full and only closed entries can be deferred to a row. Measured across three real journals, that ratio is not stable:

| Journal | Closed decisions | Open questions | Minimum scoped read |
|---|---|---|---|
| this document | 71 percent | 23 percent | 28 percent of full |
| htx `thingsboard-uat` | 86 percent | 12 percent | about 18 percent of full |
| solace `uat-provisioning` | 46 percent | **53 percent**, 184 KB of 342 KB | about 60 percent of full |

The pack that most needs the mechanism benefits least from it, and the reason is not size. Its open-questions section holds 88 bold-delimited entries while an `onboard` run over it reported 7 live questions, so the section is carrying a large amount of settled material under a heading that says it is unsettled. That is a placement problem, which is SC-Q5, presenting as a size problem.

**Consequence for sequencing.** SC-Q5 gates SC-Q7 for the worst-affected pack. Repairing placement there would move roughly half the file from always-read to deferrable, which improves the scoped read from about 60 percent to something near the other two packs, and it costs no new mechanism at all. Adopting the index first on that pack would buy 40 percent and hide the reason the other 60 percent was unavailable.

SC-Q1 closed in SC-D11, SC-Q3 in SC-D12, SC-Q2 in SC-D13, SC-Q4 in SC-D14, SC-Q5 in SC-D20. Stated rather than deleted so a reader can tell each was settled by a decision rather than dropped. SC-Q5's analysis was not deleted with its heading; it is inside SC-D20, which is where the relocation rule sends it.
