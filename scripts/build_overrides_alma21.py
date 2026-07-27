"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 21 — Aaron and
his brethren preach among the Amalekites and Amulonites in the land of
Jerusalem; Aaron contends with an Amalekite in a synagogue; the brethren
are cast into prison at Middoni and delivered by Ammon and Lamoni; Aaron
goes to the land of Nephi to the house of the king (Lamoni's father).

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

    python3 build_overrides_alma21.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 21

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "Now"),
        (2, 4, "when separated"),
        (5, 9, "Ammon and his brethren"),
        (10, 12, "themselves"),
        (13, 15, "in the borders of"),
        (16, 20, "the land of the Lamanites,"),
        (21, 21, "behold"),
        (22, 23, "Aaron"),
        (24, 27, "took his journey"),
        (28, 31, "towards the land"),
        (32, 37, "which was called by the Lamanites,"),
        (38, 39, "Jerusalem,"),
        (40, 41, "so named"),
        (42, 44, "after the land"),
        (45, 48, "where were born"),
        (49, 51, "their fathers;"),
        (52, 56, "and it was far away"),
        (57, 59, "joining"),
        (60, 62, "the borders of Mormon."),
    ],
    2: [
        (0, 1, "Now"),
        (2, 3, "had built"),
        (4, 6, "the Lamanites"),
        (7, 9, "and the Amalekites"),
        (10, 13, "and the people of Amulon"),
        (14, 16, "a great city,"),
        (17, 19, "which was called"),
        (20, 21, "Jerusalem."),
    ],
    3: [
        (0, 1, "Now"),
        (2, 6, "the Lamanites of themselves"),
        (7, 11, "were sufficiently hardened,"),
        (12, 16, "but greater was"),
        (17, 19, "the hardness of"),
        (20, 21, "the Amalekites"),
        (22, 24, "and the Amulonites;"),
        (25, 26, "therefore"),
        (27, 30, "they did stir up"),
        (31, 32, "the Lamanites"),
        (33, 34, "that they should harden"),
        (35, 37, "their hearts,"),
        (38, 40, "that they should increase"),
        (41, 44, "their wickedness"),
        (45, 49, "and their abominations."),
    ],
    4: [
        (0, 3, "And it came to pass that"),
        (4, 6, "Aaron came"),
        (7, 11, "to the city of Jerusalem,"),
        (12, 16, "and first began to preach"),
        (17, 19, "to the Amalekites."),
        (20, 23, "And he began to"),
        (24, 26, "he preach"),
        (27, 30, "to them"),
        (31, 34, "in their synagogues,"),
        (35, 35, "for"),
        (36, 38, "they had built"),
        (39, 39, "synagogues"),
        (40, 42, "according to"),
        (43, 46, "the order of the Nehors;"),
        (47, 47, "for"),
        (48, 51, "many of"),
        (52, 56, "the Amalekites and the Amulonites"),
        (57, 62, "were those who followed"),
        (63, 66, "the order of the Nehors."),
    ],
    5: [
        (0, 1, "Therefore,"),
        (2, 5, "as Aaron entered"),
        (6, 9, "into one of"),
        (10, 12, "their synagogues"),
        (13, 17, "to preach unto the people,"),
        (18, 23, "and as he was speaking"),
        (24, 27, "unto them,"),
        (28, 28, "behold"),
        (29, 31, "there arose"),
        (32, 34, "an Amalekite"),
        (35, 39, "and began to contend"),
        (40, 42, "with him,"),
        (43, 44, "saying:"),
        (45, 49, "What is that"),
        (50, 54, "thou hast testified?"),
        (55, 57, "Hast thou seen"),
        (58, 60, "an angel?"),
        (61, 61, "Why"),
        (62, 66, "do not appear"),
        (67, 68, "angels"),
        (69, 72, "unto us?"),
        (73, 73, "Behold"),
        (74, 77, "are not as good"),
        (78, 79, "this people"),
        (80, 84, "as thy people?"),
    ],
    6: [
        (0, 4, "Thou also sayest,"),
        (5, 9, "we shall perish"),
        (10, 11, "except"),
        (12, 14, "we repent."),
        (15, 19, "How knowest thou"),
        (20, 21, "the thoughts"),
        (22, 23, "and intents"),
        (24, 27, "of our hearts?"),
        (28, 32, "How knowest thou"),
        (33, 37, "that there is cause"),
        (38, 41, "for us to repent?"),
        (42, 46, "How knowest thou"),
        (47, 51, "that we are not"),
        (52, 55, "a righteous people?"),
        (56, 56, "Behold,"),
        (57, 59, "we have built"),
        (60, 60, "sanctuaries,"),
        (61, 65, "and we do assemble together"),
        (66, 68, "ourselves"),
        (69, 71, "to worship"),
        (72, 74, "God."),
        (75, 77, "We do believe"),
        (78, 81, "will save"),
        (82, 84, "God"),
        (85, 86, "all men."),
    ],
    7: [
        (0, 1, "Now"),
        (2, 4, "said"),
        (5, 5, "Aaron"),
        (6, 8, "unto him:"),
        (9, 12, "Believest thou"),
        (13, 17, "that shall come"),
        (18, 22, "the Son of God"),
        (23, 25, "to redeem mankind"),
        (26, 29, "from their sins?"),
    ],
    8: [
        (0, 3, "And said"),
        (4, 5, "the man"),
        (6, 8, "unto him:"),
        (9, 12, "We do not believe"),
        (13, 15, "that thou knowest"),
        (16, 18, "any such thing."),
        (19, 22, "We do not believe"),
        (23, 26, "in these foolish traditions."),
        (27, 30, "We do not believe"),
        (31, 33, "that thou knowest"),
        (34, 37, "concerning things"),
        (38, 42, "which are to come,"),
        (43, 47, "neither do we believe"),
        (48, 49, "did know"),
        (50, 52, "thy fathers"),
        (53, 57, "and also our fathers"),
        (58, 61, "concerning the things"),
        (62, 66, "which they spake,"),
        (67, 70, "concerning that"),
        (71, 75, "which is to come."),
    ],
    9: [
        (0, 1, "Now"),
        (2, 6, "began to read"),
        (7, 8, "Aaron"),
        (9, 12, "unto them"),
        (13, 14, "the scriptures"),
        (15, 17, "concerning"),
        (18, 22, "the coming of Christ,"),
        (23, 27, "and also concerning"),
        (28, 31, "the resurrection of"),
        (32, 34, "the dead,"),
        (35, 37, "and that"),
        (38, 43, "there could be no"),
        (44, 45, "redemption"),
        (46, 47, "for mankind"),
        (48, 48, "save"),
        (49, 52, "it were through"),
        (53, 55, "the death and"),
        (56, 58, "sufferings of Christ,"),
        (59, 62, "and the atonement of"),
        (63, 64, "his blood."),
    ],
    10: [
        (0, 3, "And it came to pass"),
        (4, 9, "as he began to expound"),
        (10, 11, "these things"),
        (12, 15, "unto them"),
        (16, 19, "they were angry"),
        (20, 22, "with him,"),
        (23, 27, "and began to mock"),
        (28, 30, "him;"),
        (31, 36, "and they would not hear"),
        (37, 38, "the words"),
        (39, 43, "which he spake."),
    ],
    11: [
        (0, 1, "Therefore,"),
        (2, 6, "when he saw"),
        (7, 12, "that they would not hear"),
        (13, 15, "his words,"),
        (16, 21, "he departed"),
        (22, 24, "out of"),
        (25, 27, "their synagogue,"),
        (28, 31, "and came over to"),
        (32, 33, "a village"),
        (34, 37, "which was called Ani-Anti,"),
        (38, 40, "and there"),
        (41, 45, "he found"),
        (46, 46, "Muloki"),
        (47, 51, "preaching the word"),
        (52, 55, "unto them;"),
        (56, 58, "and also Ammah"),
        (59, 61, "and his brethren."),
        (62, 65, "And they contended"),
        (66, 68, "with many"),
        (69, 73, "about the word."),
    ],
    12: [
        (0, 3, "And it came to pass that"),
        (4, 6, "they saw"),
        (7, 10, "that the people hardened"),
        (11, 13, "their hearts,"),
        (14, 15, "therefore"),
        (16, 20, "they departed"),
        (21, 24, "and came over into"),
        (25, 28, "the land of Middoni."),
        (29, 33, "And they did preach"),
        (34, 35, "the word"),
        (36, 38, "unto many,"),
        (39, 41, "and few"),
        (42, 43, "believed"),
        (44, 45, "on the words"),
        (46, 49, "which they taught."),
    ],
    13: [
        (0, 3, "Nevertheless"),
        (4, 6, "Aaron was taken"),
        (7, 12, "and a certain number of his brethren"),
        (13, 15, "and cast"),
        (16, 18, "into prison,"),
        (19, 23, "and the remainder"),
        (24, 26, "of them"),
        (27, 29, "fled"),
        (30, 34, "out of the land of Middoni,"),
        (35, 39, "unto the regions round about."),
    ],
    14: [
        (0, 5, "And those who"),
        (6, 10, "were cast into prison"),
        (11, 12, "suffered"),
        (13, 16, "many things,"),
        (17, 21, "and they were delivered"),
        (22, 24, "by the hand of"),
        (25, 27, "Lamoni and Ammon,"),
        (28, 32, "and they were fed"),
        (33, 34, "and clothed."),
    ],
    15: [
        (0, 5, "And they went forth again"),
        (6, 8, "to declare"),
        (9, 10, "the word,"),
        (11, 15, "and thus were delivered"),
        (16, 18, "they"),
        (19, 22, "for the first time"),
        (23, 24, "forth"),
        (25, 27, "out of prison;"),
        (28, 33, "and thus they had suffered."),
    ],
    16: [
        (0, 4, "And they went forth"),
        (5, 8, "whithersoever"),
        (9, 14, "they were led"),
        (15, 18, "by the Spirit of"),
        (19, 20, "the Lord,"),
        (21, 23, "and preaching"),
        (24, 28, "the word of God"),
        (29, 32, "in every synagogue of"),
        (33, 34, "the Amalekites,"),
        (35, 40, "or in every assembly of"),
        (41, 42, "the Lamanites"),
        (43, 49, "where they could be admitted."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 6, "began to bless"),
        (7, 8, "them"),
        (9, 11, "the Lord,"),
        (12, 14, "insomuch that"),
        (15, 16, "they brought"),
        (17, 19, "many"),
        (20, 23, "to the knowledge of"),
        (24, 25, "the truth;"),
        (26, 26, "yea,"),
        (27, 29, "they did convince"),
        (30, 32, "many"),
        (33, 35, "concerning"),
        (36, 38, "their sins,"),
        (39, 42, "and concerning"),
        (43, 47, "the traditions of their fathers,"),
        (48, 51, "which were not correct."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 6, "returned"),
        (7, 9, "Ammon and Lamoni"),
        (10, 14, "from the land of Middoni"),
        (15, 19, "to the land of Ishmael,"),
        (20, 22, "which was the land"),
        (23, 26, "of their inheritance."),
    ],
    19: [
        (0, 4, "And was not permitted"),
        (5, 5, "Ammon"),
        (6, 10, "by king Lamoni"),
        (11, 13, "to serve"),
        (14, 16, "him,"),
        (17, 20, "or to be"),
        (21, 22, "his servant."),
    ],
    20: [
        (0, 4, "But he commanded"),
        (5, 6, "that should be built"),
        (7, 8, "synagogues"),
        (9, 13, "in the land of Ishmael;"),
        (14, 18, "and he commanded"),
        (19, 21, "that should gather together"),
        (22, 24, "themselves"),
        (25, 27, "his people,"),
        (28, 31, "or the people who"),
        (32, 35, "were under"),
        (36, 37, "his reign."),
    ],
    21: [
        (0, 4, "And he rejoiced"),
        (5, 8, "over them,"),
        (9, 13, "and he taught"),
        (14, 17, "them"),
        (18, 20, "many things."),
        (21, 26, "And he also declared"),
        (27, 30, "unto them"),
        (31, 33, "that they"),
        (34, 36, "were a people"),
        (37, 42, "who were under"),
        (43, 44, "his reign,"),
        (45, 48, "and that they"),
        (49, 53, "were a free people,"),
        (54, 58, "that they were free"),
        (59, 62, "from the oppressions of"),
        (63, 64, "the king,"),
        (65, 66, "his father;"),
        (67, 67, "for"),
        (68, 71, "was granted by"),
        (72, 73, "his father"),
        (74, 76, "unto him"),
        (77, 80, "that he might reign"),
        (81, 84, "over the people who"),
        (85, 90, "were in the land of Ishmael,"),
        (91, 94, "and all the land"),
        (95, 97, "round about."),
    ],
    22: [
        (0, 5, "And he also declared"),
        (6, 9, "unto them,"),
        (10, 14, "that they might have"),
        (15, 16, "the liberty"),
        (17, 20, "of worshiping"),
        (21, 25, "the Lord their God"),
        (26, 28, "according to"),
        (29, 31, "their desires,"),
        (32, 35, "in whatsoever place"),
        (36, 39, "they were,"),
        (40, 41, "if"),
        (42, 44, "it were"),
        (45, 49, "in the land"),
        (50, 54, "which was under"),
        (55, 57, "the reign of"),
        (58, 61, "king Lamoni."),
    ],
    23: [
        (0, 3, "And did preach"),
        (4, 4, "Ammon"),
        (5, 7, "unto the people of"),
        (8, 11, "king Lamoni;"),
        (12, 15, "and it came to pass that"),
        (16, 19, "he did teach"),
        (20, 23, "them"),
        (24, 25, "all things"),
        (26, 28, "concerning"),
        (29, 33, "things pertaining to righteousness."),
        (34, 38, "And he did exhort"),
        (39, 42, "them"),
        (43, 45, "daily,"),
        (46, 49, "with all diligence;"),
        (50, 54, "and they gave heed"),
        (55, 57, "unto his word,"),
        (58, 61, "and they were zealous"),
        (62, 65, "for the keeping of"),
        (66, 69, "the commandments of God."),
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
