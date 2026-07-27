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

    python3 build_overrides_ether15.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 15

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 7, "had grown strong again"),
        (8, 8, "Coriantumr"),
        (9, 11, "from his wounds,"),
        (12, 16, "he began to remember"),
        (17, 18, "the words"),
        (19, 23, "which Ether had spoken"),
        (24, 26, "unto him."),
    ],
    2: [
        (0, 2, "He saw"),
        (3, 6, "that had been slain"),
        (7, 9, "by the sword"),
        (10, 12, "nearly"),
        (13, 15, "two millions"),
        (16, 18, "of his people,"),
        (19, 24, "and he began to mourn"),
        (25, 27, "in his heart;"),
        (28, 28, "yea,"),
        (29, 32, "there were slain"),
        (33, 36, "two millions"),
        (37, 39, "of mighty men,"),
        (40, 44, "and also their wives"),
        (45, 48, "and their children."),
    ],
    3: [
        (0, 5, "He began to repent"),
        (6, 9, "of the evil"),
        (10, 12, "which he had done;"),
        (13, 17, "he began to remember"),
        (18, 19, "the words"),
        (20, 23, "which were spoken"),
        (24, 27, "by the mouth of all prophets,"),
        (28, 32, "and he beheld"),
        (33, 37, "that they were fulfilled,"),
        (38, 41, "every single word,"),
        (42, 44, "even unto"),
        (45, 48, "this very time;"),
        (49, 53, "and his soul mourned"),
        (54, 55, "and would not"),
        (56, 57, "be comforted."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he wrote"),
        (7, 8, "a letter"),
        (9, 10, "unto Shiz,"),
        (11, 15, "desiring of him"),
        (16, 20, "that he spare the people,"),
        (21, 21, "and"),
        (22, 27, "he would give up"),
        (28, 29, "the kingdom,"),
        (30, 32, "for the lives"),
        (33, 34, "of the people."),
    ],
    5: [
        (0, 3, "And it came to pass that"),
        (4, 7, "received Shiz"),
        (8, 9, "his letter"),
        (10, 14, "and he did write"),
        (15, 16, "a letter"),
        (17, 18, "unto Coriantumr,"),
        (19, 21, "saying that if"),
        (22, 25, "he would deliver up"),
        (26, 28, "himself,"),
        (29, 33, "that he might"),
        (34, 36, "slay him"),
        (37, 40, "with his own sword,"),
        (41, 45, "he would spare"),
        (46, 47, "the lives"),
        (48, 49, "of the people."),
    ],
    6: [
        (0, 3, "And it came to pass that"),
        (4, 6, "repented not the people"),
        (7, 10, "of their iniquity;"),
        (11, 15, "and was kindled the wrath"),
        (16, 19, "of Coriantumr's people"),
        (20, 21, "against"),
        (22, 25, "the people of Shiz;"),
        (26, 30, "and was kindled the wrath"),
        (31, 34, "of Shiz's people"),
        (35, 36, "against"),
        (37, 40, "the people of Coriantumr;"),
        (41, 44, "wherefore"),
        (45, 49, "did make war"),
        (50, 52, "the people of Shiz"),
        (53, 56, "against the people of Coriantumr."),
    ],
    7: [
        (0, 4, "And when perceived"),
        (5, 5, "Coriantumr"),
        (6, 9, "that should fall"),
        (10, 11, "he"),
        (12, 16, "he again fled"),
        (17, 19, "from before"),
        (20, 22, "the people of Shiz."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he arrived"),
        (8, 11, "at the waters of Ripliancum,"),
        (12, 14, "the meaning of which,"),
        (15, 17, "when translated,"),
        (18, 19, "is large,"),
        (20, 22, "or exceeding"),
        (23, 25, "all things;"),
        (26, 29, "wherefore,"),
        (30, 34, "when they had come"),
        (35, 37, "unto these waters,"),
        (38, 40, "they set up"),
        (41, 43, "their tents;"),
        (44, 47, "and also pitched"),
        (48, 49, "Shiz"),
        (50, 51, "his tents"),
        (52, 53, "hard by"),
        (54, 57, "unto them;"),
        (58, 60, "and so,"),
        (61, 63, "the day"),
        (64, 66, "that came next,"),
        (67, 71, "they came forth"),
        (72, 73, "to battle."),
    ],
    9: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they fought"),
        (6, 10, "an exceeding sore battle,"),
        (11, 15, "wherein was again wounded"),
        (16, 16, "Coriantumr,"),
        (17, 21, "and he fainted"),
        (22, 26, "from the blood that was shed."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 5, "pressed forward"),
        (6, 8, "Coriantumr's armies"),
        (9, 11, "upon"),
        (12, 14, "Shiz's armies"),
        (15, 17, "so that"),
        (18, 19, "they did defeat"),
        (20, 21, "them,"),
        (22, 25, "and it came to pass"),
        (26, 27, "they caused"),
        (28, 31, "them"),
        (32, 34, "to flee"),
        (35, 38, "from before them;"),
        (39, 42, "and they fled"),
        (43, 45, "toward the south,"),
        (46, 49, "and they set up"),
        (50, 52, "their tents"),
        (53, 56, "in the place"),
        (57, 60, "which was called Ogath."),
    ],
    11: [
        (0, 3, "And it came to pass that"),
        (4, 8, "pitched the army of Coriantumr"),
        (9, 11, "their tents"),
        (12, 14, "beside"),
        (15, 18, "the hill of Ramah;"),
        (19, 21, "and it was"),
        (22, 24, "that very hill"),
        (25, 28, "where hid away"),
        (29, 33, "my father Mormon"),
        (34, 35, "the records,"),
        (36, 37, "which are holy,"),
        (38, 40, "unto the Lord."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 6, "the two assembled together"),
        (7, 8, "all the people"),
        (9, 12, "upon"),
        (13, 14, "all the land,"),
        (15, 16, "who"),
        (17, 19, "had not been slain,"),
        (20, 22, "save Ether."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Ether saw"),
        (6, 8, "all the things"),
        (9, 12, "which the people did;"),
        (13, 16, "and he beheld"),
        (17, 21, "the people who favored Coriantumr"),
        (22, 24, "were assembled"),
        (25, 29, "to Coriantumr's army;"),
        (30, 32, "and the people"),
        (33, 35, "who were for Shiz"),
        (36, 38, "gathered together"),
        (39, 43, "to Shiz's army."),
    ],
    14: [
        (0, 3, "Wherefore,"),
        (4, 8, "the two assembled"),
        (9, 9, "the people"),
        (10, 13, "for the space of"),
        (14, 16, "four years,"),
        (17, 22, "that they might gather"),
        (23, 24, "all the people"),
        (25, 27, "who were"),
        (28, 32, "upon the land,"),
        (33, 38, "and that they get"),
        (39, 41, "all the strength"),
        (42, 47, "which they were able to gain."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 8, "when they all gathered,"),
        (9, 11, "each person"),
        (12, 14, "to the army"),
        (15, 18, "which he had chosen,"),
        (19, 23, "along with their wives"),
        (24, 27, "and their children—"),
        (28, 29, "both men,"),
        (30, 32, "women, and children"),
        (33, 34, "were armed"),
        (35, 38, "with weapons of war,"),
        (39, 42, "having shields,"),
        (43, 44, "and breastplates,"),
        (45, 46, "and head-plates;"),
        (47, 49, "and clothed"),
        (50, 52, "even as"),
        (53, 56, "the dress of war—"),
        (57, 60, "they went forth"),
        (61, 64, "the one against"),
        (65, 67, "the other"),
        (68, 70, "to the war;"),
        (71, 74, "and they battled"),
        (75, 78, "all that day,"),
        (79, 83, "and neither conquered."),
    ],
    16: [
        (0, 3, "And it came to pass that"),
        (4, 6, "when came"),
        (7, 8, "the night"),
        (9, 11, "they grew weary,"),
        (12, 14, "and withdrew"),
        (15, 18, "to their camps;"),
        (19, 23, "and after"),
        (24, 26, "they retired"),
        (27, 30, "to their camps,"),
        (31, 35, "they began to wail"),
        (36, 37, "and mourn"),
        (38, 40, "for the loss"),
        (41, 44, "of their people"),
        (45, 46, "who were slain;"),
        (47, 51, "and so great was"),
        (52, 54, "their cry,"),
        (55, 59, "their howling and mourning,"),
        (60, 62, "which they made"),
        (63, 67, "did rend exceedingly"),
        (68, 69, "the air."),
    ],
    17: [
        (0, 2, "And it came to pass"),
        (3, 5, "on the day"),
        (6, 8, "that followed,"),
        (9, 13, "they again went forth"),
        (14, 15, "to battle,"),
        (16, 20, "and great and terrible was"),
        (21, 22, "that day;"),
        (23, 26, "nevertheless,"),
        (27, 30, "they prevailed not,"),
        (31, 36, "and when again came"),
        (37, 38, "the night"),
        (39, 41, "they caused"),
        (42, 46, "to rend the air"),
        (47, 50, "with their cries,"),
        (51, 54, "and their howlings,"),
        (55, 58, "and their mournings,"),
        (59, 62, "because of the loss"),
        (63, 66, "of their people"),
        (67, 68, "who were slain."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 8, "again wrote Coriantumr"),
        (9, 10, "a letter"),
        (11, 12, "unto Shiz,"),
        (13, 16, "desiring"),
        (17, 20, "that he come no more"),
        (21, 22, "to battle,"),
        (23, 26, "but that he take"),
        (27, 28, "the kingdom,"),
        (29, 31, "and preserve the life"),
        (32, 33, "of the people."),
    ],
    19: [
        (0, 1, "But behold,"),
        (2, 5, "strove no more"),
        (6, 10, "the Spirit of the Lord"),
        (11, 13, "with them,"),
        (14, 18, "and Satan had gained"),
        (19, 21, "full power"),
        (22, 25, "over the hearts of the people;"),
        (26, 29, "for were given up"),
        (30, 31, "they"),
        (32, 34, "to the hardness"),
        (35, 38, "of their hearts,"),
        (39, 41, "and the blindness"),
        (42, 45, "of their minds,"),
        (46, 48, "that might be destroyed"),
        (49, 50, "they;"),
        (51, 54, "wherefore"),
        (55, 59, "they went again"),
        (60, 61, "also"),
        (62, 63, "to battle."),
    ],
    20: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they fought"),
        (6, 9, "all that day,"),
        (10, 14, "and when came"),
        (15, 16, "the night"),
        (17, 19, "they did sleep"),
        (20, 23, "upon their swords."),
    ],
    21: [
        (0, 3, "And on the day"),
        (4, 6, "which came next"),
        (7, 9, "they fought"),
        (10, 12, "until came"),
        (13, 14, "the night."),
    ],
    22: [
        (0, 4, "And when came"),
        (5, 6, "the night"),
        (7, 9, "they were drunken"),
        (10, 12, "with anger,"),
        (13, 17, "even like a man"),
        (18, 21, "who is drunken"),
        (22, 24, "with wine;"),
        (25, 29, "and they again slept"),
        (30, 33, "upon their swords."),
    ],
    23: [
        (0, 3, "And on the day"),
        (4, 6, "which came next"),
        (7, 10, "they fought again;"),
        (11, 15, "and when came"),
        (16, 17, "the night"),
        (18, 21, "they had all fallen"),
        (22, 24, "by the sword"),
        (25, 26, "except"),
        (27, 29, "fifty"),
        (30, 32, "and two"),
        (33, 36, "of the people of Coriantumr,"),
        (37, 40, "and sixty"),
        (41, 43, "and nine"),
        (44, 47, "of the people of Shiz."),
    ],
    24: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they slept"),
        (6, 9, "upon their swords"),
        (10, 13, "that night,"),
        (14, 17, "and on the day"),
        (18, 20, "that followed"),
        (21, 24, "they fought again,"),
        (25, 28, "and they fought"),
        (29, 32, "with their might"),
        (33, 36, "with their swords"),
        (37, 40, "and their shields,"),
        (41, 45, "all that whole day."),
    ],
    25: [
        (0, 4, "And when came"),
        (5, 6, "the night"),
        (7, 8, "there remained"),
        (9, 11, "thirty"),
        (12, 14, "and two"),
        (15, 18, "of the people of Shiz,"),
        (19, 22, "and twenty"),
        (23, 25, "and seven"),
        (26, 29, "of the people of Coriantumr."),
    ],
    26: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they did eat"),
        (6, 7, "and sleep,"),
        (8, 9, "and made ready"),
        (10, 12, "for death"),
        (13, 15, "on the day"),
        (16, 18, "that followed."),
        (19, 22, "And they were"),
        (23, 25, "such as were men"),
        (26, 29, "large and mighty"),
        (30, 32, "even as"),
        (33, 37, "the strength of men."),
    ],
    27: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they fought"),
        (6, 9, "for the space of"),
        (10, 12, "three hours,"),
        (13, 16, "and they fainted"),
        (17, 20, "from the shed blood."),
    ],
    28: [
        (0, 3, "And it came to pass that"),
        (4, 7, "was sufficient the strength"),
        (8, 10, "which was received by"),
        (11, 13, "the people of Coriantumr"),
        (14, 19, "that they could walk,"),
        (20, 21, "it happened"),
        (22, 26, "they would flee"),
        (27, 30, "for their lives;"),
        (31, 32, "but behold,"),
        (33, 36, "Shiz rose up,"),
        (37, 40, "and his men also,"),
        (41, 44, "and he swore"),
        (45, 47, "in his anger"),
        (48, 52, "that he would slay"),
        (53, 53, "Coriantumr"),
        (54, 58, "or he should die"),
        (59, 61, "by the sword."),
    ],
    29: [
        (0, 3, "Wherefore,"),
        (4, 7, "he did pursue"),
        (8, 9, "them,"),
        (10, 13, "and on the day"),
        (14, 16, "that followed"),
        (17, 21, "he overtook"),
        (22, 23, "them;"),
        (24, 28, "and they fought again"),
        (29, 31, "with the sword."),
        (32, 35, "And it came to pass that"),
        (36, 39, "they all fell"),
        (40, 42, "by the sword,"),
        (43, 44, "except"),
        (45, 47, "Coriantumr and Shiz,"),
        (48, 48, "behold"),
        (49, 51, "Shiz swooned"),
        (52, 55, "from the loss of blood."),
    ],
    30: [
        (0, 3, "And it came to pass that"),
        (4, 6, "after"),
        (7, 9, "Coriantumr rested"),
        (10, 14, "upon his sword,"),
        (15, 17, "until he rested a little"),
        (18, 19, "he,"),
        (20, 25, "then he struck off"),
        (26, 30, "the head of Shiz."),
    ],
    31: [
        (0, 3, "And it came to pass that"),
        (4, 9, "after he had smitten off"),
        (10, 14, "the head of Shiz,"),
        (15, 19, "Shiz strove to rise"),
        (20, 24, "upon his hands"),
        (25, 27, "and fell;"),
        (28, 31, "after that"),
        (32, 34, "he strove"),
        (35, 39, "wishing to gain breath,"),
        (40, 43, "he died."),
    ],
    32: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Coriantumr sank down"),
        (6, 8, "to the ground,"),
        (9, 12, "and was as though"),
        (13, 16, "there was no life"),
        (17, 20, "in him."),
    ],
    33: [
        (0, 3, "And spake"),
        (4, 5, "the Lord"),
        (6, 7, "unto Ether,"),
        (8, 10, "and said"),
        (11, 13, "unto him:"),
        (14, 16, "Go forth."),
        (17, 20, "And went out"),
        (21, 22, "he,"),
        (23, 24, "and saw"),
        (25, 26, "were fulfilled"),
        (27, 31, "all the words of the Lord;"),
        (32, 35, "and he finished"),
        (36, 37, "his record;"),
        (38, 42, "(and I wrote not"),
        (43, 46, "the one part"),
        (47, 48, "of a hundred)"),
        (49, 52, "and he hid away"),
        (53, 54, "them"),
        (55, 57, "in a manner"),
        (58, 60, "whereby were found"),
        (61, 64, "by the people of Limhi."),
    ],
    34: [
        (0, 1, "Now"),
        (2, 5, "these last words"),
        (6, 9, "were written by Ether:"),
        (10, 13, "Whether desireth the Lord"),
        (14, 16, "that I be translated,"),
        (17, 20, "or I suffer"),
        (21, 23, "the will"),
        (24, 26, "of the Lord"),
        (27, 30, "in the flesh,"),
        (31, 33, "it mattereth not,"),
        (34, 35, "if so be"),
        (36, 38, "I be saved"),
        (39, 41, "in the kingdom"),
        (42, 44, "of God."),
        (45, 45, "Amen."),
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
