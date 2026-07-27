"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 12 — the Sermon at
the temple (Beatitudes and the higher law): Jesus calls the twelve, pronounces the
blessings on the poor in spirit, the mourners, the meek, the merciful, the pure in
heart, and the peacemakers; declares his disciples the salt of the earth and the
light of the world; testifies he came not to destroy the law but to fulfil it; and
raises the law from outward act to inward heart — anger, lust, oaths, retaliation,
and love of enemies — commanding them to be perfect even as the Father is perfect.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits were needed for this chapter.

    python3 build_overrides_3nephi12.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 12

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when Jesus had spoken"),
        (11, 12, "these words"),
        (13, 14, "unto Nephi,"),
        (15, 19, "and to those who"),
        (20, 21, "were called,"),
        (22, 23, "(now"),
        (24, 29, "the number of them"),
        (30, 33, "who were called,"),
        (34, 41, "and received power and authority"),
        (42, 45, "to baptize,"),
        (46, 47, "were twelve)"),
        (48, 50, "and behold,"),
        (51, 56, "he stretched forth his hand"),
        (57, 61, "unto the multitude,"),
        (62, 64, "and cried"),
        (65, 68, "unto them,"),
        (69, 71, "saying:"),
        (72, 73, "Blessed are ye"),
        (74, 79, "if ye give heed"),
        (80, 84, "to the words of these twelve"),
        (85, 89, "whom I have chosen"),
        (90, 94, "from among you"),
        (95, 97, "to minister"),
        (98, 100, "unto you,"),
        (101, 103, "and to be"),
        (104, 106, "your servants;"),
        (107, 110, "and unto them"),
        (111, 116, "I have given"),
        (117, 118, "the power"),
        (119, 126, "that they may baptize you"),
        (127, 129, "with water;"),
        (130, 136, "and after ye are baptized"),
        (137, 139, "with water,"),
        (140, 140, "behold,"),
        (141, 146, "I will baptize you"),
        (147, 153, "with fire and the Holy Ghost;"),
        (154, 155, "therefore"),
        (156, 158, "blessed are ye"),
        (159, 164, "if ye believe"),
        (165, 167, "in me"),
        (168, 169, "and be baptized,"),
        (170, 176, "after ye have seen"),
        (177, 179, "me"),
        (180, 186, "and know that I am."),
    ],
    2: [
        (0, 5, "And I say again,"),
        (6, 13, "more blessed are they"),
        (14, 17, "who believe"),
        (18, 20, "in your words"),
        (21, 27, "because ye will testify"),
        (28, 33, "ye have seen me,"),
        (34, 37, "and ye know"),
        (38, 42, "that I am."),
        (43, 43, "Yea,"),
        (44, 48, "blessed are they who"),
        (49, 53, "believe in your words,"),
        (54, 56, "and come down"),
        (57, 62, "into the depths of humility"),
        (63, 64, "and are baptized,"),
        (65, 71, "for they shall be visited"),
        (72, 78, "with fire and the Holy Ghost,"),
        (79, 84, "and shall receive"),
        (85, 86, "a remission"),
        (87, 90, "of their sins."),
    ],
    3: [
        (0, 0, "Yea,"),
        (1, 6, "blessed are the poor in spirit"),
        (7, 11, "who come"),
        (12, 14, "unto me,"),
        (15, 18, "for theirs is"),
        (19, 23, "the kingdom of heaven."),
    ],
    4: [
        (0, 5, "And I say again,"),
        (6, 11, "blessed are all they who"),
        (12, 13, "mourn,"),
        (14, 20, "for they shall be comforted."),
    ],
    5: [
        (0, 4, "And blessed are the meek,"),
        (5, 13, "for shall be for their inheritance"),
        (14, 15, "the earth."),
    ],
    6: [
        (0, 6, "And blessed are all they who"),
        (7, 12, "hunger and thirst"),
        (13, 15, "after righteousness,"),
        (16, 22, "for they shall be filled"),
        (23, 26, "with the Holy Ghost."),
    ],
    7: [
        (0, 5, "And blessed are the merciful,"),
        (6, 11, "for mercy shall be shown them."),
    ],
    8: [
        (0, 6, "And blessed are all they who"),
        (7, 9, "are pure in heart,"),
        (10, 15, "for they shall see"),
        (16, 18, "God."),
    ],
    9: [
        (0, 6, "And blessed are all they who"),
        (7, 10, "make peace,"),
        (11, 17, "for they shall be called"),
        (18, 22, "the children of God."),
    ],
    10: [
        (0, 6, "And blessed are all they who"),
        (7, 8, "are persecuted"),
        (9, 12, "for my name's sake,"),
        (13, 16, "for theirs is"),
        (17, 21, "the kingdom of heaven."),
    ],
    11: [
        (0, 2, "And blessed are ye"),
        (3, 9, "when they revile and persecute you"),
        (10, 11, "by men,"),
        (12, 19, "and say all manner of evil"),
        (20, 24, "against you"),
        (25, 29, "falsely accusing you,"),
        (30, 32, "because of me;"),
    ],
    12: [
        (0, 5, "For ye shall have"),
        (6, 8, "great joy"),
        (9, 12, "and exceeding gladness,"),
        (13, 17, "for great shall be"),
        (18, 20, "your reward"),
        (21, 23, "in heaven;"),
        (24, 29, "for so did they persecute"),
        (30, 33, "the prophets who"),
        (34, 38, "were before you."),
    ],
    13: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 14, "I give"),
        (15, 17, "unto you"),
        (18, 24, "to be the salt of the earth;"),
        (25, 28, "but if loses savor"),
        (29, 30, "the salt"),
        (31, 35, "with what thing"),
        (36, 40, "shall the earth be salted?"),
        (41, 47, "It shall from that time"),
        (48, 54, "be good for nothing"),
        (55, 56, "the salt,"),
        (57, 62, "but only to be cast out"),
        (63, 70, "and trodden under the feet of men."),
    ],
    14: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 14, "I give"),
        (15, 17, "unto you"),
        (18, 22, "that ye be the light"),
        (23, 25, "of this people."),
        (26, 30, "A city set"),
        (31, 35, "upon a hill"),
        (36, 40, "cannot be hid."),
    ],
    15: [
        (0, 0, "Behold,"),
        (1, 5, "do men light"),
        (6, 7, "a candle"),
        (8, 12, "and put under"),
        (13, 16, "a grain-box?"),
        (17, 18, "Nay,"),
        (19, 22, "but they set it"),
        (23, 27, "upon a candlestick,"),
        (28, 36, "and its light shall shine"),
        (37, 42, "to all who"),
        (43, 48, "are in the house."),
    ],
    16: [
        (0, 1, "Therefore"),
        (2, 8, "let your light so shine"),
        (9, 13, "before this people,"),
        (14, 18, "that they may see"),
        (19, 22, "your good works"),
        (23, 27, "and glorify your Father"),
        (28, 31, "who is in heaven."),
    ],
    17: [
        (0, 3, "Think not"),
        (4, 8, "I have come to destroy"),
        (9, 10, "the law"),
        (11, 13, "or the prophets."),
        (14, 19, "I have not come to destroy"),
        (20, 22, "but to fulfil;"),
    ],
    18: [
        (0, 0, "For"),
        (1, 6, "verily I say"),
        (7, 9, "unto you,"),
        (10, 14, "there has not passed away"),
        (15, 18, "one jot"),
        (19, 24, "nor one tittle"),
        (25, 27, "from the law,"),
        (28, 32, "but all has been fulfilled"),
        (33, 35, "in me."),
    ],
    19: [
        (0, 1, "And behold,"),
        (2, 8, "I have given unto you"),
        (9, 14, "the law and commandments of my Father,"),
        (15, 18, "that ye believe"),
        (19, 21, "in me,"),
        (22, 25, "and that ye repent"),
        (26, 28, "of your sins,"),
        (29, 34, "and come unto me"),
        (35, 38, "with a broken heart"),
        (39, 42, "and a contrite spirit."),
        (43, 43, "Behold,"),
        (44, 48, "there are before you"),
        (49, 49, "the commandments,"),
        (50, 54, "and the law is fulfilled."),
    ],
    20: [
        (0, 1, "Therefore"),
        (2, 8, "come ye unto me"),
        (9, 10, "and be saved;"),
        (11, 11, "for"),
        (12, 17, "verily I say"),
        (18, 20, "unto you,"),
        (21, 22, "except"),
        (23, 29, "ye keep my commandments"),
        (30, 35, "which I have commanded you"),
        (36, 38, "at this time,"),
        (39, 43, "there is no way"),
        (44, 52, "ye can enter"),
        (53, 58, "into the kingdom of heaven."),
    ],
    21: [
        (0, 2, "Ye have heard"),
        (3, 9, "it was said by those who"),
        (10, 12, "of ancient times,"),
        (13, 16, "and is also written"),
        (17, 20, "before you,"),
        (21, 25, "thou shalt not kill,"),
        (26, 33, "and whosoever kills"),
        (34, 38, "shall be in danger"),
        (39, 44, "of the judgment of God;"),
    ],
    22: [
        (0, 4, "But I say"),
        (5, 7, "unto you,"),
        (8, 12, "whosoever is angry"),
        (13, 15, "with his brother"),
        (16, 20, "shall be in danger"),
        (21, 23, "of his judgment."),
        (24, 31, "And whosoever says"),
        (32, 34, "to his brother,"),
        (35, 35, "Raca,"),
        (36, 40, "shall be in danger"),
        (41, 43, "of the council;"),
        (44, 51, "and whosoever says,"),
        (52, 53, "Thou fool,"),
        (54, 58, "shall be in danger"),
        (59, 63, "of hell fire."),
    ],
    23: [
        (0, 1, "Therefore,"),
        (2, 6, "if ye come"),
        (7, 9, "unto me,"),
        (10, 13, "or ye desire"),
        (14, 19, "to come unto me,"),
        (20, 22, "and thou rememberest"),
        (23, 30, "thy brother has something"),
        (31, 35, "against thee—"),
    ],
    24: [
        (0, 6, "Go thy way"),
        (7, 9, "unto thy brother,"),
        (10, 14, "and first be reconciled"),
        (15, 17, "to thy brother,"),
        (18, 23, "and then come thou"),
        (24, 26, "unto me"),
        (27, 33, "with full purpose of heart,"),
        (34, 40, "and I will receive you."),
    ],
    25: [
        (0, 4, "Quickly be reconciled"),
        (5, 7, "with thine enemy"),
        (8, 14, "while thou art in the way"),
        (15, 17, "together with him,"),
        (18, 22, "lest he seize thee"),
        (23, 25, "at some time,"),
        (26, 29, "and cast thee"),
        (30, 32, "into prison."),
    ],
    26: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto thee,"),
        (11, 14, "there is no way"),
        (15, 21, "thou shalt be let out"),
        (22, 24, "except"),
        (25, 28, "thou hast paid"),
        (29, 31, "every senine."),
        (32, 36, "And while thou art"),
        (37, 39, "in prison,"),
        (40, 45, "canst thou pay"),
        (46, 50, "one senine?"),
        (51, 54, "Verily, verily,"),
        (55, 58, "I say"),
        (59, 61, "unto thee,"),
        (62, 63, "Nay."),
    ],
    27: [
        (0, 0, "Behold,"),
        (1, 6, "it is written by those of"),
        (7, 8, "ancient times,"),
        (9, 12, "thou shalt not commit adultery;"),
    ],
    28: [
        (0, 4, "But I say"),
        (5, 7, "unto you,"),
        (8, 13, "whosoever looks"),
        (14, 16, "upon a woman,"),
        (17, 21, "to lust after her,"),
        (22, 27, "has already committed adultery"),
        (28, 30, "in his heart."),
    ],
    29: [
        (0, 0, "Behold,"),
        (1, 7, "I give unto you"),
        (8, 9, "a commandment,"),
        (10, 18, "that ye let not one of these things"),
        (19, 25, "enter into your heart;"),
    ],
    30: [
        (0, 4, "For it is better"),
        (5, 10, "that ye deny yourselves"),
        (11, 13, "of these things,"),
        (14, 22, "wherein ye will take up"),
        (23, 25, "your cross,"),
        (26, 27, "than"),
        (28, 33, "your being cast into hell."),
    ],
    31: [
        (0, 1, "It hath been written,"),
        (2, 8, "whosoever puts away"),
        (9, 11, "his wife,"),
        (12, 16, "let him give"),
        (17, 19, "unto her"),
        (20, 24, "a writing of divorcement."),
    ],
    32: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 16, "whosoever puts away"),
        (17, 19, "his wife,"),
        (20, 21, "except"),
        (22, 27, "for the cause of fornication,"),
        (28, 32, "he causes her to commit adultery;"),
        (33, 39, "and whoso marries"),
        (40, 44, "the woman who"),
        (45, 46, "is divorced,"),
        (47, 48, "commits adultery."),
    ],
    33: [
        (0, 3, "And again it is written,"),
        (4, 8, "thou shalt not swear falsely,"),
        (9, 11, "but perform"),
        (12, 13, "thine oaths"),
        (14, 16, "unto the Lord;"),
    ],
    34: [
        (0, 4, "But verily, verily,"),
        (5, 8, "I say"),
        (9, 11, "unto you,"),
        (12, 17, "swear not at all;"),
        (18, 22, "nor by heaven,"),
        (23, 30, "for it is the throne of God;"),
    ],
    35: [
        (0, 4, "Nor by the earth,"),
        (5, 11, "for his feet rest there;"),
    ],
    36: [
        (0, 5, "Neither swear thou"),
        (6, 8, "by thy head,"),
        (9, 15, "because thou canst not make black"),
        (16, 17, "or white"),
        (18, 21, "one hair;"),
    ],
    37: [
        (0, 5, "But let your communication be"),
        (6, 9, "only"),
        (10, 11, "Yea, yea;"),
        (12, 13, "Nay, nay;"),
        (14, 20, "for whatsoever is said"),
        (21, 26, "more than these,"),
        (27, 28, "is evil."),
    ],
    38: [
        (0, 1, "And behold,"),
        (2, 3, "it is written,"),
        (4, 9, "an eye for an eye,"),
        (10, 15, "and a tooth for a tooth;"),
    ],
    39: [
        (0, 4, "But I say"),
        (5, 7, "unto you,"),
        (8, 11, "resist ye not"),
        (12, 14, "evil,"),
        (15, 21, "but whosoever smites"),
        (22, 25, "on thy right cheek,"),
        (26, 29, "turn also"),
        (30, 32, "to him"),
        (33, 34, "the other;"),
    ],
    40: [
        (0, 6, "And if there be a man"),
        (7, 10, "who sues thee"),
        (11, 13, "at the law"),
        (14, 16, "and takes away"),
        (17, 18, "thy coat,"),
        (19, 25, "let him also have"),
        (26, 27, "thy cloak;"),
    ],
    41: [
        (0, 8, "And whosoever compels thee"),
        (9, 11, "to go"),
        (12, 16, "one mile,"),
        (17, 20, "go together with him"),
        (21, 24, "two miles."),
    ],
    42: [
        (0, 4, "Give to him"),
        (5, 9, "who asks"),
        (10, 12, "of thee,"),
        (13, 19, "and turn thou not away"),
        (20, 24, "from him who"),
        (25, 29, "would borrow"),
        (30, 32, "of thee."),
    ],
    43: [
        (0, 1, "And behold"),
        (2, 4, "it is also written,"),
        (5, 8, "thou shalt love"),
        (9, 11, "thy neighbor"),
        (12, 14, "and hate"),
        (15, 17, "thine enemy;"),
    ],
    44: [
        (0, 1, "But behold"),
        (2, 5, "I say"),
        (6, 8, "unto you,"),
        (9, 13, "love your enemies,"),
        (14, 20, "bless them who"),
        (21, 26, "curse you,"),
        (27, 33, "do good to them who"),
        (34, 40, "hate you,"),
        (41, 46, "and pray for them who"),
        (47, 54, "despitefully use you"),
        (55, 57, "and persecute you;"),
    ],
    45: [
        (0, 5, "That ye may be children"),
        (6, 9, "of your Father"),
        (10, 15, "who is in heaven;"),
        (16, 16, "for"),
        (17, 23, "he makes his sun rise"),
        (24, 29, "on the evil"),
        (30, 34, "and on the good."),
    ],
    46: [
        (0, 1, "Therefore"),
        (2, 7, "those things of ancient times,"),
        (8, 14, "which were under the law,"),
        (15, 17, "are all fulfilled"),
        (18, 20, "in me."),
    ],
    47: [
        (0, 4, "Old things are done away,"),
        (5, 9, "and all things have become new."),
    ],
    48: [
        (0, 1, "Therefore"),
        (2, 7, "I would that ye be perfect"),
        (8, 12, "even as I,"),
        (13, 17, "or your Father"),
        (18, 23, "who is in heaven"),
        (24, 25, "is perfect."),
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
