"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 29 — Alma's
psalm: he desires to be an angel and cry repentance to every people, but
rejoices instead in what the Lord has allotted him; he glories in the
success of his fellow laborers and gives thanks for the conversion of the
Lamanites.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), `mafai ona`/`ina ia`/
`e tatau ona` bound (rules 13/15).

    python3 build_overrides_alma29.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 29

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 0, "O,"),
        (1, 4, "that I were"),
        (5, 7, "an angel,"),
        (8, 12, "and could have"),
        (13, 17, "the wish of my heart,"),
        (18, 22, "that I might"),
        (23, 24, "go forth"),
        (25, 27, "and speak"),
        (28, 31, "with the trump of"),
        (32, 33, "God,"),
        (34, 37, "and with a voice"),
        (38, 42, "to shake the earth,"),
        (43, 47, "and cry repentance"),
        (48, 50, "unto every people!"),
    ],
    2: [
        (0, 0, "Yea,"),
        (1, 5, "I would declare"),
        (6, 9, "unto every soul,"),
        (10, 12, "with a voice"),
        (13, 17, "like the thunder,"),
        (18, 19, "repentance"),
        (20, 23, "and the plan of"),
        (24, 25, "redemption,"),
        (26, 29, "that they should repent"),
        (30, 33, "and come unto"),
        (34, 36, "our God,"),
        (37, 40, "that no more"),
        (41, 42, "there be"),
        (43, 44, "sorrow"),
        (45, 47, "upon"),
        (48, 50, "all the earth."),
    ],
    3: [
        (0, 1, "But behold,"),
        (2, 3, "I am"),
        (4, 6, "a man,"),
        (7, 10, "and I sin"),
        (11, 13, "in my wish;"),
        (14, 14, "for"),
        (15, 19, "I ought to be content"),
        (20, 21, "with the things"),
        (22, 25, "which are given by"),
        (26, 27, "the Lord"),
        (28, 30, "unto me."),
    ],
    4: [
        (0, 4, "I ought not"),
        (5, 5, "to alter"),
        (6, 8, "in my desires"),
        (9, 12, "the firm decree of"),
        (13, 15, "a just God,"),
        (16, 16, "for"),
        (17, 19, "I know"),
        (20, 24, "that he granteth"),
        (25, 26, "unto men"),
        (27, 29, "according to"),
        (30, 32, "their desire,"),
        (33, 36, "whether unto death"),
        (37, 40, "or unto life;"),
        (41, 41, "yea,"),
        (42, 44, "I know"),
        (45, 49, "that he allotteth"),
        (50, 51, "unto men,"),
        (52, 52, "yea,"),
        (53, 57, "he decreeth"),
        (58, 61, "unto them"),
        (62, 65, "decrees unalterable,"),
        (66, 68, "according to"),
        (69, 71, "their wills,"),
        (72, 76, "whether they be"),
        (77, 79, "unto salvation"),
        (80, 83, "or unto destruction."),
    ],
    5: [
        (0, 0, "Yea,"),
        (1, 4, "and I know"),
        (5, 7, "have come"),
        (8, 12, "good and evil"),
        (13, 15, "before"),
        (16, 17, "all men;"),
        (18, 21, "he that"),
        (22, 25, "knoweth not"),
        (26, 30, "good from evil"),
        (31, 33, "is blameless;"),
        (34, 38, "but he that"),
        (39, 41, "knoweth"),
        (42, 46, "good and evil,"),
        (47, 49, "it is given"),
        (50, 52, "unto him"),
        (53, 55, "according to"),
        (56, 57, "his desires,"),
        (58, 61, "whether he desireth"),
        (62, 64, "good"),
        (65, 68, "or evil,"),
        (69, 70, "life"),
        (71, 74, "or death,"),
        (75, 76, "joy"),
        (77, 81, "or the remorse of"),
        (82, 83, "conscience."),
    ],
    6: [
        (0, 1, "Now,"),
        (2, 4, "seeing"),
        (5, 7, "that I know"),
        (8, 9, "these things,"),
        (10, 10, "why"),
        (11, 15, "should I desire more"),
        (16, 20, "than the doing of"),
        (21, 22, "the work"),
        (23, 26, "to which I am called?"),
    ],
    7: [
        (0, 0, "Why"),
        (1, 4, "should I desire"),
        (5, 9, "that I were"),
        (10, 12, "an angel,"),
        (13, 17, "that I might"),
        (18, 20, "speak"),
        (21, 24, "unto all the ends of"),
        (25, 26, "the earth?"),
    ],
    8: [
        (0, 1, "For behold,"),
        (2, 5, "is granted by"),
        (6, 7, "the Lord"),
        (8, 10, "unto all nations"),
        (11, 15, "of their own nation"),
        (16, 17, "and tongue,"),
        (18, 22, "that they teach"),
        (23, 24, "his word,"),
        (25, 25, "yea,"),
        (26, 28, "in wisdom"),
        (29, 31, "all things"),
        (32, 34, "which he seeth fit"),
        (35, 39, "that they should have;"),
        (40, 41, "therefore"),
        (42, 45, "we see"),
        (46, 50, "that the Lord doth counsel"),
        (51, 53, "in wisdom,"),
        (54, 58, "according to that which"),
        (59, 62, "is just and true."),
    ],
    9: [
        (0, 2, "I know"),
        (3, 4, "that which"),
        (5, 8, "hath commanded me"),
        (9, 11, "by the Lord,"),
        (12, 16, "and I glory in it."),
        (17, 20, "I do not glory"),
        (21, 25, "of myself,"),
        (26, 29, "but I glory"),
        (30, 32, "in that which"),
        (33, 36, "hath commanded me"),
        (37, 39, "by the Lord;"),
        (40, 40, "yea,"),
        (41, 45, "and this is my glory,"),
        (46, 51, "that perhaps I may become"),
        (52, 54, "an instrument"),
        (55, 59, "in the hands of God"),
        (60, 64, "to bring some soul"),
        (65, 67, "to repentance;"),
        (68, 72, "and this is my joy."),
    ],
    10: [
        (0, 1, "And behold,"),
        (2, 5, "when I see"),
        (6, 9, "many of"),
        (10, 11, "my brethren"),
        (12, 14, "truly penitent,"),
        (15, 19, "and coming to"),
        (20, 24, "the Lord their God,"),
        (25, 28, "then is filled"),
        (29, 31, "my soul"),
        (32, 34, "with joy;"),
        (35, 38, "then do I remember"),
        (39, 42, "the things done"),
        (43, 45, "by the Lord"),
        (46, 47, "for me,"),
        (48, 48, "yea,"),
        (49, 52, "even unto"),
        (53, 55, "his hearing"),
        (56, 58, "of my prayer;"),
        (59, 59, "yea,"),
        (60, 64, "then do I remember"),
        (65, 69, "his merciful arm"),
        (70, 73, "which he extended"),
        (74, 76, "towards me."),
    ],
    11: [
        (0, 0, "Yea,"),
        (1, 5, "and I also remember"),
        (6, 8, "the captivity of"),
        (9, 10, "my fathers;"),
        (11, 11, "for"),
        (12, 16, "I surely do know"),
        (17, 20, "that they were delivered"),
        (21, 23, "by the Lord"),
        (24, 26, "out of bondage,"),
        (27, 30, "and by this thing"),
        (31, 34, "he established"),
        (35, 36, "his church;"),
        (37, 37, "yea,"),
        (38, 42, "the Lord God,"),
        (43, 47, "the God of Abraham,"),
        (48, 52, "the God of Isaac,"),
        (53, 57, "and the God of Jacob,"),
        (58, 61, "did deliver them"),
        (62, 64, "out of bondage."),
    ],
    12: [
        (0, 0, "Yea,"),
        (1, 4, "I have always remembered"),
        (5, 7, "the captivity of"),
        (8, 9, "my fathers;"),
        (10, 14, "and that same God"),
        (15, 16, "the one"),
        (17, 20, "who delivered"),
        (21, 22, "them"),
        (23, 27, "out of the hands of the Egyptians,"),
        (28, 31, "did deliver them"),
        (32, 34, "out of bondage."),
    ],
    13: [
        (0, 0, "Yea,"),
        (1, 5, "and that same God"),
        (6, 7, "the one"),
        (8, 11, "did establish his church"),
        (12, 16, "among them;"),
        (17, 17, "yea,"),
        (18, 22, "and that same God"),
        (23, 25, "hath called me"),
        (26, 29, "by a holy calling,"),
        (30, 34, "to preach his word"),
        (35, 37, "unto this people,"),
        (38, 40, "and hath given"),
        (41, 43, "unto me"),
        (44, 46, "great success,"),
        (47, 49, "in the which"),
        (50, 52, "is full"),
        (53, 54, "my joy."),
    ],
    14: [
        (0, 0, "But"),
        (1, 4, "not alone in"),
        (5, 7, "my own success"),
        (8, 11, "do I rejoice,"),
        (12, 17, "but greater is the fulness"),
        (18, 20, "of my joy"),
        (21, 25, "because of the success of"),
        (26, 27, "my brethren,"),
        (28, 32, "who went up"),
        (33, 33, "to"),
        (34, 37, "the land of Nephi."),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 4, "they have labored exceedingly,"),
        (5, 9, "and have brought forth fruit"),
        (10, 11, "much;"),
        (12, 17, "and how great shall be"),
        (18, 20, "their reward!"),
    ],
    16: [
        (0, 1, "Now,"),
        (2, 6, "when I think of"),
        (7, 9, "the success of"),
        (10, 12, "these my brethren"),
        (13, 16, "is carried away"),
        (17, 18, "my soul,"),
        (19, 21, "even unto"),
        (22, 27, "as though it were separated"),
        (28, 28, "thereby"),
        (29, 31, "from the body,"),
        (32, 35, "as it were,"),
        (36, 40, "so exceedingly great is"),
        (41, 42, "my joy."),
    ],
    17: [
        (0, 2, "And now"),
        (3, 5, "may it be"),
        (6, 9, "that be granted by"),
        (10, 11, "God"),
        (12, 16, "unto these,"),
        (17, 19, "my brethren,"),
        (20, 23, "that they may"),
        (24, 25, "sit down"),
        (26, 29, "in the kingdom of"),
        (30, 31, "God;"),
        (32, 32, "yea,"),
        (33, 37, "and also all of them"),
        (38, 39, "who"),
        (40, 42, "are the fruit of"),
        (43, 45, "their labors,"),
        (46, 50, "that they no more"),
        (51, 52, "go out"),
        (53, 57, "but that they may"),
        (58, 60, "praise him"),
        (61, 62, "forever;"),
        (63, 66, "and may it be"),
        (67, 70, "that be granted by"),
        (71, 72, "God"),
        (73, 74, "that it be done"),
        (75, 79, "according to my words,"),
        (80, 84, "even as I"),
        (85, 87, "have spoken."),
        (88, 88, "Amen."),
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
