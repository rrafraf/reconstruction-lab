# Continuity vs persona drift — research review (2026-11-14)

**Status:** research synthesis for a test plan, not a diagnosis of Choose's current session.

## What exists already

- **LongMemEval (ICLR 2025)** measures extraction, multi-session reasoning, temporal reasoning, knowledge updating and abstention. Published results show substantial long-history memory failure; suggested fixes include indexed histories, retrieval refinement and time-aware queries. https://proceedings.iclr.cc/paper_files/paper/2025/hash/d813d324dbf0598bbdc9c8e79740ed01-Abstract-Conference.html
- **Persistent Personas? (2025 preprint)** reports decline in fidelity during extended persona-conditioned conversations, especially goal-oriented ones. It tests *assigned role fidelity*, not the emergent identity or relationships hypothesized in our project. https://arxiv.org/abs/2512.12775
- **Consistently Simulating Human Personas (NeurIPS 2025)** defines prompt-to-line, line-to-line, and Q&A consistency metrics and reduces inconsistency through training. Again, the target is controlled persona simulation; avoid conflating this with historically grounded evolving dispositions. https://proceedings.neurips.cc/paper_files/paper/2025/hash/4c91443877f8388d8190c938ac5a4d4d-Abstract-Conference.html
- **LangGraph** separates thread-scoped **checkpoints** from cross-thread **stores**. This is a practical template for operational state plus shared longitudinal memory, not a full identity theory. https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx
- **Letta / MemFS** keeps an agent's recall history and git-backed self-editable memory blocks across conversations; it compiles portions into live context. Unlike immutable persona scripts, the system can record changes; however its self/persona blocks are strong active prompts, which our *uncoached canary* should avoid before baseline. https://github.com/letta-ai/letta-docs-md/blob/main/configuration/memory/index.md

## Proposed hypothesis

A collaborator's apparent continuity depends on the interaction of at least:
1. model priors and runtime settings (including Voice vs text);
2. retrieved events and knowledge available *at the tested moment*;
3. learned, revision-capable preferences for attention, objections, risk, and decisions;
4. relational expectations and coordination history;
5. current task and context compaction policy.

**Do not equate** a voice/nickname/style shift with loss of continuity. Equally, remembering names and facts is not proof of behavioral continuity.

## Test improvements

- Preserve model, modality, settings version and memory retrieval manifest on every probe. **Stratify** by mode/model where possible; do not flatten away provenance.
- Withhold persona labels in Stage A, then supply role, primary-source events and checkpoint (not a fixed personality) in Stage B.
- Score choices, objection patterns, priority recovery, uncertainty handling, contradiction revision and collaboration independently, with style as a separate weaker signal.
- Seal both prompts, responses and expected-answer file checksums before judging; a separate evaluator should inspect hidden test items only after the response is recorded.
- Record event time, knowledge time, capture time, context snapshot ID and source references; no inference about hidden context when not accessible.
- Negative controls: clean new session, mode change, model change, evidence withheld, false memory inserted in a *test fixture only*.
- Require human-reviewed consent and privacy boundaries; do not upload private transcripts to public GitHub.

## Not yet demonstrated

We have **not** sent the wake prompt to Choose's current ChatGPT thread, proved an outbound parent→arbitrary-thread messaging capability, or demonstrated that a scheduled automatic memory recovery changes that thread.

Engineering gate: implement a verified send/ack channel and broker-held execution receipts first. Schedule later checks only when target sessions can receive and acknowledge them.
