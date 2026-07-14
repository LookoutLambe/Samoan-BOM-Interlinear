"""Strip ' forth' from all gloss strings in per-verse override scripts.

Rationale: atu/mai directionals shouldn't be glossed as 'forth' in English — it makes
the gloss clunky and the next clause naturally shows the action's target.

Surgical: only modifies content inside the gloss string of (s, e, "...") tuples.
Preserves: 'henceforth', 'forthwith', 'forthcoming' (no space before 'forth').
Strips: ' forth' followed by any trailing punctuation/whitespace.
"""
from __future__ import annotations
import re
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = sorted(glob.glob(str(ROOT / "scripts" / "build_overrides_*.py")))

# Match a gloss string inside (s, e, "..."). We rewrite the inner content.
TUPLE_RE = re.compile(r'(\((\d+),\s*(\d+),\s*")((?:[^"\\]|\\.)*)("\))')


def strip_forth_in_gloss(gloss: str) -> str:
    """Strip ' forth' from inside a gloss string. Keep word boundaries intact."""
    # ' forth' followed by end-of-string or punctuation
    new = re.sub(r' forth(?=$|[\s,;:.!?\-])', '', gloss)
    return new


def process_file(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    changes = 0

    def repl(m):
        nonlocal changes
        prefix, s, e, gloss, suffix = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        new_gloss = strip_forth_in_gloss(gloss)
        if new_gloss != gloss:
            changes += 1
            return f'{prefix}{new_gloss}{suffix}'
        return m.group(0)

    new_text = TUPLE_RE.sub(repl, text)
    if changes:
        Path(path).write_text(new_text, encoding="utf-8")
    return changes


def main():
    total = 0
    for path in SCRIPTS:
        n = process_file(path)
        if n:
            print(f"  {Path(path).name}: {n} cells changed")
            total += n
    print(f"\nTotal: {total} gloss cells stripped of ' forth' across {len(SCRIPTS)} scripts")


if __name__ == "__main__":
    main()
