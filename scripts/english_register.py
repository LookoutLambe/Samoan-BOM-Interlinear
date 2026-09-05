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
    # the KJV's "unto" is the gloss's "to": a gloss "to them" is carried by a
    # verse reading "unto them" (the Book of Mormon side compares modernised
    # English, where no "unto" survives, so this changes nothing there)
    "to": {"unto"}, "unto": {"to"},
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
# near-synonyms a dictionary sense and the KJV use for one Samoan word --
# only for pairing a blank with a leftover word of the verse, never to write
# a gloss the verse does not have
SYNONYMS = {
    "behold": {"look", "see", "gaze", "view", "watch"}, "beheld": {"look", "see", "gaze", "saw"},
    "look": {"behold", "see"}, "see": {"behold", "look", "perceive"},
    "power": {"might", "strength", "authority"}, "might": {"power", "strength"},
    "sons": {"children", "child", "son"}, "children": {"sons", "son", "offspring"},
    "speak": {"say", "talk", "tell"}, "spake": {"say", "said", "talk", "tell"},
    "rejoice": {"glad", "joy", "happy"}, "glad": {"rejoice", "joy", "happy"},
    "wroth": {"angry", "anger"}, "angry": {"wroth", "anger"},
    "smite": {"strike", "beat", "hit"}, "smote": {"strike", "beat", "hit"},
    "slay": {"kill"}, "slew": {"kill"}, "kill": {"slay"},
    "fear": {"afraid", "dread"}, "afraid": {"fear", "dread"},
    "beseech": {"ask", "beg", "pray", "entreat"}, "entreat": {"ask", "beg", "pray"},
    "dwell": {"live", "stay", "abide"}, "abide": {"dwell", "stay", "remain"},
    "commandment": {"command", "law", "order"}, "commandments": {"command", "law"},
    "wicked": {"bad", "evil"}, "evil": {"bad", "wicked"},
    "servant": {"slave", "serve"}, "servants": {"slave", "serve"},
}
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


_FUTURE = re.compile(r"\b(shall|will)\b")
_PROG = re.compile(r"\b(is|are|was|were|am|be|being)\s+\w+ing\b")
_PERF = re.compile(r"\b(has|have|had)\b")
_PAST = re.compile(r"\b(did|was|were)\b|\w{3,}ed\b")
_PRES = re.compile(r"\b\w{3,}s\b")
# The regular -ed rule misses every strong verb, and scripture English is full
# of them. Listed rather than derived: there is no rule to derive.
IRREGULAR_PAST = {
    "went", "said", "saith", "came", "saw", "made", "took", "gave", "knew",
    "spake", "spoke", "wrote", "told", "found", "brought", "sent", "left",
    "put", "began", "became", "fell", "rose", "stood", "sat", "held", "kept",
    "led", "met", "read", "ran", "heard", "held", "built", "bought", "caught",
    "chose", "drew", "drove", "ate", "felt", "fought", "forgot", "got", "grew",
    "hid", "lay", "lost", "paid", "rent", "shed", "shook", "slew", "smote",
    "sought", "sold", "spent", "sprang", "stole", "struck", "swore", "taught",
    "thought", "threw", "understood", "wept", "won", "wrought", "beheld",
    "bare", "bore", "cast", "cut", "hurt", "set", "shut", "spread", "cost",
    "arose", "awoke", "bade", "bound", "burnt", "dwelt", "fled", "flew",
    "hung", "knelt", "laid", "lit", "meant", "rode", "sang", "sank", "shone",
    "shot", "sank", "slept", "slid", "spun", "sprung", "stuck", "stung",
    "strove", "swam", "swept", "swung", "tore", "trod", "woke", "wore", "wove",
}
_IRREG = re.compile(r"\b(" + "|".join(sorted(IRREGULAR_PAST)) + r")\b")


