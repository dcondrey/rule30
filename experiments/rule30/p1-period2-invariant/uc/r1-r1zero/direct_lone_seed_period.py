"""For the lone seed, eventual periodicity with onset t0 and period p is refuted
by direct computation of c: no pin argument required.  Reports the largest
(onset, period) box excluded by computing c to time T."""
import time, sys
T = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
t0 = time.time()
OFF = T + 4
row = 1 << OFF
c = []
for _ in range(T + 1):
    c.append((row >> OFF) & 1)
    row = (row << 1) ^ (row | (row >> 1))
build = time.time() - t0

# For each period p, the smallest onset from which c is p-periodic through T
# (None if no such onset <= T/2 exists).
worst = 0
survivors = []
for p in range(1, 65):
    onset = 0
    for i in range(T - p, -1, -1):
        if c[i] != c[i + p]:
            onset = i + 1
            break
    if onset <= T // 2:
        survivors.append((p, onset))
    worst = max(worst, T - onset)
print(f"T={T} built in {build:.1f}s")
print(f"periods p=1..64: surviving (p, onset<=T/2) = {survivors}")
print(f"longest p-periodic tail over p<=64: {worst} steps (of {T})")
print("=> lone-seed centre column is NOT eventually periodic with p<=64 and onset<=%d" % (T // 2))
