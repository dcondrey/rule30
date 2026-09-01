"""ARM9: factor complexity p(k) of the Rule 30 center column (A051023).

Cobham: a k-automatic sequence has an asymptotic factor-complexity function
p(k) = O(k). p(k) is a property of the INFINITE sequence: for any fixed k,
p(k) is a fixed finite number (at most 2^k, since there are only that many
possible length-k binary strings), and the correct way to estimate it from a
finite prefix of length n is to watch p(k, n) -- the count of distinct
length-k factors within the first n symbols -- as n grows. p(k, n) is
non-decreasing in n and converges (from below) to the true p(k). A sequence
whose true p(k) is small (as an automatic/eventually-periodic sequence's
must be, since Cobham bounds it by O(k)) will show p(k, n) SATURATING
(flattening) well before n gets large. A sequence with no such bound keeps
adding new distinct k-factors roughly linearly in n, with no plateau.

An earlier version of this probe made a checkpoint-design mistake: it swept
k up to a large fraction of a FIXED n and found p(k)/k declining, which
looked like a control-passing signal but was actually the trivial ceiling
p(k) <= n-k+1 binding, not measuring anything about the sequence's real
complexity. See docs/rule30/ARM9-factor-complexity.md addendum for the
correction. This version fixes small k and sweeps n instead.

No paid calls. Pure local computation. Read-only import of center_column.
"""
from __future__ import annotations

import argparse
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 2)[0] + "/rule30")
from center_column import center_column as center_column_slow  # noqa: E402

A3 = __file__.rsplit("/", 3)[0] + "/experiments/overnight-arms/frontier_attack/a3_p2_orbit_closure"
sys.path.insert(0, A3)
from band_census import _band_series  # noqa: E402  (read-only import, bit-packed O(n^2/64) kernel)


def center_column(steps: int) -> bytes:
    """Fast center column via a3's bit-packed uint64 kernel (same Theta(n^2)
    shape as the pinned ground truth -- no known sub-quadratic algorithm
    exists, that is literally Prize Problem 3 -- but ~64x better constant
    from word-parallel shifts instead of a single growing Python bignum).
    Cross-checked against the pinned `center_column_slow` in `validate()`
    before ever being trusted for a large run.
    """
    band = _band_series("30", steps, wmax=1)
    return bytes(int(code >> 1) & 1 for code in band)


def thue_morse(length: int) -> bytes:
    return bytes(bin(i).count("1") & 1 for i in range(length))


def brute_force_complexity(seq: bytes, k: int) -> int:
    seen = set()
    for i in range(len(seq) - k + 1):
        seen.add(bytes(seq[i:i + k]))
    return len(seen)


def rolling_pk_curve(seq: bytes, ks: list[int], checkpoints: list[int]) -> dict[int, list[int]]:
    """p(k, n) for each k in ks, evaluated at each n in checkpoints.

    One pass over seq per k (simple, obviously-correct sliding integer
    window + set), not a suffix automaton -- avoids the correctness risk of
    a from-scratch SAM for what is, at these small fixed k, a cheap query.
    """
    checkpoints = sorted(checkpoints)
    result: dict[int, list[int]] = {}
    for k in ks:
        mask = (1 << k) - 1
        seen: set[int] = set()
        window = 0
        curve = []
        cp_iter = iter(checkpoints)
        next_cp = next(cp_iter, None)
        for i, bit in enumerate(seq):
            window = ((window << 1) | bit) & mask
            if i >= k - 1:
                seen.add(window)
            n = i + 1
            while next_cp is not None and n == next_cp:
                curve.append(len(seen))
                next_cp = next(cp_iter, None)
        while next_cp is not None:
            curve.append(len(seen))
            next_cp = next(cp_iter, None)
        result[k] = curve
    return result


def validate(max_check: int = 5000) -> bool:
    ok = True
    fast = center_column(max_check)
    slow = center_column_slow(max_check)
    mism = sum(1 for a, b in zip(fast, slow) if a != b)
    print(f"validate[fast-vs-pinned-ground-truth]: n={max_check}, mismatches={mism}")
    ok = ok and mism == 0
    for name, seq in (("rule30", fast), ("thue_morse", thue_morse(max_check))):
        for k in (5, 9, 13):
            brute = brute_force_complexity(seq, k)
            curve = rolling_pk_curve(seq, [k], [max_check])[k][0]
            match = brute == curve
            print(f"validate[{name},k={k}]: brute={brute} rolling={curve} "
                  f"{'OK' if match else 'MISMATCH'}")
            ok = ok and match
    return ok


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5_000_000, help="largest prefix length to generate")
    ap.add_argument("--ks", type=int, nargs="+", default=[8, 12, 16, 20, 24])
    ap.add_argument("--checkpoints", type=int, nargs="+",
                     default=[10_000, 30_000, 100_000, 300_000, 1_000_000, 3_000_000])
    ap.add_argument("--validate-n", type=int, default=5000)
    args = ap.parse_args()

    print(f"Correctness gate (brute-force cross-check, n<={args.validate_n}):")
    if not validate(args.validate_n):
        print("VALIDATION FAILED -- refusing to trust the large run.")
        sys.exit(1)
    print("Correctness gate: PASS.\n")

    checkpoints = sorted(c for c in args.checkpoints if c <= args.n)
    if not checkpoints or checkpoints[-1] != args.n:
        checkpoints.append(args.n)

    for name, gen in (("thue_morse", thue_morse), ("rule30", center_column)):
        t0 = time.time()
        seq = gen(args.n)
        curves = rolling_pk_curve(seq, args.ks, checkpoints)
        dt = time.time() - t0
        print(f"[{name}] n_max={args.n}, generated+measured in {dt:.1f}s")
        header = "n".rjust(10) + "".join(f"p(k={k})".rjust(12) for k in args.ks)
        print(header)
        for row_idx, n in enumerate(checkpoints):
            vals = "".join(str(curves[k][row_idx]).rjust(12) for k in args.ks)
            print(f"{n:>10}{vals}")
        print("  saturation check (last two checkpoints equal => plateaued):")
        for k in args.ks:
            c = curves[k]
            plateaued = len(c) >= 2 and c[-1] == c[-2]
            ceiling = 1 << k
            print(f"    k={k:>3}: p={c[-1]:>10} / ceiling 2^k={ceiling:>10} "
                  f"({'PLATEAUED at last two checkpoints' if plateaued else 'still growing'})")
        print()


if __name__ == "__main__":
    main()
