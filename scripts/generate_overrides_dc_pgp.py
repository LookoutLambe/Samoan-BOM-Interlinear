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

    python3 generate_overrides_dc_pgp.py [--dry-run] [--limit N]
"""

from __future__ import annotations

import argparse
import difflib
import json
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
modernise = ER.modernise
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


VOCAB_MAXLEN = max(max(len(k.split()) for k in SG.VOCABULARY),
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

    # 0. A REGISTERED TERM OR IDIOM IS ITS OWN UNIT, BEFORE MEMORY. `i le ua
    #    faapea lava` is "and it was so"; the inventory knows `i le ua` (on the
    #    neck) and would take it first. A transliterated term likewise, even
    #    where nothing in the curation ever glossed it -- `sume` and `eseroma`
    #    head no unit in the Book of Mormon. Longest span first, up to the
    #    longest registered key.
    for span in range(min(VOCAB_MAXLEN, len(toks) - i), 0, -1):
        if SG.transliterated(n(i, i + span)) or SG.vocabulary(n(i, i + span)):
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

    def legal(span):
        key = n(i, i + span)
        if joins_two_clauses(i, i + span) or crosses_a_stop(i, i + span) or ends_on_frame_close(i, i + span):
            return False
        # `o` heads the phrase that follows it, so no unit ends on one
        return (not SG.ends_mid_phrase(key)
                and not cuts_a_construction(i, i + span)
                and not eats_a_name(i, i + span))

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
    while (len(parts) > 1 and absent(parts[0])
           and re.sub(r"[^a-z']", "", parts[0].lower()) in HEAD_TRIMMABLE):
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
                for w in re.findall(r"[A-Za-z][a-z']+", v):
                    (up if w[0].isupper() else low)[w.lower()] += 1
        _EN_NAMES = {w for w, n in up.items() if n >= 2 and low.get(w, 0) == 0}
    return _EN_NAMES


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
                    clause_initial: bool = False, before=(), after=()) -> tuple[str, str]:
    """Gloss a one-vowel particle from its CLOSED set of readings.

    choose() cannot do this job: every reading of a particle is a function
    word, so its content-word gate empties and it falls through to whichever
    reading the curation's segmentation parked on this token most often. Here
    the candidates are fixed by the grammar and the VERSE picks among them --
    frequency is only a tie-break, and a reading the verse does not contain is
    used only when the grammar has just one.
    """
    readings = SG.readings_in_frame(form, prev_tok) or SG.particle_readings(form)
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
            if in_english(alt, ew):
                return alt, "frame"
    if framed and form in FRAME_OR_SILENT:
        # the frame identified the construction; the verse has no word for
        # the marker, so the marker says nothing rather than a stray reading
        return "", "silent-by-frame"
    def carried(reading):
        # a reading of more than one word is present only if ALL of it is --
        # "to him" must not win on the "to" alone
        return all(in_english(w, ew) for w in reading.split())

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
              "aʻe", "ane", "pea", "lea"}


# English words that are never a leftover's partner: auxiliaries, the light
# verbs, and the copulas the Samoan says with a particle or not at all.
LEFTOVER_STOP = {"be", "been", "being", "is", "are", "was", "were", "am", "do", "does", "did",
                 "done", "have", "has", "had", "hath", "hast", "shall", "will", "would", "should",
                 "may", "might", "can", "could", "let", "said", "saith", "say", "says", "came",
                 "come", "went", "pass", "unto", "thereof", "therein", "thereto", "also", "even",
                 "yea", "behold", "now", "then", "there", "thus", "very", "own", "same"}


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
            if j >= 1 and glossed(j - 1):
                out[j]["en"] = out[j - 1]["en"]
                out[j - 1]["en"] = CONT
        else:
            k = j + 1
            while k < n and not out[k]["en"]:
                k += 1
            if k < n and out[k]["en"]:
                out[j]["en"] = CONT


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


def choose(cands: Counter, english: str, want_tense: str | None = None,
           strict: bool = False) -> tuple[str, str]:
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
        agrees = 1 if (want_tense and ER.tense_of(gloss) == want_tense) else 0
        scored.append((present / max(1, present + absent), neg, agrees, n, gloss))
    if scored:
        scored.sort(reverse=True)
        # trim on this path too: the scoring picks the best of what the
        # inventory offers, and the best may still carry a word the verse does
        # not have, when every candidate does
        return trim_absent_tail(scored[0][-1], english), "canon"
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
    if (RES / "tusi_paia_index.json").exists():
        bible_index = json.loads((RES / "tusi_paia_index.json").read_text(encoding="utf-8"))
        for meta in bible_index["books"]:
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
                if verb:
                    m = re.search(r"\b(there (?:was|were)) " + re.escape(verb.lower()) + r"\b", (en_text or "").lower())
                    if m and not verb.lower().startswith("there "):
                        verb = f"{m.group(1)} {verb}"
                    lead = next((alt for alt in ("then", "and") if in_english(alt, ew_)), "")
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
            term = SG.transliterated(key_sm) or SG.vocabulary(key_sm)
            if term:
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
            if len(SG.particle_readings(key_sm)) > 1 \
                    and key_sm not in SG.AMBIGUOUS:
                prev_raw = toks[i - 1] if i else ""
                gloss, why = choose_particle(
                    key_sm, en_text, inv, prev_key,
                    prev_tok=norm(prev_raw),
                    next_tok=nxt_of(i + hit),
                    clause_initial=(i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                        before=[norm(t) for t in toks[max(0, i - 6):i]], after=[norm(t) for t in toks[i + hit:i + hit + 6]])
                why = "reading/" + why
                stats["unit: " + why] += 1
                prev_key = key_sm
                if gloss:
                    gloss = modernise(align_number(gloss, en_text))
                    for j in range(i, i + hit - 1):
                        out[j]["en"] = CONT
                    out[i + hit - 1]["en"] = gloss
                i += hit
                continue

            gloss = SG.primary_gloss(key_sm)
            if gloss and hit == 1:
                # the frame outranks the fixed reading: `le po` is the night,
                # not the particle "or"; `Ia` at a clause start is "let"
                prev_raw = toks[i - 1] if i else ""
                framed = SG.contextual_reading(
                    key_sm, norm(prev_raw), nxt_of(i + 1),
                    (i == 0 or prev_raw[-1:] in SG.CLAUSE_END),
                    [norm(t) for t in toks[max(0, i - 6):i]], [norm(t) for t in toks[i + 1:i + 7]])
                if framed:
                    ew_ = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                    for alt in framed.split("|"):
                        if in_english(alt, ew_):
                            gloss = alt
                            break
                elif framed == "":
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
                    before=[norm(t) for t in toks[max(0, i - 6):i]], after=[norm(t) for t in toks[i + hit:i + hit + 6]])
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
            elif key_sm in inv:
                gloss, why = choose(inv[key_sm], en_text,
                                    SG.tense_of_tam(prev_key)
                                    or unit_tense(key_sm)
                                    or ("PAST" if seq_verb else None), strict)
                why = why + "/" + src
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
            if not gloss and dict_word and dict_word not in SG.CLOSED_CLASS \
                    and dict_word not in SG.AMBIGUOUS:
                ew = set(re.findall(r"[a-z']+", (en_text or "").lower()))
                # A dictionary sense is often several alternatives in
                # one string -- Pratt writes `maua` as "get, to obtain,
                # to acquire" -- and the verse will carry one of them,
                # not all three. Each alternative is tried on its own.
                for sense in SG.dictionary(dict_word):
                    for alt in re.split(r"[,;]", sense):
                        alt = re.sub(r"^\s*to\s+", "", alt).strip()
                        words = [w for w in re.findall(r"[a-z']+", alt)
                                 if w not in FUNCTION_ONLY]
                        if words and all(in_english(w, ew) for w in words):
                            gloss, why = alt, "dictionary/" + src
                            break
                    if gloss:
                        break

            if not gloss:
                opens = [t for t in key_sm.split()
                         if t not in SG.CLOSED_CLASS
                         and t not in SG.AMBIGUOUS and t in lex]
                if len(opens) == 1:
                    hit_g = dominant_lemma(lex[opens[0]])
                    if hit_g:
                        gloss, why = hit_g, "lexicon/" + src

            if not gloss:
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
            if not gloss and hit <= 2:
                want = SG.tense_of_tam(prev_key) or unit_tense(key_sm) or ("PAST" if seq_verb else None)
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
            if not gloss and strict and hit == 1 and key_sm in lex \
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
            if not gloss and provisional:
                # the curation's word stands where no verse-confirmed sense
                # replaced it: `gaogao` "empty" beside the KJV's "void"
                gloss, why = provisional[0], provisional[1].replace("-unconfirmed", "-kept")
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
            if is_open and gloss and gloss != CONT:
                seq_verb = False
            prev_key = key_sm
            stats["unit: " + why] += 1
            if gloss:
                gloss = modernise(align_number(gloss, en_text))
                gloss = capitalise_names(gloss, key_sm, names)
                for j in range(i, i + hit - 1):
                    out[j]["en"] = CONT
                out[i + hit - 1]["en"] = gloss
            i += hit
        attach_particles(out, toks)
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
            for x in re.findall(r"[A-Za-z][a-z']+", en_text or ""):
                lx = x.lower()
                if lx in FUNCTION_ONLY or lx in LEFTOVER_STOP or len(lx) < 3: continue
                if lx in said or (_stems(lx) & said): continue
                if x not in left: left.append(x)
            if len(left) == 1:
                out[blanks[0]]["en"] = left[0] if left[0][0].isupper() and norm(out[blanks[0]]["sm"]) in names else left[0].lower()
                stats["unit: leftover-pair"] += 1
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
                    en_text = modernise(bible_english.get(
                        f"{meta['nameEn']}|{ch['num']}|{verse['num']}", ""))
                    out = gloss_tokens(toks, en_text, strict=True)
                    verse["words"] = out
                    ntok += len(out)
                    ngl += sum(1 for w in out if (w["en"] or "").strip())
            grand_tok += ntok; grand_gl += ngl
            print(f"  {meta['nameEn']:18} {ngl:7}/{ntok:<7} {100 * ngl / max(1, ntok):5.1f}% carrying text")
            if not a.dry_run:
                blob = json.dumps(book, ensure_ascii=False, separators=(",", ":"))
                (RES / f"book_{meta['id']}.json").write_text(blob, encoding="utf-8")
                if dual_dir.exists():
                    (dual_dir / f"book_{meta['id']}.json").write_text(blob, encoding="utf-8")
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
