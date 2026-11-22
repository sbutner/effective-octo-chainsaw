# The Spine: a formal theory of knowledge production and transmission

*Draft v0.1 · 2026-11-21 · branch `claude/determined-davinci-3341ib`*

> **Superseded in part, 2026-11-22.** [`foundations.md`](foundations.md) replaces §1 and layers L0 to L3. Layers L4 to L8 are kept, but frozen until task S-02 closes.

## 0. The reframing

The project started from three conjectures about LLMs: they learn a snapshot world model; they cannot improve its fit; collapse is inevitable when sources converge. It now has a broader object:

> **A single formal model of how knowledge is produced, selected, stored, copied and lost.** It is built from mathematical primitives and information-theoretic first principles. It is instantiated at every scale from a single reading to a literary canon. It uses LLMs as the first experimental apparatus large enough to test, after the fact, claims that fundamental fields have argued about for centuries.

LLMs drop from *the subject* to *one regime of the model and one instrument for testing it*. The paradigm case of retrospective verification is **Firth (1957) and Harris (1954)**. The distributional hypothesis was a conjecture in linguistics. Sixty years later word2vec showed it is a theorem about matrix factorization (Levy & Goldberg 2014), and LLMs showed it is a working technology. Karkada et al. (2026) proved the world-symmetry version. **The distributional hypothesis was itself a sleeping beauty, woken by a hub that arrived late** (§L4). That is an instance of the theory it helped found.

The existing documents in `explorations/` become components of this spine:

| Existing document | Role in the spine |
|---|---|
| *Grounded Misprision* (GM; T1–T10, C11–C30) | **The selection core**: layers L2, L4 and L5 at the scale of an agent and a corpus |
| *Symmetry, Geometry, Convergence* (outline v1; S1–S31) | **The symmetric sector**: layer L3, where everything is computable exactly |
| *One Selection Law* | **The behavior stage**: layer L8, post-training and verifiers; the Unified Channel Law |
| Lean drafts v1 and v2 | **The lattice skeleton**: layer L0 algebra (closure operators, `InfoLattice`) |
| This conversation (new IDs K1–K60) | **The ecology and value layers**: L4–L7, plus the L8 adjudication of debates |

---

## 1. Design principles

