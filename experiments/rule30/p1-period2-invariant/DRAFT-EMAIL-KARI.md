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
   n = 30". That was **false when written on 2026-09-04** — at that point
   `(n=29, r=2, c=3)` was still running — and it became true only on
   2026-09-05. Sequence, kept intact so the claim's history is auditable:
   `(29,2,3)` returned UNSAT (`uc/r1-skeptic/gap_29_2_3.log`:
   `29 2 3 29473 91524 UNSAT 9440.73`), completing `n = 29`; then all four
   `gap_30_*` cells returned UNSAT between 00:33 and 02:42 on 2026-09-05.

   **The `n = 30` row is now complete and every cell is UNSAT**, 34.2
   CPU-hours for the row:

   | cell | vars | clauses | seconds | log |
   |---|---|---|---|---|
   | `r=0 c=2` | 29761 | 92417 | 10403.09 | `rw_sat_n30_20260903.log` |
   | `r=0 c=3` | 29761 | 92417 | 13242.53 | `rw_sat_n30_20260903.log` |
   | `r=1 c=2` | 30592 | 95001 | 27975.38 | `gap_30_1_2.log` |
   | `r=1 c=3` | 30592 | 95001 | 26581.05 | `gap_30_1_3.log` |
   | `r=2 c=2` | 31432 | 97613 | 24330.31 | `gap_30_2_2.log` |
   | `r=2 c=3` | 31432 | 97613 | 20477.98 | `gap_30_2_3.log` |

   **Trap for anyone re-verifying:** the grid is `r in {0,1,2}` x `c in {2,3}`,
   **six** cells, but only four are in `gap_30_*` logs — the `r=0` pair lives
   in `rw_sat_n30_20260903.log`. "All four gap logs returned" is not "the row
   is complete". Likewise `n=29 r=0 c=3` is in `rw_sat_n29_c3.log` in a
   different output format, so `grep '^29 0 '` misses it.

   `n = 31` has **not** been run: it was launched on 2026-09-05 08:34 and
   stopped 2m17s later with every log still empty, so no `n=31` cell has ever
   been solved. No runtime estimate for it is supportable — the per-cell
   `n=29 -> n=30` ratios range 0.88x (one cell got *faster*) to 12.55x.
2. **n=16 measured value.** The draft quotes `0.37445` at `n=16`; that is
   the `c=2` value. The `c=3` value at `n=16` is `0.38010`. The draft now
   gives the range rather than the single favorable number.
3. **Marginal vs joint.** The draft states both halves explicitly, so the
   claim cannot be read as "the process is maximum entropy".
4. **"Three independent codings" — REMOVED 2026-09-05.** The draft said the
   `phi/4` rate was "measured independently in three different codings". That
   claim is retracted: they are three codings of **one** process, not three
   independent measurements, so the wording overstated the evidence to a
   reader who would reasonably read "independently" as corroboration. The
   sentence now simply states the rate.
5. **Census range.** The body said `H_r(n) = 0` for `n <= 13`; the verified
   range is now `n <= 21` (every `r in {0,1,2}`, both `c in {2,3}`).
6. **P1 / light-cone.** If any future version of this letter mentions the
   departure index `k_dep`, it must not claim `k_dep = floor(n/2) - 2`. That
   is falsified: it misses at `n=10` and at `n=20` (both tails), and at
   `n=12` the two tails disagree, so no formula in `n` alone can be correct.
   The light-cone argument supplies a scale `~n/2`, not a formula. See
   `RESULTS-DISTINCT-CONTINUATION-COUNT.md`.

---

**Subject:** Rule 30 period-2 exclusion: maximal entropy under hard-core -- is a derandomization theorem the right target?

Dear Jarkko,

For the period-2 exclusion problem for Rule 30, we have been trying to
prove there is no binary source word whose forced continuation stays in
the hard-core shift and reaches a prescribed target state after n rows.
Computationally the statement holds as far as we can push it: exhaustive
SAT returns UNSAT for every instance through n = 30, with no gaps, and
the exact survivor census gives H_r(n) = 0 for all n <= 21.

Every proof route we tried -- bounded automata, quotient congruences,
algebraic degree bounds, descent arguments, SAT core extraction,
Markov/DFA collapse -- failed for the same reason: the obstruction does
not localize.

The measurements now point at something sharper. The recurring per-row
survival rate is

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
