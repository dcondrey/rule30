"""Arm 4 phase-0 probe: is there a low-degree / sparse-spectrum shortcut into
the rule 30 center column?

Three measurements, each with an obvious disconfirming form:
  boundary  -- GF(2) linear complexity of the light-cone edge diagonals, left
               and right, as a function of depth d in from the edge.
  bm        -- GF(2) linear complexity of the center column itself on prefixes.
  anf       -- algebraic degree and ANF density of the center bit at step t as a
               boolean function of its 2t+1 row-0 light-cone cells.

Usage: uv run --with numpy python spectral_probe.py [boundary|bm|anf|all]
"""
import sys


def berlekamp_massey(s):
    n = len(s)
    c = [0] * n
    b = [0] * n
    c[0] = b[0] = 1
    length, m = 0, 1
    for i in range(n):
        d = s[i]
        for j in range(1, length + 1):
            d ^= c[j] & s[i - j]
        if d == 0:
            m += 1
            continue
        t = c[:]
        for j in range(n - m):
            if b[j]:
                c[j + m] ^= 1
        if 2 * length <= i:
            length = i + 1 - length
            b = t
            m = 1
        else:
            m += 1
    return length


def rows(steps):
    off = steps + 2
    row = 1 << off
    for _ in range(steps):
        yield row, off
        row = (row << 1) ^ (row | (row >> 1))


def center_column(steps):
    return bytes((row >> off) & 1 for row, off in rows(steps))


def probe_boundary(n=4096, depth=32):
    left = [[] for _ in range(depth)]
    right = [[] for _ in range(depth)]
    for t, (row, off) in enumerate(rows(n)):
        for d in range(depth):
            left[d].append((row >> (off - t + d)) & 1)
            right[d].append((row >> (off + t - d)) & 1)
    print(f"{'depth':>5} {'left L':>8} {'left/N2':>8} {'right L':>8} {'right/N2':>9}")
    for d in range(depth):
        lb, rb = berlekamp_massey(left[d]), berlekamp_massey(right[d])
        print(f"{d:>5} {lb:>8} {lb / (n / 2):>8.4f} {rb:>8} {rb / (n / 2):>9.4f}")


def probe_bm(kmax=14):
    col = list(center_column(1 << kmax))
    print(f"{'len':>7} {'L':>7} {'L/(len/2)':>10}")
    for k in range(6, kmax + 1):
        n = 1 << k
        length = berlekamp_massey(col[:n])
        print(f"{n:>7} {length:>7} {length / (n / 2):>10.4f}")


def probe_anf(tmax=10):
    import numpy as np

    print(f"{'t':>3} {'vars':>5} {'deg':>5} {'max':>5} {'terms':>9} {'density':>8}")
    for t in range(1, tmax + 1):
        m = 2 * t + 1
        idx = np.arange(1 << m, dtype=np.uint64)
        cells = [((idx >> np.uint64(j)) & np.uint64(1)).astype(np.uint8) for j in range(m)]
        for _ in range(t):
            cells = [
                cells[j - 1] ^ (cells[j] | cells[j + 1]) for j in range(1, len(cells) - 1)
            ]
        f = cells[0]
        for j in range(m):
            step = 1 << j
            f = f.reshape(-1, 2 * step)
            f[:, step:] ^= f[:, :step]
            f = f.reshape(-1)
        nz = np.nonzero(f)[0]
        deg = max(int(i).bit_count() for i in nz)
        print(f"{t:>3} {m:>5} {deg:>5} {m:>5} {len(nz):>9} {len(nz) / (1 << m):>8.4f}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("boundary", "all"):
        probe_boundary()
    if which in ("bm", "all"):
        probe_bm()
    if which in ("anf", "all"):
        probe_anf()
