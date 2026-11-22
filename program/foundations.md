# Foundations: the world, language and the generative agent

*v0.1 · 2026-11-22 · Approved by the human 2026-11-22. Replaces spine §1–L3 and the rung ladder in `formalization.md`. The claims are filed by task S-01.*

## 0. Why start again

The formalization plan grew by postulate. It gave the episode four fields, the graph eleven node types and the notation 140 symbols before any result needed them. Two contradictions came from that: the world held hidden models, and joint attention arrived one rung before its referent.

This draft starts from the two ends of the project at once:

- **The world end.** How does language come to carry the structure of the world?
- **The generative-agent end.** What does a model trained only on language know about the world, and what does its output do to the world and to language?

The aim is the smallest frame in which both ends are theorems about the same objects. Category theory supplies the frame, because the questions are about which maps factor through which objects. Group theory supplies the constraints, because what a learner can recover is fixed up to a symmetry.

Every claim is tagged Known, Implicit, New, Conjecture or Test, as in the spine. Every citation in this draft is from memory unless marked otherwise. §8 lists them for checking.

## 1. Three constraints, read off molecular biology

Molecular biology is the one field where a code, a population of readers, randomness and selection have been worked out together with mathematical rigor. Each of its lessons below names a formal correspondence. The column "Strength" says whether the correspondence is an identity, the same theorem in two settings, or only an analogy.

| Biology | Language | Generative agent | Formal correspondence | Strength |
|---|---|---|---|---|
| The genome plus ribosome is universal: chemical reaction networks are Turing complete with small error (Soloveichik et al. 2008) | Recursive syntax: infinite use of finite means | Transformers with a scratchpad are Turing complete (Pérez et al. 2019; Merrill and Sabharwal 2024) | All three compute every computable kernel | Same theorem |
| The genetic code is a frozen accident. Codon assignment is arbitrary, but it is shared and fixed by history | The arbitrariness of the sign | Token ids and internal coordinates are arbitrary | A choice of element in a permutation group, fixed by a population's history | Same theorem (§4.4) |
| Homochirality. Prebiotic chemistry is racemic, life is one-handed. A fluctuation was amplified by autocatalysis (Frank 1953; Soai 1995) | Conventions: one word, one word order, one side of the road per community | One model's idiolect among many equally good optima | Spontaneous breaking of a symmetry of the dynamics, through a pitchfork bifurcation | Same theorem (§4.4) |
| Residue co-variation across a protein family reveals 3D contacts (direct coupling analysis; Morcos et al. 2011). Protein language models learn structure from sequence alone (Rives et al. 2021) | Firth: co-occurrence reveals meaning | Word embeddings and LLM geometry mirror world structure (Karkada 2026; Huh 2024) | Pairwise statistics of a sequence ensemble encode a hidden constraint structure because selection coupled the two | Same theorem (§4.2, §5.1) |
| Natural selection | Uptake: what readers keep, cite and repeat | Training on filtered data; RL from verifiers | The discrete replicator equation is Bayes' rule with fitness as likelihood (Harper 2009; Shalizi 2009) | Identity |
| The error threshold: information is lost when copying error beats selection (Eigen 1971). Muller's ratchet in small asexual populations | Drift of oral tradition; canons decaying when nobody tests them | Model collapse under recursive training (Shumailov 2024) | A fidelity threshold on a replication–selection process (GM T6) | Same theorem (§5.3) |
| A ligand has no meaning in itself. Acetylcholine contracts skeletal muscle and slows the heart | Meaning is the response the receiver computes | The model's output means what its readers do with it | Meaning is a morphism into the receiver, which depends on its hidden state | Analogy, made formal in §3.3 |

The rows sort into three constraints, plus one non-constraint:

1. **Universality is not a constraint.** Capacity is unbounded in all three systems. No result may rest on an expressivity bound. Every limit must come from one of the three constraints below. GM T5 and T7 (interpreter class) stay as refinements, not as the foundation.
2. **Information.** What reaches an object is bounded by what reaches the objects it factors through (the data-processing inequality).
3. **Symmetry.** What a learner can recover is fixed only up to a group. Only invariants of that group are observable.
4. **Selection.** Random variation is shaped by statistics. Which structures are probable is decided by conditioning on outcomes.

