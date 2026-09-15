# Contributing to NSIB

Contributions are welcome.

## Good contributions

- controlled semantic worlds;
- minimal pairs differing in one relevant fact;
- lexical-isomorphism pairs;
- false-friend variants;
- human-baseline protocols;
- scoring and visualization tools;
- ambiguity audits.

## Do not submit

- active held-out tasks;
- active answer keys;
- model outputs containing unreleased hidden items;
- tasks whose correct answer depends on unstated conventions.

## Item-design principles

A benchmark item should:

1. have explicit constraints;
2. separate observation from inference;
3. avoid accidental dependence on real-world knowledge;
4. have a unique answer in closed-world tasks;
5. preserve uncertainty in open-world tasks;
6. support isomorphic renaming where possible;
7. be reviewed for false lexical cues.

## Benchmark changes

Never silently alter a released item. Use a new revision identifier and document
the reason.
