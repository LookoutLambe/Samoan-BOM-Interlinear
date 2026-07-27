"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 35 — the conclusion
of the mission to the Zoramites: the word confounds them, the penitent are
cast out and received by the people of Ammon in Jershon, the Zoramites stir
up the Lamanites to war, and Alma sorrows over the wickedness of the people.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash baked tokens in this chapter.

    python3 build_overrides_alma35.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 35

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "Now"),
        (2, 3, "it came to pass that"),
        (4, 8, "after had made an end"),
        (9, 10, "Amulek"),
        (11, 12, "of these words,"),
        (13, 16, "they withdrew"),
        (17, 19, "themselves"),
        (20, 24, "from the multitude"),
        (25, 27, "and came over"),
        (28, 32, "into the land of Jershon."),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 6, "and the rest"),
        (7, 10, "of the brethren,"),
        (11, 15, "after they had"),
        (16, 17, "preached"),
        (18, 20, "the word"),
        (21, 23, "unto the Zoramites,"),
        (24, 28, "also came over"),
        (29, 33, "into the land of Jershon."),
    ],
    3: [
        (0, 2, "And it came to pass that"),
        (3, 8, "after had consulted together"),
        (9, 11, "the part"),
        (12, 14, "most popular"),
        (15, 17, "of the Zoramites"),
        (18, 21, "concerning the words"),
        (22, 25, "which had been preached"),
        (26, 29, "unto them,"),
        (30, 32, "they were angry"),
        (33, 36, "because of the word,"),
        (37, 37, "for"),
        (38, 40, "it did destroy"),
        (41, 44, "their false craft;"),
        (45, 46, "therefore"),
        (47, 52, "they would not hearken"),
        (53, 54, "unto the words."),
    ],
    4: [
        (0, 4, "And they sent"),
        (5, 7, "and gathered together"),
        (8, 9, "all the people"),
        (10, 13, "throughout all the land,"),
        (14, 16, "and consulted"),
        (17, 19, "with them"),
        (20, 23, "concerning the words"),
        (24, 25, "which had been spoken."),
    ],
    5: [
        (0, 1, "Now"),
        (2, 5, "did not make known"),
        (6, 9, "their rulers"),
        (10, 13, "and their priests"),
        (14, 17, "and their teachers"),
        (18, 19, "to the people,"),
        (20, 22, "concerning"),
        (23, 25, "their desires;"),
        (26, 27, "therefore"),
        (28, 32, "they found out"),
        (33, 33, "privily"),
        (34, 38, "the minds of all the people."),
    ],
    6: [
        (0, 2, "And it came to pass that"),
        (3, 8, "after they had found out"),
        (9, 10, "the minds"),
        (11, 13, "of all the people,"),
        (14, 18, "those who"),
        (19, 22, "favored the words"),
        (23, 25, "which had been spoken"),
        (26, 30, "by Alma and his brethren,"),
        (31, 33, "were cast out"),
        (34, 36, "of the land;"),
        (37, 41, "and they were many;"),
        (42, 47, "and they also came over"),
        (48, 52, "into the land of Jershon."),
    ],
    7: [
        (0, 2, "And it came to pass that"),
        (3, 5, "that did minister"),
        (6, 9, "Alma and his brethren"),
        (10, 13, "unto them."),
    ],
    8: [
        (0, 1, "Now"),
        (2, 3, "were angry"),
        (4, 7, "the people of the Zoramites"),
        (8, 11, "with the people of Ammon"),
        (12, 16, "who were in Jershon,"),
        (17, 20, "and sent over"),
        (21, 25, "the chief ruler"),
        (26, 28, "of the Zoramites,"),
        (29, 33, "being a very wicked man,"),
        (34, 38, "unto the people of Ammon"),
        (39, 40, "a message,"),
        (41, 46, "desiring them"),
        (47, 50, "that they should cast out"),
        (51, 55, "from all their land"),
        (56, 58, "all those"),
        (59, 63, "who came over"),
        (64, 68, "from them"),
        (69, 72, "into their land."),
    ],
    9: [
        (0, 4, "And he breathed out"),
        (5, 8, "many threatenings"),
        (9, 10, "against"),
        (11, 14, "them."),
        (15, 17, "And now"),
        (18, 20, "did not fear"),
        (21, 24, "the people of Ammon"),
        (25, 27, "their words;"),
        (28, 29, "therefore"),
        (30, 35, "they did not cast out"),
        (36, 37, "them,"),
        (38, 41, "but they did receive"),
        (42, 44, "all the poor"),
        (45, 47, "of the Zoramites"),
        (48, 52, "who came over"),
        (53, 56, "unto them;"),
        (57, 62, "and they did nourish them,"),
        (63, 66, "and did clothe them,"),
        (67, 70, "and did give lands"),
        (71, 74, "unto them"),
        (75, 77, "to be for"),
        (78, 80, "their inheritance;"),
        (81, 85, "and they did administer"),
        (86, 89, "unto them"),
        (90, 92, "according to"),
        (93, 95, "their wants."),
    ],
    10: [
        (0, 1, "Now,"),
        (2, 7, "this did stir up"),
        (8, 12, "the anger of the Zoramites"),
        (13, 15, "against"),
        (16, 19, "the people of Ammon,"),
        (20, 25, "and they began to mix"),
        (26, 28, "with the Lamanites"),
        (29, 33, "and to stir them up also"),
        (34, 35, "to anger"),
        (36, 37, "against"),
        (38, 41, "them."),
    ],
    11: [
        (0, 4, "And thus began"),
        (5, 7, "the Zoramites"),
        (8, 10, "and the Lamanites"),
        (11, 14, "to make preparations"),
        (15, 17, "for war"),
        (18, 20, "against"),
        (21, 24, "the people of Ammon,"),
        (25, 28, "and also against"),
        (29, 31, "the Nephites."),
    ],
    12: [
        (0, 4, "And thus ended"),
        (5, 8, "the seventeenth"),
        (9, 10, "year"),
        (11, 15, "of the reign of the judges"),
        (16, 18, "over"),
        (19, 22, "the people of Nephi."),
    ],
    13: [
        (0, 4, "And departed"),
        (5, 8, "the people of Ammon"),
        (9, 13, "out of the land of Jershon,"),
        (14, 16, "and came over"),
        (17, 21, "into the land of Melek,"),
        (22, 23, "and gave place"),
        (24, 27, "in the land of Jershon"),
        (28, 32, "for the armies of the Nephites,"),
        (33, 38, "that they might contend"),
        (39, 43, "with the armies of the Lamanites"),
        (44, 48, "and the armies of the Zoramites;"),
        (49, 53, "and thus commenced"),
        (54, 56, "a war"),
        (57, 60, "betwixt"),
        (61, 65, "the Lamanites and the Nephites,"),
        (66, 69, "in the eighteenth"),
        (70, 71, "year"),
        (72, 76, "of the reign of the judges;"),
        (77, 82, "and shall be given"),
        (83, 84, "an account"),
        (85, 88, "of their wars"),
        (89, 92, "at a time"),
        (93, 94, "hereafter."),
    ],
    14: [
        (0, 4, "And returned"),
        (5, 5, "Alma,"),
        (6, 7, "and Ammon,"),
        (8, 11, "and their brethren,"),
        (12, 16, "and also the two sons"),
        (17, 18, "of Alma"),
        (19, 23, "to the land of Zarahemla,"),
        (24, 26, "after"),
        (27, 31, "they having been"),
        (32, 34, "instruments"),
        (35, 39, "in the hands of God"),
        (40, 42, "of bringing"),
        (43, 48, "many of the Zoramites"),
        (49, 51, "to repentance;"),
        (52, 55, "and as many"),
        (56, 58, "of them"),
        (59, 62, "who were brought"),
        (63, 65, "to repentance"),
        (66, 68, "were driven out"),
        (69, 72, "from their land;"),
        (73, 73, "but"),
        (74, 78, "they have lands"),
        (79, 82, "for their inheritance"),
        (83, 87, "in the land of Jershon,"),
        (88, 91, "and they have taken"),
        (92, 95, "up weapons of war"),
        (96, 101, "to defend themselves,"),
        (102, 105, "and their wives,"),
        (106, 107, "and children,"),
        (108, 111, "and their lands."),
    ],
    15: [
        (0, 1, "Now"),
        (2, 3, "Alma,"),
        (4, 6, "being greatly grieved"),
        (7, 9, "for the iniquity"),
        (10, 12, "of his people,"),
        (13, 13, "yea,"),
        (14, 16, "for the wars,"),
        (17, 19, "and the bloodsheds,"),
        (20, 21, "and contentions"),
        (22, 24, "which were"),
        (25, 29, "among them;"),
        (30, 31, "and because"),
        (32, 36, "he had gone"),
        (37, 41, "to declare the word,"),
        (42, 45, "or was sent"),
        (46, 50, "to declare the word,"),
        (51, 55, "among all the people"),
        (56, 58, "in every city;"),
        (59, 63, "and seeing"),
        (64, 67, "began to wax hard"),
        (68, 70, "the hearts of the people,"),
        (71, 75, "and they began"),
        (76, 77, "to be offended"),
        (78, 81, "because of the strictness"),
        (82, 86, "of keeping the word,"),
        (87, 91, "was exceedingly sorrowful"),
        (92, 93, "his heart."),
    ],
    16: [
        (0, 1, "Therefore,"),
        (2, 6, "he caused"),
        (7, 10, "that should be gathered together"),
        (11, 12, "his sons,"),
        (13, 17, "that he might"),
        (18, 20, "give separately"),
        (21, 25, "unto them all"),
        (26, 26, "each one"),
        (27, 28, "his charge,"),
        (29, 32, "concerning the things"),
        (33, 37, "pertaining unto righteousness."),
        (38, 42, "And we have"),
        (43, 44, "an account"),
        (45, 47, "of his commandments,"),
        (48, 52, "which he gave"),
        (53, 56, "unto them"),
        (57, 59, "according to"),
        (60, 62, "his own record."),
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
