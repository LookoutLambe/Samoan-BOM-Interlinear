#!/usr/bin/env python3
"""The ENGLISH side of the interlinear: register, morphology and vocabulary.

Everything here started inside the D&C generator and does not belong there.
The gloss is English, so the checker, the orthography scan, the generator and
anything that compares a gloss to the canon all need the same answers to the
same three questions, and a second copy of any of them would drift:

    is this word carried by that verse?      in_english()
    what is its other number?                stems()
    what does it look like in modern English? modernise()

THE CANON IS THE DICTIONARY. bom_english.json is 10,893 verses of the official
English — the right register, already on disk, and it settles whether "comes"
or "coms" is a word without a morphology table. Where it cannot help, because
the KJV writes only `bringeth` and never `brings`, a regular rule finishes
the job rather than leaving the archaic form standing.

TWO DIRECTIONS, and they must not be confused. ARCHAIC lets a gloss written
"you" match a verse that says "ye", so a good candidate is not thrown away.
MODERN_WORD converts what is finally written, because the gloss does not have
to follow the canon's archaism: it exists to tell a reader what the Samoan
means, and "you" does that better than "thee".
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"

# Function words: present in nearly every verse, so their presence proves
# nothing about a gloss. NEGATIONS are function words by form and load-bearing
# by meaning — dropping the "not" from "shall not" says the opposite.
NEGATIONS = {"not", "no", "neither", "nor", "never", "none", "without",
             "nothing", "cannot"}
# Quantifiers are function words by form and load-bearing the same way a
# negation is: "is to all" trimmed to "is" says something different, not
# something shorter.
QUANTIFIERS = {"all", "every", "each", "both", "many", "few", "some", "any"}
PROTECTED = NEGATIONS | QUANTIFIERS
FUNCTION_ONLY = {
    "i", "you", "we", "they", "he", "she", "it", "the", "a", "an", "of", "to",
    "and", "or", "but", "in", "on", "at", "by", "for", "with", "that", "this",
    "these", "those", "is", "are", "was", "were", "be", "shall", "will",
    "unto", "ye", "thou", "thee", "thy", "his", "her", "their", "my", "your",
    "them", "him", "me", "us", "who", "which", "all", "from", "upon", "o",
} | NEGATIONS | QUANTIFIERS

ARCHAIC = {
    "you": {"ye", "thee", "thou"}, "ye": {"you", "thee", "thou"},
    "thee": {"you", "ye"}, "thou": {"you", "ye"},
    "your": {"thy", "thine"}, "thy": {"your", "thine"}, "thine": {"your", "thy"},
    "has": {"hath"}, "hath": {"has"}, "have": {"hast"}, "hast": {"have"},
    "does": {"doth"}, "doth": {"does"}, "do": {"dost"}, "dost": {"do"},
    "says": {"saith"}, "saith": {"says"}, "said": {"saith"},
    "is": {"art", "be"}, "are": {"art", "be"}, "art": {"are", "is"},
    "shall": {"will"}, "will": {"shall"},
}

MODERN_WORD = {
    "ye": "you", "thee": "you", "thou": "you",
    "thy": "your", "thine": "your",
    "hath": "has", "hast": "have", "doth": "does", "dost": "do",
    "doeth": "does", "art": "are", "wast": "were", "wert": "were",
    "shalt": "shall", "wilt": "will", "canst": "can", "mayest": "may",
    "saith": "says", "sayest": "say", "unto": "to",
    "whosoever": "whoever", "whatsoever": "whatever",
}

_ETH = re.compile(r"^([a-z]{2,})eth$")
_EST = re.compile(r"^([a-z]{2,})est$")
_VOCAB: set[str] = set()


def vocabulary() -> set[str]:
    """Every word the official English of this corpus uses."""
    if not _VOCAB:
        data = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
        for text in data.values():
            _VOCAB.update(re.findall(r"[a-z']+", text.lower()))
    return _VOCAB


def stems(word: str) -> set[str]:
    """A word and its other number. Never changes which word it is."""
    out = {word}
    if word.endswith("ies") and len(word) > 4:
        out.add(word[:-3] + "y")
    if word.endswith("es") and len(word) > 3:
        out.add(word[:-2])
    if word.endswith("s") and not word.endswith("ss"):
        out.add(word[:-1])
    out.add(word + "s")
    return out


def in_english(word: str, verse_words: set[str]) -> bool:
    """Does this verse carry this gloss word — allowing number and the
    archaic/modern pairs the canon and the glosses both use?"""
    w = word.lower()
    return (w in verse_words or bool(stems(w) & verse_words)
            or bool(ARCHAIC.get(w, set()) & verse_words))


def _third_person(stem: str) -> str:
    if stem.endswith(("s", "sh", "ch", "x", "z")):
        return stem + "es"
    if stem.endswith("y") and len(stem) > 1 and stem[-2] not in "aeiou":
        return stem[:-1] + "ies"
    return stem + "s"


def modernise(gloss: str) -> str:
    """Archaic English out of the gloss. The canon is consulted first, and a
    regular rule finishes what it cannot answer — the KJV writes `bringeth` and
    never `brings`, so its vocabulary alone would leave the archaism standing.
    """
    vocab = vocabulary()

    def one(m):
        w = m.group(0)
        low = w.lower()
        out = MODERN_WORD.get(low)
        if out is None:
            em = _ETH.match(low)
            if em:
                # `maketh` is make+eth, `bringeth` is bring+eth. The canon
                # settles which base is a word; where it has neither form,
                # the bare stem is the safer guess.
                stem = em.group(1)
                base = stem + "e" if stem + "e" in vocab else stem
                out = _third_person(base)
                if out not in vocab and _third_person(stem) in vocab:
                    out = _third_person(stem)
            else:
                sm = _EST.match(low)
                if sm:
                    for cand in (sm.group(1), sm.group(1) + "e"):
                        if cand in vocab:
                            out = cand
                            break
        if out is None:
            return w
        return out.capitalize() if w[:1].isupper() else out

    return re.sub(r"[A-Za-z]+", one, gloss)


if __name__ == "__main__":
    import sys
    for g in sys.argv[1:] or ["cometh", "giveth", "bringeth", "doeth",
                              "thou goest", "O ye", "thy God", "unto all"]:
        print("%-16r -> %r" % (g, modernise(g)))
