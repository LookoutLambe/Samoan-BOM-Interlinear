"""Hand-curated TAM-phrase gloss overrides for 2 Nifae 32 — Pray always / Holy Ghost teaches."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "2nephi"
CHAPTER_NUM = 32
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 3, "behold,"),
        (4, 7, "O my beloved brethren,"),
        (8, 10, "I suppose"),
        (11, 15, "ye are pondering"),
        (16, 19, "in your hearts"),
        (20, 22, "concerning"),
        (23, 23, "the things"),
        (24, 26, "ought"),
        (27, 28, "ye do"),
        (29, 32, "after"),
        (33, 35, "ye enter"),
        (36, 38, "in the way."),
        (39, 40, "But, behold,"),
        (41, 41, "why"),
        (42, 47, "ye are pondering thereto"),
        (48, 50, "of these things"),
        (51, 54, "in your hearts?"),
    ],
    2: [
        (0, 4, "Remember ye not indeed"),
        (5, 8, "I have said"),
        (9, 11, "unto you"),
        (12, 16, "after ye have received"),
        (17, 20, "the Holy Spirit"),
        (21, 25, "ye may"),
        (26, 27, "ye speak"),
        (28, 30, "in the language"),
        (31, 32, "of angels?"),
        (33, 35, "And now,"),
        (36, 40, "how can"),
        (41, 42, "ye speak"),
        (43, 45, "in the language"),
        (46, 47, "of angels"),
        (48, 49, "save thereto"),
        (50, 52, "by way of"),
        (53, 56, "the Holy Spirit?"),
    ],
    3: [
        (0, 1, "speak"),
        (2, 2, "angels"),
        (3, 5, "by the power"),
        (6, 9, "of the Holy Spirit;"),
        (10, 13, "wherefore,"),
        (14, 17, "they speak"),
        (18, 18, "the words"),
        (19, 20, "of Christ."),
        (21, 24, "Wherefore,"),
        (25, 29, "I have said thereto"),
        (30, 32, "unto you,"),
        (33, 35, "feast joyfully"),
        (36, 37, "on the words"),
        (38, 39, "of Christ;"),
        (40, 41, "for behold,"),
        (42, 43, "the words"),
        (44, 45, "of Christ"),
        (46, 50, "shall tell"),
        (51, 51, "thereto"),
        (52, 54, "unto you"),
        (55, 56, "all things"),
        (57, 59, "must"),
        (60, 61, "ye do."),
    ],
    4: [
        (0, 3, "Wherefore,"),
        (4, 5, "now,"),
        (6, 11, "after I have spoken"),
        (12, 14, "these words,"),
        (15, 19, "if ye understand not"),
        (20, 21, "thereto,"),
        (22, 24, "the reason is"),
        (25, 29, "ye ask not,"),
        (30, 32, "neither knock;"),
        (33, 36, "wherefore,"),
        (37, 40, "are not brought thereto"),
        (41, 41, "ye"),
        (42, 44, "into the light,"),
        (45, 45, "but"),
        (46, 50, "ye shall perish"),
        (51, 53, "in the dark."),
    ],
    5: [
        (0, 1, "For behold,"),
        (2, 6, "I again say"),
        (7, 9, "unto you"),
        (10, 14, "if ye shall enter"),
        (15, 17, "in the way,"),
        (18, 19, "and receive"),
        (20, 22, "the Holy Spirit,"),
        (23, 27, "shall show"),
        (28, 29, "by him"),
        (30, 32, "unto you"),
        (33, 34, "all things"),
        (35, 37, "must"),
        (38, 39, "ye do."),
    ],
    6: [
        (0, 0, "Behold,"),
        (1, 5, "this is the doctrine"),
        (6, 7, "of Christ,"),
        (8, 8, "and"),
        (9, 13, "there shall be no more"),
        (14, 17, "any other doctrine"),
        (18, 20, "given"),
        (21, 23, "until"),
        (24, 26, "he show"),
        (27, 29, "himself"),
        (30, 32, "unto you"),
        (33, 36, "in the flesh."),
        (37, 37, "And"),
        (38, 42, "when he shall show"),
        (43, 45, "himself"),
        (46, 48, "unto you"),
        (49, 52, "in the flesh,"),
        (53, 55, "all things"),
        (56, 60, "he shall speak"),
        (61, 61, "thereto"),
        (62, 63, "he"),
        (64, 66, "unto you,"),
        (67, 69, "ye do."),
    ],
    7: [
        (0, 2, "And now,"),
        (3, 6, "I, Nephi,"),
        (7, 10, "cannot"),
        (11, 13, "I say"),
        (14, 16, "any more words;"),
        (17, 18, "hath constrained"),
        (19, 21, "by the Spirit"),
        (22, 24, "my speaking,"),
        (25, 28, "and leaveth me thereto"),
        (29, 31, "I mourn"),
        (32, 33, "because of"),
        (34, 36, "the unbelief,"),
        (37, 39, "and the wickedness,"),
        (40, 42, "and the ignorance,"),
        (43, 46, "and the stiffneckedness"),
        (47, 48, "of men;"),
        (49, 49, "for"),
        (50, 54, "they will not search"),
        (55, 56, "knowledge,"),
        (57, 59, "nor would understand"),
        (60, 63, "great knowledge,"),
        (64, 68, "though given"),
        (69, 72, "unto them"),
        (73, 75, "in plainness,"),
        (76, 78, "according to"),
        (79, 80, "the plainness"),
        (81, 83, "may"),
        (84, 86, "reach thereto"),
        (87, 88, "a word."),
    ],
    8: [
        (0, 2, "And now,"),
        (3, 6, "O my beloved brethren,"),
        (7, 10, "I perceive"),
        (11, 16, "ye are pondering still"),
        (17, 20, "in your hearts;"),
        (21, 21, "and"),
        (22, 25, "I do grieve verily"),
        (26, 30, "because must"),
        (31, 33, "I speak"),
        (34, 36, "concerning"),
        (37, 38, "this thing."),
        (39, 39, "For"),
        (40, 43, "if ye would hearken"),
        (44, 46, "to the Spirit"),
        (47, 49, "teacheth"),
        (50, 51, "a man"),
        (52, 53, "to pray,"),
        (54, 57, "ye would know"),
        (58, 60, "must"),
        (61, 62, "ye pray;"),
        (63, 63, "for"),
        (64, 66, "doth not teach"),
        (67, 70, "by the evil spirit"),
        (71, 72, "a man"),
        (73, 74, "to pray,"),
        (75, 75, "but"),
        (76, 79, "teacheth"),
        (80, 82, "him"),
        (83, 86, "should not"),
        (87, 87, "pray"),
        (88, 89, "he."),
    ],
    9: [
        (0, 1, "But behold,"),
        (2, 5, "I say"),
        (6, 8, "unto you"),
        (9, 11, "must"),
        (12, 13, "ye pray"),
        (14, 16, "without ceasing,"),
        (17, 20, "and not faint;"),
        (21, 21, "and"),
        (22, 25, "do not"),
        (26, 27, "anything"),
        (28, 30, "for the Lord"),
        (31, 32, "save thereto"),
        (33, 35, "first"),
        (36, 38, "ye pray"),
        (39, 41, "unto the Father"),
        (42, 44, "in the name"),
        (45, 46, "of Christ,"),
        (47, 49, "that may consecrate"),
        (50, 51, "by him"),
        (52, 54, "your works"),
        (55, 56, "for you,"),
        (57, 61, "that may become"),
        (62, 64, "your works"),
        (65, 67, "for the welfare"),
        (68, 71, "of your souls."),
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
