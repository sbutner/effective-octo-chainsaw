# Handoff

*Last updated 2026-11-22. Branch: `claude/ecstatic-albattani-urj2dx`.*

## 0. Current state: start at [`program/`](program/README.md)

The project is **a formal theory of knowledge production and transmission**, running from information-theoretic first principles through archives and literary canons to LLM ecosystems. LLMs serve as an apparatus for retrospectively verifying long-standing claims in other fields; Firth's distributional hypothesis is the model case. The documents in `explorations/` are components of that spine:

| Document | Role in the spine |
|---|---|
| GM | Selection core |
| Outline v1 | Symmetric sector |
| *One Selection Law* | Behavior stage |
| Lean drafts | Lattice skeleton |

Where things are:

- **The theory and the plan.** [`program/spine.md`](program/spine.md) (layers L0–L8) and [`program/program.md`](program/program.md) (workstreams, proof queue, phases, risks).
- **Canonical data.** `program/data/*.json`: 46 claims and 5 master relations, 131 concepts, 196 references, 21 debates, 12 experiments, 43 phenomena and 24 tasks.
- **The harness.** [`program/harness.md`](program/harness.md) is the spec. Mechanical checks live in `program/checks/`, their verdicts in `program/ledger/`, and the derived tiers in [`program/claims.md`](program/claims.md). `program/tools/validate.py` is the gate, and the pre-commit hook runs it.
- **The research loop.** [`.claude/skills/research-loop/SKILL.md`](.claude/skills/research-loop/SKILL.md): pick a task, write checks, run them, record failures, gate, commit.
- **Background.** [`program/tooling.md`](program/tooling.md) reviews AI Scientist, co-scientist, co-mathematician and AlphaGeometry.

**What is established.** PSITIP and exact witnesses (`program/checks/info_core.py`) prove GM T2, the T4.1 inequality, corrected GM T4.2, OUT-S26 and MR1, and refute GM T4.2 as written. T4.1's hypotheses are unused, and MR1's verifier term and S26's channel independence are load-bearing. The matching status changes in `claims.json` await review (findings: [`program/checks/info_core.md`](program/checks/info_core.md)).

**Next:** follow `program/data/tasks.json`, highest priority first. Q-08 (finite-world proofs) is the first full run of the research loop. Q-24 clears the protocol debt the strict gate found. Sections 1–8 below still describe the sub-programs.

## 1. What this project is

The project is a mathematical research program about how world structure gets into language and into models trained on language. It started from informal notes on language (sensoria, misperception, embeddings, cants, nuance, audience models) and a hunch:

- the geometry of embeddings comes from the statistics of real-world behavior;
- speakers and listeners hold separate but mutually intelligible language models;
- language accumulates world models.

The task was to formalize this enough to connect two results:

- **Karkada et al. (2026):** symmetry in co-occurrence statistics forces the geometry of representations;
- **the Platonic Representation Hypothesis (PRH; Huh et al. 2024):** models converge toward a shared statistical model of reality.

There are now three linked documents in [`explorations/`](explorations/README.md):

1. **Grounded Misprision (GM)** is the parent program. It is a theory of the corpus as a *process*: misreading is unavoidable; selection against independent evidence decides whether misreading helps or harms; closed loops cannot gain grounded information.
2. **Symmetry, Geometry, Convergence (outline v1)** covers the *state* side: on word families with a group symmetry, PRH-style convergence becomes a theorem. It adds joint results with GM, the main one being that *convergence is not grounding*.
3. **One Selection Law** is a four-stage synthesis (world → corpus → geometry → behavior). It names five seams in GM and proposes the "Unified Channel Law."

## 2. Current state

| Item | State |
|---|---|
| Outline v1 | Done. Checked against the full texts of arXiv:2602.15029v3 (Karkada et al.), 2610.00647v1 (Storan, Tolias & Miolane) and 2405.07987 (Huh et al.). Every result S1–S31 is tagged Known, Implicit, New, Conjecture or Test |
| GM program | Author draft, unchanged. Proposal only; no proofs |
| One Selection Law | Author-supplied. Added unchanged. Its citations have **not** been checked in this session (see §5) |
| Lean files | Two core-only drafts. **Not compiled in this session**: there is no Lean toolchain in this container. Both claim zero `sorry`s |
| Proofs | GM T2, T4.1 (inequality), T4.2 (refuted as written; corrected version proved), OUT-S26 and MR1 are mechanically checked; see `program/claims.md`. Everything else beyond the cited theorems is a target |
| Experiments | None run |

## 3. The core claims, and where they live

- **Symmetry gives geometry for one model.** This is published (Karkada; Storan). Outline S5–S6.
- **Same shape across objectives, agents and modalities, with closed-form alignment.** New targets. Outline S2, S9–S15.
  - Alignment is a Plancherel inner product of the two spectra (S10).
  - The alignment ceiling is computable; this answers the PRH's question of what a score like 0.16 means.
  - Bijectivity is not needed (S14).
- **Theory for deep networks.** The exchangeability argument (S7) addresses the stated limitation of both papers: their theorems cover word embeddings only.
- **Convergence ≠ grounding.** Joint with GM.
  - Collapse acts as a low-pass filter, which *raises* CKA and mutual-$k$NN while lowering grounded information (S22, S25).
  - Alignment is evidence about the world only across training channels that are conditionally independent given the world (S26).
