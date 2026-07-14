"""Hand-curated TAM-phrase gloss overrides for 2 Nifae 7 — Isaiah 50."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "2nephi"
CHAPTER_NUM = 7
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "Yea,"),
        (1, 1, "for"),
        (2, 4, "thus"),
        (5, 6, "saith"),
        (7, 9, "the Lord:"),
        (10, 12, "Have I"),
        (13, 14, "put away"),
        (15, 15, "thee,"),
        (16, 18, "or have I"),
        (19, 21, "cast off"),
        (22, 22, "thee"),
        (23, 24, "forever?"),
        (25, 27, "For thus"),
        (28, 30, "saith the Lord"),
        (31, 33, ":"),
        (34, 35, "Where is"),
        (36, 37, "the bill"),
        (38, 38, "of divorce"),
        (39, 41, "of the divorcement"),
        (42, 44, "of thy mother?"),
        (45, 46, "To whom"),
        (47, 49, "have I put"),
        (50, 53, "away"),
        (54, 54, "thee,"),
        (55, 58, "or to which person"),
        (59, 62, "of my creditors"),
        (63, 66, "have I sold"),
        (67, 68, "thereto"),
        (69, 69, "you?"),
        (70, 70, "Yea,"),
        (71, 73, "to whom"),
        (74, 76, "have I sold"),
        (77, 80, "forth you?"),
        (81, 81, "Behold,"),
        (82, 85, "ye have sold"),
        (86, 86, "ye"),
        (87, 87, "yourselves"),
        (88, 89, "because of"),
        (90, 92, "your iniquities,"),
        (93, 96, "and is put away"),
        (97, 99, "your mother"),
        (100, 101, "because of"),
        (102, 104, "your transgressions."),
    ],
    2: [
        (0, 3, "Wherefore,"),
        (4, 5, "when"),
        (6, 7, "I came,"),
        (8, 11, "there was no man;"),
        (12, 13, "when"),
        (14, 16, "I called,"),
        (17, 17, "yea,"),
        (18, 21, "there was none"),
        (22, 23, "to answer"),
        (24, 24, "back."),
        (25, 25, "O,"),
        (26, 28, "O the house"),
        (29, 30, "of Israel,"),
        (31, 34, "is shortened"),
        (35, 36, "my hand"),
        (37, 40, "cannot"),
        (41, 42, "redeem,"),
        (43, 45, "or have"),
        (46, 47, "no"),
        (48, 49, "power"),
        (50, 53, "for me to"),
        (54, 55, "deliver?"),
        (56, 56, "Behold,"),
        (57, 59, "at my rebuke"),
        (60, 63, "I dry up"),
        (64, 65, "the sea,"),
        (66, 69, "and I make"),
        (70, 72, "their rivers"),
        (73, 75, "a wilderness"),
        (76, 78, "and their"),
        (79, 80, "fish to"),
        (81, 82, "stink because"),
        (83, 84, "are dried up"),
        (85, 86, "the waters,"),
        (87, 89, "and they die"),
        (90, 91, "they"),
        (92, 93, "because of"),
        (94, 96, "thirst."),
    ],
    3: [
        (0, 2, "I clothe"),
        (3, 4, "the heavens"),
        (5, 7, "with blackness,"),
        (8, 10, "and I make"),
        (11, 13, "sackcloth"),
        (14, 17, "their covering."),
    ],
    4: [
        (0, 2, "Hath given"),
        (3, 5, "me"),
        (6, 8, "the Lord"),
        (9, 10, "God"),
        (11, 12, "the tongue"),
        (13, 13, "of"),
        (14, 16, "the learned,"),
        (17, 20, "that I should know"),
        (21, 22, "the way"),
        (23, 26, "to speak"),
        (27, 28, "a word"),
        (29, 31, "unto thee"),
        (32, 34, "in the time"),
        (35, 37, "in season,"),
        (38, 38, "O,"),
        (39, 41, "O the house"),
        (42, 43, "of Israel."),
        (44, 47, "When ye are weary"),
        (48, 50, "he waketh"),
        (51, 52, "he"),
        (53, 55, "morning"),
        (56, 58, "by morning."),
        (59, 62, "He waketh"),
        (63, 64, "mine ear"),
        (65, 66, "to hear"),
        (67, 69, "as"),
        (70, 72, "the learned."),
    ],
    5: [
        (0, 2, "The Lord"),
        (3, 4, "God"),
        (5, 6, "hath opened"),
        (7, 8, "mine ear,"),
        (9, 12, "and I was not"),
        (13, 13, "rebellious,"),
        (14, 15, "neither turned"),
        (16, 18, "away back."),
    ],
    6: [
        (0, 3, "I gave"),
        (4, 5, "my back"),
        (6, 7, "to the"),
        (8, 9, "smiter,"),
        (10, 12, "and my cheeks"),
        (13, 15, "to them"),
        (16, 18, "that pluck"),
        (19, 20, "off"),
        (21, 22, "the hair."),
        (23, 25, "I did not"),
        (26, 26, "hide"),
        (27, 28, "my face"),
        (29, 31, "from shame"),
        (32, 34, "and spitting."),
    ],
    7: [
        (0, 0, "For"),
        (1, 3, "will"),
        (4, 5, "help"),
        (6, 7, "the Lord"),
        (8, 9, "God"),
        (10, 12, "me,"),
        (13, 16, "therefore"),
        (17, 20, "shall I"),
        (21, 22, "not be confounded"),
        (23, 23, "thereto."),
        (24, 27, "Therefore"),
        (28, 30, "have I set"),
        (31, 33, "stand firm"),
        (34, 35, "my face"),
        (36, 38, "like"),
        (39, 41, "a flint,"),
        (42, 45, "and I know"),
        (46, 48, "shall I"),
        (49, 50, "not be ashamed"),
        (51, 52, "indeed."),
    ],
    8: [
        (0, 3, "And is near"),
        (4, 5, "the Lord,"),
        (6, 8, "and he"),
        (9, 10, "justifieth me."),
        (11, 13, "Who"),
        (14, 15, "will contend"),
        (16, 17, "with me?"),
        (18, 19, "Let us"),
        (20, 22, "stand together."),
        (23, 25, "Who is"),
        (26, 27, "mine adversary?"),
        (28, 31, "Let him"),
        (32, 35, "come near"),
        (36, 38, "unto me,"),
        (39, 43, "and I will"),
        (44, 46, "smite him"),
        (47, 49, "with the strength"),
        (50, 52, "of my mouth."),
    ],
    9: [
        (0, 0, "For"),
        (1, 3, "will"),
        (4, 5, "help"),
        (6, 7, "the Lord"),
        (8, 9, "God"),
        (10, 12, "me."),
        (13, 17, "And all they"),
        (18, 19, "who"),
        (20, 22, "shall condemn"),
        (23, 23, "me,"),
        (24, 24, "behold,"),
        (25, 28, "all they"),
        (29, 31, "shall"),
        (32, 34, "wax old"),
        (35, 37, "as"),
        (38, 39, "a garment,"),
        (40, 43, "and shall"),
        (44, 44, "eat up"),
        (45, 46, "them"),
        (47, 48, "the moth."),
    ],
    10: [
        (0, 2, "Who is"),
        (3, 5, "among"),
        (6, 7, "you"),
        (8, 9, "that feareth"),
        (10, 12, "the Lord,"),
        (13, 14, "that obeyeth"),
        (15, 17, "the voice"),
        (18, 20, "of his servant,"),
        (21, 22, "that walketh"),
        (23, 25, "in darkness"),
        (26, 28, "and hath no"),
        (29, 30, "light?"),
    ],
    11: [
        (0, 0, "Behold"),
        (1, 2, "all ye"),
        (3, 4, "that"),
        (5, 6, "kindle"),
        (7, 7, "fire,"),
        (8, 10, "that ye"),
        (11, 12, "compass about"),
        (13, 14, "yourselves"),
        (15, 16, "with sparks,"),
        (17, 17, "walk"),
        (18, 20, "in the light"),
        (21, 24, "of your fire"),
        (25, 26, "and in the sparks"),
        (27, 29, "which ye have kindled."),
        (30, 33, "This"),
        (34, 37, "shall ye"),
        (38, 39, "have"),
        (40, 41, "of mine hand—"),
        (42, 44, "shall"),
        (45, 46, "ye lie down"),
        (47, 47, "down"),
        (48, 50, "in sorrow."),
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
