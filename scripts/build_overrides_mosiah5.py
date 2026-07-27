"""Hand-curated TAM-phrase gloss overrides for Mosaea 5 — the people covenant to take upon them the name of Christ.

Follows GLOSSING_RULES.md and the no-injected-words rule: each cell's English
maps only to the Samoan words in that cell's span. TAM clusters atomic (rule 1),
pronouns absorbed only when their token is IN the span (rule 2), NP/PP atoms
split (rule 3), `mai`-as-"from" (rule 7), no anaphoric-`ai` fillers when a
PP/object follows (rule 1), `mafai ona`/`ina ia`/`ina ua` bound (rules 13/15),
vocative `e`/`E …e` folded as "O X" (rule 12), directional "forth" dropped
(rule 12a). No pronoun/TAM word injected into a cell whose span lacks that
token; no content word repeats across adjacent cells (except authentic Samoan
doublings and correlatives).

To rebuild after editing:
    python3 build_overrides_mosiah5.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "mosiah"
CHAPTER_NUM = 5
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "it came to pass"),
        (5, 8, "after had made an end"),
        (9, 11, "of thus speaking"),
        (12, 15, "king Benjamin"),
        (16, 18, "to his people,"),
        (19, 23, "he sent"),
        (24, 25, "messengers"),
        (26, 27, "among"),
        (28, 31, "them,"),
        (32, 36, "desiring to know"),
        (37, 38, "his people"),
        (39, 42, "if they believed"),
        (43, 44, "the words"),
        (45, 49, "which he had spoken"),
        (50, 53, "unto them."),
    ],
    2: [
        (0, 0, "And"),
        (1, 5, "they all cried"),
        (6, 10, "with one voice,"),
        (11, 12, "saying:"),
        (13, 13, "Yea,"),
        (14, 16, "we believe"),
        (17, 19, "all the words"),
        (20, 24, "which thou hast spoken"),
        (25, 28, "unto us;"),
        (29, 31, "and also,"),
        (32, 34, "we know"),
        (35, 37, "their surety"),
        (38, 40, "and truth,"),
        (41, 44, "because of the Spirit"),
        (45, 49, "of the Lord Omnipotent,"),
        (50, 53, "which hath wrought"),
        (54, 56, "a mighty change"),
        (57, 61, "in us,"),
        (62, 65, "or in"),
        (66, 69, "our hearts,"),
        (70, 74, "that there is no more"),
        (75, 77, "our disposition"),
        (78, 81, "to do evil,"),
        (82, 82, "but"),
        (83, 86, "to do good"),
        (87, 89, "continually."),
    ],
    3: [
        (0, 3, "And we ourselves"),
        (4, 5, "also,"),
        (6, 10, "have great views"),
        (11, 12, "of that"),
        (13, 17, "which is to come,"),
        (18, 22, "through the goodness"),
        (23, 24, "infinite"),
        (25, 27, "of God,"),
        (28, 29, "and the manifestations"),
        (30, 32, "of his Spirit;"),
        (33, 37, "and were it expedient,"),
        (38, 42, "we could prophesy"),
        (43, 47, "of all things."),
    ],
    4: [
        (0, 3, "And it is the faith"),
        (4, 8, "which we have had"),
        (9, 12, "concerning the things"),
        (13, 16, "which hath spoken"),
        (17, 19, "our king"),
        (20, 23, "unto us"),
        (24, 28, "that hath brought us"),
        (29, 32, "to this great knowledge,"),
        (33, 34, "whereby"),
        (35, 38, "are made greatly glad"),
        (39, 40, "we"),
        (41, 45, "with exceeding great joy."),
    ],
    5: [
        (0, 3, "And we are willing"),
        (4, 6, "to enter"),
        (7, 9, "into a covenant"),
        (10, 13, "with our God"),
        (14, 17, "to do his will,"),
        (18, 19, "and be obedient"),
        (20, 22, "to his commandments"),
        (23, 25, "in all things"),
        (26, 32, "which he commandeth us,"),
        (33, 37, "in all our days"),
        (38, 39, "remaining,"),
        (40, 41, "that"),
        (42, 44, "we bring not"),
        (45, 49, "upon ourselves"),
        (50, 51, "a torment"),
        (52, 54, "never-ending,"),
        (55, 60, "as hath been spoken"),
        (61, 62, "the angel,"),
        (63, 64, "that"),
        (65, 67, "we drink not"),
        (68, 70, "out of the cup"),
        (71, 73, "of the wrath"),
        (74, 76, "of God."),
    ],
    6: [
        (0, 2, "And now,"),
        (3, 5, "these are the words"),
        (6, 9, "which desired"),
        (10, 13, "king Benjamin"),
        (14, 18, "of them;"),
        (19, 21, "and therefore"),
        (22, 27, "he said"),
        (28, 31, "unto them:"),
        (32, 35, "Ye have spoken"),
        (36, 36, "the words"),
        (37, 41, "that I desired;"),
        (42, 45, "and the covenant"),
        (46, 48, "which ye have made"),
        (49, 52, "is a righteous covenant."),
    ],
    7: [
        (0, 2, "And now,"),
        (3, 6, "because of the covenant"),
        (7, 9, "which ye have made,"),
        (10, 14, "ye shall be called"),
        (15, 15, "ye"),
        (16, 20, "the children of Christ,"),
        (21, 23, "his sons,"),
        (24, 26, "and his daughters;"),
        (27, 28, "for behold,"),
        (29, 31, "this day"),
        (32, 36, "he hath begotten"),
        (37, 37, "you"),
        (38, 38, "spiritually;"),
        (39, 43, "for ye say"),
        (44, 45, "are changed"),
        (46, 48, "your hearts"),
        (49, 53, "through faith"),
        (54, 56, "on his name;"),
        (57, 58, "therefore,"),
        (59, 62, "ye are born"),
        (63, 64, "of him"),
        (65, 69, "and have become"),
        (70, 72, "his sons"),
        (73, 75, "and his daughters."),
    ],
    8: [
        (0, 2, "And under"),
        (3, 5, "this head"),
        (6, 9, "ye are made free,"),
        (10, 10, "and"),
        (11, 16, "there is no other head"),
        (17, 21, "whereby can be made free"),
        (22, 22, "you."),
        (23, 25, "There is no"),
        (26, 28, "other name"),
        (29, 31, "given"),
        (32, 34, "whereby can"),
        (35, 37, "come"),
        (38, 39, "salvation;"),
        (40, 41, "therefore,"),
        (42, 45, "I desire"),
        (46, 48, "that ye take"),
        (49, 52, "upon you"),
        (53, 54, "the name"),
        (55, 56, "of Christ,"),
        (57, 58, "all you"),
        (59, 61, "that have entered"),
        (62, 64, "into the covenant"),
        (65, 67, "with God"),
        (68, 72, "that ye should be obedient"),
        (73, 74, "even unto"),
        (75, 77, "the end"),
        (78, 81, "of your lives."),
    ],
    9: [
        (0, 0, "And"),
        (1, 5, "it shall come to pass,"),
        (6, 10, "whosoever doeth"),
        (11, 12, "this thing,"),
        (13, 18, "he shall sit"),
        (19, 22, "at the right hand"),
        (23, 25, "of God,"),
        (26, 32, "for he shall know"),
        (33, 34, "the name"),
        (35, 39, "by which shall be called"),
        (40, 41, "he;"),
        (42, 48, "for he shall be called"),
        (49, 51, "by the name"),
        (52, 53, "of Christ."),
    ],
    10: [
        (0, 3, "And now also,"),
        (4, 8, "it shall come to pass,"),
        (9, 11, "whosoever"),
        (12, 14, "taketh not"),
        (15, 17, "upon him"),
        (18, 19, "the name"),
        (20, 21, "of Christ"),
        (22, 25, "shall be called"),
        (26, 29, "by some other name;"),
        (30, 31, "therefore,"),
        (32, 37, "he shall find"),
        (38, 40, "himself"),
        (41, 44, "on the left hand"),
        (45, 47, "of God."),
    ],
    11: [
        (0, 3, "And I desire"),
        (4, 7, "that ye remember also,"),
        (8, 11, "this is the name"),
        (12, 15, "that I said"),
        (16, 20, "I should give"),
        (21, 23, "unto you"),
        (24, 28, "that never should"),
        (29, 29, "be blotted out,"),
        (30, 34, "except through transgression;"),
        (35, 36, "therefore,"),
        (37, 40, "take heed"),
        (41, 44, "that ye transgress not,"),
        (45, 48, "that be not blotted out"),
        (49, 50, "the name"),
        (51, 54, "out of your hearts."),
    ],
    12: [
        (0, 3, "I say"),
        (4, 6, "unto you,"),
        (7, 9, "I desire"),
        (10, 12, "that ye remember"),
        (13, 16, "to retain the name"),
        (17, 19, "written always"),
        (20, 23, "in your hearts,"),
        (24, 25, "that"),
        (26, 28, "ye be not found"),
        (29, 32, "on the left hand"),
        (33, 35, "of God,"),
        (36, 36, "but"),
        (37, 39, "that ye hear"),
        (40, 41, "and know"),
        (42, 43, "the voice"),
        (44, 48, "by which shall be called"),
        (49, 49, "ye,"),
        (50, 53, "and also the name,"),
        (54, 61, "by which he shall call you."),
    ],
    13: [
        (0, 0, "For"),
        (1, 4, "how knoweth"),
        (5, 7, "a man"),
        (8, 9, "the master"),
        (10, 16, "whom he hath not served,"),
        (17, 19, "and who is"),
        (20, 22, "a stranger"),
        (23, 25, "unto him,"),
        (26, 29, "and is far off"),
        (30, 31, "from the thoughts"),
        (32, 33, "and intents"),
        (34, 36, "of his heart?"),
    ],
    14: [
        (0, 2, "And again also,"),
        (3, 5, "doth take"),
        (6, 8, "a man"),
        (9, 10, "an ass"),
        (11, 14, "which belongeth to his neighbor,"),
        (15, 16, "and keep"),
        (17, 19, "him?"),
        (20, 23, "I say"),
        (24, 26, "unto you,"),
        (27, 28, "Nay;"),
        (29, 34, "he will not suffer"),
        (35, 36, "him,"),
        (37, 40, "that he feed among"),
        (41, 43, "his flocks,"),
        (44, 48, "but will drive away"),
        (49, 50, "him,"),
        (51, 52, "and drive"),
        (53, 54, "him"),
        (55, 56, "out."),
        (57, 60, "I say"),
        (61, 63, "unto you,"),
        (64, 68, "even so shall it be"),
        (69, 73, "among you"),
        (74, 75, "if"),
        (76, 79, "ye know not"),
        (80, 81, "the name"),
        (82, 85, "by which ye are called."),
    ],
    15: [
        (0, 1, "Therefore,"),
        (2, 5, "I desire"),
        (6, 8, "that ye be steadfast"),
        (9, 11, "and immovable,"),
        (12, 13, "and abounding"),
        (14, 16, "always"),
        (17, 19, "in good works,"),
        (20, 21, "that"),
        (22, 23, "may"),
        (24, 25, "seal you"),
        (26, 27, "Christ,"),
        (28, 31, "the Lord God"),
        (32, 33, "Omnipotent,"),
        (34, 36, "to be his,"),
        (37, 38, "that"),
        (39, 40, "may"),
        (41, 43, "be brought you"),
        (44, 46, "to heaven,"),
        (47, 48, "that"),
        (49, 50, "may"),
        (51, 52, "ye have"),
        (53, 57, "everlasting salvation"),
        (58, 62, "and eternal life,"),
        (63, 67, "through the wisdom,"),
        (68, 70, "and power,"),
        (71, 73, "and justice,"),
        (74, 77, "and tender mercy"),
        (78, 79, "of him"),
        (80, 83, "who created"),
        (84, 85, "all things,"),
        (86, 88, "in heaven"),
        (89, 91, "and in earth,"),
        (92, 96, "who is God"),
        (97, 99, "of all things."),
        (100, 100, "Amen."),
    ],
}


def build_words(source_words, spec):
    next_expected = 0
    for s, e, _ in spec:
        if s != next_expected: raise ValueError(f"gap at {s} expected {next_expected}")
        if e < s or e >= len(source_words): raise ValueError(f"bad range {s}..{e} src len {len(source_words)}")
        next_expected = e + 1
    if next_expected != len(source_words): raise ValueError(f"spec ends at {next_expected} src has {len(source_words)}")
    out = []
    for s, e, g in spec:
        for i in range(s, e): out.append({"sm": source_words[i]["sm"], "en": "·"})
        out.append({"sm": source_words[e]["sm"], "en": g})
    return out


def main():
    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    book = next(b for b in books["books"] if b["id"] == BOOK_ID)
    chapter = next(c for c in book["chapters"] if c["num"] == CHAPTER_NUM)
    existing = {"version": 1, "verses": {}}
    if OVERRIDES_PATH.exists():
        existing = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    n = 0
    for v in chapter["verses"]:
        spec = VERSE_SPECS.get(v["num"])
        if not spec: continue
        try:
            existing["verses"][f"{BOOK_ID}|{CHAPTER_NUM}|{v['num']}"] = build_words(v["words"], spec)
            n += 1
        except ValueError as exc:
            print(f"v{v['num']}: {exc}", file=sys.stderr); sys.exit(1)
    OVERRIDES_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {n} verse overrides to {OVERRIDES_PATH}")


if __name__ == "__main__":
    main()
