"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 24 — Jesus commands the
Nephites to write the words the Father had given to Malachi and quotes Malachi 3: the
messenger of the covenant coming suddenly to his temple, the Lord as a refiner and
purifier of silver; the call to return to the Lord and to bring the tithes into the
storehouse that the windows of heaven be opened; and the book of remembrance written
for those that feared the Lord, who shall be his jewels in the day when he maketh up
his treasure.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split applied to bom_books.json before glossing:
    24:1  Malaki—Faauta,  ->  Malaki—  +  Faauta,

    python3 build_overrides_3nephi24.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 24

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he commanded"),
        (7, 10, "them"),
        (11, 15, "that they should write"),
        (16, 17, "the words"),
        (18, 20, "which were given"),
        (21, 23, "by the Father"),
        (24, 25, "unto Malachi,"),
        (26, 32, "which he should tell"),
        (33, 35, "unto them."),
        (36, 39, "And it came to pass that"),
        (40, 43, "after were written"),
        (44, 46, "these words"),
        (47, 49, "he expounded"),
        (50, 52, "them."),
        (53, 56, "And these are the words"),
        (57, 60, "which he did tell"),
        (61, 64, "unto them,"),
        (65, 66, "saying:"),
        (67, 71, "Thus said"),
        (72, 74, "the Father"),
        (75, 76, "unto Malachi—"),
        (77, 77, "Behold,"),
        (78, 83, "I will send"),
        (84, 85, "my messenger,"),
        (86, 92, "and he shall prepare"),
        (93, 94, "the way"),
        (95, 97, "before me,"),
        (98, 105, "and shall suddenly come"),
        (106, 108, "to his temple"),
        (109, 110, "the Lord,"),
        (111, 112, "whom"),
        (113, 115, "ye seek,"),
        (116, 118, "even the messenger"),
        (119, 121, "of the covenant,"),
        (122, 123, "whom"),
        (124, 128, "ye delight in;"),
        (129, 129, "behold,"),
        (130, 136, "he shall come,"),
        (137, 140, "saith"),
        (141, 142, "the Lord"),
        (143, 144, "of Hosts."),
    ],
    2: [
        (0, 3, "But who is he"),
        (4, 7, "that may abide"),
        (8, 9, "the day"),
        (10, 13, "of his coming,"),
        (14, 17, "and who is he"),
        (18, 19, "that shall stand"),
        (20, 25, "when he appeareth?"),
        (26, 26, "for"),
        (27, 30, "he is like"),
        (31, 33, "a fire"),
        (34, 37, "of the refiner,"),
        (38, 41, "and like"),
        (42, 43, "the soap"),
        (44, 46, "of the fuller."),
    ],
    3: [
        (0, 6, "And he shall sit"),
        (7, 10, "as a"),
        (11, 12, "refiner"),
        (13, 15, "and a purifier"),
        (16, 16, "of silver,"),
        (17, 22, "and he shall purify"),
        (23, 25, "the sons of Levi,"),
        (26, 27, "and purge"),
        (28, 29, "them"),
        (30, 32, "as"),
        (33, 34, "gold"),
        (35, 37, "and silver,"),
        (38, 44, "that they may offer"),
        (45, 47, "unto the Lord"),
        (48, 49, "an offering"),
        (50, 52, "in righteousness."),
    ],
    4: [
        (0, 3, "Then shall be pleasant"),
        (4, 6, "the offering"),
        (7, 8, "of Judah"),
        (9, 10, "and Jerusalem"),
        (11, 13, "unto the Lord,"),
        (14, 16, "as in"),
        (17, 18, "the days of old,"),
        (19, 22, "and as in"),
        (23, 25, "years that are past."),
    ],
    5: [
        (0, 6, "And I will come near"),
        (7, 9, "to you"),
        (10, 12, "to judgment;"),
        (13, 18, "and I will become"),
        (19, 21, "a swift witness"),
        (22, 24, "against"),
        (25, 25, "the sorcerers,"),
        (26, 28, "and against"),
        (29, 31, "the adulterers,"),
        (32, 34, "and against"),
        (35, 38, "false swearers,"),
        (39, 40, "and against"),
        (41, 45, "those"),
        (46, 47, "that oppress"),
        (48, 52, "the hireling"),
        (53, 55, "in his wages,"),
        (56, 62, "the widow,"),
        (63, 66, "and the fatherless,"),
        (67, 71, "and those"),
        (72, 75, "that turn aside"),
        (76, 78, "the stranger,"),
        (79, 83, "and fear not"),
        (84, 86, "me,"),
        (87, 90, "saith"),
        (91, 92, "the Lord"),
        (93, 94, "of Hosts."),
    ],
    6: [
        (0, 0, "For"),
        (1, 3, "I am"),
        (4, 5, "the Lord,"),
        (6, 10, "I change not;"),
        (11, 12, "therefore"),
        (13, 16, "are not consumed"),
        (17, 17, "ye"),
        (18, 18, "sons"),
        (19, 20, "of Jacob."),
    ],
    7: [
        (0, 2, "Even from"),
        (3, 3, "the days"),
        (4, 7, "of your fathers"),
        (8, 11, "ye are gone away"),
        (12, 14, "from mine ordinances,"),
        (15, 18, "and ye have not kept"),
        (19, 20, "them."),
        (21, 22, "Return"),
        (23, 25, "unto me,"),
        (26, 31, "and I will return"),
        (32, 34, "unto you,"),
        (35, 38, "saith"),
        (39, 40, "the Lord"),
        (41, 42, "of Hosts."),
        (43, 47, "But ye said:"),
        (48, 49, "Wherein"),
        (50, 53, "shall we return?"),
    ],
    8: [
        (0, 2, "Will rob"),
        (3, 5, "a man"),
        (6, 9, "God?"),
        (10, 12, "Yet ye,"),
        (13, 16, "have robbed"),
        (17, 19, "me."),
        (20, 24, "But ye say:"),
        (25, 26, "Wherein"),
        (27, 30, "have we robbed"),
        (31, 33, "thee?"),
        (34, 35, "In tithes"),
        (36, 37, "and offerings."),
    ],
    9: [
        (0, 2, "Ye are cursed"),
        (3, 5, "with a curse,"),
        (6, 9, "even"),
        (10, 12, "this whole nation,"),
        (13, 13, "for"),
        (14, 17, "ye have robbed"),
        (18, 20, "me."),
    ],
    10: [
        (0, 2, "Bring ye"),
        (3, 5, "all the tithes"),
        (6, 8, "into the storehouse,"),
        (9, 12, "that there may be"),
        (13, 14, "meat"),
        (15, 17, "in mine house;"),
        (18, 23, "and prove ye now"),
        (24, 26, "me"),
        (27, 29, "herewith,"),
        (30, 33, "saith"),
        (34, 35, "the Lord"),
        (36, 37, "of Hosts,"),
        (38, 44, "if I will not open"),
        (45, 47, "for you"),
        (48, 48, "the windows"),
        (49, 51, "of heaven,"),
        (52, 54, "and pour out"),
        (55, 57, "for you"),
        (58, 59, "a blessing,"),
        (60, 64, "that shall not be enough"),
        (65, 66, "room"),
        (67, 69, "to receive it."),
    ],
    11: [
        (0, 5, "And I will rebuke"),
        (6, 10, "the destroyer"),
        (11, 12, "for the sake of"),
        (13, 13, "you,"),
        (14, 20, "and he shall not destroy"),
        (21, 21, "the fruits"),
        (22, 25, "of your ground;"),
        (26, 31, "neither shall cast"),
        (32, 33, "the fruit"),
        (34, 37, "of your vine"),
        (38, 39, "in the field"),
        (40, 45, "before the time,"),
        (46, 49, "saith"),
        (50, 51, "the Lord"),
        (52, 53, "of Hosts."),
    ],
    12: [
        (0, 4, "And shall call blessed"),
        (5, 7, "you"),
        (8, 9, "all nations,"),
        (10, 10, "for"),
        (11, 15, "ye shall become"),
        (16, 18, "a delightsome land,"),
        (19, 22, "saith"),
        (23, 24, "the Lord"),
        (25, 26, "of Hosts."),
    ],
    13: [
        (0, 1, "Have been stout"),
        (2, 4, "your words"),
        (5, 7, "against me,"),
        (8, 11, "saith"),
        (12, 13, "the Lord."),
        (14, 18, "Yet ye say:"),
        (19, 21, "What words"),
        (22, 25, "have we spoken"),
        (26, 27, "against"),
        (28, 30, "thee?"),
    ],
    14: [
        (0, 3, "Ye have said:"),
        (4, 6, "It is vain"),
        (7, 9, "to serve"),
        (10, 12, "God,"),
        (13, 18, "and what profit is it"),
        (19, 22, "that we have kept"),
        (23, 24, "his ordinances,"),
        (25, 30, "and that we have walked mournfully"),
        (31, 33, "before"),
        (34, 35, "the Lord"),
        (36, 37, "of Hosts?"),
    ],
    15: [
        (0, 2, "And now"),
        (3, 6, "we call happy"),
        (7, 9, "the proud;"),
        (10, 10, "yea,"),
        (11, 14, "they that do"),
        (15, 18, "the works of wickedness"),
        (19, 20, "are set up;"),
        (21, 21, "yea,"),
        (22, 27, "even they"),
        (28, 33, "that tempt God"),
        (34, 35, "are even delivered."),
    ],
    16: [
        (0, 3, "Then spake often"),
        (4, 8, "they"),
        (9, 13, "that feared the Lord"),
        (14, 19, "one to another,"),
        (20, 23, "and hearkened"),
        (24, 25, "the Lord"),
        (26, 29, "and heard it;"),
        (30, 32, "and was written"),
        (33, 35, "a book of remembrance"),
        (36, 38, "before him"),
        (39, 43, "for them"),
        (44, 48, "that feared the Lord,"),
        (49, 50, "and they"),
        (51, 52, "that thought"),
        (53, 55, "upon his name."),
    ],
    17: [
        (0, 6, "And they shall become"),
        (7, 7, "mine,"),
        (8, 11, "saith"),
        (12, 13, "the Lord"),
        (14, 15, "of Hosts,"),
        (16, 18, "in that day"),
        (19, 22, "when I make up"),
        (23, 25, "my jewels;"),
        (26, 31, "and I will spare"),
        (32, 33, "them"),
        (34, 37, "as spareth"),
        (38, 40, "a man"),
        (41, 43, "his own son"),
        (44, 47, "that serveth"),
        (48, 50, "him."),
    ],
    18: [
        (0, 4, "Then shall ye return,"),
        (5, 6, "and discern"),
        (7, 8, "the difference"),
        (9, 11, "of the righteous"),
        (12, 14, "and the wicked,"),
        (15, 18, "between"),
        (19, 21, "him that serveth"),
        (22, 24, "God"),
        (25, 26, "and him"),
        (27, 32, "that serveth not"),
        (33, 35, "him."),
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
