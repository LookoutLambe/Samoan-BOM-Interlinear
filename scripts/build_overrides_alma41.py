"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 41 — Alma continues
to his son Corianton on the plan of restoration: men restored to good or evil
according to their works and desires; wickedness never was happiness; the
carnal against the spiritual; do good and be restored good.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash baked tokens in this chapter.

    python3 build_overrides_alma41.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 41

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 11, "there are yet some"),
        (12, 12, "things"),
        (13, 17, "I would say"),
        (18, 22, "concerning the restoration"),
        (23, 25, "of which hath been spoken;"),
        (26, 27, "for behold,"),
        (28, 32, "there are some"),
        (33, 36, "who have wrested the meaning"),
        (37, 39, "of the scriptures,"),
        (40, 44, "and have gone far astray"),
        (45, 46, "thereby"),
        (47, 50, "because of this thing."),
        (51, 54, "And I perceive"),
        (55, 59, "that thy mind is worried also"),
        (60, 62, "concerning this thing."),
        (63, 64, "But behold,"),
        (65, 70, "I will explain"),
        (71, 72, "this thing"),
        (73, 75, "unto thee."),
    ],
    2: [
        (0, 3, "I say"),
        (4, 6, "unto thee,"),
        (7, 9, "my son,"),
        (10, 13, "the plan of"),
        (14, 15, "restoration"),
        (16, 17, "is requisite"),
        (18, 21, "with"),
        (22, 26, "the justice of God;"),
        (27, 29, "for it is requisite"),
        (30, 33, "that should be restored"),
        (34, 36, "all things"),
        (37, 40, "to their order"),
        (41, 43, "proper."),
        (44, 44, "Behold,"),
        (45, 49, "it is requisite"),
        (50, 51, "and just,"),
        (52, 56, "according to the power"),
        (57, 62, "and resurrection of Christ,"),
        (63, 66, "that should be restored"),
        (67, 70, "the soul of"),
        (71, 72, "man"),
        (73, 75, "to its body,"),
        (76, 80, "and every part"),
        (81, 83, "of the body"),
        (84, 87, "should be restored"),
        (88, 91, "to itself."),
    ],
    3: [
        (0, 2, "And it is requisite"),
        (3, 6, "with the justice of"),
        (7, 8, "God"),
        (9, 13, "that should be judged"),
        (14, 15, "men"),
        (16, 18, "according to"),
        (19, 21, "their works;"),
        (22, 25, "and if good were"),
        (26, 28, "their works"),
        (29, 32, "in this life,"),
        (33, 36, "and good were the desires"),
        (37, 40, "of their hearts,"),
        (41, 43, "that should also"),
        (44, 47, "at the last day"),
        (48, 51, "they be restored"),
        (52, 56, "unto that which is good."),
    ],
    4: [
        (0, 3, "And if evil are"),
        (4, 6, "their works"),
        (7, 10, "they shall be restored"),
        (11, 14, "unto them"),
        (15, 17, "for evil."),
        (18, 19, "Therefore,"),
        (20, 23, "shall be restored"),
        (24, 25, "all things"),
        (26, 29, "to their order"),
        (30, 32, "proper,"),
        (33, 36, "everything"),
        (37, 40, "to its own frame"),
        (41, 42, "natural—"),
        (43, 45, "the mortal"),
        (46, 47, "raised"),
        (48, 52, "to immortality,"),
        (53, 56, "the corruption"),
        (57, 59, "to incorruption—"),
        (60, 62, "raised"),
        (63, 65, "to happiness"),
        (66, 68, "endless"),
        (69, 74, "to inherit the kingdom of"),
        (75, 76, "God,"),
        (77, 80, "or misery"),
        (81, 83, "endless"),
        (84, 89, "to inherit the kingdom of"),
        (90, 91, "the devil;"),
        (92, 94, "the one"),
        (95, 98, "on the one hand,"),
        (99, 101, "the other"),
        (102, 105, "on the other hand—"),
    ],
    5: [
        (0, 2, "The one"),
        (3, 7, "raised to happiness"),
        (8, 12, "according to his desires"),
        (13, 15, "of happiness,"),
        (16, 19, "or good"),
        (20, 24, "according to his desires"),
        (25, 27, "of good;"),
        (28, 30, "and the other"),
        (31, 33, "to evil"),
        (34, 38, "according to his desires"),
        (39, 41, "of evil;"),
        (42, 42, "for"),
        (43, 49, "as he hath desired"),
        (50, 53, "to do evil"),
        (54, 57, "in the length of"),
        (58, 60, "the whole day,"),
        (61, 65, "even so"),
        (66, 69, "shall he have"),
        (70, 74, "his reward of evil"),
        (75, 78, "when cometh"),
        (79, 80, "the night."),
    ],
    6: [
        (0, 5, "And so it is"),
        (6, 9, "on the other hand."),
        (10, 14, "If he hath repented"),
        (15, 17, "of his sins,"),
        (18, 20, "and desired"),
        (21, 23, "righteousness"),
        (24, 29, "until the end of"),
        (30, 31, "his days,"),
        (32, 36, "even so"),
        (37, 40, "he shall be rewarded"),
        (41, 43, "unto righteousness."),
    ],
    7: [
        (0, 3, "These are they"),
        (4, 7, "who are redeemed"),
        (8, 10, "of the Lord;"),
        (11, 11, "yea,"),
        (12, 15, "these are they"),
        (16, 18, "that are taken out,"),
        (19, 20, "that are delivered"),
        (21, 24, "from that night of"),
        (25, 29, "endless darkness;"),
        (30, 34, "and thus they"),
        (35, 35, "stand"),
        (36, 37, "or fall;"),
        (38, 39, "for behold,"),
        (40, 42, "they are"),
        (43, 47, "their own judges,"),
        (48, 51, "whether they do"),
        (52, 53, "good"),
        (54, 57, "or do evil."),
    ],
    8: [
        (0, 1, "Now,"),
        (2, 6, "the decrees of God"),
        (7, 9, "are unalterable;"),
        (10, 11, "therefore,"),
        (12, 15, "is prepared"),
        (16, 18, "the way"),
        (19, 22, "that whosoever"),
        (23, 26, "willeth"),
        (27, 32, "may walk therein"),
        (33, 35, "and be saved."),
    ],
    9: [
        (0, 3, "And now behold,"),
        (4, 6, "my son,"),
        (7, 10, "do not again"),
        (11, 12, "risk"),
        (13, 16, "one more sin"),
        (17, 18, "single"),
        (19, 23, "against your God"),
        (24, 26, "concerning"),
        (27, 31, "those points of doctrine,"),
        (32, 36, "which ye have risked"),
        (37, 39, "even until"),
        (40, 43, "this time"),
        (44, 47, "to commit"),
        (48, 49, "sin."),
    ],
    10: [
        (0, 3, "Do not suppose,"),
        (4, 4, "because"),
        (5, 7, "it hath been spoken"),
        (8, 12, "concerning restoration,"),
        (13, 18, "that ye shall be restored"),
        (19, 21, "from sin"),
        (22, 24, "to happiness."),
        (25, 25, "Behold,"),
        (26, 29, "I say"),
        (30, 32, "unto you,"),
        (33, 36, "never was"),
        (37, 38, "wickedness"),
        (39, 40, "happiness."),
    ],
    11: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 8, "all men"),
        (9, 11, "that are"),
        (12, 15, "in a state of"),
        (16, 17, "nature,"),
        (18, 22, "or I would say,"),
        (23, 25, "are"),
        (26, 29, "in a carnal state,"),
        (30, 33, "are in"),
        (34, 36, "the gall of bitterness"),
        (37, 39, "and the bonds of"),
        (40, 41, "iniquity;"),
        (42, 45, "they are without"),
        (46, 48, "God"),
        (49, 51, "in the world,"),
        (52, 56, "and they have become"),
        (57, 61, "contrary to"),
        (62, 66, "the nature of God;"),
        (67, 68, "therefore,"),
        (69, 72, "they are"),
        (73, 75, "in a state"),
        (76, 80, "contrary to"),
        (81, 85, "the nature of happiness."),
    ],
    12: [
        (0, 3, "And now behold,"),
        (4, 7, "is the meaning"),
        (8, 11, "of the word"),
        (12, 13, "restoration"),
        (14, 17, "the taking"),
        (18, 20, "of a thing"),
        (21, 25, "from its natural state"),
        (26, 30, "and placing in a state"),
        (31, 35, "not its state"),
        (36, 37, "natural,"),
        (38, 42, "or place it in a state"),
        (43, 45, "opposite to"),
        (46, 48, "its true nature?"),
    ],
    13: [
        (0, 0, "O,"),
        (1, 3, "my son,"),
        (4, 6, "this is not"),
        (7, 9, "the case;"),
        (10, 13, "but the meaning"),
        (14, 17, "of the word"),
        (18, 19, "restoration,"),
        (20, 24, "is to bring back again"),
        (25, 27, "evil"),
        (28, 30, "for evil,"),
        (31, 34, "or carnal"),
        (35, 37, "for carnal,"),
        (38, 41, "or devilish"),
        (42, 44, "for devilish—"),
        (45, 47, "good"),
        (48, 52, "for that which is good;"),
        (53, 55, "righteous"),
        (56, 60, "for that which is righteous;"),
        (61, 64, "just"),
        (65, 69, "for that which is just;"),
        (70, 73, "merciful"),
        (74, 77, "for that which is"),
        (78, 79, "merciful."),
    ],
    14: [
        (0, 1, "Therefore,"),
        (2, 4, "my son,"),
        (5, 5, "see"),
        (6, 9, "that ye be merciful"),
        (10, 12, "unto your brethren;"),
        (13, 15, "deal justly,"),
        (16, 19, "judge righteously,"),
        (20, 23, "and do good"),
        (24, 26, "continually;"),
        (27, 31, "and if ye do"),
        (32, 34, "all these things"),
        (35, 38, "then shall ye receive"),
        (39, 41, "your reward;"),
        (42, 42, "yea,"),
        (43, 47, "shall be restored again"),
        (48, 50, "unto you"),
        (51, 53, "mercy;"),
        (54, 58, "shall be restored again"),
        (59, 61, "unto you"),
        (62, 63, "justice;"),
        (64, 68, "shall be restored again"),
        (69, 71, "unto you"),
        (72, 74, "a righteous judgment;"),
        (75, 80, "and shall be rewarded"),
        (81, 81, "again"),
        (82, 84, "unto you"),
        (85, 86, "good."),
    ],
    15: [
        (0, 0, "For"),
        (1, 3, "that which"),
        (4, 7, "ye send out"),
        (8, 13, "shall return again"),
        (14, 14, "indeed"),
        (15, 17, "unto you,"),
        (18, 20, "and be restored;"),
        (21, 22, "therefore,"),
        (23, 26, "the word of"),
        (27, 28, "restoration"),
        (29, 32, "more fully condemneth"),
        (33, 35, "the sinner,"),
        (36, 41, "and justifieth him not"),
        (42, 45, "at all."),
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
