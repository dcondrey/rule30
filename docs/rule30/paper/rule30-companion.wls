#!/usr/bin/env wolframscript
(* ============================================================================
   Rule 30 companion notebook script  --  Wolfram Language / Wolfram Engine.

   Purpose: reproduce, in Wolfram Language, the load-bearing VISUALS and
   cross-checks of the paper "Structure and Obstructions in the Rule 30
   Eventual-Periodicity Problem", for deposit on the Wolfram Notebook Archive.

   STATUS: STAGED, NOT YET RUN.  No Wolfram Engine was installed in the session
   that wrote this file, so nothing below has been executed or verified.  Every
   Print[] that asserts an equality is a CLAIM to be checked the first time this
   runs under `wolframscript`.  Do not trust an output until you have seen the
   kernel produce it.

   Run once the free Wolfram Engine is installed and activated:
       wolframscript -file rule30-companion.wls
   or, to also emit a .nb for the archive:
       wolframscript -file rule30-companion.wls -- --notebook

   Scope of this file: the canonical CellularAutomaton reproductions only
   (period-one fibers, the Rule 30 vs Rule 90 latch contrast).  The
   forced-continuation census / gamma / terminal-class "needle" port is a
   separate, higher-risk translation of the Python forcing recursion and is
   deliberately left as a marked TODO below, to be written WITH the engine live
   so it can be cross-checked against the Python numbers rather than guessed.
   ========================================================================== *)

(* ---------- 0. environment sanity (harmless if run interactively) ---------- *)
Print["Wolfram Language version: ", $VersionNumber];

(* ---------- 1. Rule 30 and Rule 90 evolutions from the lone seed ---------- *)
(* CellularAutomaton[rule, {{1},0}, t] evolves the single-1 seed for t steps
   on a background of 0s, returning t+1 rows, each centered.  This is the
   canonical, well-tested primitive; the risk here is low. *)

loneSeedRows[rule_, t_] := CellularAutomaton[rule, {{1}, 0}, t];

centerColumn[rule_, t_] := Module[{rows = loneSeedRows[rule, t]},
  (* each row has odd length 2 k + 1; the center index is the seed column *)
  MapThread[Part, {rows, (Length /@ rows + 1)/2}]
];

(* CLAIM to verify: Rule 90's lone-seed center column is eventually 0
   (identically 0 for t >= 1), which is exactly why Rule 90 fails the paper's
   filter; Rule 30's is not visibly periodic. *)
r90center = centerColumn[90, 64];
r30center = centerColumn[30, 64];
Print["Rule 90 center column (t=0..64): ", r90center];
Print["Rule 90 center is all zero for t>=1: ",
  AllTrue[Rest[r90center], # == 0 &]];              (* expect True *)
Print["Rule 30 center column (t=0..64): ", r30center];
Print["Rule 30 center has ones past t=1: ",
  Count[Rest[r30center], 1] > 0];                   (* expect True *)

(* ---------- 2. The OR-latch contrast on one finite row (paper Fig. 1) ------ *)
(* The finite row with ones at +-1: under Rule 90 the center stays 0 forever;
   under Rule 30 the OR latch breaks it.  Paper Part I / Corollary. *)
delta11 = {1, 0, 1};   (* support at -1, +1 on the background 0 *)
r90fin = CellularAutomaton[90, {delta11, 0}, 12];
r30fin = CellularAutomaton[30, {delta11, 0}, 12];
center[rows_] := MapThread[Part, {rows, (Length /@ rows + 1)/2}];
Print["Rule 90, x=d(-1)+d(1), center stays 0: ",
  AllTrue[center[r90fin], # == 0 &]];               (* expect True *)
Print["Rule 30, same row, center escapes at t=",
  FirstPosition[center[r30fin], 1] ];               (* expect a finite t *)

(* ---------- 3. Period-one zero-trace fiber (paper Theorem 2) --------------- *)
(* For a right half with first 1 at depth m, the zero-trace-compatible left
   half is L_j = 0 (j<m), L_m = 1, L_j = j mod 2 (j>m).  We build a class-C_m
   row, evolve it, and CHECK the center trace is identically zero over its
   light cone.  This mirrors experiments/rule30/zero_tail_probe.py. *)
buildCm[m_, rightTail_List, width_] := Module[{L, R},
  R = Join[{0}, PadRight[rightTail, width]];        (* R_0=0, then the tail *)
  R[[m + 1]] = 1;                                   (* enforce first one at m *)
  L = Table[Which[j < m, 0, j == m, 1, True, Mod[j, 2]], {j, 1, width}];
  Join[Reverse[L], {R[[1]]}, Rest[R]]               (* row indexed -width..width *)
];

(* CLAIM to verify: the center trace of a C_3 row is 0 through its light cone. *)
cmRow = buildCm[3, {0, 0, 1, 0, 1, 1, 0, 1}, 16];
cmRows = CellularAutomaton[30, {cmRow, 0}, 8];
Print["C_3 zero-trace through the light cone: ",
  AllTrue[center[cmRows], # == 0 &]];               (* expect True *)

(* ---------- 4. TODO (write with the engine live, cross-check vs Python) ---- *)
(* The forced-continuation census is defined in
     experiments/rule30/p1-period2-invariant/late_pull_diagonal_sat.py
   via append_dependency_edge / cone_local over the 4-state carry alphabet.
   Porting it to WL is a faithful but non-trivial translation and MUST be
   cross-checked cell-by-cell against the Python `literal_extension` output
   (e.g. n<=16, both c) before any gamma/needle figure is trusted.  Do not
   guess it here; write it against a running kernel.  Target reproductions:
     - gamma(n) for n=8..24 vs RESULTS-KSTAR-GAMMA-EXTENDED.md,
     - the terminal-class suffix collapse vs RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md,
     - the hard-core spectral radius = GoldenRatio (trivial in WL: it is
       Max[Abs[Eigenvalues[{{0,1},{1,1}}]]] == GoldenRatio). *)
Print["Spectral radius check: ",
  Max[Abs[Eigenvalues[{{0, 1}, {1, 1}}]]] == GoldenRatio];  (* expect True *)

(* ---------- 5. optional .nb emission for the archive ----------------------- *)
If[MemberQ[$ScriptCommandLine, "--notebook"],
  Print["Notebook emission requested; implement Export of a Notebook[...] here ",
        "once the figure cells above are verified."]
];

Print["companion script reached end (verification status: UNRUN until a kernel ",
      "executes it)."];
