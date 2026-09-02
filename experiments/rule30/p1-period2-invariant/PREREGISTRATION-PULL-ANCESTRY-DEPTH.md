# Preregistration: pull-ancestry depth

Date: 2026-09-01

Status: **FROZEN AFTER DISCOVERY THROUGH LENGTH 18 AND BEFORE THE
LENGTH-19/LONG-RANDOM HELD-OUT RUN.**

## 1. Parent forest

Give every initial queue coordinate its own root node.  On each successful
update, attach the newly appended boundary coordinate to the coordinate of
the proved rightmost colex pivot.  Label the new edge by the update type:

```text
A: retreat,
B: nonretreat with source ending in 1,
C: pull with source ending in 2.
```

The **pull-depth** of a node is the number of `C` edges on its unique path to
the initial row.  Its **root** is the initial coordinate at the end of that
path.

If the initial queue is `R`, let

```text
F_R(r) = number of positions s<=r such that
         R_s=1, or R_s=0 and R_(s-1)!=0.             (1)
```

Thus `F_R(r)` counts nonleading `1` cells and maximal-zero-run starts in the
initial prefix through `r`.

## 2. Discovery boundary

The following claim was checked on every invariant normalized queue through
length 18 (2,417,975 queues total):

> **Pull-chain feature bound.**  Every pull node with root `r` and pull-depth
> `h` satisfies `h<=F_R(r)`.                          (2)

This discovery reused the exact queue iterator but introduced the parent
forest and pull-depth statistic only after the pull-ray work.  No queue of
length 19 or longer was inspected under (2) before this registration.

The claim is weaker than origin-prefix Hall.  It compares only pulls nested
on one parent chain; it does not sort or inject all pull origins globally.

## 3. Frozen held-out test

The unchanged test will use:

- every invariant queue of length 19 in both tail modes;
- 50,000 independently seeded random invariant queues per tail at lengths
  `24,32,48,64,96`; and
- 50,000 independently seeded sparse invariant queues per tail at lengths
  `24,32,48,64,96,128`.

The random generator seed is `30133`.  Every orbit cap is 1,000 successful
updates.  Any cap hit is reported and is not a pass.  The first violation of
(2), including the complete parent chain, is printed.

## 4. Algebraic temporal claim

Independently of (2), the parent forest should prove the following exact
all-length statement.  Write the successful pull times as
`t_1<t_2<...` and their pull-depths as `h_1,h_2,...`, taking missing initial
parent depths to be zero.  Pulls are separated by at least two updates.  For
every stabilized pull after the first,

```text
t_j-t_(j-1) >= 3  => h_j=h_(j-1)+1,
t_j-t_(j-1) =  2  => h_j=h_(j-2)+1,                 (3)
```

where `h_0=0`.  Consequently

```text
h_j >= ceil(j/2),       #pulls <= 2 max_j h_j.       (4)
```

Equation (3) must be proved from the already exact facts that `A/B` pivots
are terminal and every post-retreat `C` pivot is third-last.  A bounded event
word census is not the proof.

## 5. Consequence if (2) is proved

Equations (2) and (4) give, for an initial queue of length `N`,

```text
#pulls <= 2 max_r F_R(r) <= 2N.                      (5)
```

The proved retreat--productive-pull pairing then bounds retreats as well.
Thus every finite queue has finitely many retreats.  An immortal remainder
would have an eventually-`2` endpoint and is excluded by the proved dyadic
exceptional separator.  This would close the constant-tail and rank-zero
separators and exclude a nonconstant period-two center trace.

Finite held-out success will not prove (2).  The intended proof target is a
single-chain induction: show that each nested `C` edge crosses a new initial
feature start before the ancestry path can return to the same root.

