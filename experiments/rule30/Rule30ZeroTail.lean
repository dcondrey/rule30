import Std.Tactic

/-!
Kernel-checked partial formalization for the Rule 30 zero-tail proof.

This file deliberately separates the finite Boolean/inductive kernel from the
paper-level assembly step that derives `Classified` from an all-zero trace by
triangular uniqueness.  It proves, without axioms:

* Rule 30's local equation and left permutivity;
* arbitrary-depth propagation of the nearest discrepancy;
* the one-bit prefix-OR closed inverse formula under a first-right-one
  hypothesis;
* every Boolean identity used by the C_m one-step invariant;
* the infinite-left-tail contradiction once the classification is known.

It is not a full formalization of the zero-trace fiber theorem.
-/

abbrev Config := Int → Bool

def rule30 (l c r : Bool) : Bool := Bool.xor l (c || r)

def step (a : Config) : Config :=
  fun x => rule30 (a (x - 1)) (a x) (a (x + 1))

def evolve : Nat → Config → Config
  | 0, a => a
  | n + 1, a => step (evolve n a)

theorem rule30_equation (a : Config) (x : Int) :
    step a x = Bool.xor (a (x - 1)) (a x || a (x + 1)) := by
  rfl

theorem rule30_left_permutive (c r : Bool) :
    rule30 true c r = !rule30 false c r := by
  cases c <;> cases r <;> decide

theorem rule30_ne_of_left_ne {l₁ l₂ c r : Bool} (h : l₁ ≠ l₂) :
    rule30 l₁ c r ≠ rule30 l₂ c r := by
  cases l₁ <;> cases l₂ <;> cases c <;> cases r <;> simp_all [rule30]

/- The two rows differ at q but agree strictly to its right. -/
def RightBoundary (q : Int) (a b : Config) : Prop :=
  a q ≠ b q ∧ ∀ x, q < x → a x = b x

theorem rightBoundary_step {q : Int} {a b : Config}
    (h : RightBoundary q a b) : RightBoundary (q + 1) (step a) (step b) := by
  constructor
  · simp only [step]
    have hc : a (q + 1) = b (q + 1) := h.2 (q + 1) (by omega)
    have hr : a (q + 1 + 1) = b (q + 1 + 1) := h.2 (q + 1 + 1) (by omega)
    simpa [show q + 1 - 1 = q by omega, hc, hr] using
      (rule30_ne_of_left_ne (c := a (q + 1)) (r := a (q + 1 + 1)) h.1)
  · intro x hx
    simp only [step]
    have hl : a (x - 1) = b (x - 1) := h.2 (x - 1) (by omega)
    have hc : a x = b x := h.2 x (by omega)
    have hr : a (x + 1) = b (x + 1) := h.2 (x + 1) (by omega)
    simp [hl, hc, hr]

theorem rightBoundary_evolve (n : Nat) {q : Int} {a b : Config}
    (h : RightBoundary q a b) :
    RightBoundary (q + Int.ofNat n) (evolve n a) (evolve n b) := by
  induction n generalizing q with
  | zero =>
      have hz : Int.ofNat 0 = 0 := Int.ofNat_zero
      rw [hz, Int.add_zero]
      simpa only [evolve] using h
  | succ n ih =>
      have hs := rightBoundary_step (ih h)
      have hc : Int.ofNat (n + 1) = Int.ofNat n + 1 := Int.natCast_succ n
      rw [hc, ← Int.add_assoc]
      simpa only [evolve] using hs

/- Exact arbitrary-depth triangular/unit sensitivity. -/
theorem triangular_unit_sensitivity (n : Nat) {a b : Config}
    (h : RightBoundary (-(Int.ofNat n)) a b) :
    evolve n a 0 ≠ evolve n b 0 := by
  have hb := (rightBoundary_evolve n h).1
  have hz : -(Int.ofNat n) + Int.ofNat n = 0 := Int.add_left_neg _
  rw [hz] at hb
  exact hb

/- Recursive parity bit: false,true,false,true,... -/
def alt : Nat → Bool
  | 0 => false
  | n + 1 => !alt n

@[simp] theorem alt_zero : alt 0 = false := rfl
@[simp] theorem alt_succ (n : Nat) : alt (n + 1) = !alt n := rfl

theorem alt_add_two (n : Nat) : alt (n + 2) = alt n := by
  simp [alt]

theorem alt_odd (n : Nat) : alt (2 * n + 1) = true := by
  induction n with
  | zero => decide
  | succ n ih =>
      rw [show 2 * (n + 1) + 1 = (2 * n + 1) + 2 by omega]
      simpa [alt_add_two] using ih

/- The claimed one-state prefix-OR transducer. -/
def prefixOr (R : Nat → Bool) : Nat → Bool
  | 0 => false
  | k + 1 => prefixOr R k || R (k + 1)

def forcedLeft (R : Nat → Bool) (k : Nat) : Bool :=
  if alt k then prefixOr R k
  else R k && !prefixOr R (k - 1)

def leftPattern (m k : Nat) : Bool :=
  if k < m then false else if k = m then true else alt k

