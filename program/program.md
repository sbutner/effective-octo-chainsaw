# The exploratory program

*v0.1 · 2026-11-21.* This document describes how to **ground, formalize, prove, extend and connect** the spine (`spine.md`). Executable units are in `data/tasks.json` (Q-*), `data/experiments.json` (E-*) and `data/claims.json` (K-*).

---

## 1. Objective and success criteria

**Objective.** One formal model of knowledge production and transmission, with three properties:
- (a) it is derived from information-theoretic first principles;
- (b) it is instantiated at the scales of reading, corpus, canon, institution and model ecosystem;
- (c) it is used to adjudicate long-standing debates, with LLMs as the experimental apparatus.

**The program succeeds when:**
1. **Core theorems are proved.** The five master relations MR1–MR5 are each proved, refuted, or bounded in at least one exact model: a finite world, or the cyclic world from outline §6.
2. **Each master relation has a decisive test.** At least one experiment per master relation has run, with code and a pass/fail verdict.
3. **Each field gets a bridge.** At least one bridge essay per field is readable by that field's specialists, with formal claims and humanistic citations matched both ways.
4. **The debates are audited.** `debates.json` states, for every debate, what is settled, what was reframed and what remains open.
5. **The data products stay valid.** `tools/validate.py` passes, and every claim used in a bridge cites checked sources.

**Failure is informative.** Each claim has a falsifier. The program counts as a failure only if it cannot say which claims fell.

---

## 2. Workstreams

### GROUND: literature and sources
- Clear the citations marked unverified or from memory, starting with those that carry evidence for K30, K31, K33, K45, K47, K50 and K54 (Q-01, Q-02).
- Fill concepts that have fewer than two sources (Q-03; `validate.py --coverage` lists 68).
- Add the missing sides of debates: poverty of the stimulus (Q-09) and historical pedagogy (Q-20).
- **Rule:** no claim enters a bridge essay on evidence that is only from memory.

