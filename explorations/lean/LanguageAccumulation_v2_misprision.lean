/-!
# Human Language as an Accumulation System (ΔW) for the Distributed Human World Model (W)
## Ground-Up Rework: Lossy Encoding/Decoding, Destructive Misprision, and Bloomian Misprision

This file formalizes and proves in Lean 4 (using only core `Init`, with zero `sorry`s)
how human language operates as an accumulation system (`ΔW`) for a distributed human world
model (`W`) **even when agent-to-agent encoding and decoding are lossy and non-monotonic**.

## Core Architecture
1. **World Model Space (`InfoLattice State`)**:
   Informational containment (`le`), empty knowledge (`bot`), and collective aggregation (`sup`).
   Crucially, individual cognitive updates are **not** forced to be monotonic joins.
2. **Lossy Communication Channel (`LangChannel Agent State Msg`)**:
   Every utterance is an explicit two-stage codec:
   - `encode : Agent → State → Msg` (speaker compresses their state into a linguistic signal)
   - `decode : Agent → State → Msg → State` (listener reconstructs a new state from signal + prior state)
   Communication (`transmit`) updates only the listener; the speaker and bystanders keep their states.
3. **Three Regimes of Misprision**:
   - **Lossy (`IsLossy`)**: `¬ L.le (W speaker) w_new` — the listener fails to recover the speaker's state.
   - **Destructive (`IsDestructive`)**: `¬ L.le (W listener) w_new` — decoding overwrites/degrades prior knowledge.
   - **Generative / Bloomian (`IsBloomian`, `IsCollectivelyBloomian`)**:
     `¬ L.le w_new (L.sup (W speaker) (W listener))` (resp. `¬ L.le w_new (collective L agents W)`) —
     creative misreading synthesizes novel structure not present in the speaker, listener, or collective.
4. **Main Results**:
   - **Vulnerability (`destructive_can_shrink_collective`)**: Without distributed redundancy,
     destructive misprision *can* strictly shrink the collective world model (concrete witness).
   - **Distributed Shielding (`backedUp_shields_collective`)**: When a listener's prior state
     is distributedly backed up across the rest of the population (`IsDistributedlyBackedUp`),
     even *arbitrary destructive misprision* cannot shrink the collective world model.
   - **Bloomian Growth (`bloomian_strictly_grows_collective`)**: A collectively Bloomian
     misprision on a non-destructive or backed-up listener **strictly grows** the collective
     world model with zero external observation—even if it is simultaneously lossy and
     locally destructive.
   - **Diachronic Ratchet (`history_collective_monotonic`, `history_strictly_grows_of_bloomian`)**:
     Over arbitrary multi-step histories of external observations and lossy/misprision-prone
     communication, distributed redundancy sustains a monotonic cultural ratchet that
     permanently retains both discoveries and Bloomian innovations.
   - **Concrete Simultaneous Witness (`lossy_destructive_bloomian_grows_collective`)**:
     A concrete 3-bit, 3-agent model exhibiting lossiness, local destruction, Bloomian
     synthesis, and strict collective growth all in a single utterance.
-/

namespace LanguageAccumulation

/-! ## 1. Information Lattice (Ordering & Collective Aggregation) -/

/-- An information join-semilattice with bottom element representing empty knowledge. -/
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

/-- Strict informational growth: `a ≤ b` and `a ≠ b`. -/
def strictLe {State : Type} (L : InfoLattice State) (a b : State) : Prop :=
  L.le a b ∧ a ≠ b

section LatticeLaws

variable {State : Type} (L : InfoLattice State)

theorem strictLe_of_strictLe_le {a b c : State}
    (hab : strictLe L a b) (hbc : L.le b c) : strictLe L a c := by
  refine ⟨L.le_trans a b c hab.1 hbc, ?_⟩
  intro hac
  apply hab.2
  apply L.le_antisymm a b hab.1
  rw [hac]
  exact hbc

theorem strictLe_of_le_strictLe {a b c : State}
    (hab : L.le a b) (hbc : strictLe L b c) : strictLe L a c := by
  refine ⟨L.le_trans a b c hab hbc.1, ?_⟩
  intro hac
  apply hbc.2
  apply L.le_antisymm b c hbc.1
  rw [← hac]
  exact hab

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

end LatticeLaws

/-! ## 2. Distributed World Model & Lossy Encode/Decode Language Channel -/

