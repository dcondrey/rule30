# P3: preserved limits from the final session analysis

Date: 2026-09-14. This note preserves reasoning that had not yet received a
separate source report when the task switched to repository synchronization.
It makes no singleton-query complexity claim. Source arguments and finite
checks below have different scopes; none is a Lean kernel-checked theorem.

## 1. The full integer interpolation lift is not bivariate rational

Use exactly the integer-valued polynomial lift `P_k(t)` of
[the Fibonacci interpolation audit](RESULTS-p3-fibonacci-interpolation-audit.md):
`P_0=1`, `P_1=t`, `P_k(0)=0` for `k>=1`, and
`Delta P_k=P_(k-1)+P_(k-2)+P_(k-1)P_(k-2)` for `k>=2`.
That source proves `deg P_k=F_(k+2)-1`, with nonzero leading coefficient.
Define the formal series over the rationals

```
R(X,T) = sum_(k>=0) X^k sum_(t>=0) P_k(t) T^t.
```

**Source proof.** `R` is not an element of `Q(X,T)`. Indeed, the generating
function `R_k(T)` of a nonzero degree-d polynomial sequence has a pole of
exact order `d+1` at `T=1`. If `R` were rational, its coefficients in `X`
would satisfy a fixed finite linear recurrence over `Q(T)` for every
sufficiently large k. Clear denominators. Among its nonzero terms choose
the one with largest coefficient index `k-j`. Its pole order is
`F_(k-j+2)` minus the fixed order of vanishing of that recurrence
coefficient at 1. The difference from every other term's pole order tends
to infinity. For large k this unique largest pole cannot cancel. This is
a contradiction.

The argument is conditional only on the stated, separately source-proved
degree theorem. It excludes a rational expression for the **entire integer
two-variable lift**. Reduction modulo two, diagonals, other encodings, and
the singleton function `n -> c_n` are not excluded. No finite degree sample
is being used in place of the argument. No new interpolation run was made.

## 2. Retaining only rises discards a movable fall

The stronger actual-orbit counterexample is in
[the rise-chain report](RESULTS-p3-rise-chain-transparency.md): at input
times 0 and 4 the two-digit supplied `(Z,rho)` prefixes and origin phase
agree, but the high digit four fine time steps later differs: the high
at site 1 is 1 in B^4(0) and 0 in B^8(0). The first two-time endpoint
has high bit 1 in both cases. This
refutes that causal summary, with actual ancestry retained.

A separate arbitrary-input diagnostic has the same mechanism. In the
least-significant-digit-first itinerary coordinates let
`Y_r=0^r 3 0^infinity`, `r>=1`. Under the B action, put
`A=low(BY_r)`, `Z=low(Y_r)+high(Y_r)`, and
`rho_i=A_i(1+A_(i-1))`, with zero extension for rho. Direct substitution
in the two affine scans gives

```
Z=0^infinity, A=1^r 0^infinity, rho=1 0^infinity,
B^2 Y_r=2^r 3^infinity.
```

The discarded fall is at r and is not determined by `(Z,rho)`. This is an
all-r identity from the scan recurrence, not an assertion that these rays
are actual zero-seed iterates or finite-integer H states. The actual-orbit
witness, rather than this broader-input family, is used in the current
route's controls.

## 3. Other analyses that did not produce a new cost theorem

The last-rise interval has midpoint low field `1^u 0^v`. Substituting
`Z=C+A SC` in its parity readout telescopes to the existing one-pass
last-A-one reset formula. On an A-zero interval the subsequent low field
is monotone, but the next midpoint need not retain that form. These are
coordinate consequences of the saved scans; they were not promoted as
new algorithmic improvements.

Two suggestions were corrected before being used. The predecessor pair
`12` in a rise chain allows driver B **or C**, rather than B alone. The
rise-chain report states the corrected three-pair language. An even-stride
identity `G_s^(2l)0=4(B^s A^s)^l0`, where `G_s=tau_0 A^s` and s is even,
does not halve charged work: the apparent saved first `A^s 0` was already
free. No cost claim is retained from that suggestion.

The fixed-automaton exact-time relation idea and a capped period-eight
continuation were also discussed. Neither supplies a new saved exact
certificate or a singleton-query cost bound. They are **unpromoted
investigation notes**, not missing proved results. The capped continuation
cannot be read as all-width cycle closure. Literature analogies with
iterated transducers supply no applicability theorem for this reset group.

## 4. Remaining obligation

The exact B/C observer, supplied-history rise certificates, and affine
scans must be connected to an algorithm constructing the needed ordered
control histories from binary n. Its construction, arithmetic, memory,
decoding, and total sequential work all remain charged. No amortized
sublinear recurrence is established here. P3 and period-two exclusion
remain open.

## 5. 2026-09-18: a time-doubling candidate, killed

Before attempting a symbolic recursive constructor for section 4's
remaining obligation, one candidate for a self-similar reduction was
tested computationally against the bitplane-scan oracle: is
`digit_i(B^(2t)(0))` a function of `digit_(i//2)(B^t(0))` alone, i.e.
does doubling the applied power of B coarsen the spatial site index the
way doubling the exponent coarsens `k` in the alternating-guard shift
argument (`RESULTS-p3-actual-alternating-guard.md` section 1)? It is not:
the same `digit_(i//2)(B^1(0))` value already maps to two different
`digit_i(B^2(0))` outcomes, and the number of mixed classes grows with
`t` (up to `t=18` checked). This rules out the simplest coarsening
candidate; it does not rule out a recursion keyed on a wider window or on
the actual predecessor-word certificate of
[the rise-chain report](RESULTS-p3-rise-chain-transparency.md) section 2.

The [oracle](../../experiments/rule30/p3_time_doubling_candidate.py) that
ran this test first reproduces, exactly, the four saved B-power rays and
the site-1 high-bit collision at old times 0 and 4
(rise-chain-transparency.md section 4) and the `Y_r` rise/fall identity
of section 2 above, as implementation controls, before testing the new
candidate. The [artifact](../../experiments/rule30/p3-time-doubling-candidate.json)
retains the full per-`t` class/mixed counts.

## 6. 2026-09-18: a real spatial-periodicity effect that cannot reach the query site

Every candidate above fixes a site and varies time. The one genuinely
different lever tried is the reverse: fix `N` large and scan across
sites. `B^N(0)` is spatially eventually periodic (period 16, stable from
`N=300` through `N=2000` tested), which is not a coincidence: since
`Y_0=0^inf` is constant, the scan automaton of `RESULTS-p3-two-affine-scans.md`
section 1, fed constant-zero input past its information front, must settle
into its own small limit cycle. The onset site where that periodic tail
begins was measured directly and scales linearly with `N`, at a ratio
consistently between `1.5` and `1.65` (`N=100` through `N=2000`).

Since the query site for the actual singleton formula is `h-1` at depth
`N=h+1+e` (`RESULTS-p3-actual-b-query.md` equation 1), its site-to-depth
ratio is about `1`, strictly below the measured onset ratio at every
tested `N`. The periodic tail is real, but it never reaches the query
site: the light cone from the finite-propagation-speed scan always keeps
the region of interest inside the transient, not the tail. This explains
*why* a spatial-periodicity shortcut cannot work here, rather than merely
observing that it does not; it is not proposed as a route obstacle to
re-test, since the geometric reason is now explicit.

The [probe](../../experiments/rule30/p3_spatial_periodicity_probe.py) and
[artifact](../../experiments/rule30/p3-spatial-periodicity-probe.json)
retain the period and onset measurements.
