"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 23 — Jesus commands the
Nephites to search the words of Isaiah and the prophets diligently, for they testify
of him; he calls for the records to be brought and, finding that the fulfilment of
Samuel the Lamanite's prophecy concerning the resurrected saints had not been written,
he commands that it be recorded; the scriptures are amended and he expounds all things
from the beginning until his coming.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

    python3 build_overrides_3nephi23.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 23

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 3, "behold,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 15, "that ye ought to search"),
        (16, 18, "these things."),
        (19, 19, "Yea,"),
        (20, 23, "I give"),
        (24, 26, "unto you"),
        (27, 28, "a commandment"),
        (29, 31, "that ye search"),
        (32, 34, "diligently"),
        (35, 37, "these things;"),
        (38, 38, "for"),
        (39, 41, "great are"),
        (42, 44, "the words of Isaiah."),
    ],
    2: [
        (0, 2, "For surely"),
        (3, 6, "he spake"),
        (7, 9, "as touching"),
        (10, 11, "all things"),
        (12, 14, "concerning"),
        (15, 16, "my people"),
        (17, 18, "which are"),
        (19, 21, "of the house"),
        (22, 23, "of Israel;"),
        (24, 25, "therefore"),
        (26, 29, "it must needs be also"),
        (30, 33, "that he must speak"),
        (34, 35, "to the Gentiles."),
    ],
    3: [
        (0, 3, "And all things"),
        (4, 8, "that he spake"),
        (9, 10, "have been fulfilled"),
        (11, 15, "and shall be fulfilled,"),
        (16, 19, "even according to"),
        (20, 20, "the words"),
        (21, 25, "which he spake."),
    ],
    4: [
        (0, 1, "Therefore"),
        (2, 5, "give ye heed"),
        (6, 8, "to my words;"),
        (9, 10, "write"),
        (11, 12, "these things"),
        (13, 16, "which I have told"),
        (17, 19, "you;"),
        (20, 23, "and according"),
        (24, 26, "to the time"),
        (27, 29, "and the will"),
        (30, 32, "of the Father"),
        (33, 38, "shall go forth"),
        (39, 40, "these things"),
        (41, 42, "unto the Gentiles."),
    ],
    5: [
        (0, 4, "And whosoever"),
        (5, 6, "will hearken"),
        (7, 9, "unto my words"),
        (10, 11, "and repenteth"),
        (12, 13, "and is baptized,"),
        (14, 17, "the same"),
        (18, 21, "shall be saved."),
        (22, 22, "Search"),
        (23, 24, "the prophets,"),
        (25, 25, "for"),
        (26, 30, "many there be"),
        (31, 33, "that testify"),
        (34, 36, "of"),
        (37, 38, "these things."),
    ],
    6: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 10, "when had said"),
        (11, 11, "Jesus"),
        (12, 14, "these words"),
        (15, 19, "he spake again"),
        (20, 23, "unto them,"),
        (24, 31, "after he had fully expounded"),
        (32, 35, "unto them"),
        (36, 38, "all the scriptures"),
        (39, 43, "which they had,"),
        (44, 47, "he said"),
        (48, 51, "unto them:"),
        (52, 52, "Behold,"),
        (53, 55, "there are"),
        (56, 58, "other scriptures"),
        (59, 61, "that are not"),
        (62, 64, "with you,"),
        (65, 67, "I would"),
        (68, 72, "that ye should write."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he said"),
        (8, 9, "unto Nephi:"),
        (10, 11, "Bring forth"),
        (12, 14, "the record which"),
        (15, 17, "ye have kept."),
    ],
    8: [
        (0, 5, "And when had brought forth"),
        (6, 6, "the records"),
        (7, 8, "by Nephi,"),
        (9, 12, "and laid them"),
        (13, 15, "before him,"),
        (16, 20, "he looked"),
        (21, 22, "upon them"),
        (23, 25, "and said:"),
    ],
    9: [
        (0, 1, "Verily"),
        (2, 5, "I say"),
        (6, 8, "unto you,"),
        (9, 11, "I commanded"),
        (12, 13, "my servant"),
        (14, 15, "Samuel,"),
        (16, 18, "the Lamanite,"),
        (19, 25, "that he should testify"),
        (26, 28, "unto this people,"),
        (29, 30, "namely,"),
        (31, 34, "at the day that"),
        (35, 39, "should glorify"),
        (40, 42, "the Father"),
        (43, 44, "his name"),
        (45, 47, "in me,"),
        (48, 50, "there were"),
        (51, 52, "many"),
        (53, 56, "of the saints"),
        (57, 61, "who should arise"),
        (62, 65, "from the dead,"),
        (66, 71, "and should appear"),
        (72, 74, "unto many,"),
        (75, 80, "and should minister"),
        (81, 84, "unto them."),
        (85, 89, "And he said"),
        (90, 93, "unto them:"),
        (94, 98, "Was it not so?"),
    ],
    10: [
        (0, 3, "And answered"),
        (4, 5, "his disciples"),
        (6, 8, "him"),
        (9, 11, "and said:"),
        (12, 12, "Yea,"),
        (13, 15, "O Lord,"),
        (16, 18, "did prophesy"),
        (19, 19, "Samuel"),
        (20, 22, "according to"),
        (23, 24, "thy words,"),
        (25, 29, "and were all fulfilled"),
        (30, 31, "they."),
    ],
    11: [
        (0, 3, "And said"),
        (4, 4, "Jesus"),
        (5, 8, "unto them:"),
        (9, 11, "How be it"),
        (12, 15, "that ye have not written"),
        (16, 18, "this thing,"),
        (19, 24, "that so many were"),
        (25, 27, "the saints"),
        (28, 30, "did arise"),
        (31, 33, "and appear"),
        (34, 36, "unto many"),
        (37, 39, "and did minister"),
        (40, 43, "unto them?"),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 6, "Nephi remembered"),
        (7, 9, "had not been written"),
        (10, 11, "this thing."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 6, "Jesus commanded"),
        (7, 9, "that it should be written;"),
        (10, 12, "therefore"),
        (13, 15, "it was written"),
        (16, 20, "even as he commanded."),
    ],
    14: [
        (0, 1, "And now"),
        (2, 4, "it came to pass that"),
        (5, 8, "when had expounded"),
        (9, 10, "Jesus"),
        (11, 13, "all the scriptures"),
        (14, 15, "in one,"),
        (16, 16, "which"),
        (17, 19, "they had written,"),
        (20, 24, "he commanded them"),
        (25, 30, "that they should teach"),
        (31, 32, "the things"),
        (33, 36, "which he had expounded"),
        (37, 40, "unto them."),
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
