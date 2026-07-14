"""Hand-curated TAM-phrase gloss overrides for 2 Nifae 14 — Isaiah 4."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "2nephi"
CHAPTER_NUM = 14
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "And"),
        (1, 3, "in that day,"),
        (4, 8, "shall take hold thereto"),
        (9, 10, "women"),
        (11, 12, "seven"),
        (13, 14, "the man"),
        (15, 16, "one,"),
        (17, 18, "saying:"),
        (19, 23, "we will eat"),
        (24, 26, "our own"),
        (27, 27, "bread,"),
        (28, 28, "and"),
        (29, 29, "wear"),
        (30, 32, "our own"),
        (33, 33, "apparel;"),
        (34, 36, "but only"),
        (37, 39, "let be granted"),
        (40, 41, "to us"),
        (42, 43, "to be called"),
        (44, 46, "by thy name"),
        (47, 49, "to take away thereto"),
        (50, 52, "our reproach."),
    ],
    2: [
        (0, 2, "In that day"),
        (3, 6, "shall be beautiful"),
        (7, 9, "and glorious thereto"),
        (10, 11, "the branch"),
        (12, 14, "of the Lord;"),
        (15, 18, "shall be excellent"),
        (19, 19, "and"),
        (20, 20, "comely"),
        (21, 22, "the fruit"),
        (23, 25, "of the earth"),
        (26, 29, "unto them"),
        (30, 31, "who"),
        (32, 33, "are escaped"),
        (34, 35, "of Israel."),
    ],
    3: [
        (0, 0, "And"),
        (1, 5, "shall come"),
        (6, 6, "also,"),
        (7, 9, "they"),
        (10, 11, "who"),
        (12, 13, "are left"),
        (14, 15, "in Zion"),
        (16, 16, "and"),
        (17, 17, "who"),
        (18, 19, "dwell"),
        (20, 20, "still"),
        (21, 22, "in Jerusalem"),
        (23, 26, "shall be called"),
        (27, 28, "holy,"),
        (29, 31, "every one"),
        (32, 32, "all"),
        (33, 33, "that"),
        (34, 35, "is written"),
        (36, 37, "in the midst"),
        (38, 39, "of the men"),
        (40, 43, "the living"),
        (44, 45, "in Jerusalem—"),
    ],
    4: [
        (0, 3, "When"),
        (4, 5, "hath washed away"),
        (6, 8, "the Lord"),
        (9, 10, "the filth"),
        (11, 12, "of the daughters"),
        (13, 14, "of Zion,"),
        (15, 15, "and"),
        (16, 16, "hath purged"),
        (17, 18, "the blood"),
        (19, 20, "of Jerusalem"),
        (21, 21, "from"),
        (22, 23, "its midst"),
        (24, 24, "by"),
        (25, 26, "the spirit"),
        (27, 29, "of judgment"),
        (30, 30, "and"),
        (31, 32, "the spirit"),
        (33, 35, "of burning."),
    ],
    5: [
        (0, 0, "And"),
        (1, 4, "will create"),
        (5, 7, "the Lord"),
        (8, 9, "upon"),
        (10, 11, "the dwelling-places"),
        (12, 12, "every"),
        (13, 15, "of the mountain"),
        (16, 17, "of Zion,"),
        (18, 18, "and"),
        (19, 19, "upon"),
        (20, 22, "her assemblies,"),
        (23, 24, "a cloud"),
        (25, 25, "and"),
        (26, 27, "the smoke"),
        (28, 28, "by"),
        (29, 30, "the day,"),
        (31, 31, "and"),
        (32, 33, "the shining"),
        (34, 36, "of the fire"),
        (37, 37, "flaming"),
        (38, 40, "by night;"),
        (41, 41, "for"),
        (42, 46, "there shall be"),
        (47, 48, "upon"),
        (49, 51, "the glory"),
        (52, 52, "all"),
        (53, 54, "of Zion"),
        (55, 57, "a defence."),
    ],
    6: [
        (0, 0, "And"),
        (1, 5, "there shall be"),
        (6, 8, "a tabernacle"),
        (9, 9, "for"),
        (10, 11, "a shadow"),
        (12, 14, "in the daytime"),
        (15, 17, "from the heat,"),
        (18, 18, "and"),
        (19, 19, "for"),
        (20, 21, "a place"),
        (22, 22, "of refuge,"),
        (23, 23, "and"),
        (24, 25, "a covert"),
        (26, 28, "from storm"),
        (29, 29, "and"),
        (30, 32, "from rain."),
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