def tense_of(gloss: str):
    """The tense a gloss is written in, or None if it carries none.

    Deliberately shallow -- it reads the auxiliaries and the regular endings
    and nothing else. It exists to ask whether a candidate AGREES with the
    tense marker in front of it, not to parse English.
    """
    g = " " + (gloss or "").lower().strip() + " "
    for rx, name in ((_FUTURE, "FUTURE"), (_PROG, "PROGRESSIVE"),
                     (_PERF, "PERFECT"), (_PAST, "PAST"), (_IRREG, "PAST")):
        if rx.search(g):
            return name
    # PRESENT: a word in -s that is a verb, not a noun -- "the darkness",
    # "his witness", "righteousness" carry no tense
    for m in re.finditer(r"\b(\w+)\s+(\w{3,}s)\b|\b(\w{3,}s)\b", g):
        prev = m.group(1) or ""
        word = m.group(2) or m.group(3)
        if word.endswith(("ss", "us", "is", "ness", "ous", "eous", "ious")):
            continue
        if prev in ("the", "a", "an", "his", "her", "its", "their", "my", "thy", "your", "our", "of", "all", "every", "these", "those", "many", "two", "three", "seven"):
            continue
        return "PRESENT"
    return None


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
    # the strong verbs: a gloss "behold" is carried by a verse that says
    # "beheld", "see" by "saw" and "seen" -- the base and its past forms and
    # participles are one word
    # -- but not the copulas and auxiliaries: "is" and "was" are different
    # tenses, and equating them would let "there is not" pass for "there was not"
    if word not in _TENSE_BEARING:
        out |= set(BASE_TO_PAST.get(word, ()))
        if word in PAST_TO_BASE:
            out.add(PAST_TO_BASE[word])
            out |= set(BASE_TO_PAST.get(PAST_TO_BASE[word], ()))
        out |= PARTICIPLES.get(word, set())
    return out


_TENSE_BEARING = {"is", "are", "am", "was", "were", "be", "been", "have", "has", "hath", "hast",
                  "had", "do", "did", "does", "doth", "dost", "done"}


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


