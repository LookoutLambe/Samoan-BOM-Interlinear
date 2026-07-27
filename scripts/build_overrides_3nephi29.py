"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 29 — Mormon's exhortation:
when the Book of Mormon comes forth among the Gentiles, it is the sign that the Father
has begun to fulfil his covenant to gather and restore Israel; the words of the prophets
shall all be fulfilled, and none may suppose the Lord delays. He pronounces wo upon those
who spurn the doings of the Lord, who deny the Christ, who say the Lord no longer works
by revelation or by the Holy Ghost, and who work iniquity; the Lord's justice and mercy
shall not be turned aside.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15). `o le a` stays atomic and is never fused with a
following `se X` NP. A cell may run to 6 only where a split would break rule 2
(absorbed subject) or rule 7 (`o le a` + verb + directional).

    python3 build_overrides_3nephi29.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 29

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 3, "behold,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 13, "when shall see fit"),
        (14, 16, "the Lord"),
        (17, 19, "that it is meet,"),
        (20, 22, "in his wisdom,"),
        (23, 25, "that shall come"),
        (26, 27, "these sayings"),
        (28, 29, "unto the Gentiles"),
        (30, 34, "according to his word,"),
        (35, 38, "then ye may know"),
        (39, 42, "is beginning to be fulfilled"),
        (43, 46, "the covenant which"),
        (47, 51, "the Father made"),
        (52, 55, "with the children"),
        (56, 57, "of Israel,"),
        (58, 60, "concerning"),
        (61, 63, "their restoration"),
        (64, 65, "to the lands"),
        (66, 69, "of their inheritance."),
    ],
    2: [
        (0, 3, "And ye may know"),
        (4, 5, "the words"),
        (6, 8, "of the Lord,"),
        (9, 13, "which were spoken"),
        (14, 15, "the holy prophets,"),
        (16, 19, "shall be fulfilled"),
        (20, 21, "all;"),
        (22, 25, "and ye need not"),
        (26, 29, "say"),
        (30, 34, "that the Lord delays"),
        (35, 37, "his coming"),
        (38, 42, "unto the children of Israel."),
    ],
    3: [
        (0, 3, "And ye need not"),
        (4, 7, "imagine"),
        (8, 11, "in your hearts"),
        (12, 12, "that"),
        (13, 15, "are vain"),
        (16, 17, "the words"),
        (18, 20, "which were spoken,"),
        (21, 22, "for behold,"),
        (23, 26, "will remember"),
        (27, 29, "the Lord"),
        (30, 32, "his covenant which"),
        (33, 35, "he hath made"),
        (36, 38, "unto his people"),
        (39, 41, "of the house"),
        (42, 43, "of Israel."),
    ],
    4: [
        (0, 4, "And when ye shall see"),
        (5, 8, "the coming"),
        (9, 11, "of these sayings"),
        (12, 13, "among"),
        (14, 16, "you,"),
        (17, 21, "then it is no longer meet"),
        (22, 24, "that ye spurn"),
        (25, 26, "at the doings"),
        (27, 30, "which are done"),
        (31, 32, "of the Lord,"),
        (33, 33, "for"),
        (34, 36, "the sword"),
        (37, 39, "of his justice"),
        (40, 42, "is present"),
        (43, 46, "in his right hand;"),
        (47, 48, "and behold,"),
        (49, 51, "at that day,"),
        (52, 55, "if ye spurn"),
        (56, 58, "at his doings"),
        (59, 63, "he will cause"),
        (64, 68, "that it shall soon come"),
        (69, 70, "this thing"),
        (71, 74, "upon you."),
    ],
    5: [
        (0, 1, "Wo"),
        (2, 4, "unto him"),
        (5, 8, "that spurneth"),
        (9, 10, "at the doings"),
        (11, 14, "which are willed"),
        (15, 16, "of the Lord;"),
        (17, 17, "yea,"),
        (18, 19, "wo"),
        (20, 22, "unto him"),
        (23, 24, "that"),
        (25, 29, "shall deny"),
        (30, 30, "the Christ"),
        (31, 33, "and his works!"),
    ],
    6: [
        (0, 0, "Yea,"),
        (1, 2, "wo"),
        (3, 5, "unto him"),
        (6, 7, "that"),
        (8, 9, "shall deny"),
        (10, 13, "the revelations of the Lord,"),
        (14, 15, "and that"),
        (16, 18, "shall say"),
        (19, 22, "no longer worketh"),
        (23, 24, "the Lord"),
        (25, 28, "by revelation,"),
        (29, 31, "or by prophecy,"),
        (32, 34, "or by gifts,"),
        (35, 37, "or by tongues,"),
        (38, 40, "or by healings,"),
        (41, 44, "or by the power"),
        (45, 48, "of the Holy Ghost!"),
    ],
    7: [
        (0, 0, "Yea,"),
        (1, 2, "wo"),
        (3, 5, "unto him"),
        (6, 7, "that"),
        (8, 10, "shall say"),
        (11, 13, "at that day,"),
        (14, 18, "to get gain,"),
        (19, 20, "that"),
        (21, 24, "there can be no"),
        (25, 27, "more"),
        (28, 29, "miracles"),
        (30, 31, "wrought"),
        (32, 34, "by Jesus Christ;"),
        (35, 35, "for"),
        (36, 39, "he that"),
        (40, 42, "doeth"),
        (43, 44, "this thing"),
        (45, 50, "he shall become"),
        (51, 55, "like unto the son"),
        (56, 58, "of perdition,"),
        (59, 60, "for whom"),
        (61, 65, "there was no mercy,"),
        (66, 67, "for him,"),
        (68, 70, "according to"),
        (71, 72, "the word"),
        (73, 74, "of Christ!"),
    ],
    8: [
        (0, 0, "Yea,"),
        (1, 5, "and ye need not"),
        (6, 8, "any longer hiss,"),
        (9, 10, "nor spurn,"),
        (11, 12, "nor mock"),
        (13, 15, "the Jews,"),
        (16, 18, "nor any part"),
        (19, 21, "of the remnant"),
        (22, 24, "of the house"),
        (25, 26, "of Israel;"),
        (27, 28, "for behold,"),
        (29, 30, "remembereth"),
        (31, 33, "the Lord"),
        (34, 35, "his covenant"),
        (36, 39, "unto them,"),
        (40, 40, "and"),
        (41, 45, "he will do"),
        (46, 49, "unto them"),
        (50, 54, "according to that"),
        (55, 58, "which he hath sworn."),
    ],
    9: [
        (0, 1, "Therefore"),
        (2, 5, "ye need not"),
        (6, 7, "suppose"),
        (8, 12, "that ye can turn"),
        (13, 15, "the right hand"),
        (16, 18, "of the Lord"),
        (19, 22, "unto the left,"),
        (23, 26, "that he may not"),
        (27, 30, "do"),
        (31, 32, "judgment"),
        (33, 35, "unto the fulfilling"),
        (36, 38, "of the covenant which"),
        (39, 41, "he hath made"),
        (42, 44, "unto the house"),
        (45, 46, "of Israel."),
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
