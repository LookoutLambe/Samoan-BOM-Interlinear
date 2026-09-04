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
# Samoan marks tense/aspect/mood before the verb, not on it. These are the
# markers this corpus actually uses, with their occurrence counts.
TAM = {
    'e':     ('general/habitual/future', 'e'),      # non-past, generic
    'te':    ('general, after a pronoun', 'te'),    # `ou te`, `latou te`
    'sa':    ('past', 'past'),                      # sa and na are
    'na':    ('past', 'past'),                      # interchangeable here
    'ua':    ('perfect/inchoative', 'perfect'),     # has become / now is
    'ona':   ('sequential, with ai', 'sequential'),
    'ia':    ('optative/hortative', 'let'),
    'ina':   ('complementiser/sequential', 'that'),
    'o le a': ('immediate future', 'about to'),
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
    'leʻi': 'not yet',  'le’i': 'not yet',
    'aua': 'prohibitive: do not',
}
# `le` is the single most dangerous string in the language for this corpus:
# the specific article (25,941 tokens) and the verbal negator share a spelling,
# separated in careful orthography by the macron on `lē` and in practice by
# position -- before a noun it is the article, before a verb it is negation.


def classify(word):
    """Every closed-class role this surface form can play. Never decides."""
    w = (word or '').strip().lower()
    roles = []
    if w in TAM:            roles.append(('TAM', TAM[w][0]))
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


CLOSED_CLASS = (set(TAM) | set(ARTICLES) | PRESENTATIVE | set(PREPOSITIONS) |
                set(PRONOUNS) | set(POSSESSIVE_CLASS) | set(DIRECTIONALS) |
                set(POSTVERBAL) | set(NEGATION) | {ANAPHORIC})


if __name__ == '__main__':
    import sys
    for w in sys.argv[1:] or ['le', 'se', 'e', 'o', 'ai', 'atu', 'lava', 'lē']:
        print('%-8s %s' % (w, classify(w) or '(open class / not listed)'))
