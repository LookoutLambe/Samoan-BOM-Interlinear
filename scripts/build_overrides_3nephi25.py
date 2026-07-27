"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 25 — Jesus completes his
quotation of Malachi with Malachi 4: the day cometh that shall burn as an oven, when
the proud and the wicked shall be as stubble, but unto them that fear his name the Son
of Righteousness shall arise with healing in his wings; the righteous shall tread down
the wicked; the people are to remember the law of Moses; and Elijah the prophet shall
be sent before the great and dreadful day of the Lord to turn the hearts of the fathers
and the children to one another.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

    python3 build_overrides_3nephi25.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 25

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "For"),
        (1, 1, "behold,"),
        (2, 4, "cometh"),
        (5, 6, "the day"),
        (7, 11, "that shall burn"),
        (12, 16, "as an oven;"),
        (17, 20, "and all"),
        (21, 22, "the proud,"),
        (23, 23, "yea,"),
        (24, 26, "and all"),
        (27, 29, "that do wickedly,"),
        (30, 34, "shall be as"),
        (35, 37, "the stubble of grain;"),
        (38, 41, "and the day"),
        (42, 46, "that shall come"),
        (47, 50, "shall burn up"),
        (51, 52, "them,"),
        (53, 56, "saith"),
        (57, 58, "the Lord"),
        (59, 60, "of Hosts,"),
        (61, 67, "that it shall not leave"),
        (68, 69, "a root"),
        (70, 73, "nor branch"),
        (74, 76, "for them."),
    ],
    2: [
        (0, 3, "But unto you"),
        (4, 7, "that fear"),
        (8, 10, "my name,"),
        (11, 17, "shall arise"),
        (18, 19, "the Son"),
        (20, 22, "of Righteousness"),
        (23, 25, "with healing"),
        (26, 28, "in his wings;"),
        (29, 35, "and ye shall go forth"),
        (36, 38, "and grow up"),
        (39, 41, "as"),
        (42, 43, "calves"),
        (44, 46, "in the stall."),
    ],
    3: [
        (0, 7, "And ye shall tread down"),
        (8, 10, "the wicked;"),
        (11, 11, "for"),
        (12, 17, "they shall become"),
        (18, 19, "ashes"),
        (20, 22, "under"),
        (23, 25, "the soles of your feet"),
        (26, 29, "in the day that"),
        (30, 35, "I shall do"),
        (36, 37, "this thing,"),
        (38, 41, "saith"),
        (42, 43, "the Lord"),
        (44, 45, "of Hosts."),
    ],
    4: [
        (0, 2, "Remember ye"),
        (3, 4, "the law"),
        (5, 6, "of Moses,"),
        (7, 8, "my servant,"),
        (9, 9, "which"),
        (10, 13, "I commanded"),
        (14, 16, "unto him"),
        (17, 18, "in Horeb"),
        (19, 21, "for all Israel,"),
        (22, 23, "together with"),
        (24, 24, "the statutes"),
        (25, 26, "and judgments."),
    ],
    5: [
        (0, 0, "Behold,"),
        (1, 6, "I will send"),
        (7, 9, "unto you"),
        (10, 12, "Elijah the prophet"),
        (13, 16, "before the coming of"),
        (17, 19, "the great day"),
        (20, 22, "and dreadful"),
        (23, 25, "of the Lord;"),
    ],
    6: [
        (0, 5, "And he shall turn"),
        (6, 8, "the heart of the fathers"),
        (9, 10, "to the children,"),
        (11, 14, "and the heart of the children"),
        (15, 18, "to their fathers,"),
        (19, 22, "lest I come"),
        (23, 24, "and smite"),
        (25, 26, "the earth"),
        (27, 29, "with a curse."),
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
