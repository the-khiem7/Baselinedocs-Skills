---
name: commit-composer
description: Group the uncommitted changes of a git repository by project, action, and target, at hunk level rather than file level, and commit each group as a short Conventional Commits message with the project name in the title. Use explicitly when the user wants to commit, split a messy working tree into several commits, group changes before committing, or write a concise conventional commit. For a long message that lets an agent audit the task without reading the code, use commit-composer-max.
---

# Commit Composer

Turn the working tree into a short series of single-purpose commits. This skill commits only after the user approves the grouping, and never pushes.

Read `references/commit-convention.md` in full before grouping or writing any message, every time. It is the only definition of the message format, how a project is named, what must stay out of a message, how units are grouped, and the procedure; do not infer any of it from the repository's earlier commits or from memory.

Run `sh <skill-dir>/scripts/commitkit.sh scan` on the staged diff before every commit, and `sh <skill-dir>/scripts/commitkit.sh lint --concise <msgfile>` on every message before `git commit -F`. `<skill-dir>` is the folder this SKILL.md sits in. Never commit while either prints a FAIL line: a key or a credential in a commit is in history for good, and a message that breaks the format reaches every reader of the log. Without `sh`, stop and say the checks cannot run; do not commit unchecked.

## Message shape

- Title: `type(project): subject`, aim for 50 characters, never over 72.
- Body: leave it out when the title says enough. When the reason is not obvious from the title, add 2 to 5 bullets, each one line, each a single fact, saying why and not what the diff shows. No label lines.

## Rules

- Follow the procedure in the convention: snapshot, list units, name projects, group, print the plan, stop for approval, then stage and commit group by group.
- The plan is a proposal. Do not stage, reset, or commit anything before the user approves it.
- Never describe a change you did not read. A bullet that explains a reason nobody stated in the thread or the diff is an invention; leave the bullet out.

## Output

- before approval: the plan, a heading and unit list per group
- after: each commit's short hash and title, the units left uncommitted, and the starting tree id and HEAD id with what each undoes

## Non-Goals

- not a push, amend, rebase, tag, or branch tool
- does not write the long audit-grade message; `commit-composer-max` does
- does not read or write a baseline pack beyond the frontmatter and path mentions needed to name a project
