# Co-work Contract

Rules for a pack that holds a `<prefix>.cowork.md` file: several people write it at once and push to one branch. They narrow who writes where. Which document owns which content stays defined by `pack-contract.md`, and nothing here overrides it.

## Why

Two authors on one pack conflict in predictable places: the frontmatter `updated` and `code_ref` lines, the next-action section of `roadmap`, and the end of the entry index. Worse than a conflict is a silent duplicate: two authors each allocate the next identifier, git merges both cleanly, and every citation of it becomes ambiguous. Every rule below removes one of these. A region has one writer, so two pushes never edit one hunk, and an identifier has one allocator, so two entries never share a number.

## Files

Both carry baseline frontmatter with `document: "cowork"`, so every reader lists them and none treats them as retained source material.

| File | Writer | Holds |
|---|---|---|
| `<prefix>.cowork.md` | pack owner | authors, section owners, identifier ranges, file and code split |
| `<prefix>.cowork.<handle>.md` | that author only | the author's session journal, newest entry first |

A handle is lowercase letters, digits and hyphens, and is never `introduction`, `roadmap`, `hallucination`, `sourcecode`, `useguide`, `index` or `cowork`: such a handle would name a journal like a document of the pack.

## Roles

- Pack owner: exactly one. Writes every frontmatter, the `roadmap` next-action and risks sections, every `introduction` section not assigned to someone else, `sourcecode` and `useguide` unless the configuration assigns a section, and runs `fold`.
- Co-author: writes only the regions assigned to them and their own journal.

The pack owner decides who owns what. No skill and no co-author assigns a region to themselves.

## Reading a co-worked pack

Any skill that loads, onboards or briefs a co-worked pack reads the configuration and every journal in full, resolves the current author from `git config user.email` against the `Authors` table, and reports: who the author is, the phases and sections they own, their range and next free identifier, journal entries of other authors still marked `Fold: pending`, and requests addressed to them. An email absent from the table is not an author: stop and ask the pack owner to add it.

## Write regions

Regions are named by the role of the document, not by heading text, because a pack names its headings freely.

| Region | Writer |
|---|---|
| frontmatter of every document | pack owner, during `fold` |
| `roadmap` phase section | the phase's `**Owner:**` |
| `roadmap` next action, status and risks | pack owner |
| `introduction` section assigned in the configuration | its section owner |
| every other `introduction` section | pack owner |
| `hallucination` entry and its index row | the author whose range holds the identifier |
| `sourcecode`, `useguide` | pack owner, unless the configuration assigns a section |

Under a heading the label block is `**Ticket:**` first, `**Owner:**` second. Every `roadmap` phase carries `**Owner:**`.

A co-author who needs a change in a region they do not own writes it as a request in their journal. Closing another author's open question works the same way: the decision goes into the closer's own range with `Closes <ID>.`, and the question's owner deletes the question and its index row.

## Identifier ranges

Every author, the pack owner included, holds one bounded range, written `<low>-<high>`, that applies to every identifier kind (`D`, `Q`, `P`). Ranges never overlap, are never renumbered, and an identifier outside every range is a defect. Recommended: the pack owner keeps the existing counter (`1-199`), each co-author takes the next block (`200-299`, `300-399`). An author allocates only inside their range, from a scan of every document of the pack, with `packtool.sh next-id <pack-dir> <KIND> --author <handle>`. A bounded owner range is what stops the owner's counter from running into a co-author's block.

Placement keeps the hunks apart:

- owner entries go into the existing `## Closed decisions` and `## Open questions` groups, and owner index rows after the owner's last row of that kind
- co-author entries go into `## Closed decisions - <Name>` and `## Open questions - <Name>` at the end of the file, and co-author index rows at the end of the index table

At least one unchanged line separates the two insertion points, so git merges them without a conflict.

## Configuration

`<prefix>.cowork.md` holds these sections, each a table with a fixed header, so a tool can read it:

| Section | Columns |
|---|---|
| `## Authors` | `Handle`, `Name`, `Git email`, `Role` (`Pack owner` or `Co-author`). An email is recorded only when it already appears in `git log` of the repository |
| `## Introduction section owners` | `Section`, `Owner` |
| `## Identifier ranges` | `Handle`, `Range`, `Entries go under` |
| `## Files and code split` | `Area`, `Owner` |

The enabling decision is recorded in `hallucination` by the pack owner: who owns what, why, and the rejected alternatives.

## Journal

Header:

```
# <Pack> - Co-work journal - <Name>

Only <Name> writes here, except the `Fold:` line, which the pack owner updates during fold. Newest entry first.
```

Entry:

```
## YYYY-MM-DD - <topic>
- Done: <what changed, with evidence>
- State: <what is blocked or waiting, cite identifiers>
- Next: <next action>
- Requests to <handle>: <change needed in a region you do not own, or none>
- Fold: pending
```

A journal records the session. The phase section records the lasting outcome, so write the outcome into an owned phase section and only the narrative and the cross-author requests into the journal. A folded entry may be deleted once the file grows long, since its content is in `roadmap`.

## Write gate

Before every write to a co-worked pack, by any skill:

1. Is the target region owned by the current author per the configuration?
2. Is every new identifier inside the author's range, and free after a scan of the whole pack?
3. If the region is not owned, do not write it. Put the content into the author's own journal under `Requests to <handle>` and tell the user.

A skill whose job is to write the pack for the pack owner, such as `fold`, runs the same gate as the owner.

## Fold

Pack owner only. Pull first, then for every journal entry marked `Fold: pending`: write what it changes for the shared parts into the documents the owner writes, as one continuation point per fold and not one per entry; update `updated` and `code_ref` of each document touched since the last fold, re-running git for `code_ref`; mark each folded entry `Fold: done YYYY-MM-DD`. That mark is the only edit an owner makes to another author's journal.

## Git rules

| Rule | Detail |
|---|---|
| Small commits | one commit per phase change or per journal entry |
| Before push | `git pull --rebase` |
| Conflict | the later pusher resolves it and keeps the other author's region exactly as pushed |
