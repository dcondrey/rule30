# The 4-cell unit as the primitive object: what the frame gives, and what it costs

Date: 2026-09-07.  Arm: `experiments/rule30/spacetime-tiling/`.
Reproduce: `uv run --with numpy python experiments/rule30/spacetime-tiling/tiling.py 2000`;
spec: `uv run --with pytest --with numpy python -m pytest -q` there.

Status: **`K/U` — the frame is legitimate and absent from this archive, its one
new structural fact is exact, and the mechanism it suggests is measured dead.
No prize problem is advanced.**

## 0. The proposal

Stop reading the diagram one row at a time.  Take as the primitive object the
four cells the rule actually relates:

```text
        a   b   c          (t,   x-1) (t, x) (t, x+1)
            d              (t+1, x)
```

with `d = a XOR (b OR c)`.  Exactly 8 of the 16 assignments are legal, so the
spacetime diagram is a two-dimensional subshift of finite type on 8 tiles, and
space and time are treated alike instead of one being propagated into the
other.

**Archive status: absent.**  A keyword census of `docs/` returns zero files for
"subshift of finite type", "tiling", "tetromino" or "two-dimensional subshift";
the one "Wang" hit is an author name (Guan & Wang 2011).  `ARM7-dyadic-spacetime-grammar.md`
is *not* this: its "spacetime tiles" are quadtree blocks in a P3 compression
probe, not the rule's local constraint.

## 1. What the frame gives: two exact facts

**(i) Only two of the four sites are determined by the other three.**
`d` is the rule; `a` is left permutivity, `a = d XOR (b OR c)`.  Solving for
`b` or `c` fails, because the OR is not invertible in either argument.  So the
tile set has exactly two determinism directions, and the two failures are
precisely the OR's arguments.  This is where Rule 30 loses information, stated
without reference to any frame.

The Rule 90 control sharpens it rather than merely passing.  Rule 90's tile is
`d = a XOR c` and never reads `b` at all, so `b` is undetermined there because
it is a **dummy** — the tile set is a product with a free coordinate.  Rule 30
reads all four sites and is still non-invertible at two.  Same arity, different
reason: "two of four" is not a generic fact about 4-cell units, it is the OR.

**(ii) The tile is unbalanced across the two sublattices, and the odd site
enters only through the OR.**  Of the four sites, `a`, `c` and `d` all have one
parity of `t+x` and `b` has the other.  Hence the exact dichotomy

```text
c = 1  =>  d = NOT a        the other sublattice is irrelevant
c = 0  =>  d = a XOR b      the sublattices are coupled
```

The first line is verified cell by cell over the whole interior cone to
`T = 2000`.  This is the same OR dichotomy as
`NEXT-DIRECTIONS-post-rung2.md` section 1, but stated as a sublattice coupling
rather than a column identity, and it is the entry point of the Rule 18 defect
method (Eloranta & Nummelin 1992): fix the autonomous sublattice as a
background, treat the coupled sites as defects.

## 2. What it costs: the coupling is not rare

For that method the autonomous branch must dominate.  Measured on the lone
seed:

| branch | density of interior sites |
|---|---:|
| `c = 1`, autonomous (`d = NOT a`) | 0.5005 |
| `c = 0`, coupled (`d = a XOR b`) | 0.4995 |

and the coupled density is `0.4969..0.5004` in every `x/t` bucket from `-1.0`
to `+1.0` — flat across the whole cone, including the ordered left region.
Maximal runs of the autonomous branch along a row have mean length 2.02 and
maximum 12 at `t = 4000`.

So the sublattices are coupled at half of all sites, everywhere, with no sparse
regime anywhere in the diagram.  There is no background and no defect gas.
Rule 18's kink works because its background sublattice is exactly 0 and the
kinks are isolated; the Rule 30 analogue has a coupling density of one half.

## 3. Verdict

The frame is correct, it is genuinely absent here, and it is the right
instinct about a real bias — the archive does privilege the time direction.
But:

* as a *computational* method it is the ladder.  A transfer matrix on
  width-`R` vertical strips of this SFT is exactly route R7's `omega`-automaton,
  and inherits obstruction F, the free outer boundary.
* as a *structural* method it is blocked by section 2: the decomposition it
  exposes does not decouple.
