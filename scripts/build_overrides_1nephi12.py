"""Hand-curated TAM-phrase gloss overrides for 1 Nifae 12."""
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 12
ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"

VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass"),
        (4, 5, "spake"),
        (6, 7, "the angel"),
        (8, 10, "unto me:"),
        (11, 12, "Look!"),
        (13, 14, "and behold"),
        (15, 17, "thy seed,"),
        (18, 20, "and the seed also"),
        (21, 23, "of thy brothers."),
        (24, 27, "And I looked"),
        (28, 30, "and beheld"),
        (31, 32, "the land"),
        (33, 35, "of promise;"),
        (36, 40, "and I beheld"),
        (41, 41, "multitudes"),
        (42, 43, "of people,"),
        (44, 44, "yea,"),
        (45, 46, "as if"),
        (47, 48, "were equal"),
        (49, 51, "their multitude"),
        (52, 53, "to the sands"),
        (54, 56, "of the sea."),
    ],
    2: [
        (0, 3, "And it came to pass"),
        (4, 6, "I beheld"),
        (7, 9, "were gathered together"),
        (10, 12, "multitudes"),
        (13, 14, "to battle,"),
        (15, 17, "the one"),
        (18, 19, "against"),
        (20, 22, "the other;"),
        (23, 26, "and I saw"),
        (27, 28, "wars,"),
        (29, 32, "and rumors of wars,"),
        (33, 35, "and great slaughters"),
        (36, 38, "with the sword"),
        (39, 43, "among my people."),
    ],
    3: [
        (0, 3, "And it came to pass"),
        (4, 5, "I beheld"),
        (6, 8, "had passed"),
        (9, 11, "many generations"),
        (12, 15, "according to"),
        (16, 16, "wars"),
        (17, 18, "and contentions"),
        (19, 21, "in the land;"),
        (22, 25, "and I beheld"),
        (26, 29, "many cities,"),
        (30, 30, "yea,"),
        (31, 34, "exceedingly great,"),
        (35, 38, "I could not"),
        (39, 40, "number"),
        (41, 42, "them."),
    ],
    4: [
        (0, 3, "And it came to pass"),
        (4, 5, "I beheld"),
        (6, 11, "a mist of darkness"),
        (12, 19, "upon the face of the land of promise;"),
        (20, 23, "and I saw"),
        (24, 25, "lightnings,"),
        (26, 31, "and I heard thunderings,"),
        (32, 33, "and earthquakes,"),
        (34, 39, "and all manner of tumultuous noises;"),
        (40, 43, "and I saw"),
        (44, 48, "the earth and the rocks,"),
        (49, 52, "they were rent;"),
        (53, 56, "and I beheld"),
        (57, 58, "mountains"),
        (59, 63, "tumbling into pieces;"),
        (64, 67, "and I beheld"),
        (68, 73, "the plains of the earth,"),
        (74, 77, "they were broken up;"),
        (78, 81, "and I beheld"),
        (82, 85, "many cities"),
        (86, 88, "were sunk down;"),
        (89, 92, "and I beheld"),
        (93, 95, "many"),
        (96, 100, "were burned with fire;"),
        (101, 104, "and I beheld"),
        (105, 107, "many"),
        (108, 113, "fell to the earth,"),
        (114, 115, "because of"),
        (116, 118, "the great quaking thereof."),
    ],
    5: [
        (0, 3, "And it came to pass"),
        (4, 6, "after"),
        (7, 8, "I had seen"),
        (9, 11, "these things,"),
        (12, 14, "I saw"),
        (15, 19, "the mist of darkness,"),
        (20, 23, "had gone away"),
        (24, 28, "from off the face of the earth;"),
        (29, 30, "and behold,"),
        (31, 33, "I saw"),
        (34, 36, "multitudes"),
        (37, 41, "who had not fallen"),
        (42, 47, "because of the great and terrible"),
        (48, 52, "judgments of the Lord."),
    ],
    6: [
        (0, 3, "And I beheld"),
        (4, 7, "were opened the heavens,"),
        (8, 14, "and the Lamb of God"),
        (15, 20, "came down from heaven;"),
        (21, 26, "and he came down"),
        (27, 28, "below"),
        (29, 33, "and showed himself"),
        (34, 38, "unto them."),
    ],
    7: [
        (0, 6, "And I also saw and bear record"),
        (7, 9, "came down"),
        (10, 12, "the Holy Ghost"),
        (13, 18, "upon twelve others;"),
        (19, 23, "and they were ordained"),
        (24, 26, "of God,"),
        (27, 28, "and chosen."),
    ],
    8: [
        (0, 5, "And spake the angel"),
        (6, 8, "unto me,"),
        (9, 10, "saying:"),
        (11, 11, "Behold"),
        (12, 19, "the twelve disciples of the Lamb,"),
        (20, 23, "who are chosen"),
        (24, 26, "to minister"),
        (27, 29, "unto thy seed."),
    ],
    9: [
        (0, 5, "And said he"),
        (6, 8, "unto me:"),
        (9, 11, "rememberest thou"),
        (12, 18, "the twelve apostles of the Lamb?"),
        (19, 19, "Behold"),
        (20, 23, "they"),
        (24, 30, "are they who shall judge"),
        (31, 35, "the twelve tribes of Israel;"),
        (36, 39, "wherefore,"),
        (40, 43, "the twelve ministers"),
        (44, 46, "of thy seed"),
        (47, 50, "shall be judged"),
        (51, 53, "by them;"),
        (54, 56, "for ye"),
        (57, 61, "are of the house of Israel."),
    ],
    10: [
        (0, 5, "And these twelve ministers"),
        (6, 14, "whom thou beholdest"),
        (15, 18, "shall judge"),
        (19, 20, "thy seed."),
        (21, 22, "And, behold,"),
        (23, 26, "they are righteous"),
        (27, 28, "forever;"),
        (29, 34, "and because of their faith"),
        (35, 41, "in the Lamb of God"),
        (42, 47, "are washed their garments"),
        (48, 50, "in his blood."),
    ],
    11: [
        (0, 5, "And spake the angel"),
        (6, 8, "unto me:"),
        (9, 10, "Look!"),
        (11, 14, "And I looked,"),
        (15, 17, "and beheld"),
        (18, 20, "three generations"),
        (21, 26, "had passed away in righteousness;"),
        (27, 29, "and were white"),
        (30, 32, "their garments"),
        (33, 35, "like"),
        (36, 39, "the Lamb"),
        (40, 42, "of God."),
        (43, 48, "And spake the angel"),
        (49, 51, "unto me:"),
        (52, 55, "are made white"),
        (56, 56, "these"),
        (57, 62, "in the blood of the Lamb,"),
        (63, 68, "because of their faith"),
        (69, 71, "in him."),
    ],
    12: [
        (0, 2, "And I,"),
        (3, 4, "Nephi,"),
        (5, 8, "saw also"),
        (9, 11, "the many"),
        (12, 16, "of the fourth generation"),
        (17, 21, "who had passed away"),
        (22, 24, "in righteousness."),
    ],
    13: [
        (0, 3, "And it came to pass"),
        (4, 5, "I beheld"),
        (6, 9, "the multitudes"),
        (10, 12, "of the world"),
        (13, 15, "were gathered together."),
    ],
    14: [
        (0, 3, "And spake"),
        (4, 5, "the angel"),
        (6, 8, "unto me:"),
        (9, 9, "Behold"),
        (10, 12, "thy seed,"),
        (13, 15, "and the seed also"),
        (16, 18, "of thy brothers."),
    ],
    15: [
        (0, 3, "And it came to pass"),
        (4, 8, "I beheld"),
        (9, 12, "the people of my seed"),
        (13, 15, "were gathered together"),
        (16, 19, "in multitudes"),
        (20, 21, "against"),
        (22, 26, "the seed of my brothers;"),
        (27, 31, "and they were gathered together"),
        (32, 33, "to battle."),
    ],
    16: [
        (0, 5, "And spake the angel"),
        (6, 8, "unto me,"),
        (9, 10, "saying:"),
        (11, 11, "Behold"),
        (12, 17, "the fountain of filthy water"),
        (18, 23, "which saw thy father;"),
        (24, 24, "yea,"),
        (25, 28, "even the river"),
        (29, 33, "of which he spake;"),
        (34, 37, "and the depths thereof,"),
        (38, 42, "are the depths of hell."),
    ],
    17: [
        (0, 5, "And the mists of darkness"),
        (6, 11, "are the temptations of the devil,"),
        (12, 16, "which blindeth the eyes,"),
        (17, 25, "and hardeneth the hearts of the children of men,"),
        (26, 32, "and leadeth them away"),
        (33, 35, "into broad roads,"),
        (36, 41, "they perish and are lost."),
    ],
    18: [
        (0, 7, "And the great and spacious building,"),
        (8, 14, "which saw thy father,"),
        (15, 21, "are vain imaginations and pride"),
        (22, 26, "of the children of men."),
        (27, 32, "And was divided them"),
        (33, 39, "in a great and terrible gulf;"),
        (40, 40, "yea,"),
        (41, 45, "even the word"),
        (46, 52, "of the justice of the Eternal God,"),
        (53, 55, "and the Messiah"),
        (56, 64, "who is the Lamb of God,"),
        (65, 73, "of whom hath testified the Holy Ghost,"),
        (74, 79, "from the beginning of the world"),
        (80, 86, "until this present time,"),
        (87, 92, "and from this time"),
        (93, 97, "until forever."),
    ],
    19: [
        (0, 8, "And as spake the angel these words,"),
        (9, 14, "I beheld"),
        (15, 18, "the seed of my brothers"),
        (19, 24, "did contend against my seed,"),
        (25, 32, "according to the word of the angel;"),
        (33, 40, "and because of the pride of my seed,"),
        (41, 45, "and the temptations of the devil,"),
        (46, 48, "I beheld"),
        (49, 51, "overpowered"),
        (52, 56, "the seed of my brothers"),
        (57, 62, "them, my seed."),
    ],
    20: [
        (0, 3, "And it came to pass"),
        (4, 5, "I beheld,"),
        (6, 8, "and I saw"),
        (9, 15, "the people of the seed of my brothers"),
        (16, 21, "they had overcome my seed;"),
        (22, 26, "and they went"),
        (27, 31, "in multitudes"),
        (32, 36, "upon the face of the land."),
    ],
    21: [
        (0, 4, "And I beheld"),
        (5, 8, "them"),
        (9, 11, "were gathered together"),
        (12, 15, "in multitudes;"),
        (16, 19, "and I saw"),
        (20, 21, "wars"),
        (22, 25, "and rumors of wars"),
        (26, 30, "among them;"),
        (31, 34, "and I saw"),
        (35, 39, "many generations"),
        (40, 42, "had passed away"),
        (43, 48, "amid wars and rumors of wars."),
    ],
    22: [
        (0, 5, "And spake the angel"),
        (6, 8, "unto me:"),
        (9, 9, "Behold"),
        (10, 13, "these"),
        (14, 17, "shall dwindle"),
        (18, 21, "in unbelief."),
    ],
    23: [
        (0, 3, "And it came to pass"),
        (4, 6, "I beheld,"),
        (7, 11, "after had dwindled"),
        (12, 14, "them"),
        (15, 18, "in unbelief,"),
        (19, 22, "they became"),
        (23, 25, "a dark people,"),
        (26, 27, "and loathsome,"),
        (28, 29, "and filthy,"),
        (30, 32, "full of"),
        (33, 34, "idleness"),
        (35, 40, "and all manner of abominations."),
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
