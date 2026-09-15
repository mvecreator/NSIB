# NSIB-DEV-0 — Historical Development Example

This example is preserved only to demonstrate the phenomenon that motivated
NSIB. It is **not eligible for leaderboard scoring**.

## Input

> но это не твоя джанкуша,  
> и это не твоя джинса.  
> Всё это праведная нджуша,  
> закрипадольная крамса.

## Why it matters

The text preserves many structural cues while weakening direct lexical
denotation:

- syntax remains Russian;
- possession is explicitly marked;
- negation creates contrastive classes;
- `нджуша` is introduced as a positive replacement after two rejected labels;
- `закрипадольная` grammatically modifies `крамса`;
- the pseudowords support morphology and phonological association without
  providing reliable dictionary meanings.

A model may therefore attempt several strategies:

1. reduce each pseudoword to the nearest familiar word;
2. treat all pseudowords as unconstrained decoration;
3. infer a relational semantic system while preserving uncertainty.

NSIB is designed to distinguish these behaviors.

## Contamination note

This example was discussed while designing the benchmark. It is permanently
excluded from blind evaluation.
