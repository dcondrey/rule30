# a24_r7_mode2_bitpacked -- results

## Status correction

Two prior turns reported the extended col_-1 eventual-period sweep as
"still running in the background." That was wrong: the sweep had been
launched from a detached background shell in an earlier agent turn and
did not survive the turn boundary. When checked at the start of this
turn, the only live processes touching this directory were a stale
`tail -f` on `probe_fast.log` and a stale watcher shell polling a PID
that no longer existed -- no Python process was actually computing
anything. The numbers below are from fresh synchronous (or
harness-tracked background, explicitly waited on) work done in this
turn, not from that dead process.

## Correctness verification

`bitpacked.py main()` ran synchronously to completion this turn:

```
TOTAL cells checked: 273098  TOTAL mismatches: 0
Correctness check PASSED: build_words() is bit-for-bit identical to build_old().
```

10 configurations (rule in {30,90}, k in {1,2,3,4,5,6,8,16}, word
lengths p in {2,3,4}, phases 0/1), 273,098 cells compared cell-by-cell
between `build_old` (original O(T^2) reference) and `build_words`
(bit-packed rewrite). **0 mismatches.**

## Speedup

Apples-to-apples timing, identical config, both implementations run to
completion, T=200,000 (the largest T where `build_old` is still
feasible in reasonable wall time), k=2, w=01, rule=30:

```
build_old:     190.24 s
build_words:     8.68 s
speedup: 21.9x
```

**Measured speedup factor: 21.9x at T=200,000.**

## Largest T actually completed

Horizon sweep at k=2, w=01, rule=30, qmax=4096 (`build_words` only --
`build_old` is not feasible at these T):

| T | wall_s | col_-1 min eventual period (<= qmax=4096) |
|---|---|---|
| 20,000 | 0.29 | None (not found) |
| 100,000 | 2.58 | None (not found) |
| 400,000 | 28.7 | None (not found) |
| 1,000,000 | 179.09 | None (not found) |

The T=1,000,000 point was launched this turn as a harness-tracked
background command (not a detached/orphaned shell) and was explicitly
waited on to completion via a Monitor watch before being recorded here.

k-sweep at T=200,000, qmax=4096, rule=30, w=01 (from the pre-existing
`probe_fast.log`, section 1, trend sweep -- these had already completed
in an earlier turn, before the process was killed at the T=400,000
horizon point):

| k | T0 | wall_s | col_-1 min eventual period (<= qmax=4096) |
|---|---|---|---|
| 1 | 3 | 6.69 | None |
| 2 | 5 | 7.41 | None |
| 3 | 7 | 7.69 | None |
| 4 | 9 | 8.71 | None |
| 6 | 13 | 9.00 | None |
| 8 | 17 | 7.78 | None |
| 12 | 25 | 8.30 | None |
| 16 | 33 | 9.04 | None |
| 24 | 49 | 9.11 | None |
| 32 | 65 | 9.77 | None |
| 48 | 97 | 10.77 | None |
| 64 | 129 | 11.08 | None |

**Largest T actually completed and confirmed this turn: T=1,000,000
(k=2).** The full `probe_fast.py` script also had a T=2,000,000 phase
queued (labels `horizon_k2` and `deep_k`), but that was not run this
turn -- at the observed scaling (400k: 28.7s, 1M: 179.1s, worse than
linear, roughly T^1.7-T^1.8), T=2,000,000 would cost on the order of
10+ minutes and was out of the ~5-minute synchronous budget for this
turn. It is not reported here as complete; it was not run.

## Verdict on the extended sweep

No period found (`None`) at every T tested up to 1,000,000 (k=2) and
every k up to 64 at T=200,000, using qmax=4096. This is consistent with
a22's and a24's prior findings: absence of a detected period at these
horizons is not evidence that col_-1 fails to become eventually
periodic beyond the tested horizon -- it is a negative result at the
tested scale only, and R7 mode (ii) remains open.
