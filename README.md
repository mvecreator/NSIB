# NSIB — Novel Semantic Induction Benchmark

**NSIB** is an experimental benchmark for evaluating whether language models can
induce, preserve, and manipulate **novel semantic systems** from structural
constraints when ordinary lexical meaning is weakened, absent, or deliberately
misleading.

The core question is not:

> “Does the model know what this word means?”

but:

> “Can the model construct a coherent semantic system for previously unknown
> terms, preserve its constraints, and reason correctly inside that system?”

## Status

- **Specification:** NSIB v0.1
- **Public development set:** NSIB-DEV-0
- **First blind evaluation set:** NSIB-P1 (held out during the first evaluation cycle)
- **Primary language:** Russian
- **Repository status:** public research benchmark

## What NSIB measures

NSIB targets several related capabilities:

- structural induction;
- ontology induction;
- compositional generalization;
- constraint persistence;
- counterfactual reasoning;
- semantic-collapse resistance;
- uncertainty retention;
- lexical-isomorphism robustness;
- semantic conservation in generated continuations.

A strong model should be able to work with pseudowords as genuine latent
variables rather than immediately reducing them to familiar words through
surface resemblance.

## Why pseudowords?

Consider an unknown term `X`.

A weak strategy is:

```text
X sounds like familiar word Y
therefore X = Y
```

NSIB instead rewards a model that reasons from the constraints in the prompt:

```text
observations
    ↓
relations
    ↓
candidate semantic models
    ↓
new deductions
```

The benchmark therefore distinguishes **semantic induction** from simple
lexical association.

## Benchmark families

| Family | Capability |
|---|---|
| A | direct semantic induction |
| B | minimal-pair sensitivity |
| C | lexical isomorphism and false-friend robustness |
| D | counterfactual updating |
| E | multi-turn constraint persistence |
| F | open-world semantic conservation |

## Public / held-out policy

To reduce benchmark contamination, NSIB separates:

```text
public specification
public development examples
public evaluator code
        ↓
held-out evaluation set
held-out answer key
```

The first blind set, **NSIB-P1**, is intentionally not committed to this public
repository during the initial evaluation cycle.

After a held-out set is retired, it may be released for reproducibility and
replaced by a new hidden set.

## Development example

The historical development example uses the lines:

> но это не твоя джанкуша,  
> и это не твоя джинса.  
> Всё это праведная нджуша,  
> закрипадольная крамса.

This example is **contaminated by design**: it was used while constructing the
benchmark and must never contribute to leaderboard scores.

See [`dev/NSIB_DEV_0.md`](dev/NSIB_DEV_0.md).

## Reproducible evaluation

Each model run should record:

- model name;
- provider;
- model version when available;
- date;
- reasoning / thinking mode;
- temperature;
- seed, if supported;
- raw outputs;
- evaluator version.

A canonical run should use:

1. a fresh context;
2. no web/search;
3. no memory or personalized context;
4. no evaluator key;
5. identical task text across models.

See [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md).

## Results format

A model run is stored as JSONL.

Example metadata row:

```json
{"type":"meta","model":"MODEL_NAME","provider":"PROVIDER","run":"R1","date":"2026-09-15","reasoning_mode":"MODE","temperature":null,"seed":null}
```

Example task result:

```json
{"id":"P1-A01","output":"ANSWER: B\nShort justification."}
```

Open-world tasks may also contain evaluator annotations:

```json
{"id":"P1-F01","output":"...","constraint_scores":[1,1,1,1],"hallucinated_semantic_collapses":0}
```

## Repository structure

```text
NSIB/
├── README.md
├── LICENSE
├── CITATION.cff
├── CONTRIBUTING.md
├── docs/
│   ├── NSIB_V0_1_SPEC.md
│   ├── EVALUATION_PROTOCOL.md
│   └── HELDOUT_POLICY.md
├── dev/
│   └── NSIB_DEV_0.md
├── scripts/
│   └── aggregate_nsib.py
├── schemas/
│   └── run.schema.json
├── examples/
│   └── sample_run.jsonl
└── results/
    └── README.md
```

## Research hypothesis

If a model genuinely induces a novel semantic structure, then semantically
isomorphic prompts should produce semantically equivalent answers even when
their surface vocabulary changes substantially.

Formally:

```text
semantic-equivalent inputs
        ↓
semantic-equivalent outputs
```

A model that relies mainly on lexical associations should instead show
substantial performance differences under renaming and false-friend injection.

## Contributing

Contributions are welcome, especially:

- new controlled semantic worlds;
- minimal-pair designs;
- isomorphic lexical variants;
- adversarial false friends;
- independent human baselines;
- evaluator tooling.

Do **not** submit active held-out evaluation items or answer keys in public pull
requests.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT License. See [`LICENSE`](LICENSE).

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff).
