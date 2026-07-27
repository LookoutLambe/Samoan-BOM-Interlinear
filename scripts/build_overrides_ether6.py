"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 6 — the Jaredites embark in
their barges; the Lord drives them across the great deep with a furious wind for 344
days, and they sing praises to the Lord night and day. They land in the promised land,
bow themselves upon the earth, and are humbled. Jared's brother grows old and, at the
people's request, they anoint a king before the brother of Jared dies; the people begin
to spread and multiply.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether6.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 6

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Moroni,"),
        (7, 10, "do proceed"),
        (11, 13, "to give"),
        (14, 17, "the record of Jared"),
        (18, 20, "and his brother."),
    ],
    2: [
        (0, 0, "For"),
        (1, 3, "it came to pass that"),
        (4, 6, "after"),
        (7, 7, "had prepared"),
        (8, 10, "the Lord"),
        (11, 11, "the stones"),
        (12, 14, "which had carried"),
        (15, 19, "by the brother of Jared"),
        (20, 22, "upon the mount,"),
        (23, 25, "came down"),
        (26, 29, "the brother of Jared"),
        (30, 32, "from the mount,"),
        (33, 36, "and he did put"),
        (37, 40, "in the barges"),
        (41, 42, "the stones"),
        (43, 44, "which were prepared,"),
        (45, 46, "one"),
        (47, 51, "at each of their ends;"),
        (52, 53, "and behold,"),
        (54, 57, "they did give forth"),
        (58, 59, "light"),
        (60, 61, "unto the barges."),
    ],
    3: [
        (0, 2, "And thus"),
        (3, 4, "did cause"),
        (5, 7, "the Lord"),
        (8, 11, "the stones to shine"),
        (12, 14, "in the darkness,"),
        (15, 18, "to give forth"),
        (19, 20, "light"),
        (21, 22, "unto men,"),
        (23, 23, "women,"),
        (24, 25, "and children,"),
        (26, 31, "that they should not cross"),
        (32, 35, "over the great deep"),
        (36, 38, "in darkness."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 8, "when they had prepared"),
        (9, 12, "all kinds of food"),
        (13, 14, "of every sort,"),
        (15, 19, "that they might be able"),
        (20, 21, "to live thereby"),
        (22, 26, "upon the water,"),
        (27, 29, "and also food"),
        (30, 33, "for their flocks"),
        (34, 35, "and herds,"),
        (36, 39, "and whatsoever living thing"),
        (40, 43, "or beast"),
        (44, 48, "or bird"),
        (49, 53, "they should take"),
        (54, 57, "together with them—"),
        (58, 61, "and it came to pass that"),
        (62, 64, "after"),
        (65, 66, "they had done"),
        (67, 70, "all these things"),
        (71, 73, "they went aboard"),
        (74, 77, "into their ships"),
        (78, 80, "or barges,"),
        (81, 83, "and set forth"),
        (84, 86, "into the sea,"),
        (87, 89, "and committing"),
        (90, 92, "themselves"),
        (93, 95, "unto the Lord"),
        (96, 98, "their God."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 4, "caused"),
        (5, 9, "the Lord God"),
        (10, 12, "that there should blow"),
        (13, 15, "a mighty wind"),
        (16, 18, "which did blow"),
        (19, 23, "upon the face of the waters,"),
        (24, 26, "toward"),
        (27, 29, "the land"),
        (30, 31, "which was promised;"),
        (32, 34, "and thus"),
        (35, 37, "were tossed about"),
        (38, 39, "they"),
        (40, 43, "upon the waves"),
        (44, 46, "of the sea"),
        (47, 49, "driven before"),
        (50, 52, "the wind."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 5, "many times"),
        (6, 8, "were buried"),
        (9, 10, "they"),
        (11, 13, "in the depths"),
        (14, 16, "of the sea,"),
        (17, 18, "because of"),
        (19, 20, "the mountain billows"),
        (21, 22, "which broke"),
        (23, 26, "upon them,"),
        (27, 30, "and also the great tempests"),
        (31, 32, "and terrible,"),
        (33, 35, "which came"),
        (36, 39, "from the great force"),
        (40, 42, "of the wind."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 6, "when were buried"),
        (7, 8, "they"),
        (9, 11, "in the deep"),
        (12, 15, "there was no water"),
        (16, 19, "that could hurt them,"),
        (20, 23, "for were tight"),
        (24, 26, "their vessels"),
        (27, 31, "like unto a dish,"),
        (32, 36, "and also were tight"),
        (37, 38, "they"),
        (39, 43, "even as the ark"),
        (44, 45, "of Noah;"),
        (46, 47, "therefore"),
        (48, 51, "when encompassed about"),
        (52, 53, "them"),
        (54, 57, "by many waters"),
        (58, 61, "they did cry"),
        (62, 64, "unto the Lord,"),
        (65, 69, "and he brought again"),
        (70, 71, "them"),
        (72, 75, "upon the waters."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 7, "never ceased"),
        (8, 9, "the blowing"),
        (10, 12, "of the wind"),
        (13, 14, "toward"),
        (15, 17, "the land"),
        (18, 19, "of promise"),
        (20, 23, "while they continued"),
        (24, 27, "upon the waters;"),
        (28, 30, "and thus"),
        (31, 32, "were driven forth"),
        (33, 34, "they"),
        (35, 37, "onward before"),
        (38, 40, "the wind."),
    ],
    9: [
        (0, 4, "And they did sing"),
        (5, 5, "praises"),
        (6, 8, "unto the Lord;"),
        (9, 9, "yea,"),
        (10, 11, "did sing"),
        (12, 16, "the brother of Jared"),
        (17, 20, "praises unto the Lord,"),
        (21, 24, "and he did thank"),
        (25, 27, "and praise"),
        (28, 30, "unto the Lord"),
        (31, 34, "all the day long;"),
        (35, 39, "and when came"),
        (40, 41, "the night,"),
        (42, 45, "they ceased not"),
        (46, 48, "to praise"),
        (49, 51, "the Lord."),
    ],
    10: [
        (0, 2, "And thus"),
        (3, 6, "they were tossed forth"),
        (7, 8, "forward;"),
        (9, 13, "and there was no monster"),
        (14, 16, "of the sea"),
        (17, 20, "that could break"),
        (21, 21, "the barges,"),
        (22, 25, "nor a whale"),
        (26, 29, "that could mar"),
        (30, 31, "them;"),
        (32, 36, "and they still had"),
        (37, 38, "light"),
        (39, 41, "continually,"),
        (42, 44, "whether above"),
        (45, 47, "the water"),
        (48, 50, "or under"),
        (51, 53, "the water."),
    ],
    11: [
        (0, 2, "And thus"),
        (3, 6, "they were driven forth"),
        (7, 8, "forward,"),
        (9, 13, "three hundred and forty"),
        (14, 17, "and four days"),
        (18, 22, "upon the water."),
    ],
    12: [
        (0, 3, "And they did land"),
        (4, 8, "upon the shore"),
        (9, 11, "of the land"),
        (12, 13, "which was promised."),
        (14, 18, "And when they set foot"),
        (19, 23, "upon the shore"),
        (24, 26, "of the land"),
        (27, 28, "which was promised"),
        (29, 32, "they bowed themselves"),
        (33, 37, "upon the face of the land,"),
        (38, 39, "and humbled"),
        (40, 42, "themselves"),
        (43, 47, "before the Lord,"),
        (48, 49, "and did weep"),
        (50, 54, "with tears of joy"),
        (55, 59, "before the Lord,"),
        (60, 63, "because of the multitude"),
        (64, 68, "of his tender mercies"),
        (69, 72, "toward them."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 6, "they went forth"),
        (7, 11, "upon the land,"),
        (12, 15, "and began to till"),
        (16, 17, "the earth."),
    ],
    14: [
        (0, 3, "And had"),
        (4, 5, "Jared"),
        (6, 9, "four sons;"),
        (10, 14, "and they were named"),
        (15, 16, "Jacom,"),
        (17, 18, "and Gilgah,"),
        (19, 20, "and Mahah,"),
        (21, 22, "and Orihah."),
    ],
    15: [
        (0, 3, "And also begat"),
        (4, 8, "the brother of Jared"),
        (9, 12, "sons and daughters."),
    ],
    16: [
        (0, 3, "And the number"),
        (4, 7, "of Jared's friends"),
        (8, 10, "and his brother"),
        (11, 13, "was about"),
        (14, 18, "twenty and two"),
        (19, 19, "souls;"),
        (20, 24, "and they also begat"),
        (25, 27, "sons and daughters"),
        (28, 29, "before they"),
        (30, 33, "came"),
        (34, 36, "unto the land"),
        (37, 38, "of promise;"),
        (39, 40, "wherefore"),
        (41, 44, "began to be numerous"),
        (45, 46, "they."),
    ],
    17: [
        (0, 4, "And they were taught"),
        (5, 7, "to walk humbly"),
        (8, 12, "before the Lord;"),
        (13, 16, "and were also taught"),
        (17, 18, "they"),
        (19, 20, "from on high."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 7, "they began to spread"),
        (8, 12, "upon the land,"),
        (13, 14, "and to multiply"),
        (15, 16, "and to till"),
        (17, 18, "the earth;"),
        (19, 22, "and they became"),
        (23, 24, "strong"),
        (25, 27, "in the land."),
    ],
    19: [
        (0, 4, "And began to grow old"),
        (5, 8, "the brother of Jared,"),
        (9, 10, "and saw"),
        (11, 12, "was near"),
        (13, 17, "that he descend"),
        (18, 22, "down to the grave;"),
        (23, 26, "wherefore"),
        (27, 31, "he did say"),
        (32, 33, "unto Jared:"),
        (34, 36, "Let us gather"),
        (37, 39, "our people"),
        (40, 43, "that we may number"),
        (44, 45, "them,"),
        (46, 50, "that we may know"),
        (51, 54, "of them"),
        (55, 56, "the thing"),
        (57, 61, "they should desire"),
        (62, 65, "from us"),
        (66, 67, "before we"),
        (68, 71, "go down"),
        (72, 73, "below"),
        (74, 77, "into our graves."),
    ],
    20: [
        (0, 3, "And thus indeed"),
        (4, 6, "were assembled"),
        (7, 9, "the people."),
        (10, 14, "Now the number"),
        (15, 18, "of the sons and daughters"),
        (19, 23, "of the brother of Jared"),
        (24, 28, "were twenty and two"),
        (29, 29, "persons;"),
        (30, 33, "and the number"),
        (34, 37, "of the sons and daughters"),
        (38, 39, "of Jared"),
        (40, 44, "were twelve,"),
        (45, 46, "four"),
        (47, 48, "his sons."),
    ],
    21: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they numbered"),
        (6, 8, "their people;"),
        (9, 13, "and after that"),
        (14, 15, "they had numbered"),
        (16, 17, "them,"),
        (18, 21, "they desired"),
        (22, 25, "of them"),
        (26, 29, "the thing they desired"),
        (30, 32, "they should do"),
        (33, 34, "before they"),
        (35, 38, "went down"),
        (39, 40, "below"),
        (41, 44, "into their graves."),
    ],
    22: [
        (0, 3, "And it came to pass that"),
        (4, 5, "desired"),
        (6, 7, "the people"),
        (8, 11, "of them"),
        (12, 14, "that they should anoint"),
        (15, 16, "one"),
        (17, 20, "of their sons"),
        (21, 24, "to be king"),
        (25, 29, "over them."),
    ],
    23: [
        (0, 3, "And now behold,"),
        (4, 6, "were grieved"),
        (7, 8, "they"),
        (9, 12, "because of this thing."),
        (13, 16, "And said"),
        (17, 20, "the brother of Jared"),
        (21, 24, "unto them:"),
        (25, 27, "Surely"),
        (28, 30, "this thing"),
        (31, 34, "leadeth away"),
        (35, 37, "into bondage."),
    ],
    24: [
        (0, 3, "But said"),
        (4, 4, "Jared"),
        (5, 7, "unto his brother:"),
        (8, 9, "Suffer"),
        (10, 13, "unto them"),
        (14, 15, "that they have"),
        (16, 18, "a king of their own."),
        (19, 21, "And therefore"),
        (22, 26, "he did say"),
        (27, 30, "unto them:"),
        (31, 33, "Choose ye"),
        (34, 35, "from among"),
        (36, 39, "our sons,"),
        (40, 41, "one whom"),
        (42, 45, "ye desire."),
    ],
    25: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they chose"),
        (6, 9, "the eldest son"),
        (10, 14, "of the brother of Jared,"),
        (15, 17, "his name"),
        (18, 19, "was Pagag."),
        (20, 23, "And it came to pass that"),
        (24, 26, "he refused"),
        (27, 30, "and desired not"),
        (31, 33, "to become"),
        (34, 36, "their king."),
        (37, 39, "And desired"),
        (40, 41, "the people"),
        (42, 45, "that should compel him"),
        (46, 48, "his father,"),
        (49, 50, "but"),
        (51, 54, "was not willing"),
        (55, 56, "his father;"),
        (57, 62, "and he commanded them"),
        (63, 68, "that they should not compel"),
        (69, 70, "any man"),
        (71, 73, "to be"),
        (74, 76, "their king."),
    ],
    26: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they chose"),
        (6, 9, "all the brethren of Pagag,"),
        (10, 14, "and they desired not"),
        (15, 16, "it."),
    ],
    27: [
        (0, 3, "And it came to pass that"),
        (4, 7, "also desired not"),
        (8, 9, "it"),
        (10, 12, "the sons of Jared,"),
        (13, 16, "even all of them,"),
        (17, 18, "save"),
        (19, 20, "one;"),
        (21, 23, "and was anointed"),
        (24, 24, "Orihah"),
        (25, 28, "to be king"),
        (29, 33, "over the people."),
    ],
    28: [
        (0, 0, "And"),
        (1, 6, "he began to reign,"),
        (7, 11, "and began to prosper"),
        (12, 14, "the people;"),
        (15, 18, "and it came to pass that"),
        (19, 22, "they became exceedingly rich."),
    ],
    29: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Jared died,"),
        (6, 9, "and likewise also"),
        (10, 11, "his brother."),
    ],
    30: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Orihah walked"),
        (6, 8, "in humility"),
        (9, 13, "before the Lord,"),
        (14, 17, "and he remembered"),
        (18, 19, "the great things"),
        (20, 21, "which had done"),
        (22, 24, "the Lord"),
        (25, 27, "for his father,"),
        (28, 32, "and he also taught"),
        (33, 34, "his people"),
        (35, 36, "concerning"),
        (37, 39, "the great things"),
        (40, 41, "which had done"),
        (42, 44, "the Lord"),
        (45, 48, "for their fathers."),
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
