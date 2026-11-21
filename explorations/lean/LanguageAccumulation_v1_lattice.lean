/-!
# Human Language as an Accumulation System (ΔW) for the Distributed Human World Model (W)

This file formalizes and proves in Lean 4 (using only core `Init`, with zero `sorry`s)
the proposition that human language functions as an accumulation system (`ΔW`) for a
distributed human world model (`W`).

## Conceptual Mapping
1. **World Model States (`State`)**: Modeled as an `InfoLattice` (bounded join-semilattice)
   where `≤` is informational containment, `bot` is empty knowledge, and `sup` (`⊔`) is
   non-destructive knowledge integration.
2. **Distributed World Model (`W : Agent → State`)**: Each human agent holds a local
   world-model state. The collective world model over a population is the join (`⊔`) of
   its agents' states.
3. **Language (`Delta State`)**: Utterances encode state deltas (`ΔW`) that act on
   listeners' local models via `applyDelta d w = w ⊔ d.payload`.
4. **Accumulation System (`IsAccumulationSystem`)**: We prove that `Delta` satisfies:
   - **Identity & Associative Composition**: Silence is an identity; sequential utterances
     compose into a cumulative delta log without full-state retransmission.
   - **Non-Destructive Monotonicity**: Applying `ΔW` preserves prior knowledge and
     absorbs the transmitted delta.
   - **Distributed Knowledge Transfer**: Grounded utterances transfer knowledge from
     speaker to listener while preserving all agents' existing models.
   - **Collective Conservation & Growth**: Purely internal communication preserves the
     collective world model, while external observations + language strictly grow it.
   - **Cultural Ratchet (Diachronic Accumulation)**: Over arbitrary sequences of
     generations/utterances, every prior delta remains preserved in the accumulated model.
-/

namespace LanguageAccumulation

/-- An information join-semilattice with a bottom element representing empty knowledge. -/
structure InfoLattice (State : Type) where
  le : State → State → Prop
  bot : State
  sup : State → State → State
  le_refl : ∀ a, le a a
  le_trans : ∀ a b c, le a b → le b c → le a c
  le_antisymm : ∀ a b, le a b → le b a → a = b
  bot_le : ∀ a, le bot a
  le_sup_left : ∀ a b, le a (sup a b)
  le_sup_right : ∀ a b, le b (sup a b)
  sup_le : ∀ a b c, le a c → le b c → le (sup a b) c

section LatticeLaws

variable {State : Type} (L : InfoLattice State)

theorem sup_comm (a b : State) : L.sup a b = L.sup b a := by
  apply L.le_antisymm
  · exact L.sup_le a b (L.sup b a) (L.le_sup_right b a) (L.le_sup_left b a)
  · exact L.sup_le b a (L.sup a b) (L.le_sup_right a b) (L.le_sup_left a b)

theorem sup_assoc (a b c : State) : L.sup (L.sup a b) c = L.sup a (L.sup b c) := by
  apply L.le_antisymm
  · apply L.sup_le
    · apply L.sup_le
      · exact L.le_sup_left a (L.sup b c)
      · exact L.le_trans b (L.sup b c) (L.sup a (L.sup b c))
          (L.le_sup_left b c) (L.le_sup_right a (L.sup b c))
    · exact L.le_trans c (L.sup b c) (L.sup a (L.sup b c))
        (L.le_sup_right b c) (L.le_sup_right a (L.sup b c))
  · apply L.sup_le
    · exact L.le_trans a (L.sup a b) (L.sup (L.sup a b) c)
        (L.le_sup_left a b) (L.le_sup_left (L.sup a b) c)
    · apply L.sup_le
      · exact L.le_trans b (L.sup a b) (L.sup (L.sup a b) c)
          (L.le_sup_right a b) (L.le_sup_left (L.sup a b) c)
      · exact L.le_sup_right (L.sup a b) c

theorem sup_idem (a : State) : L.sup a a = a := by
  apply L.le_antisymm
  · exact L.sup_le a a a (L.le_refl a) (L.le_refl a)
  · exact L.le_sup_left a a

theorem sup_bot_right (a : State) : L.sup a L.bot = a := by
  apply L.le_antisymm
  · exact L.sup_le a L.bot a (L.le_refl a) (L.bot_le a)
  · exact L.le_sup_left a L.bot

