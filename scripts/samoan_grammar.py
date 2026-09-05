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
# ── `<verb> ona` : ona AS A COMPLEMENTISER ───────────────────────────────────
# `ona` has three jobs and the corpus uses all three heavily:
#   causal      "for, because"   before a TAM or `o`  — ona ua 197, ona sa 163
#   possessive  "his, her, its"  before a noun        — ona tagata 78 of 85
#   COMPLEMENTISER, bound to the verb in front of it, which is the one the
#   grammar did not know. Curated counts for the unit ENDING on `ona`:
#     mafai ona   351   "may / might / cannot"     amata ona  187  "began to"
#     faapea ona   92   "thus"                     uma ona     79  "after"
#     pei ona      72   "as"
# Each is one frame. Split, the verb loses its complement and `ona` is read as
# the causal, which says "because" in the middle of "he began to speak".
VERB_ONA = {
    'mafai ona':  'can, may, is able to',                 #   351
    'amata ona':  'began to',                             #   187
    'faapea ona': 'thus, so that',                        #    92
    'uma ona':    'after, when … had finished',           #    79
    'pei ona':    'as, just as',                          #    72
    'tatau ona':  'must, should, ought',
    'ave ona':    'take to',
}

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
}

# ── DISJUNCTIVE AND INTERROGATIVE ────────────────────────────────────────────
DISJUNCTIVE = {
    'pe':   'or, whether, if (polar question)',           #  866   806
    # THE EXCEPTION to the phrase-initial `o` rule, by the user's ruling:
    # `po o` is one disjunctive marker, not `po` plus a headed phrase.
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
    '’ou': ('1sg', 'I'),      'ʻou': ('1sg', 'I'),   # the glottal written
    'oe': ('2sg', 'you'),     'e': ('2sg clitic', 'you'),
    'ia': ('3sg', 'he/she'),  'na': ('3sg', 'he/she'),
    'ma': ('1du.excl', 'we two'),    'ta': ('1du.incl', 'we two'),
    'oulua': ('2du', 'you two'),      'laua': ('3du', 'them'),
    # THE GLOTTAL IS THE WHOLE WORD HERE. These were registered on the
    # glottal-LESS form, which is a different word, so the pronoun reading was
    # claimed by 1,587 tokens that are nothing of the kind:
    #
    #   maua  1,224  the VERB "obtain, receive"   ma’ua  73  1du.excl "us"
    #   taua    363  the NOUN "war"               ta’ua 295  the VERB "called"
    #   laua    359  3du "them"                   la’ua 173  the same word,
    #                                                         glottal written
    #
    # `maua` and `taua` are struck from this table entirely. `ta’ua` is not
    # added: in this corpus it is "which was called", never the 1st-dual.
    # `la’ua` IS added, because there the glottal is only inconsistent
    # spelling of one word -- both forms gloss "them / to them / they" and
    # both follow `i`, `o`, `lo`.
    'ma’ua': ('1du.excl', 'us'),      'la’ua': ('3du', 'them'),
    'matou': ('1pl.excl', 'we'),     'tatou': ('1pl.incl', 'we'),
    'outou': ('2pl', 'you all'), 'tou': ('2pl clitic', 'you all'),
    'latou': ('3pl', 'they'),
    # THE OBLIQUE FRAMES. `latou` alone is "they"; the same pronoun after `i`
    # is the object, and after `ia te` it is a dative. The grammar knew only
    # the bare pronoun, so `ia te i latou` fell through to the inventory and
    # `i latou` came back "those". Curated counts in the comment.
    'i latou': ('3pl obl', 'them'),        # them 515 / they 271
    'i matou': ('1pl.excl obl', 'us'),     # us 50
    'i tatou': ('1pl.incl obl', 'us'),     # us 27
    'i laua':  ('3du obl', 'them'),        # they 11 / them 8
    # `o ia` and `e ia` are the pronoun under the topic and the ergative. The
    # curation ends 1,578 units on the first and 611 on the second, and the
    # grammar had neither, so both were guessed from the inventory.
    'o ia':    ('3sg topic', 'he'),        # him 253 / he 248
    'e ia':    ('3sg ergative', 'him'),    # him 113 / he 45
    'lava ia': ('3sg reflexive', 'himself'),  # myself 20 / himself 18
    # ── BOUND PRONOUN + `te` ────────────────────────────────────────────
    # `te` is the TAM that clings to a preposed pronoun -- this file has said
    # so since it was written ("never stands alone, it clings to `ou te`,
    # `latou te`") -- and not one of the frames was registered, so 3,105
    # tokens fell through to the inventory. The DUALS are here too: the
    # user's point that a bound form "can also be us two depending on
    # context" is exactly this frame. Counts are the curation's first English
    # word for a unit starting with the frame.
    # ── `o` + PRONOUN : THE TOPIC FRAME ─────────────────────────────────
    # `o a’u` is "I" 97 times and "I am" 39 -- the topic-marked 1st person,
    # which the table did not have at all. The plural ones are claimed by the
    # possessive paradigm as "your/our/their", and they are BOTH: `o outou`
    # is "you" 19 and "of you" 5. Those get readings so the verse decides
    # rather than the paradigm always winning.
    'o a’u':   ('1sg topic', 'I'),       # I 97 / I am 39
    'o oe':    ('2sg topic', 'you'),
    'o ma’ua': ('1du.excl topic', 'we two'),
    'o ta’ua': ('1du.incl topic', 'we two'),
    'ou te':    ('1sg', 'I'),            # I 698
    'tou te':   ('2pl', 'you all'),      # you 85
    'e te':     ('2sg', 'you'),          # you 33
    'latou te': ('3pl', 'they'),         # they 72
    'na te':    ('3sg', 'he'),           # he 10
    'matou te': ('1pl.excl', 'we'),      # we 46
    'tatou te': ('1pl.incl', 'we'),      # we 11
    'lua te':   ('2du', 'you two'),      # 32 pairs
    'la te':    ('3du', 'they two'),     # they 4
    'ma te':    ('1du.excl', 'we two'),  # we 2
    'ta te':    ('1du.incl', 'we two'),  # we 1
    'ia te au':      ('1sg dat', 'to me'),      # to me 46
    'ia te oe':      ('2sg dat', 'to you'),     # to you 141
    'ia te ia':      ('3sg dat', 'to him'),     # to him 246
    'ia te outou':   ('2pl dat', 'to you'),     # to you 451
    'ia te i latou': ('3pl dat', 'to them'),    # to them 358
    'ia te i matou': ('1pl.excl dat', 'to us'), # to us 44
    'ia te i tatou': ('1pl.incl dat', 'to us'), # to us 26
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
    # `ae ui i lea` is ONE WORD of English: "nevertheless", 237 times, and the
    # curation records it whole 170 of those. It opens with a coordinator, so
    # the rule that makes a coordinator start its own unit was cutting it in
    # half and printing "In" on the `lea`.
    'ae ui i lea': 'nevertheless',                        #   237
    'e ui i lea':  'nevertheless, howbeit',               #    22
    'ui i lea':    'nevertheless',                        #   260 total
    'ae ui':       'although, though',
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
    'aupito': 'most, very',                               # the superlative
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


# A GENERATED FORM CAN COLLIDE WITH A REAL WORD, and the paradigm must give
# way when it does -- the same mistake as `maua` "obtain" and `taua` "war"
# sitting in the pronoun table. `sau` is `sa`+`u` on paper and the verb "come"
# in the text: 229 occurrences, and the curation glosses every unit starting
# with it "come" or "came". `o le a sau` is "will come", not "will your".
#
# The possessive it would have been is `sa’u`, with the glottal, which is
# generated separately and kept.
_NOT_POSSESSIVE = {'sau'}


def _possessives():
    """The possessive paradigm: class x person x article.

    THREE ARTICLE ROWS, not two. The bare `o-`/`a-` forms and the specific
    `lo-`/`la-` forms were here; the NON-SPECIFIC `so-`/`sa-` row was not, and
    it is the same construction with `se` in place of `le`:

        lona  his (that one)        sona  his (any) -- so + na
        lana  his (A-class)         sana  his (A-class, any)
        lo’u  my                    so’u  my (any)

    `sona` alone occurs 29 times and 39 of the family follow `leai`: `e leai
    sona gataaga` is "there is no end OF IT", which the curation renders
    "without end". None of them could be glossed while the row was missing.
    """
    out = {}
    for suffix, person in _POSS_PERSON.items():
        for cls, art in (('O', 'o'), ('A', 'a')):
            bare = (art + suffix).strip()
            out[bare] = (cls, person, 'bare')
            out[('l' + art + suffix).strip()] = (cls, person, 'with article')
            ns = ('s' + art + suffix).strip()
            if ns not in _NOT_POSSESSIVE:
                out[ns] = (cls, person, 'non-specific')
    return out


POSSESSIVES = _possessives()

# The non-specific series -- `se` and the `so-`/`sa-` possessives built on it.
# It is the grammar of NOT KNOWING: which one, whose, whether there is one at
# all. `o le a` leans on it to ask a question.
NON_SPECIFIC = ({f for f, v in POSSESSIVES.items() if v[2] == 'non-specific'}
                | {'se', 'ni', 'so', 'sa'})
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
# `o` IS PHRASE-INITIAL. It heads the complement; it is not the tail of the
# preposition. `ua i luga o tagata uma` is `ua` + `i luga` "upon" +
# `o tagata uma` "of all men" -- NOT `i luga o` + `tagata uma`, which takes the
# head off the noun phrase and leaves it to start on a bare noun.
#
# This file used to list both shapes and called the bare one the reduced
# variant. That was backwards: the bare frame IS the preposition, and every
# `... o` entry was a frame that had eaten the next phrase's head.
COMPLEX_PREPOSITIONS = {
    # THE LOCATIVE FRAMES: `i` + a directional noun. Every alternative here is
    # a reading the verse may choose (see _build_alt_readings) -- the code used
    # to take the first and only the first, so `i luga` said "upon" 773 times
    # and "over" almost never, while the curation says "over" in 90% of the
    # verses whose English carries it.
    #
    # The alternatives and their order are the curation's own, counted as the
    # first English word of a unit that starts with the frame.
    'i luga':   'upon, over, on, above, up, upward',      # 560/150/26/24/21
    'i totonu': 'among, in, into, within, amongst',       # 412/94/53/35/5
    'i luma':   'before, forward, in front of, forth',    # 184/19/7
    'i lalo':   'down, under, below, beneath',            #  66/34/11/1
    'i fafo':   'out, forth, outside, away, abroad',      #  52/10/5/3
    'i tua':    'back, backward, behind, without',        #  12/5/3/2
    # SIX MORE THE GRAMMAR NEVER HAD, found by asking the corpus which `i X`
    # pairs behave like these. `i uta` and `i tai` are not among them -- this
    # text does not use either, not once.
    'i matu':      'northward, north',                    #   86 pairs
    'i tafatafa':  'by, beside, near',                    #   68
    'i saute':     'southward, south',                    #   63
    'i sisifo':    'west, westward',                      #   52
    'i sasae':     'east, eastward',                      #   47
    'i itu':       'side, sides, about',                  #   27
    'i tala':      'beyond, beside, further',             #   14
    # `e ala i le X` is `e ala` + `i le X`: the `i` heads the phrase.
    'e ala':    'by, through, by means of',               #  130   114
    # More `e <base>` frames, all measured from the curation by the first
    # English word of a unit that starts with them. They were invisible to
    # the grammar, so each fell through to the inventory and was glossed by
    # whatever a verse happened to contain.
    'e uiga':    'concerning, about',                     #   443, "concerning" 399
    'e faasaga': 'against, toward',                       #   288, "against"    270
    'e faavavau': 'forever, everlasting',                 #   113, "forever"     69
    'e leai':    'there is no, none',                     #   120
    # ONE FRAME, like `po o`. `e tusa ma lo’u iloa` is "according to my
    # knowledge": the `ma` is part of the preposition, not the head of the
    # phrase after it, and split the gloss said "according to" and "to" twice.
    'e tusa ma': 'according to',                          #   410
    'e tusa':    'according to, like',                    #   600
}

# ── DIRECTIONALS: deixis on the verb ─────────────────────────────────────────
# These follow the verb and orient the action relative to the speaker. They are
# routinely absorbed into the verb's gloss, which is correct -- English carries
# them in the verb itself ("came" vs "went").
# These held DESCRIPTIONS, not glosses, and a lone directional printed one:
# `atu` came out "away from the speaker". Every value here is now English a
# gloss may actually say, alternatives first, with the deixis in the comment.
DIRECTIONALS = {
    'mai': 'from, forth, hither, out, here',      # toward the speaker
    'atu': 'forth, away, out, over, thither',     # away from the speaker
    'aʻe': 'up, upward',   'a’e': 'up, upward',
    'ifo': 'down, downward',
    'ane': 'by, near, along, across',             # obliquely, past, alongside
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
    # `ona o le mea lea` is `ona` "because" + `o le mea lea` "of this thing".
    # The `o` still tells you WHICH `ona` this is -- see BY_NEXT below, which
    # reads it as context without swallowing it.
    'ona': 'for, because',
}

# ── DEMONSTRATIVES ───────────────────────────────────────────────────────────
# ── INTERROGATIVES ───────────────────────────────────────────────────────────
# The question words, none of which this file had. From samoan.ws/04-questions,
# checked against the corpus (occurrences after each) and against the
# curation's own gloss where it has one.
#
# That page also states, independently, the two things the user had already
# told me: `o le a lea?` is "what is this?", and a QUESTION TAKES THE
# INDEFINITE ARTICLE `se`/`ni` where an answer takes `le`. That is the same
# uncertainty that makes `o le a` + a non-specific form interrogative.
INTERROGATIVES = {
    'fia':      'how many, how much',                     #   249
    'aisea':    'why',                                    #    79  curated "why"
    'aiseā':    'why',
    'faapefea': 'how',                                    #    59
    'fa’apefea': 'how',
    'fea':      'where',                                  #    32  curated "where"
    'afea':     'when',                                   #    10  (future)
    'anafea':   'when',                                   #        (past)
}

DEMONSTRATIVES = {
    # `o e` is the headless relative -- "those who", "they who". The curation
    # ends 218 units on this `e` with "who" as the last English word, and the
    # grammar had no entry, so it was read as an ergative or dropped.
    'o e': 'those who, they who',
    'nei':   'this, these (proximal)',                    #  966   331
    'lenei': 'this',
    'lea':   'that, the aforementioned',
    'na':    'that (distal) -- also the past TAM; position decides',
    # THE DISTAL DEMONSTRATIVE, 708 occurrences and absent from this table.
    # samoan.ws gives the paradigm as lea/lenei "this", lenā/lele "that",
    # lelā/lale "that (far)", with nei/nā/lā as their plurals. This corpus
    # writes only the unmacronned forms -- `lena` 708, `lele` 8 -- and never
    # lenā, nā, lelā or lā, not once. Curated: "that" 58 unit-initial, 23
    # unit-final.
    'lena':  'that',                                      #   708
    'lele':  'that',                                      #     8
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
# DIRECTIONALS STAY ABSORBED, and this was tested rather than assumed. They
# carry real English -- the curation glosses `atu` "forth" 170 times and "away"
# 108, `ifo` "down" 126 -- so letting them speak looked obviously right. It
# measured WORSE (content F1 86.4 -> 86.2), because far more often the curation
# binds them to the verb: `fai atu` is "said" 336 times, `sau mai` is "come"
# 356. Splitting those to gloss the particle costs more than it gains.
#
# They keep their READINGS anyway, for the times one does stand as its own unit.
# DIRECTIONALS ARE THEIR OWN WORD. `alu ifo` is "go" + "down", not one thing
# whose English piles onto the second token -- 1 Nephi 4:33 printed "to go
# down" on `ifo` and 2:5 printed a whole clause on it. One word, one gloss.
# ── TENSE ────────────────────────────────────────────────────────────────────
# The TAM markers were in this file from the start and NOTHING used them for
# tense: they are absorbed, contribute no English of their own, and the verb's
# gloss was never inflected by them. `sa alu`, `e alu` and `o le a alu` could
# all come out "go".
#
# They predict it strongly. Counting only curated glosses that carry a tense at
# all (a gloss like "the record" carries none):
#
#     o le a   2,266   FUTURE 97%
#     na       1,172   PAST 66%, PERFECT 26%          -> 92% past-ish
#     sa       3,760   PAST 66%, PRESENT 22%
#     ua       2,522   PERFECT 50%, PAST 27%          -> 77% past-ish
#     e        1,769   PRESENT 62%
#     o lo’o      31   PRESENT 42%, PROGRESSIVE 39%   -> 81% non-past durative
TENSE_OF_TAM = {
    'sa': 'PAST',      'na': 'PAST',
    'ua': 'PERFECT',
    'e': 'PRESENT',    'te': 'PRESENT',
    'o loo': 'PROGRESSIVE', 'o lo’o': 'PROGRESSIVE',
    'o le a': 'FUTURE',
}


def tense_of_tam(form):
    """The tense a marker calls for, or None."""
    return TENSE_OF_TAM.get((form or '').strip().lower())


ABSORBED = set(TAM) - {'o le a', 'o loo', 'o lo’o', 'loo'}
# `o le a` is the exception: it heads 2,599 units in this corpus, glossed
# "shall", so unlike the other TAM markers it carries an English word of its
# own rather than disappearing into the verb.
#
# `o lo’o` / `o loo` is the same kind of exception. The progressive is a
# PREDICATE marker, not a particle that vanishes into a verb: in
# `o loo i luga o motu o le sami` there is no verb at all for it to vanish
# into -- it is the copula of a locative predicate, "that ARE upon the isles
# of the sea". While it was absorbed, D&C 1:1 printed nothing under it and the
# segmentation reached past it for `o loo i`, taking the `i` off `i luga`.


# ── CONTEXT THAT DISAMBIGUATES WITHOUT BEING SWALLOWED ───────────────────────
# The old tables handled ambiguity by lengthening the form: `ona o` glossed
# "because of", `ma o` glossed "for". That reads the following `o` correctly
# and then keeps it, which is exactly the mistake -- `o` heads what comes next.
#
# A following particle can tell you which word this is without belonging to
# it. The unit stays one token; only the reading is chosen by the lookahead.
BY_NEXT = {
    ('ona', 'o'): 'because',      # ona o le mea lea -- vs sequential `ona`
    ('ma', 'o'):  'for',          # benefactive, A-class
    ('mo', 'o'):  'for',          # benefactive, O-class
}


def gloss_in_context(form, nxt=None):
    """The gloss for `form`, letting the NEXT token disambiguate it.

    Falls back to primary_gloss when the lookahead says nothing. The next
    token is never consumed -- see BY_NEXT.
    """
    f = (form or '').strip().lower()
    n = (nxt or '').strip().lower()
    if n:
        hit = BY_NEXT.get((f, n))
        if hit:
            return hit
    return primary_gloss(f)


# ── `o` IS PHRASE-INITIAL ────────────────────────────────────────────────────
# The one structural rule this file exists to state. A unit never ENDS on a
# bare `o`: the `o` is the head of the phrase that follows, so a unit ending
# on it has taken the next phrase's first word.
#
# `po o` is the exception, by the user's ruling: it is a single disjunctive
# marker rather than a word plus a headed phrase.
# THE HEADS. Each of these opens a phrase, so a unit may not end on one and
# may not contain one anywhere but in first position -- a bare `o` inside a
# unit means the unit has run through the start of the next phrase.
# `i luga o motu` is `i luga` "upon" + `o motu` "of the isles", not one thing.
#
# Measured against the 111,683 curated units, unit-final vs unit-initial:
#   o  3,635 / 16,269      a    775 / 1,533     i  1,006 / 13,211
#   ma   838 / 16,623      le   237 /  6,361    se    73 /  1,193
#   mo    25 /    817      ni     3 /    352
#
# DELIBERATELY NOT HERE, because these really do end phrases:
#   ia   an object pronoun as often as a preposition -- `iā te ia` "to him"
#   mai  a directional that follows its verb -- `sau mai` "come hither"
#   lea  a demonstrative, and Samoan puts it after the noun -- `le mea lea`
#   e    genuinely both: the ergative and TAM `e` open a phrase, but the
#        VOCATIVE `e` closes one -- `E outou e tagata` "O ye people". Until
#        those two are told apart, the rule would break every vocative.
# ── TRANSLITERATED TERMS ─────────────────────────────────────────────────────
# The Nephite measures of Alma 11. They are proper terms, but unlike the names
# they are written LOWERCASE in both languages, so the name rule cannot see
# them: `senine`, `seone`, `sume`, `limena` were all left blank and the whole
# of "a senine of gold" landed on `auro` "gold".
#
# Derived, not guessed: each English measure occurs almost nowhere else in the
# canon, so pairing it with the Samoan tokens of the same verse names its form.
#
# `leah` IS DELIBERATELY ABSENT. Its Samoan form collides with `lea`, the
# demonstrative that heads 686 curated units -- registering it would cost far
# more than the four verses it would fix.
TRANSLITERATED = {
    'senine':   'senine',    'seone':    'seon',
    'sume':     'shum',      'limena':   'limnah',
    'senuma':   'senum',     'aminoa':   'amnor',
    'eseroma':  'ezrom',     'oneti':    'onti',
    'sipelona': 'shiblon',   'sipelumo': 'shiblum',
    'anetione': 'antion',    'anetiona': 'antion',
    'onetise':  'onties',    'senuma,':  'senum',
}


# ── WORDS THE BOOK OF MORMON NEVER USES ──────────────────────────────────────
# The tool learns its vocabulary from the curated Book of Mormon, so the D&C's
# ecclesiastical words have no evidence anywhere and came out blank -- 28 forms,
# 0.23% of the corpus, and they are the words those sections are ABOUT.
#
# Derived, not guessed. Each was found by lift: how much likelier an English
# word is in the verses carrying the form than in the corpus at large. The
# figure after each is that lift.
VOCABULARY = {
    # a fixed idiom of the Bible register: one unit, one English (the shorter
    # `ua faapea lava` is NOT it -- `ua faapea lava ona alofa` is "so loved")
    'i le ua faapea lava': 'and it was so',
    'perisitua':   'priesthood',      #  86x
    'peresitene':  'president',       # 143x
    'epikopo':     'bishop',          # 158x
    'aufono':      'council',         # 179x
    'korama':      'quorum',          # 519x
    'konafesi':    'conference',      # 495x
    'ositaulaga':  'priest',          #  98x
    'faleteuoloa': 'storehouse',      # 419x
    'mea-tausi':   'stewardship',     # 371x
    'tausimea':    'steward',         # 519x
    'selesitila':  'celestial',       # 474x
    'itumalo':     'county',          # 681x
    'fuaiupu':     'verse',           # 535x
    'lotu':        'religion',        # 303x
    # `tamai` alone is "child of"; the LAMB is the pair, and the curation
    # never writes one without the other -- `le tamai mamoe` "the Lamb".
    'tamai mamoe': 'Lamb',            # 138x
    'tunoa':       'grace',           # 178x  -- `alofa tunoa`
    'siitia':      'lifted',          #  66x
    'liligi':      'pour',            # 242x
    'uluai':       'first',           #  41x
    'olive':       'olive',           # 389x
    'tuulima':     'handed',          # 431x
    'faaosoina':   'stir',            # 133x
    'segia':       'caught',          # 300x
    'fa’asoa':     'distribute',
}


_DICT = None


def _dictionary():
    """The two lexicons, merged. THE TOOL HAD NONE UNTIL NOW.

    Everything it knew about a Samoan word it had inferred from how that word
    was glossed somewhere in the curated Book of Mormon -- so a word that book
    never uses had no meaning at all, and a word with more senses than that
    book happens to show could only ever be read the way it appears there.
    `sau` had ~90 witnesses, every one of them "come"; Pratt gives it three
    senses, "come", "fall as the dew", and "thy, your".

      Pratt 1893   Samoan-English, public domain, OCR -- the archaic
                   vocabulary of the scripture register
      EALD         English-Samoan, modern and clean, inverted here -- the
                   ordinary words Pratt's scan mangles

    Pratt first where they disagree: it is a dictionary OF Samoan, and this
    corpus is 19th-century scripture register.
    """
    global _DICT
    if _DICT is None:
        import json
        from pathlib import Path
        res = (Path(__file__).resolve().parent.parent /
               "O le Tusi a Mamona Interlinear" / "Resources")
        merged = {}
        # Pratt FIRST and in its own order -- it is a dictionary of Samoan and
        # this corpus is 19th-century scripture register -- then EALD for the
        # ordinary modern words Pratt's scan mangles.
        # then the lexicon LEARNED from the verse-aligned corpus (O le Tusi
        # Paia beside the KJV; scripts/learn_bible_lexicon.py), last: only
        # words the two dictionaries lack, each sense confirmed by the verse
        # before the generator writes it
        for name in ("samoan_dictionary.json", "samoan_dictionary_eald.json",
                     "samoan_dictionary_bible.json"):
            try:
                d = json.loads((res / name).read_text(encoding="utf-8"))["entries"]
            except Exception:
                continue
            for k, v in d.items():
                for sense in v:
                    if sense not in merged.setdefault(k, []):
                        merged[k].append(sense)
        _DICT = merged
    return _DICT


def dictionary(form):
    """Every sense the two lexicons give this Samoan word, or ()."""
    return tuple(_dictionary().get((form or '').strip().lower(), ()))


def vocabulary(form):
    """A word this corpus uses that the Book of Mormon never did."""
    return VOCABULARY.get((form or '').strip().lower())


def transliterated(form):
    """The English of a transliterated Nephite term, or None."""
    return TRANSLITERATED.get((form or '').strip().lower())


# ── THE ONE-VOWEL RADICALS ───────────────────────────────────────────────────
# Samoan is built on vowels, so its heaviest grammar sits on single-vowel
# tokens, and each carries several jobs at once. The form cannot tell you which
# -- the same problem lamed, yod, he and mem pose in Hebrew, where a single
# letter is a preposition, a prefix and a radical depending on where it stands.
#
# The failure mode is specific and was measured: the 111,683 curated units
# contain a bare `o` read as almost every English word at some point, so an
# inventory lookup will always find SOMETHING, and whichever reading the verse
# happens to contain wins. Alma 32:21 came out `o`="as" three times.
#
# So a particle does not get a free lookup. It gets a CLOSED SET of readings it
# actually has in the grammar, and the verse chooses among those. Frequency
# only breaks ties. Anything outside the set is not a candidate, however often
# the curation's segmentation happened to park it on this token.
#
# Counts below are from the curation: the first English word of a unit that
# STARTS with this particle, which is the particle's own reading.
READINGS = {
    'o':    ['of'],                              # 2,288 of 3,635
    'a':    ['of'],                              #   843
    # `ma` IS A RADICAL TOO (the user's point). Six jobs, and the count hides
    # five of them behind the sixth: coordinator "and" 12,968, comitative
    # "with" 501 (and 227 of 1,404 in the `ma le` frame alone), plus the
    # phrasal frames below where the preceding word selects the reading.
    'ma':   ['and', 'with', 'as', 'to', 'from'],  # 12,968 / 501 / ...
    'mo':   ['for', 'to'],
    'le':   ['the'],                             # 4,513
    'se':   ['a', 'an', 'one', 'any'],           #   735 / 99 / 58 / 45
    'i':    ['in', 'to', 'upon', 'at', 'on', 'into'],   # 2,708 / 2,146 / 857
    'ia':   ['to', 'him', 'her', 'them', 'that'],#  2,559 / 1,123
    'e':    ['by', 'o', 'who'],                  # ergative / vocative / relative
    'ona':  ['because', 'for', 'his', 'her'],    #   672 / 521 / 162
    'ina':  ['that', 'when', 'after'],           #   889 / 175 / 124
    'pe':   ['or', 'if', 'whether', 'nor'],      #   139 / 120 / 102 / 72
    'nei':  ['these', 'this', 'now'],            #   220 / 15
    'uma':  ['all', 'every'],                    #    65 / 4
    'lava': ['himself', 'themselves', 'yourselves', 'myself', 'itself',
             'ourselves', 'even', 'verily'],     #   187 / 109 / 70
    'lo':   ['their', 'our', 'your'],            #   381 / 100 / 80
    'la':   ['their', 'our'],                    #    65 / 31
    'na':   ['which', 'who', 'that'],            #   332
    'ai':   ['thereto', 'thereof', 'therein', 'thereby'],
    # `aua` is two words. Causal "for/because" is the common one -- `aua
    # faauta` "for behold" alone is 148 -- and before a negator or a bound
    # 2nd-person pronoun it is the PROHIBITIVE, "do not". The imperative is
    # the reading the count hides.
    'aua':  ['for', 'because', 'do not', 'not'],
    'tele': ['great', 'many', 'exceedingly', 'greatly', 'much', 'very'],
    'matua': ['exceedingly', 'fully', 'greatly'],
    'ua':   [],                                  # perfect TAM: absorbed
    # the directionals, with the English the curation gives them
    'atu':  ['forth', 'away', 'out', 'over', 'to', 'unto'],   # forth 170, away 108
    'mai':  ['from', 'forth', 'out', 'here', 'up'],           # from 90, come 356
    'ifo':  ['down', 'downward'],                              # down 126
    'ae':   ['but', 'up', 'yet'],                              # but 187, up 31
    'a’e':  ['up'],
    'ane':  ['by', 'near', 'along', 'across'],                 # by 12, near 8
    # not ambiguous PARTICLES, but forms with two real readings the verse can
    # choose between rather than the grammar guessing one
    'i latou': ['them', 'they'],                 #   515 / 271
    'i laua':  ['them', 'they'],                 #     8 /  11
    'i matou': ['us', 'we'],                     #    50 /  12
    'i tatou': ['us', 'we'],                     #    27 /  10
    'o ia':    ['him', 'he'],                    #   253 / 248
    # the topic frame and the O-class possessive are the same string
    'o outou': ['your', 'you'],                  #    19 "you" /  5 "of you"
    'o matou': ['our', 'we'],
    'o tatou': ['our', 'we'],
    'o latou': ['their', 'they'],                #     9 / 1
    # `au` is the 2sg possessive AND the noun "host, band" -- `au taua` is a
    # band of war. `taua` is that war; `ta’ua`, with the glottal, is the verb
    # "be called" (called 95). Three words the table had as one pronoun.
    'au':      ['your', 'host', 'band', 'army'],
    'e ia':    ['him', 'he'],                    #   113 /  45
    # `ia` itself: a preposition before a name, an object pronoun, a
    # demonstrative, the hortative, and the head of a relative clause when a
    # tense marker follows it (`ia na` 60 of 71 "which", `ia ua` 51 of 56).
    'ia':   ['to', 'him', 'her', 'it', 'them', 'that', 'which', 'let',
             'these', 'those'],
}

# `o` heads the phrase, and when a locative frame already carries the English
# there is nothing left for it to say: `i luga o tagata uma` is "upon all men",
# with `i luga` = "upon" and the `o` silent. Same for the topic `o` that opens
# a clause -- English has no word for it.
SILENT_AFTER = set(COMPLEX_PREPOSITIONS)


# ── READINGS A PARTICLE TAKES ONLY IN A FRAME ────────────────────────────────
# `le` is the article 40,757 times and the NEGATIVE the rest, and the published
# text does not always write the macron that separates them -- Alma 32:21 has
# "e le o le maua", "is not the having", with a bare `le`. Same collapse as an
# unpointed Hebrew text.
#
# Position tells them apart. Measured over the curation, the rate at which a
# `le` in each frame was glossed with a negation:
#
#   ou te le ...   132/132   100%      e le o ...      26/26   100%
#   sa le ...      172/185    93%      ... le toe ...  88/102   86%
#   ua le ...      127/177    72%      ... le mafai   127/218   58%
#   e le <noun>   169/1269    13%   <- the article, and the common case
#
# The frame PROPOSES the negative; the verse still has to carry a negation
# before it is written, so the 72% and 58% frames cost nothing when wrong.
# the tens and the round numbers, for the `<ten> ma le <n>` compound
NUMERAL_TENS = {'sefulu', 'luasefulu', 'tolusefulu', 'fasefulu', 'limasefulu',
                'onosefulu', 'fitusefulu', 'valusefulu', 'ivasefulu',
                'selau', 'afe', 'miliona', 'lua', 'tolu', 'fa', 'lima', 'ono',
                'fitu', 'valu', 'iva'}

LE_NEG_BEFORE = {'te', 'sa', 'ua', 'na', 'latou', 'outou', 'matou', 'tatou',
                 'ou', 'oe', 'ia', 'ta', 'lua', 'lautou'}
LE_NEG_AFTER = {'toe', 'mafai', 'salamo'}

CLAUSE_END = ',;:.!?—'


_POSITIONAL = None


def _positional():
    """Positional readings learned from the curation by build_positional.py.

    The hand-written frames below were each found the same way -- split a
    particle's witnesses by the CLASS of the token before it and see which
    English goes with which class -- and doing that by hand, one form at a
    time, is the wrong way to use a 111,683-unit record. This is the same
    procedure run over every closed-class form at once.
    """
    global _POSITIONAL
    if _POSITIONAL is None:
        import json
        from pathlib import Path
        p = (Path(__file__).resolve().parent.parent /
             "O le Tusi a Mamona Interlinear" / "Resources" /
             "positional_readings.json")
        try:
            _POSITIONAL = json.loads(p.read_text(encoding="utf-8"))["readings"]
        except Exception:
            _POSITIONAL = {}
    return _POSITIONAL


def token_class(tok):
    """What KIND of word this is -- the classes the frames turned out to need."""
    t = (tok or '').strip().lower()
    if not t:
        return "START"
    if t in TAM:
        return "TAM"
    if t in POSSESSIVES:
        return "POSSESSIVE"
    if t in PRONOUNS:
        return "PRONOUN"
    if t in ARTICLE_HEADS:
        return "ARTICLE"
    if t in PREPOSITIONS or t in COMPLEX_PREPOSITIONS:
        return "PREP"
    if t in DEGREE or t in COMPARATIVE:
        return "DEGREE"
    if t in CLOSED_CLASS or t in AMBIGUOUS:
        return "PARTICLE"
    return "OPEN"


# What stands before a main-clause past marker: conjunctions, the linkers that
# open a clause, and the fronted subject pronoun (`o ia na fai` "he did").
NA_TAM_BEFORE = {'ma', 'ona', 'a', 'ae', 'aua', 'auā', 'ina', 'lea', 'ia', 'foi',
                 'afai', 'peitai', 'peita’i', 'peitaʻi'}


def contextual_reading(form, prev=None, nxt=None, clause_initial=False):
    """A reading this particle takes only in this frame, or None.

    Returning '' means SILENT: the frame carries the English already, and the
    particle adds no word of its own.
    """
    f = (form or '').strip().lower()
    p = (prev or '').strip().lower()
    n = (nxt or '').strip().lower()

    if f == 'le':
        if p in LE_NEG_BEFORE or (p == 'e' and n == 'o') or n in LE_NEG_AFTER:
            return 'not'
        return None

    if f == 'ia' and clause_initial and n and n not in PRONOUNS and n not in ('te',):
        # THE OPTATIVE. Clause-initial `Ia malamalama` is "Let there be light",
        # `Ia salamo outou` "repent ye": the curation puts the imperative on the
        # verb and the marker says "let" where English has it, nothing where it
        # does not. Left to its readings it printed "that" and "it".
        return 'let'

    if f == 'na':
        # THE PAST-TENSE MARKER before anything else. `na` sits in three tables
        # -- the TAM (past), the bound pronoun (`ua na fai` "he did", `na te
        # fai` "he does"), and the curation's relative readings which/who/that
        # -- and only the position tells them apart. Left to the readings, a
        # clause-initial `Na alu` came out "that": 410 main-clause past
        # markers in the Bible glossed as relatives, and `Na faia e le Atua`
        # firing for nothing. Clause-initial, or after a conjunction or a
        # fronted subject, it opens a main clause: the tense rides on the verb
        # and the marker says no word of its own. After a TAM it is the
        # pronoun. Before `te` the inventory's frame decides. After a noun it
        # may open a relative clause, where which/who/that still stand.
        if n == 'te':
            return None
        if clause_initial or p in NA_TAM_BEFORE:   # before the TAM test: `ia` is
            return ''                                # the fronted pronoun here
        if p in TAM or p == 'te':
            return 'he'
        return None

    if f == 'o':
        # The topic/presentative `o` opens a clause and English has no word
        # for it: `O le faatuatua e ...` is "Faith is ...", not "Of faith".
        if clause_initial:
            return ''
        # after a locative frame the preposition already said it
        if p in ('luga', 'lalo', 'totonu', 'luma', 'fafo', 'tua'):
            return ''
        return None

    if f in ('tele', 'matua', 'matuā'):
        # STRESS AGAIN, read off what it modifies. `gatete tele ai o ia` is
        # "he trembled EXCEEDINGLY" -- the intensifier on a verb -- while the
        # same word after a particle is the quantity "many". Curated:
        #   e tele 298 "many"            olioli tele 51 "great joy /
        #   le tele 171 "many of"                        rejoice exceedingly"
        #   sa tele  29 "were many"      faanoanoa tele 42 "exceedingly
        #                                                   sorrowful"
        if p and (p in CLOSED_CLASS or p in AMBIGUOUS):
            return 'many'
        if p:
            return 'exceedingly'
        return None

    if f == 'lava':
        # STRESS, AND IT TAKES ITS SENSE FROM WHAT IT STRESSES. Four readings,
        # each fixed by the preceding word (curated witnesses in brackets):
        #   after a PRONOUN    the reflexive   latou lava "themselves" [148]
        #                                      ia lava "himself" [70]
        #   after a POSSESSIVE "own"           lona lava "his own" [54]
        #   after a DEGREE word "even"         oo lava "even to" [46]
        #                                      pei lava "even as" [40]
        #   alone              "verily"        [25]
        # `ma lona loto atoa lava` carries the possessive AND the stress:
        # "with all his own heart".
        if p in PRONOUNS:
            person = PRONOUNS[p][0].split()[0]
            return {'1sg': 'myself', '2sg': 'yourself', '3sg': 'himself',
                    '1pl.excl': 'ourselves', '1pl.incl': 'ourselves',
                    '2pl': 'yourselves', '3pl': 'themselves',
                    '1du.excl': 'ourselves', '1du.incl': 'ourselves',
                    '2du': 'yourselves', '3du': 'themselves'}.get(person)
        if p in POSSESSIVES:
            return 'own'
        if p in DEGREE or p in COMPARATIVE or p in ('oo', 'faapea', 'atoa'):
            return 'even'
        return None

    if f in ('ae', 'a’e'):
        # THE GLOTTAL IS NOT ALWAYS WRITTEN (the user: "sometimes youll see
        # them with glutters others you wont the ae sometimes should be a’e").
        # So `ae` the conjunction "but" and `a’e` the upward directional "up"
        # arrive as one token, exactly like `le`/`lē`. Position separates them:
        # the conjunction OPENS a clause -- the curation glosses a unit that is
        # just `ae` as "but" 187 times -- and the directional FOLLOWS its verb,
        # where the curation ends 31 units on it with "up".
        if clause_initial or p in ('', 'ma', 'ona', 'ioe'):
            return 'but'
        if p and p not in CLOSED_CLASS and p not in AMBIGUOUS:
            return 'up'
        return None

    if f == 'aua':
        if n in ('le', 'lē', 'ne’i', 'nei', 'tou', 'nea'):
            return 'do not'
        if n == 'faauta':
            return 'for'
        return None

    if f == 'ia':
        # a tense marker after it makes a relative clause
        if n in ('na', 'ua', 'sa'):
            return 'which'
        if p == 'ina':
            return 'that'
        if p == 'lava':
            return 'himself'
        # under the topic, the ergative or the dative it is the object pronoun
        if p in ('o', 'e', 'ma', 'te'):
            return 'him'
        return None

    if f == 'o le a':
        # THE FUTURE, AND ALSO "WHAT" -- and the user's account of why: "theres
        # many ways to use it because of uncertainty and not knowing what or if
        # its that person's". The uncertainty is carried by the NON-SPECIFIC
        # series, which is why `o le a se mea` asks "what is that thing" while
        # `o le a alu` simply says "shall go":
        #
        #   o le a se mea     ->  "And WHAT will ye do..."
        #   o le a sa latou   ->  a question
        #   o le a sa outou   ->  a question
        #   o le a le         ->  59 questions against 67 futures -- a coin
        #                         flip, which is exactly why the VERSE decides
        #   everything else   ->  1-6% questions; the future
        #
        # `sau` is excluded: it is the verb "come", not `sa’u` the possessive,
        # and `o le a sau mai` is "there shall come".
        #
        # Proposing "what" costs nothing when it is wrong, because a frame's
        # answer is only written if the verse actually carries the word.
        if n == 'le' or (n in NON_SPECIFIC and n != 'sau'):
            return 'what'
        return 'shall'

    if f == 'ona':
        # before a tense marker or the topic `o` it is causal; before a noun
        # it is the possessive. `ona o` is 607 "because" of 824, `ona ua` 127
        # "for" of 197, `ona tagata` 78 "his" of 85.
        if n in ('o', 'ua', 'sa', 'na', 'e', 'te', 'latou', 'ou', 'outou',
                 'matou', 'tatou', 'ia'):
            return 'because'
        if n and n not in CLOSED_CLASS and n not in AMBIGUOUS:
            return 'his'
        return None

    if f == 'ma':
        # THE PRECEDING WORD SELECTS THE READING. Each of these is a phrasal
        # frame whose English preposition belongs to the `ma`, not to the word
        # in front of it -- `faatasi` is "together", `ma le tama` is "with the
        # boy". Curated counts: tusa 410, faatasi 96+70, avea 73, aunoa 24.
        if p == 'faatasi':
            return 'with'
        if p == 'tusa':
            return 'to'
        if p == 'avea':
            return 'as'
        if p == 'aunoa':
            return 'from'
        # in a compound numeral it is always the conjunction: `sefulu ma le
        # tasi` is "ten and one"
        if p in NUMERAL_TENS:
            return 'and'
        return None

    if f == 'e':
        # the ergative marks an AGENT, which is a person or a name; before a
        # verb the same token is the non-past TAM and says nothing
        return None

    # NOTHING HAND-WRITTEN COVERS THIS FORM -- fall back to what the curation
    # settles positionally on its own. The hand frames above win because they
    # were checked against the text one by one; this was not.
    return _positional().get(f, {}).get(token_class(p))


def _alternatives(desc):
    """The comma-separated alternatives in a table entry, as readings."""
    txt = desc[-1] if isinstance(desc, tuple) else desc
    out, seen = [], set()
    for part in re.sub(r"\([^)]*\)", "", str(txt)).split(','):
        # the parenthetical is a note to whoever reads this file -- "exceedingly
        # (intensifier)" was becoming a candidate reading and could never match
        # any verse
        w = part.strip().strip('.').lower()
        # a gloss, not a description: "marks the agent of a transitive verb"
        # is prose and must not become a candidate reading
        if not w or len(w.split()) > 3 or ':' in w or w.startswith('the same'):
            continue
        if w not in seen:
            seen.add(w); out.append(w)
    return out


def _build_alt_readings():
    """EVERY grammar entry that offers alternatives lets the verse choose.

    `i luga` is "upon, over, on top of" and the code took the first, always --
    so the corpus said "upon" 773 times and "over" almost never, while the
    curation says "over" in 90% of the verses whose English has it and this
    pass managed 14%. The alternatives were already written down; nothing was
    reading past the first comma.
    """
    out = {}
    for table in (COMPLEX_PREPOSITIONS, DIRECTIONALS, POSTVERBAL, NEGATION,
                  COORDINATORS, DISCOURSE, COMPARATIVE, DEGREE, DISJUNCTIVE,
                  SUBORDINATORS, MODALS, CAUSAL, DEMONSTRATIVES, PREPOSITIONS,
                  VERB_ONA, INTERROGATIVES):
        for form, desc in table.items():
            alts = _alternatives(desc)
            if len(alts) > 1:
                out[form] = alts
    return out


_ALT_READINGS = None


# A FRAME CAN REPLACE THE WHOLE READING SET, not just pick from it. `o` after
# a tense marker is not the linking particle at all -- it is the VERB "go,
# come": the curation glosses `na o` "who went / went forth / came", `sa o`
# "came / went forth", `ua o` "had come / were coming / and departed", `e o`
# "to go / to come". Nothing else in this file could say that, because every
# other mechanism here picks among a form's own readings.
FRAME_READINGS = {
    ('o', 'TAM'): ('come', 'go', 'came', 'went', 'gone', 'departed', 'coming'),
}


def readings_in_frame(form, prev=None):
    """A reading set that belongs to this frame, or () for the usual one."""
    f = (form or '').strip().lower()
    p = (prev or '').strip().lower()
    if p in TAM or p in ('te',):
        hit = FRAME_READINGS.get((f, 'TAM'))
        if hit:
            return hit
    return ()


def particle_readings(form):
    """The closed set of readings for a form, or ().

    READINGS first -- those are hand-checked against the curation -- then the
    alternatives the grammar tables already list.
    """
    global _ALT_READINGS
    f = (form or '').strip().lower()
    if f in READINGS:
        return tuple(READINGS[f])
    if _ALT_READINGS is None:
        _ALT_READINGS = _build_alt_readings()
    return tuple(_ALT_READINGS.get(f, ()))


# Two different jobs, and conflating them cost real segmentation.
#
# PHRASE_LINKERS are the particles that open a NEW phrase in the middle of
# one: `i luga o motu` is "upon" + "of the isles", `O le Tusi a Mamona` is
# "The Book" + "of Mormon". A unit may not run THROUGH one.
#
# PHRASE_INITIAL is the wider set that may not END a unit -- an article or a
# preposition left hanging off the back has taken the next phrase's first
# word. But those same words are perfectly at home INSIDE a phrase: `o le
# agalelei` is "of the goodness", one unit, and barring it as "contains `le`"
# broke every ordinary noun phrase in the corpus into dangling heads.
PHRASE_LINKERS = {'o', 'a'}
ARTICLE_HEADS = {'le', 'se', 'ni'}
PHRASE_INITIAL = {'o', 'a', 'i', 'le', 'se', 'ma', 'mo', 'ni'}

# Forms where one of those tokens is not the head it usually is. `po o` is one
# disjunctive marker (the user's ruling); `o le a` is the future; `pe a` is
# temporal; and in the possessive paradigm `ma` is the 1st-dual pronoun, not
# the comitative preposition.
PHRASE_RULE_EXCEPTIONS = {'po o', 'o le a', 'pe a', 'e tusa ma'}


def splits_a_phrase(unit):
    """Does this unit run through the head of a phrase that follows it?"""
    toks = (unit or '').strip().lower().split()
    key = ' '.join(toks)
    if len(toks) < 2 or key in PHRASE_RULE_EXCEPTIONS:
        return False
    # A form the grammar lists is ONE form by definition -- `o le mea lea`
    # "wherefore" is lexicalised and its `le` is not an article heading
    # anything. The rule is about spans someone PROPOSED, not about entries.
    if key in _build_primary() or key in POSSESSIVES:
        return False
    if toks[-1] in PHRASE_INITIAL:
        return True
    # ONE ARTICLE TO A PHRASE. The head is not always `o` -- it can be `i le`,
    # `a le`, or a bare `le`, and the user's point is that the `o` is often
    # simply omitted. So the article itself marks the boundary: a SECOND
    # `le`/`se`/`ni` inside a unit means a second noun phrase has begun.
    #
    # The corpus is emphatic about this. Of 111,683 curated units, 74.0% carry
    # no article at all, 25.3% carry exactly one, and 0.8% carry two or more --
    # and most of that 0.8% is already split by the linker rule below
    # (`le afioga a le atua`, `le alii o le togāolive`).
    if sum(1 for t in toks if t in ARTICLE_HEADS) > 1:
        return True

    # a linker opens a new phrase -- unless a tense marker precedes it, where
    # `o` is the verb "go/come" and `na o mai ai` is one thing, "there came"
    return any(t in PHRASE_LINKERS and toks[i - 1] not in TAM
               for i, t in enumerate(toks) if i)


# kept under the old name for callers written against it
def ends_mid_phrase(unit):
    return splits_a_phrase(unit)


def _build_primary():
    if _PRIMARY:
        return _PRIMARY
    _PRIMARY['o le a'] = 'shall'
    # the progressive is a predicate marker, not an absorbed particle;
    # number comes from the verse (english_register.stems knows is/are)
    for f in ('o lo’o', 'o loo', 'loo'):
        _PRIMARY[f] = 'is'
    for form, (_spec, _num, gloss) in ARTICLES.items():
        _PRIMARY.setdefault(form, gloss)
    for form, (_person, gloss) in PRONOUNS.items():
        _PRIMARY.setdefault(form, gloss)
    for table in (COMPLEX_PREPOSITIONS, DIRECTIONALS, POSTVERBAL, NEGATION,
                  COORDINATORS, DISCOURSE, COMPARATIVE, DEGREE, DISJUNCTIVE,
                  SUBORDINATORS, MODALS, CAUSAL, DEMONSTRATIVES, PREPOSITIONS,
                  VERB_ONA, INTERROGATIVES):
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
# ── GAGANA FA’AALOALO, the respectful register ───────────────────────────────
# The chiefly vocabulary, and in this corpus it is the DIVINE register: these
# are the words the scriptures use of God. The entries below marked "Pratt"
# were taken from his dictionary, which flags a chiefly word in its definition
# ("a chief's voice", "to speak. Used of chiefs", "life. (Chiefs word.)") --
# 110 such entries, of which 21 occur here. The web has almost nothing: the
# pages on gagana fa’aaloalo give a handful of pairs (maota/fale, suafa/igoa,
# afio/sau, soifua/ola) and no list.
RESPECTFUL = {
    # `foliga` is the respectful word for a face -- `o le foliga o le Atua` is
    # "the face of God", where `mata` would be the ordinary word. The corpus
    # also uses it for image/form/likeness, which is the same root sense.
    'foliga': ('mata', 'face, image, likeness'),
    'afioga':    ('upu', 'word, address'),          # Pratt; 294 in the corpus
    'soifua':    ('ola', 'life, live'),             # Pratt "life. (Chiefs word.)"
    'fetalaiga': ('upu', 'word, speech'),           # Pratt "a chief's speech"
    'malolo':    ('malolo', 'rest'),                # 25
    'susuga':    ('igoa', 'address, title'),        # the form for teachers, ministers
    'tofa':      ('moe', 'sleep'),                  # Pratt "to sleep, of chiefs"
    'laufofoga': ('mata', 'face'),                  # Pratt "a chief's eyelids"
    'sisila':    ('vaai', 'look, see, know'),       # Pratt "(a chief's word)"
    'lauao':     ('lauulu', 'hair'),                # Pratt "a chief's hair"
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


# Every construction the grammar knows that is longer than one token. The
# segmenter needs these to avoid cutting through one: a remembered unit that
# ends on `i` when the text reads `i luga` has taken the preposition's head.
MULTI_FORMS = {f for f in _build_primary() if len(f.split()) > 1}
MULTI_FORMS |= {f for f in COMPLEX_PREPOSITIONS if len(f.split()) > 1}
MULTI_FORMS |= {f for f in TAM if len(f.split()) > 1}
MAX_FORM_LEN = max(len(f.split()) for f in MULTI_FORMS)
