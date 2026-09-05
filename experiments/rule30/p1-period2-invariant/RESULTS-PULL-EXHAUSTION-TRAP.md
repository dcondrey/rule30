# Pull exhaustion trap: exact falsification

Date: 2026-09-02

Status: **FALSE.  THE TARGETED ZERO-RUN FAMILY FALSIFIES BOTH THE
EXHAUSTION TRAP AND THE UNDERLYING ABSTRACT COORDINATE-DEPTH CLAIM.**

The registered claim said that after a pull first creates a positive-root
node of reserve

```text
ceil(root/2)-pull_depth = 0,
```

no later pull succeeds.  It passed every invariant queue through length 19,
15,972 adversarial queues using a sparse list of zero-run lengths through
511, and 200,000 newly seeded random/zero-heavy queues through length 512.
Those tests contained only 28 exhaustion events.

The omitted zero-run lengths expose the failure.  For

```text
R_m = 3001 0^m 2,
```

`m=62` gives the exact successful event word

```text
CBACACBBA.
```

At time 3, a pull first creates a reserve-zero child rooted at coordinate 3.
After the intervening `A`, another pull succeeds at time 5.  Hence the
exhaustion trap is false.

At `m=382`, the successful event word is `CBACACBACA`.  Pulls occur at
times `0,3,5,8`.  The time-8 pull takes root 3 from depth two to depth three,
although `ceil(3/2)=2`.  Thus the original coordinate-depth inequality is
also false.  The orbit dies on its next attempted update; this is a finite
transient, not an immortal queue.

The exact lesson is that reserve-zero descendants do form a terminal block
in these examples, but a gap-two pull can use the reserve-one node immediately
to their left.  Long zero runs transport the phase needed to repeat this
process.  A proof cannot charge a chain only to coordinates on the left of
its initial root.

Their putative current right-edge diagonal begins `200`, while a hard-core
endpoint capable of the same initial pull forces `203`.  Therefore the
falsification does not rule out a bound on the endpoint-derived queues that
occur in the actual rank-zero reduction.

Reproduce the stored counterexamples with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_exhaustion_trap.py \
  --exact-length 3 --max-prefix-length 2 --random-per-kind 1
```
