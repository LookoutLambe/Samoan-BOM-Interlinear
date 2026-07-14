"""Hand-curated TAM-phrase gloss overrides for 1 Nifae 6."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 6
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Nephi,"),
        (7, 11, "do not give"),
        (12, 13, "the genealogy"),
        (14, 16, "of my fathers"),
        (17, 20, "in this part"),
        (21, 23, "of my record;"),
        (24, 28, "neither will I give"),
        (29, 32, "at any time"),
        (33, 35, "hereafter"),
        (36, 38, "upon"),
        (39, 40, "these plates"),
        (41, 44, "which I am writing;"),
        (45, 45, "for"),
        (46, 48, "it is given"),
        (49, 51, "in the record"),
        (52, 53, "which has been kept"),
        (54, 56, "by my father;"),
        (57, 60, "wherefore,"),
        (61, 64, "I do not write"),
        (65, 65, "it"),
        (66, 68, "in this work."),
    ],
    2: [
        (0, 3, "For it sufficeth me"),
        (4, 6, "to say"),
        (7, 10, "that we"),
        (11, 12, "are some"),
        (13, 15, "descended from"),
        (16, 17, "Joseph."),
    ],
    3: [
        (0, 3, "And it mattereth not"),
        (4, 6, "to me"),
        (7, 8, "if particularly"),
        (9, 12, "I should give"),
        (13, 16, "a full account"),
        (17, 19, "of all the things"),
        (20, 22, "of my father,"),
        (23, 26, "for cannot"),
        (27, 28, "be written"),
        (29, 30, "these things"),
        (31, 33, "upon"),
        (34, 35, "these plates,"),
        (36, 39, "for I desire"),
        (40, 41, "the space"),
        (42, 44, "that I may"),
        (45, 46, "write"),
        (47, 48, "the things"),
        (49, 51, "of God."),
    ],
    4: [
        (0, 3, "For the fulness"),
        (4, 6, "of mine intent"),
        (7, 9, "is that I may"),
        (10, 11, "persuade"),
        (12, 12, "men"),
        (13, 15, "to come"),
        (16, 17, "unto"),
        (18, 20, "the God of Abraham,"),
        (21, 25, "and the God of Isaac,"),
        (26, 30, "and the God of Jacob,"),
        (31, 33, "and be saved."),
    ],
    5: [
        (0, 3, "Wherefore,"),
        (4, 5, "the things"),
        (6, 9, "which please"),
        (10, 11, "the world"),
        (12, 15, "I do not write,"),
        (16, 18, "but the things"),
        (19, 22, "which please"),
        (23, 24, "God"),
        (25, 27, "and them"),
        (28, 29, "who"),
        (30, 33, "are not any"),
        (34, 36, "of the world."),
    ],
    6: [
        (0, 3, "Wherefore,"),
        (4, 8, "I shall give"),
        (9, 10, "a commandment"),
        (11, 13, "unto my seed,"),
        (14, 19, "that they shall not fill these plates"),
        (20, 24, "with things which are not of worth"),
        (25, 29, "unto the children of men."),
    ],
}


def build_words(source_words, spec):
    next_expected = 0
    for s, e, _ in spec:
        if s != next_expected: raise ValueError(f"gap at {s} expected {next_expected}")
        if e < s or e >= len(source_words): raise ValueError(f"bad range {s}..{e} src len {len(source_words)}")
        next_expected = e + 1
    if next_expected != len(source_words): raise ValueError(f"spec ends at {next_expected} src has {len(source_words)}")
    out = []
    for s, e, g in spec:
        for i in range(s, e): out.append({"sm": source_words[i]["sm"], "en": "·"})
        out.append({"sm": source_words[e]["sm"], "en": g})
    return out


def main():
    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    book = next(b for b in books["books"] if b["id"] == BOOK_ID)
    chapter = next(c for c in book["chapters"] if c["num"] == CHAPTER_NUM)
    existing = {"version": 1, "verses": {}}
    if OVERRIDES_PATH.exists():
        existing = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    n = 0
    for v in chapter["verses"]:
        spec = VERSE_SPECS.get(v["num"])
        if not spec: continue
        try:
            existing["verses"][f"{BOOK_ID}|{CHAPTER_NUM}|{v['num']}"] = build_words(v["words"], spec)
            n += 1
        except ValueError as exc:
            print(f"v{v['num']}: {exc}", file=sys.stderr); sys.exit(1)
    OVERRIDES_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {n} verse overrides to {OVERRIDES_PATH}")


if __name__ == "__main__":
    main()
