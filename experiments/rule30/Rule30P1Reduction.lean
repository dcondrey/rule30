import Std.Tactic

/-!
Kernel-checked abstract shape of the two mortality edges of the P1 reduction
chain named in `docs/rule30/REFERENCE/FORMALIZATION-LEDGER.md` (2026-09-13):

* `capacity -> mortality` (ledger line 15): "Every original has finite `Q_2`;
  a repeat bound at its capacity and the survival inequality force finite
  lifetime."
* `budget -> mortality` (ledger line 16): "The repeat inequality proves
  sufficiency; finite mortality over finitely many words at a fixed length
  gives a finite maximum repeat count."

This file formalizes the pigeonhole/finiteness content both rows lean on,
not the domain-specific Rule 30 automaton. `Q_2`, the saturating counter
`capped_edge`, and its cap `K` live in `experiments/rule30/bounded_capacity_
language.py` (see `capped_edge`, `K = 8`) and `capacity_language_
decomposition.py`; matching this file's abstract `Q` and `cap` to that
automaton's actual memory-state type and its specific cap is a separate,
unfinished obligation, not claimed here. `capacity_bounds_length` proves: a
walk `w` over a finite alphabet enumerated by `states`, in which every
letter occurs at most `cap` times, has length at most `states.length * cap`
-- the exact pigeonhole step "a repeat bound at capacity forces finite
lifetime". `finite_domain_has_uniform_mortality_bound` proves the converse
packaging: a function individually finite on every element of a finite
list has a uniform bound over that list -- "finite mortality over finitely
many words ... gives a finite maximum repeat count". Neither theorem
mentions Rule 30, `caStep`, or any specific automaton; instantiating them
against the real `Q_2`/`capped_edge`/`K` and checking the survival
inequality is future work. No `sorry`, no `native_decide`, no imported
certificate; both theorems are checked to depend only on the standard
kernel axioms `propext` and `Quot.sound`.
-/

namespace Rule30P1Reduction

variable {Q : Type _} [DecidableEq Q]

def occursIn (q : Q) : List Q → Nat
  | [] => 0
  | x :: xs => (if x = q then 1 else 0) + occursIn q xs

def remove (q : Q) : List Q → List Q
  | [] => []
  | x :: xs => if x = q then remove q xs else x :: remove q xs

theorem length_eq_occursIn_add_remove (q : Q) (w : List Q) :
    w.length = occursIn q w + (remove q w).length := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
      by_cases h : x = q
      · simp only [occursIn, remove, List.length_cons, if_pos h]
        omega
      · simp only [occursIn, remove, List.length_cons, if_neg h]
        omega

theorem mem_remove (q : Q) (w : List Q) {x : Q} (hx : x ∈ remove q w) : x ∈ w := by
  induction w with
  | nil => simp only [remove] at hx; cases hx
  | cons y ys ih =>
      by_cases h : y = q
      · rw [remove, if_pos h] at hx
        exact List.mem_cons_of_mem y (ih hx)
      · rw [remove, if_neg h] at hx
        rcases List.mem_cons.mp hx with rfl | hx'
        · exact List.mem_cons_self ..
        · exact List.mem_cons_of_mem y (ih hx')

theorem ne_of_mem_remove (q : Q) (w : List Q) {x : Q} (hx : x ∈ remove q w) : x ≠ q := by
  induction w with
  | nil => simp only [remove] at hx; cases hx
  | cons y ys ih =>
      by_cases h : y = q
      · rw [remove, if_pos h] at hx
        exact ih hx
      · rw [remove, if_neg h] at hx
        rcases List.mem_cons.mp hx with rfl | hx'
        · exact h
        · exact ih hx'

theorem occursIn_remove_of_ne (p q : Q) (w : List Q) (hpq : p ≠ q) :
    occursIn p (remove q w) = occursIn p w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
      by_cases h : x = q
      · have hxp : x ≠ p := by rw [h]; exact fun hh => hpq hh.symm
        rw [remove, if_pos h, ih, occursIn, if_neg hxp]
        omega
      · rw [remove, if_neg h, occursIn, occursIn, ih]

theorem occursIn_remove_self (q : Q) (w : List Q) : occursIn q (remove q w) = 0 := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
      by_cases h : x = q
      · rw [remove, if_pos h, ih]
      · rw [remove, if_neg h, occursIn, ih, if_neg h]

theorem capacity_bounds_length (cap : Nat) :
    ∀ (states w : List Q),
      (∀ x ∈ w, x ∈ states) →
      (∀ q ∈ states, occursIn q w ≤ cap) →
      w.length ≤ states.length * cap
  | [], w, hcover, _ => by
      match w, hcover with
      | [], _ => simp
      | x :: xs, hcover => exact absurd (hcover x (List.mem_cons_self ..)) (by simp)
  | q :: rest, w, hcover, hcap => by
      have hlen := length_eq_occursIn_add_remove q w
      have hocc : occursIn q w ≤ cap := hcap q (List.mem_cons_self ..)
      have hcover' : ∀ x ∈ remove q w, x ∈ rest := by
        intro x hx
        have hxw : x ∈ w := mem_remove q w hx
        have hxne : x ≠ q := ne_of_mem_remove q w hx
        rcases List.mem_cons.mp (hcover x hxw) with rfl | h
        · exact absurd rfl hxne
        · exact h
      have hcap' : ∀ p ∈ rest, occursIn p (remove q w) ≤ cap := by
        intro p hp
        by_cases hpq : p = q
        · subst hpq
          rw [occursIn_remove_self]
          exact Nat.zero_le _
        · rw [occursIn_remove_of_ne p q w hpq]
          exact hcap p (List.mem_cons_of_mem q hp)
      have hrec := capacity_bounds_length cap rest (remove q w) hcover' hcap'
      have hmul : (q :: rest).length * cap = rest.length * cap + cap := by
        rw [List.length_cons, Nat.succ_mul]
      omega

/-- `budget -> mortality`, abstract shape (`FORMALIZATION-LEDGER.md:16`):
a function that is individually finite ("mortal") on every element of a
finite domain has a uniform finite bound over that domain. -/
def listMax : List Nat → Nat
  | [] => 0
  | x :: xs => max x (listMax xs)

theorem le_listMax (l : List Nat) : ∀ x ∈ l, x ≤ listMax l := by
  induction l with
  | nil => intro x hx; cases hx
  | cons y ys ih =>
      intro x hx
      simp only [listMax]
      rcases List.mem_cons.mp hx with rfl | hx'
      · exact Nat.le_max_left _ _
      · exact Nat.le_trans (ih x hx') (Nat.le_max_right _ _)

omit [DecidableEq Q] in
theorem finite_domain_has_uniform_mortality_bound
    (originals : List Q) (lifetime : Q → Nat) :
    ∃ bound : Nat, ∀ q ∈ originals, lifetime q ≤ bound :=
  ⟨listMax (originals.map lifetime), fun q hq =>
    le_listMax (originals.map lifetime) (lifetime q) (List.mem_map_of_mem hq)⟩

end Rule30P1Reduction

#print axioms Rule30P1Reduction.capacity_bounds_length
#print axioms Rule30P1Reduction.finite_domain_has_uniform_mortality_bound