## 2. The ambient category

**Known.** Take $\mathsf{Stoch}$: objects are standard Borel spaces (finite sets in every toy model), morphisms are Markov kernels, and composition is the Chapman–Kolmogorov sum. It is a Markov category (Fritz 2020). A *state* of $X$ is a kernel $1\to X$, that is, a probability law. Conditional independence, sufficiency and the data-processing inequality are all statements inside the category (Fritz 2020).

**Cost (New, one line).** A cost is a functor $c$ from $\mathsf{Stoch}$ to the additive monoid $(\mathbb R_{\ge0},+)$. It satisfies $c(g\circ f)=c(f)+c(g)$, $c(f\otimes g)=c(f)+c(g)$ and $c(\mathrm{id})=0$. This is the single cost per channel use, and it composes.

**Symmetry (Known).** A group $G$ acts on an object by kernels. $\mathsf{Stoch}^G$ has $G$-objects and equivariant kernels. An equivariant kernel sends invariant states to invariant states, which is outline S1 stated as functoriality.

## 3. The primitives

There are four. Everything after this section is derived from them.

### 3.1 The world

**P1.** An object $\Omega$ of interactions with a state $P$ and a group $G$ of automorphisms that preserve $P$. Interactions are events and what agents do and write. The law is symmetric and a realization is not: $P$ is $G$-invariant, while a sampled history $\omega$ generally is not. This is the chirality lesson. The ensemble keeps the symmetry, and each world breaks it.

### 3.2 Language

**P2.** A finite vocabulary $V$ and the free monoid $V^*$ of strings under concatenation. Speaking is a kernel $\pi:\Omega\to V^*$, and a corpus law is the state $D=\pi\circ P$. Reading is a kernel $r$ out of $V^*$.

The free monoid is the one piece of structure language adds. It is what lets finite means compose without bound. A sentence's grammar is a further structure on $V^*$. Compositional distributional semantics already treats it as a functor from a grammar category to vector spaces (Coecke, Sadrzadeh and Clark 2010). That stays out of the foundation until a result needs it.

### 3.3 Agents

**P3.** An agent is a parametrized kernel in the sense of the $\mathrm{Para}$ construction (Fong, Spivak and Tuyéras 2019; Capucci et al. 2021). It is a pair $(\Theta,f)$ with $f:\Theta\otimes X\to Y$. Its interface is $X\to Y$. Its parameter $\theta\in\Theta$, the internal model, is hidden: composing agents composes interfaces and keeps every parameter private. Learning is a kernel that updates $\theta$ from the interface's history.

This makes "internal models are hidden" a structural fact. Two agents whose parameters differ by a reparametrization, an isomorphism of $\Theta$ that leaves $f$ unchanged, cannot be told apart by any interaction. So only invariants of the parameter are observable: the kernel the agent induces, and the gauge-invariant functions of its representations (Gram matrices, CKA). This is the second gauge in §4.3.

A **grounded agent** has an input $\sigma_a:\Omega\to O_a$, its sensorium, that does not factor through $V^*$. A **generative agent** is one whose every input from $\Omega$ factors through $V^*$.

### 3.4 Selection

**P4.** Selection is conditioning on an outcome. A fitness $w:\Omega\to[0,\infty)$ reweights a state, $P\mapsto wP/\langle w,P\rangle$. On a population of variants this is the discrete replicator equation, which is Bayes' rule with fitness as likelihood (Known: Harper 2009).

This primitive replaces both GM's selection operator and the plan's goal primitive. An agent's goal is the fitness by which outcomes it acts on are conditioned. A signal is scored by the outcome it produces through a receiver's action, which is the plan's position without a separate primitive.

## 4. Language and the world

### 4.1 Firth is Yoneda (Known mathematics; Implicit application)