/-- A linguistic channel between agents, separating speaker encoding from listener decoding.
    Neither `encode` nor `decode` is required to be lossless, faithful, or monotonic. -/
structure LangChannel (Agent State Msg : Type) where
  encode : Agent → State → Msg
  decode : Agent → State → Msg → State

section ChannelModel

variable {Agent State Msg : Type}

/-- The collective distributed world model across a finite population `agents`. -/
def collective (L : InfoLattice State) (agents : List Agent) (W : Agent → State) : State :=
  (agents.map W).foldl L.sup L.bot

theorem agent_le_collective (L : InfoLattice State) (agents : List Agent)
    (W : Agent → State) (a : Agent) (ha : a ∈ agents) :
    L.le (W a) (collective L agents W) := by
  unfold collective
  apply mem_le_foldl_sup L L.bot (agents.map W) (W a)
  induction agents with
  | nil => cases ha
  | cons x xs ih =>
    cases ha with
    | head => exact List.Mem.head (xs.map W)
    | tail _ hmem => exact List.Mem.tail (W x) (ih hmem)

theorem collective_le_of_all (L : InfoLattice State) (agents : List Agent)
    (W : Agent → State) (bound : State)
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

/-- The state produced at `listener` after receiving `speaker`'s encoded utterance. -/
def receivedState (C : LangChannel Agent State Msg)
    (speaker listener : Agent) (W : Agent → State) : State :=
  C.decode listener (W listener) (C.encode speaker (W speaker))

/-- Agent-to-agent linguistic transmission: `speaker` encodes `W speaker`, `listener`
    decodes it against `W listener`, and all other agents retain their states unchanged. -/
def transmit [DecidableEq Agent] (C : LangChannel Agent State Msg)
    (speaker listener : Agent) (W : Agent → State) : Agent → State :=
  fun a =>
    if a = listener then
      receivedState C speaker listener W
    else
      W a

/-! ## 3. Formalizing Lossiness, Destructive Misprision, and Bloomian Misprision -/

