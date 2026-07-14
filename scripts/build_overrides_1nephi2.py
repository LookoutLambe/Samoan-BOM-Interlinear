"""
Hand-curated TAM-phrase gloss overrides for 1 Nifae (Nephi) 2.

Mirrors the structure of build_overrides_1nephi1.py. Each verse is a list of
(start_idx, end_idx, english_gloss) tuples spanning every source token in
order, validated against the live bom_books.json before writing.

Run AFTER build_phrase_overrides.py so the per-verse curation here overrides
auto-glossed entries for this chapter.

    python3 build_overrides_1nephi2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK_ID = "1nephi"
CHAPTER_NUM = 2

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"


VERSE_SPECS: dict[int, list[tuple[int, int, str]]] = {
    1: [
        (0, 1, "For behold,"),
        (2, 4, "it came to pass"),
        (5, 6, "spoke"),
        (7, 8, "the Lord"),
        (9, 11, "unto my father,"),
        (12, 12, "yea,"),
        (13, 16, "in a dream,"),
        (17, 19, "and spoke"),
        (20, 22, "unto him:"),
        (23, 24, "Blessed art thou,"),
        (25, 25, "Lehi,"),
        (26, 28, "because of the things"),
        (29, 31, "thou hast done;"),
        (32, 33, "because"),
        (34, 36, "thou hast been faithful"),
        (37, 39, "and declared"),
        (40, 42, "unto this people"),
        (43, 43, "things"),
        (44, 47, "which I commanded"),
        (48, 48, "thee,"),
        (49, 49, "behold,"),
        (50, 52, "they have sought"),
        (53, 54, "to take away"),
        (55, 56, "thy life."),
    ],
    2: [
        (0, 3, "And it came to pass"),
        (4, 4, "commanded"),
        (5, 7, "the Lord"),
        (8, 9, "my father,"),
        (10, 13, "in a dream,"),
        (14, 19, "he should"),
        (20, 20, "take"),
        (21, 22, "his family"),
        (23, 26, "and depart"),
        (27, 29, "into the wilderness."),
    ],
    3: [
        (0, 3, "And it came to pass"),
        (4, 6, "he obeyed"),
        (7, 9, "the word"),
        (10, 12, "of the Lord,"),
        (13, 16, "wherefore"),
        (17, 21, "he did"),
        (22, 24, "even as"),
        (25, 28, "had commanded him"),
        (29, 31, "by the Lord."),
    ],
    4: [
        (0, 3, "And it came to pass"),
        (4, 8, "he departed"),
        (9, 11, "into the wilderness."),
        (12, 14, "And he left"),
        (15, 16, "by him"),
        (17, 18, "his house,"),
        (19, 21, "and the land"),
        (22, 24, "of his inheritance,"),
        (25, 27, "and his gold,"),
        (28, 30, "and his silver,"),
        (31, 34, "and his precious things,"),
        (35, 38, "and took not"),
        (39, 40, "by him"),
        (41, 42, "anything,"),
        (43, 44, "save"),
        (45, 46, "his family,"),
        (47, 49, "and provisions,"),
        (50, 51, "and tents,"),
        (52, 55, "and departed"),
        (56, 58, "into the wilderness."),
    ],
    5: [
        (0, 5, "And he went down"),
        (6, 7, "below"),
        (8, 11, "by the borders"),
        (12, 13, "near"),
        (14, 16, "to the shore"),
        (17, 20, "of the Red Sea;"),
        (21, 25, "and he traveled"),
        (26, 28, "in the wilderness"),
        (29, 33, "in the borders nearer"),
        (34, 37, "to the Red Sea;"),
        (38, 42, "and he traveled"),
        (43, 45, "in the wilderness"),
        (46, 49, "with his family,"),
        (50, 52, "there were"),
        (53, 54, "my mother,"),
        (55, 56, "Sariah,"),
        (57, 60, "and my elder brothers,"),
        (61, 62, "Laman,"),
        (63, 63, "Lemuel,"),
        (64, 65, "and Sam."),
    ],
    6: [
        (0, 3, "And it came to pass"),
        (4, 5, "had passed"),
        (6, 8, "three days"),
        (9, 13, "since he traveled"),
        (14, 16, "in the wilderness,"),
        (17, 18, "he pitched"),
        (19, 20, "by him"),
        (21, 22, "his tent"),
        (23, 25, "in a valley"),
        (26, 28, "by the side of"),
        (29, 30, "a river."),
    ],
    7: [
        (0, 3, "And it came to pass"),
        (4, 4, "built"),
        (5, 6, "by him"),
        (7, 8, "an altar"),
        (9, 10, "of stones,"),
        (11, 13, "and offered up"),
        (14, 15, "an offering"),
        (16, 18, "unto the Lord,"),
        (19, 20, "and gave"),
        (21, 22, "thanks"),
        (23, 25, "unto the Lord"),
        (26, 28, "our God."),
    ],
    8: [
        (0, 3, "And it came to pass"),
        (4, 4, "named"),
        (5, 6, "by him"),
        (7, 8, "the river,"),
        (9, 10, "Laman,"),
        (11, 14, "and it emptied"),
        (15, 18, "into the Red Sea;"),
        (19, 22, "and the valley"),
        (23, 25, "was in the borders"),
        (26, 27, "near"),
        (28, 29, "its mouth."),
    ],
    9: [
        (0, 4, "And when saw"),
        (5, 6, "my father"),
        (7, 9, "was emptying"),
        (10, 13, "the waters of the river"),
        (14, 16, "into the fountain"),
        (17, 20, "of the Red Sea,"),
        (21, 25, "he spake"),
        (26, 27, "unto Laman,"),
        (28, 29, "saying:"),
        (30, 31, "O alas"),
        (32, 34, "would that"),
        (35, 36, "could"),
        (37, 38, "be like"),
        (39, 39, "thou"),
        (40, 42, "this river,"),
        (43, 46, "continually flowing"),
        (47, 49, "into the fountain"),
        (50, 53, "of all righteousness!"),
    ],
    10: [
        (0, 6, "And he also spake"),
        (7, 8, "unto Lemuel:"),
        (9, 10, "O alas"),
        (11, 13, "would that"),
        (14, 15, "could"),
        (16, 17, "be like"),
        (18, 18, "thou"),
        (19, 21, "this valley,"),
        (22, 23, "firm"),
        (24, 25, "and steadfast,"),
        (26, 28, "and immovable"),
        (29, 31, "in the keeping"),
        (32, 33, "of the commandments"),
        (34, 36, "of the Lord!"),
    ],
    11: [
        (0, 1, "Now"),
        (2, 6, "he spake"),
        (7, 9, "these things"),
        (10, 14, "because of the hardness"),
        (15, 18, "of Laman and Lemuel;"),
        (19, 20, "for behold"),
        (21, 24, "they did murmur"),
        (25, 28, "against their father"),
        (29, 32, "in many things,"),
        (33, 35, "because he was"),
        (36, 40, "a visionary man,"),
        (41, 44, "and had led away"),
        (45, 46, "by him"),
        (47, 48, "them"),
        (49, 53, "out of the land of Jerusalem,"),
        (54, 57, "and had left the land"),
        (58, 61, "of their inheritance,"),
        (62, 65, "and their gold,"),
        (66, 69, "and their silver,"),
        (70, 74, "and their precious things,"),
        (75, 79, "to perish in the wilderness."),
        (80, 83, "And he had said"),
        (84, 85, "unto them"),
        (86, 87, "had done"),
        (88, 89, "by him"),
        (90, 91, "this thing"),
        (92, 95, "because of the foolish imaginations"),
        (96, 98, "of his heart."),
    ],
    12: [
        (0, 4, "And thus did murmur"),
        (5, 8, "Laman and Lemuel,"),
        (9, 12, "being the elder ones,"),
        (13, 16, "against their father."),
        (17, 19, "And they murmured"),
        (20, 21, "against him"),
        (22, 26, "because they knew not"),
        (27, 28, "the dealings"),
        (29, 31, "of that God"),
        (32, 35, "who had created"),
        (36, 37, "them."),
    ],
    13: [
        (0, 3, "Neither did believe"),
        (4, 5, "they"),
        (6, 9, "that could be destroyed"),
        (10, 12, "that great city,"),
        (13, 14, "of Jerusalem,"),
        (15, 17, "according to"),
        (18, 20, "the words of the prophets."),
        (21, 25, "And they were like"),
        (26, 28, "unto the Jews"),
        (29, 33, "who were at Jerusalem,"),
        (34, 37, "who sought"),
        (38, 39, "to take away"),
        (40, 41, "the life"),
        (42, 44, "of my father."),
    ],
    14: [
        (0, 3, "And it came to pass"),
        (4, 5, "did speak"),
        (6, 7, "my father"),
        (8, 11, "unto them"),
        (12, 16, "in the valley of Lemuel,"),
        (17, 19, "with power,"),
        (20, 24, "because he was filled"),
        (25, 27, "with the Spirit,"),
        (28, 31, "until did shake"),
        (32, 34, "their frames"),
        (35, 37, "before him."),
        (38, 41, "And he confounded"),
        (42, 43, "them,"),
        (44, 47, "could not"),
        (48, 50, "they"),
        (51, 53, "speak"),
        (54, 56, "against him;"),
        (57, 60, "wherefore,"),
        (61, 64, "they did do"),
        (65, 67, "even as"),
        (68, 70, "had commanded"),
        (71, 72, "them"),
        (73, 74, "by him."),
    ],
    15: [
        (0, 2, "And dwelt"),
        (3, 4, "my father"),
        (5, 7, "in a tent."),
    ],
    16: [
        (0, 3, "And it came to pass"),
        (4, 5, "I,"),
        (6, 7, "Nephi,"),
        (8, 12, "being exceedingly young,"),
        (13, 16, "nevertheless,"),
        (17, 20, "large in stature,"),
        (21, 26, "and also having"),
        (27, 29, "great desires"),
        (30, 32, "to know"),
        (33, 33, "the mysteries"),
        (34, 36, "of God,"),
        (37, 40, "wherefore,"),
        (41, 45, "I did cry"),
        (46, 48, "unto the Lord;"),
        (49, 50, "and behold"),
        (51, 55, "he did visit"),
        (56, 58, "me,"),
        (59, 60, "and softened"),
        (61, 62, "my heart,"),
        (63, 66, "wherefore"),
        (67, 70, "I did believe"),
        (71, 73, "all the words"),
        (74, 75, "spoken"),
        (76, 78, "by my father;"),
        (79, 82, "wherefore,"),
        (83, 87, "I did not rebel"),
        (88, 92, "against him"),
        (93, 95, "like"),
        (96, 97, "my brothers."),
    ],
    17: [
        (0, 4, "And I spake"),
        (5, 6, "unto Sam,"),
        (7, 9, "and made known"),
        (10, 12, "unto him"),
        (13, 13, "things"),
        (14, 16, "had shown"),
        (17, 19, "by the Lord"),
        (20, 22, "unto me"),
        (23, 25, "by"),
        (26, 29, "his Holy Spirit."),
        (30, 33, "And it came to pass"),
        (34, 36, "he believed"),
        (37, 39, "in my words."),
    ],
    18: [
        (0, 0, "But,"),
        (1, 1, "behold,"),
        (2, 6, "would not hearken"),
        (7, 9, "Laman and Lemuel"),
        (10, 12, "unto my words;"),
        (13, 17, "and being grieved"),
        (18, 21, "because of the hardness"),
        (22, 25, "of their hearts,"),
        (26, 30, "I did cry"),
        (31, 33, "unto the Lord"),
        (34, 36, "for them."),
    ],
    19: [
        (0, 3, "And it came to pass"),
        (4, 5, "spake"),
        (6, 7, "the Lord"),
        (8, 10, "unto me,"),
        (11, 13, "saying:"),
        (14, 16, "Blessed art thou,"),
        (17, 17, "Nephi,"),
        (18, 21, "because of thy faith,"),
        (22, 26, "for thou hast sought"),
        (27, 29, "me"),
        (30, 32, "with diligence,"),
        (33, 38, "and lowliness of heart."),
    ],
    20: [
        (0, 4, "And inasmuch as"),
        (5, 6, "thy keeping"),
        (7, 9, "of my commandments,"),
        (10, 14, "thou shalt prosper,"),
        (15, 20, "and shalt be led"),
        (21, 21, "thee"),
        (22, 24, "to a land"),
        (25, 27, "of promise;"),
        (28, 28, "yea,"),
        (29, 31, "even a land"),
        (32, 35, "which I have prepared"),
        (36, 37, "for thee;"),
        (38, 38, "yea,"),
        (39, 41, "a land"),
        (42, 44, "which is choice"),
        (45, 48, "above all other lands."),
    ],
    21: [
        (0, 4, "And inasmuch as"),
        (5, 6, "the rebellion"),
        (7, 9, "of thy brothers"),
        (10, 12, "against thee,"),
        (13, 17, "they shall be cut off"),
        (18, 19, "they"),
        (20, 24, "from the presence of the Lord."),
    ],
    22: [
        (0, 4, "And inasmuch as"),
        (5, 6, "thy keeping"),
        (7, 9, "of my commandments,"),
        (10, 13, "shalt be made"),
        (14, 14, "thou"),
        (15, 17, "a ruler"),
        (18, 20, "and a teacher"),
        (21, 23, "over thy brothers."),
    ],
    23: [
        (0, 1, "For behold,"),
        (2, 4, "in that day"),
        (5, 10, "they shall rebel against me,"),
        (11, 13, "me,"),
        (14, 17, "I will curse"),
        (18, 19, "them"),
        (20, 23, "with a sore curse,"),
        (24, 31, "and they shall have no power"),
        (32, 34, "over thy seed"),
        (35, 36, "except"),
        (37, 41, "they shall rebel also"),
        (42, 44, "against me."),
    ],
    24: [
        (0, 4, "And if it shall come to pass"),
        (5, 6, "thus that"),
        (7, 9, "they rebel"),
        (10, 12, "against me,"),
        (13, 16, "shall be"),
        (17, 18, "they"),
        (19, 20, "as a scourge"),
        (21, 23, "unto thy seed,"),
        (24, 26, "to stir up"),
        (27, 28, "them"),
        (29, 33, "in the ways of remembrance."),
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
