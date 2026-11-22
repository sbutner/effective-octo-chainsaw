# Gauge results on the cyclic world: pre-registration, hand proofs and findings

*Checks: [`gauge.py`](gauge.py). Task S-02, charter [`../workstreams/S-02/charter.md`](../workstreams/S-02/charter.md). Verdicts: `program/ledger/`, summarized in [`claims.md`](../claims.md).*

This file has two parts. Part A is written and committed before the first simulation run, and is never edited afterwards. Later parts are appended below it.

## Part A. Pre-registration for the naming-game simulations (K71, K72.c)

*Fixed 2026-11-22, before any ensemble run and before `naming_game.py` exists.*

### The game

A population of `M` agents plays a single-object naming game over a form set `F = {0, ..., m-1}`. Agent `i` holds an inventory `I_i`, a subset of `F`. One interaction, in order:

1. Draw an ordered pair `(i, j)`, `i != j`, uniformly.
2. Speaker `i` picks a form `f`. If `I_i` is empty, it invents `f` with probability proportional to the weights `w_f` over all of `F` and adds `f` to `I_i`. Otherwise it picks `f` from `I_i` with probability proportional to `w_f` over `I_i`.
3. If `f` is in `I_j`, both inventories collapse to `{f}`. Otherwise `I_j` gains `f`.

The initial state has every inventory empty. A run is converged when every inventory is the same single form. That form is the run's convention.

### The symmetry and the cost

With `w_f` all equal, relabeling forms by any permutation `s` in `S = Sym(F)`, applied to every inventory at once, commutes with the update kernel. Lowering the cost of form 0 gives `w_0 = r`, `w_f = 1` for `f >= 1`, with `r = exp(-c)` for a cost `c = -ln r` below the other forms. This breaks `S` down to `Sym(F \ {0})`. `r = 1` is the control.

### Exact part (small population)

`M = 3`, `m = 3`, exact `Fraction` arithmetic over the full state space. These are exact computations, not simulations, and need no tolerance.

- (a) The transition kernel is `S`-equivariant, and the absorbing states are exactly the `m` consensus states, which form one `S`-orbit.
- (b) The law of the state at each step `t = 0..8` from the empty initial state is `S`-invariant.
- (c) The `S`-fixed states (all inventories empty, or all equal to `F`) are transient, and absorption into a consensus has probability 1. Each consensus has probability exactly `1/m` from the empty state.
- K72.c exact: with `r = 2`, the absorption probability of consensus 0 is strictly above `1/m`, and consensus 1 and 2 have equal probability.
- Sanity: the same equivariance test on the `r = 2` kernel over the full `S` must fail, so the test can see broken symmetry.

### Simulation part (ensemble over seeds)

| Quantity | Value |
|---|---|
| Agents `M` | 20 |
| Forms `m` | 5 |
| Interaction budget per run `T_max` | 50 000 |
| Seeds per configuration `R` | 2000 |
| Configurations | `r` = 1 (control), 2, 3, as configuration index 0, 1, 2 |
| Seed of run `i` in configuration `c` | `10000 * c + i`, fed to `random.Random` |
| Population state | initial inventories all empty |

`p_f` is the fraction of converged runs whose convention is `f`. `R_c` is the number of converged runs.

| Prediction | Metric | Pass threshold |
|---|---|---|
| K71(c): each run breaks the symmetry | converged fraction `R_c / R`, each configuration | `>= 0.99` |
| K71(b): the ensemble is symmetric, control | `max_f abs(p_f - 1/m)`, `r = 1` | `<= tau = 0.036` |
| K72(c): the cheaper form is favored | `p_0` for `r = 2` and for `r = 3` | `>= 1/m + tau = 0.236` |
| K72(c): the effect does not shrink with `r` | `p_0(r=3) - p_0(r=2)` | `>= -tau` |
| Residual symmetry after explicit breaking | `max_{f>=1} abs(p_f - (1 - p_0)/(m-1))`, `r = 2` and `r = 3` | `<= tau' = 0.040` |

The tolerance is four standard errors of a binomial proportion at `R = 2000`. For `p = 1/m = 0.2`, one standard error is `sqrt(0.2 * 0.8 / 2000) = 0.0089`, and four of them is 0.036. For `tau'`, the largest standard error at `p <= 0.25` is `sqrt(0.25 * 0.75 / 2000) = 0.0097`, and four of them is 0.039, rounded up to 0.040. A correctly symmetric ensemble fails one of these tests by chance with probability about `10^-3`.

If a threshold is missed, the verdict stays `MISS`. Neither the thresholds, the seeds nor `naming_game.py` change after the first run. `gauge.py` pins the SHA-256 of `naming_game.py`, so a later edit to the simulator turns the verdict into an error until the pin is changed and the change is explained here.

### What the simulation does not check

The instability of the symmetric state in (c) is checked in the exact small chain, where it means transience of the `S`-fixed states. The simulation measures that every run leaves the symmetric state, not a linearization. K72 (a) and (b) are the cross-language half, out of scope here.

## Part B. Corrections to Part A

