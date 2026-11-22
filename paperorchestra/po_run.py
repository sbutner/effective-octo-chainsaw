#!/usr/bin/env python3
"""Run paper_writing_cli.py with PaperOrchestra's LLM calls sent to Claude Code.

Usage (run.sh does this for you):
    cd paperorchestra/paper-orchestra && ../.venv/bin/python ../po_run.py <paper_writing_cli.py args>
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PO = os.path.join(HERE, "paper-orchestra")
sys.path[:0] = [PO, HERE]
os.chdir(PO)

import claude_backend  # noqa: E402

claude_backend.install()
sys.argv = [os.path.join(PO, "paper_writing_cli.py")] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