def FirstRightOne (m : Nat) (R : Nat → Bool) : Prop :=
  1 ≤ m ∧ (∀ j, j < m → R j = false) ∧ R m = true

theorem prefixOr_false_of_prefix_false {R : Nat → Bool} {k : Nat}
    (h : ∀ j, j ≤ k → R j = false) : prefixOr R k = false := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [prefixOr]
      rw [ih (fun j hj => h j (by omega)), h (k + 1) (by omega)]
      decide

theorem prefixOr_true_of_one {R : Nat → Bool} {m k : Nat}
    (hmpos : 1 ≤ m) (hmk : m ≤ k) (hm : R m = true) : prefixOr R k = true := by
  induction k with
  | zero =>
      omega
  | succ k ih =>
      by_cases hmk' : m ≤ k
      · simp [prefixOr, ih hmk']
      · have : m = k + 1 := by omega
        subst m
        simp [prefixOr, hm]

/- Complete closed formula under the quantified first-one hypothesis. -/
theorem forcedLeft_eq_leftPattern {R : Nat → Bool} {m k : Nat}
    (h : FirstRightOne m R) : forcedLeft R k = leftPattern m k := by
  by_cases hkm : k < m
  · have hp : prefixOr R k = false := prefixOr_false_of_prefix_false
        (fun j hj => h.2.1 j (by omega))
    have hr : R k = false := h.2.1 k hkm
    simp [forcedLeft, leftPattern, hkm, hp, hr]
  · by_cases hkeq : k = m
    · subst k
      have hp : prefixOr R m = true := prefixOr_true_of_one h.1 (by omega) h.2.2
      have hprev : prefixOr R (m - 1) = false := prefixOr_false_of_prefix_false
        (fun j hj => h.2.1 j (by have hmpos := h.1; omega))
      cases ha : alt m <;> simp [forcedLeft, leftPattern, hp, hprev, h.2.2, ha]
    · have hmk : m < k := by omega
      have hp : prefixOr R k = true := prefixOr_true_of_one h.1 (by omega) h.2.2
      have hp' : prefixOr R (k - 1) = true := prefixOr_true_of_one h.1 (by omega) h.2.2
      cases ha : alt k <;> simp [forcedLeft, leftPattern, hkm, hkeq, hp, hp', ha]

/- Boolean/local obligations of F(C_m) ⊆ C_(m-1), m>1. -/
theorem cm_center_descend : rule30 false false false = false := by decide
theorem cm_right_front_descend : rule30 false false true = true := by decide
theorem cm_left_front_descend : rule30 true false false = true := by decide

theorem cm_left_at_old_front (p : Bool) :
    rule30 (!p) true false = p := by
  cases p <;> decide

theorem cm_left_after_old_front (p : Bool) :
    rule30 p (!p) true = !p := by
  cases p <;> decide

theorem alternating_left_fixed (p : Bool) :
    rule30 (!p) p (!p) = p := by
  cases p <;> decide

/- Boolean/local obligations of F(C_1) ⊆ C_1, including the OR latch. -/
theorem c1_center_fixed : rule30 true false true = false := by decide
theorem c1_right_latch (tail : Bool) : rule30 false true tail = true := by
  cases tail <;> decide
theorem c1_left_fixed_at_one : rule30 false true false = true := by decide

/- A quantified tail pattern cannot be left-bounded. -/
def LeftClass (m : Nat) (a : Config) : Prop :=
  ∀ k : Nat, a (-(Int.ofNat k)) = leftPattern m k

def LeftBounded (a : Config) : Prop :=
  ∃ N : Nat, ∀ k : Nat, N < k → a (-(Int.ofNat k)) = false

theorem leftClass_not_leftBounded {m : Nat} (hm : 1 ≤ m) {a : Config}
    (hc : LeftClass m a) : ¬LeftBounded a := by
  rintro ⟨N, hN⟩
  let k := 2 * (N + m) + 1
  have hNk : N < k := by dsimp [k]; omega
  have hmk : m < k := by dsimp [k]; omega
  have hkpat : leftPattern m k = true := by
    rw [leftPattern, if_neg (by omega), if_neg (by omega)]
    exact alt_odd (N + m)
  have hzero := hN k hNk
  have hone := hc k
  rw [hkpat] at hone
  simp_all

/- Final finite-support contradiction, conditional on the exact classification
disjunction stated in the paper. -/
def RightAndLeftZero (a : Config) : Prop :=
  (∀ k : Nat, a (Int.ofNat k) = false) ∧
  (∀ k : Nat, a (-(Int.ofNat k)) = false)

def Classified (a : Config) : Prop :=
  RightAndLeftZero a ∨ ∃ m : Nat, 1 ≤ m ∧ LeftClass m a

theorem classified_leftBounded_is_zero {a : Config}
    (hc : Classified a) (hb : LeftBounded a) : RightAndLeftZero a := by
  rcases hc with hz | ⟨m, hm, hclass⟩
  · exact hz
  · exact False.elim ((leftClass_not_leftBounded hm hclass) hb)
