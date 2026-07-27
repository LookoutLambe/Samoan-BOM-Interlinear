"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 16 — Jesus tells of
yet other sheep (the lost tribes) to whom he must go; he commands the record be
kept so that in the latter day the fulness of the gospel may come to the Gentiles,
and through them to the scattered remnant of Jacob; he blesses the believing
Gentiles but warns that if they reject the gospel and sin against it, the fulness
shall be taken from them and given to the house of Israel, and that Israel shall
tread down and tear the unbelieving Gentiles as a lion among the flocks of sheep.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split applied to bom_books.json before glossing:
    16:8  talitonu—ona  ->  talitonu—  +  ona

    python3 build_overrides_3nephi16.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 16

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 4, "And verily, verily,"),
        (5, 8, "I say"),
        (9, 11, "unto you,"),
        (12, 17, "I have"),
        (18, 20, "other sheep,"),
        (21, 26, "which are not of this land,"),
        (27, 33, "nor of the land of Jerusalem,"),
        (34, 39, "nor in any part of"),
        (40, 43, "that land round about"),
        (44, 49, "where I have ministered."),
    ],
    2: [
        (0, 3, "For those"),
        (4, 8, "of whom I speak,"),
        (9, 14, "are they who"),
        (15, 18, "have not yet heard"),
        (19, 21, "my voice;"),
        (22, 31, "nor have I manifested myself to them"),
        (32, 35, "at any time."),
    ],
    3: [
        (0, 5, "But I have received a commandment"),
        (6, 8, "from the Father"),
        (9, 12, "that I go"),
        (13, 16, "unto them,"),
        (17, 23, "and they shall hear"),
        (24, 26, "my voice,"),
        (27, 32, "and shall be numbered together"),
        (33, 35, "with my sheep,"),
        (36, 40, "that there be one fold"),
        (41, 45, "and one shepherd;"),
        (46, 47, "therefore"),
        (48, 52, "I go"),
        (53, 57, "to manifest myself"),
        (58, 61, "unto them."),
    ],
    4: [
        (0, 4, "And I command"),
        (5, 7, "you"),
        (8, 12, "that ye write these words"),
        (13, 18, "after I am gone,"),
        (19, 25, "so that if they ask not"),
        (26, 31, "of the Father in my name"),
        (32, 36, "my people at Jerusalem,"),
        (37, 41, "they who"),
        (42, 46, "saw me"),
        (47, 50, "and were with me"),
        (51, 53, "in my ministry,"),
        (54, 59, "that they may obtain a knowledge"),
        (60, 64, "concerning you"),
        (65, 70, "by the Holy Ghost,"),
        (71, 74, "and also concerning"),
        (75, 77, "the other tribes"),
        (78, 82, "whom they know not,"),
        (83, 88, "these words shall be kept"),
        (89, 93, "which ye shall write"),
        (94, 99, "and shall be shown"),
        (100, 101, "unto the Gentiles,"),
        (102, 104, "that there may,"),
        (105, 111, "through the fulness of the Gentiles,"),
        (112, 115, "be brought in,"),
        (116, 120, "the remnant of"),
        (121, 123, "their seed,"),
        (124, 129, "who shall be scattered"),
        (130, 134, "upon the face of the earth"),
        (135, 140, "because of their unbelief,"),
        (141, 144, "or be brought them"),
        (145, 152, "to a knowledge of me,"),
        (153, 155, "their Redeemer."),
    ],
    5: [
        (0, 7, "And then will I gather them"),
        (8, 14, "from the four quarters of the earth;"),
        (15, 18, "then will I fulfil"),
        (19, 22, "the covenant which"),
        (23, 27, "the Father made"),
        (28, 31, "unto all the people of"),
        (32, 35, "the house of Israel."),
    ],
    6: [
        (0, 3, "And blessed are the Gentiles,"),
        (4, 8, "because of their belief"),
        (9, 11, "in me,"),
        (12, 18, "through the Holy Ghost,"),
        (19, 26, "which witnesses unto them"),
        (27, 31, "of me"),
        (32, 37, "and of the Father."),
    ],
    7: [
        (0, 0, "Behold,"),
        (1, 5, "because of their belief"),
        (6, 8, "in me,"),
        (9, 14, "saith the Father,"),
        (15, 22, "and because of your unbelief,"),
        (23, 27, "O house of Israel,"),
        (28, 32, "in the last days"),
        (33, 40, "shall the truth come"),
        (41, 42, "unto the Gentiles,"),
        (43, 50, "that be made known unto them"),
        (51, 55, "the fulness of these things."),
    ],
    8: [
        (0, 2, "But wo,"),
        (3, 8, "saith the Father,"),
        (9, 12, "unto those of the Gentiles"),
        (13, 15, "who believe not—"),
        (16, 16, "for"),
        (17, 23, "though they have come"),
        (24, 26, "to this land,"),
        (27, 30, "and scattered my people"),
        (31, 37, "who are of the house of Israel;"),
        (38, 43, "and my people who"),
        (44, 48, "are of the house of Israel"),
        (49, 51, "were cast out"),
        (52, 57, "from among them,"),
        (58, 64, "and were trodden underfoot"),
        (65, 67, "by them;"),
    ],
    9: [
        (0, 2, "And because of"),
        (3, 8, "the mercies of the Father"),
        (9, 10, "unto the Gentiles,"),
        (11, 16, "and also the judgments of the Father"),
        (17, 23, "upon my people who"),
        (24, 28, "are of the house of Israel,"),
        (29, 32, "verily, verily,"),
        (33, 36, "I say"),
        (37, 39, "unto you,"),
        (40, 45, "notwithstanding all these things,"),
        (46, 51, "and I have caused to be smitten"),
        (52, 55, "my people who"),
        (56, 60, "are of the house of Israel,"),
        (61, 63, "and to be afflicted,"),
        (64, 66, "and to be slain,"),
        (67, 70, "and to be cast out"),
        (71, 76, "from among them,"),
        (77, 82, "and to be hated by them,"),
        (83, 88, "and to become a thing mocked"),
        (89, 90, "and reviled"),
        (91, 96, "among them—"),
    ],
    10: [
        (0, 8, "And thus commands the Father"),
        (9, 12, "that I say"),
        (13, 15, "unto you:"),
        (16, 18, "In that day"),
        (19, 22, "when the Gentiles sin"),
        (23, 27, "against my gospel,"),
        (28, 34, "and reject the fulness of my gospel,"),
        (35, 36, "and be puffed up"),
        (37, 43, "in the pride of their hearts"),
        (44, 48, "above all nations,"),
        (49, 53, "and above all the people"),
        (54, 57, "of the whole earth,"),
        (58, 59, "and be filled"),
        (60, 65, "with all kinds of lies,"),
        (66, 67, "and deceits,"),
        (68, 69, "and mischiefs,"),
        (70, 75, "and all kinds of false witness,"),
        (76, 78, "and murders,"),
        (79, 81, "and priestcrafts,"),
        (82, 83, "and whoredoms,"),
        (84, 87, "and secret abominations;"),
        (88, 92, "and if they do"),
        (93, 95, "all those things,"),
        (96, 103, "and reject the fulness of my gospel,"),
        (104, 104, "behold,"),
        (105, 109, "saith the Father,"),
        (110, 119, "I will take the fulness of my gospel"),
        (120, 125, "from among them."),
    ],
    11: [
        (0, 4, "And then will I remember"),
        (5, 7, "my covenant"),
        (8, 13, "which I made with my people,"),
        (14, 18, "O house of Israel,"),
        (19, 26, "and I will bring my gospel"),
        (27, 30, "unto them."),
    ],
    12: [
        (0, 5, "And I will show"),
        (6, 9, "unto thee,"),
        (10, 14, "O house of Israel,"),
        (15, 23, "the Gentiles shall not have power"),
        (24, 27, "over you;"),
        (28, 35, "but I will remember my covenant"),
        (36, 38, "unto you,"),
        (39, 43, "O house of Israel,"),
        (44, 50, "and ye shall come"),
        (51, 54, "unto the knowledge of"),
        (55, 59, "the fulness of my gospel."),
    ],
    13: [
        (0, 4, "But if the Gentiles repent"),
        (5, 10, "and return unto me,"),
        (11, 16, "saith the Father,"),
        (17, 17, "behold"),
        (18, 23, "they shall be numbered"),
        (24, 28, "among my people,"),
        (29, 33, "the house of Israel."),
    ],
    14: [
        (0, 6, "And I will not permit"),
        (7, 8, "my people,"),
        (9, 15, "who are of the house of Israel,"),
        (16, 24, "to go among them,"),
        (25, 30, "and tread them down,"),
        (31, 36, "saith the Father."),
    ],
    15: [
        (0, 8, "But if they will not turn"),
        (9, 11, "unto me,"),
        (12, 14, "and hearken"),
        (15, 17, "unto my voice,"),
        (18, 24, "I will deliver them up,"),
        (25, 25, "yea,"),
        (26, 32, "I will deliver up my people,"),
        (33, 37, "the house of Israel,"),
        (38, 48, "that they go among them,"),
        (49, 54, "and tread them down,"),
        (55, 61, "and they shall become"),
        (62, 66, "as salt"),
        (67, 70, "that has no savor,"),
        (71, 75, "and from that time"),
        (76, 79, "it is good for nothing"),
        (80, 85, "but only to be cast out,"),
        (86, 91, "and trodden under the feet"),
        (92, 94, "of my people,"),
        (95, 99, "the house of Israel."),
    ],
    16: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 18, "thus has the Father commanded me—"),
        (19, 24, "that I should give"),
        (25, 27, "unto this people"),
        (28, 29, "this land"),
        (30, 35, "to be their inheritance."),
    ],
    17: [
        (0, 4, "And then shall be fulfilled"),
        (5, 11, "the words of the prophet Isaiah,"),
        (12, 14, "which say:"),
    ],
    18: [
        (0, 7, "Thy watchmen shall lift up"),
        (8, 9, "the voice;"),
        (10, 16, "and they shall sing together"),
        (17, 19, "with the voice,"),
        (20, 25, "for they shall see"),
        (26, 28, "one another face to face"),
        (29, 33, "when Zion is brought again"),
        (34, 36, "by the Lord."),
    ],
    19: [
        (0, 4, "Cry out with joy,"),
        (5, 7, "sing together,"),
        (8, 12, "ye waste places of Jerusalem,"),
        (13, 18, "for the Lord has comforted"),
        (19, 20, "his people,"),
        (21, 24, "he has redeemed Jerusalem."),
    ],
    20: [
        (0, 4, "The Lord has made bare"),
        (5, 7, "his holy arm"),
        (8, 12, "in the eyes of all nations;"),
        (13, 22, "and all the ends of the earth shall see"),
        (23, 28, "the salvation of God."),
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
