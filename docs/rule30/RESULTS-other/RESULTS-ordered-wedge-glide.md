# The left light-cone frame: an exact glide form of a known NKS fact

Date: 2026-09-07.  Arm: `experiments/rule30/ordered-wedge/`.
Reproduce: `uv run --with numpy python experiments/rule30/ordered-wedge/ordered_wedge.py 4000`;
spec: `uv run --with pytest --with numpy python -m pytest -q` in that directory.

Status: **MEASURED (`C/M`).  No prize problem is advanced.  The central
phenomenon is prior art — NKS p. 871 — and this report says what is new here
and what is not.**

A first draft of this document overclaimed in three specific ways.  They are
recorded as retractions in section 6 rather than quietly removed, because each
is an instance of a failure mode this archive already warns about.

## 0. What is prior art

Wolfram, *A New Kind of Science*, p. 871 (notes to p. 27), records that on the
lone-seed Rule 30 diagram the diagonal `n` cells in from the **left** edge is
eventually periodic, with the first occurrence of each period at depth

```text
period    2      4      8     16       32          64
depth     3      8     29    400    87,867    2,107,985,255 or more
```

and that the boundary between the left repetitive region and the right random
region moves left at about `0.252` cells per step.  Separately, p. 949 gives
`0.2428` for the left edge of a *difference* pattern — a different quantity;
`PATH.md:269` already records both and warns they are distinct.

So "the left region of Rule 30 is ordered, with a very slowly doubling period"
is known, and the right-edge exponential growth is Rowland's.  Neither is a
discovery of this archive.

## 1. What is new here

1. **The two light-cone frames written as exact recurrences**, which is what
   makes the asymmetry mechanical rather than pictorial:

   ```text
   left    L_j[t] = s(t,-t+j) = L_{j-2}[t-1] XOR (L_{j-1}[t-1] OR L_j[t-1])
   right   R_j[t] = s(t, t-j) = R_j[t-1]     XOR (R_{j-1}[t-1] OR R_{j-2}[t-1])
   ```

   In `R_j` the self-dependence is through the XOR, so `R_j` is the running
   parity of a function of strictly lower indices — the induction behind the
   power-of-two right-diagonal periods.  In `L_j` the self-dependence is
   through the **OR**, which is absorbing: when `L_j[t-1]=1` the update
   collapses to `L_j[t] = NOT L_{j-2}[t-1]` and the middle argument is
   discarded.  `R_j` is the `E_j` of `RESULTS-diagonal-periodicity.md`; `L_j`
   is not written down anywhere else in this archive.

2. **The glide form.**  Left-frame periodicity of period `g` at every depth
   `j <= D` is exactly the spacetime isometry

   ```text
   s(t+g, x-g) = s(t, x)     on   -t <= x <= -t + D,
   ```

   verified directly in `(t,x)` coordinates on 5.5M cells at `T = 4000` with
   zero exceptions, and holding there for `g` a multiple of 16 and for no
   other `g` in `{1,2,4,8,12,15,17,20,24,28,30,40}`.  Writing it this way is
   what connects the left region to the torus objects of
   `RESULTS-ladder-rung2-periodic-realizability.md`, which are also glide
   objects.

3. **Independent reproduction of the whole NKS depth table**, which is what
   pins the coordinate identification: `L_j` *is* Wolfram's "diagonal `j` cells
   in from the left edge".  The arm computes first occurrences at
   `j = 3, 8, 29, 400` for periods `2, 4, 8, 16`, and finds the first `j` whose
   trace is not 16-periodic at exactly **`j = 87,867`** — the published depth,
   to the unit.  Two of the arm's tests assert this.

4. **The Rule 90 split.**  Replacing the OR with XOR turns the left frame into
   a running parity too; the measured Rule 90 left-frame period is exactly `j`
   (`16, 64, 256, 1024, 4096` at those depths).  Rule 90 has no ordered region
   and no order/disorder boundary.  The left/right asymmetry is an OR
   phenomenon, and in the left frame the OR is what *creates* order rather than
   what destroys it.  This is the property `START-HERE.md` step 5 asks every
   proposal to name.

5. **A correction to obstruction A**, section 3.

## 2. The measurements

Left- and right-frame minimal periods, band recurrence, horizon 212,608:

| `j` | 0 | 16 | 64 | 256 | 1024 | 4096 | 16384 | 65536 | 87867 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| left period | 1 | 4 | 4 | 8 | 16 | 16 | 16 | 16 | **32** |
| left relative preperiod `d(j)` | 0 | 0 | 24 | 63 | 275 | 1296 | 5534 | 21926 | 29457 |
| right period | 1 | 256 | > 4096 | > 4096 | > 4096 | > 4096 | > 4096 | > 4096 | > 4096 |

Glide-16 violation density by `x/t` at `T = 4000`, `t in [T/2, T-16]`:
identically `0.0000` in every bucket left of `-0.30`; `0.1831` in
`[-0.30,-0.20)`; `0.4995 +- 0.002` — the coin-flip value — in all sixteen
buckets from `-0.20` to `+1.00`.

Row tails inside the ordered region carry **no spatial period** up to a cap of
2048, on bands of width 1337 and 2737.  The region is ordered in *time* and
aperiodic in *space*; plotted, it looks exactly as random as the bulk, which is
why a frame change rather than a picture is what exposes it.

## 3. Obstruction A is a right-boundary fact

