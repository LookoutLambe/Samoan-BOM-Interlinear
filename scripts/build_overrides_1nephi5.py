"""
Hand-curated TAM-phrase gloss overrides for 1 Nifae (Nephi) 5.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

    python3 build_overrides_1nephi5.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 5

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass"),
        (4, 7, "when we went down"),
        (8, 10, "into the wilderness"),
        (11, 14, "unto our father,"),
        (15, 15, "behold,"),
        (16, 19, "he was filled"),
        (20, 22, "with joy,"),
        (23, 27, "and also my mother,"),
        (28, 29, "Sariah,"),
        (30, 32, "was exceedingly glad,"),
        (33, 34, "for"),
        (35, 39, "she had truly mourned"),
        (40, 43, "because of us."),
    ],
    2: [
        (0, 3, "For she had thought"),
        (4, 5, "had perished"),
        (6, 7, "we"),
        (8, 10, "in the wilderness;"),
        (11, 16, "and she also murmured"),
        (17, 18, "against"),
        (19, 21, "my father,"),
        (22, 24, "having said"),
        (25, 27, "unto him"),
        (28, 29, "he was"),
        (30, 34, "a visionary man;"),
        (35, 36, "saying:"),
        (37, 37, "Behold"),
        (38, 40, "thou hast led away"),
        (41, 42, "us"),
        (43, 45, "from the land"),
        (46, 49, "of our inheritance,"),
        (50, 55, "and have no more"),
        (56, 58, "my sons,"),
        (59, 64, "and we are about to perish"),
        (65, 67, "in the wilderness."),
    ],
    3: [
        (0, 2, "And after this manner"),
        (3, 6, "was the language"),
        (7, 9, "did murmur"),
        (10, 11, "my mother"),
        (12, 14, "against my father."),
    ],
    4: [
        (0, 3, "And it came to pass"),
        (4, 5, "said"),
        (6, 7, "my father"),
        (8, 10, "unto her,"),
        (11, 12, "saying:"),
        (13, 15, "I know"),
        (16, 17, "I am"),
        (18, 22, "a visionary man;"),
        (23, 23, "for"),
        (24, 28, "if I had not seen"),
        (29, 33, "the things of God"),
        (34, 37, "in a vision"),
        (38, 42, "I would not have known"),
        (43, 44, "the goodness"),
        (45, 47, "of God,"),
        (48, 52, "but had tarried"),
        (53, 54, "at Jerusalem,"),
        (55, 57, "and perished"),
        (58, 61, "with my brothers."),
    ],
    5: [
        (0, 1, "But behold,"),
        (2, 4, "I have obtained"),
        (5, 9, "a land of promise,"),
        (10, 16, "in the which I do rejoice;"),
        (17, 17, "yea,"),
        (18, 21, "and I know"),
        (22, 25, "shall deliver"),
        (26, 28, "the Lord"),
        (29, 30, "my sons"),
        (31, 34, "out of the hands of Laban,"),
        (35, 37, "and bring back"),
        (38, 39, "them"),
        (40, 43, "unto us"),
        (44, 46, "in the wilderness."),
    ],
    6: [
        (0, 2, "And after this manner"),
        (3, 6, "was the language"),
        (7, 10, "did comfort"),
        (11, 12, "my father,"),
        (13, 14, "Lehi,"),
        (15, 17, "my mother,"),
        (18, 19, "Sariah,"),
        (20, 24, "concerning us,"),
        (25, 27, "while we journeyed"),
        (28, 30, "in the wilderness"),
        (31, 33, "up"),
        (34, 36, "to the land"),
        (37, 38, "of Jerusalem,"),
        (39, 41, "to obtain"),
        (42, 44, "the record"),
        (45, 47, "of the Jews."),
    ],
    7: [
        (0, 5, "And when we had returned"),
        (6, 8, "to the tent"),
        (9, 11, "of my father,"),
        (12, 12, "behold,"),
        (13, 17, "was complete their joy,"),
        (18, 20, "and was comforted"),
        (21, 22, "my mother."),
    ],
    8: [
        (0, 5, "And she said,"),
        (6, 7, "saying:"),
        (8, 11, "I know now"),
        (12, 14, "of a surety"),
        (15, 16, "hath commanded"),
        (17, 19, "the Lord"),
        (20, 21, "my husband"),
        (22, 23, "to flee"),
        (24, 26, "into the wilderness;"),
        (27, 27, "yea,"),
        (28, 32, "and also I know"),
        (33, 35, "of a surety"),
        (36, 37, "hath protected"),
        (38, 40, "the Lord"),
        (41, 43, "my sons,"),
        (44, 45, "and delivered"),
        (46, 47, "them"),
        (48, 51, "out of the hands of Laban,"),
        (52, 54, "and given"),
        (55, 58, "unto them"),
        (59, 60, "power"),
        (61, 63, "whereby could"),
        (64, 66, "they accomplish"),
        (67, 69, "the thing"),
        (70, 72, "which had commanded"),
        (73, 74, "them"),
        (75, 77, "by the Lord."),
        (78, 80, "And after this manner"),
        (81, 84, "was the language"),
        (85, 89, "she did speak."),
    ],
    9: [
        (0, 3, "And it came to pass"),
        (4, 6, "did rejoice exceedingly"),
        (7, 8, "they,"),
        (9, 11, "and offered"),
        (12, 12, "sacrifice"),
        (13, 15, "and burnt offerings"),
        (16, 18, "unto the Lord;"),
        (19, 22, "and they gave"),
        (23, 24, "thanks"),
        (25, 27, "unto the God"),
        (28, 29, "of Israel."),
    ],
    10: [
        (0, 4, "And after"),
        (5, 7, "they had given"),
        (8, 10, "thanks"),
        (11, 13, "unto the God"),
        (14, 15, "of Israel,"),
        (16, 17, "took"),
        (18, 22, "my father, Lehi,"),
        (23, 23, "the records"),
        (24, 25, "which were engraven"),
        (26, 28, "upon"),
        (29, 30, "plates of brass,"),
        (31, 36, "and did search them"),
        (37, 40, "from the beginning."),
    ],
    11: [
        (0, 4, "And he beheld,"),
        (5, 7, "they contained"),
        (8, 12, "the five books of Moses,"),
        (13, 16, "which gave"),
        (17, 18, "an account"),
        (19, 21, "of the creation"),
        (22, 24, "of the world,"),
        (25, 27, "and also of"),
        (28, 28, "Adam"),
        (29, 30, "and Eve,"),
        (31, 33, "who were"),
        (34, 37, "our first parents;"),
    ],
    12: [
        (0, 3, "And also a record"),
        (4, 6, "of the Jews"),
        (7, 9, "from the beginning,"),
        (10, 13, "even down to"),
        (14, 16, "the commencement"),
        (17, 19, "of the reign"),
        (20, 21, "of Zedekiah,"),
        (22, 23, "king"),
        (24, 25, "of Judah;"),
    ],
    13: [
        (0, 2, "And also the prophecies"),
        (3, 5, "of the holy prophets,"),
        (6, 8, "from the beginning,"),
        (9, 11, "even down to"),
        (12, 14, "the commencement"),
        (15, 17, "of the reign"),
        (18, 19, "of Zedekiah;"),
        (20, 25, "and also many prophecies"),
        (26, 29, "which had been spoken"),
        (30, 31, "by the mouth"),
        (32, 33, "of Jeremiah."),
    ],
    14: [
        (0, 3, "And it came to pass"),
        (4, 6, "did find also"),
        (7, 10, "my father, Lehi,"),
        (11, 13, "upon"),
        (14, 15, "the plates of brass"),
        (16, 20, "a genealogy of his fathers;"),
        (21, 24, "wherefore"),
        (25, 28, "he knew"),
        (29, 30, "he was"),
        (31, 36, "a descendant of"),
        (37, 37, "Joseph;"),
        (38, 38, "yea,"),
        (39, 42, "even that Joseph"),
        (43, 45, "the son of"),
        (46, 46, "Jacob,"),
        (47, 53, "who was sold into Egypt,"),
        (54, 58, "and who was preserved"),
        (59, 64, "by the hand of the Lord,"),
        (65, 69, "that he might preserve"),
        (70, 71, "by him"),
        (72, 73, "his father,"),
        (74, 75, "Jacob,"),
        (76, 79, "and all his household"),
        (80, 82, "from perishing"),
        (83, 85, "in famine."),
    ],
    15: [
        (0, 3, "And were led also"),
        (4, 5, "they"),
        (6, 8, "out of captivity,"),
        (9, 14, "and out of the land of Egypt,"),
        (15, 18, "by that same God"),
        (19, 22, "who had preserved"),
        (23, 24, "them."),
    ],
    16: [
        (0, 5, "And thus did know"),
        (6, 10, "my father, Lehi,"),
        (11, 12, "the genealogy"),
        (13, 15, "of his fathers."),
        (16, 19, "And Laban also"),
        (20, 25, "was a descendant of"),
        (26, 26, "Joseph,"),
        (27, 30, "wherefore"),
        (31, 35, "he had kept"),
        (36, 39, "his fathers' records."),
    ],
    17: [
        (0, 2, "And now"),
        (3, 5, "when saw"),
        (6, 7, "my father"),
        (8, 11, "all these things,"),
        (12, 15, "he was filled"),
        (16, 18, "with the Spirit,"),
        (19, 22, "and began to prophesy"),
        (23, 25, "concerning"),
        (26, 27, "his seed—"),
    ],
    18: [
        (0, 1, "That"),
        (2, 5, "these plates of brass"),
        (6, 10, "should go"),
        (11, 13, "unto all nations,"),
        (14, 14, "kindreds,"),
        (15, 15, "tongues,"),
        (16, 17, "and people,"),
        (18, 21, "who were"),
        (22, 25, "of his seed."),
    ],
    19: [
        (0, 3, "Wherefore,"),
        (4, 9, "he said"),
        (10, 13, "these plates of brass"),
        (14, 19, "should never perish;"),
        (20, 23, "neither should they be"),
        (24, 26, "dimmed by time."),
        (27, 30, "And many things"),
        (31, 34, "did prophesy"),
        (35, 36, "concerning"),
        (37, 39, "his seed."),
    ],
    20: [
        (0, 3, "And it came to pass"),
        (4, 10, "up to this very time"),
        (11, 13, "we had kept"),
        (14, 18, "I and my father"),
        (19, 19, "the commandments"),
        (20, 22, "wherewith had commanded"),
        (23, 24, "us"),
        (25, 27, "the Lord."),
    ],
    21: [
        (0, 3, "And we had obtained"),
        (4, 4, "the records"),
        (5, 7, "had commanded"),
        (8, 9, "us"),
        (10, 12, "the Lord,"),
        (13, 17, "and we did search them"),
        (18, 21, "and we knew"),
        (22, 25, "they were desirable;"),
        (26, 26, "yea,"),
        (27, 30, "of great worth"),
        (31, 34, "unto us,"),
        (35, 41, "that we could preserve"),
        (42, 46, "the commandments of the Lord"),
        (47, 50, "unto our children."),
    ],
    22: [
        (0, 3, "Wherefore,"),
        (4, 6, "the wisdom"),
        (7, 10, "of the Lord"),
        (11, 16, "needs that we should carry"),
        (17, 19, "these plates"),
        (20, 23, "with us,"),
        (24, 27, "as we journeyed"),
        (28, 30, "in the wilderness"),
        (31, 31, "toward"),
        (32, 34, "to the land"),
        (35, 37, "of promise."),
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