# ── TENSE AGREEMENT ─────────────────────────────────────────────────────────
# The tense marker in front of a Samoan verb (`na`/`sa` past, `ua` perfect,
# `e`/`te`/`o loo` present) is a grammar fact, and the gloss has to say it.
# The curation remembers a verb in whatever form its verses happened to use,
# so `na ia avatu` came out "give" beside "gave he power", and `e lei iloa`
# "know" beside "knew him not" (John 1, user 2026-09-05: "grammar rules for
# past tense are not being followed"). Nothing is invented here: the verb's
# form is swapped only for a form of the SAME verb that the verse's English
# carries. Base -> past for the strong verbs scripture English uses; regular
# -ed / -d / -ied forms are derived and, again, accepted only if the verse
# has them.
BASE_TO_PAST = {
    "go": ["went"], "say": ["said"], "come": ["came"], "see": ["saw"],
    "make": ["made"], "take": ["took"], "give": ["gave"], "know": ["knew"],
    "speak": ["spake", "spoke"], "write": ["wrote"], "tell": ["told"],
    "find": ["found"], "bring": ["brought"], "send": ["sent"], "leave": ["left"],
    "begin": ["began"], "become": ["became"], "fall": ["fell"], "rise": ["rose"],
    "arise": ["arose"], "stand": ["stood"], "sit": ["sat"], "hold": ["held"],
    "keep": ["kept"], "lead": ["led"], "meet": ["met"], "run": ["ran"],
    "hear": ["heard"], "build": ["built"], "buy": ["bought"], "catch": ["caught"],
    "choose": ["chose"], "draw": ["drew"], "drive": ["drove"], "eat": ["ate"],
    "feel": ["felt"], "fight": ["fought"], "forget": ["forgot"], "get": ["got", "gat"],
    "grow": ["grew"], "hide": ["hid"], "lie": ["lay"], "lose": ["lost"],
    "pay": ["paid"], "shake": ["shook"], "slay": ["slew"], "smite": ["smote"],
    "seek": ["sought"], "sell": ["sold"], "spend": ["spent"], "spring": ["sprang"],
    "steal": ["stole"], "strike": ["struck"], "swear": ["sware", "swore"],
    "teach": ["taught"], "think": ["thought"], "throw": ["threw"],
    "understand": ["understood"], "weep": ["wept"], "win": ["won"],
    "work": ["wrought"], "behold": ["beheld"], "bear": ["bare", "bore"],
    "break": ["brake", "broke"], "beget": ["begat"], "dig": ["digged"],
    "forsake": ["forsook"], "abide": ["abode"], "cleave": ["clave"],
    "awake": ["awoke"], "bid": ["bade"], "bind": ["bound"], "burn": ["burnt"],
    "dwell": ["dwelt"], "flee": ["fled"], "fly": ["flew"], "hang": ["hung"],
    "kneel": ["knelt"], "lay": ["laid"], "light": ["lit"], "mean": ["meant"],
    "ride": ["rode"], "sing": ["sang"], "sink": ["sank"], "shine": ["shone"],
    "shoot": ["shot"], "sleep": ["slept"], "strive": ["strove"], "swim": ["swam"],
    "sweep": ["swept"], "tear": ["tore"], "tread": ["trod"], "wake": ["woke"],
    "wear": ["wore"], "weave": ["wove"], "drink": ["drank"], "blow": ["blew"],
    "overcome": ["overcame"], "forgive": ["forgave"], "partake": ["partook"],
    "bleed": ["bled"], "feed": ["fed"], "creep": ["crept"], "deal": ["dealt"],
    "lend": ["lent"], "bend": ["bent"], "rend": ["rent"], "cling": ["clung"],
    "do": ["did"], "have": ["had"], "hath": ["had"], "has": ["had"],
    "is": ["was"], "are": ["were"], "am": ["was"],
}
PAST_TO_BASE = {p: b for b, ps in BASE_TO_PAST.items() for p in ps}
# the strong participles that differ from the past: see / saw / SEEN
_PARTICIPLE_PAIRS = [
    ("see", "seen"), ("give", "given"), ("take", "taken"), ("speak", "spoken"),
    ("write", "written"), ("know", "known"), ("go", "gone"), ("do", "done"),
    ("come", "come"), ("become", "become"), ("eat", "eaten"), ("fall", "fallen"),
    ("rise", "risen"), ("arise", "arisen"), ("choose", "chosen"), ("draw", "drawn"),
    ("drive", "driven"), ("forget", "forgotten"), ("forsake", "forsaken"),
    ("hide", "hidden"), ("shake", "shaken"), ("slay", "slain"), ("smite", "smitten"),
    ("steal", "stolen"), ("swear", "sworn"), ("throw", "thrown"), ("bear", "born"),
    ("bear", "borne"), ("break", "broken"), ("beget", "begotten"), ("bid", "bidden"),
    ("ride", "ridden"), ("sing", "sung"), ("tread", "trodden"), ("wake", "woken"),
    ("wear", "worn"), ("weave", "woven"), ("drink", "drunk"), ("blow", "blown"),
    ("overcome", "overcome"), ("forgive", "forgiven"), ("partake", "partaken"),
    ("lie", "lain"), ("fly", "flown"), ("grow", "grown"), ("strive", "striven"),
    ("bind", "bound"), ("begin", "begun"), ("spring", "sprung"), ("swim", "swum"),
    ("shine", "shone"), ("stand", "stood"), ("sit", "sat"), ("hold", "held"),
    ("is", "been"), ("are", "been"), ("am", "been"), ("have", "had"),
]
PARTICIPLES: dict[str, set[str]] = {}
for _b, _p in _PARTICIPLE_PAIRS:
    PARTICIPLES.setdefault(_b, set()).add(_p)
    PARTICIPLES.setdefault(_p, set()).add(_b)
    for _past in BASE_TO_PAST.get(_b, ()):
        PARTICIPLES.setdefault(_p, set()).add(_past)
        PARTICIPLES.setdefault(_past, set()).add(_p)
del _b, _p
_TENSE_SKIP = {
    "the", "a", "an", "of", "to", "in", "on", "and", "or", "but", "he", "she",
    "it", "they", "we", "i", "you", "ye", "thou", "thee", "him", "her", "them",
    "us", "me", "his", "its", "their", "our", "my", "thy", "your", "that",
    "which", "who", "whom", "not", "no", "there", "this", "these", "those",
    "unto", "upon", "with", "by", "for", "from", "as", "at", "into", "out", "up",
    "down", "so", "then", "when", "all", "every", "also", "be", "been", "being",
    "shall", "will", "would", "should", "may", "might", "let", "yet", "even",
}


