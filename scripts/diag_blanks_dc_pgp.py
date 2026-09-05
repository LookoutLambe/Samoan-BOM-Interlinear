"""Replay the generator's decision loop over D&C/PGP only, recording WHY each blank unit stayed blank."""
import sys,re,json,collections,textwrap
sys.path.insert(0,'scripts')
import generate_overrides_dc_pgp as G
src=open('scripts/generate_overrides_dc_pgp.py',encoding='utf8').read()
body=src[src.index('    units = load_evidence()'):src.index('                attach_particles(out, toks)')]
body=body.replace('stats["unit: " + why] += 1','REC(key_sm, why, gloss, toks, i, hit, key)')
body=body.replace('if book.get("volume") not in ("bom", "dc", "pgp"):','if book.get("volume") not in ("dc", "pgp"):')
body=textwrap.dedent(body)
REC_rows=[]
def REC(key_sm, why, gloss, toks, i, hit, key):
    if not gloss:
        prev=toks[i-1] if i else '^'; nxt=toks[i+hit] if i+hit<len(toks) else '$'
        REC_rows.append((key_sm, why, prev, nxt, key))
class A: dry_run=True; limit=0
ns=dict(vars(G)); ns.update({'REC':REC,'a':A(),'print':lambda *x,**k:None})
exec(body, ns)
print('blank units recorded:', len(REC_rows))
byform=collections.Counter(r[0] for r in REC_rows)
bywhy=collections.Counter(r[1] for r in REC_rows)
print('\nWHY (all blank units):'); [print(f'  {n:6} {w}') for w,n in bywhy.most_common(20)]
print('\nTOP BLANK FORMS with their why + 3 contexts:')
for f,n in byform.most_common(36):
    whys=collections.Counter(r[1] for r in REC_rows if r[0]==f)
    ctx=[(r[2],r[3]) for r in REC_rows if r[0]==f][:3]
    print(f'{n:5} {f:14} {dict(whys.most_common(3))}  {ctx}')

# ---- per-token view: expand each blank unit into its tokens and give the why per form
import samoan_grammar as SG
def nt(s): return re.sub(r"[^\w’\- ]","",SG.normalise_glottal(s)).lower().strip()
per=collections.defaultdict(collections.Counter); units_of=collections.defaultdict(collections.Counter)
for key_sm,why,prev,nxt,key in REC_rows:
    for t in nt(key_sm).split():
        per[t][why]+=1; units_of[t][key_sm]+=1
print('\nPER-TOKEN why for the forms of interest:')
for f in ['lē','latou','outou','oulua','oe','po','tatou','ou','tatau','lea','lava','ai','ae','atu','mai','faapea','leai','toe','fia','ao','mafai','tele','matua','mea','uiga','luma','faavavau','isi','ese','atoa','misiona','tagata','faia','oo','fai','tuu','nofo','molimau','sui','maota','lalolagi','ea','taitasi']:
    print(f'{f:10} {sum(per[f].values()):5} {dict(per[f].most_common(4))}  units: {dict(units_of[f].most_common(4))}')
json.dump(REC_rows, open(sys.argv[1],'w'), ensure_ascii=False) if len(sys.argv)>1 else None
