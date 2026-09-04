import re
#!/usr/bin/env python3
"""The Samoan closed-class grammar, as facts, in one machine-readable place.

WHY THIS EXISTS. The English column of this app is 100% hand-curated: 6,604
verses across 239 per-chapter scripts, and bom_books.json carries no glosses at
all. There is no engine, so there is nothing for a hand table to override --
the Spanish problem does not exist here. The problem here is the opposite one.
Hand curation over 239 files DRIFTS, and nothing can see it drift, because
there is no rule to measure it against.

This is that rule. It covers the closed classes only, and that is not a
limitation: the corpus has just 3,741 distinct word types over 346,933 tokens,
and the top 50 types alone are 71.6% of the text. Samoan carries its grammar in
particles, so a particle inventory IS most of the corpus.

SOURCES. Facts of grammar are not copyrightable, and this file states facts
rather than reproducing anyone's prose:
  - Pratt, "A Grammar and Dictionary of the Samoan Language", 3rd ed. 1893
    (public domain; archive.org/details/agrammaranddict00pratgoog)
  - the Samoan pronoun paradigm and the specificity-based article system as
    described on Wikipedia (CC BY-SA)
  - Mosel & Hovdhaugen, "Samoan Reference Grammar" (1992) and Hunkin,
    "Gagana Samoa" (UH Press; the BYU Samoan 100 coursebook) are the standard
    references and are CONSULTED, not copied
  - and every entry below is checked against this corpus's own usage counts,
    so nothing here is asserted that the text does not show.

THE ONE FACT THAT DOES REAL WORK. Samoan articles mark SPECIFICITY, not
definiteness:

        specific    non-specific
  sg    le          se
  pl    (zero)      ni

So `le` is "the", `se` is "a", and a `se` phrase glossed "the" is a defect the
checker can find without knowing any vocabulary at all.
"""

# ── TAM: the particle that opens a verb phrase ───────────────────────────────
# Samoan marks tense/aspect/mood BEFORE the verb, not on it.
#
# Every entry carries its count in this corpus, because the first version of
# this table was nine markers written from a general description of the
# language and it was wrong twice and short eleven times. Counts are from
# bom_overrides.json: `corpus` is raw occurrences of the string, `heads` is how
# often it opens a glossed unit.
TAM = {
    #  form        gloss              corpus   heads   note
    'e':     ('general / non-past',            'e'),      # 14008  9270
    'te':    ('general, bound to a preposed pronoun', 'te'),  # 5595 but only 20
                                                            # heads: `te` never
                                                            # stands alone, it
                                                            # clings to `ou te`,
                                                            # `latou te`
    'sa':    ('past',                          'past'),   #  9988  5238
    'na':    ('past',                          'past'),   #  2725  1766
    'ua':    ('perfect / inchoative',          'perfect'),#  6923  4471
    'o lo’o': ('progressive / durative',       'is …ing'),#   146   104
    'o loo': ('progressive / durative',        'is …ing'),
    # The bare second half. It is never a word on its own, and while the
    # grammar knew only the pair, anything that split `o loo i` treated
    # `loo` as open-class and glossed it from whatever the lexicon had
    # seen once -- D&C 1:1 printed "together" under it.
    'loo':   ('progressive / durative',        'is …ing'),
    'o le a': ('future',                       'shall'),  #  ----  2599, glossed
                                                            # "shall" 102x
    'ona':   ('sequential, with ai',           'then'),   #  6983  3104
    'ia':    ('optative / hortative',          'let'),    # 12920  5815
    'ina':   ('complementiser / purposive',    'that'),   #  3234  1322
    'se’i':  ('hortative: let, until',         'let'),    #    35    33
    'sei':   ('hortative: let, until',         'let'),
}

# ── MODALS ───────────────────────────────────────────────────────────────────
# Not TAM proper -- they take a TAM marker themselves (`e mafai`) -- but they
# carry the mood the English gloss has to show, so nothing that reads the verb
# phrase can ignore them.
MODALS = {
    'mafai':  'ability / possibility: can, may, might',   # 1301   130
    'tatau':  'obligation: must, ought, lawful',          #  458    14
    'atonu':  'epistemic: perhaps, it may be',            #   59    34
    'semanu': 'counterfactual: would have, must have',    #   16    10
}

