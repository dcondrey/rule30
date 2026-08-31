# Global periodic-trace fibre rigidity: a proposal from an LLM roundtable, checked

Status: **KILLED as stated, and not a new route.**  Under the only readings of
the proposal that are not vacuous, it is a re-derivation, one representation
later, of `RESULTS-diagonal-periodicity.md` and `RESULTS-ladder-rung1.md`,
both already closed by the `O(log t)` wall (`PATH.md` obstruction A) and, in
one reading, by the Rule 90 filter itself.  Nothing here bears on Wolfram's
Problem 1.

Date: 2026-08-30.  Code:
`experiments/overnight-arms/roundtable_followup/fiber_rigidity/`.  Modal: $0.
Paid model-provider calls: $0.

## 0. The proposal, and what had to be pinned down first

The panel's Direction 1 defines `X_{p,q} = {x : (F^{t+p}x)_0 = (F^t x)_0 for
all t >= q}` (lone-seed configurations whose centre trace is eventually
`p`-periodic from time `q`), asks for a classification of `X_{p,q}`'s
connected components under finite spacetime defects, and posits: `e in
X_{p,q}` implies `F^q(e)` restricted outside some finite `[-L,R]` lies in a
finite set `A_p` of "spatially eventually periodic asymptotic phases," with a
target contradiction from "two propagating finite-support interfaces" outside
`A_p`.  Two things are wrong with this before any computation:

1. **`F^q(e)` is a single fixed row, and "propagating" is a two-dimensional
   notion.**  A lone-seed CA of radius 1 has causal support `[-q,q]` at time
   `q`, for *every* rule.  So `F^q(e)` restricted to `|x|>q` is identically
   zero — trivially the constant phase, trivially inside any `A_p` that
   contains it, for **every rule, every `p`, every `q`, with `L=R=q`, no
   Rule 30 structure invoked at all**.  Read this literally, the "theorem" is
   a content-free restatement of finite propagation speed and would prove it
   for Rule 90 exactly as fast as for Rule 30.  This alone fails the Rule 90
   filter (`PATH.md` section 0): a claim proved this easily for both rules
   proves nothing.  "Propagating" interfaces don't live in one row anyway —
   propagation is a statement about the family `{F^t(e) : t>=q}`, not about
   one snapshot.
2. **The only non-vacuous reading is a statement about growing `L(t)` as
   `t -> infinity`,** i.e. whether some spatial margin near the light-cone
   edges settles into finitely many periodic phases as time increases, with
   the "interior" (the part that never settles) doing the work.  That reading
   already exists in this repo under two names: the *right-cone diagonal
   periodicity* representation (`RESULTS-diagonal-periodicity.md`) and the
   *pin / extendability* representation (`RESULTS-ladder-rung1.md` section 1).
   Both are re-examined below because the panel's "interface conservation law
   specific to `f_30(a,b,c)=a XOR (b OR c)`" is, concretely, the OR-saturation
   pin those documents already isolated and already showed insufficient.

`A_p` is pinned down, for the purposes of testing, as the following concrete
candidate (the only well-defined object the cited literature actually
supplies): the set of sequences that are eventually periodic in *time* along
each right-cone diagonal, in Rowland's sense (`RESULTS-diagonal-periodicity.md`),
extended symmetrically to the left diagonal via Jen's general theorem. This is
what "asymptotic phase forced by the periodic temporal boundary" can mean
given what has actually been proved about Rule 30's boundary; nothing sharper
is in the source material.

## 1. Rule 90 screen: checked directly, not trusted

The panel's screen: `f_90(a,b,c) = a XOR c` has `(F_90^t e)_0 = 0` for `t>0`
(true — `c_t = C(t,t/2) mod 2 = 0` for `t>=1` by Kummer's theorem), so its
trace fibre contains the actual Sierpinski configuration, and the panel
asserts the interface-rigidity lemma must therefore be false for Rule 90.

**MEASURED, confirms the panel's algebraic intuition, by direct
construction.**  The mechanism actually available for either rule is the
one-bit right-boundary defect front, built from each rule's own left-permutive
inverse (`experiments/rule30/inverse_trace_probe.py:reconstruct_left_column`
for Rule 30, `rule90_screen.py:reconstruct_left_column_90` for Rule 90, this
cycle):

```text
rule 30:  col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))
rule 90:  col_{x-1}(t) = col_x(t+1) XOR col_{x+1}(t)
```

Perturbing the right column by one bit at a fixed time and tracking the
earliest differing time in each successively reconstructed column to the left
(`rule90_screen.py`, `p1_p2_defect_front.py`):

| rule | centre value at the perturbed instant | outcome, 40 leftward steps |
|---|---|---|
| 30 | 0 | defect survives unattenuated at every step (`front = 64,63,...,25`) |
| 30 | 1 | defect erased at step 1, stays erased forever (`front = None,...`) |
| 90 | 0 | defect survives unattenuated (`front = 64,63,...,25`) |
| 90 | 1 | defect survives unattenuated (`front = 64,63,...,25`) |

Rule 30 has an erasure event (OR saturates when `col_x(t)=1`, matching
`RESULTS-ladder-rung1.md` Lemma 1: the extendability condition is *nonvacuous*
for Rule 30); Rule 90 never erases (Lemma 1': Rule 90's extendability
condition is *vacuous*, confirmed here by direct linear-inverse construction,
not by citation).  **This part of the screen is real and rule-specific**: a
finite defect can be permanently absorbed by Rule 30 and never by Rule 90.

But — and this is the reason it doesn't reopen anything — this erasure
mechanism is not new.  It is exactly `PATH.md` section 0.5's "centre-one
erases, centre-zero passes" law, already regression-pinned in
`test_inverse_trace_probe.py:115-117`, already proved in
`RESULTS-eventual-period.md` ("run-of-ones wedge": `d_t(-1) = (1 XOR c_t) AND
d_t(1)`), and already shown by `RESULTS-ladder-rung1.md` Corollary 2/3 to buy
**strictly less than one column of ladder depth**, which rung 0 section 3
already measured to be flat over a 5,500x range.  Running it fresh at `p=1`
and `p=2` (`p1_p2_defect_front.py`) reproduces the identical erase/pass law at
both periods, byte for byte — **the period does not change the law at all**,
only how often a `1` shows up in the trace to trigger it.  So the "mechanism
specific to `f_30`'s OR nonlinearity" the panel names is the repo's own pin
lemma, already characterized, and already proved insufficient to decide
anything beyond `p=1`.

**Second, independent check on the diagonal reading of `A_p`.**  If the
charitable, non-vacuous reading of "asymptotic phase forced near the
boundary" is Rowland/Jen diagonal periodicity, that reading is *also* not
Rule-30-specific.  `RESULTS-diagonal-periodicity.md` already says Rowland's
Lemma 2 needs only "right bijective," not anything particular to
`a XOR (b OR c)`; this cycle checked whether Rule 90 actually qualifies and
gets the same theorem, since apparently nobody in this repo had run it for
Rule 90 before (fresh computation, `edge_periodicity_probe.py` diagonal
check):

```text
rule 30 diagonal periods j=0..20: [1, 2, 2, 4, 8, 8, 16, 32, 32, 64, 64, 64, 64, 64, 64, 128, 256, 256, 256, 256, 256]
rule 90 diagonal periods j=0..20: [1, 1, 2, 1, 4, 1, 4, 1, 8, 1, 8, 1, 8, 1, 8, 1, 16, 1, 16, 1, 16]
```

(Rule 30's sequence matches OEIS A094605 exactly, as already verified in
`RESULTS-diagonal-periodicity.md`.)  Rule 90's diagonals *are* exactly
periodic too, powers of two, exactly as generic right-bijective theory
predicts — `f(a,b,c)=a XOR c` is bijective in `c` for fixed `a,b`, same as
Rule 30.  **So the diagonal-periodicity reading of `A_p` independently fails
the Rule 90 filter**, on top of already being capped by the `O(log t)` wall:
an argument built purely on boundary diagonal periodicity would "prove"
whatever it proves about Rule 30's fibre for Rule 90's fibre too, which
cannot supply the target contradiction (Rule 90's actual centre trace *is*
periodic, so no contradiction is available or needed there — the mechanism
would have to distinguish the rules and this reading cannot).

Conclusion of section 1: the panel's assertion that Rule 90's actual
lone-seed configuration is a genuine counterexample to interface rigidity is
plausible in spirit (Rule 90 truly lacks Rule 30's erasure event) but the
specific mechanism proposed to exploit that asymmetry is one this repo already
has, under a different name, and already showed does not scale past `p=1`.

## 2. Attempting the mechanism at `p=1,2`: same law, no new interface

`p1_p2_defect_front.py` (Rule 30, reusing
`experiments/rule30/inverse_trace_probe.py:rotated_defect_front` unmodified)
and `rule90_screen.py`:

```text
p=1 constant-0, perturb t=64 (centre=0 there): erased_immediately=False  front[:6]=(64, 63, 62, 61, 60, 59)
p=1 constant-1, perturb t=64 (centre=1 there): erased_immediately=True   front[:6]=(None, None, None, None, None, None)
p=2 word=01,    perturb t=64 (centre=0 there): erased_immediately=False  front[:6]=(64, 63, 62, 61, 60, 59)
p=2 word=01,    perturb t=65 (centre=1 there): erased_immediately=True   front[:6]=(None, None, None, None, None, None)
```

This is not the "two propagating finite-support interfaces not in `A_p`" the
panel wants.  It is one controllable defect that either dies in one step or
propagates at exactly light speed forever, and it behaves identically at
`p=1` and `p=2`.  Trying to read this as the two edges of the actual
diagram (left light-cone edge and right light-cone edge, each propagating at
speed 1) does not help either: that pair exists for *every* finite-radius CA
from a compact seed, both rules, all `p`, and the right one is already known
to carry Rowland/Jen order (section 1) while the left one is the chaotic side
that left-permutivity guarantees has none — restating
`RESULTS-diagonal-periodicity.md`'s own verdict ("an argument anchored at the
left boundary... Rule 30 has no analogous rigidity there") rather than adding
to it.

No construction attempted here produces a periodic-trace configuration whose
forced diagram exhibits structure outside the already-known boundary order
plus the already-known one-bit pin.  Both are old news; nothing new was found
by looking.

## 3. Does this evade the `O(log t)` wall?

**No — same wall, different vocabulary.**  "Classify the entire fibre" only
becomes checkable by asking what is forced *near the light-cone boundary*,
because that is the only place either of the two ingredients on offer (pin
erasure, diagonal periodicity) supplies any constraint at all; the interior,
at distance `Theta(t)` from either edge, is exactly where the wall says
nothing reaches.  Concretely:

* The diagonal-periodicity ingredient is `RESULTS-diagonal-periodicity.md`'s
  own representation, already measured there to reach `~2.4 log2(t)`
  diagonals from the right boundary while the centre sits at diagonal `t` —
  this is obstruction A verbatim, the fourth of PATH.md's five independent
  representations of the same wall, and section 1 above adds only that the
  same reach is generic to Rule 90, not that it reaches any further for
  Rule 30.
* The pin ingredient is `RESULTS-ladder-rung1.md` Corollary 2/3, proved there
  to buy **strictly less than one column of additional right depth**, and
  rung 0 section 3 already measured plain right depth to be flat (constant
  fraction of raw window space, 5,500x range) — so the pin, run to its proven
  limit, still cannot out-run `O(log t)`.

"The entire fibre and its asymptotic components" is a different noun phrase
for the same object rung 0/1 already ground down to sand: what is forced
outside a bounded strip near the boundary.  Framing it as fibre classification
does not create new information near the boundary; it only asks the same
representations a differently-worded question.  A genuinely new resource
would have to come from the interior or from the left (chaotic) boundary,
which section 2's search did not find and which `PATH.md`'s ranking already
flags as the only route with any of that shape left (section 4, "an argument
anchored at the left boundary, or one that is not boundary-anchored at all").

## 4. Verdict

**KILLED, not viable as a route, and not a new one.**  Three independent
findings converge:

1. The literal statement is vacuous for every finite-radius rule (finite
   light cone), hence fails the Rule 90 filter trivially.
2. The only non-vacuous reading (diagonal periodicity near the boundary)
   already exists in this repo, is already capped at `O(log t)` reach
   (obstruction A), and — newly checked here — is *also* generic to Rule 90
   (Rowland/Jen needs only right-bijectivity, which Rule 90 has), so it fails
   the Rule 90 filter a second, independent way even setting the wall aside.
3. The concrete "OR-nonlinearity interface" mechanism the panel names is the
   already-published pin/extendability lemma (`RESULTS-ladder-rung1.md` Lemma
   1/1', `RESULTS-eventual-period.md` run-of-ones wedge, `PATH.md` 0.5),
   already proved to buy less than one column of depth, and reproduced here
   identically at `p=1` and `p=2` with no new behaviour at the higher period.

Nothing here is a new obstruction either; it is the same three obstructions
(the `O(log t)` wall, the Rule 90 filter, and the missing-composition-law
pattern of naming a mechanism instead of deriving new content from it)
recognized in a fourth representation before any real computation was spent
on it. No further work on this direction is recommended without a genuinely
new resource anchored away from the light-cone boundary.

## Reproduction

```sh
cd experiments/overnight-arms/roundtable_followup/fiber_rigidity
uv run python edge_periodicity_probe.py 2048      # spatial-row periodicity near the edge: 0 for both rules (naive reading is empty)
uv run python rule90_screen.py                    # Rule 90 never erases a defect, at any phase
uv run python p1_p2_defect_front.py               # Rule 30 pin law, identical at p=1 and p=2
uv run python diagonal_periods_rule90.py          # Rule 90 diagonals are also exactly periodic
```

All four scripts run in well under a second.

- Modal: **$0**.  Paid model-provider calls: **$0**.
