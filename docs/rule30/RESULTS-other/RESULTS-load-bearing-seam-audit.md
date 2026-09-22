# Load-bearing seam audit: two search bugs and several scope corrections

Date: 2026-09-09. Overnight Task 6; bounded, named coverage.

**Two paths in `gap3_probe.explore` could incorrectly return extinction.
Both are repaired. The saved Task 1 findings survive: their positive
cycles and direct empty-image certificates do not use either false return.**
The audited algebraic junctions passed. Several logical conclusions in the
four-statement report require narrower wording.

| Claim audited | Verdict and coverage |
|---|---|
| Kopra finisher at an eventual onset | PASS: journal eventual form, left-finite hypothesis; separate primary-source report |
| Family-seam `1(001)^9 00001 00001(001)^6` and k=7 boundary | PASS: independent exact strip replay, complete terminal return; arithmetic onset map checked |
| Gap explorer: exhaustion means no infinite continuation | **FAIL, repaired**: depth cap and unrecognized cross-edge cycle |
| Reversed frontier macro's last-symbol test | PASS: independent scan/macro comparison, Task 4; suffix-only restriction fails as documented |
| Image DFA includes exactly the appended terminal symbol | PASS after strengthened check: equality of output sets through seed length 7, including output length 8 |
| Image-count recurrence claimed at all lengths | PASS with a new finite linear-algebra certificate, not just the existing q<=58 regression |
| Rotated Peel identity at first/last coordinates; last-nonzero preservation | PASS: 21,840 endpoint words; 1,365 triangular prefixes; complete local boundary row and finite support checks |
| High-bit elimination from first appended symbol to final defect | PASS: 1,593 affine cases, 126 sources, and the n=15 terminal flip |
| C3 source/forced-extension seam, tail-3 final-row convention | PASS within replay range: exact frozen graph comparison and all scalar scenario rows in Task 5 |
| Repaired rung-3 bridge | PASS on all 16 entering/leaving letter pairs, checking both junctions; large existing splice grid not rerun |
| Four-statement audit's q=1/q=420, polarity and universe claims | **CORRECTION REQUIRED**; see §4 |

Evidence: `C` for enumerations/certificates, `U` for accompanying algebraic
arguments, `K` for the two explicit false-extinction witnesses. This is not
an audit of every U-level row in the capsule.

## 1. Reproduced search failures and repair

The original source at commit `76f3dc4` is loaded from that exact Git object
for regression; its hash is recorded in `seam-audit/results.json`.

**Depth boundary.** Starting with the nonempty width-8 stable gap-1 set and
`depth_cap=0`, the old code skips every expansion and returns `extinct`.
This is a counterexample using the actual Rule 30 relation. The repaired
function returns `depth_cap`. A cap is never treated as an empty frontier.

**Cross-edge cycle.** The old cycle detector checked whether an edge leads
to an ancestor in the BFS discovery tree. That misses directed cycles made
of cross edges. A four-node finite relation suffices:

```
1 --1--> 3 --1--> 7
1 --2--> 5 --1--> 7
7 --1--> 5
```

Nodes 5 and 7 form a cycle, although neither is the other's discovery-tree
ancestor. The original code returns `extinct`; the repair records all
edges and runs directed DFS, returning the cycle `[1,1]`. The test uses
singleton row-sets and a substituted block relation to isolate graph logic;
it is not offered as a Rule 30 diagram.

The direct ancestor/self-loop exits remain valid and retain their previous
behavior. Unexplored states caused by a depth cutoff are now explicitly
inconclusive. The new Task 3 automaton independently uses complete SCCs.

## 2. Algebraic and construction boundaries that passed

The family-seam check independently reconstructs all width-20 scalar
transitions, reproduces the exact 670-state fixed set, and obtains
`794,75,145,188,155,86,0` across the excursion and six returns. For k>=7,
`m=k+2>=9`; the last nine gap-2 blocks before the `4,4` seam and the first
six after it exist at every occurrence. In the canonical word the starting
sample is `h-28`, including k=7. Arithmetic boundary examples k=7,8,9,18,100
were replayed. Task 3 subsequently regenerated the exact frozen CNFs and
rechecked all 36 imported cone proofs with `drat-trim`, including all 11
saved finite family-seam cases, its uniform seam word, and 24 earlier
periodic-neighbour exclusions. Thus the finite exceptions and uniform
seam proof also received a fresh proof replay in this session.

