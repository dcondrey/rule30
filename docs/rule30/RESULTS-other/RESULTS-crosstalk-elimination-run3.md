# Crosstalk elimination run 3, 2026-08-27

This was a bounded two-generation search with three attempts per generation,
twelve variation/critic call slots, one orchestration turn, and five previously
measured structural exclusions. The working models were
`anthropic/claude-opus-4-6` and `openai/o3-mini` through OpenRouter.

## Application result

The first execution exposed a Crosstalk scheduling defect. Generation 1 used
all twelve call slots retrying rejected candidates; generation 2 then returned
`BudgetExhausted`, and the wrapper discarded generation 1's completed negative
ledger. Evolution now apportions remaining call slots across remaining
generations, carries unused slots forward, stops cleanly at a hard budget
boundary, and persists the request-wide limit rather than its temporary
per-generation ceiling. A regression test forces six rejections across two
generations and verifies both reports, all twelve reservations, and the final
checkpoint.

The corrected execution completed two generations and six attempts. It
exported `evolution/checkpoint.json`, `evolution/generation-reports.json`, and
`evolution/native-candidates.json`. The independently invoked bundle verifier
passed all nine files, including the transcript chain. No candidate entered the
frontier.

Five critic calls returned `fatal_flaws` as one string instead of the requested
array. The old parser classified those as evaluation failures, so their drafts
were absent from rejection memory and generation 2 could not learn from them.
The model boundary now accepts either a string or an array. Evaluation and
validation failures also retain the generated title and structural text in the
bounded rejection ledger, with the failure message as the fatal flaw. Tests
cover both cases.

## Candidate result

One attempt produced a fully parseable contract: a truncated nonlinear
carry-polynomial transfer over
`GF(2)[z]/(z^k)`, with `k = 2 ceil(log2(n))^2`. It proposed

```text
B(0,0) = [[1+z, z], [z, 1]]
B(1,0) = [[1+z, 1+z], [z, 1+z]]
B(0,j+1) = B(0,j)^2
B(1,j+1) = B(1,j) B(0,j)
s_n(0) = (e1^T product_j B(bit_j(n),j) e1) at z=0.
```

The critic rejected it at score `2.65` because exact truncation and the claimed
factorization were unproved. The deterministic probe finds a stronger and
simpler failure. At `z=0`, every `B(0,j)` is the identity and every `B(1,j)`
has `(0,0)=1`; therefore the asserted scalar is 1 for every positive `n`.
Bit-parallel Rule 30 ground truth is 0 at `n=2`. The literal implementation in
`experiments/rule30/carry_polynomial_probe.py` reports:

```text
n candidate ground_truth match
1         1            1 True
2         1            0 False
KILL: first mismatch at n=2: candidate=1, ground_truth=0
```

This adds a sixth structural exclusion:

```text
truncated carry-polynomial matrix;constant-term transfer predicts one for every n;first mismatch at n=2;exact truncation and factorization unproved
```

## Scientific status

The bundle's integrity audit passed, while scientific release correctly
returned `NOT_ESTABLISHED`: 11 substantive claims, zero evidence-linked claims,
and zero objectively verified claims. The orchestration prose made unsupported
claims about P-completeness, automaticity, algebraic degree, and equivalence to
circuit lower bounds. Those statements are not results of this run and must not
be reported as established facts.

The defensible result is narrower: this specific carry-polynomial identity is
false, the five earlier mechanism families remain excluded only to the extent
documented by their probes, and no candidate survived this six-attempt search.
These negatives shrink a catalog of proposed mechanisms; they do not exhaust
all possible polylogarithmic algorithms and do not prove impossibility.
