"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 10 — after the
silence, the voice of Christ again mourns over the fallen, lamenting how oft he
would have gathered them as a hen gathers her chicks, but they would not; he
promises to gather the willing; the people at last cease weeping, the darkness of
three days ends, the earth's mourning turns to joy and praise; Mormon testifies
the destruction fulfilled the words of many prophets and of Zenos, Zenock, and
especially Samuel the Lamanite, and prepares to show the ministry of Christ.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi10.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 10

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And now behold,"),
        (4, 7, "it came to pass that heard"),
        (8, 13, "all the people of the land"),
        (14, 15, "these sayings,"),
        (16, 21, "and did witness of it."),
        (22, 26, "And after there passed"),
        (27, 28, "these sayings,"),
        (29, 32, "the land was silent"),
        (33, 39, "for the space of many hours;"),
    ],
    2: [
        (0, 0, "For"),
        (1, 7, "so great was the astonishment of the people"),
        (8, 10, "insomuch that"),
        (11, 17, "they ceased lamenting and howling"),
        (18, 20, "for the loss of"),
        (21, 26, "the people of their kindred"),
        (27, 29, "who were slain;"),
        (30, 31, "therefore"),
        (32, 37, "the whole land was silent"),
        (38, 44, "for the space of many hours."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 8, "there came again a voice"),
        (9, 10, "unto the people,"),
        (11, 16, "and all the people heard,"),
        (17, 21, "and did witness of it,"),
        (22, 24, "saying:"),
    ],
    4: [
        (0, 0, "O,"),
        (1, 4, "ye people of"),
        (5, 7, "these great cities"),
        (8, 10, "which have fallen,"),
        (11, 15, "who are descended"),
        (16, 17, "from Jacob,"),
        (18, 18, "yea,"),
        (19, 25, "who are of the house of Israel,"),
        (26, 28, "how oft"),
        (29, 33, "have I gathered you"),
        (34, 38, "as gathers"),
        (39, 41, "a hen"),
        (42, 43, "her chickens"),
        (44, 48, "under her wings,"),
        (49, 51, "and nourished you."),
    ],
    5: [
        (0, 5, "And I say again,"),
        (6, 7, "how oft"),
        (8, 14, "would I have gathered you"),
        (15, 19, "as gathers"),
        (20, 22, "a hen"),
        (23, 24, "her chickens"),
        (25, 29, "under her wings,"),
        (30, 30, "yea,"),
        (31, 38, "O ye people of the house of Israel,"),
        (39, 42, "who have fallen;"),
        (43, 43, "yea,"),
        (44, 51, "O ye people of the house of Israel,"),
        (52, 56, "ye who dwell"),
        (57, 58, "at Jerusalem,"),
        (59, 64, "like ye who"),
        (65, 66, "have fallen;"),
        (67, 67, "yea,"),
        (68, 70, "how oft"),
        (71, 77, "would I have gathered you"),
        (78, 82, "as gathers"),
        (83, 85, "a hen"),
        (86, 87, "her chickens,"),
        (88, 93, "but ye would not."),
    ],
    6: [
        (0, 0, "O,"),
        (1, 6, "ye house of Israel"),
        (7, 11, "whom I have spared,"),
        (12, 14, "how oft"),
        (15, 21, "would I gather you"),
        (22, 26, "as gathers"),
        (27, 29, "a hen"),
        (30, 31, "her chickens"),
        (32, 36, "under her wings,"),
        (37, 41, "if ye repent"),
        (42, 47, "and return unto me"),
        (48, 54, "with full purpose of heart."),
    ],
    7: [
        (0, 3, "But if not,"),
        (4, 8, "O house of Israel,"),
        (9, 12, "shall be made desolate"),
        (13, 18, "the places where ye dwell"),
        (19, 24, "until the time of"),
        (25, 29, "the fulfilling of the covenant"),
        (30, 33, "to your fathers."),
    ],
    8: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 12, "after the people had heard"),
        (13, 15, "these words,"),
        (16, 16, "behold,"),
        (17, 22, "they began to weep again"),
        (23, 24, "and howl"),
        (25, 27, "because of the loss of"),
        (28, 35, "the people of their kindred and friends."),
    ],
    9: [
        (0, 7, "And thus passed away"),
        (8, 10, "the three days."),
        (11, 15, "And in the morning,"),
        (16, 22, "the darkness vanished away"),
        (23, 27, "from off the land,"),
        (28, 35, "and the trembling of the earth passed;"),
        (36, 42, "and the rending of the rocks ceased,"),
        (43, 48, "and the terrible groaning ended,"),
        (49, 57, "and all the many tumultuous noises passed away."),
    ],
    10: [
        (0, 6, "And the earth cleaved together again,"),
        (7, 8, "that it stood;"),
        (9, 11, "and ceased"),
        (12, 14, "the mourning,"),
        (15, 17, "and the weeping,"),
        (18, 21, "and the wailing of the people"),
        (22, 25, "who were spared;"),
        (26, 28, "and was turned"),
        (29, 32, "their mourning"),
        (33, 35, "into joy,"),
        (36, 39, "and their wailing"),
        (40, 45, "into praise and thanksgiving"),
        (46, 51, "unto the Lord Jesus Christ,"),
        (52, 54, "their Redeemer."),
    ],
    11: [
        (0, 4, "And thus were fulfilled"),
        (5, 7, "at that time"),
        (8, 9, "the scriptures"),
        (10, 14, "which were spoken by the prophets."),
    ],
    12: [
        (0, 5, "And the portion of the people"),
        (6, 10, "who were more righteous"),
        (11, 12, "were spared,"),
        (13, 17, "and it was they"),
        (18, 21, "who received the prophets"),
        (22, 28, "and stoned them not with stones;"),
        (29, 34, "and it was they who"),
        (35, 39, "had not shed the blood"),
        (40, 43, "of the saints,"),
        (44, 47, "who were spared—"),
    ],
    13: [
        (0, 4, "And they were spared"),
        (5, 9, "and were not sunk"),
        (10, 13, "and buried"),
        (14, 16, "in the earth;"),
        (17, 21, "and they were not drowned"),
        (22, 27, "in the depths of the sea;"),
        (28, 32, "and they were not burned"),
        (33, 35, "by fire,"),
        (36, 39, "neither fell down"),
        (40, 45, "upon them anything"),
        (46, 51, "and crushed them to death;"),
        (52, 59, "and they were not carried away"),
        (60, 62, "in the whirlwind;"),
        (63, 67, "neither were they overwhelmed"),
        (68, 73, "by the vapor of smoke"),
        (74, 76, "and of darkness."),
    ],
    14: [
        (0, 2, "And now,"),
        (3, 7, "whoso reads,"),
        (8, 11, "let him understand;"),
        (12, 16, "he who has"),
        (17, 18, "the scriptures,"),
        (19, 23, "let him"),
        (24, 27, "search them,"),
        (28, 31, "and see and behold"),
        (32, 37, "whether all these deaths"),
        (38, 39, "and destructions"),
        (40, 42, "by fire,"),
        (43, 45, "and smoke,"),
        (46, 47, "and tempests,"),
        (48, 49, "and whirlwinds,"),
        (50, 55, "and the opening of the earth"),
        (56, 60, "to receive them,"),
        (61, 65, "and all these things"),
        (66, 72, "whether not the very fulfilling"),
        (73, 79, "of the prophecies of many holy prophets."),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 4, "I say"),
        (5, 7, "unto you,"),
        (8, 8, "Yea,"),
        (9, 12, "many of them"),
        (13, 15, "testified"),
        (16, 20, "concerning these things"),
        (21, 26, "at the coming of Christ,"),
        (27, 31, "and they were slain"),
        (32, 32, "because"),
        (33, 36, "they testified"),
        (37, 41, "concerning these things."),
    ],
    16: [
        (0, 0, "Yea,"),
        (1, 7, "the prophet Zenos testified"),
        (8, 12, "concerning these things,"),
        (13, 18, "and Zenock also spoke"),
        (19, 23, "concerning those things,"),
        (24, 24, "because"),
        (25, 29, "the two testified particularly"),
        (30, 35, "concerning us,"),
        (36, 39, "who are the remnant of"),
        (40, 43, "their seed."),
    ],
    17: [
        (0, 0, "Behold,"),
        (1, 9, "our father Jacob also testified"),
        (10, 16, "concerning a remnant of"),
        (17, 21, "the seed of Joseph."),
        (22, 23, "And behold,"),
        (24, 28, "are we not"),
        (29, 33, "a remnant of"),
        (34, 38, "the seed of Joseph?"),
        (39, 42, "And these things"),
        (43, 45, "which testify"),
        (46, 51, "concerning us,"),
        (52, 56, "are they not written"),
        (57, 61, "upon the plates of brass"),
        (62, 70, "which our father Lehi brought"),
        (71, 72, "from Jerusalem?"),
    ],
    18: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the ending of"),
        (7, 13, "the thirty-fourth year,"),
        (14, 14, "behold,"),
        (15, 20, "I will show"),
        (21, 23, "unto you,"),
        (24, 30, "the people of Nephi"),
        (31, 34, "who were spared,"),
        (35, 40, "and also those who"),
        (41, 45, "were called Lamanites,"),
        (46, 50, "who also were spared,"),
        (51, 57, "were shown unto them"),
        (58, 60, "great favors,"),
        (61, 64, "and were poured out"),
        (65, 70, "upon their heads"),
        (71, 73, "great blessings,"),
        (74, 76, "insomuch that"),
        (77, 82, "not long after passed"),
        (83, 88, "the ascension of Christ"),
        (89, 91, "into heaven,"),
        (92, 99, "he truly showed himself"),
        (100, 103, "unto them—"),
    ],
    19: [
        (0, 6, "In showing his body"),
        (7, 10, "unto them;"),
        (11, 14, "and ministering"),
        (15, 18, "unto them;"),
        (19, 25, "and an account of his ministry"),
        (26, 30, "shall be given"),
        (31, 33, "hereafter."),
        (34, 35, "Therefore,"),
        (36, 41, "I make an end of my words"),
        (42, 45, "for this time."),
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
