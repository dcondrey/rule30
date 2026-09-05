"""Rigorous check of the zero-fed trajectory finding, plus the analogous
constant-1, constant-2, constant-3 fed trajectories. Uses the same
cone_local/BOUNDARY table as fastdk_fastedge (imported directly from
dyadic_periodicity_analyzer for a from-scratch independent check).
"""
from dyadic_periodicity_analyzer import cone_local, BOUNDARY, INVERSE, FORWARD
from fastdk_fastedge import append_edge_fast as append_dependency_edge

def constant_trajectory(const_value, m):
    edge = ()
    endpoint_sym = None
    history = []
    for _ in range(m):
        edge = append_dependency_edge(edge, endpoint_sym, const_value)
        endpoint_sym = const_value
        history.append(edge)
    return history

def find_eventual_period(seq, max_period=25, max_offset=40):
    n = len(seq)
    for offset in range(min(max_offset, n)):
        for period in range(1, max_period):
            if offset + 3 * period > n:
                continue
            ok = all(seq[offset + i] == seq[offset + i + period] for i in range(n - offset - period))
            if ok:
                return offset, period
    return None

for const in (0, 1, 2, 3):
    H = constant_trajectory(const, 80)
    frozen = all(H[m][: len(H[m - 1])] == H[m - 1] for m in range(1, len(H)))
    Z = H[-1]
    result = find_eventual_period(Z)
    print(f"const={const} frozen_prefix={frozen} Z[:16]={Z[:16]} eventual(offset,period)={result}")

# Rigorous algebraic check of the period-2 cycle for const=0 (Z tail = ...,2,1,2,1,...)
print()
print("Algebraic verification for const=0 tail cycle (2,1):")
print("  cone_local(2,1) =", cone_local(2, 1), " (want 2)")
print("  cone_local(1,2) =", cone_local(1, 2), " (want 1)")
print("BOUNDARY table:", BOUNDARY)
print("BOUNDARY[0] =", BOUNDARY[0], "(this should be Z[0])")

# Also verify the SECOND-ORDER RECURRENCE claim directly: for k>=2,
# Z[k] == cone_local(Z[k-2], Z[k-1]) exactly, checked over the whole computed history.
Z0 = constant_trajectory(0, 80)[-1]
mismatches = [k for k in range(2, len(Z0)) if Z0[k] != cone_local(Z0[k-2], Z0[k-1])]
print("second-order recurrence Z[k]=cone_local(Z[k-2],Z[k-1]) mismatches for k=2..79:", mismatches)
