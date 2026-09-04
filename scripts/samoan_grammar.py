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
    'soo':  'any, whosoever, whatsoever',                 #  320    78
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
    'oe': ('2sg', 'thou'),    'e': ('2sg clitic', 'thou'),
    'ia': ('3sg', 'he/she'),  'na': ('3sg', 'he/she'),
    'maua': ('1du.excl', 'we two'),  'ma': ('1du.excl', 'we two'),
    'taua': ('1du.incl', 'we two'),  'ta': ('1du.incl', 'we two'),
    'oulua': ('2du', 'ye two'),      'laua': ('3du', 'they two'),
    'matou': ('1pl.excl', 'we'),     'tatou': ('1pl.incl', 'we'),
    'outou': ('2pl', 'ye'),   'tou': ('2pl clitic', 'ye'),
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
    'lau':  ('A', '2sg', 'thy'),       'lou':  ('O', '2sg', 'thy'),
    'a':    ('A', '-', 'of'),          'o':    ('O', '-', 'of'),
}

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
                set(CAUSAL) | set(DEMONSTRATIVES) |
                set(ARTICLES) | PRESENTATIVE | set(PREPOSITIONS) |
                set(PRONOUNS) | set(POSSESSIVE_CLASS) | set(DIRECTIONALS) |
                set(POSTVERBAL) | set(NEGATION) | {ANAPHORIC})


if __name__ == '__main__':
    import sys
    for w in sys.argv[1:] or ['le', 'se', 'e', 'o', 'ai', 'atu', 'lava', 'lē']:
        print('%-8s %s' % (w, classify(w) or '(open class / not listed)'))
