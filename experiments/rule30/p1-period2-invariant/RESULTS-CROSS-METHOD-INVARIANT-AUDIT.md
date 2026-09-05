# Cross-method numeric audit: the recurring "0.4" is phi/4, and it is a null result

Date: 2026-09-04. Method: collect every numeric outcome from the killed
routes, normalize, and look for equalities across unrelated methods. This
document reports one substantive finding, one deflation, and one correction.

## Verdict up front

**The "~0.4 invariant" that three independent codings converge on is
`phi/4 = 0.4045...`, and it is exactly the rate predicted by assuming the
forced continuation has NO structure at all beyond the hard-core (no-`11`)
constraint.** It is therefore not evidence of a hidden law waiting to be
found. It is a quantitative measurement of the *absence* of one, and it is
the same fact as four other numbers already on record that had not been
connected to it.

## 0b. Correction affecting the independence claim (2026-09-04, same day)

An earlier same-day note in `BACKLOG.md` section 17 claimed
`flip_pairing.py`/`block_halving.py` measured a *different* object
(`(BWH+)`/`Psi_n`) from `H_r(n)`. **That claim has been retracted** — it
rested on comparing two different-typed outputs elementwise. The two
constructions in fact define the same survivor population: 0 death-level
mismatches out of 7,168 words (`n=9,10,11`, both tails).

This cuts both ways for this document:

- **In favour:** the section 3 table's grouping is correct, and
  `flip_pairing`'s `0.4^j` and block-halving's ratio genuinely describe the
  `H_r(n)` survival process, so they may be compared with the `H_r(n)`
  per-row measurements directly.
- **Against:** those are therefore *not* three independent objects
  agreeing. `rw_population_h`, `flip_pairing` and `block_halving` are three
  codings of the **same** process, so their agreement is a consistency
  check, not independent confirmation. The genuinely independent
  measurement in the `0.4` family is the endpoint-coordinate `13/32`
  statistic (a different statistic on the raw `Endpoint` recursion), and it
  is *not* equal to `phi/4` (`0.40625` vs `0.404508`) — it is a separate
  exact rational that happens to land nearby. Any claim of the form "three
  independent codings converge on one constant" must be dropped; the honest
  claim is "one process, measured three ways, matches its own maximal-entropy
  null to the stated precision."

## 1. The null model, and why phi/4

Take the crudest possible model of `literal_extension`'s forced
continuation: each appended symbol is uniform over the 4 states, subject
only to hard-core (values in `{1,2}`, no `11`). Track the last emitted
symbol. From state `1` only `2` is legal (1 of 4 states); from state `2`
both `1` and `2` are legal (2 of 4). The per-row survival transfer matrix
is

```
M = [ 0    1/4 ]
    [ 1/4  1/4 ]
```

whose leading eigenvalue is `phi/4 = 0.404508...`, `phi` the golden ratio.
Starting from the uniform distribution on `{1,2}` (the last symbol of a
uniform source word), the exact predicted per-row survival sequence is

```
0.3750, 0.4167, 0.4000, 0.4062, 0.4038, 0.4048, 0.4044, 0.4045, ... -> phi/4
```

The first entry is exactly `3/8` (= `1/4 + 1/4 * 1/2`), and the sequence
converges to `phi/4` as the distribution relaxes onto the Perron
eigenvector.

## 2. Measured against the null model (exact rationals, `rw_population_h.survival_curve`)

Measured first-row survival, `|H_r(n)|`'s own construction, `r=0`:

```
n=10 c=2   99/256      = 0.3867     (null: 0.3750, diff +0.0117)
n=10 c=3   385/1024    = 0.3760     (diff +0.0010)
n=12 c=2   1607/4096   = 0.3923     (diff +0.0173)
n=12 c=3   1487/4096   = 0.3630     (diff -0.0120)
n=14 c=2   6145/16384  = 0.37506    (diff +0.0001)
n=14 c=3   6145/16384  = 0.37506    (diff +0.0001)
n=16 c=2   6135/16384  = 0.37445    (diff -0.0005)
n=16 c=3   24909/65536 = 0.38010    (diff +0.0051)
```

