"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 11 — the appearance
of the risen Christ: as the multitude gathers at the temple in Bountiful they hear
the Father's voice introducing his Beloved Son; Jesus descends, declares himself
the God of the whole earth slain for the world, and invites all to thrust their
hands into his side and feel the prints of the nails; he gives Nephi and others
power to baptize, teaches the exact manner and words of baptism, forbids disputation
over baptism, and declares his doctrine — faith, repentance, baptism, and becoming
as a little child — warning against contention as being of the devil.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits applied to bom_books.json before glossing:
    11:7   igoa—ia          ->  igoa—          +  ia
    11:23  latou—Faauta,    ->  latou—         +  Faauta,

    python3 build_overrides_3nephi11.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 11

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 14, "there was a great multitude of people,"),
        (15, 19, "of the people of Nephi,"),
        (20, 23, "gathered together round about"),
        (24, 27, "the temple which"),
        (28, 33, "was in the land Bountiful;"),
        (34, 39, "and they marveled and wondered"),
        (40, 45, "one with another,"),
        (46, 54, "and showing one to another"),
        (55, 58, "the great and marvelous change"),
        (59, 62, "which had come."),
    ],
    2: [
        (0, 4, "And they also conversed"),
        (5, 10, "about this Jesus Christ,"),
        (11, 16, "of whom concerned"),
        (17, 21, "the sign that was given"),
        (22, 26, "concerning his death."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 8, "while they thus conversed"),
        (9, 14, "one with another,"),
        (15, 19, "they heard a voice"),
        (20, 23, "as if it came"),
        (24, 26, "from heaven;"),
        (27, 31, "and they looked about,"),
        (32, 32, "for"),
        (33, 36, "they understood not"),
        (37, 40, "the voice which"),
        (41, 43, "they heard;"),
        (44, 50, "and it was not a harsh voice,"),
        (51, 55, "nor a loud voice,"),
        (56, 59, "nevertheless,"),
        (60, 67, "and though it was a small voice"),
        (68, 73, "yet it pierced the centre"),
        (74, 82, "of those who heard it,"),
        (83, 85, "insomuch that"),
        (86, 92, "no part of their body"),
        (93, 96, "did not quake;"),
        (97, 97, "yea,"),
        (98, 100, "it burned even"),
        (101, 104, "to their souls,"),
        (105, 109, "which caused to burn"),
        (110, 112, "their hearts."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 6, "they heard again"),
        (7, 8, "the voice,"),
        (9, 15, "and they understood it not."),
    ],
    5: [
        (0, 6, "And they heard the voice again"),
        (7, 11, "the third time,"),
        (12, 19, "and they opened their ears"),
        (20, 23, "to hear it;"),
        (24, 30, "and their eyes turned"),
        (31, 38, "towards where that voice came from;"),
        (39, 45, "and they gazed steadfastly"),
        (46, 48, "towards heaven,"),
        (49, 56, "to where the voice came from."),
    ],
    6: [
        (0, 1, "And behold,"),
        (2, 6, "the third time"),
        (7, 10, "they understood"),
        (11, 14, "the voice which"),
        (15, 17, "they heard;"),
        (18, 21, "and it spoke"),
        (22, 25, "unto them:"),
    ],
    7: [
        (0, 0, "Behold"),
        (1, 4, "my Beloved Son,"),
        (5, 12, "in whom I am well pleased,"),
        (13, 18, "in whom I have glorified"),
        (19, 20, "my name—"),
        (21, 23, "hear ye"),
        (24, 26, "him."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 6, "as they understood"),
        (7, 10, "they gazed again"),
        (11, 15, "their eyes turned"),
        (16, 18, "towards heaven;"),
        (19, 20, "and behold,"),
        (21, 25, "they saw a Man"),
        (26, 28, "descending"),
        (29, 31, "out of heaven;"),
        (32, 36, "and he was clothed"),
        (37, 40, "in a white robe;"),
        (41, 46, "and he came down"),
        (47, 48, "and stood"),
        (49, 54, "in the midst of them;"),
        (55, 59, "and turned the eyes"),
        (60, 65, "of the whole multitude"),
        (66, 68, "upon him,"),
        (69, 74, "and they feared to open"),
        (75, 77, "their mouths,"),
        (78, 86, "even one to another,"),
        (87, 91, "and they knew not"),
        (92, 96, "the meaning of this thing,"),
        (97, 100, "for they thought"),
        (101, 104, "it was an angel that"),
        (105, 111, "had appeared unto them."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 8, "he stretched forth his hand"),
        (9, 11, "and spoke"),
        (12, 13, "unto the people,"),
        (14, 16, "saying:"),
    ],
    10: [
        (0, 0, "Behold,"),
        (1, 5, "I am Jesus Christ,"),
        (6, 12, "of whom the prophets testified"),
        (13, 16, "should come"),
        (17, 19, "into the world."),
    ],
    11: [
        (0, 1, "And behold,"),
        (2, 6, "I am the light"),
        (7, 12, "and the life of the world;"),
        (13, 16, "and I have drunk"),
        (17, 21, "of that bitter cup which"),
        (22, 27, "the Father gave"),
        (28, 30, "unto me,"),
        (31, 36, "and I have glorified the Father"),
        (37, 43, "in my taking upon me"),
        (44, 48, "the sins of the world,"),
        (49, 56, "wherein I submitted"),
        (57, 62, "to the will of the Father"),
        (63, 65, "in all things"),
        (66, 68, "from the beginning."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when Jesus had spoken"),
        (11, 13, "these words"),
        (14, 16, "fell down"),
        (17, 21, "the whole multitude"),
        (22, 24, "to the earth;"),
        (25, 28, "for they remembered"),
        (29, 35, "it was prophesied among them"),
        (36, 45, "that Christ would show himself"),
        (46, 49, "unto them"),
        (50, 52, "after there passed"),
        (53, 55, "his ascension"),
        (56, 58, "into heaven."),
    ],
    13: [
        (0, 7, "And the Lord spoke"),
        (8, 11, "unto them"),
        (12, 14, "saying:"),
    ],
    14: [
        (0, 1, "Arise"),
        (2, 4, "and come forth"),
        (5, 7, "unto me,"),
        (8, 15, "that ye may put your hands"),
        (16, 18, "into my side,"),
        (19, 24, "and that ye may also feel"),
        (25, 28, "the prints of the nails"),
        (29, 35, "in my hands and my feet,"),
        (36, 40, "that ye may know"),
        (41, 47, "I am the God of Israel,"),
        (48, 54, "and the God of the whole earth,"),
        (55, 57, "and was slain"),
        (58, 62, "for the sins of the world."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 9, "the multitude went"),
        (10, 11, "forth,"),
        (12, 17, "and put their hands"),
        (18, 20, "into his side,"),
        (21, 23, "and they felt"),
        (24, 27, "the prints of the nails"),
        (28, 33, "in his hands and his feet;"),
        (34, 39, "and this they did do,"),
        (40, 46, "going forth one by one"),
        (47, 53, "until they all went forth,"),
        (54, 59, "and saw with their eyes"),
        (60, 67, "and touched with their hands,"),
        (68, 72, "and they knew of a surety"),
        (73, 75, "and bore record,"),
        (76, 79, "that it was he himself,"),
        (80, 85, "of whom the prophets wrote,"),
        (86, 90, "would come."),
    ],
    16: [
        (0, 8, "And when they had all gone forth"),
        (9, 14, "and witnessed for themselves,"),
        (15, 18, "they cried out together,"),
        (19, 21, "saying:"),
    ],
    17: [
        (0, 0, "Hosanna!"),
        (1, 3, "Blessed be"),
        (4, 6, "the name of"),
        (7, 10, "the Most High God!"),
        (11, 15, "And they fell down"),
        (16, 19, "at the feet of Jesus,"),
        (20, 22, "and worshipped"),
        (23, 25, "him."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he spoke"),
        (8, 9, "unto Nephi"),
        (10, 14, "(for Nephi was"),
        (15, 21, "among the multitude)"),
        (22, 25, "and he commanded"),
        (26, 28, "him"),
        (29, 35, "that he come forth."),
    ],
    19: [
        (0, 3, "And Nephi arose"),
        (4, 8, "and went forth,"),
        (9, 14, "and bowed himself"),
        (15, 19, "before the Lord"),
        (20, 22, "and kissed"),
        (23, 25, "his feet."),
    ],
    20: [
        (0, 5, "And the Lord commanded"),
        (6, 8, "him"),
        (9, 10, "that he arise."),
        (11, 15, "And he arose"),
        (16, 18, "and stood"),
        (19, 21, "before him."),
    ],
    21: [
        (0, 5, "And the Lord said"),
        (6, 8, "unto him:"),
        (9, 12, "I give"),
        (13, 15, "unto you"),
        (16, 17, "the power"),
        (18, 23, "that ye baptize this people"),
        (24, 29, "when I have ascended again"),
        (30, 32, "into heaven."),
    ],
    22: [
        (0, 4, "And again were called others"),
        (5, 7, "by the Lord,"),
        (8, 14, "and likewise he said"),
        (15, 18, "unto them;"),
        (19, 23, "and he gave"),
        (24, 27, "unto them"),
        (28, 33, "the power to baptize."),
        (34, 38, "And he said"),
        (39, 42, "unto them:"),
        (43, 46, "This is the manner"),
        (47, 51, "in which ye shall baptize;"),
        (52, 59, "and there shall be no disputes"),
        (60, 64, "among you."),
    ],
    23: [
        (0, 5, "Verily I say"),
        (6, 8, "unto you,"),
        (9, 13, "whoso repents"),
        (14, 16, "of his sins"),
        (17, 22, "through your words,"),
        (23, 26, "and desires to be baptized"),
        (27, 29, "in my name,"),
        (30, 33, "this is the manner"),
        (34, 39, "in which ye shall baptize them—"),
        (40, 40, "Behold,"),
        (41, 46, "ye shall go down and stand"),
        (47, 51, "in the water,"),
        (52, 55, "and in my name"),
        (56, 61, "ye shall baptize them."),
    ],
    24: [
        (0, 3, "And now behold,"),
        (4, 6, "these are the words"),
        (7, 9, "which ye shall say,"),
        (10, 13, "and naming them"),
        (14, 17, "by their names,"),
        (18, 20, "saying:"),
    ],
    25: [
        (0, 6, "Having been given unto me"),
        (7, 11, "the authority by Jesus Christ,"),
        (12, 14, "I baptize"),
        (15, 17, "you"),
        (18, 23, "in the name of the Father,"),
        (24, 26, "and of the Son,"),
        (27, 30, "and of the Holy Ghost."),
        (31, 31, "Amen."),
    ],
    26: [
        (0, 4, "And then ye shall immerse"),
        (5, 7, "them"),
        (8, 12, "in the water,"),
        (13, 16, "and raise up again"),
        (17, 19, "out of the water."),
    ],
    27: [
        (0, 4, "And this is the manner"),
        (5, 9, "in which ye shall baptize"),
        (10, 12, "in my name;"),
        (13, 14, "for behold,"),
        (15, 20, "verily I say"),
        (21, 23, "unto you,"),
        (24, 26, "the Father,"),
        (27, 29, "and the Son,"),
        (30, 33, "and the Holy Ghost"),
        (34, 35, "are one;"),
        (36, 44, "and I am in the Father,"),
        (45, 53, "and the Father is in me,"),
        (54, 59, "and the Father and I"),
        (60, 61, "are one."),
    ],
    28: [
        (0, 7, "And thus shall ye baptize"),
        (8, 14, "as I have commanded you."),
        (15, 22, "And let there be no disputes"),
        (23, 27, "among you,"),
        (28, 33, "as there have been"),
        (34, 40, "up until now;"),
        (41, 46, "nor let there be disputes"),
        (47, 51, "among you"),
        (52, 59, "concerning the points of my doctrine,"),
        (60, 65, "as there have been"),
        (66, 72, "up until now."),
    ],
    29: [
        (0, 0, "For"),
        (1, 8, "verily, verily I say"),
        (9, 11, "unto you,"),
        (12, 16, "he who has"),
        (17, 20, "the spirit of contention"),
        (21, 28, "is not of me,"),
        (29, 34, "but is of the devil,"),
        (35, 41, "who is the father of contention,"),
        (42, 46, "and he stirs up"),
        (47, 49, "the hearts of men"),
        (50, 54, "to contend with anger,"),
        (55, 60, "one with another."),
    ],
    30: [
        (0, 0, "Behold,"),
        (1, 7, "this is not my doctrine,"),
        (8, 13, "the stirring up of the hearts of men"),
        (14, 16, "with anger,"),
        (17, 24, "one against another;"),
        (25, 30, "but this is my doctrine,"),
        (31, 34, "that such things be done away."),
    ],
    31: [
        (0, 0, "Behold,"),
        (1, 4, "verily, verily,"),
        (5, 8, "I say"),
        (9, 11, "unto you,"),
        (12, 17, "I will declare"),
        (18, 20, "unto you"),
        (21, 23, "my doctrine."),
    ],
    32: [
        (0, 5, "And this is my doctrine,"),
        (6, 11, "and it is the doctrine which"),
        (12, 17, "the Father gave"),
        (18, 20, "unto me;"),
        (21, 25, "and I bear record"),
        (26, 30, "of the Father,"),
        (31, 36, "and the Father bears record"),
        (37, 41, "of me,"),
        (42, 48, "and the Holy Ghost bears record"),
        (49, 55, "of the Father and me;"),
        (56, 60, "and I bear record"),
        (61, 67, "the Father commands all men,"),
        (68, 74, "wherever they are,"),
        (75, 76, "to repent"),
        (77, 82, "and believe in me."),
    ],
    33: [
        (0, 6, "And whoso believes"),
        (7, 10, "in me,"),
        (11, 12, "and is baptized,"),
        (13, 16, "that same one"),
        (17, 20, "shall be saved;"),
        (21, 25, "and they are they"),
        (26, 31, "who shall inherit"),
        (32, 37, "the kingdom of God."),
    ],
    34: [
        (0, 8, "And whoso believes not"),
        (9, 11, "in me,"),
        (12, 14, "and is not baptized,"),
        (15, 18, "shall be damned."),
    ],
    35: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 15, "this is my doctrine,"),
        (16, 20, "and I bear record"),
        (21, 24, "it is from the Father;"),
        (25, 35, "and whoso believes in me"),
        (36, 41, "believes in the Father also;"),
        (42, 44, "and unto him"),
        (45, 52, "the Father will bear record"),
        (53, 57, "of me,"),
        (58, 58, "for"),
        (59, 65, "he will visit"),
        (66, 68, "him"),
        (69, 75, "with fire and the Holy Ghost."),
    ],
    36: [
        (0, 7, "And thus will bear record"),
        (8, 10, "the Father"),
        (11, 15, "of me,"),
        (16, 20, "and the Holy Ghost"),
        (21, 25, "will bear record"),
        (26, 28, "unto him"),
        (29, 35, "of the Father and me;"),
        (36, 36, "for"),
        (37, 39, "the Father,"),
        (40, 41, "and I,"),
        (42, 45, "and the Holy Ghost"),
        (46, 47, "are one."),
    ],
    37: [
        (0, 5, "And again I say"),
        (6, 8, "unto you,"),
        (9, 13, "ye must repent,"),
        (14, 15, "and become"),
        (16, 20, "as a little child,"),
        (21, 22, "and be baptized"),
        (23, 25, "in my name,"),
        (26, 27, "otherwise"),
        (28, 34, "ye can in no wise receive"),
        (35, 37, "these things."),
    ],
    38: [
        (0, 5, "And again I say"),
        (6, 8, "unto you,"),
        (9, 13, "ye must repent,"),
        (14, 15, "and be baptized"),
        (16, 18, "in my name,"),
        (19, 20, "and become"),
        (21, 25, "as a little child,"),
        (26, 27, "otherwise"),
        (28, 34, "ye can in no wise inherit"),
        (35, 40, "the kingdom of God."),
    ],
    39: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 15, "this is my doctrine,"),
        (16, 22, "and whoso builds"),
        (23, 27, "upon this thing"),
        (28, 34, "builds upon my rock,"),
        (35, 40, "and shall not prevail"),
        (41, 43, "the gates of hell"),
        (44, 49, "against them."),
    ],
    40: [
        (0, 8, "And whoso declares"),
        (9, 12, "otherwise than this,"),
        (13, 14, "and sets it up"),
        (15, 21, "as if it were my doctrine,"),
        (22, 25, "that same one"),
        (26, 31, "comes of evil,"),
        (32, 35, "and is not built"),
        (36, 40, "upon my rock;"),
        (41, 43, "but builds"),
        (44, 49, "upon a sandy foundation,"),
        (50, 56, "and shall stand open"),
        (57, 59, "the gates of hell"),
        (60, 63, "to receive them"),
        (64, 68, "when the floods come"),
        (69, 72, "and the winds beat"),
        (73, 77, "upon them."),
    ],
    41: [
        (0, 1, "Therefore,"),
        (2, 5, "go ye forth"),
        (6, 8, "unto this people,"),
        (9, 12, "and declare the words"),
        (13, 17, "which I have spoken,"),
        (18, 21, "reaching to"),
        (22, 25, "the ends of the earth."),
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
