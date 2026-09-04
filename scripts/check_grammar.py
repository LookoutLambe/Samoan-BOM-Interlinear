#!/usr/bin/env python3
"""Check the hand-curated glosses against samoan_grammar.py.

239 per-chapter scripts curated by hand cannot be self-consistent, and until
now nothing could measure them, because there was no rule to measure against.
These checks need almost no vocabulary -- they are grammar, so they apply to
every verse in the book.

  --articles   Samoan articles mark SPECIFICITY, not definiteness: `le` is
               "the" and `se` is "a". A `se` phrase glossed "the" (or a `le`
               phrase glossed "a") is wrong on the grammar alone.
  --drift      one Samoan unit, more than one English gloss, across chapters.
  --units      the atomic units the corpus uses, ranked, for review.
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import samoan_grammar as SG

R = os.path.join(os.path.dirname(HERE), 'O le Tusi a Mamona Interlinear', 'Resources')
CONT = '·'


def load():
    with open(os.path.join(R, 'bom_overrides.json'), encoding='utf-8') as fh:
        return json.load(fh)['verses']


def norm(s):
    return re.sub(r'\s+', ' ', (s or '').strip())


def units(words):
    """Yield (samoan_unit, english, index) — a run of continuation markers plus
    the token that carries the gloss."""
    i = 0
    while i < len(words):
        if norm(words[i].get('en')) == CONT:
            j = i
            while j < len(words) and norm(words[j].get('en')) == CONT:
                j += 1
            if j < len(words):
                yield (' '.join(x['sm'] for x in words[i:j + 1]),
                       norm(words[j].get('en')), i)
                i = j + 1
                continue
            i = j
            continue
        en = norm(words[i].get('en'))
        if en:
            yield (words[i]['sm'], en, i)
        i += 1


def clean(sm):
    return re.sub(r'[^\wʻ’\- ]+', '', sm).lower().strip()


def check_articles(V):
    """The specificity rule, on units that are EXACTLY article + noun.

    Loosely applied this fires on anything: `se tasi o atalii` is glossed "one
    of the sons" and contains "the", but that "the" belongs to *atalii*, not to
    *se* -- the unit holds two noun phrases. So the check is restricted to a
    two-token unit, optionally opened by `o`/`i`/`ma`, whose gloss is a bare
    article + word. Then the article in the gloss can only be rendering the
    article in the Samoan, and the comparison is real.

    Reported separately, because they are not equally diagnostic:

      se/ni glossed "the"  -- CREDIBLE. A non-specific article rendered
                              definite says the phrase introduces a referent
                              the English then treats as known.
      le glossed "a"       -- EXPECTED, and reported only for review. Samoan
                              `le` marks SPECIFICITY, not definiteness, so a
                              specific-but-newly-introduced referent is
                              naturally "a" in English: `le tagata` -> "a man"
                              is right. This class is informational.
    """
    bad = []
    OPENERS = ('o', 'i', 'ma', 'e', 'mai')
    for key, words in V.items():
        for sm, en, i in units(words):
            toks = clean(sm).split()
            if toks and toks[0] in OPENERS:
                toks = toks[1:]
            if len(toks) != 2:
                continue                      # not a bare article + noun
            art = toks[0]
            g = re.sub(r'[^\w ]+', '', en).strip().lower().split()
            if len(g) != 2:
                continue                      # not a bare article + word
            det = g[0]
            if art == 'se' and det == 'the':
                bad.append((key, sm, en, 'se (non-specific) glossed "the"'))
            elif art == 'ni' and det == 'the':
                bad.append((key, sm, en, 'ni (non-specific pl) glossed "the"'))
            elif art == 'le' and det in ('a', 'an'):
                bad.append((key, sm, en, 'le (specific) glossed "a" [review]'))
    return bad


def check_drift(V, minimum=8):
    seen = defaultdict(Counter)
    where = defaultdict(list)
    for key, words in V.items():
        for sm, en, i in units(words):
            k = clean(sm)
            if k:
                seen[k][en] += 1
                where[k].append(key)
    out = []
    for k, c in seen.items():
        tot = sum(c.values())
        if tot < minimum or len(c) < 2:
            continue
        # a capitalisation-only difference is sentence position, not drift
        folded = Counter()
        for g, n in c.items():
            folded[g.lower()] += n
        if len(folded) < 2:
            continue
        out.append((k, tot, folded, where[k][:1]))
    out.sort(key=lambda x: -x[1])
    return out


def main(argv):
    V = load()
    if '--articles' in argv or not argv:
        bad = check_articles(V)
        print('ARTICLE SPECIFICITY — %d violations\n' % len(bad))
        for key, sm, en, why in bad[:40]:
            print('   %-18s %-34s %-30r %s' % (key, sm[:34], en, why))
        print()
    if '--drift' in argv:
        d = check_drift(V)
        print('UNIT DRIFT — %d units glossed more than one way (n>=8)\n' % len(d))
        for k, tot, c, ex in d[:40]:
            print('   %-30s n=%-5d %s' % (k[:30], tot,
                  '  '.join('%r:%d' % (g, n) for g, n in c.most_common(3))))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
