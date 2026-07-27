"""
Hand-curated TAM-phrase gloss overrides for Helamana (Helaman) 12 — Mormon's
editorial lament on the unsteadiness and ingratitude of the children of men:
how the Lord blesses and prospers his people, yet in their ease they harden
their hearts and forget him, so that he must chasten them to be remembered; a
meditation on the nothingness of man, the absolute power of God over earth,
mountains, and sea by his word, and the final destinies of the righteous unto
eternal life and the wicked unto everlasting damnation.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits applied to bom_books.json before glossing (12 tokens across
verses 2, 13, 14, 16, 17, 18, 19, 20, 21; v13 was a triple `lalolagi—Gaoioi—e`).

    python3 build_overrides_helaman12.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "helaman"
CHAPTER_NUM = 12

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And thus"),
        (4, 7, "we may see"),
        (8, 10, "the foolishness,"),
        (11, 16, "and also the unsteadiness of"),
        (17, 18, "the hearts of"),
        (19, 22, "the children of men;"),
        (23, 23, "yea,"),
        (24, 28, "we may see"),
        (29, 32, "doth bless and prosper"),
        (33, 35, "the Lord,"),
        (36, 39, "in his supreme goodness"),
        (40, 42, "unending,"),
        (43, 46, "those who"),
        (47, 49, "do put"),
        (50, 52, "their trust"),
        (53, 55, "in him."),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 6, "and we may see"),
        (7, 10, "at the very time"),
        (11, 15, "when he blesses"),
        (16, 17, "his people,"),
        (18, 18, "yea,"),
        (19, 24, "in the great yield of"),
        (25, 27, "their fields,"),
        (28, 31, "their flocks"),
        (32, 35, "and their herds,"),
        (36, 38, "and in gold,"),
        (39, 40, "and silver,"),
        (41, 46, "and all manner of precious things"),
        (47, 51, "of every kind and craft;"),
        (52, 55, "in the sparing of"),
        (56, 58, "their lives,"),
        (59, 62, "and delivering them"),
        (63, 65, "from the hands of"),
        (66, 68, "their enemies;"),
        (69, 72, "in the softening of"),
        (73, 74, "the hearts of"),
        (75, 77, "their enemies"),
        (78, 83, "that they raise no war"),
        (84, 85, "against"),
        (86, 89, "them;"),
        (90, 90, "yea,"),
        (91, 94, "and in summary,"),
        (95, 100, "in the doing of all things"),
        (101, 103, "for the welfare"),
        (104, 107, "and happiness of"),
        (108, 109, "his people;"),
        (110, 110, "yea,"),
        (111, 114, "that is the time"),
        (115, 118, "when they harden"),
        (119, 121, "their hearts,"),
        (122, 127, "and forgotten by them"),
        (128, 132, "the Lord their God,"),
        (133, 136, "and trample"),
        (137, 140, "under their feet"),
        (141, 144, "the Holy One—"),
        (145, 145, "yea,"),
        (146, 149, "and the cause is"),
        (150, 151, "because of"),
        (152, 155, "their ease,"),
        (156, 160, "and their exceeding prosperity."),
    ],
    3: [
        (0, 6, "And thus we see"),
        (7, 7, "that except"),
        (8, 12, "the Lord chastens"),
        (13, 14, "his people"),
        (15, 18, "with many afflictions,"),
        (19, 19, "yea,"),
        (20, 21, "except"),
        (22, 26, "he visits"),
        (27, 30, "them"),
        (31, 33, "with death"),
        (34, 36, "and with terror,"),
        (37, 39, "and with famine"),
        (40, 44, "and all manner of pestilence,"),
        (45, 50, "they will not remember him."),
    ],
    4: [
        (0, 0, "O,"),
        (1, 5, "how exceedingly foolish,"),
        (6, 10, "and how vain,"),
        (11, 15, "and how evil,"),
        (16, 18, "and devilish,"),
        (19, 23, "are the children of men,"),
        (24, 28, "and how quick"),
        (29, 31, "for them to do"),
        (32, 34, "iniquity,"),
        (35, 37, "and how slow"),
        (38, 40, "for them to do"),
        (41, 43, "good;"),
        (44, 44, "yea,"),
        (45, 49, "how quick"),
        (50, 51, "to hearken"),
        (52, 54, "unto the words of"),
        (55, 57, "the evil one,"),
        (58, 60, "and to set"),
        (61, 63, "their hearts"),
        (64, 68, "upon the vain things of"),
        (69, 70, "the world!"),
    ],
    5: [
        (0, 0, "Yea,"),
        (1, 5, "how quick"),
        (6, 7, "to be puffed up"),
        (8, 10, "in pride;"),
        (11, 11, "yea,"),
        (12, 16, "how quick"),
        (17, 18, "to boast,"),
        (19, 24, "and do all manner of things"),
        (25, 26, "which are iniquity;"),
        (27, 32, "and how slow"),
        (33, 36, "are they"),
        (37, 38, "to remember"),
        (39, 44, "the Lord their God,"),
        (45, 47, "and to incline"),
        (48, 50, "their ears"),
        (51, 53, "unto his counsels,"),
        (54, 54, "yea,"),
        (55, 59, "how slow"),
        (60, 62, "for them to walk"),
        (63, 67, "in the paths of wisdom!"),
    ],
    6: [
        (0, 0, "Behold,"),
        (1, 4, "they desire not"),
        (5, 10, "the Lord their God,"),
        (11, 14, "who made"),
        (15, 16, "them,"),
        (17, 20, "to rule and reign"),
        (21, 23, "over them;"),
        (24, 27, "notwithstanding"),
        (28, 30, "his great goodness"),
        (31, 34, "and his mercy"),
        (35, 38, "towards them,"),
        (39, 42, "they set at naught"),
        (43, 44, "his counsels,"),
        (45, 49, "and they desire not"),
        (50, 54, "that he be"),
        (55, 57, "their guide."),
    ],
    7: [
        (0, 0, "O,"),
        (1, 4, "how exceedingly great"),
        (5, 7, "the nothingness of"),
        (8, 11, "the children of men;"),
        (12, 12, "yea,"),
        (13, 16, "even"),
        (17, 21, "the dust of the earth"),
        (22, 26, "they are lower than."),
    ],
    8: [
        (0, 1, "For behold,"),
        (2, 5, "the dust of"),
        (6, 7, "the earth"),
        (8, 9, "moves about"),
        (10, 13, "hither and thither,"),
        (14, 17, "and is divided"),
        (18, 21, "into small parts,"),
        (22, 25, "at the command of"),
        (26, 29, "our supreme God"),
        (30, 33, "and enduring forever."),
    ],
    9: [
        (0, 0, "Yea,"),
        (1, 1, "behold,"),
        (2, 4, "at his voice"),
        (5, 9, "tremble and shake"),
        (10, 12, "the hills and mountains."),
    ],
    10: [
        (0, 4, "And by the power of"),
        (5, 6, "his voice"),
        (7, 11, "they are shattered,"),
        (12, 17, "and become smooth,"),
        (18, 18, "yea,"),
        (19, 24, "even like unto a valley."),
    ],
    11: [
        (0, 0, "Yea,"),
        (1, 3, "by"),
        (4, 6, "the power of"),
        (7, 8, "his voice"),
        (9, 11, "shakes"),
        (12, 14, "the whole earth;"),
    ],
    12: [
        (0, 0, "Yea,"),
        (1, 4, "by the power of"),
        (5, 6, "his voice,"),
        (7, 9, "shake"),
        (10, 10, "the foundations,"),
        (11, 14, "even to"),
        (15, 16, "the very center."),
    ],
    13: [
        (0, 0, "Yea,"),
        (1, 7, "and if he say"),
        (8, 10, "unto the earth—"),
        (11, 11, "Move—"),
        (12, 14, "it moves indeed."),
    ],
    14: [
        (0, 0, "Yea,"),
        (1, 6, "if he say"),
        (7, 9, "unto the earth—"),
        (10, 15, "Thou go back,"),
        (16, 19, "that lengthen"),
        (20, 21, "the day"),
        (22, 26, "for many hours—"),
        (27, 29, "it is done indeed;"),
    ],
    15: [
        (0, 3, "And thus,"),
        (4, 8, "goes back"),
        (9, 10, "the earth,"),
        (11, 13, "according to"),
        (14, 15, "his word,"),
        (16, 18, "and it appears"),
        (19, 21, "unto man"),
        (22, 28, "stands in one place"),
        (29, 30, "the sun;"),
        (31, 31, "yea,"),
        (32, 33, "and behold,"),
        (34, 36, "this is so;"),
        (37, 37, "for"),
        (38, 39, "surely"),
        (40, 44, "it is the earth that moves"),
        (45, 49, "and not the sun."),
    ],
    16: [
        (0, 1, "And behold,"),
        (2, 8, "if he also say"),
        (9, 11, "unto the waters of"),
        (12, 14, "the great deep—"),
        (15, 17, "Be thou dried up,"),
        (18, 20, "it is done indeed."),
    ],
    17: [
        (0, 0, "Behold,"),
        (1, 6, "if he say"),
        (7, 9, "unto this mountain—"),
        (10, 15, "Be thou lifted up,"),
        (16, 18, "and come over"),
        (19, 21, "and fall down"),
        (22, 26, "upon that city,"),
        (27, 30, "that it be buried—"),
        (31, 31, "behold"),
        (32, 34, "it is done indeed."),
    ],
    18: [
        (0, 1, "And behold,"),
        (2, 7, "if a man hide"),
        (8, 9, "a treasure"),
        (10, 12, "in the earth,"),
        (13, 18, "and shall say"),
        (19, 20, "the Lord—"),
        (21, 22, "Be cursed"),
        (23, 24, "that treasure,"),
        (25, 26, "because of"),
        (27, 29, "the iniquity of"),
        (30, 33, "him who hid it—"),
        (34, 34, "behold,"),
        (35, 39, "it shall be cursed indeed."),
    ],
    19: [
        (0, 4, "And if shall say"),
        (5, 6, "the Lord—"),
        (7, 9, "Be thou cursed,"),
        (10, 14, "that thou be not found"),
        (15, 17, "by any man"),
        (18, 22, "from this time"),
        (23, 27, "unto forever—"),
        (28, 28, "behold,"),
        (29, 32, "no man"),
        (33, 35, "shall obtain"),
        (36, 37, "that treasure"),
        (38, 40, "from that time"),
        (41, 45, "unto forever."),
    ],
    20: [
        (0, 1, "And behold,"),
        (2, 5, "if shall say"),
        (6, 7, "the Lord"),
        (8, 10, "unto a man—"),
        (11, 12, "Because of"),
        (13, 14, "thine iniquities,"),
        (15, 19, "thou shalt be cursed"),
        (20, 21, "forever—"),
        (22, 26, "it shall be done indeed."),
    ],
    21: [
        (0, 4, "And if shall say"),
        (5, 6, "the Lord—"),
        (7, 8, "Because of"),
        (9, 10, "thine iniquities"),
        (11, 17, "thou shalt be cut off"),
        (18, 20, "from my presence—"),
        (21, 25, "he will make"),
        (26, 29, "that it come to pass indeed."),
    ],
    22: [
        (0, 2, "And wo"),
        (3, 5, "unto him"),
        (6, 7, "to whom"),
        (8, 15, "he shall say"),
        (16, 17, "this thing,"),
        (18, 18, "for"),
        (19, 23, "it shall come"),
        (24, 26, "unto him"),
        (27, 32, "who will do iniquity,"),
        (33, 39, "and he cannot"),
        (40, 42, "be saved;"),
        (43, 44, "therefore,"),
        (45, 46, "because of"),
        (47, 48, "this reason,"),
        (49, 53, "that might be saved"),
        (54, 55, "men,"),
        (56, 59, "hath been declared"),
        (60, 61, "repentance."),
    ],
    23: [
        (0, 1, "Therefore,"),
        (2, 5, "blessed are they"),
        (6, 11, "who will repent"),
        (12, 13, "and hearken"),
        (14, 17, "unto the voice of"),
        (18, 22, "the Lord their God;"),
        (23, 27, "for these"),
        (28, 31, "shall be saved."),
    ],
    24: [
        (0, 3, "And may grant"),
        (4, 6, "God,"),
        (7, 10, "in his supreme fulness,"),
        (11, 15, "that might be brought"),
        (16, 17, "men"),
        (18, 20, "unto repentance"),
        (21, 23, "and good works,"),
        (24, 28, "that might be restored"),
        (29, 31, "unto them"),
        (32, 34, "grace"),
        (35, 38, "for grace,"),
        (39, 41, "according to"),
        (42, 44, "their works."),
    ],
    25: [
        (0, 3, "And I desire"),
        (4, 5, "that be saved"),
        (6, 7, "all men."),
        (8, 8, "But"),
        (9, 13, "we read that"),
        (14, 17, "in the great day"),
        (18, 20, "and the last,"),
        (21, 25, "there are some"),
        (26, 31, "who shall be cast out,"),
        (32, 32, "yea,"),
        (33, 38, "who shall be cut off"),
        (39, 42, "from the presence of"),
        (43, 44, "the Lord;"),
    ],
    26: [
        (0, 0, "Yea,"),
        (1, 6, "who shall be placed"),
        (7, 10, "in a state of"),
        (11, 15, "endless misery,"),
        (16, 18, "fulfilling"),
        (19, 22, "the words which say:"),
        (23, 27, "They"),
        (28, 31, "who did good,"),
        (32, 36, "shall obtain"),
        (37, 41, "life enduring forever;"),
        (42, 47, "and they"),
        (48, 51, "who did evil"),
        (52, 56, "shall obtain"),
        (57, 61, "damnation enduring forever."),
        (62, 65, "And thus it is."),
        (66, 66, "Amen."),
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
