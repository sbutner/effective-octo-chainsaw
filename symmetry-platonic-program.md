# Symmetry → Geometry → Convergence

*A mathematical program connecting symmetric language statistics (Karkada et al., 2026) to the Platonic Representation Hypothesis (Huh et al., 2024), built on a generous reading of a set of notes on language.*

Status: outline v0 · 2026-11-21

---

## 0. Thesis

The **Platonic Representation Hypothesis (PRH)** says that models trained on different data, objectives and modalities converge toward a shared statistical model of reality. Its supporting theory is an idealization: discrete world events, bijective observations, contrastive learners whose optimal kernel is pointwise mutual information (PMI), and infinite data. It does not say what the shared model *looks like*, how fast agents converge, why agents with *disjoint* data and *different* perceptions should agree, or what is left over when they don't.

**Karkada, Korchinski, Nava, Wyart & Bahri** show, for a single model, that when language statistics carry a symmetry the learned geometry is forced by it. The co-occurrence of two months depends only on the interval between them, so Fourier modes give the month circle, the year curve, and linearly decodable coordinates for places. The geometry survives drastic perturbations, such as deleting every sentence in which two months co-occur. It survives because a continuous latent variable controls the statistics *collectively*, across the whole vocabulary.

**Claim of this project: the symmetric sector of language is the exactly solvable sector of the PRH.** On any word family that is an orbit of a world symmetry $G$:

1. Every learner in a broad class converges to the same object: the decomposition of the family into irreducible representations (irreps) of $G$. Agents differ only by a short vector of per-irrep radii and a gauge rotation. The class covers any objective that is an entrywise function of co-occurrence statistics, and deep networks with exchangeable token initialization.
2. Alignment between two models is then a closed-form function of those radii: linear CKA is the cosine similarity of the two spectral profiles.
3. Convergence needs a shared *law*, not shared *data*. Its rate is set by the same collective eigengap that makes the geometry robust.
4. What does **not** converge is the symmetry-breaking residue: relative phases between families, community-specific associations, register. That is where the notes' cants, audience models and "what do you mean, *you people*?" live.

The notes' hunch becomes three theorems to prove:

- geometry is a pushforward of the statistics of real-world behavior (Stage A);
- separately trained ("disjoint") but mutually intelligible models are what equivariance plus concentration predict (Stage C);
- pooled corpora are consistent estimators of the world kernel's symmetric part, which is the precise sense in which language is an accumulation system for world models (Stage E).

---

## 1. Reading the notes as mathematical objects

