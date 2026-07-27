"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 11 — the final decline of the
Jaredite kings: prophets warn of destruction in the days of Com and his successors, but
the people reject them; wars, secret combinations, and wickedness increase through the
reigns of Shiblom, Seth, Ahah, Ethem, Moron, Coriantor, and Ether's father, until the
Lord declares that except they repent they and their land shall be utterly destroyed.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether11.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 11

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 4, "And there came also"),
        (5, 8, "in the days of Com"),
        (9, 12, "many prophets,"),
        (13, 16, "and prophesied the destruction"),
        (17, 20, "of that great people"),
        (21, 22, "except"),
        (23, 25, "they repent,"),
        (26, 28, "and turn"),
        (29, 31, "unto the Lord,"),
        (32, 33, "and leave off"),
        (34, 37, "their murders"),
        (38, 40, "and wickedness."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 5, "rejected the prophets"),
        (6, 7, "the people,"),
        (8, 12, "and they fled"),
        (13, 14, "unto Com"),
        (15, 17, "for protection,"),
        (18, 20, "for did seek"),
        (21, 21, "the people"),
        (22, 25, "to destroy them."),
    ],
    3: [
        (0, 4, "And they prophesied"),
        (5, 6, "unto Com"),
        (7, 9, "many things;"),
        (10, 14, "and he was blessed"),
        (15, 18, "all his days"),
        (19, 20, "that remained."),
    ],
    4: [
        (0, 4, "And he lived"),
        (5, 8, "to a long life,"),
        (9, 11, "and did beget"),
        (12, 12, "Shiblom;"),
        (13, 16, "and Shiblom reigned"),
        (17, 21, "in his stead."),
        (22, 24, "And did rebel"),
        (25, 28, "the brother of Shiblom"),
        (29, 31, "against him,"),
        (32, 35, "and there began"),
        (36, 37, "to be"),
        (38, 42, "an exceeding great war"),
        (43, 46, "in all the land."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 4, "caused"),
        (5, 9, "the brother of Shiblom"),
        (10, 11, "that be slain"),
        (12, 13, "all the prophets"),
        (14, 17, "who prophesied"),
        (18, 19, "concerning"),
        (20, 22, "the destruction"),
        (23, 25, "of the people;"),
    ],
    6: [
        (0, 3, "And there was"),
        (4, 6, "a great destruction"),
        (7, 10, "upon all the land,"),
        (11, 15, "for they testified"),
        (16, 18, "that there was"),
        (19, 21, "a great curse"),
        (22, 26, "shall come"),
        (27, 31, "upon the face of the earth,"),
        (32, 35, "and also upon"),
        (36, 37, "the people,"),
        (38, 43, "and there should be"),
        (44, 46, "a great destruction"),
        (47, 51, "among them,"),
        (52, 54, "such a manner"),
        (55, 59, "as never came"),
        (60, 62, "on the world,"),
        (63, 63, "and"),
        (64, 67, "should become"),
        (68, 70, "their bones"),
        (71, 73, "as it were"),
        (74, 76, "mounds of soil"),
        (77, 81, "upon the land"),
        (82, 86, "except they repent"),
        (87, 90, "of their iniquities."),
    ],
    7: [
        (0, 4, "And they hearkened not"),
        (5, 7, "unto the voice"),
        (8, 10, "of the Lord,"),
        (11, 12, "because of"),
        (13, 16, "their evil combinations;"),
        (17, 20, "wherefore"),
        (21, 23, "there began"),
        (24, 26, "to be"),
        (27, 30, "wars and strifes"),
        (31, 34, "in all the land,"),
        (35, 39, "and also many famines"),
        (40, 41, "and pestilences,"),
        (42, 46, "there came"),
        (47, 49, "a great destruction,"),
        (50, 52, "such a manner"),
        (53, 56, "as never was seen"),
        (57, 59, "in the world;"),
        (60, 64, "and all these things"),
        (65, 67, "did happen"),
        (68, 71, "in the days of Shiblom."),
    ],
    8: [
        (0, 3, "And began"),
        (4, 5, "the people to repent"),
        (6, 9, "of their iniquity;"),
        (10, 13, "and according"),
        (14, 17, "to their repentance,"),
        (18, 21, "showed tender mercy"),
        (22, 23, "the Lord"),
        (24, 27, "unto them."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 4, "was slain"),
        (5, 5, "Shiblom,"),
        (6, 8, "and was brought"),
        (9, 9, "Seth"),
        (10, 11, "into captivity,"),
        (12, 16, "and he dwelt"),
        (17, 17, "in captivity"),
        (18, 21, "all his days."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 4, "obtained"),
        (5, 6, "Ahah"),
        (7, 8, "his son,"),
        (9, 10, "the kingdom;"),
        (11, 15, "and he did reign"),
        (16, 20, "over the people"),
        (21, 24, "all his days."),
        (25, 28, "And he did commit"),
        (29, 32, "all manner of iniquity"),
        (33, 35, "in his days,"),
        (36, 39, "whereby came"),
        (40, 42, "from him"),
        (43, 46, "much shedding of blood;"),
        (47, 49, "and were few"),
        (50, 51, "his days."),
    ],
    11: [
        (0, 2, "And Ethem,"),
        (3, 5, "for he"),
        (6, 10, "was a descendant"),
        (11, 12, "of Ahah,"),
        (13, 15, "he did obtain"),
        (16, 17, "the kingdom;"),
        (18, 22, "and he also committed"),
        (23, 24, "wickedness"),
        (25, 27, "in his days."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 5, "came forth"),
        (6, 9, "in the days of Ethem,"),
        (10, 12, "many prophets,"),
        (13, 16, "and prophesied again"),
        (17, 18, "unto the people;"),
        (19, 19, "yea,"),
        (20, 23, "they did prophesy"),
        (24, 29, "should be utterly destroyed"),
        (30, 31, "they"),
        (32, 34, "by the Lord"),
        (35, 39, "from off the earth"),
        (40, 44, "except they repent"),
        (45, 49, "from their iniquities."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 6, "hardened the people"),
        (7, 9, "their hearts,"),
        (10, 14, "and would not hearken"),
        (15, 18, "unto their words;"),
        (19, 21, "and did mourn"),
        (22, 22, "the prophets"),
        (23, 25, "and withdrew"),
        (26, 30, "from among the people."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 6, "did do Ethem"),
        (7, 7, "judgment"),
        (8, 10, "in wickedness"),
        (11, 14, "all his days;"),
        (15, 18, "and he begat"),
        (19, 19, "Moron."),
        (20, 23, "And it came to pass that"),
        (24, 25, "Moron reigned"),
        (26, 30, "in his stead;"),
        (31, 35, "and Moron did"),
        (36, 38, "that which was wicked"),
        (39, 43, "before the Lord."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 7, "there arose a rebellion"),
        (8, 11, "among the people,"),
        (12, 13, "because of"),
        (14, 16, "that secret combination"),
        (17, 19, "which was established"),
        (20, 23, "to get"),
        (24, 25, "power"),
        (26, 28, "and gain;"),
        (29, 32, "and there arose"),
        (33, 36, "among them"),
        (37, 39, "a man mighty"),
        (40, 42, "in iniquity,"),
        (43, 45, "and gave battle"),
        (46, 47, "against Moron,"),
        (48, 52, "whereby he overthrew"),
        (53, 54, "the half"),
        (55, 57, "of the kingdom;"),
        (58, 61, "and he did rule"),
        (62, 63, "the half"),
        (64, 66, "of the kingdom"),
        (67, 70, "for many years."),
    ],
    16: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he was cast down"),
        (7, 8, "by Moron,"),
        (9, 13, "and he regained"),
        (14, 15, "the kingdom."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 5, "there arose"),
        (6, 9, "another mighty man;"),
        (10, 12, "and he"),
        (13, 17, "was a descendant"),
        (18, 21, "of the brother of Jared."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 5, "he overthrew"),
        (6, 6, "Moron"),
        (7, 8, "and obtained"),
        (9, 10, "the kingdom;"),
        (11, 14, "wherefore"),
        (15, 17, "dwelt"),
        (18, 19, "Moron a captive"),
        (20, 23, "all his days"),
        (24, 25, "that remained;"),
        (26, 29, "and he begat"),
        (30, 30, "Coriantor."),
    ],
    19: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Coriantor dwelt"),
        (6, 6, "in captivity"),
        (7, 10, "all his days."),
    ],
    20: [
        (0, 3, "And in his days"),
        (4, 5, "of Coriantor"),
        (6, 10, "there came also"),
        (11, 13, "many prophets,"),
        (14, 16, "and prophesied"),
        (17, 19, "of great things"),
        (20, 21, "and marvelous,"),
        (22, 24, "and cried"),
        (25, 26, "repentance"),
        (27, 28, "unto the people,"),
        (29, 31, "and except"),
        (32, 34, "they should repent"),
        (35, 38, "would execute"),
        (39, 43, "the Lord God"),
        (44, 45, "judgment"),
        (46, 47, "against"),
        (48, 51, "them"),
        (52, 56, "even unto full destruction"),
        (57, 59, "of them."),
    ],
    21: [
        (0, 0, "And"),
        (1, 5, "would send forth"),
        (6, 7, "or bring"),
        (8, 12, "the Lord God"),
        (13, 15, "another people"),
        (16, 19, "to possess the land,"),
        (20, 22, "by his power,"),
        (23, 27, "even as the way"),
        (28, 31, "whereby he brought"),
        (32, 34, "their fathers."),
    ],
    22: [
        (0, 3, "And they did reject"),
        (4, 7, "all the words of the prophets,"),
        (8, 9, "because of"),
        (10, 13, "their secret society"),
        (14, 16, "and abominations"),
        (17, 17, "wicked."),
    ],
    23: [
        (0, 3, "And it came to pass that"),
        (4, 5, "was begotten Ether"),
        (6, 7, "of Coriantor,"),
        (8, 12, "and he died,"),
        (13, 16, "having dwelt in captivity"),
        (17, 20, "all his days."),
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
