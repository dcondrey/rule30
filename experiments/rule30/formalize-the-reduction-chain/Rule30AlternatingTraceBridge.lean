import Std.Tactic

/-!
Kernel-checked bridge from mortality of the auxiliary Z-frontier to the
exclusion of a nonconstant period-two centre trace (ladder edge
`mortality -> pt2`), by the alternating-trace reconstruction.

`immortalFromAlternating`: a Rule 30 row with a leftmost one whose centre
trace alternates from time zero yields a legal finite frontier that passes
every chronological guard. With the leftmost one at `-d`, a time `T0` with
`c_T0 = 0`, `p = floor((d + T0)/2)` and `q = T0 - p - 1`, the frontier after
`n` updates is read off the space-time diagram along two adjacent
anti-diagonals,
`a_k(n) = x(q + 1 + n + k, -(p + n - k))`, `b_k(n) = x(q + n + k, -(p + n - k))`,
for `0 ≤ k < p + n`. Each scan step is Rule 30 at one cell, the zero start
memory and `a_0 = 1` come from the left front, and the `n`-th guard is
Rule 30 at the single cell `(T0 + 2n + 1, -1)` given the pinned value one.
Only left-finiteness is used; the right half of the row is arbitrary.

`periodTwoExcluded_of_mortality'`: if every legal finite frontier eventually
fails a guard, no nonzero finite row has a nonconstant centre trace of period
two from time zero. An eventual period is reduced to this form by P1.1 and is
not treated here.

Control, `alternatingCenter_without_finiteSupport`: the 7-periodic row with
ones at `j ≡ 6 (mod 7)` has temporal period 4 and centre trace `0,1,0,1,...`,
so finiteness cannot be dropped.

The frontier definitions are byte-identical to those of
`Rule30SurvivalBridge.lean`, restated because a bare `lean` run cannot import
a sibling file. `Z` ignores right-realizability of the scalar tape, which only
enlarges the set of frontiers mortality must kill, so no converse is claimed.
No `sorry`, `native_decide`, added axiom or imported certificate.
-/

namespace Rule30Frontier

/-- A frontier symbol `w_i = 2 a_i + b_i`, stored as `(a_i, b_i)`, high bit first. -/
abbrev Sym := Bool × Bool

/-- A frontier is legal when it is nonempty and `a_0 = 1`. -/
def Legal : List Sym → Prop
  | [] => False
  | s :: _ => s.1 = true

/-- Scan memory `(u, v, alpha)`. One step on the symbol `(a, b)`:
`v' = v XOR (alpha OR b)`, then `u' = u XOR (v' OR a)`, and the memory becomes `(u', v', a)`. -/
def scanStep (m : Bool × Bool × Bool) (s : Sym) : Bool × Bool × Bool :=
  let v' := xor m.2.1 (m.2.2 || s.2)
  let u' := xor m.1 (v' || s.1)
  (u', v', s.1)

/-- Left-to-right scan: the emitted symbols `(u', v')` and the final memory. -/
def scan : Bool × Bool × Bool → List Sym → List Sym × (Bool × Bool × Bool)
  | m, [] => ([], m)
  | m, s :: w =>
    let m' := scanStep m s
    let r := scan m' w
    ((m'.1, m'.2.1) :: r.1, r.2)

/-- The partial update `Z`. It succeeds exactly when the final `u` and `v` agree; their common
value `s` is the terminal scalar, and the birth symbol `(1, 1 XOR s)` is appended. -/
def Z (w : List Sym) : Option (List Sym × Bool) :=
  let r := scan (false, false, false) w
  if r.2.1 = r.2.2.1 then some (r.1 ++ [(true, !r.2.2.1)], r.2.2.1) else none

