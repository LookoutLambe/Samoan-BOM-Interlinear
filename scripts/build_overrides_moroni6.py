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

    python3 build_overrides_moroni6.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 6

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 6, "I speak"),
        (7, 8, "concerning"),
        (9, 11, "baptism."),
        (12, 12, "Behold,"),
        (13, 14, "were baptized"),
        (15, 16, "elders, priests,"),
        (17, 18, "and teachers;"),
        (19, 22, "and were not baptized"),
        (23, 24, "they"),
        (25, 26, "except"),
        (27, 31, "they bore fruit"),
        (32, 34, "fitting"),
        (35, 37, "whereby is known"),
        (38, 40, "they were worthy."),
    ],
    2: [
        (0, 4, "Nor did they admit"),
        (5, 7, "any person"),
        (8, 10, "unto baptism"),
        (11, 12, "except"),
        (13, 16, "they did come"),
        (17, 18, "forth"),
        (19, 22, "with a broken heart"),
        (23, 26, "and a contrite spirit,"),
        (27, 29, "and testified"),
        (30, 32, "unto the church"),
        (33, 36, "they had sincerely repented"),
        (37, 41, "of all their sins."),
    ],
    3: [
        (0, 4, "And no one"),
        (5, 6, "was admitted"),
        (7, 9, "unto baptism"),
        (10, 11, "except"),
        (12, 14, "they took"),
        (15, 18, "upon them"),
        (19, 22, "the name of Christ,"),
        (23, 26, "and there was"),
        (27, 28, "the determination"),
        (29, 31, "to serve"),
        (32, 34, "him"),
        (35, 39, "unto the end."),
    ],
    4: [
        (0, 4, "And after"),
        (5, 8, "were received they"),
        (9, 11, "unto baptism,"),
        (12, 13, "and wrought upon"),
        (14, 15, "and cleansed"),
        (16, 18, "by the power"),
        (19, 22, "of the Holy Ghost,"),
        (23, 26, "they were numbered"),
        (27, 30, "among the people"),
        (31, 35, "of the church of Christ;"),
        (36, 38, "and were taken"),
        (39, 41, "their names,"),
        (42, 46, "that they be remembered"),
        (47, 48, "and nourished"),
        (49, 52, "by the good word"),
        (53, 55, "of God,"),
        (56, 58, "to keep steadfast"),
        (59, 60, "them"),
        (61, 64, "in the right path,"),
        (65, 67, "to hold fast"),
        (68, 69, "them"),
        (70, 74, "ever watchful"),
        (75, 77, "in prayer,"),
        (78, 80, "relying only"),
        (81, 85, "upon the merits of Christ,"),
        (86, 87, "who is"),
        (88, 90, "the author"),
        (91, 93, "and the finisher"),
        (94, 97, "of their faith."),
    ],
    5: [
        (0, 4, "And did meet together oft"),
        (5, 6, "the church,"),
        (7, 8, "to fast"),
        (9, 10, "and to pray,"),
        (11, 12, "and to converse"),
        (13, 15, "one"),
        (16, 18, "with another,"),
        (19, 20, "concerning"),
        (21, 24, "the welfare"),
        (25, 28, "of their souls."),
    ],
    6: [
        (0, 3, "And they assembled"),
        (4, 5, "oft together"),
        (6, 7, "to partake"),
        (8, 10, "of the bread"),
        (11, 13, "and the wine,"),
        (14, 16, "in remembrance"),
        (17, 21, "of the Lord Jesus."),
    ],
    7: [
        (0, 3, "And they took heed"),
        (4, 6, "with diligence"),
        (7, 11, "that no iniquity be"),
        (12, 15, "among"),
        (16, 17, "them;"),
        (18, 22, "and whoso"),
        (23, 24, "was found"),
        (25, 27, "he had committed"),
        (28, 29, "iniquity,"),
        (30, 33, "and three witnesses"),
        (34, 36, "of the church"),
        (37, 40, "did condemn them"),
        (41, 44, "before the elders,"),
        (45, 46, "and if"),
        (47, 50, "they repented not,"),
        (51, 53, "and confessed not,"),
        (54, 56, "were blotted out"),
        (57, 59, "their names,"),
        (60, 63, "and were not counted"),
        (64, 65, "they"),
        (66, 68, "among"),
        (69, 71, "the people of Christ."),
    ],
    8: [
        (0, 4, "But as often as"),
        (5, 8, "they repented"),
        (9, 12, "and sought forgiveness,"),
        (13, 16, "with true intent,"),
        (17, 18, "were forgiven"),
        (19, 20, "they."),
    ],
    9: [
        (0, 2, "And were conducted"),
        (3, 5, "their meetings"),
        (6, 8, "by the church"),
        (9, 11, "according to"),
        (12, 15, "the workings of the Spirit,"),
        (16, 18, "and the power"),
        (19, 22, "of the Holy Ghost;"),
        (23, 27, "for as they were led"),
        (28, 30, "by the power"),
        (31, 34, "of the Holy Ghost"),
        (35, 36, "whether to preach,"),
        (37, 38, "or to exhort,"),
        (39, 40, "or to pray,"),
        (41, 43, "or to supplicate,"),
        (44, 45, "or to sing,"),
        (46, 50, "even so it was done."),
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
