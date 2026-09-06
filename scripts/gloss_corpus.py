"""
A FIRST-PASS interlinear for the Doctrine and Covenants and the Pearl of Great
Price, built from the Book of Mormon's own curation.

The Book of Mormon's 6,604 verses were glossed by hand across 239 chapter
scripts, and that work is an inventory: 42,538 distinct Samoan units, each with
the English the translator chose for it. Greedy longest-match segmentation of
the new volumes against that inventory covers 93.8% of their 186,684 tokens.
So this does not gloss Samoan -- it REUSES glosses this project already
settled, and refuses to do anything else.

THE RULES, and they are all refusals:

  Never invent. A unit is glossed only if the Book of Mormon glossed that exact
  unit. Anything unmatched stays empty, as the whole corpus was before curation.

  Where the Book of Mormon settled on ONE reading, use it.

  Where it drifted -- 1,367 units are glossed more than one way, because `i luga
  o` really is "upon" or "over" depending on what is above what -- the verse's
  own printed English decides, by testing which candidate's content words the
  English actually carries.

  Where nothing decides it, leave it EMPTY unless the unit is closed class,
  where the dominant reading is safe because the ambiguity is grammatical
  rather than semantic.

WHAT THIS IS NOT. It is not curation. It is the state the Book of Mormon was in
before its 239 passes: a starting point that a reader can use and a translator
can correct. Every verse it touches is listed under `generated` in
bom_overrides.json so a later audit can tell machine-proposed from
hand-curated, and so this can be re-run without trampling curation that has
happened since.

    python3 gloss_corpus.py [--dry-run] [--limit N]          (the whole corpus: bom / dc / pgp)
    python3 gloss_corpus.py --bible [--book id] [--debug key]  (O le Tusi Paia)
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_grammar as CG            # noqa: E402
import samoan_grammar as SG           # noqa: E402
import english_register as ER

# The English side of the gloss -- register, morphology, vocabulary -- lives
# in english_register so the checker and the grammar give the same answers.
FUNCTION_ONLY = ER.FUNCTION_ONLY
NEGATIONS = ER.PROTECTED
_stems = ER.stems
in_english = ER.in_english
def modernise(text: str) -> str:
    """Archaic English out of a gloss -- for the Book of Mormon volumes. O le
    Tusi Paia keeps the KJV's forms (user, 2026-09-05: "putting modern for
    this is going to make it hard because it will break the rules")."""
    if MODE["bible"]:
        return text
    return ER.modernise(text)
english_vocabulary = ER.vocabulary

RES = HERE.parent / "O le Tusi a Mamona Interlinear" / "Resources"
CONT = "·"


def norm(sm: str) -> str:
    """One key per word. See samoan_grammar.normalise_glottal: four codepoints
    spell the glottal in this corpus, and four spellings of one letter would
    split it across four index keys."""
    return re.sub(r"[^\w’\- ]", "",
                  SG.normalise_glottal(sm)).lower().strip()


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']+", (text or "").lower())}


def load_evidence() -> list:
    """The hand-curated Samoan/English unit pairs.

    They live in their own file now. They used to be read back out of
    bom_overrides.json, which is the file this script WRITES -- so its own
    guesses came back as evidence and two runs disagreed. Evidence is a fixed
    record of what a human decided; it is never the output of a pass.
    """
    data = json.loads((RES / "curated_evidence.json").read_text(encoding="utf-8"))
    return data["units"]


def build_inventory(units: list) -> dict[str, Counter]:
    inv: dict[str, Counter] = defaultdict(Counter)
    for sm, en in units:
        k = norm(sm)
        if k:
            inv[k][en] += 1
    return inv


def vetoed(gloss: str, english: str) -> bool:
    """The canon's VETO: a gloss whose content words are nowhere in the verse.

    Not a demand that the English confirm the gloss -- the two translations
    choose different words constantly and requiring agreement would empty the
    page. This only refuses a gloss the English has no room for at all.

    It is the rule that matters most here, because the inventory carries the
    Book of Mormon's context, not this verse's. `mata o` is "faces of" in the
    Book of Mormon and this verse says "no eye that shall not see"; `maia` is
    "I pray" there and this verse is "Hearken, O ye people". Both were being
    written because the unit had exactly one Book of Mormon reading and a
    single reading was trusted without asking.
    """
    ew = content_words(english)
    core = [w for w in re.findall(r"[a-z']+", gloss.lower())
            if w not in FUNCTION_ONLY]
    if not core:
        return False                      # function words are always allowed
    return not any(in_english(w, ew) for w in core)


# ── THE WORD LEXICON, DERIVED FROM THE CURATION ──────────────────────────────
# The inventory can only answer for a string it has seen whole, so common words
# came out unmatched simply because they never stood alone: `fetalai` (speak)
# occurs 561 times in the Book of Mormon and never once as a unit of its own,
# always inside "ua fetalai mai ai" and its kin.
#
# But those units can be taken apart, without any positional guessing. Strip a
# unit's CLOSED-CLASS tokens -- the grammar knows exactly which they are -- and
# strip the gloss's function words. Where that leaves precisely one Samoan word
# and one English word, the pairing is forced: `ua fetalai mai ai` -> "saith"
# has `ua`, `mai` and `ai` all closed class, so "saith" can only belong to
# `fetalai`. Nothing is aligned by position, which is the error that produced
# the Spanish corpus's worst damage; it is arithmetic on what is left over.
#
# 111,683 curated units yield 2,796 Samoan words, 1,857 of them attested more
# than once. This is the project's own translation work, read back as a
# dictionary.

def build_word_lexicon(units: list) -> dict[str, Counter]:
    lex: dict[str, Counter] = defaultdict(Counter)
    for sm, en in units:
        if True:
            toks = norm(sm).split()
            if not toks:
                continue
            open_toks = [t for t in toks if t not in SG.CLOSED_CLASS]
            # The dictionary is built modern. The Book of Mormon's curated
            # glosses are KJV-register, so `cometh` and `comes` would sit in
            # this lexicon as two different words for one Samoan verb, each
            # with half the evidence. Modernising here merges them.
            core = [w for w in re.findall(r"[a-z']+", ER.modernise(en).lower())
                    if w not in FUNCTION_ONLY]
            if len(open_toks) == 1 and len(core) == 1:
                lex[open_toks[0]][core[0]] += 1
    return lex


# ── SEGMENTATION: memory first, then the rule ────────────────────────────────
# Order matters, and I had it backwards. Putting the grammar's frames first
# looked principled and cost 12 points of coverage: a TAM frame happily spans
# "sa latou faia atu" and then nothing can gloss it, because the grammar knows
# the particles and not the verb between them. The Book of Mormon's 42,538
# units are CURATED -- a human decided each one -- so they are the ground
# truth for anything longer than a word.
#
# The grammar's job is the gap that memory structurally cannot fill: the
# closed-class forms that never occur alone in the Book of Mormon and so were
# never recorded as units. `te` 264 times, `ni` 113, `la’u` 98, `au` 84,
# `laua` 64 -- all in the grammar, none in the inventory.
#
# And TAM markers and directionals are ABSORBED: where nothing matches at a
# particle, it joins the unit that follows rather than being left blank, which
# is what the Book of Mormon's own curation does with them.

def build_names(books) -> set:
    """Proper names, derived: capitalised mid-verse and never lowercase.

    Nothing is hand-listed. A Samoan word that is always written with a capital
    somewhere other than the first position of a verse, and never written in
    lower case anywhere in 10,893 verses, is a name.
    """
    from collections import Counter
    up, low = Counter(), Counter()
    for b in books:
        for ch in b["chapters"]:
            for v in ch["verses"]:
                for i, w in enumerate(v["words"]):
                    t = re.sub(r"[^\w’]", "", w["sm"])
                    if len(t) < 3:
                        continue
                    if t[0].isupper():
                        if i > 0:
                            up[t.lower()] += 1
                    else:
                        low[t.lower()] += 1
    return {t for t, n in up.items() if n >= 2 and low.get(t, 0) == 0}


MODE = {"bible": False}   # set while O le Tusi Paia is glossed: its own readings apply
RAW_EN = {"text": ""}     # the verse's KJV English before modernise(): "lighteth" lives here


def term_of(key):
    """A registered term: the shared vocabulary, plus the Bible's own when the
    Bible is being glossed."""
    return SG.vocabulary(key) or (MODE["bible"] and SG.bible_vocabulary(key)) or None


VOCAB_MAXLEN = max(max(len(k.split()) for k in list(SG.VOCABULARY) + list(SG.BIBLE_VOCABULARY)),
                   max((len(k.split()) for k in getattr(SG, "TRANSLITERATED", {})), default=1), 3)


def seq_frame_span(toks, i):
    """`ona VERB (ai) lea` as one unit: the span length from `ona` to its closing
    `lea`, or 0. The verb phrase between is one to four tokens; `ona o …`
    ("because of") is a different word and never opens the frame."""
    if norm(toks[i]) != "ona" or i + 2 >= len(toks):
        return 0
    prev = toks[i - 1] if i else ""
    if not (i == 0 or prev[-1:] in SG.CLAUSE_END or norm(prev) in ("ma", "a", "ae")):
        return 0
    if norm(toks[i + 1]) == "o":
        return 0
    for k in range(i + 2, min(i + 7, len(toks))):
        if norm(toks[k]) == "lea":
            # the span may not run over a sentence stop before its `lea`
            if any(re.search(r"[.;:?!][”’\"')]*$", toks[m]) for m in range(i, k)):
                return 0
            return k - i + 1
    return 0


def frame_at(toks, i, inv, maxlen, lex=None, names=frozenset(), seq=False):
    """(length, source) of the unit starting at i, or (0, '').

    Memory is still consulted first -- a curated unit is a human decision and
    the grammar is not better than one. But memory may no longer draw a
    boundary the GRAMMAR forbids, and that is the whole change: the curation
    recorded `i luga o` and `o loo i` as units, and both cut a construction in
    half. Two rules govern every candidate span, whatever proposed it.
    """
    def n(a, b=None):
        return norm(" ".join(toks[a:b if b is not None else a + 1]))

    def cuts_a_construction(a, b):
        """Does the span [a, b) stop part-way through a grammar frame?

        `o loo i luga o motu` was segmented `o loo i` + `luga o` because the
        curation happens to contain `o loo i`. `i luga` is a preposition, and
        a unit that ends on its `i` has taken its head. This asks, of every
        position inside the span, whether a grammar frame starts there and
        runs past the end.
        """
        for k in range(a, b):
            for m in range(SG.MAX_FORM_LEN, 1, -1):
                if k + m > b and k + m <= len(toks) and n(k, k + m) in SG.MULTI_FORMS:
                    return True
        return False

    # 00. THE SEQUENTIAL FRAME IS ONE UNIT (the Bible): `ona malamalama ai lea`
    #     is "and there was light", glossed on its closing `lea`, the tokens
    #     before it continuing into it -- as the curation records `ona
    #     vaeluaina ai lea` "and they divided".
    if seq:
        span = seq_frame_span(toks, i)
        if span:
            return span, "seqframe"

    # 00b. THE NEGATIVE FRAME `e lei` / `e le` IS A UNIT before the lone `e` can
    #      take its ergative reading ("by") -- John 1:3 printed `e=by lei=not`.
    if MODE["bible"] and i + 1 < len(toks) and n(i, i + 2) in NEG_UNITS:
        return 2, "neg"

    # 0. A REGISTERED TERM OR IDIOM IS ITS OWN UNIT, BEFORE MEMORY. `i le ua
    #    faapea lava` is "and it was so"; the inventory knows `i le ua` (on the
    #    neck) and would take it first. A transliterated term likewise, even
    #    where nothing in the curation ever glossed it -- `sume` and `eseroma`
    #    head no unit in the Book of Mormon. Longest span first, up to the
    #    longest registered key.
    for span in range(min(VOCAB_MAXLEN, len(toks) - i), 0, -1):
        if SG.transliterated(n(i, i + span)) or term_of(n(i, i + span)):
            return span, "term"

    def eats_a_name(a, b):
        """A NAME OPENS ITS OWN PHRASE — always, not just after a verb.

        Nothing may precede a proper name inside a unit except another name
        (`Anti-Nifae-Liae`). The English of whatever stands in front of it
        lands on the name otherwise, and it always did:

            maua e sa Lamanā  ->  "the Lamanites have taken"   the verb
            i Aikupito        ->  "into Egypt"                 the preposition
            ia Siona          ->  "against Zion"               the preposition
            faapea ona ... Iesu -> "when Jesus had spoken"     the whole clause

        Split, each of those says its own word: `i` "into", `ia` "against",
        `maua` "taken", and the name says the name.
        """
        for k in range(a + 1, b):
            here = (n(k) in names or SG.transliterated(n(k))
                    or n(k) in SG.DIRECTIONALS)
            if not here:
                continue
            prev = n(k - 1)
            if (prev in names or SG.transliterated(prev)
                    or prev in SG.DIRECTIONALS):
                continue
            # A PARTICLE BELONGS WITH THE NAME. `O Nifae` is one phrase, and
            # the curation says so 1,011 times -- `o` + name glossed "Nephi"
            # bare 95 times, "of Israel" 118, "of Nephi" 54. So do `e` + name
            # ("Alma" 47, "Moroni" 47), `a` + name ("of Christ" 25), `ia` +
            # name ("in Christ" 50), `i` + name ("at Jerusalem"), `ma` + name
            # ("and Sam"). Barring those was wrong and this is the correction.
            #
            # A NOUN the name qualifies belongs with it too, ADJACENTLY:
            # `o tagata Iutaia` is "of the Jews".
            #
            # What must not happen is a VERB reaching across particles to the
            # name, because then the clause's English lands there:
            #   maua e sa Lamanā  -> "the Lamanites have taken"
            #   ... Iesu          -> "when Jesus had spoken"
            # so an open-class word before the name is allowed only when it is
            # the token immediately before it.
            for j in range(a, k - 1):
                if (n(j) not in SG.CLOSED_CLASS and n(j) not in SG.AMBIGUOUS
                        and n(j) not in names and not SG.transliterated(n(j))):
                    return True
        # A BOUND PRONOUN SAYS ITS OWN WORD. `sa ia faapa’ū ifo` is the past
        # marker + "he" + "fell" + "down" (the user's own reading), and
        # swallowed whole it printed NOTHING at all in 1 Nephi 1:7, while
        # elsewhere the clause landed on the directional -- `atu` "he spake".
        #
        # This was tried twice and reverted twice. The first failure had a
        # cause -- `maua` and `taua` sat in the pronoun table on the wrong
        # forms, so every "obtain" and every "war" became "we two". With those
        # struck it was measured again on its merits and is still wrong:
        # content F1 86.4 -> 85.0, coverage 92.8% -> 90.8%, and it does not
        # even fix the verse that prompted it. Splitting a verb from the
        # pronoun bound to it costs more than the pronoun is worth.
        return False

    def joins_two_clauses(a, b):
        """A COORDINATOR OPENS ITS OWN UNIT. `ma ua ou tusia` is four words
        doing four jobs -- "and", the tense marker, "I", "write" -- and the
        curation records it whole, so the coordinator's "and" and the bound
        pronoun's "I" both vanished and only "written" was printed."""
        if b - a <= 1 or n(a) not in SG.COORDINATORS:
            return False
        # unless the coordinator is the first word of a frame the grammar
        # knows -- `ae ui i lea` is "nevertheless", not "but" plus three words
        return not SG.primary_gloss(n(a, b))

    def crosses_a_stop(a, b):
        """A UNIT ENDS WHERE THE SENTENCE ENDS. Punctuation is stripped when a
        span is keyed, so `po. O le afiafi` matched the curated unit `po o`
        ("or") straight across the full stop. No token but the last may close a
        sentence."""
        return any(re.search(r"[.;:?!][”’\"')]*$", toks[k]) for k in range(a, b - 1))

    def ends_on_frame_close(a, b):
        """`ai lea` closes the `ona …` frame and belongs to no verb: a span
        that swallows the `ai` (`malamalama ai`) lands the verb's English on
        the particle."""
        if b - a <= 1:
            return False
        last = n(b - 1); after = n(b) if b < len(toks) else ""
        before = [n(k) for k in range(max(0, a - 6), b - 1)]
        if last == "ai" and after == "lea" and "ona" in before:
            return True
        if last == "lea" and n(b - 2) == "ai":
            return True
        return False

    def swallows_a_term(a, b):
        """A REGISTERED TERM IS ITS OWN UNIT even when memory has a longer span
        across it: `ua maliu mai` was remembered whole as "death", so the
        registered `maliu mai` "come" never got its turn (John 1:9, 1:11)."""
        for k in range(a + 1, b):
            for L in range(1, VOCAB_MAXLEN + 1):
                if k + L > len(toks):
                    break
                key = n(k, k + L)   # inside the span, or running past its end (`ua maliu` | `mai`)
                if term_of(key) or SG.transliterated(key) or key in NEG_UNITS:
                    return True
        return False

    def spans_predicate_and_subject(a, b):
        """`Sa ia te ia le ola` was one remembered unit ("the life"): a span that
        starts on a tense marker, runs through the phrase headed by i / ia, and
        on into a NEW noun phrase holds the whole simple sentence. The sentence
        pass needs marker, predicate and subject as separate units."""
        if b - a < 4 or n(a) not in SG.TAM or n(a + 1) not in ("i", "ia", "iā"):
            return False
        for k in range(a + 3, b):
            prev, prev2 = n(k - 1), n(k - 2)
            # `ia te ia le ola`: the `ia` before `le` is the pronoun after `te`,
            # so `le ola` opens the subject
            after_prep = prev in ("i", "ia", "iā", "o", "a", "e", "ma", "mo", "mai", "ona") and not (prev == "ia" and prev2 == "te")
            if n(k) in ("le", "se", "lo", "la", "ni") and not after_prep:
                return True
        return False

    def swallows_an_agent(a, b):
        """`faia e ia` was one remembered unit ("made"): the ergative agent `e` +
        pronoun / name after a verb says its own "by him" (user, John 1:3)."""
        for k in range(a + 1, b - 1):
            # the agent may be a pronoun, a name, or an indefinite noun phrase
            # (`vaaia le Atua e se tasi` "seen God by any man"); `e le` stays
            # out, being the negative as often as the agent
            if n(k) == "e" and (n(k + 1) in AGENT_PRONOUNS or n(k + 1) in ("se", "ni") or (toks[k + 1][:1].isupper() and n(k + 1) not in SG.CLOSED_CLASS)) \
                    and n(k - 1) not in SG.TAM and n(k - 1) not in ("e", "le", "lē", "lei"):
                return True
        return False

    def ends_on_agent_head(a, b):
        """A span that ENDS on `e` while an agent phrase follows has taken the
        ergative marker off the agent: `le Atua e | se tasi` was remembered as
        the vocative "O God" in John 1:18, where `e se tasi` is "by any man"."""
        if b - a < 2 or n(b - 1) != "e" or b >= len(toks):
            return False
        nxt = n(b)
        return (nxt in AGENT_PRONOUNS or nxt in ("se", "ni", "le", "lona", "lana", "ona", "ana")
                or (toks[b][:1].isupper() and nxt not in SG.CLOSED_CLASS))

    def starts_on_negator(a, b):
        """A span opening on `le` right after a marker or bound pronoun opens
        on the NEGATOR (`lua te | le oti lava` "ye shall not die"): remembered
        whole, the unit said "die" and the "not" was gone."""
        if b - a < 2 or n(a) not in ("le", "lē") or a == 0:
            return False
        prev = n(a - 1)
        return prev in SG.LE_NEG_BEFORE and not re.search(r"[,;:.?!][”’\"')]*$", toks[a - 1])

    def legal(span):
        key = n(i, i + span)
        if joins_two_clauses(i, i + span) or crosses_a_stop(i, i + span) or ends_on_frame_close(i, i + span):
            return False
        if MODE["bible"] and (spans_predicate_and_subject(i, i + span) or swallows_an_agent(i, i + span)
                              or ends_on_agent_head(i, i + span) or starts_on_negator(i, i + span)):
            return False
        # `o` heads the phrase that follows it, so no unit ends on one
        return (not SG.ends_mid_phrase(key)
                and not cuts_a_construction(i, i + span)
                and not eats_a_name(i, i + span)
                and not swallows_a_term(i, i + span))

    # 1. curated memory, longest first -- subject to both rules
    for span in range(min(maxlen, len(toks) - i), 0, -1):
        if n(i, i + span) in inv and legal(span):
            return span, "inv"

    # 2. ANY multi-token grammar frame, longest first. This used to test
    #    complex prepositions only, so the TAM pairs were invisible to the
    #    segmenter: `o loo` could never be found as a unit and only survived
    #    where the curation happened to contain it.
    for span in range(min(SG.MAX_FORM_LEN, len(toks) - i), 1, -1):
        key = n(i, i + span)
        if not legal(span):
            continue
        # a grammar frame is one phrase: it never runs across a comma (`manatu
        # atoa, ma le malosi` is not `atoa ma` "together with")
        if any(toks[k].rstrip().endswith((",", ";", ":")) for k in range(i, i + span - 1)):
            continue
        if key in SG.COMPLEX_PREPOSITIONS:
            return span, "prep"
        if SG.primary_gloss(key):
            return span, "rule"

    # 3. (see the top of this function: registered terms are matched first)

    # 4. a closed-class form the grammar can gloss on its own
    if SG.primary_gloss(n(i)):
        return 1, "rule"

    # 4. a single open-class word the curation defines
    if lex and n(i) in lex:
        return 1, "lex"

    # 5. an absorbed particle joins what follows: extend until something is
    #    known, up to the 5-token cluster GLOSSING_RULES.md allows
    if n(i) in SG.ABSORBED:
        for span in range(2, min(6, len(toks) - i + 1)):
            for inner in range(span - 1, 0, -1):
                if n(i + span - inner, i + span) in inv:
                    return span, "absorbed"
        return 0, ""

    return 0, ""


def align_number(gloss: str, english: str) -> str:
    """Take the number from the verse, not from the Book of Mormon.

    The inventory carries whatever number the source verse had. D&C 1:2 reads
    "neither ear that shall not hear, neither heart that shall not be
    penetrated" and was glossed "the ears" and "the hearts of", because that is
    how the Book of Mormon used those words.

    The canon veto did not catch it: it stems before comparing, so `ears`
    matches `ear` and the gloss passes as "carried by the English". That test
    is asking whether the WORD is right, and it should be, or a legitimate
    plural would be refused. Number is a separate question, and the English of
    this very verse answers it -- if the gloss says `ears` where the verse says
    `ear` and never says `ears`, the verse wins.

    Only ever swaps between the singular and plural of the SAME word. It cannot
    change which word is used, so it cannot introduce a wrong reading.
    """
    ew = set(re.findall(r"[a-z']+", (english or "").lower()))
    if not ew:
        return gloss

    def fix(m):
        w = m.group(0)
        low = w.lower()
        if low in ew or low in FUNCTION_ONLY or ER.ARCHAIC.get(low, set()) & ew:
            return w
        for other in _stems(low) - {low}:
            if other in ew:
                # keep the original capitalisation
                return other.capitalize() if w[:1].isupper() else other
        return w

    return re.sub(r"[A-Za-z']+", fix, gloss)


HEAD_TRIMMABLE = {"with", "and", "or", "but", "of", "for", "by", "from",
                  "upon", "at", "on", "in"}


def trim_absent_tail(gloss: str, english: str) -> str:
    """Drop leading and trailing function words the verse does not have.

    A single remembered reading is used as it stands, which is right for the
    word and can be wrong at the edges: `faatasi` is "together with" in the
    Book of Mormon, and D&C 1:1 reads "listen together" with no "with"
    anywhere. The scoring that would have caught it only runs when there is
    more than one candidate to score.

    Deliberately timid. Trailing only, function words only, and only when the
    verse does not contain them -- so it can shorten a gloss but never change
    which words it uses, and it stops at the first content word.
    """
    ew = set(re.findall(r"[a-z']+", (english or "").lower()))
    if not ew:
        return gloss
    parts = gloss.split()

    def absent(word: str) -> bool:
        w = re.sub(r"[^a-z']", "", word.lower())
        return bool(w) and (w in FUNCTION_ONLY and w not in NEGATIONS
                            and not in_english(w, ew))

    # BOTH ends, but not the same words at each. `ma outou` is "with you" in
    # the Book of Mormon and D&C 1:1 reads "and ye that are upon the islands"
    # -- `ma` is "and" there, and a gloss saying "with" asserts a relation the
    # verse does not have. Dropping it leaves "you": less, but not wrong.
    #
    # The head is the RISKIER end and gets a narrower list. Trailing function
    # words are prepositions and particles; LEADING ones are as often the
    # auxiliary that carries the tense, and the general rule turned
    # "shall not see" into "not see". Only relational words come off the front.
    while len(parts) > 1 and absent(parts[-1]):
        parts.pop()
    # IN THE BIBLE the curated unit's relative and auxiliary words come off the
    # head too when the verse has none of them: `sa mau` is "which did dwell"
    # in the Book of Mormon and John 1:14 reads "and dwelt among us"
    # -- but never the pronoun itself (`o i latou` "they were" keeps its "they")
    head_set = HEAD_TRIMMABLE | {"is", "are", "was", "were"} | ({"which", "that", "who", "whom", "did", "do", "it", "there", "then", "so", "as", "even", "yea", "now"} if MODE["bible"] else set())

    def absent_head(word: str) -> bool:
        w = re.sub(r"[^a-z']", "", word.lower())
        return bool(w) and w in head_set and w not in NEGATIONS and not in_english(w, ew)

    while len(parts) > 1 and absent_head(parts[0]):
        parts.pop(0)
    return " ".join(parts)


_EN_NAMES = None


def english_names() -> set:
    """English proper names: words the canon never writes in lower case."""
    global _EN_NAMES
    if _EN_NAMES is None:
        from collections import Counter
        up, low = Counter(), Counter()
        for name in ("bom_english.json", "tusi_paia_english.json"):
            if not (RES / name).exists():
                continue
            data = json.loads((RES / name).read_text(encoding="utf-8"))
            for v in data.values():
                # a hyphenated compound is one word: "Ramath-lehi" (Judges 15) is
                # not a lower-case "lehi", and must not cost Lehi his capital
                for w in re.findall(r"[A-Za-z][a-z']+(?:-[A-Za-z][a-z']+)*", v):
                    (up if w[0].isupper() else low)[w.lower()] += 1
        _EN_NAMES = {w for w, n in up.items() if n >= 2 and low.get(w, 0) == 0}
    return _EN_NAMES


