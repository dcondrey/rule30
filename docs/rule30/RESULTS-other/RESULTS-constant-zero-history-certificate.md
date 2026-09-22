# The 41-symbol, 22-zero history class is empty

Date: 2026-09-13. **Proved by an independently checked finite UNSAT
certificate:**

\[
\boxed{C_{41}(0^{22})=\varnothing.}
\]

No legal original length-41 auxiliary frontier survives 22 consecutive
updates emitting zero. In particular, the candidate counting inequality
holds for this test case with exact left side zero.

This is not mortality of every length-41 frontier: other tapes are not
excluded. It is not an all-length repeat bound or period-two exclusion,
and no singleton-seed reachability is asserted. Prefix inclusion does
exclude every extension `0^22 beta` at this **same original length**.

## 1. Why this case matters

The [width-three obstruction](RESULTS-coupled-message-depth-audit.md)
shows that the canonical window upper message at this tape has a global
floor `2^-20` after 40 spatial transfers. The desired probability threshold
is `2^-21`. Thus that message scheme provably cannot certify this case.

The [first exact suffix-mixture attempt](RESULTS-guarded-history-mpo.md#10-a-bounded-exact-compression-attempt-on-the-width-three-obstruction)
stopped at 11 spatial transfers and supplied only

```text
|C_41(0^22)| <= 64,435 * 2^60.
```

The [shared-prefix MPS attempt](RESULTS-shared-prefix-mps.md) completed 13
transfers under the same 4,096-state cap and supplied only

```text
|C_41(0^22)| <= 334,085 * 2^57.
```

The requested count threshold is `2^60`. Both upper bounds were valid but
insufficient. The new proof settles the exact count through a different
representation of the same original variables and guarded dynamics.
The positive floors in those upper calculations are not actual survivor
mass in this case.

## 2. Exact encoding, without a fresh completion at any time

The [encoder and verifier](../../experiments/rule30/constant_zero_history_sat.py)
start with exactly the 82 original high/low bits and impose `a_0=1`.
There are therefore 81 free original bits. Additional variables represent
deterministic gate outputs, not additional original choices.

For each prescribed scalar s, initialize the scan memories to zero and
encode, in the original chronological order,

```text
v = v XOR (previous_a OR b_i),
u = u XOR (v OR a_i),
emit (u,v),
previous_a = a_i.
```

Both final bits are constrained to equal s. The next layer is the full
emitted word with the symbol `3-s` appended. In this instance every s is
zero, so each appended symbol is 3. No intermediate guard is omitted.

**Faithfulness theorem.** For every finite legal original length and every
prescribed tape, satisfying assignments of this encoding are in bijection
with its complete original ancestor set.

**Proof.** The OR and XOR clauses impose precisely the indicated Boolean
gate, with a unique output for every input. This remains true of the
signed-literal and constant simplifications. Given the original bits,
induction through the scan determines every intermediate gate and emitted
symbol uniquely. The two terminal clauses hold exactly when that step
successfully emits the prescribed scalar. Appending `3-s` then gives
exactly the input for the next actual update. Induction over all layers
retains all earlier guards and yields the original trajectory. Conversely,
each successful original supplies those unique gate values and satisfies
every clause. Hence the encoding is parsimonious. In particular, UNSAT
means the original ancestor class is empty, not merely that a chosen
normal form or intermediate fiber is empty.

## 3. A proof checked without the generating solver

The saved formula has 4,465 variables and 15,372 clauses:

* [DIMACS formula](../../experiments/rule30/constant-zero-history-sat/r41-n22.cnf);
* [DRUP proof](../../experiments/rule30/constant-zero-history-sat/r41-n22.drup);
* [verification artifact](../../experiments/rule30/constant-zero-history-sat.json).

The accepted proof was produced with Glucose4. The existing independent
[RUP checker](../../experiments/rule30/p1-period2-invariant/verify_drup.py)
verifies all 266 proof additions, including the final empty clause. For
each addition it assumes the clause's negation and finds a contradiction
by unit propagation from the formula and earlier verified consequences.
Deletion records may be ignored soundly, because retained lemmas were
themselves verified consequences of the original formula.

The default verification command does not invoke a SAT solver:

```text
uv run --offline --no-project python experiments/rule30/constant_zero_history_sat.py
```

It rebuilds the formula byte-for-byte, checks 352 gate truth-table cases,
checks 96 directed original-word/tape cases against the frozen independent
frontier oracle, and verifies the complete proof. The saved run took
approximately 0.31 seconds. The artifact records source and proof hashes.
The controls test the implementation; the gate argument above and checked
refutation establish the stated exact result.

An earlier CaDiCaL run also reported UNSAT, but its exported proof failed
the final-empty-clause RUP check. A second, straightforward unit-propagation
check also failed there. That export is explicitly excluded from this
certificate. No modification of the frozen checker was used to accept it.

## 4. What remains unresolved

This clears a concrete test case on which the upper-message schemes
stalled. It does not supply uniform control of approximation error under
repeated transfers, nor a cumulative information argument across scalar
switches.

The [reference-message analysis](RESULTS-reference-message-compression.md)
separately proves that a small nonnegative MPS can preserve the two origin
values at a single stage. Its exact error identity shows why this alone
does not preserve them through later transfers: errors at reachable
intermediate columns contribute nonnegatively to the final count bound.
The missing estimate concerns that accumulated, trajectory-weighted error
or the original exact counts themselves.

The main inequality, every uniform positive-repeat-rate alternative, and
period-two center exclusion remain open. No further constant-episode
threshold search or larger original census was performed to infer otherwise.
