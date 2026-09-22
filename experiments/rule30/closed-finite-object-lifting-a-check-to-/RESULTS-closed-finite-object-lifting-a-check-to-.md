# Precondition Test: Closed Finite Object Lifting Applied to "A Bound at Every Capacity" (P1)

Date: 2026-09-19  
Status: **PRECONDITIONS FAIL. THE METHOD DOES NOT APPLY TO THIS STATEMENT. "A BOUND AT EVERY CAPACITY" (P1) REMAINS CONJECTURED AND OPEN. NO LADDER STATEMENT CHANGED.**

---

## 0. Exact Precondition Check (Direct Answer)

The method **"Closed finite object lifting a check to all lengths or continuations"** (taxonomy ID `closed-finite-object-lift`) **does not apply** to the target statement:
$$\text{TARGET: For every } K \in \mathbb{N}, \text{ some finite } B(K) \text{ bounds repeats uniformly over all originals with } Q_2 \le K.$$

Per the task instructions:
> *"First answer, in writing, whether the method's preconditions hold here; if they do not, say which fails and stop. Do not adapt the method until it stops being the method."*

### Why the Preconditions Fail

The method "Closed finite object lifting a check to all lengths or continuations" is defined in the taxonomy (`pattern_taxonomy.json`:1026-1038) as:
> *"A finite automaton, product, or torus certificate closed under its transitions is exhibited, so a statement checked on the finite object holds for every length, onset or right continuation.*  
> *Mechanism: Closure replaces a census by an all-length calculation, but the finite object is closed only at a fixed width or block size, so the exclusion is uniform in length and not in the width.*  
> *Test: The document builds a closed graph or product (15,424-state subset graph, 16-state block alphabet, periodic cylinder) and states a universal conclusion for a named family, with a note on what the object does not reach."*

The method has two load-bearing preconditions:
1. **Precondition 1 (Fixed Finite State Space for the Quantified Domain):**  
   The domain of the assertion must be representable by a **single fixed finite transition object** $M$ (a finite automaton, transducer, or product graph) with a fixed, finite state set $S$, such that a finite property on $S$ (e.g., deadlock, emptiness, cycle absence, or fixed-point reachability) lifts to all instances across the quantified domain.
2. **Precondition 2 (Bounded Boundary Dimension):**  
   The class of boundary or continuation patterns must be expressible by a bounded number of parameters (e.g. length $r$ or repetition power $k$) over a fixed alphabet, allowing transition closure to wrap all continuations into a finite quotient.

**Both preconditions fail for the target statement "A bound at every capacity":**

- **Failure of Precondition 1:**  
  The target statement quantifies universally over **all integer capacities $K \in \mathbb{N}$** ($\forall K$). Because every finite original frontier $w$ of length $r$ satisfies $Q_2(w) \le 2^{2r-1} < \infty$, the union $\bigcup_{K=1}^\infty \{w : Q_2(w) \le K\}$ is the **unrestricted set of all legal auxiliary frontiers of all lengths**.  
  There is no fixed finite object that covers this domain. The exact capped-count language recognizer tracking 8 inverse-path counters requires counters saturated at $K+1$; its state space grows strictly with $K$ (e.g., 74 closed product states at $K=17$, 147 closed product states at $K=32$, and unbounded as $K \to \infty$). No finite object can represent all capacity classes simultaneously.

- **Failure of Precondition 2:**  
  The family of second bulk outputs for $Q_2 \le K$ has an **unbounded number of free repetition parameters** as $K$ increases:
  - At $K \le 17$, patterns have at most 1 parameter ($k$).
  - At $K = 18$, patterns with 2 parameters appear ($(a, b)$ across a seam).
  - Across general originals, the Canonical Binary Block Freedom Theorem (`canonical_binary_blocks.py` / `AUDIT-counting-route-scope.md` §4) proves that at length $5+5m$, there are at least $2^m$ distinct canonical two-step fibers, so the language cannot be covered by any finite union of fixed-template expressions $u_0 v_1^* u_1 \dots v_t^* u_t$.  
  A closed finite object can only lift over a 1-dimensional length or continuation parameter for a *fixed* family; it cannot close over an unbounded number of spatial parameters.