# ── MORPHOLOGY ──────────────────────────────────────────────────────────────────
# `faamalamalamaina` = faʻa- (causative) + malamalama (light) + -ina (transitive /
# passive). The lexicons hold the stem, not every conjugated form, so a form
# nobody glossed is taken apart: suffix off, prefix off, the stem or root looked
# up, the English composed -- and the verse's own inflection preferred
# ("lighteth"). User, 2026-09-05: "the tool needs to be able to conjugate words".
MORPH_SUFFIXES = ["aina", "ina", "ia", "ga", "aʻi", "a‘i", "a’i", "ai", "a", "na"]
# a verb fused with its directional particle, the verb's final vowel elided:
# ave + atu -> avatu (give away / to), au + mai -> aumai (bring hither)
DIRECTIONALS = [("atu", "away"), ("mai", "hither"), ("ane", "along"), ("ifo", "down"), ("aʻe", "up"), ("a‘e", "up"), ("ae", "up")]
MORPH_PREFIXES = [("faʻa", "cause"), ("fa‘a", "cause"), ("fa’a", "cause"), ("faa", "cause"),
                  ("fe", "reciprocal"), ("ta", "plain"), ("ma", "stative")]


# the copulas and auxiliaries are never nominalised: "which is" is not "which ising"
_NO_GERUND = {"is", "are", "was", "were", "am", "be", "been", "being", "have", "has", "hath", "had",
              "do", "does", "did", "shall", "will", "may", "might", "can", "could", "should", "would",
              "not", "the", "a", "an", "of", "to", "and", "that", "which", "who"}


def _gerund(base: str) -> str:
    """come -> coming, begin -> beginning, see -> seeing; a copula stays itself."""
    b = base.lower()
    if b in _NO_GERUND:
        return base
    if b.endswith("ie"):
        return b[:-2] + "ying"
    if b.endswith("e") and not b.endswith("ee"):
        return b[:-1] + "ing"
    if len(b) >= 3 and b[-1] not in "aeiouwxy" and b[-2] in "aeiou" and b[-3] not in "aeiou" and b not in ("come", "open", "listen", "visit", "enter", "offer", "gather", "answer", "suffer", "wander", "murmur", "labor", "labour", "utter", "order", "cover", "deliver"):
        return b + b[-1] + "ing"
    return b + "ing"


def _dereduplicate(word: str) -> list[str]:
    """The stems a reduplicated form may come from.

    Samoan doubles in two ways (the user, on John 1:14: "redundancy words /
    multiplying ... mata for example see ... matamata seen"):
      the WHOLE ROOT   mata + mata = matamata  look at, behold (repeated or
                       intensified action; savali / savalivali walk about,
                       fai / faifai keep doing; tagi / tagitagi keep crying)
      ONE SYLLABLE     nofo / nonofo, moe / momoe, galue / galulue, poto /
                       popoto, malosi / malolosi, umi / uumi -- the PLURAL,
                       agreeing with a plural doer or noun (Dunn, unit two)
    Whole-root candidates first, then a doubled syllable, longest first."""
    w = word.lower()
    out = []
    half = len(w) // 2
    if len(w) % 2 == 0 and half >= 2 and w[:half] == w[half:]:
        out.append(w[:half])
    for L in (3, 2, 1):
        for i in range(len(w) - 2 * L + 1):
            piece = w[i:i + L]
            if piece == w[i + L:i + 2 * L] and any(v in piece for v in "aeiou"):
                cand = w[:i + L] + w[i + 2 * L:]
                if len(cand) >= 3 and cand not in out:
                    out.append(cand)
    return out


def _senses(word: str, lex) -> list[str]:
    out = []
    if lex is not None and word in lex:
        top = dominant_lemma(lex[word])
        if top:
            out.append(top)
        for g, n in lex[word].most_common(3):
            if g and g not in out and len(g.split()) <= 2:
                out.append(g)
    for sense in SG.dictionary(word):
        for alt in re.split(r"[,;]", sense):
            alt = re.sub(r"^\s*to\s+", "", alt).strip()
            if alt and alt not in out and len(alt.split()) <= 3:
                out.append(alt)
    return out


def morph_gloss(word: str, en_text: str, lex, want_tense=None, verse_only: bool = False) -> str:
    """A gloss for a form the lexicons do not hold, by its parts; '' if none.

    The verse's own inflection of ANY part's sense wins first (root malamalama
    "light" -> the KJV's "lighteth"); only then is the English composed from the
    stem's first sense, or from the root under its prefix's frame."""
    w = word.lower()
    raw = set(re.findall(r"[a-z']+", (RAW_EN["text"] or "").lower()))
    ew = set(re.findall(r"[a-z']+", (en_text or "").lower())) | raw

    def verse_form(base: str):
        """The verse's own inflection of a candidate word: under a present
        marker the -eth/-s form first (lighteth), under a past one the past
        form first, the bare word last. The KJV's own form ("lighteth") beats
        the modernised one ("lights")."""
        base = re.sub(r"[^a-z]", "", base)
        if not base:
            return None
        pres, past = ER._present_forms(base), ER._past_forms(base)
        order = (pres + past + [base]) if want_tense == "PRESENT" else (past + pres + [base]) if want_tense in ("PAST", "PERFECT") else ([base] + pres + past)
        for pool in (raw, ew):
            for form in order:
                if form in pool:
                    return form
        return None

    parts = []          # (cands, frame) in order of preference
    # 0. a fused directional: the verb with its elided vowel restored
    for suf, _sense in DIRECTIONALS:
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            stem = w[:-len(suf)]
            for stem2 in (stem, stem + "e", stem + "a", stem + "i", stem + "o", stem + "u"):
                c = _senses(stem2, lex)
                if c:
                    parts.append((c, "plain"))
                    break
            if parts:
                break
    for suf in MORPH_SUFFIXES:
        if parts:
            break
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            stem = w[:-len(suf)]
            c = _senses(stem, lex)
            if c:
                parts.append((c, "noun" if suf == "ga" else "plain"))
            for pre, frame in MORPH_PREFIXES:
                if stem.startswith(pre) and len(stem) - len(pre) >= 3:
                    c = _senses(stem[len(pre):], lex)
                    if c:
                        parts.append((c, frame))
            if parts:
                break
    if not parts:
        for pre, frame in MORPH_PREFIXES:
            if w.startswith(pre) and len(w) - len(pre) >= 3:
                c = _senses(w[len(pre):], lex)
                if c:
                    parts.append((c, frame))
    if not parts:
        # REDUPLICATION IS THE PLURAL (Dunn, unit two): a verb or adjective
        # agrees with a plural doer by doubling its stressed syllable -- nofo /
        # nonofo (dwell), moe / momoe (sleep), galue / galulue (work), poto /
        # popoto (wise), malosi / malolosi (strong), umi / uumi (tall). The
        # word is the same word; the number rides on the subject.
        for stem2 in _dereduplicate(w):
            c = _senses(stem2, lex)
            if c:
                parts.append((c, "plural"))
                break
    if not parts:
        return ""
    # 1. the verse's own form of any sense
    for cands, frame in parts:
        for c in cands:
            for piece in c.split():
                vf = verse_form(piece)
                if vf and piece not in ("the", "a", "an", "of", "to", "be", "is", "was"):
                    return vf
    if verse_only:
        return ""
    # 2. composed
    cands, frame = parts[0]
    c = cands[0]
    if frame == "cause":
        g = "give light" if c in ("light", "clear", "bright", "brighten") else (f"cause to {c}" if ER.tense_of(c) else f"make {c}")
    elif frame == "reciprocal":
        g = f"{c} one another"
    elif frame == "noun":
        # THE SUFFIX -ga MAKES A VERB A NOUN (Dunn, unit seven): amata / amataga
        # "beginning", faaali / faaaliga "revelation", galue / galuega "work".
        # The verse's own noun was tried above; composed, the gerund stands.
        head = c.split()[-1]
        if head in ER.BASE_TO_PAST or head in ER.PAST_TO_BASE or ER.tense_of(head):
            base = ER.PAST_TO_BASE.get(head, head)
            g = " ".join(c.split()[:-1] + [_gerund(base)])
        else:
            g = c
    else:
        g = c
    if g and want_tense:
        g = ER.agree_tense(g, want_tense, en_text)
    return g


def dominant_lemma(dist) -> str:
    """The one word a token means, when its lexicon agrees on the word and
    only disagrees on the form.

    `tusia` is written 84, write 61, wrote 9, kept 4 -- one verb in three
    tenses, and no single spelling reaches a majority, so a threshold on the
    top READING refuses a word the corpus is unanimous about. Cluster the
    forms first, then ask whether one LEMMA dominates: 154 of 158, 97%.

    Returns '' when the disagreement is real, which is the point -- a token
    read two different ways still says nothing.
    """
    total = sum(dist.values())
    if total < 3:
        return ""
    groups: list[list] = []
    for word, n in dist.most_common():
        for g in groups:
            if difflib.SequenceMatcher(None, g[0][0], word).ratio() >= 0.6:
                g.append((word, n))
                break
        else:
            groups.append([(word, n)])
    sizes = sorted((sum(n for _, n in g), i) for i, g in enumerate(groups))
    top, idx = sizes[-1]
    runner = sizes[-2][0] if len(sizes) > 1 else 0
    # A FIXED SHARE IS THE WRONG TEST when the runner-up is tiny. `foliga` is
    # appear/appears/appeared/appearance 10 times of 17 -- 58.8%, under a 60%
    # bar -- against a next-biggest group of 2. That is not a disagreement, it
    # is one word with a long tail, and the user confirms it: `e foliga mai`
    # means "it appears". So a clear plurality counts as well as a majority.
    if top / total < 0.60 and not (top >= 2 * runner and top / total >= 0.40):
        return ""
    return groups[idx][0][0]


def capitalise_names(gloss: str, key_sm: str, names) -> str:
    """A proper name is written with a capital -- and only the name is.

    `Iutaia` came out "jews", because the derived lexicon lowercases as it
    learns. Capitalising the whole unit instead gave "Of The Jews", so only
    the words the ENGLISH canon itself never writes lower case are raised.
    """
    if not any(t in names for t in key_sm.split()):
        return gloss
    en_names = english_names()
    return re.sub(r"[A-Za-z']+",
                  lambda m: (m.group(0).capitalize()
                             if m.group(0).lower() in en_names else m.group(0)),
                  gloss)


def choose_particle(form: str, english: str, inv, prev_key: str = "",
                    prev_tok: str = "", next_tok: str = "",
                    clause_initial: bool = False, before=(), after=(),
                    next_is_name: bool = False) -> tuple[str, str]:
    """Gloss a one-vowel particle from its CLOSED set of readings.

    choose() cannot do this job: every reading of a particle is a function
    word, so its content-word gate empties and it falls through to whichever
    reading the curation's segmentation parked on this token most often. Here
    the candidates are fixed by the grammar and the VERSE picks among them --
    frequency is only a tie-break, and a reading the verse does not contain is
    used only when the grammar has just one.
    """
    readings = SG.readings_in_frame(form, prev_tok, next_is_name) or SG.particle_readings(form)
    if not readings:
        return "", "absorbed-particle"
    # a locative frame already carries the English; its `o` says nothing more
    if form == "o" and prev_key in SG.SILENT_AFTER:
        return "", "silent-after-prep"
    ew = set(re.findall(r"[a-z']+", (english or "").lower()))

    # THE FRAME PROPOSES, THE VERSE CONFIRMS. A frame-only reading is written
    # only when the verse actually carries it, so a 72%-reliable frame costs
    # nothing on the 28%.
    framed = SG.contextual_reading(form, prev_tok, next_tok, clause_initial, before, after)
    if framed == "":
        return "", "silent-by-frame"
    if framed:
        for alt in framed.split("|"):        # 'then|and': the first the verse carries
            if all(in_english(w, ew) for w in re.findall(r"[a-z']+", alt)):
                return alt, "frame"
    if framed and form in FRAME_OR_SILENT:
        # the frame identified the construction; the verse has no word for
        # the marker, so the marker says nothing rather than a stray reading
        return "", "silent-by-frame"
    def carried(reading):
        # a reading of more than one word is present only if ALL of it is --
        # "to him" must not win on the "to" alone
        if not all(in_english(w, ew) for w in reading.split()):
            return False
        # A DIRECTIONAL IS AN ADVERB (Dunn: deixis on the verb). Its English
        # must stand as one -- "out" that heads "out of the land" belongs to
        # that phrase (`mai le laueleele`), and `atu` may not take it
        if form in SG.DIRECTIONALS and len(reading.split()) == 1:
            return bool(re.search(r"\b" + re.escape(reading) + r"\b(?!\s+(?:of|the|a|an|his|her|their|my|our|your|thy|unto|to|from|into)\b)", (english or "").lower()))
        return True

    # ORDER BEFORE COUNT. Each READINGS list is written in the curation's own
    # frequency order -- `i` is "in" 2,708 times, "to" 2,146, "upon" 857 --
    # and that beats inv, which counts whole gloss STRINGS and had `i` coming
    # out "to" in verses reading "in the commencement" and "at Jerusalem".
    scored = sorted(
        ((carried(r), -n, inv.get(form, {}).get(r, 0), r)
         for n, r in enumerate(readings)),
        reverse=True)
    present, _order, _weight, best = scored[0]
    if present:
        return best, "particle"
    if len(readings) == 1:
        return readings[0], "particle-sole"
    if form in ("a’o", "aʻo", "a‘o", "ina ua"):
        return readings[0], "particle-temporal"      # Dunn's temporal has a meaning even where the verse folds it
    return "", "particle-undecided"


# particles whose positional frame outranks a curated unit they would open:
# the sequential `ona … (ai) lea` and the noun `po`. Not `ia`, `tele`, `lava`:
# their curated units stand whole (splitting them cost the Book of Mormon a
# point of F1).
HEAD_FRAMES = {'ona', 'po'}

# markers whose frame reading, when the verse lacks it, means SILENT -- never
# a fall-through to the positional readings (`Ia tutupu` is not "that grow")
FRAME_OR_SILENT = {'ia', 'ona'}


def merge_punctuation(cands: Counter) -> Counter:
    """One reading is one reading, whatever punctuation trails it.

    `lona loto atoa` had exactly two readings in the curation -- "his whole
    heart," and "his whole heart" -- which is ONE reading recorded twice, and
    counting them apart split a unanimous vote 1-1 so neither could reach a
    majority and the unit came out blank. Every unit whose readings differ
    only in a comma had the same problem.

    The surviving surface is the commonest one, so the punctuation that the
    curation actually used most is what gets written.
    """
    groups: dict[str, Counter] = defaultdict(Counter)
    for gloss, n in cands.items():
        groups[re.sub(r"[^a-z ]", "", gloss.lower()).strip()][gloss] += n
    out: Counter = Counter()
    for _key, surfaces in groups.items():
        best = surfaces.most_common(1)[0][0]
        out[best] = sum(surfaces.values())
    return out


# A PARTICLE IS NEVER JUST BLANK. The user's rule: it is "either continuations
# of or part of the next". A blank says the tool does not know the word; for a
# closed-class token that is false -- it knows the word belongs to a
# neighbouring unit, and which neighbour follows from what kind of particle it
# is.
#
# LEANS BACK: the enclitics and post-verbal particles, which attach to the word
# in front of them. `ai` is the anaphoric -- `ma gatete tele ai` is "and
# tremble exceedingly", one unit (the user: "put it with the tele"), and `ai`
# alone was blank 1,987 times.
#
# LEANS FORWARD: the phrase heads and the tense markers, which stand in FRONT
# of what they govern -- `o` heads the next phrase, `ua` marks the verb after
# it. Those were the biggest blanks in the corpus: `o` 3,063, `e` 2,162,
# `ua` 1,499, `i` 963.
LEANS_BACK = {"ai", "lava", "uma", "foi", "fo’i", "atu", "mai", "ifo", "a’e",
              "aʻe", "ane", "pea", "lea", "aʻi", "a’i", "a'i"}


# English words that are never a leftover's partner: auxiliaries, the light
# verbs, and the copulas the Samoan says with a particle or not at all.
LEFTOVER_STOP = {"be", "been", "being", "is", "are", "was", "were", "am", "do", "does", "did",
                 "done", "have", "has", "had", "hath", "hast", "shall", "will", "would", "should",
                 "may", "might", "can", "could", "let", "said", "saith", "say", "says", "came",
                 "come", "went", "pass", "unto", "thereof", "therein", "thereto", "also", "even",
                 "yea", "behold", "now", "then", "there", "thus", "very", "own", "same"}


COPULA_TAM = {"sa": "was", "na": "was", "ua": "is", "e": "is", "o loo": "is", "loo": "is"}
CONNECTIVE_START = ("and ", "but ", "for ", "then ", "so ", "yet ", "nor ", "or ")


NOMINATIVE = {"him": "he", "her": "she", "them": "they", "us": "we", "me": "I"}
INTRANSITIVE = {"came", "come", "cometh", "went", "go", "goeth", "arose", "rose", "stood", "sat", "fell", "died",
                "lived", "dwelt", "departed", "returned", "passed", "fled", "ran", "walked", "entered", "ascended",
                "descended", "remained", "abode", "tarried", "journeyed", "slept", "wept", "rejoiced", "said", "saith",
                "spake", "answered", "cried", "prayed", "wondered", "marvelled", "feared", "trembled", "rested",
                "stayed", "turned", "looked", "appeared", "was", "were", "is", "became", "grew", "waxed", "laboured",
                "labored", "sinned", "repented", "fasted", "sailed", "escaped", "arrived", "fainted", "perished"}
PRON_PP = {"ia te ia": "him", "ia te au": "me", "ia te a’u": "me", "ia te aʻu": "me", "ia te oe": "thee",
           "ia te i latou": "them", "ia te i laua": "them", "ia te i matou": "us", "ia te i tatou": "us",
           "ia te i maua": "us", "ia te i taua": "us", "ia te outou": "you", "ia te oulua": "you"}
SUBJ_PRON = {"o ia": "he", "o i latou": "they", "o i laua": "they", "o i matou": "we", "o i tatou": "we",
             "o i maua": "we", "o i taua": "we", "o oe": "thou", "o a’u": "I", "o aʻu": "I", "o au": "I",
             "o outou": "ye", "o oulua": "ye"}
POSSESSIVE = {"lona": "his", "lana": "his", "ona": "his", "ana": "his",
              "lou": "thy", "lau": "thy", "ou": "thy", "au": "thy",
              "lo’u": "my", "la’u": "my", "loʻu": "my", "laʻu": "my", "lo‘u": "my", "la‘u": "my",
              "o’u": "my", "a’u": "my"}


# the two-token possessives: `lo latou pupula` "their brightness", `o matou uso`
# "our brethren" -- the merge below reads them as one possessive
PLURAL_POSS = {}
for _p, _e in (("latou", "their"), ("laua", "their"), ("matou", "our"), ("tatou", "our"), ("maua", "our"), ("taua", "our"), ("outou", "your"), ("oulua", "your")):
    for _a in ("lo", "la", "o", "a"):
        PLURAL_POSS[f"{_a} {_p}"] = _e


PREP_WORDS_ALL = {"with", "in", "at", "to", "unto", "for", "by", "from", "on", "upon", "among", "into", "before",
                  "after", "over", "under", "of", "through", "against", "toward", "towards", "about", "concerning", "and"}


