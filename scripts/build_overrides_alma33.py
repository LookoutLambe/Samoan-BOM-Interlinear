"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 33 — Alma continues
his discourse to the Zoramites: he answers their question of how to plant the
word, cites Zenos, Zenock, and Moses on prayer, worship, and the Son of God,
and exhorts them to look to Christ for eternal life.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash baked tokens in this chapter.

    python3 build_overrides_alma33.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 33

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "Now"),
        (2, 5, "after"),
        (6, 7, "had spoken"),
        (8, 9, "Alma"),
        (10, 11, "these words,"),
        (12, 15, "they sent forth"),
        (16, 18, "unto him"),
        (19, 22, "desiring to know"),
        (23, 27, "whether they should believe"),
        (28, 32, "in one God,"),
        (33, 38, "that they might obtain"),
        (39, 41, "this fruit"),
        (42, 45, "of which he spoke"),
        (46, 47, "thereof,"),
        (48, 49, "or how"),
        (50, 52, "they should plant"),
        (53, 55, "the seed,"),
        (56, 59, "or the word"),
        (60, 63, "of which he spoke"),
        (64, 65, "thereof,"),
        (66, 71, "which he said"),
        (72, 75, "must be planted"),
        (76, 79, "in their hearts;"),
        (80, 85, "or in what manner"),
        (86, 90, "they should begin"),
        (91, 93, "to exercise"),
        (94, 96, "their faith."),
    ],
    2: [
        (0, 4, "And Alma said"),
        (5, 8, "unto them:"),
        (9, 9, "Behold,"),
        (10, 13, "ye have said"),
        (14, 18, "that ye could not"),
        (19, 20, "worship"),
        (21, 24, "your God"),
        (25, 25, "because"),
        (26, 29, "ye are cast"),
        (30, 31, "out"),
        (32, 36, "from your synagogues."),
        (37, 38, "But behold,"),
        (39, 42, "I say"),
        (43, 45, "unto you,"),
        (46, 49, "if ye suppose"),
        (50, 54, "that ye cannot"),
        (55, 56, "worship"),
        (57, 59, "God,"),
        (60, 64, "ye do greatly err,"),
        (65, 70, "and ye ought to search"),
        (71, 73, "the scriptures;"),
        (74, 77, "if ye suppose"),
        (78, 81, "that they have taught"),
        (82, 84, "you"),
        (85, 86, "this thing,"),
        (87, 90, "ye understand not"),
        (91, 92, "them."),
    ],
    3: [
        (0, 2, "Do ye remember"),
        (3, 5, "to have read"),
        (6, 8, "the thing"),
        (9, 12, "which said"),
        (13, 13, "Zenos,"),
        (14, 16, "the prophet of old,"),
        (17, 19, "concerning"),
        (20, 21, "prayer"),
        (22, 25, "or worship?"),
    ],
    4: [
        (0, 0, "For"),
        (1, 5, "he said:"),
        (6, 10, "Thou art merciful"),
        (11, 13, "O God,"),
        (14, 14, "for"),
        (15, 18, "thou hast heard"),
        (19, 21, "my prayer,"),
        (22, 26, "even when I was"),
        (27, 29, "in the wilderness;"),
        (30, 30, "yea,"),
        (31, 34, "thou wast merciful"),
        (35, 39, "when I prayed"),
        (40, 45, "concerning them"),
        (46, 50, "who were"),
        (51, 52, "mine enemies,"),
        (53, 57, "and thou didst turn"),
        (58, 59, "them"),
        (60, 62, "to me."),
    ],
    5: [
        (0, 0, "Yea,"),
        (1, 3, "O God,"),
        (4, 8, "thou wast merciful"),
        (9, 11, "unto me"),
        (12, 16, "when I did cry"),
        (17, 19, "unto thee"),
        (20, 22, "in my field;"),
        (23, 27, "when I did cry"),
        (28, 30, "unto thee"),
        (31, 33, "in my prayer,"),
        (34, 37, "and thou didst hear"),
        (38, 40, "me."),
    ],
    6: [
        (0, 2, "And again,"),
        (3, 5, "O God,"),
        (6, 10, "when I did go"),
        (11, 13, "to my house"),
        (14, 17, "thou didst hear"),
        (18, 20, "me"),
        (21, 23, "in my prayer."),
    ],
    7: [
        (0, 5, "And when I did go"),
        (6, 8, "unto my closet,"),
        (9, 11, "O Lord,"),
        (12, 14, "and prayed"),
        (15, 17, "unto thee,"),
        (18, 21, "thou didst hear"),
        (22, 24, "me."),
    ],
    8: [
        (0, 0, "Yea,"),
        (1, 4, "thou art merciful"),
        (5, 7, "unto thy children"),
        (8, 12, "when they cry"),
        (13, 15, "unto thee,"),
        (16, 19, "to be heard by thee"),
        (20, 21, "them"),
        (22, 25, "and not of men,"),
        (26, 32, "and thou wilt hear"),
        (33, 33, "surely"),
        (34, 37, "them."),
    ],
    9: [
        (0, 0, "Yea,"),
        (1, 3, "O God,"),
        (4, 8, "thou hast been merciful"),
        (9, 11, "unto me,"),
        (12, 14, "and thou hast heard"),
        (15, 16, "my cries"),
        (17, 20, "in the midst of"),
        (21, 22, "thy congregations."),
    ],
    10: [
        (0, 0, "Yea,"),
        (1, 6, "and thou hast also heard"),
        (7, 9, "me,"),
        (10, 14, "when I was cast"),
        (15, 16, "out"),
        (17, 18, "and despised"),
        (19, 21, "by mine enemies;"),
        (22, 22, "yea,"),
        (23, 26, "thou didst hear"),
        (27, 29, "my cries,"),
        (30, 33, "and thou wast angry"),
        (34, 36, "with mine enemies,"),
        (37, 41, "and thou didst visit"),
        (42, 45, "them"),
        (46, 48, "in thine anger"),
        (49, 52, "with speedy destruction."),
    ],
    11: [
        (0, 4, "And thou didst hear"),
        (5, 7, "me"),
        (8, 11, "because of mine afflictions"),
        (12, 14, "and my sincerity;"),
        (15, 19, "and because of thy Son"),
        (20, 26, "thou hast been so merciful"),
        (27, 29, "unto me,"),
        (30, 31, "therefore"),
        (32, 37, "I will cry"),
        (38, 38, "unto"),
        (39, 41, "thee"),
        (42, 45, "in all mine afflictions,"),
        (46, 48, "for in thee"),
        (49, 53, "is my joy;"),
        (54, 54, "for"),
        (55, 58, "thou hast turned away"),
        (59, 60, "thy judgments"),
        (61, 64, "from me,"),
        (65, 68, "because of thy Son."),
    ],
    12: [
        (0, 2, "And now"),
        (3, 6, "Alma said"),
        (7, 10, "unto them:"),
        (11, 14, "Do ye believe"),
        (15, 18, "those scriptures"),
        (19, 20, "which were written"),
        (21, 25, "by them of old?"),
    ],
    13: [
        (0, 0, "Behold,"),
        (1, 5, "if ye believe"),
        (6, 6, "them,"),
        (7, 11, "ye must believe"),
        (12, 14, "the thing"),
        (15, 18, "which said"),
        (19, 19, "Zenos;"),
        (20, 20, "for,"),
        (21, 21, "behold,"),
        (22, 26, "he said:"),
        (27, 30, "Thou hast turned away"),
        (31, 32, "thy judgments"),
        (33, 36, "because of thy Son."),
    ],
    14: [
        (0, 2, "Now behold,"),
        (3, 5, "my brethren,"),
        (6, 10, "I would ask"),
        (11, 15, "if ye have read"),
        (16, 17, "the scriptures?"),
        (18, 21, "If ye have read,"),
        (22, 24, "how can it be"),
        (25, 28, "that ye disbelieve"),
        (29, 32, "on the Son of"),
        (33, 34, "God?"),
    ],
    15: [
        (0, 0, "For"),
        (1, 5, "it is not written that"),
        (6, 8, "Zenos alone"),
        (9, 11, "spake"),
        (12, 16, "concerning these things,"),
        (17, 20, "but also spake"),
        (21, 21, "Zenock"),
        (22, 26, "concerning these things—"),
    ],
    16: [
        (0, 0, "For"),
        (1, 1, "behold,"),
        (2, 6, "he said:"),
        (7, 9, "Thou art angry,"),
        (10, 12, "O Lord,"),
        (13, 15, "with this people,"),
        (16, 16, "because"),
        (17, 21, "they will not understand"),
        (22, 25, "thy mercies"),
        (26, 30, "which thou hast bestowed"),
        (31, 35, "upon them"),
        (36, 39, "because of thy Son."),
    ],
    17: [
        (0, 2, "And now,"),
        (3, 5, "my brethren,"),
        (6, 8, "ye see"),
        (9, 11, "hath testified"),
        (12, 15, "a second prophet"),
        (16, 17, "of old"),
        (18, 23, "concerning the Son of"),
        (24, 25, "God,"),
        (26, 27, "and because"),
        (28, 32, "the people would not understand"),
        (33, 35, "his words,"),
        (36, 37, "therefore"),
        (38, 41, "they stoned"),
        (42, 43, "him"),
        (44, 45, "with stones"),
        (46, 48, "unto death."),
    ],
    18: [
        (0, 1, "But behold,"),
        (2, 6, "this is not all;"),
        (7, 9, "not only"),
        (10, 12, "these two"),
        (13, 16, "who spake"),
        (17, 22, "concerning the Son of"),
        (23, 24, "God."),
    ],
    19: [
        (0, 0, "Behold,"),
        (1, 4, "he was spoken of"),
        (5, 6, "by Moses;"),
        (7, 7, "yea,"),
        (8, 9, "and behold"),
        (10, 14, "was raised up"),
        (15, 16, "a type"),
        (17, 19, "in the wilderness,"),
        (20, 21, "that"),
        (22, 25, "whosoever"),
        (26, 30, "would look upon it"),
        (31, 34, "might live."),
        (35, 37, "And many"),
        (38, 41, "did look"),
        (42, 44, "and live."),
    ],
    20: [
        (0, 0, "But"),
        (1, 2, "few"),
        (3, 4, "understood"),
        (5, 7, "the meaning"),
        (8, 10, "of those things,"),
        (11, 14, "and this because"),
        (15, 18, "of the hardness"),
        (19, 22, "of their hearts."),
        (23, 23, "But"),
        (24, 28, "there were many"),
        (29, 33, "who were so"),
        (34, 36, "hardened"),
        (37, 41, "they would not"),
        (42, 43, "look up,"),
        (44, 46, "therefore"),
        (47, 51, "they perished."),
        (52, 53, "Now"),
        (54, 56, "the reason"),
        (57, 61, "they would not"),
        (62, 63, "look up"),
        (64, 64, "is because"),
        (65, 68, "they did not believe"),
        (69, 73, "that it would heal"),
        (74, 75, "them."),
    ],
    21: [
        (0, 0, "O,"),
        (1, 3, "my brethren,"),
        (4, 9, "if ye could be healed"),
        (10, 13, "by merely"),
        (14, 15, "the looking"),
        (16, 19, "of your eyes"),
        (20, 23, "that ye might"),
        (24, 25, "be healed,"),
        (26, 30, "would ye not"),
        (31, 34, "look up quickly,"),
        (35, 40, "or would ye rather"),
        (41, 43, "the hardening of"),
        (44, 46, "your hearts"),
        (47, 50, "in unbelief,"),
        (51, 52, "and be slothful,"),
        (53, 57, "that ye would not"),
        (58, 59, "look up with"),
        (60, 62, "your eyes,"),
        (63, 66, "that ye might perish?"),
    ],
    22: [
        (0, 2, "If so,"),
        (3, 7, "shall come"),
        (8, 9, "wo"),
        (10, 13, "upon you;"),
        (14, 19, "but if not so,"),
        (20, 23, "then cast about"),
        (24, 27, "your eyes"),
        (28, 31, "and begin to believe"),
        (32, 35, "in the Son of"),
        (36, 37, "God,"),
        (38, 44, "that he will come"),
        (45, 48, "to redeem his people,"),
        (49, 53, "and that he shall suffer"),
        (54, 57, "and die"),
        (58, 59, "to atone"),
        (60, 63, "for their sins;"),
        (64, 69, "and that he shall rise"),
        (70, 71, "again"),
        (72, 74, "from the dead,"),
        (75, 80, "which shall bring to pass"),
        (81, 82, "the resurrection,"),
        (83, 87, "that shall stand"),
        (88, 89, "all men"),
        (90, 92, "before him,"),
        (93, 94, "to be judged"),
        (95, 99, "at the last judgment day,"),
        (100, 102, "according to"),
        (103, 105, "their works."),
    ],
    23: [
        (0, 2, "And now,"),
        (3, 5, "my brethren,"),
        (6, 8, "I desire"),
        (9, 11, "that ye shall plant"),
        (12, 14, "this word"),
        (15, 18, "in your hearts,"),
        (19, 24, "and as it beginneth to swell"),
        (25, 28, "even so nourish it"),
        (29, 32, "by your faith."),
        (33, 34, "And behold,"),
        (35, 39, "it will become"),
        (40, 40, "a tree,"),
        (41, 43, "springing up"),
        (44, 47, "in you"),
        (48, 51, "unto everlasting"),
        (52, 53, "life."),
        (54, 57, "And then be it prayed"),
        (58, 61, "that may grant"),
        (62, 63, "God"),
        (64, 66, "unto you"),
        (67, 68, "that light be"),
        (69, 71, "your burdens,"),
        (72, 77, "through the joy of"),
        (78, 79, "his Son."),
        (80, 85, "And even all this"),
        (86, 90, "can ye do"),
        (91, 95, "if ye will"),
        (96, 97, "it."),
        (98, 98, "Amen."),
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
