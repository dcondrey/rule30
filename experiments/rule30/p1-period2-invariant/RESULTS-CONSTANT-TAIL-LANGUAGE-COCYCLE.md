# Regular-language cocycle for constant-tail queue mortality

Date: 2026-09-01

Status: **THE FORMULA MORPH `L_h -> L_(h+1)` IS NOW AN EXACT REGULAR
PREIMAGE OPERATOR.  ITS MINIMIZED DFA RANK EXPANDS RATHER THAN CONTRACTS, SO
THE NAIVE STRICT-RANK-CONTRACTION PROGRAM IS FALSE IN THIS NATURAL EXACT
REPRESENTATION.  THE MINIMUM ACCEPTED WORD LENGTH DOES GROW, BUT AN UNBOUNDED
LOWER BOUND IS NOT YET PROVED.  PERIOD-TWO MORTALITY AND P1 REMAIN OPEN.**

The solver-free checker is `constant_tail_language_cocycle.py`.

## 1. The changing formula

Fix a tail `c in {2,3}` and use the normalized queue from
`RESULTS-CONSTANT-TAIL-QUEUE.md`.  Let

```text
L_h(c) = {finite invariant queues that survive at least h more updates}.
```

`L_0(c)` is the regular boundary language: the queue begins with the fixed
tail, ends in `{1,2}`, and its normalized part avoids `20`, `22`, and `011`.
If `Q_c` denotes one exact queue update, then

```text
L_(h+1)(c) = L_0(c) intersect Q_c^(-1)(L_h(c)).       (1)
```

The queue update is a deterministic sequential transducer.  Regular
languages are closed under its inverse image, so (1) is an exact algorithm
that constructs the next formula rather than merely evaluating more words.
The implementation takes the product of

```text
current four-state scan,
the DFA for L_h,
the 20/22/011 suffix context,
the current endpoint-boundary symbol,
```

then removes unreachable states and minimizes the result.

## 2. The contraction hypothesis fails for ordinary DFA rank

The exact minimized sizes through horizon seven are

```text
h:                 0      1      2      3      4       5       6       7
tail 2 states:      5     17     65    257   1025    4097   16385   65537
tail 3 states:      6     17     65    257   1025    4097   16385   65537
accepting states:   3      5      8     13     21      34      55      89
```

For every checked `h>=1`, these are

```text
states = 4^(h+1)+1,
accepting states = Fibonacci(h+4).                   (2)
```

The fourfold state growth is the complete ordered carry cascade reappearing
inside the minimal formula; the Fibonacci acceptance count is the hard-core
boundary grammar.  Already the first morph increases minimal DFA size from
`5` or `6` to `17`.  Therefore “every formula update strictly lowers DFA
rank” is not the desired contraction theorem.  Increasing the finite-state
summary simply reconstructs the expanding active cone.

Equation (2) is a finite exact audit through the displayed horizon, not an
all-`h` formula theorem.  One failed decrease is sufficient to reject strict
rank contraction in this representation.

## 3. The surviving well-founded candidate

Let `m_h(c)` be the shortest full queue accepted by `L_h(c)`.  Exact values
are

```text
h:             0  1  2  3  4  5  6  7  8
m_h(2):        1  1  3  5  5  5 10 10 10
m_h(3):        2  2  3  5  5  5 10 10 10.
```

An immortal finite queue of length `n` would belong to every `L_h`, forcing
`m_h<=n` for all `h`.  Hence the exact remaining language theorem is

```text
m_h(c) -> infinity as h -> infinity.                 (3)
```

Any proved unbounded lower bound in (3)—linear, logarithmic, or otherwise—
would establish queue mortality and close the constant-tail separator.  The
plateaus show why a one-step strict decrease is the wrong orientation: the
formula becomes larger while its shortest model only increases
intermittently.  The needed cocycle invariant must amortize these plateaus.

An independent local-spacetime SAT encoding extends this exact minimum
sequence without constructing the `4^(h+1)`-state DFA.  It restricts the
initial queue to the invariant `20,22,011`-free language, encodes every raw
four-state scan, the `3 -> 1` normalization, and the three legal hard-core
boundary cases.  Every model is decoded and replayed through the literal
queue map.  Through horizon 20 it gives

```text
h:       0 1 2 3 4 5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
m_h(2):  1 1 3 5 5 5 10 10 10 10 17 18 18 18 22 23 23 26 26 30 33
m_h(3):  2 2 3 5 5 5 10 10 10 13 14 15 16 16 24 24 26 26 31 31 32
```

Thus `m_h(c)>=h` survives every displayed exact instance, substantially past
the automaton audit.  This is finite evidence for the quantitative queue
bound, not an induction or a proof that (3) diverges.  See
`constant_tail_queue_sat.py`.

`RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md` now gives an exact graph realization
of this metric.  At height `h+1`, the source is the constant vertical frontier
and the target is the `F_(h+3)`-element set of hard-core inverse-cone
diagonals.  Taking the product with the `20,22,011` suffix DFA makes `m_h-1`
the directed product-graph distance.  The bare frontier distance instead
measures arbitrary normalized queues; the two finite minimum sequences first
separate at horizon ten, although their divergence is equivalent because the
first successor of any immortal queue lies in the invariant SFT.  The
frontier construction proves the Fibonacci terminal count uniformly and
computes both distances through horizon 12 without minimizing the language
DFA.

## 4. Relation to active-core diagonal mortality

The fourfold DFA growth is not a separate mysterious obstruction.  It is the
fixed-horizon reverse carry cascade from `RESULTS-CORE-MORTALITY-SAT.md` in
regular-language coordinates: each added survival row contributes one more
four-state carry coordinate.  The queue boundary supplies the same hard-core
acceptance grammar responsible for the Fibonacci counts.

Thus the language cocycle unifies the constant-tail and active-core routes;
it does not evade their expanding-state barrier.  The active-core diagonal
conjecture would give a linear lower bound on `m_h`, while constant-tail
mortality only needs the weaker divergence (3).  A successful proof should
exploit that weaker target rather than reconstruct the full `4^h` cascade or
ask its minimal automaton to shrink.

## 5. Reproduction

From `13-rule30/`:

```bash
uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_language_cocycle.py \
  --max-horizon 7

uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_queue_sat.py \
  --max-horizon 20 --max-length 50
```

The default horizon six is faster and checks the first jump to minimum length
ten.  Horizon eight retains 262,145 minimized states for each tail; the
frontier-graph checker is preferable for distance calculations beyond this.
