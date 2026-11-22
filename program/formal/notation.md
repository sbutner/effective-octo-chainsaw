# Notation table

*One meaning per symbol. Cut by S-01 (2026-11-22) to the symbols that [`foundations.md`](../foundations.md) and the checked results in `checks/info_core.md` use. A later result adds a row when it first uses a symbol. The 140-row F-00 table is in git history at `1842a63`.*

## Rules

1. A symbol has one meaning. A new object that is the same as an old one reuses the old symbol.
2. Multi-letter roman symbols ($\mathrm{Aut}$, $\mathrm{Para}$, $\mathrm{CKA}$) are single symbols, not products.
3. A subscript that indexes an agent, a time or a group element ($a$, $t$, $g$) is not a new symbol. So $\sigma_a$ covers $\sigma_r$, and $\theta$ covers $\theta_a$.
4. Only `\varphi`, `\varepsilon` and `\vartheta` are used, never `\phi` or `\epsilon`.
5. Claims in `claims.json` are plain ASCII. They spell symbols by name (`Omega`, `pi`, `o` for composition, `(x)` for the tensor).

## Table

| Symbol | Meaning | Defined in | First use | Replaces |
|---|---|---|---|---|
| $\mathsf{Stoch}$ | Category of standard Borel spaces (finite sets in toy models) and Markov kernels; a Markov category | foundations §2 | foundations §2 | |
| $c$ | Single cost per channel use: a functor from $\mathsf{Stoch}$ to $([0,\infty),+)$ (K64) | foundations §2 | foundations §2 | the time and energy cost pair |
| $\Omega$ | The world: an object of interactions, events and what agents do and write. Agents' parameters are not part of it (K60) | foundations §3.1 | foundations §3.1 | |
| $P$ | Law of the world, a state $1\to\Omega$ | foundations §3.1 | foundations §3.1 | |
| $\omega$ | A sampled history, $\omega\sim P$ | foundations §3.1 | foundations §3.1 | $\omega_t$ |
| $G$ | Group of automorphisms of $\Omega$ preserving $P$; $G=\mathbb Z_N$ in the cyclic world | foundations §3.1 | foundations §3.1 | |
| $g$ | An element of $G$ or of $\mathrm{Aut}(\Omega)$ | foundations §4.2 | foundations §4.2 | |
| $\mathrm{Aut}$ | Automorphism group of an object, as in $\mathrm{Aut}(\Omega)$, the reference gauge, and $\mathrm{Aut}(\Theta)$, the representation gauge | foundations §4.2 | foundations §4.2 | |
| $\mathbb Z_N$ | Cyclic group of order $N$ | outline §6 | foundations §7 | |
| $N$ | Order of the cyclic or dihedral group; never a count of agents | outline §6 | foundations §7 | |
| $D_N$ | Dihedral group of order $2N$ acting on $\mathbb Z_N$ (K68) | foundations §7 | foundations §7 | |
| $V$ | Finite vocabulary | foundations §3.2 | foundations §3.2 | |
| $V^*$ | Free monoid of strings on $V$ under concatenation (K61) | foundations §3.2 | foundations §3.2 | |
| $\pi$ | Speaking, a kernel $\Omega\to V^*$ | foundations §3.2 | foundations §3.2 | spine and GM speech channels |
| $D$ | Corpus law $D=\pi\circ P$ | foundations §3.2 | foundations §3.2 | GM corpus $D$ (same object, now a law) |
| $r$ | Reading, a kernel out of $V^*$; a grounded reader in §5.2 | foundations §3.2 | foundations §3.2 | outline $r_l$ |
| $x$ | A string in $V^*$, an object of $L$ | foundations §4.1 | foundations §4.1 | |
| $y$ | A string continuing $x$ | foundations §4.1 | foundations §4.1 | |
| $L$ | The $[0,1]$-enriched category of strings with continuation probabilities as homs (K65) | foundations §4.1 | foundations §4.1 | |
| $\hom$ | Hom object; $\hom(x,-)$ is the copresheaf that is the meaning of $x$ | foundations §4.1 | foundations §4.1 | |
| $\mathrm{Para}$ | Construction of parametrized morphisms with private parameters | foundations §3.3 | foundations §3.3 | |
| $\Theta$ | Parameter object of an agent | foundations §3.3 | foundations §3.3 | spine $(b_a,S_a)$ |
| $\theta$ | Hidden parameter $\theta\in\Theta$, the agent's internal model | foundations §3.3 | foundations §3.3 | plan's agent model $M_a$ |
| $f$ | An agent's kernel $f:\Theta\otimes X\to Y$ (K62) | foundations §3.3 | foundations §3.3 | |
| $X$ | Interface input object of an agent; in K70, a kernel out of $\Omega$ | foundations §3.3 | foundations §3.3 | |
| $Y$ | Interface output object of an agent | foundations §3.3 | foundations §3.3 | |
| $\sigma_a$ | Sensorium of agent $a$, a kernel $\Omega\to O_a$ that does not factor through $V^*$ | foundations §3.3 | foundations §3.3 | |
| $O_a$ | What agent $a$ senses | foundations §3.3 | foundations §3.3 | $O_{a,t}$ |
| $w$ | Fitness $\Omega\to[0,\infty)$; selection is $P\mapsto wP/\langle w,P\rangle$ (K63) | foundations §3.4 | foundations §3.4 | GM $\mathcal F_{\mathrm{test}}$; plan's goal |
| $I$ | Mutual information | GM, T2 | GM, T2 | |
| $\mathcal G$ | Grounded information $I(\Omega;\cdot)$ under the true joint law; gauge-invariant (K70) | GM, Primitives (measures) | foundations §4.3 | |
| $\xi$ | Randomness independent of the world, in the closed-loop and corpus results | GM, Primitives 2 | checks/info_core.md | |
| $E_{\mathrm{ver}}$ | Verifier evidence, a channel from $\Omega$ that does not factor through $V^*$ (MR1) | spine §3 | foundations §5.3 | GM $E'$ |
| $H$ | A group of bijections of $\Omega$ in the anchor result (K68) | foundations §4.3 | foundations §4.3 | |
| $A$ | Set of anchored points of $\Omega$ (K68) | foundations §4.3 | foundations §4.3 | F-00's set of agents |
| $k$ | Number of anchors | foundations §4.3 | foundations §4.3 | |
| $S$ | Group of relabelings of forms in a naming game (K71) | foundations §4.4 | foundations §4.4 | |
| $F$ | Finite set of forms in a naming game (K71) | foundations §4.4 | foundations §4.4 | |
| $e$ | Per-generation copying error rate in recursive training (K75) | foundations §5.3 | foundations §5.3 | |
| $s$ | Selection strength from independent evidence (K75) | foundations §5.3 | foundations §5.3 | |
| $\mathrm{CKA}$ | Centered kernel alignment, a representation-gauge invariant | outline S10 | foundations §3.3 | |

## Settled by the human, 2026-11-22

- $\Omega$ consists of interactions. Internal models are hidden, so $\mathcal G=I(\Omega;\cdot)$ never counts an agent's own parameters.
- A channel has a single cost $c$ per use. There is no time and energy pair.
