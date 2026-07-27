"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 13 — the Sermon at
the temple continued: Jesus teaches that alms, prayer, and fasting be done in
secret unto the Father, not for the praise of men; gives the pattern of prayer
(the Lord's Prayer) and the law of forgiveness; warns against laying up earthly
treasures and serving two masters; and (turning to the twelve) commands them to
take no thought for their lives — food, drink, or clothing — but to seek first the
kingdom of God, trusting the Father who feeds the birds and clothes the lilies.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi13.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 13

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 13, "I would that ye do"),
        (14, 15, "alms"),
        (16, 18, "unto the poor;"),
        (19, 22, "but take ye heed"),
        (23, 28, "that ye do not"),
        (29, 31, "your alms"),
        (32, 35, "before men"),
        (36, 41, "to be seen by them;"),
        (42, 43, "otherwise,"),
        (44, 48, "ye have no reward"),
        (49, 52, "from your Father"),
        (53, 58, "who is in heaven."),
    ],
    2: [
        (0, 1, "Therefore,"),
        (2, 5, "when ye do"),
        (6, 8, "your alms"),
        (9, 13, "sound not a trumpet"),
        (14, 17, "before you,"),
        (18, 23, "as the hypocrites do"),
        (24, 28, "in the synagogues"),
        (29, 31, "and in the streets,"),
        (32, 37, "that they may be glorified"),
        (38, 39, "by men."),
        (40, 45, "Verily I say"),
        (46, 48, "unto you,"),
        (49, 54, "they have their reward."),
    ],
    3: [
        (0, 4, "But when thou doest"),
        (5, 6, "alms,"),
        (7, 9, "let not know"),
        (10, 13, "thy left hand"),
        (14, 17, "what is done"),
        (18, 21, "by thy right hand;"),
    ],
    4: [
        (0, 4, "That may be secret"),
        (5, 6, "thine alms;"),
        (7, 10, "and thy Father"),
        (11, 15, "who sees"),
        (16, 17, "in secret,"),
        (18, 20, "he himself"),
        (21, 26, "shall reward thee openly."),
    ],
    5: [
        (0, 4, "And when thou prayest,"),
        (5, 8, "do thou not"),
        (9, 13, "as the hypocrites,"),
        (14, 14, "for"),
        (15, 19, "they love to pray,"),
        (20, 24, "standing in the synagogues"),
        (25, 28, "and the corners of the streets,"),
        (29, 33, "that they may be seen"),
        (34, 35, "by men."),
        (36, 41, "Verily I say"),
        (42, 44, "unto you,"),
        (45, 50, "they have their reward."),
    ],
    6: [
        (0, 1, "But thou,"),
        (2, 5, "when thou prayest,"),
        (6, 10, "enter into thy chamber,"),
        (11, 17, "and when thou hast shut"),
        (18, 20, "thy door,"),
        (21, 25, "pray to thy Father"),
        (26, 31, "who is in secret;"),
        (32, 35, "and thy Father,"),
        (36, 40, "who sees"),
        (41, 43, "in secret,"),
        (44, 49, "shall reward thee openly."),
    ],
    7: [
        (0, 4, "But when ye pray,"),
        (5, 8, "use not repeatedly"),
        (9, 12, "useless words,"),
        (13, 17, "as the heathen,"),
        (18, 21, "for they think"),
        (22, 27, "they shall be heard"),
        (28, 34, "for their many words."),
    ],
    8: [
        (0, 1, "Therefore"),
        (2, 6, "be ye not like"),
        (7, 9, "unto them,"),
        (10, 16, "for your Father knows"),
        (17, 20, "the things ye need"),
        (21, 26, "before ye have asked"),
        (27, 29, "him."),
    ],
    9: [
        (0, 1, "Therefore"),
        (2, 5, "in this manner"),
        (6, 10, "shall ye pray:"),
        (11, 14, "Our Father"),
        (15, 20, "who art in heaven,"),
        (21, 24, "hallowed be thy name."),
    ],
    10: [
        (0, 3, "Thy will be done"),
        (4, 6, "on earth"),
        (7, 10, "as it is done"),
        (11, 13, "in heaven."),
    ],
    11: [
        (0, 6, "And forgive us"),
        (7, 9, "our sins,"),
        (10, 15, "as we forgive"),
        (16, 20, "those who have wronged"),
        (21, 24, "us."),
    ],
    12: [
        (0, 6, "And lead us not"),
        (7, 9, "into temptation,"),
        (10, 14, "but deliver us"),
        (15, 17, "from evil."),
    ],
    13: [
        (0, 4, "For thine is the kingdom,"),
        (5, 7, "and the power,"),
        (8, 10, "and the glory,"),
        (11, 13, "forever."),
        (14, 14, "Amen."),
    ],
    14: [
        (0, 0, "For,"),
        (1, 5, "if ye forgive"),
        (6, 7, "men"),
        (8, 11, "their trespasses,"),
        (12, 17, "ye also shall be forgiven"),
        (18, 22, "by your heavenly Father."),
    ],
    15: [
        (0, 6, "But if ye forgive not"),
        (7, 8, "men"),
        (9, 12, "their trespasses"),
        (13, 18, "neither shall be forgiven"),
        (19, 22, "by your Father"),
        (23, 25, "your trespasses."),
    ],
    16: [
        (0, 2, "Moreover,"),
        (3, 6, "when ye fast"),
        (7, 10, "be ye not like"),
        (11, 13, "the hypocrites,"),
        (14, 16, "with a sad face,"),
        (17, 21, "for they disfigure"),
        (22, 24, "their faces"),
        (25, 31, "that they may appear to men"),
        (32, 36, "as if they fast."),
        (37, 42, "Verily I say"),
        (43, 45, "unto you,"),
        (46, 51, "they have their reward."),
    ],
    17: [
        (0, 1, "But thou,"),
        (2, 5, "when thou fastest,"),
        (6, 9, "anoint thy head,"),
        (10, 13, "and wash thy face;"),
    ],
    18: [
        (0, 6, "That thou appear not to men"),
        (7, 9, "as fasting,"),
        (10, 12, "only unto thy Father,"),
        (13, 18, "who is in secret;"),
        (19, 23, "and your Father,"),
        (24, 28, "who sees"),
        (29, 31, "in secret,"),
        (32, 37, "shall reward thee openly."),
    ],
    19: [
        (0, 3, "Lay not up"),
        (4, 7, "for yourselves treasures"),
        (8, 10, "upon earth,"),
        (11, 16, "where there is"),
        (17, 21, "moth and rust"),
        (22, 23, "that corrupt,"),
        (24, 28, "and thieves break in"),
        (29, 31, "and steal;"),
    ],
    20: [
        (0, 3, "But lay up"),
        (4, 7, "for yourselves treasures"),
        (8, 10, "in heaven,"),
        (11, 18, "where there is no"),
        (19, 24, "moth nor rust"),
        (25, 26, "that corrupts,"),
        (27, 32, "and thieves break not in"),
        (33, 34, "nor steal."),
    ],
    21: [
        (0, 6, "For where there is"),
        (7, 8, "your treasure,"),
        (9, 10, "there"),
        (11, 16, "shall be also"),
        (17, 18, "your heart."),
    ],
    22: [
        (0, 5, "The light of the body"),
        (6, 8, "is the eye;"),
        (9, 10, "therefore,"),
        (11, 14, "if be focused as one"),
        (15, 16, "thine eye,"),
        (17, 23, "thy whole body shall be full"),
        (24, 26, "of light."),
    ],
    23: [
        (0, 3, "But if be evil"),
        (4, 5, "thine eye,"),
        (6, 12, "thy whole body shall be full"),
        (13, 15, "of darkness."),
        (16, 17, "Therefore,"),
        (18, 21, "if the light"),
        (22, 27, "that is in thee"),
        (28, 30, "be darkness,"),
        (31, 36, "how exceedingly great is"),
        (37, 38, "that darkness!"),
    ],
    24: [
        (0, 7, "No man can serve"),
        (8, 11, "two masters;"),
        (12, 18, "for he will hate"),
        (19, 21, "the one"),
        (22, 26, "and love the other;"),
        (27, 30, "or else"),
        (31, 35, "he will be loyal"),
        (36, 38, "to the one"),
        (39, 43, "and despise the other."),
        (44, 49, "Ye cannot serve"),
        (50, 54, "God and Mammon."),
    ],
    25: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 11, "when Jesus had spoken"),
        (12, 13, "these words"),
        (14, 18, "he looked"),
        (19, 23, "upon the twelve whom"),
        (24, 26, "he had chosen,"),
        (27, 29, "and said"),
        (30, 33, "unto them:"),
        (34, 36, "Remember ye"),
        (37, 38, "the words which"),
        (39, 43, "I have spoken."),
        (44, 45, "For behold,"),
        (46, 50, "ye are they whom"),
        (51, 53, "I have chosen"),
        (54, 59, "to minister unto this people."),
        (60, 61, "Therefore"),
        (62, 66, "I say"),
        (67, 69, "unto you,"),
        (70, 73, "take no thought"),
        (74, 77, "for your lives,"),
        (78, 85, "what ye shall eat,"),
        (86, 94, "or what ye shall drink;"),
        (95, 100, "nor for your bodies,"),
        (101, 108, "what ye shall wear."),
        (109, 116, "Is not the life greater"),
        (117, 119, "than food,"),
        (120, 122, "and the body"),
        (123, 125, "than raiment?"),
    ],
    26: [
        (0, 5, "Behold the birds of the air,"),
        (6, 10, "for they sow not,"),
        (11, 12, "nor reap"),
        (13, 16, "nor gather into barns;"),
        (17, 21, "yet they are fed"),
        (22, 26, "by your heavenly Father."),
        (27, 32, "Are ye not much greater"),
        (33, 35, "your worth"),
        (36, 39, "than theirs?"),
    ],
    27: [
        (0, 4, "Which of you"),
        (5, 9, "can add"),
        (10, 12, "by thinking"),
        (13, 16, "one cubit"),
        (17, 19, "to his height?"),
    ],
    28: [
        (0, 5, "And why take ye thought"),
        (6, 7, "for raiment?"),
        (8, 12, "Consider the lilies of the field"),
        (13, 20, "and how they grow;"),
        (21, 24, "they toil not,"),
        (25, 29, "neither do they spin;"),
    ],
    29: [
        (0, 4, "And yet I say"),
        (5, 7, "unto you,"),
        (8, 12, "even Solomon,"),
        (13, 16, "in all his glory,"),
        (17, 19, "was not clothed"),
        (20, 24, "like one"),
        (25, 28, "of these."),
    ],
    30: [
        (0, 1, "Wherefore,"),
        (2, 9, "if God so clothes"),
        (10, 13, "the grass of the field,"),
        (14, 20, "which is today,"),
        (21, 24, "and tomorrow"),
        (25, 30, "is cast into the oven,"),
        (31, 40, "even so will he clothe you,"),
        (41, 47, "if ye are not of little faith."),
    ],
    31: [
        (0, 1, "Therefore,"),
        (2, 5, "take no thought"),
        (6, 8, "saying,"),
        (9, 17, "What shall we eat?"),
        (18, 27, "or, What shall we drink?"),
        (28, 37, "or, Wherewithal shall we be clothed?"),
    ],
    32: [
        (0, 2, "For knows"),
        (3, 7, "your heavenly Father"),
        (8, 10, "ye have need of"),
        (11, 13, "all these things."),
    ],
    33: [
        (0, 4, "But seek ye first"),
        (5, 9, "the kingdom of God"),
        (10, 12, "and his righteousness,"),
        (13, 18, "and shall be added"),
        (19, 21, "unto you"),
        (22, 24, "all these things."),
    ],
    34: [
        (0, 1, "Therefore"),
        (2, 5, "take no thought"),
        (6, 10, "for the morrow,"),
        (11, 19, "for the morrow shall take thought"),
        (20, 24, "for its own things."),
        (25, 29, "Sufficient is the day"),
        (30, 32, "for its own evils."),
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
