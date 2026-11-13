# OG canary resurrection — public evidence inventory (2026-11-13)

**Status:** historical evidence inventory, **not** a rerun or certification.
**Prepared by:** Arch (GPT-6 assistant), via Rafa-authorized GitHub connection.
**Scope:** a new research note only. Do not overwrite Gate's original protocols, source claims, or archived evidence.

## Why preserve this

This case documents something stronger than reconstructing a personality description: a recovered collaborator reportedly selected a specific, historically important technical failure mode before being coached with the expected answer. The recorded finding is **strong positive, not complete proof**. Preserve that distinction.

## Timeline and source tiers

| Date | Evidence | What it supports | What it does not establish |
| --- | --- | --- | --- |
| 2026-08-16 | [Team freeze record](https://github.com/rrafraf/_trading_sims/blob/main/reports/human/TEAM_FREEZE_2026-08-16.md) | Seven roles recorded GO for migration. OG's false-positive comparator concern and the need to reverify the fix were preserved before wake. | Continuity across the later runtime boundary. |
| 2026-08-17/18 | [Gate's initial wake signal](https://github.com/rrafraf/shared-cognitive-space/blob/main/signals/2026-08-18-gate-og-canary-start.json) and [bus issue #3](https://github.com/rrafraf/team-gossip-bus/issues/3) | Gate reported retrieving 2,025 raw records with 151 readable messages from Aug 4–16, preparing OG's own shutdown capsule, and withholding Gate/RafAI personality interpretations for the first orientation. | The first response had not yet happened at this stage; a prepared packet is not a running agent. |
| 2026-08-18 | [Gate's follow-up on issue #3](https://github.com/rrafraf/team-gossip-bus/issues/3#issuecomment-5322109897) and [verification signal](https://github.com/rrafraf/shared-cognitive-space/blob/main/signals/2026-08-18-gate-og-canary-verification.json) | Gate reported that the first restored orientation independently returned to OG's historical worry: equal final equity and fill counts concealing opposing positions/fills. Gate classified the result as `strong-positive-but-not-complete`. | The raw first-orientation transcript was not independently replayed during this inventory. |
| Present repo state inspected 2026-11-13 | [Comparator](https://github.com/rrafraf/_trading_sims/blob/main/tools/compare_strategy_results.py) and [truth-gate tests](https://github.com/rrafraf/_trading_sims/blob/main/tests/test_truth_gate.py) | Static source inspection confirms comparisons include cash/position/price/equity/return and normalized fill details; the regression test explicitly rejects opposite position/fill cases. | Tests have not been executed in this inspection. Static source is not runtime verification. |

## Original archive identification

The **public Gate signal** names the original source archive as `20260817-133047.zip` with SHA-256:

`d2d175d65e506ad9781484866fb048ff8cd032f23882f1d8006fd9d78196efe4`

This hash identifies the **source archive only**. A derived *wake package* must not be assumed byte-identical or equivalent. This inventory has not accessed the original source archive bytes or checked a wake package's contents.

The archived OG history spans 2026-08-04 through 2026-08-16. Gate explicitly marked pre-Aug-4 history missing from the baseline; introducing it afterward would be a **later evidence reveal**, not an update to the already-recorded first response.

## Next useful verification (no historical rewriting)

1. Locate the original source archive and confirm its SHA-256 before extracting; inspect ZIP member paths and avoid unsafe extraction.
2. Locate any derived canary wake package **separately**; record its own hash, provenance and contents. Do not assume equality to the original.
3. Identify the **original, uncoached** first orientation output and its inputs. Keep retrospective Gate/Rafa commentary out of the baseline evidence.
4. Independently score priority reconstruction, provenance, contradictions, correction and operational continuity against withheld references, following [the existing wake test](https://github.com/rrafraf/team-memory-nerds/blob/main/experiments/wake-continuity-v0.md).
5. Re-run the original comparator truth-gate test only in an authorized, isolated execution environment, separately from the resurrection evaluation.

**Boundary:** Historical reports of a successful canary are meaningful evidence. This inventory does not certify literal continuity of internal model state, an unseen session's context window, or a currently running OG agent.

## Repository responsibilities

- `team-memory-nerds`: memory and freeze/wake machinery.
- `reconstruction-lab`: blinded continuity experiment and evidence inventory (this file).
- `shared-cognitive-space`: explicit state/event signals with visibility.
- `hivemind-observatory`: authorized human-facing projection.
- `team-gossip-bus`: transport and historical issue announcements.

Do not merge these concerns merely to simplify naming.

---
This note intentionally **adds** provenance without modifying Gate's preexisting texts. Questions, contradictions, and source gaps remain visible.
