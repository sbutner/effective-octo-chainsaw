# F-00 report

## Findings in the outline (from the cyclic-world build)

1. **S4 needs an even N.** The hemisphere shift is $N/2$. Outline §6 lists $N=7$ and $N=365$, which have no southern hemisphere. `corpus_profile` raises an error for odd $N$.
2. **S4's "stays zero after the log" holds only at $s=\tfrac12$.** There the profile is invariant under the $N/2$ shift. For other $s$, the log's coefficients do not scale by $1-s+s(-1)^k$.
3. **S18's gains are a moving average, not coarse-graining.** The width-3 box on $\mathbb Z_{12}$ gives 0.91, 0.67, 0.33, 0, 0.24, 0.33 for $k=1$ to 6. "Months coarse-grained to seasons" would be that blur followed by decimation, which aliases, and its gains need their own derivation.
4. **S18's "diverge above the water line" is not monotone in $k$.** The gain at $k=5$ is higher than at $k=4$. The test asserts the band form: readers agree at $k=0$, and every $k\ge3$ diverges more than every $k\le2$.

## Notation (from the notation build)

`program/formal/notation.md` gives one meaning per symbol across GM, the outline, the spine and the plan, in 140 rows. Its test fails on a duplicate. I checked this by inserting one, and the test failed. Prose and code keep their old names until each rung migrates them, using the table's "Renames" list.

Judgment calls a reviewer should check:

- The plan's classification $k_t=\kappa_a(x_t)$ is the outline's quantizer, so it becomes $\mathrm{cls}_t=q_a(O_{a,t})$, and $\kappa_a$ stays GM's context.
- The plan's agent model $M_a$ is the spine's $\theta$, so it becomes $\theta_a$. Its geometry $\mathsf G_a$ becomes $\mathrm{Gram}_a$. The plan defines that geometry as a PMI matrix, so F-01 must show the Gram of the fitted representation is that object.
- The spine's fit $F(\theta)$ is read as GM's expected log score $L$.
- The agent count is $|A|$, because $A$ is GM's set of agents.

Settled by the human after review, 2026-11-22:

- $\Omega$ consists of interactions. Internal models are hidden and are not part of the world, so grounded information never counts an agent's parameters.
- A channel carries a single cost $c$ per use. The time and energy pair is gone from the plan, the ledger, the notation and the testbed.
