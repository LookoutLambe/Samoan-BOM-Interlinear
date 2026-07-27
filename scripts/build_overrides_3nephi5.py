"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 5 — after the great
deliverance the Nephites, none doubting the prophets, forsake their sins and serve
God; the robber prisoners who covenant to murder no more are freed while the rest
are condemned by law; Mormon breaks into first person, testifying that he is a
disciple of Jesus Christ, called to declare his word, abridging the record of his
people; the people again prosper in the land, and Mormon recounts how the seed of
Jacob, scattered and smitten, shall yet be gathered and brought to the knowledge
of the Lord their Redeemer.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi5.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 5

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And now behold,"),
        (4, 10, "there was not one living soul"),
        (11, 18, "among all the people of the Nephites"),
        (19, 20, "who doubted"),
        (21, 24, "in the least"),
        (25, 27, "the words of"),
        (28, 30, "all the holy prophets"),
        (31, 35, "who had spoken;"),
        (36, 39, "for they knew"),
        (40, 44, "they must surely be fulfilled"),
        (45, 46, "in them."),
    ],
    2: [
        (0, 3, "And they knew"),
        (4, 7, "that it must surely be"),
        (8, 13, "that Christ had come,"),
        (14, 15, "because of"),
        (16, 18, "the many signs"),
        (19, 23, "which had been given,"),
        (24, 26, "according to"),
        (27, 29, "the words of the prophets;"),
        (30, 32, "and because of"),
        (33, 34, "the things which"),
        (35, 38, "had already been fulfilled"),
        (39, 41, "they knew"),
        (42, 46, "that must surely be fulfilled"),
        (47, 50, "all things"),
        (51, 53, "according to"),
        (54, 56, "that which was spoken."),
    ],
    3: [
        (0, 1, "Therefore"),
        (2, 5, "they forsook"),
        (6, 9, "all their sins,"),
        (10, 14, "and their abominations,"),
        (15, 18, "and their whoredoms,"),
        (19, 22, "and they served"),
        (23, 25, "God"),
        (26, 29, "with all diligence"),
        (30, 35, "day and night."),
    ],
    4: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 11, "when they had taken captive"),
        (12, 16, "all the robbers,"),
        (17, 19, "insomuch that"),
        (20, 26, "none escaped"),
        (27, 29, "who were not slain,"),
        (30, 32, "they cast"),
        (33, 35, "their prisoners"),
        (36, 40, "into the prison,"),
        (41, 42, "and commanded"),
        (43, 45, "that be preached"),
        (46, 50, "the word of God"),
        (51, 54, "unto them;"),
        (55, 61, "and as many of them"),
        (62, 65, "as would repent"),
        (66, 68, "of their sins"),
        (69, 74, "and enter into a covenant"),
        (75, 82, "that they would murder no more"),
        (83, 84, "were set at liberty."),
    ],
    5: [
        (0, 6, "But as many of them"),
        (7, 11, "as there were"),
        (12, 15, "who did not enter"),
        (16, 18, "into a covenant,"),
        (19, 25, "and who still had"),
        (26, 29, "in their hearts"),
        (30, 33, "the secret murder,"),
        (34, 34, "yea,"),
        (35, 40, "as many of them"),
        (41, 44, "as were found"),
        (45, 47, "breathing out"),
        (48, 49, "threatening words"),
        (50, 52, "against"),
        (53, 55, "their brethren"),
        (56, 57, "were condemned"),
        (58, 59, "and punished"),
        (60, 62, "according to"),
        (63, 64, "the law."),
    ],
    6: [
        (0, 5, "And thus they did"),
        (6, 7, "to stop"),
        (8, 11, "all those combinations"),
        (12, 12, "wicked,"),
        (13, 14, "and secret,"),
        (15, 16, "and abominable,"),
        (17, 21, "from which arose"),
        (22, 27, "the doing of great wickedness,"),
        (28, 31, "and so much of"),
        (32, 34, "murder."),
    ],
    7: [
        (0, 5, "And thus passed away"),
        (6, 9, "the year"),
        (10, 13, "twenty-second,"),
        (14, 18, "and the year also"),
        (19, 22, "twenty-third,"),
        (23, 28, "and the twenty-fourth,"),
        (29, 34, "and the twenty-fifth;"),
        (35, 40, "and thus passed away"),
        (41, 46, "twenty-five"),
        (47, 48, "years."),
    ],
    8: [
        (0, 3, "And many things"),
        (4, 5, "happened,"),
        (6, 10, "which were great and marvelous,"),
        (11, 16, "in the sight of some;"),
        (17, 20, "nevertheless,"),
        (21, 25, "cannot be written"),
        (26, 28, "all those things"),
        (29, 31, "in this book;"),
        (32, 32, "yea,"),
        (33, 37, "cannot be held"),
        (38, 40, "in this book"),
        (41, 44, "even"),
        (45, 47, "a hundredth part of"),
        (48, 51, "the things done"),
        (52, 56, "among people"),
        (57, 60, "so exceedingly numerous"),
        (61, 65, "in the space of years"),
        (66, 70, "twenty-five;"),
    ],
    9: [
        (0, 1, "But behold"),
        (2, 6, "there are records"),
        (7, 11, "which contain"),
        (12, 16, "all the proceedings of this people;"),
        (17, 21, "and a short account"),
        (22, 24, "but true"),
        (25, 29, "was given by Nephi."),
    ],
    10: [
        (0, 1, "Therefore"),
        (2, 5, "I have made"),
        (6, 7, "my record"),
        (8, 10, "of these things"),
        (11, 14, "according to"),
        (15, 18, "the record of Nephi,"),
        (19, 21, "which was engraven"),
        (22, 25, "on the plates"),
        (26, 28, "which were called"),
        (29, 32, "the plates of Nephi."),
    ],
    11: [
        (0, 1, "And behold,"),
        (2, 4, "I make"),
        (5, 6, "the record"),
        (7, 10, "on plates"),
        (11, 14, "which I made"),
        (15, 18, "with mine own hands."),
    ],
    12: [
        (0, 1, "And behold,"),
        (2, 6, "I am called Mormon,"),
        (7, 8, "named"),
        (9, 12, "after the name of"),
        (13, 16, "the land of Mormon,"),
        (17, 19, "the land which"),
        (20, 24, "Alma established"),
        (25, 26, "the church"),
        (27, 31, "among the people,"),
        (32, 32, "yea,"),
        (33, 36, "the first church which"),
        (37, 38, "was established"),
        (39, 44, "among them"),
        (45, 47, "after there passed"),
        (48, 50, "their transgression."),
    ],
    13: [
        (0, 0, "Behold,"),
        (1, 8, "I am a disciple of Jesus Christ,"),
        (9, 13, "the Son of God."),
        (14, 17, "He hath called me"),
        (18, 20, "to declare"),
        (21, 22, "his word"),
        (23, 27, "among his people,"),
        (28, 33, "that they might obtain"),
        (34, 38, "the everlasting life."),
    ],
    14: [
        (0, 4, "And it became needful"),
        (5, 7, "for me,"),
        (8, 10, "according to"),
        (11, 15, "the will of God,"),
        (16, 18, "that I make"),
        (19, 20, "a record"),
        (21, 25, "of these things done,"),
        (26, 28, "that be fulfilled"),
        (29, 32, "the prayers of the righteous"),
        (33, 35, "who have passed on,"),
        (36, 40, "those who"),
        (41, 44, "were holy men,"),
        (45, 47, "according to"),
        (48, 50, "their faith—"),
    ],
    15: [
        (0, 0, "Yea,"),
        (1, 4, "a small record"),
        (5, 9, "of the things that happened"),
        (10, 12, "from the time"),
        (13, 17, "when Lehi left"),
        (18, 18, "Jerusalem,"),
        (19, 23, "even down unto"),
        (24, 26, "the present time."),
    ],
    16: [
        (0, 1, "Therefore"),
        (2, 5, "I make"),
        (6, 7, "my record"),
        (8, 10, "from the accounts which"),
        (11, 16, "were given by them"),
        (17, 21, "who came before"),
        (22, 24, "me,"),
        (25, 28, "until"),
        (29, 33, "the beginning of my days;"),
    ],
    17: [
        (0, 5, "And then I make"),
        (6, 8, "a record"),
        (9, 11, "of the things which"),
        (12, 16, "I saw"),
        (17, 20, "with mine own eyes."),
    ],
    18: [
        (0, 3, "And I know"),
        (4, 7, "the record which"),
        (8, 10, "I make"),
        (11, 13, "is a record"),
        (14, 17, "just and true;"),
        (18, 21, "nevertheless"),
        (22, 27, "there are many things,"),
        (28, 34, "which we cannot write,"),
        (35, 37, "according to"),
        (38, 40, "our language."),
    ],
    19: [
        (0, 2, "And now"),
        (3, 6, "I make an end of"),
        (7, 8, "my words,"),
        (9, 14, "these being my own words,"),
        (15, 19, "and proceed to give"),
        (20, 22, "my account"),
        (23, 26, "of the things that happened"),
        (27, 30, "before me."),
    ],
    20: [
        (0, 3, "I am Mormon,"),
        (4, 9, "and one truly descended"),
        (10, 12, "from Lehi."),
        (13, 18, "I have reason"),
        (19, 22, "to bless"),
        (23, 25, "my God,"),
        (26, 28, "and my Savior"),
        (29, 31, "Jesus Christ,"),
        (32, 34, "in his bringing"),
        (35, 38, "our fathers"),
        (39, 43, "from the land of Jerusalem,"),
        (44, 48, "(and there was none"),
        (49, 51, "who knew it"),
        (52, 53, "except"),
        (54, 56, "himself"),
        (57, 60, "and those who"),
        (61, 64, "he brought"),
        (65, 67, "from that land),"),
        (68, 72, "and in his giving"),
        (73, 78, "to me and my people"),
        (79, 82, "so great a knowledge"),
        (83, 86, "for the salvation of"),
        (87, 89, "our souls."),
    ],
    21: [
        (0, 2, "Surely"),
        (3, 5, "he hath blessed"),
        (6, 9, "the house of Jacob,"),
        (10, 13, "and hath had mercy"),
        (14, 17, "unto the seed of Joseph."),
    ],
    22: [
        (0, 6, "And inasmuch as"),
        (7, 13, "the children of Lehi kept"),
        (14, 16, "his commandments"),
        (17, 24, "so hath he blessed them"),
        (25, 28, "and prospered them"),
        (29, 31, "according to"),
        (32, 33, "his word."),
    ],
    23: [
        (0, 0, "Yea,"),
        (1, 4, "and surely"),
        (5, 10, "he shall again bring"),
        (11, 15, "a remnant of"),
        (16, 19, "the seed of Joseph"),
        (20, 23, "to the knowledge of"),
        (24, 28, "the Lord their God."),
    ],
    24: [
        (0, 4, "And as surely as"),
        (5, 7, "liveth"),
        (8, 9, "the Lord,"),
        (10, 14, "will he gather"),
        (15, 20, "from the four quarters of"),
        (21, 22, "the earth"),
        (23, 28, "all the remnant of"),
        (29, 32, "the seed of Jacob,"),
        (33, 37, "who are scattered abroad"),
        (38, 41, "upon all the earth."),
    ],
    25: [
        (0, 5, "And as he covenanted"),
        (6, 11, "with all the house of Jacob,"),
        (12, 18, "even so shall be fulfilled"),
        (19, 22, "the covenant which"),
        (23, 26, "he covenanted"),
        (27, 31, "with the house of Jacob"),
        (32, 38, "in his own due time,"),
        (39, 42, "unto the restoring of"),
        (43, 47, "all the house of Jacob"),
        (48, 51, "unto the knowledge of"),
        (52, 54, "the covenant which"),
        (55, 59, "he covenanted"),
        (60, 63, "together with them."),
    ],
    26: [
        (0, 5, "And then shall they know"),
        (6, 9, "their Redeemer,"),
        (10, 12, "who is Jesus Christ,"),
        (13, 17, "the Son of God;"),
        (18, 25, "and then shall they be gathered"),
        (26, 30, "from the four quarters of"),
        (31, 32, "the earth"),
        (33, 37, "unto their own lands,"),
        (38, 39, "from the places"),
        (40, 44, "where they were scattered;"),
        (45, 45, "yea,"),
        (46, 49, "as liveth"),
        (50, 51, "the Lord,"),
        (52, 58, "so shall it be done."),
        (59, 59, "Amen."),
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
