"""Idea: is the pure zero-fed dependency-edge trajectory (append_dependency_edge
fed constant value=0 forever) a triangular/frozen-prefix construction (i.e. a
genuine well-defined infinite word, each new step appending one symbol without
touching earlier ones)? If so, is that infinite word eventually periodic?
Read-only reuse of fastdk_fastedge.append_edge_fast.
"""
from fastdk_fastedge import append_edge_fast as append_dependency_edge

def zero_trajectory(m):
    edge = ()
    endpoint_sym = None
    history = []
    for _ in range(m):
        edge = append_dependency_edge(edge, endpoint_sym, 0)
        endpoint_sym = 0
        history.append(edge)
    return history

H = zero_trajectory(60)
# Check triangularity: is history[m][:len(history[m-1])] == history[m-1] for all m?
frozen = all(H[m][:len(H[m-1])] == H[m-1] for m in range(1, len(H)))
print("triangular/frozen-prefix:", frozen)

# The infinite word Z = H[-1] (since frozen, this is a genuine prefix of the true infinite word)
Z = H[-1]
print("Z (first 60):", Z)

# Look for eventual periodicity: try all periods p up to 20, all start offsets up to 20
def find_eventual_period(seq, max_period=20, max_offset=30):
    n = len(seq)
    for offset in range(max_offset):
        for period in range(1, max_period):
            if offset + 3*period > n:
                continue
            ok = all(seq[offset+i] == seq[offset+i+period] for i in range(n-offset-period))
            if ok:
                return offset, period
    return None

result = find_eventual_period(Z, max_period=25, max_offset=35)
print("eventual period search (offset,period):", result)
