#!/usr/bin/env python3
"""Run mechanical checks and keep the verdict ledger.

A check is one step a machine can decide. Checks live in program/checks/*.py, each module
exposing CHECKS: list[Check]. Every run writes program/ledger/<check id>.json, one file per
check, so concurrent workstreams never write the same file. Tiers are derived from the
ledger (see `tiers`), never typed in.

Usage:
    python3 program/tools/check.py                 # run checks whose verdict is missing or stale
    python3 program/tools/check.py --force [ids]   # rerun the named checks (default all)
    python3 program/tools/check.py --verify        # rerun everything in memory, compare, write nothing
    python3 program/tools/check.py --list          # list checks with their ledger state

PSITIP checks need a clone at PSITIP_COMMIT, named by $PSITIP or --psitip
(program/tools/setup_verifiers.sh makes one at ~/.cache/psitip).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402
import witness  # noqa: E402

PSITIP_COMMIT = "6caf8ea8c03c7b2c66716edfda4ff2f1c464beb7"  # cheuktingli/psitip, 2025-06-10
PSITIP_SOLVER = "ortools.GLOP"

ROLES = {"proves", "refutes", "probe", "sanity"}
EXPECT = {"psitip": {"provable", "not-provable"}, "witness": {"counterexample", "no-counterexample"}}


@dataclass(frozen=True)
class Check:
    id: str                  # "<subject or tool>/<step>", unique across modules
    subject: Optional[str]   # <claim id>[.<clause>][~<variant>]; None for sanity checks
    role: str                # proves: establishes (a conjunct of) the subject as stated
                             # refutes: a witness that the subject as stated is false
                             # probe: informational, e.g. a hypothesis ablation
                             # sanity: guards the tool; a miss invalidates its other verdicts
    kind: str                # psitip | witness
    expect: str
    statement: str           # the step in words, for the ledger and the review packet
    run: Callable            # psitip: run(p) -> (hypothesis, conclusion); witness: run() -> (hyps, gap)


def load_checks():
    """All checks with the source digest that keys their ledger entry."""
    out = []
    witness_src = (Path(witness.__file__)).read_bytes()
    for path in sorted(db.CHECKS.glob("*.py")):
        spec = importlib.util.spec_from_file_location(f"checks_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        src = path.read_bytes()
        for c in mod.CHECKS:
            h = hashlib.sha256(src + c.id.encode())
            if c.kind == "witness":
                h.update(witness_src)
            out.append((c, path.relative_to(db.REPO).as_posix(), h.hexdigest()[:16]))
    return out


def tool_id(kind):
    return f"psitip@{PSITIP_COMMIT[:12]}/{PSITIP_SOLVER}" if kind == "psitip" else "witness"


def ledger_path(check_id):
    return db.LEDGER / (check_id.replace("/", "__") + ".json")


def read_ledger():
    return {json.loads(p.read_text())["check"]: json.loads(p.read_text()) for p in sorted(db.LEDGER.glob("*.json"))}


def entry_state(check, digest, entry):
    if entry is None:
        return "missing"
    if entry["digest"] != digest or entry["tool"] != tool_id(check.kind):
        return "stale"
    return "ok" if entry["ok"] else "mismatch"


def _psitip(path):
    if not path:
        sys.exit("PSITIP checks need --psitip or $PSITIP (run program/tools/setup_verifiers.sh)")
    head = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != PSITIP_COMMIT:
        sys.exit(f"PSITIP at {path} is {head or 'not a git clone'}, expected {PSITIP_COMMIT}")
    sys.path.insert(0, path)
    import psitip
    psitip.PsiOpts.setting(solver=PSITIP_SOLVER)
    return psitip


def run_one(check, p):
    try:
        if check.kind == "psitip":
            hyp, concl = check.run(p)
            return ("provable" if bool(hyp >> concl) else "not-provable"), {}
        hyps, gap = check.run()
        return witness.verdict(hyps, gap)
    except Exception as e:  # a crash is a verdict too: it must not read as a pass
        return "error", {"error": f"{type(e).__name__}: {e}"}


def make_entry(check, src, digest, result, detail):
    return {"check": check.id, "subject": check.subject, "role": check.role, "kind": check.kind,
            "statement": check.statement, "source": src, "digest": digest, "tool": tool_id(check.kind),
            "expect": check.expect, "result": result, "ok": result == check.expect, "detail": detail}


def write_entry(entry):
    """Write via a temp file and rename, so a crash never leaves a half-written verdict."""
    path = ledger_path(entry["check"])
    text = json.dumps(entry, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    db.LEDGER.mkdir(exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    return True


def tiers(checks=None, ledger=None):
    """Derive a tier for every claim and every checked subject.

    V4 when every `proves` check of the subject is ok (it needs at least one), every psitip
    sanity check is ok, and every depends_on claim is V4 too. R when a `refutes` witness holds.
    V0 otherwise. V1-V3 need the notation registry, search budgets and calibrated review,
    which the harness does not have yet (harness.md §8).
    Returns {subject: (tier, reason)}.
    """
    checks = load_checks() if checks is None else checks
    ledger = read_ledger() if ledger is None else ledger
    state = {c.id: entry_state(c, d, ledger.get(c.id)) for c, _, d in checks}
    sane = all(state[c.id] == "ok" for c, _, _ in checks if c.role == "sanity")
    by_subject = {}
    for c, _, _ in checks:
        if c.subject:
            by_subject.setdefault(c.subject, []).append(c)

    own = {}
    for s, cs in by_subject.items():
        bad = [c.id for c in cs if state[c.id] != "ok"]
        refuted = [c.id for c in cs if c.role == "refutes" and state[c.id] == "ok"]
        proves = [c for c in cs if c.role == "proves"]
        if bad:
            own[s] = ("V0", f"checks not ok: {', '.join(bad)}")
        elif refuted and proves:
            own[s] = ("V0", "proved and refuted at once; the encoding is wrong")
        elif refuted:
            own[s] = ("R", f"witness {', '.join(refuted)}")
        elif proves and sane:
            own[s] = ("V4", f"mechanically proved: {', '.join(c.id for c in proves)}")
        elif proves:
            own[s] = ("V0", "a sanity check failed")
        else:
            own[s] = ("V0", "no proving check")

    doc = db.load("claims")
    deps = {c["id"]: c.get("depends_on", []) for c in doc["claims"]}
    out = {}

    def tier_of(cid, seen=()):
        if cid in out:
            return out[cid]
        t, why = own.get(cid, ("V0", "no checks"))
        if t == "V4":
            low = [d for d in deps.get(cid, []) if d not in seen and tier_of(d, seen + (cid,))[0] != "V4"]
            if low:
                t, why = "V0", f"capped by dependencies below V4: {', '.join(low)}"
        out[cid] = (t, why)
        return out[cid]

    for cid in list(deps) + [m["id"] for m in doc["master_relations"]] + list(own):
        tier_of(cid)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--psitip", default=os.environ.get("PSITIP"))
    a = ap.parse_args()

    checks = load_checks()
    ledger = read_ledger()
    known = {c.id for c, _, _ in checks}
    if unknown := set(a.ids) - known:
        sys.exit(f"unknown checks: {', '.join(sorted(unknown))}")
    if a.list:
        for c, _, d in checks:
            e = ledger.get(c.id)
            print(f"{entry_state(c, d, e):8} {c.kind:7} {c.role:7} {c.id}  {e['result'] if e else ''}")
        return

    def wanted(c, d):
        if a.ids and c.id not in a.ids:
            return False
        return a.force or a.verify or entry_state(c, d, ledger.get(c.id)) in ("missing", "stale")

    todo = [(c, s, d) for c, s, d in checks if wanted(c, d)]
    p = _psitip(a.psitip) if any(c.kind == "psitip" for c, _, _ in todo) else None
    failed = 0
    for c, src, d in todo:
        result, detail = run_one(c, p)
        entry = make_entry(c, src, d, result, detail)
        if a.verify:
            old = ledger.get(c.id)
            same = old is not None and all(old[k] == entry[k] for k in ("digest", "tool", "result"))
            failed += not same
            print(f"{'same' if same else 'DIFF':5} {c.id}: {result}" + ("" if same else f" (ledger: {old and old['result']})"))
        else:
            wrote = write_entry(entry)
            failed += not entry["ok"]
            print(f"{'ok' if entry['ok'] else 'MISS':4} {c.id}: {result} (expect {c.expect})" + (" [written]" if wrote else ""))
    print(f"{len(todo)} run, {len(checks) - len(todo)} up to date, {failed} {'differ' if a.verify else 'missed'}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
