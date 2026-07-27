"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 61 — Pahoran's reply to
Moroni: he explains he has not neglected the armies but has been driven from the
judgment-seat by the king-men, who have risen in rebellion, seized Zarahemla, and
made a king; Pahoran has fled to Gideon and rallies the people; he rejoices in
Moroni's greatness and calls him to come and help put down the insurrection.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_alma61.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 61

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "Behold,"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 8, "not long after"),
        (9, 11, "the sending"),
        (12, 13, "by Moroni"),
        (14, 15, "his epistle"),
        (16, 19, "unto the chief governor,"),
        (20, 22, "he received"),
        (23, 24, "an epistle"),
        (25, 27, "from Pahoran,"),
        (28, 30, "the chief governor."),
        (31, 34, "And these are the words"),
        (35, 38, "which he received:"),
    ],
    2: [
        (0, 1, "I,"),
        (2, 3, "Pahoran,"),
        (4, 8, "the chief governor of"),
        (9, 10, "this land,"),
        (11, 14, "do send"),
        (15, 16, "these words"),
        (17, 18, "unto Moroni,"),
        (19, 22, "the chief captain of"),
        (23, 24, "the army."),
        (25, 25, "Behold,"),
        (26, 29, "I say"),
        (30, 32, "unto you,"),
        (33, 33, "Moroni,"),
        (34, 37, "I do not rejoice"),
        (38, 40, "in your"),
        (41, 42, "great afflictions,"),
        (43, 43, "yea,"),
        (44, 46, "is grieved"),
        (47, 48, "my soul."),
    ],
    3: [
        (0, 1, "But behold,"),
        (2, 7, "there are those"),
        (8, 11, "who do joy"),
        (12, 14, "in your"),
        (15, 15, "afflictions,"),
        (16, 16, "yea,"),
        (17, 19, "insomuch that"),
        (20, 22, "they rose up"),
        (23, 24, "to rebel"),
        (25, 26, "against"),
        (27, 29, "me,"),
        (30, 30, "yea,"),
        (31, 35, "and all those also"),
        (36, 38, "of my people"),
        (39, 40, "who are"),
        (41, 42, "freemen,"),
        (43, 43, "yea,"),
        (44, 47, "and those"),
        (48, 52, "who have risen up"),
        (53, 55, "in rebellion"),
        (56, 59, "are exceedingly numerous."),
    ],
    4: [
        (0, 3, "And it is those"),
        (4, 7, "who sought"),
        (8, 9, "to remove"),
        (10, 11, "the judgment-seat"),
        (12, 15, "from me,"),
        (16, 19, "these are they"),
        (20, 22, "the cause of"),
        (23, 26, "this great iniquity;"),
        (27, 27, "for"),
        (28, 30, "they have used"),
        (31, 33, "great flattery,"),
        (34, 38, "and they led away"),
        (39, 40, "the hearts of"),
        (41, 44, "many people,"),
        (45, 51, "which shall become"),
        (52, 53, "the cause of"),
        (54, 55, "grievous afflictions"),
        (56, 58, "among"),
        (59, 60, "us;"),
        (61, 63, "they have withheld"),
        (64, 66, "our provisions,"),
        (67, 70, "and they have frightened"),
        (71, 74, "our freemen"),
        (75, 80, "they have not gone"),
        (81, 83, "unto you."),
    ],
    5: [
        (0, 1, "And behold,"),
        (2, 5, "they have driven me"),
        (6, 7, "out"),
        (8, 11, "before them,"),
        (12, 16, "and I have fled"),
        (17, 20, "to the land of"),
        (21, 21, "Gideon,"),
        (22, 23, "together with"),
        (24, 27, "many men"),
        (28, 30, "as I could"),
        (31, 32, "obtain."),
    ],
    6: [
        (0, 1, "And behold,"),
        (2, 5, "I have sent"),
        (6, 7, "a proclamation"),
        (8, 13, "throughout this whole part of"),
        (14, 15, "the land;"),
        (16, 17, "and behold,"),
        (18, 21, "they flock"),
        (22, 25, "to us"),
        (26, 28, "daily,"),
        (29, 32, "to their arms,"),
        (33, 36, "in the defence of"),
        (37, 39, "their country"),
        (40, 43, "and their freedom,"),
        (44, 47, "and to avenge"),
        (48, 51, "the wrongs done to us."),
    ],
    7: [
        (0, 4, "And they have come"),
        (5, 8, "unto us,"),
        (9, 11, "insomuch that"),
        (12, 14, "those"),
        (15, 18, "who stood to oppose"),
        (19, 20, "against"),
        (21, 24, "us"),
        (25, 28, "who rose up in rebellion,"),
        (29, 29, "yea,"),
        (30, 32, "insomuch that"),
        (33, 34, "they fear"),
        (35, 38, "us"),
        (39, 40, "and are afraid"),
        (41, 43, "to come out"),
        (44, 46, "to fight us."),
    ],
    8: [
        (0, 2, "They have taken"),
        (3, 4, "the land,"),
        (5, 8, "or the city,"),
        (9, 10, "of Zarahemla;"),
        (11, 13, "they have appointed"),
        (14, 15, "a king"),
        (16, 20, "over them,"),
        (21, 26, "and he has written"),
        (27, 30, "unto the king of"),
        (31, 32, "the Lamanites,"),
        (33, 37, "wherein he made"),
        (38, 39, "an alliance"),
        (40, 41, "with him;"),
        (42, 44, "which alliance"),
        (45, 48, "he consented"),
        (49, 51, "he to hold"),
        (52, 54, "the city of"),
        (55, 55, "Zarahemla,"),
        (56, 58, "which holding"),
        (59, 61, "he supposed"),
        (62, 66, "would enable"),
        (67, 69, "the Lamanites"),
        (70, 71, "to conquer"),
        (72, 77, "the remaining part of"),
        (78, 79, "the land,"),
        (80, 87, "and he shall be set"),
        (88, 90, "as the king"),
        (91, 93, "over"),
        (94, 95, "this people"),
        (96, 98, "when subdued"),
        (99, 100, "they"),
        (101, 103, "under"),
        (104, 105, "the Lamanites."),
    ],
    9: [
        (0, 2, "And now,"),
        (3, 6, "you have rebuked me"),
        (7, 9, "in your epistle,"),
        (10, 14, "but it mattereth not;"),
        (15, 19, "I am not angry,"),
        (20, 23, "but do rejoice"),
        (24, 27, "in the greatness of"),
        (28, 29, "your heart."),
        (30, 31, "I,"),
        (32, 33, "Pahoran,"),
        (34, 37, "seek not"),
        (38, 40, "for power,"),
        (41, 44, "only my wish to keep"),
        (45, 47, "my judgment-seat"),
        (48, 51, "that I may"),
        (52, 53, "I preserve"),
        (54, 54, "the rights"),
        (55, 58, "and the liberty of"),
        (59, 60, "my people."),
        (61, 64, "Stands firm still"),
        (65, 66, "my soul"),
        (67, 69, "in that liberty"),
        (70, 72, "wherein was freed"),
        (73, 74, "us"),
        (75, 77, "by God."),
    ],
    10: [
        (0, 2, "And now,"),
        (3, 3, "behold,"),
        (4, 9, "we will resist"),
        (10, 12, "against wickedness"),
        (13, 16, "even unto"),
        (17, 19, "the shedding of blood."),
        (20, 23, "We would not shed"),
        (24, 25, "the blood of"),
        (26, 27, "the Lamanites"),
        (28, 29, "if"),
        (30, 33, "they remain"),
        (34, 38, "in their own land."),
    ],
    11: [
        (0, 3, "We would not shed"),
        (4, 5, "the blood of"),
        (6, 8, "our brethren"),
        (9, 10, "if"),
        (11, 15, "they do not rise up"),
        (16, 18, "in rebellion"),
        (19, 20, "and take"),
        (21, 22, "the sword"),
        (23, 25, "against"),
        (26, 29, "us."),
    ],
    12: [
        (0, 3, "We would give"),
        (4, 6, "ourselves"),
        (7, 9, "under"),
        (10, 12, "the yoke of"),
        (13, 14, "bondage"),
        (15, 16, "if"),
        (17, 22, "this thing accorded with"),
        (23, 25, "the justice of"),
        (26, 27, "God,"),
        (28, 30, "or if also"),
        (31, 34, "he commanded"),
        (35, 36, "us"),
        (37, 41, "that we do so."),
    ],
    13: [
        (0, 1, "But behold"),
        (2, 6, "he does not command"),
        (7, 8, "us"),
        (9, 12, "that we give"),
        (13, 15, "ourselves"),
        (16, 17, "to be ruled"),
        (18, 21, "by our enemies,"),
        (22, 25, "but we should"),
        (26, 28, "we place"),
        (29, 31, "our trust"),
        (32, 34, "in him,"),
        (35, 40, "and he will deliver"),
        (41, 42, "us."),
    ],
    14: [
        (0, 1, "Therefore,"),
        (2, 5, "O my beloved brother,"),
        (6, 6, "Moroni,"),
        (7, 10, "let us resist"),
        (11, 13, "against evil,"),
        (14, 19, "and whatsoever evil"),
        (20, 23, "we cannot"),
        (24, 25, "we reject"),
        (26, 28, "with our words,"),
        (29, 29, "yea,"),
        (30, 32, "such as"),
        (33, 35, "rebellions and dissensions,"),
        (36, 38, "let us reject"),
        (39, 40, "them"),
        (41, 43, "with our swords,"),
        (44, 47, "that we may"),
        (48, 49, "we keep"),
        (50, 53, "our freedom,"),
        (54, 57, "that we may"),
        (58, 59, "we rejoice"),
        (60, 64, "in the great blessings of"),
        (65, 67, "our church,"),
        (68, 72, "and in the cause of"),
        (73, 75, "our Redeemer"),
        (76, 79, "and our God."),
    ],
    15: [
        (0, 1, "Therefore,"),
        (2, 5, "come quickly"),
        (6, 8, "unto me"),
        (9, 10, "together with"),
        (11, 14, "a few of your men,"),
        (15, 16, "but leave"),
        (17, 20, "the remaining part"),
        (21, 24, "in the care of"),
        (25, 27, "Lehi and Teancum;"),
        (28, 29, "give"),
        (30, 32, "unto them"),
        (33, 34, "the power"),
        (35, 37, "to lead"),
        (38, 39, "the war"),
        (40, 44, "in that part of"),
        (45, 46, "the land,"),
        (47, 49, "according to"),
        (50, 52, "the Spirit of"),
        (53, 54, "God,"),
        (55, 60, "which is also the spirit of"),
        (61, 62, "freedom"),
        (63, 65, "which is"),
        (66, 69, "in them."),
    ],
    16: [
        (0, 0, "Behold"),
        (1, 4, "I have sent"),
        (5, 7, "a little food"),
        (8, 11, "unto them,"),
        (12, 16, "that they may not perish,"),
        (17, 19, "until can"),
        (20, 21, "thou come"),
        (22, 24, "unto me."),
    ],
    17: [
        (0, 1, "Gather together"),
        (2, 3, "an army"),
        (4, 6, "that ye may"),
        (7, 8, "ye assemble"),
        (9, 11, "on your march"),
        (12, 13, "from here,"),
        (14, 21, "and we will go quickly"),
        (22, 24, "against"),
        (25, 27, "those dissenters,"),
        (28, 31, "in the strength of"),
        (32, 34, "our God,"),
        (35, 37, "according to"),
        (38, 39, "the faith"),
        (40, 44, "which is in us."),
    ],
    18: [
        (0, 5, "And we will take"),
        (6, 8, "the city of"),
        (9, 9, "Zarahemla,"),
        (10, 13, "that we may"),
        (14, 15, "we obtain"),
        (16, 20, "much food"),
        (21, 23, "to send"),
        (24, 27, "unto Lehi and Teancum;"),
        (28, 28, "yea,"),
        (29, 34, "we will go"),
        (35, 36, "against"),
        (37, 40, "them"),
        (41, 44, "in the strength of"),
        (45, 46, "the Lord,"),
        (47, 52, "and we will end"),
        (53, 55, "this great iniquity."),
    ],
    19: [
        (0, 2, "And now,"),
        (3, 4, "O Moroni,"),
        (5, 8, "I do joy"),
        (9, 13, "in my receiving of"),
        (14, 15, "your epistle,"),
        (16, 16, "for"),
        (17, 20, "I was greatly troubled"),
        (21, 23, "concerning"),
        (24, 27, "what should"),
        (28, 30, "we do,"),
        (31, 31, "whether"),
        (32, 33, "it be right"),
        (34, 36, "for us"),
        (37, 40, "that we go"),
        (41, 44, "against"),
        (45, 47, "our brethren."),
    ],
    20: [
        (0, 0, "But"),
        (1, 4, "thou hast said,"),
        (5, 6, "except"),
        (7, 9, "they repent,"),
        (10, 12, "hath spoken"),
        (13, 14, "the Lord"),
        (15, 17, "unto thee,"),
        (18, 20, "that thou should"),
        (21, 23, "thou go"),
        (24, 25, "against"),
        (26, 29, "them."),
    ],
    21: [
        (0, 1, "See"),
        (2, 3, "thou strengthen"),
        (4, 7, "Lehi and Teancum"),
        (8, 11, "in the Lord;"),
        (12, 13, "say"),
        (14, 17, "unto them"),
        (18, 21, "to fear not,"),
        (22, 22, "for"),
        (23, 26, "will deliver"),
        (27, 28, "them"),
        (29, 31, "the Lord,"),
        (32, 32, "yea,"),
        (33, 37, "and also all of them"),
        (38, 39, "those who"),
        (40, 42, "stand fast"),
        (43, 46, "in that liberty"),
        (47, 49, "wherein were freed"),
        (50, 51, "them"),
        (52, 54, "by God."),
        (55, 57, "And now"),
        (58, 60, "I close"),
        (61, 62, "my epistle"),
        (63, 66, "to my beloved brother,"),
        (67, 68, "Moroni."),
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
