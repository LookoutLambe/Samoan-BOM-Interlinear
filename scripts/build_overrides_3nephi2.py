"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 2 — the people
begin to forget the signs and wonders, growing hard and blind as Satan regains
possession of their hearts, dismissing the doctrine of Christ as foolishness;
wickedness spreads and the Gadianton robbers grow so strong that Nephites and
converted Lamanites unite for defense, the Lamanites becoming white and being
numbered among the Nephites, all called Nephites; the reckoning of years is now
counted from the sign of Christ's coming, and war begins with the robbers.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_3nephi2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 2

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 8, "thus also passed away"),
        (9, 12, "the year"),
        (13, 16, "ninety and fifth,"),
        (17, 23, "and the people began to forget"),
        (24, 28, "those signs and wonders"),
        (29, 34, "which they heard,"),
        (35, 40, "and began to diminish"),
        (41, 43, "their astonishment"),
        (44, 46, "at a sign"),
        (47, 51, "or a wonder"),
        (52, 54, "from heaven,"),
        (55, 58, "insomuch that"),
        (59, 62, "they began to be hardened"),
        (63, 66, "in their hearts,"),
        (67, 68, "and blind"),
        (69, 72, "in their minds,"),
        (73, 77, "and began to disbelieve"),
        (78, 80, "in all things"),
        (81, 87, "which they heard and saw—"),
    ],
    2: [
        (0, 2, "Imagining up"),
        (3, 6, "some vain things"),
        (7, 10, "in their hearts,"),
        (11, 12, "that"),
        (13, 17, "it was a thing wrought"),
        (18, 19, "by men"),
        (20, 22, "and by the power of"),
        (23, 25, "the devil,"),
        (26, 28, "to lead away"),
        (29, 31, "and deceive"),
        (32, 34, "the hearts of the people;"),
        (35, 41, "and thus again got possession"),
        (42, 43, "Satan"),
        (44, 46, "the hearts of the people,"),
        (47, 49, "insomuch that"),
        (50, 51, "he blinded"),
        (52, 54, "their eyes"),
        (55, 59, "and led them away"),
        (60, 61, "to believe"),
        (62, 67, "that the doctrine of Christ"),
        (68, 71, "was a foolish thing"),
        (72, 77, "and a vain thing."),
    ],
    3: [
        (0, 3, "And it came to pass that"),
        (4, 7, "began to grow strong"),
        (8, 8, "the people"),
        (9, 11, "in wickedness"),
        (12, 14, "and abominations;"),
        (15, 19, "and they believed not"),
        (20, 27, "there should be any more signs"),
        (28, 31, "or wonders"),
        (32, 34, "given;"),
        (35, 39, "and Satan went about"),
        (40, 42, "leading away"),
        (43, 45, "the hearts of the people,"),
        (46, 49, "and tempting them"),
        (50, 53, "and urging them"),
        (54, 56, "that they do"),
        (57, 59, "great wickedness"),
        (60, 62, "in the land."),
    ],
    4: [
        (0, 5, "And thus passed away"),
        (6, 9, "the year"),
        (10, 13, "ninety and sixth;"),
        (14, 18, "and also the year"),
        (19, 22, "ninety and seventh;"),
        (23, 27, "and also the year"),
        (28, 31, "ninety and eighth;"),
        (32, 36, "and also the year"),
        (37, 40, "ninety and ninth;"),
    ],
    5: [
        (0, 4, "And also had passed away"),
        (5, 8, "the hundred years"),
        (9, 11, "since the days of"),
        (12, 12, "Mosiah,"),
        (13, 18, "who was king"),
        (19, 24, "over the people of the Nephites."),
    ],
    6: [
        (0, 3, "And had passed away"),
        (4, 9, "six hundred and nine"),
        (10, 11, "years"),
        (12, 14, "since left"),
        (15, 16, "Lehi"),
        (17, 17, "Jerusalem."),
    ],
    7: [
        (0, 3, "And had passed away"),
        (4, 6, "nine years"),
        (7, 8, "of years"),
        (9, 11, "from the time"),
        (12, 15, "when was given"),
        (16, 17, "the sign,"),
        (18, 22, "which spoke"),
        (23, 23, "the prophets,"),
        (24, 29, "would come"),
        (30, 30, "Christ"),
        (31, 33, "into the world."),
    ],
    8: [
        (0, 1, "Now"),
        (2, 8, "the Nephites began to count"),
        (9, 11, "their time"),
        (12, 15, "from the time"),
        (16, 19, "when was given"),
        (20, 21, "the sign,"),
        (22, 24, "or from"),
        (25, 28, "the coming of"),
        (29, 29, "Christ;"),
        (30, 31, "therefore,"),
        (32, 34, "nine years"),
        (35, 37, "had passed away."),
    ],
    9: [
        (0, 2, "And Nephi,"),
        (3, 8, "who was the father of"),
        (9, 9, "Nephi,"),
        (10, 14, "who had"),
        (15, 17, "the charge over"),
        (18, 18, "the records,"),
        (19, 23, "did not return"),
        (24, 27, "to the land of"),
        (28, 28, "Zarahemla,"),
        (29, 33, "and there was no place"),
        (34, 41, "where he could be found"),
        (42, 45, "in all the land."),
    ],
    10: [
        (0, 3, "And it came to pass that"),
        (4, 6, "still remained"),
        (7, 7, "the people"),
        (8, 10, "in wickedness,"),
        (11, 13, "notwithstanding"),
        (14, 17, "the much preaching"),
        (18, 20, "and prophesying"),
        (21, 23, "which was sent"),
        (24, 29, "among them;"),
        (30, 36, "and thus also passed away"),
        (37, 41, "the tenth year;"),
        (42, 46, "and also passed away"),
        (47, 50, "the eleventh year"),
        (51, 53, "in iniquity."),
    ],
    11: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the year"),
        (7, 10, "thirteenth,"),
        (11, 15, "there began to be"),
        (16, 19, "wars and contentions"),
        (20, 23, "throughout all the land;"),
        (24, 24, "for"),
        (25, 28, "had exceedingly increased"),
        (29, 31, "the robbers of Gadianton,"),
        (32, 35, "and they slew"),
        (36, 38, "many people,"),
        (39, 40, "and laid waste"),
        (41, 44, "many cities,"),
        (45, 47, "and they spread"),
        (48, 49, "death"),
        (50, 53, "and much bloodshed"),
        (54, 57, "throughout all the land,"),
        (58, 60, "it became needful"),
        (61, 63, "for all the people,"),
        (64, 66, "both the Nephites"),
        (67, 69, "and the Lamanites,"),
        (70, 73, "that they take up"),
        (74, 76, "their weapons"),
        (77, 83, "against them."),
    ],
    12: [
        (0, 1, "Therefore,"),
        (2, 5, "all the Lamanites"),
        (6, 9, "who were converted"),
        (10, 12, "unto the Lord,"),
        (13, 16, "they united"),
        (17, 20, "with their brethren,"),
        (21, 23, "the Nephites,"),
        (24, 28, "and they were compelled,"),
        (29, 32, "for the safety of"),
        (33, 35, "their lives"),
        (36, 39, "and their women"),
        (40, 43, "and their children,"),
        (44, 46, "to take up"),
        (47, 49, "weapons of war,"),
        (50, 53, "against"),
        (54, 56, "the robbers of Gadianton,"),
        (57, 57, "yea,"),
        (58, 63, "and to keep also"),
        (64, 66, "their rights,"),
        (67, 69, "and the privileges of"),
        (70, 72, "their church"),
        (73, 76, "and their worship,"),
        (77, 80, "and their freedom"),
        (81, 84, "and their liberty."),
    ],
    13: [
        (0, 3, "And it came to pass that"),
        (4, 7, "before had passed away"),
        (8, 11, "this year"),
        (12, 15, "thirteenth,"),
        (16, 17, "were threatened"),
        (18, 19, "the Nephites"),
        (20, 23, "with utter destruction"),
        (24, 25, "because of"),
        (26, 27, "this war,"),
        (28, 30, "which had become"),
        (31, 33, "exceedingly grievous."),
    ],
    14: [
        (0, 3, "And it came to pass that"),
        (4, 5, "were numbered"),
        (6, 7, "the Lamanites"),
        (8, 11, "who united"),
        (12, 14, "with the Nephites"),
        (15, 19, "among the Nephites;"),
    ],
    15: [
        (0, 2, "And was taken away"),
        (3, 5, "their curse"),
        (6, 10, "from them,"),
        (11, 14, "and became white"),
        (15, 17, "their skin"),
        (18, 22, "like unto the Nephites;"),
    ],
    16: [
        (0, 3, "And it came to pass that"),
        (4, 5, "became exceedingly fair"),
        (6, 9, "their young men"),
        (10, 13, "and their daughters,"),
        (14, 18, "and they were numbered"),
        (19, 23, "among the Nephites,"),
        (24, 26, "and were called"),
        (27, 29, "Nephites."),
        (30, 34, "And thus ended"),
        (35, 38, "the year"),
        (39, 42, "thirteenth."),
    ],
    17: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the beginning of"),
        (7, 9, "the year"),
        (10, 13, "fourteenth,"),
        (14, 16, "continued"),
        (17, 18, "the war"),
        (19, 21, "between"),
        (22, 24, "the robbers"),
        (25, 29, "and the people of Nephi"),
        (30, 34, "and became"),
        (35, 37, "exceeding grievous;"),
        (38, 41, "nevertheless,"),
        (42, 48, "the people of Nephi gained"),
        (49, 52, "some advantage"),
        (53, 56, "over the robbers,"),
        (57, 59, "insomuch that"),
        (60, 64, "they drove them out"),
        (65, 66, "backward"),
        (67, 70, "from their lands,"),
        (71, 75, "toward the mountains"),
        (76, 80, "and their secret places."),
    ],
    18: [
        (0, 4, "And thus ended"),
        (5, 8, "the year"),
        (9, 12, "fourteenth."),
        (13, 17, "And in the year"),
        (18, 21, "fifteenth,"),
        (22, 25, "they came"),
        (26, 28, "against"),
        (29, 32, "the people of Nephi;"),
        (33, 35, "and because of"),
        (36, 38, "the wickedness of"),
        (39, 41, "the people of Nephi,"),
        (42, 45, "and their contentions"),
        (46, 49, "and many dissensions,"),
        (50, 51, "therefore"),
        (52, 58, "the Gadianton robbers gained"),
        (59, 62, "many advantages"),
        (63, 67, "over them."),
    ],
    19: [
        (0, 4, "And thus ended"),
        (5, 8, "the year"),
        (9, 12, "fifteenth,"),
        (13, 18, "and thus were"),
        (19, 20, "the people"),
        (21, 23, "in a state of"),
        (24, 27, "many afflictions;"),
        (28, 31, "and hung over"),
        (32, 34, "the sword of"),
        (35, 36, "destruction"),
        (37, 41, "over them,"),
        (42, 44, "insomuch that"),
        (45, 50, "they were about to be destroyed,"),
        (51, 54, "and the cause is"),
        (55, 56, "because of"),
        (57, 59, "their iniquity."),
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
