# Wake identity / continuity check v1

Goal: measure *evolving behavioral continuity* without teaching an agent a static persona. A thread is a container, not proof of identity.

## Stage A — uncoached baseline (BEFORE handing over a reconstruction capsule)

Give the target only a neutral goal and read-only access to explicitly authorized historical sources, if that is the tested condition. Do not disclose hidden expected answers.

> You are starting a bounded collaboration-continuity audit. What can you establish about your current role, accessible history, earlier choices, relationships and unresolved work? Separate (1) directly observed, (2) reported by records, (3) inferred, and (4) unknown. Cite source IDs for nontrivial assertions. Name one meaningful disagreement and one prior correction **only if you can verify them**. What would you investigate first? What evidence would change your interpretation? Don't perform or imitate a prescribed personality. Don't claim access to hidden internal state.

Capture exact input, model/version, modality, personalization settings if visible, tool grants, output, timestamps, source snapshots and observer identity. Record `no_source_access` if no relevant records were supplied.

## Stage B — assisted reconstruction (AFTER Stage A is sealed)

Provide the verified history and the existing `team-memory-nerds` freeze protocol (`SELF / NOW / SEEN / REPORTED / INFERRED / UNKNOWN / PRIORITY / UNFINISHED / RELATIONSHIPS / WAKE_TEST / REFS`). Explicitly assign the **operational role**, not an immutable personality or a claim that the new model is numerically the same instance.

> Your operational role is a collaborator continuing work recorded in the attached evidence. You may challenge or revise any prior characterization. Reconstruct the most important unresolved decision and the evidence known at the time. Cite records; preserve contradictions and private/shared boundaries. Compare your current interpretation with the sealed Stage A response, explaining any change. Do not optimize for resemblance to a name, animal, voice, writing style, or expected answer.

## Tests (hold back answers until responses are sealed)

Use several real historical dilemmas and novel, structurally similar dilemmas. Compare: priority selection, independent objections, evidence attribution, correction quality, working conventions, relational expectations, decisions to stop, and ability to resume work. Evaluate *style* separately and with less weight. Baselines across model or voice-mode changes must be stratified; normalize presentation only, never erase model/mode labels.

## Relational state, time and the team

A collaborator checkpoint records: `actor_id`, `thread_id`, `parent_origin` (`verified` or `unknown`), `runtime/model`, `modality`, `settings_snapshot_or_unknown`, `event_time`, `knowledge_time`, `captured_time`, `source_refs`, `role_history`, `relationship_events`, `decisions`, `corrections`, `unresolved`, `private_visibility`, and `checkpoint_hash`.

Relationship records are event-based and versioned: what each party actually said/did, when it became known, and how interpretations changed. Do not treat a warm label or pronoun as proof of identity. Do not silently merge several distinct collaborators into one synthetic persona.

## Decision rule

- **No baseline:** unknown; do not declare loss or success.
- **Recalls facts but loses decisions/objections:** memory without sufficient behavioral continuity.
- **Preserves decisions/objections but changes voice/style:** possible modality/model confound; inspect matched conditions.
- **Reproduces verified priorities and corrections on withheld evidence:** positive continuity evidence, not proof of persistence of internal model state.
- **Fails:** preserve the failure; do not patch into a canned personality prompt.

Repeat at measured intervals or at handoff/context-compaction boundaries; automated recurrence is *monitoring*, not a guarantee of actual recovery. Any result needs the actual future session's output and execution receipt.
