"""
Hand-curated TAM-phrase gloss overrides for Mamona (Mormon) 3 — a ten-year respite in
which the Lord commands Mormon to cry repentance to the people in vain; the Lamanites
come again, the Nephites beat them in the strength of the land of Desolation, and the
people boast in their own strength and swear to avenge themselves; the Lord forbids them,
and Mormon, refusing to lead a people who delight in bloodshed and revenge, utterly
refuses from that time forth to be their commander.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, imperative 16). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

Em-dash pre-split applied to bom_books.json before glossing:
    3:2  nuu—Ia  ->  nuu—  +  Ia

    python3 build_overrides_mormon3.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "mormon"
CHAPTER_NUM = 3

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 7, "did not come again"),
        (8, 9, "the Lamanites"),
        (10, 11, "to battle"),
        (12, 13, "until had passed away"),
        (14, 16, "the other ten"),
        (17, 18, "of years."),
        (19, 20, "And behold,"),
        (21, 23, "I had employed"),
        (24, 25, "my people,"),
        (26, 28, "the Nephites,"),
        (29, 31, "in preparing"),
        (32, 35, "their lands"),
        (36, 39, "and their arms"),
        (40, 42, "against the time"),
        (43, 44, "of war."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 5, "did say"),
        (6, 7, "the Lord"),
        (8, 10, "unto me:"),
        (11, 12, "Cry"),
        (13, 15, "unto this people—"),
        (16, 18, "Repent ye,"),
        (19, 21, "and come"),
        (22, 24, "unto me,"),
        (25, 26, "and be ye baptized,"),
        (27, 29, "and build up again"),
        (30, 31, "my church,"),
        (32, 34, "and ye shall be spared"),
        (35, 36, "ye."),
    ],
    3: [
        (0, 3, "And I did cry"),
        (4, 6, "unto this people,"),
        (7, 10, "but it was in vain;"),
        (11, 15, "and they did not realize"),
        (16, 18, "that it was the Lord"),
        (19, 20, "that had spared"),
        (21, 22, "them,"),
        (23, 25, "and granted"),
        (26, 29, "unto them"),
        (30, 31, "a chance"),
        (32, 34, "for repentance."),
        (35, 36, "And behold"),
        (37, 39, "they did harden"),
        (40, 42, "their hearts"),
        (43, 44, "against"),
        (45, 47, "the Lord"),
        (48, 50, "their God."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 6, "after had passed away"),
        (7, 9, "this tenth year,"),
        (10, 13, "making in the whole"),
        (14, 16, "three hundred"),
        (17, 19, "and sixty"),
        (20, 21, "years"),
        (22, 22, "since"),
        (23, 25, "the coming"),
        (26, 27, "of Christ,"),
        (28, 30, "sent"),
        (31, 33, "the king"),
        (34, 36, "of the Lamanites"),
        (37, 38, "an epistle"),
        (39, 41, "unto me,"),
        (42, 42, "which"),
        (43, 46, "made known"),
        (47, 49, "unto me"),
        (50, 53, "that they were preparing"),
        (54, 57, "to come again"),
        (58, 61, "to battle against"),
        (62, 65, "us."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 6, "I did command"),
        (7, 9, "my people"),
        (10, 13, "that they should gather together"),
        (14, 16, "themselves"),
        (17, 19, "at the land"),
        (20, 21, "of Desolation,"),
        (22, 24, "to a city"),
        (25, 27, "which was in the borders,"),
        (28, 29, "by"),
        (30, 32, "the pass"),
        (33, 34, "narrow which"),
        (35, 37, "which led"),
        (38, 40, "into the land"),
        (41, 42, "southward."),
    ],
    6: [
        (0, 2, "And there"),
        (3, 7, "did we place"),
        (8, 10, "our armies,"),
        (11, 14, "that we might"),
        (15, 16, "stop"),
        (17, 18, "the armies"),
        (19, 21, "of the Lamanites,"),
        (22, 25, "that they should not"),
        (26, 28, "get possession"),
        (29, 31, "any"),
        (32, 35, "of our lands;"),
        (36, 37, "therefore"),
        (38, 41, "we did build"),
        (42, 42, "fortifications"),
        (43, 44, "with"),
        (45, 48, "all our force"),
        (49, 51, "against"),
        (52, 55, "them."),
    ],
    7: [
        (0, 2, "And it came to pass"),
        (3, 5, "in the year"),
        (6, 8, "three hundred"),
        (9, 12, "and sixty and first,"),
        (13, 15, "it came to pass that"),
        (16, 17, "came down"),
        (18, 19, "the Lamanites"),
        (20, 22, "to the city"),
        (23, 24, "of Desolation"),
        (25, 27, "to battle against"),
        (28, 31, "us;"),
        (32, 35, "and it came to pass that"),
        (36, 37, "we did beat"),
        (38, 39, "them"),
        (40, 43, "in that year,"),
        (44, 47, "insomuch that"),
        (48, 51, "they did return again"),
        (52, 56, "to their own lands."),
    ],
    8: [
        (0, 3, "And in the year"),
        (4, 6, "three hundred"),
        (7, 10, "and sixty and second,"),
        (11, 13, "they again"),
        (14, 18, "came down"),
        (19, 20, "to battle."),
        (21, 24, "And we again"),
        (25, 26, "did beat also"),
        (27, 28, "them,"),
        (29, 30, "and did slay"),
        (31, 33, "a great number"),
        (34, 36, "of them,"),
        (37, 39, "and were cast"),
        (40, 43, "their dead"),
        (44, 46, "into the sea."),
    ],
    9: [
        (0, 2, "And now,"),
        (3, 4, "because of"),
        (5, 7, "this great thing"),
        (8, 9, "which was done"),
        (10, 12, "by my people,"),
        (13, 15, "the Nephites,"),
        (16, 20, "they began to boast"),
        (21, 25, "in their own strength,"),
        (26, 30, "and began to swear"),
        (31, 33, "before"),
        (34, 35, "the heavens"),
        (36, 40, "that they would avenge"),
        (41, 42, "the blood"),
        (43, 46, "of their brethren"),
        (47, 48, "who"),
        (49, 50, "were slain"),
        (51, 51, "by"),
        (52, 54, "their enemies."),
    ],
    10: [
        (0, 3, "And they did swear"),
        (4, 6, "by the heavens,"),
        (7, 10, "and by the throne"),
        (11, 11, "also"),
        (12, 14, "of God,"),
        (15, 20, "that they would go up"),
        (21, 23, "to battle against"),
        (24, 27, "their enemies,"),
        (28, 30, "and would cut off"),
        (31, 32, "them"),
        (33, 35, "from"),
        (36, 37, "the land."),
    ],
    11: [
        (0, 2, "And I,"),
        (3, 4, "Mormon,"),
        (5, 9, "did utterly refuse"),
        (10, 11, "from"),
        (12, 13, "this time"),
        (14, 18, "forward"),
        (19, 22, "to be a commander"),
        (23, 25, "and a leader"),
        (26, 28, "of this people,"),
        (29, 30, "because of"),
        (31, 33, "their wickedness"),
        (34, 36, "and their"),
        (37, 38, "abomination."),
    ],
    12: [
        (0, 0, "Behold,"),
        (1, 3, "notwithstanding"),
        (4, 6, "their wickedness,"),
        (7, 9, "I had led"),
        (10, 11, "them,"),
        (12, 14, "I had led"),
        (15, 16, "them"),
        (17, 21, "many times"),
        (22, 24, "to battle,"),
        (25, 28, "and had loved"),
        (29, 32, "them,"),
        (33, 35, "according to"),
        (36, 37, "the love"),
        (38, 40, "of God"),
        (41, 44, "which was in me,"),
        (45, 48, "with all my heart;"),
        (49, 52, "and had been poured out"),
        (53, 54, "my soul"),
        (55, 57, "in prayer"),
        (58, 60, "unto my God"),
        (61, 64, "all the day long"),
        (65, 67, "for them;"),
        (68, 71, "nevertheless,"),
        (72, 73, "it was done"),
        (74, 78, "without faith,"),
        (79, 80, "because of"),
        (81, 82, "the hardness"),
        (83, 86, "of their hearts."),
    ],
    13: [
        (0, 3, "And thrice"),
        (4, 5, "I delivered"),
        (6, 7, "them"),
        (8, 9, "out of the hands"),
        (10, 13, "of their enemies,"),
        (14, 18, "and they repented not"),
        (19, 19, "at all"),
        (20, 20, "of"),
        (21, 23, "their sins."),
    ],
    14: [
        (0, 4, "And when they had sworn"),
        (5, 7, "by all"),
        (8, 10, "that was forbidden"),
        (11, 12, "them"),
        (13, 16, "by our Lord"),
        (17, 19, "and the Savior"),
        (20, 22, "Jesus Christ,"),
        (23, 28, "that they would go up"),
        (29, 32, "unto their enemies"),
        (33, 34, "to battle,"),
        (35, 37, "and avenge"),
        (38, 39, "the blood"),
        (40, 43, "of their brethren,"),
        (44, 44, "behold,"),
        (45, 47, "came"),
        (48, 49, "the voice"),
        (50, 52, "of the Lord"),
        (53, 55, "unto me,"),
        (56, 58, "saying:"),
    ],
    15: [
        (0, 2, "Vengeance"),
        (3, 6, "is mine,"),
        (7, 7, "and"),
        (8, 14, "I will repay;"),
        (15, 16, "and because"),
        (17, 19, "repented not"),
        (20, 21, "this people"),
        (22, 25, "after"),
        (26, 27, "I delivered"),
        (28, 29, "them,"),
        (30, 30, "behold,"),
        (31, 35, "shall be cut off"),
        (36, 37, "they"),
        (38, 38, "from"),
        (39, 40, "the earth."),
    ],
    16: [
        (0, 3, "And it came to pass that"),
        (4, 7, "I utterly refused"),
        (8, 11, "to go up"),
        (12, 14, "against"),
        (15, 16, "mine enemies;"),
        (17, 21, "and I did even"),
        (22, 24, "as"),
        (25, 27, "commanded me"),
        (28, 30, "the Lord;"),
        (31, 34, "and I did stand"),
        (35, 37, "as a witness"),
        (38, 39, "idle"),
        (40, 42, "to manifest"),
        (43, 45, "unto the world"),
        (46, 49, "the things which I saw"),
        (50, 53, "and heard,"),
        (54, 56, "according to"),
        (57, 57, "the manifestations"),
        (58, 60, "of the Spirit"),
        (61, 61, "which"),
        (62, 64, "had testified"),
        (65, 67, "of"),
        (68, 68, "things"),
        (69, 73, "which shall come."),
    ],
    17: [
        (0, 1, "Therefore"),
        (2, 6, "I write"),
        (7, 9, "unto you,"),
        (10, 11, "Gentiles,"),
        (12, 16, "and also unto you,"),
        (17, 18, "the house"),
        (19, 20, "of Israel,"),
        (21, 23, "when shall commence"),
        (24, 25, "the work,"),
        (26, 29, "shall be near"),
        (30, 31, "to prepare"),
        (32, 33, "ye"),
        (34, 37, "to return"),
        (38, 40, "to the land"),
        (41, 44, "of your inheritance;"),
    ],
    18: [
        (0, 1, "Yea, behold,"),
        (2, 5, "I write"),
        (6, 8, "unto all the ends"),
        (9, 11, "of the earth;"),
        (12, 12, "yea,"),
        (13, 15, "unto you,"),
        (16, 18, "twelve tribes"),
        (19, 20, "of Israel,"),
        (21, 22, "who"),
        (23, 26, "shall be judged"),
        (27, 29, "according to"),
        (30, 32, "your works"),
        (33, 35, "by the twelve"),
        (36, 39, "whom chose"),
        (40, 41, "Jesus"),
        (42, 46, "to be his disciples"),
        (47, 49, "in the land"),
        (50, 51, "of Jerusalem."),
    ],
    19: [
        (0, 4, "And I write"),
        (5, 5, "also"),
        (6, 8, "unto the portion"),
        (9, 10, "of the remnant"),
        (11, 13, "of this people,"),
        (14, 15, "who"),
        (16, 20, "shall also be judged"),
        (21, 23, "by the twelve"),
        (24, 27, "whom chose"),
        (28, 29, "Jesus"),
        (30, 32, "in this land;"),
        (33, 37, "and shall be judged"),
        (38, 39, "they"),
        (40, 43, "by the other twelve"),
        (44, 47, "whom chose"),
        (48, 49, "Jesus"),
        (50, 52, "in the land"),
        (53, 54, "of Jerusalem."),
    ],
    20: [
        (0, 3, "And these things"),
        (4, 6, "doth manifest"),
        (7, 9, "the Spirit"),
        (10, 12, "unto me;"),
        (13, 14, "therefore"),
        (15, 19, "I write"),
        (20, 23, "unto you all."),
        (24, 28, "And for this cause"),
        (29, 33, "I write"),
        (34, 36, "unto you,"),
        (37, 40, "that ye may know"),
        (41, 45, "ye shall all stand"),
        (46, 46, "all"),
        (47, 49, "before"),
        (50, 51, "the judgment-seat"),
        (52, 53, "of Christ,"),
        (54, 54, "yea,"),
        (55, 58, "every soul"),
        (59, 63, "who belongs"),
        (64, 68, "to the whole human family"),
        (69, 70, "of Adam;"),
        (71, 71, "and"),
        (72, 76, "ye shall stand"),
        (77, 78, "to be judged"),
        (79, 82, "of your works,"),
        (83, 85, "whether they be good"),
        (86, 88, "or evil;"),
    ],
    21: [
        (0, 4, "And that ye may believe"),
        (5, 5, "also"),
        (6, 8, "the gospel"),
        (9, 11, "of Jesus Christ,"),
        (12, 12, "which"),
        (13, 17, "ye shall have"),
        (18, 19, "among"),
        (20, 22, "you;"),
        (23, 26, "and that may have"),
        (27, 27, "also"),
        (28, 30, "the Jews,"),
        (31, 32, "the people"),
        (33, 35, "of the covenant"),
        (36, 38, "of the Lord,"),
        (39, 40, "other witness"),
        (41, 43, "apart from"),
        (44, 46, "him"),
        (47, 48, "whom"),
        (49, 51, "they saw"),
        (52, 55, "and heard,"),
        (56, 57, "that Jesus,"),
        (58, 59, "whom"),
        (60, 62, "they slew,"),
        (63, 67, "was the very Christ"),
        (68, 72, "and the very God."),
    ],
    22: [
        (0, 4, "And I would"),
        (5, 9, "if I could"),
        (10, 11, "persuade"),
        (12, 13, "all ye"),
        (14, 14, "the ends"),
        (15, 17, "of the earth"),
        (18, 20, "to repent"),
        (21, 22, "and prepare"),
        (23, 24, "to stand"),
        (25, 27, "before"),
        (28, 29, "the judgment-seat"),
        (30, 31, "of Christ."),
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
