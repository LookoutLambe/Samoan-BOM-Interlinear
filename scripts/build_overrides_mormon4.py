"""
Hand-curated TAM-phrase gloss overrides for Mamona (Mormon) 4 — the terrible wars for the
cities of Desolation and Teancum, the back-and-forth slaughter as the Nephites take up
the offensive and are smitten for it, the Lamanite sacrifice of Nephite women and
children to their idols, the utter wickedness on both sides, and Mormon's observation
that the judgments of God overtook the wicked so that never had there been so great
wickedness among all the children of Lehi.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15). `o le a` stays atomic and is never fused with a
following `se X` NP; cells go past 5 only for rule-2 (absorbed subject) or
rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_mormon4.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "mormon"
CHAPTER_NUM = 4

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "it came to pass"),
        (5, 7, "in the year"),
        (8, 10, "three hundred"),
        (11, 14, "and sixty and third,"),
        (15, 18, "did go up"),
        (19, 20, "the Nephites"),
        (21, 24, "with their armies"),
        (25, 27, "to battle against"),
        (28, 30, "the Lamanites,"),
        (31, 32, "out of"),
        (33, 35, "the land"),
        (36, 37, "of Desolation."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 5, "were driven back again"),
        (6, 6, "the armies"),
        (7, 9, "of the Nephites"),
        (10, 12, "to the land"),
        (13, 14, "of Desolation."),
        (15, 17, "And while they"),
        (18, 18, "were weary,"),
        (19, 21, "did come"),
        (22, 24, "a fresh army"),
        (25, 27, "of the Lamanites"),
        (28, 30, "upon"),
        (31, 32, "them;"),
        (33, 36, "and they did have"),
        (37, 39, "a sore battle,"),
        (40, 42, "insomuch that"),
        (43, 46, "the Lamanites took"),
        (47, 48, "the city"),
        (49, 50, "of Desolation,"),
        (51, 53, "and did slay"),
        (54, 55, "many"),
        (56, 58, "of the Nephites,"),
        (59, 61, "and did take prisoners"),
        (62, 63, "many."),
    ],
    3: [
        (0, 2, "And they"),
        (3, 4, "who remained"),
        (5, 6, "did flee"),
        (7, 9, "and join"),
        (10, 11, "with the inhabitants"),
        (12, 14, "of the city"),
        (15, 16, "of Teancum."),
        (17, 18, "Now"),
        (19, 21, "the city"),
        (22, 23, "of Teancum"),
        (24, 25, "lay"),
        (26, 27, "in the borders"),
        (28, 30, "beside"),
        (31, 32, "the seashore,"),
        (33, 36, "and it was also near"),
        (37, 39, "the city"),
        (40, 41, "of Desolation."),
    ],
    4: [
        (0, 4, "And they began to smite"),
        (5, 7, "them,"),
        (8, 8, "because"),
        (9, 12, "had gone up in vain"),
        (13, 14, "the armies"),
        (15, 17, "of the Nephites"),
        (18, 20, "unto the Lamanites;"),
        (21, 21, "for"),
        (22, 24, "if there were not"),
        (25, 26, "that thing,"),
        (27, 27, "would have"),
        (28, 31, "no power"),
        (32, 34, "of the Lamanites"),
        (35, 37, "over"),
        (38, 39, "them."),
    ],
    5: [
        (0, 1, "But, behold,"),
        (2, 3, "will overtake"),
        (4, 5, "the judgments"),
        (6, 8, "of God"),
        (9, 11, "the wicked;"),
        (12, 15, "and it is the wicked"),
        (16, 17, "that are punished"),
        (18, 20, "by the wicked;"),
        (21, 21, "for"),
        (22, 25, "the wicked"),
        (26, 28, "that stir up"),
        (29, 29, "the hearts"),
        (30, 32, "of the children"),
        (33, 34, "of men"),
        (35, 37, "unto the shedding"),
        (38, 38, "of blood."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 4, "did make"),
        (5, 7, "the Lamanites"),
        (8, 8, "preparations"),
        (9, 10, "to come against"),
        (11, 12, "the city"),
        (13, 14, "of Teancum."),
    ],
    7: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 8, "three hundred"),
        (9, 12, "and sixty and fourth"),
        (13, 16, "did come"),
        (17, 18, "the Lamanites"),
        (19, 20, "against"),
        (21, 22, "the city"),
        (23, 24, "of Teancum,"),
        (25, 29, "that they might also"),
        (30, 30, "take"),
        (31, 33, "unto themselves"),
        (34, 35, "the city"),
        (36, 37, "of Teancum."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 4, "were repulsed"),
        (5, 9, "and driven back"),
        (10, 11, "they"),
        (12, 14, "by the Nephites."),
        (15, 18, "And when saw"),
        (19, 20, "the Nephites"),
        (21, 23, "that they had driven"),
        (24, 25, "the Lamanites,"),
        (26, 29, "they did again boast"),
        (30, 34, "of their own strength;"),
        (35, 39, "and they went forth"),
        (40, 44, "in their own might,"),
        (45, 47, "and took again"),
        (48, 49, "the city"),
        (50, 51, "of Desolation."),
    ],
    9: [
        (0, 2, "And now"),
        (3, 6, "all these things"),
        (7, 8, "had been done,"),
        (9, 12, "and there had been thousands"),
        (13, 15, "slain"),
        (16, 20, "on both sides,"),
        (21, 23, "both the Nephites"),
        (24, 26, "and the Lamanites."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 5, "had passed away"),
        (6, 7, "the year"),
        (8, 10, "three hundred"),
        (11, 14, "and sixty and sixth,"),
        (15, 17, "and again"),
        (18, 20, "came also"),
        (21, 22, "the Lamanites"),
        (23, 25, "upon"),
        (26, 27, "the Nephites"),
        (28, 29, "to battle;"),
        (30, 34, "and yet repented not"),
        (35, 36, "the Nephites"),
        (37, 39, "of the evil"),
        (40, 42, "they had done,"),
        (43, 45, "but persisted"),
        (46, 49, "in their wickedness"),
        (50, 52, "continually."),
    ],
    11: [
        (0, 3, "And it is impossible"),
        (4, 6, "for the tongue"),
        (7, 8, "to describe,"),
        (9, 11, "nor possible"),
        (12, 14, "for man"),
        (15, 16, "to write"),
        (17, 19, "a perfect description"),
        (20, 23, "of the horrible scene"),
        (24, 26, "of the blood"),
        (27, 29, "and carnage"),
        (30, 32, "which was"),
        (33, 35, "among"),
        (36, 36, "the people,"),
        (37, 39, "both the Nephites"),
        (40, 42, "and the Lamanites;"),
        (43, 45, "and was hardened"),
        (46, 47, "every heart,"),
        (48, 52, "so that they delighted"),
        (53, 55, "in the shedding"),
        (56, 58, "of blood"),
        (59, 61, "continually."),
    ],
    12: [
        (0, 3, "And there was never"),
        (4, 6, "so great wickedness"),
        (7, 9, "as was"),
        (10, 12, "among"),
        (13, 15, "all the children"),
        (16, 17, "of Lehi,"),
        (18, 20, "nor even among"),
        (21, 24, "all the house"),
        (25, 26, "of Israel,"),
        (27, 30, "according to"),
        (31, 31, "the words"),
        (32, 34, "of the Lord,"),
        (35, 39, "as was"),
        (40, 42, "among"),
        (43, 44, "this people."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 4, "did take"),
        (5, 7, "the Lamanites"),
        (8, 9, "the city"),
        (10, 11, "of Desolation,"),
        (12, 15, "and this the cause"),
        (16, 16, "because"),
        (17, 19, "did exceed"),
        (20, 21, "the greatness"),
        (22, 25, "of their number"),
        (26, 27, "than"),
        (28, 29, "the number"),
        (30, 32, "of the Nephites."),
    ],
    14: [
        (0, 4, "And they did march forth"),
        (5, 5, "also"),
        (6, 7, "forward"),
        (8, 10, "against"),
        (11, 12, "the city"),
        (13, 14, "of Teancum,"),
        (15, 18, "and did drive out"),
        (19, 19, "the inhabitants"),
        (20, 20, "out of"),
        (21, 23, "her,"),
        (24, 27, "and did take prisoners"),
        (28, 29, "many,"),
        (30, 31, "women"),
        (32, 33, "and children,"),
        (34, 37, "and did offer"),
        (38, 39, "them"),
        (40, 42, "as sacrifices"),
        (43, 45, "unto their"),
        (46, 47, "idol gods."),
    ],
    15: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 8, "three hundred"),
        (9, 12, "and sixty and seventh,"),
        (13, 14, "being angry"),
        (15, 16, "the Nephites"),
        (17, 17, "because"),
        (18, 19, "had sacrificed"),
        (20, 22, "the Lamanites"),
        (23, 23, "as offering"),
        (24, 27, "their women"),
        (28, 31, "and their children,"),
        (32, 34, "insomuch that"),
        (35, 37, "they went"),
        (38, 39, "against"),
        (40, 42, "the Lamanites"),
        (43, 46, "with exceedingly great anger,"),
        (47, 49, "insomuch that"),
        (50, 52, "they again beat"),
        (53, 54, "the Lamanites,"),
        (55, 58, "and drove out"),
        (59, 60, "them"),
        (61, 62, "out of"),
        (63, 65, "their lands."),
    ],
    16: [
        (0, 3, "And did not again"),
        (4, 5, "come"),
        (6, 7, "the Lamanites"),
        (8, 10, "against"),
        (11, 13, "the Nephites"),
        (14, 16, "until"),
        (17, 18, "the year"),
        (19, 21, "three hundred"),
        (22, 25, "and seventy and fifth."),
    ],
    17: [
        (0, 4, "And in this year,"),
        (5, 8, "they came"),
        (9, 10, "down"),
        (11, 13, "against"),
        (14, 16, "the Nephites"),
        (17, 21, "with all their powers;"),
        (22, 25, "and were not numbered"),
        (26, 27, "they"),
        (28, 29, "because of"),
        (30, 32, "the great multitude"),
        (33, 36, "of their number."),
    ],
    18: [
        (0, 4, "And beginning from"),
        (5, 6, "this time"),
        (7, 10, "onward"),
        (11, 14, "no more gained"),
        (15, 17, "the Nephites"),
        (18, 19, "power"),
        (20, 22, "over"),
        (23, 24, "the Lamanites,"),
        (25, 28, "but began to"),
        (29, 30, "be swept off"),
        (31, 33, "them"),
        (34, 36, "by them"),
        (37, 41, "even as a dew"),
        (42, 44, "before"),
        (45, 46, "the sun."),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 5, "came down"),
        (6, 7, "the Lamanites"),
        (8, 9, "against"),
        (10, 12, "the city"),
        (13, 14, "of Desolation;"),
        (15, 18, "and there was"),
        (19, 22, "an exceedingly sore battle"),
        (23, 24, "fought"),
        (25, 27, "in the land"),
        (28, 29, "of Desolation,"),
        (30, 30, "wherein"),
        (31, 34, "they did beat"),
        (35, 36, "the Nephites."),
    ],
    20: [
        (0, 4, "And they fled again"),
        (5, 6, "from"),
        (7, 9, "before them,"),
        (10, 14, "and they came"),
        (15, 17, "to the city"),
        (18, 19, "of Boaz;"),
        (20, 22, "and there"),
        (23, 25, "they did stand"),
        (26, 28, "against"),
        (29, 31, "the Lamanites"),
        (32, 35, "with exceeding boldness,"),
        (36, 38, "insomuch that"),
        (39, 42, "they were not beaten"),
        (43, 45, "by the Lamanites"),
        (46, 48, "until"),
        (49, 52, "they came again"),
        (53, 57, "the second time."),
    ],
    21: [
        (0, 3, "And when they"),
        (4, 6, "came again"),
        (7, 11, "the second time,"),
        (12, 13, "were driven"),
        (14, 15, "and slaughtered"),
        (16, 17, "the Nephites"),
        (18, 22, "with an exceedingly great slaughter;"),
        (23, 25, "were again sacrificed"),
        (26, 28, "their women"),
        (29, 32, "and their children"),
        (33, 34, "unto idols."),
    ],
    22: [
        (0, 3, "And it came to pass that"),
        (4, 6, "did again flee"),
        (7, 8, "the Nephites"),
        (9, 10, "from"),
        (11, 13, "before them,"),
        (14, 16, "taking together"),
        (17, 19, "with them"),
        (20, 21, "all the inhabitants,"),
        (22, 24, "who were in"),
        (25, 25, "towns"),
        (26, 27, "and villages."),
    ],
    23: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Mormon,"),
        (7, 10, "when I saw"),
        (11, 14, "would overthrow"),
        (15, 17, "the Lamanites"),
        (18, 19, "the land,"),
        (20, 21, "therefore"),
        (22, 26, "I did go"),
        (27, 29, "to the hill"),
        (30, 31, "of Shim,"),
        (32, 34, "and did take up"),
        (35, 36, "all the records"),
        (37, 37, "which"),
        (38, 39, "had hid up"),
        (40, 41, "Ammaron"),
        (42, 44, "unto the Lord."),
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
