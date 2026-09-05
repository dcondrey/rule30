#!/usr/bin/env python3
"""Class-null expectations from the exact class counts in quotient_bfs_u27.log.

Under the null 'each class (distinct column-(n-1) quotient) has an independent
fair-coin Psi word', the expected number of classes with constant Psi at
length n, pooled over c in {2,3}, is  N_q(n-1) * 2 * 2^-(n+2) = N_q(n-1) / 2^(n+1).
The source-level null of PREREG-psi-constraint-counting.md is 2^n / 2^(n+1) = 1/2.
Prints both, the cumulative sums, and a least-squares fit of log2 N_q(u) = alpha*u + beta
on u = 13..27 plus the local increments.
"""
import re
from math import log2

rows = []
for line in open("/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-survivors/quotient_bfs_u27.log"):
    m = re.match(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)", line)
    if m:
        u, n, N = int(m[1]), int(m[2]), int(m[3])
        rows.append((u, n, N))
print("n   N_q(n-1)   E[const classes] class-null   source-null   cum(class, n>=7)   cum(source, n>=7)")
cc = cs = 0.0
for u, n, N in rows:
    ec = N / 2 ** (n + 1)
    if n >= 7:
        cc += ec
        cs += 0.5
    print(f"{n:2d} {N:10d}   {ec:10.4f}   {0.5:6.2f}   {cc:8.3f}   {cs:8.2f}")
# geometric tail beyond the last n with the last increment
u, n, N = rows[-1]
inc = log2(rows[-1][2]) - log2(rows[-2][2])
r = 2 ** (inc - 1)
tail = (N / 2 ** (n + 1)) * r / (1 - r)
print(f"\nlast increment {inc:.4f}; geometric tail of the class-null sum beyond n={n}: {tail:.4f}; total class-null expectation over n>=7: {cc + tail:.3f}")
# fit
xs = [(u, log2(N)) for u, n, N in rows if u >= 13]
mx = sum(x for x, _ in xs) / len(xs)
my = sum(y for _, y in xs) / len(xs)
a = sum((x - mx) * (y - my) for x, y in xs) / sum((x - mx) ** 2 for x, _ in xs)
b = my - a * mx
print(f"least-squares log2 N_q(u) = {a:.4f} u + {b:.3f} on u=13..27; residual max {max(abs(y - a*x - b) for x, y in xs):.3f}")
print("increments u=13..27: " + " ".join(f"{log2(rows[i][2]) - log2(rows[i-1][2]):.4f}" for i in range(13, len(rows))))
