---
name: commit-composer-max
description: Group the uncommitted changes of a git repository by project, action, and target, at hunk level, and commit each group with the fullest Conventional Commits message that can be written - the reason, every changed file and symbol, the risks, and what was verified - so another agent can audit a task from the commit message alone without reading the code. Use explicitly when the user wants an audit-grade or exhaustive commit message, a commit log that serves as task evidence, or commits that spare a later agent from reading the diff. For a short message, use commit-composer.
---

# Commit Composer Max

Turn the working tree into a series of single-purpose commits whose messages carry everything a later reader needs. This skill commits only after the user approves the grouping, and never pushes.

Read `references/commit-convention.md` in full before grouping or writing any message, every time. It is the only definition of the message format, how a project is named, what must stay out of a message, how units are grouped, and the procedure; do not infer any of it from the repository's earlier commits or from memory.

Run `sh <skill-dir>/scripts/commitkit.sh scan` on the staged diff before every commit, and `sh <skill-dir>/scripts/commitkit.sh lint --max <msgfile>` on every message before `git commit -F`. `<skill-dir>` is the folder this SKILL.md sits in. Never commit while either prints a FAIL line: a key or a credential in a commit is in history for good, and a message that breaks the format reaches every reader of the log. Without `sh`, stop and say the checks cannot run; do not commit unchecked.

## Message shape

- Title: `type(project): subject`, never over 72 characters.
- Body: always present, no length limit, in three labelled blocks in this order. Each label line ends with a colon and is followed by bullets, one line per bullet. Leave a block out when nothing applies to it; never write `N/A`.
  - `Why:` the reason and the goal, and the problem this commit solves apart from the rest of the work.
  - `Changes:` one bullet per file or symbol touched, as `path: symbol - what it did before and what it does now`, with exact names, values, paths, and units.
  - `Risk and verification:` what can break and who is affected, any breaking change, each command run in this session with what was observed, and what was not verified.
- The test: a reader holding only this message can say what changed in every touched file, why, what it can break, and what was checked, without opening the diff.

## Rules

- Follow the procedure in the convention: snapshot, list units, name projects, group, print the plan, stop for approval, then stage and commit group by group.
- The plan is a proposal. Do not stage, reset, or commit anything before the user approves it. Show each group's proposed title with it; the full body is written at commit time from the units read.
- Read every unit before describing it. `Changes:` states what the diff does, so it needs the diff read, not the first changed line the kit prints.
- `Why:` comes from the user's request, the thread, and the diff. When none of them gives a reason, write `- reason not stated in the thread` and do not invent one.
- `Risk and verification:` records only what was run and observed in this session. A check you did not run is listed as not verified, never implied. Running one now is allowed when it is read-only and cheap, such as a syntax check or the test command the thread named; never install or change anything to run one.
- `Changes:` names a file by `path`, except for a unit inside baseline pack documents, which takes the document's role and the section's title in place of the path.
- Words that carry no fact (`various`, `misc`, `some changes`, `and more`, `etc.`) mean the bullet is not finished; name the thing.
- A change inside baseline pack documents is described by what it records: the decision's subject, the phase's title. Never by identifier, number, or filename.

## Output

- before approval: the plan, a heading and unit list per group
- after: each commit's short hash and title, the units left uncommitted, and the starting tree id and HEAD id with what each undoes

## Non-Goals

- not a push, amend, rebase, tag, or branch tool
- does not write the short message; `commit-composer` does
- does not read or write a baseline pack beyond the frontmatter and path mentions needed to name a project
