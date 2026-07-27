"""
Hand-curated TAM-phrase gloss overrides for Alema (Alma) 54 — the epistles of
Moroni and Ammoron concerning the exchange of prisoners; Moroni denounces the
Lamanites' aggression and demands terms; Ammoron replies defiantly, claiming
descent from Zoram and vowing to avenge his brother's blood.

Run AFTER build_phrase_overrides.py so this chapter's hand-curation
overlays the auto-glossed entries.

Follows GLOSSING_RULES.md and the no-injected-words rule: TAM clusters
atomic (rule 1), subject `o ia` / agent `e ia` absorbed into the verb
cluster, never split as a bare "he" (rule 2), NP/PP atoms split (rule 3),
`mai`-as-"from" (rule 7), idioms kept whole (rule 9), em-dash source splits
(rule 11), `mafai ona`/`ina ia`/`e tatau ona` bound (rules 13/15).

No em-dash pre-splits needed for this chapter.

    python3 build_overrides_alma54.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "alma"
CHAPTER_NUM = 54

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 2, "And now"),
        (3, 4, "it came to pass"),
        (5, 7, "in the beginning"),
        (8, 14, "of the twenty and ninth"),
        (15, 16, "year"),
        (17, 18, "of the judges,"),
        (19, 22, "sent"),
        (23, 24, "Ammoron"),
        (25, 26, "a message"),
        (27, 28, "unto Moroni"),
        (29, 31, "desiring"),
        (32, 34, "of him"),
        (35, 37, "they exchange"),
        (38, 38, "prisoners."),
    ],
    2: [
        (0, 3, "And it came to pass that"),
        (4, 4, "felt"),
        (5, 6, "Moroni"),
        (7, 9, "great joy"),
        (10, 12, "at this request,"),
        (13, 16, "for he desired"),
        (17, 20, "the needed things"),
        (21, 24, "which were given"),
        (25, 27, "for the keeping of"),
        (28, 31, "the Lamanite prisoners"),
        (32, 35, "for the keeping of"),
        (36, 38, "his own people;"),
        (39, 43, "and he also desired"),
        (44, 47, "his own people"),
        (48, 51, "for the strengthening of"),
        (52, 53, "his army."),
    ],
    3: [
        (0, 1, "Now"),
        (2, 3, "there were many"),
        (4, 6, "women and children"),
        (7, 11, "taken by the Lamanites,"),
        (12, 16, "but there was no woman"),
        (17, 20, "nor a child"),
        (21, 23, "among"),
        (24, 27, "all the prisoners of Moroni,"),
        (28, 30, "or the prisoners"),
        (31, 36, "whom Moroni had taken;"),
        (37, 38, "therefore"),
        (39, 42, "Moroni thought of"),
        (43, 45, "a stratagem"),
        (46, 49, "to gain"),
        (50, 53, "the many prisoners of"),
        (54, 56, "the Nephites"),
        (57, 59, "from the Lamanites,"),
        (60, 64, "as much as was possible."),
    ],
    4: [
        (0, 1, "Therefore"),
        (2, 6, "he wrote"),
        (7, 8, "a letter,"),
        (9, 11, "and sent it"),
        (12, 15, "by way of"),
        (16, 19, "the servant of Ammoron,"),
        (20, 23, "the very one who"),
        (24, 27, "brought the letter"),
        (28, 29, "to Moroni."),
        (30, 31, "Now"),
        (32, 34, "these are the words"),
        (35, 38, "which he wrote"),
        (39, 40, "unto Ammoron,"),
        (41, 42, "thus:"),
    ],
    5: [
        (0, 0, "Behold,"),
        (1, 1, "Ammoron,"),
        (2, 6, "I have indeed written"),
        (7, 9, "unto thee"),
        (10, 12, "concerning"),
        (13, 14, "this war"),
        (15, 18, "which thou hast raised"),
        (19, 21, "against"),
        (22, 23, "my people,"),
        (24, 26, "or rather"),
        (27, 29, "which was raised"),
        (30, 32, "by thy brother"),
        (33, 34, "against"),
        (35, 38, "them,"),
        (39, 40, "and which"),
        (41, 43, "thou art resolved"),
        (44, 46, "to continue"),
        (47, 49, "after passed"),
        (50, 51, "his death."),
    ],
    6: [
        (0, 0, "Behold,"),
        (1, 6, "I would explain"),
        (7, 9, "unto thee"),
        (10, 12, "concerning"),
        (13, 15, "the justice of"),
        (16, 17, "God,"),
        (18, 21, "and the sword of"),
        (22, 25, "his almighty wrath,"),
        (26, 29, "which hangs down"),
        (30, 32, "over thee,"),
        (33, 34, "except"),
        (35, 37, "thou repent"),
        (38, 40, "and turn back"),
        (41, 42, "thy armies"),
        (43, 47, "into your own lands,"),
        (48, 51, "or the land"),
        (52, 54, "which ye possess,"),
        (55, 58, "which is the land of"),
        (59, 59, "Nephi."),
    ],
    7: [
        (0, 0, "Yea,"),
        (1, 5, "I would explain"),
        (6, 8, "unto thee"),
        (9, 10, "these things"),
        (11, 14, "if it were"),
        (15, 20, "that thou couldst listen"),
        (21, 22, "to them;"),
        (23, 23, "yea,"),
        (24, 28, "I would explain"),
        (29, 31, "unto thee"),
        (32, 34, "concerning"),
        (35, 38, "that terrible hell"),
        (39, 42, "which waits"),
        (43, 44, "to receive"),
        (45, 47, "murderers"),
        (48, 48, "such as"),
        (49, 53, "as have been"),
        (54, 57, "thou and thy brother,"),
        (58, 59, "except"),
        (60, 62, "thou repent"),
        (63, 64, "and remove"),
        (65, 68, "thy murderous intentions,"),
        (69, 71, "and go back"),
        (72, 74, "with thy armies"),
        (75, 79, "into your own lands."),
    ],
    8: [
        (0, 1, "But because"),
        (2, 5, "thou rejectedst before"),
        (6, 7, "these things,"),
        (8, 10, "and thou fightest"),
        (11, 13, "against"),
        (14, 17, "the people of the Lord,"),
        (18, 23, "so likewise I think"),
        (24, 30, "thou wilt do again"),
        (31, 32, "this thing."),
    ],
    9: [
        (0, 2, "And now"),
        (3, 3, "behold,"),
        (4, 6, "we are ready"),
        (7, 9, "to receive you;"),
        (10, 10, "yea,"),
        (11, 13, "and except"),
        (14, 16, "thou remove"),
        (17, 18, "thy purposes,"),
        (19, 19, "behold,"),
        (20, 27, "thou wilt bring down"),
        (28, 33, "the wrath of that God"),
        (34, 38, "whom thou hast rejected,"),
        (39, 42, "upon you,"),
        (43, 46, "even unto"),
        (47, 50, "the complete destruction of"),
        (51, 51, "you."),
    ],
    10: [
        (0, 0, "But,"),
        (1, 4, "as liveth"),
        (5, 6, "the Lord,"),
        (7, 11, "shall come"),
        (12, 14, "our armies"),
        (15, 18, "upon you,"),
        (19, 20, "except"),
        (21, 24, "ye depart,"),
        (25, 31, "and it shall not be long"),
        (32, 35, "until ye be visited"),
        (36, 38, "with death,"),
        (39, 39, "for"),
        (40, 45, "we will keep"),
        (46, 48, "our cities"),
        (49, 52, "and our lands;"),
        (53, 53, "yea,"),
        (54, 60, "and we will firmly hold"),
        (61, 63, "our worship"),
        (64, 67, "and the cause of"),
        (68, 70, "our God."),
    ],
    11: [
        (0, 1, "But behold,"),
        (2, 4, "I think"),
        (5, 8, "there is no use"),
        (9, 13, "that I speak"),
        (14, 16, "unto thee"),
        (17, 19, "concerning"),
        (20, 21, "these things;"),
        (22, 26, "or in my opinion"),
        (27, 28, "thou art"),
        (29, 33, "a child of hell;"),
        (34, 35, "therefore"),
        (36, 41, "I will end"),
        (42, 43, "my letter"),
        (44, 47, "by declaring"),
        (48, 50, "unto thee"),
        (51, 55, "I will not exchange"),
        (56, 56, "prisoners,"),
        (57, 58, "except"),
        (59, 64, "it be done on the terms"),
        (65, 69, "of thy releasing"),
        (70, 71, "a man"),
        (72, 74, "and his wife"),
        (75, 77, "and his children,"),
        (78, 80, "for a prisoner"),
        (81, 82, "one;"),
        (83, 87, "if this is the condition"),
        (88, 91, "that thou wilt do,"),
        (92, 96, "I will exchange."),
    ],
    12: [
        (0, 1, "And behold,"),
        (2, 6, "if thou do not"),
        (7, 8, "this thing,"),
        (9, 14, "I will go"),
        (15, 18, "together with my armies"),
        (19, 20, "against"),
        (21, 23, "thee;"),
        (24, 24, "yea,"),
        (25, 30, "I will also arm"),
        (31, 32, "my women"),
        (33, 35, "and my children,"),
        (36, 42, "and I will go"),
        (43, 44, "against"),
        (45, 47, "thee,"),
        (48, 54, "and I will pursue"),
        (55, 57, "you"),
        (58, 62, "even unto"),
        (63, 66, "your own land,"),
        (67, 71, "the very land of"),
        (72, 75, "our first inheritance;"),
        (76, 76, "yea,"),
        (77, 80, "and blood"),
        (81, 83, "for blood,"),
        (84, 84, "yea,"),
        (85, 85, "life"),
        (86, 88, "for life;"),
        (89, 89, "yea,"),
        (90, 95, "and I will fight"),
        (96, 97, "with thee"),
        (98, 100, "until"),
        (101, 103, "thou art destroyed"),
        (104, 106, "from off"),
        (107, 108, "the earth's surface."),
    ],
    13: [
        (0, 0, "Behold,"),
        (1, 3, "I am angry,"),
        (4, 7, "and my people also;"),
        (8, 10, "ye have sought"),
        (11, 12, "to slay"),
        (13, 14, "us,"),
        (15, 20, "but we have only sought"),
        (21, 22, "to defend"),
        (23, 25, "ourselves."),
        (26, 27, "But behold,"),
        (28, 32, "if ye continue to seek"),
        (33, 34, "to destroy"),
        (35, 36, "us,"),
        (37, 41, "we will seek"),
        (42, 44, "to destroy you;"),
        (45, 45, "yea,"),
        (46, 51, "and we will seek"),
        (52, 54, "our land,"),
        (55, 58, "the land of"),
        (59, 62, "our first inheritance."),
    ],
    14: [
        (0, 1, "Now"),
        (2, 4, "I close"),
        (5, 6, "my letter."),
        (7, 8, "I am"),
        (9, 10, "Moroni;"),
        (11, 12, "I am"),
        (13, 16, "a leader of"),
        (17, 20, "the people of the Nephites."),
    ],
    15: [
        (0, 1, "Now"),
        (2, 4, "it came to pass that"),
        (5, 6, "when received"),
        (7, 8, "Ammoron"),
        (9, 10, "this letter,"),
        (11, 14, "he was angry;"),
        (15, 19, "and he wrote"),
        (20, 22, "another letter"),
        (23, 24, "unto Moroni,"),
        (25, 28, "and these are the words"),
        (29, 31, "which he wrote,"),
        (32, 33, "saying:"),
    ],
    16: [
        (0, 1, "I am"),
        (2, 3, "Ammoron,"),
        (4, 7, "the king of"),
        (8, 9, "the Lamanites;"),
        (10, 11, "I am"),
        (12, 14, "the brother of"),
        (15, 16, "Amalickiah"),
        (17, 21, "whom ye slew."),
        (22, 22, "Behold,"),
        (23, 27, "I will avenge"),
        (28, 29, "his blood"),
        (30, 32, "upon thee;"),
        (33, 33, "yea,"),
        (34, 40, "and I will come"),
        (41, 44, "upon you"),
        (45, 48, "together with my armies,"),
        (49, 53, "for I fear not"),
        (54, 56, "thy threats."),
    ],
    17: [
        (0, 1, "For behold,"),
        (2, 3, "did commit"),
        (4, 7, "your fathers"),
        (8, 9, "the wrong"),
        (10, 13, "against their brethren,"),
        (14, 16, "insomuch that"),
        (17, 19, "they robbed"),
        (20, 22, "them"),
        (23, 25, "their right"),
        (26, 28, "to the government,"),
        (29, 32, "when it was a thing"),
        (33, 37, "which rightly belonged"),
        (38, 39, "to them."),
    ],
    18: [
        (0, 2, "And now"),
        (3, 3, "behold,"),
        (4, 9, "if ye lay down"),
        (10, 14, "your weapons of war,"),
        (15, 19, "and yield yourselves"),
        (20, 21, "to be ruled"),
        (22, 24, "by them"),
        (25, 30, "who truly own"),
        (31, 32, "the government,"),
        (33, 36, "then I will command"),
        (37, 39, "my people"),
        (40, 43, "to lay down"),
        (44, 48, "their weapons of war"),
        (49, 54, "and shall no more"),
        (55, 55, "fight."),
    ],
    19: [
        (0, 0, "Behold,"),
        (1, 4, "thou hast breathed out"),
        (5, 8, "many threats"),
        (9, 10, "against"),
        (11, 13, "me"),
        (14, 16, "and my people;"),
        (17, 18, "but behold,"),
        (19, 22, "we fear not"),
        (23, 25, "thy threats."),
    ],
    20: [
        (0, 3, "Nevertheless,"),
        (4, 9, "I will allow"),
        (10, 12, "to exchange prisoners"),
        (13, 15, "according to"),
        (16, 17, "thy request,"),
        (18, 20, "with gladness,"),
        (21, 26, "that I may keep"),
        (27, 28, "my food"),
        (29, 32, "for my men of war;"),
        (33, 39, "and we will raise"),
        (40, 41, "a war"),
        (42, 45, "which will be everlasting,"),
        (46, 49, "either the subjecting"),
        (50, 51, "the Nephites"),
        (52, 55, "to our rule"),
        (56, 60, "or the destroying"),
        (61, 62, "them"),
        (63, 64, "forever."),
    ],
    21: [
        (0, 0, "And"),
        (1, 3, "concerning"),
        (4, 6, "that God"),
        (7, 10, "whom thou sayest"),
        (11, 13, "we have rejected,"),
        (14, 14, "behold,"),
        (15, 18, "we do not know"),
        (19, 21, "such a being;"),
        (22, 25, "nor do ye;"),
        (26, 27, "but if"),
        (28, 30, "there is"),
        (31, 33, "such a being,"),
        (34, 37, "we do not know"),
        (38, 43, "but whether he also made"),
        (44, 45, "us"),
        (46, 49, "as he did you."),
    ],
    22: [
        (0, 3, "And if it be"),
        (4, 6, "there is"),
        (7, 8, "a devil"),
        (9, 11, "and a hell,"),
        (12, 12, "behold,"),
        (13, 19, "will he not send"),
        (20, 20, "thee"),
        (21, 21, "there"),
        (22, 25, "to dwell together"),
        (26, 28, "with my brother,"),
        (29, 33, "whom ye slew,"),
        (34, 40, "of whom thou hast implied"),
        (41, 45, "he has gone"),
        (46, 49, "to such a place?"),
        (50, 51, "But behold"),
        (52, 54, "it does not matter"),
        (55, 56, "these things."),
    ],
    23: [
        (0, 1, "I am"),
        (2, 3, "Ammoron,"),
        (4, 8, "and a descendant"),
        (9, 10, "of Zoram,"),
        (11, 14, "whom compelled"),
        (15, 18, "your fathers"),
        (19, 21, "and took away"),
        (22, 23, "from Jerusalem."),
    ],
    24: [
        (0, 2, "And behold now,"),
        (3, 4, "I am"),
        (5, 9, "a brave Lamanite;"),
        (10, 10, "behold,"),
        (11, 12, "was raised"),
        (13, 15, "this war"),
        (16, 18, "to avenge"),
        (19, 22, "the wrongs they suffered,"),
        (23, 24, "and to keep"),
        (25, 28, "and to gain"),
        (29, 31, "their rights"),
        (32, 34, "to the government;"),
        (35, 38, "and I close"),
        (39, 40, "my letter"),
        (41, 42, "to Moroni."),
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
