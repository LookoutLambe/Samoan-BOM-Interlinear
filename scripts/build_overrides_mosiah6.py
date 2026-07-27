"""Hand-curated TAM-phrase gloss overrides for Mosaea 6 — the record of names, Mosiah made king, and the death of Benjamin.

Follows GLOSSING_RULES.md and the no-injected-words rule: each cell's English
maps only to the Samoan words in that cell's span. TAM clusters atomic (rule 1),
pronouns absorbed only when their token is IN the span (rule 2), NP/PP atoms
split (rule 3), `mai`-as-"from" (rule 7), no anaphoric-`ai` fillers when a
PP/object follows (rule 1), `mafai ona`/`ina ia`/`ina ua` bound (rules 13/15),
vocative `e`/`E …e` folded as "O X" (rule 12), directional "forth" dropped
(rule 12a). No pronoun/TAM word injected into a cell whose span lacks that
token; no content word repeats across adjacent cells (except authentic Samoan
doublings and correlatives).

To rebuild after editing:
    python3 build_overrides_mosiah6.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "mosiah"
CHAPTER_NUM = 6
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "thought"),
        (5, 8, "king Benjamin"),
        (9, 13, "it was expedient,"),
        (14, 17, "after had made an end"),
        (18, 21, "he of speaking"),
        (22, 24, "to the people,"),
        (25, 27, "that should"),
        (28, 29, "he record"),
        (30, 30, "the names"),
        (31, 34, "of all those"),
        (35, 39, "who had entered into a covenant"),
        (40, 42, "with God"),
        (43, 44, "to keep"),
        (45, 47, "his commandments."),
    ],
    2: [
        (0, 2, "And it came to pass"),
        (3, 5, "that there was none"),
        (6, 9, "one soul,"),
        (10, 12, "of them,"),
        (13, 16, "except little children,"),
        (17, 20, "who had not entered a covenant"),
        (21, 23, "and taken"),
        (24, 27, "upon them"),
        (28, 29, "the name"),
        (30, 31, "of Christ."),
    ],
    3: [
        (0, 2, "And again,"),
        (3, 4, "it came to pass"),
        (5, 8, "after had made an end"),
        (9, 9, "of finishing"),
        (10, 14, "king Benjamin"),
        (15, 17, "all these things,"),
        (18, 20, "and had consecrated"),
        (21, 24, "his son Mosiah"),
        (25, 28, "to be a ruler"),
        (29, 31, "and a king"),
        (32, 34, "over his people,"),
        (35, 38, "and had given"),
        (39, 41, "him"),
        (42, 44, "all the charges"),
        (45, 49, "concerning the kingdom,"),
        (50, 53, "and also had appointed"),
        (54, 54, "priests"),
        (55, 58, "to teach the people,"),
        (59, 60, "that"),
        (61, 62, "might"),
        (63, 64, "they hear"),
        (65, 66, "and know"),
        (67, 70, "the commandments of God,"),
        (71, 74, "and to stir them up"),
        (75, 76, "to remember"),
        (77, 78, "the oath"),
        (79, 81, "which they had made,"),
        (82, 86, "he dismissed"),
        (87, 90, "the multitude,"),
        (91, 95, "and they returned,"),
        (96, 98, "every one,"),
        (99, 101, "according to"),
        (102, 104, "their families,"),
        (105, 109, "to their own houses."),
    ],
    4: [
        (0, 4, "And began to reign"),
        (5, 5, "Mosiah"),
        (6, 7, "in the stead"),
        (8, 10, "of his father."),
        (11, 17, "And he began to reign"),
        (18, 21, "in the thirtieth"),
        (22, 24, "of his age,"),
        (25, 29, "making in the whole,"),
        (30, 32, "about"),
        (33, 36, "four hundred"),
        (37, 40, "and seventy"),
        (41, 45, "and six years"),
        (46, 48, "from the time"),
        (49, 52, "when was left Jerusalem"),
        (53, 54, "by Lehi."),
    ],
    5: [
        (0, 2, "And lived"),
        (3, 6, "king Benjamin"),
        (7, 10, "three years"),
        (11, 16, "then he died."),
    ],
    6: [
        (0, 2, "And it came to pass"),
        (3, 4, "that did walk"),
        (5, 8, "king Mosiah"),
        (9, 13, "in the ways of the Lord,"),
        (14, 18, "and did observe"),
        (19, 20, "his judgments"),
        (21, 23, "and his statutes,"),
        (24, 28, "and did keep"),
        (29, 30, "his commandments"),
        (31, 35, "in all things whatsoever"),
        (36, 38, "of all things"),
        (39, 43, "which he commanded"),
        (44, 45, "him."),
    ],
    7: [
        (0, 2, "And did cause"),
        (3, 7, "king Mosiah"),
        (8, 9, "his people"),
        (10, 12, "that they should till"),
        (13, 14, "the earth."),
        (15, 18, "And he also,"),
        (19, 23, "himself did till"),
        (24, 25, "the earth,"),
        (26, 27, "that"),
        (28, 29, "might"),
        (30, 33, "he become not"),
        (34, 36, "a heavy burden"),
        (37, 39, "to his people,"),
        (40, 41, "that"),
        (42, 43, "might"),
        (44, 46, "he do"),
        (47, 49, "according to"),
        (50, 51, "all things"),
        (52, 53, "which had done"),
        (54, 56, "his father."),
        (57, 61, "And there was no contention"),
        (62, 66, "among his people"),
        (67, 67, "all"),
        (68, 70, "for the space"),
        (71, 74, "of three years."),
    ],
}


def build_words(source_words, spec):
    next_expected = 0
    for s, e, _ in spec:
        if s != next_expected: raise ValueError(f"gap at {s} expected {next_expected}")
        if e < s or e >= len(source_words): raise ValueError(f"bad range {s}..{e} src len {len(source_words)}")
        next_expected = e + 1
    if next_expected != len(source_words): raise ValueError(f"spec ends at {next_expected} src has {len(source_words)}")
    out = []
    for s, e, g in spec:
        for i in range(s, e): out.append({"sm": source_words[i]["sm"], "en": "·"})
        out.append({"sm": source_words[e]["sm"], "en": g})
    return out


def main():
    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    book = next(b for b in books["books"] if b["id"] == BOOK_ID)
    chapter = next(c for c in book["chapters"] if c["num"] == CHAPTER_NUM)
    existing = {"version": 1, "verses": {}}
    if OVERRIDES_PATH.exists():
        existing = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    n = 0
    for v in chapter["verses"]:
        spec = VERSE_SPECS.get(v["num"])
        if not spec: continue
        try:
            existing["verses"][f"{BOOK_ID}|{CHAPTER_NUM}|{v['num']}"] = build_words(v["words"], spec)
            n += 1
        except ValueError as exc:
            print(f"v{v['num']}: {exc}", file=sys.stderr); sys.exit(1)
    OVERRIDES_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {n} verse overrides to {OVERRIDES_PATH}")


if __name__ == "__main__":
    main()
