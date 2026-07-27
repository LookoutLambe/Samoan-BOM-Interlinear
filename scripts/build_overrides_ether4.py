"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 4 — Moroni is commanded to seal
up the writings of the brother of Jared, which contained a revelation of all things from
the foundation of the world to the end. They are not to come to the Gentiles in their
unbelief; they shall not go forth until the Gentiles repent and become clean. The Lord
promises that when they exercise faith as the brother of Jared did, the sealed things
shall be made manifest; he invites all to come unto him, believe, and receive the greater
things.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether4.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 4

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And commanded"),
        (3, 5, "the Lord"),
        (6, 9, "the brother of Jared"),
        (10, 14, "that he go down"),
        (15, 17, "from the mount"),
        (18, 19, "from before"),
        (20, 22, "the Lord,"),
        (23, 25, "and write the things"),
        (26, 28, "which he had seen;"),
        (29, 31, "and were forbidden"),
        (32, 36, "that they should come"),
        (37, 41, "unto the children of men"),
        (42, 44, "until after"),
        (45, 48, "he was lifted up"),
        (49, 53, "upon the cross;"),
        (54, 58, "and for this reason"),
        (59, 61, "were preserved"),
        (62, 63, "them"),
        (64, 68, "by king Mosiah,"),
        (69, 73, "that they come not"),
        (74, 76, "unto the world"),
        (77, 79, "until after"),
        (80, 83, "Christ should show"),
        (84, 86, "himself"),
        (87, 89, "unto his people."),
    ],
    2: [
        (0, 4, "And after that"),
        (5, 7, "had truly appeared"),
        (8, 9, "Christ"),
        (10, 12, "himself"),
        (13, 15, "unto his people"),
        (16, 18, "he commanded"),
        (19, 20, "that should be shown"),
        (21, 23, "they."),
    ],
    3: [
        (0, 2, "And now,"),
        (3, 6, "after that,"),
        (7, 8, "have dwindled"),
        (9, 11, "all of them"),
        (12, 15, "in unbelief;"),
        (16, 20, "and there is none"),
        (21, 22, "save"),
        (23, 24, "the Lamanites,"),
        (25, 28, "and they have rejected"),
        (29, 32, "the gospel of Christ;"),
        (33, 34, "therefore"),
        (35, 38, "am I commanded"),
        (39, 42, "that I hide up again"),
        (43, 44, "them"),
        (45, 47, "in the earth."),
    ],
    4: [
        (0, 0, "Behold,"),
        (1, 3, "I have written"),
        (4, 6, "upon these plates"),
        (7, 9, "the very things"),
        (10, 14, "which he saw"),
        (15, 18, "the brother of Jared;"),
        (19, 20, "and"),
        (21, 24, "there never were"),
        (25, 29, "greater things"),
        (30, 32, "made manifest"),
        (33, 35, "than those"),
        (36, 37, "which were shown"),
        (38, 42, "unto the brother of Jared."),
    ],
    5: [
        (0, 3, "Wherefore"),
        (4, 6, "hath commanded"),
        (7, 7, "me"),
        (8, 10, "the Lord"),
        (11, 12, "to write"),
        (13, 14, "these things;"),
        (15, 18, "and I have written"),
        (19, 20, "them."),
        (21, 25, "And he commanded me"),
        (26, 28, "that I should seal up"),
        (29, 30, "them;"),
        (31, 36, "and he also commanded me"),
        (37, 39, "that I should seal up"),
        (40, 42, "their interpretation;"),
        (43, 46, "wherefore"),
        (47, 50, "I have sealed up"),
        (51, 52, "the interpreters,"),
        (53, 55, "according to"),
        (56, 60, "the commandment of the Lord."),
    ],
    6: [
        (0, 3, "For said"),
        (4, 5, "the Lord"),
        (6, 8, "unto me:"),
        (9, 14, "shall not go forth"),
        (15, 16, "them"),
        (17, 18, "unto the Gentiles"),
        (19, 23, "until the day"),
        (24, 27, "when they repent"),
        (28, 31, "of their iniquity,"),
        (32, 33, "and become clean"),
        (34, 38, "before the Lord."),
    ],
    7: [
        (0, 3, "And in that day"),
        (4, 9, "when they shall exercise"),
        (10, 11, "faith"),
        (12, 14, "in me,"),
        (15, 18, "saith"),
        (19, 20, "the Lord,"),
        (21, 24, "even as did"),
        (25, 29, "the brother of Jared,"),
        (30, 34, "that they may be sanctified"),
        (35, 36, "them"),
        (37, 39, "unto me,"),
        (40, 41, "then"),
        (42, 45, "will I manifest"),
        (46, 49, "unto them"),
        (50, 50, "the things"),
        (51, 54, "which he saw"),
        (55, 58, "the brother of Jared,"),
        (59, 61, "even unto"),
        (62, 65, "the unfolding"),
        (66, 69, "of all my revelations"),
        (70, 73, "unto them,"),
        (74, 77, "saith"),
        (78, 79, "Jesus Christ,"),
        (80, 84, "the Son of God,"),
        (85, 87, "the Father"),
        (88, 90, "of heaven"),
        (91, 93, "and of earth,"),
        (94, 96, "and all things"),
        (97, 99, "that are therein."),
    ],
    8: [
        (0, 2, "And he"),
        (3, 7, "that fighteth against"),
        (8, 10, "the word"),
        (11, 13, "of the Lord,"),
        (14, 17, "let him be accursed;"),
        (18, 19, "and he"),
        (20, 23, "that denieth"),
        (24, 25, "these things,"),
        (26, 29, "let him be accursed;"),
        (30, 30, "for"),
        (31, 36, "I will not manifest"),
        (37, 40, "unto them"),
        (41, 44, "greater things,"),
        (45, 48, "saith"),
        (49, 50, "Jesus Christ;"),
        (51, 53, "for I am"),
        (54, 58, "he who speaketh."),
    ],
    9: [
        (0, 3, "And at my command"),
        (4, 5, "are opened"),
        (6, 8, "and shut"),
        (9, 10, "the heavens;"),
        (11, 14, "and at my word"),
        (15, 17, "doth shake"),
        (18, 19, "the earth;"),
        (20, 23, "and at my command"),
        (24, 27, "shall pass away"),
        (28, 31, "the inhabitants thereof,"),
        (32, 34, "even as"),
        (35, 37, "they pass"),
        (38, 40, "as by fire."),
    ],
    10: [
        (0, 2, "And he"),
        (3, 7, "that believeth not"),
        (8, 10, "my words,"),
        (11, 13, "believeth not"),
        (14, 16, "my disciples;"),
        (17, 20, "and if it so be"),
        (21, 26, "that I do not speak,"),
        (27, 28, "judge ye;"),
        (29, 29, "for"),
        (30, 34, "ye shall know"),
        (35, 38, "at the last day,"),
        (39, 42, "that it is I myself"),
        (43, 48, "who am speaking."),
    ],
    11: [
        (0, 2, "But he"),
        (3, 6, "that believeth"),
        (7, 9, "these things"),
        (10, 14, "which I have spoken,"),
        (15, 17, "him"),
        (18, 23, "will I visit"),
        (24, 25, "thereto"),
        (26, 27, "with manifestations"),
        (28, 30, "of my Spirit,"),
        (31, 31, "and"),
        (32, 36, "he shall know"),
        (37, 38, "and testify."),
        (39, 39, "For"),
        (40, 45, "he shall know"),
        (46, 49, "that these things are true,"),
        (50, 53, "because of my Spirit;"),
        (54, 58, "for it persuadeth"),
        (59, 59, "men"),
        (60, 62, "to do"),
        (63, 64, "good."),
    ],
    12: [
        (0, 3, "And whatsoever thing"),
        (4, 6, "persuadeth men"),
        (7, 10, "to do good,"),
        (11, 12, "cometh from"),
        (13, 16, "me;"),
        (17, 21, "for there is none"),
        (22, 24, "from whom cometh"),
        (25, 26, "good"),
        (27, 29, "save it be"),
        (30, 33, "from me."),
        (34, 37, "I myself am he"),
        (38, 41, "who guideth"),
        (42, 42, "men"),
        (43, 46, "to all that is good;"),
        (47, 48, "he"),
        (49, 53, "who believeth not"),
        (54, 56, "my words"),
        (57, 62, "believeth not"),
        (63, 66, "in me—"),
        (67, 70, "who I am;"),
        (71, 73, "and he"),
        (74, 77, "believeth not"),
        (78, 80, "in me"),
        (81, 85, "believeth not"),
        (86, 88, "the Father"),
        (89, 90, "who"),
        (91, 94, "did send me."),
        (95, 96, "For behold,"),
        (97, 98, "I am"),
        (99, 101, "the Father,"),
        (102, 103, "I am"),
        (104, 106, "the light,"),
        (107, 109, "and the life,"),
        (110, 112, "and the truth"),
        (113, 115, "of the world."),
    ],
    13: [
        (0, 2, "Come"),
        (3, 5, "unto me,"),
        (6, 9, "O ye Gentiles,"),
        (10, 10, "and"),
        (11, 16, "I will manifest"),
        (17, 19, "unto you"),
        (20, 23, "the greater things,"),
        (24, 26, "the knowledge"),
        (27, 28, "which is hidden"),
        (29, 30, "because of"),
        (31, 33, "unbelief."),
    ],
    14: [
        (0, 2, "Come"),
        (3, 5, "unto me,"),
        (6, 8, "O ye house"),
        (9, 11, "of Israel,"),
        (12, 12, "and"),
        (13, 17, "shall be shown"),
        (18, 20, "unto you"),
        (21, 22, "the great things"),
        (23, 24, "which hath treasured"),
        (25, 27, "the Father"),
        (28, 29, "for you,"),
        (30, 32, "from the foundation"),
        (33, 35, "of the world;"),
        (36, 40, "and it hath not come"),
        (41, 43, "unto you,"),
        (44, 45, "because of"),
        (46, 48, "unbelief."),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 4, "when ye shall rend"),
        (5, 6, "that veil"),
        (7, 10, "of unbelief"),
        (11, 14, "which doth cause"),
        (15, 17, "to abide continually"),
        (18, 22, "in your evil state"),
        (23, 25, "of wickedness,"),
        (26, 28, "and the hardness"),
        (29, 31, "of heart,"),
        (32, 34, "and the blindness"),
        (35, 37, "of mind,"),
        (38, 42, "then shall be shown"),
        (43, 45, "unto you"),
        (46, 50, "the great and marvelous things"),
        (51, 54, "which have been hidden"),
        (55, 57, "from the foundation"),
        (58, 60, "of the world"),
        (61, 64, "from you—"),
        (65, 65, "yea,"),
        (66, 70, "when ye shall call"),
        (71, 73, "upon the Father"),
        (74, 76, "in my name,"),
        (77, 80, "with a broken heart"),
        (81, 84, "and a contrite spirit,"),
        (85, 89, "then shall ye know"),
        (90, 91, "hath remembered"),
        (92, 94, "the Father"),
        (95, 97, "the covenant"),
        (98, 100, "which he made"),
        (101, 104, "unto your fathers,"),
        (105, 107, "O house"),
        (108, 109, "of Israel."),
    ],
    16: [
        (0, 1, "And then"),
        (2, 5, "shall be unfolded"),
        (6, 10, "in the eyes of all men"),
        (11, 12, "my revelations,"),
        (13, 14, "the revelations which"),
        (15, 17, "I did command"),
        (18, 19, "to write"),
        (20, 24, "my servant John."),
        (25, 26, "Remember,"),
        (27, 30, "when ye behold"),
        (31, 33, "these things,"),
        (34, 38, "ye shall know"),
        (39, 42, "that hath come"),
        (43, 44, "the time"),
        (45, 48, "shall be manifested"),
        (49, 52, "in very deed"),
        (53, 54, "them."),
    ],
    17: [
        (0, 1, "Therefore,"),
        (2, 5, "when ye shall receive"),
        (6, 7, "this record"),
        (8, 11, "ye may"),
        (12, 14, "know"),
        (15, 16, "hath begun"),
        (17, 21, "the work of the Father"),
        (22, 24, "upon"),
        (25, 27, "all the land."),
    ],
    18: [
        (0, 1, "Therefore,"),
        (2, 5, "repent ye"),
        (6, 8, "all ye ends"),
        (9, 11, "of the earth,"),
        (12, 14, "and come"),
        (15, 17, "unto me,"),
        (18, 19, "and believe"),
        (20, 22, "in my gospel,"),
        (23, 24, "and be baptized"),
        (25, 27, "in my name;"),
        (28, 30, "for he"),
        (31, 34, "that believeth"),
        (35, 36, "and is baptized"),
        (37, 40, "shall be saved;"),
        (41, 43, "but he"),
        (44, 48, "that believeth not"),
        (49, 52, "shall be damned;"),
        (53, 53, "and"),
        (54, 58, "shall follow"),
        (59, 59, "signs"),
        (60, 63, "them"),
        (64, 67, "who believe"),
        (68, 70, "in my name."),
    ],
    19: [
        (0, 4, "And blessed is he"),
        (5, 8, "who is found"),
        (9, 10, "faithful"),
        (11, 13, "to my name"),
        (14, 17, "at the last day,"),
        (18, 18, "for"),
        (19, 23, "shall be raised up"),
        (24, 27, "he on high"),
        (28, 32, "to dwell in the kingdom"),
        (33, 36, "prepared for him"),
        (37, 39, "from the foundation"),
        (40, 42, "of the world."),
        (43, 44, "And behold,"),
        (45, 47, "it is I myself"),
        (48, 53, "who have spoken."),
        (54, 54, "Amen."),
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
