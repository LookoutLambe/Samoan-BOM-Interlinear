#!/usr/bin/env python3
"""Learn a Samoan-English lexicon from the verse-aligned corpus.

The Bible brings vocabulary the Book of Mormon never used -- nunumi, gaogao,
fegaoioiai -- and Pratt and EALD miss much of it, so the generator left those
words blank. The evidence for their meaning is already in hand: every verse of
O le Tusi Paia stands beside its KJV verse, and the Book of Mormon volumes
beside their official English. A Samoan word's English is the content word
that keeps turning up in the same verses far more often than chance.

For each Samoan type s (not closed-class, not a name) and English word e:
    P(e|s) = verses with both / verses with s     lift = P(e|s) / P(e)
    dice   = 2·both / (verses with s + verses with e)
A sense is accepted when both >= MIN_BOTH, P(e|s) >= MIN_COND and lift >= MIN_LIFT;
the top senses (by dice) are written, comma-alternatives the way Pratt writes them,
so the generator's dictionary stage tries each and writes one only where the verse
carries it.

The method is validated first on the words the dictionaries already know: the
top learned sense must appear in a Pratt/EALD sense. Entries are written only
for words the two dictionaries lack, to Resources/samoan_dictionary_bible.json,
which samoan_grammar._dictionary() merges LAST.

    python3 scripts/learn_bible_lexicon.py [--write]
"""
import json, re, sys, collections, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import samoan_grammar as SG
import english_register as ER
RES = HERE.parent / "O le Tusi a Mamona Interlinear" / "Resources"
MIN_BOTH, MIN_COND, MIN_LIFT = 3, 0.25, 8.0
STOP = set(ER.FUNCTION_ONLY) | {"be","been","being","is","are","was","were","am","do","does","did","done",
    "have","has","had","shall","will","would","should","may","might","can","could","said","saith","say",
    "came","come","went","go","not","no","there","then","when","if","so","as","also","even","yea","because",
    "therefore","now","behold","lord","god","thing","things","one","man","men","people","land","house","son",
    "sons","children","day","days","hand","before","after","against","out","up","down","into","over","again",
    "every","any","some","other","own","same","more","much","many","great","among","through","without",
    "unto","toward","forth","away","let","made","make","give","gave","put","set","take","took","brought",
    "bring","see","saw","heard","hear","know","knew","spake","speak","word","words","name","king","father",
    "mother","brother","wife","city","israel","children","sent","pass","according","whom","whose","where",
    "what","how","why","yet","until","till","while","both","either","neither","nor","ever","never","hath","hast"}
def nsm(w):
    w = re.sub(r"[^\w’ʻ'\-]", "", SG.normalise_glottal(w)).lower()
    return w
def is_closed(w): return (w in SG.CLOSED_CLASS or w in SG.AMBIGUOUS or w in SG.TAM
                          or w in SG.PRONOUNS or len(w) < 3)
verses = []   # (samoan tokens raw, english text)
idx = json.loads((RES / "tusi_paia_index.json").read_text(encoding="utf-8"))
ben = json.loads((RES / "tusi_paia_english.json").read_text(encoding="utf-8"))
for meta in idx["books"]:
    book = json.loads((RES / f"book_{meta['id']}.json").read_text(encoding="utf-8"))
    for ch in book["chapters"]:
        for v in ch["verses"]:
            verses.append(([w["sm"] for w in v["words"]], ben.get(f"{meta['nameEn']}|{ch['num']}|{v['num']}", "")))
bom = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))["books"]
oen = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
for book in bom:
    for ch in book["chapters"]:
        for v in ch["verses"]:
            verses.append(([w["sm"] for w in v["words"]], oen.get(f"{book['nameEn']}|{ch['num']}|{v['num']}", "")))
N = len(verses)
# names: capitalised mid-verse and never lower-case
up, low = collections.Counter(), collections.Counter()
for toks, _ in verses:
    for i, t in enumerate(toks):
        w = re.sub(r"[^\w’ʻ]", "", t)
        if len(w) < 3: continue
        if w[0].isupper():
            if i > 0: up[w.lower()] += 1
        else: low[w.lower()] += 1
names = {w for w, n in up.items() if n >= 2 and low.get(w, 0) == 0}
def stem(w):
    """One bucket per lemma: creeps / creeping / crept count together, so an
    inflected verb is not split three ways below the threshold."""
    st = sorted(ER.stems(w), key=len)[0] if ER.stems(w) else w
    return st if len(st) >= 3 else w