- **Grounded information indexed by irrep** (S24). Explicit content is the closure of the resolved irreps under tensor products (S30). Together these give GM's "closure operator" and a model of the Lean `InfoLattice` (S31).
- **The selection-law doc's Unified Channel Law,** $I(\Omega;\Theta_t,Y_t)\le I(\Omega;D_t)+I(\Omega;E_{\text{ver}}\mid D_t)$, is the same data-processing idea as GM T2/T4 and outline S26, extended to verifiers. Proving it needs the conditional-independence condition below.

## 4. Known corrections and seams (fix these before formalizing)

1. **GM T4, part 2** needs $\xi\perp\Omega\mid D$, not just $\xi\perp\Omega$.
   - Counterexample: Ω and D are independent fair bits and $\xi=\Omega\oplus D$; then $C=D\oplus\xi=\Omega$.
   - "Strictly under finite sampling" needs $C$ to be non-sufficient.
2. **GM T9 and outline S13 conflicted** over whether averaging should remove symmetry breaking. S27 resolves this by splitting symmetry breaking into a world part (keep: February, hemispheres, wars) and an agent part (average away).
3. **The Lean v2 main theorem holds for every channel**, so all its content is in the hypotheses ("assumed growth"). In Lean v1, `grounded_communicate_conserves_collective` and `discovery_and_language_grows_collective` are already lattice forms of GM T2 and T4.1. Keep them.
4. **The five seams from the selection-law doc:**
   - adaptive verifier reuse breaks $\Delta_{\text{select}}\ge0$ (T3);
   - pragmatic reporting bias breaks exact equivariance (T8);
   - quadratic embeddings do not explain Transformer belief states;
   - fixed-depth Transformers need chain-of-thought to act as a universal interpreter (A9/T7);
   - the RLHF-sophistry evidence (Wen et al. 2025) is reportedly contested.

   The second seam is the outline's $B^\perp$ (S3, S27); its proposed remedy, approximate equivariance with an explicit bound, is outline O4/S7(b). The first seam bears on outline S21's test term $\mathcal F_{\text{test}}$.

## 5. Unverified citations

The **selection-law doc** cites items not checked in this session:

- an April 2026 ICLR Blogposts replication audit of Wen et al.;
- *The Linear Representation Hypothesis Needs a Group Action*, arXiv:2609.27158;
- the Rogers-chain paper, arXiv:2611.06022;
- full-paper numbers from Guo, Wu & Yiu (2026): Hedges' $g>1.6$, $R^2=0.94$.

It gives Engels et al. as *Not All Language Model Features Are Linear* (2024). The published ICLR 2025 title is *…One-Dimensionally Linear*.

The **outline's** "from memory" references are listed as such in its bibliography.

## 6. Suggested next steps, in order

1. **Finite cyclic world** (outline §6; GM Phase 1). Prove GM T1, T2, T4.1–2, T5 and C11, plus outline S1, S4, S26 and S29, in a finite model with $\Omega=\mathbb Z_N\times$ seasonal phenomena.
2. **Lean.** Drop the core-only restriction and use Mathlib. Port the two drafts, then outline §8 items 1–4:
   - S1 as a reindexing of finite sums;
   - the S4 hemisphere lemma on `ZMod 12`;
   - an irrep-lattice `InfoLattice` on `Finset (Fin 7)`, replacing `Bit3`;
   - the fusion closure operator.
3. **Cheap experiments, run in parallel.**
   - Spectral low-pass collapse: outline X7, X12 and X14, equivalent to the selection-law doc's Experiment 1. Track month, triad and star-harmonic spectra *and* the symmetry-breaking facts across self-training generations.
   - Belief-simplex degradation: the selection-law doc's Experiment 4.
   - Starting code: github.com/dkarkada/symmetry-stats-repgeom.
4. **Theory.** Outline S10 (Plancherel alignment) and S25 (alignment inflation) are short proofs; write them up first. After that: S7 (exchangeability), then T3 with an adaptive-selection penalty.

## 7. Environment notes

- **Network.** `arxiv.org` was added to the Default cloud environment's allowed hosts this session, so papers can be fetched directly. No other hosts were added.
- **No Lean toolchain** is installed in the container.
- **PaperOrchestra** was removed on 2026-11-22. It drafts papers but does nothing for the grounding loop. Its one hand-written input survives as [`explorations/paper-brief-symmetry-convergence.md`](explorations/paper-brief-symmetry-convergence.md). `api.semanticscholar.org` is still an allowed host.
- **PSITIP** is pinned in `program/tools/check.py` and installed outside the repo by `program/tools/setup_verifiers.sh`, because it is GPL-3.0.
- **Git.** Earlier work was on `claude/determined-davinci-3341ib`; this session works on `claude/ecstatic-albattani-urj2dx`. No pull request has been opened. Run `git config core.hooksPath .githooks` once per clone.

## 8. Open questions for the author

- Where is GM's "File B" (add/delete monoid)? GM's roadmap uses its group-sum machinery for T8.
- Should outline v1 and GM be merged into a single document, or kept as parent and sub-program?
- Is the selection-law doc meant to supersede GM's roadmap, or to be absorbed into it as a new section on Transformers and post-training?
