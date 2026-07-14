"""Hand-curated TAM-phrase gloss overrides for 2 Nifae 22 — Isaiah 12."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "2nephi"
CHAPTER_NUM = 22
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "And"),
        (1, 3, "in that day"),
        (4, 7, "shalt thou"),
        (8, 10, "say thereto:"),
        (11, 13, "O Lord,"),
        (14, 17, "I will"),
        (18, 19, "praise"),
        (20, 22, "thee;"),
        (23, 25, "though"),
        (26, 29, "wast thou angry"),
        (30, 32, "with me"),
        (33, 33, "but"),
        (34, 36, "is turned away"),
        (37, 38, "thy anger,"),
        (39, 39, "and"),
        (40, 43, "thou hast comforted"),
        (44, 46, "me."),
    ],
    2: [
        (0, 0, "Behold,"),
        (1, 3, "the God"),
        (4, 6, "is my salvation"),
        (7, 7, "this;"),
        (8, 12, "I will trust"),
        (13, 14, "thereto,"),
        (15, 17, "and I not"),
        (18, 18, "fear;"),
        (19, 19, "for"),
        (20, 22, "the Lord"),
        (23, 24, "Jehovah"),
        (25, 27, "my strength"),
        (28, 28, "and"),
        (29, 30, "my song"),
        (31, 31, "this;"),
        (32, 33, "is become"),
        (34, 34, "also"),
        (35, 36, "he"),
        (37, 37, "as"),
        (38, 39, "my salvation."),
    ],
    3: [
        (0, 1, "Therefore,"),
        (2, 6, "shall ye draw"),
        (7, 7, "water"),
        (8, 10, "with joy"),
        (11, 11, "from"),
        (12, 12, "the wells"),
        (13, 15, "of salvation."),
    ],
    4: [
        (0, 0, "And"),
        (1, 3, "in that day"),
        (4, 7, "shall ye"),
        (8, 10, "say thereto:"),
        (11, 12, "praise ye"),
        (13, 14, "the Lord,"),
        (15, 16, "call"),
        (17, 19, "upon his name,"),
        (20, 21, "declare"),
        (22, 23, "his doings"),
        (24, 25, "in the midst"),
        (26, 28, "of the people,"),
        (29, 30, "make mention"),
        (31, 32, "is exalted"),
        (33, 34, "his name."),
    ],
    5: [
        (0, 1, "sing"),
        (2, 2, "ye"),
        (3, 5, "unto the Lord;"),
        (6, 6, "for"),
        (7, 8, "hath done"),
        (9, 10, "by him"),
        (11, 11, "things"),
        (12, 15, "excellent good;"),
        (16, 17, "is known"),
        (18, 19, "this thing"),
        (20, 22, "in the earth"),
        (23, 23, "whole."),
    ],
    6: [
        (0, 1, "cry out"),
        (2, 2, "and"),
        (3, 4, "shout,"),
        (5, 6, "thou one who"),
        (7, 8, "dwells"),
        (9, 10, "in Zion;"),
        (11, 11, "for"),
        (12, 13, "is great"),
        (14, 17, "the Holy One"),
        (18, 19, "of Israel"),
        (20, 22, "is in the midst"),
        (23, 25, "of thee."),
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
