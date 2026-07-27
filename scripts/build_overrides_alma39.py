"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 39 — Alma's charge
to his son Corianton: rebuked for forsaking the ministry to go after the
harlot Isabel; sexual sin is an abomination above all save murder and denying
the Holy Ghost; the coming of Christ preached beforehand as glad tidings.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash baked tokens in this chapter.

    python3 build_overrides_alma39.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 39

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 9, "there are yet"),
        (10, 13, "many things"),
        (14, 19, "I would say"),
        (20, 22, "unto thee"),
        (23, 25, "than that which"),
        (26, 29, "I said"),
        (30, 32, "unto thy brother;"),
        (33, 34, "for behold,"),
        (35, 39, "hast thou not observed"),
        (40, 43, "the steadiness of"),
        (44, 45, "thy brother,"),
        (46, 47, "his faithfulness,"),
        (48, 50, "and his diligence"),
        (51, 55, "in keeping the commandments"),
        (56, 58, "of God?"),
        (59, 59, "Behold,"),
        (60, 64, "hath he not set"),
        (65, 66, "for thee"),
        (67, 69, "a good example?"),
    ],
    2: [
        (0, 0, "For"),
        (1, 6, "thou gavest not much heed"),
        (7, 9, "unto my words"),
        (10, 14, "as did"),
        (15, 17, "thy brother,"),
        (18, 20, "among"),
        (21, 23, "the people of the Zoramites."),
        (24, 25, "Now,"),
        (26, 29, "this is the thing"),
        (30, 33, "which I have"),
        (34, 38, "against thee;"),
        (39, 43, "thou didst go on"),
        (44, 46, "unto boasting"),
        (47, 49, "in thy strength"),
        (50, 52, "and thy wisdom."),
    ],
    3: [
        (0, 0, "And"),
        (1, 5, "this is not all,"),
        (6, 8, "my son."),
        (9, 13, "Thou didst do that which"),
        (14, 15, "was grievous"),
        (16, 18, "unto me;"),
        (19, 19, "for"),
        (20, 22, "thou didst forsake"),
        (23, 27, "the ministry,"),
        (28, 31, "and didst go over"),
        (32, 36, "into the land of Siron"),
        (37, 41, "among the borders"),
        (42, 44, "of the Lamanites,"),
        (45, 48, "after the harlot"),
        (49, 50, "Isabel."),
    ],
    4: [
        (0, 0, "Yea,"),
        (1, 4, "she did steal away"),
        (5, 8, "the hearts of many;"),
        (9, 9, "but"),
        (10, 12, "my son,"),
        (13, 17, "this was no excuse"),
        (18, 19, "proper"),
        (20, 21, "for thee."),
        (22, 26, "Thou shouldst have tended"),
        (27, 29, "to the ministry"),
        (30, 34, "wherewith thou wast entrusted."),
    ],
    5: [
        (0, 4, "Know ye not"),
        (5, 7, "my son,"),
        (8, 10, "that these things"),
        (11, 14, "are an abomination"),
        (15, 18, "in the sight of"),
        (19, 20, "the Lord;"),
        (21, 21, "yea,"),
        (22, 25, "most abominable"),
        (26, 30, "above all sins"),
        (31, 32, "save it be"),
        (33, 35, "the shedding of"),
        (36, 39, "innocent blood"),
        (40, 44, "or the denying of"),
        (45, 47, "the Holy Ghost?"),
    ],
    6: [
        (0, 1, "For behold,"),
        (2, 5, "if ye deny"),
        (6, 8, "the Holy Ghost"),
        (9, 13, "when it hath had place"),
        (14, 16, "in you,"),
        (17, 20, "and ye know"),
        (21, 25, "that ye deny it,"),
        (26, 26, "behold,"),
        (27, 30, "this is a sin"),
        (31, 33, "which is unpardonable;"),
        (34, 34, "yea,"),
        (35, 39, "and whosoever"),
        (40, 42, "murdereth"),
        (43, 47, "against the light"),
        (48, 51, "and the knowledge of"),
        (52, 53, "God,"),
        (54, 59, "it is not easy for him"),
        (60, 64, "to obtain forgiveness;"),
        (65, 65, "yea,"),
        (66, 69, "I say"),
        (70, 72, "unto you,"),
        (73, 75, "my son,"),
        (76, 81, "it is not easy for him"),
        (82, 86, "to obtain a forgiveness."),
    ],
    7: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 11, "I would to God"),
        (12, 12, "indeed"),
        (13, 17, "that ye had not"),
        (18, 18, "been guilty"),
        (19, 23, "of so great a crime."),
        (24, 29, "I would not dwell upon"),
        (30, 31, "your crimes,"),
        (32, 35, "to harrow up"),
        (36, 37, "your soul,"),
        (38, 41, "if it were not"),
        (42, 44, "for your good."),
    ],
    8: [
        (0, 1, "But behold,"),
        (2, 6, "ye cannot"),
        (7, 7, "hide"),
        (8, 9, "your crimes"),
        (10, 12, "from God;"),
        (13, 16, "and except"),
        (17, 19, "ye repent"),
        (20, 23, "they will stand"),
        (24, 26, "as a testimony"),
        (27, 31, "against you"),
        (32, 35, "at the last day."),
    ],
    9: [
        (0, 1, "Now,"),
        (2, 4, "my son,"),
        (5, 7, "I would"),
        (8, 10, "that ye should repent"),
        (11, 14, "and forsake your sins,"),
        (15, 20, "and go no more"),
        (21, 21, "after"),
        (22, 26, "the lusts of your eyes,"),
        (27, 30, "but cross"),
        (31, 33, "yourself"),
        (34, 37, "in all these things;"),
        (38, 41, "for except"),
        (42, 46, "ye do this thing"),
        (47, 52, "ye can in nowise"),
        (53, 53, "inherit"),
        (54, 57, "the kingdom of"),
        (58, 59, "God."),
        (60, 60, "O,"),
        (61, 63, "remember,"),
        (64, 67, "and take it"),
        (68, 70, "upon you,"),
        (71, 75, "and cross yourself"),
        (76, 78, "in these things."),
    ],
    10: [
        (0, 4, "And I command"),
        (5, 7, "you"),
        (8, 10, "to take it"),
        (11, 13, "upon you"),
        (14, 16, "to counsel"),
        (17, 20, "with your elder brothers"),
        (21, 25, "in your undertakings;"),
        (26, 27, "for behold,"),
        (28, 31, "thou art in"),
        (32, 33, "thy youth,"),
        (34, 37, "and ye stand in need"),
        (38, 40, "to be nourished"),
        (41, 43, "by your brothers."),
        (44, 46, "And give heed"),
        (47, 50, "to their counsel."),
    ],
    11: [
        (0, 4, "Suffer not"),
        (5, 6, "thyself"),
        (7, 9, "to be led away"),
        (10, 13, "by any thing"),
        (14, 16, "vain"),
        (17, 19, "or foolish;"),
        (20, 24, "suffer not"),
        (25, 27, "the devil"),
        (28, 33, "to lead away again"),
        (34, 35, "your heart"),
        (36, 40, "after those wicked harlots."),
        (41, 41, "Behold,"),
        (42, 44, "O my son,"),
        (45, 48, "how great was"),
        (49, 50, "the iniquity"),
        (51, 53, "thou didst bring"),
        (54, 58, "upon the Zoramites;"),
        (59, 59, "for"),
        (60, 63, "when they saw"),
        (64, 66, "your conduct"),
        (67, 71, "they would not believe"),
        (72, 74, "in my words."),
    ],
    12: [
        (0, 2, "And now"),
        (3, 5, "doth say"),
        (6, 10, "the Spirit of the Lord"),
        (11, 13, "unto me:"),
        (14, 17, "Command thy children"),
        (18, 22, "to do good,"),
        (23, 28, "lest they lead away"),
        (29, 33, "the hearts of many people"),
        (34, 36, "to destruction;"),
        (37, 38, "therefore"),
        (39, 43, "I command"),
        (44, 46, "you,"),
        (47, 49, "my son,"),
        (50, 53, "in the fear of"),
        (54, 55, "God,"),
        (56, 58, "to refrain"),
        (59, 61, "from your iniquities;"),
    ],
    13: [
        (0, 4, "That ye turn"),
        (5, 7, "to the Lord"),
        (8, 11, "with all your mind,"),
        (12, 13, "all might,"),
        (14, 17, "and all your strength;"),
        (18, 22, "that ye no more"),
        (23, 24, "lead away"),
        (25, 28, "the hearts of them"),
        (29, 32, "to do wickedly;"),
        (33, 38, "but rather return"),
        (39, 42, "unto them,"),
        (43, 45, "and acknowledge"),
        (46, 47, "your faults"),
        (48, 50, "and that wrong"),
        (51, 53, "which ye have done."),
    ],
    14: [
        (0, 3, "Seek not"),
        (4, 5, "after riches"),
        (6, 10, "nor the vain things"),
        (11, 13, "of this world;"),
        (14, 15, "for behold,"),
        (16, 20, "ye cannot"),
        (21, 21, "carry"),
        (22, 23, "them"),
        (24, 26, "with you."),
    ],
    15: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 10, "I would say"),
        (11, 11, "somewhat"),
        (12, 14, "unto you"),
        (15, 17, "concerning"),
        (18, 22, "the coming of Christ."),
        (23, 23, "Behold,"),
        (24, 27, "I say"),
        (28, 30, "unto you,"),
        (31, 34, "that it is he"),
        (35, 36, "surely"),
        (37, 41, "that shall come"),
        (42, 44, "to take away the sins"),
        (45, 47, "of the world;"),
        (48, 48, "yea,"),
        (49, 53, "he cometh"),
        (54, 56, "to declare"),
        (57, 61, "glad tidings of salvation"),
        (62, 64, "unto his people."),
    ],
    16: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 9, "this was the ministry"),
        (10, 14, "unto which ye were called,"),
        (15, 17, "to declare"),
        (18, 20, "these glad tidings"),
        (21, 23, "unto this people,"),
        (24, 26, "to prepare"),
        (27, 29, "their minds;"),
        (30, 30, "or rather"),
        (31, 34, "that might"),
        (35, 36, "come"),
        (37, 39, "salvation"),
        (40, 43, "unto them,"),
        (44, 49, "that they may prepare"),
        (50, 54, "the minds of their children"),
        (55, 59, "to hear the word"),
        (60, 63, "at the time of"),
        (64, 66, "his coming."),
    ],
    17: [
        (0, 2, "And now"),
        (3, 7, "I will ease"),
        (8, 8, "somewhat"),
        (9, 10, "your mind"),
        (11, 15, "on this subject."),
        (16, 16, "Behold,"),
        (17, 19, "thou marvellest"),
        (20, 24, "why it should be"),
        (25, 29, "known so long beforehand"),
        (30, 32, "these things"),
        (33, 36, "ere they come."),
        (37, 37, "Behold,"),
        (38, 41, "I say"),
        (42, 44, "unto you,"),
        (45, 48, "is it not equal"),
        (49, 50, "the preciousness"),
        (51, 53, "unto God"),
        (54, 56, "of a soul"),
        (57, 60, "at this time"),
        (61, 65, "as of a soul"),
        (66, 69, "at the time of"),
        (70, 72, "his coming?"),
    ],
    18: [
        (0, 4, "Is it not as"),
        (5, 7, "necessary"),
        (8, 10, "that should be made known"),
        (11, 14, "the plan of"),
        (15, 16, "redemption"),
        (17, 19, "unto this people"),
        (20, 24, "as well as"),
        (25, 25, "also"),
        (26, 28, "unto their children?"),
    ],
    19: [
        (0, 4, "Is it not as"),
        (5, 6, "easy"),
        (7, 9, "for the Lord"),
        (10, 12, "to send"),
        (13, 16, "at this time"),
        (17, 19, "his angel"),
        (20, 22, "to declare"),
        (23, 25, "these glad tidings"),
        (26, 29, "unto us"),
        (30, 32, "as unto"),
        (33, 35, "our children,"),
        (36, 39, "or as at"),
        (40, 41, "the time"),
        (42, 46, "after the time is past"),
        (47, 50, "of his coming?"),
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
