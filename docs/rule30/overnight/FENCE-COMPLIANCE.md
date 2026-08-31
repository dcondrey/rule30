# Fence-compliance statement (overnight run, 2026-08-30)

## Method of verification

`git status` CANNOT verify this claim: `13-rule30/` is entirely untracked inside the parent
repository at /Volumes/A/researchpapers, so the whole subtree appears as a single untracked
entry and no per-file state exists. Compliance was therefore verified by modification time:

    find . -newermt '2026-08-30T04:00:00' -type f -not -path './.git/*'

grouped by directory, then inspected file by file for the directories outside the fence.

## Statement

With one disclosed exception below, no file outside `experiments/overnight-arms/`,
`docs/rule30/overnight/`, and `runs/overnight/` was created or modified by this session, and
nothing was committed to git. No `git add`, `git commit`, `git push`, or any other
repository-mutating command was run at any point.

Created by this session:
- `docs/rule30/overnight/` — CONTEXT-DIGEST.md, TRIAGE.md, PREREG-anf.md, PREREG-ergodic.md,
  RESULTS-anf.md, RESULTS-ergodic.md, RESULTS-p2-single-seed.md, RESULTS-automaticity.md,
  RESULTS-anashin.md,
  and this file.
- `experiments/overnight-arms/` — common/rule30.py; anf/{anf_probe,anf_sweep,parity_probe,
  wedge_reduction,verify_c1_proof}.py; ergodic/{markov_probe,markov_main,markov_saturate}.py.
- `experiments/overnight-arms/` also: common/ensemble_filter.py; automaticity/ore_check.py.
- `runs/overnight/` — triage-rows.json, anf/{sweep,parity,wedge}.json, anf/t13.log,
  ergodic/{main.json,saturate.json,main.log,sat3.log}.

## Disclosed exception

`experiments/rule30/__pycache__/center_column.cpython-311.pyc` (written 04:44) was created
automatically by CPython when `experiments/overnight-arms/common/rule30.py` imported the
repo's ground-truth generator `experiments/rule30/center_column.py` for its validation gate.
This is a bytecode cache produced as a side effect of a READ-ONLY import; no source file in
`experiments/rule30/` was read-modified or written by this session, and the cache file is
regenerable and carries no content of its own. It is nonetheless outside the permitted
directories and is disclosed rather than glossed.

## Concurrent-session changes, explicitly NOT ours

The following also have mtimes inside the run window and belong to the other active session
working the alternating-trace line. This session did not create, modify, or read-lock them:
- `runs/alt-trace-automaton/` (d16/d20 outputs and logs)
- `experiments/rule30/alt_trace_fiber_probe.py` and its `__pycache__` entry (04:13)
- `experiments/rule30/proof-complexity/` (clause30/clause90/ladder30/ladder90 JSON and logs,
  fit_exponent.py)
- `docs/rule30/PATH.md`, `docs/rule30/RESULTS-alt-trace-fiber.md`,
  `docs/rule30/RESULTS-orbit-closure-diagnostic.md`,
  `docs/rule30/RESULTS-proof-complexity-probe.md`
- `docs/rule30/OVERNIGHT-PROMPT.md` (read by this session; its mtime predates our first write)

The last two RESULTS files did not exist when this session's read-only docs survey ran, which
is independent evidence they are the other session's work product, not ours.

## Subagent file activity

Prover and verifier agents were instructed to write only under the session scratchpad at
/private/tmp/claude-501/.../scratchpad and did so (wedge.py, verify.py, leadC.py, verify2.py,
verify_lemmas.py, break_attempt.py, breakcheck.py, adv_verify.py). One workflow prompt
contained a typo in the scratchpad path; any file written to the mistyped path lands outside
the repository entirely and therefore does not affect this statement. No agent wrote under
/Volumes/A/researchpapers/.

## Spending

Local CPU only. Modal $0 (the MODAL-COMPUTE-CHARTER ladder was never entered). No paid compute
beyond this session's own model calls.