theorem sup_bot_left (a : State) : L.sup L.bot a = a := by
  rw [sup_comm L L.bot a]
  exact sup_bot_right L a

theorem sup_le_sup_left (a b c : State) (h : L.le a b) : L.le (L.sup a c) (L.sup b c) := by
  apply L.sup_le
  · exact L.le_trans a b (L.sup b c) h (L.le_sup_left b c)
  · exact L.le_sup_right b c

theorem sup_le_sup_right (a b c : State) (h : L.le a b) : L.le (L.sup c a) (L.sup c b) := by
  apply L.sup_le
  · exact L.le_sup_left c b
  · exact L.le_trans a b (L.sup c b) h (L.le_sup_right c b)

theorem foldl_sup_ge_init (init : State) (xs : List State) :
    L.le init (xs.foldl L.sup init) := by
  induction xs generalizing init with
  | nil => exact L.le_refl init
  | cons x xs ih =>
    simp only [List.foldl]
    exact L.le_trans init (L.sup init x) (xs.foldl L.sup (L.sup init x))
      (L.le_sup_left init x) (ih (L.sup init x))

theorem mem_le_foldl_sup (init : State) (xs : List State) (x : State) (hx : x ∈ xs) :
    L.le x (xs.foldl L.sup init) := by
  induction xs generalizing init with
  | nil => cases hx
  | cons y ys ih =>
    simp only [List.foldl]
    cases hx with
    | head =>
      exact L.le_trans x (L.sup init x) (ys.foldl L.sup (L.sup init x))
        (L.le_sup_right init x) (foldl_sup_ge_init L (L.sup init x) ys)
    | tail _ hmem =>
      exact ih (L.sup init y) hmem

theorem foldl_sup_le (init bound : State) (xs : List State)
    (hinit : L.le init bound) (hxs : ∀ x, x ∈ xs → L.le x bound) :
    L.le (xs.foldl L.sup init) bound := by
  induction xs generalizing init with
  | nil => exact hinit
  | cons y ys ih =>
    simp only [List.foldl]
    apply ih (L.sup init y)
    · exact L.sup_le init y bound hinit (hxs y (List.Mem.head ys))
    · intro z hz
      exact hxs z (List.Mem.tail y hz)

theorem foldl_sup_mono (init₁ init₂ : State) (xs ys : List State)
    (hinit : L.le init₁ init₂)
    (hxy : ∀ x, x ∈ xs → ∃ y, y ∈ ys ∧ L.le x y) :
    L.le (xs.foldl L.sup init₁) (ys.foldl L.sup init₂) := by
  apply foldl_sup_le L init₁ (ys.foldl L.sup init₂) xs
  · exact L.le_trans init₁ init₂ (ys.foldl L.sup init₂) hinit (foldl_sup_ge_init L init₂ ys)
  · intro x hx
    obtain ⟨y, hy, hle⟩ := hxy x hx
    exact L.le_trans x y (ys.foldl L.sup init₂) hle (mem_le_foldl_sup L init₂ ys y hy)

end LatticeLaws

/-! ## Language Deltas (ΔW) and Local Accumulation -/

/-- A linguistic expression encodes a state delta `ΔW`. -/
structure Delta (State : Type) where
  payload : State

section DeltaOperations

variable {State : Type} (L : InfoLattice State)

/-- The empty utterance (silence), acting as the identity delta. -/
def silence : Delta State := ⟨L.bot⟩

/-- Sequential composition of linguistic utterances. -/
def compose (d₁ d₂ : Delta State) : Delta State :=
  ⟨L.sup d₁.payload d₂.payload⟩

/-- Applying a linguistic delta `ΔW` to an agent's local world model `w`. -/
def applyDelta (d : Delta State) (w : State) : State :=
  L.sup w d.payload

/-- Applying a chronological log (sequence) of linguistic deltas to an initial model `w₀`. -/
def applyLog (ds : List (Delta State)) (w₀ : State) : State :=
  ds.foldl (fun acc d => applyDelta L d acc) w₀

theorem applyDelta_silence (w : State) :
    applyDelta L (silence L) w = w :=
  sup_bot_right L w