def simple_sentences(out, toks, en_text):
    """THE PLAIN VERBLESS SENTENCE: marker, predicate phrase, subject.

    `Sa i le amataga, le Lokou` is "In the beginning was the Word". The user's
    grammar for it (2026-09-05): the marker's phrase says its English WITH the
    copula at its end -- "in the beginning was" -- and the subject says its own,
    "the Word"; the marker itself says nothing; `sa i le Atua le Lokou` is
    "and God was" | "the Word" -- Samoan order, no smoothing, the locative `i`
    folded. Shapes:
      A  TAM + phrase + subject            Sa i le amataga, | le Lokou
                                           -> "in the beginning was" | "the Word"
      B  subject + TAM + phrase            O ia lava | sa i le Atua
                                           -> "the same" | "was God"
      C  o + noun [foi] + noun (no TAM)    O le Atua | foi | le Lokou
                                           -> "and God was" | "also" | "the Word"
    The verse's English clauses, in order, give each predicate its copula tense
    and the "and" that opens the clause. Units are walked in order -- the comma
    the 1887 text sets between predicate and subject is not a clause break."""
    if not en_text:
        return out
    n = len(out)
    _trace_on = bool(os.environ.get("SS_TRACE")) and os.environ["SS_TRACE"].lower() in en_text.lower()

    def _stage(label):
        if not _trace_on:
            return
        cur, parts = [], []
        for w in out:
            cur.append(w["sm"])
            if w["en"] and w["en"] != CONT:
                parts.append(" ".join(cur) + " = " + w["en"]); cur = []
        if cur:
            parts.append(" ".join(cur) + " = ∅")
        print(f"  [{label}] " + " | ".join(parts))

    _stage("start")
    # A UNIT NEVER ENDS ON THE ARTICLE (Dunn, unit one: the article opens its
    # noun's phrase). A remembered `sa faapea le` "the" had swallowed the
    # discourse word: the article goes to the noun after it and the word before
    # says its own carried reading -- "after this manner" | "the manner"
    # (1 Nephi 1:15)
    for k in range(1, n - 1):
        if norm(toks[k]) not in ("le", "se") or out[k]["en"] not in ("the", "a", "an") or re.search(r"[,;:.?!][”’\"')]*$", toks[k]):
            continue
        j = k - 1
        while j >= 0 and out[j]["en"] in (CONT, ""):
            j -= 1
        head = [norm(t).strip(",;.") for t in toks[j + 1:k]]
        if not head or all(h in ("sa", "ua", "na", "e", "o", "ma", "ona") for h in head):
            continue
        if norm(toks[k - 1]).strip(",;.") in ("sa", "ua", "na", "e", "te", "lei", "ou", "tou", "matou", "latou", "tatou", "outou", "lua", "ta"):
            continue                        # `e le` is the negator, not an article
        nxt = next((q for q in range(k + 1, n) if out[q]["en"] and out[q]["en"] != CONT), None)
        if nxt is None or re.match(r"^(the|a|an|his|her|their|my|thy|your|our|this|that|these|those)\b", out[nxt]["en"].lower()) or ER.tense_of(out[nxt]["en"]):
            continue
        word = head[-1]
        rd = SG.particle_readings(word)
        if not rd:
            continue
        pick = next((r_ for r_ in rd if re.search(r"\b" + re.escape(r_) + r"\b", (en_text or "").lower())), rd[0])
        out[k - 1]["en"] = pick
        out[k]["en"] = CONT
        out[nxt]["en"] = f"{'the' if norm(toks[k]) == 'le' else 'a'} {out[nxt]['en']}"
    _stage("article never ends a unit")

    # THE PREPOSITIONAL PHRASE IS ONE CONSTITUENT (Dunn, unit one: PREPOSITION +
    # DETERMINER + NOUN). Where the memory held no span for it the segmenter left
    # `i | le | motu` as three one-word units, and none of the phrase rules below
    # (the English's preposition, the object-marking `i`, the article) could see
    # a phrase. Preposition + article + noun, and article + noun, are joined
    # here first; the gloss is composed from the parts and the rules then read it.
    DETS = ("le", "se", "ni", "lo", "la", "lona", "lana", "lou", "lau", "lo’u", "la’u", "loʻu", "laʻu", "ona", "ana", "o’u", "a’u")
    DET_WORDS = ("the", "a", "an", "some", "his", "her", "their", "my", "thy", "your", "our")
    PREP_TOK = ("i", "ia", "iā", "mai", "mo", "ma", "o", "a", "e")
    NOT_NOUN = r"^(the|a|an|his|her|its|their|my|thy|your|our|this|that|these|those|he|she|they|we|i|ye|thou|it|there|and|but|not|is|was|are|were|to|of|in|by|with|for|from|unto|on|upon|who|which|all|every|some|no)\b"

    def looks_verbal(g):
        """A gloss that is a verb -- not a noun that happens to end in -s."""
        t_ = ER.tense_of(g)
        if t_ in ("PAST", "PERFECT", "FUTURE", "PROGRESSIVE"):
            return True
        last = re.sub(r"[^a-z']", "", g.lower().split()[-1]) if g.split() else ""
        if not last:
            return False
        if last.endswith("eth") or last in ER.PAST_TO_BASE:
            return True
        if t_ == "PRESENT" and last.endswith("s") and (last[:-1] in ER.BASE_TO_PAST or last[:-2] in ER.BASE_TO_PAST):
            return True
        return False

    def ends_stop(k):
        return bool(re.search(r"[,;:.?!][”’\"')]*$", toks[k]))

    # (1) article + noun: a one-token determiner unit and the noun unit after it
    k = 0
    while k < n - 1:
        tk = norm(toks[k]).strip(",;.")
        gk = out[k]["en"]
        if not (tk in DETS and gk and gk != CONT and gk.lower().strip(",;.") in DET_WORDS and not ends_stop(k)):
            k += 1
            continue
        b_ = k + 1
        tb = norm(toks[b_]).strip(",;.")
        if tb in SG.CLOSED_CLASS or tb in SG.AMBIGUOUS or out[b_]["en"] in ("", CONT):
            k += 1
            continue
        ng = out[b_]["en"]
        if looks_verbal(ng) or len(ng.split()) > 3 or re.match(NOT_NOUN, ng.lower()) or ng.lower().split()[0].strip(",;.") in PREP_WORDS_ALL:
            k += 1
            continue
        tail = ng[len(ng.rstrip(" ,;.")):]
        out[k]["en"] = CONT
        out[b_]["en"] = f"{gk.strip(',;.')} {ng.rstrip(' ,;.')}{tail}"
        k = b_ + 1
    # (2) preposition + determiner phrase: a one-token preposition unit (or a
    #     blank one) and the unit after it that opens on a determiner
    k = 0
    while k < n - 1:
        tk = norm(toks[k]).strip(",;.")
        gk = out[k]["en"]
        if not (tk in PREP_TOK and (gk == "" or (gk != CONT and len(gk.split()) == 1 and gk.lower().strip(",;.") in PREP_WORDS_ALL)) and not ends_stop(k)):
            k += 1
            continue
        a_ = k + 1
        if norm(toks[a_]).strip(",;.") not in DETS:
            k += 1
            continue
        e_ = a_
        while e_ < n and out[e_]["en"] in ("", CONT) and e_ - a_ < 3:
            e_ += 1
        if e_ >= n or out[e_]["en"] in ("", CONT) or any(ends_stop(x) for x in range(a_, e_)):
            k += 1
            continue
        ng = out[e_]["en"]
        if looks_verbal(ng) or len(ng.split()) > 4 or not re.match(r"^(" + "|".join(DET_WORDS) + r")\b", ng.lower()):
            k += 1
            continue
        prep = gk.strip(",;.") + " " if gk else ""
        for x in range(k, e_):
            out[x]["en"] = CONT
        out[e_]["en"] = f"{prep}{ng}"
        k = e_ + 1
    _stage("phrases joined")
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    en_clauses = [c.strip() for c in re.split(r"[,;:.?!]", en_text) if c.strip()]
    NP_HEADS = ("le", "se", "o", "lo", "la", "ona", "lona", "lana", "ni", "ia", "i", "latou", "laua", "outou", "matou", "tatou")

    def key_of(u):
        return " ".join(norm(t) for t in toks[u[0]:u[1]])

    def gloss_of(u):
        return out[u[1] - 1]["en"]

    def set_gloss(u, g):
        out[u[1] - 1]["en"] = g

    def is_verbal(u):
        g = gloss_of(u)
        return bool(g) and g != CONT and ER.tense_of(g) in ("PAST", "PRESENT", "PERFECT", "FUTURE", "PROGRESSIVE")

    def ends_clause(u):
        return bool(re.search(r"[;:.?!][”’\"')]*$", toks[u[1] - 1]))

    def ec_of(k):
        return en_clauses[k].lower() if k < len(en_clauses) else en_text.lower()

    def clause_english(k):
        ec = ec_of(k)
        cop = None
        for c in ("were", "was", "are", "is"):
            if re.search(r"\b" + c + r"\b", ec):
                cop = c
                break
        w = ec.split()
        conj = w[0] if w and w[0] in ("and", "but", "for", "then", "so", "yet", "nor") else None
        return cop, conj

    def tidy(g):
        g = re.sub(r"\bthe god\b", "God", g, flags=re.I)
        g = re.sub(r"\bgod\b", "God", g)
        return g

    _ewords = set(re.findall(r"[a-z']+", (en_text or "").lower()))

    def nominal(core):
        """A possessed adjective is a NOUN (Dunn, unit seven, verbs and
        adjectives as nouns): `lona tumu` is "his fulness", not "his full" --
        the -ness form when the verse has it."""
        w = core.split()
        if not w:
            return core
        head = re.sub(r"[^a-z']", "", w[-1].lower())
        for cand in (head + "ness", head[:-1] + "ness" if head.endswith("l") else None, head + "th", head[:-1] + "th"):
            if cand and cand != head and cand in _ewords:
                return " ".join(w[:-1] + [cand])
        return core

    PREPS = r"(with|in|at|to|unto|for|by|from|on|upon|among|into|before|after|over|under|of|through|against|toward|towards)"
    PREPS_X = r"(in behalf of|on behalf of|because of|out of|according to|instead of|on account of|for the sake of|" + PREPS[1:]

    def with_prep(g, ec, pos=None, nth=None):
        """The preposition the English gives the phrase: `i le Atua` is "with
        God" in John 1:1 (user: "its intended in the Samoan actually to say
        with because its a simple sentence"), and the memory had only "God".
        Where the phrase recurs, the occurrence nearest the unit's own place in
        the verse decides ("after me" … "before me", John 1:15)."""
        own = re.match(r"^" + PREPS + r"\s+", g.lower().strip(" ,;."))
        rest = g.strip(" ,;.")[own.end():] if own else g.strip(" ,;.")
        core = re.sub(r"^(the|a|an|his|her|its|their|my|thy|your|our|mine|thine)\s+", "", rest.lower())
        if not core:
            return g
        hits = list(re.finditer(r"\b" + PREPS_X + r"\s+(the\s+|a\s+|an\s+|his\s+|her\s+|their\s+|my\s+|thy\s+|your\s+|our\s+|mine\s+|thine\s+)?" + re.escape(core.split()[0]) + r"\b", ec))
        pron_obj = core.split()[0] in ("him", "her", "them", "me", "us", "you", "thee", "it")
        tail = g[len(g.rstrip(" ,;.")):]
        if pron_obj and nth is not None:
            # THE K-TH PRONOUN PHRASE IS THE VERSE'S K-TH "him": "gave unto him a
            # book, and bade him" -- the first `ia te ia` says "unto him", the
            # second "him" (1 Nephi 1:11); position alone could not tell them apart
            occ = list(re.finditer(r"\b" + core.split()[0] + r"\b", ec))
            if nth < len(occ):
                o = occ[nth]
                hit = next((h for h in hits if h.start() <= o.start() < h.end()), None)
                if hit is None:
                    return (rest + tail) if own else g
                art = (hit.group(2) or "").strip()
                if art and not re.match(r"^(the|a|an|his|her|its|their|my|thy|our|your|mine|thine)\b", rest.lower()):
                    rest = f"{art} {rest}"
                return f"{hit.group(1)} {rest}{tail}"
        if not hits:
            # the verse has the pronoun only as a PLAIN object ("did mock him"):
            # `ia te ia` says "him", not "to him" (1 Nephi 1:19)
            if own and pron_obj and re.search(r"\b" + core.split()[0] + r"\b", ec):
                return rest + tail
            return g
        if pos is None:
            m = hits[0]
        else:
            # the occurrence nearest the unit's place -- and when the nearest
            # is a PLAIN object ("commanded them"), the phrase takes no
            # preposition here: `i latou` is the object pronoun, its `i` not "to"
            bare = list(re.finditer(r"\b" + re.escape(core.split()[0]) + r"\b", ec))
            near_bare = min(bare, key=lambda h: abs(h.start() / max(1, len(ec)) - pos)) if bare else None
            m = min(hits, key=lambda h: abs(h.start() / max(1, len(ec)) - pos))
            if near_bare is not None and not any(h.start() <= near_bare.start() < h.end() for h in hits) \
                    and abs(near_bare.start() / max(1, len(ec)) - pos) + 0.05 < abs(m.start() / max(1, len(ec)) - pos):
                # "gave unto him a book, and bade him": the second `ia te ia`
                # is the plain object the verse has nearest (1 Nephi 1:11)
                if own and pron_obj:
                    return rest + tail
                return g
        art = (m.group(2) or "").strip()
        if art and not re.match(r"^(the|a|an|his|her|its|their|my|thy|our|your|mine|thine)\b", rest.lower()):
            rest = f"{art} {rest}"                # "of THE light", the article the memory dropped
        return f"{m.group(1)} {rest}{tail}"      # `to him` under "In him was life" -> "in him"

    def copula_first(core, cop, ec):
        """Where the KJV clause puts the copula relative to the phrase: "In the
        beginning WAS" -> after; "WAS with God" -> before. The clause first;
        when it lacks the phrase, the whole verse ("which is in the bosom")."""
        cw = re.sub(r"^" + PREPS + r"\s+", "", core.lower())
        cw = re.sub(r"^(the|a|an)\s+", "", cw).split()
        if not cw:
            return None
        for text in (ec, (en_text or "").lower()):
            ic = text.find(" " + cop + " ") if (" " + cop + " ") in (" " + text + " ") else -1
            ip = text.find(cw[0])
            if ic >= 0 and ip >= 0:
                return ic < ip
        return None

    def split_tail_particle(u):
        """`o le Atua foi` glossed as one unit: `foi` says "also" on its own."""
        if u[1] - u[0] >= 2 and norm(toks[u[1] - 1]) in ("foi", "fo’i", "foʻi", "lava"):
            g = gloss_of(u)
            word = "also" if norm(toks[u[1] - 1]).startswith("fo") else "indeed"
            g = re.sub(r"\b(also|indeed)\b", "", g).replace("  ", " ").strip(" ,")
            out[u[1] - 2]["en"] = g
            out[u[1] - 1]["en"] = word
            return (u[0], u[1] - 1)
        return u

    # THE PRESENTATIVE SHAPES (user, 2026-09-05, John 1:4): a unit's trailing
    # `foi` says "also" on its own; a clause-opening `o le X` is the noun, not
    # "of X"; `o le X lea` is "which is the X".
    rebuilt = []
    for idx, u in enumerate(units):
        g = gloss_of(u)
        first = norm(toks[u[0]])
        last = norm(toks[u[1] - 1])
        opens_clause = idx == 0 or re.search(r"[,;:.?!][”’\"')]*$", toks[units[idx - 1][1] - 1])
        if u[1] - u[0] >= 2 and last in ("foi", "fo’i", "foʻi") and "also" not in g.lower().split():
            out[u[1] - 2]["en"] = re.sub(r"\s+", " ", g).strip(" ,;.") or out[u[1] - 2]["en"]
            out[u[1] - 1]["en"] = "also"
            u = (u[0], u[1] - 1)
            g = out[u[1] - 1]["en"]
            rebuilt.append(u)
            rebuilt.append((u[1], u[1] + 1))
        else:
            rebuilt.append(u)
        if first == "o" and opens_clause and g and g != CONT and re.match(r"^of\s+", g.lower()):
            g = g[3:]
            if "le" in [norm(t) for t in toks[u[0]:u[1]]] and not re.match(r"^(the|a|an|his|her|their|my|thy|our|your)\b", g.lower()):
                g = "the " + g
            out[u[1] - 1]["en"] = g
        # A POSSESSIVE HEADS ITS NOUN: `lona igoa` is "his name" (user, 2026-09-05),
        # whatever the memory offered for the noun alone
        poss = POSSESSIVE.get(first)
        # `ona` before a marker is "because", `ou` before `te` is "I", `a’u` is
        # "I": the ambiguous forms count only before a noun, and never over a
        # gloss that already reads as a clause
        second = norm(toks[u[0] + 1]).strip(",;.") if u[1] - u[0] > 1 else ""
        if poss and first in ("ona", "ana", "ou", "au", "a’u", "o’u", "aʻu", "oʻu") \
                and (SG.token_class(second) != "OPEN" or ER.tense_of(g or "") or re.match(r"^(i|we|he|she|they|you|ye|thou|because|for|and|but|that|then|so|to|not|no)\b", (g or "").lower())):
            poss = None
        # -- and never on a gloss that already carries its own possessive
        # ("with MINE own hand") or opens on a preposition ("before him"): the
        # curated phrase is whole, and "my with mine own hand" / "his before
        # him" were what prefixing it produced (1 Nephi 1:3, 1:6)
        if poss and g and g != CONT and not re.search(r"\b(his|her|its|their|my|thy|your|our|mine|thine)\b", g.lower()) \
                and not re.match(r"^" + PREPS + r"\b", g.strip(" ,;.").lower()):
            core = re.sub(r"^(be|the|a|an)\s+", "", g.strip(" ,;."))
            if poss == "his" and re.search(r"\bher\b", en_text.lower()) and not re.search(r"\bhis\b", en_text.lower()):
                poss = "her"
            # a possessive before a VERB nominalises it: `lona maliu mai` "his coming"
            head = core.split()[-1] if core else ""
            if (head in ER.BASE_TO_PAST or head in ("come", "go", "believe", "witness", "speak", "hear", "see", "know", "die", "live", "rise", "fall", "return", "sit", "stand", "walk", "eat", "drink", "give", "take", "make")) and head not in _NO_GERUND:
                core = " ".join(core.split()[:-1] + [_gerund(head)])
            core = nominal(core)
            out[u[1] - 1]["en"] = f"{poss} {core}" + g[len(g.rstrip(" ,;.")):]
        # a possessive left blank INSIDE this unit, before its head: `i lona maliu
        # mai` -> "his coming" (the blank did not close a unit, so the possessive
        # sits inside the phrase headed by `i`)
        inner = [q for q in range(u[0], u[1] - 1) if norm(toks[q]) in POSSESSIVE and out[q]["en"] in ("", CONT)
                 and (q == u[0] or norm(toks[q - 1]) in ("i", "ia", "iā", "o", "e", "ma", "mo", "mai"))
                 # `ona ua`, `ou te`, `a’u`: not possessives -- only before a noun
                 and not (norm(toks[q]) in ("ona", "ana", "ou", "au", "a’u", "o’u", "aʻu", "oʻu")
                          and (q + 1 >= u[1] or SG.token_class(norm(toks[q + 1]).strip(",;.")) != "OPEN"))]
        if inner and (ER.tense_of(g or "") or re.match(r"^(i|we|he|she|they|you|ye|thou|because|for|and|but|that|then|so|to|not|no|would|shall|will)\b", (g or "").lower())):
            inner = []
        if inner and g and g != CONT and not re.search(r"\b(his|her|its|their|my|thy|your|our|mine|thine)\b", g.lower()) \
                and not re.match(r"^" + PREPS + r"\b", g.strip(" ,;.").lower()):
            poss = POSSESSIVE[norm(toks[inner[0]])]
            core = re.sub(r"^(to|be|the|a|an)\s+", "", g.strip(" ,;."))
            head = core.split()[-1] if core else ""
            if (head in ER.BASE_TO_PAST or head in ("come", "go", "believe", "witness", "speak", "hear", "see", "know", "die", "live", "rise", "fall", "return", "sit", "stand", "walk", "eat", "drink", "give", "take", "make")) and head not in _NO_GERUND:
                core = " ".join(core.split()[:-1] + [_gerund(head)])
            core = nominal(core)
            out[inner[0]]["en"] = CONT
            out[u[1] - 1]["en"] = f"{poss} {core}" + g[len(g.rstrip(" ,;.")):]
            g = out[u[1] - 1]["en"]
        # the quantifier `uma` says every / all as the English has it: `tagata uma lava` "every man"
        if "uma" in [norm(x).strip(",;.") for x in toks[u[0]:u[1]]] and g and g != CONT \
                and not re.search(r"\b(all|every|whole|each)\b", g.lower()) and not ER.tense_of(g):
            core = re.sub(r"^(the|a|an)\s+", "", g.strip(" ,;.").lower())
            if core and re.search(r"\bevery\s+" + re.escape(core.split()[0]) + r"\b", en_text.lower()):
                out[u[1] - 1]["en"] = "every " + core + g[len(g.rstrip(" ,;.")):]
            elif core and re.search(r"\ball\s+(the\s+)?" + re.escape(core.split()[0]) + r"\b", en_text.lower()):
                out[u[1] - 1]["en"] = "all " + g.strip(" ,;.") + g[len(g.rstrip(" ,;.")):]
        if first == "o" and last == "lea" and u[1] - u[0] >= 3 and g and g != CONT and not ER.tense_of(g) \
                and not re.match(r"^(which|that|who)\b", g.lower()) \
                and " ".join(norm(t) for t in toks[u[0]:u[1]]).strip(",;.") not in SG.DISCOURSE \
                and g.strip(" ,;.").lower() not in ("wherefore", "therefore", "thus", "now", "then", "so", "behold"):
            core = re.sub(r"^(this|that|which|the)\s+", "", g.strip(" ,;."))
            out[u[1] - 1]["en"] = f"which is the {core}" + g[len(g.rstrip(" ,;.")):]
    units = rebuilt

    _stage("presentative shapes")
    # THE SIMPLE SENTENCE AT TOKEN LEVEL. `Sa ia te ia le ola`: the memory left
    # `ia te ia` blank, and a blank does not end a unit, so the unit walk saw one
    # lump. Here: a marker token, the phrase headed by i / ia up to the noun that
    # opens the subject, the subject to the clause end -- whatever the glosses.
    def np_head(k):
        t = norm(toks[k]); prev = norm(toks[k - 1]) if k else ""; prev2 = norm(toks[k - 2]) if k > 1 else ""
        after_prep = prev in ("i", "ia", "iā", "o", "a", "e", "ma", "mo", "mai", "ona") and not (prev == "ia" and prev2 == "te")
        return t in ("le", "se", "lo", "la", "ni", "o") and not after_prep

    t = 0
    k_en = 0
    handled = set()
    while t < n - 2:
        tt = norm(toks[t])
        clause_start = t == 0 or re.search(r"[,;:.?!][”’\"')]*$", toks[t - 1])
        if tt in ("sa", "na", "ua", "e") and norm(toks[t + 1]) in ("i", "ia", "iā") \
                and out[t]["en"] in ("", CONT, "was", "were", "is", "are"):
            # not the ergative agent (`e i tatou` "by us"), and not after a verb
            # in this clause (`ua maua ai e i tatou uma lava`: have received we all)
            agent_key = " ".join(norm(x) for x in toks[t + 1:t + 4]).strip(",;.")
            if tt == "e" and any(agent_key.startswith(k) for k in AGENT_PRONOUNS | set(PRON_PP)):
                t += 1
                continue
            cs = t
            while cs > 0 and not re.search(r"[,;:.?!][”’\"')]*$", toks[cs - 1]):
                cs -= 1
            if any(out[x]["en"] not in ("", CONT) and ER.tense_of(out[x]["en"]) in ("PAST", "PRESENT", "PERFECT") for x in range(cs, t)):
                t += 1
                continue
            # the predicate phrase runs to the noun that opens the subject
            e = t + 2
            while e < n and not np_head(e) and not re.search(r"[,;:.?!][”’\"')]*$", toks[e - 1]):
                e += 1
            if e >= n or not np_head(e):
                t += 1
                continue
            # the subject: to the clause end
            se = e
            while se < n and not re.search(r"[,;:.?!][”’\"')]*$", toks[se]):
                se += 1
            se = min(se + 1, n)
            pred_key = " ".join(norm(x) for x in toks[t + 1:e])
            pg = next((out[x]["en"] for x in range(e - 1, t, -1) if out[x]["en"] not in ("", CONT)), "")
            if not pg:
                pg = PRON_PP.get(pred_key, "")
            if not pg or ER.tense_of(pg):
                t += 1
                continue
            sg = next((out[x]["en"] for x in range(se - 1, e - 1, -1) if out[x]["en"] not in ("", CONT)), "")
            if not sg or ER.tense_of(sg) or any(out[x]["en"] not in ("", CONT) and ER.tense_of(out[x]["en"]) for x in range(t + 1, se)):
                t += 1
                continue
            cop, conj = clause_english(k_en)
            cop = cop or COPULA_TAM[tt]
            pg = with_prep(tidy(pg), ec_of(k_en))
            core, tail = pg.rstrip(" ,;."), pg[len(pg.rstrip(" ,;.")):]
            first = copula_first(core, cop, ec_of(k_en))
            pg = f"{cop} {core}{tail}" if first is True else f"{core} {cop}{tail}"
            if clause_start and conj and not pg.lower().startswith(conj + " "):
                pg = f"{conj} {pg}"
            for x in range(t, e - 1):
                out[x]["en"] = CONT
            out[e - 1]["en"] = pg
            # the subject: nominative pronoun, its own gloss on its last token
            subj_key = " ".join(norm(x) for x in toks[e:se]).strip(",;.")
            w = sg.split()
            if subj_key in SUBJ_PRON:
                sg = SUBJ_PRON[subj_key] + (" " + " ".join(w[1:]) if len(w) > 1 and w[0].lower() in NOMINATIVE else "")
            elif w and w[0].lower() in NOMINATIVE:
                sg = NOMINATIVE[w[0].lower()] + sg[len(w[0]):]
            for x in range(e, se - 1):
                out[x]["en"] = CONT
            out[se - 1]["en"] = sg
            handled.update(range(t, se))
            k_en += 1
            t = se
            continue
        if re.search(r"[,;:.?!][”’\"')]*$", toks[t]) and t + 1 < n:
            pass
        t += 1
    # rebuild the units after the token-level pass
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1

    k = 0            # the English clause the next predicate answers to
    j = 0
    while j < len(units):
        u = units[j]
        key = key_of(u)
        g = gloss_of(u).lower().strip(" ,;.")
        if u[0] in handled:
            j += 1
            continue
        # A / B: a bare marker (copula or silent) before a phrase headed by i / ia
        # -- a PHRASE, not a bare preposition left as its own unit (`o loo | i | le
        # fatafata` printed "in is")
        if key in COPULA_TAM and g in ("", "was", "were", "is", "are") and j + 1 < len(units) \
                and norm(toks[units[j + 1][0]]) in ("i", "ia", "iā") and not is_verbal(units[j + 1]) \
                and units[j + 1][1] - units[j + 1][0] >= 2:
            pred = units[j + 1]
            cop, conj = clause_english(k)
            cop = cop or COPULA_TAM[key]
            pg = with_prep(tidy(gloss_of(pred)), ec_of(k))
            core, tail = pg.rstrip(" ,;."), pg[len(pg.rstrip(" ,;.")):]
            subject_first = j > 0 and not ends_clause(units[j - 1]) and norm(toks[units[j - 1][0]]) in NP_HEADS
            first = copula_first(core, cop, ec_of(k))
            if subject_first or first is True:
                pg = f"{cop} {core}{tail}"                          # B, or the English says "was with God"
            else:
                pg = f"{core} {cop}{tail}"                          # A: "in the beginning was"
            if not subject_first and conj and not pg.lower().startswith(conj + " "):
                pg = f"{conj} {pg}"
            if not subject_first and j + 2 < len(units):
                # the subject pronoun is nominative: `o ia` after the predicate is "he"
                sub = units[j + 2]
                sg = gloss_of(sub)
                w = sg.split()
                if w and w[0].lower() in NOMINATIVE:
                    set_gloss(sub, NOMINATIVE[w[0].lower()] + sg[len(w[0]):])
            set_gloss(u, CONT)
            set_gloss(pred, pg)
            k += 1
            j += 2
            continue
        # C: a presentative noun phrase, then (foi,) then the subject noun phrase
        if norm(toks[u[0]]) == "o" and (j == 0 or ends_clause(units[j - 1]) or toks[units[j - 1][1] - 1].endswith(",")) \
                and gloss_of(u) and gloss_of(u) != CONT and not is_verbal(u):
            m = j + 1
            if m < len(units) and key_of(units[m]) in ("foi", "fo’i", "foʻi", "lava"):
                m += 1
            if m < len(units) and norm(toks[units[m][0]]) in ("le", "se", "lo", "la", "ona", "lona") \
                    and not is_verbal(units[m]) and not any(key_of(x) in COPULA_TAM for x in units[j:m + 1]):
                cop, conj = clause_english(k)
                if cop:
                    # THE EQUATIVE: `O le Atua foi le Lokou` is "God is" | "also" |
                    # "the Word" (user, 2026-09-05) -- the presentative `o` says
                    # "is" after its noun, and the Samoan carries no "and" here
                    u2 = split_tail_particle(u)
                    fg = tidy(gloss_of(u2)).rstrip(" ,;.")
                    tail = gloss_of(u2)[len(gloss_of(u2).rstrip(" ,;.")):]
                    # the predicate says its noun, then the copula: "John is" |
                    # "his name" (John 1:6) -- a remembered "is John" is turned
                    lead = re.match(r"^(is|was|are|were)\s+", fg.lower())
                    if lead:
                        fg = fg[lead.end():]
                    # the marker-less equative is tenseless, and the user reads
                    # it "God is | also | the Word" (GLOSSING_RULES 21)
                    if not any(x in fg.lower().split() for x in ("is", "are", "was", "were")):
                        fg = f"{fg} is"
                    set_gloss(u2, fg + tail)
                    k += 1
                    j = m + 1
                    continue
        # THE PRONOUN EQUATIVE: `O ia lenei` is "This was he" (John 1:15) -- the
        # emphatic pronoun under the presentative, then the demonstrative; the
        # copula is the one the verse sets beside "this / that"
        if key in SUBJ_PRON and (j == 0 or ends_clause(units[j - 1]) or toks[units[j - 1][1] - 1].endswith(",")) \
                and j + 1 < len(units) and key_of(units[j + 1]) in ("lenei", "lea", "lena") \
                and gloss_of(u) and gloss_of(u) != CONT:
            mcop = re.search(r"\b(?:this|that|these|those)\s+(is|was|are|were)\b|\b(is|was|are|were)\s+(?:he|she|it|they|i|we)\b", en_text.lower())
            cop = (mcop.group(1) or mcop.group(2)) if mcop else None
            if cop:
                set_gloss(u, f"{SUBJ_PRON[key]} {cop}")
                k += 1
                j += 2
                continue
        # `O le` + a VERB: the headless relative, "he that cometh" (John 1:15) --
        # the article stands for the one the clause describes (Dunn, unit seven)
        if key in ("o le", "le") and gloss_of(u).strip(" ,;.").lower() in ("the", "of the") and j + 1 < len(units):
            vg = gloss_of(units[j + 1])
            vh = re.sub(r"[^a-z']", "", (vg.split()[-1] if vg and vg != CONT else "").lower())
            # a VERB: a strong verb, a KJV -eth form, or a word the verse
            # conjugates -- never a noun that happens to end in -s ("multitudes")
            if vh and (vh in ER.BASE_TO_PAST or vh in ER.PAST_TO_BASE or vh.endswith("eth") or (vh + "eth") in _ewords) \
                    and vh not in ("light", "name", "word", "work", "witness", "life", "love", "peace", "fire", "cross", "house", "glass", "hold", "lie", "lay", "sin"):
                set_gloss(u, "he that" if re.search(r"\bhe that\b", en_text.lower()) else ("they that" if re.search(r"\bthey that\b", en_text.lower()) else "the one who"))
        if ends_clause(u) and k < len(en_clauses):
            pass
        j += 1
    _stage("token-level A/B + units walk")
    # A POSSESSIVE AND ITS NOUN ARE ONE PHRASE: `O lona | tumu` came out as two
    # units, "his" | "full"; the possessive's unit takes the noun after it and
    # the noun is read as a noun -- "of his fulness" (John 1:16), with the
    # preposition the English gives the phrase
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    en_l = (en_text or "").lower()
    for idx in range(len(units) - 1):
        u, v = units[idx], units[idx + 1]
        if u[0] in handled or v[0] in handled:
            continue
        ukey = key_of(u).split()
        pk = " ".join(ukey[-2:]) if len(ukey) >= 2 else ""
        if not ukey:
            continue
        if pk in PLURAL_POSS:
            # `o lo latou` | `pupula` -> "their brightness" (1 Nephi 1:10)
            if len(ukey) > 3 or (len(ukey) == 3 and ukey[0] not in ("o", "i", "a", "e", "ma", "mo", "mai", "ia")):
                continue
        elif ukey[-1] not in POSSESSIVE or len(ukey) > 2 or (len(ukey) == 2 and ukey[0] not in ("o", "i", "a", "e", "ma", "mo", "mai", "ia")):
            continue
        # -- and read as one: `ona` before a marker is "because", `ou` before
        # `te` is "I", `a’u` is "I"; none of those is a possessive here
        if not re.fullmatch(r"((of|in|to|unto|by|with|for|from|and|but)\s+)?(his|her|its|their|my|thy|your|our)", (gloss_of(u) or "").strip(" ,;.").lower()):
            continue
        vg = gloss_of(v)
        if not vg or vg == CONT or ER.tense_of(vg) or re.match(DET if False else r"^(the|a|an|his|her|its|their|my|thy|your|our|this|that|these|those|he|she|they|we|i|ye|thou|it|there|and|but|not|is|was|are|were|to|of|in|by|with|for)\b", vg.lower()) \
                or v[1] - v[0] > 2 or re.search(r"[,;:.?!][”’\"')]*$", toks[u[1] - 1]):
            continue
        poss = PLURAL_POSS[pk] if pk in PLURAL_POSS else POSSESSIVE[ukey[-1]]
        if poss == "his" and re.search(r"\bher\b", en_l) and not re.search(r"\bhis\b", en_l):
            poss = "her"
        core = nominal(vg.strip(" ,;."))
        head = re.sub(r"[^a-z']", "", core.split()[-1].lower()) if core.split() else ""
        if head in ER.BASE_TO_PAST or head in ("come", "go", "believe", "witness", "speak", "hear", "see", "know", "die", "live", "rise", "fall", "return", "sit", "stand", "walk", "eat", "drink", "give", "take", "make"):
            ger = _gerund(head)
            if ger in _ewords:
                core = " ".join(core.split()[:-1] + [ger])
        tail = vg[len(vg.rstrip(" ,;.")):]
        prep = ""
        if ukey[0] in ("o", "i", "a", "e", "ma", "mo", "mai", "ia") and len(ukey) == (3 if pk in PLURAL_POSS else 2):
            pm = re.search(r"\b" + PREPS + r"\s+" + poss + r"\s+" + re.escape(head) + r"\b", en_l) if head else None
            prep = (pm.group(1) + " ") if pm else ""
        for x in range(u[0], v[1] - 1):
            out[x]["en"] = CONT
        out[v[1] - 1]["en"] = f"{prep}{poss} {core}{tail}"
    _stage("possessive merge")
    # THE COPULA COMES FROM THE ENGLISH (Dunn, units two and seven). Two
    # constructions of the language put no verb where English has "is/was":
    #   the STATIVE predicate   `E poto le tama`      "the boy is smart"
    #                            `Sa lelei le Alii`    "the Lord was good"
    #   DOER OMISSION           `Ua saunia le meaai`  "the food is prepared"
    #                            `Na faia mea uma`     "all things were made"
    # In both the predicate stands first under its marker and English says it
    # with a copula. So a predicate unit under a marker whose gloss the verse
    # sets right after is / are / was / were / be / been takes that copula in
    # front: "is smart", "were made". Nothing is invented -- the copula and the
    # word are both the verse's, adjacent in it.
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    en_l = (en_text or "").lower()
    for idx, u in enumerate(units):
        if u[0] in handled:
            continue
        first = norm(toks[u[0]])
        first2 = " ".join(norm(x) for x in toks[u[0]:u[0] + 2])
        under_marker = first in ("sa", "na", "ua", "e") or first2 in ("o loo", "o lo’o")
        if not under_marker:
            continue
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        core = g.strip(" ,;.")
        tail = g[len(g.rstrip(" ,;.")):]
        cl = core.lower()
        if not cl or re.search(r"\b(is|are|was|were|am|be|been|hath|hast|have|had|shall|will|not|let)\b", cl):
            continue
        if re.match(r"^(the|a|an|his|her|its|their|my|thy|your|our|this|that|these|those|he|she|they|we|i|ye|thou|it|there|and|but|for|of|to|in|by|with|from|unto|on|upon|at|who|which|because|if|when|as|so|then|no|none|by)\b", cl):
            continue
        # the clitic doer between the marker and the verb keeps its active voice:
        # `na ia faia` "he made", never "he were made"
        if any(norm(x) in SG.DESCRIPTIVE_PRONOUNS or norm(x) in SG.PRONOUNS for x in toks[u[0] + 1:u[1] - 1]):
            continue
        hits = list(re.finditer(r"\b(is|are|was|were|am|be|been|hath been|have been|had been|shall be|will be)(\s+not)?(\s+(?:very|exceeding|exceedingly|also|yet|now|then|all|so|there|thus|indeed|truly))?\s+" + re.escape(cl) + r"\b", en_l))
        if not hits:
            continue
        # the occurrence nearest this unit's place in the verse: "were made" for
        # the first `faia` of John 1:3, "was made" for the relative clause
        pos = u[0] / max(1, n)
        m = min(hits, key=lambda h: abs(h.start() / max(1, len(en_l)) - pos))
        cop = m.group(1) + (m.group(2) or "")
        set_gloss(u, f"{cop} {core}{tail}")
    _stage("copula from English")
    # THE FUTURE EXISTENTIAL: `o le a` "shall" + `i ai` "(there) shall be" is one
    # predicate, "there shall be" (Dunn: TAM + the existential `i ai`); the
    # marker is absorbed and the English's own form stands on `i ai`
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    _enl = (en_text or "").lower()
    for idx in range(len(units) - 1):
        u, v = units[idx], units[idx + 1]
        if " ".join(norm(x) for x in toks[u[0]:u[1]]) in ("o le a", "o le ā") and " ".join(norm(x) for x in toks[v[0]:v[1]]).strip(",;.") == "i ai":
            g = gloss_of(u).strip(" ,;.").lower()
            if g in ("shall", "will", "would", "should"):
                m = re.search(r"\b(there (?:shall|will|would|should) (?:be|come))\b", _enl) or re.search(r"\b((?:shall|will|would|should) (?:be|come))\b", _enl)
                last = toks[v[1] - 1]
                set_gloss(u, CONT)
                set_gloss(v, (m.group(1) if m else f"{g} be") + last[len(last.rstrip(",;.")):])
    _stage("future existential")
    # THE OPTATIVE AFTER A VERB OF WISHING (Dunn, unit three): `ou te manao ia
    # outou faalogo mai` is "I would that you hearken" -- `ia` + the clitic
    # pronoun + the verb reads "that PRONOUN VERB" wherever the English has that
    # clause, whatever order a remembered reading kept ("hearken you")
    CLITIC_EN = {"ou": "I", "e": "you", "oe": "you", "ia": "he", "outou": "you", "tatou": "we", "matou": "we", "latou": "they", "lua": "you", "la": "they", "ta": "we", "ma": "we"}
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for u in units:
        ks = [norm(x).strip(",;.") for x in toks[u[0]:u[1]]]
        if len(ks) < 3 or ks[0] != "ia" or ks[1] not in CLITIC_EN:
            continue
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        words = [re.sub(r"[^a-z']", "", w.lower()) for w in g.split()]
        verbs = [w for w in words if w and w not in FUNCTION_ONLY and w not in ("would", "should", "may", "might", "shall", "will", "be", "not")]
        if not verbs:
            continue
        found = None
        for m in re.finditer(r"\bthat (ye|you|we|they|thou|he|she|it|i) ((?:would|should|may|might|shall|will|be|not) )*(\w+)", _enl):
            vb = m.group(3)
            if any(vb == v or vb in _stems(v) or v in _stems(vb) for v in verbs):
                found = (m.group(1), vb)
                break
        if found:
            pen = {"ye": "you", "thou": "you", "i": "I"}.get(found[0], found[0])
            last = toks[u[1] - 1]
            set_gloss(u, f"that {pen} {found[1]}" + last[len(last.rstrip(",;.")):])
    _stage("optative that")
    # AFTER "CANNOT" THE VERB CARRIES NO MODAL OF ITS OWN: `e le mafai ai e se
    # tagata malaga ona toe foi mai ai` is "cannot | any traveler | return" --
    # a remembered "can return" would say the modal twice
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx in range(len(units) - 1):
        u = units[idx]
        if gloss_of(u).strip(" ,;.").lower() not in ("cannot", "could not", "can not", "could never", "can never"):
            continue
        for v in units[idx + 1:idx + 3]:
            g = gloss_of(v)
            m = re.match(r"^(can|could|may|might|shall|will)\s+(?!not\b)(\w.*)$", g.strip(), flags=re.I) if g and g != CONT else None
            if m:
                set_gloss(v, m.group(2))
                break
    _stage("modal after cannot")
    # THE CLITIC AFTER `ona` (or alone) BEFORE ITS VERB IS THE SUBJECT: `ona ou
    # alu ai lea` is "I go" (2 Nephi 1:14) -- an empty pronoun unit before a
    # verb says the pronoun the English has in front of that verb
    CL_EN = {"ou": "I", "e": "you", "ia": "he", "outou": "you", "tatou": "we", "matou": "we", "latou": "they", "lua": "you", "la": "they", "ta": "we", "ma": "we"}
    for k in range(n - 1):
        if out[k]["en"] or norm(toks[k]).strip(",;.") not in CL_EN:
            continue
        if k > 0 and norm(toks[k - 1]).strip(",;.") in ("te", "ia", "o", "e", "mo", "ma", "i", "iā"):
            continue          # a marked pronoun (`ou te`, `ia te`) is another frame
        nxt = next((j for j in range(k + 1, min(n, k + 5)) if out[j]["en"] and out[j]["en"] != CONT), None)
        if nxt is None:
            continue
        vg = out[nxt]["en"].strip(" ,;.").lower()
        if not vg or re.match(r"^(i|you|he|she|it|we|they|there)\b", vg):
            continue
        pr = CL_EN[norm(toks[k]).strip(",;.")]
        if re.search(r"\b" + pr.lower() + r"\s+(?:\w+\s+)?" + re.escape(vg.split()[0]) + r"\b", _enl):
            out[k]["en"] = pr
    _stage("clitic subject")
    # THE NEGATIVE EQUATIVE: `E le o le malamalama ia` is "he was not the light"
    # (user, John 1:8) -- `e le o` + noun phrase + the pronoun subject at the end,
    # read as one unit on the pronoun, copula tense from the English
    t = 0
    while t < n - 3:
        if norm(toks[t]) == "e" and norm(toks[t + 1]) in ("le", "lē", "le’o", "leʻo") and (norm(toks[t + 2]) == "o" or norm(toks[t + 1]) in ("le’o", "leʻo")):
            b0 = t + 3 if norm(toks[t + 2]) == "o" else t + 2
            e = b0
            while e < n and not re.search(r"[,;:.?!][”’\"')]*$", toks[e]):
                e += 1
            e = min(e + 1, n)
            last_key = norm(toks[e - 1]).strip(",;.")
            if last_key in ("ia", "latou", "laua", "matou", "tatou", "outou", "oe", "au", "a’u", "aʻu") and e - b0 >= 2:
                pron = {"ia": "he", "latou": "they", "laua": "they", "matou": "we", "tatou": "we", "outou": "ye", "oe": "thou", "au": "I", "a’u": "I", "aʻu": "I"}[last_key]
                npg = next((out[x]["en"] for x in range(e - 2, b0 - 1, -1) if out[x]["en"] not in ("", CONT)), "")
                if npg and not ER.tense_of(npg):
                    ec = en_text.lower()
                    cop = "was" if re.search(r"\bwas\b", ec) else ("were" if re.search(r"\bwere\b", ec) else "is")
                    if re.search(r"\bhe\b", ec) and re.search(r"\bshe\b", ec) is None:
                        pass
                    core = re.sub(r"^(of|as|for)\s+", "", npg.strip(" ,;."))
                    # the noun phrase keeps its determiner: "that Light" as the
                    # verse has it, else the article `le` says "the"
                    if not re.match(r"^(the|that|this|a|an|his|her|their|my|thy|your|our)\b", core.lower()):
                        head = re.sub(r"[^a-z']", "", core.lower().split()[0]) if core.split() else ""
                        det = re.search(r"\b(the|that|this|a|an)\s+" + re.escape(head) + r"\b", ec) if head else None
                        if det:
                            core = f"{det.group(1)} {core}"
                        elif norm(toks[b0]) == "le":
                            core = f"the {core}"
                        elif norm(toks[b0]) == "se":
                            core = f"a {core}"
                    for x in range(t, e - 1):
                        out[x]["en"] = CONT
                    out[e - 1]["en"] = f"{pron} {cop} not {core}" + toks[e - 1][len(toks[e - 1].rstrip(',;.')):] * 0 + npg[len(npg.rstrip(' ,;.')):]
                    t = e
                    continue
        t += 1
    _stage("negative equative")
    # THE DEMONSTRATIVE PHRASE: `i lea lava malamalama` is "of that light" -- the
    # preposition from the English, `lea (lava)` "that", the noun its own word
    t = 0
    while t < n - 2:
        if norm(toks[t]) in ("i", "o", "ia") and norm(toks[t + 1]) == "lea":
            m = t + 2
            if m < n and norm(toks[m]) == "lava":
                m += 1
            # a NOUN follows (`i lea lava malamalama`); before a marker, a
            # pronoun or a subordinator `o lea` is the discourse "therefore"
            if m < n and out[m]["en"] not in ("", CONT) and not ER.tense_of(out[m]["en"]) \
                    and SG.token_class(norm(toks[m]).strip(",;.")) == "OPEN" \
                    and out[m]["en"].strip(" ,;.").lower() not in ("wherefore", "therefore", "thus", "now", "then", "so", "if", "behold"):
                noun = re.sub(r"^(the|that|this|a|an)\s+", "", out[m]["en"].strip(" ,;."))
                tail = out[m]["en"][len(out[m]["en"].rstrip(" ,;.")):]
                prep = None
                mm = re.search(r"\b(of|in|to|unto|with|by|for|from|at|on|upon)\s+(that|this|the)?\s*" + re.escape(noun.split()[0].lower()) + r"\b", en_text.lower()) if noun else None
                if mm:
                    prep = mm.group(1)
                elif norm(toks[t]) == "o":
                    prep = "of"
                # a gloss parked on these particles by a unit that began BEFORE
                # the phrase (`molimau i lea lava` = "witness", on `lava`) goes
                # back to that unit's last own token; it is not this phrase's
                for x in range(t, m):
                    if out[x]["en"] and out[x]["en"] != CONT:
                        s = x
                        while s > 0 and out[s - 1]["en"] == CONT:
                            s -= 1
                        if s < t:
                            out[t - 1]["en"] = out[x]["en"]
                for x in range(t, m):
                    out[x]["en"] = CONT
                out[m]["en"] = (f"{prep} that {noun}" if prep else f"that {noun}") + tail
                t = m + 1
                continue
        t += 1
    _stage("demonstrative")
    # a lone `o` that repeats the verb before a noun phrase (`sau | o=came | le molimau`)
    # -- a one-token unit only: the `o` closing `e le o` carries that frame's gloss
    for k in range(1, n - 1):
        if norm(toks[k]) == "o" and out[k]["en"] not in ("", CONT) and norm(toks[k + 1]) in ("le", "se") \
                and out[k - 1]["en"] != CONT \
                and ER.tense_of(out[k]["en"]) in ("PAST", "PRESENT", "PERFECT"):
            out[k]["en"] = CONT
    # VERB + SUBJECT PRONOUN: `Na sau o ia` is "he came" -- the pronoun unit takes
    # the verb, nominative first, and the verb token goes silent (user, John 1:7)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    def agent_follows(idx):
        """An ergative `e` + pronoun / name later in this clause: then the `o ia`
        after the verb is its OBJECT (`e lei talia o ia e ona lava tagata`:
        received him not, by his own people)."""
        for w in units[idx + 2:]:
            if re.search(r"[,;:.?!][”’\"')]*$", toks[w[0] - 1]) if w[0] else False:
                break
            if norm(toks[w[0]]) == "e" and w[1] - w[0] >= 2 and (norm(toks[w[0] + 1]) in AGENT_PRONOUNS | {"ona", "lona", "lana", "ana", "le", "se"} or toks[w[0] + 1][:1].isupper()):
                return True
        return False

    for idx in range(len(units) - 1):
        u, v = units[idx], units[idx + 1]
        vkey = " ".join(norm(x) for x in toks[v[0]:v[1]]).strip(",;.")
        g = gloss_of(u)
        verb_head = re.sub(r"[^a-z]", "", (g.split()[-1] if g else "").lower())
        if vkey in SUBJ_PRON and g and g != CONT and ER.tense_of(g) in ("PAST", "PRESENT", "PERFECT") and not agent_follows(idx) \
                and verb_head in INTRANSITIVE \
                and not re.match(r"^(he|she|they|we|i|you|ye|thou)\b", g.lower()) \
                and not re.search(r"\b(was|were|is|are|am|be)\b", g.lower()):   # a copular predicate keeps its subject apart: "was in the world" | "he"
            verb = re.sub(r"^(who|which|that|and)\s+", "", g.strip(" ,;."))
            set_gloss(u, CONT)
            set_gloss(v, f"{SUBJ_PRON[vkey]} {verb}" + gloss_of(v)[len(gloss_of(v).rstrip(' ,;.')):])
    _stage("verb+subject inversion")
    # PURPOSIVE `ina ia VERB`: "to VERB" -- the particles fold into the verb
    for k in range(n - 2):
        if norm(toks[k]) == "ina" and norm(toks[k + 1]) == "ia":
            m = k + 2
            if m < n and out[m]["en"] in ("", CONT) and m + 1 < n and norm(toks[m]) not in SG.CLOSED_CLASS:
                # the verb token came back blank: its dictionary sense, base form
                senses = SG.dictionary(norm(toks[m]))
                first = re.split(r"[,;]", senses[0])[0].strip() if senses else ""
                first = re.sub(r"^\s*(to|a|an|the)\s+", "", first)   # the verb, bare: "witness", not "a witness"
                if first and len(first.split()) <= 2:
                    out[m]["en"] = first
            if m < n and out[m]["en"] not in ("", CONT) and not re.match(r"^(to|that|in order)\b", out[m]["en"].lower()):
                out[k]["en"] = CONT
                out[k + 1]["en"] = CONT
                out[m]["en"] = "to " + re.sub(r"^(may|might|should|shall|will)\s+", "", out[m]["en"])
                # `ina ia talitonu i ai` is ONE unit (user): the anaphoric `i ai`
                # folds into the verb; the explicit phrase later says "in him"
                if m + 2 < n and norm(toks[m + 1]) == "i" and norm(toks[m + 2]).strip(",;.") == "ai":
                    g = out[m]["en"]
                    out[m]["en"] = CONT
                    out[m + 1]["en"] = CONT
                    out[m + 2]["en"] = g + toks[m + 2][len(toks[m + 2].rstrip(",;.")):] * 0
    _stage("purposive")
    # `o le NOUN` right after a verb clause takes the English's own preposition:
    # "came FOR a witness" (the user reads "as a witness"; the KJV says for)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx in range(1, len(units)):
        u, prev = units[idx], units[idx - 1]
        if norm(toks[u[0]]) == "o" and u[1] - u[0] >= 2 and norm(toks[u[0] + 1]) in ("le", "se") \
                and gloss_of(prev) not in ("", CONT) and ER.tense_of(gloss_of(prev)) in ("PAST", "PRESENT", "PERFECT"):
            g = gloss_of(u)
            if g and g != CONT and not re.match(r"^(for|as|to|unto|with|by|of|in)\b", g.lower()):
                core = re.sub(r"^(the|a|an)\s+", "", g.lower().strip(" ,;."))
                m = re.search(r"\b(for|as|unto|to|with|by)\s+(a|an|the)?\s*" + re.escape(core.split()[0]) + r"\b", en_text.lower()) if core else None
                if m:
                    art = f" {m.group(2)}" if m.group(2) else ""
                    set_gloss(u, f"{m.group(1)}{art} {core}" + g[len(g.rstrip(' ,;.')):])
    _stage("o le NOUN prep")
    # THE ERGATIVE AGENT: `e ia` after a verb is "by him" (user, John 1:3), `e ona
    # lava tagata` "by his own people" -- the `e` says "by" when the memory dropped it
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    OBJ = {"he": "him", "she": "her", "they": "them", "we": "us", "i": "me", "thou": "thee", "ye": "you"}
    for idx in range(1, len(units)):
        u = units[idx]
        ukey = " ".join(norm(x) for x in toks[u[0]:u[1]])
        if norm(toks[u[0]]) == "e" and u[1] - u[0] >= 2 and ukey not in NEG_UNITS and ukey not in ("e le", "e lē") \
                and not (norm(toks[u[0] + 1]) in ("le", "lē") and (u[1] - u[0] == 2 or norm(toks[u[0] + 2]) in ("o", "lei", "mafai", "toe"))) \
                and not re.search(r"\b(not|no|never|neither|nor)\b", gloss_of(u).lower()) \
                and not (norm(toks[u[0] + 1]) in ("le", "lē") and SG.contextual_reading("le", "e", norm(toks[u[0] + 2]) if u[1] - u[0] > 2 else "", False) == "not") \
                and (norm(toks[u[0] + 1]) in AGENT_PRONOUNS | {"ona", "lona", "lana", "ana", "le", "se"} or toks[u[0] + 1][:1].isupper()):
            g = gloss_of(u)
            # the English says "by" only in the passive; where it makes the agent
            # its subject ("after I, Nephi, had made an end") the agent keeps the
            # English's own form -- `e a'u` "I", never "by I"
            if g and g != CONT and re.search(r"\bby\b", (en_text or "").lower()) \
                    and not re.match(r"^(by|of|to|for|with|from|in|unto)\b", g.lower()) \
                    and not re.match(r"^(he|she|they|we|i|you|ye|thou)\s+\w+ed\b", g.lower()):
                w = g.split()
                head = w[0].lower().strip(",;.") if w else ""
                if head in OBJ:
                    w[0] = OBJ[head] + w[0][len(head):]
                set_gloss(u, "by " + " ".join(w))
    _stage("ergative agent")
    # THE NEGATIVE FOLDS INTO ITS VERB: `e lei faia` is "not made" (user, John 1:3)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx in range(len(units) - 1):
        u, v = units[idx], units[idx + 1]
        ukey_ = " ".join(norm(x) for x in toks[u[0]:u[1]])
        # the GENERAL negative `le` folds into its verb the same way, without a
        # tense of its own: `te le oti` "not die" (Dunn: `e le` present, `e
        # lei` past)
        if ukey_ in ("le", "lē", "e le", "e lē") and gloss_of(u).strip(" ,;.").lower() == "not":
            vg = gloss_of(v)
            if not vg or vg == CONT or norm(toks[v[0]]) in SG.CLOSED_CLASS or re.search(r"[,;:.?!][”’\"')]*$", toks[u[1] - 1]):
                continue
            if re.search(r"\b\w+less\b|\b(not|no|never|without)\b|\bun\w{3,}", vg.lower()):
                # the negation is INSIDE the English word: `lē pōnā` "blameless",
                # `lē mafai` "unable" -- the particle says nothing more
                set_gloss(u, CONT)
                continue
            if not re.match(r"^(the|a|an)\b", vg.lower()):
                set_gloss(u, CONT)
                set_gloss(v, f"not {vg}")
            continue
        if ukey_ in NEG_PAST_UNITS and gloss_of(u).strip(" ,;.").lower() in ("not", "not yet"):
            vg = gloss_of(v)
            if vg and vg != CONT and not re.match(r"^(not|never)\b", vg.lower()) and norm(toks[v[0]]) not in SG.CLOSED_CLASS:
                # after `e lei` the word IS a verb, and the negative is past: a
                # bare form takes the past even where the KJV chose another word
                # (`e lei talia` "not received" beside "comprehended it not")
                if ER.tense_of(vg) is None and len(vg.split()) <= 2:
                    head = vg.split()[-1].lower()
                    # a strong verb takes its table past; a participle ("seen")
                    # is already past and stands; a regular verb only where the
                    # verse shows it conjugated -- never "seened"
                    ewords_ = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                    if head in ER.PARTICIPLES or head in ER.PAST_TO_BASE:
                        past = None
                    elif head in ER.BASE_TO_PAST:
                        past = ER.BASE_TO_PAST[head][0]
                    elif head.isalpha():
                        # the user's rule (21b): after `e lei` the word IS a
                        # verb and takes the past whatever word the KJV chose --
                        # `a e lei talia` "but not received" beside "comprehended"
                        past = ER._past_forms(head)[0]
                    else:
                        past = None
                    if past:
                        vg = " ".join(vg.split()[:-1] + [past])
                if ER.tense_of(vg) in ("PAST", "PRESENT", "PERFECT"):
                    neg = gloss_of(u).strip(" ,;.")
                    set_gloss(u, CONT)
                    set_gloss(v, f"{neg} {vg}")
    _stage("negative fold")
    # every phrase headed by i / ia says the preposition the English gives it
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    en_l = (en_text or "").lower()
    PREP_WORDS = set(PREPS.strip("()").split("|")) | {"about", "concerning", "like"}

    def verb_before(u):
        """The nearest open-class word before this unit in its clause -- the
        verb the phrase belongs to -- or ''."""
        k = u[0] - 1
        while k >= 0:
            if re.search(r"[,;:.?!][”’\"')]*$", toks[k]):
                return ""
            t_ = norm(toks[k]).strip(",;.")
            if t_ and t_ not in SG.CLOSED_CLASS and t_ not in SG.AMBIGUOUS and t_ not in SG.PRONOUNS and t_ not in SG.DESCRIPTIVE_PRONOUNS:
                return t_
            k -= 1
        return ""

    def as_object(g):
        """`alofa i le lalolagi` is "loved the world": after a verb whose
        object takes `i` (Dunn: alofa i, vaai i, manao i, talitonu i …) the
        phrase drops its preposition when the English has the noun as a plain
        object, and keeps it when the English has one ("believe ON his name")."""
        m = re.match(r"^" + PREPS + r"\s+", g.lower().strip(" ,;."))
        if not m:
            return g
        rest = g.strip(" ,;.")[m.end():]
        tail = g[len(g.rstrip(" ,;.")):]
        core = re.sub(r"^(the|a|an|his|her|their|my|thy|your|our|this|that|these|those|all|every)\s+", "", rest.lower()).split()
        if not core:
            return g
        word = re.sub(r"[^a-z']", "", core[0])
        if not word:
            return g
        plain = with_p = 0
        for mm in re.finditer(r"\b" + re.escape(word) + r"\b", en_l):
            before = en_l[:mm.start()].split()
            prev = before[-1] if before else ""
            if prev in ("the", "a", "an", "his", "her", "their", "my", "thy", "your", "our", "this", "that", "these", "those", "all", "every", "own", "same"):
                prev = before[-2] if len(before) > 1 else ""
            if prev in PREP_WORDS:
                with_p += 1
            else:
                plain += 1
        # "I say unto you … ye" keeps its "unto": only a verse that never gives
        # the word a preposition has it as a plain object
        if plain and not with_p:
            return rest + tail
        return g

    SUBJ = {"latou": "they", "matou": "we", "tatou": "we", "laua": "they", "maua": "we", "taua": "we", "outou": "ye", "oulua": "ye"}
    OBJ_OF = {"they": "them", "we": "us", "ye": "you"}
    for idx_, u in enumerate(units):
        head_ok = norm(toks[u[0]]) in ("i", "ia", "iā", "mo") and u[1] - u[0] >= 2
        if not head_ok and u[1] - u[0] >= 3:
            # the phrase closes a unit whose verb the memory left blank: `fetalai
            # mai ia te ia` "to him" -- the pronoun phrase still reads the verse
            gp_ = (gloss_of(u) or "").strip(" ,;.").lower()
            if re.fullmatch(r"(?:(?:to|unto|of|in|by|with|for|from|at|on|upon)\s+)?(him|her|them|me|us|you|thee|it)", gp_) \
                    and any(norm(toks[q]) in ("i", "ia", "iā") for q in range(u[0] + 1, u[1] - 1)):
                head_ok = True
        if head_ok:
            g = gloss_of(u)
            if g and g != CONT and not ER.tense_of(g) and not re.search(r"\b(was|were|is|are)\b", g.lower()):
                # THE SUBJECT AFTER THE VERB (Dunn, unit four): `i latou` straight
                # after a verb -- its directional or its `ai` -- with no case marker
                # between is the subject, "they", not "to them" (`sa le
                # tofatumoanaina ai i latou` "they were not swallowed up"); after
                # an agent (`e ia i latou`) or a preposition it is the object
                pron = norm(toks[u[0] + 1]).strip(",;.")
                before_ = norm(toks[u[0] - 1]).strip(",;.") if u[0] > 0 else ""
                if u[1] - u[0] == 2 and norm(toks[u[0]]) == "i" and pron in SUBJ and before_ \
                        and (before_ in SG.DIRECTIONALS or before_ == "ai" or before_ == verb_before(u)) \
                        and not re.search(r"[,;:.?!][”’\"')]*$", toks[u[0] - 1]):
                    nom, obj = SUBJ[pron], OBJ_OF[SUBJ[pron]]
                    form = nom if re.search(r"\b" + nom + r"\b", en_l) or not re.search(r"\b" + obj + r"\b", en_l) else obj
                    # before the relative `o e` it is the antecedent: `i latou o e
                    # ua o mai` "those who come" (1 Nephi 1:14)
                    if u[1] + 1 < n and norm(toks[u[1]]) == "o" and norm(toks[u[1] + 1]).strip(",;.") == "e" and re.search(r"\bthose\b", en_l):
                        form = "those"
                    last = toks[u[1] - 1]
                    set_gloss(u, form + last[len(last.rstrip(",;.")):])
                    continue
                pr_ = re.sub(r"^" + PREPS + r"\s+", "", g.strip(" ,;.").lower()).split()
                nth_ = None
                if pr_ and pr_[0] in ("him", "her", "them", "me", "us", "you", "thee", "it"):
                    nth_ = sum(len(re.findall(r"\b" + pr_[0] + r"\b", w["en"].lower())) for w in out[:u[0]] if w["en"] and w["en"] != CONT)
                g2 = with_prep(g, en_l, pos=u[0] / max(1, n), nth=nth_)
                # no preposition anywhere: `i` before a possessive phrase reads "in" (`i lona maliu mai` "in his coming")
                if g2 == g and not re.match(r"^" + PREPS + r"\b", g.lower()) and norm(toks[u[0] + 1]) in POSSESSIVE:
                    g2 = "in " + g
                # the unit before already ends on the phrase's preposition:
                # `e uiga` "concerning" | `i le faaumatiaga` "the destruction"
                # -- the `i` is that frame's, and says nothing more (1 Nephi 1:18)
                if idx_ > 0:
                    pg_ = gloss_of(units[idx_ - 1])
                    pw_ = re.findall(r"[a-z']+", (pg_ or "").lower()) if pg_ and pg_ != CONT else []
                    if pw_ and pw_[-1] in PREP_WORDS_ALL | {"concerning", "about", "unto", "than"} and pw_[-1] != "and":
                        mp_ = re.match(r"^" + PREPS + r"\s+", g2.lower())
                        if mp_:
                            g2 = g2[mp_.end():]
                # THE OBJECT-MARKING `i` (Dunn): after alofa / vaai / manao /
                # talitonu … the `i` phrase is the object, and says no preposition
                if verb_before(u) in SG.OBJECT_I_VERBS:
                    g2 = as_object(g2)
                set_gloss(u, g2)
    _stage("i-phrase preposition")
    # THE PRONOUN AFTER THE VERB IS ITS SUBJECT (Dunn, unit four: the doer
    # follows the verb). `o ia` straight after the verb, its directional, `ai`
    # or a degree word is "he" -- `a'o tatalo atu o ia` "as he prayed",
    # `gatete tele ai o ia` "he did tremble" -- and the agent `e ia` after a
    # verb is "he" wherever the English makes him the subject ("he saw and
    # heard much", 1 Nephi 1:6). Only a "by him" in the verse keeps the agent
    # form; only "VERB him" right after this verb's own word keeps the object.
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    PRON3 = {"ia": ("he", "him"), "i latou": ("they", "them"), "i laua": ("they", "them"), "i matou": ("we", "us"),
             "i tatou": ("we", "us"), "i maua": ("we", "us"), "i taua": ("we", "us"), "outou": ("ye", "you"),
             "oulua": ("ye", "you"), "oe": ("thou", "thee"), "a’u": ("I", "me"), "aʻu": ("I", "me"), "au": ("I", "me")}
    for idx in range(1, len(units)):
        u, prev = units[idx], units[idx - 1]
        key = key_of(u).strip(",;.")
        mp = re.match(r"^(o|e)\s+(.+)$", key)
        if not mp or mp.group(2) not in PRON3:
            continue
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        nom, obj = PRON3[mp.group(2)]
        gl = g.strip(" ,;.").lower()
        if gl not in (obj, "to " + obj, "unto " + obj, "by " + obj, nom.lower()):
            continue
        before_ = norm(toks[u[0] - 1]).strip(",;.")
        if not before_ or re.search(r"[,;:.?!][”’\"')]*$", toks[u[0] - 1]):
            continue
        if not (before_ in SG.DIRECTIONALS or before_ in ("ai", "lava", "tele", "foi", "uma") or before_ == verb_before(u)):
            continue
        pg = gloss_of(prev)
        pw = re.findall(r"[a-z']+", (pg or "").lower()) if pg and pg != CONT else []
        vlast = pw[-1] if pw else ""
        last = toks[u[1] - 1]
        tail = last[len(last.rstrip(",;.")):]
        if mp.group(1) == "e" and re.search(r"\bby " + obj + r"\b", en_l):
            set_gloss(u, "by " + obj + tail)
        elif vlast and re.search(r"\b" + re.escape(vlast) + r"\s+" + obj + r"\b", en_l):
            set_gloss(u, obj + tail)
        elif re.search(r"\b" + nom.lower() + r"\b", en_l):
            set_gloss(u, nom + tail)
    _stage("pronoun after the verb")
    # THE GENITIVE `o` / `a` SAYS "of" WHERE THE VERSE DOES (Dunn, unit one: the
    # possessive particles). `i luga o se papa` is "upon a rock", `i luma o
    # lo'u tama` "before my father", `o lo latou pupula` "their brightness" --
    # the English of each has no "of", and the memory's "of" was the particle
    # read out of context. And the other way: `se tala atoa o mea` "a full
    # account OF the things" -- the noun before it and the verse's own "of
    # the things" put it back (1 Nephi 1:6, 1:10, 1:11, 1:16, 1:17)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    GEN_DET = r"(?:(?:the|a|an|his|her|their|my|our|your|thy|mine|thine|this|that|these|those|all|some|own|same|many)\s+)*"
    for idx, u in enumerate(units):
        key = key_of(u).split()
        if len(key) < 2 or key[0] not in ("o", "a") or " ".join(key[:3]) in ("o le a", "o le ā") or key[1] in ("loo", "lo’o", "loʻo"):
            continue
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        core = g.rstrip(" ,;.")
        tail = g[len(core):]
        mo = re.match(r"^of\s+" + GEN_DET + r"([a-z']+)", core.lower())
        if mo:
            head = mo.group(1)
            if re.search(r"\b" + re.escape(head) + r"\b", en_l) and not re.search(r"\bof\s+" + GEN_DET + re.escape(head) + r"\b", en_l):
                # "in the firmament": the verse's own preposition, if no other
                # unit carries it; else the bare phrase ("upon" | "a rock")
                gc0 = Counter(x for w in out if w["en"] and w["en"] != CONT for x in re.findall(r"[a-z']+", w["en"].lower()))
                mp2 = re.search(r"\b" + PREPS + r"\s+" + GEN_DET + re.escape(head) + r"\b", en_l)
                if mp2 and len(re.findall(r"\b" + mp2.group(1) + r"\b", en_l)) > gc0.get(mp2.group(1), 0):
                    set_gloss(u, mp2.group(1) + " " + core[3:] + tail)
                else:
                    set_gloss(u, core[3:] + tail)
            continue
        if idx == 0 or re.match(r"^" + PREPS + r"\b", core.lower()) or ER.tense_of(core) or re.match(NOT_NOUN, core.lower()) and not re.match(r"^(the|a|an|his|her|their|my|thy|your|our|this|that|these|those|all|some)\b", core.lower()):
            continue
        pg = gloss_of(units[idx - 1])
        pw = re.findall(r"[a-z']+", (pg or "").lower()) if pg and pg != CONT else []
        if not pw or ER.tense_of(pg) or pw[-1] in FUNCTION_ONLY or re.search(r"[,;:.?!][”’\"')]*$", toks[units[idx - 1][1] - 1]):
            continue
        mh = re.match(r"^" + GEN_DET + r"([a-z']+)", core.lower())
        if mh and re.search(r"\b" + re.escape(pw[-1]) + r"\s+of\s+" + GEN_DET + re.escape(mh.group(1)) + r"\b", en_l):
            set_gloss(u, "of " + g)
    _stage("genitive of")
    # `o le` BEFORE A STOP IS THE ARTICLE OF AN ELIDED NOUN: `e pei o le:` is
    # "such as:" -- the phrase says nothing (1 Nephi 1:14)
    for idx, u in enumerate(units):
        if key_of(u).strip(",;:.") in ("o le", "le") and re.search(r"[,;:.][”’\"')]*$", toks[u[1] - 1]) \
                and gloss_of(u).strip(" ,;:.").lower() in ("of the", "the", "of"):
            set_gloss(u, CONT)
    # THE RELATIVE `o e` (Dunn: the emphatic antecedent, "those who / whom"):
    # before a marker or a clitic doer the two particles are one relative, never
    # "of" + nothing (`i latou uma o e ua ia filifilia` "all those whom he hath
    # chosen", 1 Nephi 1:20)
    for k in range(n - 2):
        if norm(toks[k]) != "o" or norm(toks[k + 1]).strip(",;.") != "e" or re.search(r"[,;:.?!][”’\"')]*$", toks[k + 1]):
            continue
        if (out[k]["en"] or "").strip(" ,;.").lower() not in ("of", "", CONT) or out[k + 1]["en"] not in ("", CONT):
            continue
        nxt = norm(toks[k + 2]).strip(",;.")
        if nxt not in ("ua", "na", "sa", "e", "o", "te") and nxt not in SG.DESCRIPTIVE_PRONOUNS:
            continue
        said = " ".join(w["en"] for w in out if w["en"] and w["en"] != CONT).lower()
        nxt_g = next((out[j]["en"] for j in range(k + 2, n) if out[j]["en"] and out[j]["en"] != CONT), "")
        out[k]["en"] = CONT
        if re.match(r"^(who|whom|which|that|those who)\b", nxt_g.lower()):
            out[k + 1]["en"] = CONT               # "whom they had cast out" already says it
            continue
        rel = "whom" if re.search(r"\bwhom\b", en_l) and not re.search(r"\bwhom\b", said) else \
              "those who" if re.search(r"\bthose who\b", en_l) and not re.search(r"\bthose\b", said) else "who"
        out[k + 1]["en"] = rel
    _stage("o e relative")
    # THE COMPLETIVE `(ina) ua uma ona VERB` (Dunn: `uma` "finished" + the
    # nominalised verb) is the English pluperfect: `ina ua uma ona faitau ma
    # vaai e lo'u tama` "when my father had read and seen" -- the frame says
    # the verse's temporal ("when", "after"), the verb its verse form, and the
    # scaffolding pass then sets "had" before it (1 Nephi 1:14, 1:18)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx in range(len(units) - 1):
        u, v = units[idx], units[idx + 1]
        ku = key_of(u).strip(",;.")
        if not re.search(r"(^|\s)(ua|a|ina ua) uma ona$", ku):
            continue
        vg = gloss_of(v)
        if not vg or vg == CONT:
            continue
        mt_ = re.search(r"\b(when|after|as soon as)\b", en_l)
        set_gloss(u, (mt_.group(1) if mt_ else CONT))
        set_gloss(v, re.sub(r"^(of\s+|the\s+(?=[a-z']+ing\b))", "", vg, count=1, flags=re.I))
    _stage("completive ua uma ona")
    # `i ai` AFTER A VERB IS A PRO-PHRASE (Dunn, unit seven): it stands for a
    # phrase of direction already named -- "to it / to him / about it". Where the
    # KJV has a compound (thereto, therein, whereby) it says that; where the KJV
    # names the object as a pronoun after the verb it says that; otherwise the
    # English carries it inside the verb and the particle folds into the verb's
    # unit, as `ina ia talitonu i ai` already does.
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx in range(1, len(units)):
        u, prev = units[idx], units[idx - 1]
        if " ".join(norm(x) for x in toks[u[0]:u[1]]).strip(",;.") != "i ai":
            continue
        pg = gloss_of(prev)
        vb = verb_before(u)
        if not pg or pg == CONT or not vb or re.match(r"^(the|a|an|his|her|their|my|thy|your|our|this|that|these|those)\b", pg.lower()):
            continue
        g = gloss_of(u)
        said = " ".join(w["en"] for w in out if w["en"] and w["en"] != CONT and w is not out[u[1] - 1]).lower()
        comp = [c for c in re.findall(r"\b(there(?:to|in|by|of|on|with|from)|where(?:in|by|with|of|on|to))\b", en_l) if not re.search(r"\b" + c + r"\b", said)]
        if comp:
            set_gloss(u, comp[0])
            continue
        if g and g != CONT and re.match(r"^((to|unto|in|on|of|by|at|with|about)\s+)?(him|it|them|her|thee|me|us|you)\b", g.lower()):
            continue
        # the KJV names the object right after the verb: `papai atu i ai` "touch it"
        vlast = re.sub(r"[^a-z']", "", pg.lower().split()[-1]) if pg.split() else ""
        mo = re.search(r"\b" + re.escape(vlast) + r"\s+((?:un)?to\s+|in\s+|on\s+|of\s+)?(him|it|them|her|thee|me|us|you)\b", en_l) if vlast else None
        if mo:
            set_gloss(u, (mo.group(1) or "") + mo.group(2))
            continue
        # fold: the verb's English moves onto the particle, the verb carries the dot
        for x in range(prev[0], u[1] - 1):
            if out[x]["en"] and out[x]["en"] != CONT:
                out[x]["en"] = CONT
        out[u[1] - 1]["en"] = pg
    # -- and the bare anaphoric `ai` (Dunn, unit seven) says a pronoun only
    # where the verse has one no other unit carries: `ia faitau ai` after
    # "bade him" says nothing (1 Nephi 1:11)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for u in units:
        ku_ = key_of(u).strip(",;.")
        if ku_ not in ("ai", "i ai"):
            continue
        g = gloss_of(u)
        mp_ = re.match(r"^(?:(?:to|unto|of|in|by|with|for|from)\s+)?(him|it|them|her|me|us|you|thee)$", (g or "").strip(" ,;.").lower())
        if not mp_:
            continue
        pr = mp_.group(1)
        have = len(re.findall(r"\b" + pr + r"\b", en_l))
        used = sum(len(re.findall(r"\b" + pr + r"\b", w["en"].lower())) for j, w in enumerate(out) if w["en"] and w["en"] != CONT and j != u[1] - 1)
        if used >= have:
            # `i ai` is the pro-phrase for the THING already named (Dunn, unit
            # seven): `ia faitau i ai` after "bade him" is "read it" -- the
            # book, never the man again (user, 1 Nephi 1:11). The bare `ai`
            # has no such object and says nothing.
            last_ = toks[u[1] - 1]
            set_gloss(u, ("it" + last_[len(last_.rstrip(",;.")):]) if ku_ == "i ai" else CONT)
    _stage("i ai pro-phrase")
    # A DIRECTIONAL NEVER BORROWS A WORD THE VERSE HAS ALREADY SPENT: `atu` after
    # `faamanatu` "rehearsed" took "out" while "out of the land" stood on `mai le
    # laueleele`. Its reading must be an English word no other unit carries;
    # otherwise the directional is absorbed into its verb (Dunn: deixis, not lexis)
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx, u in enumerate(units):
        if u[1] - u[0] != 1 or norm(toks[u[0]]).strip(",;.") not in SG.DIRECTIONALS:
            continue
        g = gloss_of(u)
        if not g or g == CONT or not g.split():
            continue
        word = re.sub(r"[^a-z']", "", g.lower().split()[0])
        if not word:
            continue
        have = len(re.findall(r"\b" + re.escape(word) + r"\b", en_l))
        spent = sum(len(re.findall(r"\b" + re.escape(word) + r"\b", w["en"].lower()))
                    for j, w in enumerate(out) if w["en"] and w["en"] != CONT and j != u[1] - 1)
        if spent >= have:
            set_gloss(u, CONT)
            continue
        # -- and the adverb must follow THIS verb in the verse: "went forth"
        # belongs to `alu atu`, so `tatalo atu` two units on does not say
        # "forth" (1 Nephi 1:5); `tautino atu` is "declare", not "declare forth"
        if idx > 0 and word in ("forth", "away", "down", "up", "out", "over", "back", "hither", "thither", "abroad", "in", "along", "off"):
            pg = gloss_of(units[idx - 1])
            pw = re.findall(r"[a-z']+", (pg or "").lower()) if pg and pg != CONT else []
            if not pw or not re.search(r"\b" + re.escape(pw[-1]) + r"\s+" + re.escape(word) + r"\b", en_l):
                set_gloss(u, CONT)
    # -- and a verb whose directional sits inside its unit takes the adverb
    # the verse sets right after it: `alu atu` "went forth" (1 Nephi 1:5),
    # `afifio ifo` "came down"
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    DIR_ADV = ("forth", "away", "down", "up", "out", "over", "back", "hither", "thither", "abroad", "in")
    for u in units:
        if u[1] - u[0] < 2 or not any(norm(t).strip(",;.") in SG.DIRECTIONALS for t in toks[u[0] + 1:u[1]]):
            continue
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        core = g.rstrip(" ,;.")
        tail = g[len(core):]
        words_ = core.split()
        if not words_:
            continue
        last = re.sub(r"[^a-z']", "", words_[-1].lower())
        if not last or last in DIR_ADV or not (looks_verbal(core) or last in ER.BASE_TO_PAST or last in ER.PAST_TO_BASE):
            continue
        ma_ = re.search(r"\b" + re.escape(last) + r"\s+(" + "|".join(DIR_ADV) + r")\b(?!\s+of\b)", en_l)
        if not ma_:
            continue
        adv = ma_.group(1)
        have = len(re.findall(r"\b" + adv + r"\b", en_l))
        spent = sum(len(re.findall(r"\b" + adv + r"\b", w["en"].lower())) for w in out if w["en"] and w["en"] != CONT)
        if spent < have:
            set_gloss(u, f"{core} {adv}{tail}")
    # THE ITERATIVE `toe` BELONGS TO ITS VERB (Dunn: "again, once more"): before
    # a verb it joins the verb's unit and says "again" only where the English
    # has an unspent "again"; `ma toe faamanatu atu` is "and rehearsed". An
    # empty `toe` is no unit of its own, so this walks the tokens
    for k in range(n - 1):
        if norm(toks[k]).strip(",;.") != "toe" or out[k]["en"] not in ("", "again"):
            continue
        nxt = next((j for j in range(k + 1, n) if out[j]["en"] and out[j]["en"] != CONT), None)
        if nxt is None or re.search(r"[,;:.?!][”’\"')]*$", toks[k]):
            continue
        have = len(re.findall(r"\bagain\b", en_l))
        spent = sum(len(re.findall(r"\bagain\b", w["en"].lower())) for j, w in enumerate(out) if w["en"] and w["en"] != CONT and j != k)
        out[k]["en"] = "again" if have > spent else CONT
    _stage("directional not borrowed")
    # THE ARTICLE: `le` is the definite singular and says "the" in every unit
    # that carries it; `se` the indefinite, "a" (user, John 1:7: `i le
    # malamalama` "of THE light"). The negator `le` (`e le o`) is not the article.
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    DET = r"^(another|other|same|own|the|a|an|his|her|its|their|my|thy|your|our|this|that|these|those|every|all|any|no|some|one|which|who|whom|whose|what|whoever|whosoever|whatever|whatsoever|whoso|none|each|both|such)\b"
    DISCOURSE_WORDS = ("wherefore", "therefore", "thus", "now", "then", "so", "behold", "yea", "nevertheless", "howbeit", "notwithstanding", "moreover", "verily", "amen")

    def verse_bare(rest):
        """"the X" where the verse has X and never "the (..) X": the X without
        its article, else None. Only a bare noun the verse itself uses bare."""
        mm = re.match(r"^the\s+(.+)$", rest.strip(), flags=re.I)
        if not mm:
            return None
        body = mm.group(1).rstrip(" ,;.")
        ws = body.split()
        if not ws or len(ws) > 3 or re.search(r"\b(is|are|was|were|be|not|of)\b", body.lower()):
            return None
        heads = {re.sub(r"[^a-z'-]", "", ws[-1].lower()), re.sub(r"[^a-z'-]", "", ws[0].lower())} - {""}
        if not heads or not all(re.search(r"\b" + re.escape(h) + r"\b", en_l) for h in heads):
            return None
        if any(re.search(r"\bthe\s+(?:(?!of\b)[a-z']+\s+){0,2}" + re.escape(h) + r"\b", en_l) for h in heads):
            return None
        return body

    for u in units:
        g = gloss_of(u)
        if not g or g == CONT or ER.tense_of(g):
            continue
        # a lexicalised discourse form (`o le mea lea` "wherefore", `o lenei`
        # "now") is one word of English and takes no article
        if " ".join(norm(t) for t in toks[u[0]:u[1]]).strip(",;.") in SG.DISCOURSE or g.strip(" ,;.").lower() in DISCOURSE_WORDS:
            continue
        # -- the negator `le` is not the article, wherever it stands: after a
        # marker or a bound pronoun in the unit, or at the unit's head right
        # after one (`lua te | le oti lava` "ye shall not die", Genesis 3:4)
        NEG_BEFORE = ("e", "te", "lei", "ua", "sa", "na", "ou", "tou", "matou", "latou", "tatou", "outou", "lua", "la", "ma", "ta")
        # -- `ma` before `le` is the conjunction "and" (`ma le alofa` "and the
        # mercies"), not the bound pronoun, when that is what it says
        arts = [q for q in range(u[0], u[1]) if norm(toks[q]) in ("le", "se")
                and not (q > 0 and norm(toks[q - 1]).strip(",;.") in NEG_BEFORE and not re.search(r"[,;:.?!][”’\"')]*$", toks[q - 1])
                         and not (norm(toks[q - 1]).strip(",;.") == "ma" and ((out[q - 1]["en"] or "").strip(" ,;.").lower() in ("and", "with", "&")
                                                                               or re.match(r"^(and|with)\b", g.lower()))))
                and not (q + 1 < u[1] and norm(toks[q + 1]) in ("o", "lei", "mafai", "toe", "iloa"))]
        if not arts:
            # NO DETERMINER -> PLURAL (user: "o le tagata" the man, "o se tagata" a
            # man, "ni tagata" some men, "o tagata" men). A bare noun unit takes
            # the plural the verse has (man -> men), else a regular one; mass
            # nouns and names stay.
            keys = [norm(t).strip(",;.") for t in toks[u[0]:u[1]]]
            if any(k in ("lea", "lenei", "lena", "lo", "la", "lona", "lana", "lou", "lau", "lo’u", "la’u", "loʻu", "laʻu", "ona", "ana", "ou", "au",
                         "tasi", "lua", "tolu", "fa", "lima", "ono", "fitu", "valu", "iva", "sefulu", "selau", "afe", "uma", "nisi", "isi", "se", "le") for k in keys):
                continue
            some = "ni" in keys
            m = re.match(r"^((?:and|but|for|then|so)\s+)?((?:out of|because of|according to|instead of|on account of|with|in|at|to|unto|for|by|from|on|upon|among|into|before|after|over|under|of|through|against|out|toward|towards|about|concerning|like|as|than|even|so)\s+)?(.*)$", g.strip(), flags=re.I)
            lead = (m.group(1) or "") + (m.group(2) or "")
            rest = m.group(3).rstrip(" ,;.")
            tail = m.group(3)[len(rest):]
            words_ = rest.split()
            # THE ARTICLE FOLLOWS THE VERSE: "the many" where the verse says "so
            # many things", "the heaven" where it says "of heaven" -- a "the"
            # the English never puts before this word is not the verse's
            bare = verse_bare(rest)
            if bare is not None:
                set_gloss(u, f"{lead}{bare}{tail}")
                continue
            if not words_ or re.match(DET, rest.lower()) or re.match(r"^[A-Z]", rest) or ER.tense_of(rest):
                continue
            head = words_[-1].lower()
            MASS = {"light", "darkness", "water", "grace", "truth", "life", "love", "faith", "glory", "world", "earth", "heaven", "flesh", "blood",
                    "peace", "power", "spirit", "wisdom", "fulness", "beginning", "name", "law", "bosom", "witness", "record", "salvation", "sin", "fire", "wine", "bread", "gold", "silver"}
            if head in MASS or head.endswith(("s", "ss")) or not head.isalpha():
                continue
            ewords = set(re.findall(r"[a-z']+", en_text.lower()))
            plural = None
            for cand in ER.IRREGULAR_NUMBER.get(head, set()) | {head + "s", head + "es", (head[:-1] + "ies") if head.endswith("y") else head + "s"}:
                if cand != head and cand in ewords:
                    plural = cand
                    break
            if plural is None and some:
                plural = next(iter(ER.IRREGULAR_NUMBER.get(head, set())), None) or (head[:-1] + "ies" if head.endswith("y") else head + "s")
            if plural:
                words_[-1] = plural
                set_gloss(u, f"{lead}{'some ' if some else ''}{' '.join(words_)}{tail}")
            continue
        art = "the" if norm(toks[arts[0]]) == "le" else "a"
        m = re.match(r"^((?:and|but|for|then|so)\s+)?((?:out of|because of|according to|instead of|on account of|with|in|at|to|unto|for|by|from|on|upon|among|into|before|after|over|under|of|through|against|out|toward|towards|about|concerning|like|as|than|even|so)\s+)?(.*)$", g.strip(), flags=re.I)
        lead = (m.group(1) or "") + (m.group(2) or "")
        rest = m.group(3)
        bare = verse_bare(rest)
        if bare is not None:
            # `o le lagi` "of heaven", `i le lalolagi` "in the world" -- the
            # verse decides whether `le` says "the" here (1 Nephi 1:9)
            set_gloss(u, f"{lead}{bare}{rest[len(rest.rstrip(' ,;.')):]}")
            continue
        if not rest or re.match(DET, rest.lower()) or re.match(r"^(was|were|is|are|be|not|it|he|she|they|we|i|you|ye|thou|there|let|to)\b", rest.lower()) \
                or re.search(r"\b(is|are|was|were|am|be|hath|have|had)\b", rest.lower()):
            continue
        if re.match(r"^[A-Z]", rest) and rest.split()[0].rstrip(",;.") not in ("God", "Word", "Light", "Lord"):
            continue          # a name takes no article
        # A VERB UNDER AN ARTICLE IS A NOUN (Dunn, unit seven, "using verbs as
        # nouns"): `le sau` "the coming", `le faalogo` "the hearing" -- the
        # gerund, when the verse has it
        words_ = rest.rstrip(" ,;.").split()
        if words_:
            head = re.sub(r"[^a-z']", "", words_[-1].lower())
            base = ER.PAST_TO_BASE.get(head, head)
            if (base in ER.BASE_TO_PAST or head in ER.PAST_TO_BASE) and base not in ("light", "name", "word", "work", "witness", "life", "love", "peace", "fire", "cross", "glass", "house", "hold", "lie", "lay"):
                ger = _gerund(base)
                if ger in set(re.findall(r"[a-z']+", (en_text or "").lower())):
                    rest = " ".join(words_[:-1] + [ger]) + rest[len(rest.rstrip(" ,;.")):]
        hw_ = re.sub(r"[^a-z'-]", "", words_[-1].lower()) if words_ else ""
        if art == "the" and hw_ and re.search(r"\b" + re.escape(hw_) + r"\b", en_l) and not re.search(r"\bthe\s+(?:(?!of\b)[a-z']+\s+){0,2}" + re.escape(hw_) + r"\b", en_l):
            continue            # "upon plates", "of heaven": the verse names it bare
        set_gloss(u, f"{lead}{art} {rest}")
    _stage("article")
    # THE QUANTIFIER PHRASE `le tele o X` IS "many X" (Dunn, unit five: `le
    # tele o` "the many of" -> many): `ua ia tusia le tele o mea` "he hath
    # written many things" -- the head says "many" (the verse's own "so many",
    # "a great many" when it has them) and the `o` phrase drops its article
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx in range(len(units) - 1):
        u, v = units[idx], units[idx + 1]
        if key_of(u).strip(",;.") not in ("le tele", "le toatele", "le anoanoai") or not key_of(v).startswith("o "):
            continue
        g, vg = gloss_of(u), gloss_of(v)
        if not g or g == CONT or not vg or vg == CONT or ER.tense_of(vg):
            continue
        mq = re.search(r"\b((?:so|a great|great|very|exceedingly)\s+)?(many|multitude)\b", en_l)
        set_gloss(u, ((mq.group(1) or "") + mq.group(2)) if mq else "many")
        set_gloss(v, re.sub(r"^(of\s+)?(the\s+)?", "", vg, count=1, flags=re.I))
    _stage("quantifier le tele o")
    # THE VERSE'S OWN FORM (the standard: the gloss names the English that word
    # renders in this verse). A curated reading the verse does not carry, whose
    # inflection or dictionary sense it DOES carry, takes the verse's form:
    # `vavalo atu` "prophesying" not "prophesy", `faatauemu` "mock" not
    # "mocking", `manino` "plainly" not "pure" (Pratt: clear, plain), `e
    # faaola ai` "of deliverance" not "to deliver" (1 Nephi 1:4, 1:8, 1:19, 1:20)
    ecount = Counter(re.findall(r"[a-z']+", en_l))
    AUXW = "must|shall|should|will|would|may|might|can|could|did|do|does|doth|hath|has|have|had|having|is|are|was|were|am|be|been|being|art|wilt|shalt|canst"
    AUX_SET = set(AUXW.split("|"))
    ADV_SET = {"not", "both", "also", "truly", "surely", "now", "then", "all", "so", "there", "thus", "indeed", "ever", "never", "yet", "still", "even", "greatly", "exceedingly"}
    SPEECH_SENSES = {"speak", "say", "tell", "talk", "command", "bid", "call", "cry", "cried", "shout"}
    SPEECH_WORDS = {"said", "spake", "saith", "bade", "commanded", "told", "saying", "answered", "cried", "asked", "spoke", "speak", "say", "tell", "declared", "exclaim", "exclaimed"}

    def _related(w, x):
        if w == x or not w or not x:
            return False
        if x in ER.stems(w) or w in ER.stems(x):
            return True
        if ER.PAST_TO_BASE.get(x) == w or ER.PAST_TO_BASE.get(w) == x:
            return True
        if x in (ER.BASE_TO_PAST.get(w) or ()) or w in (ER.BASE_TO_PAST.get(x) or ()):
            return True
        for a, b in ((w, x), (x, w)):
            if b.endswith("ing") and len(b) > 5 and (b[:-3] == a or b[:-3] + "e" == a or (len(b) > 6 and b[-4] == b[-5] and b[:-4] == a)):
                return True
            if b.endswith(("ance", "ence")) and len(b) > 6 and b[:-4] == a:
                return True
            if b.endswith("ed") and len(b) > 4 and (b[:-2] == a or b[:-1] == a or (len(b) > 5 and b[-3] == b[-4] and b[:-3] == a)):
                return True
            if b.endswith("ly") and len(b) > 5 and (b[:-2] == a or b[:-2] + "e" == a or (b.endswith("ily") and b[:-3] + "y" == a)):
                return True
            if b.endswith("s") and not b.endswith("ss") and len(b) > 3 and b[:-1] == a:
                return True
        return False

    def _gcount():
        return Counter(x for w in out if w["en"] and w["en"] != CONT for x in re.findall(r"[a-z']+", w["en"].lower()))

    DET_BEFORE = ("the", "a", "an", "his", "her", "its", "their", "my", "our", "your", "thy", "mine", "thine", "this", "that", "these", "those")

    def _senses_of(sm):
        out_ = []
        for sense in SG.dictionary(sm):
            for alt in re.split(r"[,;]", sense):
                alt = re.sub(r"^\s*(to|be|of)\s+", "", re.sub(r"\s*\(.*?\)", "", alt).strip().lower())
                if alt and len(alt.split()) == 1 and alt not in FUNCTION_ONLY and alt not in out_:
                    out_.append(alt)
        return out_

    # an open-class word left with NO gloss takes the dictionary sense the verse
    # carries, in the verse's form: `sa latou afifio ifo` "came" (1 Nephi 1:11);
    # a verb of speaking takes the verse's unspent verb of speaking (`fetalai
    # mai` "bade", the chiefly "speak")
    def fill_empty():
        for k in range(n):
            if out[k]["en"] != "":
                continue
            sm = norm(toks[k]).strip(",;.")
            if SG.token_class(sm) != "OPEN" or sm in SG.DIRECTIONALS:
                continue
            gcount = _gcount()
            senses = _senses_of(sm)
            done = False
            for alt in senses:
                cands = [x for x in ecount if x not in FUNCTION_ONLY and ecount[x] > gcount.get(x, 0) and (x == alt or _related(alt, x))]
                if cands:
                    x = max(cands, key=lambda c: (c == alt, c[:3] == alt[:3], -abs(len(c) - len(alt))))
                    out[k]["en"] = x + toks[k][len(toks[k].rstrip(",;.")):]
                    done = True
                    break
            if not done and set(senses) & SPEECH_SENSES:
                cands = [x for x in SPEECH_WORDS if ecount.get(x, 0) > gcount.get(x, 0)]
                if cands:
                    x = min(cands, key=lambda c: abs(en_l.find(c) / max(1, len(en_l)) - k / max(1, n)))
                    out[k]["en"] = x + toks[k][len(toks[k].rstrip(",;.")):]
                    done = True
            if done:
                # the auxiliary the verse sets right before the word comes with
                # it: `sa alaga atu` "did exclaim" (1 Nephi 1:14)
                x = re.sub(r"[^a-z']", "", out[k]["en"].lower())
                em_ = re.search(r"\b((?:(?:" + AUXW + r")\s+)+)(?:(?:my|his|her|their|our|your|thy|the|a|an)\s+[a-z']+\s+|(?:he|she|they|we|i|you|ye|thou|it)\s+)?" + re.escape(x) + r"\b", en_l)
                if em_:
                    aux_ = em_.group(1).split()
                    gc2 = _gcount()
                    if all(ecount.get(a_, 0) > gc2.get(a_, 0) for a_ in aux_):
                        out[k]["en"] = " ".join(aux_) + " " + out[k]["en"]
    fill_empty()
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for u in units:
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        parts = g.split()
        gcount = _gcount()
        changed = False
        for k_, tok in enumerate(parts):
            mt = re.match(r"^([^A-Za-z']*)([A-Za-z']+)(.*)$", tok)
            if not mt:
                continue
            w = mt.group(2).lower()
            if len(w) < 4 or w in FUNCTION_ONLY or w in AUX_SET or w in ecount or mt.group(2)[:1].isupper():
                continue
            if k_ > 0 and re.sub(r"[^a-z']", "", parts[k_ - 1].lower()) in DET_BEFORE:
                continue                      # a noun under its article stays a noun
            cands = [x for x in ecount if x not in FUNCTION_ONLY and ecount[x] > gcount.get(x, 0) and _related(w, x)]
            if not cands:
                # the word's own dictionary senses, in the verse's form
                sm_open = [norm(t).strip(",;.") for t in toks[u[0]:u[1]] if SG.token_class(norm(t).strip(",;.")) == "OPEN"]
                if len(sm_open) == 1 and len(parts) <= 2:
                    for alt in _senses_of(sm_open[0]):
                        cands = [x for x in ecount if x not in FUNCTION_ONLY and ecount[x] > gcount.get(x, 0) and (x == alt or _related(alt, x))]
                        if cands:
                            break
            if not cands:
                continue
            x = max(cands, key=lambda c: (c[:3] == w[:3], -abs(len(c) - len(w))))
            if k_ == 1 and parts[0].lower() == "to" and not re.search(r"\b(to|of)\s+" + re.escape(x) + r"\b", en_l):
                continue                      # "to inquire" is not "to asking"
            parts[k_] = mt.group(1) + x + mt.group(3)
            gcount[x] += 1
            changed = True
            # "to deliver" -> "of deliverance": the noun the verse has takes the
            # verse's preposition
            if k_ == 1 and parts[0].lower() == "to" and re.search(r"\bof\s+" + re.escape(x) + r"\b", en_l) and not re.search(r"\bto\s+" + re.escape(x) + r"\b", en_l):
                parts[0] = "of"
        if changed:
            set_gloss(u, " ".join(parts))
    _stage("the verse's form")
    # THE VERB'S SCAFFOLDING FOLLOWS THE VERSE. What stands before the verb --
    # auxiliary, copula, modal, "not", the relative, a stray article -- is the
    # verse's, never the memory's: `ua moni` "is true" beside "the record is
    # true" (not "are true"), `ua faaumatia` "must be destroyed", `sa olioli`
    # "did rejoice", `na ou faia` "which I have made", `sa manatu` "thought"
    # (not "a thought"), `o le a` + `faaumatia` "should" | "be destroyed", `sa
    # molimau atu ai` "testified" (never "did testified"), and a relative that
    # opens a clause after "and" has no antecedent and goes (1 Nephi 1:3, 1:4,
    # 1:8, 1:13, 1:15, 1:17, 1:19)
    ADVW = "|".join(sorted(ADV_SET))
    MODALS = ("shall", "should", "will", "would", "must", "may", "might", "can", "could")
    SUBJ_IN = r"(?:(?:my|his|her|their|our|your|thy|the|a|an)\s+[a-z']+\s+|(?:he|she|they|we|i|you|ye|thou|it)\s+)?"
    NOT_W = {"of", "to", "in", "at", "by", "for", "from", "with", "on", "upon", "into", "unto", "and", "but", "or", "if", "that", "which", "who",
             "whom", "the", "a", "an", "i", "he", "she", "it", "they", "we", "you", "ye", "thou", "me", "him", "her", "them", "us", "thee",
             "this", "these", "those", "there", "then", "so", "as", "than", "yea", "behold", "not", "no", "yes"}
    plans = {}
    units, start = [], 0
    for k in range(n):
        if out[k]["en"] and out[k]["en"] != CONT:
            units.append((start, k + 1))
            start = k + 1
    for idx, u in enumerate(units):
        g = gloss_of(u)
        if not g or g == CONT:
            continue
        core = g.rstrip(" ,;.:!?—")
        tail = g[len(core):]
        first_tok = norm(toks[u[0]]).strip(",;.")
        has_doer = any(norm(t).strip(",;.") in SG.DESCRIPTIVE_PRONOUNS or norm(t).strip(",;.") in SG.PRONOUNS for t in toks[u[0]:u[1]])
        pg = gloss_of(units[idx - 1]) if idx > 0 else ""
        pw = re.findall(r"[a-z']+", (pg or "").lower()) if pg and pg != CONT else []
        opens = idx == 0 or (pw and pw[-1] in ("and", "but", "for", "yea", "behold", "wherefore", "therefore", "now")) \
            or (idx > 0 and re.search(r"[;:.?!][”’\"')]*$", toks[units[idx - 1][1] - 1]))
        # (a) under a marker the word is a verb: "a thought" -> "thought" when the verse conjugates it
        m0 = re.match(r"^(a|an|the)\s+([a-z']+)$", core, flags=re.I)
        if m0 and first_tok in ("sa", "na", "ua") and re.search(r"\b(?:he|she|they|we|i|you|ye|thou|it|and|" + AUXW + r")\s+" + re.escape(m0.group(2).lower()) + r"\b", en_l):
            core = m0.group(2)
        # (b) a relative needs its noun: after "and" or at a clause start it goes
        mr = re.match(r"^(which|that|who|whom)\s+(.+)$", core, flags=re.I)
        if mr and first_tok in ("sa", "na", "ua", "e") and opens:
            core = mr.group(2)
        # (c) the relative clause the verse sets on the noun before: `a lo'u
        # tama, ua faia` "of my father, which consists" (1 Nephi 1:2)
        if first_tok in ("ua", "na", "sa") and not has_doer and pw and not opens and pw[-1] not in FUNCTION_ONLY:
            mrel = re.search(r"\b" + re.escape(pw[-1]) + r",?\s+(which|that|who)\s+((?:(?:" + AUXW + r")\s+)*[a-z']+)\b", en_l)
            if mrel:
                cw = re.findall(r"[a-z']+", core.lower())
                gc_ = _gcount()
                rel_last = mrel.group(2).split()[-1]
                if cw and rel_last not in cw and gc_.get(rel_last, 0) < ecount.get(rel_last, 0) and rel_last not in AUXW.split("|"):
                    core = mrel.group(1) + " " + mrel.group(2)
        # (d) "to spake": an infinitive marker before a past form the verse conjugates
        mi = re.match(r"^to\s+([a-z']+)$", core, flags=re.I)
        if mi and mi.group(1).lower() in ER.PAST_TO_BASE and not re.search(r"\bto\s+" + re.escape(mi.group(1).lower()) + r"\b", en_l):
            core = mi.group(1)
        if core + tail != g:
            set_gloss(u, core + tail)
        # (e) the auxiliaries before the verb are the verse's -- planned here,
        # applied below so that the auxiliary the verse sets right before THIS
        # word ("did mock") wins over one a memory attached elsewhere ("did testified")
        ms = re.match(r"^((?:(?:and|but|for|yea|that|which|who|whom|when|as|because|if|then|so)\s+)?)((?:(?:he|she|it|they|we|i|you|ye|thou|there)\s+)?)((?:(?:" + AUXW + r")\s+)*)((?:not\s+)?)([a-z']+)$", core, flags=re.I)
        if ms:
            lead, pron, gaux, gneg, W = ms.groups()
            Wl = W.lower()
            if Wl not in AUX_SET and Wl not in NOT_W and Wl not in ADV_SET and re.search(r"\b" + re.escape(Wl) + r"\b", en_l):
                em = re.search(r"\b((?:(?:" + AUXW + r")\s+)+)(?:(?:" + ADVW + r")\s+)?" + SUBJ_IN + re.escape(Wl) + r"\b", en_l)
                plans[idx] = {"lead": lead, "pron": pron, "gaux": gaux.lower().split(), "gneg": gneg, "W": W, "Wl": Wl,
                              "eaux": em.group(1).lower().split() if em else None, "tail": tail}

    def _apply(idx, eaux):
        pl = plans[idx]
        pron = pl["pron"]
        if eaux and eaux[0] in ("having", "being"):
            pron = ""                     # "having seen", never "I having seen"
        if eaux and eaux[0] in MODALS and idx > 0:
            # the modal belongs to the marker unit before it: `o le a` "should"
            # | "be destroyed"; `o le a ou` "I will" | "show"
            pg_ = gloss_of(units[idx - 1]) or ""
            pw_ = pg_.rstrip(" ,;.").split()
            pk_ = key_of(units[idx - 1]).strip(",;.")
            if pw_ and pw_[-1].lower() in MODALS and (pk_.startswith("o le a") or pk_.startswith("o le ā") or len(pw_) == 1):
                if pw_[-1].lower() != eaux[0]:
                    pw_[-1] = eaux[0]
                    set_gloss(units[idx - 1], " ".join(pw_) + pg_[len(pg_.rstrip(" ,;.")):])
                eaux = eaux[1:]
        set_gloss(units[idx], f"{pl['lead']}{pron}{' '.join(eaux)}{' ' if eaux else ''}{pl['gneg']}{pl['W']}{pl['tail']}")

    pending = [i for i, pl in plans.items() if pl["eaux"] is not None and pl["eaux"] != pl["gaux"]]
    for idx in sorted(pending):
        pl = plans[idx]
        later_need = Counter(a for j in pending if j > idx for a in plans[j]["eaux"])
        used = Counter()
        for j, v in enumerate(units):
            if j == idx or (j in plans and plans[j]["eaux"] is None) or j in pending and j > idx:
                continue          # the unverified and the still-pending do not count
            vg_ = gloss_of(v)
            if vg_ and vg_ != CONT:
                used.update(re.findall(r"[a-z']+", vg_.lower()))
        if all(ecount.get(a, 0) >= used.get(a, 0) + later_need.get(a, 0) + pl["eaux"].count(a) for a in set(pl["eaux"])):
            _apply(idx, list(pl["eaux"]))
    # the auxiliaries the verse does not set beside the word: kept where the
    # verse has them to spare, dropped where it does not -- and do-support
    # before a past form ("did testified") is no form at all
    for idx, pl in sorted(plans.items()):
        if pl["eaux"] is not None:
            continue
        gaux = list(pl["gaux"])
        if gaux and gaux[-1] in ("did", "do", "does", "doth") and pl["Wl"] in ER.PAST_TO_BASE:
            gaux = gaux[:-1]
        gc_ = _gcount()
        keep = [a for a in gaux if ecount.get(a, 0) >= gc_.get(a, 0)]
        if keep != pl["gaux"]:
            _apply(idx, keep)
    _stage("verb scaffolding")
    # A CAPITAL THE VERSE WRITES MID-SENTENCE IS THE VERSE'S: "he saw One
    # descending" (1 Nephi 1:9) keeps its One
    caps = {}
    lower_seen = set(re.findall(r"\b[a-z][a-z']+\b", en_text or ""))
    for mc in re.finditer(r"[A-Za-z'’]+", en_text or ""):
        wtxt = mc.group(0)
        before = (en_text or "")[:mc.start()].rstrip()
        if not before or before[-1] in ".!?:\"“‘'" or not wtxt[:1].isupper() or len(wtxt) < 3 or wtxt.lower() in lower_seen:
            continue
        if wtxt.lower() in DISCOURSE_WORDS or wtxt.lower() in ("and", "but", "for", "the", "thou", "thy", "thee", "come", "arise", "go", "hear", "let"):
            continue
        caps[wtxt.lower()] = wtxt
    if caps:
        for u in units:
            g = gloss_of(u)
            if not g or g == CONT:
                continue
            g2 = re.sub(r"\b([a-z][a-z']+)\b", lambda mm: caps.get(mm.group(1), mm.group(1)), g)
            if g2 != g:
                set_gloss(u, g2)
    # NO CONTENT GLOSS TWICE: `fetogi` "stoned" | `i maa` "stoned" where the
    # verse stones once -- the second says nothing (1 Nephi 1:20)
    seen_ = Counter()
    DEDUPE_SKIP = FUNCTION_ONLY | {"also", "again", "even", "yea", "if", "and", "but", "for", "or", "nor", "then", "so", "that", "which", "who",
                                   "when", "as", "because", "not", "no", "lo", "behold", "verily", "thus", "now", "therefore", "wherefore"}
    COUNT_SKIP = {"the", "a", "an", "of", "to", "in", "at", "by", "for", "from", "with", "on", "upon", "into", "unto", "and", "but", "or", "nor",
                  "if", "that", "which", "who", "whom", "whose", "he", "she", "it", "they", "we", "i", "you", "ye", "thou", "me", "him", "her",
                  "them", "us", "thee", "his", "its", "their", "my", "our", "your", "thy", "mine", "thine", "this", "these", "those", "there",
                  "then", "so", "as", "than", "is", "are", "was", "were", "be", "been", "am", "not", "no", "yes", "also", "again", "even", "yea",
                  "lo", "behold", "verily", "thus", "now", "therefore", "wherefore", "when", "because", "shall", "will", "should", "would", "may",
                  "might", "can", "could", "do", "did", "does", "have", "has", "had", "hath"}
    blanked = []
    for idx, u in enumerate(units):
        g = gloss_of(u)
        if not g or g == CONT or g.strip()[:1].isupper():
            continue                          # a name is never a double: "Er, and Onan"
        core = g.strip(" ,;.:!?—").lower()
        words_ = re.findall(r"[a-z']+", core)
        if all(w_ in DEDUPE_SKIP for w_ in words_):
            continue
        # counted: every word but the grammar's own (a quantifier counts --
        # "many things" is spent once the verse's one "many" is)
        content_ = [w_ for w_ in words_ if w_ not in COUNT_SKIP] or words_
        # the verse's count of the phrase's content words -- "the name of his
        # city ... his wife's name" has "name" twice, so two "the name" stand;
        # a word the verse never writes (Ieova beside "the LORD") is no evidence
        phrase_have = len(re.findall(r"\b" + re.escape(core) + r"\b", en_l)) if len(words_) > 1 else 0
        have = phrase_have if phrase_have >= 1 else min(ecount.get(w_, 0) for w_ in content_)
        if have < 1:
            seen_[core] += 1
            continue
        if seen_[core] and have <= seen_[core]:
            # the unit whose Samoan word MEANS the gloss keeps it: `le igoa`
            # "the name" beside "his wife's name" (its dictionary sense is the
            # word itself); `sa alaga atu` "many things" and `i maa` "stoned" do not
            says_ = any(any(alt in content_ for alt in _senses_of(norm(t).strip(",;.")))
                        for t in toks[u[0]:u[1]] if SG.token_class(norm(t).strip(",;.")) == "OPEN")
            if says_:
                seen_[core] += 1
                continue
            # the later unit's open-class word is left EMPTY, for the dictionary
            # pass below, its particles say nothing
            verbal_ = any(norm(t).strip(",;.") in ("sa", "na", "ua", "e", "te") for t in toks[u[0]:u[1]]) or key_of(u).startswith("o le a")
            for q in range(u[0], u[1]):
                sm_ = norm(toks[q]).strip(",;.")
                if out[q]["en"] == "":
                    continue
                if verbal_ and SG.token_class(sm_) == "OPEN" and sm_ not in SG.DIRECTIONALS:
                    out[q]["en"] = ""
                    blanked.append(q)
                else:
                    out[q]["en"] = CONT
            continue
        if len(words_) >= 2 and have <= 1:
            # "Your throne is high in the heavens" | "your throne": the phrase
            # is the later unit's (its Samoan says it), and a remembered SENTENCE
            # before it keeps the rest -- a short phrase before it is its own
            for j in range(idx):
                pg_ = gloss_of(units[j])
                if pg_ and pg_ != CONT and len(pg_.split()) >= len(words_) + 3 and re.search(r"\b" + re.escape(core) + r"\b", pg_.lower()):
                    ng_ = re.sub(r"\s*\b" + re.escape(core) + r"\b\s*", " ", pg_, count=1, flags=re.I).strip()
                    if ng_ and re.findall(r"[a-z']+", ng_.lower()):
                        set_gloss(units[j], ng_)
        seen_[core] += 1
    fill_empty()
    for q in blanked:
        if out[q]["en"] == "":
            out[q]["en"] = CONT
    _stage("capitals and doubles")
    for w in out:
        if w["en"] and w["en"] != CONT:
            w["en"] = modernise(tidy(w["en"]))     # the Bible keeps its forms; the other volumes read modern
    return out


