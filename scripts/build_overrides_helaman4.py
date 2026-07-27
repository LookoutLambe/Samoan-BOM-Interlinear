"""
Hand-curated TAM-phrase gloss overrides for Helamana (Helaman) 4 — the wars of
dissension: Nephite dissenters join the Lamanites, who overrun Zarahemla and half
the land; Moronihah recovers half the lost territory; the people are humbled and
Nephi and Lehi and Moronihah preach repentance. Mormon's reflection that the
Nephites had grown weak because of their wickedness and had cast out the Spirit.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_helaman4.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "helaman"
CHAPTER_NUM = 4

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the fiftieth"),
        (7, 11, "and fourth year,"),
        (12, 14, "there were"),
        (15, 17, "many dissensions"),
        (18, 20, "in the church,"),
        (21, 25, "and there was also"),
        (26, 27, "a contention"),
        (28, 30, "among"),
        (31, 31, "the people,"),
        (32, 34, "insomuch that"),
        (35, 36, "there was"),
        (37, 40, "much bloodshed."),
    ],
    2: [
        (0, 2, "And were slain"),
        (3, 5, "and driven out"),
        (6, 8, "from the land"),
        (9, 11, "the rebellious part,"),
        (12, 16, "and they went"),
        (17, 20, "unto the king of"),
        (21, 22, "the Lamanites."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they tried"),
        (6, 7, "to stir up"),
        (8, 9, "the Lamanites"),
        (10, 12, "to go"),
        (13, 15, "to war against"),
        (16, 18, "the Nephites;"),
        (19, 20, "but behold,"),
        (21, 24, "were exceedingly afraid"),
        (25, 26, "the Lamanites,"),
        (27, 29, "insomuch that"),
        (30, 32, "they would not listen"),
        (33, 35, "to the words of"),
        (36, 38, "those dissenters."),
    ],
    4: [
        (0, 2, "But it came to pass"),
        (3, 6, "in the fiftieth"),
        (7, 11, "and sixth year"),
        (12, 15, "of the reign of"),
        (16, 16, "the judges,"),
        (17, 19, "there were"),
        (20, 22, "dissenters"),
        (23, 28, "who departed"),
        (29, 31, "from the Nephites"),
        (32, 34, "to the Lamanites;"),
        (35, 38, "and they prevailed"),
        (39, 41, "together with others"),
        (42, 44, "in the stirring up of"),
        (45, 47, "them"),
        (48, 50, "to anger against"),
        (51, 53, "the Nephites;"),
        (54, 57, "and they prepared"),
        (58, 62, "all that year"),
        (63, 65, "for war."),
    ],
    5: [
        (0, 4, "And in the fiftieth"),
        (5, 9, "and seventh year"),
        (10, 14, "they came down"),
        (15, 16, "to battle against"),
        (17, 19, "the Nephites,"),
        (20, 23, "and they began"),
        (24, 25, "the work"),
        (26, 29, "that brings"),
        (30, 31, "death;"),
        (32, 32, "yea,"),
        (33, 34, "insomuch that"),
        (35, 38, "in the fiftieth"),
        (39, 43, "and eighth year"),
        (44, 47, "of the reign of"),
        (48, 48, "the judges"),
        (49, 53, "they prospered"),
        (54, 57, "in the gaining of"),
        (58, 60, "the land of"),
        (61, 61, "Zarahemla;"),
        (62, 62, "yea,"),
        (63, 65, "and likewise"),
        (66, 68, "all the lands,"),
        (69, 72, "even unto"),
        (73, 75, "the land which"),
        (76, 79, "was near"),
        (80, 82, "the land of"),
        (83, 83, "Bountiful."),
    ],
    6: [
        (0, 2, "And were driven"),
        (3, 4, "the Nephites"),
        (5, 7, "and the armies of"),
        (8, 8, "Moronihah"),
        (9, 13, "even unto"),
        (14, 16, "the land of"),
        (17, 17, "Bountiful;"),
    ],
    7: [
        (0, 2, "And there"),
        (3, 6, "they fortified"),
        (7, 8, "to resist"),
        (9, 11, "the Lamanites,"),
        (12, 16, "from the west sea,"),
        (17, 20, "even unto"),
        (21, 21, "the east;"),
        (22, 24, "its distance"),
        (25, 27, "was equal to"),
        (28, 30, "a journey of"),
        (31, 34, "a Nephite man"),
        (35, 38, "in a whole day,"),
        (39, 41, "upon"),
        (42, 44, "the line of"),
        (45, 46, "the border"),
        (47, 49, "which they fortified,"),
        (50, 52, "and set"),
        (53, 55, "their armies"),
        (56, 57, "to defend"),
        (58, 63, "their land northward."),
    ],
    8: [
        (0, 2, "And thus"),
        (3, 4, "obtained"),
        (5, 9, "by those dissenters of"),
        (10, 11, "the Nephites,"),
        (12, 15, "with the help of"),
        (16, 19, "a numerous army of"),
        (20, 21, "the Lamanites,"),
        (22, 24, "all the possessions of"),
        (25, 26, "the Nephites"),
        (27, 29, "which was in"),
        (30, 33, "the land southward."),
        (34, 38, "And all this"),
        (39, 40, "was done"),
        (41, 44, "in the fiftieth"),
        (45, 47, "and eighth"),
        (48, 51, "and the fiftieth"),
        (52, 56, "and ninth years"),
        (57, 60, "of the reign of"),
        (61, 61, "the judges."),
    ],
    9: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 7, "sixtieth"),
        (8, 11, "of the reign of"),
        (12, 12, "the judges,"),
        (13, 15, "prevailed"),
        (16, 16, "Moronihah"),
        (17, 19, "with his armies"),
        (20, 24, "in the regaining of"),
        (25, 28, "many parts of"),
        (29, 30, "the land;"),
        (31, 31, "yea,"),
        (32, 36, "they retook"),
        (37, 39, "many cities"),
        (40, 43, "which had fallen"),
        (44, 46, "into the hands of"),
        (47, 48, "the Lamanites."),
    ],
    10: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 10, "sixty and one"),
        (11, 14, "of the reign of"),
        (15, 15, "the judges"),
        (16, 19, "they succeeded"),
        (20, 24, "in regaining"),
        (25, 27, "even to"),
        (28, 30, "the half of"),
        (31, 34, "all their lands."),
    ],
    11: [
        (0, 1, "Now"),
        (2, 6, "this great defeat of"),
        (7, 8, "the Nephites,"),
        (9, 13, "and the great slaughter"),
        (14, 16, "that was"),
        (17, 22, "among them,"),
        (23, 26, "would not have arisen"),
        (27, 30, "were it not for"),
        (31, 33, "their wickedness"),
        (34, 38, "and their abominations"),
        (39, 42, "which were"),
        (43, 48, "among them;"),
        (49, 49, "yea,"),
        (50, 54, "and were also"),
        (55, 56, "those things"),
        (57, 61, "among them"),
        (62, 66, "who claimed"),
        (67, 69, "they belonged"),
        (70, 73, "to the church of"),
        (74, 75, "God."),
    ],
    12: [
        (0, 3, "And came about"),
        (4, 5, "these things"),
        (6, 7, "because of"),
        (8, 10, "the pride of"),
        (11, 13, "their hearts,"),
        (14, 15, "because of"),
        (16, 18, "their riches"),
        (19, 21, "exceeding great,"),
        (22, 22, "yea,"),
        (23, 25, "it came"),
        (26, 27, "because of"),
        (28, 30, "their oppression"),
        (31, 33, "to the poor,"),
        (34, 37, "in the withholding of"),
        (38, 40, "their food"),
        (41, 45, "from the hungry,"),
        (46, 49, "in the withholding of"),
        (50, 52, "their clothing"),
        (53, 58, "from the naked,"),
        (59, 62, "and the smiting of"),
        (63, 64, "the cheeks of"),
        (65, 68, "their humble brethren,"),
        (69, 69, "mocking"),
        (70, 73, "at things sacred,"),
        (74, 75, "and denying"),
        (76, 78, "the spirit of"),
        (79, 80, "prophecy"),
        (81, 82, "and revelation,"),
        (83, 85, "murdering,"),
        (86, 89, "plundering,"),
        (90, 91, "lying,"),
        (92, 92, "stealing,"),
        (93, 93, "committing adultery,"),
        (94, 96, "and rising up"),
        (97, 99, "in great contentions,"),
        (100, 103, "and fleeing away"),
        (104, 107, "into the land of"),
        (108, 108, "Nephi,"),
        (109, 110, "among"),
        (111, 112, "the Lamanites—"),
    ],
    13: [
        (0, 2, "And because of"),
        (3, 7, "this their great wickedness,"),
        (8, 11, "and their boasting"),
        (12, 16, "in their own strength,"),
        (17, 21, "they were left"),
        (22, 23, "to rely"),
        (24, 28, "on their own strength;"),
        (29, 30, "therefore"),
        (31, 35, "they did not prosper,"),
        (36, 39, "but were afflicted"),
        (40, 41, "and smitten,"),
        (42, 43, "and driven"),
        (44, 46, "before"),
        (47, 48, "the Lamanites,"),
        (49, 51, "until"),
        (52, 55, "almost all was taken"),
        (56, 59, "of all their lands."),
    ],
    14: [
        (0, 1, "But behold,"),
        (2, 4, "preached"),
        (5, 6, "Moronihah"),
        (7, 9, "many things"),
        (10, 11, "to the people"),
        (12, 13, "because of"),
        (14, 16, "their iniquity,"),
        (17, 20, "and likewise also"),
        (21, 23, "preached"),
        (24, 27, "Nephi and Lehi,"),
        (28, 32, "who were the sons of"),
        (33, 33, "Helaman,"),
        (34, 36, "many things"),
        (37, 38, "to the people,"),
        (39, 39, "yea,"),
        (40, 44, "and they two prophesied"),
        (45, 47, "many things"),
        (48, 51, "unto them"),
        (52, 53, "concerning"),
        (54, 56, "their iniquities,"),
        (57, 58, "and what"),
        (59, 63, "would come"),
        (64, 67, "unto them"),
        (68, 69, "if"),
        (70, 73, "they did not repent"),
        (74, 76, "of their sins."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they did repent,"),
        (6, 10, "and according to"),
        (11, 13, "their repentance"),
        (14, 16, "so also"),
        (17, 19, "began to"),
        (20, 22, "they prosper."),
    ],
    16: [
        (0, 0, "For"),
        (1, 3, "when saw"),
        (4, 4, "Moronihah"),
        (5, 7, "that they did repent"),
        (8, 10, "he sought"),
        (11, 13, "to lead"),
        (14, 15, "them"),
        (16, 18, "from that place"),
        (19, 21, "to that place,"),
        (22, 25, "and from that city"),
        (26, 28, "to that city,"),
        (29, 31, "even until"),
        (32, 35, "they regained"),
        (36, 38, "the half of"),
        (39, 41, "their property"),
        (42, 45, "and the half of"),
        (46, 49, "all their lands."),
    ],
    17: [
        (0, 2, "And thus"),
        (3, 4, "ended"),
        (5, 8, "the sixtieth"),
        (9, 13, "and first year"),
        (14, 17, "of the reign of"),
        (18, 18, "the judges."),
    ],
    18: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the sixtieth"),
        (7, 11, "and second year"),
        (12, 15, "of the reign of"),
        (16, 16, "the judges,"),
        (17, 22, "Moronihah could not"),
        (23, 24, "again obtain"),
        (25, 27, "any more lands"),
        (28, 30, "over"),
        (31, 32, "the Lamanites."),
    ],
    19: [
        (0, 1, "Therefore"),
        (2, 5, "they gave up"),
        (6, 8, "their plan"),
        (9, 11, "to regain"),
        (12, 16, "the remaining part of"),
        (17, 19, "their lands,"),
        (20, 20, "for"),
        (21, 24, "exceedingly numerous were"),
        (25, 26, "the Lamanites"),
        (27, 30, "it was not possible"),
        (31, 33, "for the Nephites"),
        (34, 36, "to gain again"),
        (37, 38, "power"),
        (39, 43, "over them;"),
        (44, 45, "therefore"),
        (46, 48, "used"),
        (49, 50, "Moronihah"),
        (51, 53, "all his armies"),
        (54, 56, "in the holding of"),
        (57, 58, "those parts"),
        (59, 62, "which he had taken."),
    ],
    20: [
        (0, 3, "And it came to pass that"),
        (4, 6, "were exceedingly afraid"),
        (7, 8, "the Nephites"),
        (9, 10, "because of"),
        (11, 16, "the greatness of the number of"),
        (17, 18, "the Lamanites,"),
        (19, 20, "lest be overpowered"),
        (21, 22, "them,"),
        (23, 26, "and trampled down,"),
        (27, 28, "and slain,"),
        (29, 30, "and destroyed."),
    ],
    21: [
        (0, 0, "Yea,"),
        (1, 3, "began to"),
        (4, 5, "they remember"),
        (6, 7, "the prophecies of"),
        (8, 8, "Alma,"),
        (9, 12, "and also the words of"),
        (13, 13, "Mosiah;"),
        (14, 17, "and they saw"),
        (18, 22, "they had become"),
        (23, 26, "a hard-hearted people,"),
        (27, 31, "and they had disregarded"),
        (32, 33, "the commandments of"),
        (34, 35, "God;"),
    ],
    22: [
        (0, 3, "And they had altered"),
        (4, 7, "and trampled down"),
        (8, 11, "under their feet"),
        (12, 13, "the laws of"),
        (14, 14, "Mosiah,"),
        (15, 18, "or the things"),
        (19, 23, "he was commanded"),
        (24, 26, "by the Lord"),
        (27, 29, "to give"),
        (30, 31, "to the people;"),
        (32, 35, "and they saw"),
        (36, 37, "were corrupted"),
        (38, 40, "their laws,"),
        (41, 46, "and they had become"),
        (47, 48, "a wicked people,"),
        (49, 51, "insomuch that"),
        (52, 53, "they were wicked"),
        (54, 57, "even like"),
        (58, 59, "the Lamanites."),
    ],
    23: [
        (0, 2, "And because of"),
        (3, 5, "their iniquity"),
        (6, 10, "began to diminish"),
        (11, 12, "the church;"),
        (13, 16, "and began to"),
        (17, 19, "they disbelieve"),
        (20, 23, "in the spirit of"),
        (24, 24, "prophecy"),
        (25, 28, "and the spirit of"),
        (29, 29, "revelation;"),
        (30, 34, "and glared boldly"),
        (35, 36, "before"),
        (37, 39, "their eyes"),
        (40, 42, "the judgments of"),
        (43, 43, "God."),
    ],
    24: [
        (0, 3, "And they saw"),
        (4, 6, "that they had become weak,"),
        (7, 9, "like"),
        (10, 12, "their brethren,"),
        (13, 15, "the Lamanites,"),
        (16, 20, "and no longer preserved"),
        (21, 22, "them"),
        (23, 26, "by the Spirit of"),
        (27, 28, "the Lord;"),
        (29, 29, "yea,"),
        (30, 33, "had departed"),
        (34, 37, "from them,"),
        (38, 38, "because"),
        (39, 41, "dwells not"),
        (42, 44, "the Spirit of"),
        (45, 46, "the Lord"),
        (47, 48, "in temples"),
        (49, 51, "unholy—"),
    ],
    25: [
        (0, 1, "Therefore"),
        (2, 6, "no longer preserved"),
        (7, 8, "them"),
        (9, 11, "by God"),
        (12, 15, "by his miraculous power"),
        (16, 18, "and matchless,"),
        (19, 19, "for"),
        (20, 23, "they had fallen"),
        (24, 27, "into a state of"),
        (28, 30, "unbelief"),
        (31, 34, "and awful wickedness;"),
        (35, 38, "and they saw"),
        (39, 44, "were far more numerous"),
        (45, 46, "the Lamanites"),
        (47, 50, "than they,"),
        (51, 53, "and except"),
        (54, 57, "they cleave"),
        (58, 60, "unto the Lord"),
        (61, 63, "their God,"),
        (64, 68, "would be unavoidable"),
        (69, 71, "their destruction."),
    ],
    26: [
        (0, 1, "For behold,"),
        (2, 4, "they saw"),
        (5, 7, "were equal"),
        (8, 10, "the strength of"),
        (11, 12, "the Lamanites"),
        (13, 16, "and their strength,"),
        (17, 20, "even to"),
        (21, 23, "one man"),
        (24, 27, "against another man."),
        (28, 30, "And thus"),
        (31, 34, "they had fallen"),
        (35, 38, "into this great transgression;"),
        (39, 39, "yea,"),
        (40, 41, "thus"),
        (42, 44, "they became weak,"),
        (45, 46, "because of"),
        (47, 49, "their transgressions,"),
        (50, 52, "in the space"),
        (53, 57, "of not many years."),
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
