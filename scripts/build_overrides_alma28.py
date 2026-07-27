"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 28 — a great
battle between the Lamanites and the Nephites, in which tens of thousands
are slain; the people mourn; a reflection on the state of the dead, the
righteous and the wicked, and the mercy of God through Christ.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

    python3 build_overrides_alma28.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 28

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 9, "after had settled"),
        (10, 14, "the people of Ammon"),
        (15, 19, "in the land of Jershon,"),
        (20, 22, "and also was established"),
        (23, 24, "a church"),
        (25, 29, "in the land of Jershon,"),
        (30, 31, "and were set up"),
        (32, 35, "the armies of the Nephites"),
        (36, 37, "round about"),
        (38, 41, "the land of Jershon,"),
        (42, 42, "yea,"),
        (43, 45, "in all the borders"),
        (46, 47, "round about"),
        (48, 51, "the land of Zarahemla;"),
        (52, 52, "behold"),
        (53, 55, "had followed"),
        (56, 59, "the armies of the Lamanites"),
        (60, 63, "their brethren"),
        (64, 66, "into the wilderness."),
    ],
    2: [
        (0, 3, "And thus"),
        (4, 5, "there was fought"),
        (6, 8, "a battle"),
        (9, 10, "very terrible;"),
        (11, 11, "yea,"),
        (12, 15, "so terrible a battle"),
        (16, 17, "so great"),
        (18, 21, "as never before known"),
        (22, 26, "among all the people"),
        (27, 29, "in the land"),
        (30, 33, "from the time"),
        (34, 37, "when was left Jerusalem"),
        (38, 39, "by Lehi;"),
        (40, 40, "yea,"),
        (41, 46, "and tens of thousands"),
        (47, 47, "of"),
        (48, 49, "the Lamanites"),
        (50, 51, "were slain"),
        (52, 54, "and scattered abroad."),
    ],
    3: [
        (0, 0, "Yea,"),
        (1, 5, "and also there was"),
        (6, 8, "a great slaughter"),
        (9, 11, "among"),
        (12, 15, "the people of Nephi;"),
        (16, 19, "nevertheless,"),
        (20, 23, "were driven and scattered"),
        (24, 25, "the Lamanites,"),
        (26, 29, "and returned again"),
        (30, 32, "the people of Nephi"),
        (33, 36, "to their land."),
    ],
    4: [
        (0, 2, "And now"),
        (3, 6, "this was a time"),
        (7, 9, "wherein there was"),
        (10, 11, "a mourning"),
        (12, 15, "and a great lamentation"),
        (16, 17, "heard"),
        (18, 21, "throughout all the land,"),
        (22, 24, "among"),
        (25, 28, "all the people of Nephi—"),
    ],
    5: [
        (0, 0, "Yea,"),
        (1, 5, "the cry of the women"),
        (6, 10, "whose husbands had died"),
        (11, 13, "in mourning"),
        (14, 17, "for their husbands,"),
        (18, 20, "and also fathers"),
        (21, 23, "in mourning"),
        (24, 27, "for their sons,"),
        (28, 30, "and the daughter"),
        (31, 33, "for the brother,"),
        (34, 34, "yea,"),
        (35, 37, "the brother"),
        (38, 40, "for the father;"),
        (41, 45, "and thus was heard"),
        (46, 49, "the cry of"),
        (50, 51, "mourning"),
        (52, 56, "among them"),
        (57, 57, "all,"),
        (58, 60, "in mourning"),
        (61, 63, "for the people of"),
        (64, 66, "their kindred"),
        (67, 70, "who had been slain."),
    ],
    6: [
        (0, 2, "And now"),
        (3, 4, "surely"),
        (5, 10, "this was a very sorrowful day;"),
        (11, 11, "yea,"),
        (12, 15, "a time of"),
        (16, 18, "solemnity"),
        (19, 23, "and a time of"),
        (24, 26, "much fasting"),
        (27, 29, "and prayer."),
    ],
    7: [
        (0, 4, "And thus endeth"),
        (5, 9, "the fifteenth"),
        (10, 11, "year"),
        (12, 16, "of the reign of the judges"),
        (17, 19, "over"),
        (20, 23, "the people of Nephi;"),
    ],
    8: [
        (0, 4, "And this is the account"),
        (5, 8, "concerning Ammon"),
        (9, 11, "and his brethren,"),
        (12, 15, "their journeyings"),
        (16, 20, "in the land of Nephi,"),
        (21, 23, "their sufferings"),
        (24, 26, "in the land,"),
        (27, 29, "their sorrows,"),
        (30, 33, "and their afflictions,"),
        (34, 37, "and their joy"),
        (38, 39, "unspeakable,"),
        (40, 42, "and the reception"),
        (43, 45, "and safety"),
        (46, 49, "of the brethren"),
        (50, 54, "in the land of Jershon."),
        (55, 57, "And now"),
        (58, 59, "may"),
        (60, 64, "their souls be blessed"),
        (65, 67, "by the Lord,"),
        (68, 72, "the Redeemer of all men,"),
        (73, 74, "forever."),
    ],
    9: [
        (0, 4, "And this is the account"),
        (5, 8, "of the wars and contentions"),
        (9, 13, "among the Nephites,"),
        (14, 16, "and also the wars"),
        (17, 20, "between"),
        (21, 25, "the Nephites and the Lamanites;"),
        (26, 28, "and is ended"),
        (29, 32, "the fifteenth"),
        (33, 34, "year"),
        (35, 39, "of the reign of the judges."),
    ],
    10: [
        (0, 2, "and from"),
        (3, 5, "the first year"),
        (6, 8, "to the year"),
        (9, 11, "fifteenth,"),
        (12, 14, "has brought to pass"),
        (15, 17, "the destruction of"),
        (18, 22, "many thousands of"),
        (23, 23, "lives;"),
        (24, 24, "yea,"),
        (25, 28, "there has come to pass"),
        (29, 32, "an awful scene of"),
        (33, 34, "bloodshed."),
    ],
    11: [
        (0, 3, "And the bodies of"),
        (4, 8, "many thousands of"),
        (9, 9, "people"),
        (10, 12, "are laid low"),
        (13, 15, "in the earth,"),
        (16, 18, "while the bodies of"),
        (19, 22, "many other thousands"),
        (23, 26, "are moldering in heaps"),
        (27, 31, "upon the face of the earth;"),
        (32, 32, "yea,"),
        (33, 37, "and many thousands of"),
        (38, 38, "people"),
        (39, 40, "are mourning"),
        (41, 44, "for the loss of"),
        (45, 46, "the people of"),
        (47, 49, "their kindred"),
        (50, 51, "who were slain,"),
        (52, 52, "because"),
        (53, 57, "there is to them"),
        (58, 59, "a cause"),
        (60, 62, "wherefore to fear"),
        (63, 65, "according to"),
        (66, 69, "the promises of the Lord,"),
        (70, 74, "that they are consigned"),
        (75, 78, "to a state of"),
        (79, 83, "endless wo."),
    ],
    12: [
        (0, 1, "Though"),
        (2, 6, "many thousands of"),
        (7, 9, "other people"),
        (10, 12, "did greatly mourn"),
        (13, 16, "for the loss of"),
        (17, 18, "the people of"),
        (19, 21, "their kindred,"),
        (22, 25, "yet they did rejoice"),
        (26, 27, "and exult"),
        (28, 30, "in the hope,"),
        (31, 35, "and even unto"),
        (36, 38, "their assurance,"),
        (39, 41, "according to"),
        (42, 45, "the promises of the Lord,"),
        (46, 50, "that they are raised up"),
        (51, 56, "to dwell at the right hand"),
        (57, 59, "of God,"),
        (60, 63, "in a state of"),
        (64, 68, "never-ending happiness."),
    ],
    13: [
        (0, 4, "and thus we"),
        (5, 6, "see"),
        (7, 11, "the great inequality"),
        (12, 13, "of man"),
        (14, 17, "because of sin"),
        (18, 20, "and transgression,"),
        (21, 24, "and the power of"),
        (25, 26, "the devil,"),
        (27, 31, "which cometh by"),
        (32, 33, "the cunning plans"),
        (34, 37, "which he hath devised"),
        (38, 40, "to ensnare"),
        (41, 43, "the hearts of men."),
    ],
    14: [
        (0, 4, "and thus we"),
        (5, 6, "see"),
        (7, 11, "the mighty call"),
        (12, 13, "unto men"),
        (14, 17, "to labor diligently"),
        (18, 22, "in the vineyards of the Lord;"),
        (23, 27, "and thus we"),
        (28, 29, "see"),
        (30, 34, "the great cause of"),
        (35, 36, "sorrow,"),
        (37, 41, "and also of joy—"),
        (42, 44, "the sorrow"),
        (45, 48, "because of death"),
        (49, 50, "and destruction"),
        (51, 54, "among men,"),
        (55, 58, "and the joy"),
        (59, 63, "because of the light of"),
        (64, 64, "Christ"),
        (65, 67, "unto life."),
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