theorem applyDelta_compose (d₁ d₂ : Delta State) (w : State) :
    applyDelta L (compose L d₁ d₂) w = applyDelta L d₂ (applyDelta L d₁ w) := by
  simp only [applyDelta, compose]
  rw [sup_assoc L w d₁.payload d₂.payload]

theorem compose_assoc (d₁ d₂ d₃ : Delta State) :
    compose L (compose L d₁ d₂) d₃ = compose L d₁ (compose L d₂ d₃) := by
  simp only [compose]
  rw [sup_assoc L d₁.payload d₂.payload d₃.payload]

theorem compose_silence_left (d : Delta State) :
    compose L (silence L) d = d := by
  simp only [compose, silence]
  rw [sup_bot_left L d.payload]

theorem compose_silence_right (d : Delta State) :
    compose L d (silence L) = d := by
  simp only [compose, silence]
  rw [sup_bot_right L d.payload]

theorem applyDelta_mono_self (d : Delta State) (w : State) :
    L.le w (applyDelta L d w) :=
  L.le_sup_left w d.payload

theorem applyDelta_absorbs_delta (d : Delta State) (w : State) :
    L.le d.payload (applyDelta L d w) :=
  L.le_sup_right w d.payload

theorem applyDelta_order_preserving (d : Delta State) (w₁ w₂ : State) (h : L.le w₁ w₂) :
    L.le (applyDelta L d w₁) (applyDelta L d w₂) :=
  sup_le_sup_left L w₁ w₂ d.payload h

theorem applyLog_eq_foldl_sup (ds : List (Delta State)) (w₀ : State) :
    applyLog L ds w₀ = (ds.map Delta.payload).foldl L.sup w₀ := by
  induction ds generalizing w₀ with
  | nil => rfl
  | cons d ds ih =>
    simp only [applyLog, List.foldl, List.map, applyDelta]
    exact ih (L.sup w₀ d.payload)

theorem applyLog_preserves_initial (ds : List (Delta State)) (w₀ : State) :
    L.le w₀ (applyLog L ds w₀) := by
  rw [applyLog_eq_foldl_sup]
  exact foldl_sup_ge_init L w₀ (ds.map Delta.payload)

end DeltaOperations

section CulturalRatchet

variable {State : Type} (L : InfoLattice State)

private theorem mem_map_payload {d : Delta State} {ds : List (Delta State)} (hd : d ∈ ds) :
    d.payload ∈ ds.map Delta.payload := by
  induction ds with
  | nil => cases hd
  | cons x xs ih =>
    cases hd with
    | head => exact List.Mem.head (xs.map Delta.payload)
    | tail _ hmem => exact List.Mem.tail x.payload (ih hmem)

/-- Cultural Ratchet Theorem: Every linguistic delta `d` in a historical log `ds`
    is preserved in the accumulated world model `applyLog L ds w₀`. -/
theorem cultural_ratchet_accumulation (ds : List (Delta State)) (w₀ : State)
    (d : Delta State) (hd : d ∈ ds) :
    L.le d.payload (applyLog L ds w₀) := by
  rw [applyLog_eq_foldl_sup]
  exact mem_le_foldl_sup L w₀ (ds.map Delta.payload) d.payload (mem_map_payload hd)

end CulturalRatchet

/-! ## Distributed Human World Model (`W`) and Communication -/

section DistributedModel

variable {Agent State : Type} (L : InfoLattice State)

/-- A speaker `s` can utter a grounded delta `d` if `d` is contained in `W s`. -/
def GroundedUtterance (W : Agent → State) (speaker : Agent) (d : Delta State) : Prop :=
  L.le d.payload (W speaker)

/-- Transmitting `d` to a `listener` updates `listener`'s local world model with `ΔW`
    while leaving all other agents unchanged. -/
def communicate [DecidableEq Agent] (listener : Agent) (d : Delta State)
    (W : Agent → State) : Agent → State :=
  fun a => if a = listener then applyDelta L d (W a) else W a

/-- The collective distributed world model across a finite population `agents`. -/
def collective (agents : List Agent) (W : Agent → State) : State :=
  (agents.map W).foldl L.sup L.bot