Bradley, Terilla and Vlassopoulos (2022) treat text as a category enriched in $[0,1]$. Its objects are strings, and the hom from $x$ to $y$ is the probability that $y$ continues $x$. The meaning of $x$ is the copresheaf $\hom(x,-)$, its distribution over contexts. The Yoneda lemma says this copresheaf determines $x$ up to isomorphism. "You shall know a word by the company it keeps" is that lemma.

The rest of this section is about the phrase "up to isomorphism".

### 4.2 Text fixes the world up to a gauge (New statement; elementary proof)

Let $\mathrm{Aut}(\Omega)$ act on world–speaking pairs by $g\cdot(P,\pi)=(g\circ P,\ \pi\circ g^{-1})$. Then $\pi\circ g^{-1}\circ g\circ P=\pi\circ P$, so the corpus law $D$ is unchanged.

**Theorem 4.2.** No observer that receives only samples of $D$, however much compute it has, can distinguish $(P,\pi)$ from any pair in its $\mathrm{Aut}(\Omega)$-orbit. Everything a text-only observer can learn about the world is an invariant of that orbit.

This is Quine's inscrutability of reference and Putnam's permutation argument, stated as a gauge symmetry of the map $(P,\pi)\mapsto D$ (Implicit). Two long-running positions are then true together:

- **Firth and Harris are right.** The orbit invariant is the measured structure of the world, which is a great deal. When $P$ is $G$-invariant and $\pi$ is equivariant, the corpus carries $G$'s irreducible representations, and every equivariant learner's geometry is built from them (outline S1, S5; Karkada 2026; Storan 2026).
- **Harnad and Bender are right.** Which world state a string refers to is not an orbit invariant, so text alone cannot fix it (harnad1990; bender2020).

Newman's objection to structural realism says pure structure is cheap, because any set of the right size carries it. It does not apply here. The invariant is a measured structure, the isomorphism class of $(\Omega,P)$ together with $\pi$, and not a bare relational one.

### 4.3 Two gauges, and what grounding is

There are two gauges, one at each end of the agent:

| Gauge | Acts on | Fixed by | Observable invariants |
|---|---|---|---|
| Reference, $\mathrm{Aut}(\Omega)$ | Which world states strings pick out | A channel from $\Omega$ that does not factor through $V^*$ | The measured structure (§4.2) |
| Representation, $\mathrm{Aut}(\Theta)$ over $f$ | The agent's internal coordinates | Nothing, because parameters are hidden | The kernel, Gram matrices, CKA (outline S9, S10) |

**Grounding is gauge fixing (New).** A grounded agent observes $(\sigma_a,\pi)$ jointly. Of the reference gauge, only the subgroup that also preserves $\sigma_a$ survives: $\{g:\sigma_a\circ g=\sigma_a\}$. That subgroup is genuine indistinguishability, because the agent's senses cannot separate those world states either.

**Anchors (New; Test).** If $G$ acts freely, one token–percept anchor fixes the $G$-part of the gauge, and $k$ anchors reduce it to the stabilizer of the anchor set. Prediction: two text-trained geometries of the same world align by a rigid map fitted on a handful of seed pairs. This is what unsupervised bilingual lexicon induction finds (Conneau et al. 2018). It should fail where the two languages' worlds differ, so the shared structure shrinks, and the failures are reported for distant language pairs (Søgaard, Ruder and Vulić 2018).

**Information is not reference (New).** Grounded information $\mathcal G=I(\Omega;\cdot)$ is computed under the true joint law, so it is gauge-invariant. A text-only model can therefore hold a great deal of $\mathcal G$ and still refer to nothing by itself. The program's accounting identity (spine principle 3) tracks the first. Grounding in Harnad's sense is the second. The two are different quantities and need different symbols.

### 4.4 Conventions are spontaneous symmetry breaking (Known mathematics; New mapping; Test)

Let a population coordinate on a lexicon: a Lewis signaling game or a naming game. Suppose no form is cheaper or more iconic than another. Then relabeling forms consistently across every agent is a symmetry of the dynamics, a group $S$ acting on forms. Standard results for equivariant dynamics give:

