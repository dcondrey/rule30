# Recalibration: finite success has not predicted closure

Date: 2026-09-02

Status: **METHODOLOGICAL CHECKPOINT.  NO NEW PERIOD-TWO LEMMA IS CLAIMED.**

This note records the failed extrapolations that must govern the remaining
work.  A finite pass is useful only as a falsification attempt against a
specific symbolic statement.  It supplies no positive weight toward the
missing all-length quantifier.

## Conjectures that survived substantial finite tests and then failed

1. **Sharp binary-wedge horizon.**  The proposed bound
   `M_c(n) <= n` passed every complete length through `n=14`.  At `n=15`,
   tail `c=3`, the source `111122211212112` has continuation length 16, so
   `M_3(15)=16` and the claim is false.

2. **Two-step fan-out retreat cover.**  The proposed ancestry assigned every
   retreat, apart from one boundary credit, to a state-1 fan-out event in the
   current or preceding update.  It fails already at queue length five:
   `21101` has two retreats and no fan-out event anywhere in its orbit.

3. **Two-ended bounded annotation.**  Adding both endpoint symbols to the
   anchored defect data had no transition collision through the complete
   held-out lengths 11 and 12.  At length 13 the tail-3 words
   `1212221222122` and `1221221222122` have the same annotation and different
   successors.  The missing information lies in the interior dependency
   queues.

4. **Actual-language ancestry depth-two cap.**  Exact actual endpoints
   suggested maximum depth two through endpoint length 26.  A hard-core
   endpoint of length 64 has a realizable orbit of ancestry depth four.  The
   apparent cap was a finite artifact, not an invariant of the actual
   language.

5. **Nonfinal alpha support (NAS).**  NAS passed 370,944 exact held-out
   word/tail cases (and 390,944 completed cases when the later random rows are
   included).  It was then retired logically: at `j=n` its witness interval
   is empty, so its assertion is exactly the desired conclusion
   `s_c(W) <= n+1`.  The successful test measured a restatement, not a
   mechanism.

## Honest weight of the live statements

- **`M_c(n) <= n+1`, equivalently nonconstancy of `Psi_n`.**  Low weight.
  It has the same linear-horizon shape as the bound that first failed at
  length 15, and `Psi_n` is an exact coordinate change rather than
  independent corroboration.  The extra cell is exactly what the known
  counterexample leaves; it is not a discovered invariant.

- **A bounded carried-phase composition law for `(Q_n,Psi_n)`.**  Very low
  weight until an explicit closed state and update are derived.  Prefix and
  suffix recursions already fail without phase, under reversal and
  complementation.  The two-ended annotation and actual-language depth cap
  show that a state which merely delays collisions is not evidence of
  closure.

- **The hard-core rotated-wedge statement / three-row late-diagonal
  statement.**  More structurally plausible than the arbitrary-binary
  relaxation because it retains the hard-core junction and terminal `12a`
  event, but still unproved and entitled to no positive inference from its
  finite UNSAT instances.  Its value is logical weakness, not empirical
  confirmation.

- **The endpoint-orbit separator.**  This is the single open unbounded lemma
  after the proved reductions.  It is the correct public question, not
  evidence for itself.  Rephrasing it as queue mortality, a wedge equality,
  or a deterministic defect map does not create additional lemmas or
  independent support.

The number of open unbounded lemmas remains **one**.
