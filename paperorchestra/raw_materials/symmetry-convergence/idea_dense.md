# Convergence Is Not Grounding: Closed-Form Representational Alignment on Symmetric Word Families

## Problem Statement

The Platonic Representation Hypothesis (PRH; Huh, Cheung, Wang & Isola, 2024) holds that neural networks trained on different data, objectives and modalities converge toward a shared statistical model of reality. It is supported by alignment scores (CKA, mutual-kNN) that rise with scale, but it leaves two questions open in its own §6: what a given alignment score (e.g. a mutual-kNN of 0.16) actually means, and whether alignment is capped by the mutual information between the input signals. Separately, recent work shows that when word co-occurrence statistics are invariant under a group G, the geometry of a single model's embeddings is fixed by G's irreducible representations (Karkada et al., 2026; Storan, Tolias & Miolane, 2026). Neither line of work connects the single-model geometry result to multi-model convergence, and neither says when alignment between models is evidence about the world rather than about a shared corpus.

## Core Hypothesis

On word families whose statistics carry a group symmetry (months, weekdays, hues, musical chords, celestial positions), PRH-style convergence is a theorem rather than a hypothesis, and it has a closed form: the alignment between two models is a Plancherel inner product of their irrep spectra, so the alignment ceiling is computable. The same harmonic analysis shows that **convergence is not grounding**. Closed-loop (self-generated) training acts as a spectral low-pass filter; alignment metrics are dominated by the leading irrep; so collapse can *raise* cross-model alignment while *lowering* the grounded information the representations carry about the world. Alignment is evidence about reality only across training channels that are conditionally independent given the world.

## Proposed Approach (theory paper; no new experiments have been run)

1. **Setting.** A world with a symmetry group G acting on an orbit of states; an equivariant lexicalization channel; a word family in bijection with the orbit; learners whose targets are entrywise transforms (PMI, shifted PMI, the M* surrogate) followed by spectral maps (positive part, absolute value), plus a class of exchangeable deep networks.
2. **Symmetry inheritance and objective independence (S1–S3).** Invariant world statistics push forward to invariant co-occurrence statistics; every learner in the linear class shares the same isotypic decomposition; deviations split into a G-invariant part (which only rescales) and an orthogonal part (the only part that can rotate eigenvectors).
3. **Theory for deep networks (S7).** Equivariant training plus exchangeable initialization plus an invariant corpus law makes the law of every token-level representation G-invariant, addressing the limitation both anchor papers state (their theorems cover word embeddings only).
4. **Closed-form alignment and ceilings (S9–S15).** CKA between two models on a family equals the Plancherel inner product of their Fourier coefficients; disjoint corpora still align, with Davis–Kahan rates in the family-relevant token mass; bijective observations are not needed for cross-modal convergence.
5. **Convergence versus grounding (S22, S24–S27).** Grounded information decomposes by irrep; collapse removes high irreps first; a lower bound CKA ≥ sqrt((1−τ_a)(1−τ_b)) shows collapsed models align almost perfectly; a data-processing bound shows agreement implies grounding only under conditional independence of the training channels; symmetry breaking splits into a world part (keep) and an agent part (average away).
6. **A finite cyclic world testbed (§6)** in which every statement is computable, and a list of falsifiable experiments with stated predictions.

## Expected Contributions

- A closed-form answer, on symmetric families, to the PRH's question of what an alignment score means.
- The first theory of family geometry for deep networks (via exchangeability), not only word embeddings.
- A precise, falsifiable statement that alignment metrics are blind to exactly what model collapse destroys, with a recommendation for tail-sensitive, independently checked grounding measures.
- A set of pre-registered experimental predictions (not yet run).

## Honesty constraints for the writer

- This is a theory/position paper. **No experiments have been run by the authors.** Every number in the paper must be either derived in closed form from the stated theory or quoted from a cited paper with attribution.
- Results tagged New or Conjecture are proof targets or proof sketches, not established theorems; present them as Propositions with proof sketches or as Conjectures, matching the status given in the idea and log.

---

# Technical content (from the project's verified outline)


Labels S1–S31 are result IDs, O1–O7 open problems, GM-* items from the parent Grounded Misprision program. Each result carries a status tag: Known (published), Implicit, New (target theorem), Conjecture, or Test. Preserve these tags in the paper.


## 1. Thesis

There are two claims, one per program.

**State: the PRH side.** Take a word family whose co-occurrence statistics are invariant under a group $G$. On such a family, representational convergence is a theorem, not a hypothesis. The shape every learner reaches is fixed by $G$: it is made of matrix elements of $G$'s irreducible representations (irreps). This much is Karkada et al. and Storan et al.

