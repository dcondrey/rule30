"""The Rule 90 ensemble filter: why ensemble-level arguments cannot reach P1 or P2.

Rule 90 is additive, surjective, positively expansive, has positive entropy, and is
strongly mixing with respect to uniform Bernoulli — i.e. it is maximally "chaotic"
and "thermalizing" by every ensemble-level measure. Yet its single-seed center
column is eventually constant.

Any argument for P1 or P2 whose hypotheses are ensemble-level (ergodicity, mixing,
ETH, operator scrambling, holographic entropy bounds, spectral dimension of the
shift algebra, attractor dimension) therefore proves too much: it applies verbatim
to Rule 90, where the conclusion is false.

Run: uv run python experiments/overnight-arms/common/ensemble_filter.py
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def center_column(rule: str, n: int) -> list[int]:
    row = 1  # shifted frame b_t(i) = s(t, i-t); single seed
    out = []
    for t in range(n):
        out.append((row >> t) & 1)
        if rule == "30":
            row = (row << 2) ^ ((row << 1) | row)
        elif rule == "90":
            row = (row << 2) ^ row
        else:
            raise ValueError(rule)
    return out


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    n = 20000
    for rule in ("90", "30"):
        c = center_column(rule, n)
        ones = sum(c)
        first_nonzero_after = [t for t in range(1, n) if c[t]]
        log.info(
            "rule %s: ones in first %d = %d (density %.4f); nonzero t>0: %s",
            rule, n, ones, ones / n,
            "none" if not first_nonzero_after else f"{len(first_nonzero_after)} of them",
        )
        log.info("   prefix: %s", "".join(map(str, c[:40])))
    log.info(
        "Conclusion: rule 90's single-seed center column is 1 then 0 forever "
        "(eventually periodic, period 1, density 0), despite rule 90 being ergodic "
        "and strongly mixing w.r.t. uniform Bernoulli. Ensemble chaos does not "
        "constrain the single-seed column."
    )


if __name__ == "__main__":
    main()