def attach_particles(out, toks):
    """Make a blank particle a CONTINUATION of the unit it belongs to."""
    n = len(out)

    def glossed(k):
        return bool(out[k]["en"]) and out[k]["en"] != CONT

    for j in range(n):
        if out[j]["en"]:
            continue
        tok = norm(out[j]["sm"])
        back = tok in LEANS_BACK
        fwd = (tok in SG.PHRASE_INITIAL or tok in SG.TAM
               or tok in SG.PHRASE_LINKERS)
        if not (back or fwd):
            continue
        if back:
            # `aso lea`, `lelei lava`, `malamalama ai lea`: the particle is
            # part of the word before it. The renderers group a `·` with the
            # word that FOLLOWS, so binding backwards means the word's gloss
            # moves onto the particle and the word carries the `·` -- the
            # curation's own unit-final convention (`o le mea lea` = therefore,
            # glossed on `lea`). Left to right, a chain (`ai lea`) walks the
            # gloss to its last particle.
            k = j - 1
            while k >= 0 and out[k]["en"] == CONT:     # over the unit's own particles: `silasila atu i ai`
                k -= 1
            if k >= 0 and glossed(k):
                out[j]["en"] = out[k]["en"]
                for m in range(k, j):
                    out[m]["en"] = CONT
        else:
            k = j + 1
            while k < n and not out[k]["en"]:
                k += 1
            if k < n and out[k]["en"]:
                out[j]["en"] = CONT


