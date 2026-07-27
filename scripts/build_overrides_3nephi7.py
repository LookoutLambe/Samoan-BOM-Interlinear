"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 7 — the secret
combination murders the chief judge and destroys the government; the people split
into tribes, each with its own leader; the conspirators fail to make Jacob king,
who flees north with his band; amid this anarchy Nephi, son of Nephi, ministers
with great power, working miracles in the name of Jesus, casting out devils and
even raising his brother from the dead, and boldly calling the people to repent,
though most harden their hearts against him in the thirty-first and thirty-second
years, when signs and wonders begin.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi7.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 7

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "Now behold,"),
        (3, 8, "I will show"),
        (9, 11, "unto you"),
        (12, 15, "they did not set up"),
        (16, 17, "a king"),
        (18, 22, "over the land;"),
        (23, 28, "but in this very year,"),
        (29, 29, "yea,"),
        (30, 34, "the thirtieth year,"),
        (35, 38, "they destroyed"),
        (39, 43, "upon the judgment-seat,"),
        (44, 44, "yea,"),
        (45, 48, "they slew"),
        (49, 54, "the chief judge of the land."),
    ],
    2: [
        (0, 4, "And the people were divided,"),
        (5, 12, "one against another;"),
        (13, 17, "and they went apart,"),
        (18, 23, "one from another,"),
        (24, 26, "into tribes,"),
        (27, 32, "each man went"),
        (33, 35, "according to"),
        (36, 37, "his family"),
        (38, 40, "and his kindred"),
        (41, 42, "and friends;"),
        (43, 48, "and thus they broke up"),
        (49, 54, "the government of the land."),
    ],
    3: [
        (0, 5, "And each tribe appointed"),
        (6, 7, "a chief"),
        (8, 11, "or a leader"),
        (12, 16, "over them;"),
        (17, 24, "and thus they became"),
        (25, 26, "tribes"),
        (27, 30, "and leaders of tribes."),
    ],
    4: [
        (0, 2, "Now behold,"),
        (3, 6, "there was no one"),
        (7, 13, "among them"),
        (14, 18, "who did not have"),
        (19, 21, "a large family"),
        (22, 25, "and great kindreds"),
        (26, 30, "and many friends;"),
        (31, 32, "therefore"),
        (33, 37, "became exceedingly great"),
        (38, 40, "their tribes."),
    ],
    5: [
        (0, 1, "Now"),
        (2, 5, "all these things"),
        (6, 7, "were done,"),
        (8, 13, "and there were not yet"),
        (14, 15, "any wars"),
        (16, 21, "among them;"),
        (22, 25, "and had come"),
        (26, 28, "all this iniquity"),
        (29, 32, "upon the people"),
        (33, 33, "because"),
        (34, 40, "they yielded themselves"),
        (41, 45, "unto the power of Satan."),
    ],
    6: [
        (0, 2, "And were broken up"),
        (3, 7, "the regulations of the government,"),
        (8, 9, "because of"),
        (10, 12, "the secret combination"),
        (13, 19, "of the friends and kindreds of them"),
        (20, 23, "who slew"),
        (24, 24, "the prophets."),
    ],
    7: [
        (0, 3, "And they stirred up"),
        (4, 6, "a great contention"),
        (7, 9, "in the land,"),
        (10, 12, "insomuch that"),
        (13, 17, "nearly all became wicked"),
        (18, 24, "the greater part who were righteous;"),
        (25, 25, "yea,"),
        (26, 28, "there were very few"),
        (29, 30, "righteous"),
        (31, 33, "who were"),
        (34, 39, "among them."),
    ],
    8: [
        (0, 6, "And thus had not passed away"),
        (7, 10, "the six years"),
        (11, 14, "since turned away"),
        (15, 20, "the greater part of the people"),
        (21, 24, "from their righteousness,"),
        (25, 29, "like the dog"),
        (30, 32, "to his vomit,"),
        (33, 38, "or like the sow"),
        (39, 41, "to her wallowing."),
    ],
    9: [
        (0, 1, "Now"),
        (2, 6, "this secret combination,"),
        (7, 9, "which brought"),
        (10, 12, "this great iniquity"),
        (13, 17, "upon the people,"),
        (18, 21, "they gathered together"),
        (22, 24, "themselves,"),
        (25, 27, "and set"),
        (28, 31, "at their head,"),
        (32, 33, "a man"),
        (34, 38, "whom they called Jacob;"),
    ],
    10: [
        (0, 5, "And they called him"),
        (6, 9, "their king;"),
        (10, 11, "therefore"),
        (12, 19, "he became a king"),
        (20, 25, "over this wicked band;"),
        (26, 34, "and he was one of the chief men"),
        (35, 41, "who gave his voice"),
        (42, 46, "against the prophets"),
        (47, 51, "who testified"),
        (52, 53, "of Jesus."),
    ],
    11: [
        (0, 3, "And it came to pass that"),
        (4, 9, "their strength was not equal"),
        (10, 13, "in total number"),
        (14, 20, "like the tribes of the people,"),
        (21, 24, "who were united"),
        (25, 28, "save the establishing"),
        (29, 32, "by their leaders"),
        (33, 36, "of their laws,"),
        (37, 39, "each man"),
        (40, 45, "according to his own tribe;"),
        (46, 49, "nevertheless"),
        (50, 55, "they became enemies;"),
        (56, 58, "although"),
        (59, 67, "they were not righteous men,"),
        (68, 71, "yet they were united"),
        (72, 75, "in their hatred"),
        (76, 79, "of those"),
        (80, 84, "who made a covenant"),
        (85, 88, "to destroy the government."),
    ],
    12: [
        (0, 1, "Therefore,"),
        (2, 6, "when Jacob saw"),
        (7, 11, "were more numerous"),
        (12, 15, "their enemies"),
        (16, 19, "than they,"),
        (20, 28, "for he was the king of the band,"),
        (29, 30, "therefore"),
        (31, 34, "he commanded"),
        (35, 36, "his people"),
        (37, 42, "that they take their flight"),
        (43, 48, "into the furthermost part of"),
        (49, 52, "the land northward,"),
        (53, 56, "and there establish"),
        (57, 58, "a kingdom"),
        (59, 62, "for themselves,"),
        (63, 67, "until joined"),
        (68, 71, "unto them"),
        (72, 73, "the dissenters,"),
        (74, 79, "(for he deceived them"),
        (80, 85, "that many dissenters"),
        (86, 90, "there would be)"),
        (91, 96, "and their strength suffice"),
        (97, 100, "to contend with"),
        (101, 104, "the tribes of the people;"),
        (105, 111, "and thus they did."),
    ],
    13: [
        (0, 3, "And so very swift"),
        (4, 6, "their march"),
        (7, 11, "that it could not be impeded"),
        (12, 14, "until"),
        (15, 17, "they went forth"),
        (18, 20, "to a place"),
        (21, 28, "where could not reach"),
        (29, 34, "the people to them."),
        (35, 39, "And thus ended"),
        (40, 44, "the thirtieth year;"),
        (45, 48, "and thus were the affairs of"),
        (49, 53, "the people of Nephi."),
    ],
    14: [
        (0, 2, "And it came to pass"),
        (3, 6, "in the year"),
        (7, 10, "thirty-first,"),
        (11, 14, "they were divided"),
        (15, 16, "into tribes,"),
        (17, 19, "each man"),
        (20, 22, "according to"),
        (23, 24, "his family,"),
        (25, 27, "kindred and friends;"),
        (28, 31, "nevertheless"),
        (32, 36, "they made an agreement"),
        (37, 41, "they would not raise war"),
        (42, 47, "one with another;"),
        (48, 52, "but they were not united"),
        (53, 57, "as to their laws,"),
        (58, 63, "and their kind of government,"),
        (64, 66, "for they were set up"),
        (67, 73, "according to the minds of those"),
        (74, 77, "who were"),
        (78, 81, "their chiefs"),
        (82, 85, "and their leaders."),
        (86, 89, "But they established"),
        (90, 92, "strict laws"),
        (93, 96, "that not trespass"),
        (97, 101, "one against another,"),
        (102, 104, "insomuch that"),
        (105, 107, "they had"),
        (108, 113, "some measure of peace"),
        (114, 116, "in the land;"),
        (117, 120, "nevertheless,"),
        (121, 126, "their hearts were turned away"),
        (127, 132, "from the Lord their God,"),
        (133, 137, "and they stoned the prophets"),
        (138, 142, "and cast them out"),
        (143, 148, "from among them."),
    ],
    15: [
        (0, 3, "And it came to pass that"),
        (4, 7, "Nephi having been visited—"),
        (8, 9, "by angels"),
        (10, 16, "and also the voice of the Lord,"),
        (17, 18, "therefore"),
        (19, 23, "having seen"),
        (24, 25, "angels,"),
        (26, 32, "and he becoming an eye-witness,"),
        (33, 39, "and having been given"),
        (40, 42, "unto him"),
        (43, 45, "the power"),
        (46, 51, "that he might understand"),
        (52, 58, "concerning the ministry of Christ,"),
        (59, 66, "and he also being"),
        (67, 68, "an eye-witness"),
        (69, 75, "to their quick returning"),
        (76, 78, "from righteousness"),
        (79, 85, "to their wickedness and abominations;"),
    ],
    16: [
        (0, 1, "Therefore,"),
        (2, 4, "in his sorrow"),
        (5, 6, "because of"),
        (7, 12, "the hardness of their hearts"),
        (13, 19, "and the blindness of their minds—"),
        (20, 25, "he went forth"),
        (26, 29, "among them"),
        (30, 33, "in that same year,"),
        (34, 38, "and began to testify,"),
        (39, 41, "boldly,"),
        (42, 43, "repentance"),
        (44, 48, "and the remission of sins"),
        (49, 53, "through faith"),
        (54, 59, "in the Lord Jesus Christ."),
    ],
    17: [
        (0, 3, "And many things"),
        (4, 8, "he ministered"),
        (9, 12, "unto them;"),
        (13, 18, "and cannot be written"),
        (19, 21, "all those things,"),
        (22, 26, "and would not suffice"),
        (27, 32, "even a part of them,"),
        (33, 34, "therefore"),
        (35, 40, "these things are not written"),
        (41, 43, "in this book."),
        (44, 48, "And Nephi ministered"),
        (49, 51, "with power"),
        (52, 55, "and great authority."),
    ],
    18: [
        (0, 3, "And it came to pass that"),
        (4, 5, "they were angry"),
        (6, 8, "with him,"),
        (9, 12, "even because"),
        (13, 18, "he had the power"),
        (19, 24, "greater than they,"),
        (25, 32, "for they could not disbelieve"),
        (33, 35, "his words,"),
        (36, 40, "for angels ministered"),
        (41, 43, "unto him"),
        (44, 46, "daily,"),
        (47, 54, "because of the great strength of his faith"),
        (55, 60, "in the Lord Jesus Christ."),
    ],
    19: [
        (0, 4, "And he cast out"),
        (5, 9, "devils and unclean spirits"),
        (10, 14, "in the name of Jesus;"),
        (15, 20, "and even his brother"),
        (21, 26, "he raised from the dead,"),
        (27, 33, "after he had been stoned"),
        (34, 37, "by the people with stones"),
        (38, 40, "and suffered"),
        (41, 43, "unto death."),
    ],
    20: [
        (0, 5, "And the people saw it,"),
        (6, 8, "and did witness of it,"),
        (9, 12, "and were angry"),
        (13, 15, "with him"),
        (16, 19, "because of his power;"),
        (20, 24, "and he also did"),
        (25, 28, "many other miracles,"),
        (29, 34, "before the eyes of the people,"),
        (35, 39, "in the name of Jesus."),
    ],
    21: [
        (0, 5, "And there passed away"),
        (6, 9, "the year"),
        (10, 12, "thirty-first,"),
        (13, 20, "and there were but few"),
        (21, 25, "who were converted"),
        (26, 28, "unto the Lord;"),
        (29, 35, "but as many of them"),
        (36, 38, "as were converted"),
        (39, 43, "did truly show forth"),
        (44, 45, "unto the people"),
        (46, 49, "they were visited"),
        (50, 58, "by the power and Spirit of God,"),
        (59, 63, "which was in Jesus Christ,"),
        (64, 70, "in whom they believed."),
    ],
    22: [
        (0, 6, "And as many of them"),
        (7, 11, "as had cast out"),
        (12, 16, "from them"),
        (17, 18, "the devils,"),
        (19, 22, "and who were healed"),
        (23, 27, "of their sicknesses"),
        (28, 31, "and their infirmities,"),
        (32, 36, "did truly manifest"),
        (37, 38, "unto the people"),
        (39, 45, "the Spirit of God worked"),
        (46, 50, "upon them,"),
        (51, 55, "and had been healed;"),
        (56, 61, "and they also showed forth"),
        (62, 62, "signs"),
        (63, 68, "and they did miracles"),
        (69, 72, "among the people."),
    ],
    23: [
        (0, 5, "Thus also passed away"),
        (6, 9, "the year"),
        (10, 13, "thirty-second."),
        (14, 18, "And Nephi cried"),
        (19, 20, "unto the people"),
        (21, 24, "in the beginning of"),
        (25, 31, "the thirty-third year;"),
        (32, 36, "and he preached"),
        (37, 40, "unto them"),
        (41, 43, "repentance"),
        (44, 47, "and remission of sins."),
    ],
    24: [
        (0, 1, "Now"),
        (2, 4, "I desire"),
        (5, 8, "that ye also remember,"),
        (9, 12, "there was none"),
        (13, 16, "who were brought"),
        (17, 19, "unto repentance"),
        (20, 22, "who were not baptized"),
        (23, 25, "with water."),
    ],
    25: [
        (0, 1, "Therefore,"),
        (2, 5, "Nephi ordained,"),
        (6, 7, "men"),
        (8, 10, "unto this ministry,"),
        (11, 16, "that be baptized with water"),
        (17, 19, "all those"),
        (20, 24, "who should come"),
        (25, 28, "unto them,"),
        (29, 33, "and this being done"),
        (34, 39, "as a witness and a testimony"),
        (40, 44, "before God,"),
        (45, 47, "and unto the people,"),
        (48, 50, "that they repented"),
        (51, 54, "and received a remission"),
        (55, 58, "of their sins."),
    ],
    26: [
        (0, 5, "And there were many"),
        (6, 11, "in the beginning of this year"),
        (12, 13, "who were baptized"),
        (14, 16, "unto repentance;"),
        (17, 22, "and thus passed away"),
        (23, 29, "the greater part of the year."),
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