Part A is unchanged. One parenthetical in its exact-part item (c) is wrong. It lists the `S`-fixed states as "all inventories empty, or all equal to `F`". The exact chain lumps anonymous agents into multisets, and a multiset is `S`-fixed when relabeling permutes its inventories among themselves. There are six such states: `(∅,∅,∅)`, `(∅,∅,F)`, `(∅,F,F)`, `(F,F,F)`, one agent per single form, and one agent per pair of forms. The check `K71.small-population/symmetric-transient` covers all six. The first encoding assumed four and raised `error`; see `failures.md`. No simulation parameter, threshold or seed changed.

## Part C. Results of the pre-registered run

First and only run, 2026-11-22. `naming_game.py` SHA-256 `d4237674fe32…`, pinned in `gauge.py`. Rerun with `check.py --verify` reproduces every verdict.

| Configuration | Converged | Shares of forms 0 to 4 | Mean, max interactions |
|---|---|---|---|
| `r = 1` (control) | 2000 of 2000 | 0.1895, 0.2030, 0.1915, 0.2075, 0.2085 | 221, 795 |
| `r = 2` | 2000 of 2000 | 0.7475, 0.0595, 0.0620, 0.0685, 0.0625 | 187, 675 |
| `r = 3` | 2000 of 2000 | 0.9250, 0.0195, 0.0140, 0.0215, 0.0200 | 144, 800 |

| Pre-registered test | Observed | Threshold | Result |
|---|---|---|---|
| Converged fraction, all configurations | 1.000 | `>= 0.99` | pass |
| Control, `max abs(p_f - 1/5)` | 0.0105 (1.2 standard errors) | `<= 0.036` | pass |
| `p_0`, `r = 2` | 0.7475 | `>= 0.236` | pass |
| `p_0`, `r = 3` | 0.9250 | `>= 0.236` | pass |
| `p_0(3) - p_0(2)` | +0.1775 | `>= -0.036` | pass |
| Residual symmetry, `r = 2`, `r = 3` | 0.0054 and 0.0047 | `<= 0.040` | pass |

The thresholds were loose for this game. The effect of `r = 2` is 15 times the tolerance, so the simulation separates symmetric from broken ensembles with a wide margin, but it would not detect a bias of 0.03 in the control. The tolerance was set from sampling error, not from the effect.

The exact 3-agent, 3-form chain gives the same direction without sampling: from the empty state the probability of consensus 0 is `77085/143608 = 0.537` at `r = 2` and `315069/483425 = 0.652` at `r = 3`, and consensus 1 and 2 tie exactly. The ensemble shares (0.7475 and 0.925) are higher because 20 agents and 5 forms amplify the bias. The two sizes are different systems, so the match is in direction and in the residual tie, not in the number.

## Part D. Hand proofs

- **K66.** Under `g`, `D'(a,b) = sum_w' P'(w') K'(a|w') K'(b|w')`. Substituting `w' = g w` gives `sum_w P(w) K(a|w) K(b|w) = D(a,b)`. An observer of `n` samples sees `D^n`, so its output law is the same for the pair and its orbit. The check confirms this exactly for all of `Sym(5)` on a generic world and all of `D_12` on the cyclic world.
- **K66, text fixes geometry, not reference.** On `Z_N` with uniform `P`, the shift by `s` maps `K(a|w) = kappa(a - w)` to `kappa(a - w + s)`. That is a different speaker whenever `kappa` is not `s`-periodic, and the corpus law is the same. The witness has total variation between 0.115 and 0.318 on the 11 nontrivial shifts. `D(a,b) = c(a - b)` with `c(d)` proportional to `sum_u kappa(u + d) kappa(u)`, and this is even in `d`. So `D` is a symmetric circulant matrix, and its automorphism group contains `D_N`. Exhaustive search over `Sym(6)` and `Sym(7)` shows it is exactly `D_N` for the default profile.
- **K67 containment.** Under `(gP, K o g^-1)` the joint law of `(sigma, words)` is `sum_w' [sigma(w') = o] P(g^-1 w') K(a | g^-1 w') K(b | g^-1 w')`. Put `w = g^-1 w'` and use `sigma(g w) = sigma(w)`.
- **K68.** A rotation `w -> w + s` fixes a point only if `s = 0`, so `Z_N` is free. A reflection `w -> t - w` fixes `a` only if `t = 2a`. So `H_{a}` in `D_N` is `{id, w -> 2a - w}`, which has order 2 for every `N >= 3`. For anchors `a` and `b`, the reflection through `a` also fixes `b` iff `2(b - a) = 0 mod N`, which needs `N` even and `b = a + N/2`.
- **K70.** `I(Omega; Y) = sum_w P(w) sum_y X(y|w) log(X(y|w)/q(y))`, `q(y) = sum_w P(w) X(y|w)`. The action sends `P(w) X(y|w)` to `P'(g w) X'(y|g w)`, which is the same number, and leaves `q` alone. The sum is reindexed by `g`.
- **K71 (a), (b).** If the kernel `T` satisfies `T(pi s -> pi s') = T(s -> s')`, then `pi` carries the law at time `t` to the law at time `t` from the image of the initial law, so invariant initial laws stay invariant. The check verifies the equivariance condition on all 120 states of the 3-agent, 3-form chain and the invariance of the law for 9 steps. The general statement for every population size is the same one-line induction, and is not checked beyond this instance.
- **K71 (c), finite form.** The absorption linear system is non-singular, so no recurrent class other than the consensus states exists. Every `S`-fixed multiset is therefore transient, and by symmetry reaches each consensus with probability `1/3`. This is not the linearization at the symmetric state that (c) names. It is the finite-chain statement that the symmetric state is left with probability 1, and the dynamical instability remains informal residue (see the report).