What this program adds is the multi-agent part:

- the shape is shared across objectives, agents, corpora and modalities;
- alignment between two models has a closed form, a Plancherel inner product of their spectra;
- the alignment ceiling is computable.

On symmetric families, that answers the PRH's own open question of what an alignment score of 0.16 means. It also makes precise the PRH's §6 conjecture that alignment is "capped by the mutual information between the input signals."

**Process: the GM side.** Convergence is not grounding. Models trained on a shared or self-generated corpus converge to *the corpus's* kernel. That kernel equals the world's kernel only through channels that are conditionally independent of the corpus given the world (GM A2, T4).

In the symmetric sector this has a sharp signature:

- closed-loop training acts as a low-pass filter (GM T9);
- alignment metrics are dominated by the leading irrep;
- so **collapse raises cross-model alignment while lowering grounded information**.

PRH alignment is therefore evidence about reality only across conditionally independent channels (S26).

**Together.** Reference carries world symmetry into word statistics, and geometry is a snapshot of that symmetry (GM T8 = S1). Convergence of snapshots across agents is the PRH. Whether a snapshot stays true is a matter of selection (GM T3).

## 2. The anchor results, verified

### 2.1 Karkada, Korchinski, Nava, Wyart & Bahri (2026), arXiv:2602.15029v3, ICML 2026

- **Model.** Word embeddings learn the top eigenmodes of
  $$M^\star_{ij}=\frac{P_{ij}-P_iP_j}{\tfrac12(P_{ij}+P_iP_j)},$$
  which equals PMI up to third order. The embeddings are $W=\Phi\sqrt{|\Lambda^\star|}$ (Karkada et al., 2025).
  - Asymmetric (word/context) factorization is identifiable only up to an invertible linear map. With their balanced initialization, the Gram matrix factors $|M^\star|$.
  - Empirically $M^\star$ is far from positive semidefinite: $\operatorname{rank}M^+\approx\operatorname{rank}M^-$.
- **Assumption 3.1.** $P_{ij}=P_iP_j\,\tilde C(\mathrm{dist}(x_i,x_j))$, so $M^\star_{ij}=C(\mathrm{dist})$ with $C=f\circ\tilde C$ and $f(y)=2(y-1)/(y+1)$.
- **Results.**
  - Prop. 1: Fourier geometry on periodic lattices.
  - Cor. 2: for the periodized exponential kernel, amplitudes $a_n=\sqrt{2\sigma/(1+\sigma^2k_n^2)}$ with $k_n=\pi n$.
  - Prop. 3: open boundary conditions (years), with wavenumbers set by a transcendental quantization condition. This gives Lissajous curves.
  - Prop. 4: linear coordinate decoding error scales as $\varepsilon^2\sim r^{-1/D}$ in the probe rank $r$.
- **Robustness (§4).**
  - Latent model: $P(i\mid t)=P(i)(1+g(t-t_i))$, so PMI is circulant in seasonal phase.
  - Eigenvalues *and the gaps between them* scale with the number of seasonal words $N$. So editing a fixed block, such as the $12^2$ month–month entries, cannot move the top eigenvectors (Weyl or Davis–Kahan).
  - Experiment: month–month co-occurrence is set to independence ($M^\star_{\mathcal S}=0$), with $d=10^3\ll V=2.5\times10^4$. The month circle survives.
  - With $H$ seasonal "helper" words, reconstruction error falls like $1/\sqrt H$. Number words ("one" through "seventeen") do not help.
- **Product structure (App. D).** Seasonality times binary attributes gives a Kronecker-structured PMI. Its eigenbasis is Fourier modes times Walsh functions: harmonic analysis on $\mathbb Z_N\times\mathbb Z_2^d$.
- **Symmetry breakers they report.**
  - "May" polysemy, which an LLM resolves from context and word2vec does not.
  - Kinks in the year manifold at WWI and WWII.
  - Digit tokenization of years.
  - Two-token US state names.
- **Not addressed:** the PRH, or alignment across models. Their discussion does call the geometry "task-agnostic and architecture-agnostic," and notes that text-only models acquire "a form of perceptual grounding."

### 2.2 Storan, Tolias & Miolane (2026), arXiv:2610.00647v1

