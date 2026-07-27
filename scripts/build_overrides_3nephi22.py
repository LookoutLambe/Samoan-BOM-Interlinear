"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 22 — Jesus quotes
Isaiah 54 to the Nephites: the song of the barren woman (covenant Zion) who shall
break forth on the right hand and the left, her seed inheriting the Gentiles; the
Lord as her Maker and Redeemer gathers her with everlasting kindness, swearing as in
the days of Noah that his covenant of peace shall not be removed; the building of
Zion with fair colours and precious stones, her children taught of the Lord, and the
promise that no weapon formed against her shall prosper — the heritage of the
servants of the Lord.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

    python3 build_overrides_3nephi22.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 22

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 4, "And then shall come to pass"),
        (5, 7, "that which"),
        (8, 9, "is written:"),
        (10, 12, "Sing,"),
        (13, 13, "O thou"),
        (14, 15, "barren,"),
        (16, 16, "thou"),
        (17, 20, "that didst not bear;"),
        (21, 23, "break forth"),
        (24, 25, "into singing,"),
        (26, 29, "and cry aloud,"),
        (30, 30, "thou"),
        (31, 33, "that didst not travail"),
        (34, 36, "with child;"),
        (37, 37, "for"),
        (38, 41, "more are"),
        (42, 44, "the children"),
        (45, 48, "of the desolate"),
        (49, 50, "than"),
        (51, 52, "the children"),
        (53, 56, "of the married wife,"),
        (57, 60, "saith"),
        (61, 62, "the Lord."),
    ],
    2: [
        (0, 1, "Enlarge"),
        (2, 3, "the place"),
        (4, 6, "of thy tent,"),
        (7, 10, "and let"),
        (11, 14, "them"),
        (15, 17, "stretch forth"),
        (18, 18, "the curtains"),
        (19, 21, "of thine habitations;"),
        (22, 24, "spare not,"),
        (25, 26, "lengthen"),
        (27, 28, "thy cords,"),
        (29, 30, "and strengthen"),
        (31, 32, "thy stakes;"),
    ],
    3: [
        (0, 0, "For"),
        (1, 6, "thou shalt break forth"),
        (7, 10, "on the right hand"),
        (11, 14, "and on the left,"),
        (15, 21, "and shall take for inheritance"),
        (22, 24, "thy seed"),
        (25, 25, "the Gentiles,"),
        (26, 28, "and they make"),
        (29, 30, "the desolate cities"),
        (31, 32, "to be inhabited."),
    ],
    4: [
        (0, 3, "Fear not,"),
        (4, 4, "for"),
        (5, 10, "thou shalt not be ashamed;"),
        (11, 12, "neither be confounded"),
        (13, 13, "thou,"),
        (14, 14, "for"),
        (15, 19, "thou shalt not be put to shame"),
        (20, 20, "thee;"),
        (21, 21, "for"),
        (22, 28, "thou shalt forget"),
        (29, 30, "the shame"),
        (31, 33, "of thy youth,"),
        (34, 41, "and shalt no more remember"),
        (42, 43, "the reproach"),
        (44, 46, "of thy youth,"),
        (47, 54, "and shalt no more remember"),
        (55, 56, "the reproach"),
        (57, 59, "of thy state"),
        (60, 65, "of a widow."),
    ],
    5: [
        (0, 0, "For"),
        (1, 5, "he that made thee,"),
        (6, 8, "thy husband,"),
        (9, 11, "the Lord"),
        (12, 13, "of Hosts,"),
        (14, 17, "is his name;"),
        (18, 21, "and thy Redeemer,"),
        (22, 26, "the Holy One"),
        (27, 28, "of Israel—"),
        (29, 32, "shall he be called"),
        (33, 35, "the God"),
        (36, 39, "of the whole earth."),
    ],
    6: [
        (0, 0, "For"),
        (1, 3, "hath called thee"),
        (4, 6, "the Lord"),
        (7, 9, "as a woman"),
        (10, 11, "forsaken"),
        (12, 14, "and grieved"),
        (15, 17, "in spirit,"),
        (18, 21, "and a wife"),
        (22, 24, "of youth,"),
        (25, 28, "when was refused"),
        (29, 29, "thou,"),
        (30, 33, "saith"),
        (34, 35, "thy God."),
    ],
    7: [
        (0, 2, "I forsook"),
        (3, 3, "thee"),
        (4, 7, "for a small moment,"),
        (8, 14, "but I will gather"),
        (15, 15, "thee"),
        (16, 20, "with great mercies."),
    ],
    8: [
        (0, 3, "In a little wrath"),
        (4, 6, "I hid"),
        (7, 8, "my face"),
        (9, 9, "from"),
        (10, 12, "thee"),
        (13, 15, "for a moment,"),
        (16, 18, "but with"),
        (19, 21, "the kindness everlasting"),
        (22, 23, "for ever"),
        (24, 29, "will I have mercy"),
        (30, 32, "on thee,"),
        (33, 36, "saith"),
        (37, 38, "the Lord,"),
        (39, 40, "thy Redeemer."),
    ],
    9: [
        (0, 1, "For"),
        (2, 3, "this cause,"),
        (4, 6, "it is as"),
        (7, 10, "the waters of Noah"),
        (11, 13, "unto me,"),
        (14, 14, "for"),
        (15, 19, "as I have sworn"),
        (20, 23, "that should no more overflow"),
        (24, 25, "the earth"),
        (26, 28, "with the waters"),
        (29, 30, "of Noah,"),
        (31, 36, "so have I sworn"),
        (37, 43, "that I will no more be wroth"),
        (44, 46, "with thee."),
    ],
    10: [
        (0, 0, "For"),
        (1, 5, "shall depart"),
        (6, 6, "the mountains"),
        (7, 9, "and be removed"),
        (10, 10, "the hills,"),
        (11, 18, "but shall not depart"),
        (19, 20, "my kindness"),
        (21, 21, "from"),
        (22, 24, "thee,"),
        (25, 30, "neither shall be removed"),
        (31, 32, "the covenant"),
        (33, 35, "of my peace,"),
        (36, 39, "saith"),
        (40, 41, "the Lord"),
        (42, 46, "that hath mercy"),
        (47, 49, "on thee."),
    ],
    11: [
        (0, 0, "O,"),
        (1, 2, "thou"),
        (3, 4, "afflicted,"),
        (5, 6, "tossed"),
        (7, 8, "with tempest,"),
        (9, 12, "and not comforted!"),
        (13, 13, "behold,"),
        (14, 18, "I will lay"),
        (19, 20, "thy stones"),
        (21, 23, "with fair colours,"),
        (24, 25, "and lay"),
        (26, 27, "thy foundations"),
        (28, 29, "with sapphires."),
    ],
    12: [
        (0, 5, "And I will make"),
        (6, 7, "thy windows"),
        (8, 10, "of agates,"),
        (11, 13, "and thy gates"),
        (14, 16, "of carbuncles,"),
        (17, 20, "and all thy borders"),
        (21, 23, "of pleasant stones."),
    ],
    13: [
        (0, 4, "And shall be taught"),
        (5, 7, "all thy children"),
        (8, 10, "of the Lord;"),
        (11, 16, "and great shall be"),
        (17, 18, "the peace"),
        (19, 21, "of thy children."),
    ],
    14: [
        (0, 2, "In righteousness"),
        (3, 7, "shalt be established"),
        (8, 8, "thou;"),
        (9, 11, "thou shalt be far"),
        (12, 13, "from oppression"),
        (14, 19, "and thou shalt not fear,"),
        (20, 21, "and from"),
        (22, 23, "terror"),
        (24, 24, "for"),
        (25, 32, "it shall not come near"),
        (33, 35, "thee."),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 7, "they shall surely gather together"),
        (8, 10, "against"),
        (11, 13, "thee,"),
        (14, 18, "but not by me;"),
        (19, 21, "whosoever"),
        (22, 24, "shall gather together"),
        (25, 26, "against"),
        (27, 29, "thee"),
        (30, 34, "shall fall"),
        (35, 36, "for the sake of"),
        (37, 37, "thee."),
    ],
    16: [
        (0, 0, "Behold,"),
        (1, 3, "I have created"),
        (4, 6, "the smith"),
        (7, 8, "that bloweth"),
        (9, 9, "the coals"),
        (10, 12, "in the fire,"),
        (13, 17, "and that bringeth forth"),
        (18, 19, "an instrument"),
        (20, 22, "for his work;"),
        (23, 26, "and I have created"),
        (27, 29, "the waster"),
        (30, 31, "to destroy."),
    ],
    17: [
        (0, 3, "No weapon"),
        (4, 5, "that is formed"),
        (6, 7, "against"),
        (8, 10, "thee"),
        (11, 12, "shall prosper;"),
        (13, 17, "and every tongue"),
        (18, 19, "that shall revile"),
        (20, 20, "against"),
        (21, 23, "thee"),
        (24, 26, "in judgment"),
        (27, 29, "thou shalt condemn."),
        (30, 33, "This is the heritage"),
        (34, 35, "of the servants"),
        (36, 38, "of the Lord,"),
        (39, 43, "and their righteousness"),
        (44, 45, "is of"),
        (46, 48, "me,"),
        (49, 52, "saith"),
        (53, 54, "the Lord."),
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
