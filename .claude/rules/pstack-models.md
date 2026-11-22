# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Task `model` and spawn `generalPurpose`). Alias entries in a panel list still count toward its fan-out.
# defaults: 3
# budget: small (medium)
feature, refactoring: sonnet medium
bug-fix: sonnet medium
perf-issue: sonnet medium
hillclimb: sonnet medium
judgment and prose: sonnet medium
arena runners: opus low, sonnet low, inherit-parent
arena cross-judge pool: sonnet low, inherit-parent
swarm workers: sonnet low
interrogate reviewers: opus low, sonnet low, inherit-parent
