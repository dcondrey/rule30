#!/usr/bin/env python3
"""Round-5 kill tests (fifth external batch, source reading, W of length n, Psi of length n+2)."""
from itertools import product
from psi_kernel import psi

def hc(W): return "11" not in "".join(map(str, W))
def ham(a, b): return sum(x != y for x, y in zip(a, b))

print("== first-diff-visible: hard-core W,W' with first difference d, Psi equal on [n, min(2n+1, d+n+6)]?")
for n in range(6, 15):
    P = {W: psi(W)[1] for W in product((1, 2), repeat=n) if hc(W)}
    Ws = list(P)
    bad = None
    for a in range(len(Ws)):
        for b in range(a + 1, len(Ws)):
            W, V = Ws[a], Ws[b]
            d = next(i for i in range(n) if W[i] != V[i])
            hi = min(n + 2, d + 7)  # indices j-n in [0, hi)
            if P[W][:hi] == P[V][:hi]:
                bad = (W, V, d); break
        if bad: break
    print(f"   n={n}: {'KILLED e.g. ' + str(bad) if bad else 'holds'}")

print("== klein-toggle: sum of 6 pairwise Psi distances over {W, W^R, W^C, W^RC} >= n/10, all four hard-core")
for n in range(6, 16):
    P = {W: psi(W)[1] for W in product((1, 2), repeat=n)}
    worst = None
    for W in P:
        R = W[::-1]; C = tuple(3 - s for s in W); RC = C[::-1]
        if not all(hc(x) for x in (W, R, C, RC)): continue
        fam = [P[W], P[R], P[C], P[RC]]
        s = sum(ham(fam[i], fam[j]) for i in range(4) for j in range(i + 1, 4))
        if worst is None or s < worst[0]: worst = (s, W)
    print(f"   n={n}: min sum={worst[0]} need {n/10:.1f} -> {'KILLED' if worst[0] < n/10 else 'holds'}  at W={''.join(map(str,worst[1]))}")

print("== periodic-source-defect-oscillation: periodic hard-core W, p<=12, n multiple of p, n<=60: Psi constant?")
found = []
for p in range(1, 13):
    for w in product((1, 2), repeat=p):
        if "11" in "".join(map(str, w * 2)): continue
        for n in range(p, 61, p):
            if n > 22: break
            W = tuple((w * (n // p + 1))[:n])
            _, ps = psi(W)
            if len(set(ps)) == 1: found.append((p, "".join(map(str, w)), n, ps[0]))
print(f"   constant Psi tails: {found[:8]} -> {'KILLED' if found else 'holds (n<=22 by cost)'}")

print("== boundary-read-reversal-shot: W^S = reversed Q_n(W) truncated to n; pointwise Psi_j(W^S) != Psi_{L-1-j}(W)?")
for n in range(6, 15):
    bad = 0; tot = 0
    for W in product((1, 2), repeat=n):
        if not hc(W): continue
        q, ps = psi(W)
        S = tuple(q[::-1][:n])
        if not hc(S): continue
        _, ps2 = psi(S)
        tot += 1
        if any(ps2[j] == ps[len(ps) - 1 - j] for j in range(len(ps))): bad += 1
    print(f"   n={n}: {bad} of {tot} admissible pairs have an equal mirrored position -> {'KILLED' if bad else 'holds'}")

print("== haar-influence: #bits whose hard-core-preserving flip changes Psi somewhere >= n-4, min over hard-core W")
for n in range(6, 16):
    P = {W: psi(W)[1] for W in product((1, 2), repeat=n)}
    worst = None
    for W in P:
        if not hc(W): continue
        cnt = 0
        for i in range(n):
            V = W[:i] + (3 - W[i],) + W[i + 1:]
            if hc(V) and P[V] != P[W]: cnt += 1
        if worst is None or cnt < worst[0]: worst = (cnt, W)
    print(f"   n={n}: min influential bits={worst[0]} need {n-4} -> {'KILLED' if worst[0] < n-4 else 'holds'}  at W={''.join(map(str,worst[1]))}")
