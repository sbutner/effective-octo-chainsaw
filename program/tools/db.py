"""Paths, loading and the schema for program/data/*.json.

Every enum the tools enforce lives here, so validate.py, render.py and check.py agree.
Reads only. Agents edit the JSON with Edit (see AGENTS.md for the file layouts).
"""
import json
import re
from pathlib import Path

PROGRAM = Path(__file__).resolve().parent.parent
REPO = PROGRAM.parent
DATA = PROGRAM / "data"
CHECKS = PROGRAM / "checks"
LEDGER = PROGRAM / "ledger"

LAYERS = {f"L{i}" for i in range(9)}

# collection file -> (list key, id key)
COLLECTIONS = {
    "bibliography": ("entries", "key"),
    "concepts": ("nodes", "id"),
    "claims": ("claims", "id"),
    "debates": ("debates", "id"),
    "experiments": ("experiments", "id"),
    "tasks": ("tasks", "id"),
    "phenomena": ("phenomena", "id"),
}

# Field specs: a type, a set of allowed values, or a list of either ([str] = list of str).
# Fields not listed are allowed; listed fields are required unless named in OPTIONAL.
SCHEMA = {
    "bibliography": {"key": str, "authors": str, "year": int, "title": str, "venue": str,
                     "status": {"checked", "checked-repo", "from-memory", "unverified", "not-found"},
                     "layers": [LAYERS], "concepts": [str], "supports": [str], "challenges": [str],
                     "annotation": str},
    "concepts": {"id": str, "layer": LAYERS, "definition": str},
    "claims": {"id": str, "layer": LAYERS, "title": str, "statement": str,
               "status": {"known", "implicit", "new", "conjecture", "test", "definition", "refuted"},
               "difficulty": {"easy", "medium", "hard", "open"},
               "depends_on": [str], "links": [str], "evidence": [str], "falsifier": str,
               "proof_route": [str]},
    "debates": {"id": str, "field": str, "question": str, "claims": [str], "llm_evidence": [str],
                "verdict_strength": {"early", "formalized", "open", "partial", "reframed", "strong"}},
    "experiments": {"id": str, "title": str, "design": str, "prediction": str, "tests": [str],
                    "related": [str], "cost": {"low", "medium", "high"}},
    "tasks": {"id": str, "title": str, "priority": {1, 2, 3, 4},
              "workstream": {"GROUND", "FORMALIZE", "PROVE", "EXTEND", "CONNECT", "INFRA"},
              "status": {"open", "in_progress", "done", "blocked"},
              "inputs": [str], "outputs": [str], "acceptance": str, "depends_on": [str], "log": [str]},
}
OPTIONAL = {"bibliography": {"url", "concepts", "supports", "challenges"},
            "claims": {"links", "evidence", "proof_route"},
            "experiments": {"related"}}

# Ids defined outside program/data: (pattern, lowest, highest).
EXTERNAL = [
    (re.compile(r"^GM-T([0-9]+)$"), 1, 10),
    (re.compile(r"^GM-C([0-9]+)$"), 11, 30),
    (re.compile(r"^GM-A([0-9]+)$"), 1, 14),
    (re.compile(r"^OUT-S([0-9]+)$"), 1, 31),
    (re.compile(r"^OUT-X([0-9]+)$"), 1, 14),
    (re.compile(r"^OUT-O([0-9]+)$"), 1, 7),
]
EXTERNAL_LITERALS = {"OSL-UCL"}


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def records(name):
    key, _ = COLLECTIONS[name]
    return load(name)[key]


def is_external(cid):
    if cid in EXTERNAL_LITERALS:
        return True
    for rx, lo, hi in EXTERNAL:
        m = rx.match(cid)
        if m:
            return lo <= int(m.group(1)) <= hi
    return False


def claim_space():
    """Every id a claim reference may name: K-claims, master relations, external ids."""
    doc = load("claims")
    ids = {c["id"] for c in doc["claims"]} | {m["id"] for m in doc["master_relations"]}
    return lambda cid: cid in ids or is_external(cid)


def subject_base(subject):
    """'GM-T4.2~corrected' -> 'GM-T4'. A subject is <claim id>[.<clause>][~<variant>]."""
    return re.split(r"[.~]", subject, maxsplit=1)[0]


# Protocol debt that predates the strict gate (2026-11-22). validate.py warns on these ids,
# errors on any new violation, and errors when a listed id is fixed but still listed, so the
# lists only shrink. Clearing them is task Q-24.
DEBT = {
    "falsifier": {"K27", "K36", "K40", "K46", "K49", "K50", "K51", "K53", "K55", "K56", "K57"},
    "unchecked-strength": {"P-001", "P-002", "P-003", "P-004", "P-005", "P-006", "P-007", "P-010", "P-012",
                           "P-013", "P-014", "P-015", "P-016", "P-017", "P-018", "P-020", "P-036", "P-037",
                           "P-042", "P-050", "P-060", "P-061", "P-064", "N-001", "N-002", "N-005"},
}