`FACT-INDEX.md` records A as "`O(log t)` propagation cannot meet a `Theta(t)`
target" and `PATH.md` closes R4, "anything anchored at the right boundary", on
it.  Correct for the right.  The left is different in kind:

| | right boundary | left boundary |
|---|---|---|
| depth reached with period `<= P` | `~2.4 log2 P` | `3, 8, 29, 400, 87867, >2.1e9` for `P = 2,4,8,16,32,64` |
| growth of that depth in `log2 P` | linear | super-exponential |

Both are unbounded-period requirements at depth `Theta(t)`, so neither reaches
the centre column with a *fixed* period; but the left reaches vastly deeper per
unit of period budget, and the quantitative claim in A is false there.  The
honest left-side statement is not an obstruction with a slope in it — see the
retraction of screen J below — it is that the left-frame period is an unbounded
but extremely slowly growing function of depth, whose growth law is the open
question.

## 4. The live target, restated

Not "`L_j` has period dividing 16 for every `j`" — that is false at
`j = 87,867`.  The target is the **doubling law** of the left frame: which
depths `D_k` first carry period `2^k`, and why.  NKS sketches the mechanism in
a parenthetical — a doubling occurs when a diagonal becomes a white stripe and
the diagonal to its left has an odd number of 1s per block — and the left-frame
recurrence above, with its absorbing OR, is the natural place to make that
exact.  A proved doubling law would be a real lemma about the tame cone.  It
would not be P1, and by section 3 it would not cross the interface.

## 5. What this does *not* do

**It does not touch fiber rigidity.**  The missing step is still "periodic
centre forces a tame `col_1`" (`NEXT-DIRECTIONS-post-rung2.md` section 3).  The
ordered region is on the far side of the centre column's reach, and a
left-region theorem does not propagate rightward through the interface.  (An
earlier version of this sentence cited the one-column reach lemma, which was
retracted on 2026-09-07: the centre *does* force `col_{-k}` along a run of `k`
ones.  The reach is `O(log t)` rather than 1, which does not change the
conclusion here — the ordered region is `Theta(t)` away — but the correct
statement is in `NEXT-DIRECTIONS-post-rung2.md` section 1.)

**The composition argument of the first draft does not reach the centre, and
does not refute anything.**  The intended argument was: assume `(col_0, col_1)`
is `p`-periodic; leftward reconstruction is pointwise, so every `col_{-k}` is
`p`-periodic with the same `p` and a uniform onset; compose with the glide to
get `s(t,x) = s(t, x-16p)`.  Two holes, both fatal as stated:

* the glide is known only on the ordered region, while the reconstruction gives
  periodicity on the whole left half-plane, so the composition yields spatial
  periodicity only *inside* the ordered region — it does not produce a band
  advancing toward `x = 0`; and
* the spatial aperiodicity measured in section 2 is a property of the **real**
  seed diagram, which is not width-two periodic.  Under the hypothesis the
  diagram is a different one, whose ordered region may perfectly well be
  spatially periodic.  Measuring the seed cannot refute a hypothesis the seed
  does not satisfy.

So this is a *consequence* of the width-two hypothesis, not a contradiction
with it, and **Kopra 2023 Thm 3.5 stays in the chain.**  The check that would
give the argument content is on **synthetic** width-two periodic diagrams — the
five `T = 24` on-cycle witnesses of the rung-2 census are ready-made — asking
whether their ordered regions carry spatial period `16p`.  That is not run
here.

## 6. Retractions from the first draft of this document

1. **"Left-frame period is 16, bounded, for every `j`."**  False.  The scan
   reached `j = 65,536` and the plateau ends at `87,867`.  A horizon was read
   as a law, which is obstruction H in the form this archive most often meets
   it, and the published value that would have caught it was already cited two
   lines away in `PATH.md:269`.
2. **Screen J, "the ordered region's slope does not depend on the glide
   length."**  Retracted.  At `T = 4000..6000` every glide `>= 16` gave the
   same edge `0.2417..0.2464` because the binding constraint at that horizon is
   the *settling* time `d(j) ~ 0.34 j`, not the period.  The depth constraint
   only binds past `t ~ 1.3 * 87,867`, and there a longer glide does buy
   ground: glide 32 is valid to depth `2.1e9`.  The measurement was a
   finite-horizon artifact.
3. **The `0.252` attribution.**  The measured glide-violation edge is
   `0.2417` at `T = 4000`, which is nearer p. 949's difference-front `0.2428`
   than p. 871's order/disorder `0.252`, and is in any case a third cut — the
   glide-violation boundary — that has not been shown to coincide with either.
   The three should not be pooled without measuring them separately.

## 7. One numerical coincidence, flagged so it is not chased

`RESULTS-followup2-dendro-frost-year.md` section 4 reports rule 30 frost-year
densities `0.7481` and `0.2539`.  Those are time-densities of a predicate on
column 0, near `3/4` and `1/4` for the ordinary reason.  They are not the
ordered region's width fraction and have nothing to do with it.

## 8. Explicit non-claims

* No novelty is claimed for left-region order or for the depth table; both are
  NKS p. 871.  What is claimed as new here is the recurrence pair, the glide
  form, the Rule 90 split, and the reproduction that pins the identification.
* The glide identity is verified on finite windows and is not proved.
* No statement here bears on P1, P2 or P3, and section 5 records that the one
  route the first draft proposed does not survive.
