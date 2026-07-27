"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 14 — a great curse comes upon
the land because of the iniquity of the people, such that whoso laid down his tool could
not find it again; every man kept his sword to defend his property; Coriantumr wars against
Gilead, then Lib, then Shiz, who sweeps the earth before him, and the whole face of the
land is covered with dead bodies as the two mighty armies pursue one another to the death.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_moroni1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 1

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "Now"),
        (2, 3, "I,"),
        (4, 5, "Moroni,"),
        (6, 11, "after I had finished"),
        (12, 14, "the ending"),
        (15, 17, "of the abridgment"),
        (18, 20, "of the record"),
        (21, 25, "of the people of Jared,"),
        (26, 28, "I thought"),
        (29, 35, "I would not write again"),
        (36, 39, "any more things,"),
        (40, 40, "nevertheless"),
        (41, 45, "I have not yet perished;"),
        (46, 51, "and I reveal not"),
        (52, 53, "myself"),
        (54, 56, "unto the Lamanites"),
        (57, 60, "lest they slay"),
        (61, 61, "me."),
    ],
    2: [
        (0, 1, "For behold,"),
        (2, 5, "are very fierce"),
        (6, 8, "their wars"),
        (9, 11, "among"),
        (12, 14, "themselves;"),
        (15, 17, "and because of"),
        (18, 20, "their anger"),
        (21, 24, "they put to death"),
        (25, 27, "all the Nephites"),
        (28, 32, "who will not deny"),
        (33, 34, "the Christ."),
    ],
    3: [
        (0, 2, "And I,"),
        (3, 4, "Moroni,"),
        (5, 8, "I will not deny"),
        (9, 10, "the Christ;"),
        (11, 14, "wherefore,"),
        (15, 19, "I do wander about"),
        (20, 23, "to any place"),
        (24, 30, "whither I can go"),
        (31, 33, "for the safety"),
        (34, 37, "of my own life."),
    ],
    4: [
        (0, 3, "Wherefore,"),
        (4, 7, "I write"),
        (8, 12, "a few more things,"),
        (13, 16, "contrary to"),
        (17, 18, "that thing"),
        (19, 23, "which I supposed;"),
        (24, 27, "for I thought"),
        (28, 34, "I would not write again"),
        (35, 38, "any more things;"),
        (39, 44, "but I will write"),
        (45, 48, "a few small additions,"),
        (49, 49, "perhaps"),
        (50, 53, "may be of worth"),
        (54, 56, "unto my brethren,"),
        (57, 59, "the Lamanites,"),
        (60, 62, "in some day"),
        (63, 65, "to come,"),
        (66, 69, "according to"),
        (70, 74, "the will of the Lord."),
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