# ── CLAUSE OPENERS ───────────────────────────────────────────────────────────
# Conditionals and temporals. These were missing entirely from the first
# version, and `afai` alone occurs 520 times.
SUBORDINATORS = {
    'afai':   'conditional: if',                          #  520   270
    'pe a':   'temporal / future conditional: when, after',#  212   185
    'pe ana': 'counterfactual conditional: had it been',  #    2
    'ina ia': 'purposive: that, so that',
    'ona o':  'causal: because of',                       #  824
}

# ── DISJUNCTIVE AND INTERROGATIVE ────────────────────────────────────────────
DISJUNCTIVE = {
    'pe':   'or, whether, if (polar question)',           #  866   806
    'po o': 'or, whether',                                #  400   385
    'soo':  'any, whoever, whatever',                 #  320    78
}

# ── ARTICLES: specificity, not definiteness ──────────────────────────────────
ARTICLES = {
    'le': ('specific', 'sg', 'the'),
    'se': ('non-specific', 'sg', 'a'),
    'ni': ('non-specific', 'pl', 'some'),
    'si': ('diminutive/affectionate', 'sg', 'the'),
    'sina': ('diminutive non-specific', 'sg', 'a little'),
}
# Specific plural is ZERO-marked: `o tagata` is "the people", not "people".

# ── THE PARTICLE o ───────────────────────────────────────────────────────────
# Two distinct o's, and they are not the same word:
#   1. presentative/topic marker opening a nominal predicate or a fronted NP
#   2. the O-class possessive preposition (see POSSESSIVE_CLASS)
PRESENTATIVE = {'o'}

# ── PREPOSITIONS ─────────────────────────────────────────────────────────────
PREPOSITIONS = {
    'i':    'locative/directional/oblique: in, at, to, on',
    'ia':   'the same, before a pronoun or personal name',
    'iā':   'the same, before a pronoun or personal name',
    'mai':  'source: from',
    'ma':   'comitative/coordinating: and, with',
    'e':    'ergative: BY (marks the agent of a transitive verb)',
    'a':    'possessive, A-class',
    'o':    'possessive, O-class',
    'mo':   'benefactive, O-class: for',
    'ma o': 'benefactive, A-class: for',
    'faatasi ma': 'together with',
}

# ── ERGATIVITY ───────────────────────────────────────────────────────────────
# Samoan is ergative-absolutive: the agent of a transitive verb takes `e`, and
# the single argument of an intransitive takes none. `e` before a noun phrase
# after a verb is the AGENT, not the TAM marker -- the same string, two jobs,
# and telling them apart is positional.
ERGATIVE = 'e'

# ── PRONOUNS ─────────────────────────────────────────────────────────────────
# Samoan distinguishes dual from plural, and inclusive from exclusive in the
# first person -- a distinction English has no way to show, so the gloss cannot
# carry it and the reader loses it. Recorded here because a checker still needs
# to know that `taua` and `matou` are BOTH "we".
PRONOUNS = {
    'a’u': ('1sg', 'I'),      'ou': ('1sg', 'I'),        'aʻu': ('1sg', 'I'),
    'oe': ('2sg', 'you'),     'e': ('2sg clitic', 'you'),
    'ia': ('3sg', 'he/she'),  'na': ('3sg', 'he/she'),
    'maua': ('1du.excl', 'we two'),  'ma': ('1du.excl', 'we two'),
    'taua': ('1du.incl', 'we two'),  'ta': ('1du.incl', 'we two'),
    'oulua': ('2du', 'you two'),      'laua': ('3du', 'they two'),
    'matou': ('1pl.excl', 'we'),     'tatou': ('1pl.incl', 'we'),
    'outou': ('2pl', 'you all'), 'tou': ('2pl clitic', 'you all'),
    'latou': ('3pl', 'they'),
}

