"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 9 — out of the
darkness the voice of Christ is heard by all the people, declaring the cities he
has destroyed and why, calling the more righteous survivors to repent and return;
he proclaims himself Jesus Christ, the Son of God, creator of heaven and earth,
the light and life of the world, testifying that he came unto his own and was
rejected, that the law of Moses is fulfilled in him, and inviting all to come
unto him with a broken heart and contrite spirit to be baptized and saved.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi9.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 9

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass"),
        (4, 6, "a voice was heard"),
        (7, 11, "among all those"),
        (12, 16, "who dwelt in the world,"),
        (17, 22, "upon all this land,"),
        (23, 25, "crying:"),
    ],
    2: [
        (0, 1, "Wo,"),
        (2, 3, "wo,"),
        (4, 5, "wo"),
        (6, 8, "unto this people;"),
        (9, 10, "wo"),
        (11, 17, "unto all the people of the whole earth"),
        (18, 19, "except"),
        (20, 22, "they repent;"),
        (23, 23, "for"),
        (24, 27, "the devil laughs,"),
        (28, 31, "and his angels rejoice,"),
        (32, 33, "because of"),
        (34, 36, "the slaying of"),
        (37, 40, "the fair sons and daughters"),
        (41, 43, "of my people;"),
        (44, 48, "and it is their iniquity"),
        (49, 53, "and their abominations"),
        (54, 57, "for which they fell!"),
    ],
    3: [
        (0, 0, "Behold,"),
        (1, 6, "that great city of Zarahemla"),
        (7, 9, "I have burned"),
        (10, 12, "with fire,"),
        (13, 16, "together with its inhabitants."),
    ],
    4: [
        (0, 1, "And behold,"),
        (2, 7, "that great city of Moroni"),
        (8, 13, "I have caused to sink"),
        (14, 19, "into the depths of the sea,"),
        (20, 24, "and its inhabitants were drowned."),
    ],
    5: [
        (0, 1, "And behold,"),
        (2, 7, "that great city of Moronihah"),
        (8, 10, "I have covered"),
        (11, 12, "with earth,"),
        (13, 16, "likewise with its inhabitants,"),
        (17, 19, "to hide"),
        (20, 22, "their iniquities"),
        (23, 27, "and their abominations"),
        (28, 32, "from before my face,"),
        (33, 41, "that no more come unto me"),
        (42, 44, "the blood of the prophets"),
        (45, 48, "and the saints"),
        (49, 54, "against them."),
    ],
    6: [
        (0, 1, "And behold,"),
        (2, 6, "the city of Gilgal"),
        (7, 12, "I have caused to sink,"),
        (13, 16, "and that be buried"),
        (17, 18, "its inhabitants"),
        (19, 24, "in the depths of the earth;"),
    ],
    7: [
        (0, 0, "Yea,"),
        (1, 6, "and the city of Onihah"),
        (7, 9, "and its inhabitants;"),
        (10, 14, "and the city of Mocum"),
        (15, 17, "and its inhabitants;"),
        (18, 22, "and the city of Jerusalem"),
        (23, 25, "and its inhabitants;"),
        (26, 32, "and I have caused to come up"),
        (33, 33, "waters"),
        (34, 36, "in their place,"),
        (37, 39, "to hide"),
        (40, 42, "their wickedness"),
        (43, 47, "and their abominations"),
        (48, 52, "from before my face,"),
        (53, 61, "that no more come unto me"),
        (62, 64, "the blood of the prophets"),
        (65, 68, "and the saints"),
        (69, 74, "against them."),
    ],
    8: [
        (0, 1, "And behold,"),
        (2, 6, "the city of Gadiandi,"),
        (7, 11, "and the city of Gadiomnah,"),
        (12, 16, "and the city of Jacob,"),
        (17, 21, "and the city of Gimgimno,"),
        (22, 25, "all those cities"),
        (26, 30, "I have caused to be sunk,"),
        (31, 35, "and made hills and valleys"),
        (36, 38, "in their place;"),
        (39, 43, "and their inhabitants"),
        (44, 46, "I have buried"),
        (47, 52, "in the depths of the earth,"),
        (53, 55, "to hide"),
        (56, 58, "their wickedness"),
        (59, 63, "and their abominations"),
        (64, 68, "from before my face,"),
        (69, 77, "that no more come unto me"),
        (78, 80, "the blood of the prophets"),
        (81, 84, "and the saints"),
        (85, 90, "against them."),
    ],
    9: [
        (0, 1, "And behold,"),
        (2, 7, "that great city of Jacobugath,"),
        (8, 10, "which was inhabited"),
        (11, 17, "by the people of king Jacob,"),
        (18, 22, "I have caused to be burned"),
        (23, 25, "with fire"),
        (26, 27, "because of"),
        (28, 30, "their sins"),
        (31, 34, "and their wickedness,"),
        (35, 38, "which exceeded"),
        (39, 47, "above the wickedness of the whole earth,"),
        (48, 49, "because of"),
        (50, 53, "their murders"),
        (54, 56, "and secret combinations;"),
        (57, 60, "for it was they"),
        (61, 62, "who destroyed"),
        (63, 67, "the peace of my people"),
        (68, 73, "and the government of the land;"),
        (74, 75, "therefore"),
        (76, 79, "I have caused"),
        (80, 83, "that they be burned,"),
        (84, 89, "to destroy them"),
        (90, 94, "from before my face,"),
        (95, 103, "that no more come unto me"),
        (104, 106, "the blood of the prophets"),
        (107, 110, "and the saints"),
        (111, 116, "against them."),
    ],
    10: [
        (0, 1, "And behold,"),
        (2, 6, "the city of Laman,"),
        (7, 11, "and the city of Josh,"),
        (12, 16, "and the city of Gad,"),
        (17, 21, "and the city of Kishkumen,"),
        (22, 26, "I have caused to be burned"),
        (27, 29, "with fire,"),
        (30, 34, "together with their inhabitants,"),
        (35, 36, "because of"),
        (37, 39, "their wickedness"),
        (40, 45, "in their casting out the prophets,"),
        (46, 52, "and their stoning of them"),
        (53, 54, "with stones"),
        (55, 60, "whom I sent"),
        (61, 67, "to declare unto them"),
        (68, 72, "concerning their wickedness"),
        (73, 77, "and their abominations."),
    ],
    11: [
        (0, 3, "And because"),
        (4, 9, "they cast them all out,"),
        (10, 15, "until there was none righteous"),
        (16, 24, "who was among them,"),
        (25, 26, "therefore"),
        (27, 33, "I sent down"),
        (34, 35, "the fire"),
        (36, 40, "and destroyed them,"),
        (41, 43, "that be hidden"),
        (44, 46, "their wickedness"),
        (47, 51, "and their abominations"),
        (52, 56, "from before my face,"),
        (57, 65, "that no more cry unto me"),
        (66, 68, "from the ground"),
        (69, 71, "the blood of the prophets"),
        (72, 75, "and the saints"),
        (76, 81, "whom I sent"),
        (82, 85, "unto them,"),
        (86, 91, "against them."),
    ],
    12: [
        (0, 4, "And many great destructions"),
        (5, 10, "I have caused to come"),
        (11, 15, "upon this land,"),
        (16, 21, "and upon this people,"),
        (22, 23, "because of"),
        (24, 26, "their wickedness"),
        (27, 31, "and their abominations."),
    ],
    13: [
        (0, 0, "O,"),
        (1, 3, "all ye who"),
        (4, 5, "are spared"),
        (6, 6, "because"),
        (7, 12, "your righteousness was greater"),
        (13, 16, "than theirs,"),
        (17, 24, "will ye not now return"),
        (25, 27, "unto me,"),
        (28, 29, "and repent"),
        (30, 32, "of your sins,"),
        (33, 34, "and be converted,"),
        (35, 39, "that I may heal you?"),
    ],
    14: [
        (0, 0, "Yea,"),
        (1, 6, "verily I say"),
        (7, 9, "unto you,"),
        (10, 14, "if ye come"),
        (15, 17, "unto me,"),
        (18, 22, "ye shall obtain"),
        (23, 25, "eternal life."),
        (26, 26, "Behold,"),
        (27, 29, "is stretched forth"),
        (30, 32, "towards you"),
        (33, 36, "my arm of mercy,"),
        (37, 43, "and whosoever comes,"),
        (44, 46, "that one"),
        (47, 51, "will I receive;"),
        (52, 58, "and blessed are those who"),
        (59, 64, "come unto me."),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 5, "I am Jesus Christ,"),
        (6, 10, "the Son of God."),
        (11, 14, "I created"),
        (15, 19, "the heaven and the earth,"),
        (20, 25, "and all things that are in them."),
        (26, 31, "I was"),
        (32, 35, "with the Father"),
        (36, 38, "from the beginning."),
        (39, 44, "I am"),
        (45, 49, "in the Father,"),
        (50, 52, "and the Father"),
        (53, 57, "in me;"),
        (58, 60, "and in me"),
        (61, 66, "the Father has glorified"),
        (67, 68, "his name."),
    ],
    16: [
        (0, 2, "I came"),
        (3, 6, "unto my own people,"),
        (7, 11, "and received me not"),
        (12, 15, "my own people."),
        (16, 19, "And are fulfilled"),
        (20, 21, "the scriptures"),
        (22, 26, "concerning my coming."),
    ],
    17: [
        (0, 6, "And as many of them"),
        (7, 12, "as have received me,"),
        (13, 16, "to them"),
        (17, 22, "I have granted"),
        (23, 29, "to become sons of God;"),
        (30, 39, "and even so will I grant"),
        (40, 45, "to as many of them"),
        (46, 52, "as believe on my name,"),
        (53, 54, "for behold,"),
        (55, 60, "by me comes"),
        (61, 62, "the redemption,"),
        (63, 65, "and in me"),
        (66, 68, "is fulfilled"),
        (69, 72, "the law of Moses."),
    ],
    18: [
        (0, 4, "I am the light"),
        (5, 10, "and the life of the world."),
        (11, 18, "I am the Alpha and the Omega,"),
        (19, 23, "the beginning and the end."),
    ],
    19: [
        (0, 6, "And ye shall no more offer up"),
        (7, 10, "unto me"),
        (11, 12, "a sacrifice"),
        (13, 18, "in the shedding of blood;"),
        (19, 19, "yea,"),
        (20, 23, "your sacrifices"),
        (24, 28, "and your burnt offerings"),
        (29, 31, "shall be done away,"),
        (32, 36, "for there shall be none"),
        (37, 40, "of your sacrifices"),
        (41, 46, "and your burnt offerings"),
        (47, 51, "that I will accept."),
    ],
    20: [
        (0, 4, "And ye shall offer"),
        (5, 7, "for a sacrifice"),
        (8, 10, "unto me"),
        (11, 13, "a broken heart"),
        (14, 17, "and a contrite spirit."),
        (18, 24, "And whoso comes"),
        (25, 27, "unto me"),
        (28, 31, "with a broken heart"),
        (32, 35, "and a contrite spirit,"),
        (36, 38, "that one"),
        (39, 43, "will I baptize"),
        (44, 50, "with fire and the Holy Ghost,"),
        (51, 55, "even as were baptized"),
        (56, 57, "the Lamanites"),
        (58, 64, "with fire and the Holy Ghost,"),
        (65, 72, "at the time of their conversion,"),
        (73, 74, "because of"),
        (75, 81, "their faith in me,"),
        (82, 87, "yet they knew it not."),
    ],
    21: [
        (0, 0, "Behold,"),
        (1, 3, "I have come"),
        (4, 6, "unto the world"),
        (7, 10, "to bring redemption"),
        (11, 13, "unto the world,"),
        (14, 17, "to save the world"),
        (18, 20, "from sin."),
    ],
    22: [
        (0, 1, "Therefore,"),
        (2, 6, "whoso repents"),
        (7, 11, "and comes unto me"),
        (12, 16, "as a little child,"),
        (17, 19, "that one"),
        (20, 24, "will I receive,"),
        (25, 29, "for of such is"),
        (30, 35, "the kingdom of God."),
        (36, 36, "Behold,"),
        (37, 41, "for such"),
        (42, 46, "I laid down"),
        (47, 48, "my life,"),
        (49, 54, "and I took it up again;"),
        (55, 56, "therefore"),
        (57, 60, "repent ye,"),
        (61, 66, "and come unto me"),
        (67, 71, "ye ends of the earth,"),
        (72, 74, "and be saved."),
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
