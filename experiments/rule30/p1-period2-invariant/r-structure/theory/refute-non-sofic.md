# Refutation of attempt (b): non-soficity of X_R

Verdict: refuted. The claim (X_R not sofic, R not regular) is not established by the attempt, which is what the attempt itself says. The logical steps 1, 2, 3, 4, 5, 8 check out. The fatal step is 9, as the author names it. But two of the record facts the attempt leans on (steps 6 and 7) are misread, and one of them overstates the evidence for the chosen pumping word by a factor of seven. All checks below are against `uc/r1-hardcore/r_exact_language_m60.json` and a direct simulation of the vacuum orbit to k = 3000 (script in scratchpad, not kept).

## Steps that hold

- Step 1. 100101 begins 3,995 words of R_60 (matches), 0100101 and 11 are in the forbidden list (matches), so 100101 has no left extension and L(X_R) is a proper subset of R. "R regular implies X_R sofic" is correct: the minimal DFA of a factorial regular language, with the sink removed, is a labelled graph whose bi-infinite path labels are exactly X_R (compactness for one inclusion, suffix-closure for the other), so X_R is an edge shift image, hence sofic.
- Step 2. (1_t) is the rule at cell 1 with the pin as left neighbour. 11 forbidden follows. Matches the record.
- Step 3. Every line of both case analyses was re-derived by hand; each equation is applied correctly and the two contradictions stand. 0000 allowed, 00000 minimal forbidden matches the record.
- Step 4. F(P^{n+1}) is contained in F(P^n) by factor-closure; a decreasing chain in a finite family stabilises; the contrapositive is right. The shape (suffix of P) P^n (prefix of z_n) is right because infinitely many drops force P^{n+1} in R for every n.
- Step 5. Standard compactness on the seed space; correct.
- Step 8. The light-cone count n(m) = floor((m-2)/2)+1 is right (the right neighbour enters only through the OR, so influence moves left at speed at most 1), and the Nerode pigeonhole is right. One defect in the statement: n(2j) = n(2j+1), and for such a pair V_{n(m)} u^{(m')} = trace(e_{m'}) is trivially in R, so the criterion as written ("for all distinct m, m' in M") is unsatisfiable unless M is restricted to distinct n-values, e.g. even m. Not fatal, since such an M exists.

## Misread record facts

- Step 7 (fatal for the evidence, not the logic). The vacuum trace is 0 1 0 0 0 1 0 1 0 (matches) and the period-7 stretch covers k = 2..153 (the attempt says 154; immaterial). But that stretch holds (1000010)^n as a factor only for n <= 21 (positions 7..153), not n <= 152. The attempt counted symbols of the periodic stretch as periods. So the only evidence that P^infinity is a trace for P = 1000010 is P^21 in R, three times the record's ceiling of n <= 8, not nineteen times. Whether P^22 is in R is open.
- Step 6, the word. The printed factor (1000010)^5 0000100100100001001001001001 has length 63 and is not in the record. The record's word is (1000010)^5 0100100001001001001001, length 57; the printed tail repeats the last six symbols of the fifth period. The substantive claim (F(P^n) drops at n = 4, 22-symbol tail) survives.
- Step 6, the rotation. "None of the 34 minimal forbidden factors with prefix (1010000)^2 has prefix (1010000)^3" is false. One does: 1010000101000010100001001001000010010000100001001001001000 (length 58), so F((1010000)^n) drops at n = 2. The inference "the drops depend on the rotation" is unsupported; on the record both rotations drop.
- Step 6, the periodic prefix lengths 27 (period 3) and 35 (period 5) are right when read as rotations of 001 and 00001 (the words begin 100 and 00010).

## Fatal step

Step 9. Nothing in steps 1 to 8 produces a single n beyond the record for either criterion, and the attempt's own diagnosis is correct: both criteria need a universal statement over the fibre of a long prefix, and no tool in the attempt sees the right half-line. The corrected step 7 makes this worse than stated: the pumping word P = 1000010 was chosen because P^infinity looked like a trace on the strength of n <= 152, and the actual support is n <= 21.

The claim "X_R is not sofic" therefore remains a conjecture with no proof and, after correction, thinner empirical backing.

## What survives

- U: 11 and 00000 forbidden, 0000 forces a_{2k+1} = 1 (steps 2, 3).
- U: L(X_R) is a proper subset of R; R regular implies X_R sofic (step 1).
- U: the chain criterion (4), compactness (5) and the transplant criterion (8, with M restricted to distinct n(m)) are valid sufficient conditions for non-regularity of R, and the chain criterion over L(X_R) for non-soficity of X_R.
- C: F((1000010)^n) drops at n = 4 and F((1010000)^n) drops at n = 2, each witnessed by one minimal forbidden factor; (1000010)^n is in R for n <= 21 from the vacuum orbit, and no further.
- Nothing about soficity of X_R or regularity of R.
