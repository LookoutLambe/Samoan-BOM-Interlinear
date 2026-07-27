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

    python3 build_overrides_moroni3.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 3

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "The manner"),
        (3, 5, "by which ordained"),
        (6, 9, "the disciples,"),
        (10, 13, "who were called"),
        (14, 18, "the elders of the church,"),
        (19, 20, "priests"),
        (21, 22, "and teachers—"),
    ],
    2: [
        (0, 6, "After they had prayed"),
        (7, 9, "unto the Father"),
        (10, 14, "in the name of Christ,"),
        (15, 17, "they laid"),
        (18, 20, "their hands"),
        (21, 24, "upon them,"),
        (25, 27, "and said:"),
    ],
    3: [
        (0, 2, "In the name"),
        (3, 5, "of Jesus Christ"),
        (6, 9, "I ordain"),
        (10, 10, "thee"),
        (11, 15, "to be a priest,"),
        (16, 17, "(or if"),
        (18, 20, "a teacher,"),
        (21, 24, "I ordain"),
        (25, 25, "thee"),
        (26, 30, "to be a teacher)"),
        (31, 35, "to preach repentance"),
        (36, 40, "and remission of sins"),
        (41, 42, "through"),
        (43, 45, "Jesus Christ,"),
        (46, 48, "by the enduring"),
        (49, 51, "in the faith"),
        (52, 54, "on his name"),
        (55, 59, "unto the end."),
        (60, 60, "Amen."),
    ],
    4: [
        (0, 4, "And after this manner"),
        (5, 8, "did they ordain"),
        (9, 11, "priests and teachers,"),
        (12, 14, "according to"),
        (15, 17, "the gifts and callings"),
        (18, 20, "of God"),
        (21, 22, "unto men;"),
        (23, 26, "and they did ordain"),
        (27, 28, "them"),
        (29, 31, "by the power"),
        (32, 35, "of the Holy Ghost,"),
        (36, 37, "which was"),
        (38, 41, "in them."),
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