# ── POSSESSIVE CLASS: the a/o distinction ────────────────────────────────────
# Alienable (A-class) vs inalienable (O-class). It is a real distinction with
# no English exponent -- both are "his" -- so it cannot show in the gloss, but
# it decides which Samoan form is correct and so belongs in the grammar.
POSSESSIVE_CLASS = {
    'lana': ('A', '3sg', 'his/her'),   'lona': ('O', '3sg', 'his/her'),
    'laʻu': ('A', '1sg', 'my'),        'loʻu': ('O', '1sg', 'my'),
    'la’u': ('A', '1sg', 'my'),        'lo’u': ('O', '1sg', 'my'),
    'lau':  ('A', '2sg', 'your'),      'lou':  ('O', '2sg', 'your'),
    'a':    ('A', '-', 'of'),          'o':    ('O', '-', 'of'),
}


# ── COORDINATORS AND DISCOURSE PARTICLES ─────────────────────────────────────
# Found by an EXHAUSTIVE pass, not by asking whether the ones I had guessed
# were right. `ae` is 1,241 occurrences of the basic adversative "but" and it
# was simply absent, while `ma` -- "and" -- had been there from the first
# version. That is what a candidate list does: it can only confirm or refute
# what you already thought of.
COORDINATORS = {
    'ma':     'and, with',                                # 18548 16623
    'ae':     'but (adversative)',                        #  1241  1166
    'peitai': 'but, yet, nevertheless',                   #   204   201
    'po':     'or',                                       #   597   475
    'ao':     'while, as',                                #   163    29
}

DISCOURSE = {
    'ioe':    'yea (affirmative opener)',                 #  1253  1244
    'faauta': 'behold',                                   #  1582   831
    'faapea': 'thus, so, in this manner',                 #   996    55
    'o lea':  'therefore',
    'o le mea lea': 'wherefore',
}

# ── COMPARATIVE AND MANNER ───────────────────────────────────────────────────
# All of these are `e` + a base, which is why the bare base heads almost no
# units: `pei` alone heads 7, `e pei` heads 460. The marker is the pair.
COMPARATIVE = {
    'e pei':   'as, even as, like',                       #   495   460
    'e tusa':  'according to',                            #   623   600
    'e tusa ma': 'according to',
    'faapei':  'like, as though',                         #    24     3
    # bare `faatasi` is "together"; the "with" belongs to the `ma` that
    # follows it, and is already carried by the 'faatasi ma' entry above.
    'faatasi': 'together',                                #   530   224
}

# ── DEGREE AND ITERATIVE ─────────────────────────────────────────────────────
DEGREE = {
    'toe':   'again, once more (iterative)',              #   782   108
    'tele':  'great, exceedingly (intensifier)',          #  1526    59
    'matua': 'fully, exceedingly (intensifier)',          #   115    13
    'naua':  'excessively, too much',                     #    55     0
}

# ── THE POSSESSIVE PARADIGM ──────────────────────────────────────────────────
# The A/O distinction is PRODUCTIVE, not a list of eight words. It combines
# with every person and number, and with or without the article `l-`:
#
#     bare      o’u    a’u     o latou   a latou   o outou   o tatou
#     with l-   lo’u   la’u    lo latou  la latou  lo outou  lo tatou
#
# The first version held eight fixed forms and so missed `lo` (1,380), `la`
# (354), `o latou` (1,319), `a latou` (940), `lo latou` (788) and the rest --
# together more of the corpus than the eight it did hold. Generated rather
# than listed, so nothing can fall out of it again.
_POSS_PERSON = {
    '’u': '1sg', 'u': '2sg', 'na': '3sg',
    ' matou': '1pl.excl', ' tatou': '1pl.incl',
    ' outou': '2pl', ' latou': '3pl', ' ma': '1du.excl', ' ta': '1du.incl',
}


def _possessives():
    out = {}
    for suffix, person in _POSS_PERSON.items():
        for cls, art in (('O', 'o'), ('A', 'a')):
            bare = (art + suffix).strip()
            out[bare] = (cls, person, 'bare')
            out[('l' + art + suffix).strip()] = (cls, person, 'with article')
    return out


