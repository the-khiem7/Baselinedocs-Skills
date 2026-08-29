# Report Style

Rules for what the agent says to the user. Formatting rules for what goes inside a pack document live in `pack-contract.md`; this file governs the conversation only, and the two never override each other.

## Name an element, then say what it is

A pack element identifier carries no meaning on its own. The first time a message mentions one, follow it immediately with a short gloss of what it is. Later mentions inside the same message may stand bare.

Wrong: choose `D1a` over `D1c`, because `D7d` makes `D1a` unstable.

Right: choose `D1a` (plain NLB, no ALB in front) over `D1c` (ALB terminating TLS), because `D7d` (the imported certificate was deleted from ACM) makes `D1a` unstable.

The reader cannot scroll a terminal to recover a meaning the message never carried. An identifier they have to look up is a question they have to ask, and the cost lands on every sentence that cites one. This holds for every identifier a pack uses: closed decisions, open questions, phases, and anything a later scheme adds.

## Say where an element lives when the user may want to open it

Name the document with the identifier the first time, not the identifier alone. `Q5` in `hallucination` is findable; `Q5` is not, in a pack with five documents.

## A quotation needs the same gloss an identifier needs

A line lifted out of a document means no more to a reader who has not read that document than a bare identifier does. Say in your own words what the document needs and what it costs the user if it stays unanswered, then give the quotation and its location as the evidence for what you just said. Meaning first, quotation second. Dropping the quotation is not the alternative: it is what makes the claim checkable.

## Restructure a next action, never change what it tells the user to do

A next action is the one field a reader acts on directly, so what it instructs has to survive intact: every instruction, condition, prohibition, name, number, and ordering kept, none added, none softened. Within that, render it for reading rather than reproducing the source layout. A heading per pack or phase, one bullet per instruction, the source's own numbering preserved where it has one. Do not wrap it in a blockquote, which returns a list of instructions to the wall of text this rule exists to prevent. Name the document and phase it came from, so the user can check the rendering against the source.

## Do not present an identifier as an argument

An identifier names a decision; it is not a reason. "This follows `D11`" tells the user nothing they can check or disagree with. State the substance, then cite the identifier as the place the full reasoning lives.

## Structure a report, do not narrate it

A report with more than one part names each part as a heading, states each fact as its own bullet, and nests a bullet under what it qualifies. Name a section after the document whose role owns its content, so the reader sees the source without a citation. A paragraph carrying several independent facts reads as one statement and hides all but the first; prose is for an argument that has to be followed in order, and everything else is a list.

## Keep a table inside the terminal's width

Three columns at most, every cell short. A path, a URL, a quotation, or a full sentence goes in a bullet under the table, never inside a cell. A table too wide to render degrades into a vertical dump of field names and empty rows, which is worse than the prose it replaced. When rows repeat the same value, state it once above the table and list only the rows that differ.

## When asking, state what one word of agreement means

Give each question its recommended answer, then close the block with the full default set spelled out, so a user replying `approve` accepts something stated rather than something inferred. One exception, and it is absolute: a default set never carries an authorization the user has to give affirmatively, such as committing, deleting, or applying. Ask for those separately and leave them out of the shortcut.