- **Non-closure at the first open step ($K=18$):**  
  Even if one attempted to adapt the method to check each capacity $K$ individually (which ceases to be a uniform proof of $\forall K$), the closed finite object method **already failed at the very next capacity, $K=18$**. As documented in `RESULTS-cap18-open-seam-lifetimes.md`, attempting to close joint state sets for the 4 open two-parameter seams hit memory caps of $2 \times 10^6$ states at depths 12–16 without closing. Explicit witnesses with $Q_2 = 18$ live to depth $N = 35, D = 22$, requiring certificate depth $d \ge 34$, which by branching rate $\approx 3\times$ per depth would require on the order of $10^{14}$ states—far beyond finite tractability.

Per instruction ("*if they do not, say which fails and stop. Do not adapt the method until it stops being the method*"), we **stop here**. The method cannot be applied to "A bound at every capacity".

---

## 1. Reproduction of All Relied-Upon Numbers and Identities from Code

Every quantity, bound, state count, and witness cited in this evaluation has been re-executed and verified directly from the repository code via `test_preconditions.py`.

### A. Capacity $K \le 17$ Language and Mortality (`capacity_language_decomposition.py`, `capacity17_mortality.py`)
- **Language classification**: Running `capacity_language_decomposition.py --cap 17` verifies:
  - Reachable coaccessible states: 19.
  - Closed product with the pattern NFA: **74 states**, **296 edges**.
  - All-length equality proved: `True`.
  - Exactly 13 patterns occur (6 singletons, 7 periodic families).
  - Only capacities **1, 2, 6, 12** occur for $Q_2 \le 17$.
  - Maximum number of independent repetition parameters: **1**.
- **Mortality and Repeat Bound**: Running `capacity17_mortality.py` checks:
  - Small originals cross-check: **10,922 originals** across lengths $r \in [1, 7]$, **68 exact non-empty fibers**.
  - Across all 13 patterns, the maximum successful updates is $N_{\max} = 24$ and maximum repeats is $D_{\max} = 14$.
  - **Sharp witness at $Q_2 = 6$**: Original $w = 20001\, 0^{1633864}$ of length $r = 1633869$ attains $N = 24, D = 14$ with tape `001000001101001100000111`.
  - Thus $B(17) = 14$ is proved and sharp for $Q_2 \le 17$.

### B. Capacity $K = 32$ / $K = 18$ Language and Two-Parameter Emergence (`capacity_language_decomposition.py`)
- Running `capacity_language_decomposition.py --cap 32` verifies:
  - Reachable coaccessible states: 40.
  - Closed product: **147 states**, **588 edges**.
  - Capacities present: **1, 2, 6, 12, 18, 20, 24**.
  - Maximum independent repetition parameters: **2**.
  - Exactly **7 patterns** first appear at $Q_2 = 18$ containing 2 free parameters $(a, b)$:
    1. `21213(13)^a 031(31)^b 3` [00]
    2. `21213(13)^a 1213(13)^b` [00] (index 8)
    3. `213(13)^a 031(31)^b 3` [00]
    4. `213(13)^a 1213(13)^b` [00] (index 15)
    5. `3031(31)^a 213(13)^b` [00] (index 23)
    6. `3031(31)^a 3031(31)^b 3` [00]
    7. `30322(2)^a 100(0)^b` [01] (index 34)

### C. Direct $Q_2 = 18$ Witness Fibers and Lifetimes (`cap18_witness_fibers.py`, `cap18_lifetime_census.py`)
Direct product-automaton matrix evaluation via `cap18_witness_fibers.py` confirms exact two-step fibers $Q_2 = 18$ for all explicit witnesses:
- **Index 8** at $(a, b) = (753, 12291)$: $Q_2 = 18$, initial tape `00`, lifetime $N = 35$, repeats $D = 22$, $\ell = 33$.
- **Index 15** at $(0, 11630084)$: $Q_2 = 18$, $N = 32, D = 20$; at $(1534, 15247338)$: $Q_2 = 18, N = 33, D = 15$.
- **Index 23** at $(533, 2533308)$: $Q_2 = 18$, $N = 33, D = 16$.
- **Index 34** at $(20, 8964344)$: $Q_2 = 18$, $N = 30, D = 15$.

### D. Canonical Binary Block Freedom Theorem (`canonical_binary_blocks.py`)
- Concatenating prefix `32001` with $m$ blocks chosen from $\{00000, 10001\}^m$:
  - All $2^m$ words are irreducible in the normal automaton and have distinct second images $32100 \prod \phi(b_i) 32$.
  - First two guarded scalars are always `01`.
  - Checked against 7 compositional controls across $m \in \{0, 1, 2\}$, producing $1, 2, 4$ distinct endpoints respectively.

