# Refutation: attempt-zero-entropy

Date: 2026-09-16. Refuter of `attempt-zero-entropy.md`. Verdict: refuted. Fatal step: Step 6, the "iff".

## Fatal step

Step 6 proves one implication and asserts two. From `|R_m| <= 2^(D(m)+1)` it follows that `D(m) = o(m)` implies `h(R) = 0`, and (with Fekete, `|R_m| >= 2^(h m)` for a factorial language) that `h(R) > 0` implies `D(m) >= h(R) m - 1`. Those are the same implication read twice. The converse, `h(R) = 0` implies `D(m) = o(m)`, is never argued. Counting cannot give it: a language can have subexponentially many words each of which needs a full-width witness. Yet the Claim section says the document "reduces `h(R) = 0` to one statement, (W)", and the "What is actually proved" list records `h(R) = 0 iff D(m) = o(m)` as U, "up to one-sided constants". A missing direction is not a constant.

The gap is load-bearing three times over.

1. Step 7's mechanism is aimed at (W). (W) is strictly stronger than `h(R) = 0`, so even a proof of the mechanism's negation would leave `h(R) = 0` open, and the "CONJ in both directions" framing of (W) is not a framing of `h(R)`.
2. The proposed decisive computation is misread. "`D(60)` near 119 kills (W)" is right; the document's own equivalence would then have it kill `h(R) = 0`, which nothing proves. Only the sublinear outcome is informative (it proves `h(R) = 0`); the linear outcome says nothing about `h(R)`.
3. The data already sit in the uninformative branch. Brute force over all light-cone seeds (`2^(2m-1)` seeds, run here, counts match the m60 record exactly) gives

       m     1  2  3  4  5  6  7  8  9 10 11 12 13
       D(m)  1  2  4  6  6  7  8  9 10 11 11 12 14

   `D(m) >= m` for `m >= 12`, slope about 1. The words that need the widest seed are the alternating ones (`0101010100`, `101010100`, `0010101010100`): a period-2 trace of length `m` needs a seed of width about `m`. These are exactly the words Step 7 says a narrow seed can mimic, and they are the wall pattern of Step 4. At every length computed, (W) is failing linearly while the record's local rate falls (0.130 bits at `m = 60`) and the fits cannot separate `h(R)` from 0. That is the profile of the unproved direction being false: few words, each needing a wide witness.

## Steps checked and standing

- Step 1: the Boolean derivation is correct (`pin(2k) = 0`, `pin(2k+1) = 1`; the case split on `rho_k` gives `rho_(k+1) = [s(2k,1..3) = 000]`). U stands.
- Step 2: correct, trivial.
- Step 3: `00000` is proved in the archive (`RESULTS-RIGHT-FILTERED-MORTALITY.md`, light-cone lemma) and is in the MFF record; the block language and `lambda = 1.5342` check numerically (`lambda^5 = 8.500 = lambda^3 + lambda^2 + lambda + 1`). Stands.
- Step 4: interior cells see `(0,1,0)` or `(1,0,1)` and are fixed; cell `p` gives `s(p-1) XOR 1`, independent of `s(p+1)` for every block length including 1. The insulation of column one beyond the light cone is real: with the block consumed at `T`, cells `<= p` at `T` depend only on cells `<= p` at `t`, so the far seed first reaches column one at `T + p`, later than `t + p`. Stands.
- Step 5: stands, but is longer than needed. For the maximal block with `q >= 2`, `s(t+1,q) = NOT s(t,q-1)` and maximality forces `s(t,q-1) = s(t,q)`, so cell `q` leaves at every step: the wall loses exactly one cell per step, not "at most one", and is consumed in exactly `p - q + 1` steps (one more at most when `q = 1`, since the pin alternates). Nothing in the document relies on the weaker form.
- Step 6, forward half: stands.
- Step 7: CONJ as labelled; the three objections in "Where it fails" are fair. The `|R_13| = 156` figure matches the record.

## What survives

- `D(m) = o(m)` implies `h(R) = 0`; `h(R) > 0` implies `D(m) >= h(R) m - 1`. One-way only.
- Steps 1 to 5 as listed, with Step 5 sharpened to exact one-cell-per-step consumption.
- The headline "neither direction is proved" is true, but the document's route to it is not a reduction. The honest statement is: (W) is a sufficient condition for `h(R) = 0`, it fails at every length where `D(m)` has been computed (`m <= 13`, `D(m) >= m` from `m = 12`), and no reformulation of `h(R) = 0` that is both necessary and sufficient has been found.
