#!/usr/bin/env python3
"""Prerequisite check for BACKLOG.md section 18 (pushdown-language route).

fib_transfer_screen_20260902.log found RW forced-symbol blocks missing at
m=8 (18/55 hard-core blocks), pooled over n=10..17.  The m=7 analogue
(1221222) was later shown to be a sampling artifact of that same n range
(fib_absent_check.py: present at n=18,19).  Before building any CFL/PDA
machinery for section 18, check whether the m=8,9,10 absences are the same
kind of artifact: recompute the exact absent-block sets at n=10..17, then
search for each at n=18..20.

If every "absent" block reappears, section 18's motivating premise (a
missing-block signal beyond finite-state structure) has no evidence and the
pushdown route is moot without ever writing a pumping-lemma checker.  If any
block stays absent at n=18..20 despite many deep RW runs, that is the first
real candidate for the CFL pumping-lemma test.
"""
from itertools import product

from fib_transfer_screen import forced_words, blocks


def absent_blocks(mmax, n_lo, n_hi):
    agg = {m: {} for m in range(2, mmax + 1)}
    for n in range(n_lo, n_hi):
        for c in (2, 3):
            for m, d in blocks(forced_words(n, c, True, True, n + 2), mmax).items():
                for k, v in d.items():
                    agg[m][k] = agg[m].get(k, 0) + v
    out = {}
    for m in range(8, mmax + 1):
        hc = ["".join(map(str, w)) for w in product((1, 2), repeat=m) if "11" not in "".join(map(str, w))]
        out[m] = [w for w in hc if w not in agg[m]]
    return out


def main():
    print("recomputing exact absent-block sets for m=8,9,10, RW language, n=10..17", flush=True)
    absent = absent_blocks(10, 10, 18)
    for m, blks in absent.items():
        print(f"m={m}: {len(blks)} absent: {blks}", flush=True)

    print(flush=True)
    print("searching n=18,19,20 (both c) for each absent block", flush=True)
    for m, blks in absent.items():
        if not blks:
            continue
        blks_set = set(blks)
        found_total = set()
        for n in (18, 19, 20):
            for c in (2, 3):
                runs = list(forced_words(n, c, True, True, n + 2))
                deep = [w for w in runs if len(w) >= m]
                found = set()
                for w in deep:
                    s = "".join(map(str, w))
                    for i in range(len(s) - m + 1):
                        blk = s[i : i + m]
                        if blk in blks_set:
                            found.add(blk)
                found_total |= found
                print(
                    f"  m={m} n={n} c={c}: runs>=m: {len(deep)}; "
                    f"found {len(found)}/{len(blks)} of the absent blocks",
                    flush=True,
                )
        still_absent = blks_set - found_total
        print(
            f"  m={m} UNION over n=18,19,20, both c: found {len(found_total)}/{len(blks)}; "
            f"still absent everywhere ({len(still_absent)}): {sorted(still_absent)}",
            flush=True,
        )
    print("done", flush=True)


if __name__ == "__main__":
    main()
