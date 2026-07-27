"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 19 — word spreads
overnight and a great multitude gathers on the morrow; Nephi and the twelve
disciples divide the people and teach them to pray, then are baptized and filled
with the Holy Ghost, angels ministering to them; Jesus appears again, has the
people and disciples kneel and pray to him, and prays three times unto the Father,
his countenance and garments shining exceedingly white; he rejoices at the faith
of the people, who are made white and pure, and thanks the Father for purifying
those in whom he has chosen.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits applied to bom_books.json before glossing:
    19:4  Iesu—ma        ->  Iesu—     +  ma
    19:8  Iesu—faauta,   ->  Iesu—     +  faauta,

    python3 build_overrides_3nephi19.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 19

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 12, "when Jesus had ascended"),
        (13, 15, "into heaven,"),
        (16, 18, "there dispersed"),
        (19, 22, "the multitude,"),
        (23, 27, "and each man"),
        (28, 31, "took his wife"),
        (32, 34, "and his children"),
        (35, 37, "and returned"),
        (38, 41, "to his own home."),
    ],
    2: [
        (0, 6, "And quickly spread the report"),
        (7, 12, "among all the people,"),
        (13, 15, "before it was dark,"),
        (16, 17, "that"),
        (18, 23, "the multitude had seen"),
        (24, 25, "Jesus,"),
        (26, 28, "and that"),
        (29, 32, "he had ministered"),
        (33, 36, "unto them;"),
        (37, 48, "and he would also show himself again"),
        (49, 54, "on the morrow"),
        (55, 59, "unto the multitude."),
    ],
    3: [
        (0, 0, "Yea,"),
        (1, 6, "the report spread"),
        (7, 10, "concerning Jesus"),
        (11, 14, "all the night;"),
        (15, 25, "and so much was their telling to the people"),
        (26, 30, "that there became many,"),
        (31, 31, "yea,"),
        (32, 38, "an exceedingly great number of people,"),
        (39, 41, "labored hard"),
        (42, 45, "all that night,"),
        (46, 52, "that they might be"),
        (53, 58, "on the morrow"),
        (59, 62, "at the place where"),
        (63, 73, "Jesus would show himself"),
        (74, 78, "unto the multitude."),
    ],
    4: [
        (0, 2, "And it came to pass"),
        (3, 8, "on the next day,"),
        (9, 12, "when had gathered together"),
        (13, 16, "the multitude,"),
        (17, 17, "behold,"),
        (18, 19, "Nephi"),
        (20, 22, "and his brother"),
        (23, 28, "whom he raised from the dead,"),
        (29, 32, "his name was Timothy,"),
        (33, 36, "and his son also,"),
        (37, 40, "his name was Jonas,"),
        (41, 43, "and also Mathoni,"),
        (44, 47, "and Mathonihah, his brother,"),
        (48, 49, "and Kumen,"),
        (50, 51, "and Kumenonhi,"),
        (52, 53, "and Jeremiah,"),
        (54, 55, "and Shemnon,"),
        (56, 57, "and Jonas,"),
        (58, 59, "and Zedekiah,"),
        (60, 61, "and Isaiah—"),
        (62, 63, "now"),
        (64, 70, "these are the names of the disciples"),
        (71, 74, "whom Jesus chose—"),
        (75, 78, "and it came to pass that"),
        (79, 81, "they went forth"),
        (82, 83, "and stood"),
        (84, 91, "in the midst of the multitude."),
    ],
    5: [
        (0, 1, "And behold,"),
        (2, 5, "was exceedingly great"),
        (6, 9, "the multitude"),
        (10, 12, "they commanded"),
        (13, 16, "that they be divided"),
        (17, 21, "into twelve groups."),
    ],
    6: [
        (0, 5, "And the twelve taught"),
        (6, 9, "the multitude;"),
        (10, 11, "and behold,"),
        (12, 15, "they commanded"),
        (16, 23, "that the multitude kneel down"),
        (24, 28, "upon the earth,"),
        (29, 33, "and that they pray"),
        (34, 36, "unto the Father"),
        (37, 41, "in the name of Jesus."),
    ],
    7: [
        (0, 7, "And the disciples also prayed"),
        (8, 10, "unto the Father"),
        (11, 15, "in the name of Jesus."),
        (16, 19, "And it came to pass that"),
        (20, 21, "they arose"),
        (22, 26, "and ministered unto the people."),
    ],
    8: [
        (0, 7, "And when they had spoken"),
        (8, 11, "those same words"),
        (12, 15, "which Jesus spoke—"),
        (16, 21, "nothing differed"),
        (22, 27, "from the words Jesus spoke—"),
        (28, 28, "behold,"),
        (29, 32, "they knelt again"),
        (33, 38, "and prayed unto the Father"),
        (39, 43, "in the name of Jesus."),
    ],
    9: [
        (0, 4, "And they prayed"),
        (5, 7, "for that thing"),
        (8, 14, "which they most desired;"),
        (15, 18, "and they desired"),
        (19, 24, "that the Holy Ghost be given"),
        (25, 28, "unto them."),
    ],
    10: [
        (0, 7, "And when they had thus prayed"),
        (8, 11, "they went down"),
        (12, 17, "unto the edge of the water,"),
        (18, 25, "and the multitude followed"),
        (26, 29, "them."),
    ],
    11: [
        (0, 4, "And it came to pass that"),
        (5, 7, "Nephi went down"),
        (8, 12, "into the water"),
        (13, 16, "and was baptized."),
    ],
    12: [
        (0, 5, "And he arose"),
        (6, 8, "out of the water"),
        (9, 13, "and began to baptize."),
        (14, 20, "And he baptized them all"),
        (21, 26, "whom Jesus had chosen."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when they were all baptized"),
        (11, 16, "and came up out of the water,"),
        (17, 22, "the Holy Ghost descended"),
        (23, 27, "upon them,"),
        (28, 32, "and they were filled"),
        (33, 39, "with the Holy Ghost and fire."),
    ],
    14: [
        (0, 1, "And behold,"),
        (2, 5, "they were encircled"),
        (6, 9, "as if encircled"),
        (10, 12, "by fire;"),
        (13, 16, "and it came down"),
        (17, 19, "from heaven,"),
        (20, 28, "and the multitude saw it,"),
        (29, 32, "and bore record;"),
        (33, 37, "and angels descended"),
        (38, 40, "out of heaven"),
        (41, 47, "and ministered unto them."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 8, "while the angels ministered"),
        (9, 12, "unto the disciples,"),
        (13, 13, "behold,"),
        (14, 17, "Jesus came"),
        (18, 23, "and stood in the midst"),
        (24, 30, "and ministered unto them."),
    ],
    16: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he spoke"),
        (8, 12, "unto the multitude,"),
        (13, 16, "and commanded them"),
        (17, 22, "that they kneel down again"),
        (23, 27, "upon the earth,"),
        (28, 35, "and that his disciples also kneel down"),
        (36, 40, "upon the earth."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 11, "when they had all knelt down"),
        (12, 16, "upon the earth,"),
        (17, 20, "he commanded"),
        (21, 23, "his disciples"),
        (24, 26, "that they pray."),
    ],
    18: [
        (0, 1, "And behold,"),
        (2, 6, "they began to pray;"),
        (7, 11, "and they prayed"),
        (12, 13, "unto Jesus,"),
        (14, 17, "calling him"),
        (18, 21, "their Lord"),
        (22, 25, "and their God."),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 7, "Jesus departed"),
        (8, 14, "from the midst of them,"),
        (15, 18, "and went a little apart"),
        (19, 23, "from them"),
        (24, 28, "and bowed himself"),
        (29, 31, "to the earth,"),
        (32, 35, "and he said:"),
    ],
    20: [
        (0, 2, "O Father,"),
        (3, 6, "I give thanks"),
        (7, 9, "unto thee"),
        (10, 17, "that thou hast given the Holy Ghost"),
        (18, 24, "unto these whom"),
        (25, 27, "I have chosen;"),
        (28, 33, "and because of their belief"),
        (34, 36, "in me"),
        (37, 42, "I have chosen them"),
        (43, 45, "out of the world."),
    ],
    21: [
        (0, 2, "O Father,"),
        (3, 6, "I pray"),
        (7, 9, "unto thee"),
        (10, 16, "that thou give the Holy Ghost"),
        (17, 23, "unto all those who"),
        (24, 31, "shall believe in their words."),
    ],
    22: [
        (0, 2, "O Father,"),
        (3, 10, "thou hast given them"),
        (11, 13, "the Holy Ghost"),
        (14, 21, "because they believe in me;"),
        (22, 25, "and thou seest"),
        (26, 32, "they believe in me"),
        (33, 38, "because thou hearest them,"),
        (39, 46, "and they pray unto me;"),
        (47, 54, "and they pray unto me"),
        (55, 62, "because I am with them."),
    ],
    23: [
        (0, 5, "And now O Father,"),
        (6, 12, "I pray unto thee"),
        (13, 15, "for them,"),
        (16, 22, "and also all those who"),
        (23, 30, "shall believe in their words,"),
        (31, 37, "that they may believe in me,"),
        (38, 44, "that I may be"),
        (45, 49, "in them"),
        (50, 55, "as thou art,"),
        (56, 57, "O Father,"),
        (58, 62, "in me,"),
        (63, 67, "that we may be one."),
    ],
    24: [
        (0, 3, "And it came to pass that"),
        (4, 11, "when Jesus had thus prayed"),
        (12, 14, "unto the Father,"),
        (15, 19, "he came"),
        (20, 22, "unto his disciples,"),
        (23, 24, "and behold,"),
        (25, 28, "they continued still,"),
        (29, 33, "without ceasing,"),
        (34, 39, "to pray unto him;"),
        (40, 44, "and they multiplied not"),
        (45, 47, "many words,"),
        (48, 55, "for it was given unto them"),
        (56, 63, "what they should pray,"),
        (64, 68, "and they were filled"),
        (69, 70, "with desire."),
    ],
    25: [
        (0, 8, "And Jesus blessed them"),
        (9, 16, "as they prayed unto him;"),
        (17, 22, "and his countenance smiled"),
        (23, 25, "upon them,"),
        (26, 34, "and the light of his countenance shone"),
        (35, 38, "upon them,"),
        (39, 40, "and behold"),
        (41, 44, "they were white"),
        (45, 53, "as the face and garments of Jesus;"),
        (54, 55, "and behold"),
        (56, 59, "their whiteness"),
        (60, 62, "exceeded"),
        (63, 68, "the whiteness of all things,"),
        (69, 69, "yea,"),
        (70, 75, "truly there is nothing"),
        (76, 80, "upon the earth"),
        (81, 84, "that can be white"),
        (85, 88, "like this."),
    ],
    26: [
        (0, 4, "And Jesus said"),
        (5, 8, "unto them:"),
        (9, 12, "Continue ye to pray;"),
        (13, 16, "nevertheless"),
        (17, 23, "they ceased not praying."),
    ],
    27: [
        (0, 6, "And he turned away again"),
        (7, 10, "from them,"),
        (11, 16, "and went a little apart"),
        (17, 22, "and bowed himself"),
        (23, 25, "to the earth;"),
        (26, 31, "and he prayed again"),
        (32, 34, "unto the Father,"),
        (35, 37, "saying:"),
    ],
    28: [
        (0, 2, "O Father,"),
        (3, 6, "I give thanks"),
        (7, 9, "unto thee"),
        (10, 16, "that thou hast purified those"),
        (17, 21, "whom I have chosen,"),
        (22, 26, "because of their faith,"),
        (27, 31, "and I pray"),
        (32, 34, "for them,"),
        (35, 40, "and also those who"),
        (41, 47, "shall believe in their words,"),
        (48, 52, "that they may be purified"),
        (53, 55, "in me,"),
        (56, 63, "through faith in their words,"),
        (64, 69, "even as they are purified"),
        (70, 72, "in me."),
    ],
    29: [
        (0, 2, "O Father,"),
        (3, 6, "I pray not"),
        (7, 9, "for the world,"),
        (10, 13, "but for those"),
        (14, 20, "thou hast given me"),
        (21, 23, "out of the world,"),
        (24, 28, "because of their faith,"),
        (29, 33, "that they may be purified"),
        (34, 36, "in me,"),
        (37, 43, "that I may be"),
        (44, 48, "in them"),
        (49, 54, "as thou art,"),
        (55, 56, "O Father,"),
        (57, 61, "in me,"),
        (62, 66, "that we may be one,"),
        (67, 71, "that I may be glorified"),
        (72, 74, "in them."),
    ],
    30: [
        (0, 7, "And when Jesus had spoken"),
        (8, 10, "these words"),
        (11, 16, "he came again"),
        (17, 19, "unto his disciples;"),
        (20, 21, "and behold"),
        (22, 28, "they prayed still, without ceasing,"),
        (29, 31, "unto him;"),
        (32, 38, "and he smiled lovingly again"),
        (39, 41, "upon them;"),
        (42, 43, "and behold"),
        (44, 47, "they were white,"),
        (48, 52, "even as Jesus."),
    ],
    31: [
        (0, 3, "And it came to pass that"),
        (4, 9, "he went a little apart again"),
        (10, 13, "and prayed"),
        (14, 16, "unto the Father;"),
    ],
    32: [
        (0, 7, "And the tongue cannot speak"),
        (8, 14, "the words he prayed,"),
        (15, 22, "nor can any man write"),
        (23, 28, "the words he prayed."),
    ],
    33: [
        (0, 8, "And the multitude heard it"),
        (9, 11, "and they witnessed it;"),
        (12, 17, "and their hearts were opened"),
        (18, 24, "and they understood in their hearts"),
        (25, 30, "the words he prayed."),
    ],
    34: [
        (0, 3, "Nevertheless,"),
        (4, 9, "so exceedingly great and marvelous"),
        (10, 15, "were the words he prayed"),
        (16, 22, "they cannot be written,"),
        (23, 28, "nor can be uttered"),
        (29, 31, "by man."),
    ],
    35: [
        (0, 3, "And it came to pass that"),
        (4, 9, "when Jesus had ended"),
        (10, 12, "praying,"),
        (13, 18, "he came again"),
        (19, 21, "unto his disciples,"),
        (22, 24, "and said"),
        (25, 28, "unto them:"),
        (29, 33, "I have never seen"),
        (34, 38, "so great a faith"),
        (39, 44, "among all the Jews;"),
        (45, 46, "wherefore"),
        (47, 54, "I could not show"),
        (55, 58, "unto them"),
        (59, 63, "such great miracles,"),
        (64, 69, "because of their unbelief."),
    ],
    36: [
        (0, 5, "Verily I say"),
        (6, 8, "unto you,"),
        (9, 15, "there is none of them"),
        (16, 22, "who has seen such great things"),
        (23, 29, "as ye have seen;"),
        (30, 34, "nor have they heard"),
        (35, 39, "such great things"),
        (40, 46, "as ye have heard."),
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