| Note | Formal object |
|---|---|
| We speak compulsively, for the performance or for the content | Utterances come from a mixture of a *content channel* (informative about world state $\theta$) and a *performance channel* (informative about speaker type $\tau$) |
| Sensoria: perceived, classified, encoded lexically | Perception kernel $\pi_a(s \mid \theta,\iota)$, then a quantizer $\kappa_a: S\to C_a$ (classification), then lexicalization $\lambda_a: C_a \to \Delta(V)$ |
| …includes metacognitive observations | The state includes the agent's internal state $\iota$; mental-state words are lexicalizations of $\iota$ |
| …and imaginative excursions | Some utterances are generated from $\theta \sim q_a$ (the agent's own model) rather than from the world |
| Misperceptions: a shared world, divergent categorizations | Agent-specific distortions of a shared world kernel, and different quantizers $\kappa_a \neq \kappa_b$ |
| Embeddings vary by person; each has a subset of the corpus | Agent corpus $D_a$, empirical statistics $\hat M_a$, learned embedding $E_a: V\to\mathbb{R}^{d_a}$ |
| …varies with expectation and sensoria co-occurrence | Context-conditioned kernels $M_a(\cdot,\cdot \mid c)$, where expectation acts as prior or context state |
| Cants and shared experiences align associations efficiently | Shared side information and shared codebooks on the symmetry-breaking subspace (Wyner–Ziv) |
| Speech shares sensoria or invokes a behavior | Two message types: source coding of $\theta$ (assertive) and control of the listener's action $b$ (directive), as in Lewis signaling games |
| Hearing: decode in reverse, rate-limited, decide on a response | A Bayesian decoder under a capacity constraint, followed by a decision rule |
| Nuance: put quantization precision where it pays most in context | Rate allocation across components under a context-dependent distortion: reverse water-filling |
| "What do you mean, *you people*?" | A second-order model: the listener's estimate $\hat E_S$ of the speaker's lexicon, via an inferred speaker type (Rational Speech Acts) |
| Hunch | **H1:** geometry is a pushforward of the statistics of world states and behaviors. **H2:** disjoint corpora still give mutually intelligible models. **H3:** pooled corpora estimate the world kernel, and large learners recover it |

---

## 2. The two anchor results in a common language

### 2.1 Symmetry → geometry (Karkada et al., 2026)

**Phenomena explained.** Circular month and weekday features in LLMs (Engels et al., 2024), and linear probes for years, latitude and longitude (Gurnee & Tegmark, 2024).

**Mechanism (paraphrased).** Embedding models approximately learn the top eigenvectors of a PMI-like target matrix $M$ (Levy & Goldberg, 2014; Karkada et al., 2025).

- If $M$ restricted to the months is circulant, $M_{ij} = f\big((i-j) \bmod 12\big)$, its eigenvectors are discrete Fourier modes. The top pair $\big(\cos\tfrac{2\pi i}{12}, \sin\tfrac{2\pi i}{12}\big)$ puts the months on a circle.
- Toeplitz structure (years) gives cosine-like modes and a smooth 1-D curve.
- Distance-dependent statistics on the sphere (places) give spherical harmonics. Their $\ell = 1$ block is the Cartesian embedding of the globe.

**Robustness.** The geometry survives when direct co-occurrences are removed. The reason is that a continuous latent variable (seasonal time, position) drives each month's co-occurrence with the *rest* of the vocabulary.

**Generalization.** A follow-up (arXiv:2610.00647, *Group-Invariant Statistics Determine Embedding Geometry*) appears to extend this to general symmetry groups, with embeddings given by irreps. Marchetti et al. (2024) show Fourier features emerging in group-invariant networks. Stage B below takes the group-theoretic version as its starting point and does not claim it as new.

### 2.2 Platonic Representation Hypothesis (Huh, Cheung, Wang & Isola, 2024)

**Hypothesis.** Representations are converging toward a shared statistical model of reality. Convergence is measured with mutual nearest-neighbor kernel alignment. As evidence, alignment rises with competence and scale, including across vision and language.

**Their idealized argument.** The world is a sequence of discrete events $z$, and each modality observes them through $\mathrm{obs}_X$. A contrastive learner's optimal kernel is $K(x_a,x_b) = \mathrm{PMI}(x_a,x_b) + c_X$. If observations are bijective, the PMI over observations equals the PMI over events. So every modality converges to the same $K_{\mathrm{PMI}}(z_a,z_b)$.

**What it leaves open:**

- (a) the *shape* of the limit;
- (b) finite and disjoint data;
- (c) observation channels that are not bijective and differ by agent (misperception);
- (d) objectives whose optimum is not exactly PMI;
- (e) rates, ceilings, and an account of what does *not* converge.

### 2.3 The bridge in one line

The PRH says that in the idealized limit everyone's kernel equals $K_{\mathrm{PMI}}$. The symmetry result says that if $K$ commutes with $G$, its eigenbasis is fixed by $G$ alone.

**Bridge: commuting with $G$ is far more robust than $K$ itself.** It survives every entrywise transform (so any objective), equivariant misperception, independent sampling, and, in law, architecture. So the eigenbasis, which is the geometry, converges even when the kernels do not.

---

## 3. Formal setup

**3.1 World.** A latent space $(\Theta,\mu)$ holds world states *and behaviors*: what people do, and when. A compact group $G$ acts measurably on $\Theta$ and preserves $\mu$. Let $\rho$ be the joint law of the latent contexts of two tokens in the same window. Assume $\rho$ is invariant under the diagonal action $(\theta,\theta')\mapsto(g\theta, g\theta')$.

**3.2 Agents and corpora.** Agent $a$ emits tokens through a composite channel $p_a(v\mid\theta)$: perception, then categorization, then lexicalization, then the speech act. Collective control takes the latent-variable form

$$P_a(u,v) = \int p_a(u\mid\theta)\,p_a(v\mid\theta')\,\rho(d\theta,d\theta'), \qquad M_a(u,v) = \log\frac{P_a(u,v)}{P_a(u)\,P_a(v)} .$$

Equivalently, $P_a = \Lambda_a K_{\text{world}} \Lambda_a^{\top}$ with $(\Lambda_a)_{u\theta} = p_a(u\mid\theta)$. The corpus $D_a$ has $n_a$ tokens, and corpora may be disjoint. The pooled corpus is $D=\bigcup_a D_a$.

**3.3 G-families.** A family $W \subset V$ is a set of words with a bijection onto an orbit $\mathcal O \cong G/H \subset \Theta$. Examples: months onto $\mathbb Z_{12}$; city names onto $S^2 = SO(3)/SO(2)$.

$G$ acts on the vocabulary by permutations $\sigma_g$: on $W$ through the orbit, on bulk words through their latent phases, and trivially on neutral words. The channel is **equivariant** if $p_a(\sigma_g v \mid g\theta) = p_a(v\mid\theta)$. The family is **multiplicity-free** when $(G,H)$ is a Gelfand pair, which holds for $\mathbb Z_N$, for $U(1)$, and for $S^2$ under $SO(3)$.

**3.4 Learners.**

- $\mathcal L_{\text{lin}}$: the population target is $T = \mathrm{trunc}_d\,\psi\big(F(M)\big)$.
  - $F$ acts entrywise: PMI, shifted PMI (SGNS), log counts (GloVe), PPMI.
  - $\psi$ is a spectral reshaping, for example from finite-time training dynamics.
  - The learned embedding satisfies $EE^\top \approx T$, up to an invertible linear map fixed by a canonical inner product or whitening.
- $\mathcal L_{\text{exch}}$: any deep network that meets three conditions:
  - token identity enters only through embedding and unembedding rows;
  - initialization is i.i.d. across rows;
  - training uses a permutation-equivariant optimizer (SGD, Adam).

**3.5 Alignment.** Linear CKA (Kornblith et al., 2019), mutual-$k$NN (the PRH metric) and Procrustes distance, each computed on a family $W$.

---

## 4. The program

### Stage A: symmetry inheritance (world → corpus)

- **A1 (pushforward).** If $\rho$ is $G$-invariant and the channel is equivariant, then $M_a(\sigma_g u,\sigma_g v) = M_a(u,v)$. *Proof:* change of variables in 3.2.
  - *This is H1 as a lemma.* The geometry a corpus can support is inherited from the symmetry of world behavior: months co-occur with harvests, snow and holidays according to where those behaviors sit in the year.
- **A2 (entrywise invariance).** For any function $f$, $f(M)$ also commutes with $R_g$, the permutation matrices of $\sigma_g$.
  - Trivial, and central: every objective in $\mathcal L_{\text{lin}}$ has the same commutant, hence the same isotypic decomposition. On a multiplicity-free family it also has the same eigenvectors.
  - Only the eigenvalues depend on the objective.
- **A3 (decomposing distortions).** Any agent-specific distortion $B_a = M_a - M$ splits as $B_a = B_a^G + B_a^\perp$, where $B_a^G = \int_G R_g B_a R_g^{-1}\,dg$ is the Reynolds average.
  - Only $B^\perp$ can rotate eigenvectors. $B^G$ only reshapes the spectrum.
- **A4 (worked example: hemispheres).** In the north, snow co-occurs with Dec–Feb; in the south, with Jun–Aug. So $p_S(\text{snow}\mid i) = p_N(\text{snow}\mid i+6)$.
  - Pooling a southern fraction $s$ multiplies the $k$-th Fourier coefficient of every seasonal co-occurrence profile by $1 - s + s(-1)^k$.
  - At $s=\tfrac12$, odd harmonics vanish exactly. They stay zero after taking the log, because a function with period 6 still has period 6.
  - The pooled statistics are still circulant, so the basis is unchanged, but the *spectrum is reordered*. If seasonal content dominates calendar-sequence content, $k=2$ overtakes $k=1$, and the top two principal components put June next to December.
  - Calendar co-occurrence ("from May to June", fixed-date holidays) does not depend on hemisphere, so it keeps $k=1$ alive.
  - *A clean instance of "a shared world produces divergent categorizations": the same calendar, with phase-shifted associations.*

### Stage B: symmetry → geometry (single agent)

- **B1 (Schur / Peter–Weyl; known).** Let $K_W$ be any $G$-commuting Gram matrix on a multiplicity-free family. Then

  $$K_W = \sum_{\rho\ne \mathbf 1} \alpha_\rho\, P_\rho^W, \qquad E(w_x) = \bigoplus_\rho \sqrt{\alpha_\rho}\;\Phi_\rho(x),$$

  with fixed projections $P^W_\rho$ and fixed harmonic frames $\Phi_\rho$:
  - Fourier modes on $\mathbb Z_N$: the circle, then torus-knot curves when higher harmonics are kept;
  - cosine modes for Toeplitz kernels on an interval: the "horseshoe" of Diaconis, Goel & Holmes (2008);
  - spherical harmonics on $S^2$: the $\ell=1$ block is $(x,y,z)$, so latitude $=\arcsin z$ and longitude $=\operatorname{atan2}(y,x)$.

  *The shape is universal; agents differ only in the spectral profile $\alpha = (\alpha_\rho)_\rho$.* Truncation must not split a degenerate irrep; otherwise the choice of $d$ itself breaks the symmetry.

- **B2 (why deletion fails to destroy geometry: two mechanisms).**
  - *Basis.* Deleting all within-family co-occurrences, as in the paper's ablation, is a $G$-invariant edit $\Delta$. By A2 and A3 it cannot rotate the basis; it can only reshape $\alpha$.
  - *Ordering.* Collective control preserves the order of the irreps. With $|V_\theta|$ bulk words coupled to $\theta$, the family's leading eigenvalues scale like $|V_\theta|$, while $\lVert\Delta\rVert = O(|W|)$. A Davis–Kahan bound then gives $\sin\angle = O(|W|/|V_\theta|)$.
  - **Goal:** prove this with explicit constants.

- **B3 (exchangeability theorem; new; for deep networks).** Assume:
  - (i) the training algorithm is equivariant: $\mathrm{Alg}(\sigma D,\sigma\xi) = \sigma\,\mathrm{Alg}(D,\xi)$;
  - (ii) the initialization is exchangeable: $\sigma\xi \overset{d}{=} \xi$;
  - (iii) the corpus *law* is invariant: $\sigma_g D \overset{d}{=} D$.

  Then the *law* of every token-level representation is $G$-invariant. This covers a static embedding and the mean contextual state at any layer. Hence $\mathbb E[\mathrm{Gram}_W]$ commutes with $G$, and B1 applies to it. *No linearity is needed.*

  Open:
  - (a) *Self-averaging:* how close is a realized Gram matrix to its mean? This is measurable as variance across seeds, and is itself a PRH-style statement.
  - (b) *Approximate symmetry:* a quantitative version when (iii) holds only approximately. This needs algorithmic stability with respect to the fraction of symmetry-breaking text. Known breakers: tokenization (years split into digits), polysemy ("May"), and distinguished origins (New Year).

- **B4 (learning order).** In the solvable dynamics of Karkada et al. (2025), eigenmodes are learned one after another in order of eigenvalue. Combined with B1, irreps appear low-frequency first: the circle forms before the finer harmonics.
  - **Prediction:** cross-model alignment on a family rises in discrete steps during training, one irrep at a time.

### Stage C: convergence across agents (the PRH bridge)

- **C1 (population universality).** Let agents $a$ and $b$ differ in their equivariant channels, objectives $F_a, F_b$, dimensions $d_a, d_b$, and even modality, while sharing $G$ and the family orbit. Then

  $$E_a|_W = D_{\alpha^a}\,\Phi\,O_a, \qquad E_b|_W = D_{\alpha^b}\,\Phi\,O_b,$$

  with a common harmonic frame $\Phi$, diagonal radii $D_\alpha$, and gauge rotations $O$ that commute with $G$ (choice of origin and reflection within each irrep block).
  - *This is the PRH's "shared model of reality", in closed form: the harmonic structure of the world's symmetry group.*

- **C2 (closed-form alignment).** Centering removes the trivial irrep. Then

  $$\mathrm{CKA}(a,b) = \frac{\sum_\rho m_\rho\,\alpha^a_\rho\,\alpha^b_\rho}{\sqrt{\sum_\rho m_\rho (\alpha^a_\rho)^2}\,\sqrt{\sum_\rho m_\rho (\alpha^b_\rho)^2}}, \qquad m_\rho = \operatorname{rank} P_\rho^W .$$

  That is, CKA is the cosine similarity of the two spectral profiles.
  - **Mutual-$k$NN corollary on $\mathbb Z_N$.** Squared embedding distance depends only on circular distance $\delta$, through the profile $\delta \mapsto \sum_k \alpha_k m_k\big(1-\cos\tfrac{2\pi k\delta}{N}\big)$. If that profile increases on $[0, N/2]$, which holds when $\alpha_1$ dominates, every agent's $k$NN graph is the cycle, and mutual-$k$NN alignment is exactly 1.
  - *The PRH's own metric saturates on symmetric families under a checkable condition.*

- **C3 (finite, disjoint corpora).** Let $\varepsilon_a = \lVert \hat T_a - T_a\rVert_{op}$ be the estimation error.
  - Bounding $\varepsilon_a$ with matrix Bernstein under a Zipfian frequency profile is a technical milestone.
  - Davis–Kahan then gives $\lVert \sin\Theta(U_a, U_b)\rVert \le 2(\varepsilon_a + \varepsilon_b)/\delta$.
  - **No shared data is required, only a shared law.** This is H2: disjoint but mutually intelligible models.
  - The family eigengap $\delta$ grows with the number of bulk words coupled to the latent variable. So **one mechanism, collective control, gives both robustness (B2) and fast convergence (C3).**

- **C4 (ordering condition; blur theorem).** Equivariant distortions keep the basis but can reorder the spectrum. Reordering is the only population-level failure mode.
  - **Theorem target.** Suppose agent $a$ perceives $\tilde\theta = \theta + \eta$, with $\eta \sim \kappa_a$ symmetric and unimodal on $G$ (wrapped Gaussian, von Mises) and independent per token. In the linear-response regime (small PMI), $\alpha^a_k = |\hat\kappa_a(k)|^2\,\alpha_k$. Since $|\hat\kappa_a(k)|$ decreases in $|k|$, the order of the irreps is preserved whenever $\alpha$ is decreasing.
  - *Blur-type misperception is harmless. Multimodal distortion, like the hemisphere mixture of A4, is exactly what reorders.*

- **C5 (pooling theorem).** Suppose the agents' $B_a^\perp$ are independent with mean zero. Then, in linear response, the symmetry-breaking part of the pooled target shrinks like $\sqrt{\log|V|/A}$ in operator norm, where $A$ is the number of independent sources.
  - **Prediction (a refinement of the PRH):** at a fixed token count, more independent sources give higher cross-model alignment on symmetric families. Diversity matters, not just scale.

- **C6 (cross-modal; weakens the PRH's bijectivity assumption).** Suppose a second modality observes $\theta$ through an equivariant channel, such as images of seasons or satellite tiles of places.
  - In the multiplicity-free case, Schur's lemma forces the induced operator to act as a scalar $c_\rho$ on each irrep. Cross-modal alignment is then the C2 formula with $\alpha^X_\rho \propto |c_\rho|^2 \alpha_\rho$.
  - **Bijectivity is not needed.** It suffices that the channel is equivariant and that $c_\rho \neq 0$ on the leading irreps. A many-to-one, lossy observation channel is fine, provided it does not annihilate the leading irreps.

- **C7 (scaling with a ceiling).** $\mathrm{Align}(a,b) \approx \mathrm{CKA}_{\text{pop}}(\alpha^a,\alpha^b) - O\big((\varepsilon_a+\varepsilon_b)/\delta\big)$.
  - As scale grows, estimation noise falls and more irreps are resolved, so alignment rises, as the PRH observes.
  - It saturates at a **computable ceiling**. The ceiling equals 1 only when the two profiles are proportional, which depends on the objective $F$ and on the channel scalars $c_\rho$.
  - *Falsifiable in a way the PRH is not: it predicts the limiting alignment value for each family and each pair of model classes.*

### Stage D: communication (speech, hearing, nuance, audience)

- **D1 (error decomposition).** Speaker $S$ encodes $x\in\mathcal O$ (an assertion) or an intended listener action $b$ (a directive). Listener $L$ decodes with $E_L$ and with $\hat E_S$, its model of the speaker. Target bound:

  $$\text{error} \;\lesssim\; \underbrace{\min_O \lVert E_S - E_L O\rVert_W}_{\text{lexical; vanishes on families (Stage C)}} \;+\; \underbrace{\lVert E_S - \hat E_S\rVert}_{\text{audience model}} \;+\; \underbrace{\text{rate term}}_{\text{hearing is rate-limited}} .$$

- **D2 (nuance = water-filling over irreps).** Any $G$-invariant distortion of negative type on a Gelfand homogeneous space has a harmonic expansion with $w_\rho \ge 0$ (Schoenberg):

  $$d_c(x,\hat x) = \sum_\rho w_\rho(c)\,\lVert \Phi_\rho(x) - \Phi_\rho(\hat x)\rVert^2 .$$

  Under a Gaussian surrogate with per-irrep variance $\alpha_\rho$, the optimal rate–distortion trade-off is reverse water-filling:

  $$R(D) = \sum_\rho \frac{m_\rho}{2}\log^+\frac{w_\rho(c)\,\alpha_\rho}{\eta} .$$

  - **Nuance is the context dependence of $w(c)$.** "Let's meet next season" puts weight on $\rho_1$; "the deadline is the 14th" puts weight on high irreps. Lexical precision goes where the context-weighted variance clears the water line.
  - Embedding truncation at dimension $d$ is the special case of uniform weights and a hard dimension budget. So the month circle is the two-dimensional water-filling solution.

- **D3 (divergent categorization = aliasing).** Coarse categories are equivariant quantizers onto a subgroup. Example: months to seasons, $\mathbb Z_{12}\to\mathbb Z_4$, by averaging three-month blocks.
  - Block averaging sends the month harmonic $k$ to the season harmonic $k \bmod 4$ with gain $\left|\tfrac{\sin(\pi k/4)}{3\sin(\pi k/12)}\right|$:

    | $k$ | 1 | 2 | 3 | 4 | 5 |
    |---|---|---|---|---|---|
    | gain | 0.91 | 0.67 | 0.33 | 0 | 0.24 |

  - **Proposition:** two agents with different categorizations agree on the band below both Nyquist limits, with fidelity $1 - O(\alpha_3/\alpha_1)$. They cannot share distinctions above it. *Mutual intelligibility is agreement at low frequency; misperception lives at high frequency.*
  - Connects to information-bottleneck color naming (Zaslavsky et al., 2018), since hue is an approximate $U(1)$ family. In Gaussian IB, components switch on at critical $\beta$ values (Chechik et al., 2005); under symmetry they should switch on one irrep at a time.
  - **Prediction:** the lexical refinement of a symmetric domain proceeds irrep by irrep.

- **D4 (audience models: "what do you mean, *you people*?").** The listener infers a speaker type $\tau$ from performance-channel cues, then decodes with

  $$P_L(x\mid u) \propto \sum_\tau P(\tau\mid\text{cues})\,S_\tau(u\mid x)\,P_\tau(x).$$

  This is a Rational Speech Acts model (Frank & Goodman, 2012) with uncertainty over speaker type.
  - On $G$-families, Stage C makes the $S_\tau$ nearly identical, *except for relative phases between families*: "a December wedding" is warm or cold depending on $\tau$.
  - Off families, the $E_\tau$ differ in residual directions.
  - **The "*you people*" moment is a type-posterior event.** The listener's inferred $\tau$ selects an $E_\tau$ in which the phrase points at a group, whether or not the speaker's own $E_S$ does.
  - **Cants:** a shared $\tau$ means a shared residual codebook, which acts as Wyner–Ziv side information, so $R_{WZ}(D) \le R(D)$. This is the formal version of "efficient, expressive association alignments within the frame."

- **D5 (social-residual conjecture).** Train models on corpora from communities $\tau_1$ and $\tau_2$, and remove the best Procrustes fit on $G$-families. The residual:
  - (i) is nearly orthogonal to the family subspaces;
  - (ii) linearly predicts $\tau$;
  - (iii) concentrates on vocabulary heavy in the performance channel: register markers, in-group terms, politeness, slurs.

  *Convergence belongs to the content channel; plurality persists in the performance channel.*

### Stage E: language as an accumulation system

- **E1 (generational map).** $T_{t+1} = \beta\,T_{\text{world}} + (1-\beta)\,\Phi(T_t)$.
  - $\beta$ is the fraction of fresh, grounded speech.
  - $1-\beta$ covers imaginative excursions, retellings and synthetic text generated by models trained on $T_t$.
  - If $\Phi$ is equivariant in law, every iterate shares the $G$-basis, and $\beta$ only sets the radii at the fixed point.
- **E2 (collapse ordering).** Truncation and finite resampling inside $\Phi$ shrink small-eigenvalue irreps geometrically, and only $\beta$ replenishes them.
  - **Prediction:** under recursive training (Shumailov et al., 2024), radii collapse from high frequency to low, and the circle is the last structure to go.
  - Contrast Bayesian iterated learning (Griffiths & Kalish, 2007), which converges to the learners' prior. Grounding ($\beta>0$) pins the fixed point to the world, while $G$ pins the *shape* for every $\beta$.
- **E3 (what the limit is).** $T_\infty \approx F\big(\mathbb E_a[\Lambda_a K_{\text{world}} \Lambda_a^{\top}]\big)$: the world kernel seen through the *average* lexicalization channel.
  - It recovers the world's harmonic structure on every irrep whose average channel scalar is nonzero.
  - Shared equivariant biases ($B^G$) distort the radii but not the shape.
  - What nobody lexicalizes is lost.
  - *This is H3 with its scope stated: language accumulates the symmetric, lexicalized part of the world model.* Whether large models also learn the world's *dynamics*, not only its relational geometry, is a separate and harder question (compare Li et al., 2023).

---

## 5. Experiments (each tied to a prediction above)

| # | Setup | Prediction |
|---|---|---|
| X1 | word2vec, GloVe and small transformers trained on disjoint corpus shards | Family CKA matches the C2 formula computed from each model's own spectrum; mutual-$k$NN = 1 wherever $\alpha_1$ dominates |
| X2 | Northern- vs southern-hemisphere corpora, then mixtures with southern fraction $s$ | Odd seasonal harmonics scale as $1-2s$; seasonal words' phase relative to months differs by $\pi$; the month circle survives through calendar co-occurrence (A4) |
| X3 | Replace month tokens with season tokens in one corpus | Agreement on $k=1$ with the D3 gains; no agreement above Nyquist |
| X4 | Direct co-occurrence ablation (as in Karkada et al.), compared across agents | Basis unchanged; profile reshaped; leading-order shift $O(\lvert W\rvert/\lvert V_\theta\rvert)$ |
| X5 | Fixed token budget, varying number of independent sources | Alignment rises with the number of sources (C5) |
| X6 | Language vs vision on seasonal imagery and satellite tiles of places | Cross-modal CKA ≈ the profile cosine with channel scalars $c_\rho$ (C6) |
| X7 | Recursive train-and-generate loops | High irreps collapse first; the circle is the last to go (E2) |
| X8 | Community-split corpora (register, region) | The social residual is orthogonal to families and predicts community (D5) |
| X9 | Open LLM checkpoints across seeds, data orders and model families | Stepwise alignment during training (B4); seed variance tests self-averaging (B3) |
| X10 | Metacognitive and perceptual sensoria: affect words (Russell's 1980 circumplex) and hue words | Whether introspective and perceptual domains behave as approximate $U(1)$ families |

---

## 6. Open problems and risks

1. **Most vocabulary is not an exact $G$-family.** Without symmetry, C3-style convergence still holds for the eigenfunctions of the latent kernel, but objective-independence (A2) fails, because an entrywise $F$ changes the eigenvectors.
   - **Sharp question:** when is the eigenbasis of $f(M)$ the same for every $f$? Write $M=\sum_i v_i A_i$ over its level sets. Then $\{f(M)\}_f$ is simultaneously diagonalizable **iff the level-set indicator matrices $A_i$ pairwise commute**. Monotone $f$ suffice, since indicators of single values are differences of monotone functions.
   - Commutative association schemes give a natural sufficient condition. Group orbitals (Schurian schemes) are the main example, and on a single orbit they are commutative exactly when $(G,H)$ is a Gelfand pair.
   - So the exact condition for *objective-free* PRH convergence is combinatorial, and group symmetry is a special case.
   - Next steps: approximate versions of this criterion, and a model of the whole lexicon as "many small approximate families plus a residual."
2. **Approximate symmetry.** New Year pins the origin of $\mathbb Z_{12}$, "May" is polysemous, and years are tokenized into digits.
   - Symmetry-breaking terms also *fix the gauge*. **Prediction:** across models, the phase of the month circle relative to "New Year" and "cold" aligns. Sparse-autoencoder or neuron-level month features, however, are arbitrary rotations within the irrep block unless something pins them.
3. **Contextual representations.** Which layer and which pooling count as "the" representation? B3 covers any token-level functional, but self-averaging may vary by layer.
4. **The link from LLMs to PMI** is only approximate (it goes through the log-bilinear output layer). B3 is meant to remove the dependence on it.
5. **Rare words and Zipf tails** dominate the estimation error. They need reweighting before C3 holds with useful constants.
6. **PRH evidence is metric-sensitive.** C2 gives CKA and mutual-$k$NN in closed form, which allows a principled comparison of the two metrics on families.

---

## 7. Milestones

- **Paper 1, "Objective-free geometry":** A1–A3, B3, and open problem 1 (commutants, exchangeability, the level-set commutation criterion).
- **Paper 2, "Platonic convergence on symmetric families":** C1–C7 (closed-form alignment, rates with disjoint data, pooling, cross-modal convergence without bijectivity). Experiments X1, X4–X6, X9.
- **Paper 3, "Nuance and intelligibility":** D2–D4 (water-filling over irreps, aliasing between categorizations, audience models). Experiments X2, X3, X8, X10.
- **Paper 4, "Accumulation and collapse":** E1–E3. Experiment X7.

---

## References

- Chechik, Globerson, Tishby & Weiss (2005). Information bottleneck for Gaussian variables. *JMLR*.
- Diaconis, Goel & Holmes (2008). Horseshoes in multidimensional scaling and local kernel methods. *Annals of Applied Statistics*.
- Engels, Michaud, Liao, Gurnee & Tegmark (2024). Not all language model features are linear.
- Frank & Goodman (2012). Predicting pragmatic reasoning in language games. *Science*.
- Griffiths & Kalish (2007). Language evolution by iterated learning with Bayesian agents. *Cognitive Science*.
- Gurnee & Tegmark (2024). Language models represent space and time. *ICLR*.
- Huh, Cheung, Wang & Isola (2024). The Platonic Representation Hypothesis. *ICML*.
- Karkada, Simon, Bahri & DeWeese (2025). Solvable dynamics of self-supervised word embeddings and the emergence of analogical reasoning.
- Karkada, Korchinski, Nava, Wyart & Bahri (2026). Symmetry in language statistics shapes the geometry of model representations. arXiv:2602.15029 (ICML 2026).
- Kornblith, Norouzi, Lee & Hinton (2019). Similarity of neural network representations revisited. *ICML*.
- Levy & Goldberg (2014). Neural word embedding as implicit matrix factorization. *NeurIPS*.
- Li et al. (2023). Emergent world representations: exploring a sequence model trained on a synthetic task. *ICLR*.
- Marchetti, Hillar, Kragic & Sanborn (2024). Harmonics of learning: universal Fourier features emerge in invariant networks. *COLT*.
- Russell (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*.
- Shumailov et al. (2024). AI models collapse when trained on recursively generated data. *Nature*.
- Wyner & Ziv (1976). The rate-distortion function for source coding with side information at the decoder. *IEEE Transactions on Information Theory*.
- Zaslavsky, Kemp, Regier & Tishby (2018). Efficient compression in color naming and its evolution. *PNAS*.
- arXiv:2610.00647 (2026). Group-invariant statistics determine embedding geometry: harmonic analysis of representations from Bach to the night sky. *(Not read in full; cited for scope only.)*