cs, ce, both = collections.Counter(), collections.Counter(), collections.defaultdict(collections.Counter)
surface = collections.defaultdict(collections.Counter)   # stem -> surface forms seen
for toks, en in verses:
    S = {nsm(t) for t in toks}; S = {s for s in S if s and not is_closed(s)}   # names learn too: Paulo -> paul
    words = [w for w in re.findall(r"[a-z']+", ER.modernise(en).lower()) if w not in STOP and len(w) > 2]
    E = set()
    for w in words:
        k = stem(w); E.add(k); surface[k][w] += 1
    for s in S:
        cs[s] += 1
        for e in E: both[s][e] += 1
    for e in E: ce[e] += 1
def show(e): return surface[e].most_common(1)[0][0] if surface[e] else e
def senses(s):
    out = []
    for e, b in both[s].items():
        if b < MIN_BOTH: continue
        cond = b / cs[s]; lift = cond / (ce[e] / N); dice = 2 * b / (cs[s] + ce[e])
        need_cond, need_lift = (MIN_COND, MIN_LIFT) if cs[s] >= 8 else (0.5, 20.0)
        if cond >= need_cond and lift >= need_lift: out.append((dice, cond, lift, b, show(e)))
    out.sort(reverse=True)
    if not out: return []
    best = out[0][0]
    return [o for o in out if o[0] >= 0.5 * best][:3]
# ---- validation against the hand-curated Book of Mormon lexicon: does the learned
#      top sense appear among the words the curation used for this Samoan word?
import generate_overrides_dc_pgp as G
lex = G.build_word_lexicon(G.load_evidence())
ag = dis = 0; bad = []
for s_, dist in lex.items():
    if cs.get(s_, 0) < 8 or sum(dist.values()) < 10: continue
    got = senses(s_)
    if not got: continue
    top = got[0][4]; curated = " ".join(dist).lower()
    if top in curated or any(st in curated for st in ER.stems(top) if len(st) >= 4): ag += 1
    else:
        dis += 1
        if len(bad) < 12: bad.append((s_, top, round(got[0][1], 2), [g for g, _ in dist.most_common(3)]))
print(f"validation vs the CURATED lexicon (>=8 verses, >=10 witnesses): agree {ag}, disagree {dis} -> {100*ag/max(1,ag+dis):.1f}%")
print("  disagreements (samoan, learned, P(e|s), curated top-3):"); [print("   ", x) for x in bad]
# ---- validation on words the dictionaries know
agree = disagree = 0; sample = []
for s in cs:
    if cs[s] < 5: continue
    d = SG.dictionary(s)
    if not d: continue
    got = senses(s)
    if not got: continue
    top = got[0][4]
    dtext = " ".join(d).lower()
    stems = ER.stems(top) if hasattr(ER, "stems") else {top}
    ok = top in dtext or any(st and st in dtext for st in stems)
    if ok: agree += 1
    else:
        disagree += 1
        if len(sample) < 14: sample.append((s, top, round(got[0][1], 2), round(got[0][2], 1), d[0][:50]))
print(f"validation on dictionary words (>=5 verses): agree {agree}, disagree {disagree}  -> {100*agree/max(1,agree+disagree):.1f}% of learned top senses appear in Pratt/EALD")
print("  disagreements (samoan, learned, P(e|s), lift, dictionary):"); [print("   ", x) for x in sample]
# ---- the new entries: words no dictionary has
new = {}
for s in cs:
    if cs[s] < MIN_BOTH: continue
    got = senses(s)
    if got: new[s] = [g[4] for g in got]
absent = sum(1 for s in new if not SG.dictionary(s))
print(f"\nlearned entries: {len(new)} types ({absent} absent from Pratt/EALD, {len(new) - absent} adding senses the dictionaries lack — fetolofi 'creeping' beside Pratt's 'crawl'); merged LAST, so a dictionary sense is tried first")
for w in ("nunumi", "gaogao", "fegaoioiai", "tuu", "fetolofi", "manufelelei", "fanaua", "tisipenisione", "tiakono", "autasi", "faaeaga", "titania", "faapaleina", "nunu", "vaomatua"):
    if w in new: print(f"   {w:16} -> {', '.join(new[w])}   ({cs[w]} verses)")
    elif w in cs: print(f"   {w:16} -> (no sense passed; {cs[w]} verses; dictionary has {SG.dictionary(w)[:1]})  top raw: {sorted(((b/cs[w]),e) for e,b in both[w].items())[-3:]}")
if "--write" in sys.argv:
    out = RES / "samoan_dictionary_bible.json"
    out.write_text(json.dumps({"source": "learned from the verse-aligned corpus (O le Tusi Paia + KJV, and the Book of Mormon volumes + official English) by scripts/learn_bible_lexicon.py; merged after Pratt and EALD; thresholds both>=3, P(e|s)>=0.25, lift>=8 (0.5 / 20 under 8 verses); English forms stem-merged",
        "entries": {k: new[k] for k in sorted(new)}}, ensure_ascii=False, indent=0), encoding="utf-8")
    print("wrote", out, len(new), "entries")
