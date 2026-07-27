"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 8 — the sign of
Christ's death: in the thirty-fourth year a great tempest, earthquakes, whirlwinds,
fire, and upheaval destroy cities and multitudes across the land; Zarahemla burns,
Moroni sinks into the sea, Moronihah is buried under a mountain, and after three
hours of destruction a thick darkness covers the whole land for three days, so
that no light can be kindled, and the people mourn and howl for their dead.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits applied to bom_books.json before glossing:
    8:1   talafaamaumau—ona  ->  talafaamaumau—  +  ona
    8:19  eleele—aua         ->  eleele—         +  aua
    8:19  itula—ma           ->  itula—          +  ma

    python3 build_overrides_3nephi8.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 8

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "And now"),
        (2, 4, "it came to pass"),
        (5, 6, "according to"),
        (7, 9, "our record,"),
        (10, 13, "and we know"),
        (14, 15, "is true"),
        (16, 18, "our record,"),
        (19, 20, "for behold,"),
        (21, 24, "it was a righteous man"),
        (25, 28, "who kept the record—"),
        (29, 29, "for"),
        (30, 34, "he truly did"),
        (35, 37, "many miracles"),
        (38, 42, "in the name of Jesus;"),
        (43, 47, "and there was no man"),
        (48, 52, "who could do"),
        (53, 55, "a miracle"),
        (56, 60, "in the name of Jesus"),
        (61, 62, "except"),
        (63, 66, "he was cleansed"),
        (67, 70, "in all things"),
        (71, 73, "from his iniquity—"),
    ],
    2: [
        (0, 2, "And now"),
        (3, 5, "it came to pass"),
        (6, 10, "if there was no error"),
        (11, 15, "made by this man"),
        (16, 19, "in the reckoning of"),
        (20, 22, "our time,"),
        (23, 26, "there has now passed away"),
        (27, 31, "thirty-three"),
        (32, 33, "years;"),
    ],
    3: [
        (0, 6, "And the people began to watch"),
        (7, 10, "with great eagerness"),
        (11, 14, "for the sign which"),
        (15, 22, "was given by the prophet Samuel,"),
        (23, 25, "the Lamanite,"),
        (26, 26, "yea,"),
        (27, 30, "for the time when"),
        (31, 38, "the darkness should come"),
        (39, 42, "for three days"),
        (43, 47, "over the land."),
    ],
    4: [
        (0, 5, "And there began to be"),
        (6, 10, "great doubts and disputes"),
        (11, 14, "among the people,"),
        (15, 17, "notwithstanding"),
        (18, 22, "the many signs"),
        (23, 27, "that had been given."),
    ],
    5: [
        (0, 2, "And it came to pass"),
        (3, 8, "in the thirty-fourth"),
        (9, 10, "year,"),
        (11, 14, "in the first month,"),
        (15, 19, "on the fourth day"),
        (20, 22, "of the month,"),
        (23, 26, "there fell"),
        (27, 29, "a great storm,"),
        (30, 32, "of a kind"),
        (33, 37, "never known before"),
        (38, 41, "in all the land."),
    ],
    6: [
        (0, 4, "And there was also"),
        (5, 10, "a great and terrible wind"),
        (11, 13, "that arose;"),
        (14, 17, "and there was"),
        (18, 20, "terrible thunder,"),
        (21, 23, "insomuch that"),
        (24, 28, "it shook the whole earth"),
        (29, 30, "as if"),
        (31, 33, "it would split apart."),
    ],
    7: [
        (0, 3, "And there were"),
        (4, 6, "great flashing lightnings,"),
        (7, 9, "of a kind"),
        (10, 14, "never known before"),
        (15, 18, "in all the land."),
    ],
    8: [
        (0, 2, "And burned"),
        (3, 6, "the city of Zarahemla."),
    ],
    9: [
        (0, 2, "And sank"),
        (3, 6, "the city of Moroni"),
        (7, 14, "into the depths of the sea,"),
        (15, 18, "and were drowned"),
        (19, 22, "those who dwelt there."),
    ],
    10: [
        (0, 5, "And the earth was heaped up"),
        (6, 10, "upon the city of Moronihah,"),
        (11, 14, "insomuch that became"),
        (15, 21, "the place where the city was"),
        (22, 24, "a great mountain."),
    ],
    11: [
        (0, 3, "And there was"),
        (4, 6, "a great destruction"),
        (7, 11, "in the land southward."),
    ],
    12: [
        (0, 1, "But behold,"),
        (2, 4, "there was"),
        (5, 11, "a greater and more terrible destruction"),
        (12, 16, "in the land northward;"),
        (17, 18, "for behold,"),
        (19, 22, "the face was changed of"),
        (23, 25, "the whole land,"),
        (26, 27, "because of"),
        (28, 31, "the wind and whirlwinds,"),
        (32, 35, "and thunder and lightning,"),
        (36, 41, "and the exceedingly great shaking of"),
        (42, 44, "the whole land;"),
    ],
    13: [
        (0, 2, "And were broken up"),
        (3, 3, "the highways,"),
        (4, 5, "and were ruined"),
        (6, 7, "the level roads,"),
        (8, 10, "and were made rough"),
        (11, 15, "many level places."),
    ],
    14: [
        (0, 6, "And many great and notable cities"),
        (7, 8, "were sunk,"),
        (9, 13, "and many were burned,"),
        (14, 18, "and many were shaken"),
        (19, 23, "until fell down"),
        (24, 26, "their buildings"),
        (27, 29, "to the earth,"),
        (30, 32, "and were slain"),
        (33, 36, "those who dwelt there,"),
        (37, 40, "and the places were left desolate."),
    ],
    15: [
        (0, 7, "And there were some cities"),
        (8, 10, "which still stood;"),
        (11, 16, "but exceedingly great was"),
        (17, 19, "their damage,"),
        (20, 22, "and there were many"),
        (23, 29, "who were in those cities"),
        (30, 31, "who were slain."),
    ],
    16: [
        (0, 5, "And there were some"),
        (6, 10, "who were carried away"),
        (11, 13, "in the whirlwind;"),
        (14, 17, "and to where"),
        (18, 23, "they went,"),
        (24, 27, "there is no man"),
        (28, 30, "who knows it,"),
        (31, 34, "only the thing"),
        (35, 37, "they know"),
        (38, 42, "is that they were carried away."),
    ],
    17: [
        (0, 4, "And thus was changed"),
        (5, 10, "the face of the whole earth,"),
        (11, 13, "because of the winds,"),
        (14, 15, "and the thunderings,"),
        (16, 17, "and the lightnings,"),
        (18, 23, "and the quaking of the earth."),
    ],
    18: [
        (0, 1, "And behold,"),
        (2, 4, "the rocks were split;"),
        (5, 6, "they were shattered"),
        (7, 12, "upon the whole earth,"),
        (13, 16, "insomuch that were found"),
        (17, 20, "in broken pieces of rock,"),
        (21, 23, "and in seams"),
        (24, 25, "and cracks,"),
        (26, 31, "upon all the land."),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 6, "the thunderings ceased,"),
        (7, 8, "and lightnings,"),
        (9, 11, "and the rain,"),
        (12, 14, "and the wind,"),
        (15, 20, "and the quaking of the earth—"),
        (21, 22, "for behold,"),
        (23, 27, "these things happened"),
        (28, 33, "for about the space"),
        (34, 36, "of three hours;"),
        (37, 42, "and some said"),
        (43, 47, "the time was greater"),
        (48, 50, "than that;"),
        (51, 54, "nevertheless,"),
        (55, 60, "these great and terrible things"),
        (61, 62, "were done"),
        (63, 67, "in about the space"),
        (68, 70, "of three hours—"),
        (71, 74, "and behold also,"),
        (75, 78, "there came a darkness"),
        (79, 85, "upon all the land."),
    ],
    20: [
        (0, 5, "And there was"),
        (6, 8, "a thick darkness"),
        (9, 14, "upon all the land,"),
        (15, 19, "insomuch that could"),
        (20, 24, "the inhabitants"),
        (25, 29, "who had not fallen"),
        (30, 31, "feel"),
        (32, 36, "the vapor of darkness;"),
    ],
    21: [
        (0, 6, "And there could not be"),
        (7, 9, "any light,"),
        (10, 13, "because of the darkness,"),
        (14, 18, "nor candles,"),
        (19, 22, "nor torches;"),
        (23, 28, "neither could be kindled"),
        (29, 31, "a fire"),
        (32, 36, "with their very fine wood"),
        (37, 39, "and dry,"),
        (40, 46, "so that there could not be at all"),
        (47, 50, "any light;"),
    ],
    22: [
        (0, 4, "And there was no light"),
        (5, 6, "seen,"),
        (7, 10, "nor fire,"),
        (11, 14, "nor any glimmer,"),
        (15, 18, "nor the sun,"),
        (19, 22, "nor the moon,"),
        (23, 25, "nor the stars,"),
        (26, 27, "because of"),
        (28, 34, "the exceeding greatness of the darkness which"),
        (35, 37, "was"),
        (38, 42, "upon the land."),
    ],
    23: [
        (0, 6, "And it continued"),
        (7, 8, "this darkness"),
        (9, 14, "for the space of three days"),
        (15, 19, "and there was no light"),
        (20, 21, "seen;"),
        (22, 25, "and there was"),
        (26, 28, "great mourning"),
        (29, 31, "and howling"),
        (32, 34, "and weeping"),
        (35, 39, "among all the people"),
        (40, 42, "continually;"),
        (43, 43, "yea,"),
        (44, 50, "great indeed were the groans of the people,"),
        (51, 52, "because of"),
        (53, 54, "the darkness"),
        (55, 59, "and the great destruction which"),
        (60, 62, "had come"),
        (63, 66, "upon them."),
    ],
    24: [
        (0, 4, "And in one place"),
        (5, 8, "they were heard"),
        (9, 10, "crying,"),
        (11, 12, "saying:"),
        (13, 13, "O,"),
        (14, 18, "if we had repented"),
        (19, 22, "before there came"),
        (23, 28, "this great and terrible day,"),
        (29, 31, "then would have been spared"),
        (32, 34, "our brethren,"),
        (35, 41, "and would not have been burned they"),
        (42, 47, "in that great city of Zarahemla."),
    ],
    25: [
        (0, 5, "And in another place"),
        (6, 9, "they were heard"),
        (10, 13, "crying and mourning,"),
        (14, 15, "saying:"),
        (16, 16, "O,"),
        (17, 21, "if we had repented"),
        (22, 25, "before there came"),
        (26, 31, "this great and terrible day,"),
        (32, 35, "and we had not slain"),
        (36, 38, "and stoned the prophets,"),
        (39, 43, "and cast them out;"),
        (44, 47, "then would have been spared"),
        (48, 50, "our mothers"),
        (51, 55, "and our fair daughters,"),
        (56, 59, "and our children,"),
        (60, 64, "and would not have been buried"),
        (65, 70, "in that great city of Moronihah."),
        (71, 78, "And thus great and terrible were"),
        (79, 83, "the howlings of the people."),
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
