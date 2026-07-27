"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 63 — the final chapter
of Alma: the deaths of Shiblon, Moroni, and Corianton's departure; the migrations
northward, Hagoth's ships and the lost colony, renewed Lamanite war and Moronihah's
victories, and the record passing to Helaman son of Helaman as the account of Alma
is brought to a close.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_alma63.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 63

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the commencement of"),
        (7, 8, "the year"),
        (9, 13, "thirty and six"),
        (14, 17, "of the reign of"),
        (18, 18, "the judges"),
        (19, 21, "over"),
        (22, 25, "the people of Nephi,"),
        (26, 28, "were placed"),
        (29, 31, "under"),
        (32, 34, "the charge of"),
        (35, 35, "Shiblon"),
        (36, 39, "those sacred things"),
        (40, 42, "which were delivered"),
        (43, 44, "unto Helaman"),
        (45, 46, "by Alma."),
    ],
    2: [
        (0, 2, "And he was"),
        (3, 6, "a righteous man,"),
        (7, 14, "and he walked uprightly"),
        (15, 17, "before"),
        (18, 19, "God;"),
        (20, 23, "and he kept"),
        (24, 27, "to do good"),
        (28, 30, "continually,"),
        (31, 32, "to keep"),
        (33, 34, "the commandments of"),
        (35, 36, "the Lord"),
        (37, 38, "his God;"),
        (39, 42, "and likewise"),
        (43, 44, "his brother."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 5, "died also"),
        (6, 6, "Moroni."),
        (7, 9, "And thus"),
        (10, 11, "ended"),
        (12, 14, "the year"),
        (15, 19, "thirty and six"),
        (20, 23, "of the reign of"),
        (24, 24, "the judges."),
    ],
    4: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 10, "thirty and seven"),
        (11, 14, "of the reign of"),
        (15, 15, "the judges,"),
        (16, 18, "there was"),
        (19, 22, "a large company of"),
        (23, 23, "men,"),
        (24, 28, "reaching the number of"),
        (29, 31, "five thousand"),
        (32, 36, "and four hundred of"),
        (37, 37, "men,"),
        (38, 39, "together with"),
        (40, 42, "their wives"),
        (43, 46, "and their children,"),
        (47, 50, "departed from"),
        (51, 53, "the land of"),
        (54, 54, "Zarahemla"),
        (55, 57, "toward"),
        (58, 60, "the land which"),
        (61, 63, "was northward."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Hagoth,"),
        (6, 7, "he was"),
        (8, 12, "an exceedingly curious man,"),
        (13, 14, "therefore"),
        (15, 20, "he went forth"),
        (21, 24, "and built for himself"),
        (25, 28, "an exceedingly large ship,"),
        (29, 31, "on the borders of"),
        (32, 34, "the land of"),
        (35, 35, "Bountiful,"),
        (36, 38, "by the side of"),
        (39, 41, "the land of"),
        (42, 42, "Desolation,"),
        (43, 45, "and launched it"),
        (46, 50, "into the west sea,"),
        (51, 54, "beside"),
        (55, 58, "the narrow neck of land which"),
        (59, 62, "led into"),
        (63, 66, "the land northward."),
    ],
    6: [
        (0, 1, "And behold,"),
        (2, 4, "there were"),
        (5, 7, "many of"),
        (8, 9, "the Nephites"),
        (10, 12, "who entered"),
        (13, 15, "into"),
        (16, 17, "that ship"),
        (18, 21, "and sailed forth"),
        (22, 25, "with much provisions,"),
        (26, 30, "and also many of"),
        (31, 33, "women and children;"),
        (34, 37, "and their course went"),
        (38, 41, "toward the north."),
        (42, 44, "And thus"),
        (45, 47, "ended"),
        (48, 49, "the year"),
        (50, 54, "thirty and seven."),
    ],
    7: [
        (0, 3, "And in the year"),
        (4, 8, "thirty and eight,"),
        (9, 11, "built"),
        (12, 14, "this man"),
        (15, 17, "other ships."),
        (18, 22, "And returned again"),
        (23, 25, "the first ship,"),
        (26, 29, "and even more"),
        (30, 33, "many people"),
        (34, 38, "entered into it"),
        (39, 40, "within;"),
        (41, 45, "and they also took"),
        (46, 48, "much provisions,"),
        (49, 51, "and sailed again"),
        (52, 54, "toward"),
        (55, 58, "the land northward."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 6, "was never again heard"),
        (7, 8, "a report"),
        (9, 10, "concerning"),
        (11, 14, "them."),
        (15, 18, "And we suppose"),
        (19, 22, "that they were drowned"),
        (23, 26, "in the depths of"),
        (27, 28, "the sea."),
        (29, 32, "And it came to pass that"),
        (33, 36, "there was also"),
        (37, 41, "one other ship"),
        (42, 44, "did sail forth;"),
        (45, 48, "and the place"),
        (49, 52, "it went,"),
        (53, 56, "we know not."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 6, "there were many people"),
        (7, 11, "who went"),
        (12, 16, "into the land northward"),
        (17, 20, "in this year."),
        (21, 23, "And thus"),
        (24, 25, "ended"),
        (26, 28, "the year"),
        (29, 33, "thirty and eight."),
    ],
    10: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 10, "thirty and nine"),
        (11, 14, "of the reign of"),
        (15, 15, "the judges,"),
        (16, 19, "died also"),
        (20, 20, "Shiblon,"),
        (21, 23, "and went"),
        (24, 24, "Corianton"),
        (25, 27, "toward"),
        (28, 31, "the land northward"),
        (32, 34, "in a ship,"),
        (35, 37, "to carry"),
        (38, 38, "food"),
        (39, 40, "unto the people"),
        (41, 45, "who went before"),
        (46, 48, "into that land."),
    ],
    11: [
        (0, 1, "Therefore"),
        (2, 4, "it was necessary"),
        (5, 6, "for Shiblon"),
        (7, 9, "to hand over"),
        (10, 12, "those sacred things,"),
        (13, 17, "before his death,"),
        (18, 20, "upon"),
        (21, 23, "the son of"),
        (24, 24, "Helaman,"),
        (25, 26, "who"),
        (27, 30, "was named Helaman,"),
        (31, 32, "named"),
        (33, 35, "after the name of"),
        (36, 38, "his father."),
    ],
    12: [
        (0, 1, "Now"),
        (2, 2, "behold,"),
        (3, 6, "all those engravings"),
        (7, 9, "which were"),
        (10, 13, "in the keeping of"),
        (14, 14, "Helaman"),
        (15, 16, "were written"),
        (17, 19, "and sent forth"),
        (20, 22, "among"),
        (23, 26, "the children of men"),
        (27, 30, "throughout all the land,"),
        (31, 32, "except"),
        (33, 34, "those parts"),
        (35, 36, "which were commanded"),
        (37, 38, "by Alma"),
        (39, 42, "should not"),
        (43, 44, "be sent forth."),
    ],
    13: [
        (0, 3, "Nevertheless,"),
        (4, 6, "these things"),
        (7, 8, "were commanded"),
        (9, 10, "to be kept"),
        (11, 13, "in holiness,"),
        (14, 17, "and handed down"),
        (18, 21, "from one generation"),
        (22, 25, "to another generation;"),
        (26, 27, "therefore,"),
        (28, 31, "in this year,"),
        (32, 35, "were conferred"),
        (36, 37, "these things"),
        (38, 40, "upon"),
        (41, 41, "Helaman,"),
        (42, 44, "before died"),
        (45, 45, "Shiblon."),
    ],
    14: [
        (0, 2, "And it came to pass"),
        (3, 7, "also in this same year"),
        (8, 10, "there were"),
        (11, 14, "some dissenters"),
        (15, 19, "who went"),
        (20, 22, "unto the Lamanites;"),
        (23, 28, "and were again stirred up"),
        (29, 30, "them"),
        (31, 33, "to anger"),
        (34, 35, "against"),
        (36, 38, "the Nephites."),
    ],
    15: [
        (0, 5, "And in this same year"),
        (6, 7, "the very same"),
        (8, 12, "they came down"),
        (13, 17, "with a numerous army"),
        (18, 22, "to war against"),
        (23, 25, "the people of"),
        (26, 26, "Moronihah,"),
        (27, 30, "or against"),
        (31, 33, "the army of"),
        (34, 34, "Moronihah,"),
        (35, 39, "wherein they were defeated"),
        (40, 44, "and driven back again"),
        (45, 49, "to their own lands,"),
        (50, 52, "and suffering"),
        (53, 56, "great loss."),
    ],
    16: [
        (0, 2, "And thus"),
        (3, 4, "ended"),
        (5, 7, "the year"),
        (8, 12, "thirty and nine"),
        (13, 16, "of the reign of"),
        (17, 17, "the judges"),
        (18, 20, "over"),
        (21, 24, "the people of Nephi."),
    ],
    17: [
        (0, 2, "And thus"),
        (3, 4, "ended"),
        (5, 8, "the account of"),
        (9, 9, "Alma,"),
        (10, 11, "and Helaman"),
        (12, 13, "his son,"),
        (14, 16, "and also Shiblon,"),
        (17, 18, "who was"),
        (19, 21, "his son."),
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
