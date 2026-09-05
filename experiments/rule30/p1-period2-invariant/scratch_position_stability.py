"""Precise test: once edge has been built to some length L (state edge_A),
and we then append MORE symbols (arbitrary, varying), do LOW/OLD positions
of edge (e.g. position 0, 1, ..., L-1) stay EXACTLY as they were in edge_A,
or do they change value as more symbols get appended on top?
This is the real triangularity question, tested directly and cleanly.
"""
import random
from fastdk_fastedge import append_edge_fast as append_dependency_edge

def run(seq, edge=(), endpoint_sym=None):
    for v in seq:
        edge = append_dependency_edge(edge, endpoint_sym, v)
        endpoint_sym = v
    return edge, endpoint_sym

random.seed(2)
warmup = [random.choice([0,1,2,3]) for _ in range(20)]
edge_A, sym_A = run(warmup)
print("edge_A (len", len(edge_A), "):", edge_A)

# Now append 10 more RANDOM symbols on top, and see if edge_A's own values
# reappear at the SAME positions in the longer result.
more = [random.choice([0,1,2,3]) for _ in range(10)]
edge_B, sym_B = run(more, edge=edge_A, endpoint_sym=sym_A)
print("edge_B (len", len(edge_B), "):", edge_B)
print("edge_B[:20] == edge_A ?", edge_B[:20] == edge_A)
print("edge_B[:20]:", edge_B[:20])

# Try a DIFFERENT continuation from the SAME edge_A, see if ITS low positions
# also match edge_A (should, if position i for i<20 is a frozen fact of the
# first 20 steps alone, independent of what comes after).
more2 = [random.choice([0,1,2,3]) for _ in range(10)]
edge_C, sym_C = run(more2, edge=edge_A, endpoint_sym=sym_A)
print("edge_C[:20] == edge_A ?", edge_C[:20] == edge_A)
print("edge_B[:20] == edge_C[:20] ?", edge_B[:20] == edge_C[:20])
