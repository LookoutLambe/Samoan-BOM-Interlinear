"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 23 — the king
proclaims religious freedom throughout the land; Aaron and his brethren
convert thousands of the Lamanites; the converts take upon them the name
Anti-Nephi-Lehies and never fall away.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

Em-dash token split in the source per rule 11: `latou—ioe,` (v6) — so
v6 = 113 tokens.

    python3 build_overrides_alma23.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 23

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "Behold,"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 8, "was sent by"),
        (9, 13, "the king of the Lamanites"),
        (14, 15, "a proclamation"),
        (16, 18, "among"),
        (19, 21, "all his people,"),
        (22, 26, "that should not lay"),
        (27, 29, "their hands"),
        (30, 31, "on Ammon,"),
        (32, 34, "or Aaron,"),
        (35, 37, "or Omner,"),
        (38, 40, "or Himni,"),
        (41, 45, "nor any of"),
        (46, 48, "their brethren"),
        (49, 53, "who should go forth"),
        (54, 56, "preaching"),
        (57, 61, "the word of God,"),
        (62, 65, "in whatsoever place"),
        (66, 69, "they should be,"),
        (70, 74, "in any part of"),
        (75, 77, "their land."),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 4, "he sent"),
        (5, 6, "a decree"),
        (7, 8, "among"),
        (9, 12, "them,"),
        (13, 17, "that should not lay"),
        (18, 20, "their hands"),
        (21, 24, "on them"),
        (25, 28, "to bind them,"),
        (29, 32, "or cast them"),
        (33, 35, "into prison;"),
        (36, 39, "neither should they spit"),
        (40, 44, "upon them,"),
        (45, 46, "nor smite"),
        (47, 48, "them,"),
        (49, 53, "nor cast them out"),
        (54, 55, "forth"),
        (56, 59, "of their synagogues,"),
        (60, 61, "nor scourge"),
        (62, 65, "them;"),
        (66, 70, "neither should they cast"),
        (71, 72, "at them"),
        (73, 74, "stones,"),
        (75, 80, "but that they should have"),
        (81, 83, "free access"),
        (84, 87, "to enter"),
        (88, 90, "their houses,"),
        (91, 95, "and also their temples,"),
        (96, 100, "and their sanctuaries."),
    ],
    3: [
        (0, 5, "and thus might"),
        (6, 7, "they"),
        (8, 9, "go forth"),
        (10, 12, "and preach"),
        (13, 14, "the word"),
        (15, 18, "according to"),
        (19, 21, "their desires,"),
        (22, 22, "for"),
        (23, 26, "the king had been converted"),
        (27, 29, "unto the Lord,"),
        (30, 33, "and all his household;"),
        (34, 35, "therefore"),
        (36, 40, "he sent"),
        (41, 42, "his proclamation"),
        (43, 46, "throughout the land"),
        (47, 49, "unto his people,"),
        (50, 54, "that there might be no obstruction"),
        (55, 58, "to the word of"),
        (59, 60, "God,"),
        (61, 66, "but that it might go forth"),
        (67, 70, "throughout all the land,"),
        (71, 75, "that might be convinced"),
        (76, 77, "his people"),
        (78, 81, "concerning the wicked traditions of"),
        (82, 84, "their fathers,"),
        (85, 89, "and that might be convinced"),
        (90, 91, "they"),
        (92, 95, "that they all"),
        (96, 97, "were brethren,"),
        (98, 103, "and that they ought not"),
        (104, 105, "to murder,"),
        (106, 107, "nor to plunder,"),
        (108, 109, "nor to steal,"),
        (110, 111, "nor to commit adultery,"),
        (112, 113, "nor to commit"),
        (114, 119, "any manner of wickedness."),
    ],
    4: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 10, "when had sent forth"),
        (11, 13, "the king"),
        (14, 15, "this proclamation,"),
        (16, 18, "that"),
        (19, 24, "Aaron and his brethren went forth"),
        (25, 27, "from city"),
        (28, 30, "to city,"),
        (31, 36, "and from one house of worship"),
        (37, 39, "to another,"),
        (40, 42, "establishing churches,"),
        (43, 47, "and consecrating priests and teachers"),
        (48, 51, "throughout the land"),
        (52, 56, "among the Lamanites,"),
        (57, 61, "to preach and to teach"),
        (62, 66, "the word of God"),
        (67, 71, "among them;"),
        (72, 78, "and thus they began"),
        (79, 79, "to have"),
        (80, 82, "great success."),
    ],
    5: [
        (0, 4, "And thousands"),
        (5, 6, "were brought"),
        (7, 10, "to the knowledge of"),
        (11, 12, "the Lord,"),
        (13, 13, "yea,"),
        (14, 17, "thousands"),
        (18, 19, "were brought"),
        (20, 21, "to believe"),
        (22, 26, "in the traditions of the Nephites;"),
        (27, 31, "and they were taught"),
        (32, 35, "the records and prophecies"),
        (36, 39, "which were handed"),
        (40, 42, "down"),
        (43, 46, "even unto"),
        (47, 50, "the present time."),
    ],
    6: [
        (0, 4, "And as surely"),
        (5, 9, "as the Lord liveth,"),
        (10, 12, "so surely"),
        (13, 17, "as many"),
        (18, 19, "as"),
        (20, 21, "believed,"),
        (22, 26, "or as many"),
        (27, 28, "as"),
        (29, 30, "were brought"),
        (31, 34, "to the knowledge of"),
        (35, 36, "the truth,"),
        (37, 39, "through"),
        (40, 43, "the preaching of Ammon"),
        (44, 46, "and his brethren,"),
        (47, 49, "according to"),
        (50, 53, "the spirit of revelation"),
        (54, 55, "and of prophecy,"),
        (56, 59, "and the working by"),
        (60, 64, "the power of God"),
        (65, 66, "of miracles"),
        (67, 69, "wrought"),
        (70, 73, "in them—"),
        (74, 74, "yea,"),
        (75, 78, "I say"),
        (79, 81, "unto you,"),
        (82, 85, "as liveth"),
        (86, 87, "the Lord,"),
        (88, 91, "as many of"),
        (92, 93, "the Lamanites"),
        (94, 97, "as believed"),
        (98, 101, "in their preaching,"),
        (102, 104, "and were converted"),
        (105, 107, "unto the Lord,"),
        (108, 112, "never did fall away."),
    ],
    7: [
        (0, 0, "For"),
        (1, 4, "they became"),
        (5, 7, "a righteous people;"),
        (8, 12, "they laid down"),
        (13, 14, "the weapons of"),
        (15, 17, "their rebellion,"),
        (18, 22, "they did no more fight"),
        (23, 26, "against God,"),
        (27, 29, "neither against"),
        (30, 33, "any of"),
        (34, 36, "their brethren."),
    ],
    8: [
        (0, 1, "Now,"),
        (2, 5, "these are they"),
        (6, 9, "who were converted"),
        (10, 12, "unto the Lord:"),
    ],
    9: [
        (0, 2, "The people of"),
        (3, 4, "the Lamanites"),
        (5, 8, "who were in"),
        (9, 12, "the land of Ishmael;"),
    ],
    10: [
        (0, 1, "And the people"),
        (2, 4, "of the Lamanites also"),
        (5, 8, "who were in"),
        (9, 12, "the land of Middoni;"),
    ],
    11: [
        (0, 1, "And the people"),
        (2, 4, "of the Lamanites also"),
        (5, 9, "who were"),
        (10, 14, "in the city of Nephi;"),
    ],
    12: [
        (0, 1, "And the people"),
        (2, 4, "of the Lamanites also"),
        (5, 6, "who were in"),
        (7, 10, "the land of Shilom,"),
        (11, 14, "and who were in"),
        (15, 18, "the land of Shemlon,"),
        (19, 20, "and in"),
        (21, 24, "the city of Lemuel,"),
        (25, 26, "and in"),
        (27, 30, "the city of Shimnilom."),
    ],
    13: [
        (0, 4, "And these are the names of"),
        (5, 8, "the cities of the Lamanites"),
        (9, 10, "which were converted"),
        (11, 13, "unto the Lord;"),
        (14, 18, "and these are they"),
        (19, 24, "that laid down"),
        (25, 26, "the weapons of"),
        (27, 29, "their rebellion,"),
        (30, 30, "yea,"),
        (31, 34, "all their weapons"),
        (35, 37, "of war;"),
        (38, 42, "and they all"),
        (43, 45, "were Lamanites."),
    ],
    14: [
        (0, 3, "And the Amalekites"),
        (4, 6, "were not converted,"),
        (7, 8, "save"),
        (9, 11, "only one;"),
        (12, 16, "neither any"),
        (17, 17, "of"),
        (18, 19, "the Amulonites;"),
        (20, 23, "but they did harden"),
        (24, 26, "their hearts,"),
        (27, 30, "and also the hearts of"),
        (31, 32, "the Lamanites"),
        (33, 37, "in that part of"),
        (38, 39, "the land"),
        (40, 43, "wheresoever"),
        (44, 47, "they dwelt,"),
        (48, 48, "yea,"),
        (49, 53, "and all their villages"),
        (54, 58, "and all their cities."),
    ],
    15: [
        (0, 1, "Therefore,"),
        (2, 5, "we have named"),
        (6, 10, "the names of all the cities of"),
        (11, 12, "the Lamanites"),
        (13, 16, "in which they did repent"),
        (17, 19, "and come"),
        (20, 23, "to the knowledge of"),
        (24, 25, "the truth,"),
        (26, 28, "and were converted."),
    ],
    16: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 8, "the king was desirous"),
        (9, 13, "and those who"),
        (14, 15, "were converted"),
        (16, 18, "that there might be"),
        (19, 21, "a name for them,"),
        (22, 25, "that thereby might"),
        (26, 28, "be distinguished"),
        (29, 30, "they"),
        (31, 34, "from their brethren;"),
        (35, 36, "therefore"),
        (37, 41, "the king consulted"),
        (42, 44, "with Aaron"),
        (45, 48, "and many of"),
        (49, 51, "their priests,"),
        (52, 56, "concerning the name"),
        (57, 61, "that they should take"),
        (62, 65, "upon them,"),
        (66, 69, "that thereby might"),
        (70, 72, "be distinguished"),
        (73, 74, "they."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they called"),
        (6, 8, "their names"),
        (9, 10, "Anti-Nephi-Lehies;"),
        (11, 15, "and they were called"),
        (16, 18, "by this name"),
        (19, 23, "and were no more called"),
        (24, 25, "they"),
        (26, 29, "Lamanites."),
    ],
    18: [
        (0, 4, "And began to be"),
        (5, 6, "they"),
        (7, 11, "a very industrious people;"),
        (12, 12, "yea,"),
        (13, 16, "and they were friendly"),
        (17, 20, "with the Nephites;"),
        (21, 22, "therefore,"),
        (23, 26, "they did open"),
        (27, 28, "a correspondence"),
        (29, 31, "with them,"),
        (32, 36, "and did no more follow"),
        (37, 40, "them"),
        (41, 45, "the curse of God."),
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