/-- Lossy transmission: the listener does not recover the speaker's full state. -/
def IsLossy (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (speaker listener : Agent) (W : Agent → State) : Prop :=
  ¬ L.le (W speaker) (receivedState C speaker listener W)

/-- Non-destructive decoding: the listener preserves all prior knowledge. -/
def IsNonDestructive (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (speaker listener : Agent) (W : Agent → State) : Prop :=
  L.le (W listener) (receivedState C speaker listener W)

/-- Destructive misprision: decoding overwrites or degrades part of the listener's prior state. -/
def IsDestructive (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (speaker listener : Agent) (W : Agent → State) : Prop :=
  ¬ IsNonDestructive L C speaker listener W

/-- Local Bloomian misprision: decoding synthesizes structure not contained in the
    join of the speaker's and listener's prior states. -/
def IsBloomian (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (speaker listener : Agent) (W : Agent → State) : Prop :=
  ¬ L.le (receivedState C speaker listener W) (L.sup (W speaker) (W listener))

/-- Collective Bloomian misprision: decoding synthesizes genuinely novel structure
    not contained anywhere in the entire population's prior collective world model. -/
def IsCollectivelyBloomian (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent) (W : Agent → State) : Prop :=
  ¬ L.le (receivedState C speaker listener W) (collective L agents W)

theorem collectivelyBloomian_implies_bloomian
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent) (W : Agent → State)
    (hs : speaker ∈ agents) (hl : listener ∈ agents)
    (hcb : IsCollectivelyBloomian L C agents speaker listener W) :
    IsBloomian L C speaker listener W := by
  intro hle
  apply hcb
  exact L.le_trans (receivedState C speaker listener W)
    (L.sup (W speaker) (W listener)) (collective L agents W) hle
    (L.sup_le (W speaker) (W listener) (collective L agents W)
      (agent_le_collective L agents W speaker hs)
      (agent_le_collective L agents W listener hl))

/-! ## 4. Distributed Redundancy & Shielding Against Destructive Misprision -/

/-- Single-agent redundancy: another agent in the population already holds at least `W listener`. -/
def IsRedundant (L : InfoLattice State) (agents : List Agent)
    (listener : Agent) (W : Agent → State) : Prop :=
  ∃ backup, backup ∈ agents ∧ backup ≠ listener ∧ L.le (W listener) (W backup)

/-- General distributed backup: `W listener` is covered collectively by the remaining agents
    in `agents` (even if no single other agent holds all of `W listener`). -/
def IsDistributedlyBackedUp (L : InfoLattice State) (agents : List Agent)
    (listener : Agent) (W : Agent → State) : Prop :=
  ∀ bound : State, (∀ a, a ∈ agents → a ≠ listener → L.le (W a) bound) →
    L.le (W listener) bound

theorem redundant_implies_backedUp (L : InfoLattice State) (agents : List Agent)
    (listener : Agent) (W : Agent → State)
    (h : IsRedundant L agents listener W) :
    IsDistributedlyBackedUp L agents listener W := by
  obtain ⟨b, hb_mem, hb_neq, hb_le⟩ := h
  intro bound hbound
  exact L.le_trans (W listener) (W b) bound hb_le (hbound b hb_mem hb_neq)

/-- **Distributed Shielding Theorem**: Even when `listener` suffers arbitrary destructive
    misprision (up to complete local amnesia), distributed backup across the remaining
    population prevents any regression in the collective world model. -/
theorem backedUp_shields_collective [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent) (W : Agent → State)
    (hback : IsDistributedlyBackedUp L agents listener W) :
    L.le (collective L agents W) (collective L agents (transmit C speaker listener W)) := by
  apply collective_le_of_all L agents W
  intro a ha
  by_cases h : a = listener
  · rw [h]
    apply hback
    intro b hb hneq
    have heq : transmit C speaker listener W b = W b := by
      rw [transmit, if_neg hneq]
    rw [← heq]
    exact agent_le_collective L agents (transmit C speaker listener W) b hb
  · have heq : transmit C speaker listener W a = W a := by
      rw [transmit, if_neg h]
    rw [← heq]
    exact agent_le_collective L agents (transmit C speaker listener W) a ha

/-- Non-destructive transmission also preserves the collective world model. -/
theorem nonDestructive_preserves_collective [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent) (W : Agent → State)
    (hnd : IsNonDestructive L C speaker listener W) :
    L.le (collective L agents W) (collective L agents (transmit C speaker listener W)) := by
  apply collective_le_of_all L agents W
  intro a ha
  by_cases h : a = listener
  · rw [h]
    have hstep : L.le (W listener) (transmit C speaker listener W listener) := by
      rw [transmit, if_pos rfl]
      exact hnd
    exact L.le_trans (W listener) (transmit C speaker listener W listener)
      (collective L agents (transmit C speaker listener W))
      hstep (agent_le_collective L agents (transmit C speaker listener W) listener (h ▸ ha))
  · have heq : transmit C speaker listener W a = W a := by
      rw [transmit, if_neg h]
    rw [← heq]
    exact agent_le_collective L agents (transmit C speaker listener W) a ha

/-- Unified shielding: either local non-destruction OR distributed backup guarantees
    collective monotonicity. -/
theorem shielded_comm_preserves_collective [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent) (W : Agent → State)
    (hshield : IsNonDestructive L C speaker listener W ∨
               IsDistributedlyBackedUp L agents listener W) :
    L.le (collective L agents W) (collective L agents (transmit C speaker listener W)) := by
  cases hshield with
  | inl hnd => exact nonDestructive_preserves_collective L C agents speaker listener W hnd
  | inr hback => exact backedUp_shields_collective L C agents speaker listener W hback

/-- **Bloomian Growth Theorem**: Whenever a shielded transmission exhibits collective
    Bloomian misprision, the collective world model **strictly grows** without any
    external observation—even if the transmission is lossy and locally destructive. -/
theorem bloomian_strictly_grows_collective [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent) (W : Agent → State)
    (hl : listener ∈ agents)
    (hshield : IsNonDestructive L C speaker listener W ∨
               IsDistributedlyBackedUp L agents listener W)
    (hbloom : IsCollectivelyBloomian L C agents speaker listener W) :
    strictLe L (collective L agents W)
               (collective L agents (transmit C speaker listener W)) := by
  refine ⟨shielded_comm_preserves_collective L C agents speaker listener W hshield, ?_⟩
  intro heq
  apply hbloom
  have hmem := agent_le_collective L agents (transmit C speaker listener W) listener hl
  rw [← heq] at hmem
  rw [transmit, if_pos rfl] at hmem
  exact hmem

/-! ## 5. Diachronic Accumulation (Multi-Step Histories & Cultural Ratchet) -/

/-- A step in the evolution of a distributed world model: either an agent-to-agent
    linguistic transmission (possibly lossy, destructive, or Bloomian) or an external
    observation integrated by an agent. -/
inductive Event (Agent State : Type) where
  | comm (speaker listener : Agent) : Event Agent State
  | observe (agent : Agent) (obs : State) : Event Agent State

/-- Execute a single event on the distributed world model `W`. -/
def step [DecidableEq Agent] (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (e : Event Agent State) (W : Agent → State) : Agent → State :=
  match e with
  | Event.comm speaker listener => transmit C speaker listener W
  | Event.observe agent obs => fun a => if a = agent then L.sup (W a) obs else W a

/-- Execute a chronological history of events. -/
def runHistory [DecidableEq Agent] (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (es : List (Event Agent State)) (W : Agent → State) : Agent → State :=
  match es with
  | [] => W
  | e :: rest => runHistory L C rest (step L C e W)

/-- A history is **distributedly shielded** if every communication step is either locally
    non-destructive or occurs at a listener whose prior state is backed up across the
    rest of the population. -/
def SafeHistory [DecidableEq Agent] (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (es : List (Event Agent State)) (W : Agent → State) : Prop :=
  match es with
  | [] => True
  | Event.observe a obs :: rest =>
      SafeHistory L C agents rest (step L C (Event.observe a obs) W)
  | Event.comm s l :: rest =>
      (IsNonDestructive L C s l W ∨ IsDistributedlyBackedUp L agents l W) ∧
      SafeHistory L C agents rest (step L C (Event.comm s l) W)

/-- A history contains at least one collectively Bloomian communication event. -/
def HasBloomianStep [DecidableEq Agent] (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (es : List (Event Agent State)) (W : Agent → State) : Prop :=
  match es with
  | [] => False
  | Event.observe a obs :: rest =>
      HasBloomianStep L C agents rest (step L C (Event.observe a obs) W)
  | Event.comm s l :: rest =>
      (l ∈ agents ∧ IsCollectivelyBloomian L C agents s l W) ∨
      HasBloomianStep L C agents rest (step L C (Event.comm s l) W)

theorem observe_preserves_collective [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (agent : Agent) (obs : State) (W : Agent → State) :
    L.le (collective L agents W)
         (collective L agents (step L C (Event.observe agent obs) W)) := by
  apply collective_le_of_all L agents W
  intro a ha
  have hstep : L.le (W a) (step L C (Event.observe agent obs) W a) := by
    dsimp only [step]
    by_cases h : a = agent
    · rw [if_pos h]
      exact L.le_sup_left (W a) obs
    · rw [if_neg h]
      exact L.le_refl (W a)
  exact L.le_trans (W a) (step L C (Event.observe agent obs) W a)
    (collective L agents (step L C (Event.observe agent obs) W))
    hstep (agent_le_collective L agents (step L C (Event.observe agent obs) W) a ha)

/-- **Diachronic Ratchet Theorem**: Across any distributedly shielded history of
    observations and lossy/misprision-prone communications, the collective world model
    never regresses. -/
theorem history_collective_monotonic [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (es : List (Event Agent State)) (W : Agent → State)
    (hsafe : SafeHistory L C agents es W) :
    L.le (collective L agents W) (collective L agents (runHistory L C es W)) := by
  induction es generalizing W with
  | nil => exact L.le_refl (collective L agents W)
  | cons e rest ih =>
    cases e with
    | observe a obs =>
      exact L.le_trans (collective L agents W)
        (collective L agents (step L C (Event.observe a obs) W))
        (collective L agents (runHistory L C rest (step L C (Event.observe a obs) W)))
        (observe_preserves_collective L C agents a obs W)
        (ih (step L C (Event.observe a obs) W) hsafe)
    | comm s l =>
      exact L.le_trans (collective L agents W)
        (collective L agents (step L C (Event.comm s l) W))
        (collective L agents (runHistory L C rest (step L C (Event.comm s l) W)))
        (shielded_comm_preserves_collective L C agents s l W hsafe.1)
        (ih (step L C (Event.comm s l) W) hsafe.2)

/-- **Permanent Retention of Innovations**: Any state synthesized at `listener ∈ agents`
    during a communication step (including a Bloomian misprision) remains permanently
    preserved in the final collective world model after any subsequent shielded history. -/
theorem innovation_permanently_retained [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (speaker listener : Agent)
    (rest : List (Event Agent State)) (W : Agent → State)
    (hl : listener ∈ agents)
    (hsafe_rest : SafeHistory L C agents rest (transmit C speaker listener W)) :
    L.le (receivedState C speaker listener W)
         (collective L agents (runHistory L C (Event.comm speaker listener :: rest) W)) := by
  have h1 : L.le (receivedState C speaker listener W)
                 (collective L agents (transmit C speaker listener W)) := by
    have hmem := agent_le_collective L agents (transmit C speaker listener W) listener hl
    rw [transmit, if_pos rfl] at hmem
    exact hmem
  have h2 := history_collective_monotonic L C agents rest (transmit C speaker listener W) hsafe_rest
  exact L.le_trans (receivedState C speaker listener W)
    (collective L agents (transmit C speaker listener W))
    (collective L agents (runHistory L C rest (transmit C speaker listener W)))
    h1 h2

/-- **Diachronic Bloomian Growth Theorem**: Any shielded history containing at least one
    collectively Bloomian communication step strictly expands the collective world model. -/
theorem history_strictly_grows_of_bloomian [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg)
    (agents : List Agent) (es : List (Event Agent State)) (W : Agent → State)
    (hsafe : SafeHistory L C agents es W)
    (hbloom : HasBloomianStep L C agents es W) :
    strictLe L (collective L agents W) (collective L agents (runHistory L C es W)) := by
  induction es generalizing W with
  | nil => cases hbloom
  | cons e rest ih =>
    cases e with
    | observe a obs =>
      exact strictLe_of_le_strictLe L
        (observe_preserves_collective L C agents a obs W)
        (ih (step L C (Event.observe a obs) W) hsafe hbloom)
    | comm s l =>
      cases hbloom with
      | inl hhere =>
        exact strictLe_of_strictLe_le L
          (bloomian_strictly_grows_collective L C agents s l W hhere.1 hsafe.1 hhere.2)
          (history_collective_monotonic L C agents rest (transmit C s l W) hsafe.2)
      | inr hlater =>
        exact strictLe_of_le_strictLe L
          (shielded_comm_preserves_collective L C agents s l W hsafe.1)
          (ih (step L C (Event.comm s l) W) hsafe.2 hlater)

end ChannelModel

/-! ## 6. Concrete Non-Vacuity Witnesses (3-Bit World Model) -/

section ConcreteWitnesses

/-- A concrete 3-proposition world model state. -/
structure Bit3 where
  b0 : Bool
  b1 : Bool
  b2 : Bool
  deriving DecidableEq

/-- A 3-agent population. -/
inductive Trio where
  | alice
  | bob
  | carol
  deriving DecidableEq

private theorem bool_eq_of_imp {x y : Bool}
    (h1 : x = true → y = true) (h2 : y = true → x = true) : x = y := by
  cases x <;> cases y
  · rfl
  · cases h2 rfl
  · cases h1 rfl
  · rfl

private theorem bool_le_or_left (x y : Bool) : x = true → (x || y) = true := by
  cases x <;> intro h
  · cases h
  · rfl

private theorem bool_le_or_right (x y : Bool) : y = true → (x || y) = true := by
  cases x <;> cases y <;> intro h
  · cases h
  · rfl
  · cases h
  · rfl

private theorem bool_or_le (x y z : Bool)
    (hx : x = true → z = true) (hy : y = true → z = true) :
    (x || y) = true → z = true := by
  cases x <;> cases y <;> intro h
  · cases h
  · exact hy rfl
  · exact hx rfl
  · exact hx rfl

def bit3Le (a b : Bit3) : Prop :=
  (a.b0 = true → b.b0 = true) ∧
  (a.b1 = true → b.b1 = true) ∧
  (a.b2 = true → b.b2 = true)

def bit3Sup (a b : Bit3) : Bit3 :=
  ⟨a.b0 || b.b0, a.b1 || b.b1, a.b2 || b.b2⟩

def Bit3Lattice : InfoLattice Bit3 where
  le := bit3Le
  bot := ⟨false, false, false⟩
  sup := bit3Sup
  le_refl a := ⟨fun h => h, fun h => h, fun h => h⟩
  le_trans _ _ _ hab hbc :=
    ⟨fun h => hbc.1 (hab.1 h), fun h => hbc.2.1 (hab.2.1 h), fun h => hbc.2.2 (hab.2.2 h)⟩
  le_antisymm a b hab hba := by
    cases a with
    | mk a0 a1 a2 =>
      cases b with
      | mk b0 b1 b2 =>
        have h0 := bool_eq_of_imp hab.1 hba.1
        have h1 := bool_eq_of_imp hab.2.1 hba.2.1
        have h2 := bool_eq_of_imp hab.2.2 hba.2.2
        rw [h0, h1, h2]
  bot_le _ := ⟨fun h => by cases h, fun h => by cases h, fun h => by cases h⟩
  le_sup_left a b :=
    ⟨bool_le_or_left a.b0 b.b0, bool_le_or_left a.b1 b.b1, bool_le_or_left a.b2 b.b2⟩
  le_sup_right a b :=
    ⟨bool_le_or_right a.b0 b.b0, bool_le_or_right a.b1 b.b1, bool_le_or_right a.b2 b.b2⟩
  sup_le a b c hac hbc :=
    ⟨bool_or_le a.b0 b.b0 c.b0 hac.1 hbc.1,
     bool_or_le a.b1 b.b1 c.b1 hac.2.1 hbc.2.1,
     bool_or_le a.b2 b.b2 c.b2 hac.2.2 hbc.2.2⟩

/-- **Concrete Witness 1 (Destructive Vulnerability Without Redundancy)**:
    When Bob holds unique knowledge (`b1`) with no backup in the population and receives
    a destructive transmission from Alice, the collective world model strictly shrinks. -/
theorem destructive_can_shrink_collective :
    ∃ (C : LangChannel Trio Bit3 Bool) (agents : List Trio) (W : Trio → Bit3),
      IsDestructive Bit3Lattice C Trio.alice Trio.bob W ∧
      ¬ Bit3Lattice.le (collective Bit3Lattice agents W)
                       (collective Bit3Lattice agents (transmit C Trio.alice Trio.bob W)) := by
  let C : LangChannel Trio Bit3 Bool :=
    { encode := fun _ s => s.b0
      decode := fun _ _ m => ⟨m, false, false⟩ }
  let agents : List Trio := [Trio.alice, Trio.bob]
  let W : Trio → Bit3 := fun a =>
    match a with
    | Trio.alice => ⟨true, false, false⟩
    | Trio.bob => ⟨false, true, false⟩
    | Trio.carol => ⟨false, false, false⟩
  refine ⟨C, agents, W, ?_, ?_⟩
  · intro hnd
    have hbad : false = true := hnd.2.1 rfl
    cases hbad
  · intro hmono
    have hbad : false = true := hmono.2.1 rfl
    cases hbad

/-- **Concrete Witness 2 (Simultaneous Lossy + Destructive + Bloomian Collective Growth)**:
    Alice encodes `{b0, b1}` through a lossy 1-bit channel (`b0` only). Bob decodes it
    against his prior `{b1}` into `{b2}`—losing Alice's `b0`, destroying his own `b1`,
    and creatively synthesizing `b2` (Bloomian misprision). Because Carol backs up `b1`,
    the collective world model strictly grows from `{b0, b1}` to `{b0, b1, b2}`. -/
theorem lossy_destructive_bloomian_grows_collective :
    ∃ (C : LangChannel Trio Bit3 Bool) (agents : List Trio) (W : Trio → Bit3),
      IsLossy Bit3Lattice C Trio.alice Trio.bob W ∧
      IsDestructive Bit3Lattice C Trio.alice Trio.bob W ∧
      IsCollectivelyBloomian Bit3Lattice C agents Trio.alice Trio.bob W ∧
      strictLe Bit3Lattice
        (collective Bit3Lattice agents W)
        (collective Bit3Lattice agents (transmit C Trio.alice Trio.bob W)) := by
  let C : LangChannel Trio Bit3 Bool :=
    { encode := fun _ s => s.b0
      decode := fun _ w m => ⟨false, false, m && w.b1⟩ }
  let agents : List Trio := [Trio.alice, Trio.bob, Trio.carol]
  let W : Trio → Bit3 := fun a =>
    match a with
    | Trio.alice => ⟨true, true, false⟩
    | Trio.bob => ⟨false, true, false⟩
    | Trio.carol => ⟨false, true, false⟩
  have hlossy : IsLossy Bit3Lattice C Trio.alice Trio.bob W := by
    intro hle
    have hbad : false = true := hle.1 rfl
    cases hbad
  have hdestr : IsDestructive Bit3Lattice C Trio.alice Trio.bob W := by
    intro hnd
    have hbad : false = true := hnd.2.1 rfl
    cases hbad
  have hbloom : IsCollectivelyBloomian Bit3Lattice C agents Trio.alice Trio.bob W := by
    intro hle
    have hbad : false = true := hle.2.2 rfl
    cases hbad
  have hback : IsDistributedlyBackedUp Bit3Lattice agents Trio.bob W := by
    apply redundant_implies_backedUp
    refine ⟨Trio.carol, ?_, ?_, ?_⟩
    · exact List.Mem.tail Trio.alice (List.Mem.tail Trio.bob (List.Mem.head []))
    · intro h; cases h
    · exact Bit3Lattice.le_refl (W Trio.bob)
  have hbob : Trio.bob ∈ agents :=
    List.Mem.tail Trio.alice (List.Mem.head [Trio.carol])
  have hgrow :=
    bloomian_strictly_grows_collective Bit3Lattice C agents Trio.alice Trio.bob W
      hbob (Or.inr hback) hbloom
  exact ⟨C, agents, W, hlossy, hdestr, hbloom, hgrow⟩

end ConcreteWitnesses

/-! ## 7. Bundled Main Theorem -/

/-- Specification of human language as a misprision-aware accumulation system (`ΔW`)
    for a distributed world model (`W`). -/
structure IsMisprisionAccumulationSystem (Agent State Msg : Type) [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg) : Prop where
  distributed_shielding :
    ∀ (agents : List Agent) (s l : Agent) (W : Agent → State),
      IsDistributedlyBackedUp L agents l W →
      L.le (collective L agents W) (collective L agents (transmit C s l W))
  bloomian_growth :
    ∀ (agents : List Agent) (s l : Agent) (W : Agent → State),
      l ∈ agents →
      (IsNonDestructive L C s l W ∨ IsDistributedlyBackedUp L agents l W) →
      IsCollectivelyBloomian L C agents s l W →
      strictLe L (collective L agents W) (collective L agents (transmit C s l W))
  diachronic_ratchet :
    ∀ (agents : List Agent) (es : List (Event Agent State)) (W : Agent → State),
      SafeHistory L C agents es W →
      L.le (collective L agents W) (collective L agents (runHistory L C es W))
  permanent_innovation_retention :
    ∀ (agents : List Agent) (s l : Agent) (rest : List (Event Agent State)) (W : Agent → State),
      l ∈ agents →
      SafeHistory L C agents rest (transmit C s l W) →
      L.le (receivedState C s l W)
           (collective L agents (runHistory L C (Event.comm s l :: rest) W))
  diachronic_bloomian_growth :
    ∀ (agents : List Agent) (es : List (Event Agent State)) (W : Agent → State),
      SafeHistory L C agents es W →
      HasBloomianStep L C agents es W →
      strictLe L (collective L agents W) (collective L agents (runHistory L C es W))

/-- **Main Theorem**: Any lossy, misprision-capable linguistic channel `C` acts as a
    distributed accumulation system (`ΔW`) for `W`—shielded from local destructive
    misprision by distributed redundancy, strictly expanded by Bloomian misprision,
    and ratcheted forward across histories. -/
theorem human_language_is_misprision_accumulation_system
    (Agent State Msg : Type) [DecidableEq Agent]
    (L : InfoLattice State) (C : LangChannel Agent State Msg) :
    IsMisprisionAccumulationSystem Agent State Msg L C where
  distributed_shielding := fun agents s l W hback =>
    backedUp_shields_collective L C agents s l W hback
  bloomian_growth := fun agents s l W hl hshield hbloom =>
    bloomian_strictly_grows_collective L C agents s l W hl hshield hbloom
  diachronic_ratchet := fun agents es W hsafe =>
    history_collective_monotonic L C agents es W hsafe
  permanent_innovation_retention := fun agents s l rest W hl hsafe =>
    innovation_permanently_retained L C agents s l rest W hl hsafe
  diachronic_bloomian_growth := fun agents es W hsafe hbloom =>
    history_strictly_grows_of_bloomian L C agents es W hsafe hbloom

end LanguageAccumulation