# `te lei` is the past negative after a clitic doer (Dunn: `ou te lei alu` "I
# did not go") -- the same frame as `e lei`, with the marker in its bound form
NEG_PAST_UNITS = {"e lei", "e le’i", "e leʻi", "lei", "le’i", "leʻi", "te lei", "te le’i", "te leʻi"}
NEG_UNITS = NEG_PAST_UNITS | {"leai", "e leai"}
# THE NEGATED MODAL (user, 2 Nephi 1:14: "e le mafai ai - this is a grammar rule"):
# `e le mafai` "cannot"; its `ai` is the anaphoric pro-phrase ("thence") and its
# `ona` the verb's link, both absorbed into the frame (Dunn, unit five)
MODAL_NEG = {"e le mafai", "e lē mafai", "e le mafai ai", "e lē mafai ai", "e le mafai ona", "e lē mafai ona",
             "te le mafai", "te lē mafai", "te le mafai ona", "te lē mafai ona", "le mafai ona", "lē mafai ona"}
# after these the verb stands bare: the purposive, the optative / imperative,
# the deferential `sei`, and `ne’i` "lest" (Dunn, units three and six)
BARE_AFTER = {"ina ia", "ia", "sei", "se’i", "seʻi", "seia", "se’ia", "ne’i", "neʻi", "ina", "aua", "aua nei", "soia"}
AGENT_PRONOUNS = {"ia", "i latou", "i laua", "i matou", "i tatou", "i maua", "i taua", "oe", "au", "a’u", "aʻu", "outou", "oulua", "latou", "laua", "matou", "tatou"}
DEBUG = {"key": ""}   # the verse being glossed, for --debug


