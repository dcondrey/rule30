# Clock-free automatic-diagram construction class

Date: 2026-09-09. Status: prepared exact class; no Rule 30 search result yet.

## 1. Mechanism and kill condition

Search for a Rule 30 half-plane represented by a binary MSB paired-digit
automaton with at most six full states, at most three reachable time-axis
states, and a single binary output function. No separate temporal or
spatial lookup clock is supplied. The exact observation predicate asks
for an eventually periodic centre and an aperiodic masked right neighbour;
it prescribes neither a centre word nor an eventual onset or period.

This is a distinct construction class from the four-state, time-40,
space-eight model. More state transitions are available, while the output
depends solely on the state reached by the coordinate digits. No
containment between these two fixed-size classes is asserted.

Before a run, the resource cap is 60 seconds. A proposed counterdiagram
must pass the complete 20,736-state gate-product bound and the exact
observation test. UNSAT requires a saved DRUP proof and independent replay
before a certified class exclusion is reported. UNKNOWN preserves the
entire candidate/cut pool and proves no class exclusion. No finite-class
result by itself proves or kills R1.

## 2. Exact representation reduction — U

The existing audited composition formulas distinguish the final time
digit through a formal lookup period two. Set the spatial lookup period
to one and equate the two output tables entry by entry. The resulting
value at every coordinate is exactly the output of the final DFA state;
the formal period-two phase carries no additional information. Conversely,
every single-output-table six-state DFA has precisely such a presentation.
Thus the equality constraints define the intended clock-free class.

Only the reachable time-axis states use symbols zero and two. Rename its
at most three states first in discovery order, and keep every off-axis
transition and return arbitrary. The same 50 canonical axes suffice.
For each axis, compute the exact endpoint relation from the
[uniform MSB period theorem](RESULTS-r1-automatic-period-bound.md).
With formal period two, no upper low-digit folding remains: each
endpoint pair supplies both possible final-time phases. Centre equality
on every pair and a zero-centre/right-unequal pair are exactly the
eventual-centre/aperiodic-mask predicate. The output-table equalities do
not alter this equivalence.

The Rule 30-only necessary tail clause excludes an eventually zero
centre: then the right neighbour obeys `r_(t+1)=r_t OR s(t,2)` and becomes
constant. All endpoint pairs, including diagonal pairs, contribute to
the tail's left projection. This use of OR is not imposed on Rule 90.

## 3. Prepared formula and controls — C

`direct_dfa_clockfree_encoding.py` builds an observation formula with 178
variables and 1,003 clauses: 50 exact axis cases, 140 phase-forest edges,
57 naming clauses, 168 composition clauses, and 50 OR-tail clauses.
Adding 64 ordinary gates and the uniform depth-three prefix equations
gives 4,118 variables and 59,152 clauses. The prefix criterion covers
252 guarded gates over six prefix types; it remains only a necessary
condition. The full gate bound is `6^4*8*2=20736`.

The exact Rule 90 control uses six reachable full states, projecting to
the independently verified minimal three-state control through
`[0,1,2,2,2,2]`. Every transition respects that projection, so equality of
the represented diagrams is uniform. The control has three time-axis
states and satisfies the exact R1 observation. Its complete gate check
uses 317 states, 65 terminal cases and 832 transitions; all 252 scalar
prefix gates and the full prepared Rule 90 CNF under fixed parameters
pass. A separate 8,192-coordinate check confirms the formal-period-two
and single-table values agree. This last count is calibration of the
symbolic table-equality argument, not its proof.

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_clockfree_encoding.py
```

## 4. Scope

The representation reduction is uniform. The setup and controls are
finite checks of an exact finite-class predicate. No Rule 30 diagram,
UNSAT result, or R1 conclusion has yet been obtained in this class.
