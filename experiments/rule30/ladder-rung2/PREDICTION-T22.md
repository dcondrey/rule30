# Registered prediction, written before reading sweep30-22.log

Measured so far (exhaustive cyclic core for T <= 12, vectorised on-cycle
search for T = 14..20):

| T  | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
|----|---|---|---|----|----|----|----|----|----|
| max minimal period of col_-1 | 4 | 6 | 4 | 10 | 6 | 14 | 4 | 6 | 10 |

Reading: at time period T = 2m the largest achievable minimal period of
`col_{-1}` is `2 * (largest prime factor of m)`.  New periods appear only at
T = 2p' with p' prime: p' = 2,3,5,7 gave 4,6,10,14; the composite m = 4,6,8,9,10
gave nothing beyond their prime divisors.

**Prediction.**  T = 22 (m = 11, prime) yields a torus with `col_{-1}` of
minimal period exactly 22.

**What a miss means.**  If T = 22 gives max period 2, 4, or any value < 22, the
"2 x prime" reading is refuted, the achievable period set may be finite, and
the mode (ii) limitation theorem stays partial (only the q's not divisible by
lcm(4,6,10,14) = 420 are covered).  That is the K2 branch of the
pre-registration.
