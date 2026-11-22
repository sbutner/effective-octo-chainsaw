#!/usr/bin/env python3
"""Prove the gates fail when they should: each case mutates a scratch copy of program/
and asserts that validate.py exits 1 with the expected message. Needs no prover.

Usage: python3 program/tools/test_gates.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROGRAM = Path(__file__).resolve().parent.parent


def sub(path, old, new):
    def go(root):
        p = root / path
        s = p.read_text(encoding="utf-8")
        assert old in s, f"{path}: pattern not found: {old}"
        p.write_text(s.replace(old, new, 1), encoding="utf-8")
    return go


def regex(path, pattern, new):
    def go(root):
        p = root / path
        s, n = re.subn(pattern, new, p.read_text(encoding="utf-8"), count=1)
        assert n, f"{path}: pattern not found: {pattern}"
        p.write_text(s, encoding="utf-8")
    return go


def touch(path, text):
    def go(root):
        (root / path).write_text(text, encoding="utf-8")
    return go


CASES = [
    ("bad task status", sub("data/tasks.json", '"status": "open"', '"status": "bogus"'), "bad status 'bogus'"),
    ("string priority", sub("data/tasks.json", '"priority": 1,', '"priority": "1",'), "bad priority '1'"),
    ("bad claim status", sub("data/claims.json", '"status": "new"', '"status": "proved"'), "bad status 'proved'"),
    ("missing required field", regex("data/experiments.json", r'"cost": "\w+", ?', ""), "missing cost"),
    ("unknown dependency", sub("data/claims.json", '"depends_on": ["K10"]', '"depends_on": ["K999"]'), "unknown claim K999"),
    ("new protocol violation", regex("data/claims.json", r'("id": "K10".*?"falsifier": )"[^"]*"', r'\1""'), "K10: implicit claim needs a falsifier"),
    ("fixed debt still listed", regex("data/claims.json", r'("id": "K27".*?"falsifier": )""', r'\1"a falsifier"'), "K27 is fixed"),
    ("hand-edited view", sub("concept-map.md", "# Concept map", "# Concept map (edited)"), "out of date: program/concept-map.md"),
    ("check source changed", sub("checks/info_core.py", "Unconstrained I(W;D)", "Unconstrained  I(W;D)"), "verdict stale"),
    ("orphan verdict", touch("ledger/ghost.json", '{"check": "ghost"}\n'), "ledger ghost: no such check"),
    ("verdict missed", sub("ledger/GM-T2__main.json", '"ok": true', '"ok": false'), "verdict mismatch"),
    ("JSON layout broken", sub("data/tasks.json", '{"id": "Q-02", "workstream"', '{"id": "Q-02",\n     "workstream"'),
     "tasks record Q-02 is not on one line"),
    ("frozen wording, against HEAD", sub("data/phenomena.json", "Words that occur in similar contexts",
                                         "Words occurring in similar contexts"), "P-001: behavior is frozen once assessed"),
    ("verdict changed without a new derivation", regex("data/phenomena.json", r'("verdict": )"emergent"', r'\1"parametric"'),
     "needs a changed derivation"),
]


def run(root, baseline=None):
    args = ["--baseline", str(baseline)] if baseline else []
    return subprocess.run([sys.executable, str(root / "tools" / "validate.py"), *args], capture_output=True, text=True)


def main():
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "base" / "program"
        shutil.copytree(PROGRAM, base, ignore=shutil.ignore_patterns("__pycache__"))
        baseline = Path(tmp) / "baseline"
        baseline.mkdir()
        shutil.copy(base / "data" / "phenomena.json", baseline / "phenomena.json")
        r = run(base, baseline)
        if r.returncode != 0:
            sys.exit("the unmutated tree fails validate.py; fix that first:\n" + r.stdout[-2000:])
        for i, (name, mutate, expect) in enumerate(CASES):
            root = Path(tmp) / f"case{i}" / "program"
            shutil.copytree(base, root)
            mutate(root)
            r = run(root, baseline)
            ok = r.returncode == 1 and expect in r.stdout
            failures += not ok
            print(f"{'pass' if ok else 'FAIL'}  {name}" + ("" if ok else f"\n      expected exit 1 with {expect!r}; got {r.returncode}:\n{r.stdout[-800:]}"))
    print(f"{len(CASES) - failures}/{len(CASES)} gate cases pass")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
