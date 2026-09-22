# The quarter-wave current is not an additive time-difference on the seed orbit, windows up to 8

Status: **proved, by exact integer certificates (§7). No ladder statement changed; "current sum o(t)" stays
conjectured.** One sub-family of the lever the history-window kill leaves
standing is closed on the orbit. The rest of it is not touched.

## 1. What was open

The telescoped identity `A(T) - T/2 = P_T + sum_(t<T) (K_t - 1/2)` puts the
centre column's density excess into the current `K`. If `K_t - 1/2` were an
exact time-difference `Phi(x^(t+1)) - Phi(x^t)` of some local functional on the
orbit, the current sum would telescope.

`r30-p2-history-window-horizon-refuted-shape-independent` refutes every
correction reading a bounded window inside radius 18, of any support shape, and
states what survives as exactly "an `h` reading a cell outside `[-18, 18]`:
untruncated half-row sums ... and windows growing past radius 18". The
seam-routes twisted-conservation kill covers laws that hold on **every** input,
which says nothing about identities holding only on the orbit. Untruncated
half-row sums on the orbit were therefore untested, and no least-squares or
null-space fit of the current exists anywhere under `experiments/rule30`.

## 2. The test

For window length `m` and phase period `p`, take

    Phi(x) = sum_i rho(i mod p, x_i .. x_(i+m-1)),   rho(., 0^m) = 0,

summed over every window start `i >= 0` (right half-row, the range `K` itself
reads) or over every start (full row). Asking `2K(x^t) - 1 = Phi(x^(t+1)) -
Phi(x^t)` for every `t < T` is one linear system in the `p(2^m - 1)` unknowns,
row `t` being the difference of the phase-indexed window-count vectors of
consecutive rows. Consistency is decided by comparing the ranks of `A` and
`[A|b]` modulo two independent 31-bit primes, which must agree.

**Controls, all passing, all required before any verdict prints.**

- `K` and `P` computed here equal `quarter_wave_current_audit.scalar_current`
  and `scalar_potential` at every `t < 128`, and `x_0 = P(Fx) - P(x) + K(x)`
  holds at every `t` in range.
- **Positive control.** By that identity the target `K - x_0` is exactly
  `-(P(Fx) - P(x))`, and `P` is additive with a phase-4 weight on the right
  half-row. So the same system with that target **must** be consistent at
  `p = 4`. It is, and it is correctly **inconsistent** at `p = 1` and `p = 2`,
  where no phase-4 weight can be expressed. The solver therefore finds this kind
  of solution when one exists and says no when it does not, and a mis-specified
  half-row or phase convention would have failed here first.
- A planted random `rho` at `m = 5`, `p = 2` is recovered.

## 3. Result

At `T = 2048`, **no configuration is consistent**: every `m = 1..8`, every
`p in {1, 2, 4}`, on both the right half-row and the full row. The largest
system has 1020 unknowns against 2048 equations.

A trial at `T = 256` returned consistent exactly for the six configurations
with more than about 256 unknowns, which is the underdetermined regime and
carries no information. Inconsistency at `T = 2048` holds at every larger
horizon, since added rows cannot restore consistency.

## 4. What it changes, and what survives

The surviving lever of the history-window kill loses one sub-family on the
orbit: **additive, phase-periodic with period 1, 2 or 4, window at most 8**,
summed over the whole half-row or row. That is the untruncated shape the kill
reserved, at these parameters.

Still standing, and not claimed: windows longer than 8; phase periods other
than 1, 2, 4, including 8 and 16, which the clocked-window kill reaches;
non-additive functionals; functionals depending on history rather than the
current row; and coefficients that vary with scale or time. A positive answer
would also not have been success, since a telescoping `Phi` over a row of width
`2t` is `O(t)`, not `o(t)`, without further control.

## 5. Scope

Seed orbit `t < 2048`, `m <= 8`, `p in {1, 2, 4}`, right half-row and full row.
**Proved over Q** (§7): exact integer dual vectors `y` with `y^T A = 0`,
`y^T b != 0` are extracted and checked in integer arithmetic; the modular rank
test above was the search, the certificate is the proof.

## 6. Files

`orbit_additive_current.py` (`orbit_additive_current.log`), 38 s
single-process. Writes no tracked artifact. Logs are hidden by the global
ignore; `git add -f` to commit them.

## 7. Exact certificates: the whole table is proved, not computed

§5 recorded this result as computed, because the consistency test is modular
rank. `exact_certificate.py` turns it into a proof. For an inconsistent system
it selects a small set `S` of rows exposing the inconsistency, solves exactly
over `Q` for the one-dimensional left null vector of `A_S`, clears denominators
to an integer vector `y`, and checks `y^T A_S = 0` and `y^T b_S != 0` in plain
integer arithmetic. Zero-extended to the other rows, `y` proves `A rho = b` has
no rational solution, however `y` was found; the row selection is heuristic and
certifies nothing, only the integer check does.

**Nesting makes two certificates enough.** A window-`m`, phase-`p` functional
with `p | 4` and `m <= 8` equals the window-8, phase-4 functional
`rho_8(phase, w) = rho_m(phase mod p, low m bits of w)` over the same window
starts, with `rho_8(0^8) = 0` preserved. So one certificate for `(m = 8, p = 4)`
per support proves all 24 systems on that support.

| support | rows in `S` | unknowns | largest entry of `y` | `y^T A_S = 0` | `y^T b_S != 0` |
|---|---|---|---|---|---|
| right half-row | 639 | 1020 | 394 digits | yes | yes |
| full row | 513 | 1020 | 360 digits | yes | yes |

Both certificates are in `exact-certificate-m8-p4.json`, 50 minutes of
single-process exact arithmetic. Smaller certificates at `m = 4, 6, 7` were
extracted on the way and agree; they are implied by the `m = 8` pair and kept
only as a record of the run. The inconsistency appears early in the orbit: at
`m = 4` it needs only the first 40 rows on the half-row.

**Status is now proved**, for every window `m <= 8` and phase period
`p in {1, 2, 4}` on both supports, over the orbit `t < 2048` and therefore at
every larger horizon. Windows above 8, other phase periods, non-additive and
history-dependent functionals remain exactly as open as §4 says.
