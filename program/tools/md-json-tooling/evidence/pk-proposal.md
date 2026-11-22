# Proposal under review: `pk`, a token-efficient md/JSON CLI

Repo: /home/user/effective-octo-chainsaw (research "program": canonical JSON in program/data/*.json,
generated md via program/tools/render.py and phenomena.py, validator program/tools/validate.py,
conventions in program/AGENTS.md).

## Evidence it rests on (from recon of the one prior session that built this repo, ~195 tool calls)
Per-window recon summaries: scratchpad/recon_early.json, recon_mid.json, recon_late.json (same dir as this file).

| Pattern | ~Count | ~Cost |
|---|---|---|
| Whole-file Write of md/JSON | ~25 | ~355k chars in |
| Whole-file / big-range reads to orient or find one thing | ~20 | ~190k chars out |
| Python heredoc s.replace patches on md (assert count==1) | ~15 | ~45k chars in |
| Ad-hoc `python3 -c json.load…` lookups/counts/filters | ~20 | ~35k chars |
| JSON mutation by full load+dump (broke tasks.json layout once) | ~5 | — |
| validate -> render -> git diff --stat cycles | ~10 | small/noisy |

Claims: Edit tool used only ~2 times; Bash heredocs dominate. JSON layouts are mixed
(tasks/claims/debates/experiments one-record-per-line; others fully indented).

## Proposed tool: program/tools/pk.py (single file, stdlib, reuses validate.py load())
Principles: output only what was asked for (compact, truncated by default); address by id/heading;
preserve each file's layout so diffs touch only changed records; validate after every write.

JSON read:   pk get K12 [-f fields] [--max 400] | pk ls claims [--where k=v k!=v] [-f ...] |
             pk count claims by status | pk refs K12 | pk ids tasks | pk schema claims
JSON write:  pk set <id> field=value (bumps meta.updated) | pk add tasks @file|- (auto next id) |
             pk push <id> <listfield> "<text>" | pk task Q-05 start|done|blocked "reason"
Markdown:    pk outline f.md [--ids] | pk sec f.md "<heading|path|id>" |
             pk sec-set f.md "<heading>" < new | pk sec-add f.md --after "<h>" < new |
             pk row README.md add|set <key> "| … |" | pk grep <re> [--md --json]
Session:     pk check (validate+render+phenomena, one line) | pk brief (~30-line orientation) |
             pk changed <file> (unchanged-since-sha or diff stat)

Claimed saving: 40-60% of md/JSON token spend (section ops ~60-80k chars, id ops ~40k,
brief/changed ~30k). Authoring new docs unchanged.
Phase 1: get/ls/refs/set/add/task/outline/sec/sec-set/check. Phase 2: row/brief/changed.
Adoption: a "use pk first" section in AGENTS.md.