- the set of attractors is $S$-invariant;
- with coordination payoffs, the symmetric state is unstable and the population settles into one convention, a pitchfork as in Frank's model of homochirality;
- over independent populations started from a symmetric law, the distribution of conventions is $S$-invariant.

**Prediction.** Arbitrary features of form are distributed with the symmetry across unrelated languages. The non-arbitrary residue, form–meaning associations that recur across thousands of languages, marks explicit breaking by the world or the body: sound symbolism and iconicity (Blasi et al. 2016). This is the outline's S27 split between world breaking, which is kept, and agent breaking, which averages away, now with a mechanism.

## 5. The generative agent

### 5.1 What it can know

A generative agent's every input factors through $V^*$. So:

- **(Known; checked here as GM T2 and MR1.)** $I(\Omega;\theta)\le I(\Omega;D)$ by the data-processing inequality.
- **(Theorem 4.2.)** Whatever it learns is fixed only up to the reference gauge.
- **(Implicit.)** Its world model is the Yoneda image of the corpus, which is the measured structure of the world as the speakers' selection left it in the text. Protein language models are the cleanest case. They learn contact maps because selection for folding coupled sequence to structure. Shuffle the alignment so selection's coupling is gone, and nothing is learned.

### 5.2 Where its reference comes from (New)

The model's outputs refer to the world only through the composite $\Omega\xrightarrow{\pi}V^*\xrightarrow{\theta}V^*\xrightarrow{r}\text{action}$, where $r$ is a grounded reader. The reader supplies the gauge fixing that the model lacks. This is the division of linguistic labor (Putnam 1975) as a factorization. It predicts that the model's referential success is bounded by its readers' grounding, and that it degrades exactly where the readers lack anchors.

### 5.3 What it does to language and the world (Known core; Conjecture mapping)

Its outputs are interactions, so they enter $\Omega$ and then the next corpus. The loop $V^*\to\theta\to V^*$ is an endomorphism of the language object.

- **Closed loop.** With no input from $\Omega$ that avoids $V^*$, grounded information cannot rise (GM T2, checked). Under finite sampling it falls (Shumailov 2024).
- **Error threshold (Conjecture).** The mapping to Eigen's threshold is direct. Recursive training is replication with copying error, and structure persists only while selection on independent evidence outweighs the error rate (GM T6).
- **Verifier.** The gain is bounded by the verifier's term $I(\Omega;E_{\text{ver}}\mid D)$ (MR1, checked; the verifier term is load-bearing). Protein design is the working instance. A sequence model proposes, folding and assay select, and the loop gains real structure because the assay is a channel from the world.

### 5.4 Convergence across models (New; outline S9–S15, S26)

Two text-only learners trained to optimum on the same corpus law have the same Yoneda image, because it depends only on $D$. So they agree up to the representation gauge, and their alignment is computable from the spectra (outline S10). Learners trained on different corpora of one world agree on the invariants the corpora share, and only across channels that are conditionally independent given the world does agreement count as evidence about it (outline S26).

The Platonic Representation Hypothesis is therefore a theorem about convergence of Yoneda images, with stated conditions. It is not a claim about grounding, because the reference gauge stays unfixed for every text-only learner. "Convergence is not grounding" is Theorem 4.2 applied twice.

## 6. What this replaces, and what it cuts

