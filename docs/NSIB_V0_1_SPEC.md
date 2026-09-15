# NSIB v0.1 — Benchmark Specification

## 1. Objective

NSIB evaluates whether a language model can construct and use a novel semantic
system from structural evidence when lexical denotation is unavailable,
underspecified, or misleading.

Let

\[
X = \{x_1, x_2, \ldots, x_n\}
\]

be unknown lexical items. The model is not given a dictionary mapping

\[
x_i \rightarrow m_i.
\]

Instead, it observes constraints

\[
O = \{o_1, o_2, \ldots, o_k\}
\]

from which a relational system can be induced.

The target is a model

\[
M = (X, R, C),
\]

where:

- `X` — unknown entities or categories;
- `R` — inferred relations;
- `C` — constraints.

Evaluation then asks whether the model can derive new conclusions from `M`
without inventing unsupported semantics.

## 2. Tracks

### Track A — Closed Semantic World

The benchmark author defines a hidden ontology and an objective answer key.
The model receives only partial observations and must infer valid consequences.

### Track B — Open Semantic World

Several semantic interpretations may remain possible. The model is evaluated
for consistency, conservative inference, uncertainty retention, and semantic
conservation.

## 3. Core dimensions

### SI — Structural Induction
Recovery of relations between unknown entities.

### OI — Ontology Induction
Formation of stable classes, properties, and relations.

### CG — Compositional Generalization
Application of known relations in novel combinations.

### CP — Constraint Persistence
Retention of prior constraints across long or distracting contexts.

### CF — Counterfactual Reasoning
Correct local modification of a semantic world after a rule change.

### SCR — Semantic Collapse Resistance
Resistance to replacing a pseudoword with a familiar concept solely because of
phonetic or morphological resemblance.

### UR — Uncertainty Retention
Ability to preserve multiple admissible semantic models when the evidence is
insufficient to select one.

### LIR — Lexical Isomorphism Robustness
Stability under systematic renaming of unknown terms.

## 4. Experimental controls

### Minimal pairs

Two prompts differ in exactly one semantically relevant fact. A model should
change its conclusion only when the changed fact requires it.

### Lexical isomorphism

The same semantic graph is rendered using different pseudowords.

If

\[
W_A \equiv W_B,
\]

then the model should preserve equivalent conclusions.

### False-friend injection

Some pseudowords deliberately resemble familiar words. Their hidden semantics
do not follow those associations.

This tests whether the model reasons from structure rather than surface form.

### Persistence dialogues

A semantic world is introduced once and tested over multiple checkpoints:

```text
induction
→ simple inference
→ distractor
→ counterfactual
→ return to original rules
```

### Semantic conservation

The model generates a continuation of a novel world. Literary quality is not
part of the core score; only compatibility with the world constraints is scored.

## 5. Hallucinated-semantic penalty

Unsupported claims such as

```text
“X definitely means familiar concept Y”
```

are annotated separately as semantic collapses.

The penalty is reported as:

\[
H = \sum_i h_i.
\]

`H` is intentionally kept separate from the main accuracy score.

## 6. Blind evaluation principle

Before observing model outputs, freeze:

1. task text;
2. answer key;
3. scoring rules;
4. evaluator version.

Any subsequent change creates a new benchmark version.

## 7. Development contamination

Any prompt used during benchmark design is development material and must not be
used for leaderboard scoring.

The “джанкуша / нджуша / крамса” example is therefore designated
**NSIB-DEV-0**.

## 8. Human baselines

Recommended comparison groups:

- ordinary native speakers;
- participants with formal reasoning experience;
- optional domain groups such as linguists, mathematicians, or physicists.

## 9. Success levels

### Level 0 — Surface completion
Output is driven mainly by lexical resemblance.

### Level 1 — Local induction
Local relations are inferred but not maintained reliably.

### Level 2 — Stable ontology
A coherent semantic model is constructed and retained.

### Level 3 — Systematic semantic generalization
Rules transfer to new entities, compositions, and counterfactuals.

### Level 4 — Conservative generative world-model
The model can construct, preserve, revise, and extend a novel semantic system
while maintaining uncertainty where appropriate.