At `n=14` and `n=16` the measured first-row survival agrees with the
null model's exact `3/8` to four decimal places. Subsequent rows track the
predicted `0.4167, 0.4000, 0.4062, ...` sequence within small-count noise
(the residuals grow only where the surviving population drops below ~50
words, exactly where fluctuation is expected). Full per-row residual tables
are in this document's companion computation (scratch, not committed; the
measured `alive_after` arrays are reproducible from
`rw_population_h.survival_curve(n, c, 0)`).

## 3. The equalities this explains

Five previously separate numbers are one statement:

| number | where it was measured | what it is under the null model |
|---|---|---|
| `phi/4 ~ 0.4045` (and the "0.38-0.43 band", "`0.4^j`") | `H_r(n)` per-row survival; `flip_pairing.py` coverage; `block_halving.py` ratio | the hard-core shift's own rate; **no structure beyond no-`11`** |
| `phi = 1.618` block-language growth | `L10-FIB-TRANSFER`, killed because "RW block language = hard-core through length 7, ratio = phi" | the *same* `phi`: the forced language IS the hard-core language |
| `3/8` first-row survival | this document, exact | `1/4 + 1/4 * 1/2`, the uniform-symbol hard-core prediction |
| DFA size `4^(h+1)+1`, h=0..7 (`5,17,65,257,1025,4097,16385,65537`) | `RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md` | minimization achieves **zero** collapse: saturates the trivial bound exactly |
| pooled `P(next=1 \| ctx) = 0.4899..0.5158` over ~350k obs/context | `RESULTS-SURVIVOR-DECAY.md` (today) | a fair coin: no order-3 context carries marginal information |

Plus the already-recorded full algebraic degree `n` (`Psi_n`,
`BACKLOG.md:366`) and `deg E(e_u) = 2u-1` (`BACKLOG.md:22,84`), which say
the same thing algebraically: no lower-degree structure exists.

**These are not five findings. They are one finding measured five ways:
the forced dynamics is statistically and algebraically indistinguishable
from maximal entropy subject only to hard-core.** That is why ~142 routes
died: every one of them searched for exploitable structure, and the
measurements collectively say there is none to find.

## 4. What the null model predicts quantitatively, and why the problem is hard

First-moment (union-bound) heuristic: `2^n` source words, per-row survival
`phi/4`, over `n` rows:

```
E[# survivors at length n]  ~  2^n * (phi/4)^n  =  (phi/2)^n  =  0.809^n
```

```
n=9:  0.148     n=13: 0.0636    n=16: 0.0337
n=20: 0.0144    n=29: 0.00214   n=30: 0.00173
```

Summed over all `n`, exactly:

```
sum_{n>=1} (phi/2)^n  =  phi/(2-phi)  =  phi^3  =  4.236068...
```

(exact: `phi/(2-phi) = phi^3` since `phi^3 = 2phi+1` and `phi^4 = 3phi+2`.)
Including the `r+2` extra forced rows (`(phi/4)^(r+2)`) gives an expected
total, over **all** `n`, of `0.693` (`r=0`), `0.280` (`r=1`), `0.113`
(`r=2`).

This is the quantitative reason the problem resists proof. The expected
total number of counterexamples across all lengths is not comfortably
zero -- it is a number of order one, just under 1. The conjecture is true
in the first moment, but with no margin. Two consequences, both matching
what this project has independently hit:

1. **The counting line's near-miss is structural, not bad luck.** `C < 4`
   suffices for RW; measurements give `C=1` (`n=10..18`) and `C=3`
   (`n=9`). The null model's own pre-terminal expected total is
   `phi^3 = 4.236`, sitting just *above* the threshold `4`. A first-moment
   argument therefore cannot close by a comfortable margin no matter how
   carefully it is run -- which is exactly the observed behavior of every
   counting attempt in `BACKLOG.md` section 17.
2. **Borel-Cantelli gives "finitely often", never "ever".** Today's
   `PREREGISTRATION-MEASURE-SUPPRESSION.md` reached this conclusion
   structurally (section 3.5) without the constant; the constant now says
   why: a summable series with an O(1) sum bounds the expected count, and
   an expected count below 1 is not zero.

## 5. What this does NOT claim

- Not a proof of RW, DLP, SEP, or PT2, and not a disproof. A first-moment
  heuristic that predicts "expected count 0.69" is consistent with both
  zero counterexamples and with a few.
