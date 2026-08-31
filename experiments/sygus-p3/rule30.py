"""Ground-truth reference simulators for elementary CA centre columns.

Two independent implementations of the same object, kept deliberately
unlike each other so that agreement is evidence:

  * ``centre_column_naive``  -- explicit python list of cells, one triple
    lookup per cell, rule given as an 8-entry table indexed by (l,c,r).
  * ``centre_column_bitwise`` -- whole rows held as python bignums, one
    shift/mask expression per step.

INDEX CONVENTION.  ``c[0]`` is the seed row itself (the row consisting of a
single 1).  So ``c[0] = 1`` for every rule.  The alternative convention that
starts one row later is available as ``offset=1``; both are measured in the
experiment because the choice changes the truth table.
"""

RULE30 = 30
RULE90 = 90


def _table(rule: int) -> list[int]:
    """rule number -> table[(l<<2)|(c<<1)|r]."""
    return [(rule >> i) & 1 for i in range(8)]


def centre_column_naive(rule: int, steps: int) -> list[int]:
    """List-of-cells simulator.  Returns c[0..steps-1], c[0] = seed row."""
    tab = _table(rule)
    # width big enough that the light cone never reaches the boundary
    w = 2 * steps + 5
    mid = w // 2
    cells = [0] * w
    cells[mid] = 1
    out = []
    for _ in range(steps):
        out.append(cells[mid])
        nxt = [0] * w
        for i in range(1, w - 1):
            nxt[i] = tab[(cells[i - 1] << 2) | (cells[i] << 1) | cells[i + 1]]
        cells = nxt
    return out


def centre_column_bitwise(rule: int, steps: int) -> list[int]:
    """Bignum-row simulator.  Independent of the naive one in representation.

    A row is an integer whose bit ``k`` is the cell at lattice position
    ``k - mid``.  The next row is computed by combining the three shifted
    copies with the rule expressed as a sum over the 8 neighbourhoods.
    """
    tab = _table(rule)
    w = 2 * steps + 5
    mid = w // 2
    mask = (1 << w) - 1
    row = 1 << mid
    out = []
    for _ in range(steps):
        out.append((row >> mid) & 1)
        left = (row << 1) & mask
        right = row >> 1
        nxt = 0
        for n in range(8):
            bl, bc, br = (n >> 2) & 1, (n >> 1) & 1, n & 1
            if not tab[n]:
                continue
            sel = (left if bl else ~left) & (row if bc else ~row) & (right if br else ~right)
            nxt |= sel & mask
        row = nxt & mask
    return out


def truth_table(rule: int, m: int, offset: int = 0) -> list[int]:
    """Truth table of n -> c(n + offset) for n in [0, 2^m), n given in binary."""
    n = 1 << m
    col = centre_column_naive(rule, n + offset)
    return col[offset : offset + n]


if __name__ == "__main__":
    for rule in (30, 90, 110, 150):
        a = centre_column_naive(rule, 200)
        b = centre_column_bitwise(rule, 200)
        assert a == b, f"simulators disagree for rule {rule}"
        print(f"rule {rule:3d}: two simulators agree to t=200")
    print("rule30 c[0..63] =", "".join(map(str, centre_column_naive(30, 64))))
    print("rule90 c[0..63] =", "".join(map(str, centre_column_naive(90, 64))))
