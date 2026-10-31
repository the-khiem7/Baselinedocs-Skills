---
name: baselinedocs-cowork
description: Enable, reassign, fold, or disable co-work mode on an existing baseline pack, where two or more people write the same pack in parallel and push to one git branch without merge conflicts or duplicate identifiers. Records authors, phase owners, section owners and identifier ranges in a per-pack cowork configuration and gives each author a journal. Use explicitly when the pack owner says co-work, cowork, pair-work, multi-author or co-author on a doc pack, wants to assign phases or sections to people, split identifier ranges, fold co-author journals into the shared parts, or turn co-work off.
version: "3.4.0"
---

# Baseline Docs Co-work

Several people write one pack at once, and every region of it has exactly one writer. This skill is the pack owner's: it sets co-work up, changes who owns what, folds the journals, and turns it off. A co-author needs none of it, because `baselinedocs-load`, `baselinedocs-onboard`, `baselinedocs-brief` and `baselinedocs-save` apply the co-work contract by themselves to any pack that holds a cowork configuration.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `<core-dir>/references/cowork-contract.md` in full before enabling, reassigning, folding or disabling co-work, every time. It is the only definition of who writes which region and how identifier ranges work; a region assigned from memory of it is the duplicate identifier and the overwritten hunk it exists to prevent.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` after every pack write and before reporting it, and allocate every new identifier with `sh <core-dir>/scripts/packtool.sh next-id <pack-dir> <D|Q|P> [PREFIX]`, never from memory. A new pack's first identifier needs its PREFIX. Never report a write as done while `check` prints a FAIL line: a duplicate identifier or a missing index row resolves citations to the wrong entry, and nothing else detects it. Without `sh`, say the checks were not run.

In a co-worked pack the tool refuses a bare `next-id`; add `--author <handle>` so the number comes from that author's range.

## Inputs

- the pack root
- the mode, chosen from the request and the pack: `enable` when the pack holds no `<prefix>.cowork.md`; `assign`, `fold` or `disable` when it does
- the current author, resolved from `git config user.email` against the `Authors` table. Only the pack owner runs `assign`, `fold` and `disable`. An email not in the table is not an author: stop and tell the user to ask the pack owner. `enable` makes the person running it the pack owner.

## enable

1. Refuse when the pack already holds a cowork configuration; offer `assign`.
2. A pack on schema `2.0` is enabled only after the owner says whether its documents move to `3.0` (the `cowork` document needs `3.0`). Never upgrade unasked; when the owner declines, only the new cowork files carry `3.0`.
3. Ask the owner, as labelled questions grouped by topic, for the authors (handle, name, git email already present in `git log`), the owner of every phase, the owner of every `introduction` section that is not theirs, and one identifier range per author. Recommend the owner keeps the existing counter (`1-199`, or wider than the highest number in use) and each co-author takes the next block (`200-299`, `300-399`).
4. Write `<prefix>.cowork.md` from `references/config-template.md`, and one `<prefix>.cowork.<handle>.md` per author from `references/journal-template.md`.
5. In `roadmap`, add `**Owner:** <handle>` under every phase heading, after a `**Ticket:**` line when there is one.
6. When one `introduction` section must serve two owners, split it into `###` sub-sections and move each existing bullet verbatim under the one that owns its topic: a relocation, not a rewrite. Name every assigned section in the configuration table.
7. In `hallucination`, add at the end of the file one `## Closed decisions - <Name>` and one `## Open questions - <Name>` per co-author, each holding one line that names that author's range.
8. Record the enablement as a closed decision in the owner's range: who owns what, why, and the rejected alternatives the thread produced. Add the continuation point to `roadmap`.
9. Run `check`; resolve every FAIL.
10. Commit only when the user authorized it, following the git rules of the co-work contract.

## assign

Change an owner, a range or the author list in the configuration, and the `**Owner:**` lines that follow from it. A range is never renumbered and never shrinks below an identifier in use; widening or adding one is allowed. Record the change as a decision in the owner's range when it changes who owns a region. Run `check`.

## fold

1. Pull first (`git pull --rebase`).
2. For every journal entry marked `Fold: pending`, write what it changes for the shared parts into the documents the owner writes, as one continuation point per fold and not one per entry.
3. Update `updated` and `code_ref` of each document touched since the last fold; re-run git for `code_ref`.
4. Mark each folded entry `Fold: done YYYY-MM-DD` in the journal it came from. That mark is the only edit made to another author's journal.
5. Run `check`.

## disable

Fold everything first. Then remove the `**Owner:**` lines, keep the co-author groups in `hallucination` (identifiers are never renumbered), and delete the configuration and the journals. Merge split `introduction` sections back only when the owner asks. Record the disablement as a decision in the owner's range. Run `check`.

## Output

Report the files changed and what is left for the user: a commit, a push, a request to a co-author. Name each identifier you cite with its meaning.

## Non-Goals

- does not decide who owns what; the pack owner does, and this skill asks
- does not write in a region it does not own for the current author; the contract's write gate applies to this skill too
- does not resolve a git conflict by overwriting another author's region
- not a replacement for `baselinedocs-save`; a co-author records their session with `save`, which writes their journal
