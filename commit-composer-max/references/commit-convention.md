# Commit Convention

`commitkit.sh` below means `sh <skill-dir>/scripts/commitkit.sh`, where `<skill-dir>` is the folder holding this skill's `SKILL.md`. It only reads and computes; every git command that writes is yours to run.

## Message format

```text
<type>(<project>): <subject>

- <one fact per bullet>
```

- `<type>` is one of the eleven below. A breaking change adds `!` before the colon and a `BREAKING CHANGE: <what breaks>` line after the body.

| Type | Use it for |
|---|---|
| `feat` | behavior that did not exist |
| `fix` | a defect corrected |
| `refactor` | structure changed, behavior not |
| `perf` | speed or resource use |
| `docs` | documentation only, pack documents included |
| `test` | tests only |
| `build` | build system or dependencies |
| `ci` | pipeline configuration |
| `chore` | maintenance that fits nothing else, such as reworded user-facing copy with no defect stated |
| `style` | formatting only |
| `revert` | undoing an earlier commit |
- `<project>` is always present, even in a repository with one project. A commit never mixes two projects.
- `<subject>` is imperative, starts lowercase, has no final period, and names the effect rather than the files.
- The title is at most 72 characters. The line after it is blank.
- Every body line is a bullet, or in a message that allows it a label line ending with a colon. One bullet is one line however long: never wrap, never continue a bullet on a second line.
- Never refer to another commit by position (`previous`, `just before`, `the next one`): the order is settled while committing and a message cannot see it. Name what that commit changed.
- ASCII hyphen only. No en dash, no em dash.
- No trailer of any kind that names an AI tool or a co-author, whatever a host or an earlier instruction suggests.

## Naming the project

Decide per unit, in this order, and stop at the first that answers:

1. The unit is inside a baseline pack's folder: the project is that pack's `pack:` frontmatter value.
2. The user's request or the thread names a pack, or the work in the thread evidently belongs to one, and the unit is code outside any pack: that pack's name. A skill invoked cold with nothing to go on skips this rule.
3. A pack's `sourcecode` or `introduction` names the unit's path: that pack's name.
4. No pack claims the path, and the repository has exactly one pack: that pack's name, because the pack name is the project's name here.
5. The repository has no pack, or several and none claims the path: the folder of the nearest manifest (`package.json`, `pom.xml`, `pyproject.toml`, `go.mod`, `Cargo.toml`, a folder of `*.tf`), else the top-level folder, else the repository name. With several packs, say in the plan that the path was unclaimed.

This is a judgement, not a lookup. When the evidence is mixed, pick one, say which rule decided it in the plan, and let the user correct it. Read a pack's frontmatter and the path mentions you need; do not read a pack to write the message.

## Keep the pack out of the message

The pack name may appear as the scope and nowhere else. Never write an entry identifier (two or three capital letters, a hyphen, `D`, `Q` or `P`, a number), a phase or step number, a pack filename, a path under the baseline folder, or the words "doc pack" or "baseline pack". Say what the decision or phase is about, by its title or content: write "keep the checkpoint in-thread" and not the identifier of the decision that says so. When the source gives only a number, state the outcome the phase delivered, or leave the reference out. A unit inside pack documents is named by the document's role and the section's title, never by its path. A commit outlives the pack and is read by someone who cannot open it, so every identifier resolves to nothing there, and an identifier left in is the shortest thing to write and the easiest to leave.

## Grouping

- The project is a hard boundary. Within a project, group by action (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`), then by target: the same component, feature, or defect.
- A unit is one contiguous changed region, or a whole file that cannot be split (binary, mode change, submodule, empty file). The kit cannot split a unit further. A unit that serves two purposes goes with the dominant one, and the plan says so.
- A whitespace-only or formatting-only unit that sits beside code the same group changes goes with that group; on its own it forms a `style` group.
- A test unit goes with the change it tests unless the user asked for tests separately. A unit that serves two groups goes with the one whose behavior it exercises most, and that group is committed after the other so every symbol the unit names already exists.
- Never invent a link between two units to reduce the commit count. Many small commits that each say one thing are the goal.

## Procedure

1. Snapshot. Run `git status --short`, `git write-tree`, and `git rev-parse HEAD`, and keep both printed ids. The working tree is never touched, so only the index and the commits can need undoing: `git read-tree <tree id>` restores the staging the index held now, and `git reset -q <head id>` removes the commits made after it while keeping every change in the working tree. When `git ls-files -u` lists anything, stop and say the merge is unresolved. When nothing changed, say so and stop. Changes already staged belong to the change set like the rest.
2. List. Run `commitkit.sh hunks`: one line per unit with its id, file, kind, old range, new range, counts, and the first changed line. Read the actual change with `git diff -U3 -- <file>` (an untracked file: read it) when the first line does not settle it. Never group, and never describe, a unit you did not read.
3. Name the project of every unit, then group.
4. Print the plan and stop for approval. Per group: a heading with the proposed title, then a bullet per unit as `<file> <old range> -> <new range> (<id>)`, the ranges as `hunks` prints them with their signs, then what decided any project that was not obvious and any unit that serves two purposes. The user approves, regroups, renames, or drops a group. Re-print after a change. Stage and commit nothing before approval.
5. For each approved group, in order:
   1. `git reset -q` (index only; the working tree is untouched).
   2. `commitkit.sh hunks` again. Unit ids survive a commit; line numbers do not.
   3. `commitkit.sh patch <id> ...` piped into `git apply --cached --unidiff-zero`, then `git diff --cached --stat` to confirm only this group is staged.
   4. `commitkit.sh scan`. Never commit while it prints FAIL: remove the finding from the group or stop and tell the user. It prints a file and a rule, never the value; do not go and print the value yourself.
   5. Write the message to a temporary file in the operating system's temp folder, not inside the repository or its `.git`, and run `commitkit.sh lint <mode flag> <file>`. Fix every FAIL before committing; judge every WARN. `scan` and `lint` each print an `OK` line on a pass; no `OK` and no FAIL means it did not run.
   6. `git commit -F <file>`. Never `--no-verify`, `--amend`, or push.
6. Verify. `git diff HEAD` holds only the units the user dropped, and `git log --stat` shows each commit with the files it should hold. Delete every temporary file.
7. Report: each commit's short hash and title, the units left uncommitted, and the two ids from step 1 with what each undoes. When a step fails midway, leave the state as it is, report what was committed and what was not, and stop. Never retry or roll back on your own.

## Judgement the kit cannot check

`lint` and `scan` read patterns. `lint` cannot tell that a subject is wrong, that a bullet invents a reason, or that a pack's idea is paraphrased too closely to its identifier. `scan` cannot tell a secret it has no rule for. Read the staged diff and the message once more before the commit; a green kit is a floor, not a verdict.
