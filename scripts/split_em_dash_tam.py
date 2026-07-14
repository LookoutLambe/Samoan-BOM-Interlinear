"""Split all em-dash + TAM particle tokens (e.g. Atua—o → Atua—, o) in bom_books.json,
and shift affected per-verse override script indices accordingly.

After: o le a (and other TAM clusters) is no longer trapped in em-dash tokens."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
SCRIPTS_DIR = ROOT / "scripts"

# TAM particles that get trapped after em-dash
TAM_PARTICLES = {'e', 'o', 'a', 'ua', 'na', 'sa'}

BOOK_TO_SCRIPT_PREFIX = {
    "1nephi": "1nephi",
    "2nephi": "2nephi",
    "jacob": "jacob",
    "enos": "enos",
    "jarom": "jarom",
    "wom": "wom",
    "mosiah": "mosiah",
    "alma": "alma",
    "helaman": "helaman",
    "3nephi": "3nephi",
    "4nephi": "4nephi",
    "mormon": "mormon",
    "ether": "ether",
    "moroni": "moroni",
}


def find_splits():
    """Returns list of (book_id, chap_num, verse_num, em_idx) for each em-dash+TAM token,
    sorted descending by em_idx so we can split in-place without messing up indices."""
    data = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    splits = []
    for book in data["books"]:
        for chap in book["chapters"]:
            for v in chap["verses"]:
                for i, t in enumerate(v["words"]):
                    sm = t["sm"]
                    if "—" in sm:
                        parts = sm.split("—", 1)
                        if len(parts) == 2:
                            before, after = parts
                            if after in TAM_PARTICLES:
                                splits.append((book["id"], chap["num"], v["num"], i))
    return data, splits


def apply_token_splits(data, splits):
    """Apply splits in-place. Process splits in descending order of em_idx so earlier
    splits don't invalidate later indices within the same verse."""
    splits_by_verse: dict[tuple[str, int, int], list[int]] = {}
    for book_id, chap_num, verse_num, em_idx in splits:
        splits_by_verse.setdefault((book_id, chap_num, verse_num), []).append(em_idx)
    for key in splits_by_verse:
        splits_by_verse[key].sort(reverse=True)  # descending

    for book in data["books"]:
        for chap in book["chapters"]:
            for v in chap["verses"]:
                key = (book["id"], chap["num"], v["num"])
                if key not in splits_by_verse:
                    continue
                for em_idx in splits_by_verse[key]:
                    sm = v["words"][em_idx]["sm"]
                    before, after = sm.split("—", 1)
                    v["words"][em_idx:em_idx+1] = [
                        {"sm": f"{before}—", "en": ""},
                        {"sm": after, "en": ""},
                    ]


def shift_spec_indices(script_path: Path, verse_num: int, em_idx: int):
    """In the .py file, find the verse_num: [...] block, and shift all (s, e) indices
    where the boundary crosses em_idx. The OLD em_idx token (e.g. Atua—o) splits into
    em_idx (Atua—) and em_idx+1 (o). All OLD tokens with index > em_idx shift by +1.

    For each (s, e, gloss) in the spec:
      - if s > em_idx: (s+1, e+1, gloss)  [pure shift]
      - if s == em_idx+1: (s, e+1, gloss)  [absorbs freed particle, s stays, e shifts]
      - if s <= em_idx and e == em_idx: unchanged
      - if s <= em_idx and e > em_idx: shouldn't happen normally; (s, e+1)
    """
    text = script_path.read_text(encoding="utf-8")
    # Find the verse block: r"    VERSE_NUM: \[\n.*?\n    \]"
    pattern = rf"(    {verse_num}: \[\n)(.*?)(\n    \],?\n)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        print(f"  WARNING: verse {verse_num} not found in {script_path.name}")
        return False
    body = m.group(2)
    # Replace each (s, e, "...") tuple
    tuple_pattern = re.compile(r'\((\d+),\s*(\d+),\s*("(?:[^"\\]|\\.)*")\)')

    def repl(t_m):
        s = int(t_m.group(1))
        e = int(t_m.group(2))
        g = t_m.group(3)
        if s > em_idx:
            return f"({s+1}, {e+1}, {g})"
        if s == em_idx + 1:
            return f"({s}, {e+1}, {g})"
        if e > em_idx:
            return f"({s}, {e+1}, {g})"
        return t_m.group(0)

    new_body = tuple_pattern.sub(repl, body)
    new_text = text[: m.start(2)] + new_body + text[m.end(2):]
    script_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    data, splits = find_splits()
    print(f"Found {len(splits)} em-dash + TAM tokens to split")

    # Skip 2nephi 28:8 — already split
    splits = [s for s in splits if s != ("2nephi", 28, 8, 22)]
    print(f"After skipping already-split: {len(splits)}")

    # Group splits by verse, descending order within each verse
    splits_by_verse: dict[tuple[str, int, int], list[int]] = {}
    for book_id, chap_num, verse_num, em_idx in splits:
        splits_by_verse.setdefault((book_id, chap_num, verse_num), []).append(em_idx)
    for key in splits_by_verse:
        splits_by_verse[key].sort(reverse=True)

    # First, shift indices in override scripts (in descending order within each verse)
    for (book_id, chap_num, verse_num), em_indices in splits_by_verse.items():
        prefix = BOOK_TO_SCRIPT_PREFIX.get(book_id)
        if not prefix:
            print(f"  skip: no prefix for {book_id}")
            continue
        script_path = SCRIPTS_DIR / f"build_overrides_{prefix}{chap_num}.py"
        if not script_path.exists():
            print(f"  skip: no script for {book_id} chap {chap_num} (verse {verse_num} unchanged spec)")
            continue
        for em_idx in em_indices:
            ok = shift_spec_indices(script_path, verse_num, em_idx)
            if ok:
                print(f"  shifted {script_path.name} v{verse_num} em_idx={em_idx}")

    # Then apply the source data splits
    apply_token_splits(data, splits)
    BOOKS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {BOOKS_PATH}")


if __name__ == "__main__":
    main()
