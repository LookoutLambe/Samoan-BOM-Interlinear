"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 5 — Moroni addresses the future
translator (Joseph Smith): he has written and sealed the words, which are not to be
touched save in the Lord's due time. Three witnesses shall be shown the plates by the
power of God, and in the mouth of three witnesses these things shall be established, to
stand as a testimony against the world at the last day.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether5.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 5

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Moroni,"),
        (7, 9, "have written"),
        (10, 10, "the words"),
        (11, 14, "which were commanded"),
        (15, 15, "me,"),
        (16, 18, "according to"),
        (19, 20, "my remembrance;"),
        (21, 21, "and"),
        (22, 27, "I have made known"),
        (28, 30, "unto thee"),
        (31, 32, "the things"),
        (33, 35, "which I have sealed;"),
        (36, 37, "therefore"),
        (38, 41, "touch not"),
        (42, 43, "them"),
        (44, 47, "that thou translate;"),
        (48, 50, "for is forbidden"),
        (51, 52, "that thing"),
        (53, 55, "unto thee,"),
        (56, 59, "save when cometh"),
        (60, 61, "the time"),
        (62, 64, "appointed"),
        (65, 67, "in the wisdom"),
        (68, 70, "of God."),
    ],
    2: [
        (0, 1, "And behold,"),
        (2, 6, "perhaps thou mayest"),
        (7, 9, "be able to obtain"),
        (10, 11, "the privilege"),
        (12, 15, "to show forth"),
        (16, 16, "the plates"),
        (17, 20, "unto them"),
        (21, 22, "who"),
        (23, 26, "shall assist"),
        (27, 28, "to bring forth"),
        (29, 30, "this work;"),
    ],
    3: [
        (0, 0, "And"),
        (1, 5, "shall be shown"),
        (6, 7, "them"),
        (8, 10, "unto three"),
        (11, 13, "by the power"),
        (14, 16, "of God;"),
        (17, 18, "wherefore"),
        (19, 24, "they shall know"),
        (25, 27, "of a surety"),
        (28, 31, "that these things are true."),
    ],
    4: [
        (0, 3, "And in the mouth"),
        (4, 6, "of three witnesses"),
        (7, 11, "shall be established"),
        (12, 13, "these things;"),
        (14, 17, "and the testimony"),
        (18, 20, "of three,"),
        (21, 23, "and this work,"),
        (24, 24, "in which"),
        (25, 30, "shall be manifested"),
        (31, 35, "the power of God"),
        (36, 39, "and his word also,"),
        (40, 44, "which is testified of"),
        (45, 46, "the Father,"),
        (47, 49, "and the Son,"),
        (50, 53, "and the Holy Ghost—"),
        (54, 58, "and all these things"),
        (59, 62, "shall stand forth"),
        (63, 65, "for a witness"),
        (66, 70, "against the world"),
        (71, 74, "at the last day."),
    ],
    5: [
        (0, 3, "And if it so be"),
        (4, 8, "they shall repent"),
        (9, 11, "and come"),
        (12, 14, "unto the Father"),
        (15, 19, "in the name of Jesus,"),
        (20, 23, "they shall be received"),
        (24, 25, "they"),
        (26, 28, "into the kingdom"),
        (29, 31, "of God."),
    ],
    6: [
        (0, 2, "And now,"),
        (3, 7, "if there is no power"),
        (8, 11, "in me"),
        (12, 14, "for these things,"),
        (15, 16, "judge ye;"),
        (17, 17, "for"),
        (18, 22, "ye shall know"),
        (23, 26, "that I have"),
        (27, 28, "the power"),
        (29, 33, "when ye behold"),
        (34, 36, "me,"),
        (37, 37, "and"),
        (38, 42, "we shall stand"),
        (43, 47, "before God"),
        (48, 51, "at the last day."),
        (52, 52, "Amen."),
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
