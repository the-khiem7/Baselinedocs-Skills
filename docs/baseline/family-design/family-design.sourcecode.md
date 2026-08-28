---
baseline_schema: "2.0"
pack: "family-design"
document: "sourcecode"
status: "active"
updated: "2026-08-28"
code_ref: "0cb913f"
---

# Design Mechanisms

The parts of the repository that carry the family design rather than the consolidation. Folder shape, the two asset fanouts, the pointer graph, and the test surface are topology this pack does not own: `skill-consolidation.sourcecode.md` holds them, and nothing here restates them.

## Instruction surfaces

Four surfaces reach a running agent, and they do not offer the same guarantee. The whole rule-placement argument, FD-D7, turns on this table.

| Surface | Loaded | Carries | Enforced by |
|---|---|---|---|
| `description` frontmatter | always, on every host, before selection | one line, enough to select the skill | the host's selection mechanism |
| `agents/openai.yaml` | Codex only | `allow_implicit_invocation`, display name, default prompt | `tests/test_skill_metadata.py` |
| `SKILL.md` body | whenever the skill runs | the gate sentence that sends the agent to a reference file | `tests/test_references.py`, both gate wordings |
| `references/*.md` | only if `SKILL.md` says to read it and the agent complies | the contract itself, and the report-style rules | `tests/test_references.py`, byte-identity against canonical |

The consequence that drives the design: a rule requiring a reference file to be read cannot live in that reference file, because an agent that skipped the file never reaches the sentence telling it not to skip it. That one sentence is the only thing restated per skill.

## Checkpoint hook

Five files, 130 lines total, and the design point is what is absent from them.

| Path | Lines | Role |
|---|---|---|
| `hooks/checkpoint.py` | 76 | the adapter. Reads a JSON payload on stdin, applies the loop guard, emits the prompt in the shape the host expects |
| `hooks/prompts/checkpoint.md` | 11 | the prompt itself, the entire semantic content of the mechanism |
| `hooks/examples/codex.hooks.json` | 18 | host wiring example |
| `hooks/examples/claude.settings.json` | 15 | host wiring example |
| `hooks/examples/cursor.hooks.json` | 10 | host wiring example |

Execution flow, on a Stop event:

1. `load_payload` parses stdin as JSON and returns `None` on any decode failure or a non-object payload.
2. The run aborts to `{}` when the payload is `None`, when `hook_event_name` is missing or blank, or when `already_continued` is true.
3. `already_continued` is the loop guard: true when `stop_hook_active` is set, or when `loop_count` is a positive integer, or when `loop_count` cannot be read as an integer at all. Unparseable means already continued, so an unknown host field fails closed rather than looping.
4. `load_prompt` reads `hooks/prompts/checkpoint.md` relative to the adapter's own directory and returns `None` on an OSError or an empty file, which also aborts to `{}`.
5. `output_for` selects the response shape: `followup_message` for Cursor, `{"decision": "block", "reason": prompt}` for a Stop event on the other hosts, and `systemMessage` otherwise.

What the adapter never does, and this is the design rather than an omission: no roadmap discovery, no Git inspection, no timestamp comparison, no semantic completion check, no repository detection of any kind. `tests/test_checkpoint.py` asserts the absence. The reasoning is FD-D6.

The prompt carries every judgment the mechanism makes. It tells the agent to use only a pack established in the current thread, to finish without modifying files when no pack is clear or more than one is plausible or the roadmap already reflects the work, to inspect only the identified pack, that a shared working tree may hold another thread's changes, and not to commit.

`baselinedocs-setup-hooks` installs this by running its bundled `scripts/install_hooks.py`, merging the selected host's configuration rather than replacing it, and running a second time to confirm no further change. `tests/test_install_hooks.py` pins packaged asset identity, idempotence, and preservation of existing host configuration.

## Execution policy

`baselinedocs-run` ships `references/execution-contract.md`, which has no second copy anywhere because no other skill executes phases.

| Policy | Values | Effect |
|---|---|---|
| `approval_policy` | `phase`, `continuous` | pause after each phase, or continue through every ready phase, checkpointing after each |
| `commit_policy` | `none`, `per-phase` | leave changes uncommitted, or commit only that phase's files after verification and the docs checkpoint |

The selection gate requires both to be unambiguous before implementation begins, and forbids inferring either from an earlier turn. `tests/test_run_policy.py` pins it. FD-D23 records why silence is not a default.

## Pack layout on disk

```text
docs/baseline/
  baselinedocs.index.md           # initiative routing metadata
  family-design/
    family-design.introduction.md
    family-design.roadmap.md
    family-design.hallucination.md
    family-design.sourcecode.md
  skill-consolidation/
    skill-consolidation.introduction.md
    skill-consolidation.roadmap.md
    skill-consolidation.hallucination.md
    skill-consolidation.sourcecode.md
```

Every document filename is `<pack-prefix>.<document>.md`, and the prefix repeats the directory name so a file identifies its pack when it is open alone in an editor. The index sits at the initiative root beside the packs it routes, not inside either of them.

Neither pack carries a `useguide`. `README.md` is the consumer-facing surface for the family, so a `useguide` here would restate it in a file that ships nowhere. FD-D25 records that.
