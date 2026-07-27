"""
Hand-curated TAM-phrase gloss overrides for Helamana (Helaman) 15 — the close of
Samuel the Lamanite's prophecy: wo to the impenitent Nephites whose houses will
be left desolate; the Lord loved and chastened the Nephites as a chosen people,
but the converted Lamanites now walk steadfastly in the faith, firm and immovable
and full of charity, unashamed to bring souls to repentance; a warning that the
Nephites, having greater light, face a heavier judgment if they will not repent.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split applied to bom_books.json before glossing:
    15:9  agasala—aua  ->  agasala—  +  aua

    python3 build_overrides_helaman15.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "helaman"
CHAPTER_NUM = 15

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now,"),
        (3, 6, "O my beloved brethren,"),
        (7, 7, "behold,"),
        (8, 11, "I declare"),
        (12, 14, "unto you"),
        (15, 16, "except"),
        (17, 19, "ye repent"),
        (20, 23, "shall be left"),
        (24, 26, "your houses"),
        (27, 29, "unto you"),
        (30, 31, "desolate."),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 2, "except"),
        (3, 5, "ye repent"),
        (6, 10, "there shall be"),
        (11, 13, "a great cause"),
        (14, 18, "to mourn"),
        (19, 21, "your women"),
        (22, 27, "in the day of giving suck;"),
        (28, 28, "for"),
        (29, 33, "ye shall try"),
        (34, 35, "to flee"),
        (36, 42, "and there shall be no place"),
        (43, 47, "ye may take refuge;"),
        (48, 48, "yea,"),
        (49, 52, "and wo unto"),
        (53, 55, "those with child,"),
        (56, 56, "for"),
        (57, 61, "they shall be heavy"),
        (62, 66, "and cannot flee;"),
        (67, 68, "therefore,"),
        (69, 76, "they shall be trodden down"),
        (77, 82, "and shall be left"),
        (83, 84, "to perish."),
    ],
    3: [
        (0, 0, "Yea,"),
        (1, 3, "wo unto"),
        (4, 5, "this people"),
        (6, 10, "who are called"),
        (11, 14, "the people of Nephi"),
        (15, 18, "when they see"),
        (19, 22, "all these signs"),
        (23, 25, "and wonders"),
        (26, 27, "except"),
        (28, 30, "they repent;"),
        (31, 32, "for behold,"),
        (33, 36, "they have been"),
        (37, 41, "a chosen people of"),
        (42, 43, "the Lord;"),
        (44, 44, "yea,"),
        (45, 48, "he loved"),
        (49, 52, "the people of Nephi,"),
        (53, 57, "and he hath also chastened"),
        (58, 59, "them;"),
        (60, 60, "yea,"),
        (61, 65, "he chastened them"),
        (66, 68, "in the days of"),
        (69, 71, "their iniquities"),
        (72, 72, "because"),
        (73, 76, "he loves"),
        (77, 80, "them."),
    ],
    4: [
        (0, 1, "But behold,"),
        (2, 4, "O my brethren,"),
        (5, 8, "he hated"),
        (9, 11, "the Lamanites"),
        (12, 12, "because"),
        (13, 17, "were continually evil"),
        (18, 22, "their deeds,"),
        (23, 29, "and the cause of this"),
        (30, 31, "because of"),
        (32, 34, "the iniquity of"),
        (35, 37, "the tradition of"),
        (38, 40, "their fathers."),
        (41, 42, "But behold,"),
        (43, 47, "salvation has come"),
        (48, 51, "unto them"),
        (52, 53, "because of"),
        (54, 56, "the preaching of"),
        (57, 58, "the Nephites;"),
        (59, 63, "and for this intent"),
        (64, 66, "hath prolonged"),
        (67, 69, "the Lord"),
        (70, 72, "their days."),
    ],
    5: [
        (0, 3, "And I desire"),
        (4, 7, "that ye behold"),
        (8, 14, "the greater part of them"),
        (15, 18, "are"),
        (19, 21, "in the path of"),
        (22, 25, "their duty,"),
        (26, 29, "and they walk"),
        (30, 32, "circumspectly"),
        (33, 37, "before God,"),
        (38, 41, "and they observe"),
        (42, 43, "to keep"),
        (44, 45, "his commandments"),
        (46, 48, "and his statutes"),
        (49, 51, "and his judgments,"),
        (52, 54, "according to"),
        (55, 57, "the law of"),
        (58, 58, "Moses."),
    ],
    6: [
        (0, 0, "Yea,"),
        (1, 4, "I say"),
        (5, 7, "unto you,"),
        (8, 14, "the greater part of them"),
        (15, 18, "are doing"),
        (19, 20, "this thing,"),
        (21, 25, "and they are striving"),
        (26, 31, "with unwearied diligence"),
        (32, 35, "that they may"),
        (36, 37, "bring"),
        (38, 42, "the remainder of"),
        (43, 45, "their brethren"),
        (46, 49, "to the knowledge of"),
        (50, 51, "the truth;"),
        (52, 53, "therefore"),
        (54, 56, "there are many"),
        (57, 58, "who are added"),
        (59, 62, "to their number"),
        (63, 65, "daily."),
    ],
    7: [
        (0, 1, "And behold,"),
        (2, 4, "ye know"),
        (5, 7, "of yourselves,"),
        (8, 8, "for"),
        (9, 11, "ye have witnessed,"),
        (12, 17, "as many of them"),
        (18, 21, "as are brought"),
        (22, 25, "to the knowledge of"),
        (26, 27, "the truth,"),
        (28, 31, "and to know"),
        (32, 37, "the wicked and abominable"),
        (38, 39, "traditions of"),
        (40, 42, "their fathers,"),
        (43, 46, "and are led"),
        (47, 48, "to believe"),
        (49, 51, "the holy scriptures,"),
        (52, 52, "yea,"),
        (53, 55, "the prophecies of"),
        (56, 57, "the holy prophets,"),
        (58, 60, "which are written,"),
        (61, 65, "which leadeth"),
        (66, 67, "them"),
        (68, 70, "to faith"),
        (71, 73, "on the Lord,"),
        (74, 77, "and unto repentance,"),
        (78, 83, "which faith and repentance"),
        (84, 86, "brings"),
        (87, 91, "a change of heart"),
        (92, 95, "unto them—"),
    ],
    8: [
        (0, 1, "Therefore,"),
        (2, 7, "as many of them"),
        (8, 10, "as have come"),
        (11, 13, "to this knowledge of"),
        (14, 16, "the truth,"),
        (17, 19, "ye know"),
        (20, 22, "of yourselves"),
        (23, 28, "they are firm and steadfast"),
        (29, 31, "in the faith,"),
        (32, 35, "and in the thing"),
        (36, 40, "wherewith they were made free."),
    ],
    9: [
        (0, 4, "And ye know also"),
        (5, 7, "they have buried"),
        (8, 11, "their weapons of"),
        (12, 12, "war,"),
        (13, 16, "and they fear"),
        (17, 20, "to take them up"),
        (21, 25, "lest in any way"),
        (26, 31, "they should sin;"),
        (32, 32, "yea,"),
        (33, 37, "ye can see"),
        (38, 40, "they fear"),
        (41, 42, "to sin—"),
        (43, 44, "for behold"),
        (45, 53, "they will suffer themselves"),
        (54, 57, "to be trodden down"),
        (58, 59, "and slain"),
        (60, 63, "by their enemies,"),
        (64, 71, "and they will not lift up"),
        (72, 74, "their swords"),
        (75, 80, "against them,"),
        (81, 86, "and they did this"),
        (87, 88, "because of"),
        (89, 91, "their faith"),
        (92, 93, "in Christ."),
    ],
    10: [
        (0, 2, "And now,"),
        (3, 4, "because of"),
        (5, 7, "their steadfastness"),
        (8, 11, "when they believe"),
        (12, 14, "in that thing"),
        (15, 19, "which they believe,"),
        (20, 21, "because of"),
        (22, 24, "their firmness"),
        (25, 29, "when they are enlightened,"),
        (30, 30, "behold,"),
        (31, 36, "shall bless them"),
        (37, 39, "the Lord"),
        (40, 42, "and prolong"),
        (43, 45, "their days,"),
        (46, 48, "notwithstanding"),
        (49, 51, "their iniquity—"),
    ],
    11: [
        (0, 0, "Yea,"),
        (1, 3, "even if"),
        (4, 9, "they should dwindle"),
        (10, 13, "in unbelief,"),
        (14, 17, "shall prolong"),
        (18, 20, "the Lord"),
        (21, 23, "their days,"),
        (24, 26, "until"),
        (27, 30, "the time comes"),
        (31, 35, "which was spoken"),
        (36, 38, "by our fathers,"),
        (39, 43, "and also the prophet"),
        (44, 44, "Zenos,"),
        (45, 50, "and many other prophets,"),
        (51, 53, "concerning"),
        (54, 56, "the restoration of"),
        (57, 59, "our brethren,"),
        (60, 62, "the Lamanites,"),
        (63, 66, "to the knowledge of"),
        (67, 68, "the truth—"),
    ],
    12: [
        (0, 0, "Yea,"),
        (1, 4, "I say"),
        (5, 7, "unto you,"),
        (8, 10, "have been extended"),
        (11, 15, "to the latter days"),
        (16, 19, "the promises of the Lord"),
        (20, 23, "to our brethren,"),
        (24, 26, "the Lamanites;"),
        (27, 30, "and notwithstanding"),
        (31, 35, "the many afflictions"),
        (36, 39, "which shall come"),
        (40, 43, "upon them,"),
        (44, 47, "and notwithstanding"),
        (48, 53, "they shall be driven"),
        (54, 59, "to and fro"),
        (60, 64, "upon the earth,"),
        (65, 66, "and be hunted,"),
        (67, 71, "and shall be smitten"),
        (72, 74, "and scattered about,"),
        (75, 78, "having no place"),
        (79, 81, "for them"),
        (82, 85, "to take refuge;"),
        (86, 90, "shall be merciful"),
        (91, 92, "the Lord"),
        (93, 96, "unto them."),
    ],
    13: [
        (0, 6, "And this accordeth with"),
        (7, 8, "the prophecy,"),
        (9, 10, "that"),
        (11, 17, "they shall again be brought"),
        (18, 21, "to the true knowledge,"),
        (22, 26, "which is the knowledge of"),
        (27, 29, "their Redeemer,"),
        (30, 35, "and their great shepherd"),
        (36, 38, "and true,"),
        (39, 40, "and be numbered"),
        (41, 43, "among"),
        (44, 45, "his sheep."),
    ],
    14: [
        (0, 1, "Therefore"),
        (2, 6, "I say"),
        (7, 9, "unto you,"),
        (10, 15, "it shall be better"),
        (16, 18, "for them"),
        (19, 21, "than for you"),
        (22, 23, "except"),
        (24, 26, "ye repent."),
    ],
    15: [
        (0, 1, "For behold,"),
        (2, 6, "if had been shown"),
        (7, 10, "unto them"),
        (11, 13, "the mighty works"),
        (14, 16, "which were shown"),
        (17, 19, "unto you,"),
        (20, 20, "yea,"),
        (21, 24, "unto them"),
        (25, 28, "who have dwindled"),
        (29, 32, "in unbelief"),
        (33, 34, "because of"),
        (35, 36, "the traditions of"),
        (37, 39, "their fathers,"),
        (40, 44, "ye can see"),
        (45, 47, "of yourselves"),
        (48, 52, "that they would not"),
        (53, 56, "again dwindle"),
        (57, 60, "in unbelief."),
    ],
    16: [
        (0, 1, "Therefore,"),
        (2, 4, "saith"),
        (5, 6, "the Lord:"),
        (7, 14, "I will not utterly destroy"),
        (15, 16, "them,"),
        (17, 22, "but I will cause"),
        (23, 25, "in the day"),
        (26, 29, "according to"),
        (30, 31, "my wisdom"),
        (32, 39, "they shall return again"),
        (40, 42, "unto me,"),
        (43, 46, "saith"),
        (47, 48, "the Lord."),
    ],
    17: [
        (0, 3, "And now, behold,"),
        (4, 6, "saith"),
        (7, 8, "the Lord,"),
        (9, 11, "concerning"),
        (12, 15, "the people of the Nephites:"),
        (16, 20, "If they will not repent,"),
        (21, 22, "and observe"),
        (23, 24, "to do"),
        (25, 26, "my will,"),
        (27, 33, "I will utterly destroy"),
        (34, 35, "them,"),
        (36, 39, "saith"),
        (40, 41, "the Lord,"),
        (42, 43, "because of"),
        (44, 47, "their unbelief"),
        (48, 50, "notwithstanding"),
        (51, 55, "the many mighty works"),
        (56, 58, "which I have done"),
        (59, 64, "among them;"),
        (65, 69, "and as surely as"),
        (70, 72, "liveth"),
        (73, 74, "the Lord,"),
        (75, 79, "shall surely come to pass"),
        (80, 81, "these things,"),
        (82, 85, "saith"),
        (86, 87, "the Lord."),
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
