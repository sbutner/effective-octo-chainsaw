# Experimental Log
## 0. Summary of evidence status (read first)
- **The authors have run no experiments for this paper.** There are no new datasets, training runs, baselines, metrics or numerical results of our own.
- The paper is theoretical. Its evidence is (a) closed-form derivations stated in the idea, and (b) empirical findings already published in the cited anchor papers, reported below with attribution.
- Do **not** produce results tables, ablations or plots of our own measurements. Any figure must be a conceptual diagram or a plot of a closed-form function defined in the idea (e.g. the seasonal coarse-graining gains in S18 or the CKA lower bound in S25).
- Experiments listed in §3 are **pre-registered predictions** to be presented as future work / falsification tests, never as results.

## 1. Closed-form quantities that may be reported
- S18: coarse-graining months to seasons multiplies harmonic k by |sin(pi k/4) / (3 sin(pi k/12))|; for k = 1..5 the gains are 0.91, 0.67, 0.33, 0, 0.24.
- S4: with southern-hemisphere corpus share s, the k-th Fourier coefficient of every seasonal profile is multiplied by 1 - s + s(-1)^k; at s = 1/2 the odd harmonics vanish exactly.
- S25: for scalar nonnegative spectra with a shared leading irrep, CKA(a,b) >= sqrt((1 - tau_a)(1 - tau_b)), where tau is the spectral mass outside the leading irrep.
- S26: if D_a and D_b are conditionally independent given Omega, I(X_a;X_b) <= I(D_a;D_b) <= min{I(Omega;D_a), I(Omega;D_b)}.

## 2. Published empirical findings this paper builds on (prior work, not ours)
These were checked against the full texts of the cited papers. Attribute every number.

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

