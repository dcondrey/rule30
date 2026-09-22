# P3: scope of the reviewed support-wave implementation

Date: 2026-09-14. This records the source review already made during this
session. It adds no new external experiment and claims no P3 solution.

## 1. Source and version

The reviewed release is [Fomin's support-wave v6](https://zenodo.org/records/22646809),
dated 2026-09-07. The previously inspected record `22158026` was v2, not v3.
The v6 paper, TeX, README and relevant Python source have now been preserved
under `research/p3-session-sync/external/fomin-v6/`, with byte hashes in
[the provenance manifest](../../research/p3-session-sync/external/fomin-v6/provenance.json).
The [reviewed implementation](../../research/p3-session-sync/external/fomin-v6/wave/window_fast.py)
and [paper source](../../research/p3-session-sync/external/fomin-v6/flagship.tex)
are retained verbatim. They were copied from this session's existing downloaded
files without a new network fetch. The source code was read, not executed.
The archived README identifies the paper license as CC-BY-4.0 and code as MIT.

## 2. What the supplied window evaluator costs

The archived `wave/window_fast.py` represents two entire support indicators
of length `M=2^k`, for integer `k>=1` (the script's main loop uses k=2..14).
Every iteration of `run_k` performs three `zeta_fast`
transforms. Each transform visits k stages and updates M/2 entries per
stage. It then constructs the shifted indicator and serializes both full
rows for the `seen` dictionary. Consequently **one performed support
advance costs Theta(M log M) scalar Boolean/array-entry operations**.
It is not one unit-cost operation on a giant integer.

If this evaluator is used for t-O(1) advances at M=Theta(t)>t, those
advances cost Theta(t^2 log t) in that scalar accounting, before additional
indexing and dictionary costs. Retaining all serialized history keys can
also use Theta(tM) bytes before a repeated pair is found. The program's
time and iteration caps may stop it early; such termination is not a
correct exact-center answer. This is a static loop-count argument for
this implementation, not a measured benchmark or a lower bound on other
implementations of support-set algebra.

The center formula and the safe support cutoff remain exact in their
specified indexing; see [the Fibonacci audit](RESULTS-p3-fibonacci-interpolation-audit.md).
They still require constructing the relevant support memberships. The
front's small state does not supply those interior memberships for free.

## 3. Corrections and remaining claims

The v6 abstract and introduction explicitly describe the minimal moving
front period `2B` as measured on the tested octaves. The finite automaton
establishes eventual periodicity for its fixed finite front object; its
existence alone does not prove minimal period `2B` at every width. This
review therefore retains `2B` as finite evidence, not as an all-width
theorem or a refuted conjecture.

The README records that later revisions corrected the earlier OR-maximum
argument and withdrew a NOR identification. That correction history is
preserved; it does not invalidate the separate exact support identities.
The session did not independently replay the external scripts, prove every
claim in the three companion papers, or establish an all-input fast
implementation. No fresh verification receipt is inferred from archival
hashes. The next P3 obligation remains an actual singleton constructor
with all work charged, rather than another finite moving-front census.
