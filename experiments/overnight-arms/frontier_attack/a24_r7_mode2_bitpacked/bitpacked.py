"""a24_r7_mode2_bitpacked: bit-packed / word-vectorized rewrite of a22's
build()/diag_step_series() to remove the O(T^2) bottleneck that stalled
a22_r7_mode2/mode2_probe.py at T=400,000 (see FINDINGS.md line ~458).

This file contains THREE things:

1. `diag_step_series_old` / `build_old` -- the ORIGINAL uint8, per-cell
   `np.bitwise_xor.accumulate` implementation, copied verbatim from
   a22_r7_mode2/mode2_probe.py (which itself copied it verbatim from
   a7_ladder_realizability/realize.py). Not imported, not mutated --
   repo convention is each arm writes only inside its own directory, so
   the reference implementation is duplicated here byte-for-byte for the
   correctness check to compare against.

2. `build_words` -- the NEW bit-packed implementation. Cells are packed
   into `numpy.uint64` words (bit i of word w = cell 64*w+i). Each outer
   step computes the exclusive-prefix-XOR of the "g" array via:
     (a) intra-word inclusive prefix-XOR by Kogge-Stone doubling
         (shifts 1,2,4,8,16,32), vectorized over the WHOLE word array,
     (b) intra-word exclusive prefix = inclusive ^ own-bit,
     (c) inter-word carry = exclusive prefix-XOR, over WORDS (not bits),
         of each word's total parity (bit 63 of the inclusive prefix),
     (d) broadcast each word's carry bit to all 64 positions and XOR in,
     (e) XOR in d0, broadcast the same way.
   This turns the O(n) `np.bitwise_xor.accumulate` call into one over
   n/64 words (step c) plus O(n/64) vectorized word ops (steps a,b,d,e),
   i.e. O(n/64) per step instead of O(n) per step.

3. A correctness-check `main()` that runs both implementations on
   identical inputs (rule in {30,90}, several k / word / phase
   combinations, T in the low thousands) and asserts every cell of
   `cols` and `target` matches exactly. Nothing downstream is trusted
   until this passes with zero mismatches.
"""

from __future__ import annotations

import time

import numpy as np

MASK64 = np.uint64(0xFFFFFFFFFFFFFFFF)


# ---------------------------------------------------------------------------
# 1. OLD reference implementation (verbatim copy from a22_r7_mode2, which is
#    itself a verbatim copy from a7_ladder_realizability/realize.py). DO NOT
#    EDIT to "improve" -- this is the ground truth the new code is checked
#    against.
# ---------------------------------------------------------------------------

def diag_step_series_old(prev1: np.ndarray, prev2: np.ndarray, d0: int, rule: int) -> np.ndarray:
    if rule == 30:
        g = prev1 | prev2
    elif rule == 90:
        g = prev2
    else:
        raise ValueError(rule)
    out = np.empty_like(prev1)
    out[0] = d0
    np.bitwise_xor.accumulate(g[:-1], out=out[1:])
    out[1:] ^= d0
    return out


def build_old(rule: int, k: int, word: tuple[int, ...], T: int, xlo: int, xhi: int,
              phase0: int = 0):
    T0 = 2 * k + 1
    p = len(word)
    jmax = T + max(0, -xlo) + 2
    n = jmax + 2

    zero = np.zeros(n, dtype=np.uint8)
    prev2 = zero.copy()
    prev1 = zero.copy()

    cols = {x: np.zeros(T + 1, dtype=np.uint8) for x in range(xlo, xhi + 1)}
    target = np.zeros(T + 1, dtype=np.uint8)

    for j in range(0, jmax + 1):
        if j == 0:
            d0 = 1
        elif j <= 2 * k:
            d0 = 0
        else:
            base = diag_step_series_old(prev1, prev2, 0, rule)
            want = int(word[(j - T0 + phase0) % p])
            d0 = int(base[j]) ^ want if j < n else 0
        cur = diag_step_series_old(prev1, prev2, d0, rule)
        for x in range(xlo, xhi + 1):
            t = j + x
            if 0 <= t <= T:
                cols[x][t] = cur[t]
        prev2, prev1 = prev1, cur

    for t in range(T + 1):
        target[t] = word[(t - T0 + phase0) % p] if t >= T0 else cols[0][t]
    return {"cols": cols, "target": target, "T0": T0}


# ---------------------------------------------------------------------------
# 2. NEW bit-packed implementation.
# ---------------------------------------------------------------------------

def _excl_prefix_xor_words(g_words: np.ndarray) -> np.ndarray:
    """Exclusive prefix-XOR over the bit-stream packed into g_words
    (bit i of word w = bit 64*w+i of the stream), returned as a same-shape
    uint64 word array (bit i of result word w = XOR of all stream bits
    strictly before 64*w+i)."""
    p = g_words.copy()
    p ^= p << np.uint64(1)
    p ^= p << np.uint64(2)
    p ^= p << np.uint64(4)
    p ^= p << np.uint64(8)
    p ^= p << np.uint64(16)
    p ^= p << np.uint64(32)
    # p[w] bit i now = inclusive prefix-XOR (within word w only) of bits 0..i
    intra_excl = p ^ g_words  # exclusive prefix within word

    word_parity = (p >> np.uint64(63)) & np.uint64(1)  # full-word parity, per word
    incl_word = np.bitwise_xor.accumulate(word_parity)  # inclusive prefix over WORDS
    carry = np.zeros_like(word_parity)
    if len(carry) > 1:
        carry[1:] = incl_word[:-1]
    carry_mask = np.where(carry == np.uint64(1), MASK64, np.uint64(0))

    return intra_excl ^ carry_mask