POSSESSIVES = _possessives()
# The bare articles themselves, which the paradigm above does not generate
# because they carry no person: `lo` and `la` stand before a following
# pronoun or noun phrase (`lo latou atua`, `la latou savaliga`).
POSSESSIVES['lo'] = ('O', '-', 'article')        # 1380  591
POSSESSIVES['la'] = ('A', '-', 'article')        #  354  143


# ── COMPLEX PREPOSITIONS ─────────────────────────────────────────────────────
# Samoan builds most spatial relations as `i` + a LOCATIVE NOUN + `o`, so the
# preposition is a three-token frame and neither end of it is a preposition on
# its own. `luga` alone means "top" and sits outside any closed class; the
# preposition is `i luga o`, and it is 773 occurrences of "upon" and "over".
# An inventory of single words cannot hold these, which is why `luga` and
# `totonu` kept surfacing as frequent forms "outside the grammar".
COMPLEX_PREPOSITIONS = {
    'i luga o':   'upon, over, on top of',                #  773   649
    'i totonu o': 'among, within, in the midst of',       #  584   472
    'i luma o':   'before, in front of',                  #  198   173
    'i lalo o':   'under, beneath',                       #   63    30
    'i fafo o':   'outside, out of',                      #   17     8
    'i tua o':    'behind, without',                      #    5     2
    'e ala i':    'by, through, by means of',             #  130   114
}
# The same frames occur without the closing `o` when no complement follows --
# `i luga` 907, `i totonu` 720, `i lalo` 243 -- so both shapes are listed.
COMPLEX_PREPOSITIONS.update({
    'i luga': 'upon, above', 'i totonu': 'among, within',
    'i lalo': 'down, beneath', 'i luma': 'before', 'i fafo': 'outside',
})

# ── DIRECTIONALS: deixis on the verb ─────────────────────────────────────────
# These follow the verb and orient the action relative to the speaker. They are
# routinely absorbed into the verb's gloss, which is correct -- English carries
# them in the verb itself ("came" vs "went").
DIRECTIONALS = {
    'mai': 'toward the speaker (hither)',
    'atu': 'away from the speaker (thither)',
    'aʻe': 'upward',   'a’e': 'upward',
    'ifo': 'downward',
    'ane': 'obliquely, past, alongside',
}

# ── ai: the anaphoric particle ───────────────────────────────────────────────
# Refers back to something already named -- a place, a reason, an instrument.
# GLOSSING_RULES.md already records the consequence: when `ai` caps a verb
# cluster AND the clause goes on to name the place, `ai` IS that place and must
# not be echoed as "thereto".
ANAPHORIC = 'ai'

# ── POST-VERBAL PARTICLES ────────────────────────────────────────────────────
POSTVERBAL = {
    'lava': 'intensifier: very, indeed, -self',
    'uma':  'completive/universal: all, entirely',
    'foi':  'also, too',   'foʻi': 'also, too',   'fo’i': 'also, too',
    'ua':   'already (post-verbal)',
    'pea':  'still, continuing',
}

# ── NEGATION ─────────────────────────────────────────────────────────────────
NEGATION = {
    'le': 'not (verbal negator -- NOT the article; position decides)',
    'lē': 'not (verbal negator)',
    'leai': 'no, there is not',
    'le’i': 'not yet',  'lei': 'not yet',                 #  188
    'aua': 'prohibitive: do not',                         #  see the note below
}
# `le` is the single most dangerous string in the language for this corpus:
# the specific article (25,941 tokens) and the verbal negator share a spelling,
# separated in careful orthography by the macron on `lē` and in practice by
# position -- before a noun it is the article, before a verb it is negation.
#
# TWO ENTRIES HERE WERE WRONG, and the corpus said so:
#
#   `nei` was listed as the prohibitive "lest". In this corpus it is the
#   DEMONSTRATIVE, 966 times, heading units glossed "these things" (128),
#   "all these things" (34), "these words" (29). It has been moved to
#   DEMONSTRATIVES below and taken out of negation entirely.
#
#   `aua` was listed only as the prohibitive "do not". It occurs 427 times and
#   heads a unit 363 of them, glossed "for behold" (148) and "for" (65) -- in
#   this corpus it is overwhelmingly the CAUSAL conjunction, and the
#   prohibitive is the minority reading. Both are kept, prohibitive first,
#   because a reader of this table has to know it is ambiguous.
CAUSAL = {
    'aua': 'for, because (the dominant reading here, 213 of 363 unit heads)',
    'ona': 'for, because',
    'ona o': 'because of',
}

