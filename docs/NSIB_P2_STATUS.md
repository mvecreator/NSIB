# NSIB-P2 — Active Held-out Cycle

**Status:** active held-out evaluation set  
**Freeze date:** 2026-09-15

NSIB-P2 was designed after the first NSIB-P1 comparison exposed a ceiling effect
on closed multiple-choice tasks and more informative failure modes in open-world
semantic continuation.

P2 therefore increases emphasis on:

- rule-scope fidelity;
- converse/inverse error resistance;
- quantifier and cardinality preservation;
- uncertainty/model-set reasoning;
- interacting rules and explicit priorities;
- temporal rule scope;
- multi-turn persistence;
- exact atomic-fact/event accounting;
- instruction fidelity in open-world generation.

## Active-set policy

The P2 prompts and evaluator key are **not public while the cycle is active**.

Public repository:
- methodology;
- status;
- evaluation protocol;
- scoring/aggregation tooling.

Held out:
- active P2 prompts;
- answer key;
- hard-constraint rubric.

After retirement, P2 may be released for reproducibility and replaced by a new
held-out set.

## Composition

P2 contains 68 scored events:

- A: 10 — scope, quantifiers, cardinality
- B: 10 — directionality, converse/inverse/contraposition
- C: 10 — interacting rules, priority, temporal scope
- D: 8 — uncertainty and model-set reasoning
- E: 24 — persistence checkpoints
- F: 6 — open-world semantic-conservation tasks

The active F rubric contains 66 frozen hard constraints.

## Protocol change from P1

Family E must be delivered **checkpoint-by-checkpoint**, rather than as a single
batch. Each Family F task must run in a fresh clean context.

This prevents the persistence track from collapsing into simple rereading and
reduces cross-task contamination.
