# Refutation: attempt-masking-entropy

Verdict: refuted at step 8. Steps 1 to 7 check out and survive.

## What was checked

All of steps 1 to 5 were recomputed from the spec (pin s(t,0) = t mod 2,
columns 1..k under the rule, column k+1 an arbitrary 0/1 sequence in t,
trace read at even times), using the two-step transition graph on 2^k
states and a subset construction to a deterministic presentation. The
depth-3 table in step 5 matches the computation entry for entry,
including the transient state (1,1,0). Word counts and entropies:

| k | words of length 1..12 | h(S_k) |
|---|---|---|
| 1,2,3 | 2 3 5 8 13 21 34 55 89 144 233 377 | 0.69424 = log2 phi |
| 4 | 2 3 5 8 12 18 28 43 66 101 155 238 | 0.61745 |
| 5 | 2 3 5 8 12 18 27 40 58 83 119 170 | 0.50902 |
| 6 | 2 3 5 8 12 17 25 36 50 69 95 129 | 0.44148 |
| 7 | 2 3 5 8 12 17 25 36 50 68 91 119 | 0.37725 |
| 9 | same as R through 12 | 0.32230 |
| 12 | same as R through 12 | 0.25784 |

R_1..R_12 from the record: 2 3 5 8 12 17 25 36 50 68 91 119, so R is
contained in every S_k as claimed and S_1 = S_2 = S_3 = golden-mean shift
exactly. Steps 1, 2, 3, 4, 5 are correct. Step 7's arithmetic (Parry
frequency 0.2764, ratio 0.959) is correct. The nested-limit claim
h(cap S_k) = lim h(S_k) = h(R) is correct.

## Fatal step: 8

Step 8 asserts, labelled (U, using C), that "no S_k with k of moderate
depth can have zero entropy" and that "the masking approach cannot prove
h(R) = 0 at any finite depth". The offered justification is that R grows
by a factor 1.11 per symbol at m = 48 and a zero-entropy sofic shift grows
polynomially. That inference is invalid. A zero-entropy sofic shift on N
states has language growth up to degree N-1 polynomial, and the
deterministic presentation of S_9 already has 87 states, S_12 has 413. A
per-symbol ratio r at length m is consistent with polynomial growth of
degree about m(r-1); the record gives 3.98 at m = 20, 5.17 at m = 48,
5.54 at m = 60. Nothing in the counts separates "exponential with small
rate" from "polynomial of degree 5 or 6". So the counts cannot exclude
h(S_k) = 0 at some finite k, and if that happened it would prove h(R) = 0
outright, the opposite of what step 8 concludes. Step 8 is therefore
unproved in both directions: it neither shows every S_k has positive
entropy nor shows R is not polynomially growing. The author's own caveat
("leans on the measured count") understates this: the count does not
bear on the question at all.

The headline consequence that fails is the third bullet of "What is
actually proved": a masking bound is not merely "equivalent in kind to
the forbidden-factor list". Unlike a truncated forbidden list, a single
finite S_k can in principle certify h(R) = 0, and the sequence h(S_k) is
the only object in the attempt whose limit is h(R). Whether some finite
S_k has zero entropy is exactly the open question, and the attempt gives
no argument either way.

## Secondary errors, not fatal

- Step 6, sentence "S_k contains every 11-free word of length
  <= (k+1)/2": false as written. The correct statement (which the same
  step uses) is that S_k agrees with R on words of length <= (k+1)/2,
  and R already lacks 00000 at length 5. Harmless to the argument.
- Step 6 and the CONJ bullet are settled by the table above: 00000 is
  excluded at k = 4, not "somewhere in 4..8, certainly by 9";
  h(S_4) = 0.61745 equals the {11, 00000} SFT bound to five places, and
  h(S_5) = 0.509 is already below 0.6174. The light-cone guarantee
  (agreement through m <= (k+1)/2) is far from sharp: S_7 agrees with R
  through m = 12, where the guarantee is m <= 4.
- The claim in the headline that masking "cannot improve on {11, 00000}"
  is true only for depth <= 3 and is contradicted at depth 4 (equal) and
  depth 5 (strictly better). The body says this correctly; the summary
  line does not.

## What survives

- (U, verified) S_1, S_2, S_3 are each exactly the golden-mean shift, so
  masking through three columns gives h(R) <= log2 phi = 0.6942 and
  nothing tighter.
- (U) The density-of-zeros bound h_mu <= 1 - mu(1) is weaker than
  log2 phi under the Parry measure and trivial without a lower bound on
  mu(1).
- (U) h(S_k) is a nonincreasing sequence of computable upper bounds with
  limit h(R); computed values reach 0.258 at k = 12, below the m = 60
  count bound (1/60) log2 103220 = 0.2776.
- Nothing about h(R) = 0 is proved, and nothing about the impossibility
  of proving it by finite-depth masking is proved either.