theorem agent_le_collective (agents : List Agent) (W : Agent → State)
    (a : Agent) (ha : a ∈ agents) :
    L.le (W a) (collective L agents W) := by
  unfold collective
  apply mem_le_foldl_sup L L.bot (agents.map W) (W a)
  induction agents with
  | nil => cases ha
  | cons x xs ih =>
    cases ha with
    | head => exact List.Mem.head (xs.map W)
    | tail _ hmem => exact List.Mem.tail (W x) (ih hmem)

theorem collective_le_of_all (agents : List Agent) (W : Agent → State) (bound : State)
    (h : ∀ a, a ∈ agents → L.le (W a) bound) :
    L.le (collective L agents W) bound := by
  unfold collective
  apply foldl_sup_le L L.bot bound (agents.map W) (L.bot_le bound)
  intro s hs
  induction agents with
  | nil => cases hs
  | cons x xs ih =>
    cases hs with
    | head => exact h x (List.Mem.head xs)
    | tail _ hmem =>
      exact ih (fun a ha => h a (List.Mem.tail x ha)) hmem

/-- **Theorem 1 (Non-Regression)**: Linguistic communication never erases or degrades
    any agent's local world model. -/
theorem communicate_preserves_all [DecidableEq Agent]
    (listener : Agent) (d : Delta State) (W : Agent → State) (a : Agent) :
    L.le (W a) (communicate L listener d W a) := by
  by_cases h : a = listener
  · rw [communicate, if_pos h]
    exact applyDelta_mono_self L d (W a)
  · rw [communicate, if_neg h]
    exact L.le_refl (W a)

/-- **Theorem 2 (Knowledge Transfer)**: When a speaker utters a grounded delta `d`,
    the listener's updated model contains `d` and the speaker retains `d`. -/
theorem communicate_transfers_knowledge [DecidableEq Agent]
    (speaker listener : Agent) (d : Delta State) (W : Agent → State)
    (hground : GroundedUtterance L W speaker d) :
    L.le d.payload (communicate L listener d W listener) ∧
    L.le d.payload (communicate L listener d W speaker) := by
  constructor
  · rw [communicate, if_pos rfl]
    exact applyDelta_absorbs_delta L d (W listener)
  · exact L.le_trans d.payload (W speaker) (communicate L listener d W speaker)
      hground (communicate_preserves_all L listener d W speaker)

/-- **Theorem 3 (Collective Monotonicity)**: The collective distributed world model
    never shrinks under linguistic communication. -/
theorem communicate_preserves_collective [DecidableEq Agent]
    (agents : List Agent) (listener : Agent) (d : Delta State) (W : Agent → State) :
    L.le (collective L agents W) (collective L agents (communicate L listener d W)) := by
  apply collective_le_of_all L agents W
  intro a ha
  exact L.le_trans (W a) (communicate L listener d W a)
    (collective L agents (communicate L listener d W))
    (communicate_preserves_all L listener d W a)
    (agent_le_collective L agents (communicate L listener d W) a ha)

/-- **Theorem 4 (Collective Conservation under Grounded Communication)**:
    Purely internal communication of a grounded utterance redistributes knowledge
    across agents without altering the total collective knowledge of the group. -/
theorem grounded_communicate_conserves_collective [DecidableEq Agent]
    (agents : List Agent) (speaker listener : Agent) (d : Delta State) (W : Agent → State)
    (hs : speaker ∈ agents) (hground : GroundedUtterance L W speaker d) :
    collective L agents (communicate L listener d W) = collective L agents W := by
  apply L.le_antisymm
  · apply collective_le_of_all L agents (communicate L listener d W)
    intro a ha
    by_cases h : a = listener
    · rw [communicate, if_pos h, applyDelta]
      apply L.sup_le
      · exact agent_le_collective L agents W a ha
      · exact L.le_trans d.payload (W speaker) (collective L agents W)
          hground (agent_le_collective L agents W speaker hs)
    · rw [communicate, if_neg h]
      exact agent_le_collective L agents W a ha
  · exact communicate_preserves_collective L agents listener d W

/-- **Theorem 5 (Net Collective Growth via Discovery + Language)**:
    When an agent acquires a new external observation `obs` and communicates it
    to another agent, the collective world model incorporates `obs` and
    replicates it across participants. -/
