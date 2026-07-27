"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 38 — Alma's charge
to his son Shiblon: commended for his steadiness and faithfulness among the
Zoramites; taught to trust in God for deliverance, to bridle his passions,
to refrain from idleness, and to preach the word with soberness.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split done up front against bom_books.json:
  v14 `mutimutivale—ioe,` -> 64 tokens

    python3 build_overrides_alma38.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 38

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "My son,"),
        (3, 6, "give ear"),
        (7, 9, "to my words,"),
        (10, 10, "for"),
        (11, 14, "I say"),
        (15, 17, "unto you,"),
        (18, 21, "even as I"),
        (22, 23, "said"),
        (24, 25, "unto Helaman,"),
        (26, 27, "that"),
        (28, 31, "inasmuch as"),
        (32, 35, "ye keep the commandments"),
        (36, 38, "of God"),
        (39, 43, "ye shall prosper"),
        (44, 46, "in the land;"),
        (47, 51, "and inasmuch as"),
        (52, 56, "ye keep not the commandments"),
        (57, 59, "of God"),
        (60, 65, "ye shall be cut off"),
        (66, 68, "from his presence."),
    ],
    2: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 8, "I trust"),
        (9, 13, "that I shall have"),
        (14, 16, "great joy"),
        (17, 19, "in you,"),
        (20, 23, "because of your steadiness"),
        (24, 26, "and your faithfulness"),
        (27, 29, "unto God;"),
        (30, 30, "for"),
        (31, 34, "as thou"),
        (35, 36, "hast commenced"),
        (37, 39, "in thy youth"),
        (40, 43, "to look"),
        (44, 48, "to the Lord thy God,"),
        (49, 54, "even so I hope"),
        (55, 59, "that thou wilt continue"),
        (60, 62, "in keeping"),
        (63, 65, "his commandments;"),
        (66, 66, "for"),
        (67, 71, "blessed is he"),
        (72, 75, "that endureth"),
        (76, 80, "to the end."),
    ],
    3: [
        (0, 3, "I say"),
        (4, 6, "unto you,"),
        (7, 9, "my son,"),
        (10, 14, "that I have had already"),
        (15, 18, "great joy"),
        (19, 21, "in thee,"),
        (22, 25, "because of thy faithfulness"),
        (26, 28, "and thy diligence,"),
        (29, 31, "and thy patience"),
        (32, 34, "and thy long-suffering"),
        (35, 37, "among"),
        (38, 40, "the people of the Zoramites."),
    ],
    4: [
        (0, 0, "For"),
        (1, 3, "I know"),
        (4, 7, "that thou wast"),
        (8, 9, "in bonds;"),
        (10, 10, "yea,"),
        (11, 15, "and I also know"),
        (16, 20, "that thou wast stoned"),
        (21, 24, "for the word's sake;"),
        (25, 28, "and thou didst bear"),
        (29, 31, "all these things"),
        (32, 34, "with patience"),
        (35, 35, "because"),
        (36, 39, "the Lord was"),
        (40, 41, "with thee;"),
        (42, 44, "and now"),
        (45, 47, "thou knowest"),
        (48, 50, "that the Lord"),
        (51, 53, "did deliver thee."),
    ],
    5: [
        (0, 2, "And now,"),
        (3, 5, "my son"),
        (6, 6, "Shiblon,"),
        (7, 9, "I would"),
        (10, 12, "that ye should remember,"),
        (13, 17, "as much as ye put"),
        (18, 19, "your trust"),
        (20, 22, "in God"),
        (23, 26, "even so much"),
        (27, 31, "he shall deliver"),
        (32, 32, "thee"),
        (33, 35, "out of thy trials,"),
        (36, 38, "and thy troubles,"),
        (39, 41, "and thy afflictions,"),
        (42, 48, "and thou shalt be lifted up"),
        (49, 52, "at the last day."),
    ],
    6: [
        (0, 1, "Now,"),
        (2, 4, "my son,"),
        (5, 8, "I would not"),
        (9, 11, "that ye should think"),
        (12, 13, "that"),
        (14, 18, "I know these things"),
        (19, 22, "of myself,"),
        (23, 27, "but the Spirit of"),
        (28, 29, "God"),
        (30, 35, "which is in me"),
        (36, 40, "which maketh known"),
        (41, 42, "these things"),
        (43, 45, "unto me;"),
        (46, 50, "for if I had not been born"),
        (51, 54, "of God,"),
        (55, 59, "I should not have known"),
        (60, 61, "these things."),
    ],
    7: [
        (0, 1, "But behold,"),
        (2, 4, "the Lord"),
        (5, 9, "in his great mercy"),
        (10, 14, "sent"),
        (15, 16, "his angel"),
        (17, 19, "to declare"),
        (20, 22, "unto me"),
        (23, 27, "that I must stop"),
        (28, 32, "the work of destruction"),
        (33, 37, "among his people;"),
        (38, 38, "yea,"),
        (39, 42, "and I have seen"),
        (43, 45, "an angel"),
        (46, 47, "face to face,"),
        (48, 52, "and he spake"),
        (53, 55, "with me,"),
        (56, 59, "and his voice"),
        (60, 64, "was as thunder,"),
        (65, 68, "and it shook"),
        (69, 71, "the whole earth."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 7, "I was"),
        (8, 11, "three days"),
        (12, 15, "and three nights"),
        (16, 19, "in the most bitter pain"),
        (20, 23, "and great anguish"),
        (24, 26, "of soul;"),
        (27, 31, "and I did not receive"),
        (32, 32, "at all"),
        (33, 35, "until"),
        (36, 38, "I did cry out"),
        (39, 44, "unto the Lord Jesus Christ"),
        (45, 48, "for mercy,"),
        (49, 52, "I received"),
        (53, 54, "a remission"),
        (55, 57, "of my sins."),
        (58, 59, "But behold,"),
        (60, 64, "I did cry"),
        (65, 67, "unto him"),
        (68, 71, "and I did find"),
        (72, 73, "peace"),
        (74, 76, "to my soul."),
    ],
    9: [
        (0, 2, "And now,"),
        (3, 5, "my son,"),
        (6, 9, "I have told"),
        (10, 12, "you"),
        (13, 14, "this thing"),
        (15, 20, "that ye may learn"),
        (21, 22, "wisdom,"),
        (23, 28, "that ye may learn"),
        (29, 32, "of me,"),
        (33, 36, "there is no other"),
        (37, 38, "way"),
        (39, 42, "or means"),
        (43, 47, "whereby can be saved"),
        (48, 50, "man,"),
        (51, 53, "only in him,"),
        (54, 58, "and through Christ."),
        (59, 59, "Behold,"),
        (60, 64, "he is the life"),
        (65, 67, "and the light"),
        (68, 70, "of the world."),
        (71, 71, "Behold,"),
        (72, 76, "he is the word"),
        (77, 79, "of truth"),
        (80, 82, "and righteousness."),
    ],
    10: [
        (0, 2, "And now,"),
        (3, 3, "as"),
        (4, 7, "ye have begun"),
        (8, 9, "to teach"),
        (10, 12, "the word"),
        (13, 15, "even so"),
        (16, 18, "I would"),
        (19, 23, "that ye should continue to teach;"),
        (24, 27, "and I would"),
        (28, 30, "that ye be diligent"),
        (31, 32, "and temperate"),
        (33, 35, "in all things."),
    ],
    11: [
        (0, 0, "See"),
        (1, 5, "that thou be not lifted up"),
        (6, 8, "up unto"),
        (9, 10, "pride;"),
        (11, 11, "yea,"),
        (12, 12, "see"),
        (13, 17, "that thou boast not"),
        (18, 21, "in thine own wisdom,"),
        (22, 26, "nor of thy much strength."),
    ],
    12: [
        (0, 2, "Use boldness,"),
        (3, 7, "but not overbearance;"),
        (8, 10, "and also see"),
        (11, 15, "that ye bridle all your passions,"),
        (16, 21, "that thou mayest be filled"),
        (22, 24, "with love;"),
        (25, 25, "see"),
        (26, 28, "that ye refrain"),
        (29, 31, "from idleness."),
    ],
    13: [
        (0, 3, "Do not pray"),
        (4, 7, "as do"),
        (8, 10, "the Zoramites,"),
        (11, 11, "for"),
        (12, 14, "ye have seen"),
        (15, 17, "that they pray"),
        (18, 21, "to be heard"),
        (22, 23, "of men,"),
        (24, 27, "and to be praised"),
        (28, 29, "them"),
        (30, 33, "for their wisdom."),
    ],
    14: [
        (0, 4, "Do not say:"),
        (5, 7, "O God,"),
        (8, 11, "I thank"),
        (12, 14, "thee"),
        (15, 18, "that better is"),
        (19, 21, "our goodness"),
        (22, 26, "than our brethren;"),
        (27, 30, "but say:"),
        (31, 33, "O Lord,"),
        (34, 38, "forgive my unworthiness,"),
        (39, 42, "and remember"),
        (43, 44, "my brethren"),
        (45, 48, "in mercy—"),
        (49, 49, "yea,"),
        (50, 54, "acknowledge thy unworthiness"),
        (55, 59, "before God"),
        (60, 63, "at all times."),
    ],
    15: [
        (0, 4, "And may the Lord"),
        (5, 7, "bless"),
        (8, 10, "thy soul,"),
        (11, 13, "and receive thee"),
        (14, 17, "at the last day"),
        (18, 20, "into his kingdom,"),
        (21, 24, "to sit down"),
        (25, 27, "in peace."),
        (28, 29, "Now"),
        (30, 31, "go,"),
        (32, 34, "my son,"),
        (35, 39, "and teach the word"),
        (40, 42, "unto this people."),
        (43, 46, "Be sober."),
        (47, 49, "My son,"),
        (50, 50, "farewell."),
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
