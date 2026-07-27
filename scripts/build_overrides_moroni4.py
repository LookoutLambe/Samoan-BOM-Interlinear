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

    python3 build_overrides_moroni4.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 4

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "The manner"),
        (3, 4, "of blessing"),
        (5, 8, "and administering"),
        (9, 12, "by their elders"),
        (13, 14, "and priests"),
        (15, 19, "the body and the blood"),
        (20, 21, "of Christ"),
        (22, 24, "unto the church;"),
        (25, 28, "and they did it"),
        (29, 31, "according to"),
        (32, 34, "the commandments of Christ;"),
        (35, 38, "wherefore"),
        (39, 42, "we do know"),
        (43, 46, "the way is right;"),
        (47, 50, "and the elder"),
        (51, 54, "or the priest"),
        (55, 56, "did perform"),
        (57, 58, "the blessing—"),
    ],
    2: [
        (0, 3, "And they knelt"),
        (4, 5, "down"),
        (6, 9, "with the church,"),
        (10, 12, "and prayed"),
        (13, 15, "unto the Father"),
        (16, 20, "in the name of Christ,"),
        (21, 23, "saying:"),
    ],
    3: [
        (0, 2, "O God,"),
        (3, 5, "the Eternal Father,"),
        (6, 9, "we do ask"),
        (10, 12, "of thee"),
        (13, 15, "in the name"),
        (16, 18, "of thy Son,"),
        (19, 21, "even Jesus Christ,"),
        (22, 24, "that thou wilt bless"),
        (25, 26, "and sanctify"),
        (27, 28, "this bread"),
        (29, 31, "to the souls"),
        (32, 34, "of all of them"),
        (35, 37, "those who"),
        (38, 40, "partake of it;"),
        (41, 44, "that they may eat"),
        (45, 47, "in remembrance"),
        (48, 50, "of the body"),
        (51, 53, "of thy Son,"),
        (54, 56, "and witness"),
        (57, 59, "unto thee,"),
        (60, 62, "O God,"),
        (63, 65, "the Eternal Father,"),
        (66, 68, "that they are willing"),
        (69, 70, "to take"),
        (71, 74, "upon them"),
        (75, 79, "the name of thy Son,"),
        (80, 82, "and always remember"),
        (83, 84, "him,"),
        (85, 89, "and keep his commandments"),
        (90, 93, "which he hath given"),
        (94, 97, "unto them,"),
        (98, 102, "that they may always have"),
        (103, 104, "his Spirit"),
        (105, 109, "to be with them."),
        (110, 110, "Amen."),
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
