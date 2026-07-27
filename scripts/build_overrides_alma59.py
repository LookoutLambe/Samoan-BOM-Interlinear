"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 59 — Moroni rejoices at
Helaman's success and writes to Pahoran for reinforcements; but while he prepares
to move against the Lamanites, the city of Nephihah is attacked and falls, its
people fleeing to Moroni's camp. Moroni is angered at the government, marveling
at their neglect, and mourns the wickedness that has weakened the Nephites.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_alma59.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 59

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "And now"),
        (2, 3, "it came to pass"),
        (4, 6, "in the year"),
        (7, 9, "thirtieth"),
        (10, 13, "of the reign of"),
        (14, 14, "the judges"),
        (15, 17, "over"),
        (18, 21, "the people of Nephi,"),
        (22, 24, "after"),
        (25, 28, "receiving and reading"),
        (29, 30, "by Moroni"),
        (31, 32, "the epistle"),
        (33, 34, "of Helaman,"),
        (35, 39, "he was exceedingly rejoiced"),
        (40, 41, "because of"),
        (42, 43, "the welfare,"),
        (44, 44, "yea,"),
        (45, 48, "the exceeding success"),
        (49, 50, "which was gained"),
        (51, 52, "by Helaman,"),
        (53, 57, "in the regaining of"),
        (58, 59, "those lands"),
        (60, 61, "which were seized."),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 5, "and he made known"),
        (6, 7, "this thing"),
        (8, 11, "unto all his people,"),
        (12, 15, "in all the land"),
        (16, 18, "round about"),
        (19, 22, "in that part"),
        (23, 27, "where he was,"),
        (28, 29, "that"),
        (30, 32, "they also rejoice."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 8, "he quickly sent"),
        (9, 10, "an epistle"),
        (11, 12, "to Pahoran,"),
        (13, 14, "desiring"),
        (15, 19, "that he should"),
        (20, 22, "command"),
        (23, 25, "that be gathered"),
        (26, 27, "men"),
        (28, 29, "to strengthen"),
        (30, 31, "Helaman,"),
        (32, 35, "or the armies of"),
        (36, 36, "Helaman,"),
        (37, 39, "that it be easy"),
        (40, 42, "for him"),
        (43, 44, "to hold"),
        (45, 47, "that part of"),
        (48, 49, "the land"),
        (50, 50, "which"),
        (51, 56, "he was miraculously prospered in"),
        (57, 61, "in the regaining."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 8, "when had sent"),
        (9, 10, "by Moroni"),
        (11, 12, "this epistle"),
        (13, 16, "to the land of"),
        (17, 17, "Zarahemla,"),
        (18, 21, "he began to"),
        (22, 23, "again lay out"),
        (24, 26, "a plan"),
        (27, 30, "that may"),
        (31, 33, "he obtain"),
        (34, 35, "the lands"),
        (36, 38, "and those cities"),
        (39, 40, "remaining"),
        (41, 42, "which were taken"),
        (43, 45, "by the Lamanites"),
        (46, 50, "from them."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 7, "while thus making"),
        (8, 9, "by Moroni"),
        (10, 10, "preparations"),
        (11, 13, "to go"),
        (14, 15, "against"),
        (16, 18, "the Lamanites"),
        (19, 21, "to battle,"),
        (22, 22, "behold,"),
        (23, 25, "the people of"),
        (26, 26, "Nephihah,"),
        (27, 31, "who were gathered together"),
        (32, 35, "from the city of"),
        (36, 36, "Moroni"),
        (37, 40, "and the city of"),
        (41, 41, "Lehi"),
        (42, 45, "and the city of"),
        (46, 46, "Morianton,"),
        (47, 48, "were attacked"),
        (49, 51, "by the Lamanites."),
    ],
    6: [
        (0, 0, "Yea,"),
        (1, 5, "even unto them"),
        (6, 9, "who had been compelled"),
        (10, 12, "to flee"),
        (13, 16, "from the land of"),
        (17, 17, "Manti,"),
        (18, 22, "and from the land of"),
        (23, 24, "round about,"),
        (25, 27, "had come over"),
        (28, 31, "and had joined with"),
        (32, 33, "the Lamanites"),
        (34, 38, "in this part of"),
        (39, 40, "the land."),
    ],
    7: [
        (0, 2, "And because of"),
        (3, 6, "their great number"),
        (7, 8, "so exceeding,"),
        (9, 9, "yea,"),
        (10, 14, "and their gaining of"),
        (15, 16, "the strength"),
        (17, 19, "from that day"),
        (20, 22, "to that day,"),
        (23, 27, "they came forth,"),
        (28, 30, "by"),
        (31, 33, "the command of"),
        (34, 34, "Ammoron,"),
        (35, 37, "against"),
        (38, 39, "the people of"),
        (40, 40, "Nephihah,"),
        (41, 44, "and began to"),
        (45, 46, "they slay"),
        (47, 49, "them"),
        (50, 52, "with a slaughter"),
        (53, 54, "exceedingly great."),
    ],
    8: [
        (0, 4, "And so exceedingly great were"),
        (5, 7, "their armies"),
        (8, 11, "insomuch that were forced"),
        (12, 15, "the remaining people of"),
        (16, 16, "Nephihah"),
        (17, 19, "to flee"),
        (20, 23, "before them;"),
        (24, 29, "and they came even"),
        (30, 32, "and joined together"),
        (33, 36, "with the army of"),
        (37, 37, "Moroni."),
    ],
    9: [
        (0, 2, "And now,"),
        (3, 3, "as"),
        (4, 6, "Moroni supposed"),
        (7, 11, "that there should be"),
        (12, 13, "men"),
        (14, 16, "sent"),
        (17, 20, "to the city of"),
        (21, 21, "Nephihah"),
        (22, 23, "to help"),
        (24, 25, "the people"),
        (26, 27, "to hold"),
        (28, 29, "that city,"),
        (30, 33, "and knowing"),
        (34, 38, "that it was easier"),
        (39, 41, "the holding of"),
        (42, 43, "the city"),
        (44, 47, "from falling"),
        (48, 50, "into the hands of"),
        (51, 52, "the Lamanites"),
        (53, 54, "than"),
        (55, 58, "the retaking of"),
        (59, 60, "the city"),
        (61, 65, "from them,"),
        (66, 69, "he supposed"),
        (70, 73, "would be easy"),
        (74, 76, "they hold"),
        (77, 79, "that city."),
    ],
    10: [
        (0, 1, "Therefore"),
        (2, 5, "he kept"),
        (6, 8, "all his force"),
        (9, 10, "to hold"),
        (11, 12, "those places"),
        (13, 17, "which he had retaken."),
    ],
    11: [
        (0, 2, "And now,"),
        (3, 6, "when Moroni saw"),
        (7, 8, "was seized"),
        (9, 11, "the city of"),
        (12, 12, "Nephihah,"),
        (13, 17, "he was exceedingly sorrowful,"),
        (18, 21, "and began to doubt,"),
        (22, 23, "because of"),
        (24, 26, "the wickedness of"),
        (27, 28, "the people,"),
        (29, 29, "whether"),
        (30, 37, "they would not fall"),
        (38, 40, "into the hands of"),
        (41, 43, "their brethren."),
    ],
    12: [
        (0, 1, "Now"),
        (2, 5, "this same condition"),
        (6, 8, "was"),
        (9, 10, "with his"),
        (11, 13, "all chief captains."),
        (14, 16, "They doubted"),
        (17, 19, "and marveled also"),
        (20, 21, "because of"),
        (22, 24, "the wickedness of"),
        (25, 26, "the people,"),
        (27, 31, "and the cause of"),
        (32, 33, "this thing"),
        (34, 35, "because of"),
        (36, 38, "the victory of"),
        (39, 40, "the Lamanites"),
        (41, 43, "over them."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Moroni was angry"),
        (6, 8, "with the government,"),
        (9, 10, "because of"),
        (11, 14, "their unconcern"),
        (15, 17, "concerning"),
        (18, 19, "the freedom"),
        (20, 23, "of their country."),
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
