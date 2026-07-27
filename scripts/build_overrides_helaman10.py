"""
Hand-curated TAM-phrase gloss overrides for Helamana (Helaman) 10 — the divided
crowd leaves Nephi alone; as he ponders on the way home, a voice from heaven
blesses him for his unwearying diligence and grants him the sealing power, that
whatsoever he binds or looses on earth shall be so in heaven; the Lord commands
him to declare repentance or destruction; and Nephi, caught away by the Spirit,
goes from multitude to multitude preaching, though the people harden their
hearts and contend to the point of civil strife.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits applied to bom_books.json before glossing:
    10:3  ia—ma    ->  ia—    +  ma
    10:3  uma—ma   ->  uma—   +  ma

    python3 build_overrides_helaman10.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "helaman"
CHAPTER_NUM = 10

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 5, "arose"),
        (6, 7, "a division"),
        (8, 11, "among the people,"),
        (12, 14, "insomuch that"),
        (15, 17, "they divided"),
        (18, 23, "to this side and that side"),
        (24, 28, "and departed"),
        (29, 32, "to their ways,"),
        (33, 36, "but leaving"),
        (37, 39, "Nephi alone,"),
        (40, 43, "as he stood"),
        (44, 49, "in the midst of them."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 5, "went"),
        (6, 6, "Nephi"),
        (7, 9, "on his way"),
        (10, 13, "toward"),
        (14, 16, "his own house,"),
        (17, 19, "pondering deeply"),
        (20, 21, "upon the things"),
        (22, 24, "which were shown"),
        (25, 27, "by the Lord"),
        (28, 30, "unto him."),
    ],
    3: [
        (0, 3, "And it came to pass"),
        (4, 7, "as thus"),
        (8, 11, "he pondered deeply—"),
        (12, 15, "with great sorrow"),
        (16, 17, "because of"),
        (18, 20, "the wickedness of"),
        (21, 23, "the Nephite people,"),
        (24, 28, "in their secret works"),
        (29, 31, "of darkness,"),
        (32, 36, "and their murderings,"),
        (37, 40, "and their plunderings,"),
        (41, 44, "and all manner of iniquities—"),
        (45, 47, "and it came to pass"),
        (48, 51, "as thus"),
        (52, 55, "he pondered deeply"),
        (56, 58, "in his heart,"),
        (59, 59, "behold,"),
        (60, 62, "came"),
        (63, 64, "a voice"),
        (65, 67, "unto him,"),
        (68, 70, "saying:"),
    ],
    4: [
        (0, 2, "Blessed indeed art thou"),
        (3, 3, "Nephi,"),
        (4, 5, "because of"),
        (6, 7, "those things"),
        (8, 10, "which thou didst;"),
        (11, 11, "for"),
        (12, 14, "I have seen"),
        (15, 18, "thy preaching"),
        (19, 22, "with unwearyingness"),
        (23, 25, "the word"),
        (26, 29, "which I gave"),
        (30, 32, "unto thee,"),
        (33, 35, "unto this people."),
        (36, 40, "And thou hast not feared"),
        (41, 44, "them,"),
        (45, 49, "and thou hast not sought"),
        (50, 52, "thine own life,"),
        (53, 56, "but thou hast sought"),
        (57, 58, "my will,"),
        (59, 61, "and to keep"),
        (62, 63, "my commandments."),
    ],
    5: [
        (0, 2, "And now,"),
        (3, 3, "because"),
        (4, 6, "thou hast done"),
        (7, 8, "this thing"),
        (9, 12, "with unwearyingness,"),
        (13, 13, "behold,"),
        (14, 18, "I will bless"),
        (19, 19, "thee"),
        (20, 21, "forever;"),
        (22, 27, "and I will make mighty"),
        (28, 28, "thee"),
        (29, 31, "in word"),
        (32, 35, "and in deed,"),
        (36, 38, "in faith"),
        (39, 40, "and works;"),
        (41, 41, "yea,"),
        (42, 47, "even to the doing of"),
        (48, 49, "all things"),
        (50, 53, "unto thee"),
        (54, 57, "according to"),
        (58, 59, "thy word,"),
        (60, 60, "for"),
        (61, 65, "thou wilt not ask"),
        (66, 68, "for anything"),
        (69, 73, "which is contrary to"),
        (74, 75, "my will."),
    ],
    6: [
        (0, 0, "Behold,"),
        (1, 4, "thou art Nephi,"),
        (5, 10, "and I am God."),
        (11, 11, "Behold,"),
        (12, 15, "I declare"),
        (16, 18, "this thing"),
        (19, 21, "unto thee"),
        (22, 24, "in the presence of"),
        (25, 26, "mine angels,"),
        (27, 32, "thou shalt have"),
        (33, 34, "the power"),
        (35, 39, "over this people,"),
        (40, 45, "and thou shalt smite"),
        (46, 47, "the earth"),
        (48, 50, "with famine,"),
        (51, 53, "and with pestilence,"),
        (54, 56, "and destruction,"),
        (57, 59, "according to"),
        (60, 62, "the wickedness of"),
        (63, 64, "this people."),
    ],
    7: [
        (0, 0, "Behold,"),
        (1, 4, "I give"),
        (5, 7, "unto thee"),
        (8, 9, "power,"),
        (10, 13, "whatsoever"),
        (14, 16, "thou shalt seal"),
        (17, 21, "on the earth"),
        (22, 25, "shall be sealed"),
        (26, 28, "in heaven;"),
        (29, 33, "and whatsoever"),
        (34, 36, "thou shalt loose"),
        (37, 39, "on the earth"),
        (40, 43, "shall be loosed"),
        (44, 46, "in heaven;"),
        (47, 52, "and thus shall"),
        (53, 57, "thou have power"),
        (58, 62, "among this people."),
    ],
    8: [
        (0, 3, "And thus,"),
        (4, 8, "if thou say"),
        (9, 11, "unto this temple"),
        (12, 13, "be rent in twain,"),
        (14, 18, "it shall be done."),
    ],
    9: [
        (0, 5, "And if thou say"),
        (6, 8, "unto this mountain,"),
        (9, 13, "Be thou cast down"),
        (14, 16, "and become smooth,"),
        (17, 21, "it shall be done."),
    ],
    10: [
        (0, 1, "And behold,"),
        (2, 6, "if thou say"),
        (7, 10, "shall smite"),
        (11, 12, "this people"),
        (13, 15, "by God,"),
        (16, 20, "it shall come to pass."),
    ],
    11: [
        (0, 3, "And now behold,"),
        (4, 7, "I command"),
        (8, 10, "thee,"),
        (11, 14, "that thou go"),
        (15, 17, "and declare"),
        (18, 20, "unto this people,"),
        (21, 25, "thus saith"),
        (26, 30, "the Lord God,"),
        (31, 35, "who is the Most Powerful:"),
        (36, 37, "Except"),
        (38, 40, "ye repent"),
        (41, 45, "ye shall be smitten,"),
        (46, 50, "even unto destruction."),
    ],
    12: [
        (0, 1, "And behold,"),
        (2, 3, "now"),
        (4, 6, "it came to pass that"),
        (7, 11, "had finished speaking"),
        (12, 14, "the Lord"),
        (15, 17, "these words"),
        (18, 19, "unto Nephi,"),
        (20, 23, "he stopped"),
        (24, 28, "and did not go"),
        (29, 32, "unto his own house,"),
        (33, 37, "but returned again"),
        (38, 41, "unto the multitudes"),
        (42, 46, "who were scattered about"),
        (47, 51, "upon the land,"),
        (52, 54, "and began to"),
        (55, 56, "declare"),
        (57, 60, "unto them"),
        (61, 65, "the word of the Lord"),
        (66, 69, "which was spoken"),
        (70, 72, "unto him,"),
        (73, 75, "concerning"),
        (76, 80, "the destruction of them"),
        (81, 86, "if they did not repent."),
    ],
    13: [
        (0, 2, "Now behold,"),
        (3, 5, "notwithstanding"),
        (6, 8, "that great miracle"),
        (9, 12, "which Nephi did"),
        (13, 16, "in the telling"),
        (17, 20, "unto them"),
        (21, 23, "concerning"),
        (24, 26, "the death of"),
        (27, 29, "the chief judge,"),
        (30, 32, "they hardened"),
        (33, 35, "their hearts"),
        (36, 38, "and hearkened not"),
        (39, 41, "unto the words of"),
        (42, 43, "the Lord."),
    ],
    14: [
        (0, 1, "Therefore"),
        (2, 7, "Nephi declared"),
        (8, 11, "unto them"),
        (12, 16, "the word of the Lord,"),
        (17, 18, "saying:"),
        (19, 20, "Except"),
        (21, 23, "ye repent,"),
        (24, 28, "even as saith"),
        (29, 31, "the Lord,"),
        (32, 36, "ye shall be smitten"),
        (37, 41, "even unto destruction."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 8, "had finished declaring"),
        (9, 10, "Nephi"),
        (11, 12, "his words"),
        (13, 16, "unto them,"),
        (17, 17, "behold,"),
        (18, 21, "they still hardened"),
        (22, 24, "their hearts"),
        (25, 29, "and would not hearken"),
        (30, 32, "unto his words;"),
        (33, 34, "therefore"),
        (35, 38, "they reviled"),
        (39, 44, "against him,"),
        (45, 46, "and sought"),
        (47, 49, "to lay"),
        (50, 52, "their hands"),
        (53, 57, "upon him"),
        (58, 61, "that they might"),
        (62, 65, "cast him"),
        (66, 68, "into prison."),
    ],
    16: [
        (0, 1, "But behold,"),
        (2, 3, "was together"),
        (4, 8, "the power of God"),
        (9, 10, "with him,"),
        (11, 15, "and they could not"),
        (16, 19, "take him"),
        (20, 21, "to cast"),
        (22, 24, "into prison,"),
        (25, 25, "for"),
        (26, 29, "he was taken"),
        (30, 32, "by the Spirit"),
        (33, 36, "and caught away"),
        (37, 42, "from the midst of them."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 5, "thus"),
        (6, 9, "he went forth"),
        (10, 15, "by the Spirit,"),
        (16, 20, "from one multitude"),
        (21, 25, "to another multitude,"),
        (26, 28, "declaring"),
        (29, 31, "the word of"),
        (32, 33, "God,"),
        (34, 39, "even until finished"),
        (40, 42, "he declared"),
        (43, 47, "unto them all,"),
        (48, 50, "or sent forth"),
        (51, 55, "among all the people."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 8, "they would not hearken"),
        (9, 11, "unto his words;"),
        (12, 17, "and there began to be"),
        (18, 19, "contentions,"),
        (20, 22, "insomuch that"),
        (23, 24, "they divided"),
        (25, 30, "against themselves"),
        (31, 33, "and began to"),
        (34, 35, "they slay"),
        (36, 41, "one another"),
        (42, 44, "with the sword."),
    ],
    19: [
        (0, 4, "And thus ended"),
        (5, 7, "the seventieth"),
        (8, 10, "and first"),
        (11, 12, "year"),
        (13, 16, "of the reign of"),
        (17, 17, "the judges"),
        (18, 23, "over the people of"),
        (24, 24, "Nephi."),
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
