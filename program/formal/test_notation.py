"""F-00 notation test: parse the table in notation.md and check it.

Run: python3 -m pytest program/formal/test_notation.py -q
"""
import re
from collections import Counter
from pathlib import Path

NOTATION = Path(__file__).with_name("notation.md")
HEADER = ["Symbol", "Meaning", "Defined in", "First use", "Replaces"]

# ASCII name from the F-00 task list -> the LaTeX symbol that must be a table row.
REQUIRED = {
    "Omega": r"\Omega",
    "G": r"G",
    "D": r"D",
    "theta": r"\theta",
    "delta": r"\delta",
    "N_e": r"N_e",
    "v": r"v",
    "c": r"c",
    "phi": r"\varphi",
    "r": r"r",
    "lambda": r"\lambda",
    "L": r"L",
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def parse_rows():
    """Return (line_number, [cells]) for each data row of the notation table."""
    rows, in_table = [], False
    for n, line in enumerate(NOTATION.read_text(encoding="utf-8").splitlines(), 1):
        if not line.lstrip().startswith("|"):
            if in_table:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells == HEADER:
            in_table = True
            continue
        if not in_table or set("".join(cells)) <= set("-: "):
            continue
        rows.append((n, cells))
    return rows


def symbol_of(cell: str):
    m = re.fullmatch(r"\$([^$]+)\$", cell.strip())
    return norm(m.group(1)) if m else None


def test_table_found():
    assert parse_rows(), "no notation table with header " + " | ".join(HEADER)


def test_rows_have_five_cells_and_one_symbol():
    for n, cells in parse_rows():
        assert len(cells) == 5, f"line {n}: expected 5 cells, got {len(cells)}"
        assert symbol_of(cells[0]) is not None, (
            f"line {n}: symbol cell must be exactly one $...$ span: {cells[0]!r}")


def test_no_duplicate_symbol():
    counts = Counter(symbol_of(c[0]) for _, c in parse_rows())
    dups = sorted(s for s, k in counts.items() if k > 1)
    assert not dups, f"duplicate symbols: {dups}"


def test_task_symbols_present():
    present = {symbol_of(c[0]) for _, c in parse_rows()}
    missing = [k for k, v in REQUIRED.items() if norm(v) not in present]
    assert not missing, f"missing task symbols: {missing}"


def test_cells_nonempty():
    for n, cells in parse_rows():
        assert cells[1], f"line {n}: empty Meaning for {cells[0]}"
        assert cells[2], f"line {n}: empty Defined-in for {cells[0]}"
        assert cells[3], f"line {n}: empty First-use for {cells[0]}"


def test_no_phi_or_epsilon_variants():
    # Only symbol cells: the Replaces column and Renames section quote old uses.
    for n, cells in parse_rows():
        sym = symbol_of(cells[0]) or ""
        assert not re.search(r"\\phi(?![a-z])", sym), f"line {n}: use \\varphi"
        assert not re.search(r"\\epsilon(?![a-z])", sym), f"line {n}: use \\varepsilon"