/-- `run w N = some (w', tape)`: `N` successive updates all pass their guard, `w'` is the
frontier reached and `tape` lists the scalars in emission order. `none` once a guard fails. -/
def run (w : List Sym) : Nat → Option (List Sym × List Bool)
  | 0 => some (w, [])
  | n + 1 =>
    match run w n with
    | none => none
    | some (w', t) =>
      match Z w' with
      | none => none
      | some (w'', s) => some (w'', t ++ [s])

/-- `D`: the number of equal adjacent scalars in a tape. -/
def repeats : List Bool → Nat
  | a :: b :: t => (if a = b then 1 else 0) + repeats (b :: t)
  | _ => 0

/-- The high bit of the last symbol. -/
def terminalHigh (w : List Sym) : Bool :=
  match w.getLast? with
  | some s => s.1
  | none => false

/-- Formal scalar-history fields. `W j` is the scalar emitted `j` updates ago.
`F 0 = 1`, `F 1 = W`, `F d j = F (d-1) j XOR (G (d-1) j OR F (d-2) (j+1))`;
`G 0 = 1 XOR W`, `G 1 = W`, `G d j = G (d-1) j XOR (F (d-1) (j+1) OR G (d-2) (j+1))`. -/
def FG (W : Nat → Bool) : Nat → Nat → Bool × Bool
  | 0, j => (true, !W j)
  | 1, j => (W j, W j)
  | d + 2, j =>
    (xor (FG W (d + 1) j).1 ((FG W (d + 1) j).2 || (FG W d (j + 1)).1),
     xor (FG W (d + 1) j).2 ((FG W (d + 1) (j + 1)).1 || (FG W d (j + 1)).2))

/-- The window of a tape: the scalar emitted `j` updates ago, `false` beyond the tape. -/
def window (tape : List Bool) (j : Nat) : Bool := tape.reverse.getD j false

/-- The symbol at depth `d`, counted inward from the terminal end. -/
def atDepth (w : List Sym) (d : Nat) : Sym := w.reverse.getD d (false, false)

/-- Reconstruction thresholds. After `n` successful updates from a legal frontier, the high bit
at an existing depth `d` equals `F d 0` once `n ≥ 1 + floor(d/2)` and the low bit equals
`G d 0` once `n ≥ 1 + ceil(d/2)`. From an onset with terminal high bit one the thresholds are
`n ≥ ceil(d/2)` and `n ≥ 1 + floor(d/2)`. -/
def Reconstruction : Prop :=
  ∀ (w w' : List Sym) (n : Nat) (tape : List Bool), Legal w → run w n = some (w', tape) →
    ∀ d, d < w'.length →
      ((1 + d / 2 ≤ n ∨ (terminalHigh w = true ∧ (d + 1) / 2 ≤ n)) →
        (atDepth w' d).1 = (FG (window tape) d 0).1) ∧
      ((1 + (d + 1) / 2 ≤ n ∨ (terminalHigh w = true ∧ 1 + d / 2 ≤ n)) →
        (atDepth w' d).2 = (FG (window tape) d 0).2)

/-- Alternating-run bounds: a run with no repeated scalar from a legal frontier of length `a`
has length at most `a + 3`, and at most `a + 1` when the terminal high bit is one. -/
def RunBound : Prop :=
  ∀ (w w' : List Sym) (L : Nat) (tape : List Bool), Legal w → run w L = some (w', tape) →
    repeats tape = 0 →
      L ≤ w.length + 3 ∧ (terminalHigh w = true → L ≤ w.length + 1)

/-- The survival inequality `r + N + 1 ≤ 2^(D+1) (r + 2)`, and `(r + 1)` in place of `(r + 2)`
when the terminal high bit is one, on every successful prefix. -/
def Survival : Prop :=
  ∀ (w w' : List Sym) (N : Nat) (tape : List Bool), Legal w → 1 ≤ N →
    run w N = some (w', tape) →
      w.length + N + 1 ≤ 2 ^ (repeats tape + 1) * (w.length + 2) ∧
      (terminalHigh w = true → w.length + N + 1 ≤ 2 ^ (repeats tape + 1) * (w.length + 1))

/-- A repeat budget at length `r`: one `B` bounds `D` on every successful tape of every legal
frontier of length `r`. -/
def BudgetAt (r : Nat) : Prop :=
  ∃ B : Nat, ∀ (w w' : List Sym) (N : Nat) (tape : List Bool), Legal w → w.length = r →
    run w N = some (w', tape) → repeats tape ≤ B

/-- Mortality at length `r`: every legal frontier of length `r` eventually fails a guard. -/
def MortalAt (r : Nat) : Prop :=
  ∀ w : List Sym, Legal w → w.length = r → ∃ N : Nat, run w N = none

/-- Mortality: every legal finite frontier eventually fails a chronological guard. -/
def Mortality : Prop := ∀ w : List Sym, Legal w → ∃ N : Nat, run w N = none

abbrev CAConfig := Int → Bool

/-- Rule 30: `l XOR (c OR r)`. -/
def caRule (left center right : Bool) : Bool :=
  xor left (center || right)

def caStep (a : CAConfig) : CAConfig :=
  fun x => caRule (a (x - 1)) (a x) (a (x + 1))

def caEvolve : Nat → CAConfig → CAConfig
  | 0, a => a
  | t + 1, a => caStep (caEvolve t a)

/-- The centre trace `Tr_0(y)_t`. -/
def centerOf (y : CAConfig) (t : Nat) : Bool := caEvolve t y 0

def Nonzero (y : CAConfig) : Prop := ∃ j : Int, y j = true

def FiniteSupport (y : CAConfig) : Prop := ∃ R : Nat, ∀ j : Int, R < j.natAbs → y j = false

/-- A leftmost one at `-d`. Only this half of finiteness is used by the reconstruction. -/
def LeftFinite (y : CAConfig) : Prop :=
  ∃ d : Int, y (-d) = true ∧ ∀ j : Int, j < -d → y j = false

/-- A nonconstant centre trace of period two from time zero. -/
def AlternatingCenter (y : CAConfig) : Prop :=
  (∀ t : Nat, centerOf y (t + 2) = centerOf y t) ∧ centerOf y 1 ≠ centerOf y 0

/-- Alternating-trace reconstruction: a left-finite row with an alternating centre trace yields
a legal finite frontier that passes every chronological guard. -/
def ImmortalFromAlternating : Prop :=
  ∀ y : CAConfig, LeftFinite y → AlternatingCenter y →
    ∃ w : List Sym, Legal w ∧ ∀ n : Nat, run w n ≠ none

/-- Node pt2: no nonzero finite row has a nonconstant period-two centre trace. -/
def PeriodTwoExcluded : Prop :=
  ∀ y : CAConfig, Nonzero y → FiniteSupport y → ¬ AlternatingCenter y

/-! ## The alternating-trace dictionary -/

/-!
Alternating-trace reconstruction. Notation: x(t, j) = caEvolve t y j, c_t = x(t, 0).

D1 (front). Leftmost one of row 0 at -d. Then row t vanishes left of -(d+t), x(t, -(d+t)) = 1,
   and for t ≥ 1 the right neighbour x(t, -(d+t)+1) = 1. Induction on t with the rule.
D2 (pin). c_t = 1 and c_(t+1) = 0 force x(t, -1) = 1, since c_(t+1) = x(t,-1) XOR (c_t OR x(t,1)).
Dictionary. With q + 1 + p = T0, c_T0 = 0, p ≤ d + q + 1 ≤ p + 1, 1 ≤ p:
   a_k(n) = x(q + 1 + n + k, -(p + n - k)),  b_k(n) = x(q + n + k, -(p + n - k)),
   w_n = [(a_k(n), b_k(n)) | k < p + n].
D3 (scan). The scan memory before site k is
   mem n k = (x(q+1+n+k, -(p+n+2-k)), x(q+n+k, -(p+n+2-k)), x(q+n+k, -(p+n+1-k)))
   and scanStep (mem n k) (sym n k) = mem n (k+1) = (a_k(n+1), b_k(n+1), a_k(n)): two uses of the rule.
D4. mem n 0 = (0,0,0) since the three cells are strictly left of the front; a_0(n) = 1 since it is
   the front cell (d+q+1 = p) or its right neighbour at a time ≥ 1 (d+q+1 = p+1).
D5. Final memory mem n (p+n) = (x(T,-2), x(T-1,-2), x(T-1,-1)) with T = T0 + 2n.
   x(T,-1) = x(T-1,-2) XOR 1 (c_(T-1) = 1), x(T+1,-1) = x(T,-2) XOR x(T,-1) (c_T = 0),
   pin at T+1 gives x(T+1,-1) = 1, so x(T,-2) = x(T-1,-2): guard passes, and the birth symbol
   (1, !x(T-1,-2)) = (x(T+1,-1), x(T,-1)) = sym (n+1) (p+n).
-/

theorem caEvolve_succ (y : CAConfig) (t : Nat) (j : Int) :
    caEvolve (t + 1) y j
      = xor (caEvolve t y (j - 1)) (caEvolve t y j || caEvolve t y (j + 1)) := rfl

theorem rule_at (y : CAConfig) (t t' tl tc tr : Nat) (j jl jc jr : Int)
    (ht : t' = t + 1) (htl : tl = t) (htc : tc = t) (htr : tr = t)
    (hl : jl = j - 1) (hc : jc = j) (hr : jr = j + 1) :
    caEvolve t' y j = xor (caEvolve tl y jl) (caEvolve tc y jc || caEvolve tr y jr) := by
  subst ht htl htc htr hl hc hr; rfl

theorem cell_congr (y : CAConfig) (t t' : Nat) (j j' : Int) (ht : t = t') (hj : j = j') :
    caEvolve t y j = caEvolve t' y j' := by
  subst ht hj; rfl

/-- D1: the left front moves one cell left per step. -/
theorem front (y : CAConfig) (d : Int) (h1 : y (-d) = true)
    (h0 : ∀ j : Int, j < -d → y j = false) :
    ∀ t : Nat, (∀ j : Int, j < -(d + (t : Int)) → caEvolve t y j = false) ∧
      caEvolve t y (-(d + (t : Int))) = true ∧
      (1 ≤ t → caEvolve t y (-(d + (t : Int)) + 1) = true) := by
  intro t
  induction t with
  | zero =>
    refine ⟨?_, ?_, ?_⟩
    · intro j hj
      exact h0 j (by omega)
    · have e : -(d + ((0 : Nat) : Int)) = -d := by omega
      rw [e]; exact h1
    · intro h; omega
  | succ t ih =>
    obtain ⟨ihz, ih1, _⟩ := ih
    have e1 : -(d + ((t + 1 : Nat) : Int)) + 1 = -(d + (t : Int)) := by omega
    refine ⟨?_, ?_, ?_⟩
    · intro j hj
      rw [caEvolve_succ, ihz (j - 1) (by omega), ihz j (by omega), ihz (j + 1) (by omega)]
      rfl
    · rw [caEvolve_succ, ihz _ (by omega), ihz _ (by omega), e1, ih1]
      rfl
    · intro _
      rw [caEvolve_succ, e1, ih1, ihz _ (by omega)]
      simp

/-- D2: the pin. -/
theorem pin (y : CAConfig) (t : Nat) (h1 : caEvolve t y 0 = true)
    (h0 : caEvolve (t + 1) y 0 = false) : caEvolve t y (-1) = true := by
  rw [caEvolve_succ, h1] at h0
  have e : (0 : Int) - 1 = -1 := by omega
  rw [e] at h0
  revert h0
  cases caEvolve t y (-1) <;> simp

/-- An alternating centre flips at every step. -/
theorem center_flip (y : CAConfig) (h : AlternatingCenter y) :
    ∀ t : Nat, caEvolve (t + 1) y 0 = !caEvolve t y 0 := by
  obtain ⟨hper, hne⟩ := h
  have key : ∀ t : Nat, centerOf y (t + 1) ≠ centerOf y t := by
    intro t
    induction t with
    | zero => exact hne
    | succ t ih =>
      rw [hper t]
      exact fun h => ih h.symm
  intro t
  have := key t
  unfold centerOf at this
  revert this
  cases caEvolve (t + 1) y 0 <;> cases caEvolve t y 0 <;> simp

def symA (y : CAConfig) (p q n k : Nat) : Bool :=
  caEvolve (q + 1 + n + k) y (-((p : Int) + (n : Int) - (k : Int)))

def symB (y : CAConfig) (p q n k : Nat) : Bool :=
  caEvolve (q + n + k) y (-((p : Int) + (n : Int) - (k : Int)))

def sym (y : CAConfig) (p q n k : Nat) : Sym := (symA y p q n k, symB y p q n k)

def mem (y : CAConfig) (p q n k : Nat) : Bool × Bool × Bool :=
  (caEvolve (q + 1 + n + k) y (-((p : Int) + (n : Int) + 2 - (k : Int))),
   caEvolve (q + n + k) y (-((p : Int) + (n : Int) + 2 - (k : Int))),
   caEvolve (q + n + k) y (-((p : Int) + (n : Int) + 1 - (k : Int))))

def seg (f : Nat → Sym) : Nat → Nat → List Sym
  | _, 0 => []
  | k, L + 1 => f k :: seg f (k + 1) L

theorem seg_snoc (f : Nat → Sym) : ∀ (L k : Nat), seg f k (L + 1) = seg f k L ++ [f (k + L)] := by
  intro L
  induction L with
  | zero => intro k; rfl
  | succ L ih =>
    intro k
    show f k :: seg f (k + 1) (L + 1) = (f k :: seg f (k + 1) L) ++ [f (k + (L + 1))]
    rw [ih (k + 1)]
    have e : k + 1 + L = k + (L + 1) := by omega
    rw [e]; rfl

def W (y : CAConfig) (p q n : Nat) : List Sym := seg (sym y p q n) 0 (p + n)

/-- D3, one site. -/
theorem scanStep_mem (y : CAConfig) (p q n k : Nat) :
    scanStep (mem y p q n k) (sym y p q n k) = mem y p q n (k + 1) := by
  have hv : symB y p q (n + 1) k
      = xor (caEvolve (q + n + k) y (-((p : Int) + (n : Int) + 2 - (k : Int))))
          (caEvolve (q + n + k) y (-((p : Int) + (n : Int) + 1 - (k : Int)))
            || symB y p q n k) := by
    unfold symB
    exact rule_at y (q + n + k) _ _ _ _ _ _ _ _ (by omega) (by omega) (by omega) (by omega)
      (by omega) (by omega) (by omega)
  have hu : symA y p q (n + 1) k
      = xor (caEvolve (q + 1 + n + k) y (-((p : Int) + (n : Int) + 2 - (k : Int))))
          (symB y p q (n + 1) k || symA y p q n k) := by
    unfold symA symB
    exact rule_at y (q + 1 + n + k) _ _ _ _ _ _ _ _ (by omega) (by omega) (by omega) (by omega)
      (by omega) (by omega) (by omega)
  have m1 : (mem y p q n (k + 1)).1 = symA y p q (n + 1) k := by
    unfold mem symA
    exact cell_congr y _ _ _ _ (by omega) (by omega)
  have m2 : (mem y p q n (k + 1)).2.1 = symB y p q (n + 1) k := by
    unfold mem symB
    exact cell_congr y _ _ _ _ (by omega) (by omega)
  have m3 : (mem y p q n (k + 1)).2.2 = symA y p q n k := by
    unfold mem symA
    exact cell_congr y _ _ _ _ (by omega) (by omega)
  have hs : scanStep (mem y p q n k) (sym y p q n k)
      = (symA y p q (n + 1) k, symB y p q (n + 1) k, symA y p q n k) := by
    rw [hu, hv]
    rfl
  rw [hs, ← m1, ← m2, ← m3]

/-- D3: the scan correspondence from a general start site. -/
theorem scan_seg (y : CAConfig) (p q n : Nat) : ∀ (L k : Nat),
    scan (mem y p q n k) (seg (sym y p q n) k L)
      = (seg (sym y p q (n + 1)) k L, mem y p q n (k + L)) := by
  intro L
  induction L with
  | zero => intro k; rfl
  | succ L ih =>
    intro k
    show (((scanStep (mem y p q n k) (sym y p q n k)).1,
            (scanStep (mem y p q n k) (sym y p q n k)).2.1)
          :: (scan (scanStep (mem y p q n k) (sym y p q n k)) (seg (sym y p q n) (k + 1) L)).1,
          (scan (scanStep (mem y p q n k) (sym y p q n k)) (seg (sym y p q n) (k + 1) L)).2)
        = (sym y p q (n + 1) k :: seg (sym y p q (n + 1)) (k + 1) L, mem y p q n (k + (L + 1)))
    rw [scanStep_mem, ih (k + 1)]
    have e : k + 1 + L = k + (L + 1) := by omega
    rw [e]
    have m1 : (mem y p q n (k + 1)).1 = symA y p q (n + 1) k := by
      unfold mem symA
      exact cell_congr y _ _ _ _ (by omega) (by omega)
    have m2 : (mem y p q n (k + 1)).2.1 = symB y p q (n + 1) k := by
      unfold mem symB
      exact cell_congr y _ _ _ _ (by omega) (by omega)
    rw [m1, m2]
    rfl

/-- D4: the start memory at site 0 is zero, all three cells lying strictly left of the front. -/
theorem mem_zero (y : CAConfig) (d : Int) (p q : Nat) (h1 : y (-d) = true)
    (h0 : ∀ j : Int, j < -d → y j = false) (hhi : d + (q : Int) + 1 ≤ (p : Int) + 1) (n : Nat) :
    mem y p q n 0 = (false, false, false) := by
  have f1 := (front y d h1 h0 (q + 1 + n + 0)).1
  have f2 := (front y d h1 h0 (q + n + 0)).1
  unfold mem
  rw [f1 _ (by omega), f2 _ (by omega), f2 _ (by omega)]

/-- D4: the first high bit is one: the front cell, or its right neighbour at a time ≥ 1. -/
theorem symA_zero (y : CAConfig) (d : Int) (p q : Nat) (h1 : y (-d) = true)
    (h0 : ∀ j : Int, j < -d → y j = false) (hlo : (p : Int) ≤ d + (q : Int) + 1)
    (hhi : d + (q : Int) + 1 ≤ (p : Int) + 1) (n : Nat) :
    symA y p q n 0 = true := by
  have f := front y d h1 h0 (q + 1 + n + 0)
  unfold symA
  by_cases h : d + (q : Int) + 1 = (p : Int)
  · exact (cell_congr y _ _ _ _ rfl (by omega)).trans f.2.1
  · exact (cell_congr y _ _ _ _ rfl (by omega)).trans (f.2.2 (by omega))

theorem legal_W (y : CAConfig) (d : Int) (p q : Nat) (h1 : y (-d) = true)
    (h0 : ∀ j : Int, j < -d → y j = false) (hlo : (p : Int) ≤ d + (q : Int) + 1)
    (hhi : d + (q : Int) + 1 ≤ (p : Int) + 1) (hp : 1 ≤ p) (n : Nat) :
    Legal (W y p q n) := by
  unfold W
  obtain ⟨m, hm⟩ : ∃ m, p + n = m + 1 := ⟨p + n - 1, by omega⟩
  rw [hm]
  show (sym y p q n 0).1 = true
  exact symA_zero y d p q h1 h0 hlo hhi n

/-- D5: the guard identity at a time `T1` with centre values 1, 0, 1, 0 from `T1` on. -/
theorem guard (y : CAConfig) (T1 : Nat) (c1 : caEvolve T1 y 0 = true)
    (c2 : caEvolve (T1 + 1) y 0 = false) (c3 : caEvolve (T1 + 2) y 0 = true)
    (c4 : caEvolve (T1 + 3) y 0 = false) :
    caEvolve (T1 + 1) y (-2) = caEvolve T1 y (-2) ∧ caEvolve (T1 + 2) y (-1) = true ∧
      caEvolve (T1 + 1) y (-1) = !caEvolve T1 y (-2) := by
  have r1 : caEvolve (T1 + 1) y (-1)
      = xor (caEvolve T1 y (-2)) (caEvolve T1 y (-1) || caEvolve T1 y 0) :=
    rule_at y T1 _ _ _ _ _ _ _ _ rfl rfl rfl rfl (by omega) rfl (by omega)
  have r2 : caEvolve (T1 + 2) y (-1)
      = xor (caEvolve (T1 + 1) y (-2)) (caEvolve (T1 + 1) y (-1) || caEvolve (T1 + 1) y 0) :=
    rule_at y (T1 + 1) _ _ _ _ _ _ _ _ rfl rfl rfl rfl (by omega) rfl (by omega)
  have pn : caEvolve (T1 + 2) y (-1) = true := pin y (T1 + 2) c3 c4
  rw [c1] at r1
  rw [c2, pn, r1] at r2
  refine ⟨?_, pn, ?_⟩
  · revert r2
    cases caEvolve (T1 + 1) y (-2) <;> cases caEvolve T1 y (-2) <;> simp
  · rw [r1]
    cases caEvolve T1 y (-2) <;> cases caEvolve T1 y (-1) <;> rfl

theorem center_even (y : CAConfig) (flip : ∀ t : Nat, caEvolve (t + 1) y 0 = !caEvolve t y 0)
    (T0 : Nat) (hc : caEvolve T0 y 0 = false) : ∀ m : Nat, caEvolve (T0 + 2 * m) y 0 = false := by
  intro m
  induction m with
  | zero => exact hc
  | succ m ih =>
    have e : T0 + 2 * (m + 1) = T0 + 2 * m + 1 + 1 := by omega
    rw [e, flip, flip, ih]
    rfl

/-- One update: `Z w_n = some (w_(n+1), scalar)`. -/
theorem Z_W (y : CAConfig) (d : Int) (p q : Nat) (h1 : y (-d) = true)
    (h0 : ∀ j : Int, j < -d → y j = false)
    (hhi : d + (q : Int) + 1 ≤ (p : Int) + 1)
    (flip : ∀ t : Nat, caEvolve (t + 1) y 0 = !caEvolve t y 0)
    (hc : caEvolve (q + 1 + p) y 0 = false) (n : Nat) :
    Z (W y p q n) = some (W y p q (n + 1), caEvolve (q + p + 2 * n) y (-2)) := by
  have c2 : caEvolve (q + p + 2 * n + 1) y 0 = false := by
    have := center_even y flip (q + 1 + p) hc n
    exact (cell_congr y _ _ _ _ (by omega) rfl).trans this
  have c1 : caEvolve (q + p + 2 * n) y 0 = true := by
    have := flip (q + p + 2 * n)
    rw [c2] at this
    revert this
    cases caEvolve (q + p + 2 * n) y 0 <;> simp
  have c3 : caEvolve (q + p + 2 * n + 2) y 0 = true := by
    have := flip (q + p + 2 * n + 1)
    rw [c2] at this
    exact this
  have c4 : caEvolve (q + p + 2 * n + 3) y 0 = false := by
    have := flip (q + p + 2 * n + 2)
    rw [c3] at this
    exact this
  obtain ⟨g1, g2, g3⟩ := guard y (q + p + 2 * n) c1 c2 c3 c4
  have hscan := scan_seg y p q n (p + n) 0
  rw [mem_zero y d p q h1 h0 hhi n] at hscan
  have hu : (mem y p q n (0 + (p + n))).1 = caEvolve (q + p + 2 * n) y (-2) := by
    unfold mem
    exact (cell_congr y _ _ _ _ (by omega) (by omega)).trans g1
  have hv : (mem y p q n (0 + (p + n))).2.1 = caEvolve (q + p + 2 * n) y (-2) := by
    unfold mem
    exact cell_congr y _ _ _ _ (by omega) (by omega)
  have hW : W y p q (n + 1)
      = seg (sym y p q (n + 1)) 0 (p + n) ++ [(true, !caEvolve (q + p + 2 * n) y (-2))] := by
    unfold W
    have e : p + (n + 1) = (p + n) + 1 := by omega
    rw [e, seg_snoc]
    have ea : symA y p q (n + 1) (0 + (p + n)) = true := by
      unfold symA
      exact (cell_congr y _ _ _ _ (by omega) (by omega)).trans g2
    have eb : symB y p q (n + 1) (0 + (p + n)) = !caEvolve (q + p + 2 * n) y (-2) := by
      unfold symB
      exact (cell_congr y _ _ _ _ (by omega) (by omega)).trans g3
    unfold sym
    rw [ea, eb]
  unfold Z
  rw [hW]
  unfold W
  rw [hscan]
  simp only [hu, hv]
  rfl

theorem run_W (y : CAConfig) (d : Int) (p q : Nat) (h1 : y (-d) = true)
    (h0 : ∀ j : Int, j < -d → y j = false)
    (hhi : d + (q : Int) + 1 ≤ (p : Int) + 1)
    (flip : ∀ t : Nat, caEvolve (t + 1) y 0 = !caEvolve t y 0)
    (hc : caEvolve (q + 1 + p) y 0 = false) :
    ∀ n : Nat, ∃ tape : List Bool, run (W y p q 0) n = some (W y p q n, tape) := by
  intro n
  induction n with
  | zero => exact ⟨[], rfl⟩
  | succ n ih =>
    obtain ⟨tape, ht⟩ := ih
    refine ⟨tape ++ [caEvolve (q + p + 2 * n) y (-2)], ?_⟩
    show (match run (W y p q 0) n with
      | none => none
      | some (w', t) =>
        match Z w' with
        | none => none
        | some (w'', s) => some (w'', t ++ [s])) = _
    rw [ht]
    show (match Z (W y p q n) with
        | none => none
        | some (w'', s) => some (w'', tape ++ [s])) = _
    rw [Z_W y d p q h1 h0 hhi flip hc n]

theorem immortalFromAlternating : ImmortalFromAlternating := by
  intro y hL hA
  obtain ⟨d, h1, h0⟩ := hL
  have flip := center_flip y hA
  obtain ⟨T0, hT1, hT2, hc⟩ : ∃ T0 : Nat, d + 2 ≤ (T0 : Int) ∧ 2 - d ≤ (T0 : Int) ∧
      caEvolve T0 y 0 = false := by
    by_cases h : caEvolve (d.natAbs + 3) y 0 = false
    · exact ⟨d.natAbs + 3, by omega, by omega, h⟩
    · refine ⟨d.natAbs + 3 + 1, by omega, by omega, ?_⟩
      rw [flip]
      revert h
      cases caEvolve (d.natAbs + 3) y 0 <;> simp
  obtain ⟨s, hs⟩ : ∃ s : Nat, (s : Int) = d + (T0 : Int) := ⟨(d + (T0 : Int)).toNat, by omega⟩
  obtain ⟨p, hp⟩ : ∃ p : Nat, p = s / 2 := ⟨_, rfl⟩
  obtain ⟨q, hq⟩ : ∃ q : Nat, q + 1 + p = T0 := ⟨T0 - p - 1, by omega⟩
  have hp1 : 1 ≤ p := by omega
  have hlo : (p : Int) ≤ d + (q : Int) + 1 := by omega
  have hhi : d + (q : Int) + 1 ≤ (p : Int) + 1 := by omega
  have hc' : caEvolve (q + 1 + p) y 0 = false := by rw [hq]; exact hc
  refine ⟨W y p q 0, legal_W y d p q h1 h0 hlo hhi hp1 0, ?_⟩
  intro n
  obtain ⟨tape, ht⟩ := run_W y d p q h1 h0 hhi flip hc' n
  rw [ht]
  intro h
  cases h

/-! ## Packaging and the control -/

/-
(1) Leftmost one. Support inside [-R, R]. Scan j = -R, -R+1, ... : after n steps either every
cell left of -R + n is zero, or a leftmost one has been found. y j is a Bool, so each step is a
case split and no choice is used. A one at j makes the first alternative fail at
n = (j + R).toNat + 1, which leaves the leftmost one j0; take d = -j0.
-/
theorem leftmost_search (y : CAConfig) (R : Nat)
    (hR : ∀ j : Int, R < j.natAbs → y j = false) :
    ∀ n : Nat, (∀ j : Int, j < -(R : Int) + (n : Int) → y j = false) ∨
      (∃ j0 : Int, y j0 = true ∧ ∀ j : Int, j < j0 → y j = false) := by
  intro n
  induction n with
  | zero =>
    left
    intro j hj
    apply hR
    omega
  | succ n ih =>
    rcases ih with h | h
    · cases hy : y (-(R : Int) + (n : Int)) with
      | true => exact Or.inr ⟨_, hy, h⟩
      | false =>
        left
        intro j hj
        by_cases hjn : j < -(R : Int) + (n : Int)
        · exact h j hjn
        · have hje : j = -(R : Int) + (n : Int) := by omega
          rw [hje]
          exact hy
    · exact Or.inr h

theorem leftFinite_of_nonzero_finiteSupport (y : CAConfig) :
    Nonzero y → FiniteSupport y → LeftFinite y := by
  intro hnz hfs
  rcases hnz with ⟨j, hj⟩
  rcases hfs with ⟨R, hR⟩
  rcases leftmost_search y R hR ((j + (R : Int)).toNat + 1) with h | ⟨j0, h1, h2⟩
  · have hjf : y j = false := h j (by omega)
    rw [hj] at hjf
    cases hjf
  · refine ⟨-j0, ?_, ?_⟩
    · rw [Int.neg_neg]
      exact h1
    · intro k hk
      rw [Int.neg_neg] at hk
      exact h2 k hk

/-
(2) A nonzero finite row is left-finite by (1), so hI turns an alternating centre into a legal
frontier that never fails a guard; Mortality gives a failing guard. Contradiction.
-/
theorem periodTwoExcluded_of_mortality (hI : ImmortalFromAlternating) :
    Mortality → PeriodTwoExcluded := by
  intro hM y hnz hfs hac
  rcases hI y (leftFinite_of_nonzero_finiteSupport y hnz hfs) hac with ⟨w, hw, hrun⟩
  rcases hM w hw with ⟨N, hN⟩
  exact hrun N hN

/-
(3) Control without finite support. A spatially 7-periodic row is a pattern l of length 7 read
at index j mod 7. Rule 30 acts on patterns by the cyclic update stepPattern, and
caStep (fromPattern l) = fromPattern (stepPattern l). From 0000001 the patterns are
  t=0 0000001, t=1 1000011, t=2 0100110, t=3 1111101, t=4 0000001,
so the orbit has temporal period 4 and column 0 reads 0,1,0,1.
-/
def fromPattern (l : List Bool) : CAConfig := fun j => l.getD (j % 7).toNat false

def stepPattern (l : List Bool) : List Bool :=
  [caRule (l.getD 6 false) (l.getD 0 false) (l.getD 1 false),
   caRule (l.getD 0 false) (l.getD 1 false) (l.getD 2 false),
   caRule (l.getD 1 false) (l.getD 2 false) (l.getD 3 false),
   caRule (l.getD 2 false) (l.getD 3 false) (l.getD 4 false),
   caRule (l.getD 3 false) (l.getD 4 false) (l.getD 5 false),
   caRule (l.getD 4 false) (l.getD 5 false) (l.getD 6 false),
   caRule (l.getD 5 false) (l.getD 6 false) (l.getD 0 false)]

def iterPattern : Nat → List Bool → List Bool
  | 0, l => l
  | t + 1, l => stepPattern (iterPattern t l)

def seedPattern : List Bool := [false, false, false, false, false, false, true]

theorem stepPattern_getD (l : List Bool) (r : Nat) (hr : r < 7) :
    (stepPattern l).getD r false =
      caRule (l.getD ((r + 6) % 7) false) (l.getD r false) (l.getD ((r + 1) % 7) false) := by
  have hc : r = 0 ∨ r = 1 ∨ r = 2 ∨ r = 3 ∨ r = 4 ∨ r = 5 ∨ r = 6 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

theorem caStep_fromPattern (l : List Bool) :
    caStep (fromPattern l) = fromPattern (stepPattern l) := by
  funext x
  have e1 : ((x - 1) % 7).toNat = ((x % 7).toNat + 6) % 7 := by omega
  have e2 : ((x + 1) % 7).toNat = ((x % 7).toNat + 1) % 7 := by omega
  have hr : (x % 7).toNat < 7 := by omega
  show caRule (l.getD ((x - 1) % 7).toNat false) (l.getD (x % 7).toNat false)
      (l.getD ((x + 1) % 7).toNat false) = (stepPattern l).getD (x % 7).toNat false
  rw [e1, e2, stepPattern_getD l _ hr]

theorem caEvolve_fromPattern (l : List Bool) :
    ∀ t : Nat, caEvolve t (fromPattern l) = fromPattern (iterPattern t l) := by
  intro t
  induction t with
  | zero => rfl
  | succ t ih =>
    show caStep (caEvolve t (fromPattern l)) = fromPattern (stepPattern (iterPattern t l))
    rw [ih, caStep_fromPattern]

theorem caEvolve_add (a : CAConfig) (k : Nat) :
    ∀ t : Nat, caEvolve (t + k) a = caEvolve t (caEvolve k a) := by
  intro t
  induction t with
  | zero => rw [Nat.zero_add]; rfl
  | succ t ih =>
    rw [Nat.add_right_comm]
    show caStep (caEvolve (t + k) a) = caStep (caEvolve t (caEvolve k a))
    rw [ih]

theorem iterPattern_four_seed : iterPattern 4 seedPattern = seedPattern := by decide

theorem caEvolve_four_seed : caEvolve 4 (fromPattern seedPattern) = fromPattern seedPattern := by
  rw [caEvolve_fromPattern, iterPattern_four_seed]

theorem centerOf_seed_period_four (t : Nat) :
    centerOf (fromPattern seedPattern) (t + 4) = centerOf (fromPattern seedPattern) t := by
  show caEvolve (t + 4) (fromPattern seedPattern) 0 = caEvolve t (fromPattern seedPattern) 0
  rw [caEvolve_add, caEvolve_four_seed]

theorem centerOf_seed_small (t : Nat) :
    centerOf (fromPattern seedPattern) t = (iterPattern t seedPattern).getD 0 false := by
  show caEvolve t (fromPattern seedPattern) 0 = _
  rw [caEvolve_fromPattern]
  rfl

theorem seed_is_residue_six :
    fromPattern seedPattern = fun j : Int => decide (j % 7 = 6) := by
  funext x
  have hc : x % 7 = 0 ∨ x % 7 = 1 ∨ x % 7 = 2 ∨ x % 7 = 3 ∨ x % 7 = 4 ∨ x % 7 = 5 ∨
      x % 7 = 6 := by omega
  show seedPattern.getD (x % 7).toNat false = decide (x % 7 = 6)
  rcases hc with h | h | h | h | h | h | h <;> rw [h] <;> decide

theorem seed_alternating_block (t : Nat) :
    (centerOf (fromPattern seedPattern) (t + 2) = centerOf (fromPattern seedPattern) t) ∧
    (centerOf (fromPattern seedPattern) (t + 3) = centerOf (fromPattern seedPattern) (t + 1)) ∧
    (centerOf (fromPattern seedPattern) (t + 4) = centerOf (fromPattern seedPattern) (t + 2)) ∧
    (centerOf (fromPattern seedPattern) (t + 5) = centerOf (fromPattern seedPattern) (t + 3)) := by
  induction t with
  | zero =>
    refine ⟨?_, ?_, ?_, ?_⟩ <;> simp only [Nat.zero_add, centerOf_seed_small] <;> decide
  | succ t ih =>
    rcases ih with ⟨h0, h1, h2, h3⟩
    refine ⟨h1, h2, h3, ?_⟩
    have e1 : t + 1 + 5 = (t + 2) + 4 := by omega
    have e2 : t + 1 + 3 = t + 4 := by omega
    rw [e1, e2, centerOf_seed_period_four, centerOf_seed_period_four]
    exact h0

theorem seed_nonzero : Nonzero (fromPattern seedPattern) := ⟨6, by decide⟩

theorem seed_alternatingCenter : AlternatingCenter (fromPattern seedPattern) := by
  refine ⟨fun t => (seed_alternating_block t).1, ?_⟩
  simp only [centerOf_seed_small]
  decide

theorem seed_not_finiteSupport : ¬ FiniteSupport (fromPattern seedPattern) := by
  intro hfs
  rcases hfs with ⟨R, hR⟩
  have h : fromPattern seedPattern (7 * (R : Int) + 6) = false := hR _ (by omega)
  have e : (7 * (R : Int) + 6) % 7 = 6 := by omega
  have h' : seedPattern.getD ((7 * (R : Int) + 6) % 7).toNat false = false := h
  rw [e] at h'
  exact absurd h' (by decide)

theorem alternatingCenter_without_finiteSupport :
    ∃ y : CAConfig, Nonzero y ∧ AlternatingCenter y :=
  ⟨fromPattern seedPattern, seed_nonzero, seed_alternatingCenter⟩

/-- The same control with the hypothesis it drops made explicit, on the row `j % 7 = 6`. -/
theorem residue_six_control :
    Nonzero (fun j : Int => decide (j % 7 = 6)) ∧
    ¬ FiniteSupport (fun j : Int => decide (j % 7 = 6)) ∧
    AlternatingCenter (fun j : Int => decide (j % 7 = 6)) := by
  rw [← seed_is_residue_six]
  exact ⟨seed_nonzero, seed_not_finiteSupport, seed_alternatingCenter⟩

/-! ## The bridge, with its hypothesis discharged -/

/-- mortality -> pt2. -/
theorem periodTwoExcluded_of_mortality' : Mortality → PeriodTwoExcluded :=
  periodTwoExcluded_of_mortality immortalFromAlternating

end Rule30Frontier

#print axioms Rule30Frontier.immortalFromAlternating
#print axioms Rule30Frontier.leftFinite_of_nonzero_finiteSupport
#print axioms Rule30Frontier.periodTwoExcluded_of_mortality'
#print axioms Rule30Frontier.alternatingCenter_without_finiteSupport