def looks_like_name(toks, i, en_text, names) -> bool:
    """Is this token a proper name IN THIS VERSE?

    The corpus-wide set (`build_names`) needs a word never written in lower
    case, and `Elia` (Elias) fails it because `elia` "digged" is a word too.
    So the verse decides: a capital that is not sentence-initial, beside an
    English that has a capitalised word (not sentence-initial either) opening
    with the same two letters. Nothing is hand-listed."""
    core = re.sub(r"[^\w’ʻ]", "", toks[i])
    if len(core) < 3 or not core[0].isupper():
        return False
    if core.lower() in names:
        return True
    prev = toks[i - 1] if i else ""
    if i == 0 or re.search(r"[.?!][”’\"')]*$", prev) or prev.endswith(("“", "‘", '"')):
        return False
    caps = set()
    for sentence in re.split(r"(?<=[.?!])\s+", en_text or ""):
        words = re.findall(r"[A-Za-z][A-Za-z']+", sentence)
        for w in words[1:]:
            if w[0].isupper():
                caps.add(w.lower())
    return any(w[:2] == core.lower()[:2] for w in caps)


def clause_tense(toks, i):
    """The tense of the nearest marker earlier in this clause, or None.

    `e` is left out: it is the ergative and the relative marker far more often
    than the general TAM, and a wrong present would undo a right past."""
    for k in range(i - 1, -1, -1):
        if toks[k][-1:] in SG.CLAUSE_END:
            return None
        t = norm(toks[k])
        if t in SG.TAM and t != "e" and SG.tense_of_tam(t):   # `ia` is a marker with no tense: keep looking
            return SG.tense_of_tam(t)
    return None


