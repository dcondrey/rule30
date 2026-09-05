#!/usr/bin/env python3
"""Exact actual-right trace language R_m by SAT, beyond the enumerated length 13.

R_m is the set of length-m words rho_0..rho_(m-1) with rho_k = s(2k, 1), the
column-one bit at even times, realizable by some initial right half-line of
2m-1 free cells under Rule 30 with the centre column alternating 0101...
(the convention of right_trace_forbidden.numeric_rho: the left neighbour of
cell 1 at time t is t & 1).  The repository has the exact language through
length 13 by seed enumeration (2^25 seeds) and SAT-audited factors of
lengths 12 and 13.  This script extends the exact language length by length:

    R_m = { w b : w in R_(m-1), b in {0,1}, w b realizable }

with realizability decided by one CaDiCaL query per candidate on the exact
minimal light cone (2m-1 initial cells, 2m-2 time steps, Tseitin encoded),
using assumptions so that one solver per length serves every candidate.

Gate: the SAT language equals right_trace_forbidden.realized_language(m) for
every m <= --gate (seed enumeration), and reproduces the recorded counts
2,3,5,8,12,17,25,36,50,68,91,119,156 through length 13.

Output: |R_m| per length, the growth ratio, every new minimal forbidden
factor (unrealizable word whose two length-(m-1) factors are realizable),
and a JSON file with the complete forbidden-factor list and the words of the
last length, for use by hf_lang_survival.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from pysat.solvers import Solver  # noqa: E402
from right_trace_forbidden import realized_language  # noqa: E402


class Cone:
    """Tseitin encoding of the minimal right light cone for trace length L."""

    def __init__(self, length: int, solver_name: str = "cadical153") -> None:
        self.length = length
        self.nvars = 0
        self.clauses: list[list[int]] = []
        width = 2 * length - 1
        row = [self.new_var() for _ in range(width)]
        self.samples: list[int] = [row[0]]
        for t in range(2 * length - 2):
            boundary = t & 1
            new_width = len(row) - 1
            new = []
            for i in range(new_width):
                o = self.or_gate(row[i], row[i + 1])
                if i == 0:
                    x = self.new_var()
                    if boundary == 0:
                        self.clauses.append([-x, o])
                        self.clauses.append([x, -o])
                    else:
                        self.clauses.append([x, o])
                        self.clauses.append([-x, -o])
                else:
                    x = self.xor_gate(row[i - 1], o)
                new.append(x)
            row = new
            if (t + 1) % 2 == 0:
                self.samples.append(row[0])
        assert len(self.samples) == length
        self.solver = Solver(name=solver_name, bootstrap_with=self.clauses)

    def new_var(self) -> int:
        self.nvars += 1
        return self.nvars

    def or_gate(self, a: int, b: int) -> int:
        o = self.new_var()
        self.clauses.append([-a, o])
        self.clauses.append([-b, o])
        self.clauses.append([a, b, -o])
        return o

    def xor_gate(self, l: int, o: int) -> int:
        x = self.new_var()
        self.clauses.append([-l, -o, -x])
        self.clauses.append([l, o, -x])
        self.clauses.append([l, -o, x])
        self.clauses.append([-l, o, x])
        return x

    def realizable(self, word: str) -> bool:
        assert len(word) == self.length
        assumptions = [v if ch == "1" else -v for v, ch in zip(self.samples, word)]
        return bool(self.solver.solve(assumptions=assumptions))

    def close(self) -> None:
        self.solver.delete()


def has_forbidden_suffix(word: str, forbidden: list[str]) -> bool:
    return any(word.endswith(f) for f in forbidden)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-length", type=int, default=30)
    ap.add_argument("--gate", type=int, default=10)
    ap.add_argument("--out", default="/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-hardcore/r_exact_language.json")
    args = ap.parse_args()

    recorded = [2, 3, 5, 8, 12, 17, 25, 36, 50, 68, 91, 119, 156]
    forbidden: list[str] = []
    language = {""}
    counts = []
    print(" m   |R_m|   ratio   sat-calls  new minimal forbidden factors   (time)")
    for m in range(1, args.max_length + 1):
        t0 = time.time()
        cone = Cone(m)
        new_language = set()
        new_forbidden = []
        calls = 0
        for w in language:
            for b in "01":
                cand = w + b
                if has_forbidden_suffix(cand, forbidden):
                    continue
                calls += 1
                if cone.realizable(cand):
                    new_language.add(cand)
                else:
                    # w = cand[:-1] is realizable by construction; cand[1:] is
                    # a minimal forbidden factor test: minimal iff cand[1:]
                    # realizable (it is a word of length m-1).
                    if cand[1:] in language:
                        new_forbidden.append(cand)
        cone.close()
        if m <= args.gate:
            exact = realized_language(m)
            assert exact == new_language, (m, len(exact), len(new_language))
            gate_note = " gate=PASS"
        else:
            gate_note = ""
        if m <= len(recorded):
            assert len(new_language) == recorded[m - 1], (m, len(new_language), recorded[m - 1])
            gate_note += " recorded=PASS"
        ratio = len(new_language) / len(language) if language and m > 1 else float("nan")
        counts.append(len(new_language))
        forbidden.extend(sorted(new_forbidden))
        language = new_language
        print(
            f"{m:2d} {len(language):7d}  {ratio:6.3f}  {calls:9d}  "
            f"{','.join(sorted(new_forbidden)) or '-'}   ({time.time() - t0:.1f}s){gate_note}"
        )
        sys.stdout.flush()
    with open(args.out, "w") as fh:
        json.dump(
            {
                "max_length": args.max_length,
                "counts": counts,
                "forbidden": forbidden,
                "words_last_length": sorted(language),
            },
            fh,
        )
    print(f"wrote {args.out}: {len(forbidden)} minimal forbidden factors through length {args.max_length}")
    print("counts:", counts)


if __name__ == "__main__":
    main()
