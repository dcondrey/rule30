#!/usr/bin/env python3
"""Write the time-reversed forbidden-factor list of an r_exact_sat.py JSON.

Orientation control for hf_lang_survival.py --exact-json.  The repository's
convention (constant_tail_actual_frontier.endpoint_bits with
right_trace_realizable: bits[k] = rho_k = s(2k, 1), k increasing with time,
and psi_kernel.Endpoint.append adding the later symbol) puts e_0 earliest, so
the exact language is applied in index order.  If the reversed language gave
materially different survival, the orientation would be load-bearing.
"""

import json
import sys

src, dst = sys.argv[1], sys.argv[2]
with open(src) as fh:
    data = json.load(fh)
data["forbidden"] = [f[::-1] for f in data["forbidden"]]
data["words_last_length"] = [w[::-1] for w in data["words_last_length"]]
data["reversed"] = True
with open(dst, "w") as fh:
    json.dump(data, fh)
print(f"wrote {dst}: {len(data['forbidden'])} reversed factors")
