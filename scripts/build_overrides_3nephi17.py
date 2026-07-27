"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 17 — perceiving the
people are weak, Jesus bids them go home and ponder, but seeing their tears and
their longing that he stay, he is filled with compassion; he heals all their sick,
lame, blind, and afflicted; commands the little children be brought, kneels and
prays to the Father with words too great to be written, weeps, blesses the children
one by one, and angels descend encircled in fire to minister to them, the multitude
seeing and hearing things unspeakable that no tongue can utter.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi17.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 17

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "Behold,"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 12, "when Jesus had spoken"),
        (13, 15, "these words"),
        (16, 21, "he looked round about again"),
        (22, 26, "on the multitude,"),
        (27, 31, "and he said"),
        (32, 35, "unto them:"),
        (36, 36, "Behold,"),
        (37, 41, "my time has come."),
    ],
    2: [
        (0, 2, "I perceive"),
        (3, 5, "ye are weak,"),
        (6, 11, "ye cannot understand"),
        (12, 15, "all my words"),
        (16, 23, "which the Father commanded me"),
        (24, 29, "to speak unto you"),
        (30, 33, "at this time."),
    ],
    3: [
        (0, 1, "Therefore,"),
        (2, 5, "go ye"),
        (6, 9, "unto your homes,"),
        (10, 11, "and ponder"),
        (12, 14, "on the things which"),
        (15, 19, "I have said,"),
        (20, 22, "and ask"),
        (23, 25, "of the Father,"),
        (26, 28, "in my name,"),
        (29, 32, "that ye may understand,"),
        (33, 37, "and prepare your minds"),
        (38, 40, "for the morrow,"),
        (41, 46, "and I will come again"),
        (47, 49, "unto you."),
    ],
    4: [
        (0, 7, "But now I go"),
        (8, 10, "unto the Father,"),
        (11, 17, "and to manifest myself also"),
        (18, 23, "unto the lost tribes of Israel,"),
        (24, 30, "for they are not lost"),
        (31, 33, "unto the Father,"),
        (34, 38, "for he knows"),
        (39, 47, "the place whither he has taken them."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 11, "when Jesus had thus spoken,"),
        (12, 18, "he cast his eyes round about again"),
        (19, 25, "upon the multitude,"),
        (26, 28, "and saw"),
        (29, 33, "their tears were flowing,"),
        (34, 38, "and they gazed steadfastly"),
        (39, 41, "upon him"),
        (42, 46, "as if they desired"),
        (47, 52, "to ask him"),
        (53, 57, "that he stay"),
        (58, 61, "with them"),
        (62, 67, "for a little longer time."),
    ],
    6: [
        (0, 4, "And he said"),
        (5, 8, "unto them:"),
        (9, 9, "Behold,"),
        (10, 13, "my feelings are filled"),
        (14, 16, "with compassion"),
        (17, 19, "towards you."),
    ],
    7: [
        (0, 5, "Are there any"),
        (6, 9, "among you"),
        (10, 11, "who are sick?"),
        (12, 16, "Bring them here."),
        (17, 24, "Are there any of you"),
        (25, 26, "who are lame,"),
        (27, 29, "or blind,"),
        (30, 32, "or crippled,"),
        (33, 35, "or wounded,"),
        (36, 38, "or leprous,"),
        (39, 41, "or paralyzed,"),
        (42, 44, "or deaf,"),
        (45, 47, "or afflicted"),
        (48, 51, "in any way?"),
        (52, 56, "Bring them here"),
        (57, 64, "and I will heal them,"),
        (65, 69, "for I have great compassion"),
        (70, 72, "upon you;"),
        (73, 76, "my feelings are filled"),
        (77, 80, "with mercy."),
    ],
    8: [
        (0, 3, "For I perceive"),
        (4, 6, "ye desire"),
        (7, 13, "that I show unto you"),
        (14, 17, "what I did"),
        (18, 23, "unto your brethren at Jerusalem,"),
        (24, 27, "for I see"),
        (28, 32, "your faith is sufficient"),
        (33, 37, "that I heal you."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 11, "when he had thus spoken,"),
        (12, 16, "all went forth together"),
        (17, 20, "the multitude,"),
        (21, 25, "with their sick"),
        (26, 30, "and their afflicted,"),
        (31, 34, "and their lame,"),
        (35, 38, "and their blind,"),
        (39, 42, "and their dumb,"),
        (43, 48, "and all those who"),
        (49, 54, "were afflicted in any way;"),
        (55, 62, "and he healed them every one"),
        (63, 67, "when they were brought"),
        (68, 70, "unto him."),
    ],
    10: [
        (0, 4, "And they all,"),
        (5, 11, "all they who were healed"),
        (12, 18, "and they who were whole,"),
        (19, 24, "they bowed down"),
        (25, 27, "at his feet,"),
        (28, 30, "and worshipped"),
        (31, 33, "him;"),
        (34, 40, "and as many of them"),
        (41, 45, "of the multitude"),
        (46, 52, "who could come"),
        (53, 57, "kissed his feet,"),
        (58, 60, "insomuch that"),
        (61, 64, "they bathed his feet"),
        (65, 68, "with their tears."),
    ],
    11: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he commanded"),
        (8, 13, "that their little children be brought."),
    ],
    12: [
        (0, 1, "So"),
        (2, 5, "they brought"),
        (6, 9, "their little children"),
        (10, 16, "and set them down"),
        (17, 22, "upon the ground round about"),
        (23, 25, "him,"),
        (26, 29, "and Jesus stood"),
        (30, 32, "in the midst;"),
        (33, 40, "and the multitude gave way"),
        (41, 47, "until they were all brought"),
        (48, 50, "unto him."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 11, "when they were all brought,"),
        (12, 15, "and Jesus stood"),
        (16, 18, "in the midst,"),
        (19, 25, "he commanded the multitude"),
        (26, 30, "that they kneel down"),
        (31, 35, "upon the ground."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 8, "when they had knelt"),
        (9, 13, "upon the ground,"),
        (14, 16, "Jesus groaned"),
        (17, 22, "within himself,"),
        (23, 24, "and said:"),
        (25, 27, "O Father,"),
        (28, 31, "I am troubled"),
        (32, 37, "because of the wickedness of the people"),
        (38, 42, "of the house of Israel."),
    ],
    15: [
        (0, 6, "And when he had spoken"),
        (7, 9, "these words,"),
        (10, 15, "he himself also knelt"),
        (16, 20, "upon the earth;"),
        (21, 22, "and behold,"),
        (23, 27, "he prayed"),
        (28, 30, "unto the Father,"),
        (31, 38, "and the things he prayed"),
        (39, 43, "cannot be written,"),
        (44, 50, "and the multitude bore record"),
        (51, 57, "who heard him."),
    ],
    16: [
        (0, 4, "And after this manner"),
        (5, 9, "do they bear record:"),
        (10, 13, "Never has seen"),
        (14, 16, "the eye,"),
        (17, 21, "nor has heard before"),
        (22, 24, "the ear,"),
        (25, 30, "the greatness and marvelousness"),
        (31, 32, "of the things"),
        (33, 39, "as we saw and heard"),
        (40, 43, "Jesus speaking"),
        (44, 46, "unto the Father."),
    ],
    17: [
        (0, 6, "And no tongue can"),
        (7, 9, "speak them,"),
        (10, 15, "nor can any man"),
        (16, 17, "write them,"),
        (18, 24, "nor can the hearts of men"),
        (25, 28, "conceive the things"),
        (29, 32, "so great"),
        (33, 36, "and so marvelous"),
        (37, 43, "as we saw and heard"),
        (44, 48, "Jesus speaking;"),
        (49, 53, "and no man"),
        (54, 57, "can conceive"),
        (58, 61, "of the joy which"),
        (62, 67, "filled our hearts"),
        (68, 74, "at the time we heard"),
        (75, 80, "him praying"),
        (81, 83, "unto the Father"),
        (84, 86, "for us."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 9, "when Jesus had ended"),
        (10, 15, "praying unto the Father,"),
        (16, 19, "he arose;"),
        (20, 26, "but so exceedingly great was the joy"),
        (27, 31, "of the multitude"),
        (32, 35, "that they were overwhelmed."),
    ],
    19: [
        (0, 6, "And Jesus spoke"),
        (7, 10, "unto them,"),
        (11, 13, "and commanded"),
        (14, 16, "that they arise."),
    ],
    20: [
        (0, 3, "And they arose"),
        (4, 6, "from the earth,"),
        (7, 11, "and he said"),
        (12, 15, "unto them:"),
        (16, 18, "Blessed are ye"),
        (19, 23, "because of your faith."),
        (24, 27, "And now behold,"),
        (28, 31, "my joy is full."),
    ],
    21: [
        (0, 7, "And when he had spoken"),
        (8, 10, "these words,"),
        (11, 14, "he wept,"),
        (15, 22, "and the multitude witnessed"),
        (23, 24, "this thing,"),
        (25, 27, "and he took"),
        (28, 32, "their little children,"),
        (33, 33, "one by one,"),
        (34, 37, "and blessed them,"),
        (38, 40, "and prayed"),
        (41, 43, "unto the Father"),
        (44, 46, "for them."),
    ],
    22: [
        (0, 6, "And when he had done"),
        (7, 9, "this thing"),
        (10, 14, "he wept again;"),
    ],
    23: [
        (0, 4, "And he spoke"),
        (5, 9, "unto the multitude,"),
        (10, 12, "and said"),
        (13, 16, "unto them:"),
        (17, 17, "Behold"),
        (18, 21, "your little ones."),
    ],
    24: [
        (0, 5, "And as they looked"),
        (6, 11, "they cast up their eyes"),
        (12, 16, "towards heaven,"),
        (17, 20, "and they saw"),
        (21, 24, "the heavens open,"),
        (25, 30, "and they saw angels"),
        (31, 36, "descending out of heaven"),
        (37, 41, "as if being"),
        (42, 47, "in the midst of fire;"),
        (48, 54, "and they came down"),
        (55, 57, "and encircled about"),
        (58, 60, "those little children,"),
        (61, 66, "and they were encircled"),
        (67, 69, "with fire;"),
        (70, 74, "and the angels ministered"),
        (75, 78, "unto them."),
    ],
    25: [
        (0, 6, "And saw and heard and witnessed"),
        (7, 10, "the multitude;"),
        (11, 14, "and they know"),
        (15, 19, "their record is true"),
        (20, 26, "for they all saw and heard,"),
        (27, 32, "every man for himself;"),
        (33, 37, "and their number"),
        (38, 47, "was about two thousand five hundred"),
        (48, 48, "souls;"),
        (49, 54, "and they consisted"),
        (55, 56, "of men,"),
        (57, 57, "women,"),
        (58, 59, "and children."),
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
