"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 16 — the
Lamanites destroy Ammonihah; Zoram and his sons lead the Nephites to
victory; Alma and Amulek preach; the church prospers.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

Em-dash token split in the source per rule 11: `atoa—ina` (v21) — so
v21 = 73 tokens.

    python3 build_overrides_alma16.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 16

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass in"),
        (4, 7, "the eleventh"),
        (8, 9, "year"),
        (10, 13, "of the reign of"),
        (14, 14, "the judges"),
        (15, 17, "over"),
        (18, 21, "the people of Nephi,"),
        (22, 26, "on the fifth day"),
        (27, 31, "of the second month,"),
        (32, 34, "there having been"),
        (35, 37, "much peace"),
        (38, 42, "in the land of Zarahemla,"),
        (43, 45, "there having been no"),
        (46, 47, "wars"),
        (48, 51, "nor contentions"),
        (52, 55, "for a certain number of years,"),
        (56, 59, "even until"),
        (60, 63, "the fifth day"),
        (64, 68, "of the second month"),
        (69, 72, "in the eleventh"),
        (73, 74, "year,"),
        (75, 78, "there was heard"),
        (79, 81, "a cry of"),
        (82, 83, "war"),
        (84, 87, "throughout all the land."),
    ],
    2: [
        (0, 1, "For behold,"),
        (2, 4, "had come"),
        (5, 8, "the armies of the Lamanites"),
        (9, 11, "up"),
        (12, 15, "by the way of"),
        (16, 17, "the wilderness,"),
        (18, 20, "even unto the borders of"),
        (21, 22, "the land,"),
        (23, 26, "even unto"),
        (27, 30, "the city of Ammonihah,"),
        (31, 33, "and began to"),
        (34, 34, "slay"),
        (35, 35, "the people"),
        (36, 37, "and destroy"),
        (38, 39, "the city."),
    ],
    3: [
        (0, 0, "And"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 7, "could not"),
        (8, 11, "the Nephites"),
        (12, 16, "raise a sufficient army"),
        (17, 20, "to drive out"),
        (21, 22, "them"),
        (23, 25, "from the land,"),
        (26, 28, "they had destroyed"),
        (29, 31, "the people who"),
        (32, 36, "were in the city of"),
        (37, 37, "Ammonihah,"),
        (38, 40, "and also some"),
        (41, 44, "in the borders of"),
        (45, 45, "Noah,"),
        (46, 48, "and taken others"),
        (49, 49, "captive"),
        (50, 52, "into the wilderness."),
    ],
    4: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 5, "were desirous"),
        (6, 7, "the Nephites"),
        (8, 10, "to obtain"),
        (11, 12, "those"),
        (13, 17, "who had been carried away"),
        (18, 18, "captive"),
        (19, 21, "into the wilderness."),
    ],
    5: [
        (0, 1, "Therefore,"),
        (2, 7, "he that had been appointed"),
        (8, 12, "to be chief captain"),
        (13, 15, "over"),
        (16, 19, "the armies of the Nephites,"),
        (20, 20, "(and"),
        (21, 25, "his name was Zoram,"),
        (26, 30, "and he had"),
        (31, 34, "two sons,"),
        (35, 38, "Lehi and Aha)—"),
        (39, 40, "now"),
        (41, 43, "knowing"),
        (44, 45, "Zoram"),
        (46, 50, "and his two sons"),
        (51, 52, "that Alma"),
        (53, 57, "was high priest of"),
        (58, 59, "the church,"),
        (60, 63, "and having heard"),
        (64, 67, "that he had"),
        (68, 71, "the spirit of prophecy,"),
        (72, 73, "therefore"),
        (74, 78, "they went"),
        (79, 81, "unto him"),
        (82, 84, "and desired"),
        (85, 87, "of him"),
        (88, 90, "to know"),
        (91, 93, "whither"),
        (94, 97, "the Lord would"),
        (98, 103, "they should go"),
        (104, 106, "into the wilderness"),
        (107, 109, "in search of"),
        (110, 112, "their brethren,"),
        (113, 117, "who had been taken captive"),
        (118, 120, "by the Lamanites."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 5, "inquired"),
        (6, 6, "Alma"),
        (7, 9, "of the Lord"),
        (10, 12, "concerning"),
        (13, 14, "the matter."),
        (15, 15, "And"),
        (16, 19, "returned"),
        (20, 20, "Alma"),
        (21, 23, "and said"),
        (24, 27, "unto them:"),
        (28, 28, "Behold,"),
        (29, 32, "will cross"),
        (33, 35, "the Lamanites"),
        (36, 39, "the river Sidon"),
        (40, 42, "in the wilderness"),
        (43, 47, "on the south,"),
        (48, 52, "away up"),
        (53, 56, "beyond"),
        (57, 58, "the borders of"),
        (59, 62, "the land of Manti."),
        (63, 64, "And behold"),
        (65, 66, "there"),
        (67, 72, "shall ye meet"),
        (73, 75, "them,"),
        (76, 80, "on the east"),
        (81, 85, "of the river Sidon,"),
        (86, 88, "and there"),
        (89, 94, "will deliver"),
        (95, 97, "the Lord"),
        (98, 100, "unto thee"),
        (101, 102, "thy brethren"),
        (103, 107, "who have been taken captive"),
        (108, 110, "by the Lamanites."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 4, "crossed over"),
        (5, 9, "Zoram and his sons"),
        (10, 13, "the river Sidon,"),
        (14, 15, "with"),
        (16, 18, "their armies,"),
        (19, 22, "and marched away"),
        (23, 26, "beyond"),
        (27, 29, "the borders of Manti"),
        (30, 32, "into the wilderness"),
        (33, 37, "on the south,"),
        (38, 40, "which was on"),
        (41, 45, "the east side of"),
        (46, 49, "the river Sidon."),
    ],
    8: [
        (0, 0, "And"),
        (1, 5, "they came upon"),
        (6, 9, "the armies of the Lamanites,"),
        (10, 12, "and were scattered"),
        (13, 14, "the Lamanites"),
        (15, 16, "and driven"),
        (17, 19, "into the wilderness;"),
        (20, 23, "and they took"),
        (24, 26, "their brethren"),
        (27, 31, "who had been taken captive"),
        (32, 34, "by the Lamanites,"),
        (35, 37, "and there was not"),
        (38, 41, "one soul"),
        (42, 44, "of them"),
        (45, 49, "who were taken captive"),
        (50, 51, "had been lost."),
        (52, 54, "And were brought"),
        (55, 56, "they"),
        (57, 60, "by their brethren"),
        (61, 63, "to possess"),
        (64, 67, "their own lands."),
    ],
    9: [
        (0, 3, "And thus"),
        (4, 5, "ended"),
        (6, 9, "the eleventh"),
        (10, 11, "year"),
        (12, 13, "of the judges,"),
        (14, 16, "having been driven out"),
        (17, 18, "the Lamanites"),
        (19, 21, "of the land,"),
        (22, 24, "and were destroyed"),
        (25, 27, "the people of Ammonihah;"),
        (28, 28, "yea,"),
        (29, 30, "was destroyed"),
        (31, 34, "every living soul of"),
        (35, 36, "the Ammonihahites,"),
        (37, 41, "and their great city"),
        (42, 42, "also,"),
        (43, 47, "which they said"),
        (48, 50, "could not"),
        (51, 54, "God"),
        (55, 55, "destroy,"),
        (56, 57, "because of"),
        (58, 59, "its greatness."),
    ],
    10: [
        (0, 1, "But behold,"),
        (2, 5, "in one day"),
        (6, 8, "it was left desolate;"),
        (9, 11, "and were mangled"),
        (12, 13, "by dogs"),
        (14, 17, "and wild beasts of"),
        (18, 19, "the wilderness"),
        (20, 24, "the bodies of the dead."),
    ],
    11: [
        (0, 3, "Nevertheless,"),
        (4, 6, "after had passed"),
        (7, 10, "many days,"),
        (11, 12, "were heaped up"),
        (13, 16, "their dead bodies"),
        (17, 21, "upon the face of the earth,"),
        (22, 24, "and were covered"),
        (25, 26, "they"),
        (27, 30, "with a shallow covering."),
        (31, 33, "And now"),
        (34, 37, "so great was"),
        (38, 40, "the scent thereof"),
        (41, 46, "did not go in"),
        (47, 47, "the people"),
        (48, 52, "for many years"),
        (53, 57, "to possess"),
        (58, 61, "the land of Ammonihah."),
        (62, 64, "And it was called"),
        (65, 68, "the Desolation of"),
        (69, 71, "the Nehors;"),
        (72, 72, "for"),
        (73, 75, "they"),
        (76, 79, "who were slain,"),
        (80, 83, "these"),
        (84, 88, "were of the profession of Nehor;"),
        (89, 91, "and continued"),
        (92, 94, "the desolation of"),
        (95, 97, "their lands."),
    ],
    12: [
        (0, 3, "and did not again"),
        (4, 5, "come"),
        (6, 7, "the Lamanites"),
        (8, 10, "to war"),
        (11, 13, "against the Nephites"),
        (14, 16, "until"),
        (17, 20, "the fourteenth"),
        (21, 22, "year"),
        (23, 26, "of the reign of"),
        (27, 27, "the judges"),
        (28, 31, "over the people of Nephi."),
        (32, 35, "And thus"),
        (36, 37, "did have"),
        (38, 42, "the people of Nephi"),
        (43, 47, "continual peace"),
        (48, 51, "in all the land"),
        (52, 56, "for three years."),
    ],
    13: [
        (0, 3, "And went forth"),
        (4, 6, "Alma and Amulek"),
        (7, 9, "preaching"),
        (10, 11, "repentance"),
        (12, 13, "to the people"),
        (14, 17, "in their temples,"),
        (18, 22, "and in their sanctuaries,"),
        (23, 27, "and in their synagogues"),
        (28, 28, "also,"),
        (29, 31, "which were built"),
        (32, 34, "after"),
        (35, 37, "the manner of"),
        (38, 39, "the Jews."),
    ],
    14: [
        (0, 3, "and as many"),
        (4, 5, "as"),
        (6, 8, "would hear"),
        (9, 11, "their words,"),
        (12, 15, "unto them"),
        (16, 18, "they did impart"),
        (19, 22, "continually"),
        (23, 25, "the word of"),
        (26, 27, "God,"),
        (28, 30, "without"),
        (31, 33, "any respect of persons."),
    ],
    15: [
        (0, 3, "and thus"),
        (4, 5, "did go forth"),
        (6, 9, "Alma and Amulek,"),
        (10, 14, "and also many more"),
        (15, 18, "who had been chosen"),
        (19, 21, "for the work,"),
        (22, 24, "to preach"),
        (25, 26, "the word"),
        (27, 30, "throughout all the land."),
        (31, 35, "And the establishment of"),
        (36, 37, "the church"),
        (38, 39, "became general"),
        (40, 43, "throughout all the land,"),
        (44, 46, "in all the region"),
        (47, 49, "round about,"),
        (50, 52, "among"),
        (53, 55, "all the people of"),
        (56, 57, "the Nephites."),
    ],
    16: [
        (0, 2, "And there was no"),
        (3, 5, "inequality"),
        (6, 10, "among them;"),
        (11, 13, "did pour out"),
        (14, 16, "the Lord"),
        (17, 18, "his Spirit"),
        (19, 21, "upon"),
        (22, 24, "all the land"),
        (25, 27, "to prepare"),
        (28, 29, "the minds of"),
        (30, 33, "the children of men,"),
        (34, 36, "or to prepare"),
        (37, 39, "their hearts,"),
        (40, 41, "to receive"),
        (42, 43, "the word"),
        (44, 48, "which should be taught"),
        (49, 53, "among them"),
        (54, 57, "at the time of"),
        (58, 60, "his coming—"),
    ],
    17: [
        (0, 4, "That they might not be hardened"),
        (5, 7, "against"),
        (8, 9, "the word,"),
        (10, 14, "that might not"),
        (15, 17, "they be unbelieving,"),
        (18, 21, "and go on"),
        (22, 24, "to destruction,"),
        (25, 29, "but that might"),
        (30, 31, "they receive"),
        (32, 33, "the word"),
        (34, 36, "with joy,"),
        (37, 40, "and be grafted in"),
        (41, 42, "to become"),
        (43, 46, "a branch of"),
        (47, 48, "the true vine,"),
        (49, 52, "that might"),
        (53, 55, "they enter"),
        (56, 59, "into the rest of"),
        (60, 61, "the Lord"),
        (62, 64, "their God."),
    ],
    18: [
        (0, 1, "Now"),
        (2, 4, "those priests"),
        (5, 9, "who did go forth"),
        (10, 14, "among the people"),
        (15, 18, "did preach"),
        (19, 21, "against"),
        (22, 23, "all lyings,"),
        (24, 26, "and deceivings,"),
        (27, 29, "and envyings,"),
        (30, 31, "and strifes,"),
        (32, 34, "and malice,"),
        (35, 37, "and revilings,"),
        (38, 40, "and stealing,"),
        (41, 41, "robbing,"),
        (42, 42, "plundering,"),
        (43, 44, "murdering,"),
        (45, 48, "committing adultery,"),
        (49, 52, "and all manner of"),
        (53, 53, "lasciviousness;"),
        (54, 56, "crying,"),
        (57, 62, "that ought not so to be"),
        (63, 65, "these things—"),
    ],
    19: [
        (0, 2, "and declaring"),
        (3, 3, "things"),
        (4, 8, "which must shortly come;"),
        (9, 9, "yea,"),
        (10, 11, "declaring"),
        (12, 15, "the coming of"),
        (16, 17, "the Son"),
        (18, 20, "of God,"),
        (21, 23, "his sufferings"),
        (24, 26, "and death,"),
        (27, 31, "and also the resurrection"),
        (32, 35, "of the dead."),
    ],
    20: [
        (0, 0, "And"),
        (1, 3, "many of the people"),
        (4, 5, "did inquire"),
        (6, 8, "concerning"),
        (9, 10, "the place"),
        (11, 15, "where should come"),
        (16, 17, "thereto"),
        (18, 19, "the Son"),
        (20, 22, "of God;"),
        (23, 25, "and were taught"),
        (26, 27, "they"),
        (28, 34, "that he would appear"),
        (35, 38, "unto them"),
        (39, 41, "after"),
        (42, 44, "his resurrection;"),
        (45, 48, "and this"),
        (49, 53, "did hear"),
        (54, 54, "the people"),
        (55, 58, "with great joy"),
        (59, 61, "and gladness."),
    ],
    21: [
        (0, 2, "And now"),
        (3, 7, "after had been established"),
        (8, 10, "the church"),
        (11, 14, "throughout all the land—"),
        (15, 17, "having got"),
        (18, 19, "the victory"),
        (20, 22, "over the devil,"),
        (23, 26, "and being preached"),
        (27, 31, "the word of God"),
        (32, 34, "in its purity"),
        (35, 38, "in all the land,"),
        (39, 42, "and pouring out"),
        (43, 45, "the Lord"),
        (46, 47, "his blessings"),
        (48, 51, "upon the people—"),
        (52, 55, "thus ended"),
        (56, 60, "the fourteenth"),
        (61, 62, "year"),
        (63, 66, "of the reign of"),
        (67, 67, "the judges"),
        (68, 72, "over the people of Nephi."),
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
