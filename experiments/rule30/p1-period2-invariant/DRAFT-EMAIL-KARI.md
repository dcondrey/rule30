# PARKED DRAFT -- NOT SENT

Status: **not sent, not approved for sending.** Parked deliberately while
the domination inequality (`RESULTS-CROSS-METHOD-INVARIANT-AUDIT.md`
section 6b) is attempted in-house, since knowing whether it is plausible
changes what the letter should ask for. Do not send without explicit
instruction.

Recipient: Jarkko Kari (Prof. Mathematics, Turku, `jkari@utu.fi`), already
a paper contact per `docs/rule30/paper/PUBLICATION-NOTES.md`.

## Factual corrections applied to the draft before parking

1. **SAT range.** An earlier wording said "exhaustive SAT is UNSAT through
   n = 30". That is **false as of 2026-09-04**. Verified state: UNSAT for
   every instance through `n = 29` **except** `(n=29, r=2, c=3)`, which is
   still running (1h59m elapsed at time of writing, empty log), and all
   four `n = 30` instances (`r=1,2` x `c=2,3`) are still running and
   unfinished. The draft below states the verified range. Re-check
   `uc/r1-skeptic/gap_29_2_3.log` and `gap_30_*.log` before sending; if
   they have since returned UNSAT, the range may be updated to n=30, but
   only then.
2. **n=16 measured value.** The draft quotes `0.37445` at `n=16`; that is
   the `c=2` value. The `c=3` value at `n=16` is `0.38010`. The draft now
   gives the range rather than the single favorable number.
3. **Marginal vs joint.** The draft states both halves explicitly, so the
   claim cannot be read as "the process is maximum entropy".

---

**Subject:** Rule 30 period-2 exclusion: maximal entropy under hard-core -- is a derandomization theorem the right target?

Dear Jarkko,

For the period-2 exclusion problem for Rule 30, we have been trying to
prove there is no binary source word whose forced continuation stays in
the hard-core shift and reaches a prescribed target state after n rows.
Computationally the statement holds as far as we can push it: exhaustive
SAT returns UNSAT for every instance through n = 29 (one cell at n = 29
and the n = 30 row are still in flight as I write), and the exact survivor
census gives H_r(n) = 0 for all n <= 13.

Every proof route we tried -- bounded automata, quotient congruences,
algebraic degree bounds, descent arguments, SAT core extraction,
Markov/DFA collapse -- failed for the same reason: the obstruction does
not localize.

The measurements now point at something sharper. The recurring per-row
survival rate, measured independently in three different codings, is

    lambda = phi/4 = (1+sqrt 5)/8 = 0.404508...

which is exactly the leading eigenvalue of the trivial "uniform over 4
states, subject only to no-11" transfer matrix

    M = [ 0    1/4 ]
        [ 1/4  1/4 ]

The first-row survival predicted by that null model is 3/8 = 0.375;
measured values are 0.37506 at n = 14 and 0.37445-0.38010 at n = 16
(the two target states). Marginally, the forced dynamics is statistically
indistinguishable from maximum entropy under hard-core.

The important qualification is that this is a marginal statement only. The
same output sequence is provably *not* Markov at any bounded order: the
context-conditional frequencies for a fixed order-3 context swing across
nearly the whole interval as n grows, and the minimized survivor DFA
saturates 4^(h+1)+1 states through horizon 7, i.e. achieves no state
collapse at all. So the process is marginally maximum-entropy and jointly
not that process, simultaneously.

The first-moment consequence is what makes me want a second opinion:

    sum_{n>=1} (2 lambda)^n = phi/(2-phi) = phi^3 = 4.236...

and after the r+2 extra forced rows, the expected total number of
counterexamples over all lengths is about 0.69 at r = 0 -- just under one.
So the conjecture is true in the first moment with essentially no margin,
which would explain why counting bounds of the form C < 4 keep coming out
sharp but unprovable.

That suggests the real theorem is a domination inequality rather than a
structural one: show the actual per-step survival weight is dominated by
the null transfer matrix up to a uniform factor, so that 2*lambda < 1
turns the expected count into a genuine upper bound and emptiness follows
for all large n, with the remaining finite window closed by the existing
census. No automaton, no locality, no algebraic miracle required.

Two questions, if you have the time:

1. Is this "maximal entropy subject only to hard-core" signature a known
   phenomenon for nonlinear cellular-automaton column dynamics, or is it
   unusual enough to be worth reporting on its own?
2. Is there a standard tool for proving such a domination inequality when
   the process is provably not Markov at any bounded order, but behaves
   marginally as though it were?

I am happy to share the exact construction, the SAT certificates, and the
full list of ruled-out routes if any of it would be useful.

Best,
David Condrey
