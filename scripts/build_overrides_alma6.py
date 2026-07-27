"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 6 — the church
at Zarahemla set in order; ordination of priests and elders; Alma departs
to preach in Gideon.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

    python3 build_overrides_alma6.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 6

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "And"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 8, "after had made an end"),
        (9, 10, "of speaking"),
        (11, 12, "Alma"),
        (13, 14, "unto the people"),
        (15, 17, "of the church,"),
        (18, 20, "which was established"),
        (21, 24, "in the city of"),
        (25, 25, "Zarahemla,"),
        (26, 28, "he ordained"),
        (29, 29, "priests"),
        (30, 31, "and elders,"),
        (32, 35, "by laying on"),
        (36, 38, "his hands,"),
        (39, 41, "according to"),
        (42, 43, "the order"),
        (44, 46, "of God,"),
        (47, 48, "to preside"),
        (49, 50, "and watch over"),
        (51, 53, "over"),
        (54, 55, "the church."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 7, "whosoever"),
        (8, 10, "did not belong"),
        (11, 13, "to the church"),
        (14, 15, "who"),
        (16, 17, "repented"),
        (18, 21, "of their sins"),
        (22, 23, "were baptized"),
        (24, 26, "unto repentance,"),
        (27, 28, "and were received"),
        (29, 31, "into the church."),
    ],
    3: [
        (0, 0, "And"),
        (1, 4, "it came to pass also, that"),
        (5, 8, "whosoever"),
        (9, 10, "did belong"),
        (11, 13, "to the church"),
        (14, 15, "that"),
        (16, 18, "did not repent"),
        (19, 22, "of their wickedness"),
        (23, 23, "and"),
        (24, 26, "did not humble"),
        (27, 29, "themselves"),
        (30, 32, "before"),
        (33, 34, "God—"),
        (35, 37, "I mean"),
        (38, 41, "those"),
        (42, 43, "who"),
        (44, 45, "were lifted up"),
        (46, 49, "in the pride of"),
        (50, 52, "their hearts—"),
        (53, 57, "the same"),
        (58, 60, "were rejected,"),
        (61, 63, "and were blotted out"),
        (64, 66, "their names,"),
        (67, 70, "that were not numbered"),
        (71, 73, "their names"),
        (74, 76, "among"),
        (77, 79, "those of the righteous."),
    ],
    4: [
        (0, 0, "And"),
        (1, 3, "thus"),
        (4, 5, "began to"),
        (6, 7, "they establish"),
        (8, 10, "the order of"),
        (11, 13, "the church"),
        (14, 17, "in the city of"),
        (18, 18, "Zarahemla."),
    ],
    5: [
        (0, 1, "Now"),
        (2, 4, "I would"),
        (5, 8, "that ye should understand"),
        (9, 12, "was liberal"),
        (13, 14, "the word"),
        (15, 17, "of God"),
        (18, 20, "unto all,"),
        (21, 24, "that none"),
        (25, 27, "were deprived"),
        (28, 30, "of the privilege"),
        (31, 34, "of assembling together"),
        (35, 37, "themselves"),
        (38, 39, "to hear"),
        (40, 42, "the word"),
        (43, 45, "of God."),
    ],
    6: [
        (0, 3, "Nevertheless"),
        (4, 5, "were commanded"),
        (6, 7, "the children of"),
        (8, 9, "God"),
        (10, 12, "that should"),
        (13, 15, "they gather together"),
        (16, 16, "oft"),
        (17, 19, "themselves,"),
        (20, 21, "and join"),
        (22, 24, "in fasting"),
        (25, 28, "and mighty prayer"),
        (29, 31, "in behalf of the welfare"),
        (32, 33, "of the souls"),
        (34, 36, "of those"),
        (37, 38, "who"),
        (39, 42, "knew not"),
        (43, 44, "God."),
    ],
    7: [
        (0, 0, "And"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 9, "when had made"),
        (10, 11, "Alma"),
        (12, 13, "these regulations"),
        (14, 19, "he departed"),
        (20, 24, "from them,"),
        (25, 25, "yea,"),
        (26, 28, "from the church"),
        (29, 31, "which was in"),
        (32, 34, "the city of"),
        (35, 35, "Zarahemla,"),
        (36, 38, "and went up"),
        (39, 40, "over"),
        (41, 46, "on the east of"),
        (47, 48, "the river"),
        (49, 50, "of Sidon,"),
        (51, 54, "into the valley of"),
        (55, 55, "Gideon,"),
        (56, 60, "there having been built"),
        (61, 62, "a city,"),
        (63, 65, "which was called"),
        (66, 69, "the city of"),
        (70, 70, "Gideon,"),
        (71, 75, "which was in the valley"),
        (76, 77, "that was called"),
        (78, 79, "Gideon,"),
        (80, 82, "being called"),
        (83, 85, "after the man"),
        (86, 87, "who"),
        (88, 89, "was slain"),
        (90, 93, "by the hand of"),
        (94, 94, "Nehor"),
        (95, 97, "with the sword."),
    ],
    8: [
        (0, 0, "And"),
        (1, 3, "went"),
        (4, 4, "Alma"),
        (5, 5, "and"),
        (6, 7, "began to"),
        (8, 9, "declare"),
        (10, 12, "the word"),
        (13, 15, "of God"),
        (16, 18, "unto the church"),
        (19, 21, "which was established"),
        (22, 25, "in the valley of"),
        (26, 26, "Gideon,"),
        (27, 29, "according to"),
        (30, 32, "the revelation of"),
        (33, 34, "the truth"),
        (35, 38, "of the word which"),
        (39, 40, "had been spoken"),
        (41, 43, "by his fathers,"),
        (44, 44, "and"),
        (45, 47, "according to"),
        (48, 49, "the spirit"),
        (50, 51, "of prophecy"),
        (52, 55, "which was in him,"),
        (56, 58, "according to"),
        (59, 60, "the testimony"),
        (61, 63, "of"),
        (64, 65, "Jesus Christ,"),
        (66, 67, "the Son"),
        (68, 70, "of God,"),
        (71, 72, "who"),
        (73, 77, "should come"),
        (78, 79, "to redeem"),
        (80, 81, "his people"),
        (82, 85, "from their sins,"),
        (86, 86, "and"),
        (87, 89, "according to"),
        (90, 92, "the holy order"),
        (93, 93, "by which"),
        (94, 99, "he was called."),
        (100, 100, "And"),
        (101, 103, "thus it is"),
        (104, 104, "written."),
        (105, 105, "Amen."),
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
