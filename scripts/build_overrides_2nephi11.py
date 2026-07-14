"""Hand-curated TAM-phrase gloss overrides for 2 Nifae 11 — Nephi's testimony of Isaiah."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "2nephi"
CHAPTER_NUM = 11
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "many"),
        (5, 5, "things"),
        (6, 9, "spake thereto"),
        (10, 10, "Jacob"),
        (11, 13, "unto my people"),
        (14, 16, "at the time"),
        (17, 17, "that;"),
        (18, 21, "nevertheless"),
        (22, 23, "are only"),
        (24, 25, "these things"),
        (26, 28, "I caused"),
        (29, 30, "to be written,"),
        (31, 32, "for"),
        (33, 33, "the things"),
        (34, 36, "I have written"),
        (37, 38, "sufficeth"),
        (39, 41, "me."),
    ],
    2: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Nephi,"),
        (7, 9, "write"),
        (10, 11, "more"),
        (12, 12, "words"),
        (13, 14, "many"),
        (15, 16, "of Isaiah,"),
        (17, 17, "for"),
        (18, 19, "delighteth"),
        (20, 21, "my soul"),
        (22, 24, "in his words."),
        (25, 25, "For"),
        (26, 30, "I will liken"),
        (31, 32, "his words"),
        (33, 35, "unto my people,"),
        (36, 36, "and"),
        (37, 42, "I will send"),
        (43, 44, "the words"),
        (45, 47, "unto my children"),
        (48, 48, "all,"),
        (49, 49, "for"),
        (50, 51, "saw"),
        (52, 53, "verily"),
        (54, 55, "he"),
        (56, 58, "my Redeemer,"),
        (59, 62, "even as"),
        (63, 64, "I saw"),
        (65, 67, "him."),
    ],
    3: [
        (0, 0, "And"),
        (1, 3, "my brother,"),
        (4, 5, "Jacob,"),
        (6, 8, "also saw"),
        (9, 11, "him"),
        (12, 14, "as"),
        (15, 17, "I saw"),
        (18, 20, "him;"),
        (21, 24, "wherefore,"),
        (25, 31, "I will send thereto"),
        (32, 34, "their words"),
        (35, 37, "unto my children"),
        (38, 40, "to prove thereto"),
        (41, 44, "unto them"),
        (45, 46, "are true"),
        (47, 48, "my words."),
        (49, 52, "Wherefore,"),
        (53, 54, "the words"),
        (55, 57, "of the three,"),
        (58, 61, "hath said"),
        (62, 63, "God,"),
        (64, 69, "I will establish thereto"),
        (70, 71, "my word."),
        (72, 75, "Nevertheless,"),
        (76, 78, "sendeth"),
        (79, 81, "by God"),
        (82, 83, "more"),
        (84, 84, "witnesses"),
        (85, 86, "many,"),
        (87, 87, "and"),
        (88, 89, "proveth"),
        (90, 91, "he"),
        (92, 93, "his words"),
        (94, 94, "all."),
    ],
    4: [
        (0, 0, "Behold,"),
        (1, 2, "delighteth"),
        (3, 4, "my soul"),
        (5, 8, "in the proving"),
        (9, 11, "unto my people"),
        (12, 13, "the truth"),
        (14, 17, "of the coming"),
        (18, 19, "of Christ;"),
        (20, 20, "for,"),
        (21, 23, "the end"),
        (24, 24, "this"),
        (25, 28, "hath been given"),
        (29, 30, "the law"),
        (31, 32, "of Moses;"),
        (33, 33, "and"),
        (34, 35, "the things"),
        (36, 36, "all"),
        (37, 39, "hath been given"),
        (40, 42, "by God"),
        (43, 45, "from the beginning"),
        (46, 48, "of the world,"),
        (49, 51, "unto man,"),
        (52, 54, "are typifyings"),
        (55, 56, "of him."),
    ],
    5: [
        (0, 0, "And"),
        (1, 3, "also delighteth"),
        (4, 5, "my soul"),
        (6, 7, "in the covenants"),
        (8, 10, "of the Lord"),
        (11, 14, "he hath made"),
        (15, 18, "unto our fathers;"),
        (19, 19, "yea,"),
        (20, 21, "delighteth"),
        (22, 23, "my soul"),
        (24, 24, "in"),
        (25, 25, "his"),
        (26, 27, "grace,"),
        (28, 28, "and"),
        (29, 30, "his justice,"),
        (31, 31, "and"),
        (32, 33, "the power,"),
        (34, 34, "and"),
        (35, 37, "tender mercy"),
        (38, 40, "in the plan"),
        (41, 41, "great"),
        (42, 43, "and eternal"),
        (44, 46, "of the deliverance"),
        (47, 49, "from death."),
    ],
    6: [
        (0, 0, "And"),
        (1, 2, "delighteth"),
        (3, 4, "my soul"),
        (5, 7, "in proving"),
        (8, 10, "unto my people"),
        (11, 12, "must perish"),
        (13, 14, "all men"),
        (15, 16, "save"),
        (17, 19, "should come"),
        (20, 20, "Christ."),
    ],
    7: [
        (0, 1, "For if"),
        (2, 3, "there is no"),
        (4, 5, "Christ"),
        (6, 7, "there is no"),
        (8, 9, "God;"),
        (10, 11, "and if"),
        (12, 13, "there is no"),
        (14, 15, "God"),
        (16, 17, "are no"),
        (18, 19, "us,"),
        (20, 21, "for"),
        (22, 23, "could be no"),
        (24, 25, "creation."),
        (26, 26, "But"),
        (27, 29, "there is"),
        (30, 30, "a"),
        (31, 31, "God,"),
        (32, 32, "and"),
        (33, 34, "he is"),
        (35, 36, "Christ,"),
        (37, 37, "and"),
        (38, 42, "he cometh"),
        (43, 45, "in the fulness"),
        (46, 48, "of his own"),
        (49, 49, "time."),
    ],
    8: [
        (0, 2, "And now,"),
        (3, 5, "I write"),
        (6, 7, "some"),
        (8, 9, "of the words"),
        (10, 11, "of Isaiah,"),
        (12, 13, "that"),
        (14, 14, "may"),
        (15, 18, "whoso"),
        (19, 21, "of my people"),
        (22, 23, "shall see"),
        (24, 26, "these words"),
        (27, 29, "lift up"),
        (30, 32, "their hearts"),
        (33, 33, "and"),
        (34, 34, "rejoice"),
        (35, 35, "for"),
        (36, 36, "men"),
        (37, 37, "all."),
        (38, 39, "Therefore"),
        (40, 41, "the words"),
        (42, 42, "these,"),
        (43, 43, "and"),
        (44, 46, "may"),
        (47, 47, "ye"),
        (48, 48, "liken"),
        (49, 50, "the words"),
        (51, 53, "unto you"),
        (54, 55, "and unto"),
        (56, 57, "all men."),
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
