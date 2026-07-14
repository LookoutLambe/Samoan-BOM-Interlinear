"""Hand-curated TAM-phrase gloss overrides for 1 Nifae 9."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 9
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "And"),
        (1, 4, "all these things"),
        (5, 6, "saw,"),
        (7, 8, "and heard,"),
        (9, 12, "and spake"),
        (13, 14, "my father,"),
        (15, 15, "while"),
        (16, 18, "he dwelt"),
        (19, 21, "in a tent,"),
        (22, 24, "in the valley"),
        (25, 26, "of Lemuel,"),
        (27, 31, "and many more also"),
        (32, 34, "other things,"),
        (35, 38, "which cannot be"),
        (39, 39, "written"),
        (40, 42, "upon"),
        (43, 44, "these plates."),
    ],
    2: [
        (0, 2, "And now,"),
        (3, 5, "as"),
        (6, 8, "I spake"),
        (9, 11, "concerning"),
        (12, 13, "these plates,"),
        (14, 14, "behold"),
        (15, 19, "not on these plates"),
        (20, 23, "that I have made"),
        (24, 26, "a full account"),
        (27, 29, "of the history"),
        (30, 32, "of my people;"),
        (33, 35, "for the plates"),
        (36, 39, "I have made"),
        (40, 42, "a full account"),
        (43, 45, "of my people"),
        (46, 48, "I have called"),
        (49, 50, "Nephi;"),
        (51, 54, "wherefore,"),
        (55, 57, "are called"),
        (58, 61, "the plates of Nephi,"),
        (62, 63, "called"),
        (64, 67, "after mine own name;"),
        (68, 71, "and these plates"),
        (72, 74, "also are called"),
        (75, 78, "the plates of Nephi."),
    ],
    3: [
        (0, 3, "Nevertheless"),
        (4, 6, "I have received"),
        (7, 8, "a commandment"),
        (9, 11, "from the Lord"),
        (12, 14, "that I should"),
        (15, 16, "I make"),
        (17, 18, "these plates,"),
        (19, 22, "for the special purpose"),
        (23, 25, "that should be there"),
        (26, 27, "an account"),
        (28, 29, "engraven"),
        (30, 32, "of the ministry"),
        (33, 35, "of my people."),
    ],
    4: [
        (0, 2, "Upon"),
        (3, 4, "the other plates"),
        (5, 7, "should be"),
        (8, 9, "engraven"),
        (10, 11, "an account"),
        (12, 15, "of the reign of the kings,"),
        (16, 19, "and the wars and contentions"),
        (20, 22, "of my people;"),
        (23, 26, "wherefore"),
        (27, 29, "these plates"),
        (30, 33, "are the more part"),
        (34, 35, "concerning"),
        (36, 38, "the ministry"),
        (39, 41, "of my people;"),
        (42, 45, "and the other plates"),
        (46, 49, "the more part"),
        (50, 51, "concerning"),
        (52, 55, "the reign of the kings"),
        (56, 57, "and the wars"),
        (58, 59, "and contentions"),
        (60, 62, "of my people."),
    ],
    5: [
        (0, 3, "Wherefore,"),
        (4, 7, "have commanded me"),
        (8, 10, "the Lord"),
        (11, 13, "that I should make"),
        (14, 15, "these plates"),
        (16, 19, "for a wise purpose"),
        (20, 23, "in him,"),
        (24, 26, "a purpose"),
        (27, 30, "I know not."),
    ],
    6: [
        (0, 2, "But knoweth"),
        (3, 5, "the Lord"),
        (6, 7, "all things"),
        (8, 10, "from the beginning;"),
        (11, 14, "wherefore,"),
        (15, 17, "he prepareth"),
        (18, 19, "by him"),
        (20, 21, "a way"),
        (22, 24, "to accomplish"),
        (25, 27, "all his works"),
        (28, 31, "among"),
        (32, 34, "the children of men;"),
        (35, 36, "for behold,"),
        (37, 40, "he hath"),
        (41, 43, "all power"),
        (44, 46, "to fulfil"),
        (47, 49, "all his words."),
        (50, 53, "And thus it is."),
        (54, 54, "Amen."),
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
