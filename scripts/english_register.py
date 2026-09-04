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


# Pairs English spells as two words that are one word here. Kept SHORT and
# literal: this is not a synonym list, and anything that changes which word
# the gloss uses belongs nowhere near it.
VARIANTS = {"far": {"afar"}, "afar": {"far"},
            "among": {"amongst"}, "amongst": {"among"},
            "while": {"whilst"}, "whilst": {"while"},
            "toward": {"towards"}, "towards": {"toward"}}


# Number that -s cannot reach. `o loo` glosses "is" and D&C 1:1 reads "ye that
# ARE upon the islands" -- one word in two numbers, exactly like heart/hearts,
# and without this the verse looked like it did not carry the gloss at all.
IRREGULAR_NUMBER = {
    "is": {"are"}, "are": {"is"}, "was": {"were"}, "were": {"was"},
    "has": {"have"}, "have": {"has"}, "does": {"do"}, "do": {"does"},
    "man": {"men"}, "men": {"man"}, "woman": {"women"}, "women": {"woman"},
    "child": {"children"}, "children": {"child"},
    "foot": {"feet"}, "feet": {"foot"}, "tooth": {"teeth"}, "teeth": {"tooth"},
    "this": {"these"}, "these": {"this"}, "that": {"those"}, "those": {"that"},
    "ox": {"oxen"}, "oxen": {"ox"}, "brother": {"brethren"},
    "brethren": {"brother"}, "person": {"people"}, "people": {"person"},
}


def stems(word: str) -> set[str]:
    """A word and its inflections. Never changes which word it is.

    Number and TENSE both. `sao` is "escaped" in the Book of Mormon and D&C
    1:2 reads "there is none to escape" -- one word, and without the tense
    pair the verse looked like it did not have it and the gloss was dropped.
    """
    out = {word}
    if word.endswith("ies") and len(word) > 4:
        out.add(word[:-3] + "y")
    if word.endswith("es") and len(word) > 3:
        out.add(word[:-2])
    if word.endswith("s") and not word.endswith("ss"):
        out.add(word[:-1])
    out.add(word + "s")
    if word.endswith("ed") and len(word) > 3:
        out.add(word[:-1])          # escaped -> escape
        out.add(word[:-2])          # walked  -> walk
    elif word.endswith("e"):
        out.add(word + "d")
    else:
        out.add(word + "ed")
    out |= VARIANTS.get(word, set())
    out |= IRREGULAR_NUMBER.get(word, set())
    return out


def in_english(word: str, verse_words: set[str]) -> bool:
    """Does this verse carry this gloss word — allowing number and the
    archaic/modern pairs the canon and the glosses both use?"""
    w = word.lower()
    return (w in verse_words or bool(stems(w) & verse_words)
            or bool(ARCHAIC.get(w, set()) & verse_words))


def _third_person(stem: str) -> str:
    if stem.endswith(("s", "sh", "ch", "x", "z", "o")):
        return stem + "es"          # go -> goes, not "gos"
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
                # settles which base is a word.
                #
                # THE BASE MUST BE A WORD, or the rule eats nouns: `teeth`
                # also ends in -eth, and without this it comes out "tes".
                stem = em.group(1)
                # stem+e FIRST: `com` is in the canon (an abbreviation),
                # so stem-first turned `cometh` into "coms".
                base = next((c for c in (stem + "e", stem) if c in vocab), None)
                if base:
                    out = _third_person(base)
            else:
                sm = _EST.match(low)
                if sm:
                    # -est is a SUPERLATIVE as often as a verb, and `vilest`
                    # -> "vile" and `mightiest` -> "mighty" are both wrong. A
                    # verb that takes -est in this register also takes -eth, so
                    # the canon can say which this is: `denieth` is in it,
                    # `vileth` is not.
                    stem = sm.group(1)
                    if stem + "eth" in vocab:
                        undouble = (stem[:-1] if len(stem) > 2
                                    and stem[-1] == stem[-2] else None)
                        dey = stem[:-1] + "y" if stem.endswith("i") else None
                        for cand in (stem, stem + "e", undouble, dey):
                            if cand and cand in vocab:
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
