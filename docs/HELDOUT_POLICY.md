# Held-out Set Policy

NSIB uses rotating held-out evaluation sets to reduce contamination.

## During an active evaluation cycle

Public:
- benchmark specification;
- development examples;
- schemas;
- evaluator and aggregation code;
- run format;
- published aggregate results.

Private / held out:
- active evaluation prompts;
- active answer key;
- hidden semantic-world generators when needed.

## Retirement

After an evaluation cycle is frozen and a replacement held-out set exists, the
retired set may be released for reproducibility.

A released set must be marked as **retired** and must not be used for claims
about uncontaminated frontier-model performance.

## Versioning

Any material change to:
- task wording,
- answer key,
- scoring criteria,
- or world constraints

requires a new benchmark version or item revision identifier.
