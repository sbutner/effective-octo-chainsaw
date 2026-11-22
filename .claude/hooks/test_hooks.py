#!/usr/bin/env python3
"""Drive the hooks with the payloads Claude Code sends, against a scratch clone of the repo.

Usage: python3 .claude/hooks/test_hooks.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOOKS = REPO / ".claude" / "hooks"


def call(script, payload, root, *args):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    r = subprocess.run([sys.executable, str(root / ".claude/hooks" / script), *args], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, cwd=root)
    if r.returncode != 0:
        raise RuntimeError(f"{script} exited {r.returncode}: {r.stderr}")
    return json.loads(r.stdout)["hookSpecificOutput"] if r.stdout.strip() else {}


def edit(root, path, old, new, sid="s1"):
    return {"session_id": sid, "tool_name": "Edit",
            "tool_input": {"file_path": str(root / path), "old_string": old, "new_string": new}}


def bash(cmd):
    return {"session_id": "s1", "tool_name": "Bash", "tool_input": {"command": cmd}}


def guard_cases(root):
    claims = (root / "program/data/claims.json").read_text()
    k10 = next(l for l in claims.splitlines() if '"id": "K10"' in l)
    tasks = json.loads((root / "program/data/tasks.json").read_text())
    blind_old = '"added_by": "seed",\n    "blind": false'
    blind_new = '"added_by": "seed",\n    "blind": true'
    return [
        ("hand edit of a generated view", edit(root, "program/claims.md", "# Claims", "# Claims!"), "deny"),
        ("write into the ledger", {"session_id": "s1", "tool_name": "Write",
                                   "tool_input": {"file_path": str(root / "program/ledger/x.json"), "content": "{}"}}, "deny"),
        ("claim status change", edit(root, "program/data/claims.json", k10, k10.replace('"status": "implicit"', '"status": "known"')), "ask"),
        ("claim title change", edit(root, "program/data/claims.json", k10, k10.replace("Closed-system C2", "Closed-system C2.")), None),
        ("JSON layout broken", {"session_id": "s1", "tool_name": "Write", "tool_input": {
            "file_path": str(root / "program/data/tasks.json"), "content": json.dumps(tasks, indent=2)}}, "deny"),
        ("frozen phenomenon wording", edit(root, "program/data/phenomena.json", "Words that occur in similar contexts",
                                           "Words occurring in similar contexts"), "deny"),
        ("blind mark by a reader of the formalism", edit(root, "program/data/phenomena.json", blind_old, blind_new, "reader"), "deny"),
        ("blind mark by an agent that has not read it", edit(root, "program/data/phenomena.json", blind_old, blind_new, "fresh"), None),
        ("shell redirect into a view", bash("echo x > program/claims.md"), "deny"),
        ("shell read of a view piped elsewhere", bash("grep K10 program/claims.md > /tmp/out.txt"), None),
        ("render.py may write views", bash("python3 program/tools/render.py"), None),
        ("sed -i on claims.json", bash("sed -i 's/a/b/' program/data/claims.json"), "ask"),
        ("ledger edit by shell", bash("sed -i 's/true/false/' program/ledger/MR1__main.json"), "deny"),
        ("plain read", bash("jq '.claims[0]' program/data/claims.json"), None),
    ]


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        subprocess.run(["git", "clone", "-q", str(REPO), str(root)], check=True)
        shutil.copytree(HOOKS, root / ".claude/hooks", dirs_exist_ok=True)
        for sub in ("program", ".githooks"):
            shutil.copytree(REPO / sub, root / sub, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
        subprocess.run(["git", "-C", str(root), "checkout", "-q", "-b", "test-handoff"], check=True)

        call("guard.py", {"session_id": "reader", "tool_name": "Read",
                          "tool_input": {"file_path": str(root / "program/spine.md")}}, root, "--track-reads")
        for name, payload, want in guard_cases(root):
            got = call("guard.py", payload, root).get("permissionDecision")
            ok = got == want
            results.append(ok)
            print(f"{'pass' if ok else 'FAIL'}  guard: {name}" + ("" if ok else f" (expected {want}, got {got})"))

        out = call("session_start.py", {"session_id": "h1", "source": "startup"}, root)
        ok = (root / ".claude/state/sessions/h1.json").exists() and \
            subprocess.run(["git", "-C", str(root), "config", "core.hooksPath"], capture_output=True, text=True).stdout.strip() == ".githooks"
        results.append(ok)
        print(f"{'pass' if ok else 'FAIL'}  session_start: arms the git gate and records the start")

        transcript = root / "t.jsonl"
        transcript.write_text("\n".join(json.dumps(e) for e in [
            {"type": "ai-title", "aiTitle": "Test session"},
            {"type": "user", "message": {"content": "<command-name>/pstack:poteto-mode</command-name>\n<command-args>prove K10</command-args>"}},
            {"type": "user", "message": {"content": "<system-reminder>noise</system-reminder>"}},
            {"type": "user", "isMeta": True, "message": {"content": "skill body"}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "K10 is V4 now."}]}},
        ]))
        call("handoff.py", {"session_id": "h1", "reason": "clear", "transcript_path": str(transcript)}, root)
        files = list((root / ".claude/handoffs").glob("*-h1.md"))
        text = files[0].read_text() if files else ""
        committed = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%s"], capture_output=True, text=True).stdout
        ok = bool(files) and "/pstack:poteto-mode prove K10" in text and "noise" not in text and "skill body" not in text \
            and "K10 is V4 now." in text and "Session handoff: Test session" in committed
        results.append(ok)
        print(f"{'pass' if ok else 'FAIL'}  handoff: written from the transcript and committed" + ("" if ok else f"\n{text}\n{committed}"))

        out = call("session_start.py", {"session_id": "h2", "source": "clear"}, root)
        ok = "K10 is V4 now." in out.get("additionalContext", "")
        results.append(ok)
        print(f"{'pass' if ok else 'FAIL'}  session_start on clear: hands the handoff to the next session")

    print(f"{sum(results)}/{len(results)} hook cases pass")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
