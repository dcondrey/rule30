"""Does a LOCAL constant run at the end of an arbitrary (wild) feed history
pull the top few diagonal entries onto the SAME period-2 attractor found for
the pure-constant-from-scratch case, regardless of what came before?
This would be a genuine 'forgetting'/coupling result if true.
"""
import random
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

random.seed(1)
mismatches = 0
trials = 0
for trial in range(200):
    warmup_len = random.randint(0, 40)
    warmup = [random.choice([0, 1, 2, 3]) for _ in range(warmup_len)]
    const = random.choice([0, 1, 2, 3])
    tail_len = random.randint(10, 30)
    seq = warmup + [const] * tail_len
    edge, endpoint_sym = run(seq)
    # Compare the LAST few entries of edge to the pure-constant-from-scratch
    # trajectory of the SAME const, same length as the constant run.
    pure_edge = pure_constant_tail(const, tail_len)
    # both arrays have different total lengths (edge has warmup_len+tail_len,
    # pure_edge has tail_len) -- compare their LAST min(len) entries.
    k = min(len(edge), len(pure_edge), 8)
    tail_actual = edge[-k:]
    tail_pure = pure_edge[-k:]
    trials += 1
    if tail_actual != tail_pure:
        mismatches += 1
        if mismatches <= 5:
            print(f"MISMATCH trial={trial} warmup_len={warmup_len} const={const} tail_len={tail_len}")
            print(f"  actual last{k}={tail_actual}  pure last{k}={tail_pure}")

print(f"\ntrials={trials} mismatches={mismatches}")
