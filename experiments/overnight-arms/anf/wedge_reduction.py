"""anf arm: triangular wedge reduction of C1 (RESULTS-anf.md, reduction chain R2'/R3/R4).

C1(t)  <=>  M(t) = #{ w on cells -t+1..t : s(t,0)=1 and s(u,t-u)=0 for u=0..t-1 } is odd.
The t wedge conditions are left-permutive in y_{t-2u}, so they determine the t cells
y_t, y_{t-2}, ..., y_{-t+2} from the t free cells y_{t-1}, y_{t-3}, ..., y_{-t+1}.
M(t) is therefore a weight over a 2^t cube, not 2^(2t+1): C1 becomes "the restricted
function h_t on t variables has odd weight", i.e. its full degree-t monomial survives.

Bit-parallel over all 2^t free assignments using Python big-int masks.
Validated against the brute-force M(t) for t = 2..9 (values 1,5,5,15,33,65,117,253).
Writes runs/overnight/anf/wedge.json.

Run: uv run python experiments/overnight-arms/anf/wedge_reduction.py [tmax]
"""

from __future__ import annotations

import json
import logging
import pathlib
import sys
import time

log = logging.getLogger(__name__)
OUT = pathlib.Path("/Volumes/A/researchpapers/13-rule30/runs/overnight/anf/wedge.json")
BRUTE = {2: 1, 3: 5, 4: 5, 5: 15, 6: 33, 7: 65, 8: 117, 9: 253}


def free_masks(t: int) -> list[int]:
    """mask[k] has bit j set iff bit k of j is 1, over j < 2^t."""
    total = 1 << t
    out = []
    for k in range(t):
        block = 1 << k
        unit = ((1 << block) - 1) << block  # zeros then ones, width 2*block
        rep = 0
        width = block << 1
        for i in range(total // width):
            rep |= unit << (i * width)
        out.append(rep)
    return out


def evolve(cells: list[int], steps: int, full: int) -> list[int]:
    """Rule 30 on packed masks; `full` is the all-ones mask of width 2^t."""
    for _ in range(steps):
        cells = [
            cells[j - 1] ^ (cells[j] | cells[j + 1]) for j in range(1, len(cells) - 1)
        ]
    return cells


def wedge_count(t: int) -> int:
    full = (1 << (1 << t)) - 1
    fm = free_masks(t)
    # cell offsets -t+1..t ; odd-parity offsets (t-1, t-3, ...) are free
    y: dict[int, int] = {}
    for k, off in enumerate(range(t - 1, -t, -2)):
        y[off] = fm[k]
    # wedge condition u determines y[t-2u]; process u = 0..t-1 (rightmost first)
    for u in range(t):
        target = t - 2 * u
        y[target] = 0
        cells = [y[off] for off in range(target, t + 1)]
        e = evolve(cells, u, full)
        assert len(e) == 1, (u, len(e))
        y[target] = e[0]
    row = [0] + [y[off] for off in range(-t + 1, t + 1)]  # cell -t is fixed to 0
    res = evolve(row, t, full)
    assert len(res) == 1
    return int(res[0]).bit_count()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    results = json.loads(OUT.read_text()) if OUT.exists() else []
    done = {r["t"] for r in results}
    for t in range(2, tmax + 1):
        if t in done:
            continue
        t0 = time.monotonic()
        m = wedge_count(t)
        dt = time.monotonic() - t0
        gate = ""
        if t in BRUTE:
            gate = "  brute-match" if m == BRUTE[t] else f"  BRUTE-MISMATCH({BRUTE[t]})"
        results.append({"t": t, "M": m, "odd": m % 2 == 1, "seconds": round(dt, 2)})
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(results, indent=1))
        log.info("t=%2d M(t)=%d odd=%s (%.1fs)%s", t, m, m % 2 == 1, dt, gate)


if __name__ == "__main__":
    main()