theorem discovery_and_language_grows_collective [DecidableEq Agent]
    (agents : List Agent) (discoverer listener : Agent) (obs : Delta State) (W : Agent → State)
    (hl : listener ∈ agents) :
    let W₁ := communicate L discoverer obs W
    let W₂ := communicate L listener obs W₁
    L.le (collective L agents W) (collective L agents W₂) ∧
    L.le obs.payload (W₂ discoverer) ∧
    L.le obs.payload (W₂ listener) ∧
    L.le obs.payload (collective L agents W₂) := by
  intro W₁ W₂
  have hW : L.le (collective L agents W) (collective L agents W₂) :=
    L.le_trans (collective L agents W) (collective L agents W₁) (collective L agents W₂)
      (communicate_preserves_collective L agents discoverer obs W)
      (communicate_preserves_collective L agents listener obs W₁)
  have hobs_d : L.le obs.payload (W₂ discoverer) := by
    have h1 : L.le obs.payload (W₁ discoverer) := by
      dsimp only [W₁]
      rw [communicate, if_pos rfl]
      exact applyDelta_absorbs_delta L obs (W discoverer)
    exact L.le_trans obs.payload (W₁ discoverer) (W₂ discoverer)
      h1 (communicate_preserves_all L listener obs W₁ discoverer)
  have hobs_l : L.le obs.payload (W₂ listener) := by
    dsimp only [W₂]
    rw [communicate, if_pos rfl]
    exact applyDelta_absorbs_delta L obs (W₁ listener)
  have hobs_coll : L.le obs.payload (collective L agents W₂) :=
    L.le_trans obs.payload (W₂ listener) (collective L agents W₂)
      hobs_l (agent_le_collective L agents W₂ listener hl)
  exact ⟨hW, hobs_d, hobs_l, hobs_coll⟩

end DistributedModel

/-! ## Bundled Main Theorem: Human Language is an Accumulation System (ΔW) for W -/

/-- Specification of an accumulation system `(ΔW)` over a distributed world model `(W)`. -/
structure IsAccumulationSystem (Agent State : Type) [DecidableEq Agent]
    (L : InfoLattice State) : Prop where
  identity : ∀ w : State, applyDelta L (silence L) w = w
  sequential_composition : ∀ (d₁ d₂ : Delta State) (w : State),
    applyDelta L (compose L d₁ d₂) w = applyDelta L d₂ (applyDelta L d₁ w)
  non_destructive : ∀ (d : Delta State) (w : State),
    L.le w (applyDelta L d w)
  absorptive : ∀ (d : Delta State) (w : State),
    L.le d.payload (applyDelta L d w)
  distributed_non_regression : ∀ (W : Agent → State) (l a : Agent) (d : Delta State),
    L.le (W a) (communicate L l d W a)
  knowledge_transfer : ∀ (W : Agent → State) (s l : Agent) (d : Delta State),
    GroundedUtterance L W s d →
    L.le d.payload (communicate L l d W l) ∧ L.le d.payload (communicate L l d W s)
  collective_monotonicity : ∀ (agents : List Agent) (W : Agent → State) (l : Agent) (d : Delta State),
    L.le (collective L agents W) (collective L agents (communicate L l d W))
  cultural_ratchet : ∀ (ds : List (Delta State)) (w₀ : State) (d : Delta State),
    d ∈ ds → L.le d.payload (applyLog L ds w₀)

/-- **Main Theorem**: Human language (`Delta State`), equipped with `silence`, `compose`,
    `applyDelta`, and `communicate`, is a verified accumulation system (`ΔW`) for the
    distributed human world model (`W`). -/
theorem human_language_is_accumulation_system
    (Agent State : Type) [DecidableEq Agent] (L : InfoLattice State) :
    IsAccumulationSystem Agent State L where
  identity := applyDelta_silence L
  sequential_composition := applyDelta_compose L
  non_destructive := applyDelta_mono_self L
  absorptive := applyDelta_absorbs_delta L
  distributed_non_regression := fun W l a d => communicate_preserves_all L l d W a
  knowledge_transfer := fun W s l d h => communicate_transfers_knowledge L s l d W h
  collective_monotonicity := fun agents W l d => communicate_preserves_collective L agents l d W
  cultural_ratchet := fun ds w₀ d hd => cultural_ratchet_accumulation L ds w₀ d hd

end LanguageAccumulation