# ── DEMONSTRATIVES ───────────────────────────────────────────────────────────
DEMONSTRATIVES = {
    'nei':   'this, these (proximal)',                    #  966   331
    'lenei': 'this',
    'lea':   'that, the aforementioned',
    'na':    'that (distal) -- also the past TAM; position decides',
}

def classify(word):
    """Every closed-class role this surface form can play. Never decides."""
    w = (word or '').strip().lower()
    roles = []
    if w in TAM:            roles.append(('TAM', TAM[w][0]))
    if w in MODALS:         roles.append(('MODAL', MODALS[w]))
    if w in SUBORDINATORS:  roles.append(('SUBORDINATOR', SUBORDINATORS[w]))
    if w in DISJUNCTIVE:    roles.append(('DISJUNCTIVE', DISJUNCTIVE[w]))
    if w in CAUSAL:         roles.append(('CAUSAL', CAUSAL[w]))
    if w in DEMONSTRATIVES: roles.append(('DEMONSTRATIVE', DEMONSTRATIVES[w]))
    if w in COORDINATORS:   roles.append(('COORDINATOR', COORDINATORS[w]))
    if w in DISCOURSE:      roles.append(('DISCOURSE', DISCOURSE[w]))
    if w in COMPARATIVE:    roles.append(('COMPARATIVE', COMPARATIVE[w]))
    if w in DEGREE:         roles.append(('DEGREE', DEGREE[w]))
    if w in COMPLEX_PREPOSITIONS:
        roles.append(('COMPLEX PREPOSITION', COMPLEX_PREPOSITIONS[w]))
    if w in POSSESSIVES:
        c, person, shape = POSSESSIVES[w]
        roles.append(('POSSESSIVE', '%s-class, %s, %s' % (c, person, shape)))
    if w in ARTICLES:       roles.append(('ARTICLE', ARTICLES[w][0]))
    if w in PRESENTATIVE:   roles.append(('PRESENTATIVE', 'topic/nominal predicate'))
    if w in PREPOSITIONS:   roles.append(('PREPOSITION', PREPOSITIONS[w]))
    if w in PRONOUNS:       roles.append(('PRONOUN', PRONOUNS[w][0]))
    if w in POSSESSIVE_CLASS: roles.append(('POSSESSIVE', POSSESSIVE_CLASS[w][0] + '-class'))
    if w in DIRECTIONALS:   roles.append(('DIRECTIONAL', DIRECTIONALS[w]))
    if w in POSTVERBAL:     roles.append(('POSTVERBAL', POSTVERBAL[w]))
    if w in NEGATION:       roles.append(('NEGATION', NEGATION[w]))
    if w == ANAPHORIC:      roles.append(('ANAPHORIC', 'refers to something already named'))
    return roles


CLOSED_CLASS = (set(TAM) | set(MODALS) | set(SUBORDINATORS) | set(DISJUNCTIVE) |
                set(COORDINATORS) | set(DISCOURSE) | set(COMPARATIVE) |
                set(DEGREE) | set(POSSESSIVES) | set(COMPLEX_PREPOSITIONS) |
                set(CAUSAL) | set(DEMONSTRATIVES) |
                set(ARTICLES) | PRESENTATIVE | set(PREPOSITIONS) |
                set(PRONOUNS) | set(POSSESSIVE_CLASS) | set(DIRECTIONALS) |
                set(POSTVERBAL) | set(NEGATION) | {ANAPHORIC})


