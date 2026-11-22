# Cyclic world (F-00, rung R0)

A finite testbed for the formalization ladder: world Z_N, channels, many agents, episode streams.
It adds no learning; the agent model is R1's job. Code is in `cyclic_world.py`.

| Object | What it is | Primitive |
|---|---|---|
| `World(N, f)` | Z_N with a positive seasonal profile `f` (default: annual plus semiannual harmonic), state `t mod N`, shift action `g.w = w+g` | 1 |
| `Channel(K, time_cost, energy_cost)` | Row-stochastic kernel `K[w, o]` with per-use costs. `noiseless`, `constant`, `box_blur(N, w)`; `.gains()` gives the DFT magnitudes of a shift-invariant kernel | 2 |
| `Agent(id, offset, sensorium)` | Hemisphere offset (0 north, N//2 south) and a sensorium channel. It observes phase `w + offset` | 3 (shell only) |
| `Episode(t, x, k, m, u)` | Frozen. `x` is the observed local phase; `k`, `m`, `u` are `None` until R1/R2 | 3 |
| `run(world, agents, T, rng)` | `agent_id -> list[Episode]`, deterministic given a seeded `numpy` Generator | |
| `corpus_profile(world, s)` | `(1-s) f(w) + s f(w+N/2)`; needs even N | |
| `grounded_information(prior, K)` | Exact I(Omega; O) in bits | |

Primitive 4 (goal) is not in R0. The channel costs are stored but nothing spends them yet.
`A` is the agent count throughout; `N` is the group size.

Run the tests from the repo root: `python3 -m pytest program/experiments/cyclic_world -q`

Notes on the outline (symmetry-platonic-program.md)
- S4 needs even N, since the hemisphere shift is N/2. N = 7 and 365 have no south. Only s = 1/2 gives the exact odd-harmonic zero after the log; for other s the log is not covered.
- S18 gains hold exactly: |sin(pi k/4) / (3 sin(pi k/12))| for the width-3 box on Z_12. "Diverge above the water lines" is ambiguous. The gains are not monotone in k (k=5 gives 0.24, k=4 gives 0), and the default profile has no energy above k=2. The test asserts the band statement on a profile with every harmonic: k=3..6 diverge more than k=1..2, with the peak at k=4.
