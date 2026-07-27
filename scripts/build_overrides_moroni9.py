"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 14 — a great curse comes upon
the land because of the iniquity of the people, such that whoso laid down his tool could
not find it again; every man kept his sword to defend his property; Coriantumr wars against
Gilead, then Lib, then Shiz, who sweeps the earth before him, and the whole face of the
land is covered with dead bodies as the two mighty armies pursue one another to the death.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_moroni9.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "moroni"
CHAPTER_NUM = 9

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "My beloved son,"),
        (4, 8, "I write again"),
        (9, 11, "unto thee"),
        (12, 15, "that thou mayest know"),
        (16, 20, "that I am still alive;"),
        (21, 25, "but I do write"),
        (26, 27, "concerning"),
        (28, 29, "the things"),
        (30, 34, "which grieve me sorely."),
    ],
    2: [
        (0, 1, "For behold,"),
        (2, 4, "I did fight"),
        (5, 7, "a sore battle"),
        (8, 10, "with the Lamanites,"),
        (11, 12, "wherein"),
        (13, 16, "we conquered not;"),
        (17, 19, "and hath fallen"),
        (20, 23, "Archeantus by the sword,"),
        (24, 28, "and Luram and Emron also;"),
        (29, 29, "yea,"),
        (30, 33, "and were lost"),
        (34, 37, "from us"),
        (38, 40, "a great number"),
        (41, 44, "of our men"),
        (45, 47, "the most choice."),
    ],
    3: [
        (0, 3, "And now behold,"),
        (4, 6, "my son,"),
        (7, 9, "I fear"),
        (10, 11, "lest destroy"),
        (12, 14, "the Lamanites"),
        (15, 16, "this people;"),
        (17, 17, "for"),
        (18, 21, "they repent not,"),
        (22, 25, "and ever provoketh"),
        (26, 27, "them"),
        (28, 29, "Satan"),
        (30, 31, "to anger"),
        (32, 34, "one"),
        (35, 37, "with another."),
    ],
    4: [
        (0, 0, "Behold,"),
        (1, 5, "I do labour still"),
        (6, 8, "without ceasing"),
        (9, 12, "with them;"),
        (13, 17, "and when I preach"),
        (18, 20, "the word"),
        (21, 23, "of God"),
        (24, 27, "with sharpness"),
        (28, 30, "they do tremble"),
        (31, 33, "and are angered"),
        (34, 36, "with me;"),
        (37, 39, "and when I"),
        (40, 42, "declare not"),
        (43, 47, "with sharpness also"),
        (48, 50, "they harden"),
        (51, 53, "their hearts"),
        (54, 57, "against it;"),
        (58, 61, "wherefore,"),
        (62, 64, "I fear"),
        (65, 67, "lest it be that"),
        (68, 71, "hath striven no more"),
        (72, 76, "the Spirit of the Lord"),
        (77, 79, "with them."),
    ],
    5: [
        (0, 2, "For they"),
        (3, 5, "rage exceedingly"),
        (6, 8, "that it seemeth"),
        (9, 11, "unto me"),
        (12, 16, "they have no dread"),
        (17, 19, "of death;"),
        (20, 22, "and there is not"),
        (23, 25, "their love,"),
        (26, 28, "one"),
        (29, 31, "toward another;"),
        (32, 35, "and they crave"),
        (36, 38, "for blood"),
        (39, 43, "and vengeance"),
        (44, 46, "without ceasing."),
    ],
    6: [
        (0, 2, "And now,"),
        (3, 6, "my beloved son,"),
        (7, 9, "though"),
        (10, 12, "their hardness,"),
        (13, 16, "let us still work"),
        (17, 19, "diligently;"),
        (20, 21, "for if"),
        (22, 26, "we two leave off the work,"),
        (27, 30, "shall be brought"),
        (31, 32, "we"),
        (33, 35, "under condemnation;"),
        (36, 39, "for there is"),
        (40, 42, "our work"),
        (43, 44, "to perform"),
        (45, 48, "while we abide"),
        (49, 53, "in this house of clay,"),
        (54, 57, "that we conquer"),
        (58, 59, "the foe"),
        (60, 63, "of all righteousness,"),
        (64, 66, "and rest"),
        (67, 69, "our souls"),
        (70, 72, "in the kingdom"),
        (73, 75, "of God."),
    ],
    7: [
        (0, 2, "And now"),
        (3, 7, "I do write"),
        (8, 9, "concerning"),
        (10, 14, "the sufferings of this people."),
        (15, 18, "For according to"),
        (19, 21, "the knowledge"),
        (22, 25, "which I received"),
        (26, 27, "from Amoron,"),
        (28, 28, "behold,"),
        (29, 33, "the Lamanites have taken"),
        (34, 37, "many prisoners,"),
        (38, 41, "which they brought"),
        (42, 46, "from the tower of Sherrizah;"),
        (47, 50, "and there were"),
        (51, 54, "men, women, and children."),
    ],
    8: [
        (0, 4, "And the men and fathers"),
        (5, 9, "of those women and children"),
        (10, 12, "they have slain;"),
        (13, 16, "and they feed"),
        (17, 17, "the women"),
        (18, 20, "with the flesh"),
        (21, 23, "of their husbands,"),
        (24, 25, "and the children"),
        (26, 28, "with the flesh"),
        (29, 31, "of their fathers;"),
        (32, 36, "and they give no"),
        (37, 40, "unto them"),
        (41, 42, "water,"),
        (43, 44, "except"),
        (45, 47, "a little bit."),
    ],
    9: [
        (0, 3, "And notwithstanding"),
        (4, 7, "this great wickedness"),
        (8, 10, "of the Lamanites,"),
        (11, 14, "it surpasseth not"),
        (15, 19, "that which was done"),
        (20, 23, "by our people"),
        (24, 25, "in Moriantum."),
        (26, 27, "For behold,"),
        (28, 30, "many daughters"),
        (31, 33, "of the Lamanites"),
        (34, 37, "have they taken captive;"),
        (38, 42, "and after"),
        (43, 45, "they took away"),
        (46, 49, "from them"),
        (50, 52, "that thing"),
        (53, 58, "was most cherished and prized"),
        (59, 63, "above all things,"),
        (64, 67, "which is the pure life"),
        (68, 71, "and virtue—"),
    ],
    10: [
        (0, 6, "And after they had done"),
        (7, 9, "this thing,"),
        (10, 12, "they did slay"),
        (13, 14, "them"),
        (15, 21, "in a most brutal way,"),
        (22, 26, "tormenting their bodies"),
        (27, 30, "until they died;"),
        (31, 37, "and after they had done"),
        (38, 40, "this thing,"),
        (41, 43, "they consumed"),
        (44, 46, "their bodies"),
        (47, 51, "like wild animals,"),
        (52, 55, "because of the hardness"),
        (56, 59, "of their hearts;"),
        (60, 63, "and they did it"),
        (64, 65, "this thing"),
        (66, 68, "as a sign"),
        (69, 72, "of courage."),
    ],
    11: [
        (0, 0, "O,"),
        (1, 4, "my beloved son,"),
        (5, 7, "how is it possible"),
        (8, 11, "for such a people,"),
        (12, 14, "without"),
        (15, 17, "civilization—"),
    ],
    12: [
        (0, 2, "(And only"),
        (3, 6, "a few years"),
        (7, 9, "have gone by,"),
        (10, 14, "were they made"),
        (15, 17, "a people"),
        (18, 19, "civilized"),
        (20, 21, "and delightsome)"),
    ],
    13: [
        (0, 0, "But"),
        (1, 3, "my son,"),
        (4, 6, "how is it possible"),
        (7, 10, "for such a people,"),
        (11, 12, "who"),
        (13, 16, "their delight"),
        (17, 20, "is therein"),
        (21, 23, "in the doing"),
        (24, 28, "of so much abomination—"),
    ],
    14: [
        (0, 2, "How is it possible"),
        (3, 5, "that we expect"),
        (6, 9, "shall withhold"),
        (10, 12, "God"),
        (13, 14, "his hand"),
        (15, 17, "in judgment"),
        (18, 19, "against"),
        (20, 23, "us?"),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 3, "doth cry"),
        (4, 5, "my heart:"),
        (6, 7, "Wo"),
        (8, 10, "unto this people."),
        (11, 13, "Come thou forth,"),
        (14, 16, "O God,"),
        (17, 19, "in judgment,"),
        (20, 24, "and cover their sins,"),
        (25, 26, "and iniquities,"),
        (27, 29, "and abominations"),
        (30, 34, "from before thy face!"),
    ],
    16: [
        (0, 2, "And again,"),
        (3, 5, "my son,"),
        (6, 8, "many women"),
        (9, 13, "whose husbands have died,"),
        (14, 18, "and their daughters,"),
        (19, 22, "who yet dwell"),
        (23, 24, "in Sherrizah;"),
        (25, 28, "and the portion"),
        (29, 30, "of food"),
        (31, 34, "which was not taken"),
        (35, 37, "by the Lamanites,"),
        (38, 38, "behold,"),
        (39, 41, "hath carried off"),
        (42, 45, "the army of Zenephi,"),
        (46, 49, "and left"),
        (50, 51, "them"),
        (52, 54, "to roam about"),
        (55, 58, "to any place"),
        (59, 62, "that they may be able"),
        (63, 66, "to go there"),
        (67, 69, "for food;"),
        (70, 72, "and many"),
        (73, 74, "old women"),
        (75, 76, "do swoon"),
        (77, 79, "by the way"),
        (80, 82, "and perish."),
    ],
    17: [
        (0, 3, "And the army"),
        (4, 7, "which is with me"),
        (8, 9, "is weak;"),
        (10, 12, "and the armies"),
        (13, 15, "of the Lamanites"),
        (16, 20, "are in the midst"),
        (21, 24, "between Sherrizah and me;"),
        (25, 28, "and the many"),
        (29, 30, "who"),
        (31, 33, "fled"),
        (34, 38, "to the army of Aaron"),
        (39, 41, "have fallen slain"),
        (42, 45, "by their cruelty"),
        (46, 47, "terrible and beastly."),
    ],
    18: [
        (0, 0, "O,"),
        (1, 3, "the wickedness"),
        (4, 6, "of my people!"),
        (7, 10, "They lack"),
        (11, 13, "order,"),
        (14, 16, "and are without"),
        (17, 20, "tender mercy."),
        (21, 21, "Behold,"),
        (22, 23, "I am"),
        (24, 27, "but a man,"),
        (28, 32, "and but the strength"),
        (33, 35, "of a man"),
        (36, 39, "have I,"),
        (40, 43, "and cannot"),
        (44, 47, "I any more enforce"),
        (48, 50, "my commands."),
    ],
    19: [
        (0, 3, "And they are mighty"),
        (4, 8, "in their perverse ways;"),
        (9, 11, "and are as"),
        (12, 15, "their beastly cruelty,"),
        (16, 18, "sparing not"),
        (19, 20, "any one,"),
        (21, 24, "whether old or young;"),
        (25, 28, "and they take joy"),
        (29, 31, "in all things"),
        (32, 33, "save"),
        (34, 36, "the good thing;"),
        (37, 40, "and the suffering"),
        (41, 44, "of our women"),
        (45, 48, "and our children"),
        (49, 52, "upon"),
        (53, 55, "all this land"),
        (56, 58, "doth surpass"),
        (59, 61, "all things;"),
        (62, 62, "yea,"),
        (63, 68, "the tongue is not able"),
        (69, 70, "to tell,"),
        (71, 73, "nor can"),
        (74, 75, "be written."),
    ],
    20: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 10, "I no longer desire"),
        (11, 13, "to speak"),
        (14, 15, "concerning"),
        (16, 20, "this horrible dreadful scene."),
        (21, 21, "Behold,"),
        (22, 24, "thou dost know"),
        (25, 29, "the wickedness of this people;"),
        (30, 32, "thou knowest"),
        (33, 36, "that they lack"),
        (37, 39, "any honour,"),
        (40, 42, "and they"),
        (43, 45, "feel no more"),
        (46, 47, "any good;"),
        (48, 52, "and their wickedness"),
        (53, 55, "surpasseth"),
        (56, 59, "that of the Lamanites."),
    ],
    21: [
        (0, 0, "Behold,"),
        (1, 3, "my son,"),
        (4, 10, "I cannot commend"),
        (11, 12, "them"),
        (13, 15, "unto God"),
        (16, 17, "lest strike"),
        (18, 20, "me he."),
    ],
    22: [
        (0, 1, "But behold,"),
        (2, 4, "my son,"),
        (5, 8, "I do recommend"),
        (9, 9, "thee"),
        (10, 12, "unto God,"),
        (13, 16, "and I rely"),
        (17, 18, "on Christ"),
        (19, 21, "that thou be saved;"),
        (22, 26, "and I do pray"),
        (27, 29, "unto God"),
        (30, 33, "that he preserve"),
        (34, 35, "thy life,"),
        (36, 37, "to witness"),
        (38, 41, "the return"),
        (42, 44, "of his people"),
        (45, 47, "unto him,"),
        (48, 51, "or their"),
        (52, 53, "utter ruin;"),
        (54, 57, "for I do know"),
        (58, 61, "shall perish"),
        (62, 63, "they"),
        (64, 68, "except they repent"),
        (69, 72, "and return"),
        (73, 75, "unto him."),
    ],
    23: [
        (0, 1, "And if"),
        (2, 5, "they should perish"),
        (6, 9, "shall be as"),
        (10, 12, "the Jaredites,"),
        (13, 16, "because of the desire"),
        (17, 20, "of their hearts,"),
        (21, 23, "seeking after"),
        (24, 25, "blood"),
        (26, 28, "and revenge."),
    ],
    24: [
        (0, 3, "And if it be so"),
        (4, 7, "they shall perish,"),
        (8, 9, "they,"),
        (10, 12, "we do know"),
        (13, 17, "that many of our brethren"),
        (18, 20, "have deserted"),
        (21, 23, "unto the Lamanites,"),
        (24, 28, "and yet more"),
        (29, 30, "some others"),
        (31, 35, "shall flee"),
        (36, 39, "unto them;"),
        (40, 43, "wherefore,"),
        (44, 47, "write thou"),
        (48, 51, "a few little things,"),
        (52, 56, "if thou art preserved"),
        (57, 57, "and"),
        (58, 62, "I shall perish"),
        (63, 65, "and see not"),
        (66, 68, "thee;"),
        (69, 72, "but I believe"),
        (73, 76, "that it may be soon"),
        (77, 79, "that I see"),
        (80, 82, "thee;"),
        (83, 87, "for there is unto me"),
        (88, 90, "sacred records"),
        (91, 96, "that I will give"),
        (97, 99, "unto thee."),
    ],
    25: [
        (0, 2, "My son,"),
        (3, 5, "be thou faithful"),
        (6, 7, "in Christ;"),
        (8, 11, "and may not be"),
        (12, 15, "the things I have written"),
        (16, 19, "made into things"),
        (20, 23, "which grieve thee,"),
        (24, 25, "to burden"),
        (26, 28, "thee"),
        (29, 32, "until thou die;"),
        (33, 34, "but I pray"),
        (35, 37, "that lift up"),
        (38, 40, "thee on high"),
        (41, 42, "by Christ,"),
        (43, 44, "and may"),
        (45, 46, "there abide"),
        (47, 48, "his sufferings"),
        (49, 51, "and his death,"),
        (52, 55, "and the manifestation"),
        (56, 58, "of his body"),
        (59, 62, "unto our fathers,"),
        (63, 66, "and his tender mercy"),
        (67, 69, "and long-suffering,"),
        (70, 72, "and the hope"),
        (73, 75, "of his glory"),
        (76, 79, "and of everlasting life,"),
        (80, 82, "abide in"),
        (83, 84, "thy mind"),
        (85, 86, "for ever."),
    ],
    26: [
        (0, 2, "And may be"),
        (3, 5, "the grace"),
        (6, 10, "of God the Father,"),
        (11, 15, "whose throne"),
        (16, 17, "is exalted"),
        (18, 20, "in heaven,"),
        (21, 24, "and our Lord"),
        (25, 27, "Jesus Christ,"),
        (28, 31, "who is seated"),
        (32, 36, "at the right hand"),
        (37, 39, "of his power,"),
        (40, 42, "until"),
        (43, 45, "he reigneth"),
        (46, 48, "over all things,"),
        (49, 51, "and abide"),
        (52, 54, "with you"),
        (55, 56, "for ever."),
        (57, 57, "Amen."),
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
