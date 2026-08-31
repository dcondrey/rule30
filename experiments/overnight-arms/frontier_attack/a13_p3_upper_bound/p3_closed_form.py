"""Closed forms for the backward-elimination family, checked mechanically.

This is the guard against reading the finite-size log-log fit as sub-quadratic:
the two lengths below have exact quadratic closed forms, yet a least-squares
fit over n = 4..128 reads 1.8935 and 1.8165 for them.

Run:
    /Volumes/A/researchpapers/.venv/bin/python p3_closed_form.py
"""

from __future__ import annotations

import logging

import p3_core as P


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ok = True
    logging.info("n      cells   |D_n| formula  bwd30  n^2/2+n   bwd90  n^2/4+n")
    for n in range(2, 201, 2):
        inst30 = P.Instance(30, n)
        c = len(inst30.cone)
        f = n * n // 2 + n + 1
        w30, _ = P.derive_backward(30, n)
        w90, _ = P.derive_backward(90, n)
        p30, p90 = n * n // 2 + n, n * n // 4 + n
        good = c == f and w30.length == p30 and w90.length == p90
        ok &= good
        if n <= 16 or n % 50 == 0:
            logging.info(
                "%-6d %-7d %-13d %-6d %-9d %-6d %-7d %s",
                n, c, f, w30.length, p30, w90.length, p90,
                "ok" if good else "MISMATCH",
            )
    logging.info("")
    logging.info(
        "CLOSED FORM VERIFIED for every even n in 2..200" if ok else "MISMATCH"
    )
    logging.info("  |D_n|            = n^2/2 + n + 1")
    logging.info("  rule 30 backward = n^2/2 + n = |D_n| - 1   (exponent exactly 2)")
    logging.info("  rule 90 backward = n^2/4 + n               (exponent exactly 2)")
    logging.info(
        "A least-squares fit over n=4..128 reads 1.8935 and 1.8165 for these two "
        "exact quadratics.  Short ladders manufacture sub-quadratic exponents."
    )


if __name__ == "__main__":
    main()