def unit_tense(key_sm: str):
    """The tense the marker at the head of this unit calls for, if any."""
    toks = key_sm.split()
    for k in (3, 2, 1):
        if len(toks) >= k:
            t = SG.tense_of_tam(" ".join(toks[:k]))
            if t:
                return t
    return None


def align_to_verse(gloss: str, english: str) -> str:
    """Say it in the VERSE'S words where the curation used a synonym.

    The English column decides the rendering. 1 Nephi 1:8 reads "in the
    attitude of singing"; the curation glosses `e foliga mai` "in the manner
    of". One content word apart, so the veto threw the whole phrase away and
    the verse got a literal "appears" instead of the column's own wording.

    So: if the candidate matches a run of the verse word for word EXCEPT for a
    single content word, take the verse's word. The shape has to match exactly
    -- same length, same function words in the same places -- which is what
    stops this from being a synonym generator. It can only ever swap one word
    for the word the verse itself uses in that position.
    """
    # TRIED AND REVERTED. Matching the SHAPE is not enough to know two words
    # mean the same thing: this turned "the voice of" into "the attitude of"
    # as readily as it turned "in the manner of" into it, because both differ
    # from the verse by one content word in the same slot. Content F1 86.0 ->
    # 84.4. Doing it properly needs evidence that the two words are synonyms,
    # and the dictionary gives Samoan->English, not English->English.
    return gloss

    g = gloss.split()
    if len(g) < 3:
        return gloss
    e = re.findall(r"[A-Za-z’']+", english)
    gl = [w.lower().strip(".,;:") for w in g]
    for i in range(len(e) - len(g) + 1):
        window = [w.lower() for w in e[i:i + len(g)]]
        diff = [k for k in range(len(g)) if window[k] != gl[k]]
        if len(diff) != 1:
            continue
        k = diff[0]
        # the differing word must be CONTENT on both sides -- swapping a
        # function word would change the grammar, not the vocabulary
        if gl[k] in FUNCTION_ONLY or window[k] in FUNCTION_ONLY:
            continue
        out = list(g)
        out[k] = e[i + k]
        return " ".join(out)
    return gloss


def _spent_before(out, i) -> Counter:
    """The English words the units before token i already carry, by form."""
    c = Counter()
    for w in out[:i]:
        if w["en"] and w["en"] != CONT:
            for x in re.findall(r"[a-z']+", w["en"].lower()):
                c[x] += 1
                if x == "cannot":
                    c["can"] += 1; c["not"] += 1
    return c


def _over_spent(words, english, spent) -> int:
    """How many of these words the verse has no unspent copy of: "made" is
    in 2 Nephi 1:1 once, on "had made an end", so a candidate "made" for
    `na faia` four clauses later borrows it -- "had done" is what is left."""
    if not spent:
        return 0
    enc = Counter(re.findall(r"[a-z']+", (english or "").lower()))
    over = 0
    for w in words:
        forms = {w} | _stems(w)
        have = sum(enc.get(f, 0) for f in forms)
        used = sum(spent.get(f, 0) for f in forms)
        if have and used >= have:
            over += 1
    return over


