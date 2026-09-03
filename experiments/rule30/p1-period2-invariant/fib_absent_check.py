#!/usr/bin/env python3
"""Is the length-7 hard-core block 1221222 genuinely absent from RW forced words,
or was n <= 17 too thin?  Search n = 18, 19, both c, every W, every forced run."""
from fib_transfer_screen import forced_words
target = "1221222"
for n in (18, 19):
    for c in (2, 3):
        found = 0
        runs7 = 0
        for w in forced_words(n, c, True, True, n + 2):
            if len(w) >= 7:
                runs7 += 1
                if target in "".join(map(str, w)):
                    found += 1
        print(f"n={n} c={c}: runs of length >= 7: {runs7}; containing {target}: {found}", flush=True)
