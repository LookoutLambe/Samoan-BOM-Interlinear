"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 14 — the close of
the Sermon at the temple: Jesus warns against unrighteous judgment (the mote and
the beam), against casting pearls before swine; promises that they who ask, seek,
and knock shall receive; teaches the golden rule and the strait gate and narrow
way; warns against false prophets known by their fruits, and against those who
say "Lord, Lord" yet do not the Father's will; and likens the doer of his sayings
to a wise man building on a rock, the hearer only to a fool building on sand.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split applied to bom_books.json before glossing:
    14:4  mata—ae  ->  mata—  +  ae

    python3 build_overrides_3nephi14.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 14

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 12, "when Jesus had spoken"),
        (13, 14, "these words,"),
        (15, 20, "he turned again"),
        (21, 25, "to the multitude,"),
        (26, 32, "and opened his mouth again"),
        (33, 36, "unto them,"),
        (37, 39, "saying:"),
        (40, 43, "Verily, verily,"),
        (44, 47, "I say"),
        (48, 50, "unto you,"),
        (51, 54, "Judge not,"),
        (55, 59, "that ye be not judged."),
    ],
    2: [
        (0, 0, "For"),
        (1, 3, "with the judgment"),
        (4, 8, "by which ye judge,"),
        (9, 14, "ye shall be judged;"),
        (15, 18, "and with the measure"),
        (19, 22, "ye mete,"),
        (23, 28, "it shall be measured again"),
        (29, 31, "to you."),
    ],
    3: [
        (0, 5, "And why beholdest thou"),
        (6, 10, "the mote which"),
        (11, 18, "is in thy brother's eye,"),
        (19, 22, "but considerest not"),
        (23, 26, "the beam which"),
        (27, 32, "is in thine own eye?"),
    ],
    4: [
        (0, 6, "Or how wilt thou say"),
        (7, 9, "to thy brother:"),
        (10, 14, "Allow me"),
        (15, 18, "to pull out"),
        (19, 21, "the mote"),
        (22, 24, "from thine eye—"),
        (25, 26, "and behold,"),
        (27, 32, "there is a beam"),
        (33, 36, "in thine own eye?"),
    ],
    5: [
        (0, 4, "Thou hypocrite,"),
        (5, 7, "first remove"),
        (8, 9, "the beam"),
        (10, 13, "from thine own eye;"),
        (14, 18, "and then shall be clear"),
        (19, 21, "thy sight"),
        (22, 27, "to remove the mote"),
        (28, 33, "from thy brother's eye."),
    ],
    6: [
        (0, 3, "Give not"),
        (4, 6, "that which is holy"),
        (7, 8, "unto the dogs,"),
        (9, 12, "nor cast ye"),
        (13, 15, "your pearls"),
        (16, 19, "before swine,"),
        (20, 25, "lest they trample them"),
        (26, 31, "under their feet,"),
        (32, 36, "and turn again"),
        (37, 39, "and rend you."),
    ],
    7: [
        (0, 1, "Ask,"),
        (2, 7, "and it shall be given"),
        (8, 10, "unto you;"),
        (11, 11, "seek,"),
        (12, 17, "and ye shall find;"),
        (18, 19, "knock,"),
        (20, 25, "and it shall be opened"),
        (26, 28, "unto you."),
    ],
    8: [
        (0, 4, "For all those"),
        (5, 7, "who ask,"),
        (8, 12, "it is given to them;"),
        (13, 19, "and he who seeks,"),
        (20, 23, "he finds;"),
        (24, 29, "and he who knocks,"),
        (30, 34, "it shall be opened"),
        (35, 37, "unto him."),
    ],
    9: [
        (0, 6, "Or is there a man"),
        (7, 9, "among you,"),
        (10, 11, "who,"),
        (12, 17, "if his son asks"),
        (18, 20, "for bread,"),
        (21, 25, "will he give"),
        (26, 28, "unto him"),
        (29, 30, "a stone?"),
    ],
    10: [
        (0, 6, "Or if he asks"),
        (7, 9, "for a fish,"),
        (10, 14, "will he give"),
        (15, 17, "unto him"),
        (18, 19, "a serpent?"),
    ],
    11: [
        (0, 2, "If ye,"),
        (3, 4, "being evil,"),
        (5, 12, "know the way to give"),
        (13, 14, "good gifts"),
        (15, 17, "unto your children,"),
        (18, 22, "how much more"),
        (23, 32, "will your Father who is in heaven"),
        (33, 38, "give good things"),
        (39, 44, "to those who"),
        (45, 50, "ask him?"),
    ],
    12: [
        (0, 1, "Therefore,"),
        (2, 5, "all things whatsoever"),
        (6, 10, "ye would"),
        (11, 15, "that men do"),
        (16, 18, "to you,"),
        (19, 24, "even so do ye"),
        (25, 28, "to them,"),
        (29, 33, "for this is the law"),
        (34, 35, "and the prophets."),
    ],
    13: [
        (0, 3, "Enter ye in"),
        (4, 7, "at the strait gate;"),
        (8, 8, "for"),
        (9, 12, "wide is the gate,"),
        (13, 16, "and broad is the way,"),
        (17, 20, "which leads"),
        (21, 23, "to destruction,"),
        (24, 27, "and many are they who"),
        (28, 34, "will go in thereat;"),
    ],
    14: [
        (0, 0, "Because"),
        (1, 4, "strait is the gate,"),
        (5, 8, "and narrow is the way,"),
        (9, 12, "which leads"),
        (13, 15, "unto life,"),
        (16, 19, "and few are they who"),
        (20, 24, "shall find it."),
    ],
    15: [
        (0, 1, "Beware"),
        (2, 4, "of false prophets,"),
        (5, 9, "who come"),
        (10, 12, "to you"),
        (13, 15, "in sheep's clothing,"),
        (16, 18, "but inwardly"),
        (19, 24, "they are ravening wolves."),
    ],
    16: [
        (0, 6, "Ye shall know them"),
        (7, 10, "by their fruits."),
        (11, 17, "Do men gather grapes"),
        (18, 21, "from the thorn bush,"),
        (22, 24, "or figs"),
        (25, 27, "from thistles?"),
    ],
    17: [
        (0, 5, "Even so brings forth"),
        (6, 9, "every good tree"),
        (10, 11, "good fruit;"),
        (12, 17, "but a corrupt tree"),
        (18, 23, "brings forth evil fruit."),
    ],
    18: [
        (0, 6, "A good tree cannot"),
        (7, 12, "bring forth evil fruit,"),
        (13, 18, "nor can a corrupt tree"),
        (19, 24, "bring forth good fruit."),
    ],
    19: [
        (0, 3, "Every tree"),
        (4, 10, "that brings not forth good fruit"),
        (11, 14, "is hewn down,"),
        (15, 19, "and cast into the fire."),
    ],
    20: [
        (0, 1, "Wherefore,"),
        (2, 8, "ye shall know them"),
        (9, 12, "by their fruits."),
    ],
    21: [
        (0, 3, "Shall not enter"),
        (4, 9, "into the kingdom of heaven"),
        (10, 14, "all those who"),
        (15, 20, "say unto me,"),
        (21, 23, "Lord,"),
        (24, 26, "Lord;"),
        (27, 31, "but he who"),
        (32, 36, "does the will"),
        (37, 39, "of my Father"),
        (40, 45, "who is in heaven."),
    ],
    22: [
        (0, 6, "Many will say"),
        (7, 9, "unto me"),
        (10, 12, "in that day:"),
        (13, 15, "Lord,"),
        (16, 18, "Lord,"),
        (19, 24, "have we not prophesied"),
        (25, 27, "in thy name,"),
        (28, 34, "and was it not in thy name"),
        (35, 39, "that we cast out"),
        (40, 40, "devils,"),
        (41, 47, "and was it not in thy name"),
        (48, 51, "that we did"),
        (52, 55, "many marvelous works?"),
    ],
    23: [
        (0, 6, "And then will I declare"),
        (7, 10, "unto them:"),
        (11, 16, "I never knew you;"),
        (17, 21, "depart ye"),
        (22, 25, "from me,"),
        (26, 28, "ye who"),
        (29, 32, "do iniquity."),
    ],
    24: [
        (0, 1, "Therefore,"),
        (2, 7, "whoso hears"),
        (8, 11, "these my words"),
        (12, 15, "and does them,"),
        (16, 20, "I will liken him"),
        (21, 24, "unto a wise man,"),
        (25, 30, "who built his house"),
        (31, 35, "upon a rock—"),
    ],
    25: [
        (0, 4, "And the rain fell,"),
        (5, 8, "and the floods came,"),
        (9, 12, "and the winds blew,"),
        (13, 17, "and beat that house;"),
        (18, 22, "and it fell not,"),
        (23, 25, "for it was founded"),
        (26, 30, "upon a rock."),
    ],
    26: [
        (0, 7, "And all those who hear"),
        (8, 11, "these my words"),
        (12, 16, "and do them not,"),
        (17, 20, "shall be likened"),
        (21, 24, "unto a foolish man,"),
        (25, 30, "who built his house"),
        (31, 35, "upon the sand—"),
    ],
    27: [
        (0, 4, "And the rain fell,"),
        (5, 8, "and the floods flowed,"),
        (9, 12, "and the winds blew,"),
        (13, 17, "and beat that house;"),
        (18, 21, "and it fell,"),
        (22, 27, "and great was its fall."),
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
