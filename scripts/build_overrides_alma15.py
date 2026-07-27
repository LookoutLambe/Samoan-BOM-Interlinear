"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 15 — Alma and
Amulek go to Sidom; Zeezrom healed and baptized; a church established;
Amulek forsaken by his kindred; Alma and Amulek return to Zarahemla.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

    python3 build_overrides_alma15.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 15

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 4, "were commanded"),
        (5, 7, "Alma and Amulek"),
        (8, 10, "to depart"),
        (11, 13, "out of that city;"),
        (14, 16, "and they"),
        (17, 19, "departed,"),
        (20, 22, "and came"),
        (23, 26, "even unto"),
        (27, 30, "the land of Sidom;"),
        (31, 32, "and behold,"),
        (33, 34, "there"),
        (35, 39, "they found"),
        (40, 41, "all the people"),
        (42, 47, "who had departed out of"),
        (48, 51, "the land of Ammonihah,"),
        (52, 56, "who had been cast out"),
        (57, 58, "and stoned"),
        (59, 60, "with stones,"),
        (61, 61, "because"),
        (62, 64, "they believed"),
        (65, 67, "in the words of"),
        (68, 68, "Alma."),
    ],
    2: [
        (0, 0, "And"),
        (1, 4, "they related"),
        (5, 8, "unto them"),
        (9, 10, "all that"),
        (11, 12, "had happened"),
        (13, 15, "unto their wives"),
        (16, 17, "and children,"),
        (18, 21, "and also concerning"),
        (22, 25, "themselves,"),
        (26, 29, "and of"),
        (30, 33, "their power of"),
        (34, 35, "deliverance."),
    ],
    3: [
        (0, 0, "And"),
        (1, 3, "lay"),
        (4, 4, "Zeezrom"),
        (5, 6, "at Sidom"),
        (7, 8, "sick,"),
        (9, 12, "with a burning fever,"),
        (13, 17, "which was caused by"),
        (18, 21, "the great tribulations of"),
        (22, 23, "his mind"),
        (24, 25, "on account of"),
        (26, 28, "his wickedness,"),
        (29, 29, "for"),
        (30, 33, "he supposed"),
        (34, 38, "were no more"),
        (39, 41, "Alma and Amulek;"),
        (42, 42, "and"),
        (43, 46, "he supposed"),
        (47, 48, "had been slain"),
        (49, 50, "they"),
        (51, 52, "because of"),
        (53, 54, "his iniquity."),
        (55, 59, "And this great sin,"),
        (60, 63, "and his many"),
        (64, 66, "other sins,"),
        (67, 69, "did harrow up"),
        (70, 71, "his mind"),
        (72, 74, "until"),
        (75, 78, "it became exceedingly sore,"),
        (79, 83, "having no deliverance;"),
        (84, 85, "therefore"),
        (86, 89, "began to"),
        (90, 92, "he be scorched"),
        (93, 96, "with a burning heat."),
    ],
    4: [
        (0, 1, "Now,"),
        (2, 6, "when he heard"),
        (7, 9, "were"),
        (10, 12, "Alma and Amulek"),
        (13, 17, "in the land of Sidom,"),
        (18, 20, "began to"),
        (21, 21, "take courage"),
        (22, 23, "his heart;"),
        (24, 24, "and"),
        (25, 29, "he sent immediately"),
        (30, 31, "a message"),
        (32, 35, "unto them,"),
        (36, 40, "desiring them"),
        (41, 43, "to come"),
        (44, 46, "unto him."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 7, "went immediately"),
        (8, 9, "they,"),
        (10, 13, "obeying"),
        (14, 15, "the message"),
        (16, 20, "which he had sent"),
        (21, 24, "unto them;"),
        (25, 29, "and they went in"),
        (30, 34, "unto the house"),
        (35, 36, "unto Zeezrom;"),
        (37, 41, "and they found"),
        (42, 43, "him"),
        (44, 48, "upon his bed,"),
        (49, 50, "sick,"),
        (51, 53, "being very low"),
        (54, 57, "with a burning fever;"),
        (58, 58, "and"),
        (59, 62, "also was exceedingly sore"),
        (63, 64, "his mind"),
        (65, 66, "because of"),
        (67, 68, "his iniquities;"),
        (69, 75, "and when he saw"),
        (76, 79, "them,"),
        (80, 83, "he stretched forth"),
        (84, 84, "his"),
        (85, 85, "hand,"),
        (86, 88, "and besought"),
        (89, 92, "them,"),
        (93, 96, "that they would heal"),
        (97, 98, "him."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 5, "said"),
        (6, 6, "Alma"),
        (7, 9, "unto him,"),
        (10, 12, "taking by"),
        (13, 13, "his"),
        (14, 14, "hand:"),
        (15, 18, "Believest thou"),
        (19, 22, "in the power of"),
        (23, 23, "Christ"),
        (24, 26, "unto salvation?"),
    ],
    7: [
        (0, 0, "And"),
        (1, 5, "he answered"),
        (6, 8, "and said:"),
        (9, 9, "Yea,"),
        (10, 12, "I believe"),
        (13, 15, "all the words"),
        (16, 19, "that thou hast taught."),
    ],
    8: [
        (0, 0, "And"),
        (1, 3, "said"),
        (4, 4, "Alma:"),
        (5, 8, "If thou believest"),
        (9, 12, "in the redemption of"),
        (13, 13, "Christ"),
        (14, 16, "canst"),
        (17, 17, "be healed"),
        (18, 18, "thou."),
    ],
    9: [
        (0, 0, "And"),
        (1, 5, "he said:"),
        (6, 6, "Yea,"),
        (7, 9, "I believe"),
        (10, 12, "according to"),
        (13, 14, "thy words."),
    ],
    10: [
        (0, 0, "And"),
        (1, 5, "then cried"),
        (6, 7, "Alma"),
        (8, 10, "unto the Lord,"),
        (11, 13, "saying:"),
        (14, 16, "O Lord,"),
        (17, 19, "our God,"),
        (20, 24, "have mercy"),
        (25, 27, "on this man,"),
        (28, 29, "and heal"),
        (30, 31, "him"),
        (32, 34, "according to"),
        (35, 36, "his faith"),
        (37, 40, "which is in Christ."),
    ],
    11: [
        (0, 4, "And when had finished"),
        (5, 6, "speaking"),
        (7, 8, "Alma"),
        (9, 11, "these words,"),
        (12, 15, "leaped up"),
        (16, 16, "Zeezrom"),
        (17, 19, "upon his feet,"),
        (20, 23, "and began to walk;"),
        (24, 28, "and this was done"),
        (29, 33, "to the great astonishment of"),
        (34, 35, "all the people;"),
        (36, 39, "and went forth"),
        (40, 42, "the report of"),
        (43, 44, "this"),
        (45, 49, "throughout all the land of"),
        (50, 50, "Sidom."),
    ],
    12: [
        (0, 0, "And"),
        (1, 2, "baptized"),
        (3, 3, "Zeezrom"),
        (4, 5, "Alma"),
        (6, 8, "unto the Lord;"),
        (9, 11, "and began"),
        (12, 15, "from that time"),
        (16, 18, "forth"),
        (19, 21, "onward"),
        (22, 25, "to preach"),
        (26, 27, "unto the people."),
    ],
    13: [
        (0, 0, "And"),
        (1, 2, "established"),
        (3, 4, "Alma"),
        (5, 6, "a church"),
        (7, 11, "in the land of Sidom,"),
        (12, 13, "and consecrated"),
        (14, 14, "priests"),
        (15, 16, "and teachers"),
        (17, 19, "in the land,"),
        (20, 21, "to baptize"),
        (22, 24, "unto the Lord"),
        (25, 29, "whosoever"),
        (30, 31, "were desirous"),
        (32, 33, "to be baptized."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 5, "were many"),
        (6, 7, "they;"),
        (8, 8, "for"),
        (9, 12, "they did flock in"),
        (13, 14, "all the region"),
        (15, 17, "round about Sidom,"),
        (18, 18, "and"),
        (19, 20, "were baptized."),
    ],
    15: [
        (0, 0, "But"),
        (1, 2, "as to the people"),
        (3, 6, "that were in"),
        (7, 10, "the land of Ammonihah,"),
        (11, 13, "yet remained"),
        (14, 15, "they"),
        (16, 19, "a hard-hearted people"),
        (20, 22, "and stiffnecked;"),
        (23, 27, "and they repented not"),
        (28, 30, "of their sins,"),
        (31, 33, "ascribing"),
        (34, 37, "all the power of"),
        (38, 40, "Alma and Amulek"),
        (41, 43, "to the devil;"),
        (44, 44, "for"),
        (45, 48, "they were of"),
        (49, 51, "the profession of"),
        (52, 52, "Nehor,"),
        (53, 57, "and did not believe"),
        (58, 60, "in the repentance"),
        (61, 65, "of their sins."),
    ],
    16: [
        (0, 3, "And it came to pass that"),
        (4, 7, "Alma and Amulek,"),
        (8, 11, "having forsaken"),
        (12, 13, "Amulek"),
        (14, 17, "all his gold,"),
        (18, 19, "and silver,"),
        (20, 24, "and his precious things,"),
        (25, 27, "which were in"),
        (28, 31, "the land of Ammonihah,"),
        (32, 35, "for the word of"),
        (36, 37, "God,"),
        (38, 42, "he being rejected"),
        (43, 45, "by them"),
        (46, 50, "who were"),
        (51, 52, "his friends"),
        (53, 56, "and also his father"),
        (57, 59, "and his kindred;"),
    ],
    17: [
        (0, 1, "Therefore,"),
        (2, 6, "after had established"),
        (7, 8, "Alma"),
        (9, 10, "the church"),
        (11, 12, "at Sidom,"),
        (13, 15, "seeing"),
        (16, 18, "a great check,"),
        (19, 19, "yea,"),
        (20, 22, "seeing"),
        (23, 24, "were checked"),
        (25, 25, "the people"),
        (26, 27, "as to"),
        (28, 30, "the pride of"),
        (31, 33, "their hearts,"),
        (34, 36, "and began to"),
        (37, 38, "they humble"),
        (39, 41, "themselves"),
        (42, 44, "before"),
        (45, 46, "God,"),
        (47, 49, "and began to"),
        (50, 52, "they assemble together"),
        (53, 55, "themselves"),
        (56, 59, "at their sanctuaries"),
        (60, 62, "to worship"),
        (63, 64, "God"),
        (65, 67, "before"),
        (68, 69, "the altar,"),
        (70, 70, "watching"),
        (71, 72, "and praying"),
        (73, 75, "continually,"),
        (76, 78, "that might be delivered"),
        (79, 80, "they"),
        (81, 83, "from Satan,"),
        (84, 87, "and from death,"),
        (88, 91, "and from destruction—"),
    ],
    18: [
        (0, 1, "Now"),
        (2, 4, "as"),
        (5, 7, "I said,"),
        (8, 10, "having seen"),
        (11, 11, "Alma"),
        (12, 15, "all these things,"),
        (16, 17, "therefore"),
        (18, 21, "he took"),
        (22, 22, "Amulek"),
        (23, 25, "and came over"),
        (26, 30, "to the land of Zarahemla,"),
        (31, 31, "and"),
        (32, 34, "took"),
        (35, 36, "him"),
        (37, 40, "to his own house,"),
        (41, 42, "and did administer"),
        (43, 45, "unto him"),
        (46, 48, "in his tribulations,"),
        (49, 50, "and strengthened"),
        (51, 52, "him"),
        (53, 56, "in the Lord."),
    ],
    19: [
        (0, 3, "And thus"),
        (4, 4, "ended"),
        (5, 8, "the tenth"),
        (9, 10, "year"),
        (11, 14, "of the reign of"),
        (15, 15, "the judges"),
        (16, 18, "over"),
        (19, 22, "the land of Nephi."),
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
