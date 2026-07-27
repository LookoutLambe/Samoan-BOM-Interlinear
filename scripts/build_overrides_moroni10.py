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

    python3 build_overrides_moroni10.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 10

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "Now"),
        (2, 3, "I,"),
        (4, 5, "Moroni,"),
        (6, 9, "I do write"),
        (10, 11, "some things"),
        (12, 16, "which I myself deem"),
        (17, 18, "are good;"),
        (19, 23, "and I write forth"),
        (24, 26, "unto my brethren,"),
        (27, 29, "the Lamanites;"),
        (30, 33, "and I wish"),
        (34, 36, "that they know"),
        (37, 40, "have exceeded"),
        (41, 43, "four hundred"),
        (44, 48, "and twenty years"),
        (49, 51, "have gone by"),
        (52, 55, "since there was given"),
        (56, 58, "the sign"),
        (59, 62, "of the advent"),
        (63, 64, "of Christ."),
    ],
    2: [
        (0, 3, "And I do seal"),
        (4, 5, "these records,"),
        (6, 9, "after"),
        (10, 12, "I have spoken"),
        (13, 16, "a few words"),
        (17, 19, "by way of"),
        (20, 22, "exhortation"),
        (23, 25, "unto you."),
    ],
    3: [
        (0, 0, "Behold,"),
        (1, 4, "I do exhort"),
        (5, 7, "unto you"),
        (8, 11, "when ye read"),
        (12, 13, "these things,"),
        (14, 15, "if"),
        (16, 18, "it be according"),
        (19, 22, "to the wise will"),
        (23, 25, "of God"),
        (26, 28, "that ye read,"),
        (29, 33, "that ye may remember"),
        (34, 37, "the great tender mercy"),
        (38, 40, "of the Lord"),
        (41, 45, "unto the children of men,"),
        (46, 49, "from the creation"),
        (50, 51, "of Adam"),
        (52, 55, "even down unto"),
        (56, 58, "the time"),
        (59, 64, "that ye shall obtain"),
        (65, 66, "these things,"),
        (67, 70, "and meditate thereon"),
        (71, 74, "in your hearts."),
    ],
    4: [
        (0, 4, "And when ye obtain"),
        (5, 6, "these things,"),
        (7, 10, "I do exhort"),
        (11, 13, "unto you"),
        (14, 17, "that ye should ask"),
        (18, 20, "of God,"),
        (21, 23, "the Eternal Father,"),
        (24, 26, "in the name"),
        (27, 29, "of Jesus Christ,"),
        (30, 34, "whether are not true"),
        (35, 36, "these things;"),
        (37, 38, "and if"),
        (39, 42, "ye shall ask"),
        (43, 46, "with a true heart,"),
        (47, 50, "with real intent"),
        (51, 52, "therein,"),
        (53, 57, "and faith in Christ,"),
        (58, 63, "he will manifest"),
        (64, 68, "the truth of these things"),
        (69, 71, "unto you,"),
        (72, 74, "by the power"),
        (75, 78, "of the Holy Ghost."),
    ],
    5: [
        (0, 3, "And by the power"),
        (4, 7, "of the Holy Ghost"),
        (8, 13, "ye may know"),
        (14, 16, "the truth"),
        (17, 19, "of all things."),
    ],
    6: [
        (0, 4, "And whatever thing"),
        (5, 6, "is good"),
        (7, 10, "is just and true;"),
        (11, 14, "wherefore,"),
        (15, 18, "there is nothing"),
        (19, 20, "which is good"),
        (21, 22, "that denieth"),
        (23, 24, "the Christ,"),
        (25, 27, "but doth acknowledge"),
        (28, 32, "that he liveth."),
    ],
    7: [
        (0, 5, "And ye may know"),
        (6, 10, "that he liveth,"),
        (11, 13, "by the power"),
        (14, 17, "of the Holy Ghost;"),
        (18, 21, "wherefore"),
        (22, 26, "I do exhort"),
        (27, 29, "unto you"),
        (30, 33, "that ye deny not"),
        (34, 38, "the power of God;"),
        (39, 43, "for he doth work"),
        (44, 48, "by power,"),
        (49, 51, "according to"),
        (52, 53, "the faith"),
        (54, 58, "of the children of men,"),
        (59, 60, "the same"),
        (61, 63, "today"),
        (64, 65, "and tomorrow,"),
        (66, 68, "and for ever."),
    ],
    8: [
        (0, 2, "And again,"),
        (3, 6, "I do exhort"),
        (7, 9, "unto you,"),
        (10, 12, "my brethren,"),
        (13, 16, "that ye deny not"),
        (17, 20, "the gifts of God,"),
        (21, 25, "for they are many;"),
        (26, 29, "and are bestowed"),
        (30, 31, "they"),
        (32, 36, "from the one God."),
        (37, 40, "And divers are the ways"),
        (41, 43, "of doing"),
        (44, 45, "these gifts;"),
        (46, 49, "but it is God"),
        (50, 51, "the same"),
        (52, 56, "who doth work"),
        (57, 60, "in every thing"),
        (61, 64, "and in all;"),
        (65, 68, "and are granted"),
        (69, 70, "these gifts"),
        (71, 73, "by way of"),
        (74, 76, "the manifestations"),
        (77, 80, "of the Spirit of God"),
        (81, 82, "unto men,"),
        (83, 88, "that they be profited."),
    ],
    9: [
        (0, 1, "For behold,"),
        (2, 4, "is given"),
        (5, 7, "to one"),
        (8, 10, "by the Spirit"),
        (11, 13, "of God,"),
        (14, 20, "that he may teach"),
        (21, 25, "the word of wisdom;"),
    ],
    10: [
        (0, 3, "And to another,"),
        (4, 10, "that he may teach"),
        (11, 15, "the word of knowledge"),
        (16, 18, "by the Spirit"),
        (19, 22, "that same one;"),
    ],
    11: [
        (0, 3, "And to one,"),
        (4, 8, "exceeding great faith;"),
        (9, 12, "and to another,"),
        (13, 16, "the gifts of healing"),
        (17, 20, "by way of the"),
        (21, 23, "one Spirit;"),
    ],
    12: [
        (0, 2, "And again,"),
        (3, 5, "to one,"),
        (6, 11, "that he may do"),
        (12, 13, "great miracles;"),
    ],
    13: [
        (0, 2, "And again,"),
        (3, 5, "to another,"),
        (6, 11, "that he may prophesy"),
        (12, 13, "concerning"),
        (14, 16, "all things;"),
    ],
    14: [
        (0, 2, "And again,"),
        (3, 5, "to one,"),
        (6, 8, "the seeing"),
        (9, 10, "of angels"),
        (11, 14, "and ministering spirits;"),
    ],
    15: [
        (0, 2, "And again,"),
        (3, 5, "to another,"),
        (6, 8, "all kinds"),
        (9, 10, "of tongues;"),
    ],
    16: [
        (0, 2, "And again,"),
        (3, 5, "to one,"),
        (6, 8, "the interpretation"),
        (9, 10, "of languages"),
        (11, 15, "and divers kinds of tongues."),
    ],
    17: [
        (0, 4, "And all these gifts"),
        (5, 7, "do come"),
        (8, 10, "by way of"),
        (11, 14, "the Spirit of Christ;"),
        (15, 18, "and they come"),
        (19, 20, "them"),
        (21, 24, "unto each man,"),
        (25, 27, "according to"),
        (28, 29, "his will."),
    ],
    18: [
        (0, 5, "And I do exhort"),
        (6, 8, "unto you,"),
        (9, 12, "my beloved brethren,"),
        (13, 15, "that ye remember"),
        (16, 19, "every good gift"),
        (20, 23, "cometh from Christ."),
    ],
    19: [
        (0, 5, "And I would exhort"),
        (6, 8, "unto you,"),
        (9, 12, "my beloved brethren,"),
        (13, 15, "that ye remember"),
        (16, 19, "that he is the same"),
        (20, 20, "yesterday,"),
        (21, 22, "today,"),
        (23, 25, "and forever,"),
        (26, 30, "and all these gifts"),
        (31, 35, "of which I have spoken,"),
        (36, 38, "which are spiritual,"),
        (39, 44, "shall never be taken away,"),
        (45, 49, "or however long"),
        (50, 54, "shall endure"),
        (55, 56, "the world,"),
        (57, 58, "save only"),
        (59, 61, "according to"),
        (62, 65, "the unbelief"),
        (66, 70, "of the children of men."),
    ],
    20: [
        (0, 3, "Wherefore,"),
        (4, 9, "there must needs be"),
        (10, 12, "faith;"),
        (13, 14, "and if"),
        (15, 19, "there must be"),
        (20, 22, "faith,"),
        (23, 28, "there must also be"),
        (29, 31, "hope;"),
        (32, 33, "and if"),
        (34, 38, "there must be"),
        (39, 41, "hope,"),
        (42, 47, "there must also be"),
        (48, 51, "the pure love."),
    ],
    21: [
        (0, 3, "And unless"),
        (4, 7, "ye have"),
        (8, 10, "charity"),
        (11, 17, "cannot in any wise"),
        (18, 20, "ye be saved"),
        (21, 23, "in the kingdom"),
        (24, 26, "of God;"),
        (27, 29, "nor is possible"),
        (30, 32, "for you to be saved"),
        (33, 35, "in the kingdom"),
        (36, 38, "of God"),
        (39, 40, "if"),
        (41, 45, "ye have not"),
        (46, 47, "faith;"),
        (48, 52, "nor can ye,"),
        (53, 54, "if"),
        (55, 59, "ye have no hope."),
    ],
    22: [
        (0, 1, "And if"),
        (2, 6, "ye have not hope"),
        (7, 11, "ye must needs despair;"),
        (12, 15, "and there cometh"),
        (16, 17, "despair"),
        (18, 21, "because of iniquity."),
    ],
    23: [
        (0, 3, "And indeed spake"),
        (4, 4, "Christ"),
        (5, 8, "unto our fathers:"),
        (9, 13, "If ye have"),
        (14, 15, "faith,"),
        (16, 20, "ye are able to do"),
        (21, 23, "all things"),
        (24, 26, "that are expedient"),
        (27, 29, "unto me."),
    ],
    24: [
        (0, 5, "And now I speak"),
        (6, 8, "unto all the ends"),
        (9, 11, "of the world—"),
        (12, 15, "if cometh"),
        (16, 17, "the day"),
        (18, 20, "when is taken away"),
        (21, 24, "the power and gifts"),
        (25, 27, "of God"),
        (28, 31, "from among you,"),
        (32, 36, "it shall be even thus"),
        (37, 38, "because of"),
        (39, 41, "the unbelief."),
    ],
    25: [
        (0, 2, "And wo"),
        (3, 7, "unto the children of men"),
        (8, 9, "if"),
        (10, 13, "this be the case;"),
        (14, 20, "for there shall be no one"),
        (21, 24, "among you"),
        (25, 28, "who doeth good,"),
        (29, 30, "nay,"),
        (31, 35, "not one at all."),
        (36, 37, "For if"),
        (38, 42, "there is one"),
        (43, 46, "among you"),
        (47, 50, "who doeth good,"),
        (51, 56, "he shall labour"),
        (57, 61, "by the power and gifts"),
        (62, 64, "of God."),
    ],
    26: [
        (0, 2, "And wo"),
        (3, 6, "unto them"),
        (7, 8, "who"),
        (9, 12, "do not"),
        (13, 15, "these things"),
        (16, 17, "and die,"),
        (18, 21, "for they perish"),
        (22, 25, "in their sins,"),
        (26, 29, "and are not able"),
        (30, 33, "for them to be saved"),
        (34, 36, "in the kingdom"),
        (37, 39, "of God;"),
        (40, 44, "and I speak"),
        (45, 46, "this thing"),
        (47, 49, "according to"),
        (50, 52, "the words of Christ;"),
        (53, 58, "and I do not lie."),
    ],
    27: [
        (0, 4, "And I do exhort"),
        (5, 7, "unto you"),
        (8, 10, "that ye remember"),
        (11, 12, "these things;"),
        (13, 18, "for soon cometh"),
        (19, 21, "the time"),
        (22, 27, "that ye shall know"),
        (28, 31, "I do not lie,"),
        (32, 32, "for"),
        (33, 37, "ye shall see"),
        (38, 40, "me"),
        (41, 44, "at the judgment-bar"),
        (45, 47, "of God;"),
        (48, 53, "and shall say"),
        (54, 57, "the Lord God"),
        (58, 60, "unto you:"),
        (61, 66, "Did I not cry out"),
        (67, 69, "unto you"),
        (70, 71, "my words,"),
        (72, 74, "which were written"),
        (75, 77, "by this man,"),
        (78, 82, "even as one"),
        (83, 85, "crying forth"),
        (86, 88, "from the dead,"),
        (89, 89, "yea,"),
        (90, 92, "even like"),
        (93, 95, "one who"),
        (96, 98, "speaketh"),
        (99, 101, "from the dust?"),
    ],
    28: [
        (0, 3, "I do declare"),
        (4, 5, "these things"),
        (6, 8, "unto the fulfilment"),
        (9, 10, "of the prophecies."),
        (11, 13, "And behold,"),
        (14, 18, "shall come forth"),
        (19, 20, "they"),
        (21, 23, "from the mouth"),
        (24, 26, "of God"),
        (27, 29, "who endureth forever;"),
        (30, 36, "and shall come forth mightily"),
        (37, 38, "his word"),
        (39, 41, "from that generation"),
        (42, 44, "to another generation."),
    ],
    29: [
        (0, 5, "And shall reveal"),
        (6, 8, "God"),
        (9, 11, "unto you,"),
        (12, 14, "are true the things"),
        (15, 17, "which I have written."),
    ],
    30: [
        (0, 5, "And I again exhort"),
        (6, 8, "unto you,"),
        (9, 12, "that ye come forth"),
        (13, 14, "unto Christ,"),
        (15, 16, "and lay hold"),
        (17, 20, "on every good gift,"),
        (21, 25, "and touch not"),
        (26, 29, "the evil gift,"),
        (30, 33, "nor the thing"),
        (34, 36, "that is unclean."),
    ],
    31: [
        (0, 3, "And awake thou,"),
        (4, 6, "and arise"),
        (7, 9, "from the dust,"),
        (10, 11, "O Jerusalem;"),
        (12, 12, "yea,"),
        (13, 17, "and put on thy beautiful garments,"),
        (18, 22, "O daughter of Zion;"),
        (23, 26, "and strengthen thy stakes"),
        (27, 30, "and enlarge thy borders"),
        (31, 32, "forever,"),
        (33, 37, "that thou be no more confounded"),
        (38, 38, "thee,"),
        (39, 43, "that may be fulfilled"),
        (44, 46, "the covenants"),
        (47, 49, "of the Eternal Father"),
        (50, 53, "which he made"),
        (54, 56, "unto thee,"),
        (57, 59, "O house"),
        (60, 61, "of Israel."),
    ],
    32: [
        (0, 0, "Yea,"),
        (1, 2, "come forth"),
        (3, 4, "unto Christ,"),
        (5, 6, "and be perfected"),
        (7, 9, "in him,"),
        (10, 13, "and deny yourselves"),
        (14, 16, "of all things"),
        (17, 19, "which are ungodly;"),
        (20, 21, "and if"),
        (22, 26, "ye deny yourselves"),
        (27, 29, "of every thing"),
        (30, 32, "wholly ungodly,"),
        (33, 37, "and love God"),
        (38, 42, "with all your mind,"),
        (43, 43, "and heart,"),
        (44, 47, "and all strength,"),
        (48, 50, "then is sufficient"),
        (51, 54, "his grace"),
        (55, 56, "for you,"),
        (57, 61, "and by his grace"),
        (62, 67, "ye may be perfected"),
        (68, 69, "in Christ;"),
        (70, 71, "and if"),
        (72, 74, "ye are perfected"),
        (75, 76, "in Christ"),
        (77, 79, "through"),
        (80, 82, "the grace"),
        (83, 85, "of God,"),
        (86, 89, "there is no way"),
        (90, 95, "can ye deny"),
        (96, 100, "the power of God."),
    ],
    33: [
        (0, 3, "And now also,"),
        (4, 4, "if"),
        (5, 7, "ye are made perfect"),
        (8, 9, "in Christ"),
        (10, 12, "through"),
        (13, 15, "the grace"),
        (16, 18, "of God,"),
        (19, 21, "and deny not"),
        (22, 23, "his power,"),
        (24, 28, "then ye are made holy"),
        (29, 30, "in Christ"),
        (31, 34, "through the grace"),
        (35, 37, "of God,"),
        (38, 41, "by means of"),
        (42, 45, "the shedding of the blood"),
        (46, 47, "of Christ,"),
        (48, 51, "which lieth"),
        (52, 54, "in the covenant"),
        (55, 57, "of the Father"),
        (58, 60, "for the remission"),
        (61, 64, "of your sins,"),
        (65, 68, "that ye be holy,"),
        (69, 73, "without any blemish."),
    ],
    34: [
        (0, 2, "And now"),
        (3, 6, "I do say"),
        (7, 10, "unto you all,"),
        (11, 12, "farewell."),
        (13, 18, "I am soon to go"),
        (19, 20, "to rest"),
        (21, 23, "in the paradise"),
        (24, 26, "of God,"),
        (27, 29, "until again is joined"),
        (30, 31, "my spirit"),
        (32, 34, "and my body,"),
        (35, 37, "and I am brought"),
        (38, 40, "through the air"),
        (41, 43, "in triumph,"),
        (44, 47, "to meet you"),
        (48, 50, "before"),
        (51, 54, "the pleasing judgment-bar"),
        (55, 58, "of the great Jehovah,"),
        (59, 61, "the Everlasting Judge"),
        (62, 65, "of both the living"),
        (66, 69, "and the dead."),
        (70, 70, "Amen."),
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
