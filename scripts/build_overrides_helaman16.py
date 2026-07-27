"""
Hand-curated TAM-phrase gloss overrides for Helamana (Helaman) 16 — the close of
the book: believers seek out Nephi to be baptized while unbelievers hurl stones
and arrows at Samuel in vain, protected by the Spirit; Samuel escapes and is seen
no more; Nephi baptizes and works miracles; the people grow ever more contentious
and hardened, dismissing the prophecies as foolish tradition; and despite signs
and wonders they harden their hearts, Satan stirring them up, so that by the
ninetieth year the whole face of the land is in wickedness.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_helaman16.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "helaman"
CHAPTER_NUM = 16

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 5, "it came to pass that"),
        (6, 9, "there were many"),
        (10, 13, "who heard"),
        (14, 17, "the words of Samuel,"),
        (18, 20, "the Lamanite,"),
        (21, 26, "which he spake"),
        (27, 30, "upon the walls of"),
        (31, 33, "the city."),
        (34, 40, "And as many of them"),
        (41, 44, "as believed"),
        (45, 47, "on his word"),
        (48, 50, "went forth"),
        (51, 54, "and sought for Nephi;"),
        (55, 60, "and when they went forth"),
        (61, 65, "and found him"),
        (66, 69, "they confessed"),
        (70, 72, "unto him"),
        (73, 75, "their sins"),
        (76, 79, "and denied not,"),
        (80, 81, "desiring"),
        (82, 85, "that they be baptized"),
        (86, 88, "unto the Lord."),
    ],
    2: [
        (0, 6, "But as many of them"),
        (7, 10, "as there were"),
        (11, 14, "who believed not"),
        (15, 18, "in the words of Samuel"),
        (19, 20, "were angry"),
        (21, 23, "with him;"),
        (24, 29, "and they cast stones"),
        (30, 32, "at him"),
        (33, 37, "upon the wall,"),
        (38, 41, "and also many"),
        (42, 45, "shot arrows"),
        (46, 48, "at him"),
        (49, 53, "as he stood"),
        (54, 58, "upon the wall;"),
        (59, 59, "but"),
        (60, 61, "was together"),
        (62, 66, "the Spirit of the Lord"),
        (67, 68, "with him,"),
        (69, 71, "insomuch that"),
        (72, 77, "he could not be struck"),
        (78, 80, "by their stones"),
        (81, 85, "nor by their arrows."),
    ],
    3: [
        (0, 1, "Now"),
        (2, 5, "when they saw"),
        (6, 12, "he could not be struck"),
        (13, 15, "by them,"),
        (16, 23, "there were many more"),
        (24, 27, "who believed"),
        (28, 30, "on his words,"),
        (31, 33, "insomuch that"),
        (34, 36, "they went"),
        (37, 38, "unto Nephi"),
        (39, 43, "to be baptized."),
    ],
    4: [
        (0, 1, "For behold,"),
        (2, 5, "at this time"),
        (6, 8, "was baptizing"),
        (9, 9, "Nephi,"),
        (10, 12, "and prophesying,"),
        (13, 15, "and preaching,"),
        (16, 20, "crying repentance"),
        (21, 22, "unto the people,"),
        (23, 25, "showing"),
        (26, 29, "signs and wonders,"),
        (30, 32, "working miracles"),
        (33, 36, "among the people,"),
        (37, 41, "that they might know"),
        (42, 46, "must shortly come"),
        (47, 48, "the Christ—"),
    ],
    5: [
        (0, 2, "And telling"),
        (3, 6, "them"),
        (7, 7, "the things"),
        (8, 12, "which shortly come,"),
        (13, 16, "that they might know"),
        (17, 18, "and remember"),
        (19, 22, "at the time of"),
        (23, 26, "their coming,"),
        (27, 29, "were made known"),
        (30, 33, "unto them"),
        (34, 37, "before they came,"),
        (38, 40, "to the intent"),
        (41, 44, "that they might believe;"),
        (45, 46, "therefore"),
        (47, 50, "went forth"),
        (51, 53, "unto him"),
        (54, 58, "as many of them"),
        (59, 62, "as believed"),
        (63, 66, "on the words of Samuel,"),
        (67, 69, "to be baptized,"),
        (70, 70, "for"),
        (71, 74, "they came"),
        (75, 77, "repenting"),
        (78, 80, "and confessing"),
        (81, 84, "their sins."),
    ],
    6: [
        (0, 8, "But the more part of them"),
        (9, 11, "believed not"),
        (12, 15, "in the words of Samuel;"),
        (16, 17, "therefore"),
        (18, 22, "when they saw"),
        (23, 29, "he could not be struck"),
        (30, 32, "by their stones"),
        (33, 36, "and their arrows,"),
        (37, 40, "they cried out"),
        (41, 44, "unto their captains,"),
        (45, 47, "saying:"),
        (48, 51, "Take this man"),
        (52, 55, "and bind him,"),
        (56, 57, "for behold"),
        (58, 63, "he hath a devil;"),
        (64, 66, "and because of"),
        (67, 72, "the power of the devil"),
        (73, 76, "which is in him"),
        (77, 84, "he cannot be struck"),
        (85, 87, "by our stones"),
        (88, 91, "and our arrows;"),
        (92, 93, "therefore"),
        (94, 97, "take him"),
        (98, 101, "and bind him,"),
        (102, 106, "and take him away."),
    ],
    7: [
        (0, 5, "And as they went forth"),
        (6, 8, "to lay"),
        (9, 11, "their hands"),
        (12, 14, "on him,"),
        (15, 15, "behold,"),
        (16, 22, "he cast himself down"),
        (23, 25, "from the wall,"),
        (26, 30, "and fled away"),
        (31, 34, "out of their lands,"),
        (35, 35, "yea,"),
        (36, 39, "even unto his own country,"),
        (40, 42, "and began to"),
        (43, 46, "preach and prophesy"),
        (47, 52, "among his own people."),
    ],
    8: [
        (0, 1, "And behold,"),
        (2, 8, "he was heard of no more"),
        (9, 14, "among the Nephite people;"),
        (15, 17, "and thus were"),
        (18, 21, "the affairs that were"),
        (22, 24, "among the people."),
    ],
    9: [
        (0, 4, "And thus ended"),
        (5, 8, "the year"),
        (9, 12, "eighty and sixth"),
        (13, 16, "of the reign of"),
        (17, 17, "the judges"),
        (18, 23, "over the people of"),
        (24, 24, "Nephi."),
    ],
    10: [
        (0, 5, "And thus ended also"),
        (6, 9, "the year"),
        (10, 13, "eighty and seventh"),
        (14, 18, "of the reign of the judges,"),
        (19, 24, "the greater part of the people"),
        (25, 27, "still remaining"),
        (28, 31, "in their pride"),
        (32, 34, "and wickedness,"),
        (35, 39, "and the lesser part"),
        (40, 41, "walking"),
        (42, 44, "circumspectly"),
        (45, 49, "before God."),
    ],
    11: [
        (0, 4, "And these were the circumstances also,"),
        (5, 8, "in the year"),
        (9, 12, "eighty and eighth"),
        (13, 16, "of the reign of"),
        (17, 17, "the judges."),
    ],
    12: [
        (0, 5, "And there was but little change"),
        (6, 8, "which was"),
        (9, 13, "in the affairs of the people,"),
        (14, 15, "except"),
        (16, 20, "the beginning to be more hardened"),
        (21, 22, "of the people"),
        (23, 25, "in iniquity,"),
        (26, 31, "and doing more and more"),
        (32, 33, "the things"),
        (34, 37, "which were contrary to"),
        (38, 39, "the commandments of"),
        (40, 41, "God,"),
        (42, 45, "in the year"),
        (46, 49, "eighty and ninth"),
        (50, 53, "of the reign of"),
        (54, 54, "the judges."),
    ],
    13: [
        (0, 2, "But it came to pass"),
        (3, 7, "in the ninetieth year"),
        (8, 11, "of the reign of"),
        (12, 12, "the judges,"),
        (13, 15, "there were"),
        (16, 17, "great signs"),
        (18, 20, "and wonders"),
        (21, 23, "which were given"),
        (24, 25, "unto the people;"),
        (26, 30, "and began to be fulfilled"),
        (31, 32, "the words of"),
        (33, 33, "the prophets."),
    ],
    14: [
        (0, 3, "And appeared"),
        (4, 4, "angels"),
        (5, 6, "unto men,"),
        (7, 9, "wise men,"),
        (10, 13, "and declared"),
        (14, 17, "unto them"),
        (18, 20, "glad tidings of"),
        (21, 23, "great joy;"),
        (24, 29, "thus began"),
        (30, 33, "in this year"),
        (34, 36, "the fulfilling of"),
        (37, 38, "the holy scriptures."),
    ],
    15: [
        (0, 3, "Nevertheless,"),
        (4, 7, "began to harden"),
        (8, 9, "the people"),
        (10, 12, "their hearts,"),
        (13, 15, "all of them"),
        (16, 17, "except"),
        (18, 26, "the most believing part of them,"),
        (27, 29, "both the Nephites"),
        (30, 33, "and also the Lamanites,"),
        (34, 36, "and began to"),
        (37, 38, "they depend"),
        (39, 43, "upon their own strength"),
        (44, 48, "and upon their own wisdom,"),
        (49, 50, "saying:"),
    ],
    16: [
        (0, 6, "Perhaps there are some things"),
        (7, 10, "they guessed rightly,"),
        (11, 13, "from among"),
        (14, 16, "many things;"),
        (17, 18, "but behold,"),
        (19, 21, "we know"),
        (22, 26, "cannot be fulfilled"),
        (27, 31, "all these great works"),
        (32, 33, "and marvelous,"),
        (34, 36, "which have been spoken."),
    ],
    17: [
        (0, 3, "And began to"),
        (4, 5, "they reason"),
        (6, 7, "and contend"),
        (8, 14, "among themselves,"),
        (15, 16, "saying:"),
    ],
    18: [
        (0, 4, "It is not a thing"),
        (5, 6, "that is right"),
        (7, 9, "to the mind"),
        (10, 13, "the coming of"),
        (14, 17, "such a being"),
        (18, 20, "as a Christ;"),
        (21, 24, "if he exists,"),
        (25, 31, "and he be the Son of"),
        (32, 33, "God,"),
        (34, 36, "the Father of"),
        (37, 38, "heaven"),
        (39, 41, "and earth,"),
        (42, 46, "as it has been spoken,"),
        (47, 47, "why"),
        (48, 54, "will he not show"),
        (55, 57, "himself"),
        (58, 61, "unto us"),
        (62, 64, "as well also"),
        (65, 68, "unto them"),
        (69, 74, "who shall be"),
        (75, 77, "at Jerusalem?"),
    ],
    19: [
        (0, 0, "Yea,"),
        (1, 1, "why"),
        (2, 9, "will he not show"),
        (10, 12, "himself"),
        (13, 15, "in this land"),
        (16, 18, "as well also"),
        (19, 22, "in the land of"),
        (23, 23, "Jerusalem?"),
    ],
    20: [
        (0, 1, "But behold,"),
        (2, 4, "we know"),
        (5, 9, "this is a wicked tradition,"),
        (10, 14, "which was handed down"),
        (15, 18, "unto us"),
        (19, 22, "by our fathers,"),
        (23, 27, "to draw us"),
        (28, 30, "that we believe"),
        (31, 36, "in some great and marvelous things"),
        (37, 41, "which shall come,"),
        (42, 49, "but not among us,"),
        (50, 53, "but in a land"),
        (54, 57, "which is very far away,"),
        (58, 60, "a land"),
        (61, 64, "which we know not;"),
        (65, 66, "therefore"),
        (67, 75, "they can keep us"),
        (76, 79, "in ignorance,"),
        (80, 80, "for"),
        (81, 86, "we cannot witness"),
        (87, 91, "with our own eyes"),
        (92, 95, "that they are true."),
    ],
    21: [
        (0, 6, "And they will do it,"),
        (7, 9, "by"),
        (10, 11, "the cunning"),
        (12, 15, "and secret arts of"),
        (16, 18, "the evil one,"),
        (19, 21, "some great mystery"),
        (22, 29, "which we cannot understand,"),
        (30, 39, "which will keep us down"),
        (40, 42, "as servants"),
        (43, 45, "to their words,"),
        (46, 49, "and also servants"),
        (50, 53, "unto them,"),
        (54, 54, "for"),
        (55, 57, "we depend"),
        (58, 61, "upon them"),
        (62, 64, "to teach"),
        (65, 68, "us"),
        (69, 70, "his words;"),
        (71, 75, "and thus will"),
        (76, 81, "they keep us"),
        (82, 85, "in ignorance"),
        (86, 91, "if we yield"),
        (92, 94, "ourselves"),
        (95, 98, "unto them,"),
        (99, 102, "all the days of"),
        (103, 105, "our lives."),
    ],
    22: [
        (0, 5, "And many more things"),
        (6, 9, "the people imagined"),
        (10, 13, "in their hearts,"),
        (14, 16, "foolish things"),
        (17, 19, "and vain;"),
        (20, 24, "and they were greatly troubled,"),
        (25, 25, "for"),
        (26, 29, "were stirred up they"),
        (30, 31, "by Satan"),
        (32, 35, "to do iniquity"),
        (36, 38, "continually;"),
        (39, 39, "yea,"),
        (40, 42, "he went about"),
        (43, 44, "and spreading"),
        (45, 47, "rumors and contentions"),
        (48, 53, "upon all the land,"),
        (54, 59, "that he might harden"),
        (60, 62, "the hearts of the people"),
        (63, 67, "against good things"),
        (68, 70, "and against"),
        (71, 76, "things which should come."),
    ],
    23: [
        (0, 3, "And notwithstanding"),
        (4, 7, "the signs and wonders"),
        (8, 10, "which were wrought"),
        (11, 15, "among the people of"),
        (16, 17, "the Lord,"),
        (18, 22, "and the many miracles"),
        (23, 25, "which they did,"),
        (26, 28, "was very strong"),
        (29, 32, "the hold of Satan"),
        (33, 36, "upon the hearts of the people"),
        (37, 42, "upon all the land."),
    ],
    24: [
        (0, 4, "And thus ended"),
        (5, 9, "the ninetieth year"),
        (10, 13, "of the reign of"),
        (14, 14, "the judges"),
        (15, 20, "over the people of"),
        (21, 21, "Nephi."),
    ],
    25: [
        (0, 4, "And thus ended"),
        (5, 8, "the book of"),
        (9, 9, "Helaman,"),
        (10, 12, "according to"),
        (13, 15, "the record of"),
        (16, 16, "Helaman"),
        (17, 19, "and his sons."),
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
