# Baseline Docs Workflow Design

## Decision Summary

This version separates deliberate user workflow starts, one-time administration, and lifecycle behavior that an agent can select automatically.

| Concern | Decision |
|---|---|
| Skill overload | Expose three primary user entrypoints and visually label lifecycle skills as internal |
| Brownfield capture | Add `baselinedocs-save` |
| Long-running execution | Add `baselinedocs-run` with phase checkpoints |
| Context compaction | Add advisory Stop hooks and an optional strict gate |
| Hook administration | Add an explicit per-repository setup skill that safely merges host configuration |
| Pack bloat | Store outcomes and material failures, not attempt history |
| Inconsistent formatting | Add schema, status, date, and code provenance frontmatter |
| Reusable knowledge | Add a separate wiki extraction workflow |
| Redundant useguide | Make it a conditional consumer-contract extension |
| Post-initial feedback | Reopen or revise phases before creating new ones |
| Multi-domain chains | Use a directly linked initiative index and dependency graph |

## Trigger Architecture

Codex supports explicit and implicit skill invocation and allows `agents/openai.yaml` to disable implicit invocation per skill. The three user entrypoints and the one-time `baselinedocs-setup-hooks` utility set `allow_implicit_invocation: false`. Lifecycle skills keep it enabled.

This policy does not hide internal skills from every picker and is not a portable Agent Skills field. Therefore:

- UI names mark helpers as `Baseline Docs Internal: ...`
- descriptions state automatic trigger contexts
- the README teaches only the three entrypoints
- hook administration is documented separately as a one-time utility

This is progressive disclosure rather than a claim that every host can maintain two physically separate skill registries.

## Pack Schema

Schema `2.0` changes the fixed five-file contract into a three-core plus two-extension contract.

Core:

- introduction
- roadmap
- hallucination

Conditional:

- sourcecode
- useguide

The transition is additive. Existing five-file packs remain valid. Agents should not delete an existing extension simply because a new pack would omit it.

## Frontmatter Semantics

`updated` records the document edit date. `code_ref` records the code state inspected while writing.

The document cannot reliably contain its own Git commit hash because changing the file changes the commit. Therefore `code_ref` is code provenance, not the document commit. Drift audits compare later scoped code changes against the claim body before declaring drift.

## Checkpoint Model

A semantic checkpoint belongs in the roadmap and contains:

- phase outcome and status
- final evidence
- affected files
- open risk
- exact next action

Hooks cannot safely infer business outcomes from a diff. They only detect a likely missing checkpoint and return model-visible guidance. The default hook is advisory and avoids endless continuations by honoring each host's stop-loop marker. Strict mode is opt-in because blocking automatic compaction can interrupt a request near its context limit.

## Evidence Retention

Keep:

- final passing or failing result supporting current status
- unresolved failures
- failures that explain a changed design
- reproduction details for an active defect

Discard from active docs:

- routine failed fixture iterations
- repeated commands with the same meaning
- transient syntax or setup mistakes already resolved
- chat chronology that does not affect current truth

External raw logs may still be linked when auditability requires them.

## Useguide Role

`useguide` means a consumer contract. Valid forms include:

- API request and response behavior
- method or library usage
- migration or conversion procedure
- operator workflow
- black-box behavior needed by another team

If no consumer exists, omit the file. Reusable procedures that apply across tasks should move to the wiki.

## Loop Engineering

`baselinedocs-run` has no silent execution-policy defaults. Before implementation, it asks for any missing `approval_policy` and `commit_policy`. Selecting `per-phase` in the user's reply is explicit commit authorization for that run.

After initial completion, feedback is assigned to the phase whose acceptance criteria it refines. A new phase requires a new outcome, dependency, release gate, deployable unit, or independently reviewable body of work.

## Multi-Pack Routing

An initiative index is routing metadata:

- direct child-pack links
- domain scope
- dependency edges
- current cross-pack checkpoint

It is not a general introduction or roadmap that duplicates child content. This keeps every sub-pack directly queryable while preserving cross-domain order.

## Deferred Work

- Package-level installation profiles could hide internal helpers more completely, but Skills.sh does not currently provide a portable hidden-skill category.
- Organization-wide hook rollout remains deferred. The setup skill handles one repository at a time and preserves unknown configuration rather than replacing it.
- Automated semantic doc writing from transcripts is intentionally rejected until a trustworthy evidence extraction and review gate exists.

## Research Basis

- [OpenAI Codex skills](https://developers.openai.com/codex/skills): explicit and implicit invocation plus `allow_implicit_invocation`
- [OpenAI Codex hooks](https://developers.openai.com/codex/hooks): project hook discovery, trust review, Stop, and compaction events
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks): Stop, task, and compaction lifecycle behavior
- [Cursor agent best practices](https://cursor.com/blog/agent-best-practices): dynamic skills and the `stop` continuation pattern
- [Skills.sh CLI](https://www.skills.sh/docs/cli): installation and discovery surface
