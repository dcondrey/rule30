"""Does append_dependency_edge preserve earlier positions when fed a
NON-constant (varying) sequence, i.e. is 'edge' a genuine frozen/growing
prefix in general, or was the frozen-prefix observation for constant feed
just a coincidence of feeding the same value repeatedly? Independent check,
random feed, exhaustive small feed.
"""
import random
from fastdk_fastedge import append_edge_fast as append_dependency_edge

def run(seq):
    edge = ()
    endpoint_sym = None
    history = []
    for v in seq:
        edge = append_dependency_edge(edge, endpoint_sym, v)
        endpoint_sym = v
        history.append(edge)
    return history

random.seed(0)
seq = [random.choice([0,1,2,3]) for _ in range(40)]
H = run(seq)
frozen = all(H[m][:len(H[m-1])] == H[m-1] for m in range(1, len(H)))
print("random feed, frozen prefix across full run:", frozen)
if not frozen:
    for m in range(1, len(H)):
        if H[m][:len(H[m-1])] != H[m-1]:
            print("  first break at m=", m, "old=", H[m-1], "new_prefix=", H[m][:len(H[m-1])])
            break

# Exhaustive over all length-6 sequences from {0,1,2,3}
import itertools
bad = 0
total = 0
for seq in itertools.product(range(4), repeat=6):
    H = run(seq)
    total += 1
    if not all(H[m][:len(H[m-1])] == H[m-1] for m in range(1, len(H))):
        bad += 1
print(f"exhaustive length-6 over alphabet 4: total={total} violating_frozen_prefix={bad}")
