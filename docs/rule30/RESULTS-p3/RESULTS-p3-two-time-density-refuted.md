# P3: the rises of rho are dense, so a sparse rise index is no shortcut; no lower bound follows

Date: 2026-09-18, corrected 2026-09-21. Bears on the open question left by
[the implicit boundary investigation](RESULTS-p3-implicit-boundary-investigation.md),
lines 772-779: both center parities reduce to an actual last-rise position
of rho (rising edges of A=low(B^h(0)), or the C-analogue) and a range parity
of Z=D+H, but constructing those two quantities cheaply across many time
steps was left open. It stays open; this measurement removes one hope only.

## Result

rho has positive density on every prefix measured, so its rises are not
sparse there, and a summary that stores or skips between rise positions is
not sublinear on that range. Nothing here bounds from below the cost of
answering the last-rise query by other means. Measured directly from
`p3_itinerary_conjugacy.k_prefix`
applied h times with state `'B'` starting at 0, then extracting the low bit
of each digit and computing rho_0=A_0, rho_i=A_i(1-A_(i-1)):

| digits | h | rises | density | max gap |
|---|---|---|---|---|
| 400 | 40 | 60 | 0.150 | 8 |
| 2000 | 100 | 500 | 0.250 | 10 |
| 2000 | 500 | 428 | 0.214 | 10 |
| 4000 | 1000 | 997 | 0.249 | 13 |

Density over these prefixes lies between 0.15 and 0.25 and does not decay
toward 0. The maximum gap between consecutive rises is 8, 10, 10, 13: it is
not in single digits and it does not fall as the scale grows, so these four
rows do not show bounded spacing.

Two properties of the measured object limit what the table can say.

1. B^h(0) is eventually periodic for every h. `k_digits` is a three-state
   Mealy machine reading digits low-first, B(0) is the constant word 1, and
   a Mealy machine maps an eventually periodic word to an eventually
   periodic word. Section 6 of
   [the session-limits supplement](RESULTS-p3-session-limits-supplement.md)
   already measured this tail, with a saved probe and artifact: period 16
   from N = 300, onset between 1.5N and 1.65N, always beyond the query site
   h-1. The rows here take 4 to 20 times as many digits as h, so most of
   each prefix is that periodic tail. Recomputed 2026-09-21 by the procedure
   above, with all four rows of the table reproduced exactly: the computed
   digit word satisfies d_i = d_(i+p) from digit 68, 155, 773 and 1617 to
   its end, with p = 8, 8, 16, 16, and 42 of 60, 461 of 500, 229 of 428 and
   596 of 997 of the counted rises sit there. Before the tail the density
   is 0.265, 0.252, 0.257 and 0.248, with the same maximum gaps 8, 10, 10,
   13. The reduction queries position h-1, inside that aperiodic head, so
   the head figures are the relevant ones. The split of the rises between
   head and tail comes from an in-session run of the existing module and is
   not saved as an artifact; the tail itself is the supplement's.
2. Positive density with bounded gaps puts no lower bound on a last-rise
   query. On the periodic tail just described the rises have positive
   density, 0.13 to 0.25 on these four rows, and gaps bounded by the period,
   and the last rise at or before any position is O(1) arithmetic from the
   period word. The number of rises bounds the size of an explicit list of
   them and nothing else.

**Verdict: refuted**, for a sparse or skip-list summary of rho's rise
positions only, on the measured range. The 2026-09-18 text of this section
said the gaps stay in single digits, and concluded that any index over the
rises "needs Theta(h) work to answer a worst-case last-rise query". The
first contradicts the table, and the second fails on the control in item 2;
both are withdrawn. Whether the last rise at position h-1 and the range
parity can be constructed from binary n in o(h) work is the open obligation
of ladder node `p3_control_construction`, and this measurement does not
touch it. The source doc's statement that the old one-pass B^2 kernel costs
O(m) on an m-digit prefix stands as a statement about that kernel.

## Scope

A finite measurement on four prefixes with h <= 1000. It removes only the
hope that rho's rises are sparse enough to index cheaply. It is not a lower
bound on any constructor. It does not address whether the intermediate
field A itself (not just its rise mask) admits a sublinear representation
through the Phi conjugacy or K-automaton of section 4 of the
implicit-boundary doc; that is a separate, harder question about the
itinerary map and remains untouched.

Reproduced with `p3_itinerary_conjugacy.k_prefix` (existing verified
module); no new script added.
