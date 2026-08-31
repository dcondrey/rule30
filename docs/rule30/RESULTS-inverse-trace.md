# Rule 30 inverse-trace arm

## Status

The inverse map is exact and useful as a proof interface, but it has not yet
produced a period-independent contradiction. This is not a solution to the
center-column nonperiodicity problem.

## Exact construction

For Rule 30,

```text
s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
```

Fix an initial right half `s(0,x)` for `x >= 0` and a desired center trace
`c(0), c(1), ...`. The left-permutive term makes the initial cell at `-k`
the only not-yet-fixed input that can reach the center at time `k`. Toggling
that cell toggles the time-`k` center and cannot change an earlier center.
Consequently, the trace and right half uniquely reconstruct positions
`-1, -2, ...` in order.

`experiments/rule30/inverse_trace_probe.py` implements this triangular map
without using a Rule-30-specific closed form. Its tests reconstruct random
finite rows for Rules 30, 90, 120, 180, and 210 and independently check the
unit-sensitivity claim at every reconstructed depth.

The construction is a standard consequence of left permutivity and should not
be reported as a new theorem. The potentially useful object is the forced
left tail produced by a periodic trace on the particular lone-seed orbit.

## Periodic continuation test

At an actual orbit time `T`, take the first `p` center bits as a proposed period
word and repeat them forever. Combine that desired trace with the actual right
half of row `T`; inverse reconstruction gives the unique left half that the
periodic continuation would require.

The actual row has finite support in `[-T,T]`. Therefore either of the
following is an exact contradiction:

1. a reconstructed cell inside the support differs from the actual row; or
2. any reconstructed cell left of `-T` is one.

The first spatial mismatch must occur at exactly the first temporal mismatch.
This is checked as an invariant, not inferred from matching plots.

For the strongest finite agreement previously found (`T=1855`, `p=148`), the
period word survives 18 comparisons after its first complete block. Both the
first temporal mismatch and first reconstructed spatial mismatch occur at
depth 166. If reconstruction is continued despite that already decisive
mismatch, its first forced one beyond the actual support occurs immediately at
depth 1856.

## Required adversarial control

Rule 90 from a single seed has center trace `1,0,0,...`. At `T=1`, the
period-one zero continuation is genuine. Reconstruction through depth 512
returns the actual finite left half and never forces a one beyond its support.
Thus the inverse method does not falsely turn left permutivity, finite support,
or a chaotic-looking spacetime diagram into center nonperiodicity.

## Falsified shortcuts

The claim that every proposed Rule-30 period forces a one in the *first* cell
outside the support is false. It already fails at `T=4`, `p=1` (and for many
other small pairs). On the finite grid `1 <= T <= 100`, `1 <= p <= T+1`, a
100-cell lookahead found zero-tail prefixes of varying lengths; the longest
survived 17 cells and forced its first one at depth 106 for `T=88`, `p=48`.
Those finite measurements reject a one-step boundary lemma but establish no
asymptotic bound.

### Periodic-mask contraction also fails

Rotating the local equation gives an exact recurrence between complete time
columns. If `B(t)=s(t,x)` and `C(t)=s(t,x+1)`, then the column immediately to
their left is

```text
A(t)=s(t,x-1)=B(t+1) XOR (B(t) OR C(t)).
```

This exposes a real Rule-30-specific filter. A discrepancy in `C(t)` is erased
when `B(t)=1` and passes into `A(t)` when `B(t)=0`. It is tempting to hope that
a periodic center repeatedly erases all right-column information, making a
width-two trace periodic far enough to the left.

The hope is false for every period word containing a zero. Once a discrepancy
crosses at a zero phase, take its earliest differing time `tau`. In the next
left column the `B(t+1)` term creates a discrepancy at `tau-1`; the other terms
at that earlier time still agree. Inductively, the earliest defect moves one
time step earlier per reconstructed column and cannot be erased. The executable
control uses center word `01`: a right-column perturbation at zero-phase time
64 has earliest-defect front `64,63,...,33` through 32 left columns, while the
same perturbation at one-phase time 65 is erased immediately.

The only periodic word with no zero is constant one. That subcase is ruled out
directly: if the center is eventually one, the same recurrence forces its left
neighbor eventually zero, making the width-two trace `(-1,0)` eventually
constant, contrary to Kopra's width-two theorem. This is a small exact partial
result, not the general solution; constant zero and every nonconstant period
still contain zero phases through which nonperiodic information can propagate.

## Remaining proof obligation

The inverse construction reformulates the open step precisely:

> For every proposed period `p`, show that sufficiently late lone-seed rows
> cannot equal the left half reconstructed from their repeated center word and
> actual right half.

A useful next result must make this cheaper than comparing the original center
trace. Eligible mechanisms are:

- a finite transition graph, parameterized uniformly in `p`, in which an
  eventually-zero reconstructed tail would be a forbidden cycle;
- a descent invariant for the rotated reconstruction wedge; or
- a formula for a forced nonzero tail position from `(T,p)` with a proof that
  does not inspect `Theta(T)` orbit cells.

Without one of those, inverse reconstruction merely rotates the same unknown
sequence and does not solve the prize problem. No Modal job is justified by
the current finite sweep.

## Bounded Crosstalk run

A two-provider follow-up was aimed only at the missing uniform tail
obstruction. It reserved 20 evolution call slots for two generations of five
candidates, with a 900-second stage timeout and a 24-call session ceiling.
Bundle: `runs/rule30-inverse-trace`.

No theorem or candidate is established:

- native evolution reached the stage timeout before returning its aggregate
  outcome;
- the final orchestration repeated the known open recurrence and expanding
  right-boundary obstruction rather than closing it;
- two generated Lean artifacts contained `sorry` and were correctly rejected
  as policy violations;
- zero of 72 extracted claims had accepting objective verification, final
  synthesis was empty, and scientific release was `NOT_ESTABLISHED`.

The only proposed Rule-30-specific ingredient was the monotonicity of OR in a
periodically driven right-defect system. No closed state, descent measure, or
period-uniform lemma was supplied. This is the same missing closure already in
the rejection ledger, not a surviving mechanism.

The run also found an application-level loss mode. The evolution wrapper
returned checkpoints only after *all* generations, so an outer timeout dropped
any completed earlier generation and exported no evolution ledger. Crosstalk
now snapshots after every completed generation, emits headless progress, and
exports `evolution/status.json`; a timed-out run retains its latest completed
checkpoint, candidates, and generation reports. This infrastructure fix does
not justify rerunning the same scientific prompt.

## Reproduction

From `experiments/rule30`:

```bash
uv run python -m unittest test_inverse_trace_probe.py
uv run python inverse_trace_probe.py --json
```