def choose(cands: Counter, english: str, want_tense: str | None = None,
           strict: bool = False, spent: Counter | None = None) -> tuple[str, str]:
    cands = merge_punctuation(cands)
    """(gloss, why). '' means leave it empty."""
    if len(cands) == 1:
        only = cands.most_common(1)[0][0]
        # IN THE BIBLE THE VERSE STILL DECIDES. A unanimous curated reading is a
        # human decision about the Book of Mormon's usage; O le Tusi Paia uses
        # the same word elsewhere -- `uiga` is "concerning" in every curated
        # verse and "kind" in "after his kind" -- so there a unanimous reading
        # the verse does not carry is vetoed, and the dictionaries and the
        # learned lexicon get their turn.
        if strict and vetoed(only, english):
            return trim_absent_tail(only, english), "settled-unconfirmed"
        # A UNANIMOUS CURATED READING IS A HUMAN DECISION about this exact
        # Samoan string, and the veto exists to arbitrate between COMPETING
        # readings -- not to overrule one. `sa ia faapa’ū ifo` is glossed "he
        # fell down" in the curation and 1 Nephi 1:7 reads "he cast himself
        # upon his bed": the English chose other words and the Samoan still
        # says fell down. Vetoed, the verse printed nothing at all.
        return trim_absent_tail(only, english), "settled"
    ew = content_words(english)
    stem_ew = set()
    for w in ew:
        stem_ew |= _stems(w)
    scored = []
    for gloss, n in cands.items():
        words = re.findall(r"[a-z']+", gloss.lower())
        core = [w for w in words
                if w not in ("i", "you", "we", "they", "he", "she", "it", "the",
                             "a", "an", "of", "to", "and")]
        # the SAME test the scoring uses; when these two disagreed, a gloss
        # could fail the gate on `you` while the verse said `ye` and be thrown
        # away before it was ever scored
        if not core or not all(in_english(w, ew) for w in core):
            continue
        # EVERY word counts, function words included. The old score looked only
        # at content words, so `faatasi` -> "together with" beat "together" in a
        # verse reading "listen together" and no "with" anywhere: the stray
        # preposition was invisible to the test that was supposed to catch it.
        present = sum(1 for w in words if in_english(w, ew))
        absent = sum(1 for w in words if not in_english(w, ew))
        # A RATIO, not a count. Counting rewarded length: `tagata uma` came out
        # "all the people" over "all men" because three words of the English
        # beat two, though both are entirely carried by it. The question is
        # what fraction of the gloss the verse accounts for; how often the
        # Book of Mormon chose it breaks the tie.
        # a candidate that carries a negation the verse has outranks one that
        # silently drops it, whatever the ratio says
        neg = sum(1 for w in words if w in NEGATIONS and in_english(w, ew))
        # TENSE AGREEMENT. The marker in front of the unit says what tense the
        # verb is in -- `o le a` is future 97% of the time, `sa`/`na` past 66%,
        # `ua` perfect -- and nothing used to consult it, so `sa alu` and `o le
        # a alu` could come out the same word. A candidate that agrees with the
        # marker outranks one that does not, AFTER the verse's own evidence:
        # the verse still decides what the words are, this only decides which
        # form of them.
        # BASE: after the purposive `ina ia` or the optative `ia` the verb is
        # uninflected ("to witness", "let … believe"), so a bare candidate wins
        agrees = 1 if (want_tense == "BASE" and ER.tense_of(gloss) is None) or (want_tense and want_tense != "BASE" and ER.tense_of(gloss) == want_tense) else 0
        over = _over_spent([w for w in core if w not in FUNCTION_ONLY], english, spent)
        scored.append((present / max(1, present + absent), -over, neg, agrees, n, gloss))
    if scored:
        scored.sort(reverse=True)
        # trim on this path too: the scoring picks the best of what the
        # inventory offers, and the best may still carry a word the verse does
        # not have, when every candidate does
        return trim_absent_tail(scored[0][-1], english), "canon"
    # THE BEST PARTIAL READING, when no candidate is carried whole: `na faia e
    # le Alii` is "which the Lord had done" in the curation and 2 Nephi 1:1
    # reads "how great things the Lord had done" -- the relative pronoun is the
    # only word missing. A candidate the verse carries at least three-quarters
    # of, its tensed verb included, is taken with its absent edges trimmed;
    # anything looser stays empty for the sentence pass and the lexicon
    partial = []
    for gloss, cnt in cands.items():
        words = re.findall(r"[a-z']+", gloss.lower())
        if len(words) < 2:
            continue
        present = [w for w in words if in_english(w, ew)]
        if len(present) / len(words) >= 0.75 and any(ER.tense_of(w) for w in present):
            # the words that stand TOGETHER in the English, in this order, are
            # the verse's own phrase: "the Lord had done" over "the Lord made",
            # whose "made" is borrowed from "had made an end" four clauses away
            en_words = re.findall(r"[a-z']+", (english or "").lower())
            contig = 0
            for i0 in range(len(en_words)):
                j = i0; hit = 0
                for w in present:
                    while j < len(en_words) and j - i0 < len(present) + 2 and not (en_words[j] == w or en_words[j] in _stems(w)):
                        j += 1
                    if j < len(en_words) and j - i0 < len(present) + 2:
                        hit += 1; j += 1
                    else:
                        break
                contig = max(contig, hit)
            over = _over_spent([w for w in present if w not in FUNCTION_ONLY], english, spent)
            partial.append((contig == len(present), -over, len(present) / len(words), cnt, gloss))
    if partial:
        partial.sort(reverse=True)
        best = partial[0][-1]
        first = re.sub(r"[^a-z']", "", best.split()[0].lower())
        if first in ("which", "that", "who", "whom", "whose") and not in_english(first, ew):
            best = best.split(None, 1)[1]
        return trim_absent_tail(best, english), "canon-partial"
    dom, n = cands.most_common(1)[0]
    if vetoed(dom, english):
        return "", "vetoed"
    total = sum(cands.values())
    if n / total >= 0.90:
        return trim_absent_tail(dom, english), ("dominant-unconfirmed" if strict else "dominant")
    return "", "undecided"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--bible", action="store_true",
                    help="gloss O le Tusi Paia (book_<id>.json) instead of the Book of Mormon volumes")
    ap.add_argument("--book", default="", help="with --bible: one book id, e.g. genesis")
    ap.add_argument("--all", action="store_true",
                    help="the whole corpus in one run: Book of Mormon, D&C and Pearl of Great Price, then the Old and New Testaments")
    ap.add_argument("--debug", default="", help="print every unit's (samoan, gloss, why) for one verse key, e.g. john|1|12")
    a = ap.parse_args(argv)

    ov = json.loads((RES / "bom_overrides.json").read_text(encoding="utf-8"))

    # EVIDENCE IS CURATED VERSES ONLY. The inventory was being built from every
    # verse in the file, and this script's own previous output is in that file:
    # a gloss it guessed last run came back as evidence this run, outvoted the
    # curation it was derived from, and the two runs disagreed with each other.
    # A corpus can never be validated against itself. `generated` is the list
    # of verses this script wrote, so the Book of Mormon's 42,538 hand-curated
    # units are exactly what is left.
    units = load_evidence()
    inv = build_inventory(units)
    lex = build_word_lexicon(units)
    maxlen = max(len(k.split()) for k in inv)
    english = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
    books = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))["books"]
    # O le Tusi Paia: its books are one file each. They join the name
    # derivation whether or not they are being glossed, so a Bible name that
    # the Book of Mormon never writes (Aperaamo, Hanoka) still counts as one.
    bible_books = []
    bible_index = None
    # THE TOKENS COME FROM THE DUAL BUILD. build_tusi_paia_dual.py writes the
    # verse tokens (1887 text, fallbacks, hand layer, text fixes) to
    # corpus/tusi_paia/dual/; this pass glosses them and writes the glossed
    # books to Resources. It used to read Resources -- its own last output --
    # so a rebuilt text (the `ie` -> `le` repair) never reached the app until
    # someone copied the files by hand. The dual index and English are synced
    # to Resources here for the same reason.
    dual_src = HERE.parent / "corpus" / "tusi_paia" / "dual"
    if (dual_src / "tusi_paia_index.json").exists():
        import shutil
        for name in ("tusi_paia_index.json", "tusi_paia_english.json"):
            if (dual_src / name).exists():
                shutil.copyfile(dual_src / name, RES / name)
    if (RES / "tusi_paia_index.json").exists():
        bible_index = json.loads((RES / "tusi_paia_index.json").read_text(encoding="utf-8"))
        for meta in bible_index["books"]:
            path = dual_src / f"book_{meta['id']}.json"
            if not path.exists():
                path = RES / f"book_{meta['id']}.json"
            if path.exists():
                bible_books.append(json.loads(path.read_text(encoding="utf-8")))
    names = build_names(books + bible_books)
    print(f"proper names derived   {len(names)}")

    # EVERY VOLUME. The curated segmentation drew boundaries the grammar
    # forbids -- `i luga o`, `o loo i`, 3,635 units ending on a phrase head --
    # so it no longer decides where units fall anywhere in the corpus. It is
    # kept in full as EVIDENCE (curated_evidence.json, 111,683 pairs): it still
    # says what a Samoan string was read as, it just no longer says where the
    # string stops.
    already = set()
    hand = set()
    stats = Counter()
    made = 0

    # THE DECISION LOOP, once, for every volume. Given a verse's tokens and its
    # (modernised) English, gloss it: grammar first, then the curated
    # inventory, the lexicon, the dictionary, the dominant lemma. The Book of
    # Mormon volumes and O le Tusi Paia both come through here.
    def gloss_tokens(toks, en_text, strict=False, inner=False, tense=None):
        trace = []   # (unit, gloss, why) per unit, printed for --debug
        nonlocal stats
        out = [{"sm": t, "en": ""} for t in toks]
        i = 0
        prev_key = ""
        # THE SEQUENTIAL FRAME `ona … ai lea` IS NARRATIVE PAST. Between the
        # `ona` the grammar has just read as then/and and the `lea` that closes
        # it, the verb is in the past, and a stative takes the copula the verse
        # gives it: `ona malamalama ai lea` is "and / there was light / · / ·".
        seq_frame = False      # between `ona` and its `lea`: the closing `ai lea` is silent
        seq_verb = (tense == "PAST")   # the first open-class unit after `ona` takes the narrative past
        while i < len(toks):
            hit, src = frame_at(toks, i, inv, maxlen, lex, names, seq=strict)
            if src == "seqframe":
                # gloss the verb phrase inside the frame on its own, then fold
                # the frame's "and/then", its past, and the verse's copula round it
                close = i + hit - 1
                inner_end = close - 1 if norm(toks[close - 1]) == "ai" else close
                sub = gloss_tokens(toks[i + 1:inner_end], en_text, strict, inner=True, tense="PAST")
                verb = " ".join(w["en"] for w in sub if w["en"] and w["en"] != CONT).strip()
                ew_ = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                # the clitic pronoun inside the frame is the subject: `ona ou alu
                # ai lea` is "and I go", not "go" (2 Nephi 1:14)
                first_ = norm(toks[i + 1]) if i + 1 < inner_end else ""
                CLIT_ = {"ou": "I", "e": "you", "ia": "he", "outou": "you", "tatou": "we", "matou": "we", "latou": "they", "lua": "you", "la": "they", "ta": "we", "ma": "we"}
                if verb and first_ in CLIT_ and not re.match(r"^(i|you|he|she|it|we|they|there)\b", verb.lower()):
                    pr_ = CLIT_[first_]
                    if re.search(r"\b" + pr_.lower() + r"\s+" + re.escape(verb.lower().split()[0]), (en_text or "").lower()):
                        verb = f"{pr_} {verb}"
                if verb:
                    m = re.search(r"\b(there (?:was|were)) " + re.escape(verb.lower()) + r"\b", (en_text or "").lower())
                    if m and not verb.lower().startswith("there "):
                        verb = f"{m.group(1)} {verb}"
                    lead = next((alt for alt in ("then", "and") if in_english(alt, ew_)), "")
                    if lead and re.match(r"^(and|then|so)\b", verb.lower()):
                        lead = ""                      # the verb's own gloss already opens the clause ("and answered")
                    gloss = f"{lead} {verb}".strip()
                    for j in range(i, close):
                        out[j]["en"] = CONT
                    out[close]["en"] = modernise(gloss)
                    stats["unit: seqframe"] += 1
                    prev_key = "lea"
                    i += hit
                    continue
                # nothing glossable inside: fall back to the ordinary framing of `ona`
                hit, src = 1, "frame"
            if not hit:
                # A WORD NOBODY HAS SEEN IS STILL A WORD. Nothing in the
                # curation, the lexicon or the grammar frames it, so it used to
                # be skipped before the dictionaries were ever asked -- and the
                # Bible is full of words the Book of Mormon never used
                # (fegaoioiai, nunumi). It stands as its own unit and goes
                # through the later stages: Pratt, EALD, the learned lexicon,
                # the leftover pairing.
                stats["token: no unit"] += 1
                hit, src = 1, "none"
            def nxt_of(k):
                """the next token for a frame, or '' when the unit ends a sentence"""
                if re.search(r"[.;:?!][”’\"')]*$", toks[k - 1]) or k >= len(toks):
                    return ""
                return norm(toks[k])
            # A CURATED UNIT THE VERSE DOES NOT CARRY WHOLE GIVES WAY TO ITS
            # CURATED PARTS. `na faia e le Alii` was remembered twice ("which
            # the Lord made", "has done the Lord") and 2 Nephi 1:1 reads "the
            # Lord had done": the whole falls to a partial reading while its
            # parts `na faia` "had done" and `e le Alii` "the Lord" are carried
            # entire. The longest memory wins only when the verse carries it.
            if hit >= 3 and src == "inv":
                whole = norm(" ".join(toks[i:i + hit]))
                if whole in inv:
                    g0, why0 = choose(inv[whole], en_text, None, strict, _spent_before(out, i))
                    doubled = bool(g0) and _over_spent([w for w in re.findall(r"[a-z']+", g0.lower()) if w not in FUNCTION_ONLY or w in ("can", "could", "may", "might", "shall", "will")], en_text, _spent_before(out, i)) > 0
                    if why0 in ("canon-partial", "undecided", "vetoed", "settled-unconfirmed", "dominant-unconfirmed") or doubled:
                        for k_ in range(1, hit):
                            a_, b_ = norm(" ".join(toks[i:i + k_])), norm(" ".join(toks[i + k_:i + hit]))
                            if a_ in inv and b_ in inv:
                                ga, wa = choose(inv[a_], en_text, None, strict, _spent_before(out, i))
                                gb, wb = choose(inv[b_], en_text, None, strict)
                                # a degree word (`tele`, `matua`) or a particle may close the
                                # split: the English often has no word for it, and the
                                # particle reader handles it on its own next
                                tail_ok = (hit - k_ == 1 and (b_ in SG.DEGREE or b_ in SG.CLOSED_CLASS))
                                # and a closed-class HEAD (`ona`, `ia`, `e`) may open the split
                                # the same way: `ona | toe foi mai ai` -- the particle reader
                                # and the frames handle it, the tail is carried whole
                                head_ok = (k_ == 1 and a_ in SG.CLOSED_CLASS and gb and wb in ("canon", "settled", "dominant"))
                                if head_ok or (ga and wa in ("canon", "settled", "dominant") and (tail_ok or (gb and wb in ("canon", "settled", "dominant")))):
                                    hit = k_
                                    stats["unit: whole gives way to parts"] += 1
                                    break
            if strict and hit > 1 and norm(toks[i]) in HEAD_FRAMES:   # the Bible: its curated units are the Book of Mormon's
                # THE FRAME OUTRANKS MEMORY AT THE UNIT'S HEAD. `ona malamalama`
                # is a curated unit, so the `ona … ai lea` frame was never asked;
                # a particle the grammar can read in this position opens its own
                # unit and the rest follows as before.
                prev_raw = toks[i - 1] if i else ""
                framed = SG.contextual_reading(
                    norm(toks[i]), norm(prev_raw), nxt_of(i + 1),
                    (i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                    [norm(t) for t in toks[max(0, i - 6):i]], [norm(t) for t in toks[i + 1:i + 7]])
                if framed:
                    hit, src = 1, "frame"
            # the negated modal outranks the memory's cut of these tokens
            for span_ in (4, 3, 2):
                if i + span_ <= len(toks) and norm(" ".join(toks[i:i + span_])) in MODAL_NEG:
                    hit, src = span_, "frame"
                    break
            key_sm = norm(" ".join(toks[i:i + hit]))
            if src == "absorbed" and key_sm not in inv:
                # the particle carries no English; the gloss belongs to
                # the word it attached to
                for back in range(1, hit):
                    tail = norm(" ".join(toks[i + back:i + hit]))
                    if tail in inv:
                        key_sm = tail
                        break
            # THE GRAMMAR FIRST. A rule states what a form reads as
            # everywhere; the inventory only remembers what it read as
            # somewhere. Where the grammar refuses -- the ambiguous
            # forms, where position decides -- the inventory and the
            # verse's English take over.
            term = SG.transliterated(key_sm) or term_of(key_sm)
            if term:
                if strict and not SG.transliterated(key_sm):
                    want_t = SG.tense_of_tam(prev_key) or unit_tense(key_sm) or clause_tense(toks, i)
                    if want_t:
                        term = ER.agree_tense(term, want_t, en_text)   # `ua maliu mai` -> came
                stats["unit: transliterated"] += 1
                prev_key = key_sm
                for j in range(i, i + hit - 1):
                    out[j]["en"] = CONT
                out[i + hit - 1]["en"] = term
                i += hit
                continue

            # A FORM WITH TWO REAL READINGS lets the verse choose;
            # only a form with one gets a fixed answer. `i latou` is
            # "them" 515 times and "they" 271, and the grammar has no
            # business picking for a verse it can see.
            if key_sm in MODAL_NEG:
                enl_ = (en_text or "").lower()
                gloss = next((alt for alt in ("cannot", "could not", "can not", "could never", "can never", "not able", "unable") if re.search(r"\b" + alt + r"\b", enl_)), "cannot")
                why = "grammar/modal-neg"
                prev_key = key_sm
                stats["unit: " + why] += 1
                trace.append((key_sm, gloss, why))
                for j in range(i, i + hit - 1):
                    out[j]["en"] = CONT
                out[i + hit - 1]["en"] = gloss
                i += hit
                continue
            if key_sm in NEG_UNITS:
                # THE NEGATIVES ARE FRAMES, never memory. `e lei X` is the past
                # negative: "not" (the verb carries the past: knew not, hath not
                # seen), "not yet" only where the verse says yet -- the memory
                # had `e lei` = "not yet" from 188 curated units and kept it
                # unconfirmed in every verse. `e leai (se mea)` is the
                # existential: "not any" / "none" / "no", as the verse has it.
                ew_ = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                alts = SG.contextual_reading(key_sm.split()[-1], None, None, False).split("|")
                gloss = next((alt for alt in alts if all(w in ew_ for w in alt.split())), alts[-1])
                why = "grammar/neg-past"
                prev_key = key_sm
                stats["unit: " + why] += 1
                trace.append((key_sm, gloss, why))
                for j in range(i, i + hit - 1):
                    out[j]["en"] = CONT
                out[i + hit - 1]["en"] = gloss
                i += hit
                continue

            if hit == 1 and key_sm in SG.ABSORBED and key_sm not in SG.AMBIGUOUS:
                # A BARE TENSE MARKER SAYS NO WORD OF ITS OWN. `sa`, `ua`, `te`
                # are absorbed into the verb; the memory still had `sa` = "and"
                # from verses where an "And" stood nearby, and John 1:1 printed
                # it. The frame alone decides (the copula before a locative:
                # `Sa i le amataga` "was"), and otherwise the marker is silent.
                prev_raw = toks[i - 1] if i else ""
                framed = SG.contextual_reading(
                    key_sm, norm(prev_raw), nxt_of(i + 1),
                    (i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                    [norm(t) for t in toks[max(0, i - 6):i]], [norm(t) for t in toks[i + 1:i + 7]])
                gloss = ""
                if framed:
                    ew_ = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                    for alt in framed.split("|"):
                        if all(in_english(w, ew_) for w in re.findall(r"[a-z']+", alt)):
                            gloss = alt
                            break
                why = "grammar/tam"
                prev_key = key_sm
                stats["unit: " + why] += 1
                trace.append((key_sm, gloss, why))
                if gloss:
                    out[i]["en"] = gloss
                i += hit
                continue

            # the token after this unit is a proper name in this verse: `ia
            # Iesu` is a preposition (Dunn: `ia` before names), never "him"
            name_next = (i + hit < len(toks) and not re.search(r"[.;:?!][”’\"')]*$", toks[i + hit - 1])
                         and looks_like_name(toks, i + hit, en_text, names))
            if len(SG.particle_readings(key_sm)) > 1 \
                    and key_sm not in SG.AMBIGUOUS:
                prev_raw = toks[i - 1] if i else ""
                gloss, why = choose_particle(
                    key_sm, en_text, inv, prev_key,
                    prev_tok=norm(prev_raw),
                    next_tok=nxt_of(i + hit),
                    clause_initial=(i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                        before=[norm(t) for t in toks[max(0, i - 6):i]], after=[norm(t) for t in toks[i + hit:i + hit + 6]],
                    next_is_name=name_next)
                why = "reading/" + why
                if not gloss and strict and key_sm in SUBJ_PRON:
                    # THE EMPHATIC PRONOUN SAYS ITSELF even where the English
                    # drops it (`sa mau foi o ia ma i tatou` "dwelt among us")
                    gloss, why = SUBJ_PRON[key_sm], "grammar/pronoun"
                stats["unit: " + why] += 1
                trace.append((key_sm, gloss, why))
                prev_key = key_sm
                if gloss:
                    gloss = modernise(align_number(gloss, en_text))
                    for j in range(i, i + hit - 1):
                        out[j]["en"] = CONT
                    out[i + hit - 1]["en"] = gloss
                i += hit
                continue

            gloss = SG.primary_gloss(key_sm)
            if gloss and (hit == 1 or key_sm in SG.MULTI_CONTEXTUAL):
                # the frame outranks the fixed reading: `le po` is the night,
                # not the particle "or"; `Ia` at a clause start is "let"; the
                # listed multi-token forms too (`o lea` before a noun is
                # "that", not "therefore"), and only a spoken reading counts
                prev_raw = toks[i - 1] if i else ""
                framed = SG.contextual_reading(
                    key_sm, norm(prev_raw), nxt_of(i + hit),
                    (i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                    [norm(t) for t in toks[max(0, i - 6):i]], [norm(t) for t in toks[i + hit:i + hit + 6]])
                if framed:
                    ew_ = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                    for alt in framed.split("|"):
                        if all(in_english(w, ew_) for w in re.findall(r"[a-z']+", alt)):
                            gloss = alt
                            break
                elif framed == "" and hit == 1:
                    gloss = ""
            if gloss:
                # A rule says what a form reads as EVERYWHERE, and the
                # verse still gets a say at the edges: `faatasi` was
                # "together with" in a verse reading "listen together"
                # because the grammar's answer went straight to the
                # page, skipping the finishing every other path gets.
                gloss = trim_absent_tail(gloss, en_text)
                why = "grammar/" + src
            elif key_sm in SG.AMBIGUOUS:
                prev_raw = toks[i - 1] if i else ""
                gloss, why = choose_particle(
                    key_sm, en_text, inv, prev_key,
                    prev_tok=norm(prev_raw),
                    next_tok=nxt_of(i + hit),
                    clause_initial=(i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                    before=[norm(t) for t in toks[max(0, i - 6):i]], after=[norm(t) for t in toks[i + hit:i + hit + 6]],
                    next_is_name=name_next)
                why = why + "/" + src
            elif False:
                # THE ONE-VOWEL RADICALS. `o`, `e`, `a`, `i`, `le`,
                # `ma` each carry several grammatical jobs and the form
                # cannot tell you which -- the same problem lamed, yod,
                # he and mem pose in Hebrew. The inventory will happily
                # answer anyway, because somewhere in 111,683 units a
                # bare `o` was read as almost every English word, and
                # then whichever reading the verse happens to contain
                # wins. That is not evidence, it is drift: Alma 32:21
                # came out `o`="as" three times and `le`="the
                # knowledge" twice.
                #
                # These are glossed by POSITION or not at all.
                gloss, why = "", "ambiguous/" + src
            elif hit == 1 and key_sm in inv and looks_like_name(toks, i, en_text, names) \
                    and not inv[key_sm].most_common(1)[0][0][:1].isupper():
                # A NAME NEVER TAKES A COMMON WORD'S MEMORY. `Elia` (Elias, John
                # 1:21) is not `elia` "digged"; the name stays blank here and the
                # verse's leftover English name pairs with it below.
                gloss, why = "", "name/no-memory"
            elif key_sm in inv:
                # the unit's own marker first (`na talia` is past whatever stands
                # before it), then the marker in front, then the narrative frame;
                # after the purposive / optative the verb is bare
                gloss, why = choose(inv[key_sm], en_text,
                                    ("BASE" if prev_key in BARE_AFTER else None)
                                    or unit_tense(key_sm)
                                    or SG.tense_of_tam(prev_key)
                                    or ("PAST" if seq_verb else None), strict, spent=_spent_before(out, i))
                why = why + "/" + src
                # THE GRAMMAR'S READING OUTRANKS A REMEMBERED ONE THE VERSE DOES NOT
                # CARRY: `tetele` (the plural of `tele`) was "mighty" in one curated
                # verse and 2 Nephi 1:12 says "great visitations" -- the form's own
                # reading set (its base's, for a reduplicated plural) has "great"
                if hit == 1 and why.startswith(("settled", "dominant")) and gloss and vetoed(gloss, en_text):
                    ew_ = content_words(en_text)
                    for base_ in [key_sm] + _dereduplicate(key_sm):
                        alt_ = next((r for r in SG.particle_readings(base_) if r and all(in_english(w, ew_) for w in r.split())), None)
                        if alt_:
                            gloss, why = alt_, "grammar/reading-over-settled"
                            break
            elif key_sm in lex:
                gloss, why = choose(lex[key_sm], en_text, strict=strict)
                why = why + "/lex"

            else:
                gloss, why = "", "no-gloss/" + src
            # BACK OFF TO THE CONTENT WORD. A remembered reading of a
            # whole phrase is rejected when the verse does not carry
            # all of it -- `o ona fofoga` is "of his eyes," somewhere
            # in the Book of Mormon and D&C 1:1 says "whose eyes",
            # so the "his" sank the whole unit and `fofoga` printed
            # nothing. The unit's one open-class word still has a
            # reading, and the verse still decides which: this can
            # only ever produce a word the verse actually has.
            # THE VERSE IS A GUIDE, NOT A GAG. `tusia` is "write"
            # and 1 Nephi 1:3 reads "I make it with mine own hand" --
            # the English chose another word, and the Samoan still
            # says write. Where a lone open-class token would be left
            # BLANK and its lexicon is overwhelmingly one reading,
            # that reading is written. Nothing is invented: the word
            # comes from the curation, and a token with a divided
            # lexicon still says nothing.
            # THE DICTIONARY, last. Everything above is evidence from
            # this corpus; this is the two lexicons, and it speaks only
            # where the corpus has nothing to say. The verse still has
            # to carry the sense, so a dictionary entry that does not
            # fit the verse is not written.
            name_blocked = (why == "name/no-memory")
            # A UNIT MADE ONLY OF PARTICLES has no word of its own to fall back
            # on: `ua na` kept "there are" and `sa` "the Lamanites" unconfirmed
            # (John 1:18, 1:19). Its reading must be one the verse carries.
            particle_unit = all(t in SG.CLOSED_CLASS or t in SG.AMBIGUOUS or t in SG.TAM
                                or t in SG.PRONOUNS for t in key_sm.split())
            provisional = None
            if gloss and why.split("/")[0].endswith("-unconfirmed"):
                provisional = (gloss, why)
                gloss = ""
            dict_word = key_sm if hit == 1 else None
            if hit > 1:
                # a unit of particles around ONE content word -- `na fegaoioiai
                # foi`, `i le fogatai` -- is looked up by that word
                opens_ = [t for t in key_sm.split()
                          if t not in SG.CLOSED_CLASS and t not in SG.AMBIGUOUS and t not in SG.TAM]
                if len(opens_) == 1:
                    dict_word = opens_[0]
            if not gloss and not name_blocked and dict_word and dict_word not in SG.CLOSED_CLASS \
                    and dict_word not in SG.AMBIGUOUS:
                ew = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                # A dictionary sense is often several alternatives in
                # one string -- Pratt writes `maua` as "get, to obtain,
                # to acquire" -- and the verse will carry one of them,
                # not all three. Each alternative is tried on its own.
                # the grammar's own derivations are senses too: `faalua` twice,
                # `toalua` two (persons), `taitasi` each (Dunn, unit eight)
                senses_ = list(SG.dictionary(dict_word))
                nd_ = SG.numeral_derived(dict_word)
                if nd_:
                    senses_.append(nd_)
                for sense in senses_:
                    for alt in re.split(r"[,;]", sense):
                        alt = re.sub(r"^\s*to\s+", "", alt).strip()
                        words = [w for w in re.findall(r"[a-z']+", alt)
                                 if w not in FUNCTION_ONLY]
                        if words and all(in_english(w, ew) for w in words):
                            gloss, why = alt, "dictionary/" + src
                            break
                    if gloss:
                        break

            if not gloss and not name_blocked:
                opens = [t for t in key_sm.split()
                         if t not in SG.CLOSED_CLASS
                         and t not in SG.AMBIGUOUS and t in lex]
                if len(opens) == 1:
                    hit_g = dominant_lemma(lex[opens[0]])
                    if hit_g:
                        gloss, why = hit_g, "lexicon/" + src

            if not gloss and not name_blocked:
                open_toks = [t for t in key_sm.split()
                             if t not in SG.CLOSED_CLASS
                             and t not in SG.AMBIGUOUS]
                if len(open_toks) == 1 and open_toks[0] in lex:
                    d = lex[open_toks[0]]
                    back, bwhy = choose(d, en_text, strict=strict)
                    # A COMMON WORD'S RARE READING needs more than one
                    # verse happening to contain it. `mea` is "thing"
                    # 1,714 times and was read "own" off 3 witnesses,
                    # because the verse said "own" somewhere in it.
                    total = sum(d.values())
                    share = d.get(back, 0) / total if total else 0
                    if back and not (total >= 500 and share < 0.01):
                        if bwhy.endswith("-unconfirmed"):
                            provisional = provisional or (back, bwhy + "/backoff")
                        else:
                            gloss, why = back, bwhy + "/backoff"
            # UNDER AN EXPLICIT TENSE MARKER, A VERB SAYS ITS WORD. `Na faia e le
            # Atua` reads "created" in the KJV, and the curation has faia only as
            # made / wrought / did / done, so every reading was vetoed and the verb
            # printed nothing while its past marker fired for nothing. The marker's
            # tense is a grammar fact; the verb's plurality reading in that tense is
            # the curation's own word for it. Nothing is invented: the word comes
            # from the curation and the tense from the marker -- the verse only
            # failed to confirm which English word, not that the verb was there.
            if not gloss and strict and not name_blocked and dict_word and dict_word not in SG.CLOSED_CLASS \
                    and dict_word not in SG.AMBIGUOUS and dict_word not in SG.TAM:
                # THE FORM TAKEN APART: prefix, root, suffix (faamalamalamaina).
                # Freely for a form the lexicons do not hold at all; for a form
                # they hold but whose senses the verse did not confirm, only the
                # verse's own inflection of a part counts (`faamalamalamaina` ->
                # the KJV's "lighteth"), never a composed guess -- `manuia` is a
                # word (blessing), not manu + ia, and came out "beasts"
                known = bool(SG.dictionary(dict_word)) or dict_word in lex
                want_m = None if prev_key in BARE_AFTER else (unit_tense(key_sm) or SG.tense_of_tam(prev_key) or clause_tense(toks, i))
                mg = morph_gloss(dict_word, en_text, lex, want_m, verse_only=known)
                if mg:
                    gloss, why = mg, "morphology/" + src
            if not gloss and not name_blocked and hit <= 2:
                want = None if prev_key in BARE_AFTER else (unit_tense(key_sm) or SG.tense_of_tam(prev_key) or ("PAST" if seq_verb else None))
                opens = [t for t in key_sm.split()
                         if t not in SG.CLOSED_CLASS and t not in SG.AMBIGUOUS]
                if want and len(opens) == 1 and (key_sm in inv or opens[0] in lex):
                    d = inv.get(key_sm) or lex[opens[0]]
                    tensed = [(n, g) for g, n in merge_punctuation(d).items()
                              if ER.tense_of(g) == want and len(g.split()) <= 2
                              and not any(w in ("which", "who", "that", "there")
                                          for w in g.lower().split())]
                    if tensed:
                        tensed.sort(reverse=True)
                        gloss, why = tensed[0][1], "tensed-plurality/" + src
            if not gloss and not name_blocked and strict and hit == 1 and key_sm in lex \
                    and key_sm not in SG.CLOSED_CLASS and key_sm not in SG.AMBIGUOUS:
                # THE WORD'S USUAL ENGLISH, in the Bible only. `tagata` is people
                # 591 times, men 329, man 262 in the curation; where the KJV
                # says "inhabitants" nothing confirms any of them and the word
                # printed nothing 1,182 times. A strongly attested word says its
                # plurality reading -- the Samoan still says tagata -- and the
                # reader sees the word rather than a hole.
                d = merge_punctuation(lex[key_sm])
                top, n = d.most_common(1)[0]
                total = sum(d.values())
                verb_position = prev_key in SG.TAM or prev_key == "ia" or seq_verb
                if total >= 20 and n / total >= 0.30 and len(top.split()) <= 2 and not verb_position:
                    gloss, why = top, "plurality/lex"
            if not gloss and provisional and not particle_unit:
                # the curation's word stands where no verse-confirmed sense
                # replaced it: `gaogao` "empty" beside the KJV's "void"
                gloss, why = provisional[0], provisional[1].replace("-unconfirmed", "-kept")
            if not gloss and strict and key_sm in SUBJ_PRON:
                # THE EMPHATIC PRONOUN SAYS ITSELF even where the English drops
                # it (`sa mau foi o ia ma i tatou` "dwelt among us" -- the Samoan
                # says "he"); the sentence pass decides subject or object
                gloss, why = SUBJ_PRON[key_sm], "grammar/pronoun"
            if not gloss and strict and key_sm.endswith(" uma") and key_sm[:-4] in SUBJ_PRON:
                # `o i latou uma` "they all" -- the quantifier on the pronoun
                gloss, why = SUBJ_PRON[key_sm[:-4]] + " all", "grammar/pronoun"
            is_open = key_sm not in SG.CLOSED_CLASS and key_sm not in SG.AMBIGUOUS and key_sm not in SG.TAM
            if key_sm == "ona" and "frame" in why:
                seq_frame = True; seq_verb = True
            elif key_sm == "lea" and seq_frame:
                seq_frame = False; seq_verb = False
            elif strict and gloss and gloss != CONT and is_open and len(gloss.split()) <= 2 \
                    and not gloss.lower().startswith(("there ", "let ")):
                # THE COPULA RIDES WITH THE WORD, by frame. In the sequential
                # frame the stative is "there was light"; after the optative
                # `Ia` it is "there be light" (the `Ia` already says "let").
                # Elsewhere only a plain "there is/are X" in the verse.
                lower = (en_text or "").lower(); g = re.escape(gloss.lower())
                if seq_verb:
                    m = re.search(r"\b(there (?:was|were)) " + g + r"\b", lower)
                elif prev_key == "ia":
                    m = re.search(r"\blet (there be) " + g + r"\b", lower)
                else:
                    m = re.search(r"\b(there (?:is|are)) " + g + r"\b", lower)
                if m:
                    gloss = f"{m.group(1)} {gloss}"
            want_t = None
            # a unit headed by a preposition or a determiner is a NOUN PHRASE:
            # the marker's tense is not written on it (`i lea lava malamalama`
            # "of that light", never "lit")
            noun_phrase = (prev_key.split() or [""])[-1] in ("le", "se", "lea", "lenei", "lena", "lo", "la", "ni", "lava", "lona", "lana", "ona", "ana") \
                or (key_sm.split() or [""])[0] in ("i", "ia", "iā", "o", "a", "mai", "mo", "le", "se", "lea", "lenei", "lena", "lo", "la", "ni", "ona", "lona", "lana", "lou", "lau", "lo’u", "la’u", "loʻu", "laʻu")
            if gloss and gloss != CONT and is_open and not noun_phrase:
                # THE MARKER'S TENSE IS WRITTEN ON THE VERB, in the verse's own
                # form: the unit's marker, the marker in front of it, the
                # narrative frame, the past negative `e lei`, or the last marker
                # of this clause (`sa aʻu fai atu`: the pronoun sits between).
                want_t = (unit_tense(key_sm) or SG.tense_of_tam(prev_key)
                          or ("PAST" if seq_verb else None)
                          or ("PAST" if prev_key.split()[-1:] and prev_key.split()[-1] in ("lei", "le’i", "leʻi") else None)
                          or clause_tense(toks, i))
                # AFTER THE PURPOSIVE OR THE OPTATIVE THE VERB IS BARE (Dunn: `ina
                # ia` "in order to", `ia` "let / imperative", `sei` "let"): "to
                # witness", "let there be" -- the clause's past does not reach it
                if prev_key in BARE_AFTER:
                    want_t = None
                if want_t:
                    agreed = ER.agree_tense(gloss, want_t, en_text)
                    if agreed != gloss:
                        gloss = agreed
                        stats["unit: tense-agreed"] += 1
            if is_open and gloss and gloss != CONT:
                seq_verb = False
            prev_key = key_sm
            stats["unit: " + why] += 1
            trace.append((key_sm, gloss, why + (f" [{want_t}]" if want_t else "")))
            if gloss:
                gloss = modernise(align_number(gloss, en_text))
                gloss = capitalise_names(gloss, key_sm, names)
                # a remembered IMPERATIVE keeps a capital ("Go") that belongs to a
                # sentence start; mid-sentence an ordinary word is lowercase
                fw = gloss.split()[0]
                if i > 0 and fw[:1].isupper() and not re.search(r"[.?!:][”’\"')]*$", toks[i - 1]) \
                        and fw.rstrip(",;.").lower() not in english_names() and fw.rstrip(",;.") not in ("God", "Lord", "Christ", "Father", "Son", "Spirit", "Holy", "Ghost", "Word", "Lamb", "Almighty", "Redeemer", "Savior", "Saviour", "Messiah", "Jehovah", "I", "O") \
                        and fw.rstrip(",;.").lower() in english_vocabulary():
                    gloss = fw[:1].lower() + gloss[1:]
                for j in range(i, i + hit - 1):
                    out[j]["en"] = CONT
                out[i + hit - 1]["en"] = gloss
            i += hit
        # THE GLOSS'S PUNCTUATION IS THE TOKEN'S: a remembered "return." under
        # `ai;` says "return;", "Awake," under `ia!` says "Awake!" -- the mark
        # belongs to the verse being glossed, not to the verse the memory came from
        for w in out:
            g = w["en"]
            if not g or g == CONT:
                continue
            m = re.search(r"([,;:.!?]+)[”’\"')]*$", w["sm"])
            core = g.rstrip(" ,;:.!?")
            if core and m:
                w["en"] = core + m.group(1)
            elif core and not m and re.search(r"[,;:.!?]$", g):
                w["en"] = core
        attach_particles(out, toks)
        if not inner:
            # THE GRAMMAR IS THE LANGUAGE'S, not one volume's (user, 2026-09-05:
            # "the entire corpus even the BOM"): the sentence pass runs on every
            # volume; the curated units were consulted first and still stand
            # where a rule has nothing to say
            simple_sentences(out, toks, en_text)
        if a.debug and DEBUG["key"] in a.debug.split(",") and not inner:
            print(f"--- {a.debug}: {en_text}")
            for u, g, w in trace:
                print(f"    {u!r:32} {g!r:28} {w}")
        if inner:
            return out
        # THE LAST WORD PAIRS ITSELF. When exactly one open-class token of the
        # verse is still blank and exactly one content word of the verse's
        # English is carried by no gloss, they are each other's: a verse is a
        # closed system, and one Samoan word left over against one English word
        # left over is an alignment the verse itself makes. `Sa soona nunumi le
        # lalolagi` -- nunumi occurs once in the whole corpus, and "form" is the
        # one word of Genesis 1:2 nothing else accounts for. Names pair the same
        # way (Samita / Smith) when they are the verse's only leftovers.
        blanks = [j for j, w in enumerate(out)
                  if not w["en"] and len(norm(w["sm"])) >= 3
                  and norm(w["sm"]) not in SG.CLOSED_CLASS and norm(w["sm"]) not in SG.AMBIGUOUS
                  and norm(w["sm"]) not in SG.TAM and norm(w["sm"]) not in SG.PRONOUNS]
        if len(blanks) == 1:
            said = set()
            for w in out:
                if w["en"] and w["en"] != CONT:
                    for x in re.findall(r"[a-z']+", w["en"].lower()):
                        said.add(x); said |= _stems(x)
            left = []
            left_pos = []
            en_words_ = re.findall(r"[A-Za-z][a-z']+", en_text or "")
            for k_, x in enumerate(en_words_):
                lx = x.lower()
                if lx in FUNCTION_ONLY or lx in LEFTOVER_STOP or len(lx) < 3: continue
                if lx in said or (_stems(lx) & said): continue
                if x not in left: left.append(x); left_pos.append(k_)
            if len(left) == 1:
                out[blanks[0]]["en"] = left[0] if left[0][0].isupper() and norm(out[blanks[0]]["sm"]) in names else left[0].lower()
                stats["unit: leftover-pair"] += 1
            elif strict and len(left) > 1:
                # ONE BLANK, SEVERAL LEFTOVERS (the Bible): the leftover nearest
                # the blank's place in the verse, when one is clearly nearest --
                # `matamata` against "beheld" in John 1:14. A word the
                # dictionaries know pairs only with a leftover that is a sense
                # of it or a near-synonym of one (behold / look); `manuia`
                # "blessing" is not paired with "sons" because it stood nearest.
                pos = blanks[0] / max(1, len(out))
                bw = norm(out[blanks[0]]["sm"])
                sense_words = set()
                for s in SG.dictionary(bw):
                    for x in re.findall(r"[a-z']+", s.lower()):
                        if x not in FUNCTION_ONLY:
                            sense_words.add(x); sense_words |= _stems(x)
                def fits(x):
                    if not sense_words:
                        return True
                    lx = x.lower()
                    return bool((_stems(lx) | {lx} | ER.SYNONYMS.get(lx, set())) & sense_words)
                cands = sorted((abs(k_ / max(1, len(en_words_)) - pos), k_, x) for k_, x in zip(left_pos, left) if fits(x))
                if cands and cands[0][0] <= 0.10 and (len(cands) == 1 or cands[1][0] - cands[0][0] >= 0.12):
                    x = cands[0][2]
                    out[blanks[0]]["en"] = x if x[0].isupper() and norm(out[blanks[0]]["sm"]) in names else x.lower()
                    stats["unit: leftover-nearest"] += 1
        elif strict and 2 <= len(blanks) <= 4:
            # THE DUAL DECIDES THE REST. In the Bible, the verse's leftover
            # English words are laid against its leftover Samoan words by
            # position: the same number in the same order pairs one to one,
            # and otherwise a blank takes the leftover nearest to its place in
            # the verse, when one is clearly nearest. The English column is the
            # translation of this very verse, so a word it has and the gloss
            # line lacks belongs to a Samoan word that lacks a gloss.
            said = set()
            for w in out:
                if w["en"] and w["en"] != CONT:
                    for x in re.findall(r"[a-z']+", w["en"].lower()):
                        said.add(x); said |= _stems(x)
            en_words = re.findall(r"[A-Za-z][a-z']+", en_text or "")
            left = [(k, x) for k, x in enumerate(en_words)
                    if x.lower() not in FUNCTION_ONLY and x.lower() not in LEFTOVER_STOP and len(x) >= 3
                    and x.lower() not in said and not (_stems(x.lower()) & said)]
            seen = set(); left = [(k, x) for k, x in left if not (x.lower() in seen or seen.add(x.lower()))]
            if left:
                def put(j, x):
                    out[j]["en"] = x if x[0].isupper() and norm(out[j]["sm"]) in names else x.lower()
                if len(left) == len(blanks):
                    for j, (k, x) in zip(blanks, left): put(j, x)
                    stats["unit: leftover-aligned"] += len(blanks)
                else:
                    ne, ns = max(1, len(en_words)), max(1, len(out))
                    taken = set()
                    for j in blanks:
                        pos = j / ns
                        cands = sorted(((abs(k / ne - pos), k, x) for k, x in left if k not in taken))
                        if cands and cands[0][0] <= 0.2 and (len(cands) == 1 or cands[1][0] - cands[0][0] >= 0.12):
                            _, k, x = cands[0]; taken.add(k); put(j, x)
                            stats["unit: leftover-nearest"] += 1
        return out

    if a.all:
        # ALL FIVE VOLUMES, one tool (user, 2026-09-05: "the tool should include
        # all 5... OT, NT, BOM, DC, PGP"): the three restoration volumes first,
        # then the Bible pass, each written where its readers look for it
        import subprocess
        here = str(Path(__file__).resolve())
        rc = subprocess.call([sys.executable, here] + (["--dry-run"] if a.dry_run else []))
        if rc:
            return rc
        return subprocess.call([sys.executable, here, "--bible"] + (["--dry-run"] if a.dry_run else []))

    if a.bible:
        if bible_index is None:
            print("no tusi_paia_index.json in Resources"); return 1
        bible_english = json.loads((RES / "tusi_paia_english.json").read_text(encoding="utf-8"))
        hand_path = RES / "tusi_paia_hand.json"
        hand_bible = json.loads(hand_path.read_text(encoding="utf-8"))["verses"] if hand_path.exists() else {}
        dual_dir = HERE.parent / "corpus" / "tusi_paia" / "dual"
        by_id = {b["id"]: b for b in bible_books}
        grand_tok = grand_gl = 0
        for meta in bible_index["books"]:
            if a.book and meta["id"] != a.book:
                continue
            book = by_id.get(meta["id"])
            if book is None:
                continue
            ntok = ngl = 0
            for ch in book["chapters"]:
                for verse in ch["verses"]:
                    hkey = f"{meta['id']}|{ch['num']}|{verse['num']}"
                    if hkey in hand_bible:
                        # HAND-CURATED: the Samoan and its glosses are the
                        # user's, verse by verse (tusi_paia_hand.json)
                        verse["words"] = [{"sm": w["sm"], "en": w["en"]} for w in hand_bible[hkey]["words"]]
                        ntok += len(verse["words"]); ngl += sum(1 for w in verse["words"] if (w["en"] or "").strip())
                        stats["verse: hand-curated (Bible)"] += 1
                        continue
                    toks = [w["sm"] for w in verse["words"]]
                    MODE["bible"] = True
                    SG.REGISTER["bible"] = True
                    en_text = (bible_english.get(
                        f"{meta['nameEn']}|{ch['num']}|{verse['num']}", ""))
                    DEBUG["key"] = hkey
                    MODE["bible"] = True
                    RAW_EN["text"] = bible_english.get(f"{meta['nameEn']}|{ch['num']}|{verse['num']}", "")
                    out = gloss_tokens(toks, en_text, strict=True)
                    verse["words"] = out
                    ntok += len(out)
                    ngl += sum(1 for w in out if (w["en"] or "").strip())
            grand_tok += ntok; grand_gl += ngl
            print(f"  {meta['nameEn']:18} {ngl:7}/{ntok:<7} {100 * ngl / max(1, ntok):5.1f}% carrying text")
            if not a.dry_run:
                blob = json.dumps(book, ensure_ascii=False, separators=(",", ":"))
                (RES / f"book_{meta['id']}.json").write_text(blob, encoding="utf-8")   # the dual dir keeps the token master
        print(f"O le Tusi Paia: {grand_gl} of {grand_tok} tokens carrying text ({100 * grand_gl / max(1, grand_tok):.1f}%)")
        for k, n in stats.most_common(60):
            print(f"   {k:24} {n}")
        return 0

    for book in books:
        if book.get("volume") not in ("bom", "dc", "pgp"):
            continue
        for ch in book["chapters"]:
            for verse in ch["verses"]:
                key = f"{book['id']}|{ch['num']}|{verse['num']}"
                if key in hand:
                    stats["left: hand-curated"] += 1
                    continue
                toks = [w["sm"] for w in verse["words"]]
                # MATCH MODERN AGAINST MODERN. The glosses are modern English
                # now and the canon is KJV-register, so every test that asks
                # whether the verse carries a gloss word was comparing across
                # registers: "to" stopped matching "unto", 3,652 times. The
                # published English is untouched -- this is a comparison copy,
                # and nothing written to the page comes from it.
                en_text = modernise(english.get(
                    f"{book['nameEn']}|{ch['num']}|{verse['num']}", ""))
                DEBUG["key"] = key          # so --debug 2nephi|1|1 traces this volume too
                out = gloss_tokens(toks, en_text)
                ov["verses"][key] = out
                already.add(key)
                made += 1
                if a.limit and made >= a.limit:
                    break
            if a.limit and made >= a.limit:
                break
        if a.limit and made >= a.limit:
            break

    ov["generated"] = sorted(already)
    glossed = sum(1 for k in already
                  for w in ov["verses"][k] if (w["en"] or "").strip())
    tokens = sum(len(ov["verses"][k]) for k in already)
    print(f"verses generated      {made}")
    print(f"tokens carrying text  {glossed} of {tokens} "
          f"({100 * glossed / tokens:.1f}%)")
    for k, n in stats.most_common():
        print(f"   {k:24} {n}")
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    (RES / "bom_overrides.json").write_text(
        json.dumps(ov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {RES / 'bom_overrides.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
