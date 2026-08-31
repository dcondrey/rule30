"""Independent verification of the C1 proof skeleton (RESULTS-anf.md).

Re-derives h_t from the wedge definition (no reuse of the prover's code or
indexing) and checks the three load-bearing steps of the submitted proof:

  S2  wedge-determined cells: y_{t-2u} = h_u(v_1..v_u), for u = 0..t-1
  S3  recursion: h_t(v) = (v_t OR h_{t-1}(v')) XOR h_{t-1}(w_1..w_{t-1}),
                 w_k = v_{k+1} XOR (h_k(v_1..v_k) OR v_k)
  S4  parity: v' -> (w_1..w_{t-2}) is exactly 2-to-1 onto {0,1}^{t-2},
              hence M(t) = M(t-1) mod 2

Convention: v_k = y_{t+1-2k}, so v_1 = y_{t-1} and v_t = y_{-t+1}.

Run: uv run python experiments/overnight-arms/anf/verify_c1_proof.py [tmax]
"""

from __future__ import annotations

import logging
import sys
from collections import Counter

log = logging.getLogger(__name__)


def step(cells: list[int]) -> list[int]:
    return [cells[j - 1] ^ (cells[j] | cells[j + 1]) for j in range(1, len(cells) - 1)]


def build_row(t: int, v: tuple[int, ...]) -> dict[int, int]:
    """Solve the wedge triangularly for the free assignment v. Returns cells -t..t."""
    y = {-t: 0}
    for k in range(1, t + 1):
        y[t + 1 - 2 * k] = v[k - 1]
    for u in range(t):  # W_u determines y_{t-2u}
        target = t - 2 * u
        y[target] = 0
        cells = [y[off] for off in range(target, t + 1)]
        for _ in range(u):
            cells = step(cells)
        assert len(cells) == 1
        y[target] = cells[0]
    return y


def h_table(t: int) -> dict[tuple[int, ...], int]:
    """h_t over all 2^t free assignments, computed from the definition."""
    out = {}
    for idx in range(1 << t):
        v = tuple((idx >> i) & 1 for i in range(t))
        y = build_row(t, v)
        cells = [y[off] for off in range(-t, t + 1)]
        for _ in range(t):
            cells = step(cells)
        assert len(cells) == 1
        out[v] = cells[0]
    return out


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    H = {t: h_table(t) for t in range(1, tmax + 1)}
    M = {t: sum(H[t].values()) for t in H}
    log.info("M(t) from independent wedge build: %s", [M[t] for t in range(2, tmax + 1)])

    for t in range(2, tmax + 1):
        # S2: determined cells equal h_u
        s2 = True
        for idx in range(1 << t):
            v = tuple((idx >> i) & 1 for i in range(t))
            y = build_row(t, v)
            for u in range(1, t):
                if y[t - 2 * u] != H[u][v[:u]]:
                    s2 = False
                    break
            if not s2:
                break
        # S3: recursion, pointwise
        s3 = True
        for idx in range(1 << t):
            v = tuple((idx >> i) & 1 for i in range(t))
            vp = v[: t - 1]
            Hp = H[t - 1][vp]
            w = tuple(
                v[k] ^ (H[k][v[:k]] | v[k - 1]) for k in range(1, t)
            )  # w_k, k=1..t-1 (0-indexed v)
            rhs = (v[t - 1] | Hp) ^ H[t - 1][w]
            if rhs != H[t][v]:
                s3 = False
                break
        # S4: w-map on v' -> (w_1..w_{t-2}) exactly 2-to-1
        fibers = Counter()
        for idx in range(1 << (t - 1)):
            vp = tuple((idx >> i) & 1 for i in range(t - 1))
            wsub = tuple(vp[k] ^ (H[k][vp[:k]] | vp[k - 1]) for k in range(1, t - 1))
            fibers[wsub] += 1
        two_to_one = t <= 2 or (
            set(fibers.values()) == {2} and len(fibers) == 1 << (t - 2)
        )
        parity_ok = M[t] % 2 == M[t - 1] % 2
        log.info(
            "t=%2d M=%-8d S2=%s S3=%s S4(2-to-1)=%s M(t)=M(t-1) mod2=%s odd=%s",
            t, M[t], s2, s3, two_to_one, parity_ok, M[t] % 2 == 1,
        )


if __name__ == "__main__":
    main()
