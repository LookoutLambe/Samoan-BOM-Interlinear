"""
Hand-curated TAM-phrase gloss overrides for Mamona (Mormon) 1 — the boy Mormon is
entrusted by Ammaron with the charge to recover the plates of Nephi at age twenty-four
and record the doings of his people; the wickedness of the Nephites and Lamanites, the
withdrawal of the three disciples and of the Holy Ghost because of iniquity, the
sorceries and witchcrafts abroad in the land, the renewal of war between the Nephites
and Lamanites, and young Mormon's forbidden preaching.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15). `o le a` stays atomic and is never fused with a
following `se X` NP; cells go past 5 only for rule-2 (absorbed subject) or
rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_mormon1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "mormon"
CHAPTER_NUM = 1

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Mormon,"),
        (7, 9, "make"),
        (10, 11, "a record"),
        (12, 13, "of the things"),
        (14, 16, "which I have seen"),
        (17, 18, "and heard,"),
        (19, 21, "and call it"),
        (22, 24, "the Book"),
        (25, 26, "of Mormon."),
    ],
    2: [
        (0, 3, "And about"),
        (4, 5, "the time"),
        (6, 9, "that hid up"),
        (10, 11, "Ammaron"),
        (12, 12, "the records"),
        (13, 15, "unto the Lord,"),
        (16, 20, "he came"),
        (21, 23, "unto me,"),
        (24, 26, "(about"),
        (27, 28, "ten"),
        (29, 32, "years of age,"),
        (33, 36, "and I began to"),
        (37, 39, "be learned"),
        (40, 42, "somewhat after"),
        (43, 45, "the manner of the learning"),
        (46, 48, "of my people)"),
        (49, 52, "and said"),
        (53, 53, "Ammaron"),
        (54, 56, "unto me:"),
        (57, 59, "I perceive"),
        (60, 62, "that thou art"),
        (63, 64, "a child"),
        (65, 66, "sober,"),
        (67, 70, "and art quick to"),
        (71, 72, "observe;"),
    ],
    3: [
        (0, 1, "Therefore,"),
        (2, 4, "when ye come to"),
        (5, 7, "about"),
        (8, 12, "twenty and four"),
        (13, 13, "years"),
        (14, 16, "of your age,"),
        (17, 19, "I would"),
        (20, 23, "that ye should remember"),
        (24, 27, "the things that ye have observed"),
        (28, 30, "concerning"),
        (31, 32, "this people;"),
        (33, 37, "and when ye come"),
        (38, 41, "of that age,"),
        (42, 44, "go"),
        (45, 47, "to the land"),
        (48, 49, "of Antum,"),
        (50, 52, "unto the hill"),
        (53, 54, "which is called"),
        (55, 56, "Shim;"),
        (57, 59, "and there"),
        (60, 63, "have I deposited"),
        (64, 66, "unto the Lord"),
        (67, 69, "all the sacred engravings"),
        (70, 72, "concerning"),
        (73, 74, "this people."),
    ],
    4: [
        (0, 1, "And behold,"),
        (2, 4, "ye shall take"),
        (5, 8, "unto yourself"),
        (9, 9, "the plates"),
        (10, 11, "of Nephi,"),
        (12, 15, "and the part"),
        (16, 17, "remaining"),
        (18, 21, "shall ye leave"),
        (22, 24, "in the place"),
        (25, 27, "where they are;"),
        (28, 31, "and ye shall engrave"),
        (32, 35, "on the plates"),
        (36, 37, "of Nephi"),
        (38, 39, "all the things"),
        (40, 42, "that ye have observed"),
        (43, 45, "concerning"),
        (46, 47, "this people."),
    ],
    5: [
        (0, 2, "And I,"),
        (3, 4, "Mormon,"),
        (5, 6, "being one"),
        (7, 9, "descended"),
        (10, 11, "of Nephi,"),
        (12, 15, "(and the name"),
        (16, 18, "of my father"),
        (19, 20, "was Mormon)"),
        (21, 23, "I remembered"),
        (24, 24, "the things"),
        (25, 28, "which commanded me"),
        (29, 30, "by Ammaron."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 8, "being eleven"),
        (9, 10, "years old,"),
        (11, 13, "I was carried"),
        (14, 16, "by my father"),
        (17, 19, "into the land"),
        (20, 21, "southward,"),
        (22, 25, "even to the land"),
        (26, 27, "of Zarahemla."),
    ],
    7: [
        (0, 1, "Had become covered"),
        (2, 3, "the face of"),
        (4, 6, "the whole land"),
        (7, 8, "with buildings,"),
        (9, 11, "and the people"),
        (12, 16, "were almost as numerous"),
        (17, 19, "their multitude,"),
        (20, 21, "as the sand"),
        (22, 24, "of the sea."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 4, "there began"),
        (5, 8, "in this year"),
        (9, 10, "a war"),
        (11, 14, "between"),
        (15, 16, "the Nephites,"),
        (17, 21, "who consisted of"),
        (22, 23, "the Nephites"),
        (24, 26, "and the Jacobites"),
        (27, 29, "and the Josephites"),
        (30, 32, "and the Zoramites;"),
        (33, 36, "and this war"),
        (37, 38, "was"),
        (39, 42, "between"),
        (43, 44, "the Nephites,"),
        (45, 47, "and the Lamanites"),
        (48, 50, "and the Lemuelites"),
        (51, 53, "and the Ishmaelites."),
    ],
    9: [
        (0, 1, "Now,"),
        (2, 4, "the Lamanites"),
        (5, 7, "and the Lemuelites"),
        (8, 10, "and the Ishmaelites"),
        (11, 12, "were called"),
        (13, 15, "Lamanites,"),
        (16, 20, "and the two parties"),
        (21, 23, "were Nephites"),
        (24, 26, "and Lamanites."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 4, "began"),
        (5, 6, "the war"),
        (7, 8, "among"),
        (9, 12, "them"),
        (13, 14, "in the borders"),
        (15, 16, "of Zarahemla,"),
        (17, 19, "beside"),
        (20, 21, "the waters"),
        (22, 23, "of Sidon."),
    ],
    11: [
        (0, 3, "And it came to pass that"),
        (4, 5, "had gathered together"),
        (6, 8, "the Nephites"),
        (9, 11, "a great number"),
        (12, 13, "of men,"),
        (14, 17, "even to exceed"),
        (18, 20, "the number"),
        (21, 24, "of thirty thousand."),
        (25, 28, "And it came to pass that"),
        (29, 30, "they did have"),
        (31, 34, "in this same year"),
        (35, 38, "a number of battles,"),
        (39, 42, "in which did beat"),
        (43, 45, "the Nephites"),
        (46, 48, "the Lamanites"),
        (49, 52, "and did slay"),
        (53, 54, "many"),
        (55, 57, "of them."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 4, "did withdraw"),
        (5, 7, "the Lamanites"),
        (8, 10, "their design,"),
        (11, 13, "and was settled"),
        (14, 15, "peace"),
        (16, 18, "in the land;"),
        (19, 21, "and did remain"),
        (22, 24, "peace"),
        (25, 28, "for the space of"),
        (29, 31, "about"),
        (32, 34, "four years,"),
        (35, 38, "that there was"),
        (39, 40, "no"),
        (41, 42, "bloodshed."),
    ],
    13: [
        (0, 3, "But did prevail"),
        (4, 5, "wickedness"),
        (6, 8, "upon"),
        (9, 11, "the whole land,"),
        (12, 14, "insomuch that"),
        (15, 15, "did take away"),
        (16, 18, "the Lord"),
        (19, 21, "his beloved disciples,"),
        (22, 24, "and did cease"),
        (25, 27, "the work of miracles"),
        (28, 29, "and of healing"),
        (30, 31, "because of"),
        (32, 33, "the iniquity"),
        (34, 35, "of the people."),
    ],
    14: [
        (0, 4, "And there were no gifts"),
        (5, 5, "from"),
        (6, 7, "the Lord,"),
        (8, 12, "and did not come"),
        (13, 15, "the Holy Ghost"),
        (16, 18, "upon"),
        (19, 20, "any,"),
        (21, 22, "because of"),
        (23, 25, "their wickedness"),
        (26, 29, "and unbelief."),
    ],
    15: [
        (0, 2, "And I,"),
        (3, 5, "being ten"),
        (6, 8, "and five"),
        (9, 11, "years of age"),
        (12, 16, "and being somewhat"),
        (17, 20, "of myself"),
        (21, 23, "a mind"),
        (24, 24, "sober,"),
        (25, 26, "therefore"),
        (27, 30, "visited"),
        (31, 32, "the Lord"),
        (33, 35, "unto me,"),
        (36, 38, "and tasted"),
        (39, 41, "and knew"),
        (42, 43, "the goodness"),
        (44, 45, "of Jesus."),
    ],
    16: [
        (0, 3, "And I did endeavor"),
        (4, 6, "to preach"),
        (7, 9, "unto this people,"),
        (10, 12, "but was shut"),
        (13, 14, "my mouth,"),
        (15, 18, "and I was forbidden"),
        (19, 22, "that I should preach"),
        (23, 26, "unto them;"),
        (27, 28, "for behold,"),
        (29, 31, "they had rebelled"),
        (32, 36, "wilfully"),
        (37, 39, "against"),
        (40, 42, "their God;"),
        (43, 45, "and were taken away"),
        (46, 47, "the beloved disciples"),
        (48, 48, "out of"),
        (49, 50, "the land,"),
        (51, 52, "because of"),
        (53, 55, "their iniquity."),
    ],
    17: [
        (0, 0, "But"),
        (1, 5, "I did remain"),
        (6, 8, "among"),
        (9, 10, "them,"),
        (11, 14, "but I was forbidden"),
        (15, 18, "to preach"),
        (19, 22, "unto them,"),
        (23, 24, "because of"),
        (25, 26, "the hardness"),
        (27, 30, "of their hearts;"),
        (31, 33, "and because of"),
        (34, 35, "the hardness"),
        (36, 39, "of their hearts"),
        (40, 42, "was cursed"),
        (43, 44, "the land"),
        (45, 46, "for the sake of"),
        (47, 48, "them."),
    ],
    18: [
        (0, 3, "And these robbers"),
        (4, 5, "of Gadianton,"),
        (6, 7, "who"),
        (8, 11, "were among"),
        (12, 13, "the Lamanites,"),
        (14, 16, "did fill"),
        (17, 18, "the land,"),
        (19, 21, "insomuch that"),
        (22, 24, "the people began"),
        (25, 27, "who dwelt there"),
        (28, 29, "to hide up"),
        (30, 32, "their treasures"),
        (33, 35, "in the earth;"),
        (36, 39, "and it came that"),
        (40, 40, "became slippery"),
        (41, 42, "these things,"),
        (43, 43, "because"),
        (44, 45, "was cursed"),
        (46, 47, "the land"),
        (48, 50, "by the Lord,"),
        (51, 53, "that"),
        (54, 58, "they could not hold,"),
        (59, 61, "nor retain again"),
        (62, 63, "them."),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 6, "there were"),
        (7, 8, "sorceries,"),
        (9, 10, "and witchcrafts,"),
        (11, 14, "and magics;"),
        (15, 17, "and the power"),
        (18, 20, "of the devil"),
        (21, 22, "was wrought"),
        (23, 25, "upon"),
        (26, 28, "all the land,"),
        (29, 31, "even unto"),
        (32, 34, "the fulfilling"),
        (35, 37, "of all the words"),
        (38, 39, "of Abinadi,"),
        (40, 42, "and also Samuel"),
        (43, 45, "the Lamanite."),
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