def _get_bit(words: np.ndarray, idx: int) -> int:
    w, b = divmod(idx, 64)
    return int((int(words[w]) >> b) & 1)


def build_words(rule: int, k: int, word: tuple[int, ...], T: int, xlo: int, xhi: int,
                phase0: int = 0):
    T0 = 2 * k + 1
    p = len(word)
    jmax = T + max(0, -xlo) + 2
    n = jmax + 2
    n_words = (n + 63) // 64

    prev2_words = np.zeros(n_words, dtype=np.uint64)
    prev1_words = np.zeros(n_words, dtype=np.uint64)

    cols = {x: np.zeros(T + 1, dtype=np.uint8) for x in range(xlo, xhi + 1)}
    target = np.zeros(T + 1, dtype=np.uint8)

    for j in range(0, jmax + 1):
        if rule == 30:
            g_words = prev1_words | prev2_words
        elif rule == 90:
            g_words = prev2_words
        else:
            raise ValueError(rule)

        excl_words = _excl_prefix_xor_words(g_words)  # d0 = 0 version ("base")

        if j == 0:
            d0 = 1
        elif j <= 2 * k:
            d0 = 0
        else:
            base_bit = _get_bit(excl_words, j) if j < n else 0
            want = int(word[(j - T0 + phase0) % p])
            d0 = base_bit ^ want if j < n else 0

        if d0:
            cur_words = excl_words ^ MASK64
        else:
            cur_words = excl_words

        for x in range(xlo, xhi + 1):
            t = j + x
            if 0 <= t <= T:
                cols[x][t] = _get_bit(cur_words, t)
        prev2_words, prev1_words = prev1_words, cur_words

    for t in range(T + 1):
        target[t] = word[(t - T0 + phase0) % p] if t >= T0 else cols[0][t]
    return {"cols": cols, "target": target, "T0": T0}


def min_eventual_period(seq: np.ndarray, qmax: int, drop: int):
    tail = seq[drop:]
    for q in range(1, qmax + 1):
        if len(tail) <= q:
            break
        if np.array_equal(tail[q:], tail[:-q]):
            return q
    return None


def probe(build_fn, rule: int, k: int, word: str, T: int, qmax: int, phase: int = 0):
    w = tuple(int(c) for c in word)
    xlo, xhi = -k - 2, 1
    b = build_fn(rule, k, w, T, xlo, xhi, phase)
    m1 = b["cols"][-1]
    drop = b["T0"] + 4
    mp = min_eventual_period(m1, qmax, drop)
    return {"rule": rule, "k": k, "w": word, "T": T, "qmax": qmax, "phase": phase,
            "T0": b["T0"], "col_m1_min_eventual_period_le_qmax": mp,
            "tail_len": T - drop}


# ---------------------------------------------------------------------------
# 3. Correctness check.
# ---------------------------------------------------------------------------

def _check_one(rule, k, word, T, phase, xlo, xhi):
    old = build_old(rule, k, word, T, xlo, xhi, phase)
    new = build_words(rule, k, word, T, xlo, xhi, phase)
    mismatches = 0
    cells = 0
    for x in range(xlo, xhi + 1):
        a, b = old["cols"][x], new["cols"][x]
        cells += a.size
        mismatches += int(np.count_nonzero(a != b))
    cells += old["target"].size
    mismatches += int(np.count_nonzero(old["target"] != new["target"]))
    assert old["T0"] == new["T0"]
    return cells, mismatches


def main():
    configs = [
        # (rule, k, word, T, phase)
        (30, 1, (0, 1), 3000, 0),
        (30, 2, (0, 1), 3000, 0),
        (30, 4, (0, 1), 3000, 0),
        (30, 8, (0, 1), 3000, 1),
        (30, 16, (0, 1), 2500, 0),
        (90, 1, (0, 1), 3000, 0),
        (90, 3, (0, 1), 3000, 0),
        (90, 6, (1, 0), 2500, 1),
        (30, 2, (1, 0, 1), 3000, 0),   # p=3 word, off-label but exercises the same code paths
        (30, 5, (0, 0, 1, 1), 2500, 0),  # p=4 word
    ]
    total_cells = 0
    total_mismatches = 0
    for rule, k, word, T, phase in configs:
        xlo, xhi = -k - 2, 1
        cells, mism = _check_one(rule, k, word, T, phase, xlo, xhi)
        total_cells += cells
        total_mismatches += mism
        status = "OK" if mism == 0 else "MISMATCH"
        print(f"[{status}] rule={rule} k={k:3d} word={word} T={T} phase={phase} "
              f"cells_checked={cells} mismatches={mism}")

    print(f"\nTOTAL cells checked: {total_cells}  TOTAL mismatches: {total_mismatches}")
    if total_mismatches != 0:
        raise SystemExit("CORRECTNESS CHECK FAILED -- do not trust build_words()")
    print("Correctness check PASSED: build_words() is bit-for-bit identical to build_old().")

    # Apples-to-apples timing at a T where the old O(T^2) version is still
    # feasible (a22 found the old version stalled at T=400,000; use
    # T=200,000 here so both sides actually finish).
    print("\n-- timing comparison at T=200000, k=2, w=01, rule=30 --")
    T_time = 200_000
    k_time = 2
    word_time = (0, 1)
    xlo, xhi = -k_time - 2, 1

    t0 = time.time()
    build_old(30, k_time, word_time, T_time, xlo, xhi, 0)
    t_old = time.time() - t0
    print(f"build_old:   {t_old:8.2f} s")

    t0 = time.time()
    build_words(30, k_time, word_time, T_time, xlo, xhi, 0)
    t_new = time.time() - t0
    print(f"build_words: {t_new:8.2f} s")
    print(f"speedup: {t_old / t_new:.1f}x")


if __name__ == "__main__":
    main()