### FORMALIZE: definitions before theorems
Settle these definitions in this order, because the later items depend on the earlier ones:
1. **Notation** (Q-04): one symbol table across GM, outline v1 and the spine.
2. **The independence criterion** (GM roadmap): conditional independence given ω, relaxed to a correlation bound ρ. Every closed-loop theorem uses it.
3. **Grounded information 𝒢 and its proxies:** a held-out log score on tasks scored against the world, not against text. Index it by target (GM) and by irrep (outline S24).
4. **δ_latent, δ_surface and N_e as estimators** (Q-05).
5. **Collapse.** Choose one of Schaeffer et al.'s eight definitions per theorem, and state the regime (replacement or accumulation).
6. **Sustained compression progress** 𝓛(x;R) (Q-06).
7. **Reading trajectories, not outputs** (GM's heresy-of-paraphrase revision). Needed for L7.

### PROVE: the theorem queue

Ordered by how much each result unlocks per unit of difficulty:

| # | Target | Claims | Difficulty | Tools | Task |
|---|---|---|---|---|---|
| 1 | Finite-world core | GM T1, T2 (corrected), T4.1–2, T5, C11; K10, K26 | Easy | Data-processing inequality, Fano, counting | Q-08 |
| 2 | Migration–drift for source mixtures | K31 → MR3 | Medium | Wright–Fisher, island model, generalized Jensen–Shannon divergence | Q-10 |
| 3 | Plancherel alignment; alignment inflation under collapse | OUT-S10, OUT-S25 | Easy–Medium | Harmonic analysis | HANDOFF §6.4 |
| 4 | Rogers threshold in a stateful world | K33 | Medium | Rogers 1988; Enquist 2007; drift processes | Q-11 |
| 5 | Selection identity and λ\* | GM T3 → MR2 | Hard | Proper scoring rules; branching processes | — |
| 6 | Performative decomposition is identifiable | K40 → MR4 | Medium | Performative prediction; causal identification | Q-12 |
| 7 | Precision theorem (gaslighting versus psychosis) | K54 | Medium | Precision-weighted Gaussian updates | Q-13 |
| 8 | Sustained compression progress | K45 → MR5 | Hard | Algorithmic information; reader dynamics | Q-06 |
| 9 | World models from prediction beyond HMMs | K1 | Hard | Computational mechanics; identifiability | — |
| 10 | Bounded-resource inexhaustibility | GM T7, K13 | Hard | Resource-bounded Kolmogorov complexity | — |

**Formal verification.** Port the Lean drafts to Mathlib (HANDOFF §6.2). Formalize items 1 and 2 in Lean once their paper proofs are stable. Mutual information over finite distributions may have to be defined by hand.

### EXTEND: experiments and data

Run the cheap, decisive experiments first: **E-01** (latent versus surface diversity), **E-04** (migration–drift ecosystem), **E-12** (archival tail loss versus model tail loss), **E-08** (resonance) and **E-09** (sleeping beauties). Together they test MR3 and the canon layer with public data and small models. Next come **E-02** and **E-05** (closed-loop limits; the Rogers chain), then **E-03**, **E-06**, **E-07** and **E-10**, which need corpora and annotation.

**The testbed:** the cyclic world from outline §6 (Ω = ℤ_N × seasonal phenomena). In that world 𝒢 is computable exactly, so every proxy can be calibrated there before it is used on natural text.

**Historical datasets:**
- Kestemont's medieval survival counts;
- the French Revolution debates (Barron et al.);
- HathiTrust or Gutenberg with Underwood's prestige labels;
- Constellate/JSTOR for reception histories;
- PubMed abstracts and YouTube transcripts for performativity (Kobak; Yakura).

### CONNECT: bridges between fields

One bridge per field. Each bridge translates a formal result into that field's own questions and returns the field's hard cases to the formalism.

| Field | Bridge essay | Core claims | Likely venue type |
|---|---|---|---|
| Epistemology | Closed loops, testimony and the reasoning gap | K10, K11, K33, K34, K51 | Philosophy journal |
| Literary theory | Literature as sustained compression progress; Jauss formalized | K45–K49 | Literary-theory or digital-humanities journal |
| Literary history | The canon as a transmission network | K20–K28 | Digital-humanities or cultural-analytics venue |
| Cultural evolution | Model collapse as a Rogers chain; migration–drift for culture | K30–K33 | Evolutionary human sciences |
| Science of science | Careers, exploration and sharpening | K39, K41 | Science-of-science venue |
| ML theory | Unified Channel Law; latent-diversity collapse | MR1, MR3, K30 | ML conference |
| Philosophy of language | Retrospective verification of Firth; Quine as identifiability | K3, K5 | Philosophy of language |
| Psychiatry and social epistemology | The precision mirror: gaslighting and psychosis | K54–K56 | Interdisciplinary venue |

**A meta-bridge** (Q-16): *retrospective verification* as a method. The method needs validity conditions.

**When an LLM result bears on a humanistic claim.** All four conditions must hold:
1. **The claim has been formalized,** and the formalization has been accepted by at least one specialist in the field, or offered explicitly as a reading.
2. **The LLM setup instantiates the formal model's assumptions.** In particular, it must satisfy the independence structure.
3. **Rival formalizations make different predictions.**
4. **The result holds across model families.** Otherwise it may be an artifact of one architecture.

Firth passes all four. Plato's mimesis passes 2–4 only under a stated formalization.

---

## 3. Phases and milestones

| Phase | Content | Milestone |
|---|---|---|
| **P0 Infrastructure** (done: v0.1) | Spine, data products, validator, renderer | `validate.py` exits 0 |
| **P1 Definitions** | FORMALIZE items 1–5; Q-01, Q-02 | `notation.md`; estimators specified; core citations checked |
| **P2 Exact core** | Proof queue items 1–4; E-01, E-04, E-12 | MR1 and MR3 proved in finite or cyclic worlds; first experiment verdicts |
| **P3 Dynamics** | Items 5–7; E-02, E-05, E-10 | Selection threshold λ\*; Rogers threshold v\*; performative term estimated |
| **P4 Value layer** | Items 8 and 10; E-03, E-07, E-08, E-09 | Literariness measure validated or refuted |
| **P5 Synthesis** | Bridges; the debate audit; a monograph-length treatment | Bridge essays submitted; `debates.json` audited |

---

## 4. Decisions to settle early

1. **Realism about Ω.** The spine needs some outside to the text for 𝒢 to be defined. Adopt *minimal realism*: some evidence channels are conditionally independent of the corpus given Ω. State the strong-textualist alternative as a falsifier rather than ignoring it.
2. **The unit of selection.** Choose between forms (texts), readings (interpretations) and positions (camps). GM C11 favors forms for 𝒢. The canon layer needs all three.
3. **The definition of collapse per theorem.** Pick from Schaeffer et al.'s eight.
4. **How strong the humanistic claims should be.** Present formalizations as *readings* of Jauss, Heidegger and the others, not as their meaning. Invite specialists to contest them.
5. **One document or many.** Should GM and outline v1 merge into the spine or stay as sub-programs? (HANDOFF §8.) Recommendation: keep them as sub-programs. The spine indexes them, and `claims.json` links IDs across them.

---

## 5. Risk register

| Risk | Consequence | Mitigation |
|---|---|---|
| Analogy without mechanism ("collapse" as metaphor) | Bridges get dismissed by specialists | Every analogy must name its formal correspondence and its falsifier in `claims.json` |
| False precision (MI as "meaning") | Category error | The spine claims 𝒢 is necessary, never sufficient, for meaning (spine §5) |
| Hallucinated or drifted citations | Credibility loss | Status field; Q-01/Q-02; the "no from-memory evidence in bridges" rule |
| The definitions problem in the collapse literature | The spine's claims become ambiguous | Fix one definition per theorem (decision 3) |
| Nostalgia: the high-cost filter was never neutral | The program reads as an argument for gatekeeping | Keep the canon layer explicit about whose value function bore *c* (K20) |
| Romanticizing madness | Harm and loss of credibility | K50 and K54 are structural claims; that caution belongs in every bridge |
| Scope creep | Nothing gets proved | The phase gates: no P4 work before the P2 milestones |

---

## 6. How agents should use this program

See `AGENTS.md`. In short:
1. Pick the highest-priority open task in `data/tasks.json` whose inputs exist.
2. Work it.
3. Update the JSON. Never edit the generated `.md` views.
4. Run `tools/validate.py`, then `tools/render.py`.
5. Append a line to the task's `log`.
6. Commit with the task ID in the message.
