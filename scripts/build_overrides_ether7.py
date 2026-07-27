"""
Hand-curated TAM-phrase gloss overrides for Eteru (Ether) 7 — the reign of the early
Jaredite kings: Orihah, then his son Kib; Corihor rebels and takes his father captive,
but Kib begets Shule in captivity; Shule makes swords, restores the kingdom to his
father, and reigns. Corihor's son Noah rebels, captures Shule and part of the kingdom,
but Shule's sons slay Noah and restore their father. Prophets come among the people to
warn of judgments; the people repent and the land has peace.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: atomic 2-5 token
cells (TAM clusters 1, subject `o ia`/agent `e ia` absorbed 2, NP/PP atoms
split 3, `mai`-as-"from" 7, idioms 9, em-dash splits 11, `mafai ona`/`ina ia`/
`e tatau ona` bound 13/15, vocative 12). `o le a` stays atomic and is never
fused with a following `se X` NP; cells go past 5 only for rule-2 (absorbed
subject) or rule-7 (`o le a` + verb + directional) clusters.

    python3 build_overrides_ether7.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "ether"
CHAPTER_NUM = 7

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 4, "administered"),
        (5, 6, "Orihah"),
        (7, 10, "judgment in righteousness"),
        (11, 15, "upon the land"),
        (16, 19, "all his days,"),
        (20, 22, "whose days"),
        (23, 26, "were exceeding many."),
    ],
    2: [
        (0, 4, "And he begat"),
        (5, 7, "sons and daughters;"),
        (8, 8, "yea,"),
        (9, 11, "he begat"),
        (12, 14, "thirty"),
        (15, 17, "and one,"),
        (18, 20, "there were"),
        (21, 25, "among them"),
        (26, 27, "sons"),
        (28, 30, "twenty"),
        (31, 33, "and three."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he also begat"),
        (8, 8, "Kib"),
        (9, 13, "in his old age."),
        (14, 17, "And it came to pass that"),
        (18, 19, "Kib reigned"),
        (20, 24, "in his place;"),
        (25, 27, "and begat"),
        (28, 29, "Kib"),
        (30, 30, "Corihor."),
    ],
    4: [
        (0, 2, "And when"),
        (3, 7, "was thirty and two years"),
        (8, 9, "old was Corihor,"),
        (10, 13, "he did rebel"),
        (14, 16, "against his father,"),
        (17, 17, "and"),
        (18, 22, "he went forth"),
        (23, 24, "and dwelt"),
        (25, 29, "in the land of Nehor;"),
        (30, 34, "and he begat"),
        (35, 37, "sons and daughters,"),
        (38, 41, "and it came to pass that"),
        (42, 45, "they were exceeding fair;"),
        (46, 49, "wherefore"),
        (50, 53, "did draw away"),
        (54, 55, "Corihor"),
        (56, 58, "many people"),
        (59, 61, "to follow after"),
        (62, 64, "him."),
    ],
    5: [
        (0, 3, "And after that"),
        (4, 7, "he had assembled"),
        (8, 10, "an army,"),
        (11, 15, "he went up"),
        (16, 20, "unto the land of Moron"),
        (21, 24, "where dwelt"),
        (25, 26, "the king,"),
        (27, 30, "and took him"),
        (31, 31, "captive,"),
        (32, 35, "which fulfilled"),
        (36, 38, "the word of"),
        (39, 42, "the brother of Jared"),
        (43, 46, "they would be brought"),
        (47, 48, "them"),
        (49, 50, "into captivity."),
    ],
    6: [
        (0, 1, "Now"),
        (2, 6, "the land of Moron,"),
        (7, 10, "where dwelt"),
        (11, 12, "the king,"),
        (13, 17, "was near the land"),
        (18, 20, "which is called"),
        (21, 22, "Desolation"),
        (23, 25, "by the Nephites."),
    ],
    7: [
        (0, 3, "And it came to pass that"),
        (4, 5, "dwelt in captivity"),
        (6, 7, "Kib"),
        (8, 10, "and his people,"),
        (11, 15, "under the rule"),
        (16, 17, "of Corihor,"),
        (18, 19, "his son,"),
        (20, 22, "until"),
        (23, 26, "he grew very old;"),
        (27, 30, "nevertheless"),
        (31, 32, "begat"),
        (33, 34, "Kib"),
        (35, 36, "Shule"),
        (37, 39, "in the days"),
        (40, 42, "of his very old age,"),
        (43, 45, "while yet a captive"),
        (46, 47, "was he."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Shule was wroth"),
        (6, 8, "with his brother;"),
        (9, 13, "and waxed strong"),
        (14, 14, "Shule,"),
        (15, 18, "and became"),
        (19, 20, "exceeding strong"),
        (21, 23, "according to"),
        (24, 26, "the strength of"),
        (27, 29, "a grown man;"),
        (30, 34, "and also mighty"),
        (35, 36, "was he"),
        (37, 39, "in judgment."),
    ],
    9: [
        (0, 3, "Wherefore,"),
        (4, 9, "he went forth"),
        (10, 14, "to the hill Ephraim,"),
        (15, 17, "and did molt"),
        (18, 19, "the ore"),
        (20, 22, "out of the hill,"),
        (23, 25, "and did make"),
        (26, 26, "swords"),
        (27, 29, "out of steel"),
        (30, 32, "for them"),
        (33, 38, "whom he had drawn away"),
        (39, 41, "together with him;"),
        (42, 45, "and after that"),
        (46, 48, "he had armed"),
        (49, 51, "them"),
        (52, 53, "with swords,"),
        (54, 58, "he returned again"),
        (59, 63, "to the city of Nehor,"),
        (64, 66, "and fought with"),
        (67, 70, "his brother Corihor,"),
        (71, 75, "whereby he gained"),
        (76, 77, "the kingdom,"),
        (78, 80, "and gave back"),
        (81, 83, "to his father"),
        (84, 85, "Kib."),
    ],
    10: [
        (0, 2, "And now"),
        (3, 6, "because of the thing"),
        (7, 10, "which Shule did,"),
        (11, 15, "did bestow his father"),
        (16, 19, "upon him"),
        (20, 21, "the kingdom;"),
        (22, 23, "therefore"),
        (24, 26, "began"),
        (27, 30, "he to reign"),
        (31, 32, "in place"),
        (33, 35, "of his father."),
    ],
    11: [
        (0, 3, "And it came to pass that"),
        (4, 6, "he executed"),
        (7, 7, "judgment"),
        (8, 10, "in righteousness;"),
        (11, 14, "and he did enlarge"),
        (15, 16, "his kingdom"),
        (17, 21, "upon all the land,"),
        (22, 26, "for were very numerous"),
        (27, 27, "the people."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 5, "also begat"),
        (6, 7, "Shule"),
        (8, 10, "sons and daughters"),
        (11, 12, "many."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Corihor repented"),
        (6, 8, "of the multitude"),
        (9, 11, "of evils"),
        (12, 14, "which he had done;"),
        (15, 18, "wherefore"),
        (19, 22, "did grant"),
        (23, 24, "Shule"),
        (25, 27, "unto him"),
        (28, 29, "power"),
        (30, 32, "in his kingdom."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 5, "there were unto"),
        (6, 7, "Corihor"),
        (8, 10, "sons and daughters"),
        (11, 12, "many."),
        (13, 16, "And there was"),
        (17, 19, "among"),
        (20, 22, "Corihor's sons"),
        (23, 24, "one"),
        (25, 26, "who was called"),
        (27, 28, "Noah."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 5, "Noah did rebel"),
        (6, 7, "against Shule,"),
        (8, 9, "the king,"),
        (10, 13, "and also his father"),
        (14, 15, "Corihor,"),
        (16, 19, "and did draw away"),
        (20, 20, "Cohor,"),
        (21, 22, "his brother,"),
        (23, 26, "and all his brethren"),
        (27, 29, "and a multitude"),
        (30, 32, "of the people."),
    ],
    16: [
        (0, 4, "And he did battle"),
        (5, 6, "against Shule,"),
        (7, 8, "the king,"),
        (9, 13, "wherein he obtained"),
        (14, 15, "the land"),
        (16, 18, "which became"),
        (19, 22, "their first inheritance;"),
        (23, 27, "and he became"),
        (28, 29, "a king"),
        (30, 32, "over"),
        (33, 35, "that portion"),
        (36, 38, "of the land."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 7, "he contended again"),
        (8, 9, "with Shule,"),
        (10, 11, "the king;"),
        (12, 15, "and he seized"),
        (16, 16, "Shule,"),
        (17, 18, "the king,"),
        (19, 21, "and carried away captive"),
        (22, 23, "unto Moron."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 8, "as he would slay"),
        (9, 11, "him,"),
        (12, 14, "crept in"),
        (15, 17, "the sons of Shule"),
        (18, 22, "into the house of Noah"),
        (23, 25, "by night"),
        (26, 29, "and slew him,"),
        (30, 33, "and did break down"),
        (34, 35, "the door"),
        (36, 38, "of the prison"),
        (39, 42, "and brought forth"),
        (43, 45, "their father,"),
        (46, 49, "and set him"),
        (50, 54, "upon his throne"),
        (55, 58, "in his own kingdom."),
    ],
    19: [
        (0, 3, "Wherefore,"),
        (4, 6, "did establish"),
        (7, 11, "the son of Noah"),
        (12, 13, "his kingdom"),
        (14, 18, "in his place;"),
        (19, 22, "nevertheless"),
        (23, 27, "they no longer gained"),
        (28, 29, "power"),
        (30, 33, "over Shule"),
        (34, 35, "the king,"),
        (36, 40, "and did prosper"),
        (41, 43, "and waxed strong"),
        (44, 44, "the people"),
        (45, 49, "who were under"),
        (50, 52, "the reign"),
        (53, 56, "of Shule the king."),
    ],
    20: [
        (0, 2, "And was divided"),
        (3, 4, "the kingdom;"),
        (5, 8, "and there were"),
        (9, 12, "two kingdoms,"),
        (13, 17, "the kingdom of Shule,"),
        (18, 22, "and the kingdom of Cohor,"),
        (23, 26, "the son of Noah."),
    ],
    21: [
        (0, 2, "And did direct"),
        (3, 4, "Cohor,"),
        (5, 8, "the son of Noah,"),
        (9, 10, "his people,"),
        (11, 12, "to fight"),
        (13, 14, "against Shule,"),
        (15, 18, "in which battle"),
        (19, 22, "Shule prevailed"),
        (23, 26, "over them"),
        (27, 29, "and did slay"),
        (30, 30, "Cohor."),
    ],
    22: [
        (0, 2, "And now"),
        (3, 5, "there was"),
        (6, 9, "a son of Cohor"),
        (10, 11, "who was named"),
        (12, 13, "Nimrod;"),
        (14, 17, "and did give up"),
        (18, 19, "Nimrod"),
        (20, 23, "the kingdom of Cohor"),
        (24, 25, "unto Shule,"),
        (26, 29, "and Shule was pleased"),
        (30, 32, "with him;"),
        (33, 36, "wherefore"),
        (37, 41, "did bestow Shule"),
        (42, 44, "great favor"),
        (45, 47, "upon him,"),
        (48, 51, "and he acted"),
        (52, 56, "in the kingdom of Shule"),
        (57, 59, "according to"),
        (60, 61, "his desires."),
    ],
    23: [
        (0, 4, "And also in the reign"),
        (5, 6, "of Shule"),
        (7, 10, "there came"),
        (11, 11, "prophets"),
        (12, 16, "among the people,"),
        (17, 21, "who were sent"),
        (22, 24, "of the Lord,"),
        (25, 27, "and prophesying"),
        (28, 30, "the wickedness"),
        (31, 35, "and idolatry"),
        (36, 37, "of the people"),
        (38, 40, "did bring"),
        (41, 42, "a curse"),
        (43, 47, "upon the land,"),
        (48, 48, "and"),
        (49, 52, "should be destroyed"),
        (53, 54, "they"),
        (55, 57, "if they"),
        (58, 60, "repent not."),
    ],
    24: [
        (0, 3, "And it came to pass that"),
        (4, 5, "reviled the people"),
        (6, 9, "against the prophets,"),
        (10, 11, "and did mock"),
        (12, 15, "them."),
        (16, 19, "And it came to pass that"),
        (20, 20, "did execute"),
        (21, 25, "king Shule"),
        (26, 26, "judgment"),
        (27, 28, "against"),
        (29, 32, "them"),
        (33, 36, "who did revile"),
        (37, 40, "against the prophets."),
    ],
    25: [
        (0, 3, "And he did make"),
        (4, 5, "a law"),
        (6, 9, "in all the land,"),
        (10, 14, "wherein was given"),
        (15, 16, "power"),
        (17, 18, "unto the prophets"),
        (19, 23, "that they might go"),
        (24, 27, "whithersoever"),
        (28, 32, "they desired;"),
        (33, 36, "and this thing"),
        (37, 39, "did bring"),
        (40, 40, "the people"),
        (41, 43, "unto repentance."),
    ],
    26: [
        (0, 1, "And because"),
        (2, 4, "the people repented"),
        (5, 8, "of their iniquities"),
        (9, 13, "and their idolatries"),
        (14, 15, "therefore"),
        (16, 18, "did preserve"),
        (19, 20, "them"),
        (21, 23, "by the Lord,"),
        (24, 28, "and they began"),
        (29, 30, "again to prosper"),
        (31, 33, "in the land."),
        (34, 37, "And it came to pass that"),
        (38, 40, "begat Shule"),
        (41, 43, "sons and daughters"),
        (44, 48, "in his old age."),
    ],
    27: [
        (0, 3, "And no more"),
        (4, 5, "were there"),
        (6, 7, "wars"),
        (8, 11, "in the days of Shule;"),
        (12, 15, "and he remembered"),
        (16, 17, "the great things"),
        (18, 19, "which had done"),
        (20, 22, "the Lord"),
        (23, 25, "for his fathers"),
        (26, 28, "in the bringing"),
        (29, 31, "them"),
        (32, 34, "who sailed"),
        (35, 38, "over the great deep"),
        (39, 41, "unto the land"),
        (42, 43, "which was promised;"),
        (44, 47, "wherefore"),
        (48, 51, "he did execute"),
        (52, 52, "judgment"),
        (53, 55, "in righteousness"),
        (56, 59, "all his days."),
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
