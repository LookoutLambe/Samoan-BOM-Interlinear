"""
Hand-curated TAM-phrase gloss overrides for 1 Nifae (Nephi) 3.

Same mechanism as build_overrides_1nephi1.py and 1nephi2.py. Per-verse spec
of (start, end, english) tuples, validated against the live bom_books.json
word count before writing.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overrides the auto-glossed entries.

    python3 build_overrides_1nephi3.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 3

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass"),
        (4, 5, "I,"),
        (6, 7, "Nephi,"),
        (8, 11, "returned"),
        (12, 15, "from speaking with the Lord,"),
        (16, 18, "in the tent"),
        (19, 21, "of my father."),
    ],
    2: [
        (0, 3, "And it came to pass"),
        (4, 7, "he spake"),
        (8, 10, "unto me,"),
        (11, 12, "saying:"),
        (13, 13, "Behold,"),
        (14, 18, "I have dreamed a dream,"),
        (19, 22, "in which I am commanded"),
        (23, 25, "by the Lord,"),
        (26, 29, "that thou shalt return"),
        (30, 32, "with thy brothers"),
        (33, 34, "to Jerusalem."),
    ],
    3: [
        (0, 1, "For behold,"),
        (2, 7, "Laban hath"),
        (8, 8, "the record"),
        (9, 11, "of the Jews"),
        (12, 15, "and the genealogy also"),
        (16, 20, "of my forefathers,"),
        (21, 23, "and are engraven"),
        (24, 26, "upon"),
        (27, 28, "plates of brass."),
    ],
    4: [
        (0, 3, "Wherefore,"),
        (4, 7, "I have been commanded"),
        (8, 10, "by the Lord,"),
        (11, 15, "that thou shouldest"),
        (16, 19, "and thy brothers should"),
        (20, 21, "go down"),
        (22, 26, "to the house of Laban,"),
        (27, 29, "and seek the records,"),
        (30, 33, "and bring them"),
        (34, 36, "down hither"),
        (37, 39, "into the wilderness."),
    ],
    5: [
        (0, 2, "And now,"),
        (3, 3, "behold"),
        (4, 5, "have murmured"),
        (6, 7, "thy brothers,"),
        (8, 9, "saying"),
        (10, 13, "it is a hard thing"),
        (14, 17, "I have required"),
        (18, 19, "of them,"),
        (20, 21, "but behold"),
        (22, 26, "I have not required it"),
        (27, 28, "of them,"),
        (29, 29, "but"),
        (30, 32, "it is a commandment"),
        (33, 35, "from the Lord."),
    ],
    6: [
        (0, 5, "Therefore go thou,"),
        (6, 8, "my son,"),
        (9, 14, "and thou shalt be favored"),
        (15, 17, "by the Lord,"),
        (18, 22, "because thou hast not murmured."),
    ],
    7: [
        (0, 3, "And it came to pass"),
        (4, 6, "I said"),
        (7, 8, "Nephi,"),
        (9, 11, "unto my father:"),
        (12, 16, "I will go"),
        (17, 19, "and do the things"),
        (20, 21, "which hath commanded"),
        (22, 24, "the Lord,"),
        (25, 28, "for I know"),
        (29, 32, "giveth not"),
        (33, 35, "the Lord"),
        (36, 37, "commandments"),
        (38, 42, "unto the children of men,"),
        (43, 43, "save"),
        (44, 47, "he shall prepare"),
        (48, 49, "by him"),
        (50, 54, "a way for them"),
        (55, 58, "that they may"),
        (59, 61, "accomplish"),
        (62, 64, "the thing"),
        (65, 68, "which he hath commanded"),
        (69, 70, "them."),
    ],
    8: [
        (0, 3, "And it came to pass"),
        (4, 6, "when heard"),
        (7, 8, "my father"),
        (9, 11, "these words"),
        (12, 16, "he was exceedingly glad,"),
        (17, 21, "for he knew"),
        (22, 23, "had been blessed"),
        (24, 24, "I"),
        (25, 27, "by the Lord."),
    ],
    9: [
        (0, 2, "And I,"),
        (3, 4, "Nephi,"),
        (5, 7, "with my brothers,"),
        (8, 12, "did take our journey"),
        (13, 15, "in the wilderness"),
        (16, 19, "with our tents,"),
        (20, 23, "to go up"),
        (24, 26, "to the land"),
        (27, 28, "of Jerusalem."),
    ],
    10: [
        (0, 3, "And it came to pass"),
        (4, 7, "when we went up"),
        (8, 12, "to the land of Jerusalem,"),
        (13, 14, "I"),
        (15, 17, "and my brothers,"),
        (18, 20, "did consult"),
        (21, 23, "one"),
        (24, 26, "with another."),
    ],
    11: [
        (0, 3, "And we did cast"),
        (4, 5, "lots—who"),
        (6, 7, "of"),
        (8, 10, "us"),
        (11, 13, "should"),
        (14, 15, "go in"),
        (16, 17, "unto"),
        (18, 22, "the house of Laban."),
        (23, 26, "And it came to pass"),
        (27, 29, "fell the lot"),
        (30, 31, "upon Laman;"),
        (32, 36, "and Laman went in"),
        (37, 38, "unto"),
        (39, 43, "the house of Laban,"),
        (44, 47, "and he talked"),
        (48, 49, "with him"),
        (50, 53, "as he sat"),
        (54, 56, "in his house."),
    ],
    12: [
        (0, 4, "And he desired"),
        (5, 7, "from Laban"),
        (8, 8, "the records"),
        (9, 10, "which were engraven"),
        (11, 13, "upon"),
        (14, 15, "plates of brass,"),
        (16, 18, "wherein were"),
        (19, 20, "the genealogy"),
        (21, 23, "of my father."),
    ],
    13: [
        (0, 1, "And behold,"),
        (2, 4, "it came to pass"),
        (5, 6, "Laban was angry,"),
        (7, 11, "and he thrust him out"),
        (12, 14, "from his presence;"),
        (15, 20, "and he would not"),
        (21, 26, "give unto him"),
        (27, 27, "the records."),
        (28, 31, "Wherefore,"),
        (32, 36, "he said"),
        (37, 39, "unto him:"),
        (40, 40, "Behold"),
        (41, 42, "thou"),
        (43, 45, "art a robber,"),
        (46, 51, "and I will slay"),
        (52, 54, "thee."),
    ],
    14: [
        (0, 0, "But"),
        (1, 4, "Laman fled"),
        (5, 7, "from his presence,"),
        (8, 10, "and told"),
        (11, 14, "unto us"),
        (15, 15, "things"),
        (16, 17, "had done"),
        (18, 19, "Laban."),
        (20, 22, "And began"),
        (23, 25, "we to mourn"),
        (26, 26, "exceedingly,"),
        (27, 30, "and my brothers"),
        (31, 38, "were about to return"),
        (39, 41, "to my father"),
        (42, 44, "in the wilderness."),
    ],
    15: [
        (0, 1, "But behold"),
        (2, 5, "I said"),
        (6, 9, "unto them:"),
        (10, 13, "As liveth"),
        (14, 15, "the Lord,"),
        (16, 19, "and as also"),
        (20, 22, "we live,"),
        (23, 28, "we will not go down"),
        (29, 32, "to our father"),
        (33, 35, "in the wilderness"),
        (36, 38, "until"),
        (39, 41, "we accomplish"),
        (42, 44, "the thing"),
        (45, 47, "which hath commanded"),
        (48, 49, "us"),
        (50, 52, "by the Lord."),
    ],
    16: [
        (0, 3, "Wherefore,"),
        (4, 6, "let us be faithful"),
        (7, 9, "in keeping"),
        (10, 11, "the commandments"),
        (12, 14, "of the Lord;"),
        (15, 16, "therefore"),
        (17, 20, "let us go down"),
        (21, 23, "to the land"),
        (24, 26, "of inheritance"),
        (27, 30, "of our father,"),
        (31, 32, "for behold"),
        (33, 36, "he hath left"),
        (37, 38, "gold"),
        (39, 40, "and silver,"),
        (41, 46, "and all manner of riches."),
        (47, 51, "And all these things"),
        (52, 55, "he hath done"),
        (56, 58, "because of the commandments"),
        (59, 61, "of the Lord."),
    ],
    17: [
        (0, 4, "For he knew"),
        (5, 8, "would be destroyed"),
        (9, 9, "Jerusalem,"),
        (10, 13, "because of the wickedness"),
        (14, 15, "of the people."),
    ],
    18: [
        (0, 1, "For behold,"),
        (2, 4, "they have rejected"),
        (5, 7, "the words of the prophets."),
        (8, 11, "Wherefore,"),
        (12, 14, "if shall tarry"),
        (15, 16, "my father"),
        (17, 19, "in the land"),
        (20, 26, "after he is commanded"),
        (27, 32, "to flee out of the land,"),
        (33, 33, "behold,"),
        (34, 38, "he will perish also."),
        (39, 42, "Wherefore,"),
        (43, 45, "needs must that"),
        (46, 50, "he flee"),
        (51, 53, "out of the land."),
    ],
    19: [
        (0, 1, "And behold,"),
        (2, 8, "the wisdom of God"),
        (9, 11, "needs must that"),
        (12, 16, "we obtain"),
        (17, 17, "the records,"),
        (18, 23, "that we may preserve"),
        (24, 27, "unto our children"),
        (28, 29, "the language"),
        (30, 33, "of our fathers;"),
    ],
    20: [
        (0, 7, "And that we may also preserve"),
        (8, 10, "unto them"),
        (11, 11, "the words"),
        (12, 14, "which were spoken"),
        (15, 19, "by the mouths of all the holy prophets,"),
        (20, 26, "which had been delivered unto them"),
        (27, 29, "by the Spirit"),
        (30, 32, "and power"),
        (33, 35, "of God,"),
        (36, 39, "since the beginning"),
        (40, 42, "of the world,"),
        (43, 46, "even down"),
        (47, 50, "to this present time."),
    ],
    21: [
        (0, 3, "And it came to pass"),
        (4, 6, "according to"),
        (7, 10, "the manner of language"),
        (11, 14, "I did persuade"),
        (15, 16, "my brothers,"),
        (17, 20, "that they should be faithful"),
        (21, 23, "in keeping"),
        (24, 25, "the commandments"),
        (26, 28, "of God."),
    ],
    22: [
        (0, 3, "And it came to pass"),
        (4, 6, "we went down"),
        (7, 9, "to the land"),
        (10, 13, "of our inheritance,"),
        (14, 17, "and we did gather together"),
        (18, 20, "our gold,"),
        (21, 24, "and our silver,"),
        (25, 29, "and our precious things."),
    ],
    23: [
        (0, 4, "And after"),
        (5, 7, "we had gathered together"),
        (8, 10, "these things,"),
        (11, 15, "we went again"),
        (16, 17, "up"),
        (18, 22, "to the house of Laban."),
    ],
    24: [
        (0, 3, "And it came to pass"),
        (4, 6, "we went in"),
        (7, 8, "unto"),
        (9, 10, "Laban,"),
        (11, 12, "and desired"),
        (13, 15, "of him"),
        (16, 20, "that he would give"),
        (21, 24, "unto us"),
        (25, 25, "the records"),
        (26, 27, "which were engraven"),
        (28, 30, "upon"),
        (31, 32, "plates of brass,"),
        (33, 35, "and we offered"),
        (36, 38, "unto him"),
        (39, 41, "our gold,"),
        (42, 45, "and our silver,"),
        (46, 51, "and all our precious things."),
    ],
    25: [
        (0, 3, "And it came to pass"),
        (4, 7, "when Laban saw"),
        (8, 10, "our property,"),
        (11, 14, "and that it was exceedingly great,"),
        (15, 20, "he did lust after it,"),
        (21, 23, "it came to pass"),
        (24, 30, "that he did thrust us out,"),
        (31, 35, "and sent his servants"),
        (36, 39, "to slay us,"),
        (40, 45, "that he might obtain"),
        (46, 49, "our property."),
    ],
    26: [
        (0, 3, "And it came to pass"),
        (4, 7, "we did flee"),
        (8, 9, "from before"),
        (10, 12, "the servants of Laban,"),
        (13, 17, "and we were obliged"),
        (18, 22, "to leave behind our property,"),
        (23, 26, "and fell"),
        (27, 30, "into the hands of Laban."),
    ],
    27: [
        (0, 3, "And it came to pass"),
        (4, 5, "we fled"),
        (6, 8, "into the wilderness,"),
        (9, 15, "and we were not found"),
        (16, 19, "by the servants of Laban,"),
        (20, 23, "and we did hide"),
        (24, 26, "in the cavity"),
        (27, 29, "of a rock."),
    ],
    28: [
        (0, 3, "And it came to pass"),
        (4, 5, "Laman was angry"),
        (6, 8, "with me,"),
        (9, 14, "and also with my father;"),
        (15, 19, "and so was Lemuel,"),
        (20, 24, "for he hearkened"),
        (25, 28, "unto the words of Laman."),
        (29, 32, "Wherefore"),
        (33, 36, "did speak"),
        (37, 40, "Laman and Lemuel"),
        (41, 44, "many hard words"),
        (45, 48, "unto us,"),
        (49, 52, "their younger brothers,"),
        (53, 56, "and they smote"),
        (57, 58, "even also"),
        (59, 60, "us"),
        (61, 63, "with a rod."),
    ],
    29: [
        (0, 3, "And it came to pass"),
        (4, 7, "as they were smiting"),
        (8, 9, "us"),
        (10, 12, "with a rod,"),
        (13, 13, "behold,"),
        (14, 16, "came"),
        (17, 21, "an angel of the Lord"),
        (22, 23, "and stood"),
        (24, 27, "before them,"),
        (28, 33, "and he spake"),
        (34, 37, "unto them,"),
        (38, 39, "saying:"),
        (40, 40, "Why"),
        (41, 44, "do ye smite"),
        (45, 48, "your younger brother"),
        (49, 51, "with a rod?"),
        (52, 56, "Know ye not that"),
        (57, 60, "he hath been chosen"),
        (61, 63, "by the Lord"),
        (64, 67, "to be a ruler"),
        (68, 70, "over you,"),
        (71, 73, "and this"),
        (74, 78, "because of your iniquities?"),
        (79, 79, "Behold"),
        (80, 84, "ye shall go up again"),
        (85, 86, "to Jerusalem,"),
        (87, 92, "and shall deliver"),
        (93, 93, "Laban"),
        (94, 96, "by the Lord"),
        (97, 100, "into your hands."),
    ],
    30: [
        (0, 4, "And after"),
        (5, 9, "had spoken the angel"),
        (10, 13, "unto us,"),
        (14, 19, "he departed."),
    ],
    31: [
        (0, 4, "And after"),
        (5, 7, "had departed"),
        (8, 10, "the angel,"),
        (11, 15, "began again to murmur"),
        (16, 19, "Laman and Lemuel,"),
        (20, 21, "saying:"),
        (22, 24, "How can it be"),
        (25, 27, "the Lord"),
        (28, 30, "deliver"),
        (31, 31, "Laban"),
        (32, 35, "into our hands?"),
        (36, 36, "Behold,"),
        (37, 42, "he is a mighty man,"),
        (43, 47, "and he can"),
        (48, 51, "command fifty,"),
        (52, 52, "yea,"),
        (53, 56, "he can"),
        (57, 60, "slay fifty;"),
        (61, 66, "why then can not"),
        (67, 68, "we?"),
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
