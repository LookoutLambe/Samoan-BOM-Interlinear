"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 1 — Moroni's abridgment of the
record of the Jaredites begins: he will not give the full account from the creation but
starts with the tower; the genealogy of Ether traced back through the generations to
Jared, who came with his brother and their families and friends from the great tower at
the time the Lord confounded the language of the people; the brother of Jared cries unto
the Lord that their language not be confounded, and the Lord has compassion upon him.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 1

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "I,"),
        (5, 6, "Moroni,"),
        (7, 9, "proceed"),
        (10, 12, "to give"),
        (13, 14, "an account"),
        (15, 19, "concerning them"),
        (20, 22, "those ancient inhabitants"),
        (23, 26, "who were destroyed"),
        (27, 29, "by the hand"),
        (30, 32, "of the Lord"),
        (33, 37, "upon this land"),
        (38, 39, "in the north."),
    ],
    2: [
        (0, 4, "And I take"),
        (5, 6, "my account"),
        (7, 8, "from the plates"),
        (9, 13, "twenty and four"),
        (14, 16, "which were found"),
        (17, 20, "by the people of Limhi,"),
        (21, 23, "which is called"),
        (24, 28, "the Book of Ether."),
    ],
    3: [
        (0, 4, "And as I suppose"),
        (5, 8, "that the first part"),
        (9, 11, "of this record,"),
        (12, 14, "which speaketh"),
        (15, 16, "concerning"),
        (17, 19, "the creation"),
        (20, 22, "of the world,"),
        (23, 25, "and also of Adam,"),
        (26, 29, "and an account"),
        (30, 32, "from that time"),
        (33, 36, "even down to"),
        (37, 40, "the great tower,"),
        (41, 44, "and whatsoever things"),
        (45, 46, "happened"),
        (47, 48, "among"),
        (49, 53, "the children of men"),
        (54, 56, "until"),
        (57, 60, "that time,"),
        (61, 63, "are had"),
        (64, 68, "among the Jews—"),
    ],
    4: [
        (0, 1, "Therefore"),
        (2, 6, "I write not"),
        (7, 8, "the things"),
        (9, 10, "which happened"),
        (11, 14, "from the days of Adam"),
        (15, 17, "until"),
        (18, 21, "that time;"),
        (22, 25, "but are had"),
        (26, 27, "they"),
        (28, 31, "upon the plates;"),
        (32, 36, "and whosoever"),
        (37, 41, "shall obtain them,"),
        (42, 45, "the same"),
        (46, 50, "shall have"),
        (51, 52, "the power"),
        (53, 58, "whereby he may obtain"),
        (59, 62, "the full account."),
    ],
    5: [
        (0, 1, "But behold,"),
        (2, 6, "I give not"),
        (7, 9, "the full account,"),
        (10, 14, "but I give"),
        (15, 19, "a part of the account,"),
        (20, 22, "from the tower"),
        (23, 25, "down until"),
        (26, 29, "they were destroyed."),
    ],
    6: [
        (0, 3, "And on this wise"),
        (4, 8, "do I give"),
        (9, 10, "the account:"),
        (11, 14, "He who wrote"),
        (15, 16, "this record"),
        (17, 18, "was Ether,"),
        (19, 21, "and he"),
        (22, 26, "was a descendant"),
        (27, 28, "of Coriantor."),
    ],
    7: [
        (0, 1, "Coriantor"),
        (2, 4, "was the son"),
        (5, 6, "of Moron."),
    ],
    8: [
        (0, 2, "And Moron"),
        (3, 5, "was the son"),
        (6, 7, "of Ethem."),
    ],
    9: [
        (0, 2, "And Ethem"),
        (3, 5, "was the son"),
        (6, 7, "of Ahah."),
    ],
    10: [
        (0, 2, "And Ahah"),
        (3, 5, "was the son"),
        (6, 7, "of Seth."),
    ],
    11: [
        (0, 2, "And Seth"),
        (3, 5, "was the son"),
        (6, 7, "of Shiblon."),
    ],
    12: [
        (0, 2, "And Shiblon"),
        (3, 5, "was the son"),
        (6, 7, "of Com."),
    ],
    13: [
        (0, 2, "And Com"),
        (3, 5, "was the son"),
        (6, 7, "of Coriantum."),
    ],
    14: [
        (0, 2, "And Coriantum"),
        (3, 5, "was the son"),
        (6, 7, "of Amnigaddah."),
    ],
    15: [
        (0, 2, "And Amnigaddah"),
        (3, 5, "was the son"),
        (6, 7, "of Aaron."),
    ],
    16: [
        (0, 2, "And Aaron"),
        (3, 7, "was a descendant"),
        (8, 9, "of Heth,"),
        (10, 12, "who was the son"),
        (13, 15, "of Hearthom."),
    ],
    17: [
        (0, 2, "And Hearthom"),
        (3, 5, "was the son"),
        (6, 7, "of Lib."),
    ],
    18: [
        (0, 2, "And Lib"),
        (3, 5, "was the son"),
        (6, 7, "of Kish."),
    ],
    19: [
        (0, 2, "And Kish"),
        (3, 5, "was the son"),
        (6, 7, "of Corom."),
    ],
    20: [
        (0, 2, "And Corom"),
        (3, 5, "was the son"),
        (6, 7, "of Levi."),
    ],
    21: [
        (0, 2, "And Levi"),
        (3, 5, "was the son"),
        (6, 7, "of Kim."),
    ],
    22: [
        (0, 2, "And Kim"),
        (3, 5, "was the son"),
        (6, 7, "of Morianton."),
    ],
    23: [
        (0, 2, "And Morianton"),
        (3, 5, "was a descendant"),
        (6, 7, "of Riplakish."),
    ],
    24: [
        (0, 2, "And Riplakish"),
        (3, 5, "was the son"),
        (6, 7, "of Shez."),
    ],
    25: [
        (0, 2, "And Shez"),
        (3, 5, "was the son"),
        (6, 7, "of Heth."),
    ],
    26: [
        (0, 2, "And Heth"),
        (3, 5, "was the son"),
        (6, 7, "of Com."),
    ],
    27: [
        (0, 2, "And Com"),
        (3, 5, "was the son"),
        (6, 7, "of Coriantum."),
    ],
    28: [
        (0, 2, "And Coriantum"),
        (3, 5, "was the son"),
        (6, 7, "of Emer."),
    ],
    29: [
        (0, 2, "And Emer"),
        (3, 5, "was the son"),
        (6, 7, "of Omer."),
    ],
    30: [
        (0, 2, "And Omer"),
        (3, 5, "was the son"),
        (6, 7, "of Shule."),
    ],
    31: [
        (0, 2, "And Shule"),
        (3, 5, "was the son"),
        (6, 7, "of Kib."),
    ],
    32: [
        (0, 2, "And Kib"),
        (3, 5, "was the son"),
        (6, 7, "of Orihah,"),
        (8, 11, "who was the son"),
        (12, 13, "of Jared;"),
    ],
    33: [
        (0, 2, "This Jared"),
        (3, 5, "came forth"),
        (6, 8, "with his brother,"),
        (9, 12, "and their families,"),
        (13, 15, "together with others"),
        (16, 19, "and their families,"),
        (20, 23, "from the great tower,"),
        (24, 26, "at the time"),
        (27, 29, "when confounded"),
        (30, 32, "the Lord"),
        (33, 36, "the language of the people,"),
        (37, 39, "and sware"),
        (40, 42, "in his wrath"),
        (43, 46, "should be scattered"),
        (47, 48, "them"),
        (49, 51, "upon"),
        (52, 54, "all the earth;"),
        (55, 58, "and according to"),
        (59, 63, "the word of the Lord,"),
        (64, 66, "were scattered"),
        (67, 67, "the people."),
    ],
    34: [
        (0, 2, "And because"),
        (3, 6, "the brother of Jared"),
        (7, 11, "was a large man"),
        (12, 13, "and strong,"),
        (14, 17, "and a man"),
        (18, 20, "greatly beloved"),
        (21, 23, "of the Lord,"),
        (24, 26, "said"),
        (27, 27, "Jared,"),
        (28, 29, "his brother,"),
        (30, 32, "unto him:"),
        (33, 34, "Cry"),
        (35, 37, "unto the Lord,"),
        (38, 41, "that he confound not"),
        (42, 45, "us,"),
        (46, 50, "that we may not"),
        (51, 52, "understand"),
        (53, 55, "our words."),
    ],
    35: [
        (0, 3, "And it came to pass that"),
        (4, 5, "cried"),
        (6, 9, "the brother of Jared"),
        (10, 12, "unto the Lord,"),
        (13, 16, "and had compassion"),
        (17, 18, "the Lord"),
        (19, 20, "upon Jared;"),
        (21, 22, "therefore"),
        (23, 28, "he confounded not"),
        (29, 32, "Jared's language;"),
        (33, 36, "and was not confounded"),
        (37, 37, "Jared"),
        (38, 40, "and his brother."),
    ],
    36: [
        (0, 4, "Then said"),
        (5, 6, "Jared"),
        (7, 9, "unto his brother:"),
        (10, 12, "Cry again"),
        (13, 15, "unto the Lord,"),
        (16, 17, "and perhaps"),
        (18, 24, "he will turn away"),
        (25, 26, "his anger"),
        (27, 31, "from them"),
        (32, 35, "our friends,"),
        (36, 41, "that he confound not"),
        (42, 44, "their language."),
    ],
    37: [
        (0, 3, "And it came to pass that"),
        (4, 5, "cried"),
        (6, 9, "the brother of Jared"),
        (10, 12, "unto the Lord,"),
        (13, 16, "and had compassion"),
        (17, 18, "the Lord"),
        (19, 21, "upon their friends,"),
        (22, 26, "and their families also,"),
        (27, 30, "that were not confounded"),
        (31, 32, "they."),
    ],
    38: [
        (0, 3, "And it came to pass that"),
        (4, 6, "again spake"),
        (7, 7, "Jared"),
        (8, 10, "unto his brother,"),
        (11, 12, "saying:"),
        (13, 16, "Go and inquire"),
        (17, 19, "of the Lord,"),
        (20, 20, "whether"),
        (21, 26, "he will drive out"),
        (27, 28, "us"),
        (29, 31, "out of the land,"),
        (32, 33, "and if"),
        (34, 39, "he will drive out"),
        (40, 41, "us"),
        (42, 44, "from the land,"),
        (45, 46, "cry"),
        (47, 49, "unto him"),
        (50, 52, "whither"),
        (53, 59, "we shall go."),
        (60, 62, "And who"),
        (63, 65, "knoweth"),
        (66, 66, "but"),
        (67, 71, "will lead"),
        (72, 73, "us"),
        (74, 76, "the Lord"),
        (77, 79, "into a land"),
        (80, 83, "which is most choice"),
        (84, 86, "above"),
        (87, 89, "all the earth?"),
        (90, 93, "And if it so be,"),
        (94, 96, "let us have faith"),
        (97, 99, "in the Lord,"),
        (100, 103, "that we may receive"),
        (104, 105, "that land"),
        (106, 108, "to be"),
        (109, 111, "our inheritance."),
    ],
    39: [
        (0, 3, "And it came to pass that"),
        (4, 5, "cried"),
        (6, 9, "the brother of Jared"),
        (10, 12, "unto the Lord"),
        (13, 15, "according to"),
        (16, 17, "that which"),
        (18, 20, "had been spoken"),
        (21, 25, "by the mouth of Jared."),
    ],
    40: [
        (0, 3, "And it came to pass that"),
        (4, 5, "hearkened"),
        (6, 7, "the Lord"),
        (8, 12, "unto the brother of Jared,"),
        (13, 15, "and had compassion"),
        (16, 18, "upon him,"),
        (19, 21, "and said"),
        (22, 24, "unto him:"),
    ],
    41: [
        (0, 2, "Go to"),
        (3, 5, "and gather together"),
        (6, 8, "thy flocks,"),
        (9, 11, "both the male"),
        (12, 14, "and the female,"),
        (15, 18, "of every kind;"),
        (19, 21, "and also seed"),
        (22, 25, "of every kind"),
        (26, 28, "of the earth;"),
        (29, 31, "and thy families;"),
        (32, 35, "and also thy brother"),
        (36, 37, "Jared,"),
        (38, 40, "and his family;"),
        (41, 44, "and also thy friends"),
        (45, 48, "and their families,"),
        (49, 52, "and the friends of Jared"),
        (53, 56, "and their families."),
    ],
    42: [
        (0, 3, "And when"),
        (4, 5, "thou hast done"),
        (6, 7, "this thing,"),
        (8, 11, "thou shalt go"),
        (12, 16, "before them"),
        (17, 18, "down"),
        (19, 22, "into the valley"),
        (23, 24, "which is"),
        (25, 28, "northward."),
        (29, 31, "And there"),
        (32, 37, "will I meet"),
        (38, 39, "with thee,"),
        (40, 40, "and"),
        (41, 47, "I will go"),
        (48, 50, "before thee"),
        (51, 53, "into a land"),
        (54, 57, "which is choice"),
        (58, 60, "above"),
        (61, 65, "all the lands of the earth."),
    ],
    43: [
        (0, 2, "And there"),
        (3, 8, "will I bless"),
        (9, 12, "thee and thy seed,"),
        (13, 15, "and raise up"),
        (16, 17, "unto me"),
        (18, 20, "of thy seed,"),
        (21, 23, "and of the seed"),
        (24, 26, "of thy brother,"),
        (27, 31, "and of them"),
        (32, 33, "who"),
        (34, 38, "shall go"),
        (39, 41, "together with thee,"),
        (42, 44, "a great nation."),
        (45, 45, "And"),
        (46, 49, "there shall be no"),
        (50, 51, "nation"),
        (52, 54, "greater"),
        (55, 59, "than this nation"),
        (60, 65, "which I will raise up"),
        (66, 67, "unto me"),
        (68, 70, "of thy seed,"),
        (71, 73, "upon"),
        (74, 76, "all the earth."),
        (77, 81, "And thus shall it be"),
        (82, 84, "that I do"),
        (85, 87, "unto thee"),
        (88, 89, "because of"),
        (90, 92, "this long time"),
        (93, 97, "which thou hast cried"),
        (98, 100, "unto me."),
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
