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

    python3 build_overrides_moroni2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 2

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "The words of Christ,"),
        (4, 7, "which he spoke"),
        (8, 10, "unto his disciples,"),
        (11, 12, "the twelve"),
        (13, 17, "whom he chose,"),
        (18, 21, "while he laid his hands"),
        (22, 25, "upon them—"),
    ],
    2: [
        (0, 3, "And he called"),
        (4, 5, "them"),
        (6, 9, "by their names,"),
        (10, 12, "saying:"),
        (13, 16, "Call ye upon"),
        (17, 19, "the Father"),
        (20, 22, "in my name,"),
        (23, 26, "in mighty prayer;"),
        (27, 32, "and after ye have done"),
        (33, 35, "this thing,"),
        (36, 40, "ye shall receive"),
        (41, 42, "the power"),
        (43, 47, "that ye give"),
        (48, 50, "the Holy Ghost"),
        (51, 53, "unto him"),
        (54, 55, "he on whom"),
        (56, 62, "ye shall lay"),
        (63, 65, "your hands"),
        (66, 68, "upon him;"),
        (69, 72, "and in my name"),
        (73, 77, "shall ye give it,"),
        (78, 82, "for thus is done"),
        (83, 85, "by mine apostles."),
    ],
    3: [
        (0, 1, "Now"),
        (2, 6, "spake Christ"),
        (7, 10, "unto them"),
        (11, 12, "these words"),
        (13, 15, "at the time"),
        (16, 20, "of his first appearing;"),
        (21, 24, "and heard it not"),
        (25, 29, "the multitude of people,"),
        (30, 32, "but heard it"),
        (33, 36, "the disciples;"),
        (37, 40, "and as many"),
        (41, 43, "of them"),
        (44, 48, "as were laid upon"),
        (49, 51, "their hands,"),
        (52, 55, "there came upon them"),
        (56, 58, "the Holy Ghost."),
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
