"""Does convergence to the 2-cycle attractor during a constant run eventually
happen given enough steps, or does it genuinely never happen for some
histories? And does the number of steps needed scale with warmup length
(no fixed mixing time) or stay bounded (fixed mixing time, independent of
history length)?
"""
from fastdk_fastedge import append_edge_fast as append_dependency_edge

def run(seq):
    edge = ()
    endpoint_sym = None
    for v in seq:
        edge = append_dependency_edge(edge, endpoint_sym, v)
        endpoint_sym = v
    return edge, endpoint_sym

def pure_constant_tail(const, length):
    edge, _ = run([const] * length)
    return edge

def first_convergence_step(warmup, const, max_tail=200):
    """Return the smallest tail_len at which edge[-1] matches the pure
    constant trajectory's corresponding f(tail_len-1) value AND stays
    matched for the rest up to max_tail (to rule out a fluke one-off
    coincidence rather than genuine lock-in)."""
    seq = list(warmup)
    edge = ()
    endpoint_sym = None
    for v in seq:
        edge = append_dependency_edge(edge, endpoint_sym, v)
        endpoint_sym = v
    tops = []
    for t in range(1, max_tail + 1):
        edge = append_dependency_edge(edge, endpoint_sym, const)
        endpoint_sym = const
        tops.append(edge[-1])
    # pure trajectory tops (same length range)
    pure_edge_full = pure_constant_tail(const, max_tail)
    # pure_edge_full[i] corresponds to tops[i] IF the recursion only cared
    # about how many constant steps have elapsed -- check this alignment.
    match_from = None
    for i in range(max_tail):
        if tops[i:] == list(pure_edge_full[i:]) and len(tops[i:]) > 10:
            match_from = i
            break
    return match_from, tops[:20], pure_edge_full[:20]

# The problematic case from before
warmup_len = 39
const = 3
import random
random.seed(1)
_ = [random.choice([0,1,2,3]) for _ in range(1)]  # burn to reproduce same seed state as before (trial index 7)
# Reconstruct exact warmup used in trial 7 of the previous script deterministically:
random.seed(1)
warmups = []
for trial in range(10):
    wl = random.randint(0, 40)
    warmup = [random.choice([0,1,2,3]) for _ in range(wl)]
    c = random.choice([0,1,2,3])
    tl = random.randint(10,30)
    warmups.append((warmup, c, tl))
warmup7, const7, tail7 = warmups[7]
print("reconstructed trial7: warmup_len=", len(warmup7), "const=", const7, "orig_tail_len=", tail7)

match_from, tops20, pure20 = first_convergence_step(warmup7, const7, max_tail=300)
print("match_from (steps of constant feed needed before permanent lock-in):", match_from)
print("tops[:20] =", tops20)
print("pure[:20] =", pure20)
