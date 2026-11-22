#!/usr/bin/env bash
# Install the mechanical verifiers that check.py runs. Idempotent.
#   program/tools/setup_verifiers.sh          # PSITIP clone at ${PSITIP:-~/.cache/psitip}
# PSITIP is GPL-3.0, so it is cloned outside the repo, never vendored.
set -euo pipefail
DEST="${PSITIP:-$HOME/.cache/psitip}"
COMMIT="$(python3 -c 'import re,sys; print(re.search(r"PSITIP_COMMIT = \"(\w+)\"", open(sys.argv[1]).read())[1])' "$(dirname "$0")/check.py")"

[ -d "$DEST/.git" ] || git clone -q https://github.com/cheuktingli/psitip "$DEST"
if [ "$(git -C "$DEST" rev-parse HEAD)" != "$COMMIT" ]; then
  git -C "$DEST" fetch -q origin "$COMMIT" 2>/dev/null || git -C "$DEST" fetch -q --unshallow origin || true
  git -C "$DEST" checkout -q "$COMMIT"
fi
python3 -m pip install -q numpy scipy sympy ortools lark-parser pylatexenc
echo "PSITIP $COMMIT at $DEST. Run checks with: PSITIP=$DEST python3 program/tools/check.py"