if __name__ == '__main__':
    import sys
    for w in sys.argv[1:] or ['le', 'se', 'e', 'o', 'ai', 'atu', 'lava', 'lē']:
        print('%-8s %s' % (w, classify(w) or '(open class / not listed)'))


# ── THE GLOSS A RULE GIVES ───────────────────────────────────────────────────
# classify() says what a form IS. This says what it READS as in English, for
# the forms where the grammar alone settles it -- which is most of the closed
# class and 70% of the corpus.
#
# AMBIGUOUS is the important half. `le` is the specific article AND the verbal
# negator; `e` is a TAM marker AND the ergative AND a 2sg pronoun; `o` is the
# presentative AND the O-class possessive; `na` is past tense AND a distal
# demonstrative. For those the grammar states the ambiguity and refuses to
# choose -- position or context decides, and the caller has the corpus and the
# verse's English to decide with. A rule that guesses is worse than no rule.
AMBIGUOUS = {'le', 'e', 'o', 'a', 'na', 'ia', 'aua', 'ma', 'lo', 'la', 'se',
             'ina', 'ona', 'pe', 'ai', 'nei', 'lava', 'uma', 'ua'}

_PRIMARY = {}


def _first(text):
    """The head reading of a description.

    Two shapes appear in the tables: a plain list, "upon, over, on top of",
    where the head is the first item; and a labelled one, "conditional: if" or
    "ability / possibility: can", where the label is the grammatical category
    and the gloss is what follows the colon.
    """
    if not text:
        return ''
    if ':' in text:
        text = text.split(':', 1)[1]
    return re.split(r'[,;(]', text)[0].strip()


# TAM markers and directionals are ABSORBED, not glossed. Samoan puts tense
# before the verb and deixis after it, and English carries both inside the verb
# itself -- "came" against "went" is `mai` against `atu`, and there is no
# separate English word to hang on them. In this corpus they are continuation
# tokens inside a verb cluster, which is what GLOSSING_RULES.md rule 1 and rule
# 2 describe. So the grammar's contribution here is knowing where a cluster
# STARTS, not what the particle reads as on its own.
ABSORBED = (set(TAM) | set(DIRECTIONALS)) - {'o le a'}
# `o le a` is the exception: it heads 2,599 units in this corpus, glossed
# "shall", so unlike the other TAM markers it carries an English word of its
# own rather than disappearing into the verb.


def _build_primary():
    if _PRIMARY:
        return _PRIMARY
    _PRIMARY['o le a'] = 'shall'
    for form, (_spec, _num, gloss) in ARTICLES.items():
        _PRIMARY.setdefault(form, gloss)
    for form, (_person, gloss) in PRONOUNS.items():
        _PRIMARY.setdefault(form, gloss)
    for table in (COMPLEX_PREPOSITIONS, DIRECTIONALS, POSTVERBAL, NEGATION,
                  COORDINATORS, DISCOURSE, COMPARATIVE, DEGREE, DISJUNCTIVE,
                  SUBORDINATORS, MODALS, CAUSAL, DEMONSTRATIVES, PREPOSITIONS):
        for form, desc in table.items():
            _PRIMARY.setdefault(form, _first(desc))
    for form, (cls, person, shape) in POSSESSIVES.items():
        eng = {'1sg': 'my', '2sg': 'your', '3sg': 'his', '1pl.excl': 'our',
               '1pl.incl': 'our', '2pl': 'your', '3pl': 'their',
               '1du.excl': 'our', '1du.incl': 'our'}.get(person)
        if eng:
            _PRIMARY.setdefault(form, eng)
    return _PRIMARY


def primary_gloss(form):
    """The English a closed-class form reads as, or '' when the grammar
    deliberately refuses (see AMBIGUOUS) or does not know the form."""
    f = (form or '').strip().lower()
    if not f or f in AMBIGUOUS or f in ABSORBED:
        return ''
    return _build_primary().get(f, '')