## 3. Pre-registered experiments (NOT run; predictions only)
| # | Setup | Prediction | Materials |
|---|---|---|---|
| X1 | Word embeddings and small transformers trained on disjoint shards | Family CKA matches the Plancherel formula (S10) | Karkada code: github.com/dkarkada/symmetry-stats-repgeom |
| X2 | Northern- vs southern-hemisphere corpora, and mixtures | Odd seasonal harmonics scale as $1-2s$ (S4) | Regional news, Wikipedia |
| X3 | Season tokens replace month tokens in one corpus | S18 gains; no agreement above Nyquist | Wikipedia |
| X4 | Deletion ablation, compared across agents | Basis fixed, radii shift (S6) | As in Karkada Fig. 4 |
| X5 | Fixed token count; vary the number and correlation of sources | Alignment tracks $A_{\text{eff}}$ (S13) | Multi-source corpora |
| X6 | Vision vs language on seasonal imagery, satellite tiles, sky | Cross-modal CKA predicted from Schur scalars (S14) | Storan's sky setup |
| X7 | Recursive training, replacing vs accumulating data | High irreps die first; accumulation plateaus (S22) | GM experiment 2 |
| X8 | Corpora split by community | Social residual behaves as in S20 | — |
| X9 | Training checkpoints and seeds | Alignment rises in steps (S8); seed variance tests S7 | Open model suites |
| X10 | Affect words and hue words | Do they behave as approximate $U(1)$ families? | PRH Fig. 8; Abdou et al. |
| X11 | Grounded vs random filtering at equal strength (GM experiment 1) | Strong collapse vanishes only under grounded filtering, which preserves per-irrep radii and $B^\perp_{\text{world}}$ | GM |
| X12 | Alignment during collapse | Cross-model CKA and mutual-$k$NN rise or hold while tail-sensitive grounded fidelity falls (S25) | X7 runs |
| X13 | The same families across languages | Month and number circles align across languages up to gauge, and $B^\perp_{\text{world}}$ pins the gauge (GM's translatability case) | Multilingual Wikipedia |
| X14 | Dates across self-training generations | Number of retained harmonics vs $n_{\text{eff}}$ and fidelity (S28) | Karkada Fig. 9 setup |

### Related program experiments (NOT run)
- **E-01: Latent vs surface diversity across model ensembles.** Design: Sample N frontier/open models on Infinity-Chat-style open prompts; compute delta_surface (style embeddings) and delta_latent (content embeddings with style regressed out); estimate effective N_e of the model ecosystem. Prediction: delta_surface >> delta_latent; effective N_e << number of models. Cost: low. Tests claims K35, K30, K26.
- **E-04: Migration-drift balance in synthetic training ecosystems.** Design: M small LMs trained iteratively on a pooled corpus with controllable source divergence delta, attention weights w (setting N_e), fresh-data rate mu, and verifier fraction v; track latent diversity and grounded probe accuracy. Prediction: Stationary diversity fits 4 N_e m/(1+4 N_e m) with m increasing in delta; collapse at low N_e*delta unless v>v*. Cost: low. Tests claims K31, K30, K27.

## 4. Claim status (do not overstate)
| Claim | Status | Meaning |
|---|---|---|
| K1 Snapshot world model from statistical geometry | conjecture | plausible but unproven; may be false |
| K3 Quinean indeterminacy = identifiability class | new | new theorem target; at most a proof sketch exists |
| K4 Convergence vs collapse | new | new theorem target; at most a proof sketch exists |
| K5 Retrospective verification of Firth | implicit | follows from published results with little work |
| K30 C3 restated: latent-weighted collapse | conjecture | plausible but unproven; may be false |

## 5. Reference verification status
`checked` = verified against a primary index page; `from-memory` = not yet verified, so confirm via literature search before citing details.

- `huh2024` [checked-repo]: Huh, M.; Cheung, B.; Wang, T.; Isola, P. (2024). *The Platonic Representation Hypothesis*. ICML; arXiv:2405.07987
- `karkada2026` [checked-repo]: Karkada, D.; Korchinski, D.; Nava, A.; Wyart, M.; Bahri, Y. (2026). *Symmetry in language statistics shapes the geometry of model representations*. ICML 2026; arXiv:2602.15029
- `storan2026` [checked-repo]: Storan; Tolias; Miolane (2026). *Group-Invariant Statistics Determine Embedding Geometry*. arXiv:2610.00647
- `shai2024` [from-memory]: Shai, A. S.; Marzen, S. E.; Teixeira, L.; Oldenziel, A. G.; Riechers, P. M. (2024). *Transformers Represent Belief State Geometry in their Residual Stream*. NeurIPS
- `roeder2021` [from-memory]: Roeder, G.; Metz, L.; Kingma, D. P. (2021). *On Linear Identifiability of Learned Representations*. ICML
- `marconato2025` [checked]: Marconato, E.; Lachapelle, S.; Weichwald, S.; Gresele, L. (2025). *All or None: Identifiable Linear Properties of Next-token Predictors in Language Modeling*. AISTATS (PMLR 258); arXiv:2410.23501
- `levy2014` [from-memory]: Levy, O.; Goldberg, Y. (2014). *Neural Word Embedding as Implicit Matrix Factorization*. NeurIPS
- `arora2016` [from-memory]: Arora, S.; Li, Y.; Liang, Y.; Ma, T.; Risteski, A. (2016). *A Latent Variable Model Approach to PMI-based Word Embeddings*. TACL
- `li2023othello` [from-memory]: Li, K.; Hopkins, A. K.; Bau, D.; Viegas, F.; Pfister, H.; Wattenberg, M. (2023). *Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task*. ICLR
- `gurnee2024` [from-memory]: Gurnee, W.; Tegmark, M. (2024). *Language Models Represent Space and Time*. ICLR
- `abdou2021` [from-memory]: Abdou, M. et al. (2021). *Can Language Models Encode Perceptual Structure Without Grounding? A Case Study in Color*. CoNLL
- `quine1960` [from-memory]: Quine, W. V. O. (1960). *Word and Object*. MIT Press
- `peirce1878` [from-memory]: Peirce, C. S. (1878). *How to Make Our Ideas Clear*. Popular Science Monthly 12
- `jiang2025hivemind` [checked]: Jiang, L. et al. (2025). *Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond)*. NeurIPS Datasets & Benchmarks (oral); arXiv:2510.22954
- `harris1954` [from-memory]: Harris, Z. S. (1954). *Distributional Structure*. Word 10(2-3)
- `firth1957` [from-memory]: Firth, J. R. (1957). *A Synopsis of Linguistic Theory 1930-1955*. Studies in Linguistic Analysis
- `shumailov2024` [from-memory]: Shumailov, I.; Shumaylov, Z.; Zhao, Y.; Papernot, N.; Anderson, R.; Gal, Y. (2024). *AI Models Collapse When Trained on Recursively Generated Data*. Nature 631
- `alemohammad2024` [from-memory]: Alemohammad, S. et al. (2024). *Self-Consuming Generative Models Go MAD*. ICLR
- `gerstgrasser2024` [checked-repo]: Gerstgrasser, M. et al. (2024). *Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data*. arXiv:2404.01413
- `schaeffer2025` [checked]: Schaeffer, R.; Kazdan, J.; Arulandu, A. C.; Koyejo, S. (2025). *Position: Model Collapse Does Not Mean What You Think (ICML 2026: Multiple Definitions & Unrealistic Assumptions of Model Collapse Distract from Real World Threats)*. arXiv:2503.03150; PMLR 306
- `guo2024diversity` [from-memory]: Guo, Y. et al. (2024). *The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text*. NAACL Findings
- `march1991` [from-memory]: March, J. G. (1991). *Exploration and Exploitation in Organizational Learning*. Organization Science 2
