"""Hand-curated TAM-phrase gloss overrides for Iakopo 6 — Allegory application / Final exhortation."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "jacob"
CHAPTER_NUM = 6
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 3, "behold,"),
        (4, 6, "my brethren,"),
        (7, 9, "as"),
        (10, 12, "I have said"),
        (13, 15, "unto you"),
        (16, 21, "I shall prophesy,"),
        (22, 22, "behold,"),
        (23, 25, "my prophecy"),
        (26, 26, "this—"),
        (27, 28, "the things"),
        (29, 32, "spake thereto"),
        (33, 34, "this prophet"),
        (35, 36, "Zenos,"),
        (37, 39, "concerning"),
        (40, 42, "the house"),
        (43, 43, "of Israel,"),
        (44, 44, "which"),
        (45, 49, "he likened thereto"),
        (50, 50, "them"),
        (51, 55, "unto a tame olive tree,"),
        (56, 60, "shall surely come to pass."),
    ],
    2: [
        (0, 0, "And"),
        (1, 3, "the day"),
        (4, 9, "shall set again thereto"),
        (10, 11, "by him"),
        (12, 13, "his hand"),
        (14, 18, "the second time"),
        (19, 22, "to recover his people,"),
        (23, 23, "that"),
        (24, 26, "the day,"),
        (27, 27, "yea,"),
        (28, 33, "even the last time,"),
        (34, 34, "wherein"),
        (35, 40, "shall go thereto"),
        (41, 44, "the servants of the Lord"),
        (45, 47, "in his power,"),
        (48, 49, "to nourish"),
        (50, 51, "and prune"),
        (52, 53, "his vineyard;"),
        (54, 54, "and"),
        (55, 57, "after that,"),
        (58, 60, "soon"),
        (61, 63, "cometh"),
        (64, 66, "the end."),
    ],
    3: [
        (0, 0, "And"),
        (1, 4, "blessed indeed are they"),
        (5, 6, "those who"),
        (7, 11, "have labored diligently"),
        (12, 14, "in his vineyard;"),
        (15, 15, "and"),
        (16, 18, "cursed indeed"),
        (19, 22, "those who"),
        (23, 26, "shall"),
        (27, 29, "be cast"),
        (30, 34, "into their own place!"),
        (35, 35, "And"),
        (36, 38, "shall be burned"),
        (39, 41, "the world"),
        (42, 44, "with fire."),
    ],
    4: [
        (0, 0, "And"),
        (1, 4, "is merciful"),
        (5, 7, "our God"),
        (8, 11, "unto us,"),
        (12, 12, "for"),
        (13, 16, "he remembereth"),
        (17, 20, "the house of Israel,"),
        (21, 21, "both"),
        (22, 23, "roots"),
        (24, 25, "and branches;"),
        (26, 26, "and"),
        (27, 31, "he stretcheth"),
        (32, 35, "his hands unto them"),
        (36, 39, "all the day long;"),
        (40, 40, "and"),
        (41, 43, "they are"),
        (44, 46, "a stiffnecked people"),
        (47, 50, "and a gainsaying;"),
        (51, 51, "but"),
        (52, 57, "as many of them"),
        (58, 65, "as will not harden their hearts"),
        (66, 69, "shall be saved"),
        (70, 72, "in the kingdom"),
        (73, 75, "of the God."),
    ],
    5: [
        (0, 3, "Wherefore,"),
        (4, 7, "my beloved brethren,"),
        (8, 11, "I beseech"),
        (12, 14, "unto you"),
        (15, 19, "in words of soberness"),
        (20, 22, "that ye repent,"),
        (23, 23, "and"),
        (24, 26, "come"),
        (27, 33, "with full purpose of heart,"),
        (34, 36, "and cleave"),
        (37, 39, "unto the God"),
        (40, 45, "as he cleaveth"),
        (46, 48, "unto you."),
        (49, 49, "And"),
        (50, 54, "while extendeth"),
        (55, 55, "his hand"),
        (56, 58, "of mercy"),
        (59, 61, "unto you"),
        (62, 64, "in the light"),
        (65, 67, "of the day,"),
        (68, 69, "harden not"),
        (70, 73, "your hearts."),
    ],
    6: [
        (0, 0, "Yea,"),
        (1, 3, "today,"),
        (4, 7, "if ye will hear"),
        (8, 10, "his voice,"),
        (11, 13, "harden not"),
        (14, 16, "your hearts;"),
        (17, 17, "for"),
        (18, 18, "why"),
        (19, 23, "shall ye choose thereto"),
        (24, 25, "to die"),
        (26, 26, "ye?"),
    ],
    7: [
        (0, 1, "For behold,"),
        (2, 5, "after"),
        (6, 6, "fed"),
        (7, 9, "ye have been"),
        (10, 12, "all the day"),
        (13, 19, "with the good word of God,"),
        (20, 25, "shall ye bring forth indeed"),
        (26, 28, "evil fruit,"),
        (29, 33, "shall ye thereto"),
        (34, 35, "be hewn down"),
        (36, 38, "ye"),
        (39, 40, "and cast"),
        (41, 43, "into the fire?"),
    ],
    8: [
        (0, 0, "Behold,"),
        (1, 6, "will ye reject thereto these words?"),
        (7, 13, "Will ye reject thereto the words of the prophets;"),
        (14, 14, "and"),
        (15, 26, "will ye reject all the words which have been spoken concerning Christ,"),
        (27, 32, "after so many have spoken"),
        (33, 40, "concerning him;"),
        (41, 41, "and"),
        (42, 47, "deny the good word of Christ,"),
        (48, 53, "and the power of God,"),
        (54, 60, "and the gift of the Holy Spirit,"),
        (61, 65, "and quench the Holy Spirit,"),
        (66, 75, "and make a mock of the great plan of redemption,"),
        (76, 81, "which hath been laid for you?"),
    ],
    9: [
        (0, 4, "Know ye not"),
        (5, 10, "if ye do these things,"),
        (11, 15, "shall bring you"),
        (16, 24, "the power of redemption and resurrection,"),
        (25, 27, "which is in Christ,"),
        (28, 33, "ye shall stand with shame"),
        (34, 37, "and awful guilt"),
        (38, 39, "before"),
        (40, 43, "the bar"),
        (44, 46, "of the God?"),
    ],
    10: [
        (0, 0, "And"),
        (1, 2, "according to"),
        (3, 5, "the power"),
        (6, 8, "of justice,"),
        (9, 9, "for"),
        (10, 13, "cannot"),
        (14, 17, "be denied justice,"),
        (18, 25, "ye shall go away thereto"),
        (26, 32, "into that lake of fire and brimstone,"),
        (33, 33, "which"),
        (34, 38, "is unquenchable its flames,"),
        (39, 39, "and"),
        (40, 42, "its smoke"),
        (43, 46, "ascendeth up"),
        (47, 48, "above"),
        (49, 52, "forever and ever,"),
        (53, 59, "which lake of fire and brimstone"),
        (60, 63, "is the torment"),
        (64, 66, "endless."),
    ],
    11: [
        (0, 3, "O then,"),
        (4, 7, "my beloved brethren,"),
        (8, 10, "repent ye,"),
        (11, 13, "and enter ye"),
        (14, 18, "in at the strait gate,"),
        (19, 22, "and continue still"),
        (23, 27, "in the way that is narrow,"),
        (28, 30, "until"),
        (31, 32, "ye obtain"),
        (33, 35, "the life"),
        (36, 36, "eternal."),
    ],
    12: [
        (0, 0, "O,"),
        (1, 3, "be wise ye!"),
        (4, 9, "What more can I"),
        (10, 12, "may"),
        (13, 16, "I say?"),
    ],
    13: [
        (0, 1, "Finally,"),
        (2, 5, "I bid farewell"),
        (6, 8, "unto you,"),
        (9, 12, "until I shall meet"),
        (13, 14, "with you"),
        (15, 16, "before"),
        (17, 21, "the pleasing bar"),
        (22, 24, "of the God,"),
        (25, 28, "which bar"),
        (29, 32, "smiteth thereto"),
        (33, 35, "the wicked"),
        (36, 38, "with awful"),
        (39, 41, "and dread"),
        (42, 42, "terrible."),
        (43, 43, "Amen."),
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
