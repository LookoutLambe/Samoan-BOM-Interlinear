"""Hand-curated TAM-phrase gloss overrides for Mosaea 16 — Abinadi concludes: the resurrection, redemption through Christ, and the fate of the wicked.

Follows GLOSSING_RULES.md and the no-injected-words rule: each cell's English
maps only to the Samoan words in that cell's span. TAM clusters atomic (rule 1),
subject `o ia` / agent `e ia` absorbed into the verb cluster, never split as a
bare "he" (rule 2), NP/PP atoms split (rule 3), `mai`-as-"from" (rule 7), no
anaphoric-`ai` fillers when a PP/object follows (rule 1), `mafai ona`/`ina ia`/
`ina ua` bound (rules 13/15), vocative `e`/`E …e` folded as "O X" (rule 12),
directional "forth" dropped (rule 12a). No pronoun/TAM word injected into a cell
whose span lacks that token; no content word repeats across adjacent cells
(except authentic Samoan doublings and correlatives).

To rebuild after editing:
    python3 build_overrides_mosiah16.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "mosiah"
CHAPTER_NUM = 16
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 4, "it came to pass"),
        (5, 8, "after had made an end"),
        (9, 10, "of speaking"),
        (11, 11, "Abinadi"),
        (12, 14, "these words"),
        (15, 19, "he stretched forth"),
        (20, 21, "his hand"),
        (22, 24, "and said:"),
        (25, 27, "shall come"),
        (28, 29, "the time"),
        (30, 34, "when shall see"),
        (35, 36, "all men"),
        (37, 39, "the salvation"),
        (40, 42, "of the Lord;"),
        (43, 45, "when it cometh"),
        (46, 48, "to every nation,"),
        (49, 49, "kindred,"),
        (50, 50, "tongue,"),
        (51, 52, "and people,"),
        (53, 54, "then shall see"),
        (55, 57, "themselves"),
        (58, 58, "and"),
        (59, 63, "shall confess"),
        (64, 68, "before God"),
        (69, 70, "that are just"),
        (71, 72, "his judgments."),
    ],
    2: [
        (0, 1, "And then"),
        (2, 4, "shall be driven"),
        (5, 6, "out"),
        (7, 9, "the wicked,"),
        (10, 15, "and there shall be"),
        (16, 17, "a cause"),
        (18, 23, "for which they shall howl,"),
        (24, 25, "and weep,"),
        (26, 27, "and wail,"),
        (28, 30, "and gnash"),
        (31, 33, "their teeth;"),
        (34, 36, "and now"),
        (37, 39, "because they"),
        (40, 42, "would not hearken"),
        (43, 45, "unto the voice"),
        (46, 48, "of the Lord;"),
        (49, 50, "therefore"),
        (51, 54, "redeemeth not"),
        (55, 56, "them"),
        (57, 59, "the Lord."),
    ],
    3: [
        (0, 3, "For they are carnal"),
        (4, 5, "and devilish,"),
        (6, 9, "and there is"),
        (10, 12, "in the devil"),
        (13, 14, "the power"),
        (15, 19, "over them;"),
        (20, 20, "yea,"),
        (21, 24, "even that old serpent"),
        (25, 28, "who did beguile"),
        (29, 32, "our first parents,"),
        (33, 35, "which was the cause"),
        (36, 39, "of their fall;"),
        (40, 43, "which was the cause"),
        (44, 46, "whereby became"),
        (47, 48, "all men"),
        (49, 51, "carnal,"),
        (52, 52, "sensual,"),
        (53, 53, "devilish,"),
        (54, 57, "knowing the evil"),
        (58, 60, "from the good,"),
        (61, 63, "and yielding up"),
        (64, 66, "themselves"),
        (67, 68, "to be ruled"),
        (69, 71, "by the devil."),
    ],
    4: [
        (0, 1, "Thus"),
        (2, 4, "were lost"),
        (5, 7, "all men;"),
        (8, 9, "and behold,"),
        (10, 14, "they would be lost"),
        (15, 17, "endlessly,"),
        (18, 22, "were it not that redeemed"),
        (23, 25, "God"),
        (26, 27, "his people"),
        (28, 32, "from their lost state"),
        (33, 35, "and fallen."),
    ],
    5: [
        (0, 2, "But remember"),
        (3, 7, "that he that continueth"),
        (8, 12, "in his own carnal nature,"),
        (13, 16, "and goeth on"),
        (17, 18, "in the ways"),
        (19, 21, "of sin"),
        (22, 24, "and rebellion"),
        (25, 28, "against God,"),
        (29, 31, "remaineth"),
        (32, 35, "in his fallen state"),
        (36, 39, "and there is"),
        (40, 42, "in the devil"),
        (43, 45, "all the power"),
        (46, 48, "over him."),
        (49, 50, "Therefore"),
        (51, 53, "it is as if"),
        (54, 56, "was made not"),
        (57, 58, "a redemption"),
        (59, 60, "for him,"),
        (61, 65, "for he is become"),
        (66, 67, "an enemy"),
        (68, 70, "to God;"),
        (71, 75, "and also the devil"),
        (76, 78, "is an enemy"),
        (79, 81, "to God."),
    ],
    6: [
        (0, 2, "And now"),
        (3, 5, "if it were that"),
        (6, 9, "had not come"),
        (10, 10, "Christ"),
        (11, 13, "into the world,"),
        (14, 16, "speaking concerning"),
        (17, 18, "things"),
        (19, 23, "which are to come"),
        (24, 25, "as if"),
        (26, 30, "already had come,"),
        (31, 33, "then there is no"),
        (34, 35, "redemption."),
    ],
    7: [
        (0, 3, "And if it were that"),
        (4, 7, "had not risen"),
        (8, 8, "Christ"),
        (9, 12, "from the dead,"),
        (13, 17, "or he have broken"),
        (18, 21, "the bands of death"),
        (22, 25, "that should not triumph"),
        (26, 27, "the grave,"),
        (28, 31, "and that there be no"),
        (32, 33, "sting"),
        (34, 36, "of death,"),
        (37, 39, "then there is no"),
        (40, 41, "resurrection."),
    ],
    8: [
        (0, 3, "But there is"),
        (4, 5, "a resurrection,"),
        (6, 7, "therefore"),
        (8, 10, "there is no"),
        (11, 12, "victory"),
        (13, 15, "in the grave,"),
        (16, 19, "and the sting"),
        (20, 22, "of death"),
        (23, 24, "is swallowed up"),
        (25, 27, "in Christ."),
    ],
    9: [
        (0, 1, "He is"),
        (2, 4, "the light"),
        (5, 7, "and the life"),
        (8, 10, "of the world;"),
        (11, 11, "yea,"),
        (12, 14, "a light"),
        (15, 17, "that is endless,"),
        (18, 22, "that can never"),
        (23, 23, "be darkened;"),
        (24, 24, "yea,"),
        (25, 28, "and also a life"),
        (29, 31, "that is endless,"),
        (32, 34, "that cannot"),
        (35, 38, "there be any more"),
        (39, 40, "death."),
    ],
    10: [
        (0, 2, "Even"),
        (3, 5, "this mortal body"),
        (6, 9, "shall be clothed"),
        (10, 14, "with the immortal body,"),
        (15, 19, "and this corruptible body"),
        (20, 23, "shall be clothed"),
        (24, 28, "with the incorruptible body,"),
        (29, 33, "and shall be brought"),
        (34, 35, "to stand"),
        (36, 41, "before the judgment-seat"),
        (42, 44, "of God,"),
        (45, 46, "to be judged"),
        (47, 48, "of him"),
        (49, 51, "according to"),
        (52, 54, "their works"),
        (55, 56, "whether good"),
        (57, 58, "or evil."),
    ],
    11: [
        (0, 2, "If be good"),
        (3, 5, "their works,"),
        (6, 8, "they rise"),
        (9, 11, "to life"),
        (12, 14, "and happiness"),
        (15, 17, "endless;"),
        (18, 21, "and if be evil"),
        (22, 24, "their works,"),
        (25, 27, "they rise"),
        (28, 30, "to damnation"),
        (31, 33, "endless,"),
        (34, 37, "for are delivered up"),
        (38, 39, "them"),
        (40, 42, "to the devil,"),
        (43, 46, "who hath power"),
        (47, 50, "over them,"),
        (51, 54, "which is damnation—"),
    ],
    12: [
        (0, 2, "For went"),
        (3, 4, "they"),
        (5, 7, "according to"),
        (8, 11, "their own hearts"),
        (12, 14, "and carnal desires;"),
        (15, 21, "for they never called"),
        (22, 24, "upon the Lord"),
        (25, 27, "while were extended"),
        (28, 32, "the arms of mercy"),
        (33, 36, "towards them;"),
        (37, 40, "for were extended"),
        (41, 44, "unto them"),
        (45, 49, "the arms of mercy,"),
        (50, 54, "but they would not"),
        (55, 56, "desire it;"),
        (57, 58, "were warned"),
        (59, 60, "they"),
        (61, 62, "concerning"),
        (63, 65, "their iniquities"),
        (66, 70, "but they would not"),
        (71, 74, "depart therefrom;"),
        (75, 77, "and were commanded"),
        (78, 79, "they"),
        (80, 81, "to repent"),
        (82, 86, "but they would not"),
        (87, 87, "repent."),
    ],
    13: [
        (0, 2, "And now,"),
        (3, 7, "ought it not"),
        (8, 10, "that ye tremble"),
        (11, 12, "and repent"),
        (13, 16, "of your sins,"),
        (17, 18, "and remember"),
        (19, 22, "that only Christ"),
        (23, 25, "can"),
        (26, 28, "save you?"),
    ],
    14: [
        (0, 1, "Therefore,"),
        (2, 6, "if ye teach"),
        (7, 10, "the law of Moses,"),
        (11, 14, "teach ye also"),
        (15, 18, "that it is a shadow"),
        (19, 20, "of things"),
        (21, 25, "which are to come—"),
    ],
    15: [
        (0, 2, "Teach"),
        (3, 4, "them"),
        (5, 7, "the redemption"),
        (8, 10, "cometh through"),
        (11, 13, "Christ"),
        (14, 15, "the Lord,"),
        (16, 19, "he is the very same"),
        (20, 23, "the Eternal Father."),
        (24, 24, "Amen."),
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
