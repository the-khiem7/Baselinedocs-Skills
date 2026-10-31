# Academic Contract

Rules for a lesson built from the baseline packs of one or more projects. A lesson is a derived page: the packs stay the record, and the lesson teaches from them.

## Sources

- Facts come only from pack documents the run read. Never browse the web for a fact, and never fill a gap from memory.
- A lesson never edits, moves or deletes a pack document or any file of a source project.
- An index row is a locator, not a source. A point may rest on an entry only after that entry's full text was read.
- A point found in one pack is marked `[single source]`. A point found in several packs says how many.
- Two packs that disagree are both shown, each with its project label. Never pick the newer or the more common claim.
- A fact the packs do not give is marked `[missing: <what is needed>]`. A value the run worked out rather than read is marked `[inferred]`.

## Citation

- Every point ends with a citation: `[<project label> / <document> / <entry heading>]`, for example `[Project A / hallucination / <entry heading>]`.
- The project label is the anonymized label whenever anonymization applies. Name the entry by its heading text, so a reader without the pack can still tell what it is about.
- A fact shared by several lessons is stated once, in the shared-facts block of the series page, and each lesson cites it by key, so lessons cannot drift apart.

## Lesson format

- One standalone HTML file per lesson: inline CSS and script only, no network request, no external font or library, readable offline. A series adds one index page and one reference page.
- Design backward. Write the outcome first, as what the learner must be able to do after reading, then choose the points that serve it. Cut a point that serves no outcome, or label it `enrichment`.
- Sections in this order: Outcome, Context, Points, Common mistake, Check, Sources.
- Common mistake: a mistake from a pack with why it looked reasonable, what disproved it and the fix, kept in full.
- Check: at least one question per outcome, with its answer and the point that answers it. A check without an answer does not count.
- Carry structure with headings, tables and lists. Prose only where reasoning has to be followed in order.
- Quizzes that record answers and progress tracking are out of scope until a decision adds them.

## Anonymization

Applies to every lesson drawn from more than one project, and to a single-project lesson only when the user says the page will be shared.

- Replace five classes before any page is written: project names, account identifiers, host names, customer names, person names.
- Labels: `Project A`, `Account 1`, `Host 1`, `Customer 1`, `Person 1`. One real value keeps one label for the whole series.
- Drop every co-work handle, author email, owner line and identifier range from the lesson; they name people. Drop every work ticket line and ticket key from the lesson, with its tracker URL. A ticket names the employer's tracker and project and teaches nothing; it is removed, not labelled.
- Keep the real-to-label mapping in one file per series, in the directory the skill was called from. Before writing it, check with `git check-ignore` that git ignores it; when it does not, add one entry for that file to the directory's ignore file and check again, and stop without writing when it is still not ignored. Never print its contents and never copy it into a page.
- Report the count of replacements per class after each run, and state that replacement is a heuristic that was not proven complete. The user reviews the page for identifiers it missed before it leaves the machine.
- Before writing a page, scan its text for keys, tokens, passwords and connection strings. On a finding, stop and name the file and the rule, never the value.

## Output location

Write into the directory the skill was called from, and nowhere else. When that directory is a project repository and the lesson draws on several projects, warn before writing.
