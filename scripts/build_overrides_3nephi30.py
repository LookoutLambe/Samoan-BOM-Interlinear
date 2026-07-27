"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 30 — the closing chapter:
Jesus, through Mormon, commands the Gentiles to hearken and turn from all their wicked
ways — their lyings, whoredoms, secret abominations, idolatries, murders, priestcrafts,
envyings and strifes — and to come unto him, be baptized in his name, receive a remission
of sins and the Holy Ghost, that they may be numbered with the covenant house of Israel.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, imperative `Ia ... ia` envelope 16,
vocative `E, ... e` envelope 12). `o le a` stays atomic and is never fused
with a following `se X` NP.

    python3 build_overrides_3nephi30.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 30

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "Hearken ye,"),
        (3, 6, "O ye Gentiles,"),
        (7, 9, "and hear"),
        (10, 11, "the words"),
        (12, 14, "of Jesus Christ,"),
        (15, 16, "the Son"),
        (17, 20, "of the living God,"),
        (21, 21, "which"),
        (22, 25, "he hath commanded"),
        (26, 26, "me"),
        (27, 29, "that I should"),
        (30, 33, "speak"),
        (34, 35, "concerning"),
        (36, 38, "you,"),
        (39, 40, "for behold,"),
        (41, 43, "he commandeth"),
        (44, 44, "me"),
        (45, 47, "that I should write,"),
        (48, 49, "saying:"),
    ],
    2: [
        (0, 2, "Turn ye away,"),
        (3, 4, "all ye"),
        (5, 6, "Gentiles,"),
        (7, 8, "from"),
        (9, 12, "your wicked ways;"),
        (13, 15, "and repent"),
        (16, 18, "of your"),
        (19, 20, "evil doings,"),
        (21, 23, "and of"),
        (24, 26, "your lyings"),
        (27, 28, "and deceivings,"),
        (29, 31, "and of"),
        (32, 34, "your whoredoms,"),
        (35, 37, "and of"),
        (38, 41, "your abominations"),
        (42, 42, "secret,"),
        (43, 45, "and your"),
        (46, 48, "bowing to idols,"),
        (49, 51, "and of"),
        (52, 53, "your"),
        (54, 55, "murders,"),
        (56, 58, "and your"),
        (59, 60, "priestcrafts,"),
        (61, 63, "and your"),
        (64, 64, "envyings,"),
        (65, 67, "and your"),
        (68, 68, "strifes,"),
        (69, 71, "and from"),
        (72, 75, "all your wickedness"),
        (76, 78, "and abominations,"),
        (79, 81, "and come"),
        (82, 84, "unto me,"),
        (85, 87, "and be baptized"),
        (88, 90, "in my name,"),
        (91, 94, "that ye may"),
        (95, 96, "receive"),
        (97, 99, "a remission"),
        (100, 103, "of your sins,"),
        (104, 105, "and be filled"),
        (106, 109, "with the Holy Ghost,"),
        (110, 112, "that may be numbered"),
        (113, 113, "ye"),
        (114, 115, "with"),
        (116, 117, "my people"),
        (118, 119, "who are"),
        (120, 122, "of the house"),
        (123, 124, "of Israel."),
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
