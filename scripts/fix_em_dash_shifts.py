"""Fix the buggy em-dash shifts applied earlier.

For each em-dash split with em_idx_old in a verse, the cell whose OLD s == em_idx_old + 1
should have its NEW s = em_idx_old + 1 + (count of other em-dashes in same verse with smaller em_idx).
But the buggy script shifted it by +1 too many, so current s is wrong by exactly +1.

Fix: subtract 1 from the s of the specific "absorb" cell for each em_idx_old.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
SCRIPTS_DIR = ROOT / "scripts"

# Em-dashes already applied (book_id, chap_num, verse_num, em_idx_old)
# Read from the original list (excluding 2nephi 28:8 already-done case)
APPLIED_SHIFTS = [
    ("1nephi", 1, 13, 35),
    ("1nephi", 10, 4, 33),
    ("1nephi", 10, 17, 81),
    ("1nephi", 13, 34, 58),
    ("1nephi", 13, 34, 127),
    ("1nephi", 14, 7, 53),
    ("1nephi", 21, 5, 7),
    ("1nephi", 21, 5, 28),
    ("2nephi", 7, 11, 41),
    ("2nephi", 8, 17, 27),
    ("2nephi", 10, 23, 19),
    ("2nephi", 12, 4, 36),
    ("2nephi", 15, 5, 24),
    ("2nephi", 19, 3, 8),
]

BOOK_TO_PREFIX = {
    "1nephi": "1nephi",
    "2nephi": "2nephi",
}


def fix_absorb_cell(script_path: Path, verse_num: int, em_idx_old: int, smaller_count: int):
    """Find the cell whose s should be decremented by 1 to fix the bug.
    The cell is at current s = em_idx_old + 2 + smaller_count.
    Change its s to em_idx_old + 1 + smaller_count (s - 1)."""
    target_s = em_idx_old + 2 + smaller_count
    correct_s = em_idx_old + 1 + smaller_count

    text = script_path.read_text(encoding="utf-8")
    pattern = rf"(    {verse_num}: \[\n)(.*?)(\n    \],?\n)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        return False
    body = m.group(2)

    # Match (target_s, e, "...")
    tuple_re = re.compile(rf'\({target_s},\s*(\d+),\s*("(?:[^"\\]|\\.)*")\)')
    found = [False]

    def repl(t_m):
        if found[0]:
            return t_m.group(0)
        found[0] = True
        e = int(t_m.group(1))
        g = t_m.group(2)
        return f"({correct_s}, {e}, {g})"

    new_body = tuple_re.sub(repl, body, count=1)
    if not found[0]:
        print(f"  WARNING: no cell at s={target_s} in v{verse_num} of {script_path.name}")
        return False
    new_text = text[: m.start(2)] + new_body + text[m.end(2):]
    script_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    # Group by (book, chap, verse) to compute smaller_count for each em_idx_old
    by_verse: dict[tuple[str, int, int], list[int]] = {}
    for book_id, chap_num, verse_num, em_idx in APPLIED_SHIFTS:
        by_verse.setdefault((book_id, chap_num, verse_num), []).append(em_idx)

    for (book_id, chap_num, verse_num), em_idxs in by_verse.items():
        prefix = BOOK_TO_PREFIX.get(book_id)
        if not prefix:
            continue
        script_path = SCRIPTS_DIR / f"build_overrides_{prefix}{chap_num}.py"
        if not script_path.exists():
            continue
        # For each em_idx, compute smaller_count = number of other em-dashes in same verse with smaller em_idx
        sorted_em = sorted(em_idxs)
        for em_idx in em_idxs:
            smaller_count = sum(1 for e in em_idxs if e < em_idx)
            ok = fix_absorb_cell(script_path, verse_num, em_idx, smaller_count)
            if ok:
                print(f"  fixed {script_path.name} v{verse_num} em_idx={em_idx} smaller_count={smaller_count}")


if __name__ == "__main__":
    main()