## Part E. Findings

1. **K67 equality fails, and K67 itself stands.** The surviving gauge `S(sigma) = {g : the joint law of (sigma, words) is unchanged}` is strictly larger than `Stab(sigma)` on the hemisphere-blind world. That world is `N = 12` with the speaking profile `corpus_profile(World(12), 1/2)`, which has period 6: the S4 case where the corpus cannot tell hemispheres apart. There the shift by 6 maps the pair `(P, K)` to itself, so it survives every sensorium. Refuted by exact witness: `K67~equality/hemisphere-identity` and `K67~equality/hemisphere-anchor`. On a world with no such symmetry, equality holds: all of `Sym(6)` for four sensoria (anchor, two quantizers, identity), and `Z_12`, `D_12` for the identity and one-anchor sensoria at `N = 12` (the latter in `K68.cyclic-world/surviving-gauge`).
   On all four hemisphere-blind cases computed, `S(sigma) = Stab(sigma) · Fix(P, K)`, with `Fix(P, K) = {g : g.(P, K) = (P, K)}`. These four cases are the evidence; the general statement is a conjecture.
2. **One anchor fixes the rotation only modulo `Fix(P, K)`.** `K68` as stated is about the pointwise stabilizer and is true: `H_A` is trivial in `Z_N`, and has order 2 in `D_N` with one anchor. In the cyclic world with a generic profile, the surviving gauge inside `D_12` under one anchor is exactly `{id, r_a}`. In the hemisphere-blind world it is `{id, r_a, shift 6, r_a o shift 6}`, order 4. Foundations §4.3 and §7 check 2 should say "up to the symmetry of the corpus-world pair".
3. **Two anchors do not always remove the reflection.** In `D_N` with `N` even, two antipodal anchors leave a reflection; any other two anchors remove it. This is a probe, outside the charter, in `K68/two-anchors`.
4. **Pair statistics cannot see chirality.** The default speaking profile is not reflection-symmetric (`kappa(1) = 177`, `kappa(11) = 117` at `N = 12`), yet `Aut(D)` is the full `D_N` for `N = 6, 7`. The two words of a string are exchangeable given the phase, so `D(a,b) = D(b,a)` and `D` is blind to the reflection. A text-only learner built from unordered pair statistics recovers a circle up to rotation and reflection. Chirality would need ordered strings whose words come from different phases.
5. **K70 extends to reflections.** `grounded_information` is unchanged under all of `D_12` and all of `Sym(5)`, so the existing shift-only test extends to reflections. The new pytest `test_info_invariant_under_the_whole_dihedral_group` also asserts that a reflection really moves the prior.
6. **Tiers.** `check.py` derives V0, V4 and R only (`harness.md` §5.4). V3 has no derivation, so no subject can show V3 in `claims.md`. The narrowed subjects below show V4, which means "every `proves` check passed on the stated finite instance", not that the universal claim is proved. The bare claim rows K66 to K72 stay V0 because no check names them, and K60 to K64, their dependencies, are definitions with no checks, which would cap any claim at V0 in any case.

| Subject | Derived tier | What it covers |
|---|---|---|
| `K66.cyclic-world` | V4 | `D` invariance, `Sym(5)` and `D_12` |
| `K66.geometry` | V4 | `Aut(D) = D_N`, N = 6, 7 |
| `K66~reference-identifiable` | R | the corpus law does not determine reference |
| `K67.containment` | V4 | all stabilizers in `Sym(6)` and `Sym(5)`, 8 cases |
| `K67~equality` | R | equality fails on the hemisphere-blind world |
| `K68.cyclic-world` | V4 | `Z_N` free, `D_N` one reflection, N = 3..16; surviving gauge at N = 12 |
| `K70.cyclic-world` | V4 | exact relabeling, `Sym(5)`, `D_12` |
| `K71.small-population` | V4 | (a), (b), (c) exact, 3 agents, 3 forms |
| `K71.ensemble` | V0 | simulation, 2 probes |
| `K72.c` | V4 | exact direction at 3 agents, 3 forms; 4 simulation probes |

7. **The checks are finite.** Every exhaustive check covers the stated groups and sizes. The statements for all `N`, all finite worlds and all populations rest on the hand proofs above, which need review.
8. **psitip.** No subject needed it. Every check is a `witness` check, so the missing PSITIP clone did not block anything.
9. **Digest coverage.** `check.py` hashes the check module, not the files it imports. `gauge.py` pins `naming_game.py` and `cyclic_world.py` by SHA-256 and raises an error if either changes, which turns the verdict stale on the next edit of the pin.