- **Theorems.**
  - Finite group acting freely and transitively on the words (a torsor), Thm 4.1 / B.3: the principal-component scores are $\sqrt{\lambda^{(s)}_\rho d_\rho/n}\,\rho(g)_{as}$. Here $\lambda^{(s)}_\rho$ are the eigenvalues of the matrix Fourier coefficient $\widehat C(\rho)$. This covers non-abelian groups and irreps that appear more than once.
  - Compact groups (Thm C.5).
  - Homogeneous spaces (Thm D.1), with a Gelfand-pair corollary (D.3) in which eigenvalues are integrals of spherical functions.
  - The sphere $S^2$ (Thm 4.2).
  - If the kernel is a class function, then $\widehat C(\rho)=\hat c_\rho I$.
- **Method.** They test invariance with the Reynolds projection $\Pi_GM^\star$ (averaging $M^\star$ over the group) and report its $R^2$.
  - Months: $R^2=0.87$.
  - Bach triads: $R^2=0.822$ under transposition–inversion $T/I\cong D_{12}$, versus 0.830 under transposition alone ($\mathbb Z_{12}$), which uses 7 more parameters.
  - $T/I$ is the most data-efficient hypothesis on held-out chorales.
- **Evidence across models.** They do not frame this as PRH evidence, but it is:
  - the circle of fifths appears in chord embeddings (per-chord cosine 0.98) and in ChordBERT activations (0.91);
  - the sky sphere appears as degree-ordered spherical-harmonic blocks in 5 of 7 LLMs;
  - the same fingerprint appears in embeddings trained on four star guides totalling 131k tokens;
  - simulations suggest roughly 32–64 times that corpus would match the 123B model's sharpness;
  - genre matters more than volume: text8 (17M tokens) shows no sky signal.
- **Shape versus radii.** Across choices of context window, the rotation angles and isotypic energy stay stable while the eigenvalues drift. In their words, "corpora that have the same symmetries can still have wildly different eigenvalues."
- **Not addressed:** the PRH, perturbation theory, or theory for LLM activations. Their stated limitation is that applying the result to activations "rests on an empirical premise."

### 2.3 Huh, Cheung, Wang & Isola (2024), arXiv:2405.07987, ICML 2024

- **Idealized world.**
  - The world is a sequence of discrete events $\mathbf Z$.
  - Observations are **bijective, deterministic** functions of events.
  - Noise-contrastive (NCE-type) learners converge to $K_{\mathrm{PMI}}+c_X$.
  - Bijectivity carries PMI over to the events, so all modalities converge to $K_{\mathrm{PMI}}(z_a,z_b)$.
- **§6 limitations.**
  - For non-bijective observations, they conjecture that alignment is "capped by the mutual information between the input signals and by the capacity of each model."
  - They leave open whether a mutual-$k$NN score of 0.16 is strong or weak.
  - Their color experiment (after Abdou et al., 2021) is a symmetric-family case: hue is roughly a circle, $U(1)$.
  - Their metric family CKNNA interpolates between CKA and mutual-$k$NN.

### 2.4 Settled versus open

| Question | Status |
|---|---|
| Invariant statistics give irrep geometry, for one model, in word embeddings | **Known** (Karkada; Storan) |
| Robustness to block edits through a collective eigengap | **Known** (Karkada §4.1) |
| Same structure in LLMs, text-embedding models and a chord transformer | **Empirical** (Karkada; Storan); no theory |
| Shape shared across objectives (entrywise transforms) | **Implicit** in Karkada Eq. 3; stated and used here (S2) |
| Shape shared across agents, corpora and modalities; closed-form alignment; ceilings | **New** (S9–S15) |
| Theory for deep networks, not just word embeddings | **New** (S7) |
| Convergence versus grounding; alignment under collapse | **New, joint with GM** (S24–S31) |

## 4. Shared primitives and notation

This version uses GM's notation and renames the v0 symbols that clashed with it.

