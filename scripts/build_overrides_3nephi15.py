"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 15 — Jesus declares
the law of Moses fulfilled in him, for he is the God who gave the law and
covenanted with Israel; he explains that the Nephites are the "other sheep" of
whom he spoke at Jerusalem — not the Gentiles, who would not hear his voice — and
that the Father commanded he should not yet manifest himself to the tribes of the
house of Israel; and he foretells that in the latter day the gospel shall come to
this remnant of Joseph through the Gentiles.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi15.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 15

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 9, "when Jesus had finished"),
        (10, 12, "these words"),
        (13, 18, "he cast his eyes round about"),
        (19, 23, "on the multitude,"),
        (24, 26, "and said"),
        (27, 30, "unto them:"),
        (31, 31, "Behold,"),
        (32, 36, "ye have heard the things"),
        (37, 40, "I taught"),
        (41, 46, "before I ascended"),
        (47, 49, "to my Father;"),
        (50, 51, "therefore,"),
        (52, 57, "whoso remembers"),
        (58, 60, "these my words"),
        (61, 64, "and does them,"),
        (65, 67, "that one"),
        (68, 73, "will I raise up"),
        (74, 77, "at the last day."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when Jesus had spoken"),
        (11, 13, "these words"),
        (14, 16, "he perceived"),
        (17, 21, "there were some"),
        (22, 27, "among them"),
        (28, 29, "who marveled,"),
        (30, 32, "and pondered"),
        (33, 38, "what his will was"),
        (39, 45, "concerning the law of Moses;"),
        (46, 50, "for they understood not"),
        (51, 55, "the saying that"),
        (56, 60, "old things had passed away,"),
        (61, 65, "and all things had become new."),
    ],
    3: [
        (0, 4, "And he said"),
        (5, 8, "unto them:"),
        (9, 12, "Marvel not"),
        (13, 17, "that I said"),
        (18, 20, "unto you"),
        (21, 25, "old things had passed away,"),
        (26, 30, "and all things had become new."),
    ],
    4: [
        (0, 0, "Behold,"),
        (1, 4, "I say"),
        (5, 7, "unto you,"),
        (8, 12, "the law is fulfilled which"),
        (13, 17, "was given unto Moses."),
    ],
    5: [
        (0, 0, "Behold,"),
        (1, 4, "I am he who"),
        (5, 9, "gave the law,"),
        (10, 14, "and I am he who"),
        (15, 16, "covenanted"),
        (17, 21, "with my people Israel;"),
        (22, 23, "therefore,"),
        (24, 27, "the law is fulfilled"),
        (28, 30, "in me,"),
        (31, 34, "for I have come"),
        (35, 38, "to fulfil the law;"),
        (39, 40, "therefore"),
        (41, 44, "the law is ended."),
    ],
    6: [
        (0, 0, "Behold,"),
        (1, 4, "I do not do away with"),
        (5, 5, "the prophets,"),
        (6, 11, "for the many prophecies"),
        (12, 14, "not yet fulfilled"),
        (15, 17, "in me,"),
        (18, 23, "verily I say"),
        (24, 26, "unto you,"),
        (27, 32, "shall all be fulfilled."),
    ],
    7: [
        (0, 5, "And because I said"),
        (6, 8, "unto you"),
        (9, 13, "old things have passed away,"),
        (14, 20, "I do not do away with the things"),
        (21, 24, "which have been spoken"),
        (25, 33, "concerning things to come."),
    ],
    8: [
        (0, 1, "For behold,"),
        (2, 5, "is not all fulfilled"),
        (6, 8, "the covenant which"),
        (9, 11, "I made"),
        (12, 15, "with my people;"),
        (16, 19, "but the law"),
        (20, 24, "given unto Moses,"),
        (25, 29, "is ended in me."),
    ],
    9: [
        (0, 0, "Behold,"),
        (1, 5, "I am the law,"),
        (6, 8, "and the light."),
        (9, 12, "Look ye"),
        (13, 15, "unto me,"),
        (16, 17, "and endure"),
        (18, 22, "unto the end,"),
        (23, 29, "and ye shall live;"),
        (30, 36, "for he who endures"),
        (37, 41, "unto the end"),
        (42, 49, "will I give to him"),
        (50, 52, "eternal life."),
    ],
    10: [
        (0, 0, "Behold,"),
        (1, 7, "I have given unto you"),
        (8, 8, "the commandments;"),
        (9, 10, "therefore"),
        (11, 16, "keep ye my commandments."),
        (17, 21, "And this is the law"),
        (22, 23, "and the prophets,"),
        (24, 28, "for they truly testified"),
        (29, 31, "of me."),
    ],
    11: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 11, "when Jesus had spoken"),
        (12, 14, "these words,"),
        (15, 19, "he said"),
        (20, 24, "unto the twelve whom"),
        (25, 27, "he had chosen:"),
    ],
    12: [
        (0, 4, "Ye are my disciples;"),
        (5, 10, "and ye are a light"),
        (11, 13, "unto this people,"),
        (14, 19, "who are a remnant of"),
        (20, 24, "the house of Joseph."),
    ],
    13: [
        (0, 1, "And behold,"),
        (2, 5, "this is the land"),
        (6, 9, "of your inheritance;"),
        (10, 16, "and the Father has given it"),
        (17, 19, "unto you."),
    ],
    14: [
        (0, 7, "And there was never a time"),
        (8, 14, "the Father gave"),
        (15, 19, "a commandment unto me"),
        (20, 25, "that I tell this thing"),
        (26, 31, "unto your brethren at Jerusalem."),
    ],
    15: [
        (0, 6, "Neither was there a time"),
        (7, 13, "the Father gave"),
        (14, 18, "a commandment unto me"),
        (19, 26, "that I tell unto them"),
        (27, 31, "concerning the other tribes"),
        (32, 36, "of the house of Israel,"),
        (37, 44, "whom the Father has led away"),
        (45, 47, "from the land."),
    ],
    16: [
        (0, 5, "This is how much"),
        (6, 9, "the Father commanded me"),
        (10, 12, "by the Father,"),
        (13, 18, "that I tell"),
        (19, 22, "unto them:"),
    ],
    17: [
        (0, 5, "I have"),
        (6, 8, "other sheep"),
        (9, 14, "which are not of this fold;"),
        (15, 22, "them also I must bring;"),
        (23, 28, "and they shall hear"),
        (29, 31, "my voice;"),
        (32, 38, "and there shall be one fold,"),
        (39, 43, "and one shepherd."),
    ],
    18: [
        (0, 2, "And now,"),
        (3, 7, "because of stiffneckedness"),
        (8, 11, "and unbelief"),
        (12, 16, "they understood not"),
        (17, 19, "my words;"),
        (20, 21, "therefore"),
        (22, 25, "I was commanded"),
        (26, 34, "that I say no more word"),
        (35, 37, "from the Father"),
        (38, 42, "concerning this thing"),
        (43, 46, "unto them."),
    ],
    19: [
        (0, 0, "But,"),
        (1, 2, "verily,"),
        (3, 6, "I say"),
        (7, 9, "unto you,"),
        (10, 15, "the Father has commanded me,"),
        (16, 20, "and I tell"),
        (21, 23, "unto you,"),
        (24, 27, "ye were separated"),
        (28, 33, "from among them"),
        (34, 38, "because of their iniquity;"),
        (39, 40, "therefore"),
        (41, 45, "because of their iniquity"),
        (46, 50, "they know not"),
        (51, 55, "concerning you."),
    ],
    20: [
        (0, 2, "And verily,"),
        (3, 7, "I say again"),
        (8, 10, "unto you"),
        (11, 16, "the Father has separated"),
        (17, 18, "the other tribes"),
        (19, 23, "from them;"),
        (24, 29, "and because of their iniquity"),
        (30, 34, "they know not"),
        (35, 40, "concerning them."),
    ],
    21: [
        (0, 6, "And verily I say"),
        (7, 9, "unto you,"),
        (10, 14, "ye are they of whom"),
        (15, 19, "I spoke:"),
        (20, 23, "I have"),
        (24, 26, "other sheep"),
        (27, 32, "which are not of this fold;"),
        (33, 40, "them also I must bring,"),
        (41, 46, "and they shall hear"),
        (47, 49, "my voice;"),
        (50, 56, "and there shall be one fold,"),
        (57, 61, "and one shepherd."),
    ],
    22: [
        (0, 4, "And they understood not"),
        (5, 7, "me,"),
        (8, 11, "for they supposed"),
        (12, 17, "that they were the Gentiles;"),
        (18, 22, "for they understood not"),
        (23, 27, "the Gentiles should be converted"),
        (28, 33, "through their preaching."),
    ],
    23: [
        (0, 7, "And they understood me not"),
        (8, 12, "when I said"),
        (13, 18, "they shall hear"),
        (19, 21, "my voice;"),
        (22, 30, "and they understood not from me"),
        (31, 37, "there should be no time"),
        (38, 41, "the Gentiles hear"),
        (42, 44, "my voice—"),
        (45, 53, "I should not manifest myself"),
        (54, 57, "unto them"),
        (58, 59, "save"),
        (60, 65, "by the Holy Ghost."),
    ],
    24: [
        (0, 1, "But behold,"),
        (2, 6, "ye have all heard"),
        (7, 9, "my voice,"),
        (10, 15, "and seen me;"),
        (16, 21, "and ye are my sheep,"),
        (22, 25, "and ye are numbered"),
        (26, 31, "among those whom"),
        (32, 37, "the Father has given"),
        (38, 40, "unto me."),
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
