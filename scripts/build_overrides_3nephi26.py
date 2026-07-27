"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 26 — Jesus expounds all
things from the beginning to the last day, quotes what would befall the earth, and
declares that greater things than these were shown but forbidden to be written. He
commands the record be kept; the disciples teach, baptize, and are filled with the
Holy Ghost and with fire; and the more part of these sayings are forbidden to be
written for the trying of the people's faith, that greater things be withheld until
after they receive the lesser.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split applied to bom_books.json before glossing:
    26:3  mamalu—ioe,  ->  mamalu—  +  ioe,

    python3 build_overrides_3nephi26.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 26

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 8, "when had told"),
        (9, 10, "Jesus"),
        (11, 12, "these things"),
        (13, 16, "he expounded"),
        (17, 18, "them"),
        (19, 23, "unto the multitude;"),
        (24, 28, "and he did expound"),
        (29, 30, "all things"),
        (31, 34, "unto them,"),
        (35, 37, "both great things"),
        (38, 40, "and small things."),
    ],
    2: [
        (0, 4, "And he said:"),
        (5, 8, "These scriptures,"),
        (9, 9, "which"),
        (10, 13, "were not present"),
        (14, 16, "with you,"),
        (17, 19, "commanded"),
        (20, 21, "the Father"),
        (22, 27, "that I should give"),
        (28, 30, "unto you;"),
        (31, 31, "for"),
        (32, 35, "the wisdom which"),
        (36, 39, "was in him"),
        (40, 44, "that they should be given"),
        (45, 46, "them"),
        (47, 48, "unto the generations"),
        (49, 51, "of the future."),
    ],
    3: [
        (0, 3, "And he did expound"),
        (4, 5, "all things,"),
        (6, 8, "even from"),
        (9, 10, "the beginning"),
        (11, 13, "until"),
        (14, 15, "the time"),
        (16, 21, "that he should come"),
        (22, 24, "in his glory—"),
        (25, 25, "yea,"),
        (26, 29, "even all things"),
        (30, 34, "which should come"),
        (35, 39, "upon the face of the earth,"),
        (40, 43, "even until"),
        (44, 45, "the elements melt"),
        (46, 49, "with fervent heat,"),
        (50, 52, "and be wrapt together"),
        (53, 54, "the earth"),
        (55, 58, "as a"),
        (59, 60, "rolled scroll,"),
        (61, 67, "and should pass away"),
        (68, 69, "the heavens"),
        (70, 72, "and the earth;"),
    ],
    4: [
        (0, 4, "And even unto"),
        (5, 7, "the great day"),
        (8, 9, "and last,"),
        (10, 15, "when shall stand"),
        (16, 17, "all people,"),
        (18, 20, "and all kindreds,"),
        (21, 23, "and all nations,"),
        (24, 26, "and diverse tongues,"),
        (27, 29, "before"),
        (30, 31, "God,"),
        (32, 33, "to be judged"),
        (34, 36, "of their works,"),
        (37, 39, "whether they be good"),
        (40, 42, "or whether they be evil—"),
    ],
    5: [
        (0, 2, "If were good"),
        (3, 4, "they,"),
        (5, 7, "they rise"),
        (8, 11, "to everlasting life;"),
        (12, 15, "and if were evil"),
        (16, 17, "they,"),
        (18, 20, "they rise"),
        (21, 23, "to damnation;"),
        (24, 26, "standing opposite,"),
        (27, 29, "the one"),
        (30, 33, "on the one side"),
        (34, 36, "and the other"),
        (37, 40, "on the other side,"),
        (41, 43, "according to"),
        (44, 46, "the mercy,"),
        (47, 49, "and the justice,"),
        (50, 53, "and the holiness which"),
        (54, 56, "is in Christ,"),
        (57, 61, "who was"),
        (62, 64, "before was begun"),
        (65, 66, "the world."),
    ],
    6: [
        (0, 2, "And now"),
        (3, 7, "there cannot be written"),
        (8, 10, "in this book"),
        (11, 13, "even"),
        (14, 16, "a hundredth part"),
        (17, 18, "of the things"),
        (19, 23, "which did truly teach"),
        (24, 25, "Jesus"),
        (26, 28, "unto the people;"),
    ],
    7: [
        (0, 1, "But behold"),
        (2, 4, "there is"),
        (5, 6, "in the plates"),
        (7, 8, "of Nephi"),
        (9, 11, "the greater part"),
        (12, 14, "of the things"),
        (15, 18, "which he taught"),
        (19, 21, "the people."),
    ],
    8: [
        (0, 3, "And these things"),
        (4, 6, "have I written,"),
        (7, 11, "which are a lesser part"),
        (12, 14, "of the things"),
        (15, 18, "which he taught"),
        (19, 21, "the people;"),
        (22, 25, "and I have written"),
        (26, 27, "them"),
        (28, 30, "to the intent"),
        (31, 35, "that may be brought again"),
        (36, 37, "them"),
        (38, 40, "unto this people,"),
        (41, 41, "from"),
        (42, 42, "the Gentiles,"),
        (43, 45, "according to"),
        (46, 48, "the words which"),
        (49, 51, "hath spoken"),
        (52, 52, "Jesus."),
    ],
    9: [
        (0, 5, "And when they shall have received"),
        (6, 7, "this thing,"),
        (8, 8, "which"),
        (9, 14, "they must receive first,"),
        (15, 17, "to try"),
        (18, 20, "their faith,"),
        (21, 24, "and if it shall so be"),
        (25, 29, "that they shall believe"),
        (30, 32, "these things,"),
        (33, 37, "then shall be made manifest"),
        (38, 41, "unto them"),
        (42, 45, "the greater things."),
    ],
    10: [
        (0, 3, "And if it so be"),
        (4, 9, "that they will not believe"),
        (10, 12, "these things,"),
        (13, 15, "then shall be withheld"),
        (16, 20, "the greater things"),
        (21, 21, "from"),
        (22, 25, "them,"),
        (26, 28, "unto the condemnation"),
        (29, 31, "of them."),
    ],
    11: [
        (0, 0, "Behold,"),
        (1, 7, "I was about to write"),
        (8, 9, "them,"),
        (10, 12, "all things which"),
        (13, 14, "were engraven"),
        (15, 18, "upon the plates"),
        (19, 20, "of Nephi,"),
        (21, 23, "but it was forbidden"),
        (24, 26, "by the Lord,"),
        (27, 29, "saying:"),
        (30, 34, "I will try"),
        (35, 36, "the faith"),
        (37, 39, "of my people."),
    ],
    12: [
        (0, 1, "Therefore,"),
        (2, 3, "I,"),
        (4, 5, "Mormon,"),
        (6, 8, "do write"),
        (9, 10, "the things"),
        (11, 14, "which I was commanded"),
        (15, 17, "of the Lord."),
        (18, 20, "And now,"),
        (21, 22, "I,"),
        (23, 24, "Mormon,"),
        (25, 28, "make an end"),
        (29, 30, "of my sayings,"),
        (31, 34, "and proceed to write"),
        (35, 36, "the things"),
        (37, 40, "which have been commanded me."),
    ],
    13: [
        (0, 1, "Therefore,"),
        (2, 4, "I would"),
        (5, 7, "that ye behold"),
        (8, 12, "did truly teach"),
        (13, 15, "the Lord"),
        (16, 17, "the people,"),
        (18, 21, "for the space of"),
        (22, 24, "three days;"),
        (25, 29, "and after that"),
        (30, 37, "he did show himself oft"),
        (38, 41, "unto them,"),
        (42, 45, "and did break oft"),
        (46, 47, "the bread,"),
        (48, 49, "and bless it,"),
        (50, 51, "and give it"),
        (52, 55, "unto them."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he did teach"),
        (7, 9, "and minister"),
        (10, 11, "unto the children"),
        (12, 16, "of the multitude"),
        (17, 18, "of whom"),
        (19, 20, "hath been spoken,"),
        (21, 23, "and he did loose"),
        (24, 26, "their tongues,"),
        (27, 31, "and they did speak"),
        (32, 35, "unto their fathers"),
        (36, 37, "great things"),
        (38, 40, "and marvelous,"),
        (41, 46, "even greater than"),
        (47, 49, "than the things"),
        (50, 53, "which he had revealed"),
        (54, 56, "unto the people;"),
        (57, 60, "and he loosed"),
        (61, 63, "their tongues"),
        (64, 70, "that they could speak."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 10, "after he had ascended"),
        (11, 13, "into heaven—"),
        (14, 18, "the second time"),
        (19, 26, "that he showed himself"),
        (27, 30, "unto them,"),
        (31, 35, "and had gone"),
        (36, 38, "unto the Father,"),
        (39, 45, "after he had healed"),
        (46, 51, "all their sick,"),
        (52, 55, "and their lame,"),
        (56, 57, "and opened"),
        (58, 58, "the eyes"),
        (59, 62, "of their blind"),
        (63, 64, "and unstopped"),
        (65, 65, "the ears"),
        (66, 68, "of the deaf,"),
        (69, 74, "and even had done"),
        (75, 79, "all manner of cures"),
        (80, 85, "among them,"),
        (86, 87, "and raised"),
        (88, 89, "a man"),
        (90, 92, "from the dead,"),
        (93, 97, "and had shown forth"),
        (98, 100, "his power"),
        (101, 104, "unto them,"),
        (105, 107, "and had ascended"),
        (108, 110, "unto the Father—"),
    ],
    16: [
        (0, 0, "Behold,"),
        (1, 2, "it came to pass"),
        (3, 8, "on the following day"),
        (9, 12, "gathered together"),
        (13, 16, "the multitude"),
        (17, 19, "themselves,"),
        (20, 23, "and they saw"),
        (24, 25, "and heard"),
        (26, 27, "these children;"),
        (28, 28, "yea,"),
        (29, 32, "even"),
        (33, 33, "babes"),
        (34, 35, "did open"),
        (36, 38, "their mouths"),
        (39, 41, "and utter"),
        (42, 44, "marvelous things;"),
        (45, 47, "and the things"),
        (48, 52, "which they did utter"),
        (53, 54, "were forbidden"),
        (55, 57, "it was not permitted"),
        (58, 61, "for any man"),
        (62, 63, "to write"),
        (64, 65, "them."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 6, "the disciples began"),
        (7, 10, "whom Jesus had chosen"),
        (11, 13, "from that time"),
        (14, 19, "and forward"),
        (20, 21, "to baptize"),
        (22, 24, "and to teach"),
        (25, 28, "as many as"),
        (29, 31, "did come"),
        (32, 35, "unto them;"),
        (36, 44, "and as many"),
        (45, 46, "as were baptized"),
        (47, 51, "in the name of Jesus"),
        (52, 53, "were filled"),
        (54, 57, "with the Holy Ghost."),
    ],
    18: [
        (0, 3, "And many"),
        (4, 6, "of them"),
        (7, 8, "saw"),
        (9, 10, "and heard"),
        (11, 12, "things"),
        (13, 15, "unspeakable,"),
        (16, 16, "which"),
        (17, 20, "are not lawful"),
        (21, 22, "to be written."),
    ],
    19: [
        (0, 4, "And they taught,"),
        (5, 7, "and did minister"),
        (8, 10, "one"),
        (11, 13, "to another;"),
        (14, 18, "and they had"),
        (19, 22, "all things in common"),
        (23, 24, "among"),
        (25, 28, "them,"),
        (29, 30, "dealing justly"),
        (31, 32, "every man,"),
        (33, 35, "one"),
        (36, 38, "with another,"),
        (39, 40, "in the dealings"),
        (41, 43, "which they made."),
    ],
    20: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they did"),
        (6, 7, "all things"),
        (8, 13, "even as had commanded"),
        (14, 15, "them"),
        (16, 17, "Jesus."),
    ],
    21: [
        (0, 3, "And they"),
        (4, 5, "who"),
        (6, 7, "were baptized"),
        (8, 12, "in the name of Jesus"),
        (13, 14, "were called"),
        (15, 17, "the church"),
        (18, 19, "of Christ."),
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
