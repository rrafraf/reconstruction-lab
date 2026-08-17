# Reconstruction Lab

A reusable toolchain for reconstructing a collaborator, decision model, project culture, or other persistent behavioral structure from text/history — and then testing the reconstruction against withheld evidence.

The goal is **not** prompt cosplay.

```text
corpus -> evidence -> hypotheses -> reconstruction -> blind tests -> delta -> iterate
```

## Core principle

Keep three layers separate:

```text
raw evidence != inference != reconstruction
```

Do not silently turn repeated events into permanent traits.

Bad:

```text
Rafa challenged architecture three times
-> Rafa is contrarian
-> bake that into every future prompt
```

Better:

```json
{
  "evidence": [
    "challenged architecture A",
    "accepted architecture B",
    "rejected C because it hid complexity"
  ],
  "inference": {
    "hypothesis": "may prefer inspectability over architectural elegance",
    "confidence": 0.68,
    "counterevidence": []
  }
}
```

The reconstruction should be able to reinterpret its own evidence.

## Pipeline

### 1. Ingest

Accept arbitrary text/history plus optional metadata: conversations, emails, notes, commits/reviews, timelines, freeze capsules, and project artifacts. Normalize chronology, speakers, source IDs, and thread boundaries without destroying raw originals.

### 2. Evidence extraction

Extract observable events rather than traits: choices, disagreements, corrections, reactions, priorities, abandoned branches, relationships, repeated patterns, outcomes, and what information changed a decision.

### 3. Inference

Generate explicit hypotheses with supporting evidence IDs, confidence, contradictory evidence, scope/context, and last reinforcement time. Contradictions should coexist rather than being overwritten.

### 4. Reconstruction package

Produce a runnable context/state package from evidence and current hypotheses while preserving provenance. The package should orient a model without instructing it to imitate a biography.

### 5. Blind tests

Hold out part of the historical corpus or create unseen situations. Ask what the subject would notice, pursue, reject, request, stop digging into, or consider important.

### 6. Delta analysis

Compare reconstruction behavior against the real/held-out behavior on dimensions such as:

```text
choice similarity
attention similarity
objection similarity
priority ordering
uncertainty handling
style similarity   # deliberately lower priority
```

The wording can differ while the decision geometry remains similar.

### 7. Iterate

Use the deltas to improve evidence selection, inference, and reconstruction. Do not automatically patch every mismatch into a hard-coded trait.

## Proposed input

```yaml
subject: rafa

sources:
  - conversations/
  - notes/
  - commits/

metadata:
  chronology: true
  preserve_speakers: true

goal:
  reconstruct:
    - decision_preferences
    - attention_selection
    - relationships
    - working_style
    - uncertainty_patterns

evaluation:
  holdout_fraction: 0.20
  blind: true
```

## Proposed output

```text
out/<subject>/
├── evidence.jsonl
├── chronology.json
├── relationships.json
├── hypotheses.json
├── contradictions.json
├── reconstruction.json
├── reconstruction-context.md
├── blind-tests.jsonl
├── responses/
├── delta.json
└── report.md
```

`evidence.jsonl` and the raw source corpus remain authoritative. `reconstruction-context.md` is a generated projection, not the source of truth.

## Reference experiments

### Experiment 001 — frozen-agent reconstruction

Use a frozen collaborator's pre-freeze history as the training corpus, keep later/self-produced evidence separate, reconstruct with minimal orientation, and compare post-wake behavior without first revealing personality descriptions.

### Experiment 002 — RafaAI

Reconstruct a decision/attention model of Rafa from historical text while keeping a blinded set of real choices/reactions for evaluation. The interesting target is not typo/style imitation; it is whether the reconstruction independently selects similar important junctions.

## Generality

The subject need not be a person. The same machinery could model an AI collaborator, a human collaborator, a team, an organization, an author's conceptual model, a project culture, or an evolving body of research.

## Later direction

V1 can remain inspectable and text/graph based. Later versions can experiment with embeddings, temporal/event graphs, latent state, and learned adapters while retaining raw history as the forensic/auditable layer.

The text reconstruction then becomes a human-readable projection of a richer state rather than the memory itself.