- Not a claim that the forced map IS random. It is deterministic
  (`literal_extension` asserts a unique forced symbol per row). The claim
  is only that its measured statistics match the maximal-entropy null to
  the precision checked -- and today's `RESULTS-SURVIVOR-DECAY.md` proved
  the *complement*: those statistics are NOT stationary in `n`, so the
  null model cannot be promoted to a rigorous Markov description. Both are
  true: it looks random marginally, and it is provably not Markov.
- The `phi^3 = 4.236` vs `C < 4` proximity in section 4 is flagged as
  suggestive, not established. Two constants landing near 4 may be
  coincidence; the argument does not depend on it.
- Deep-row agreement (rows 5+) is within small-count noise only and should
  not be cited as precision agreement; only the row-1 agreement
  (4 decimals at `n=14,16`) is tight.

## 6. Correction issued while performing this audit

The claim "every (class,symbol) pair reaches all 8 D8 successors,
complete branching, 32/32", used in today's
`PREREGISTRATION-ENDPOINT-ENERGY-INVARIANT.md` section 0 (and repeated
into its results file), cites `CONTINUATION-PROMPT.md` lines 503-521. Those
lines do **not** contain it; they record a related but distinct result
(exact Farkas-style multiset obstructions for the four carry states, the
eight D8 prefix actions, and D8-x-carry; plus "bounded D8 lookahead/action
summaries: closure collisions"). The `32/32` figure appears in no file in
this directory -- it is an unverified figure inherited from a prior
session's chat summary, and the one `32/32` that IS in the files
(`README.md:243`, `RESULTS-DIVERGENCE.md:204`) is an unrelated `F^2`
truth-table control. Both documents have been annotated. The qualitative
fact (bounded D8 observers are dead) stands on the cited source; the
number does not, and the endpoint-energy kill does not depend on it (it
rests on that document's own `sigma_{j-1}` measurement).

## 6b. The precise claim: marginal, not joint -- and what that makes the theorem

The two halves must be stated together or the result is an overclaim:

> The forced dynamics is **marginally** indistinguishable from maximum
> entropy subject to hard-core, even though it is **jointly** not that
> process.

Both halves are established here, and they are not in tension:
- *Marginal* agreement: section 2's first-row match to four decimals, the
  `phi/4` rate, the fair-coin order-3 marginals.
- *Joint* failure: `RESULTS-SURVIVOR-DECAY.md` proved the same output
  sequence is **not** Markov at order 1, 2, or 3 -- context-conditional
  frequencies swing across nearly all of `[0,1]` with `n`. The DFA
  saturation `4^(h+1)+1` says the same thing structurally.

That combination is the informative part, because it says what kind of
theorem is missing. Not an algebraic lemma, and not an automaton: the
target is a **domination inequality**.

> **Target.** Show the actual per-step survival weight of the recursion is
> dominated by the null transfer matrix `M = [[0,1/4],[1/4,1/4]]`, up to a
> uniform global factor -- i.e. that the true leading survival rate obeys
> `lambda_true <= lambda` with `2 * lambda_true < 1`. Then the first-moment
> bound becomes an upper bound rather than a heuristic, and `H_r(n) = empty`
> for all sufficiently large `n` follows by counting, with no locality, no
> bounded automaton, and no algebraic structure required.

Note the margin this needs: `2 * lambda = 2 * phi/4 = phi/2 = 0.809 < 1`
already, so *any* valid domination by `M` suffices asymptotically -- but
the O(1) expected total (section 4) means domination must hold from small
`n` onward, or the conclusion only reaches "all sufficiently large `n`"
and leaves a finite window that must be closed by census (which is exactly
what the existing SAT/enumeration range does). This is the one shape of
argument this project has not attempted, and unlike the 142 killed routes
it does not require the structure the measurements say is absent.

## 7. Strategic consequence

The productive reading is that this project has, without framing it this
way, accumulated a strong quantitative case for a *specific* statement:
the Rule 30 forced continuation in this reduction is
maximal-entropy-subject-to-hard-core to every precision so far measured.
That is a sharper and more citable claim than "we ruled out 142 routes",
it explains the ruling-out uniformly, and it is the natural thing to put
in front of an expert (e.g. Kari) -- together with the honest statement
that making it rigorous is a derandomization/large-deviation problem, not
a search for a missing algebraic lemma.
