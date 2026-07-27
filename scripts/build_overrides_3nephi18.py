"""
Hand-curated TAM-phrase gloss overrides for 3 Nifae (3 Nephi) 18 — Jesus institutes
the sacrament of bread and wine as a witness and remembrance of his body and blood;
he teaches the people to always pray to the Father in his name, warns that the
worthy alone should partake, forbids casting out any from their meetings, commands
them to hold up their light and pray always lest they be tempted and led captive by
Satan; he gives the twelve power to bestow the Holy Ghost, touches them one by one,
and departs, a cloud overshadowing the multitude as he ascends into heaven.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

Em-dash pre-split applied to bom_books.json before glossing:
    18:24  luga—mea  ->  luga—  +  mea

    python3 build_overrides_3nephi18.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "3nephi"
CHAPTER_NUM = 18

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 6, "And Jesus commanded"),
        (7, 9, "his disciples"),
        (10, 14, "that they bring bread"),
        (15, 17, "and wine"),
        (18, 20, "unto him."),
    ],
    2: [
        (0, 5, "And while they went"),
        (6, 11, "for the bread and the wine,"),
        (12, 15, "he commanded"),
        (16, 20, "the multitude"),
        (21, 25, "that they sit down"),
        (26, 30, "upon the earth."),
    ],
    3: [
        (0, 6, "And when his disciples came"),
        (7, 11, "with bread and wine,"),
        (12, 15, "he took"),
        (16, 18, "of the bread"),
        (19, 20, "and brake it"),
        (21, 22, "and blessed it;"),
        (23, 26, "and he gave"),
        (27, 30, "unto the disciples"),
        (31, 33, "and commanded"),
        (34, 36, "that they eat."),
    ],
    4: [
        (0, 6, "And when they had eaten"),
        (7, 8, "and were filled,"),
        (9, 12, "he commanded"),
        (13, 15, "that they give"),
        (16, 20, "unto the multitude."),
    ],
    5: [
        (0, 7, "And when had eaten and were filled"),
        (8, 11, "the multitude,"),
        (12, 15, "he said"),
        (16, 19, "unto the disciples:"),
        (20, 20, "Behold,"),
        (21, 27, "there is one among you"),
        (28, 31, "who shall be ordained,"),
        (32, 34, "and to him"),
        (35, 42, "will I give"),
        (43, 44, "the power"),
        (45, 49, "that he break"),
        (50, 51, "the bread"),
        (52, 55, "and bless it"),
        (56, 57, "and give it"),
        (58, 62, "unto the people of my church,"),
        (63, 68, "unto all those who"),
        (69, 74, "shall believe and be baptized"),
        (75, 77, "in my name."),
    ],
    6: [
        (0, 7, "And ye shall observe to do this thing"),
        (8, 10, "continually,"),
        (11, 16, "even as I have done,"),
        (17, 22, "even as I have broken"),
        (23, 24, "the bread"),
        (25, 28, "and blessed it"),
        (29, 30, "and given it"),
        (31, 33, "unto you."),
    ],
    7: [
        (0, 5, "And ye shall do this thing"),
        (6, 11, "in remembrance of my body,"),
        (12, 16, "which I have shown"),
        (17, 19, "unto you."),
        (20, 28, "And it shall become a testimony"),
        (29, 31, "unto the Father"),
        (32, 36, "that ye always remember me."),
        (37, 43, "And if ye always remember me"),
        (44, 49, "ye shall have my Spirit"),
        (50, 54, "to be with you."),
    ],
    8: [
        (0, 3, "And it came to pass that"),
        (4, 9, "when he had spoken"),
        (10, 12, "these words,"),
        (13, 16, "he commanded"),
        (17, 19, "his disciples"),
        (20, 23, "that they take wine"),
        (24, 27, "from the cup"),
        (28, 30, "and drink it,"),
        (31, 35, "and that they also give it"),
        (36, 40, "unto the multitude"),
        (41, 45, "that they drink it."),
    ],
    9: [
        (0, 7, "And thus they did,"),
        (8, 11, "and they drank"),
        (12, 15, "and were satisfied;"),
        (16, 19, "and they gave it"),
        (20, 24, "unto the multitude,"),
        (25, 28, "and they drank,"),
        (29, 33, "and they were satisfied."),
    ],
    10: [
        (0, 9, "And when the disciples had done"),
        (10, 11, "this thing,"),
        (12, 15, "Jesus said"),
        (16, 19, "unto them:"),
        (20, 22, "Blessed are ye"),
        (23, 26, "because of this thing"),
        (27, 29, "which ye have done,"),
        (30, 33, "for this thing"),
        (34, 40, "is the fulfilling of my commandments,"),
        (41, 44, "and this thing"),
        (45, 48, "witnesses"),
        (49, 51, "unto the Father"),
        (52, 56, "ye are willing to do"),
        (57, 63, "what I have commanded you."),
    ],
    11: [
        (0, 3, "And this thing"),
        (4, 9, "ye shall always do"),
        (10, 15, "unto those who"),
        (16, 19, "repent and are baptized"),
        (20, 22, "in my name;"),
        (23, 26, "and ye shall do it"),
        (27, 31, "in remembrance of my blood,"),
        (32, 35, "which I have shed"),
        (36, 37, "for you,"),
        (38, 43, "that ye may witness"),
        (44, 46, "unto the Father"),
        (47, 51, "that ye always remember me."),
        (52, 58, "And if ye always remember me"),
        (59, 64, "ye shall have my Spirit"),
        (65, 69, "to be with you."),
    ],
    12: [
        (0, 7, "And I give unto you"),
        (8, 9, "a commandment"),
        (10, 14, "that ye do these things."),
        (15, 22, "And if ye always do these things,"),
        (23, 25, "blessed are ye,"),
        (26, 29, "for ye are built"),
        (30, 34, "upon my rock."),
    ],
    13: [
        (0, 4, "But whosoever"),
        (5, 10, "among you"),
        (11, 15, "does something"),
        (16, 21, "more or less"),
        (22, 25, "than these things,"),
        (26, 28, "is not built"),
        (29, 33, "upon my rock,"),
        (34, 36, "but is built"),
        (37, 42, "upon a sandy foundation;"),
        (43, 48, "and when the rain falls,"),
        (49, 52, "and the floods come,"),
        (53, 56, "and the winds blow,"),
        (57, 61, "and beat upon them,"),
        (62, 68, "they shall fall down,"),
        (69, 72, "and are already opened"),
        (73, 76, "the gates of hell"),
        (77, 80, "to receive them."),
    ],
    14: [
        (0, 1, "Therefore"),
        (2, 4, "blessed are ye"),
        (5, 9, "if ye keep"),
        (10, 11, "my commandments,"),
        (12, 19, "which the Father commanded me"),
        (20, 23, "that I give"),
        (24, 26, "unto you."),
    ],
    15: [
        (0, 3, "Verily, verily,"),
        (4, 7, "I say"),
        (8, 10, "unto you,"),
        (11, 15, "ye must watch"),
        (16, 20, "and pray always,"),
        (21, 23, "lest ye be tempted"),
        (24, 26, "by the devil,"),
        (27, 32, "and ye be led away"),
        (33, 35, "captive by him."),
    ],
    16: [
        (0, 6, "And as I have prayed"),
        (7, 9, "with you"),
        (10, 15, "even so shall ye pray"),
        (16, 18, "in my church,"),
        (19, 24, "among my people who"),
        (25, 29, "repent and are baptized"),
        (30, 32, "in my name."),
        (33, 33, "Behold,"),
        (34, 38, "I am the light;"),
        (39, 43, "I have set an example"),
        (44, 45, "for you."),
    ],
    17: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when Jesus had spoken"),
        (11, 13, "these words"),
        (14, 16, "unto his disciples,"),
        (17, 22, "he turned again"),
        (23, 27, "unto the multitude"),
        (28, 30, "and said"),
        (31, 34, "unto them:"),
    ],
    18: [
        (0, 0, "Behold,"),
        (1, 4, "verily, verily,"),
        (5, 8, "I say"),
        (9, 11, "unto you,"),
        (12, 16, "ye must watch"),
        (17, 21, "and pray always"),
        (22, 27, "lest ye enter into temptation;"),
        (28, 31, "for Satan desires"),
        (32, 34, "to have you,"),
        (35, 40, "that he may sift you"),
        (41, 44, "as wheat."),
    ],
    19: [
        (0, 1, "Therefore"),
        (2, 9, "ye must always pray"),
        (10, 12, "unto the Father"),
        (13, 15, "in my name;"),
    ],
    20: [
        (0, 4, "And whatsoever"),
        (5, 9, "ye shall ask"),
        (10, 12, "of the Father"),
        (13, 15, "in my name,"),
        (16, 17, "being right,"),
        (18, 19, "and believing"),
        (20, 24, "ye shall receive,"),
        (25, 25, "behold,"),
        (26, 31, "it shall surely be given"),
        (32, 34, "unto you."),
    ],
    21: [
        (0, 5, "Pray always"),
        (6, 8, "unto the Father,"),
        (9, 12, "in your families,"),
        (13, 15, "in my name,"),
        (16, 18, "that be blessed"),
        (19, 21, "your wives"),
        (22, 25, "and your children."),
    ],
    22: [
        (0, 1, "And behold,"),
        (2, 5, "ye shall gather together"),
        (6, 8, "often;"),
        (9, 15, "and forbid ye not"),
        (16, 20, "any man from coming"),
        (21, 23, "unto you"),
        (24, 28, "when ye gather together,"),
        (29, 33, "but allow them"),
        (34, 39, "that they may come"),
        (40, 42, "unto you"),
        (43, 48, "and forbid them not."),
    ],
    23: [
        (0, 3, "But ye shall pray"),
        (4, 6, "for them,"),
        (7, 14, "and cast them not out;"),
        (15, 23, "and if they come often"),
        (24, 26, "unto you"),
        (27, 29, "ye shall pray"),
        (30, 32, "unto the Father"),
        (33, 35, "for them,"),
        (36, 38, "in my name."),
    ],
    24: [
        (0, 1, "Therefore,"),
        (2, 8, "hold up your light"),
        (9, 12, "that it may shine"),
        (13, 15, "unto the world."),
        (16, 16, "Behold,"),
        (17, 22, "I am the light which"),
        (23, 29, "ye must hold up—"),
        (30, 34, "the things ye saw"),
        (35, 37, "I did."),
        (38, 38, "Behold"),
        (39, 41, "ye saw"),
        (42, 45, "I prayed"),
        (46, 48, "unto the Father,"),
        (49, 53, "and ye all witnessed it."),
    ],
    25: [
        (0, 3, "And ye see"),
        (4, 6, "I commanded"),
        (7, 15, "that none of you"),
        (16, 19, "go away,"),
        (20, 24, "but I commanded"),
        (25, 28, "that ye come"),
        (29, 31, "unto me,"),
        (32, 37, "that ye might feel and see;"),
        (38, 43, "even so shall ye do"),
        (44, 46, "unto the world;"),
        (47, 54, "and whoso breaks"),
        (55, 56, "this commandment"),
        (57, 62, "suffers himself"),
        (63, 67, "to be led into temptation."),
    ],
    26: [
        (0, 2, "And now"),
        (3, 5, "it came to pass that"),
        (6, 11, "when Jesus had spoken"),
        (12, 14, "these words,"),
        (15, 21, "he turned his eyes again"),
        (22, 27, "upon the disciples whom"),
        (28, 30, "he had chosen,"),
        (31, 33, "and said"),
        (34, 37, "unto them:"),
    ],
    27: [
        (0, 0, "Behold"),
        (1, 4, "verily, verily,"),
        (5, 8, "I say"),
        (9, 11, "unto you,"),
        (12, 18, "I give unto you"),
        (19, 21, "another commandment,"),
        (22, 29, "and then I must go"),
        (30, 32, "unto my Father"),
        (33, 38, "that I may fulfil"),
        (39, 41, "other commandments which"),
        (42, 48, "he gave me."),
    ],
    28: [
        (0, 3, "And now behold,"),
        (4, 7, "this is the commandment"),
        (8, 14, "which I give unto you,"),
        (15, 21, "that ye not knowingly allow"),
        (22, 26, "any one to partake"),
        (27, 29, "unworthily"),
        (30, 35, "of my flesh and blood,"),
        (36, 40, "when ye distribute it;"),
    ],
    29: [
        (0, 4, "For whosoever"),
        (5, 9, "eats of my flesh"),
        (10, 14, "and drinks of my blood"),
        (15, 17, "unworthily"),
        (18, 23, "eats and drinks"),
        (24, 25, "damnation"),
        (26, 28, "to his soul;"),
        (29, 32, "therefore,"),
        (33, 36, "if ye know"),
        (37, 41, "a man is unworthy"),
        (42, 45, "to eat and drink"),
        (46, 51, "of my flesh and blood"),
        (52, 57, "ye shall forbid him."),
    ],
    30: [
        (0, 3, "Nevertheless,"),
        (4, 12, "cast him not out"),
        (13, 16, "from among you,"),
        (17, 20, "but ye shall minister"),
        (21, 23, "unto him,"),
        (24, 27, "and pray for him"),
        (28, 30, "unto the Father,"),
        (31, 33, "in my name;"),
        (34, 39, "and if he repents"),
        (40, 44, "and is baptized in my name,"),
        (45, 50, "then shall ye receive him,"),
        (51, 56, "and give unto him"),
        (57, 61, "my flesh and blood."),
    ],
    31: [
        (0, 6, "But if he repents not,"),
        (7, 11, "let him not be numbered"),
        (12, 15, "among my people,"),
        (16, 21, "that he destroy not"),
        (22, 23, "my people,"),
        (24, 25, "for behold,"),
        (26, 30, "I know my sheep,"),
        (31, 35, "and they are numbered."),
    ],
    32: [
        (0, 4, "Nevertheless,"),
        (5, 12, "cast him not out"),
        (13, 16, "from your synagogues,"),
        (17, 23, "or your places of worship,"),
        (24, 27, "for unto such people"),
        (28, 33, "ye shall continue to labor;"),
        (34, 38, "for ye know not"),
        (39, 46, "whether they will return"),
        (47, 48, "and repent,"),
        (49, 54, "and come unto me"),
        (55, 61, "with full purpose of heart,"),
        (62, 70, "and I shall heal them;"),
        (71, 78, "and ye shall become the means"),
        (79, 83, "of bringing salvation"),
        (84, 87, "unto them."),
    ],
    33: [
        (0, 1, "Therefore,"),
        (2, 6, "keep ye these words"),
        (7, 11, "which I have commanded you"),
        (12, 17, "that ye come not down"),
        (18, 20, "into condemnation;"),
        (21, 23, "for wo"),
        (24, 27, "unto him whom"),
        (28, 33, "the Father condemns."),
    ],
    34: [
        (0, 7, "And I give unto you"),
        (8, 9, "these commandments"),
        (10, 13, "because of the disputes which"),
        (14, 21, "have been among you."),
        (22, 25, "And blessed are ye"),
        (26, 31, "if there be no disputes"),
        (32, 36, "among you."),
    ],
    35: [
        (0, 2, "And now"),
        (3, 8, "I go"),
        (9, 11, "unto the Father,"),
        (12, 18, "because I must go"),
        (19, 21, "unto the Father"),
        (22, 23, "for your sakes."),
    ],
    36: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when Jesus had ended"),
        (11, 13, "these sayings,"),
        (14, 19, "he touched with his hand"),
        (20, 22, "the disciples, one by one,"),
        (23, 27, "whom he had chosen,"),
        (28, 32, "until he had touched"),
        (33, 37, "them all,"),
        (38, 44, "and spoke unto them"),
        (45, 50, "as he touched"),
        (51, 54, "them."),
    ],
    37: [
        (0, 8, "And the multitude heard not"),
        (9, 14, "the words he spoke,"),
        (15, 16, "therefore"),
        (17, 21, "they bore no record;"),
        (22, 27, "but the disciples bore record"),
        (28, 35, "he gave unto them"),
        (36, 44, "the power to give the Holy Ghost."),
        (45, 54, "And I will show unto you"),
        (55, 60, "at a later time"),
        (61, 64, "this record is true."),
    ],
    38: [
        (0, 3, "And it came to pass that"),
        (4, 10, "when Jesus had touched"),
        (11, 14, "them all,"),
        (15, 18, "there came a cloud"),
        (19, 23, "and overshadowed"),
        (24, 28, "the multitude"),
        (29, 35, "so that they could not see"),
        (36, 38, "Jesus."),
    ],
    39: [
        (0, 5, "And while they were overshadowed"),
        (6, 11, "he departed"),
        (12, 15, "from them,"),
        (16, 18, "and ascended"),
        (19, 21, "into heaven."),
        (22, 27, "And the disciples saw"),
        (28, 29, "and bore record"),
        (30, 35, "that he ascended again"),
        (36, 38, "into heaven."),
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
