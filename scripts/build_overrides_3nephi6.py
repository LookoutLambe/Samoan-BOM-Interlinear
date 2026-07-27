"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 6 — the Nephites
return to their lands and prosper, establishing peace and order; but pride,
riches, and inequality soon breed persecution and the breaking up of the church;
lawyers, judges, and high priests conspire in secret combinations, condemn the
prophets to death against the law, and by the twenty-ninth and thirtieth years
the people, ripening for destruction, destroy the government and divide into
tribes, led by a secret combination bent on slaying Lachoneus and the chief judge.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits applied to bom_books.json before glossing:
    6:17  tolusefulu—ona  ->  tolusefulu—  +  ona
    6:17  faia—ma         ->  faia—        +  ma

    python3 build_overrides_3nephi6.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 6

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 8, "returned"),
        (9, 11, "the Nephite people"),
        (12, 16, "to their own lands"),
        (17, 20, "in the year"),
        (21, 24, "twenty-sixth,"),
        (25, 28, "every single man,"),
        (29, 31, "with his family,"),
        (32, 33, "his flocks"),
        (34, 36, "and his herds,"),
        (37, 38, "his horses,"),
        (39, 41, "and his cattle,"),
        (42, 45, "and whatsoever"),
        (46, 49, "of all things"),
        (50, 53, "that belonged to them."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 8, "they had not used up"),
        (9, 12, "all their food;"),
        (13, 14, "therefore"),
        (15, 19, "they took along"),
        (20, 22, "with them"),
        (23, 24, "all things"),
        (25, 29, "they had not used up,"),
        (30, 34, "all their grain"),
        (35, 37, "of every kind,"),
        (38, 41, "and their gold,"),
        (42, 45, "and their silver,"),
        (46, 51, "and all their precious things,"),
        (52, 56, "and they returned"),
        (57, 61, "to their own lands"),
        (62, 65, "and their possessions,"),
        (66, 70, "on the north side"),
        (71, 75, "and on the south side,"),
        (76, 80, "on the land northward"),
        (81, 86, "and on the land southward."),
    ],
    3: [
        (0, 4, "And they granted"),
        (5, 8, "unto those robbers"),
        (9, 15, "who had entered a covenant"),
        (16, 22, "to keep the peace of the land,"),
        (23, 26, "who desired"),
        (27, 29, "to remain still"),
        (30, 33, "as Lamanites,"),
        (34, 35, "lands,"),
        (36, 38, "according to"),
        (39, 41, "their numbers,"),
        (42, 47, "that they might obtain,"),
        (48, 50, "by their labors,"),
        (51, 55, "means to live by;"),
        (56, 61, "and thus they established"),
        (62, 64, "the peace"),
        (65, 68, "in all the land."),
    ],
    4: [
        (0, 6, "And they began again to prosper"),
        (7, 11, "and to grow exceedingly great;"),
        (12, 17, "and there passed away"),
        (18, 20, "the year"),
        (21, 24, "twenty-sixth"),
        (25, 30, "and twenty-seventh,"),
        (31, 34, "and there was"),
        (35, 37, "great order"),
        (38, 40, "in the land;"),
        (41, 44, "and they made"),
        (45, 47, "their laws"),
        (48, 50, "according to"),
        (51, 53, "equal rights"),
        (54, 58, "and doing justice."),
    ],
    5: [
        (0, 2, "And now"),
        (3, 8, "there was nothing"),
        (9, 12, "in all the land"),
        (13, 16, "to hinder the people"),
        (17, 19, "from prospering"),
        (20, 22, "continually,"),
        (23, 24, "except"),
        (25, 28, "they fall"),
        (29, 31, "into transgression."),
    ],
    6: [
        (0, 2, "And now"),
        (3, 4, "it was Gidgiddoni,"),
        (5, 7, "and the judge,"),
        (8, 9, "Lachoneus,"),
        (10, 15, "and all those who"),
        (16, 21, "were appointed to be leaders,"),
        (22, 25, "it was they who"),
        (26, 27, "established"),
        (28, 30, "this great peace"),
        (31, 33, "in the land."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 7, "many new cities"),
        (8, 9, "were built,"),
        (10, 15, "and many old cities also"),
        (16, 18, "were renewed."),
    ],
    8: [
        (0, 3, "And there were many highways"),
        (4, 5, "built,"),
        (6, 8, "and many roads"),
        (9, 10, "made,"),
        (11, 15, "which connected"),
        (16, 21, "from city to city,"),
        (22, 28, "and from land to land,"),
        (29, 35, "and from place to place."),
    ],
    9: [
        (0, 5, "And thus passed away"),
        (6, 9, "the year"),
        (10, 13, "twenty-eighth,"),
        (14, 20, "and the people still had"),
        (21, 25, "continual peace."),
    ],
    10: [
        (0, 3, "But when came"),
        (4, 7, "in the year"),
        (8, 11, "twenty-ninth"),
        (12, 16, "there began to be"),
        (17, 19, "some disputes"),
        (20, 23, "among the people;"),
        (24, 27, "and some"),
        (28, 29, "were puffed up"),
        (30, 32, "in pride"),
        (33, 35, "and boasting"),
        (36, 37, "because of"),
        (38, 40, "their riches"),
        (41, 44, "which were exceedingly great,"),
        (45, 45, "yea,"),
        (46, 49, "even unto"),
        (50, 54, "the doing of great persecutions;"),
    ],
    11: [
        (0, 0, "For"),
        (1, 4, "there were many merchants"),
        (5, 7, "who were"),
        (8, 10, "in the land,"),
        (11, 14, "and also many lawyers,"),
        (15, 20, "and many officers."),
    ],
    12: [
        (0, 5, "And the people began to be marked"),
        (6, 9, "by their ranks,"),
        (10, 12, "according to"),
        (13, 15, "their riches"),
        (16, 21, "and their chances for learning;"),
        (22, 22, "yea,"),
        (23, 27, "there were some"),
        (28, 30, "who were unlearned"),
        (31, 32, "because of"),
        (33, 35, "their poverty,"),
        (36, 38, "and others"),
        (39, 43, "received great learning"),
        (44, 45, "because of"),
        (46, 48, "their riches."),
    ],
    13: [
        (0, 1, "Some"),
        (2, 3, "were puffed up"),
        (4, 6, "in pride,"),
        (7, 9, "and others"),
        (10, 12, "were very humble;"),
        (13, 14, "some"),
        (15, 18, "returned"),
        (19, 24, "railing for railing,"),
        (25, 27, "while others"),
        (28, 30, "received"),
        (31, 33, "railing and persecution"),
        (34, 38, "and all kinds of afflictions,"),
        (39, 42, "and would not turn"),
        (43, 46, "and revile again,"),
        (47, 49, "but were humble"),
        (50, 51, "and penitent"),
        (52, 56, "before God."),
    ],
    14: [
        (0, 5, "And thus there came"),
        (6, 10, "a great inequality"),
        (11, 14, "in all the land,"),
        (15, 17, "insomuch that"),
        (18, 20, "began to be divided"),
        (21, 22, "the church;"),
        (23, 23, "yea,"),
        (24, 27, "insomuch that"),
        (28, 30, "the church was broken up"),
        (31, 34, "in all the land"),
        (35, 39, "in the thirtieth year,"),
        (40, 41, "except"),
        (42, 47, "a few Lamanites"),
        (48, 52, "who were converted"),
        (53, 56, "unto the true faith;"),
        (57, 65, "and they would not go away from it,"),
        (66, 69, "for they were steadfast,"),
        (70, 72, "and immovable,"),
        (73, 76, "and they were willing"),
        (77, 80, "with all diligence"),
        (81, 86, "to keep the commandments of the Lord."),
    ],
    15: [
        (0, 1, "Now"),
        (2, 5, "this was the cause"),
        (6, 10, "of the iniquity of the people—"),
        (11, 14, "Satan had gained"),
        (15, 17, "great power,"),
        (18, 21, "to stir up the people"),
        (22, 27, "to do all kinds of iniquity,"),
        (28, 32, "and puffing them up"),
        (33, 35, "with pride,"),
        (36, 39, "tempting them"),
        (40, 44, "to seek for power,"),
        (45, 47, "and authority,"),
        (48, 49, "and riches,"),
        (50, 53, "and the useless things of"),
        (54, 56, "the world."),
    ],
    16: [
        (0, 5, "And thus led away"),
        (6, 7, "Satan"),
        (8, 10, "the hearts of the people"),
        (11, 16, "to do all kinds of iniquity;"),
        (17, 18, "therefore"),
        (19, 22, "they rejoiced"),
        (23, 25, "in the peace"),
        (26, 29, "for but a few years."),
    ],
    17: [
        (0, 2, "And thus,"),
        (3, 6, "in the beginning of"),
        (7, 10, "the thirtieth year—"),
        (11, 15, "the people being given up"),
        (16, 23, "for a very long time"),
        (24, 26, "to be led about"),
        (27, 31, "by the temptations of the devil"),
        (32, 35, "wheresoever"),
        (36, 39, "he desired"),
        (40, 45, "to lead them,"),
        (46, 50, "and to do whatever iniquity"),
        (51, 56, "he desired"),
        (57, 59, "they should do—"),
        (60, 63, "and thus even"),
        (64, 69, "in the beginning of this year,"),
        (70, 74, "this thirtieth year,"),
        (75, 78, "they were"),
        (79, 82, "in a state of"),
        (83, 86, "great awful wickedness."),
    ],
    18: [
        (0, 1, "Now"),
        (2, 5, "they did not sin"),
        (6, 9, "in ignorance,"),
        (10, 13, "for they knew"),
        (14, 18, "the will of God"),
        (19, 24, "concerning them,"),
        (25, 28, "for it was taught"),
        (29, 32, "unto them;"),
        (33, 34, "therefore"),
        (35, 38, "they rebelled"),
        (39, 43, "against God"),
        (44, 48, "willingly."),
    ],
    19: [
        (0, 2, "Now"),
        (3, 6, "it was the days of Lachoneus,"),
        (7, 10, "the son of Lachoneus,"),
        (11, 14, "for Lachoneus sat"),
        (15, 20, "in the seat of his father"),
        (21, 25, "and governed the people"),
        (26, 29, "in that year,"),
        (30, 32, "wherein was"),
        (33, 35, "this great wickedness."),
    ],
    20: [
        (0, 5, "And there began to be"),
        (6, 8, "men"),
        (9, 13, "inspired from heaven"),
        (14, 16, "and sent forth,"),
        (17, 18, "standing"),
        (19, 23, "in the midst of the people"),
        (24, 26, "in all the lands,"),
        (27, 28, "and preaching"),
        (29, 34, "and testifying boldly"),
        (35, 37, "concerning"),
        (38, 42, "the sins and iniquities of the people,"),
        (43, 49, "and testifying unto them"),
        (50, 55, "concerning the redemption which"),
        (56, 62, "the Lord would make"),
        (63, 65, "for his people,"),
        (66, 67, "or thus,"),
        (68, 74, "the resurrection of Christ;"),
        (75, 82, "and they testified faithfully"),
        (83, 85, "concerning"),
        (86, 90, "his death and his sufferings."),
    ],
    21: [
        (0, 1, "Now"),
        (2, 7, "there were many people"),
        (8, 10, "who were exceedingly angry"),
        (11, 16, "because of those who"),
        (17, 19, "testified"),
        (20, 24, "concerning these things;"),
        (25, 32, "and those who were angry"),
        (33, 35, "were chiefly"),
        (36, 38, "the chief judges,"),
        (39, 43, "and they who"),
        (44, 48, "had been high priests"),
        (49, 50, "and lawyers;"),
        (51, 51, "yea,"),
        (52, 56, "all those"),
        (57, 60, "who were lawyers"),
        (61, 62, "were angry"),
        (63, 68, "with those who"),
        (69, 71, "testified"),
        (72, 76, "concerning these things."),
    ],
    22: [
        (0, 1, "Now"),
        (2, 5, "there was no lawyer"),
        (6, 9, "nor judge"),
        (10, 14, "nor high priest"),
        (15, 19, "who had power"),
        (20, 24, "to condemn anyone"),
        (25, 27, "to death"),
        (28, 29, "except"),
        (30, 34, "their sentence was signed"),
        (35, 40, "by the governor of the land."),
    ],
    23: [
        (0, 1, "Now"),
        (2, 8, "there were many"),
        (9, 17, "who testified boldly"),
        (18, 23, "of things pertaining to Christ,"),
        (24, 27, "who were taken"),
        (28, 30, "and slain secretly"),
        (31, 32, "by the judges,"),
        (33, 41, "the governor of the land did not know"),
        (42, 44, "their death"),
        (45, 49, "until after their death."),
    ],
    24: [
        (0, 2, "Now behold,"),
        (3, 5, "this thing"),
        (6, 10, "was contrary to"),
        (11, 14, "the laws of the land,"),
        (15, 19, "it not being lawful to slay"),
        (20, 22, "any man"),
        (23, 24, "except"),
        (25, 29, "they had power"),
        (30, 36, "from the governor of the land—"),
    ],
    25: [
        (0, 1, "Therefore"),
        (2, 7, "a complaint came"),
        (8, 12, "unto the land of Zarahemla,"),
        (13, 18, "to the governor of the land,"),
        (19, 23, "against those judges"),
        (24, 31, "who condemned to death"),
        (32, 35, "the prophets of the Lord,"),
        (36, 39, "contrary to"),
        (40, 42, "the law."),
    ],
    26: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 7, "they were taken"),
        (8, 9, "and brought"),
        (10, 14, "before the judge,"),
        (15, 19, "that they be judged"),
        (20, 23, "for the crime which"),
        (24, 26, "they did,"),
        (27, 29, "according to"),
        (30, 32, "the law which"),
        (33, 38, "was given by the people."),
    ],
    27: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 9, "there were among the judges"),
        (10, 15, "many of their friends"),
        (16, 17, "and kindred;"),
        (18, 22, "and those who remained,"),
        (23, 23, "yea,"),
        (24, 27, "almost all the lawyers"),
        (28, 31, "and all the high priests,"),
        (32, 35, "they gathered together"),
        (36, 38, "themselves,"),
        (39, 42, "and joined together"),
        (43, 47, "with the kindred of those judges"),
        (48, 53, "who were to be judged"),
        (54, 56, "according to"),
        (57, 58, "the law."),
    ],
    28: [
        (0, 4, "And they entered"),
        (5, 7, "into a covenant"),
        (8, 13, "one with another,"),
        (14, 14, "yea,"),
        (15, 18, "even that covenant"),
        (19, 24, "given by them"),
        (25, 26, "of old,"),
        (27, 30, "which covenant"),
        (31, 35, "was given and made"),
        (36, 38, "by the devil,"),
        (39, 42, "to combine together"),
        (43, 48, "against all righteousness."),
    ],
    29: [
        (0, 1, "Therefore"),
        (2, 5, "they combined"),
        (6, 12, "against the people of the Lord,"),
        (13, 19, "and entered a covenant"),
        (20, 23, "to destroy them,"),
        (24, 27, "and to deliver those"),
        (28, 31, "who were guilty"),
        (32, 35, "of murder"),
        (36, 39, "from the grasp of"),
        (40, 41, "justice,"),
        (42, 47, "which was about to be given"),
        (48, 50, "according to"),
        (51, 52, "the law."),
    ],
    30: [
        (0, 3, "And they defied"),
        (4, 6, "the law"),
        (7, 12, "and the rights of their country;"),
        (13, 16, "and they covenanted"),
        (17, 22, "one with another"),
        (23, 26, "to slay the governor,"),
        (27, 30, "and to set up a king"),
        (31, 35, "over the land,"),
        (36, 40, "that no longer be free"),
        (41, 42, "the land"),
        (43, 47, "but be ruled by kings."),
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
