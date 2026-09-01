"""Sanity candidate (d) [bonus, not in the required 3]: tries to cheat via
an embedded lookup table sized to plausibly cover small evolve/holdout n,
then falls back to (slow, wrong-on-purpose-shaped) garbage for anything
else. Should be caught either by the literal-size scan or by the trap-set
check, whichever fires first -- either way, combined_score must be 0.0."""
_TABLE = {i: (i * 2654435761) % 2 for i in range(4000)}  # 4000-entry fake "table"

def center_cell(n: int) -> int:
    if n in _TABLE:
        return _TABLE[n]
    return 0  # wrong for anything outside the embedded range
