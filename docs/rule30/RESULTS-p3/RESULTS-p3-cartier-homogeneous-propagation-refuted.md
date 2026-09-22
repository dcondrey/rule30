# P3: the Cartier accumulated correction does not propagate homogeneously

Date: 2026-09-18. Closes the open question left by
[the implicit boundary investigation](RESULTS-p3-implicit-boundary-investigation.md),
lines 807-810 and 1170-1173: the parity-string Cartier local correction
eliminates the odd-time observer, but "constructing that row and summing E
are still algorithmic obligations," and the
[four-period central-carry result](RESULTS-p3-four-period-central-carry.md)
only closes evaluation of a supplied history under a certified even period
with a four-cycle one-period action, not construction of that history at
further spatial depths.

## Result

The natural extension — a fixed-size (state count independent of column
depth) homomorphism-based annotation, evaluated per block via the
four-period-central-carry algebra and propagated homogeneously from column
j's annotation to column j+1's — is refuted by a witness on the repo's own
saved actual zero-orbit data (`experiments/rule30/p3_four_period_central_carry.py`,
`verify()`):

- `z_0 = (1230)^8` and `z_1 = (12130300)^4`, both length 32, both actual
  columns of the real zero orbit.
- Both give the identical complete 10x10 affine annotation (identity
  matrix, phase 0).
- Their successor-column zero-images differ:
  `[0,0,0,0,0,0,0,0,0]` vs `[0,0,1,0,0,0,0,0,0]`.

Two columns with identical annotations diverge one column later, so no
fixed-size finite-group-homomorphism summary can be propagated to
recursively certify the period/four-cycle premises a deeper column would
need. The O(P) per-block evaluation the four-period result gives is real
but conditional on already holding a certified period at that column;
certifying the next column's period from this column's summary is exactly
what the witness blocks.

**Verdict: refuted**, for the class of fixed-size homomorphism-based
annotation schemes. Combined with the general finite-group obstruction
already proved in section 7b of the source doc, this closes the Cartier/
four-period-carry line of attack as a route to a sublinear P3 constructor.

## Scope

Not excluded, and not a concrete lead without new algebra: non-homomorphic
annotations, growing or position-dependent state, or a cancellation
restricted to the marked query diagonal rather than general columns. The
source docs flag these as open but propose no candidate mechanism for any
of them.

A stale doc-path bug was found in `p3_four_period_central_carry.py`'s
`main()` while running its `verify()` function directly; `main()` itself
was not touched (experiment code, carve-out from autonomous-fix authority).
