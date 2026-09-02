# Forum and informal-source audit for the Rule 30 period-two attack

Date: 2026-09-02

Status: **NO EXTERNAL POST SUPPLIES THE MISSING PROOF.  TWO INFORMAL IDEAS
HAVE EXACT INTERNAL FORMS, BUT BOTH CONTROL ONLY THE ALREADY-UNDERSTOOD
TRIANGULAR BIJECTION.  THE NEW USEFUL SYNTHESIS IS `(BWH+)`.**

## 1. Sources searched

### Brunnbauer / Wolfram Community: right diagonals

Michael Brunnbauer describes the right-diagonal recurrence as OR of the two
preceding diagonals followed by cumulative XOR, and reports same-or-double
period behavior:

- <https://community.wolfram.com/groups/-/m/t/1802242>
- <https://brunni.de/findings30/>

The rigorous version is already available in Eric Rowland's paper on local
nested structure:

- <https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf>

This is mathematically real but does not reach the center: the periodic
right-boundary region grows only logarithmically in time, while the center
samples a diagonal whose index grows linearly.  That route was already
closed in `docs/rule30/RESULTS-diagonal-periodicity.md`.

### Reddit: unique paths and backward reconstruction

Two informal posts emphasize unique ancestry paths and reconstructing Rule
30 backward from neighboring columns:

- <https://www.reddit.com/r/cellular_automata/comments/n2iznz/>
- <https://www.reddit.com/r/cellular_automata/comments/n8vq69/working_backwards_in_rule_30_from_an_arbitrary/>

The exact reusable statement is right-permutivity of the Peel rule.  If two
finite words first differ at coordinate `k>=1`, their Peel images first
differ at `k-1`.  Iterating transports the first difference to the boundary.
This proves unique lifting and is a useful correctness check.  It does not
exclude a lift: the entire difficulty is whether the uniquely forced lift
stays in the binary alphabet.

### Nersissian / Wolfram Community and Mathematica Stack Exchange

A proposed subset-support recurrence packages the algebraic-normal-form
evolution using symmetric difference and OR-convolution:

- <https://community.wolfram.com/groups/-/m/t/3647733>
- <https://mathematica.stackexchange.com/questions/318912/rule-30-finding-a-closed-formula-for-the-s-m-subset-recurrence/319098>

This may be a useful exact representation after independent verification,
but the author explicitly reports that evaluation of the support set remains
recursive and asks whether unresolved increment/carry collisions could imply
irreducibility.  That is an open step, not a proof of P1, P2, or P3.  ANF
degree growth also does not give a lower bound for the fixed single-seed bit
problem.

### Other searches

The Math Stack Exchange information-transmission question has no theorem
answer relevant to the fixed seed:

- <https://math.stackexchange.com/questions/3969403/can-information-transmission-be-proven-in-a-rule-30-eca>

The remaining forum and repository hits were simulations, cryptographic
applications, or restatements of left-permutivity.  None supplied an
all-length center-trace invariant.

## 2. Exact mashup

The diagonal cumulative-XOR observation and the backward unique-path
observation are two views of the same triangular mechanism:

```text
right-permutivity
      -> one forced endpoint symbol per desired cut symbol
      -> high output bit = complete-diagonal activity parity
      -> only the low/defect bit can make the lift leave {1,2}.
```

Combining this with the rotated-wedge identity removes the distracting
actual-right constraint.  To kill every DLP witness it suffices to prove

```text
M_c(n) <= n+1 for c in {2,3}.                       (BWH+)
```

`RESULTS-BINARY-WEDGE-HORIZON.md` gives the exact reduction and census.

## 3. What the search changes

The search does not justify returning to spectral metaphors, generic chaos,
Lyapunov exponents, normality, or finite-width limit cycles.  Those concern
different quantifiers or lose the single moving center column.

It does justify concentrating on one algebraic obstruction: simultaneous
binary legality of the two affine coordinates along a triangular lift.
The promising proof objects are therefore:

1. a nonlinear source clause or branched ancestry extracted uniformly from
   the terminal defect;
2. a scale induction explaining why every `n+1`-cell saturator dies on the
   next cell; or
3. a period-two phase invariant for the complete diagonal, not a bounded
   local window or one parity coordinate.

No searched source closes any of these three steps.