---

## 2. Exhaustive and Machine-Checked Controls

The verification script `test_preconditions.py` executed three automated controls:

1. **Negative Control 1 (Failure of $K \le 17$ repeat bound at $K = 18$):**  
   - Hypothesis: The repeat bound $B(17) = 14$ holds across higher capacities.  
   - Control check: Evaluates repeat count of the certified $Q_2 = 18$ witness (Index 8 at $a=753, b=12291$).  
   - Outcome: **FAILS** with $D = 22 > 14$. Proves that repeat bounds are not uniform across capacities without separate proof per capacity.

2. **Negative Control 2 (Failure of 1-parameter closed template coverage):**  
   - Hypothesis: All capacity classes are expressible by single-parameter periodic families.  
   - Control check: Compares maximum repetition parameters in $K \le 17$ (1) against $K \le 32$ (2).  
   - Outcome: **FAILS** (7 two-parameter families at $Q_2 = 18$). Proves parameter dimensionality expands with capacity.

3. **Negative Control 3 (Failure of bounded-parameter union coverage):**  
   - Hypothesis: The set of all canonical originals can be covered by a finite union of fixed-template expressions $u_0 v_1^* \dots v_t^* u_t$.  
   - Control check: Computes number of distinct canonical fibers at length $5+5m$ for $m=2$.  
   - Outcome: **FAILS** (produces $2^2 = 4$ independent branches, growing exponentially as $2^m$, exceeding polynomial growth $(r+1)^t$ of any finite union of fixed-template expressions).

---

## 3. Required Reporting

- **STATUS:**  
  **PRECONDITIONS FAIL.** The method "Closed finite object lifting a check to all lengths or continuations" does not apply to "A bound at every capacity".

- **WHAT IS PROVED:**  
  1. The method "Closed finite object lifting a check to all lengths or continuations" cannot prove "A bound at every capacity" because its preconditions (fixed finite state space covering the quantified domain, and bounded parameter dimensionality) fail on universally quantified capacity $K \in \mathbb{N}$.
  2. All cited numerical identities and bounds ($K \le 17$: 74 states, 296 edges, $N \le 24, D \le 14$; $K = 32$: 147 states, 588 edges, 2 parameters at $Q_2 = 18$; Index 8 witness: $Q_2 = 18, N = 35, D = 22$) are independently reproduced and verified by machine check.

- **WHAT IS REFUTED:**  
  1. Refuted the applicability of method `closed-finite-object-lift` to ladder statement `A bound at every capacity` (`capacity`).
  2. Refuted the hypothesis that the capacity-17 bound $D \le 14$ bounds repeats at capacity 18 (witness has $D = 22$).
  3. Refuted the hypothesis that single-parameter closed objects suffice beyond capacity 17.

- **WHAT IS STILL OPEN:**  
  1. The target statement **"A bound at every capacity"** (P1, ladder node `capacity`): whether for every $K$, there exists finite $B(K)$ bounding repeats uniformly over all originals with $Q_2 \le K$ remains **conjectured and open**.
  2. Uniform mortality and repeat bounds for capacity 18 (the 4 open joint seams 8, 15, 23, 34 remain open).
  3. Period-two exclusion and prize problem P1.

- **WHICH LADDER STATEMENT CHANGED:**  
  **NONE.** Ladder statement **"A bound at every capacity"** (`capacity`) remains **conjectured** (unchanged).

---

## 4. Artifacts and Reproduction

All scripts, certificates, and logs are contained strictly within `experiments/rule30/closed-finite-object-lifting-a-check-to-/`:
- Audit Script: [`test_preconditions.py`](file:///Volumes/A/researchpapers/13-rule30/experiments/rule30/closed-finite-object-lifting-a-check-to-/test_preconditions.py)
- Machine Certificate: [`precondition-audit.json`](file:///Volumes/A/researchpapers/13-rule30/experiments/rule30/closed-finite-object-lifting-a-check-to-/precondition-audit.json)
- Execution Log: [`precondition-audit.log`](file:///Volumes/A/researchpapers/13-rule30/experiments/rule30/closed-finite-object-lifting-a-check-to-/precondition-audit.log)

Replay command:
```sh
cd /Volumes/A/researchpapers/13-rule30
python3 experiments/rule30/closed-finite-object-lifting-a-check-to-/test_preconditions.py
```
