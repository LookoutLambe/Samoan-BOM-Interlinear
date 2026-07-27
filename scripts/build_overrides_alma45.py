"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 45 — Alma blesses and
prophesies to his son Helaman, foretells the destruction of the Nephites,
departs and is never heard of again (presumed translated); Helaman leads the
church, and dissension arises among the people.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-splits done up front against bom_books.json:
  v16 `Atua—O`  -> 99 tokens

    python3 build_overrides_alma45.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 45

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "Behold,"),
        (1, 2, "now"),
        (3, 5, "it came to pass that"),
        (6, 7, "greatly rejoiced"),
        (8, 11, "the people of Nephi,"),
        (12, 15, "because had again delivered"),
        (16, 17, "them"),
        (18, 20, "the Lord"),
        (21, 23, "out of the hands of"),
        (24, 26, "their enemies;"),
        (27, 28, "therefore"),
        (29, 32, "they gave"),
        (33, 34, "thanks"),
        (35, 37, "unto the Lord"),
        (38, 40, "their God;"),
        (41, 41, "yea,"),
        (42, 45, "and they fasted"),
        (46, 47, "and prayed"),
        (48, 50, "continually,"),
        (51, 55, "and they worshipped"),
        (56, 58, "God"),
        (59, 63, "with exceedingly great joy."),
    ],
    2: [
        (0, 2, "And it came to pass"),
        (3, 9, "in the nineteenth"),
        (10, 11, "year"),
        (12, 16, "of the reign of the judges"),
        (17, 20, "over the people of"),
        (21, 21, "Nephi,"),
        (22, 24, "came"),
        (25, 25, "Alma"),
        (26, 28, "unto his son"),
        (29, 30, "Helaman"),
        (31, 33, "and said"),
        (34, 36, "unto him:"),
        (37, 39, "Believest thou"),
        (40, 41, "the words"),
        (42, 46, "which I spoke"),
        (47, 49, "unto thee"),
        (50, 52, "concerning"),
        (53, 54, "those records"),
        (55, 56, "which have been kept?"),
    ],
    3: [
        (0, 3, "And said"),
        (4, 4, "Helaman"),
        (5, 7, "unto him:"),
        (8, 8, "Yea,"),
        (9, 11, "I believe"),
        (12, 13, "it."),
    ],
    4: [
        (0, 4, "And said again"),
        (5, 5, "Alma:"),
        (6, 8, "Believest thou"),
        (9, 11, "in Jesus Christ,"),
        (12, 12, "who"),
        (13, 17, "shall come?"),
    ],
    5: [
        (0, 5, "And he said:"),
        (6, 6, "Yea,"),
        (7, 9, "I believe"),
        (10, 12, "all the words"),
        (13, 17, "which thou hast spoken."),
    ],
    6: [
        (0, 4, "And said again"),
        (5, 5, "Alma"),
        (6, 8, "unto him:"),
        (9, 14, "Wilt thou keep"),
        (15, 16, "my commandments?"),
    ],
    7: [
        (0, 5, "And he said:"),
        (6, 6, "Yea,"),
        (7, 11, "I will keep"),
        (12, 13, "thy commandments"),
        (14, 17, "with all my heart."),
    ],
    8: [
        (0, 3, "Then said"),
        (4, 5, "Alma"),
        (6, 8, "unto him:"),
        (9, 11, "Blessed art thou;"),
        (12, 16, "and shall bless"),
        (17, 17, "thee"),
        (18, 20, "the Lord"),
        (21, 23, "in this land."),
    ],
    9: [
        (0, 1, "But behold,"),
        (2, 5, "I have"),
        (6, 9, "some things"),
        (10, 13, "I prophesy"),
        (14, 16, "unto thee;"),
        (17, 19, "but the things"),
        (20, 24, "I prophesy"),
        (25, 27, "unto thee"),
        (28, 30, "let not"),
        (31, 33, "thou make known;"),
        (34, 34, "yea,"),
        (35, 36, "the things"),
        (37, 41, "I prophesy"),
        (42, 44, "unto thee"),
        (45, 51, "shall not be made known,"),
        (52, 54, "until"),
        (55, 55, "is fulfilled"),
        (56, 57, "the prophecy;"),
        (58, 59, "therefore"),
        (60, 61, "write"),
        (62, 62, "the words"),
        (63, 69, "which I shall speak."),
    ],
    10: [
        (0, 0, "And"),
        (1, 3, "these are the words:"),
        (4, 4, "Behold,"),
        (5, 7, "I perceive,"),
        (8, 11, "this very people,"),
        (12, 14, "the Nephites,"),
        (15, 17, "according to"),
        (18, 21, "the spirit of revelation"),
        (22, 25, "which is in me,"),
        (26, 29, "in four hundred"),
        (30, 30, "years"),
        (31, 33, "from the time"),
        (34, 39, "shall manifest"),
        (40, 42, "Jesus Christ"),
        (43, 45, "himself"),
        (46, 49, "unto them,"),
        (50, 53, "shall dwindle"),
        (54, 57, "in unbelief."),
    ],
    11: [
        (0, 0, "Yea,"),
        (1, 6, "and then they shall see"),
        (7, 8, "wars"),
        (9, 10, "and diseases,"),
        (11, 11, "yea,"),
        (12, 13, "famines"),
        (14, 17, "and the shedding of blood,"),
        (18, 21, "even until"),
        (22, 25, "is no more"),
        (26, 29, "the people of Nephi—"),
    ],
    12: [
        (0, 0, "Yea,"),
        (1, 4, "and the cause"),
        (5, 7, "of this thing"),
        (8, 14, "because they shall dwindle"),
        (15, 18, "in unbelief"),
        (19, 22, "and fall"),
        (23, 25, "into the works of"),
        (26, 27, "darkness,"),
        (28, 30, "and lasciviousness,"),
        (31, 33, "and all manner of"),
        (34, 35, "iniquities;"),
        (36, 36, "yea,"),
        (37, 40, "I say"),
        (41, 43, "unto thee,"),
        (44, 49, "because they shall sin"),
        (50, 52, "against"),
        (53, 54, "the light"),
        (55, 57, "and the knowledge"),
        (58, 60, "so great,"),
        (61, 61, "yea,"),
        (62, 65, "I say"),
        (66, 68, "unto thee,"),
        (69, 71, "from"),
        (72, 73, "that day,"),
        (74, 76, "even to"),
        (77, 80, "the fourth generation,"),
        (81, 87, "shall not all pass away"),
        (88, 91, "before comes"),
        (92, 94, "this great iniquity."),
    ],
    13: [
        (0, 3, "And when comes"),
        (4, 6, "that great day,"),
        (7, 7, "behold,"),
        (8, 13, "very near is the coming"),
        (14, 16, "of the time,"),
        (17, 19, "those"),
        (20, 24, "who are"),
        (25, 25, "now,"),
        (26, 29, "or the children of"),
        (30, 31, "them"),
        (32, 35, "who are numbered"),
        (36, 36, "now"),
        (37, 39, "among"),
        (40, 42, "the people of Nephi,"),
        (43, 48, "shall no more be numbered"),
        (49, 51, "among"),
        (52, 54, "the people of Nephi."),
    ],
    14: [
        (0, 0, "But"),
        (1, 4, "whosoever"),
        (5, 6, "remaineth,"),
        (7, 10, "and is not destroyed"),
        (11, 14, "in that great day"),
        (15, 17, "and dreadful,"),
        (18, 21, "shall be numbered"),
        (22, 24, "among"),
        (25, 26, "the Lamanites,"),
        (27, 31, "and shall become"),
        (32, 36, "like unto them,"),
        (37, 39, "all of them,"),
        (40, 41, "except"),
        (42, 45, "some few"),
        (46, 51, "who shall be called"),
        (52, 54, "the disciples of"),
        (55, 56, "the Lord;"),
        (57, 61, "and these"),
        (62, 65, "shall seek"),
        (66, 68, "the Lamanites"),
        (69, 72, "even until"),
        (73, 75, "they are destroyed."),
        (76, 78, "And now,"),
        (79, 80, "because of"),
        (81, 82, "the iniquity,"),
        (83, 85, "this prophecy"),
        (86, 90, "shall surely be fulfilled."),
    ],
    15: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 10, "after had said"),
        (11, 12, "Alma"),
        (13, 14, "these things"),
        (15, 16, "to Helaman,"),
        (17, 21, "he blessed him,"),
        (22, 24, "and also others"),
        (25, 26, "his sons;"),
        (27, 31, "and he also blessed"),
        (32, 33, "the earth"),
        (34, 36, "for the benefit"),
        (37, 40, "of the righteous."),
    ],
    16: [
        (0, 5, "And he said:"),
        (6, 10, "Thus saith"),
        (11, 13, "the Lord"),
        (14, 15, "God—"),
        (16, 19, "Shall be cursed"),
        (20, 21, "the land,"),
        (22, 22, "yea,"),
        (23, 25, "this land,"),
        (26, 27, "unto every nation,"),
        (28, 28, "kindred,"),
        (29, 29, "tongue,"),
        (30, 32, "and all people,"),
        (33, 36, "even unto"),
        (37, 38, "destruction,"),
        (39, 43, "when they are fully ripe"),
        (44, 46, "in the doing of"),
        (47, 48, "wickedness;"),
        (49, 52, "and as"),
        (53, 55, "I have said,"),
        (56, 62, "so shall it be done;"),
        (63, 64, "for"),
        (65, 67, "this curse"),
        (68, 70, "and the blessing"),
        (71, 73, "of God"),
        (74, 76, "upon"),
        (77, 78, "the land,"),
        (79, 84, "for cannot look"),
        (85, 87, "the Lord"),
        (88, 90, "upon sin"),
        (91, 94, "with the least degree"),
        (95, 98, "that could be allowed."),
    ],
    17: [
        (0, 2, "And now,"),
        (3, 8, "after had said"),
        (9, 10, "Alma"),
        (11, 13, "these words,"),
        (14, 16, "he blessed"),
        (17, 18, "the church,"),
        (19, 19, "yea,"),
        (20, 22, "all of them"),
        (23, 24, "who"),
        (25, 29, "should stand steadfast"),
        (30, 32, "in the faith"),
        (33, 36, "from that time"),
        (37, 41, "and henceforth."),
    ],
    18: [
        (0, 5, "And when had done"),
        (6, 7, "Alma"),
        (8, 10, "this thing"),
        (11, 15, "he departed"),
        (16, 19, "out of the land of"),
        (20, 20, "Zarahemla,"),
        (21, 22, "as if"),
        (23, 25, "to go"),
        (26, 29, "into the land of"),
        (30, 30, "Melek."),
        (31, 34, "And it came to pass that"),
        (35, 37, "was no more heard"),
        (38, 40, "any word"),
        (41, 42, "concerning"),
        (43, 45, "him;"),
        (46, 48, "concerning his death"),
        (49, 52, "or his burial"),
        (53, 56, "we know not"),
        (57, 60, "anything of it."),
    ],
    19: [
        (0, 0, "Behold,"),
        (1, 4, "this is the thing"),
        (5, 7, "we know,"),
        (8, 9, "that he"),
        (10, 12, "was a man"),
        (13, 14, "who was righteous;"),
        (15, 17, "and went out"),
        (18, 19, "a report"),
        (20, 23, "in the whole church"),
        (24, 28, "that he was taken up"),
        (29, 31, "by the Spirit,"),
        (32, 32, "or"),
        (33, 36, "he was buried"),
        (37, 40, "by the hand of"),
        (41, 42, "the Lord,"),
        (43, 46, "even as"),
        (47, 47, "Moses."),
        (48, 49, "But behold,"),
        (50, 52, "saith"),
        (53, 54, "the holy scriptures"),
        (55, 56, "took"),
        (57, 59, "the Lord"),
        (60, 60, "Moses"),
        (61, 64, "unto himself;"),
        (65, 68, "and we suppose"),
        (69, 72, "that he also received"),
        (73, 73, "Alma"),
        (74, 76, "in the spirit,"),
        (77, 80, "unto himself;"),
        (81, 82, "therefore,"),
        (83, 86, "this is the cause,"),
        (87, 91, "we do not know"),
        (92, 93, "anything"),
        (94, 96, "concerning"),
        (97, 98, "his death"),
        (99, 101, "and his burial."),
    ],
    20: [
        (0, 2, "And now"),
        (3, 4, "it came to pass"),
        (5, 7, "in the commencement"),
        (8, 14, "of the nineteenth"),
        (15, 16, "year"),
        (17, 21, "of the reign of the judges"),
        (22, 25, "over the people of"),
        (26, 26, "Nephi,"),
        (27, 30, "went forth"),
        (31, 31, "Helaman"),
        (32, 34, "among"),
        (35, 36, "the people"),
        (37, 39, "to declare"),
        (40, 41, "the word"),
        (42, 45, "unto them."),
    ],
    21: [
        (0, 1, "For behold,"),
        (2, 3, "because of"),
        (4, 6, "their wars"),
        (7, 9, "with the Lamanites"),
        (10, 13, "and the many"),
        (14, 15, "little dissensions"),
        (16, 17, "and contentions"),
        (18, 20, "which were"),
        (21, 23, "among"),
        (24, 25, "the people,"),
        (26, 27, "therefore"),
        (28, 31, "it was necessary that"),
        (32, 33, "should be declared"),
        (34, 36, "the word"),
        (37, 39, "of God"),
        (40, 42, "among"),
        (43, 44, "them,"),
        (45, 45, "yea,"),
        (46, 48, "and it was necessary that"),
        (49, 50, "should be made"),
        (51, 54, "a proper regulation"),
        (55, 58, "in the whole church."),
    ],
    22: [
        (0, 1, "Therefore,"),
        (2, 5, "went forth"),
        (6, 6, "Helaman"),
        (7, 9, "and his brethren"),
        (10, 12, "to re-establish"),
        (13, 14, "the church"),
        (15, 18, "in the whole land,"),
        (19, 19, "yea,"),
        (20, 22, "in all the cities"),
        (23, 26, "throughout the whole land"),
        (27, 29, "which belonged to"),
        (30, 33, "the people of Nephi."),
        (34, 37, "And it came to pass that"),
        (38, 39, "they appointed"),
        (40, 41, "priests"),
        (42, 44, "and teachers"),
        (45, 48, "throughout the whole land,"),
        (49, 51, "over"),
        (52, 53, "all the congregations."),
    ],
    23: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 9, "after had appointed"),
        (10, 11, "Helaman"),
        (12, 14, "and his brethren"),
        (15, 16, "priests"),
        (17, 18, "and teachers"),
        (19, 21, "over"),
        (22, 23, "all the congregations,"),
        (24, 26, "it came to pass that"),
        (27, 28, "there arose"),
        (29, 30, "a dissension"),
        (31, 33, "among"),
        (34, 35, "them,"),
        (36, 42, "and they would not hearken"),
        (43, 45, "to the words of"),
        (46, 46, "Helaman"),
        (47, 49, "and his brethren;"),
    ],
    24: [
        (0, 4, "But they grew"),
        (5, 7, "in pride,"),
        (8, 11, "in the swelling of"),
        (12, 14, "their hearts,"),
        (15, 16, "because of"),
        (17, 19, "their riches"),
        (20, 23, "which were exceedingly great;"),
        (24, 25, "therefore"),
        (26, 28, "was increased"),
        (29, 31, "their wealth"),
        (32, 36, "in their own sight,"),
        (37, 41, "and would not hearken"),
        (42, 45, "to their words,"),
        (46, 47, "to walk"),
        (48, 50, "in righteousness"),
        (51, 53, "before"),
        (54, 55, "God."),
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
