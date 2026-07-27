"""
Hand-curated TAM-phrase gloss overrides for Mamona (Mormon) 6 — the last battle at
Cumorah: Mormon gathers all the Nephites to the land of Cumorah, hides up the records in
the hill save the few plates he gives to Moroni, and the Lamanites fall upon them; the
utter destruction of the Nephite nation, the death of the twenty-three commanders with
their ten thousands each, and Mormon's great lamentation over the slain — "O ye fair
ones, how could ye have departed from the ways of the Lord!"

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_mormon6.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "mormon"
CHAPTER_NUM = 6

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 5, "I finish"),
        (6, 7, "my record"),
        (8, 10, "concerning"),
        (11, 12, "the destruction"),
        (13, 15, "of my people,"),
        (16, 18, "the Nephites."),
        (19, 22, "And it came to pass that"),
        (23, 25, "we did march forth"),
        (26, 28, "before"),
        (29, 30, "the Lamanites."),
    ],
    2: [
        (0, 2, "And I,"),
        (3, 4, "Mormon,"),
        (5, 8, "wrote"),
        (9, 10, "an epistle"),
        (11, 13, "unto the king"),
        (14, 16, "of the Lamanites,"),
        (17, 20, "and desired"),
        (21, 23, "of him,"),
        (24, 27, "that he grant"),
        (28, 29, "us"),
        (30, 33, "that we might gather together"),
        (34, 36, "our people"),
        (37, 39, "unto the land"),
        (40, 41, "of Cumorah,"),
        (42, 44, "beside"),
        (45, 46, "a hill"),
        (47, 48, "which was called"),
        (49, 50, "Cumorah,"),
        (51, 53, "and there"),
        (54, 59, "we could give battle"),
        (60, 62, "with them."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 5, "did grant"),
        (6, 8, "the king"),
        (9, 11, "of the Lamanites"),
        (12, 14, "unto me"),
        (15, 16, "the thing"),
        (17, 20, "which I desired."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 6, "we did march forth"),
        (7, 9, "unto the land"),
        (10, 11, "of Cumorah,"),
        (12, 15, "and we did pitch"),
        (16, 18, "our tents"),
        (19, 19, "round about"),
        (20, 22, "the hill"),
        (23, 24, "of Cumorah;"),
        (25, 25, "and"),
        (26, 28, "it was a land"),
        (29, 32, "wherein were many waters,"),
        (33, 34, "rivers,"),
        (35, 36, "and fountains;"),
        (37, 37, "and"),
        (38, 39, "here"),
        (40, 42, "we did hope"),
        (43, 48, "we should gain"),
        (49, 52, "an advantage"),
        (53, 54, "over"),
        (55, 57, "the Lamanites."),
    ],
    5: [
        (0, 0, "And"),
        (1, 3, "when had passed away"),
        (4, 6, "the three hundred and eighty"),
        (7, 9, "and fourth"),
        (10, 11, "year,"),
        (12, 15, "we had gathered together"),
        (16, 19, "all our people"),
        (20, 21, "that remained"),
        (22, 24, "in the land"),
        (25, 26, "of Cumorah."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 6, "after"),
        (7, 9, "we had gathered together"),
        (10, 13, "all our people"),
        (14, 16, "in the land"),
        (17, 18, "of Cumorah,"),
        (19, 19, "behold,"),
        (20, 21, "I,"),
        (22, 23, "Mormon,"),
        (24, 28, "began to grow old;"),
        (29, 29, "and"),
        (30, 32, "seeing"),
        (33, 37, "this last struggle"),
        (38, 40, "of my people,"),
        (41, 41, "and"),
        (42, 44, "when had been commanded"),
        (45, 45, "me"),
        (46, 48, "by the Lord"),
        (49, 52, "that I should not give up"),
        (53, 53, "the records"),
        (54, 58, "which had been handed down"),
        (59, 62, "by our fathers,"),
        (63, 66, "lest they should fall"),
        (67, 68, "into the hands"),
        (69, 71, "of the Lamanites,"),
        (72, 75, "(for would be destroyed"),
        (76, 77, "them"),
        (78, 80, "by the Lamanites)"),
        (81, 82, "therefore"),
        (83, 86, "I made"),
        (87, 88, "this record"),
        (89, 90, "from the plates"),
        (91, 92, "of Nephi,"),
        (93, 93, "and"),
        (94, 95, "hid up"),
        (96, 98, "in the hill"),
        (99, 100, "Cumorah"),
        (101, 103, "all the records"),
        (104, 106, "which had been delivered"),
        (107, 109, "unto me"),
        (110, 112, "by the hand"),
        (113, 115, "of the Lord,"),
        (116, 117, "save it were"),
        (118, 121, "these few plates"),
        (122, 125, "which I gave"),
        (126, 128, "unto my son"),
        (129, 130, "Moroni."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 6, "did behold"),
        (7, 9, "my people,"),
        (10, 13, "and their wives"),
        (14, 17, "and their children,"),
        (18, 21, "the armies of the Lamanites"),
        (22, 25, "marching toward"),
        (26, 29, "them;"),
        (30, 30, "and"),
        (31, 33, "they did await"),
        (34, 35, "them,"),
        (36, 38, "with that"),
        (39, 40, "great fear"),
        (41, 43, "of death"),
        (44, 46, "which doth fill"),
        (47, 47, "the hearts"),
        (48, 51, "of them all"),
        (52, 53, "who"),
        (54, 55, "are wicked."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 6, "they came"),
        (7, 9, "to battle against"),
        (10, 13, "us,"),
        (14, 14, "and"),
        (15, 18, "every man was filled"),
        (19, 21, "with fear"),
        (22, 23, "because of"),
        (24, 26, "the exceeding great number"),
        (27, 30, "of their numbers."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 6, "they did fall upon"),
        (7, 9, "upon"),
        (10, 11, "my people"),
        (12, 14, "with the sword,"),
        (15, 17, "and with the bow,"),
        (18, 20, "and with the arrow,"),
        (21, 23, "and with the axe,"),
        (24, 28, "and with all manner of weapons"),
        (29, 30, "of war."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 5, "were hewn down"),
        (6, 7, "my people,"),
        (8, 8, "yea,"),
        (9, 10, "even"),
        (11, 14, "unto my ten thousand"),
        (15, 15, "even"),
        (16, 19, "who were"),
        (20, 21, "with me,"),
        (22, 25, "and I fell"),
        (26, 27, "and swooned"),
        (28, 32, "in the midst of them;"),
        (33, 33, "and"),
        (34, 37, "they passed by"),
        (38, 40, "by me"),
        (41, 41, "and"),
        (42, 45, "they did not end"),
        (46, 48, "my very life."),
    ],
    11: [
        (0, 4, "and after"),
        (5, 7, "they had gone forth"),
        (8, 11, "and hewn down"),
        (12, 14, "all my people"),
        (15, 16, "save"),
        (17, 21, "the twenty and four"),
        (22, 24, "of us,"),
        (25, 27, "(among whom was"),
        (28, 29, "in the number"),
        (30, 31, "my son"),
        (32, 33, "Moroni)"),
        (34, 34, "and"),
        (35, 37, "had been spared"),
        (38, 39, "we"),
        (40, 43, "among those slain"),
        (44, 47, "of our people,"),
        (48, 50, "we did behold"),
        (51, 53, "on the day"),
        (54, 56, "following,"),
        (57, 59, "from atop"),
        (60, 63, "the hill Cumorah,"),
        (64, 68, "when had returned"),
        (69, 70, "the Lamanites"),
        (71, 74, "to their camps,"),
        (75, 77, "the ten thousand"),
        (78, 80, "of my people"),
        (81, 84, "who had been hewn"),
        (85, 86, "down,"),
        (87, 91, "whom I had led"),
        (92, 93, "in the front."),
    ],
    12: [
        (0, 4, "And we also beheld"),
        (5, 7, "the ten thousand"),
        (8, 10, "of my people"),
        (11, 14, "who were led"),
        (15, 17, "by my son"),
        (18, 19, "Moroni."),
    ],
    13: [
        (0, 1, "And behold,"),
        (2, 4, "there fell also"),
        (5, 7, "the ten thousand"),
        (8, 9, "of Gidgiddonah,"),
        (10, 12, "and he also"),
        (13, 14, "in the midst"),
        (15, 17, "of them."),
    ],
    14: [
        (0, 3, "And there fell also"),
        (4, 4, "Lamah"),
        (5, 7, "together with"),
        (8, 10, "his ten thousand;"),
        (11, 14, "and there fell also"),
        (15, 15, "Gilgal"),
        (16, 17, "with"),
        (18, 20, "his ten thousand;"),
        (21, 24, "and there fell also"),
        (25, 25, "Limhah"),
        (26, 29, "with his ten thousand;"),
        (30, 33, "and there fell also"),
        (34, 34, "Jeneum"),
        (35, 38, "with his ten thousand;"),
        (39, 42, "and there fell also"),
        (43, 43, "Cumenihah,"),
        (44, 45, "and Moronihah,"),
        (46, 47, "and Antionum,"),
        (48, 49, "and Shiblom,"),
        (50, 51, "and Shem,"),
        (52, 53, "and Josh"),
        (54, 55, "with"),
        (56, 60, "each their ten thousand."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 7, "there were also"),
        (8, 11, "another ten"),
        (12, 16, "who were also slain"),
        (17, 19, "by the sword,"),
        (20, 21, "with"),
        (22, 26, "each their ten thousand;"),
        (27, 27, "yea,"),
        (28, 32, "even all my people,"),
        (33, 36, "save those"),
        (37, 39, "the twenty"),
        (40, 42, "and four"),
        (43, 45, "who were"),
        (46, 48, "with me,"),
        (49, 52, "and also some others"),
        (53, 54, "few"),
        (55, 59, "who had escaped"),
        (60, 63, "into the south countries,"),
        (64, 66, "and a few"),
        (67, 71, "who had gone over"),
        (72, 74, "and had joined"),
        (75, 77, "the Lamanites,"),
        (78, 79, "had fallen;"),
        (80, 82, "and there lay"),
        (83, 85, "their flesh,"),
        (86, 87, "and bones,"),
        (88, 89, "and blood"),
        (90, 94, "upon the face of the earth,"),
        (95, 96, "being left"),
        (97, 98, "by the hands"),
        (99, 102, "of those who slew"),
        (103, 104, "them"),
        (105, 107, "to moulder"),
        (108, 112, "upon the land,"),
        (113, 115, "and to crumble"),
        (116, 119, "and return"),
        (120, 123, "to their mother"),
        (124, 126, "the earth."),
    ],
    16: [
        (0, 2, "And was rent"),
        (3, 4, "my soul"),
        (5, 7, "with anguish,"),
        (8, 9, "because of"),
        (10, 13, "those of my people"),
        (14, 15, "who were slain,"),
        (16, 19, "and I cried:"),
    ],
    17: [
        (0, 4, "O ye fair ones,"),
        (5, 9, "how could it be"),
        (10, 10, "that"),
        (11, 13, "ye departed"),
        (14, 15, "from the ways"),
        (16, 18, "of the Lord!"),
        (19, 23, "O ye fair ones,"),
        (24, 28, "how could it be"),
        (29, 29, "that"),
        (30, 31, "ye have rejected"),
        (32, 33, "that Jesus,"),
        (34, 38, "who stood forth"),
        (39, 42, "with arms outstretched"),
        (43, 45, "to receive you!"),
    ],
    18: [
        (0, 0, "Behold,"),
        (1, 3, "had ye"),
        (4, 5, "not done"),
        (6, 7, "this thing,"),
        (8, 10, "ye would"),
        (11, 12, "not have fallen."),
        (13, 14, "But behold,"),
        (15, 17, "ye are fallen,"),
        (18, 21, "and I mourn"),
        (22, 24, "for the loss"),
        (25, 26, "of you."),
    ],
    19: [
        (0, 0, "O"),
        (1, 4, "ye sons and daughters"),
        (5, 6, "fair,"),
        (7, 10, "ye fathers and mothers,"),
        (11, 14, "ye husbands and wives,"),
        (15, 18, "ye fair ones,"),
        (19, 22, "how could it be"),
        (23, 23, "that"),
        (24, 25, "ye are fallen!"),
    ],
    20: [
        (0, 1, "But behold,"),
        (2, 5, "ye are gone,"),
        (6, 9, "and cannot"),
        (10, 12, "my sorrow"),
        (13, 16, "bring back again"),
        (17, 17, "you."),
    ],
    21: [
        (0, 2, "And soon"),
        (3, 5, "shall come"),
        (6, 8, "the day"),
        (9, 11, "when shall be clothed"),
        (12, 15, "your mortal bodies"),
        (16, 20, "with immortality,"),
        (21, 24, "and these bodies"),
        (25, 28, "which now"),
        (29, 31, "unto corruption"),
        (32, 34, "ere long"),
        (35, 37, "and become"),
        (38, 40, "incorruptible bodies;"),
        (41, 45, "and then must"),
        (46, 48, "ye stand"),
        (49, 53, "before the judgment-seat"),
        (54, 55, "of Christ,"),
        (56, 57, "to be judged"),
        (58, 60, "according to"),
        (61, 63, "your works;"),
        (64, 66, "if it so be"),
        (67, 69, "that ye are righteous,"),
        (70, 72, "then blessed"),
        (73, 74, "ye"),
        (75, 76, "with"),
        (77, 79, "your fathers"),
        (80, 84, "who have gone before"),
        (85, 87, "you."),
    ],
    22: [
        (0, 0, "O"),
        (1, 5, "would that ye had repented"),
        (6, 9, "before came"),
        (10, 12, "this great destruction"),
        (13, 15, "upon you."),
        (16, 17, "But behold,"),
        (18, 21, "ye are gone,"),
        (22, 24, "and knoweth"),
        (25, 27, "the Father,"),
        (28, 28, "yea,"),
        (29, 31, "the Eternal Father"),
        (32, 34, "of heaven,"),
        (35, 37, "your state;"),
        (38, 42, "and he dealeth"),
        (43, 45, "with you"),
        (46, 48, "according to"),
        (49, 50, "his justice"),
        (51, 54, "and his tender mercy."),
    ],
}


def build_words(source_words: list[dict], spec: list[tuple[int, int, str]]) -> list[dict]:
    next_expected = 0
    for start, end, _ in spec:
        if start != next_expected:
            raise ValueError(f"gap or overlap at index {start} (expected {next_expected})")
        if end < start or end >= len(source_words):
            raise ValueError(f"bad range {start}..{end} (source len {len(source_words)})")
        next_expected = end + 1
    if next_expected != len(source_words):
        raise ValueError(
            f"spec ends at {next_expected} but source has {len(source_words)} words"
        )

    out: list[dict] = []
    for start, end, gloss in spec:
        for i in range(start, end):
            out.append({"sm": source_words[i]["sm"], "en": "·"})
        out.append({"sm": source_words[end]["sm"], "en": gloss})
    return out


def main() -> None:
    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    book = next(b for b in books["books"] if b["id"] == BOOK_ID)
    chapter = next(c for c in book["chapters"] if c["num"] == CHAPTER_NUM)

    existing = {"version": 1, "verses": {}}
    if OVERRIDES_PATH.exists():
        existing = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))

    written = 0
    for verse in chapter["verses"]:
        spec = VERSE_SPECS.get(verse["num"])
        if not spec:
            continue
        try:
            new_words = build_words(verse["words"], spec)
        except ValueError as exc:
            print(f"v{verse['num']}: {exc}", file=sys.stderr)
            sys.exit(1)
        key = f"{BOOK_ID}|{CHAPTER_NUM}|{verse['num']}"
        existing["verses"][key] = new_words
        written += 1

    OVERRIDES_PATH.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {written} verse overrides to {OVERRIDES_PATH}")


if __name__ == "__main__":
    main()