def _past_forms(base: str) -> list[str]:
    out = list(BASE_TO_PAST.get(base, []))
    if base.endswith("e"):
        out.append(base + "d")
    elif base.endswith("y") and len(base) > 2 and base[-2] not in "aeiou":
        out.append(base[:-1] + "ied")
    else:
        out += [base + "ed", base + base[-1] + "ed"]
    return out


def _bases(word: str) -> list[str]:
    """A present-form word back to its base: comes/cometh -> come, lighteth -> light."""
    out = [word]
    for suf in ("eth", "ies", "es", "th", "s"):
        if word.endswith(suf) and len(word) > len(suf) + 2:
            stem = word[:-len(suf)]
            out.append(stem)
            if suf in ("eth", "es"):
                out.append(stem + "e")
            if suf == "ies":
                out.append(stem + "y")
    return out


def _present_forms(base: str) -> list[str]:
    return [base + "eth", base + "th", base + "es", base + "s", base]


def agree_tense(gloss: str, want: str, english: str) -> str:
    """The gloss with its verb in the marker's tense, IF the verse carries that form.

    PAST/PERFECT: a base or present verb becomes the past form the verse has
    (give -> gave, receive -> received); under the perfect `ua` the verse's
    -eth form stands in when it has no past form (ua maliu mai / cometh).
    PRESENT: a strong past form becomes the -eth/-s/base form the verse has.
    Anything the verse does not carry is left exactly as it was.
    """
    if not gloss or not want or not english:
        return gloss
    ew = set(re.findall(r"[a-z']+", english.lower()))
    words = gloss.split()
    for k, w in enumerate(words):
        core = re.sub(r"[^a-z']", "", w.lower())
        if not core or core in _TENSE_SKIP:
            continue
        # a word after an article or possessive is a noun: "the light" is never
        # "the lit" (John 1:5), "his name" never "his named"
        if k > 0 and re.sub(r"[^a-z']", "", words[k - 1].lower()) in ("the", "a", "an", "his", "her", "its", "their", "my", "thy", "your", "our", "this", "that", "these", "those", "every", "all", "no",
                                                                    "of", "in", "at", "on", "upon", "with", "by", "from", "unto", "to", "into", "for", "through", "among", "over", "under", "before", "after"):
            continue          # after a determiner or preposition the word is a noun: "in darkness", never "in darknesed"
        t = tense_of(core)
        swap = None
        if want in ("PAST", "PERFECT") and t in (None, "PRESENT"):
            for base in _bases(core):
                for pf in _past_forms(base):
                    if pf in ew and pf != core:
                        swap = pf
                        break
                if swap:
                    break
            if not swap and want == "PERFECT" and t is None:
                for pf in _present_forms(core):
                    if pf in ew and pf != core and pf.endswith("th"):
                        swap = pf
                        break
            if not swap and t is None:
                # THE MARKER IS DECISIVE (user, 2026-09-05: "Sa and Na are past
                # tense particles"). When the verse has no form of this verb to
                # copy, the past is still written: the strong verbs from the
                # table (come -> came), and a regular verb the verse attests in
                # some form (believe / believeth -> believed). A word the verse
                # never uses at all is left alone -- it may be a noun.
                for base in _bases(core):
                    if base in BASE_TO_PAST and base not in ("is", "are", "am", "hath", "has", "have"):
                        swap = BASE_TO_PAST[base][0]
                        break
                    # a regular verb only when the verse shows it CONJUGATED
                    # (-eth / -s); the bare word proves nothing -- "grace" and
                    # "priest" are nouns and came out "graced", "priested"
                    if any(f in ew for f in _present_forms(base) if f != base and f != core and f.endswith(("eth", "th", "s"))) \
                            and base not in ("grace", "priest", "witness", "light", "life", "name", "word", "world", "truth", "peace", "glass", "cross", "house"):
                        swap = _past_forms(base)[0]
                        break
        elif want == "PRESENT" and t == "PAST" and core in PAST_TO_BASE:
            for pf in _present_forms(PAST_TO_BASE[core]):
                if pf in ew and pf != core:
                    swap = pf
                    break
        if swap:
            words[k] = w.replace(core, swap) if core in w else w.lower().replace(core, swap)
    return " ".join(words)
