"""Exact right-cone (causal-pyramid) reconstruction for Rule 30 center traces.

Boundary-anchored representation: for a configuration with all cells zero at
positions above the right boundary, index space-time by the right-cone diagonal
``k`` with ``D_k[t] = s(t, t-k)``.  Rule 30 becomes the branch-free recursion

    D_k[t] = D_k[t-1] XOR (D_{k-1}[t-1] OR D_{k-2}[t-1]),

with ``D_k[0] = a(-k)`` and ``D_k[k] = c_k``.  Because ``D_k[t]`` depends on
``D_k[0]`` only through an XOR chain, the forced value of ``a(-k)`` is a single
XOR of the target center bit with the ``a(-k)=0`` evaluation.  That makes the
whole inverse-trace reconstruction data-independent and bit-parallel over an
exponential family of right parts.

The reconstruction itself is left permutivity and is not new; see
``docs/rule30/RESULTS-inverse-trace.md``.  New here is the branch-free
bit-parallel form and the pinned right-cone diagonals it exposes.
"""

from __future__ import annotations

import argparse
import json

RULE30 = 30
RULE90 = 90
RULES = {RULE30: "or", RULE90: "xor"}


def step(cells: frozenset[int], rule: int) -> frozenset[int]:
    if not cells:
        return frozenset()
    lo, hi = min(cells) - 1, max(cells) + 1
    out = set()
    for x in range(lo, hi + 1):
        l = (x - 1) in cells
        c = x in cells
        r = (x + 1) in cells
        v = (l ^ (c or r)) if rule == 30 else (l ^ r)
        if v:
            out.add(x)
    return frozenset(out)


def center_trace(cells: frozenset[int], horizon: int, rule: int) -> list[int]:
    out = []
    cur = cells
    for _ in range(horizon + 1):
        out.append(1 if 0 in cur else 0)
        cur = step(cur, rule)
    return out


def reconstruct(right: list[int], target: list[int], depth: int, rule: int) -> list[int]:
    """Forced ``a(-1..-depth)`` from ``right = a(0..W)`` and the target trace.

    ``target`` must have length at least ``depth+1``.  Positions above ``W`` are
    zero.  Returns the unique left half compatible with the target trace.
    """
    width = len(right) - 1
    horizon = depth
    prev2 = [0] * (horizon + 1)
    prev1 = [0] * (horizon + 1)
    left: list[int] = []
    for k in range(-width, depth + 1):
        cur = [0] * (horizon + 1)
        cur[0] = right[-k] if k <= 0 else 0
        for t in range(1, horizon + 1):
            gate = (prev1[t - 1] | prev2[t - 1]) if rule == 30 else prev2[t - 1]
            cur[t] = cur[t - 1] ^ gate
        if k >= 1:
            delta = cur[k] ^ target[k]
            if delta:
                for t in range(horizon + 1):
                    cur[t] ^= 1
            left.append(cur[0])
        elif k == 0 and cur[0] != target[0]:
            raise ValueError("a(0) disagrees with c_0")
        prev2, prev1 = prev1, cur
    return left


def _case_mask(count: int, bit: int) -> int:
    """Bit ``i`` of the result is bit ``bit`` of ``i``, for ``i < count``."""
    half = 1 << bit
    block = ((1 << half) - 1) << half
    period = 2 * half
    reps = (count + period - 1) // period
    m = 0
    for r in range(reps):
        m |= block << (r * period)
    return m & ((1 << count) - 1)


def case_right_part(case: int, width: int, c0: int) -> list[int]:
    """The right part ``a(0..width)`` that ``sweep_bits`` assigns to ``case``."""
    return [c0] + [(case >> (j - 1)) & 1 for j in range(1, width + 1)]


def sweep_bits(width: int, target: list[int], depth: int, rule: int) -> tuple[int, list[int]]:
    """Reconstruct every right part ``a(0..width)`` at once, bit-parallel.

    ``a(0)`` is pinned to ``c_0``; ``a(1..width)`` are free, so the family has
    ``2^width`` members and covers every row with right endpoint at most
    ``width``.  Returns ``(count, left_bits)`` where bit ``i`` of
    ``left_bits[k]`` is the forced ``a(-k)`` for case ``i``.
    """
    if width < 0:
        raise ValueError("width must be non-negative")
    if len(target) <= depth:
        raise ValueError("target shorter than depth+1")
    count = 1 << width
    full = (1 << count) - 1
    masks = [0] * (width + 1)
    masks[0] = full if target[0] else 0
    for j in range(1, width + 1):
        masks[j] = _case_mask(count, j - 1)

    prev2 = [0] * (depth + 1)
    prev1 = [0] * (depth + 1)
    left_bits = [0] * (depth + 1)
    for k in range(-width, depth + 1):
        cur = [0] * (depth + 1)
        cur[0] = masks[-k] if k <= 0 else 0
        for t in range(1, depth + 1):
            gate = (prev1[t - 1] | prev2[t - 1]) if rule == 30 else prev2[t - 1]
            cur[t] = cur[t - 1] ^ gate
        if k >= 1:
            delta = cur[k] ^ (full if target[k] else 0)
            if delta:
                for t in range(depth + 1):
                    cur[t] ^= delta
            left_bits[k] = cur[0]
        prev2, prev1 = prev1, cur
    return count, left_bits


