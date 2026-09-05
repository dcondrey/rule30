"""Complete functional-graph structure of F(a,b) = (b, cone_local(a,b)) on
the full 4x4=16 state space {0,1,2,3}^2. Pure finite check, no simulation
needed -- exhaustive over all 16 states."""
from dyadic_periodicity_analyzer import cone_local

def F(pair):
    a, b = pair
    return (b, cone_local(a, b))

states = [(a, b) for a in range(4) for b in range(4)]
# Find all cycles in the functional graph
import itertools
visited = {}
cycles = []
for s in states:
    if s in visited:
        continue
    path = []
    cur = s
    seen = {}
    while cur not in seen and cur not in visited:
        seen[cur] = len(path)
        path.append(cur)
        cur = F(cur)
    if cur in seen:
        cyc = path[seen[cur]:]
        cycles.append(tuple(cyc))
    for i, p in enumerate(path):
        visited[p] = True

print("All 16 states:", states)
print()
print("Cycles found in F's functional graph:")
for c in cycles:
    print(" ", c, "length", len(c))

print()
print("Per-state eventual cycle (which cycle each of the 16 states drains into), and transient length:")
for s in states:
    path = []
    cur = s
    seen = {}
    while cur not in seen:
        seen[cur] = len(path)
        path.append(cur)
        cur = F(cur)
    cyc_start = seen[cur]
    cyc = tuple(path[cyc_start:])
    print(f"  start={s} transient_len={cyc_start} cycle={cyc}")
