"""Directly assert the closed form for _edge_after_zero_padding(n) at every
n=1..80, rather than trusting the inductive sketch alone."""
from fastdk_core import _edge_after_zero_padding

def predicted(n):
    # f(0)=3; f(i)=2 if i odd, 1 if i even, for i=1..n-1
    vals = [3]
    for i in range(1, n):
        vals.append(2 if i % 2 == 1 else 1)
    return tuple(vals)

bad = []
for n in range(1, 81):
    edge, endpoint_sym = _edge_after_zero_padding(n)
    pred = predicted(n)
    if edge != pred or endpoint_sym != 0:
        bad.append((n, edge, pred, endpoint_sym))

print("checked n=1..80, mismatches:", len(bad))
for row in bad[:10]:
    print(" ", row)