* the SFT is deterministic downward, so the tiling literature's power —
  undecidability, aperiodic tile sets, forced structure — does not apply.  A
  deterministic SFT's configuration space is just the orbit space; naming it a
  tiling adds vocabulary, not constraints.

What survives is fact 1(i), which is worth keeping: it locates Rule 30's
information loss at two named sites of the local unit and separates that from
Rule 90's free coordinate, in a frame with no distinguished time direction.

## 4. Rotating the unit, and the light-ray reading

Two follow-on proposals, both settled by `rotations.py` in the same arm.

**Rotating the unit.**  Separate two things.  Rotating the *frame* — relabelling
which axis is read as time — is legitimate and changes no dynamics; that is the
light-cone frame change of `RESULTS-ordered-wedge-glide.md`.  Rotating the
*rule* — permuting the roles of the four sites — is informative only if some
rotation **fixes** rule 30.  None does:

```text
mirror(30) = 86      complement(30) = 135
orbit of 30 under <mirror, complement> = {30, 86, 135, 149}
```

Four members, and 30 is fixed by neither generator.  So every rotation of the
rule leaves rule 30 for one of three other rules, and a theorem about the
rotated system is obstruction B in its purest form — a statement about a
different automaton.  There is no rotational symmetry here to exploit, and that
is a fact about rule 30, not a limitation of the method.

Measured anyway, in case aperiodicity were fragile under mirroring (lone seed,
`T = 20000`, period cap 4000):

| schedule | centre period | centre density |
|---|---|---:|
| plain rule 30 / plain mirror | none / none | 0.5060 |
| alternate rule each step | none | 0.4955 |
| alternate every 4 steps | none | 0.5056 |
| switch on the centre value | none | 0.3986 |
| switch when the centre hits 0 | none | 0.3986 |

Every schedule keeps the centre aperiodic within the cap.  The two
centre-controlled rows agree exactly because they are mirror images of each
other and the lone seed is its own mirror, so their centre columns coincide
cell for cell — a consistency check, not a coincidence.  Switching does move
the density (0.399 against 0.506), confirming these really are different
systems, which is the point.

**The trigger family, swept** (`triggers.py`).  "Rotate the block each time we
hit ..." was run under six readings of the trigger — centre is 0; centre is 1;
the unit at the centre is quiescent; four consecutive 0s; every fourth step;
and a chosen state of the four-state kernel — crossed with two rotation sets,
the mirror pair `{30,86}` and the full Klein four-group orbit
`{30,86,135,149}`, plus never/always controls.  Sixteen Rule 30 systems,
`T = 20000`, period cap 4000.

**Every one keeps the centre aperiodic.  Every one of the eight Rule 90
controls locks, to period 1, 2, 3, 4, 6 or 8.**  Centre density across the
Rule 30 systems ranges over `0.376..0.668`, so the schedules genuinely change
the dynamics; they simply never make it periodic.  The family is a clean
separator, in the direction obstruction B wants: it preserves Rule 90's
periodicity and does not disturb Rule 30's aperiodicity.

One structural note falls out.  Rule 90's orbit under `<mirror, complement>`
has only **two** members, `{90,165}`, because rule 90 is its own mirror; rule
30's has four because nothing fixes it.  That asymmetry is why the rotation
question even has different answers for the two rules.

**The light-ray reading.**  Describing the unit as a ray striking `a, b, c` and
casting `d` as a weak projection below is exactly right, and it names the
archive's central object: the rule is a `3 -> 1` map and the fibers of that map
are what 35 files here already call the fiber.  Section 1(i) is the sharp form
of "weak": the projection can be inverted at `d` and at `a`, and at neither `b`
nor `c`, so the projection's kernel is precisely the OR's two arguments.  The
ray reading therefore re-derives the retained fact rather than adding to it.
Rays of intermediate slope were probed separately and carry no periodicity:
only the two exact light-cone directions do, because any other rational slope
crosses infinitely many diagonal frames.

## 5. Explicit non-claims

* Nothing here bears on P1, P2 or P3.
* The coupling density is measured on the lone seed to `T = 4000`; no limit is
  proved to exist.
* No claim that a 2D-SFT treatment of Rule 30 is unpublished elsewhere; the
  census in section 0 covers this repository only.
* The Eloranta & Nummelin comparison is a method analogy; its citation is taken
  from the publication record, not read in the primary.