| Object | GM | Here |
|---|---|---|
| World, states, law, symmetry | $(\Omega,P)$, $\omega_t$, $G$ | same; orbit $\mathcal O\cong G/K\subset\Omega$ |
| Sensoria, private evidence | $O_{a,t}=\sigma_a(\omega_t,\xi_{a,t})$, $E_a$ | same |
| Agent state | $s_a=(b_a,S_a,\kappa_a)$ | same; $\kappa$ is *context* (v0's quantizer is now $q_a$, v0's blur is now $\nu_a$) |
| Reading | $\rho_l(h\mid u,\kappa_l)$ | written $r_l(\cdot)$, freeing $\rho$ for irreps |
| Collective state, grounded information | $W_t$, $\mathcal G_t=I(\Omega;W_t)$ | same; spectral version $\mathcal G=\sum_\rho\mathcal G_\rho$ (S24) |
| Corpus, machine reader | $D$, $q\approx P_D$ | same |
| Word family | — | $\mathcal S\subset V$, in bijection with $\mathcal O$ (v0's $W$) |
| Representations | — | $X_a$ (v0's $E_a$, which clashed with GM's evidence) |
| Co-occurrence target | — | $M^\star_a$; irreps $\rho\in\widehat G$; Fourier coefficients $\widehat C_a(\rho)$ |

**Where the two programs meet.**

| GM item | Here |
|---|---|
| A14: co-occurrence is induced by co-occurrence in the world | Karkada §4.1's latent model is the formal instance |
| T1: misprision is unavoidable | S17–S18, restricted to a family |
| T6: fidelity threshold | S28, restricted to a family |
| T8: equivariant reference transfers symmetry | S1 |
| T9: collapse is a low-pass filter | S21–S22, S28 |
| T10: geometry as a weak internal test | S29 |
| C13: correlated evidence turns aggregation into cascades | enters S13 |
| C21, C28: camps; conspiracy communities | S20 |

**Original notes, and where each now lives.**

| Note | Location |
|---|---|
| Speaking for the performance or for the content | Performance channel = speaker-type cues (S19–S20); content channel = families |
| Sensoria, metacognition, imaginative excursions | GM primitive 2; imagination as untested readings, the drift term (S21); metacognition tested in X10 (affect circumplex) |
| Misperceptions | S4, S12, S18 |
| Embeddings vary by person; each holds a subset of the corpus | S9–S13 |
| Cants and shared experiences | S19 (Wyner–Ziv side information) |
| Speech shares sensoria or invokes a behavior; hearing is rate-limited | GM primitives 5–7; S16–S17 |
| Nuance | S17 |
| "What do you mean, *you people*?" | S19 |
| Hunch | S1 (geometry comes from behavior); S11 and S26 (disjoint but intelligible, and when agreement means reality); S23 and GM T4 (accumulation) |

## 5. The program

**Learner classes.**

- $\mathcal L_{\text{lin}}$: the target is $\mathcal T_a=\mathrm{trunc}_d\,\psi(F(M_a))$.
  - $F$ acts entrywise: PMI, shifted PMI, log counts, or $M^\star$.
  - $\psi$ is spectral: positive part, absolute value, or reshaping by finite-time training.
- $\mathcal L_{\text{exch}}$: deep networks in which
  - token identity enters only through embedding and unembedding rows;
  - those rows are initialized i.i.d.;
  - the optimizer is permutation-equivariant.

### Stage A: symmetry inheritance (world → corpus)

- **S1. Pushforward (GM T8). Implicit/Known.** Suppose the joint law $\Pi$ of co-occurring contexts is $G$-invariant, and the channel is equivariant: $p_a(\sigma_gv\mid g\omega)=p_a(v\mid\omega)$. Then $M^\star_a(\sigma_gu,\sigma_gv)=M^\star_a(u,v)$.
  - Proof: change of variables. Karkada §4.1 is the $U(1)$ case.
- **S2. Objective independence. Implicit, now stated.** Every entrywise $F$ and every spectral $\psi$ preserves commutation with the permutation matrices $R_g$.
  - So every learner in $\mathcal L_{\text{lin}}$ has the same isotypic decomposition; only the spectra differ.
- **S3. Decomposing distortions. New, elementary.** Write an agent's deviation as $B_a=M_a-M=B_a^G+B_a^\perp$, with $B^G=\int_GR_gBR_g^{-1}\,dg$.
  - This is the same projection Storan et al. use to test invariance.
  - Only $B^\perp$ can rotate eigenvectors.
- **S4. Hemispheres. New; Test X2.** Let $s$ be the southern share of the corpus.
  - The $k$-th Fourier coefficient of every seasonal profile is multiplied by $1-s+s(-1)^k$.
  - At $s=\tfrac12$ the odd harmonics vanish exactly, and stay zero after taking the log.
  - The basis is unchanged, but the spectrum can reorder: when seasonal content dominates calendar-sequence content, June lands next to December.

### Stage B: symmetry → geometry (one agent)

- **S5. Known** (Storan Thms 4.1, C.5, D.1, D.3; Karkada Props 1–4). Family geometry consists of irrep matrix elements weighted by $\sqrt{\lambda_\rho^{(s)}}$.
- **S6. Known** (Karkada §4.1), with one remark. The collective eigengap scales with the number of coupled words. The deletion ablation is $G$-invariant, so it changes the radii and not the basis.
- **S7. Exchangeability for deep networks. New.** Assume:
  - (i) the algorithm is equivariant: $\mathrm{Alg}(\sigma D,\sigma\xi)=\sigma\,\mathrm{Alg}(D,\xi)$;
  - (ii) the initialization is exchangeable: $\sigma\xi\overset d=\xi$;
  - (iii) the corpus law is invariant: $\sigma_gD\overset d=D$.

  Then the *law* of every token-level representation is $G$-invariant. This covers static embeddings and context-averaged activations at any layer. So $\mathbb E[\mathrm{Gram}_{\mathcal S}]$ satisfies S5, and no linearity is needed.
  - This targets the limitation both papers state.
  - Open: self-averaging (measurable as variance across seeds), and a quantitative version under approximate invariance (algorithmic stability).
  - Empirical hint: in Karkada's Fig. 14, context sharpens the circle across layers.
- **S8. Learning order. Conjecture; Test X9.** In the closed-form dynamics of Karkada et al. (2025), eigenmodes are learned in order of eigenvalue.
  - So irreps should appear low-frequency first, and cross-model alignment should rise in steps.

### Stage C: convergence across agents (the bridge to the PRH)

- **S9. Population universality. New; empirical support in Storan Fig. 9.** Suppose agents differ in equivariant channel, objective, dimension and modality, but share $G$ and the orbit $\mathcal O$.
  - Then $X_a|_{\mathcal S}$ and $X_b|_{\mathcal S}$ share the harmonic frame.
  - They differ only in their spectra $\{\widehat C_a(\rho)\}$ and in a gauge transformation: the choice of origin and reflection within each irrep block.
- **S10. Closed-form alignment. New.** For centered family Gram matrices (full rank, positive part):
  $$\mathrm{CKA}(a,b)=\frac{\sum_{\rho\neq\mathbf 1}d_\rho\,\langle\widehat C_a(\rho),\widehat C_b(\rho)\rangle_F}{\big(\sum_\rho d_\rho\lVert\widehat C_a(\rho)\rVert_F^2\big)^{1/2}\big(\sum_\rho d_\rho\lVert\widehat C_b(\rho)\rVert_F^2\big)^{1/2}}$$
  - This is the Plancherel inner product of the two kernels.
  - For class-function or Gelfand-pair kernels, it reduces to the multiplicity-weighted cosine of the two scalar spectral profiles.
  - Mutual-$k$NN equals 1 whenever the distance profile is monotone, for example when the leading irrep dominates on $\mathbb Z_N$.
  - *On symmetric families, this answers the PRH's question of what a given score means: the ceiling is computable from the two spectra.*
- **S11. Disjoint corpora, with rates. New.** By Davis–Kahan, $\lVert\sin\Theta(U_a,U_b)\rVert\le2(\varepsilon_a+\varepsilon_b)/\delta$. No shared data is needed.
  - The gap $\delta$ scales with the number $H$ of words coupled to the family.
  - The estimation error $\varepsilon$ scales with the family-relevant token mass $n_{\text{eff}}$, not with total tokens.
  - Evidence: Karkada's $1/\sqrt H$ helper scaling; Storan's genre-over-volume result and their 32–64× simulation.
- **S12. Ordering and blur. New.** A symmetric, unimodal perceptual blur $\nu_a$ multiplies the spectrum by $|\hat\nu_a(\rho)|^2$ (abelian case, linear-response regime), so the order of the irreps is preserved.
  - A multimodal distortion, such as S4's hemisphere mixture, can reorder it.
- **S13. Pooling with correlated sources. New; uses GM C13.** Agent idiosyncrasies shrink like $\sqrt{\log|V|/A_{\text{eff}}}$, where $A_{\text{eff}}=A/(1+(A-1)\bar\gamma)$ and $\bar\gamma$ is the mean pairwise correlation of the agents' distortions.
  - At a fixed token count, more independent sources give more alignment. Correlated sources give cascades.
- **S14. Cross-modal, weakening bijectivity. New.** If an equivariant observation channel has nonzero Schur scalars on the leading irreps, that is enough for cross-modal convergence on the family (when no irrep repeats). Bijectivity is not needed.
  - This is the precise, family-level form of PRH §6's mutual-information cap.
- **S15. A ceiling. New.** Alignment ≈ the population Plancherel CKA $-\,O((\varepsilon_a+\varepsilon_b)/\delta)$.
  - As scale grows, alignment rises toward a ceiling. The ceiling is below 1 unless the two spectra are proportional.

### Stage D: communication

- **S16. Schematic.** Communication error splits into three terms:
  - lexical misalignment, which vanishes on families by Stage C;
  - error in the listener's model of the speaker;
  - a rate term.
- **S17. Nuance as water-filling over irreps. New.** For $G$-invariant distortions of negative type:
  $$R(D)=\sum_\rho\frac{m_\rho}{2}\log^+\frac{w_\rho(\kappa)\,\alpha_\rho}{\eta}$$
  - The context $\kappa$ sets the weights $w_\rho$, so context decides where precision goes.
- **S18. Misprision is high-pass (GM T1 on a family). New.** Two readers in different contexts, or with different quantizers $q_a$, agree below both water lines and both Nyquist limits, and diverge above them.
  - Months coarse-grained to seasons: the gains $|\sin(\pi k/4)/(3\sin(\pi k/12))|$ are 0.91, 0.67, 0.33, 0 and 0.24 for $k=1$ to $5$.
  - *Unavoidable misprision has a spectral address: the high irreps.*
- **S19. Audience models and "you people". New.** The listener decodes with a posterior over speaker types:
  $$P_L(h\mid u)\propto\sum_\tau P(\tau\mid\text{cues})\,S_\tau(u\mid h)\,P_\tau(h)$$
  This is a Rational Speech Acts model with type uncertainty.
  - On families, the $S_\tau$ agree, except for relative phases *between* families: "a December wedding" is warm or cold depending on hemisphere.
  - Cants act as shared side information (Wyner–Ziv).
  - Negative trust, GM's conspiracy case, is a type posterior that flips the sign of evidence.
- **S20. The social residual (GM C21, C28). Conjecture; Test X8.** Fit two community-trained models to each other by Procrustes on the families. The residual:
  - is orthogonal to the families;
  - predicts the community;
  - clusters into camps.

  Prediction: corpora from conspiracy communities keep the calendar circle while their residual diverges. They agree about December.

### Stage E: accumulation (GM's process, specialized)

- **S21. Generational map with selection. New.**
  $$M_{t+1}=\beta M_{\text{world}}+(1-\beta)\big[\pi\,\mathcal F_{\text{test}}(\Phi(M_t))+(1-\pi)\,\Phi(M_t)\big]$$
  - $\beta$: the fraction of fresh, grounded speech.
  - $\pi$: the fraction of synthetic or retold readings that pass a test on independent evidence (GM's select term).
  - The remainder is GM's drift term.
  - If $\Phi$ is equivariant in law, every iterate keeps the $G$-basis.
- **S22. Low-pass collapse (GM T9). Conjecture, with a mechanism.** Suppose each generation re-estimates from $n_{\text{eff}}$ samples with Wiener-type shrinkage $s_\rho=\alpha_\rho/(\alpha_\rho+\sigma^2/n_{\text{eff}})$.
  - Then the radii evolve as $\alpha^{(t+1)}_\rho=s^{(t)}_\rho\alpha^{(t)}_\rho$.
  - Small radii decay fastest, so harmonics die in order and the circle goes last.
  - If data accumulate rather than being replaced, $n_{\text{eff}}$ grows and the radii plateau (Gerstgrasser et al., 2024).
- **S23. What the limit is. New.** $M_\infty$ is the world kernel seen through the *average lexicalization channel*. That is meaning from form as a state, as in GM T8.

### Stage F: joint results (grounding, alignment, the irrep lattice)

- **S24. Grounded information by irrep. New.** Assume $G$-invariance and a Gaussian surrogate: the world's family kernel is a stationary Gaussian field on $\mathcal O$, and the representation observes it with noise. Then
  $$\mathcal G=\sum_\rho\mathcal G_\rho,\qquad \mathcal G_\rho=\tfrac{m_\rho}{2}\log(1+\mathrm{SNR}_\rho)$$
  - *In the symmetric sector, GM's "index $\mathcal G$ by target" becomes "index $\mathcal G$ by irrep."*
  - Water-filling (S17), aliasing (S18) and collapse (S22) are all statements about the vector $(\mathcal G_\rho)_\rho$.
- **S25. Collapse inflates alignment. New; Test X12.** Take scalar, nonnegative spectra (class-function or Gelfand-pair kernels) with a shared leading irrep. Let $\tau_a$ be the share of spectral mass outside the leading irrep. Then
  $$\mathrm{CKA}(a,b)\ \ge\ \sqrt{(1-\tau_a)(1-\tau_b)}$$
  - Collapse drives $\tau\to0$ (S22). Collapsed models then align almost perfectly with each other, and with any kernel dominated by the leading irrep, while $\mathcal G$ falls (GM T2).
  - **CKA and mutual-$k$NN cannot see exactly what collapse destroys.**
  - Measuring grounding needs a tail-sensitive measure: per-irrep radii, plus the world-asymmetry component (S27), each checked against an independent channel. Examples: climate records for months, geodesic distances for places, true celestial angles as in Storan §7.
- **S26. When alignment is evidence of reality. New, easy.** Suppose $D_a\perp D_b\mid\Omega$ (GM A2), and the two models' training randomness is independent. For any learners, the data-processing inequality along $D_a\to\Omega\to D_b$ gives
  $$I(X_a;X_b)\le I(D_a;D_b)\le\min\{I(\Omega;D_a),\,I(\Omega;D_b)\}$$
  - Agreement can then only come from the world.
  - Without conditional independence (shared web text, or synthetic data from a common model), agreement is bounded only by the shared corpus, and grounding can be zero.
  - Agreement that comes from shared *priors* is invisible to mutual information but visible to CKA. That is S25's inflation.
  - *Alignment between LLMs trained on overlapping web corpora does not by itself show convergence to reality. Alignment across conditionally independent channels (different modalities, languages, eras or hemispheres) can.*
  - This is the information-theoretic form of PRH §6's cap. Relating population mutual information to CKA on a single training run is a further step (O5).
- **S27. Two kinds of symmetry breaking. New.** Split $B^\perp=B^\perp_{\text{world}}+B^\perp_{\text{agent}}$.
  - The world part: February is short; seasons flip by hemisphere; the year manifold kinks at WWI and WWII (Karkada); New Year pins the origin.
  - The agent part: idiosyncrasy.
  - Pooling removes the agent part (S13).
  - Collapse removes the world part first (GM T9, second bullet), because irregularities are small modes and closed loops regress toward a smooth prior.
  - The world part is also what fixes the gauge across models (O3).
- **S28. An error threshold per irrep (GM T6 on a family). Conjecture.** An irrep survives transmission if its per-generation signal-to-noise ratio clears the copy noise.
  - The number of retained harmonics, $K(n_{\text{eff}},\varphi,A_{\text{eff}})$, is the family-level analogue of Eigen's $K$.
  - Calendar dates (365 tokens, many harmonics; Karkada Fig. 9) give a high-resolution testbed.
- **S29. Geometry as a weak test (GM T10). New, easy.** The Reynolds projection $\Pi_G$ is a function of the corpus, so it cannot raise $\mathcal G$ (GM T2).
  - It does lower variance, which is why $T/I$ is the most data-efficient chord hypothesis in Storan et al.
  - It also erases $B^\perp_{\text{world}}$.
  - So it slows collapse at the cost of smoothing away the world's irregularities. It is a bias–variance trade, not a source of information.
- **S30. Explicit content as closure under tensor products (GM: "`sup` should become a closure operator"). New.**
  - Once the leading irrep is resolved, every higher harmonic is *computable* from it: $e^{ik\theta}=(e^{i\theta})^k$, and in general through tensor products and fusion rules.
  - So explicit content on a family is the closure of the resolved irreps under tensor products.
  - The radii $\alpha_\rho$, which say how strongly the world couples to each harmonic, are not computable. They are grounded information.
  - This is GM's split between explicit and grounded content, realized exactly. It also gives GM the closure operator it wants: $\mathrm{cl}(R)$ = the irreps generated by $R$ under $\otimes$.
  - Consistency check with S4: a reader who resolves only $k=2$ (hemisphere-mixed seasonal text) has closure equal to the even frequencies, so the annual cycle cannot be deduced from the semiannual one.
- **S31. The irrep lattice as a grounded `InfoLattice`. New.** When no irrep repeats, let a state be a subset of $\widehat G$ (in general, a subrepresentation), with sup = union, bot = $\varnothing$. An agent "knows $\rho$" when $\mathrm{SNR}_\rho$ is above threshold. Then:
  - collapse is a deflationary operator that removes high irreps;
  - aliasing is restriction to a subgroup's dual;
  - deduction is S30's closure;
  - $\mathcal G$ is monotone on the lattice.

  This gives the Lean drafts' `InfoLattice` a concrete model anchored in the world (§8).

## 6. Shared testbed: a cyclic world

This is a finite instance for GM's Phase 1 ("finite Ω, finite H, Bayesian agents"), in which nearly every statement above is computable.

- **World.** $\Omega$ is $\mathbb Z_N$ (the calendar) times seasonal phenomena, with $G=\mathbb Z_N$ shifting both.
- **Agents.** Two hemispheres (S4), with independent sensoria (say, thermometers) or none.
- **Lexicalization.** Equivariant, except for designated irregularities: a short month, a fixed-date holiday.
- **Readers.** Human readers have the corpus plus independent evidence $E_i$. The machine reader runs a closed loop, optionally with a verifier.
- **Computable here:** GM T1, T2, T4, T8 and T9, and S4, S10, S13, S22 and S24–S29.
- **Sizes.** $N=12$ for months, $N=7$ for weekdays, $N=365$ for dates.

## 10. Open problems

- **O1. Objective-free geometry beyond groups.** $\{f(M)\}_f$ is simultaneously diagonalizable if and only if the indicator matrices of $M$'s level sets commute. Commutative association schemes are sufficient. Group orbitals are the Schurian case, and on a single orbit they commute exactly when $(G,K)$ is a Gelfand pair.
- **O2. Many small families plus a residual.** Product groups (Karkada App. D, $\mathbb Z_N\times\mathbb Z_2^d$) are the first case. Approximate and local symmetries are next.
- **O3. Gauge.** Symmetry-breaking anchors pin the phase across models. Prediction: neuron-level or sparse-autoencoder features are arbitrary rotations within irrep blocks unless something pins them.
- **O4.** Self-averaging, and approximate invariance, for S7.
- **O5. From population to realization.** Connect S26's mutual-information bound to CKA computed on a single training run.
- **O6. Asymmetric identifiability.** Word/context factorizations are fixed only up to an invertible map (Karkada App. B.2). Alignment comparisons need the balanced solution or a canonical inner product.
- **O7. A family-level selection threshold.** GM's $\lambda^*$, worked out in the cyclic world (S21), as the first exact case.

---

# Spine claims this paper addresses


### K1: Snapshot world model from statistical geometry
- **Status:** conjecture (plausible but unproven; may be false); difficulty: hard
- **Statement:** If text is generated by a latent world-state process (GM A14) with sufficiently varied contexts, any near-optimal next-token predictor admits a simple decoder g with g(phi_theta) ~ s(Omega), where s(Omega) is the linguistically visible sufficient statistic of Omega, identified up to an equivalence class.
- **Corresponds to:** GM-T8, OUT-S1
- **Proof route:** Sufficiency lemma: optimal predictors encode posteriors over hidden states (generalize Shai 2024 from HMMs); Linear identifiability (Roeder 2021; Marconato 2025) fixes the equivalence class; PMI geometry (Levy & Goldberg 2014; Arora 2016) links geometry to world co-occurrence
- **Falsifier:** Near-optimal predictors on synthetic worlds whose representations admit no simple decoder for latent state

### K3: Quinean indeterminacy = identifiability class
- **Status:** new (new theorem target; at most a proof sketch exists); difficulty: medium
- **Statement:** The set of world models consistent with a corpus is the distribution-equivalence class of predictors; 'All or None' partitions linear properties into determinate (in every member) and indeterminate.
- **Proof route:** Translate Quine's radical-translation setup into distribution equivalence; apply Marconato 2025
- **Falsifier:** A semantic property that is fixed by behavior but varies across distribution-equivalent predictors

### K4: Convergence vs collapse
- **Status:** new (new theorem target; at most a proof sketch exists); difficulty: easy
- **Statement:** delta -> 0 among learners is convergence when I(Omega; theta) rises and collapse when it falls; alignment metrics alone cannot distinguish them, a tail-sensitive grounded probe can.
- **Corresponds to:** OUT-S25, OUT-S26
- **Proof route:** Outline S25 (alignment inflation) and S26 (conditional independence)
- **Falsifier:** A case where alignment across conditionally dependent channels tracks grounding

### K5: Retrospective verification of Firth
- **Status:** implicit (follows from published results with little work); difficulty: easy
- **Statement:** Given GM A14 (reference anchors distribution), the distributional hypothesis holds as a theorem about structure: co-occurrence statistics determine geometry up to the identifiability class, and world symmetries appear in that geometry.
- **Corresponds to:** GM-T8, OUT-S1
- **Proof route:** Compose Levy & Goldberg (factorization) with Karkada/Storan (symmetry) and A14
- **Falsifier:** Structured world features absent from distributional geometry despite frequent mention

### K30: C3 restated: latent-weighted collapse
- **Status:** conjecture (plausible but unproven; may be false); difficulty: hard
- **Statement:** Collapse (stationary latent diversity -> 0, G decreasing) occurs when N_e * delta_latent falls below a mutation-drift threshold and verification fraction v < v*; it is not governed by volume or cost. Regime (replace vs accumulate) and definition must be stated.
- **Corresponds to:** GM-T9, GM-C12, OUT-S22, OUT-S28
- **Proof route:** Reduce to single chain as delta->0; Wright-Fisher fixation (discrete); Gaussian a.s. variance collapse (Shumailov); Migration-drift balance with m increasing in delta (K31); Add verification as selection (GM T3)
- **Falsifier:** Diversity loss tracking volume/cost with N_e*delta and v held fixed; or no loss at low N_e*delta and low v
