#!/usr/bin/env python3
"""Check the two proposed bounds against every class_tree log:
   RW : S_k <= 8  * S_0 * 2^-k
   BWH: S_k <= 16 * S_0 * 2^-k
Prints the tightest ratio S_k / (S_0 2^-k) per (n, c, regime) and any violation."""
import re, glob
logs = sorted(glob.glob("/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-survivors/class_tree*.log"))
worst = {"rw": (0, None), "bwh": (0, None)}
for path in logs:
    n = None
    S0 = None
    for line in open(path):
        m = re.match(r"===== n=(\d+): sources \d+, initial classes (\d+)", line)
        if m:
            n, S0 = int(m[1]), int(m[2])
            continue
        m = re.match(r"\s+c=(\d) (rw|bwh)\s*: (.*)", line)
        if m:
            c, reg, rest = int(m[1]), m[2], m[3]
            for kk, N, S in re.findall(r"k(\d+):(\d+)/(\d+)", rest):
                k, S = int(kk), int(S)
                if S == 0:
                    continue
                ratio = S / (S0 * 2.0 ** -k)
                if ratio > worst[reg][0]:
                    worst[reg] = (ratio, (n, c, k, S, S0))
for reg, C in (("rw", 8), ("bwh", 16)):
    r, where = worst[reg]
    print(f"{reg}: max S_k/(S_0 2^-k) = {r:.3f} at (n,c,k,S_k,S_0)={where}; bound constant {C}: {'OK' if r <= C else 'VIOLATED'}")