The rotated Peel checker compares whole finite output tuples, including
the empty tuple at the shortest applicable input length. Its literal row
`phi(s,0)=(0,3,3,3)` closes the last-nonzero boundary used in the uniform
rank argument. The proof itself handles eventual endpoint periodicity by
deleting its finite prefix, then uses the commuting identity; no finite
census replaces that step.

High-bit elimination's affine argument includes the boundary permutation,
and its newest-cell controls allow depth zero and depth equal to the
current prefix length. The explicit n=15 witness has 16 output threes
followed by a two; the final flip is checked. The C3 graph replay includes
all returned legal rows and compares full affine triples and forced symbols;
it does not substitute the alpha-only graph.

For the image DFA, the existing membership test permitted every accepted
word at length 8 without comparing it with the produced set, via
`or n > 7`. Its loop actually generates seed length 7, so those length-8
outputs were available to check. The new audit performs exact set equality
separately for every seed length 1–7. The claim passes; the finding is a
narrow checker-coverage gap, not a false image theorem.

## 3. A uniform certificate for the image-count recurrence

Let `T` be the integer transition-count matrix of the exact 11-state
one-step image DFA, `e` its start row and `v` its accepting column. The
number of images of length-q seeds is `a(q)=e*T^(q+1)*v`.
The artifact records the complete matrix and verifies

```
e*T^j*T^2*(T^3-T^2-3*T-I)*v = 0,   j=0,...,10.
```

By Cayley-Hamilton, the same moments vanish for every j>=0. Hence
`a(q+3)=a(q+2)+3*a(q+1)+a(q)` for all q>=1. The exact initial values
`a(1),a(2),a(3)=(1,1,4)` then give
`a(q)=2*a(q-1)+a(q-2)+(-1)^(q+1)` for all q>=3.
This supplies an explicit all-length justification for the original
recurrence; checking a long finite list alone would not supply one.
It still says nothing about iterated-image mortality.

## 4. Logical seams in the four-statement report

These corrections preserve the verified S1/P1 equivalence, the proof of
S2, and the implication S4=>P1(2).

1. **q=1 is outside the q=420 residual.** A witness refuting a forced
   period at `(R,k,q)=(1,2,1)` does not refute the existential claim that
   some other ladder parameters force a period divisible by 420. It also
   does not supply a countermodel to the implication from the unresolved
   singleton S1(2). The converse from S1(2) to the ladder certificate is
   **unproved**, not established false by that witness. The witness still
   correctly distinguishes the singleton question from a particular
   stronger pointwise relaxation.
2. **The polarity matters.** At the end of §2.5, replace the claim that
   S3 and S4 both imply P1(2) by: **not-S3** and S4 imply P1(2), under the
   report's mode-(ii) certificate interpretation. S3 itself is the
   limitation direction.
3. **A bounded torus census is not a temporal-period classification.**
   PATH §11's assertion that the first clause of the quoted R7 sentence
   stands contradicts the prior rung-3 audit §6. Periods beyond the census
   and periodic neighbours without a global diagram period are not excluded.
   No proof that every q=420 escape must be aperiodic is available.
4. **Different types need maps before comparison.** `L(R,k)` consists of
   letter words; `D_lfin` consists of diagrams. Literal set-inclusion
   comparisons between these are not established by giving diagrams on
   either side. A torus tail spliced into a ladder word is not the
   projection of the unmodified torus at its seed-prefix times. The right
   wedge and the `{1,4}` example likewise do not provide the missing
   encodings or separate the S3/S4 statements. Their implication relation
   remains unresolved; the claimed two-way universe separation is withdrawn
   as written.
5. **The torus disproves sufficiency of i.o. for aperiodicity.** It does not
   prove model-theoretic independence of four fixed mathematical statements
   or independence in both directions. The appropriate conclusion is:
   S2 is proved, and that recurrence property supplies no aperiodicity
   conclusion by itself. P1's truth is not decided by the example.

These are logical coverage defects rather than new counterexamples to P1.
Correction notes are appended to the affected reports; their original text
is retained for provenance.

## 5. Reproduction and scope

```
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/seam-audit/audit.py
```

The artifact verifies all twelve source hashes in the earlier family-seam
freeze manifest, including `ladder.py` at
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.
Task 3 reuses the unchanged rung-2 Rule 90 control; Task 5 also checks its
separate affine-kernel control. No new P1 argument or averaged statistic
is proposed. The audit fixes the specified checker defects and validates
the named seams; unaudited capsule rows remain outside its coverage.
