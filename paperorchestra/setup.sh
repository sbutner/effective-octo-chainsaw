#!/usr/bin/env bash
# One-time setup for running PaperOrchestra against this repo.
# Installs a LaTeX toolchain (pdflatex + bibtex; the refinement agent compiles PDFs),
# fetches the PaperOrchestra submodule, and creates a Python venv with its requirements.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"

git -C "$ROOT" submodule update --init paperorchestra/paper-orchestra

if ! command -v pdflatex >/dev/null || ! command -v bibtex >/dev/null; then
  SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
  $SUDO apt-get update
  $SUDO apt-get install -y --no-install-recommends texlive-latex-base texlive-latex-recommended \
    texlive-latex-extra texlive-fonts-recommended texlive-bibtex-extra
fi

if [ ! -x "$HERE/.venv/bin/python" ]; then
  python3 -m venv "$HERE/.venv"
fi
"$HERE/.venv/bin/pip" install -q -r "$HERE/paper-orchestra/requirements.txt"

[ -f "$HERE/.env" ] || cp "$HERE/.env.example" "$HERE/.env"
python3 "$HERE/build_materials.py"
command -v claude >/dev/null || echo "WARNING: claude CLI not found. Install Claude Code and log in with your subscription (run \`claude\`, then /login)."
echo "Setup done. Run: paperorchestra/run.sh symmetry-convergence   (optional settings in $HERE/.env)"