# ── ORTHOGRAPHY: one glottal, and marks that are NOT folded ──────────────────
# The corpus writes the glottal with U+2019 (12,147 times), but three other
# codepoints leak in from the source: U+2018 (16), U+02BC (in `Saraʼemila`) and
# the plain ASCII apostrophe. Four spellings of one letter split a word across
# four index keys, so every lookup, every unit and every derived lexicon has to
# key on a normalised form. This is the "sweep hyphen-tolerant" lesson from the
# Hebrew and Spanish corpora, in its Samoan dress.
#
# WHAT IS NOT FOLDED: the glottal itself, and the macron. They are CONTRASTIVE.
#   au     your, current    a’u     I, me
#   ai     anaphoric        a’i     with, by means of
#   ou     I                o’u     my
#   ia     he, to           i’a     fish        iā   to (before a name)
#   savali to walk          sāvali  a messenger
# Folding them would merge distinct words exactly as folding Spanish accents
# merged `él` with `el`. 504 forms in this corpus differ only by a glottal or a
# macron, and most of those pairs are different words.
#
# A WARNING ABOUT DETECTING "TYPOS" BY FOLDING. A scan for rare forms whose
# accent-and-glottal-stripped shape matches a much commoner form returns 78
# candidates here, and it looks like a list of stray markings. It is not a
# reliable one: `sāvali` occurs once against `savali` sixty times and is not a
# mistyped `savali` at all, it is a different word. The fold that finds the
# candidates is the same fold that cannot tell them apart, which is how a
# gentilic sweep on the Spanish corpus once read `un` as "Jun" and `ella` as
# "Elah". Such a list locates; only a reader who knows Samoan can judge it.
GLOTTALS = "\u2019\u2018\u02bb\u02bc'\u00b4\u0060"
GLOTTAL = "\u2019"


def normalise_glottal(text):
    """One codepoint for the glottal. Nothing else is touched."""
    out = text
    for ch in GLOTTALS:
        if ch != GLOTTAL:
            out = out.replace(ch, GLOTTAL)
    return out


# ── REGISTER: gagana fa’aaloalo, the respectful language ─────────────────────
# Samoan has a chiefly register with its own words for everyday things, and
# scripture uses it constantly, because it is speaking of and to God. It is not
# decoration: it changes which Samoan word appears, and the English gloss
# usually flattens it, so a tool that does not know the pairs will treat the
# respectful word as unknown vocabulary.
#
# This is why `le siufofoga o` glosses "the voice of" and `o ona fofoga` was
# left undecided: `siufofoga` and `fofoga` are the respectful forms of `leo`
# and `mata`. It is also why the first-pass generator wanted to write `mata o`
# as "faces of" in a verse about eyes.
#
# Every pair below is attested in this corpus, with its own occurrence counts,
# and the glosses are the ones the translator actually chose.
RESPECTFUL = {
    # respectful          common      sense           (respectful n, common n)
    'fetalai':   ('tautala', 'speak, says'),          # 561 / 382
    'saunoa':    ('tautala', 'speak'),                 #   8 / 382
    'afio':      ('sau',     'come, go (of a chief)'), # 211 / 125
    'maliu':     ('oti',     'die, pass away'),        #  73 / 340
    'silasila':  ('vaai',    'see, behold'),           #  34 / 691
    'silafia':   ('iloa',    'know'),                  #  44 / 775
    'finagalo':  ('manao',   'will, desire'),          #  71 / 238
    'taumafa':   ('ai',      'eat'),                   #   3
    'gasegase':  ('mai',     'be sick'),               #   1
    'suafa':     ('igoa',    'name'),                  # 148 / 200
    'aao':       ('lima',    'hand, arm'),             # 106 / 344
    'fofoga':    ('mata',    'face, eyes, mouth'),     #  73 / 112
    'siufofoga': ('leo',     'voice'),                 #  67 / 107
    'alo':       ('tama',    'son, child'),            # 101 /  34
    'maota':     ('fale',    'house, mansion'),        #   9 / 112
}
COMMON_OF = {r: c for r, (c, _s) in RESPECTFUL.items()}
