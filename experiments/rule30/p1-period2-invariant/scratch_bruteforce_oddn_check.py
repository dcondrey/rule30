"""Independent brute-force check (crude literal_extension loop, same as
RESULTS-EXTINCTION-MARGIN.md's reproduction block) of max_survival at
n=13,15, c=2, r=0 -- to verify the fast dedup method (scratch_finalist_via_dedup.py)
agrees at ODD n, not just the even n the project's existing crosschecks cover.
"""
from itertools import product
from late_pull_diagonal_sat import literal_extension

def max_survival(n, tail, residue):
    target = n + residue
    rows = target + 2
    best = -1
    for w in product((1, 2), repeat=n):
        cont = literal_extension(w, tail, rows)
        prev = w[-1]
        fail_at = None
        for i, v in enumerate(cont):
            if v not in (1, 2) or (prev == 1 and v == 1):
                fail_at = i
                break
            prev = v
        survived = rows if fail_at is None else fail_at
        best = max(best, survived)
    return best, rows

for n in (13, 15):
    best, rows = max_survival(n, 2, 0)
    print(f"n={n} c=2 r=0 (brute force) max_survival={best} rows={rows} gamma={rows-best}", flush=True)
