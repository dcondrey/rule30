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

best, rows = max_survival(9, 3, 0)
print(f"n=9 c=3 r=0 (brute force) max_survival={best} rows={rows} gamma={rows-best}")
