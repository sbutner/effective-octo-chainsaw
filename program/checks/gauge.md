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
