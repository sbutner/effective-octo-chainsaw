# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Task `model` and spawn `generalPurpose`). Alias entries in a panel list still count toward its fan-out.
# defaults: 3
# budget: small (medium)
feature, refactoring: opus medium
bug-fix: opus medium
perf-issue: opus medium
hillclimb: opus medium
judgment and prose: opus medium
arena runners: fable low, opus low, inherit-parent
arena cross-judge pool: opus low, inherit-parent
swarm workers: opus low
interrogate reviewers: fable low, opus low, inherit-parent
