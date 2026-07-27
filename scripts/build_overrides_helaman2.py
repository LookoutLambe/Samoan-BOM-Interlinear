"""
Hand-curated TAM-phrase gloss overrides for Helamana (Helaman) 2 — Helaman son of
Helaman fills the judgment-seat; Gadianton leads the secret band of Kishkumen and
plots his death; but Helaman's servant infiltrates the band, learns their plan,
and slays Kishkumen; Gadianton and his robbers flee into the wilderness. The
origin and warning of the Gadianton band that would work the ruin of the people.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_helaman2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "helaman"
CHAPTER_NUM = 2

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the fortieth"),
        (7, 11, "and second year"),
        (12, 15, "of the reign of"),
        (16, 16, "the judges,"),
        (17, 20, "after had finished"),
        (21, 22, "re-establishing"),
        (23, 24, "by Moronihah"),
        (25, 26, "the peace"),
        (27, 29, "between"),
        (30, 32, "the Nephites"),
        (33, 35, "and the Lamanites,"),
        (36, 36, "behold,"),
        (37, 40, "there was no one"),
        (41, 43, "to sit in"),
        (44, 45, "the judgment-seat;"),
        (46, 47, "therefore"),
        (48, 54, "there began to be again"),
        (55, 57, "a contention"),
        (58, 60, "among"),
        (61, 62, "the people"),
        (63, 65, "concerning"),
        (66, 70, "who should sit"),
        (71, 73, "in the judgment-seat."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Helaman,"),
        (6, 7, "who was"),
        (8, 11, "the son of"),
        (12, 12, "Helaman,"),
        (13, 14, "was appointed"),
        (15, 18, "by the voice of"),
        (19, 20, "the people,"),
        (21, 23, "to sit in"),
        (24, 25, "the judgment-seat."),
    ],
    3: [
        (0, 1, "But behold,"),
        (2, 3, "Kishkumen,"),
        (4, 7, "who slew"),
        (8, 8, "Pahoran,"),
        (9, 11, "lay in wait"),
        (12, 14, "to destroy also"),
        (15, 16, "Helaman;"),
        (17, 21, "and he was supported"),
        (22, 24, "by his band,"),
        (25, 29, "who entered"),
        (30, 32, "into a covenant"),
        (33, 36, "that no one"),
        (37, 39, "should know"),
        (40, 41, "his wickedness."),
    ],
    4: [
        (0, 0, "For"),
        (1, 5, "there was one"),
        (6, 9, "named Gadianton,"),
        (10, 11, "who"),
        (12, 15, "was very skilled"),
        (16, 19, "in many words,"),
        (20, 22, "and likewise"),
        (23, 25, "in his trade,"),
        (26, 30, "which was the doing of"),
        (31, 33, "the secret work"),
        (34, 37, "of murder"),
        (38, 40, "and of robbery;"),
        (41, 42, "therefore"),
        (43, 48, "he became"),
        (49, 50, "the leader of"),
        (51, 53, "the band of"),
        (54, 54, "Kishkumen."),
    ],
    5: [
        (0, 1, "Therefore"),
        (2, 5, "he flattered"),
        (6, 7, "them,"),
        (8, 10, "and also Kishkumen,"),
        (11, 11, "if"),
        (12, 16, "they set him"),
        (17, 19, "in the judgment-seat"),
        (20, 25, "he would give"),
        (26, 29, "unto them"),
        (30, 33, "who joined"),
        (34, 36, "his band"),
        (37, 40, "that they be appointed"),
        (41, 42, "to have"),
        (43, 44, "power"),
        (45, 47, "and authority"),
        (48, 50, "among"),
        (51, 52, "the people;"),
        (53, 54, "therefore"),
        (55, 57, "sought"),
        (58, 58, "Kishkumen"),
        (59, 60, "to slay"),
        (61, 61, "Helaman."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 8, "as he went forth"),
        (9, 9, "toward"),
        (10, 12, "the judgment-seat"),
        (13, 14, "to slay"),
        (15, 15, "Helaman,"),
        (16, 16, "behold,"),
        (17, 20, "one of"),
        (21, 22, "the servants of"),
        (23, 23, "Helaman,"),
        (24, 26, "was out"),
        (27, 29, "in the night,"),
        (30, 33, "and having obtained,"),
        (34, 36, "by means of"),
        (37, 39, "disguise,"),
        (40, 41, "a knowledge"),
        (42, 44, "concerning"),
        (45, 46, "those plans"),
        (47, 48, "which were made"),
        (49, 51, "by this band"),
        (52, 53, "to slay"),
        (54, 54, "Helaman—"),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he met"),
        (7, 8, "with Kishkumen,"),
        (9, 12, "and he gave"),
        (13, 15, "unto him"),
        (16, 17, "a sign;"),
        (18, 19, "therefore"),
        (20, 23, "made known"),
        (24, 25, "Kishkumen"),
        (26, 28, "unto him"),
        (29, 30, "the thing"),
        (31, 36, "which he desired,"),
        (37, 38, "desiring"),
        (39, 42, "that he lead"),
        (43, 44, "him"),
        (45, 47, "to the judgment-seat,"),
        (48, 51, "that he may"),
        (52, 53, "he slay"),
        (54, 54, "Helaman."),
    ],
    8: [
        (0, 3, "And when knew"),
        (4, 7, "the servant of"),
        (8, 8, "Helaman"),
        (9, 10, "all the things"),
        (11, 15, "that were in the heart of"),
        (16, 16, "Kishkumen,"),
        (17, 20, "and his aim"),
        (21, 25, "was to murder,"),
        (26, 31, "and also the aim"),
        (32, 35, "of all of them"),
        (36, 39, "who joined"),
        (40, 42, "his band"),
        (43, 45, "to murder,"),
        (46, 47, "and to rob,"),
        (48, 51, "and to gain power,"),
        (52, 55, "(and this was their"),
        (56, 58, "secret plan,"),
        (59, 62, "and their combination),"),
        (63, 65, "said"),
        (66, 68, "the servant of"),
        (69, 69, "Helaman"),
        (70, 71, "unto Kishkumen:"),
        (72, 75, "Let us go"),
        (76, 78, "to the judgment-seat."),
    ],
    9: [
        (0, 1, "Now"),
        (2, 4, "was greatly pleased"),
        (5, 5, "Kishkumen"),
        (6, 8, "at this,"),
        (9, 9, "for"),
        (10, 13, "he supposed"),
        (14, 18, "he would accomplish"),
        (19, 20, "his plan;"),
        (21, 22, "but behold,"),
        (23, 26, "as they two went"),
        (27, 29, "to the judgment-seat,"),
        (30, 31, "stabbed"),
        (32, 35, "the servant of"),
        (36, 36, "Helaman"),
        (37, 38, "Kishkumen"),
        (39, 41, "even unto"),
        (42, 43, "the heart,"),
        (44, 46, "insomuch that"),
        (47, 49, "he fell"),
        (50, 51, "down"),
        (52, 53, "dead"),
        (54, 56, "without"),
        (57, 58, "a sound."),
        (59, 64, "And he ran"),
        (65, 67, "and told"),
        (68, 69, "Helaman"),
        (70, 71, "all the things"),
        (72, 74, "he saw,"),
        (75, 78, "and heard,"),
        (79, 81, "and done."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 5, "sent"),
        (6, 7, "Helaman"),
        (8, 9, "men"),
        (10, 12, "to seize"),
        (13, 15, "this band of"),
        (16, 17, "robbers"),
        (18, 21, "and secret murderers,"),
        (22, 24, "that be slain"),
        (25, 26, "them"),
        (27, 30, "according to"),
        (31, 32, "the law."),
    ],
    11: [
        (0, 1, "But behold,"),
        (2, 4, "when learned"),
        (5, 6, "Gadianton"),
        (7, 10, "did not return"),
        (11, 11, "Kishkumen"),
        (12, 15, "he was afraid"),
        (16, 19, "lest he be destroyed;"),
        (20, 21, "therefore"),
        (22, 25, "he commanded"),
        (26, 27, "his band"),
        (28, 30, "to follow"),
        (31, 33, "him."),
        (34, 36, "And went"),
        (37, 39, "their flight"),
        (40, 42, "from the land,"),
        (43, 46, "by a secret way,"),
        (47, 49, "into"),
        (50, 51, "the wilderness;"),
        (52, 54, "and thus"),
        (55, 58, "when sent"),
        (59, 60, "Helaman"),
        (61, 62, "men"),
        (63, 64, "to seize"),
        (65, 66, "them,"),
        (67, 71, "could not be found"),
        (72, 73, "them"),
        (74, 76, "anywhere."),
    ],
    12: [
        (0, 5, "And will be told"),
        (6, 8, "more things"),
        (9, 11, "concerning"),
        (12, 13, "this Gadianton"),
        (14, 19, "at a time to come."),
        (20, 22, "And thus"),
        (23, 25, "ended"),
        (26, 29, "the fortieth"),
        (30, 34, "and second year"),
        (35, 38, "of the reign of"),
        (39, 39, "the judges"),
        (40, 43, "over the people of"),
        (44, 44, "Nephi."),
    ],
    13: [
        (0, 1, "And behold,"),
        (2, 5, "at the end of"),
        (6, 7, "this book,"),
        (8, 13, "ye shall see"),
        (14, 16, "that this Gadianton"),
        (17, 19, "caused"),
        (20, 21, "the overthrow,"),
        (22, 22, "yea,"),
        (23, 26, "almost"),
        (27, 29, "the whole destruction"),
        (30, 33, "of the people of"),
        (34, 34, "Nephi."),
    ],
    14: [
        (0, 0, "Behold"),
        (1, 4, "it does not refer"),
        (5, 6, "my account"),
        (7, 10, "to the end of"),
        (11, 13, "the book of"),
        (14, 14, "Helaman,"),
        (15, 19, "but the meaning of"),
        (20, 21, "my account"),
        (22, 25, "the end of"),
        (26, 28, "the book of"),
        (29, 29, "Nephi,"),
        (30, 34, "from which I took"),
        (35, 37, "the whole account"),
        (38, 41, "which I have written."),
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