1. **One state, many scales.** The same variables describe a reader, a classroom, a canon and a training run. A scale is a choice of what counts as an agent and what counts as the archive.
2. **Every arrow is a channel.** Every relation (perceives, writes, copies, reads, cites, trains on, verifies) is a Markov kernel, so the data-processing inequality (DPI) applies everywhere it is not explicitly broken.
3. **Grounding is an accounting identity, not a metaphor.** Track $\mathcal G=I(\Omega;\cdot)$ (grounded information) separately from explicit content $\mathcal X$ (what can be stated or computed). Most debates mix the two up.
4. **Selection decides the sign.** Variation is unavoidable (GM T1). Whether it helps or harms is set by what it is tested against (GM T3).
5. **The world is stateful and partly reflexive.** $\Omega_t\neq\Omega_{t+1}$, and part of $\Omega$ is made of what agents do and write. Their internal models are hidden and enter $\Omega$ only through those actions. This is what breaks the clean DPI chain and what makes canons retroactive.
6. **Status tags are mandatory.** Every claim is tagged Known, Implicit, New, Conjecture or Test (outline v1's convention), and every citation is tagged checked or from memory.

---

## 2. The layers

Each layer lists its **primitives**, its **laws** (with claim IDs), the **fields it connects**, and its **anchor literature**. Full entries are in `data/`.

### L0. Mathematical primitives

| Object | Formal type | Notes |
|---|---|---|
| World $\Omega$ with law $P$ and state process $\omega_t$ | Probability space; stochastic process, stateful (not ergodic in general) | GM primitive 1. Statefulness: K40 |
| Symmetry $G$ acting on $\Omega$ | Group action preserving $P$ (in general only approximately) | Outline S1–S8 |
| Agents $a\in A$ | Tuple $s_a=(b_a,S_a,\kappa_a)$: belief, store, context | GM primitive 3 |
| Channels | Markov kernels $K:X\to\Delta(Y)$ | Sensoria $\sigma_a$, speech $\pi$, reading $r$, copying $\phi$, training, verifying |
| Archive $\mathcal A_t$ | Multiset of forms with provenance and copy counts | GM primitive 8; K20 |
| Attention and citation graph $\Gamma_t$ | Directed graph with weights $w$; growth kernel | K24–K28 |
| Hypothesis or reading space $H$ | Space of *procedures* (GM: meanings are instructions), with a running cost | GM A7, A9 |
| Information lattice | Join-semilattice with a closure operator cl | Lean v1; outline S30–S31 |
| Interpreter class | Computability class (finite, TC⁰, universal) | GM T5, T7; *One Selection Law* |

### L1. First principles: laws of information and computation

| Law | Statement | Role |
|---|---|---|
| DPI | $X\to Y\to Z\Rightarrow I(X;Z)\le I(X;Y)$ | Every closed-loop result (GM T2, T4.2; K10) |
| Rate–distortion | $D(R)>0$ when the source rate exceeds $R$ | Misprision is unavoidable (GM T1) |
| Sufficiency and belief states | An optimal predictor encodes the posterior over hidden states | World models from prediction (K1, K2) |
| Identifiability | Representations are fixed up to an equivalence class | Quine made formal (K3) |
| Kolmogorov complexity and compression progress | $K(x\mid M)$; interestingness = $-\frac{d}{dt}K_t(x)$ | Literature versus pulp (K45–K48) |
| Logical depth | Computation needed to unfold $x$ from its shortest description | The analytic residue (K13) |
| Error threshold (Eigen) | $K\lesssim\ln\sigma/\varepsilon$ | Fidelity and the canon (GM T6; K21) |
| Bayes risk | $F(\theta)\le F^\*(D)$ for any estimator that depends only on $D$ | The reasoning-gap bound (K11) |
| Undecidability | The deductive closure of a corpus is r.e. but not decidable | Inexhaustibility (GM T7) |

### L2. Reading, misprision and selection: the GM core

GM T1 (unavoidable misprision), T2 (closed loop), T3 (pool + select − drift), T4 (grounding dichotomy), T10 (internal tests). New here:

- **K10.** C2 restated as the closed-system theorem $I(\Omega;\theta_{\text{post}})\le I(\Omega;D)$, with explicit content free to rise. (Known/Implicit; the same claim as GM T2 and the Unified Channel Law.)
- **K11.** The reasoning gap $F^\*(D)-F(\theta)$ is the generation–verification gap of Song et al. (2025). Sharpening (Huang et al. 2025) closes it without adding $\mathcal G$. (New identification.)
- **K12.** RL against the model's own support narrows coverage (Yue et al. 2025), and distillation from an independent model adds $\mathcal G$. The two map onto GM's select and pool terms. (Test.)
- **K13.** Two sources of inexhaustibility: *depth*, internal to the text, which is the analytic residue; and *sensitivity*, through the reader, a fixed probe read against a changing $\Omega_t$. This refines GM T7's "two sources". (New.)

### L3. Language and geometry: the distributional layer

Outline S1–S31; GM T8 and T9. New here:

- **K1.** World models from the statistical geometry of language (C1): an optimal next-token predictor identifies $s(\Omega)$, the part of $\Omega$ that language makes visible, up to an identifiable equivalence class. (Conjecture. Route: belief-state sufficiency (Shai 2024), linear identifiability (Roeder 2021; Marconato 2025), PMI geometry (Levy & Goldberg 2014; Arora 2016).)
- **K2.** The snapshot is **time-integrated**: a model without time indexing learns a composite of the states $\Omega_t$ across the corpus's history, not $\Omega_T$. (Conjecture; Test via Lazaridou 2021, Cheng 2024.)
- **K3.** Quine's indeterminacy equals the identifiability class, and "All or None" (Marconato 2025) separates determinate linear properties from indeterminate ones. (New identification.)
- **K4.** Convergence versus collapse: δ→0 together with rising $\mathcal G$ is Peircean convergence; δ→0 together with falling $\mathcal G$ is collapse. This separates the PRH from homogenization. (New; formalized for the symmetric sector in outline S25–S26.)
- **K5.** Retrospective verification of Firth: the distributional hypothesis has the status of a theorem, *conditional on* GM A14 (reference anchors distribution). (Implicit.)

### L4. Media, archives and the canon network

- **K20.** The replication filter: a form is copied iff its perceived value exceeds the cost of copying, $v>c$. The canon is what cleared the threshold repeatedly. (Model definition.)
- **K21.** Media regimes (oral, manuscript, print, digital, generative) are points in the space of cost $c$, fidelity $\varphi$ and literate population $n$. This extends GM T6 and C26–C27. (Implicit.)
- **K22.** When $c$ falls, the filter moves from production to attention (Simon 1971). Survival rises while the chance of being rediscovered falls (Chu & Evans 2021). (Conjecture with partial evidence.)
- **K23.** Evenness of survival: works with few copies are lost first (Kestemont 2022). This is the archival analogue of tail loss in model collapse. (Known empirically; the formal link is New.)
- **K24.** The canon is a growing network with fitness × degree attachment (Bianconi–Barabási) and **edges drawn backward in time**. Eliot's "ideal order modified by the new" and Borges's "each writer creates his precursors" describe the same thing. (New formalization.)
- **K25.** A sleeping beauty requires (i) survival through the filter, (ii) a later hub with high fitness that attaches to it, and (iii) a world state $\Omega_t$ in which it resonates. Cases: Hopkins with Bridges and Leavis; Beowulf with Tolkien; Mendel; Firth with word2vec. (Conjecture; Test via Ke et al. 2015.)
- **K26.** Effective population of sources: $N_e=1/\sum_i w_i^2$ over attention shares. Diversity is lost at a rate set by $N_e$, not by how many sources there are or how much they produce. (New application of standard population genetics.)
- **K27.** Hubs break the wisdom of crowds (Golub & Jackson 2010). LLMs are the largest hubs in history. (Known plus Implicit.)
- **K28.** Frames change attachment: Tolkien's 1936 lecture moved Beowulf from philological quarry to poem. Literariness is a property of the reading frame, and reframing is an edge-rewiring event in $\Gamma$. (New.)

### L5. The population ecology of knowledge

- **K30.** C3 restated: collapse is governed by **latent** diversity weighted by effective population, $N_e\cdot\delta_{\text{latent}}$, relative to a mutation–drift threshold, together with the verification fraction $v$. It is not governed by volume or cost. (Conjecture; this is the central ecological claim.)
- **K31.** Diversity among sources acts as migration $m$. Equilibrium heterozygosity is $\approx 4N_em/(1+4N_em)$, and δ→0 implies $m\to0$, which implies fixation. (New mapping; the proof is standard once the mapping holds.)
- **K32.** Self-consuming chains converge to the learners' prior (Griffiths & Kalish 2007). Model collapse is **the prior gradually replacing the evidence**. (Known, re-applied.)
- **K33.** Rogers' paradox is C2 and C3 in evolutionary anthropology. There is a minimum verification fraction $v^\*$ below which $\mathcal G$ decays in a changing world. Critical social learners (Enquist et al. 2007) raise the threshold. (Known plus a new identification.)
- **K34.** Epistemic vigilance checks testimony against the reader's own *prior*, not against $\Omega$. It guards against noise (madness) but not against a coherent consensus error (pulp or collapse). (New.)
- **K35.** Surface versus latent diversity: $I(\text{source};\text{style})\gg I(\text{source};\text{content})$ is "clowns in different makeup." δ must be measured in latent space. (New; evidence: Artificial Hivemind, Jiang et al. 2025.)
- **K36.** Two readings of homogeneity: convergence on each other (collapse) or on an invariant $\Omega$ (the human condition). K4 is the test. (New.)
- **K37.** Information cascades (Bikhchandani et al. 1992) are the limiting case where $v\to0$ under sequential testimony. This links to GM C13. (Known.)

### L6. Institutions, pedagogy and careers

- **K40.** The stateful, reflexive world: $\Omega_{t+1}$ depends on $\theta_t$. Change in fit splits as $\Delta F=\Delta F_{\text{learn}}+\Delta F_{\text{perform}}$ (learning versus the world conforming), following performative prediction (Perdomo et al. 2020). (New application; the second term has not been estimated for LLMs.)
- **K41.** Co-collapse: human sources lose diversity toward the models (Kobak 2025; Yakura 2024; Doshi & Hauser 2024; Padmakumar & He 2024; Hao et al. 2026). (Test, with early evidence.)
- **K42.** Pedagogy as error correction: when replication is noisy, cultures invest in fidelity (internalization). When fidelity is cheap, they invest in exploration. This is Eigen's threshold applied to curricula. (Conjecture.)
- **K43.** A 2×2 of institutions: conservation versus exploration crossed with grounded versus ungrounded. The four cells: apprenticeship, the eight-legged essay (pulp), science, and ungrounded novelty (madness). (Typology.)
- **K44.** A third phase of pedagogy: when composing is nearly free, the scarce capacities are verification and judgment. Prediction: assessment moves back toward oral examination and toward verification tasks. (Conjecture.)
- **K38.** March (1991): learning slowly from the organizational code preserves the diversity the code needs. This is C3 thirty years early. (Known, re-applied.)
- **K39.** Careers as generators: the Q model (Sinatra 2016) is a stationary generator plus luck. Hot streaks start with exploration followed by exploitation (Liu 2021). Exploration is migration; exploitation is sharpening. **Prediction: sharpening alone gives no hot streaks.** Yue et al. (2025) find the machine analogue. (New identification.)

### L7. Value, interpretation and pathology

- **K45.** Literature versus pulp: a text's value is the compression progress it sustains *over rereadings and readers*. Pulp gives a single burst; literature does not run out. (New formalization, after Schmidhuber 2009.)
- **K46.** Literariness is relational: a property of the pair (text, interpretive community). (Fish 1980; Herrnstein Smith 1988. Formalized.)
- **K47.** Jauss's aesthetic distance is $\mathrm{KL}(\text{text}\,\|\,\text{horizon})$, and "culinary" art is distance near zero. Distance fades as the horizon moves. (New formalization of Jauss 1970.)
- **K48.** A self-consuming chain converges to pulp, meaning to genre (K32 plus K47). (Conjecture; this is GM C20 restated.)
- **K49.** Aristotle's "contrary to expectation yet on account of one another": improbable under the prior, yet with a short description under the text's own code. The bibliometric correlate is Uzzi et al. (2013). (New formalization.)
- **K50.** Genius and madness: both are large deviations $d=\mathrm{KL}(\text{output}\,\|\,\text{consensus})$. Genius has high $I(\Omega;\text{output}\mid\text{consensus})$; madness has near-zero. Hallucination is the formal analogue of madness. (New.)
- **K51.** Two kinds of genius: analytic (mining the reasoning gap; possible in a closed system) and synthetic (adds $\mathcal G$; impossible in a closed system). (New.)
- **K52.** Novelty, transience and resonance (Barron et al. 2018) give an operational test that separates genius from madness and literature from pulp. (Test.)
- **K53.** Performativity of either sign: genius pulls $\Omega$ toward its deviation and raises δ (Wordsworth's "creating the taste"). Consensus-tuned LLMs pull $\Omega$ toward the mode and lower δ. (New.)
- **K54.** Gaslighting is the adversarial limit: the precision placed on one's own sensoria is pushed toward 0, so beliefs track the adversary. It is the mirror image of psychosis, which places too much precision on one's own signals. Calibration lies between, and genius is calibration plus the willingness to stand against consensus. (New formalization.)
- **K55.** Orwell's archive: an adversary who controls $\mathcal A_t$ in a stateful world controls future $\theta$. This is collapse engineered on purpose. (New.)
- **K56.** Sycophancy is the model as gaslighting victim, weighting testimony over its own evidence (Sharma et al. 2024). Confident hallucination is the model as perpetrator. (New identification.)
- **K57.** Literature and art are a seed bank: institutions that preserve deviation *without* requiring the world to ratify it first. They hold δ above zero. Science preserves deviation *with* that requirement. (New.)

### L8. LLMs as instruments: retrospective verification

LLMs are the first apparatus in which every variable of the spine can be manipulated: corpus $D$, archive policy, selection regime, verifier, $N_e$, $v$ and the reflexivity $r$. `data/debates.json` lists 21 long-standing debates together with what LLM evidence currently says about each and what the spine predicts. The headline cases:

| Debate | Retrospective verdict | Status |
|---|---|---|
| Distributional hypothesis (Harris, Firth) | Confirmed as a theorem about structure (K5) | Strong |
| Structuralism (Saussure) | Relational geometry suffices for much semantic structure | Strong, partial |
| Symbol grounding (Harnad, Searle, Bender & Koller) | Meaning from form is possible as a *state* and impossible as a *process* (GM T8 with T2) | Reframed |
| Indeterminacy (Quine) | The identifiability class makes it formal (K3) | Formalized |
| Empiricism versus rationalism | The reasoning gap is real and bounded by $F^\*(D)$ (K10–K12) | Strong evidence |
| Testimony (Hume, Reid, Coady) | An LLM is a pure testimony reasoner; aggregation can exceed every individual source only when δ>0 | Formalized |
| Rogers' paradox | Model collapse is a Rogers chain | Strong analogy, testable |
| Mimesis (Plato, *Republic* X) | Copies of copies lose their tails first | Strong |
| Mill on diversity of opinion | Homogenization measurably lowers collective novelty | Early evidence |
| Jauss, culinary versus art | Aesthetic distance is measurable as KL from the genre prior | Test |
| Convergent realism (Peirce; the PRH) | Convergence counts as evidence only across conditionally independent channels (outline S26) | Formalized |

---

## 3. The state vector and the master relations

At every scale the spine tracks:

$$\Sigma_t=\big(\mathcal G_t,\ \mathcal X_t;\ c,\ \varphi,\ N_e,\ \delta_{\text{latent}},\ \delta_{\text{surface}},\ v,\ r,\ \lambda\big)$$

where $\lambda$ is GM's ratio of test power to untested retention.

**Candidate master relations** (to be proved or refuted, in order of priority):

1. **Unified Channel Law** (*One Selection Law*; GM T2/T4; outline S26):
   $I(\Omega;\Theta_t,Y_t)\le I(\Omega;D_t)+I(\Omega;E_{\text{ver}}\mid D_t)$, under the Markov condition $\Omega - (D_t,E_{\text{ver}}) - (\Theta_t,Y_t)$ (check `MR1/main`; the verifier term is load-bearing). The T4.2 condition $\xi\perp\Omega\mid D$ (HANDOFF §4.1) belongs to GM T4.2, not to MR1.
2. **The selection identity** (GM T3): $\mathbb E[\Delta L]=\Delta_{\text{pool}}+\Delta_{\text{select}}-\Delta_{\text{drift}}$, with a threshold $\lambda^\*$.
3. **Mutation–migration–drift–selection balance** (K30–K31): the stationary latent diversity $H^\*(N_e,m,\mu,v,\lambda)$. Collapse is $H^\*\to0$.
4. **Performative decomposition** (K40): $\Delta F=\Delta F_{\text{learn}}+\Delta F_{\text{perform}}$.
5. **Sustained compression progress** (K45): $\mathcal L(x;R)=\lim_{T\to\infty}\sum_{t\le T}\big[K_{t-1}(x\mid R_t)-K_t(x\mid R_t)\big]$ over a population of readers $R_t$ whose states change. Pulp has finite $\mathcal L$; literature has $\mathcal L$ diverging.

**Historical regimes as trajectories of Σ** (from the conversation; to be estimated, see `data/tasks.json` Q-07):

| | c | N_e | v | δ_latent | r |
|---|---|---|---|---|---|
| Oral | high | local, many | embedded in practice | high across communities | low |
| Manuscript | very high | few | low (textual authority) | low within elites | low |
| Print | medium | growing | rising (science) | rising | medium |
| Digital | ≈0 | power-law | mixed | surface ↑, latent ? | high |
| Generative | ≈0, including composition | ≈ number of frontier models | falling | surface high, latent low | very high |

The thesis: **the generative regime is the first in which every parameter moves toward collapse at once** (K30, K41).

---

## 4. Mapping the whole conversation onto the spine

| Conversation item | Layer | IDs |
|---|---|---|
| C1: snapshot world model from statistical geometry | L3 | K1, K2, K3, K5; outline S1–S8; GM T8 |
| C2: cannot increase fit | L2 | K10–K12; GM T2, T4; Unified Channel Law |
| C3: collapse as source distance → 0 | L5 | K30–K32; GM T9; outline S22, S25 |
| Convergence versus collapse (PRH tension) | L3, L5 | K4, K36; outline S25–S26 |
| Symbol grounding, Quine, Wittgenstein, Saussure, Firth | L3, L8 | K3, K5; D1–D6 |
| Hume, Kant and analytic/synthetic; testimony | L1, L2 | K10, K11, K51; D7, D8 |
| Plato, Heidegger's *Gerede*, Baudrillard, Benjamin | L5, L7 | K32, K48; D10 |
| Mill, Davidson's triangulation, Condorcet | L5 | K26, K27, K31; D11 |
| Literature versus pulp; frame-dependence | L7 | K45–K49; GM C18–C20 |
| Genius versus madness | L7 | K50–K53 |
| A stateful W; reflexivity; co-collapse | L6 | K2, K40, K41 |
| Jauss, Barthes, Shklovsky, Borges, Calvino | L7, L4 | K24, K28, K47 |
| The material replication filter | L4 | K20–K23 |
| Pedagogy: trivium, eight-legged essay, peer review | L6 | K42–K44 |
| Science of science: Q model, hot streaks, disruption | L6 | K39; Park 2023; Hao 2026 |
| Preferential attachment; Hopkins, Eliot, Beowulf, Tolkien | L4 | K24–K28 |
| "All clowns in different makeup" | L5 | K35, K36 |
| Stochastic repeaters; gaslighting | L5, L7 | K33, K34, K54–K56 |
| Retrospective verification of Firth | L8 | K5; D1 |

---

## 5. What would break the spine

- **No conditional independence anywhere.** If no human channel is conditionally independent of the corpus given $\Omega$ (strong textualism, or Derrida's "no outside-text"), then $\mathcal G$ is undefined and L2 and L5 lose their content. *Test:* a held-out grounded probe that improves only with fresh observation.
- **Collapse of diversity does not follow $N_e\cdot\delta_{\text{latent}}$.** If diversity loss tracks raw volume or cost instead, K30 is false.
- **Sustained compression progress does not separate the canon from pulp.** If $\mathcal L$ is uncorrelated with long-run critical attention once survival is controlled for, K45 is false.
- **Sharpening produces hot streaks.** If pure exploitation (RLVR) produces breakthroughs beyond the base model's coverage, K12 and K39 are false.
- **Gaslighting and psychosis do not mirror each other.** If precision-weighting accounts are wrong, K54 falls back to a mere analogy.
