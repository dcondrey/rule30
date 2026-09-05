"""Gate the int-row left-half-plane kernel against references before any kill test is trusted.

(a) int-row update versus a dict-based cell-by-cell simulation, random finite y and random drive c.
(b) the lone-seed left half-plane of the TRUE diagram equals LHP_seed(c*) with c* the true centre column,
    and the pin holds there with zero violations (implication step (1) of the lemma).
(c) planted lock: an adaptively pin-consistent drive survives to the cap, so tail_survival can detect a lock.
(d) Pi-tree leaf counts and maximal tail survivals reproduce pin_survival2_L8-32.log at L = 28.
"""
import sys, random
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-screen-pin-pi-no-periodic')
from r1zero_lib import lone_seed_rows, lone_seed_columns
from lhp_lib import lhp_step, tail_survival, naive_lhp, periodic_tail
from collections import Counter

out = []
# (a)
rng = random.Random(1)
bad = 0
cases = 0
for trial in range(300):
    T = 60
    width = T + 20
    y = [0] + [rng.getrandbits(1) for _ in range(12)]
    c = [rng.getrandbits(1) for _ in range(T + 2)]
    ref = naive_lhp(y, c, T, width)
    row = sum(b << i for i, b in enumerate(y) if i >= 1) | c[0]
    for t in range(T + 1):
        cases += 1
        if row != ref[t]:
            bad += 1
        row = lhp_step(row, c[t + 1])
out.append(f"(a) int-row versus dict reference: {cases} rows compared, mismatches={bad}")

# (b)
T = 1500
xs = list(range(-40, 1))
cols = lone_seed_columns(T + 1, xs)
cstar = cols[0]
row = 1
mism = 0
viol = 0
ones = 0
for t in range(T + 1):
    for x in xs:
        if ((row >> (-x)) & 1) != cols[x][t]:
            mism += 1
    if t < T:
        if cstar[t] == 1:
            ones += 1
            if ((row >> 1) & 1) != (1 ^ cstar[t + 1]):
                viol += 1
        row = lhp_step(row, cstar[t + 1])
out.append(f"(b) lone seed T={T}: LHP_seed(c*) versus true diagram on columns -40..0: {len(xs)*(T+1)} cells, mismatches={mism}; pin: ones={ones} violations={viol}")

# (c)
rng = random.Random(5)
cap = 400
detected = 0
for trial in range(50):
    row = rng.getrandbits(10) | 1
    tail = [row & 1]
    r = row
    for k in range(cap + 1):
        if r & 1:
            nxt = 1 ^ ((r >> 1) & 1)
        else:
            nxt = rng.getrandbits(1)
        tail.append(nxt)
        r = lhp_step(r, nxt)
    if tail_survival(row, tail, cap) == cap:
        detected += 1
    # and a corrupted copy must fail
out.append(f"(c) planted pin-consistent drives reaching cap={cap}: {detected}/50")

# (d)
def leaves_at(L):
    leaves = []
    stack = [(1, 0)]
    while stack:
        row, t = stack.pop()
        if t == L:
            leaves.append(row)
            continue
        if row & 1:
            stack.append((lhp_step(row, 1 ^ ((row >> 1) & 1)), t + 1))
        else:
            stack.append((lhp_step(row, 0), t + 1))
            stack.append((lhp_step(row, 1), t + 1))
    return leaves
L = 28
leaves = leaves_at(L)
res = {}
for spec in ["01", "0001", "011", "1"]:
    w = [int(ch) for ch in spec]
    mx = 0
    n = 0
    for row in leaves:
        for ph in range(len(w)):
            tail = periodic_tail(w, ph, cap + 2)
            if tail[0] != (row & 1):
                continue
            n += 1
            mx = max(mx, tail_survival(row, tail, cap))
    res[spec] = (n, mx)
out.append(f"(d) L=28 leaves={len(leaves)} (expected 43664); tests,max per tail: {res} (expected 01:(43664,20) 0001:(89052,22) 011:(64634,18) 1:(20970,7))")
print("\n".join(out))
