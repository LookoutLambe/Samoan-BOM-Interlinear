"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 14 — a great curse comes upon
the land because of the iniquity of the people, such that whoso laid down his tool could
not find it again; every man kept his sword to defend his property; Coriantumr wars against
Gilead, then Lib, then Shiz, who sweeps the earth before him, and the whole face of the
land is covered with dead bodies as the two mighty armies pursue one another to the death.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether14.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 14

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 7, "there began to be"),
        (8, 11, "a great curse"),
        (12, 15, "upon"),
        (16, 17, "all the land"),
        (18, 21, "because of the iniquity"),
        (22, 23, "of the people,"),
        (24, 27, "that when laid"),
        (28, 30, "a man"),
        (31, 32, "his tool"),
        (33, 36, "or his sword"),
        (37, 41, "upon his shelf,"),
        (42, 45, "or upon"),
        (46, 47, "a place"),
        (48, 51, "he desired"),
        (52, 54, "to store it,"),
        (55, 55, "behold,"),
        (56, 58, "the day"),
        (59, 61, "that came next,"),
        (62, 64, "was not able"),
        (65, 68, "for him to regain it,"),
        (69, 73, "because so great"),
        (74, 76, "was the curse"),
        (77, 81, "upon the land."),
    ],
    2: [
        (0, 3, "Wherefore"),
        (4, 6, "held fast"),
        (7, 9, "every man"),
        (10, 12, "his own goods,"),
        (13, 15, "in his hands,"),
        (16, 20, "and would not borrow"),
        (21, 25, "nor lend;"),
        (26, 30, "and every man"),
        (31, 34, "grasped the handle"),
        (35, 37, "of his sword"),
        (38, 41, "in his right hand,"),
        (42, 44, "for the defence"),
        (45, 47, "of his property"),
        (48, 51, "and his own life,"),
        (52, 53, "and the lives"),
        (54, 58, "of his wives and children."),
    ],
    3: [
        (0, 2, "And now,"),
        (3, 5, "after had passed"),
        (6, 8, "the space of"),
        (9, 11, "two years,"),
        (12, 15, "and after came"),
        (16, 19, "the death of Shared,"),
        (20, 20, "behold,"),
        (21, 23, "there rose"),
        (24, 27, "the brother of Shared"),
        (28, 31, "and he fought"),
        (32, 33, "with Coriantumr,"),
        (34, 37, "wherein was beaten"),
        (38, 39, "he"),
        (40, 41, "by Coriantumr"),
        (42, 46, "and pursued him"),
        (47, 49, "until reaching"),
        (50, 54, "the wilderness of Akish."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 8, "fought the brother of Shared"),
        (9, 10, "against him"),
        (11, 15, "in the wilderness of Akish;"),
        (16, 19, "and it came to pass"),
        (20, 22, "exceeding sore was"),
        (23, 24, "the battle,"),
        (25, 29, "and thousands upon thousands"),
        (30, 32, "did fall"),
        (33, 35, "by the sword."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 6, "besieged Coriantumr"),
        (7, 8, "the wilderness;"),
        (9, 12, "and marched forth"),
        (13, 16, "the brother of Shared"),
        (17, 19, "from the wilderness"),
        (20, 22, "by night,"),
        (23, 26, "and slew a portion"),
        (27, 31, "of Coriantumr's army,"),
        (32, 32, "while"),
        (33, 35, "they were drunk."),
    ],
    6: [
        (0, 3, "And went forth"),
        (4, 5, "he"),
        (6, 10, "to the land of Moron,"),
        (11, 13, "and dwelt"),
        (14, 16, "he himself"),
        (17, 21, "upon the throne"),
        (22, 23, "of Coriantumr."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Coriantumr dwelt"),
        (6, 8, "with his army"),
        (9, 11, "in the wilderness"),
        (12, 15, "for the space of"),
        (16, 18, "two years,"),
        (19, 23, "wherein he obtained"),
        (24, 26, "great strength"),
        (27, 29, "for his army."),
    ],
    8: [
        (0, 1, "Now,"),
        (2, 6, "the brother of Shared,"),
        (7, 9, "whose name"),
        (10, 11, "was Gilead,"),
        (12, 15, "he also gained"),
        (16, 18, "great strength"),
        (19, 21, "to his army,"),
        (22, 23, "because of"),
        (24, 25, "secret combinations."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 6, "was slain he"),
        (7, 10, "by his high priest"),
        (11, 14, "while he sat"),
        (15, 19, "upon his throne."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 6, "was slain he"),
        (7, 9, "by one"),
        (10, 12, "of the secret combinations"),
        (13, 15, "within"),
        (16, 18, "a secret way,"),
        (19, 22, "and gained"),
        (23, 25, "for himself"),
        (26, 27, "the kingdom;"),
        (28, 31, "and his name"),
        (32, 33, "was Lib;"),
        (34, 36, "and Lib"),
        (37, 39, "was a man"),
        (40, 42, "of unusual tallness,"),
        (43, 47, "greater than"),
        (48, 51, "any other man"),
        (52, 54, "among"),
        (55, 57, "all the nation."),
    ],
    11: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the first year"),
        (7, 8, "of Lib,"),
        (9, 12, "Coriantumr came"),
        (13, 15, "up into"),
        (16, 19, "the land of Moron,"),
        (20, 23, "and fought against Lib."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he fought"),
        (7, 8, "with Lib,"),
        (9, 12, "wherein was struck"),
        (13, 14, "by Lib"),
        (15, 16, "his arm"),
        (17, 20, "whereby was wounded"),
        (21, 22, "he;"),
        (23, 26, "nevertheless,"),
        (27, 31, "pressed onward"),
        (32, 35, "the army of Coriantumr"),
        (36, 39, "upon Lib,"),
        (40, 42, "so that"),
        (43, 45, "he fled"),
        (46, 47, "to the borders"),
        (48, 52, "upon the seashore."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 6, "was pursued he"),
        (7, 8, "by Coriantumr;"),
        (9, 13, "and he battled"),
        (14, 15, "with Lib"),
        (16, 20, "upon the seashore."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 6, "smote Lib"),
        (7, 10, "the army of Coriantumr,"),
        (11, 13, "so that"),
        (14, 17, "they again fled"),
        (18, 22, "to the wilderness of Akish."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 6, "was pursued he"),
        (7, 8, "by Lib"),
        (9, 11, "until"),
        (12, 15, "he came"),
        (16, 20, "to the plains of Agosh."),
        (21, 25, "And Coriantumr carried"),
        (26, 27, "all the people"),
        (28, 30, "together with him"),
        (31, 34, "while he fled"),
        (35, 38, "before Lib,"),
        (39, 42, "to that part"),
        (43, 45, "of the land"),
        (46, 49, "where he fled"),
        (50, 51, "unto."),
    ],
    16: [
        (0, 4, "And when came"),
        (5, 6, "he"),
        (7, 11, "to the plains of Agosh,"),
        (12, 15, "he fought"),
        (16, 17, "with Lib,"),
        (18, 21, "and he struck"),
        (22, 23, "him"),
        (24, 28, "until he was slain;"),
        (29, 32, "nevertheless,"),
        (33, 34, "came forth"),
        (35, 38, "the brother of Lib"),
        (39, 42, "against Coriantumr"),
        (43, 47, "in his place,"),
        (48, 51, "and it came to pass"),
        (52, 55, "exceeding sore was"),
        (56, 57, "the war,"),
        (58, 62, "wherein fled again"),
        (63, 63, "Coriantumr"),
        (64, 68, "before the army"),
        (69, 73, "of the brother of Lib."),
    ],
    17: [
        (0, 4, "Now the name"),
        (5, 9, "of the brother of Lib"),
        (10, 11, "was named"),
        (12, 13, "Shiz."),
        (14, 17, "And it came to pass"),
        (18, 20, "pursued Shiz"),
        (21, 22, "after Coriantumr,"),
        (23, 27, "and he did throw down"),
        (28, 30, "many cities,"),
        (31, 34, "and he did kill"),
        (35, 37, "women and children,"),
        (38, 40, "and he burned"),
        (41, 41, "the cities."),
    ],
    18: [
        (0, 3, "And there came"),
        (4, 7, "over all the land"),
        (8, 11, "the dread of Shiz;"),
        (12, 12, "yea,"),
        (13, 15, "there went forth"),
        (16, 17, "a cry"),
        (18, 21, "through all the land—"),
        (22, 23, "Who"),
        (24, 28, "is able to stand"),
        (29, 33, "before the army"),
        (34, 35, "of Shiz?"),
        (36, 36, "Behold,"),
        (37, 40, "he doth sweep away"),
        (41, 42, "the land"),
        (43, 45, "before him!"),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 5, "began"),
        (6, 8, "to flock together"),
        (9, 9, "the people"),
        (10, 12, "unto his armies,"),
        (13, 16, "upon"),
        (17, 18, "all the land."),
    ],
    20: [
        (0, 2, "And were divided"),
        (3, 4, "they;"),
        (5, 7, "a part"),
        (8, 10, "of them"),
        (11, 13, "did flee"),
        (14, 18, "to the army of Shiz,"),
        (19, 22, "and a portion"),
        (23, 25, "of them"),
        (26, 28, "did flee"),
        (29, 33, "to the army of Coriantumr."),
    ],
    21: [
        (0, 2, "And because of"),
        (3, 5, "the great size"),
        (6, 8, "and the length"),
        (9, 11, "of the war,"),
        (12, 15, "and long had lasted"),
        (16, 17, "the sight"),
        (18, 21, "of the shedding of blood"),
        (22, 24, "and the dead,"),
        (25, 29, "it came that was covered"),
        (30, 34, "all the face of the land"),
        (35, 39, "with the bodies of the dead."),
    ],
    22: [
        (0, 2, "And so swift"),
        (3, 5, "and so speedy"),
        (6, 7, "was the war"),
        (8, 9, "there was not"),
        (10, 13, "any left"),
        (14, 15, "to bury"),
        (16, 17, "the dead,"),
        (18, 18, "but"),
        (19, 22, "they went forth"),
        (23, 24, "onward"),
        (25, 28, "from the shedding"),
        (29, 31, "of blood"),
        (32, 34, "to the shedding"),
        (35, 37, "of blood,"),
        (38, 40, "and left"),
        (41, 43, "the bodies of men,"),
        (44, 46, "women, and children"),
        (47, 49, "spread abroad"),
        (50, 54, "upon the land,"),
        (55, 58, "to become meat"),
        (59, 63, "for the flesh-worms."),
    ],
    23: [
        (0, 3, "And went forth"),
        (4, 6, "their stench"),
        (7, 11, "upon the land,"),
        (12, 12, "yea,"),
        (13, 17, "upon all the land"),
        (18, 20, "the whole of it;"),
        (21, 24, "wherefore"),
        (25, 27, "were troubled"),
        (28, 28, "the people"),
        (29, 31, "by day"),
        (32, 34, "and by night,"),
        (35, 38, "because of the stench"),
        (39, 41, "that was there."),
    ],
    24: [
        (0, 3, "Nevertheless,"),
        (4, 8, "Shiz left not off"),
        (9, 12, "the pursuing of Coriantumr;"),
        (13, 17, "for he swore"),
        (18, 22, "that he would repay"),
        (23, 26, "upon Coriantumr"),
        (27, 31, "the blood of his brother,"),
        (32, 35, "who had been slain,"),
        (36, 38, "and the word"),
        (39, 41, "of the Lord"),
        (42, 45, "which came"),
        (46, 47, "unto Ether"),
        (48, 49, "that saith"),
        (50, 55, "shall not perish"),
        (56, 56, "Coriantumr"),
        (57, 59, "by the sword."),
    ],
    25: [
        (0, 2, "And so"),
        (3, 6, "we do see"),
        (7, 10, "did indeed visit"),
        (11, 12, "the Lord"),
        (13, 16, "unto them"),
        (17, 19, "in the fulness"),
        (20, 22, "of his anger,"),
        (23, 25, "and prepared"),
        (26, 29, "by their iniquity"),
        (30, 34, "and their abominations"),
        (35, 36, "a way"),
        (37, 40, "for their destruction"),
        (41, 42, "everlasting."),
    ],
    26: [
        (0, 3, "And it came to pass that"),
        (4, 6, "pursued Shiz"),
        (7, 8, "after Coriantumr"),
        (9, 11, "toward the east,"),
        (12, 15, "even until reaching"),
        (16, 17, "the borders"),
        (18, 22, "by the seashore,"),
        (23, 25, "and there"),
        (26, 30, "he fought"),
        (31, 32, "against Shiz"),
        (33, 36, "for the space of"),
        (37, 39, "three days."),
    ],
    27: [
        (0, 4, "And so dreadful was"),
        (5, 6, "the slaughter"),
        (7, 9, "among"),
        (10, 12, "Shiz's armies"),
        (13, 16, "began to fear"),
        (17, 17, "the people,"),
        (18, 21, "and began to flee"),
        (22, 24, "from before"),
        (25, 27, "Coriantumr's armies;"),
        (28, 32, "and they fled"),
        (33, 37, "to the land of Corihor,"),
        (38, 41, "and swept away"),
        (42, 44, "before them"),
        (45, 48, "the inhabitants there,"),
        (49, 52, "all of them"),
        (53, 54, "who"),
        (55, 58, "were unwilling to join"),
        (59, 62, "together with them."),
    ],
    28: [
        (0, 3, "And they pitched"),
        (4, 6, "their tents"),
        (7, 11, "in the valley of Corihor;"),
        (12, 16, "and Coriantumr set up"),
        (17, 18, "his tents"),
        (19, 23, "in the valley of Shurr."),
        (24, 25, "Now"),
        (26, 30, "the valley of Shurr"),
        (31, 32, "was near"),
        (33, 37, "the hill of Comnor;"),
        (38, 41, "wherefore"),
        (42, 45, "did assemble"),
        (46, 47, "Coriantumr"),
        (48, 49, "his armies"),
        (50, 54, "upon the hill"),
        (55, 56, "of Comnor,"),
        (57, 59, "and sounded"),
        (60, 61, "a horn"),
        (62, 65, "to the armies of Shiz"),
        (66, 69, "to summon"),
        (70, 73, "unto them"),
        (74, 76, "to come forth"),
        (77, 78, "to battle."),
    ],
    29: [
        (0, 3, "And it came to pass that"),
        (4, 6, "they came,"),
        (7, 10, "but were driven back"),
        (11, 12, "they;"),
        (13, 17, "and they came forth"),
        (18, 18, "again,"),
        (19, 23, "and again were driven back"),
        (24, 25, "they"),
        (26, 30, "the second time."),
        (31, 34, "And it came to pass that"),
        (35, 38, "they came once more"),
        (39, 43, "the third time,"),
        (44, 47, "and it came to pass"),
        (48, 50, "exceeding sore was"),
        (51, 52, "the battle."),
    ],
    30: [
        (0, 3, "And it came to pass that"),
        (4, 6, "smote Shiz"),
        (7, 8, "Coriantumr"),
        (9, 12, "so that"),
        (13, 15, "he inflicted"),
        (16, 18, "upon him"),
        (19, 23, "many deep wounds;"),
        (24, 26, "and Coriantumr,"),
        (27, 30, "because of the much"),
        (31, 35, "of his blood that was shed,"),
        (36, 37, "fainted,"),
        (38, 41, "and was borne away"),
        (42, 43, "he"),
        (44, 47, "as if he were dead."),
    ],
    31: [
        (0, 1, "Now"),
        (2, 6, "because so many"),
        (7, 8, "of men,"),
        (9, 11, "women, and children"),
        (12, 13, "were killed"),
        (14, 18, "on both sides,"),
        (19, 23, "wherefore did charge"),
        (24, 25, "Shiz"),
        (26, 27, "his people"),
        (28, 33, "that they should not chase"),
        (34, 36, "the armies of Coriantumr;"),
        (37, 40, "wherefore,"),
        (41, 42, "they"),
        (43, 46, "returned again"),
        (47, 50, "to their camp."),
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
