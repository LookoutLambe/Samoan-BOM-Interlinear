"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 25 — the
Lamanites' anger turns against the Amalekites and Nephite dissenters; the
prophecy of Abinadi and Alma fulfilled in the destruction of the Nephite
dissenters and the seed of the priests of Noah; many more Lamanites are
converted and join the Anti-Nephi-Lehies; the converts keep the law of
Moses, looking forward to Christ.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

    python3 build_overrides_alma25.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 25

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "And behold,"),
        (2, 3, "now"),
        (4, 6, "it came to pass that"),
        (7, 8, "were exceedingly angry"),
        (9, 11, "those Lamanites"),
        (12, 12, "because"),
        (13, 15, "they had slain"),
        (16, 18, "their brethren;"),
        (19, 20, "therefore"),
        (21, 24, "they swore"),
        (25, 28, "vengeance"),
        (29, 33, "upon the Nephites;"),
        (34, 38, "and they no more"),
        (39, 39, "attempted"),
        (40, 41, "to slay"),
        (42, 45, "the people of Anti-Nephi-Lehi"),
        (46, 49, "at that time."),
    ],
    2: [
        (0, 3, "But they took"),
        (4, 6, "their armies"),
        (7, 10, "and went over into"),
        (11, 12, "the borders of"),
        (13, 16, "the land of Zarahemla,"),
        (17, 19, "and fell upon the people"),
        (20, 23, "who were in"),
        (24, 27, "the land of Ammonihah"),
        (28, 31, "and destroyed them."),
    ],
    3: [
        (0, 4, "And after that,"),
        (5, 7, "they fought"),
        (8, 10, "many battles"),
        (11, 13, "with the Nephites,"),
        (14, 17, "wherein were driven"),
        (18, 19, "they"),
        (20, 21, "and slain."),
    ],
    4: [
        (0, 3, "and among"),
        (4, 5, "the Lamanites"),
        (6, 9, "who were slain,"),
        (10, 12, "were almost"),
        (13, 17, "all the seed of Amulon"),
        (18, 20, "and his brethren,"),
        (21, 25, "who were"),
        (26, 28, "the priests of Noah,"),
        (29, 33, "and they were slain"),
        (34, 36, "by the hands of"),
        (37, 38, "the Nephites;"),
    ],
    5: [
        (0, 2, "and those who"),
        (3, 4, "remained,"),
        (5, 9, "having fled into"),
        (10, 13, "the east wilderness,"),
        (14, 17, "and having"),
        (18, 19, "usurped"),
        (20, 24, "the power and authority"),
        (25, 29, "over the Lamanites,"),
        (30, 32, "caused"),
        (33, 34, "that should perish"),
        (35, 39, "many of the Lamanites"),
        (40, 42, "by fire"),
        (43, 47, "because of their belief—"),
    ],
    6: [
        (0, 0, "Now"),
        (1, 4, "the more part of"),
        (5, 6, "them,"),
        (7, 11, "after they had suffered"),
        (12, 16, "because of the great loss"),
        (17, 21, "and the many afflictions,"),
        (22, 25, "began to be stirred up"),
        (26, 30, "in remembrance of the words"),
        (31, 33, "which had been preached"),
        (34, 37, "to them"),
        (38, 42, "by Aaron and his brethren"),
        (43, 46, "in their land;"),
        (47, 48, "therefore"),
        (49, 53, "they began"),
        (54, 55, "to disbelieve"),
        (56, 58, "the traditions of"),
        (59, 61, "their fathers,"),
        (62, 64, "and to believe"),
        (65, 67, "in the Lord,"),
        (68, 70, "and that"),
        (71, 74, "he gave"),
        (75, 77, "great power"),
        (78, 80, "unto the Nephites;"),
        (81, 84, "and thus"),
        (85, 86, "were converted"),
        (87, 91, "many of them"),
        (92, 94, "in the wilderness."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 6, "those rulers"),
        (7, 11, "who were the remnant of"),
        (12, 14, "the children of Amulon,"),
        (15, 17, "caused"),
        (18, 21, "that death be brought"),
        (22, 25, "upon them,"),
        (26, 26, "yea,"),
        (27, 31, "all those who"),
        (32, 33, "believed"),
        (34, 36, "in these things."),
    ],
    8: [
        (0, 1, "Now"),
        (2, 4, "this martyrdom"),
        (5, 7, "caused"),
        (8, 12, "the stirring up to anger"),
        (13, 16, "of many of"),
        (17, 19, "their brethren;"),
        (20, 23, "and there began"),
        (24, 25, "to be"),
        (26, 27, "contentions"),
        (28, 30, "in the wilderness;"),
        (31, 35, "and began to hunt"),
        (36, 38, "the Lamanites"),
        (39, 41, "the seed of Amulon"),
        (42, 44, "and his brethren"),
        (45, 48, "and began to slay"),
        (49, 50, "them;"),
        (51, 55, "and they fled into"),
        (56, 59, "the east wilderness."),
    ],
    9: [
        (0, 1, "And behold"),
        (2, 6, "they are hunted"),
        (7, 9, "by the Lamanites"),
        (10, 13, "at this day."),
        (14, 18, "Thus were fulfilled"),
        (19, 22, "the words of Abinadi,"),
        (23, 27, "which he spake"),
        (28, 30, "concerning"),
        (31, 33, "the seed of the priests"),
        (34, 37, "who caused"),
        (38, 42, "that should come upon him"),
        (43, 44, "death"),
        (45, 47, "by fire."),
    ],
    10: [
        (0, 0, "For"),
        (1, 5, "he said"),
        (6, 9, "unto them:"),
        (10, 12, "That which"),
        (13, 17, "ye shall do"),
        (18, 20, "unto me,"),
        (21, 26, "shall become a type"),
        (27, 27, "of"),
        (28, 28, "things"),
        (29, 33, "which are to come."),
    ],
    11: [
        (0, 2, "And now"),
        (3, 4, "Abinadi"),
        (5, 9, "was the first man who"),
        (10, 14, "suffered death"),
        (15, 17, "by fire"),
        (18, 21, "because of his belief"),
        (22, 24, "in God;"),
        (25, 26, "now"),
        (27, 31, "this is the meaning of"),
        (32, 33, "his word,"),
        (34, 35, "that many"),
        (36, 39, "should suffer"),
        (40, 42, "death"),
        (43, 45, "by fire,"),
        (46, 49, "even as"),
        (50, 53, "he had suffered."),
    ],
    12: [
        (0, 4, "And he said"),
        (5, 8, "unto the priests of Noah,"),
        (9, 12, "that their seed"),
        (13, 18, "should cause that"),
        (19, 19, "should be slain"),
        (20, 23, "many people,"),
        (24, 28, "in the manner like"),
        (29, 33, "as he was slain,"),
        (34, 38, "and should be scattered"),
        (39, 39, "abroad"),
        (40, 41, "they"),
        (42, 43, "and slain,"),
        (44, 47, "even as"),
        (48, 49, "a sheep"),
        (50, 54, "having no shepherd"),
        (55, 58, "is driven and destroyed"),
        (59, 61, "by wild beasts;"),
        (62, 65, "and now behold,"),
        (66, 70, "these words are verified"),
        (71, 71, "for"),
        (72, 75, "they were driven"),
        (76, 78, "by the Lamanites,"),
        (79, 83, "and they were hunted,"),
        (84, 88, "and they were smitten."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 7, "when the Lamanites saw"),
        (8, 13, "that they could not overpower"),
        (14, 15, "the Nephites,"),
        (16, 20, "they returned again"),
        (21, 21, "to"),
        (22, 25, "their own land;"),
        (26, 30, "and many of them"),
        (31, 33, "came over"),
        (34, 36, "to dwell in"),
        (37, 40, "the land of Ishmael"),
        (41, 45, "and the land of Nephi,"),
        (46, 48, "and joined"),
        (49, 51, "themselves"),
        (52, 56, "to the people of God,"),
        (57, 61, "who were the people of"),
        (62, 62, "Anti-Nephi-Lehi."),
    ],
    14: [
        (0, 4, "And they also buried"),
        (5, 9, "their weapons of war,"),
        (10, 14, "even as had done"),
        (15, 18, "their brethren,"),
        (19, 23, "and began to be"),
        (24, 25, "they"),
        (26, 28, "a righteous people;"),
        (29, 33, "and they did walk in"),
        (34, 37, "the ways of the Lord,"),
        (38, 41, "and they did observe"),
        (42, 43, "to keep"),
        (44, 45, "his commandments"),
        (46, 48, "and his statutes."),
    ],
    15: [
        (0, 0, "Yea,"),
        (1, 4, "and they did keep"),
        (5, 8, "the law of Moses;"),
        (9, 14, "for it was meet that they"),
        (15, 16, "should keep still"),
        (17, 21, "the law of Moses,"),
        (22, 22, "for"),
        (23, 27, "it was not all fulfilled."),
        (28, 31, "But notwithstanding"),
        (32, 35, "the law of Moses,"),
        (36, 40, "they did look forward"),
        (41, 45, "to the coming of"),
        (46, 46, "Christ,"),
        (47, 49, "considering"),
        (50, 51, "that"),
        (52, 56, "the law of Moses"),
        (57, 61, "was a type of"),
        (62, 64, "his coming,"),
        (65, 66, "and believing"),
        (67, 70, "that they must"),
        (71, 72, "keep still"),
        (73, 76, "those outward performances"),
        (77, 81, "until the time"),
        (82, 89, "that he should be revealed"),
        (90, 93, "unto them."),
    ],
    16: [
        (0, 1, "Now"),
        (2, 5, "they did not suppose"),
        (6, 10, "that salvation came"),
        (11, 13, "by"),
        (14, 17, "the law of Moses;"),
        (18, 20, "but did serve"),
        (21, 24, "the law of Moses"),
        (25, 27, "to strengthen"),
        (28, 30, "their faith"),
        (31, 32, "in Christ;"),
        (33, 35, "and thus"),
        (36, 39, "they did retain"),
        (40, 41, "a hope"),
        (42, 46, "through faith,"),
        (47, 51, "unto eternal salvation,"),
        (52, 54, "relying upon"),
        (55, 58, "the spirit of prophecy,"),
        (59, 62, "which spake"),
        (63, 66, "of things"),
        (67, 71, "which are to come."),
    ],
    17: [
        (0, 3, "And now behold,"),
        (4, 6, "did rejoice exceedingly"),
        (7, 7, "Ammon,"),
        (8, 9, "and Aaron,"),
        (10, 11, "and Omner,"),
        (12, 13, "and Himni,"),
        (14, 17, "and their brethren,"),
        (18, 21, "for the success which"),
        (22, 24, "they had had"),
        (25, 29, "among the Lamanites,"),
        (30, 32, "seeing"),
        (33, 36, "that had granted"),
        (37, 38, "the Lord"),
        (39, 42, "unto them"),
        (43, 45, "according to"),
        (46, 48, "their prayers,"),
        (49, 54, "and he had also verified"),
        (55, 57, "his word"),
        (58, 61, "unto them"),
        (62, 65, "in every particular."),
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
