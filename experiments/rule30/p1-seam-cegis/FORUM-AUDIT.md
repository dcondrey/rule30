# Targeted Nersissian Parts II/III audit

Date: 2026-09-02

Status: **two exact discrete identities are retained, but neither supplies an
interval seam law for the P1 `(Q_n, Delta)` object.  The continuum/PDE layer
is not used.**

## Clean-room source capture

The Wolfram Community attachments were downloaded in fresh cookie jars from
messages `3671492` and `3673723`.  The notebook SHA-256 digests were:

```text
Part II  1066b56d809e5bde8a4b1dc68df73314fc59804ff7486f3483bfbbd10489e5f8
Part III 3694162dba739cf7293c5cea4adb7c4cfe2f7876746c0e189f0a60d976baaec7
```

Both messages currently attach the same two-page `rule30_wolfram.pdf`
preview (SHA-256
`e194ae2f635534d38f40bd0602e0d5e0dec2106beca51dac953b0f50755558fa`),
so the distinct notebooks, not the PDF preview, are the audited sources.

## Exact discrete content retained

Part II states, for its integer-lift generating polynomials,

```text
P_m(x+1)-P_m(x)
  = P_(m-1)(x) + P_(m-2)(x) + P_(m-1)(x) P_(m-2)(x),
P_1(x)=1, P_2(x)=x.
```

The shift `R_m=P_m+1` (called `Q_m` in that notebook) factors the source:

```text
Delta_x R_m = R_(m-1) R_(m-2) - 1.
```

Part III recompiles the same construction from a cellular automaton's ANF.
For Rule 30 it reproduces exactly the Part II source and the support recurrence

```text
S_m = Inc(S_(m-1) XOR S_(m-2)
          XOR (S_(m-1) OR-CONV S_(m-2))).
```

The repository's independent `nersissian_block_audit.py` already verifies
that last recurrence against the center-column oracle.  Part III adds a
generic compiler, not a new Rule-30-specific factorization.

## Relevance to the seam program

The notebook symbol `Q_m=P_m+1` is unrelated to the forced continuation
`Q_n(W)` in the P1 binary-wedge reduction.  The exact product factorization
is the integer-lift version of the familiar Rule-30 OR term.  It advances
successively in `m`; it does not compose two source intervals, expose an
entering/exiting `D8` phase, or isolate `Delta_j` at a split.

Consequently it is safe to reuse the discrete DPDE/support recurrence as an
independent coordinate system or equality-saturation rewrite, but it cannot
be treated as the missing `Join` theorem.  The PDE characteristics and
symmetry classification discard precisely the Boolean parity/carry data
needed by the seam target.

