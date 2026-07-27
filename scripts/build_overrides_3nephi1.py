"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 1 — Nephi the son
of Helaman departs and disappears, leaving the records to his son Nephi; the
unbelievers set a day to slay the believers unless the sign of Christ's birth
comes; Nephi prays all day, and the Lord answers that the sign is at hand; that
night there is no darkness, a new star appears, and the prophecies of Samuel are
fulfilled; Christ is born, the people are converted, but Satan sends lyings to
harden hearts, and the Gadianton robbers begin again.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_3nephi1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 1

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 6, "had passed away"),
        (7, 9, "the year"),
        (10, 13, "ninety and first"),
        (14, 21, "and it was six hundred years"),
        (22, 24, "from the time"),
        (25, 29, "that Lehi left"),
        (30, 30, "Jerusalem;"),
        (31, 35, "and it was the year"),
        (36, 40, "that Lachoneus became"),
        (41, 42, "the chief judge"),
        (43, 44, "and governor"),
        (45, 47, "over the land."),
    ],
    2: [
        (0, 2, "And Nephi,"),
        (3, 5, "the son of"),
        (6, 6, "Helaman,"),
        (7, 10, "had departed"),
        (11, 14, "out of the land of"),
        (15, 15, "Zarahemla,"),
        (16, 19, "and gave"),
        (20, 24, "unto his son Nephi,"),
        (25, 29, "his eldest son,"),
        (30, 31, "the charge"),
        (32, 34, "concerning"),
        (35, 36, "the plates of brass,"),
        (37, 40, "and all the records"),
        (41, 42, "which were kept,"),
        (43, 45, "and all things"),
        (46, 50, "which were kept sacred"),
        (51, 57, "from the departing of Lehi"),
        (58, 59, "from Jerusalem."),
    ],
    3: [
        (0, 7, "Therefore he departed"),
        (8, 10, "out of the land,"),
        (11, 14, "and whither"),
        (15, 20, "he went,"),
        (21, 24, "no man"),
        (25, 27, "knoweth it;"),
        (28, 30, "and were kept"),
        (31, 31, "the records"),
        (32, 36, "by his son Nephi"),
        (37, 41, "in his stead,"),
        (42, 42, "yea,"),
        (43, 45, "the record of"),
        (46, 47, "this people."),
    ],
    4: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the beginning of"),
        (7, 9, "the year"),
        (10, 13, "ninety and second,"),
        (14, 14, "behold,"),
        (15, 18, "began to be fulfilled"),
        (19, 21, "more fully"),
        (22, 23, "the prophecies of"),
        (24, 24, "the prophets;"),
        (25, 25, "for"),
        (26, 30, "there began to be"),
        (31, 33, "greater signs"),
        (34, 36, "and greater miracles"),
        (37, 39, "which were shown"),
        (40, 44, "among the people."),
    ],
    5: [
        (0, 5, "But there were some"),
        (6, 12, "who began to say"),
        (13, 16, "the time was past"),
        (17, 20, "for the fulfilling of"),
        (21, 21, "the words,"),
        (22, 26, "which were spoken"),
        (27, 27, "Samuel,"),
        (28, 30, "the Lamanite."),
    ],
    6: [
        (0, 3, "And began to"),
        (4, 5, "they rejoice"),
        (6, 9, "over their brethren,"),
        (10, 11, "saying:"),
        (12, 12, "Behold"),
        (13, 15, "is past"),
        (16, 17, "the time,"),
        (18, 21, "and are not fulfilled"),
        (22, 23, "the words of"),
        (24, 24, "Samuel;"),
        (25, 26, "therefore,"),
        (27, 29, "hath been vain"),
        (30, 32, "your joy"),
        (33, 36, "and your faith"),
        (37, 39, "concerning this thing."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they made"),
        (6, 8, "a great uproar"),
        (9, 12, "throughout all the land;"),
        (13, 15, "and the people"),
        (16, 19, "who believed"),
        (20, 24, "began to be very sorrowful,"),
        (25, 29, "lest in any way"),
        (30, 34, "perhaps not come to pass"),
        (35, 36, "those things"),
        (37, 38, "which were spoken."),
    ],
    8: [
        (0, 1, "But behold,"),
        (2, 8, "they watched steadfastly"),
        (9, 11, "for that day"),
        (12, 14, "and that night"),
        (15, 17, "and that day"),
        (18, 22, "which should be"),
        (23, 29, "as one day"),
        (30, 35, "as if there were no night,"),
        (36, 40, "that they might know"),
        (41, 43, "was not vain"),
        (44, 46, "their faith."),
    ],
    9: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 9, "there was a day"),
        (10, 11, "set apart"),
        (12, 16, "by the unbelievers,"),
        (17, 19, "that be slain"),
        (20, 22, "all them"),
        (23, 26, "who believed"),
        (27, 29, "in those traditions,"),
        (30, 31, "except"),
        (32, 33, "came to pass"),
        (34, 35, "the sign"),
        (36, 39, "which was given"),
        (40, 43, "by Samuel the prophet."),
    ],
    10: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 8, "when Nephi saw,"),
        (9, 12, "the son of Nephi,"),
        (13, 16, "this wickedness of"),
        (17, 18, "his people,"),
        (19, 22, "was exceedingly sorrowful"),
        (23, 24, "his heart."),
    ],
    11: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he went out"),
        (8, 13, "and bowed himself down"),
        (14, 18, "upon the earth,"),
        (19, 22, "and cried mightily"),
        (23, 25, "to his God"),
        (26, 28, "in behalf of his people,"),
        (29, 29, "yea,"),
        (30, 33, "those"),
        (34, 39, "who were about to be destroyed"),
        (40, 41, "because of"),
        (42, 44, "their faith"),
        (45, 47, "in the tradition of"),
        (48, 50, "their fathers."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 8, "he cried mightily"),
        (9, 11, "unto the Lord"),
        (12, 15, "all that day;"),
        (16, 17, "and behold,"),
        (18, 20, "came"),
        (21, 23, "the voice of"),
        (24, 25, "the Lord"),
        (26, 28, "unto him,"),
        (29, 31, "saying:"),
    ],
    13: [
        (0, 2, "Lift up"),
        (3, 4, "your head"),
        (5, 7, "and rejoice;"),
        (8, 9, "for behold,"),
        (10, 13, "is at hand"),
        (14, 15, "the time,"),
        (16, 20, "and on this night"),
        (21, 26, "shall be given"),
        (27, 28, "the sign,"),
        (29, 31, "and on the morrow"),
        (32, 36, "I go forth"),
        (37, 39, "into the world,"),
        (40, 43, "to show"),
        (44, 46, "unto the world"),
        (47, 51, "I will fulfil"),
        (52, 54, "all things"),
        (55, 57, "which I caused"),
        (58, 59, "to be spoken"),
        (60, 62, "by the mouth of"),
        (63, 65, "my holy prophets."),
    ],
    14: [
        (0, 0, "Behold,"),
        (1, 4, "I come"),
        (5, 7, "unto my own,"),
        (8, 9, "to fulfil"),
        (10, 12, "all things"),
        (13, 16, "which I made known"),
        (17, 21, "unto the children of men"),
        (22, 24, "from the foundation of"),
        (25, 27, "the world,"),
        (28, 33, "and to do all the will of"),
        (34, 35, "the Father"),
        (36, 38, "and the Son—"),
        (39, 41, "of the Father"),
        (42, 44, "because of me,"),
        (45, 48, "and of the Son"),
        (49, 50, "because of"),
        (51, 52, "my flesh."),
        (53, 54, "And behold,"),
        (55, 58, "is at hand"),
        (59, 60, "the time,"),
        (61, 65, "and this night"),
        (66, 71, "shall be given"),
        (72, 73, "the sign."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 4, "were fulfilled"),
        (5, 6, "the words"),
        (7, 9, "which came"),
        (10, 11, "unto Nephi,"),
        (12, 18, "even as they were spoken;"),
        (19, 20, "for behold,"),
        (21, 27, "at the going down of"),
        (28, 29, "the sun,"),
        (30, 33, "there was no darkness;"),
        (34, 38, "and began to be astonished"),
        (39, 40, "the people"),
        (41, 45, "because there was no darkness"),
        (46, 50, "when the night came."),
    ],
    16: [
        (0, 5, "And there were many,"),
        (6, 10, "who believed not"),
        (11, 14, "in the words of the prophets,"),
        (15, 17, "who fell down"),
        (18, 20, "to the earth"),
        (21, 26, "and became as if dead,"),
        (27, 27, "for"),
        (28, 30, "they knew"),
        (31, 32, "was frustrated"),
        (33, 36, "the great plan of"),
        (37, 38, "destruction"),
        (39, 42, "which they had laid"),
        (43, 45, "for those"),
        (46, 49, "who believed"),
        (50, 53, "in the words of the prophets;"),
        (54, 54, "for"),
        (55, 58, "was already at hand"),
        (59, 61, "the sign"),
        (62, 64, "which was given."),
    ],
    17: [
        (0, 3, "And began to"),
        (4, 5, "they know,"),
        (6, 10, "must shortly come"),
        (11, 13, "the Son of"),
        (14, 15, "God;"),
        (16, 16, "yea,"),
        (17, 19, "in summary,"),
        (20, 22, "all the people"),
        (23, 29, "upon the whole earth"),
        (30, 33, "from west to east,"),
        (34, 39, "in all the land north"),
        (40, 44, "and the land south,"),
        (45, 48, "were exceedingly astonished"),
        (49, 55, "so that they fell down"),
        (56, 58, "to the earth."),
    ],
    18: [
        (0, 0, "For"),
        (1, 3, "they knew"),
        (4, 7, "the prophets testified"),
        (8, 12, "concerning these things"),
        (13, 16, "for many years,"),
        (17, 21, "and was already at hand"),
        (22, 24, "the sign"),
        (25, 27, "which was given;"),
        (28, 31, "and began to"),
        (32, 33, "they fear"),
        (34, 35, "because of"),
        (36, 38, "their iniquity"),
        (39, 43, "and their unbelief."),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 7, "there was no darkness"),
        (8, 11, "in all that night,"),
        (12, 14, "but it was light"),
        (15, 19, "as if it were midday."),
        (20, 23, "And it came to pass that"),
        (24, 26, "rose again"),
        (27, 28, "the sun"),
        (29, 31, "in the morning,"),
        (32, 34, "according to"),
        (35, 39, "its proper order;"),
        (40, 43, "and they knew"),
        (44, 47, "it was the day"),
        (48, 53, "would be born"),
        (54, 55, "the Lord,"),
        (56, 57, "because of"),
        (58, 60, "the sign"),
        (61, 63, "which was given."),
    ],
    20: [
        (0, 2, "And it was fulfilled,"),
        (3, 3, "yea,"),
        (4, 6, "all things,"),
        (7, 10, "every detail,"),
        (11, 13, "according to"),
        (14, 16, "the words of the prophets."),
    ],
    21: [
        (0, 4, "And it came to pass also that"),
        (5, 6, "appeared"),
        (7, 9, "a new star,"),
        (10, 12, "according to"),
        (13, 14, "his word."),
    ],
    22: [
        (0, 3, "And it came to pass that"),
        (4, 9, "beginning from this time"),
        (10, 15, "and going onward"),
        (16, 18, "were sent forth"),
        (19, 20, "lyings,"),
        (21, 22, "by Satan,"),
        (23, 24, "among the people,"),
        (25, 27, "to harden"),
        (28, 30, "their hearts,"),
        (31, 33, "to the intent"),
        (34, 38, "that they not believe"),
        (39, 43, "in the signs and wonders"),
        (44, 49, "which they saw;"),
        (50, 50, "but"),
        (51, 52, "notwithstanding"),
        (53, 55, "these lyings"),
        (56, 57, "and deceivings,"),
        (58, 59, "believed"),
        (60, 64, "the greater part of the people,"),
        (65, 69, "and were converted they"),
        (70, 72, "unto the Lord."),
    ],
    23: [
        (0, 3, "And it came to pass that"),
        (4, 5, "went forth"),
        (6, 6, "Nephi,"),
        (7, 11, "and also many others,"),
        (12, 13, "among the people,"),
        (14, 16, "baptizing"),
        (17, 19, "unto repentance,"),
        (20, 24, "in which came"),
        (25, 27, "a great remission of"),
        (28, 29, "sins."),
        (30, 35, "And thus began"),
        (36, 40, "the people again to have"),
        (41, 42, "peace"),
        (43, 45, "in the land."),
    ],
    24: [
        (0, 4, "And there were not"),
        (5, 6, "any contentions,"),
        (7, 8, "except"),
        (9, 12, "a few of them"),
        (13, 18, "who began to preach,"),
        (19, 20, "endeavoring"),
        (21, 23, "to prove"),
        (24, 27, "by the scriptures"),
        (28, 33, "it was no more needful to keep"),
        (34, 38, "the law of Moses."),
        (39, 40, "Now,"),
        (41, 44, "they erred"),
        (45, 47, "in this thing,"),
        (48, 48, "for"),
        (49, 52, "they understood not"),
        (53, 55, "the scriptures."),
    ],
    25: [
        (0, 3, "But it came to pass that"),
        (4, 7, "it was not long before"),
        (8, 10, "they were converted,"),
        (11, 12, "and believed"),
        (13, 16, "in the error"),
        (17, 20, "they were in,"),
        (21, 21, "for"),
        (22, 24, "was made known"),
        (25, 28, "unto them"),
        (29, 33, "was not yet fulfilled"),
        (34, 35, "the law,"),
        (36, 41, "and must be fulfilled"),
        (42, 44, "in every detail;"),
        (45, 45, "yea,"),
        (46, 48, "came"),
        (49, 52, "unto them"),
        (53, 54, "the word"),
        (55, 59, "that it must be fulfilled;"),
        (60, 60, "yea,"),
        (61, 64, "shall not pass away"),
        (65, 66, "one jot"),
        (67, 70, "or a letter"),
        (71, 73, "until all be fulfilled;"),
        (74, 75, "therefore,"),
        (76, 79, "in this same year"),
        (80, 84, "were they brought"),
        (85, 88, "to the knowledge of"),
        (89, 91, "their error"),
        (92, 96, "and they confessed"),
        (97, 99, "their faults."),
    ],
    26: [
        (0, 5, "And thus passed away"),
        (6, 9, "the year"),
        (10, 13, "ninety and second,"),
        (14, 18, "bringing glad tidings"),
        (19, 20, "unto the people"),
        (21, 22, "because of"),
        (23, 24, "the signs"),
        (25, 26, "which were fulfilled"),
        (27, 29, "according to"),
        (30, 33, "the words of the prophecy of"),
        (34, 36, "all the holy prophets."),
    ],
    27: [
        (0, 3, "And it came to pass that"),
        (4, 6, "also passed away"),
        (7, 9, "the year"),
        (10, 13, "ninety and third"),
        (14, 16, "in peace,"),
        (17, 18, "except"),
        (19, 22, "the robbers of"),
        (23, 23, "Gadianton,"),
        (24, 27, "who dwelt"),
        (28, 31, "upon the mountains,"),
        (32, 36, "who infested"),
        (37, 38, "the land;"),
        (39, 39, "for"),
        (40, 43, "were exceedingly strong"),
        (44, 46, "their strongholds"),
        (47, 51, "and their secret places"),
        (52, 59, "the people could not"),
        (60, 62, "overpower them;"),
        (63, 64, "therefore"),
        (65, 68, "they slew"),
        (69, 71, "many people,"),
        (72, 76, "and made much slaughter"),
        (77, 80, "among the people."),
    ],
    28: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the year"),
        (7, 10, "ninety and fourth,"),
        (11, 14, "began to increase"),
        (15, 17, "they"),
        (18, 21, "in a great degree,"),
        (22, 22, "because"),
        (23, 28, "there were many"),
        (29, 33, "dissenters of the Nephites"),
        (34, 38, "who fled"),
        (39, 42, "unto them,"),
        (43, 48, "which caused"),
        (49, 51, "great sorrow"),
        (52, 57, "unto those Nephites"),
        (58, 62, "who still remained"),
        (63, 65, "in the land."),
    ],
    29: [
        (0, 4, "And there was also"),
        (5, 6, "a cause"),
        (7, 10, "of much sorrow"),
        (11, 13, "to the Lamanite people;"),
        (14, 15, "for behold,"),
        (16, 21, "there were many of"),
        (22, 24, "their children"),
        (25, 27, "who grew up"),
        (28, 32, "and grew strong in years,"),
        (33, 39, "they acted for themselves,"),
        (40, 43, "and were led away"),
        (44, 49, "by some Zoramites,"),
        (50, 52, "by their lyings"),
        (53, 57, "and their flattering words,"),
        (58, 59, "to join"),
        (60, 64, "the robbers of"),
        (65, 65, "Gadianton."),
    ],
    30: [
        (0, 4, "And thus also"),
        (5, 5, "were afflicted"),
        (6, 7, "the Lamanites,"),
        (8, 12, "and began to diminish"),
        (13, 16, "in their faith"),
        (17, 20, "and their righteousness,"),
        (21, 22, "because of"),
        (23, 25, "the wickedness of"),
        (26, 29, "the rising generation."),
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
