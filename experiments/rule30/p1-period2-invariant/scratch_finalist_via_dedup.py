"""Recover a representative extremal (max-survival) SOURCE WORD per n, using
the fast dedup state walk (fastdk_core.distinct_final_states), instead of
brute force. Read-only reuse of fastdk_core/fastdk_fastedge; writes nothing
into either. Purpose: idea (2) from the task brief -- do extremal words
converge to a common suffix / infinite limiting word as n grows?
"""
import sys
from fastdk_core import (
    _edge_after_zero_padding,
    forced_continuation_from_state,
    survived_prefix,
)
from fastdk_fastedge import append_edge_fast as append_dependency_edge


def distinct_final_states_with_word(n):
    zero_edge, zero_endpoint = _edge_after_zero_padding(n)
    states = {(zero_edge, zero_endpoint): ()}
    for step in range(n):
        new_states = {}
        for (edge, endpoint_sym), word in states.items():
            for value in (1, 2):
                new_edge = append_dependency_edge(edge, endpoint_sym, value)
                key = (new_edge, value)
                if key not in new_states:
                    new_states[key] = word + (value,)
        states = new_states
    return states


def main():
    tail = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    residue = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    ns = [int(x) for x in sys.argv[3:]] if len(sys.argv) > 3 else list(range(6, 27))

    for n in ns:
        target = n + residue
        rows = target + 2
        states = distinct_final_states_with_word(n)
        best = -1
        best_words = []
        for (edge, endpoint_sym), word in states.items():
            cont = forced_continuation_from_state(edge, endpoint_sym, tail, rows)
            survived = survived_prefix(cont, endpoint_sym)
            if survived > best:
                best = survived
                best_words = [word]
            elif survived == best:
                best_words.append(word)
        gamma = rows - best
        ws = [''.join(map(str, w)) for w in best_words[:6]]
        extra = f" (+{len(best_words)-6} more)" if len(best_words) > 6 else ""
        print(f"n={n:3d} c={tail} r={residue} max_survival={best:3d} gamma={gamma:3d} "
              f"n_distinct_states={len(states):8d} finalists={ws}{extra}", flush=True)


if __name__ == "__main__":
    main()
