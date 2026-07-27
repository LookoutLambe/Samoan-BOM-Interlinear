"""Hand-curated TAM-phrase gloss overrides for Mosaea 14 — Abinadi quotes Isaiah 53 (the Suffering Servant).

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
    python3 build_overrides_mosiah14.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "mosiah"
CHAPTER_NUM = 14
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "Yea,"),
        (1, 2, "even"),
        (3, 4, "Isaiah"),
        (5, 9, "doth not say:"),
        (10, 14, "Who hath believed"),
        (15, 18, "our report,"),
        (19, 21, "and to whom"),
        (22, 25, "is revealed"),
        (26, 30, "the arm of the Lord?"),
    ],
    2: [
        (0, 0, "For"),
        (1, 7, "he shall grow up"),
        (8, 10, "before him"),
        (11, 13, "as"),
        (14, 16, "a tender plant,"),
        (17, 19, "and as"),
        (20, 21, "a root"),
        (22, 24, "which springeth up"),
        (25, 28, "out of dry ground;"),
        (29, 32, "he hath no form"),
        (33, 36, "nor comeliness;"),
        (37, 40, "and when we see"),
        (41, 43, "him"),
        (44, 47, "there is no beauty"),
        (48, 51, "that we should desire"),
        (52, 54, "him."),
    ],
    3: [
        (0, 1, "He is despised"),
        (2, 5, "and rejected"),
        (6, 7, "of men;"),
        (8, 10, "a man"),
        (11, 12, "of sorrows,"),
        (13, 15, "and acquainted"),
        (16, 18, "with grief;"),
        (19, 23, "as it were hid away"),
        (24, 26, "our faces"),
        (27, 30, "from him;"),
        (31, 34, "he was despised,"),
        (35, 39, "and we esteemed not"),
        (40, 41, "him."),
    ],
    4: [
        (0, 2, "Surely"),
        (3, 6, "he hath borne"),
        (7, 9, "our griefs,"),
        (10, 11, "and carried"),
        (12, 14, "our sorrows;"),
        (15, 18, "yet we did esteem"),
        (19, 21, "him"),
        (22, 23, "stricken,"),
        (24, 25, "smitten"),
        (26, 28, "of God,"),
        (29, 31, "and afflicted."),
    ],
    5: [
        (0, 0, "But"),
        (1, 4, "he was wounded"),
        (5, 8, "for our transgressions,"),
        (9, 12, "he was bruised"),
        (13, 16, "for our iniquities;"),
        (17, 20, "was upon him"),
        (21, 22, "the chastisement"),
        (23, 26, "of our peace;"),
        (27, 30, "and with his stripes"),
        (31, 33, "are healed"),
        (34, 35, "we."),
    ],
    6: [
        (0, 3, "All we,"),
        (4, 7, "like sheep,"),
        (8, 10, "have gone astray;"),
        (11, 13, "we each"),
        (14, 16, "and have turned"),
        (17, 18, "each man"),
        (19, 22, "to his own way;"),
        (23, 25, "and hath laid"),
        (26, 28, "the Lord"),
        (29, 31, "on him"),
        (32, 32, "the iniquities"),
        (33, 36, "of us all."),
    ],
    7: [
        (0, 3, "He was oppressed,"),
        (4, 8, "and he was afflicted,"),
        (9, 14, "yet he opened not"),
        (15, 16, "his mouth;"),
        (17, 20, "he is brought"),
        (21, 26, "as a lamb"),
        (27, 28, "to the slaughter,"),
        (29, 32, "and as"),
        (33, 35, "a dumb sheep"),
        (36, 40, "before her shearers"),
        (41, 42, "so"),
        (43, 48, "he openeth not"),
        (49, 50, "his mouth."),
    ],
    8: [
        (0, 4, "He was taken"),
        (5, 7, "from prison"),
        (8, 11, "and from judgment;"),
        (12, 14, "and who"),
        (15, 18, "shall declare"),
        (19, 20, "his generation?"),
        (21, 21, "for"),
        (22, 26, "he was cut off"),
        (27, 29, "out of the land"),
        (30, 32, "of the living;"),
        (33, 33, "for"),
        (34, 37, "he was stricken"),
        (38, 39, "for the transgressions"),
        (40, 42, "of my people."),
    ],
    9: [
        (0, 4, "And he made"),
        (5, 6, "his grave"),
        (7, 10, "with the wicked,"),
        (11, 12, "and with"),
        (13, 15, "the rich"),
        (16, 18, "in his death;"),
        (19, 19, "because"),
        (20, 24, "he had done not"),
        (25, 27, "any evil,"),
        (28, 31, "neither was there"),
        (32, 33, "deceit"),
        (34, 36, "in his mouth."),
    ],
    10: [
        (0, 2, "Yet it pleased"),
        (3, 4, "the Lord"),
        (5, 6, "to bruise"),
        (7, 8, "him;"),
        (9, 11, "he hath put"),
        (12, 13, "him"),
        (14, 15, "to grief;"),
        (16, 19, "when thou shalt make"),
        (20, 21, "his soul"),
        (22, 24, "an offering"),
        (25, 26, "for sin,"),
        (27, 32, "he shall see"),
        (33, 35, "his seed,"),
        (36, 40, "he shall prolong"),
        (41, 42, "his days,"),
        (43, 43, "and"),
        (44, 47, "shall prosper"),
        (48, 52, "the pleasure of the Lord"),
        (53, 55, "in his hand."),
    ],
    11: [
        (0, 5, "He shall see"),
        (6, 8, "the travail"),
        (9, 11, "of his soul,"),
        (12, 16, "and shall be satisfied"),
        (17, 18, "therein;"),
        (19, 21, "by his knowledge"),
        (22, 26, "shall justify"),
        (27, 30, "my righteous servant"),
        (31, 32, "many;"),
        (33, 33, "for"),
        (34, 39, "he shall bear"),
        (40, 42, "their iniquities."),
    ],
    12: [
        (0, 1, "Therefore"),
        (2, 8, "will I divide"),
        (9, 11, "unto him"),
        (12, 13, "a portion"),
        (14, 15, "with"),
        (16, 18, "the great,"),
        (19, 19, "and"),
        (20, 24, "he shall divide"),
        (25, 26, "the spoil"),
        (27, 28, "with"),
        (29, 30, "the strong;"),
        (31, 31, "because"),
        (32, 36, "he hath poured out"),
        (37, 38, "his soul"),
        (39, 43, "unto death;"),
        (44, 48, "and he was numbered"),
        (49, 50, "with"),
        (51, 52, "the transgressors;"),
        (53, 56, "and he bare"),
        (57, 57, "the sins"),
        (58, 60, "of many,"),
        (61, 62, "and made"),
        (63, 64, "intercession"),
        (65, 67, "for the transgressors."),
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
