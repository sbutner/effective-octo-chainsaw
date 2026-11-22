#!/usr/bin/env python3
"""SessionStart: re-arm the git gate, note where the session began, hand over the last handoff.

A cloud session clones the repo fresh, so `core.hooksPath` (local git config) is lost each
time. Setting it here, on every start, is what makes .githooks/pre-commit persist.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
HANDOFFS = ROOT / ".claude" / "handoffs"
SESSIONS = ROOT / ".claude" / "state" / "sessions"


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


def main():
    event = json.load(sys.stdin)
    if git("rev-parse", "--is-inside-work-tree") == "true":
        git("config", "core.hooksPath", ".githooks")
    SESSIONS.mkdir(parents=True, exist_ok=True)
    marker = SESSIONS / f"{event.get('session_id', 'unknown')}.json"
    if not marker.exists():
        marker.write_text(json.dumps({"head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
                                      "started": datetime.now(timezone.utc).isoformat(timespec="seconds")}))
    if event.get("source") not in ("startup", "clear"):
        return
    latest = max(HANDOFFS.glob("*.md"), default=None)
    if latest is None:
        return
    context = (f"Handoff from the previous session ({latest.relative_to(ROOT)}). "
               "It was generated from that session's transcript and git state; verify before relying on it.\n\n"
               + latest.read_text(encoding="utf-8"))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))


if __name__ == "__main__":
    main()
