"""
Hand-curated TAM-phrase gloss overrides for 1 Nifae (Nephi) 1.

Each verse is specified as a list of (start_idx, end_idx, english_gloss) tuples
spanning *every* token in source order without gaps or overlaps. The builder
expands each tuple into a run of `{sm, en:"·"}` continuation entries followed
by the final word carrying the real English gloss. Total word count is asserted
against the live `bom_books.json` source, so a stale spec fails loudly.

To rebuild after editing:
    python3 build_overrides_1nephi1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 1

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


# Each verse: [(start_idx_inclusive, end_idx_inclusive, english_gloss), ...]
# Indices match the tokenization in bom_books.json (printed via the helper script).
# Trailing punctuation on the surface form is preserved in the gloss to keep
# the reader's punctuation flow honest.
VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "I,"),
        (2, 3, "Nephi,"),
        (4, 5, "was born"),
        (6, 8, "of goodly parents,"),
        (9, 10, "therefore"),
        (11, 15, "I was taught"),
        (16, 19, "in all the learning"),
        (20, 22, "of my father;"),
        (23, 27, "and because I have seen"),
        (28, 29, "afflictions"),
        (30, 31, "many,"),
        (32, 34, "in the course"),
        (35, 37, "of my days,"),
        (38, 41, "nevertheless,"),
        (42, 45, "I was highly favored"),
        (46, 48, "by the Lord"),
        (49, 52, "in all my days;"),
        (53, 53, "yea,"),
        (54, 57, "because I have gained"),
        (58, 60, "a great knowledge"),
        (61, 63, "of the goodness"),
        (64, 68, "and mysteries of God,"),
        (69, 70, "therefore"),
        (71, 74, "I make"),
        (75, 76, "a record"),
        (77, 79, "of my proceedings"),
        (80, 82, "in my days."),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 3, "I make"),
        (4, 5, "a record"),
        (6, 8, "in the language"),
        (9, 11, "of my father,"),
        (12, 13, "made"),
        (14, 16, "in the learning"),
        (17, 19, "of the Jews"),
        (20, 22, "and the language"),
        (23, 25, "of the Egyptians."),
    ],
    3: [
        (0, 3, "And I knew"),
        (4, 5, "is true"),
        (6, 7, "the record"),
        (8, 10, "which I have made;"),
        (11, 14, "and I have written it"),
        (15, 18, "with mine own hand;"),
        (19, 22, "and I have made it"),
        (23, 27, "according to my knowledge."),
    ],
    4: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the beginning"),
        (6, 9, "of the first year"),
        (10, 12, "of the reign"),
        (13, 14, "of Zedekiah,"),
        (15, 16, "the king"),
        (17, 18, "of Judah,"),
        (19, 20, "(dwelt"),
        (21, 22, "my father,"),
        (23, 24, "Lehi,"),
        (25, 26, "at Jerusalem"),
        (27, 30, "in all his days);"),
        (31, 31, "and"),
        (32, 35, "in that same year"),
        (36, 39, "came"),
        (40, 42, "many prophets,"),
        (43, 45, "and prophesying"),
        (46, 47, "unto the people"),
        (48, 49, "saying"),
        (50, 54, "they must repent,"),
        (55, 55, "or"),
        (56, 57, "should be destroyed"),
        (58, 60, "the great city"),
        (61, 62, "of Jerusalem."),
    ],
    5: [
        (0, 3, "Wherefore,"),
        (4, 6, "it came to pass"),
        (7, 9, "went"),
        (10, 11, "my father,"),
        (12, 13, "Lehi,"),
        (14, 18, "he prayed"),
        (19, 21, "unto the Lord,"),
        (22, 22, "yea,"),
        (23, 27, "with all his heart,"),
        (28, 30, "for his people."),
    ],
    6: [
        (0, 3, "And it came to pass"),
        (4, 8, "as he was praying"),
        (9, 11, "unto the Lord,"),
        (12, 14, "there came"),
        (15, 17, "a pillar of fire"),
        (18, 20, "and dwelt"),
        (21, 25, "upon a rock"),
        (26, 28, "before him;"),
        (29, 31, "and he saw"),
        (32, 33, "and heard"),
        (34, 35, "by him"),
        (36, 38, "many things;"),
        (39, 40, "and because"),
        (41, 42, "of the things"),
        (43, 45, "which he saw"),
        (46, 47, "and heard,"),
        (48, 49, "did quake"),
        (50, 53, "and tremble exceedingly"),
        (54, 55, "he."),
    ],
    7: [
        (0, 3, "And it came to pass"),
        (4, 8, "he returned"),
        (9, 12, "to his own house"),
        (13, 14, "at Jerusalem;"),
        (15, 18, "and he cast himself"),
        (19, 21, "down"),
        (22, 24, "upon his bed,"),
        (25, 29, "being overcome"),
        (30, 32, "with the Spirit"),
        (33, 37, "and the things which he had seen."),
    ],
    8: [
        (0, 2, "And being thus"),
        (3, 4, "overcome"),
        (5, 6, "he"),
        (7, 9, "with the Spirit,"),
        (10, 11, "was carried away"),
        (12, 13, "he"),
        (14, 17, "in a vision,"),
        (18, 21, "even that saw"),
        (22, 23, "he"),
        (24, 27, "the heavens open,"),
        (28, 30, "and he thought"),
        (31, 32, "he"),
        (33, 34, "saw"),
        (35, 36, "he"),
        (37, 39, "God"),
        (40, 41, "sitting"),
        (42, 44, "upon his throne,"),
        (45, 46, "surrounded"),
        (47, 49, "with hosts of angels"),
        (50, 52, "innumerable"),
        (53, 55, "in the manner of"),
        (56, 57, "singing"),
        (58, 60, "and praising"),
        (61, 64, "their God."),
    ],
    9: [
        (0, 3, "And it came to pass"),
        (4, 7, "he saw"),
        (8, 10, "One"),
        (11, 14, "descending"),
        (15, 19, "out of the midst of heaven,"),
        (20, 24, "and he beheld"),
        (25, 29, "his luster was greater"),
        (30, 33, "than the sun"),
        (34, 36, "at noon-day."),
    ],
    10: [
        (0, 0, "And"),
        (1, 5, "he also saw"),
        (6, 7, "others"),
        (8, 9, "twelve in number"),
        (10, 12, "following"),
        (13, 15, "after him,"),
        (16, 20, "and their brightness"),
        (21, 23, "did exceed"),
        (24, 26, "that of the stars"),
        (27, 29, "of the firmament."),
    ],
    11: [
        (0, 4, "And they came down"),
        (5, 7, "and went"),
        (8, 12, "upon the face of the earth;"),
        (13, 16, "and there came"),
        (17, 19, "the first"),
        (20, 21, "and stood"),
        (22, 26, "before my father,"),
        (27, 29, "and gave"),
        (30, 32, "unto him"),
        (33, 34, "a book,"),
        (35, 37, "and spake"),
        (38, 40, "unto him"),
        (41, 43, "that should"),
        (44, 45, "he read"),
        (46, 47, "it."),
    ],
    12: [
        (0, 3, "And it came to pass"),
        (4, 6, "as he read,"),
        (7, 10, "he was filled"),
        (11, 13, "with the Spirit"),
        (14, 16, "of the Lord."),
    ],
    13: [
        (0, 4, "And he read,"),
        (5, 6, "saying:"),
        (7, 10, "Wo, wo,"),
        (11, 12, "unto Jerusalem,"),
        (13, 16, "for I have seen"),
        (17, 20, "thine abominations!"),
        (21, 22, "Yea, and"),
        (23, 25, "many things"),
        (26, 29, "did read"),
        (30, 31, "my father"),
        (32, 35, "concerning Jerusalem—"),
        (36, 37, "that"),
        (38, 41, "should be destroyed,"),
        (42, 46, "and the inhabitants thereof;"),
        (47, 48, "many"),
        (49, 52, "should perish"),
        (53, 55, "by the sword,"),
        (56, 59, "and many also"),
        (60, 64, "should be carried away captive"),
        (65, 66, "into Babylon."),
    ],
    14: [
        (0, 3, "And it came to pass"),
        (4, 7, "when he had read"),
        (8, 11, "and seen my father"),
        (12, 14, "many"),
        (15, 17, "great things"),
        (18, 20, "and marvelous,"),
        (21, 23, "he did exclaim"),
        (24, 26, "many things"),
        (27, 31, "unto the Lord;"),
        (32, 35, "such as:"),
        (36, 37, "Great are"),
        (38, 39, "and marvelous"),
        (40, 41, "thy works,"),
        (42, 44, "O Lord"),
        (45, 48, "God Almighty!"),
        (49, 53, "Thy throne is high in the heavens,"),
        (54, 55, "thy throne,"),
        (56, 59, "and thy power,"),
        (60, 62, "and goodness,"),
        (63, 66, "and mercy"),
        (67, 71, "are over"),
        (72, 74, "all who"),
        (75, 76, "dwell"),
        (77, 79, "upon the earth;"),
        (80, 81, "and, because"),
        (82, 85, "thou art merciful,"),
        (86, 89, "thou wilt not suffer"),
        (90, 93, "those who"),
        (94, 96, "come"),
        (97, 99, "unto thee"),
        (100, 103, "that they should perish!"),
    ],
    15: [
        (0, 2, "And after this manner"),
        (3, 6, "was the language"),
        (7, 9, "of my father"),
        (10, 12, "in the praising"),
        (13, 15, "of his God;"),
        (16, 16, "for"),
        (17, 18, "did rejoice"),
        (19, 20, "his soul,"),
        (21, 23, "and was filled"),
        (24, 26, "his whole heart,"),
        (27, 31, "because of the things"),
        (32, 33, "he had seen,"),
        (34, 34, "yea,"),
        (35, 37, "had shown"),
        (38, 40, "by the Lord"),
        (41, 43, "unto him."),
    ],
    16: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Nephi,"),
        (7, 10, "do not make"),
        (11, 13, "a full account"),
        (14, 17, "of the things which have been written"),
        (18, 20, "by my father,"),
        (21, 25, "for he hath written"),
        (26, 28, "many things"),
        (29, 32, "which he saw"),
        (33, 36, "in visions and in dreams;"),
        (37, 37, "and"),
        (38, 42, "he hath also written"),
        (43, 45, "many things"),
        (46, 49, "which he prophesied"),
        (50, 53, "and spake"),
        (54, 56, "unto his children,"),
        (57, 59, "shall"),
        (60, 62, "I not make"),
        (63, 64, "thereof"),
        (65, 67, "a full account."),
    ],
    17: [
        (0, 0, "But"),
        (1, 5, "I shall make"),
        (6, 7, "an account"),
        (8, 10, "of my proceedings"),
        (11, 13, "in my days."),
        (14, 14, "Behold,"),
        (15, 17, "I make"),
        (18, 19, "an abridgment"),
        (20, 22, "of the record"),
        (23, 25, "of my father,"),
        (26, 29, "upon plates"),
        (30, 32, "which I have made"),
        (33, 36, "with mine own hands;"),
        (37, 40, "wherefore,"),
        (41, 45, "after I have abridged"),
        (46, 48, "the record"),
        (49, 51, "of my father"),
        (52, 56, "then will I make"),
        (57, 58, "an account"),
        (59, 62, "of mine own life."),
    ],
    18: [
        (0, 1, "Therefore,"),
        (2, 4, "I would"),
        (5, 7, "that ye should know,"),
        (8, 11, "that after"),
        (12, 16, "the Lord had shown"),
        (17, 19, "unto my father,"),
        (20, 21, "Lehi,"),
        (22, 24, "so many"),
        (25, 27, "marvelous things,"),
        (28, 30, "concerning"),
        (31, 35, "the destruction of Jerusalem,"),
        (36, 36, "behold,"),
        (37, 41, "he went forth"),
        (42, 43, "among the people,"),
        (44, 47, "and began to prophesy"),
        (48, 50, "and to declare"),
        (51, 54, "unto them"),
        (55, 57, "concerning"),
        (58, 61, "the things which he saw"),
        (62, 63, "and heard."),
    ],
    19: [
        (0, 3, "And it came to pass"),
        (4, 6, "the Jews did mock"),
        (7, 9, "him"),
        (10, 12, "because of the things"),
        (13, 15, "which he testified"),
        (16, 16, "thereof"),
        (17, 18, "he"),
        (19, 20, "concerning"),
        (21, 24, "them;"),
        (25, 27, "for truly"),
        (28, 30, "did testify"),
        (31, 32, "he"),
        (33, 36, "of their wickedness"),
        (37, 41, "and their abominations;"),
        (42, 42, "and"),
        (43, 47, "he testified"),
        (48, 49, "that the things"),
        (50, 52, "which he saw"),
        (53, 54, "and heard,"),
        (55, 57, "and also the things"),
        (58, 60, "which he read"),
        (61, 63, "in the book,"),
        (64, 68, "manifested plainly"),
        (69, 71, "the coming"),
        (72, 74, "of a Messiah,"),
        (75, 78, "and also the redemption"),
        (79, 81, "of the world."),
    ],
    20: [
        (0, 2, "And when"),
        (3, 5, "the Jews heard"),
        (6, 9, "these things"),
        (10, 14, "they were angry with him;"),
        (15, 15, "yea,"),
        (16, 19, "even as"),
        (20, 22, "they did"),
        (23, 25, "unto the prophets of old,"),
        (26, 30, "whom they had cast out,"),
        (31, 34, "and stoned,"),
        (35, 36, "and slain;"),
        (37, 41, "and they also sought"),
        (42, 43, "his life,"),
        (44, 47, "that they might take it away."),
        (48, 49, "But behold,"),
        (50, 51, "I,"),
        (52, 53, "Nephi,"),
        (54, 59, "I will show forth"),
        (60, 62, "unto you"),
        (63, 65, "that"),
        (66, 70, "the tender mercies"),
        (71, 73, "of the Lord"),
        (74, 76, "are over"),
        (77, 79, "all those"),
        (80, 81, "who"),
        (82, 84, "he hath chosen,"),
        (85, 88, "because of their faith,"),
        (89, 93, "to make mighty"),
        (94, 95, "them"),
        (96, 100, "even unto the power"),
        (101, 104, "of deliverance."),
    ],
}


def build_words(source_words: list[dict], spec: list[tuple[int, int, str]]) -> list[dict]:
    # Verify spec covers every index exactly once, in order.
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
