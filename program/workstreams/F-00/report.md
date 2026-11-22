# F-00 report

## Findings in the outline (from the cyclic-world build)

1. **S4 needs an even N.** The hemisphere shift is $N/2$. Outline §6 lists $N=7$ and $N=365$, which have no southern hemisphere. `corpus_profile` raises an error for odd $N$.
2. **S4's "stays zero after the log" holds only at $s=\tfrac12$.** There the profile is invariant under the $N/2$ shift. For other $s$, the log's coefficients do not scale by $1-s+s(-1)^k$.
3. **S18's gains are a moving average, not coarse-graining.** The width-3 box on $\mathbb Z_{12}$ gives 0.91, 0.67, 0.33, 0, 0.24, 0.33 for $k=1$ to 6. "Months coarse-grained to seasons" would be that blur followed by decimation, which aliases, and its gains need their own derivation.
4. **S18's "diverge above the water line" is not monotone in $k$.** The gain at $k=5$ is higher than at $k=4$. The test asserts the band form: readers agree at $k=0$, and every $k\ge3$ diverges more than every $k\le2$.
