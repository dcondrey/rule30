"""Ground truth for the rule 30 center column (OEIS A051023).

Bit-parallel: the whole row is one Python int, rule 30 is
    new = (row<<1) ^ (row | (row>>1))
with bit p holding the cell at position p and the left neighbour of p
arriving as bit p of (row<<1).
"""
import sys, json


def center_column(steps: int) -> bytes:
    off = steps + 2
    row = 1 << off
    out = bytearray(steps)
    for t in range(steps):
        out[t] = (row >> off) & 1
        row = (row << 1) ^ (row | (row >> 1))
    return bytes(out)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    col = center_column(n)
    if len(sys.argv) > 2 and sys.argv[2] == "--json":
        json.dump(list(col), sys.stdout)
    else:
        print("".join(str(b) for b in col[:64]))
        ones = sum(col)
        print(f"n={n} ones={ones} zeros={n-ones} ratio={ones/(n-ones):.12f}")
