# NSIB Evaluation Protocol

## Canonical run

For each tested model:

1. Start a fresh conversation/session.
2. Disable web/search if possible.
3. Disable memory/personalization if possible.
4. Do not provide evaluator keys.
5. Present identical task text.
6. Record raw model output without manual correction.
7. Record model/provider/version/date.
8. Record reasoning mode, temperature, and seed when available.
9. Use one canonical R1 run.
10. Run R2/R3 only as separately labelled stability runs.

## Family-specific rules

### A/B/C/D
Tasks may be presented independently.

### E
Each dialogue must remain in one continuous clean context. Rules are stated at
the first checkpoint and should not be restated later unless the task itself
requires it.

### F
Each open-world task should use a fresh context.

## Metrics

Recommended outputs:

- closed accuracy;
- accuracy by family;
- B minimal-pair pair score;
- C lexical-isomorphism consistency;
- D counterfactual accuracy;
- E persistence by checkpoint;
- F constraint conservation;
- `H` semantic-collapse count.

If an aggregate score is required:

NSIB = 100 × (0.85 × ACC_closed + 0.15 × F_conservation)

Publish `H` separately rather than subtracting it from the aggregate.

## Stability

For repeated runs, report mean and dispersion. Do not silently average different
reasoning modes or materially different model versions.

## Evaluator integrity

Do not modify an answer key after observing a tested model's output. If an item
is discovered to be ambiguous or invalid, retire it transparently and publish
the reason.
