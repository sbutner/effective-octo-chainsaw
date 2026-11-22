---
name: research-loop
description: Run one turn of this repo's research loop on a Q-task, as coordinator or as workstream agent. Use when asked to work the research program, take the next task, prove or refute a claim, or continue a workstream.
---

# Research loop

The loop turns a task in `program/data/tasks.json` into recorded verdicts. Nothing moves a claim except a verdict in `program/ledger/`, and a claim's tier is derived from the ledger. The spec is `program/harness.md`. The conventions are in `program/AGENTS.md`, so read that first.

## Coordinator (the main session)

1. **Pick.** Choose the highest-priority open task whose dependencies are done:
   `jq -c '(.tasks|map({(.id):.status})|add) as $s | [.tasks[]|select(.status=="open" and all(.depends_on[]; $s[.]=="done"))]|sort_by(.priority)[]|{id,priority,title}' program/data/tasks.json`
   Prefer a task whose claims have checks that can run. A PROVE task outranks a writing task of the same priority.
2. **Charter.** Write `program/workstreams/<Q>/charter.md` with the goal, the subjects in scope, the acceptance criterion as a tier ("every subject V4 or R"), and what is out of scope. Ask the human to approve the charter once. That is the only question the loop asks before it starts.
3. **Dispatch.** Give each workstream its own git worktree (`isolation: "worktree"`) and branch. Workstreams write different check modules and ledger files, so their branches merge without conflicts. Never let two workstreams edit the same check module.
4. **Merge.** Merge each finished branch, then run `python3 program/tools/render.py` and `python3 program/tools/validate.py` once on the merged tree. Generated views are rebuilt after the merge and never merged by hand.
5. **Escalate.** A workstream that reports `blocked` goes to the human with its `failures.md` and the review packet (harness.md §5.3.7). Do not retry it silently.

## Workstream agent

1. Set the task `in_progress` and log the start (AGENTS.md workflow).
2. **State each subject exactly.** Use explicit quantifiers and named variables. Narrow the subject to what you will check, such as `GM-T4.1.inequality`. A corrected statement is a new subject, `<id>~<variant>`, and the original keeps its own checks.
3. **Write checks** in `program/checks/<topic>.py`. For each subject, write:
   - `proves` checks whose conclusions together give the statement;
   - one `probe` per hypothesis, with that hypothesis removed;
   - for each `not-provable` probe, a `witness` that breaks the bound, so the hypothesis is shown to be load-bearing. A `provable` probe shows the hypothesis is unused: record that as a finding.
4. **Run** `PSITIP=~/.cache/psitip python3 program/tools/check.py`. A `MISS` means the expectation was wrong or the encoding is. Find out which before you change either.
5. **When a step will not close** (AlphaGeometry loop):
   - (a) search for a witness;
   - (b) if none turns up, propose an auxiliary variable or an extra hypothesis and retry;
   - (c) log every dead end in `program/workstreams/<Q>/failures.md`, which is append-only.
6. **Write the residue.** Hand proofs and findings go in `program/checks/<topic>.md`. Steps no runner can decide go to `report.md` as informal residue, for review.
7. **Gate.** Run `python3 program/tools/render.py`, then `python3 program/tools/validate.py`. Commit with the task id. The pre-commit hook reruns the gate.
8. **Finish.** If `claims.md` shows the acceptance tier, mark the task `done`. Otherwise mark it `blocked` with the reason. Three rounds without progress on one step means blocked.

## Fences

The hooks enforce the hard fences: generated views and the ledger, JSON layouts, the human gate on claim statuses, frozen phenomena, and blind provenance (`program/AGENTS.md`, "Enforced rules"). When a hook denies a call, fix the cause it names. Do not route around it with a shell write. When it asks the person about a status change, that ask is the human gate: put the evidence in `checks/<topic>.md` first.

These fences take judgment, so no hook enforces them:

- A `MISS` is information. Never edit `expect` just to turn a check green.
- `not-provable` is never a refutation. Only an exact witness refutes, and `validate.py` rejects a `refutes` check of any other kind.
- Add a kind to `check.py` only with a sanity check and a case in `program/tools/test_gates.py`.
