"""
Hand-curated TAM-phrase gloss overrides for Mamona (Mormon) 7 — Mormon's closing
exhortation to the remnant of the house of Israel: know ye that ye are of the house of
Israel, lay down your weapons of war, repent and be baptized, believe in Jesus Christ
and in the record which shall come from the Gentiles; for this is written that ye may
believe the gospel, and if ye believe it ye shall be saved.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_mormon7.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "mormon"
CHAPTER_NUM = 7

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 3, "behold,"),
        (4, 8, "I would speak"),
        (9, 9, "somewhat"),
        (10, 14, "unto the remnant"),
        (15, 17, "of this people"),
        (18, 21, "who are spared,"),
        (22, 25, "if it so be"),
        (26, 28, "should give"),
        (29, 31, "God"),
        (32, 35, "unto them"),
        (36, 37, "my words,"),
        (38, 43, "that they may know"),
        (44, 44, "the things"),
        (45, 46, "concerning"),
        (47, 50, "of their fathers;"),
        (51, 51, "yea,"),
        (52, 55, "I speak"),
        (56, 58, "unto you,"),
        (59, 61, "ye remnant"),
        (62, 63, "who remain"),
        (64, 68, "of the house of Israel;"),
        (69, 72, "and these are the words"),
        (73, 77, "which I speak:"),
    ],
    2: [
        (0, 2, "Know ye"),
        (3, 4, "that ye are"),
        (5, 9, "of the house of Israel."),
    ],
    3: [
        (0, 2, "Know ye"),
        (3, 7, "that ye must repent,"),
        (8, 9, "or else"),
        (10, 14, "cannot be saved"),
        (15, 15, "ye."),
    ],
    4: [
        (0, 2, "Know ye"),
        (3, 7, "that ye must lay"),
        (8, 9, "down"),
        (10, 14, "your weapons of war,"),
        (15, 19, "and delight no more"),
        (20, 22, "in the shedding"),
        (23, 25, "of blood,"),
        (26, 30, "and take up no more"),
        (31, 32, "them,"),
        (33, 36, "save should be commanded"),
        (37, 37, "you"),
        (38, 40, "by God."),
    ],
    5: [
        (0, 2, "Know ye"),
        (3, 7, "that ye must understand"),
        (8, 9, "concerning"),
        (10, 13, "your fathers,"),
        (14, 15, "and repent"),
        (16, 19, "of all your sins"),
        (20, 21, "and iniquities,"),
        (22, 23, "and believe"),
        (24, 26, "in Jesus Christ,"),
        (27, 28, "that he is"),
        (29, 31, "the Son"),
        (32, 34, "of God,"),
        (35, 39, "and was slain"),
        (40, 42, "by the Jews,"),
        (43, 48, "and hath risen again"),
        (49, 50, "through"),
        (51, 53, "the power"),
        (54, 56, "of the Father,"),
        (57, 58, "whereby"),
        (59, 63, "he hath gained"),
        (64, 65, "the victory"),
        (66, 68, "over the grave;"),
        (69, 73, "and also is swallowed up"),
        (74, 76, "in him"),
        (77, 78, "the sting"),
        (79, 81, "of death."),
    ],
    6: [
        (0, 4, "And he hath brought to pass"),
        (5, 7, "the resurrection"),
        (8, 11, "of the dead,"),
        (12, 13, "whereby"),
        (14, 19, "shall be raised up"),
        (20, 21, "man"),
        (22, 23, "to stand"),
        (24, 25, "before"),
        (26, 28, "his judgment-seat."),
    ],
    7: [
        (0, 4, "And he hath brought to pass"),
        (5, 9, "the redemption of the world,"),
        (10, 10, "whereby"),
        (11, 16, "shall be brought"),
        (17, 19, "unto him"),
        (20, 23, "who is found"),
        (24, 26, "without condemnation"),
        (27, 29, "before him"),
        (30, 33, "at the day of judgment,"),
        (34, 35, "to dwell"),
        (36, 40, "in the presence of God"),
        (41, 43, "in his kingdom,"),
        (44, 46, "to sing praises"),
        (47, 48, "unceasing"),
        (49, 51, "with the choirs"),
        (52, 53, "above,"),
        (54, 56, "unto the Father,"),
        (57, 60, "and unto the Son,"),
        (61, 65, "and unto the Holy Ghost,"),
        (66, 70, "which are Gods"),
        (71, 72, "made one,"),
        (73, 75, "in a state"),
        (76, 78, "of happiness"),
        (79, 83, "which hath no end."),
    ],
    8: [
        (0, 2, "Therefore repent,"),
        (3, 5, "and be baptized"),
        (6, 10, "in the name of Jesus,"),
        (11, 12, "and lay hold upon"),
        (13, 16, "the gospel of Christ,"),
        (17, 17, "which"),
        (18, 22, "shall be set"),
        (23, 26, "before you,"),
        (27, 29, "not only"),
        (30, 32, "in this record,"),
        (33, 37, "but also in the record"),
        (38, 38, "which"),
        (39, 43, "shall come"),
        (44, 45, "unto the Gentiles"),
        (46, 48, "from the Jews,"),
        (49, 52, "which record"),
        (53, 56, "shall come"),
        (57, 58, "from the Gentiles"),
        (59, 61, "unto you."),
    ],
    9: [
        (0, 1, "For behold,"),
        (2, 5, "this record is written"),
        (6, 8, "to the intent"),
        (9, 11, "that ye may believe"),
        (12, 13, "that;"),
        (14, 18, "and if ye believe"),
        (19, 20, "that,"),
        (21, 25, "ye will believe"),
        (26, 26, "also"),
        (27, 28, "this;"),
        (29, 33, "and if ye believe"),
        (34, 35, "this"),
        (36, 40, "ye will know"),
        (41, 42, "concerning"),
        (43, 46, "of your fathers,"),
        (47, 50, "and also the marvelous works"),
        (51, 53, "which were wrought"),
        (54, 56, "by the power"),
        (57, 59, "of God"),
        (60, 64, "among them."),
    ],
    10: [
        (0, 0, "And"),
        (1, 5, "ye will know"),
        (6, 6, "also"),
        (7, 8, "that ye are"),
        (9, 13, "a remnant"),
        (14, 18, "of the seed of Jacob;"),
        (19, 20, "therefore"),
        (21, 24, "ye are numbered"),
        (25, 28, "among the people"),
        (29, 32, "of the first covenant;"),
        (33, 36, "and if it so be"),
        (37, 41, "ye will believe"),
        (42, 43, "in Christ,"),
        (44, 45, "and are baptized,"),
        (46, 49, "first with water,"),
        (50, 53, "then afterward"),
        (54, 56, "with fire"),
        (57, 60, "and with the Holy Ghost,"),
        (61, 62, "following"),
        (63, 65, "the example"),
        (66, 69, "of our Savior,"),
        (70, 72, "according to"),
        (73, 77, "which he hath commanded"),
        (78, 79, "us,"),
        (80, 84, "it shall be well"),
        (85, 87, "with you"),
        (88, 90, "in the day"),
        (91, 93, "of judgment."),
        (94, 94, "Amen."),
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
