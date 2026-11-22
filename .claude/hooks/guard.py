#!/usr/bin/env python3
"""Edit-time enforcement of the repo's protocol (see program/AGENTS.md, "Enforced rules").

PreToolUse (Edit, Write, NotebookEdit, Bash): deny or ask before a tool call breaks a rule.
PostToolUse (Read, Grep, Bash), invoked with --track-reads: remember which agents have read the
formalism, so they cannot add phenomena marked blind.

The commit gate (.githooks/pre-commit) re-checks the deterministic rules on the staged tree.
This hook catches them earlier, and it is the only place the human gate on claim statuses
can be enforced, because only here can it ask a person.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
sys.path.insert(0, str(ROOT / "program" / "tools"))
import protocol  # noqa: E402

STATE = ROOT / ".claude" / "state" / "readers.json"
GENERATED = {f"program/{n}" for n in protocol.GENERATED}
REDIRECT = re.compile(r">>?\s*([^\s;&|]+)")
IN_PLACE = re.compile(r"\btee\b|\bsed\s+-i|\bperl\s+-i|\bcp\b|\bmv\b|\btruncate\b|write_text|\.write\(|json\.dump\(|open\([^)]*['\"][wa]['\"]")
SHELL_TOOLS_OK = re.compile(r"program/tools/(check|render)\.py|^\s*git\b")


def rel(path):
    try:
        return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None


def decide(kind, reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": kind, "permissionDecisionReason": reason}}))
    sys.exit(0)


def reader_key(event):
    return f"{event.get('session_id', '?')}/{event.get('agent_id') or 'main'}"


def has_read_formalism(event):
    try:
        return reader_key(event) in json.loads(STATE.read_text())
    except (OSError, ValueError):
        return False


def new_text(tool, inp, path):
    if tool == "Write":
        return inp.get("content", "")
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    a, b = inp.get("old_string", ""), inp.get("new_string", "")
    return old.replace(a, b) if inp.get("replace_all") else old.replace(a, b, 1)


def check_file_edit(event, tool, inp):
    r = rel(inp.get("file_path") or inp.get("notebook_path") or "")
    if r is None:
        return
    if r in GENERATED:
        decide("deny", f"{r} is generated. Edit its source and run python3 program/tools/render.py.")
    if r.startswith("program/ledger/"):
        decide("deny", "The ledger is written only by program/tools/check.py. Change the check and rerun it.")
    m = re.fullmatch(r"program/data/(\w+)\.json", r)
    if not m or tool == "NotebookEdit":
        return
    name, path = m.group(1), ROOT / r
    text = new_text(tool, inp, path)
    try:
        new = json.loads(text)
        old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except ValueError as e:
        decide("deny", f"{r} would not parse as JSON: {e}")
    errs = protocol.layout_errors(name, text)
    if errs:
        decide("deny", "; ".join(errs) + ". Use Edit on single records (AGENTS.md, Editing the JSON).")
    if name == "phenomena":
        errs = protocol.phenomena_violations(old, new)
        if errs:
            decide("deny", "; ".join(errs))
        blind = protocol.blind_additions(old, new)
        if blind and has_read_formalism(event):
            decide("deny", f"{', '.join(blind)}: only an agent that has not read the formalism "
                           f"({', '.join(protocol.FORMALISM_FILES)}) may mark a phenomenon blind.")
    if name == "claims":
        changes = protocol.claim_status_changes(old, new)
        if changes:
            desc = ", ".join(f"{i}: {a or 'new'} -> {b}" for i, a, b in changes)
            decide("ask", f"Human gate: claim status change ({desc}). Approve only if you reviewed the evidence.")


def shell_targets(cmd):
    """Paths a shell command may write: redirect targets, or every token if it edits in place."""
    targets = REDIRECT.findall(cmd)
    if IN_PLACE.search(cmd):
        targets += cmd.split()
    return " ".join(targets)


def check_shell(cmd):
    if SHELL_TOOLS_OK.search(cmd):
        return
    t = shell_targets(cmd)
    if not t:
        return
    if "program/ledger/" in t or "ledger/" in t:
        decide("deny", "The ledger is written only by program/tools/check.py.")
    for g in GENERATED:
        if g in t or re.search(rf"(^|[\s/]){re.escape(Path(g).name)}($|\s)", t):
            decide("deny", f"{g} is generated. Edit its source and run python3 program/tools/render.py.")
    if "claims.json" in t:
        decide("ask", "Shell write to claims.json bypasses the status gate. Use Edit, or approve if no status changes.")


def track_reads(event):
    inp = event.get("tool_input", {})
    blob = " ".join(str(inp.get(k, "")) for k in ("file_path", "path", "command", "pattern"))
    if not any(f in blob or Path(f).name in blob for f in protocol.FORMALISM_FILES):
        return
    STATE.parent.mkdir(parents=True, exist_ok=True)
    try:
        seen = json.loads(STATE.read_text())
    except (OSError, ValueError):
        seen = {}
    seen[reader_key(event)] = True
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(seen))
    tmp.replace(STATE)


def main():
    event = json.load(sys.stdin)
    if "--track-reads" in sys.argv:
        track_reads(event)
        return
    tool, inp = event.get("tool_name"), event.get("tool_input", {})
    if tool in ("Edit", "Write", "NotebookEdit"):
        check_file_edit(event, tool, inp)
    elif tool == "Bash":
        check_shell(inp.get("command", ""))


if __name__ == "__main__":
    main()
