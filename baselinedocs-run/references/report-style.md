# Report Style

Rules for what the agent says to the user. Formatting rules for what goes inside a pack document live in `pack-contract.md`; this file governs the conversation only, and the two never override each other.

## Name an element, then say what it is

A pack element identifier carries no meaning on its own. The first time a message mentions one, follow it immediately with a short gloss of what it is. Later mentions inside the same message may stand bare.

Wrong: choose `D1a` over `D1c`, because `D7d` makes `D1a` unstable.

Right: choose `D1a` (plain NLB, no ALB in front) over `D1c` (ALB terminating TLS), because `D7d` (the imported certificate was deleted from ACM) makes `D1a` unstable.

The reader cannot scroll a terminal to recover a meaning the message never carried. An identifier they have to look up is a question they have to ask, and the cost lands on every sentence that cites one. This holds for every identifier a pack uses: closed decisions, open questions, phases, and anything a later scheme adds.

## Say where an element lives when the user may want to open it

Name the document with the identifier the first time, not the identifier alone. `Q5` in `hallucination` is findable; `Q5` is not, in a pack with five documents.

## Quote a next action, never paraphrase one

A next action is the one field a reader acts on directly. Paraphrasing it silently changes what they will do. Quote it and say which document it came from.

## Do not present an identifier as an argument

An identifier names a decision; it is not a reason. "This follows `D11`" tells the user nothing they can check or disagree with. State the substance, then cite the identifier as the place the full reasoning lives.
