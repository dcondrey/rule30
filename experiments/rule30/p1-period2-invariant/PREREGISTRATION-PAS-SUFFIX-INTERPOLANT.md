# Preregistration: PAS suffix/interpolant audit

Date: 2026-09-02

Status: frozen before the substantive search.

## Question

For a word `W=L U` with `|L|=j`, the pull-row alpha-support (PAS)
contrapositive separates into two pieces:

- the statement that `alpha_(j,k)` is constant for `j<=k<=n` depends only
  on the suffix `U`; and
- the statement that the original forced endpoint has a nonfinal pull at
  row `j` may also depend on `L`.

Can the information crossing the cut between `L` and `U` be represented by
a fixed finite state, or by an exact recurrence in `(j,|U|)`, so that the
two languages can be proved disjoint?

## Frozen experiment

1. Verify directly that the alpha profile for `k>=j` is independent of the
   chosen length-`j` prefix, including prefixes outside the hard-core
   language.
2. For small exact rectangles `(j,m)`, enumerate hard-core suffixes `U` of
   length `m` and all compatible hard-core prefixes `L` of length `j`.
3. Record:
   - the zero-profile suffix language `Z_(j,m,c)`;
   - all endpoint triples `(previous, forced, next)` achievable from a
     compatible prefix;
   - whether a bounded suffix statistic separates `Z` from nonfinal pulls;
   - transition/minimization data for any candidate finite-state summary.
4. Search only the frozen range `0<=j<=8`, `1<=m<=12`.  Larger ranges may
   be used only after a candidate recurrence has been written down first.

## Success and failure criteria

A success is an exact identity, a branch-complete finite transition table,
or a recurrence whose induction statement is independent of the tested
rectangle.  Mere disjointness in the rectangle is evidence, not a proof.

The finite-state route is rejected if the required boundary state or
distinguishing suffix width grows throughout the frozen range without a
stable recurrence.  Simple endpoint telescoping is already a negative
control: `W=121`, tail `3`, row `0` has alpha profile `(0,1,1,0)`, so its
two endpoints agree although PAS holds.