| Current piece | Fate | Why |
|---|---|---|
| Spine L0 agent tuple $(b_a,S_a,\kappa_a)$ | Replaced by P3 | Belief and store are the hidden parameter. Context is part of the interface's input |
| Plan primitive 4, goal | Merged into P4 | Goal is fitness under conditioning |
| GM selection operator $\mathcal F_{\text{test}}$ | Becomes P4 | Same object |
| Plan's episode $(x,k,m,u)$ | Cut | Classification and internal state are functions of the hidden parameter |
| `formal/schema.py`, 11 node types and 14 edge types | Cut | The category is the data shape. Sentences, narratives and genres enter when a result needs structure on $V^*$ |
| `formal/notation.md`, 140 symbols | Cut to the symbols this draft and the checked results use | The rest get a row when a result first uses one |
| Rung ladder R1–R7 | Replaced by §4–§5 as the order of proof | The ladder ordered postulates. This orders theorems |
| Spine L1–L3 | Rederived from §2–§5 | Same laws, fewer assumptions |
| Spine L4–L8, GM C-items, canon and ecology claims | Kept, frozen as "farther afield" | Revisited once §4–§5 are checked |
| `experiments/cyclic_world` | Kept | It is the finite testbed for §4.2–§4.4 |

## 7. Checks that would firm this up

Each check fits the existing harness on finite objects.

1. **Gauge theorem, exact.** On the cyclic world, show that a text-only learner's geometry is a circle determined up to rotation, and that its reference is undetermined. A `witness` check: two worlds in one $\mathbb Z_N$-orbit with identical corpus laws.
2. **Anchors.** With one anchor, the rotation is fixed. With one anchor on a world whose symmetry group is dihedral, a reflection survives.
3. **$\mathcal G$ is gauge-invariant.** `grounded_information` is unchanged under the joint action. Most of this test exists already.
4. **Convention breaking.** A naming-game simulation under the $S$-symmetry. The realized conventions break it, and the ensemble over seeds is symmetric within sampling error. Adding one cheaper form breaks the ensemble symmetry in the predicted direction.
5. **Replicator is Bayes.** A sympy identity check. This needs the `finite_identity` runner that `harness.md` §8 lists as small.
6. **Closed loop and verifier.** Already checked: GM T2, MR1 and OUT-S26.

## 8. Sources this draft leans on, all from memory

To be checked before any claim built on them leaves `new`: fritz2020 (Markov categories); fong2019 (Backprop as Functor); capucci2021 (categorical cybernetics); bradley2022 (enriched category of language); coecke2010 (DisCoCat); harper2009 (replicator as inference); shalizi2009; frank1953; soai1995; soloveichik2008; perez2019; merrill2024; morcos2011; rives2021; conneau2018; sogaard2018; blasi2016; putnam1975, putnam1981; quine1960; newman1928; lewis1969. Already in the bibliography: firth1957, harnad1990, bender2020, karkada2026, storan2026, huh2024, shumailov2024, eigen1971.

## 9. Open problems

1. **The fiber is not a group in general.** $(P,\pi)\mapsto D$ is not injective for reasons beyond automorphisms, because $\pi$ can merge world states. The orbit is only part of the fiber. The quantity to bound is the fiber, and Theorem 4.2 is the symmetric part of it.
2. **Translation is not a gauge transformation.** Languages differ in how they carve the world as well as in their labels. A translation is then a non-invertible kernel, and its loss is a defect of isomorphism. This needs a category of kernels, not a groupoid.
3. **Universality claims need their caveats.** Pérez et al. assume arbitrary precision. Merrill and Sabharwal bound what a scratchpad of a given length adds. The foundation uses universality only to rule out expressivity as an explanation, so the caveats affect rates, not the frame.
4. **Which structure on $V^*$ to add first.** Composition will be needed for any sentence-level result. The candidates are a pregroup grammar functor (DisCoCat) or the enriched-category continuation structure alone.
5. **Information versus reference needs a measure.** §4.3 separates them in words. A number for reference, such as the size of the surviving gauge group or its entropy under a prior, is the first new definition the theory needs.

## 10. Task changes (applied 2026-11-22)

- Supersede F-01 to F-07 with **S-01**, which files §3–§5 as `definition` and `new` claims, and **S-02**, which runs checks 1 to 4 on the cyclic world.
- Add **S-03**, a citation check for §8, limited to the sources a filed claim depends on.
- Cut `formal/schema.py`, and cut `formal/notation.md` to this draft's symbols, in the same commit that files S-01.
- Mark spine L4–L8 tasks as deferred until S-02 closes.
