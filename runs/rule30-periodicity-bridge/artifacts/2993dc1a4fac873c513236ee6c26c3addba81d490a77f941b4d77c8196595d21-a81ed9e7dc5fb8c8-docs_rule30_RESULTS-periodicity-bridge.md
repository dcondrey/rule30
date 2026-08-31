# Rule 30 periodicity bridge: exact exclusions before cloud compute

## Question

Can the known nonperiodicity of a width-two Rule 30 trace be converted into
nonperiodicity of the center column by a local reconstruction or by extending
the theorem to a natural nonlinear subclass?

This is the narrow gap left by Johan Kopra's width-two result.  Corollary 3.7
of *Rapid left expansivity and nonparametrizable initial conditions in cellular
automata* proves non-eventual-periodicity for every width-two trace in the
relevant left-permutive, left-spreading class.  The paper explicitly notes
that the single center column remains open and gives Rule 90 as a counterexample
to an unrestricted width-one extension:

<https://www.utupub.fi/bitstream/handle/10024/174540/1-s2.0-S0304397522007502-main.pdf?isAllowed=y&sequence=1>

The official prize page still lists the center-column question as open:

<https://rule30prize.org/>

## Exact defect identity

Write the Rule 30 state as `s(t,x)` and, for a proposed period `p`, define

```text
D(t,x) = s(t+p,x) XOR s(t,x).
```

Rule 30 is

```text
s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
```

Whenever `D(t,0)=D(t+1,0)=0`, direct Boolean subtraction gives

```text
D(t,-1) = (1 XOR s(t,0)) AND D(t,1).
```

Consequently, an assumed periodic center would force every left defect at a
center-one time to vanish.  At a center-zero time, the left and right defects
must agree.  `periodicity_bridge_probe.py` checks this identity for all
eligible times in each requested finite sample; no violations occur.

This is a valid constraint, but it is not yet a contradiction.  Width-two
nonperiodicity merely ensures that adjacent defects recur.  The identity lets
them recur at center-zero phases on both sides.

## Eliminated bridge families

### 1. Nonlinear left-permutive rules are not enough

Every binary left-permutive rule has the form

```text
f(a,b,c) = a XOR g(b,c).
```

Requiring a quiescent zero leaves eight elementary rules.  Exactly four have
a nonlinear `g`.  Their single-seed center prefixes are:

| packed residual bits `g(11)g(10)g(01)g(00)` | rule | sampled center prefix |
|---|---:|---|
| `0010` | 210 | `1000000000000000` |
| `0100` | 180 | `1100000000000000` |
| `1000` | 120 | `1000000000000000` |
| `1110` | 30 | `1101110011000101` |

The first three nonlinear residuals have a single nonzero input and trivial
sampled centers.  Rule 30 is the only nonlinear residual with all three
nonzero inputs enabled (`g=b OR c`).  Thus “nonlinear” is too broad, while
adding the full-support condition reduces this binary class to Rule 30 itself
and supplies no transferable theorem.

### 2. Finite-delay center observability fails

For every time shift through 256 and every time through 4096, the probe finds
the longest run satisfying `s(t,0)=s(t+p,0)`.  Rule 30 has an 18-step run at
`p=148`, beginning at `t=1855`, while both adjacent columns contain a defect
during that run.  Extending the local sample to time 16384 and shifts through
512 produces a 24-step run at `p=110`, beginning at `t=13219`.

These are finite counterexamples to reconstruction delays up to the observed
lengths.  They are not asymptotic claims.  Rule 90 is the adversarial control:
its single-seed center is zero after time zero, so the center agrees with a
unit time shift forever while adjacent defects remain.  Any class-wide
finite-delay reconstruction lemma is therefore false.

### 3. The center trace is not an injective observation

Two finite initial configurations have the same Rule 30 center trace in every
checked step:

```text
A = {0}
B = {0,1}.
```

The probe checks a stronger moving-defect certificate.  At every checked even
time `t`, the two full configurations differ only at `x=t+1`; at every checked
odd time they differ only at `x=t` and `x=t+1`.  This supplies a simple
induction target and explains the observed failure to reach the center.  Generic trace
injectivity cannot bridge width two to width one; a valid proof must use the
specific comparison between two times of the lone-seed orbit.

### 4. A direct doubling separation is false

The tempting period witness

```text
s(p,0) != s(2p,0) for every p > 0
```

first fails at `p=4`, where both values are one.  Left-permutivity guarantees
propagation at one extreme of a finite configuration difference, but that
extreme moves away from the center in this comparison.  It does not force a
center mismatch.

## Decision

No Modal job is admitted from these results.  Scaling the same finite checks
would only lengthen counterexample tables and cannot establish eventual
behavior.  The next eligible candidate must exploit the exact defect identity
plus a property specific to the lone-seed orbit and must return one of:

1. a period-independent descent measure;
2. a finite transition graph whose forbidden cycles encode every proposed
   center period; or
3. a parameterized mismatch certificate computable from `p`, not a larger
   checked range.

Until one of those mechanisms survives a local falsifier and the Rule 90
control, the rational Modal expenditure is **$0**.

## Reproduction

From `experiments/rule30`:

```bash
uv run python -m unittest test_periodicity_bridge_probe.py
uv run python periodicity_bridge_probe.py --horizon 4096 --max-shift 256
```