def first_forced_one(left_bits: list[int], count: int, after: int) -> list[int]:
    """Per-case least ``k > after`` with a forced one, or 0 when there is none."""
    res = [0] * count
    remaining = (1 << count) - 1
    for k in range(after + 1, len(left_bits)):
        new = left_bits[k] & remaining
        if not new:
            continue
        remaining &= ~new
        while new:
            low = new & -new
            res[low.bit_length() - 1] = k
            new ^= low
        if not remaining:
            break
    return res


def deepest_forced_one(left_bits: list[int], count: int) -> list[int]:
    """Per-case greatest ``k >= 1`` with a forced one, or 0 when there is none."""
    res = [0] * count
    remaining = (1 << count) - 1
    for k in range(len(left_bits) - 1, 0, -1):
        new = left_bits[k] & remaining
        if not new:
            continue
        remaining &= ~new
        while new:
            low = new & -new
            res[low.bit_length() - 1] = k
            new ^= low
        if not remaining:
            break
    return res


def sweep(width: int, target: list[int], depth: int, rule: int, slack: int = 16) -> dict:
    """Summarise the forced left halves over all ``2^width`` right parts.

    ``min_deepest_one`` is the certificate: no row with right endpoint at most
    ``width`` whose trace matches ``target`` through time ``depth`` has left
    endpoint above ``-min_deepest_one``.  ``shallow_cases`` are the right parts
    whose forced tail goes silent at least ``slack`` before ``depth``; those are
    falsification candidates and must be re-simulated before use.
    """
    count, left_bits = sweep_bits(width, target, depth, rule)
    full = (1 << count) - 1
    found = 0
    hist: dict[int, int] = {}
    shallow_masks: dict[int, int] = {}
    for k in range(depth, 0, -1):
        new = left_bits[k] & ~found
        if not new:
            continue
        found |= new
        hist[k] = new.bit_count()
        if k <= depth - slack:
            shallow_masks[k] = new
    missing = full & ~found

    shallow = []
    for k in sorted(shallow_masks):
        m = shallow_masks[k]
        while m and len(shallow) < 8:
            low = m & -m
            case = low.bit_length() - 1
            shallow.append({"case": case, "deepest_one": k,
                            "right": case_right_part(case, width, target[0])})
            m ^= low
        if len(shallow) >= 8:
            break

    unresolved = []
    m = missing
    while m and len(unresolved) < 8:
        low = m & -m
        unresolved.append(low.bit_length() - 1)
        m ^= low

    return {
        "width": width,
        "cases": count,
        "depth": depth,
        "min_deepest_one": min(hist) if hist else 0,
        "max_deepest_one": max(hist) if hist else 0,
        "deepest_one_histogram": {str(k): hist[k] for k in sorted(hist)},
        "n_shallow_cases": sum(v for k, v in hist.items() if k <= depth - slack),
        "shallow_cases": shallow,
        "n_cases_with_no_forced_one": missing.bit_count(),
        "cases_with_no_forced_one": unresolved,
    }


def periodic_target(word: list[int], depth: int) -> list[int]:
    p = len(word)
    return [word[t % p] for t in range(depth + 1)]


def nonconstant_words(period: int) -> list[list[int]]:
    out = []
    for code in range(1, (1 << period) - 1):
        word = [(code >> i) & 1 for i in range(period)]
        if len(set(word)) == 1:
            continue
        out.append(word)
    return out


def survival_horizon(cells: frozenset[int], period: int, horizon: int, rule: int) -> int:
    """Largest H with the trace matching its own first ``period`` bits through H."""
    tr = center_trace(cells, horizon, rule)
    h = period - 1
    for t in range(period, horizon + 1):
        if tr[t] != tr[t % period]:
            return t - 1
        h = t
    return h


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-width", type=int, default=1)
    ap.add_argument("--max-width", type=int, default=8)
    ap.add_argument("--depth", type=int, default=32)
    ap.add_argument("--periods", type=int, nargs="*", default=[2, 3, 4, 5, 6])
    ap.add_argument("--rule", type=int, default=30)
    ap.add_argument("--zero-target", action="store_true",
                    help="sweep the all-zero target instead of periodic words")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    report = []
    if args.zero_target:
        tgt = [0] * (args.depth + 1)
        for w in range(args.min_width, args.max_width + 1):
            report.append({"period": 0, "word": [0],
                           **sweep(w, tgt, args.depth, args.rule)})
    else:
        for p in args.periods:
            for word in nonconstant_words(p):
                tgt = periodic_target(word, args.depth)
                for w in range(args.min_width, args.max_width + 1):
                    report.append({"period": p, "word": word,
                                   **sweep(w, tgt, args.depth, args.rule)})
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for row in report:
            print(row)


if __name__ == "__main__":
    main()
