"""A transliterated name is matched to the English name in its own verse by consonant skeleton.
Validated first on the curated Book of Mormon name pairs, then dry-run on the D&C/PGP blanks."""
import sys,re,json,collections,difflib
sys.path.insert(0,'scripts')
import samoan_grammar as SG
R='O le Tusi a Mamona Interlinear/Resources/'
SM_MAP={'k':'k','g':'k','q':'k','c':'k','s':'s','z':'s','t':'t','d':'t','p':'p','b':'p','f':'f','v':'v','w':'v','l':'l','r':'l','m':'m','n':'n','h':'h','j':'y','y':'y','x':'ks'}
def skel_sm(w):
    w=SG.normalise_glottal(w).lower(); w=re.sub(r"[^a-z]","",w)
    # initial i- before a vowel spells English j/y (Iosefa, Iakopo, Iareto)
    if re.match(r'^i[aeou]',w): w='y'+w[1:]
    return ''.join(SM_MAP.get(c,'') for c in w if c not in 'aeiou')
EN_MAP={'c':'k','k':'k','q':'k','g':'k','s':'s','z':'s','t':'t','d':'t','p':'p','b':'p','f':'f','v':'v','w':'v','l':'l','r':'l','m':'m','n':'n','h':'h','j':'y','y':'y','x':'ks'}
def skel_en(w):
    w=w.lower(); w=re.sub(r'ph','f',w); w=re.sub(r'th','t',w); w=re.sub(r'ch','k',w); w=re.sub(r'sh','s',w); w=re.sub(r'ck','k',w); w=re.sub(r'(.)\1',r'\1',w)
    w=re.sub(r"[^a-z]","",w)
    return ''.join(EN_MAP.get(c,'') for c in w if c not in 'aeiouy' or False)
def best_match(sm, en_caps):
    s=skel_sm(sm)
    if not s: return None,0
    best=(None,0.0)
    for e in en_caps:
        r=difflib.SequenceMatcher(None,s,skel_en(e)).ratio()
        if r>best[1]: best=(e,r)
    return best
STOP={'And','Behold','Wherefore','For','But','Yea','Now','Therefore','Thus','Verily','Amen','O','The','Let','Which','What','It','If','He','She','They','We','I','Be','Hearken','Saying','Listen','Go','Come','Lord','God','Spirit','Holy','Ghost','Christ','Father','Son','Redeemer','Jesus','Israel','Zion','Jun','Mc'}
ev=json.load(open(R+'curated_evidence.json',encoding='utf8'))['units']
books=json.load(open(R+'bom_books.json',encoding='utf8'))['books']
en=json.load(open(R+'bom_english.json',encoding='utf8'))
ov=json.load(open(R+'bom_overrides.json',encoding='utf8'))
vol={b['id']:b.get('volume') for b in books}; name={b['id']:b['nameEn'] for b in books}
# ---- validation on curated name pairs: gold = curated English for single capitalised tokens
gold=collections.Counter()
for sm,e in ev:
    s=re.sub(r"[^\w’\- ]","",sm).strip(); g=re.sub(r"[^\w’\- ]","",e).strip()
    if ' ' in s or ' ' in g or not s or not g: continue
    if s[:1].isupper() and g[:1].isupper() and g not in STOP and s.lower()!=g.lower(): gold[(s,g)]+=1
gold_by_sm={}
for (s,g),n in gold.items():
    gold_by_sm.setdefault(s,collections.Counter())[g]+=n
right=wrong=nomatch=0; errs=[]
for bk in books:
    if vol[bk['id']]!='bom': continue
    for ch in bk['chapters']:
        for v in ch['verses']:
            E=en.get(f"{bk['nameEn']}|{ch['num']}|{v['num']}","")
            caps=[w for w in re.findall(r"[A-Z][a-z']+",E) if w not in STOP]
            for i,w in enumerate(v['words']):
                if i==0: continue
                t=re.sub(r"[^\w’\-]","",w['sm'])
                if t in gold_by_sm and caps:
                    g=gold_by_sm[t].most_common(1)[0][0]
                    m,r=best_match(t,caps)
                    if m is None or r<0.5: nomatch+=1
                    elif m==g: right+=1
                    else:
                        wrong+=1
                        if len(errs)<25: errs.append((t,g,m,round(r,2)))
print(f'VALIDATION on curated names: right {right}  wrong {wrong}  no-match {nomatch}  precision {100*right/max(1,right+wrong):.1f}%')
print('sample errors (samoan, gold, chosen, ratio):', errs)
# ---- dry run on D&C/PGP blank capitalised tokens
prop=collections.Counter(); ident=collections.Counter(); miss=collections.Counter()
for k,words in ov['verses'].items():
    bid,ch,vn=k.split('|')
    if vol.get(bid) not in ('dc','pgp'): continue
    E=en.get(f"{name[bid]}|{ch}|{vn}","")
    caps=[w for w in re.findall(r"[A-Z][a-z']*",E) if w not in STOP]
    for i,w in enumerate(words):
        if (w['en'] or '')!='' or not w['sm'][:1].isupper(): continue
        t=re.sub(r"[^\w’\-]","",w['sm'])
        if len(t)<=2 or t in ('Ou','Au','A’u','O','E','Ia','Ma'): continue
        if t in re.findall(r"[A-Z][a-z']*",E): ident[t]+=1; continue
        m,r=best_match(t,caps)
        if m and r>=0.5: prop[(t,m)]+=1
        else: miss[t]+=1
print(f'\nD&C/PGP: identity {sum(ident.values())} tokens/{len(ident)} types; matched {sum(prop.values())}/{len(prop)}; unmatched {sum(miss.values())}/{len(miss)}')
print('PROPOSED (n, samoan -> english):')
for (t,m),n in prop.most_common(60): print(f'  {n:4} {t:16} -> {m}')
print('UNMATCHED top:', miss.most_common(30))
