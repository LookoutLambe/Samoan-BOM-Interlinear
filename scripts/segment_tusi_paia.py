"""Segment the OCR'd Samoan Bible (page-ordered text) into KJV-numbered verses.
Anchors: running heads (book), inline verse numbers, uppercase title runs (book titles,
"O LE SALAMO N (M)" headings); the KJV verse counts constrain chapter breaks. Unnumbered
spans are split at punctuation in proportion to the KJV verse lengths and flagged est."""
import re,json,sys,difflib,collections,statistics
from pathlib import Path
D=Path(__file__).resolve().parent.parent/'corpus'/'tusi_paia'
K=json.load(open(D/'english_ot_nt.json',encoding='utf8')); KV=K['verses']; KC=K['counts']
OT=[('KENESE','Genesis'),('ESOTO','Exodus'),('LEVITIKO','Leviticus'),('NUMERA','Numbers'),('TEUTERONOME','Deuteronomy'),('IOSUA','Joshua'),('FAAMASINO','Judges'),('RUTA','Ruth'),('I SAMUELU','1 Samuel'),('II SAMUELU','2 Samuel'),('I TUPU','1 Kings'),('II TUPU','2 Kings'),('I NOFOAIGA A TUPU','1 Chronicles'),('II NOFOAIGA A TUPU','2 Chronicles'),('ESERA','Ezra'),('NEEMIA','Nehemiah'),('ESETA','Esther'),('IOPU','Job'),('SALAMO','Psalms'),('FAATAOTO','Proverbs'),('FAILAUGA','Ecclesiastes'),('LE PESE A SOLOMONA','Song of Songs'),('ISAIA','Isaiah'),('IEREMIA','Jeremiah'),('AUEGA','Lamentations'),('ESEKIELU','Ezekiel'),('TANIELU','Daniel'),('HOSEA','Hosea'),('IOELU','Joel'),('AMOSA','Amos'),('OPETAIA','Obadiah'),('IONA','Jonah'),('MIKA','Micah'),('NAUMA','Nahum'),('SAPAKUKA','Habakkuk'),('SEFANAIA','Zephaniah'),('HAKAI','Haggai'),('SAKARIA','Zechariah'),('MALAKI','Malachi')]
NT=[('MATAIO','Matthew'),('MAREKO','Mark'),('LUKA','Luke'),('IOANE','John'),('GALUEGA','Acts'),('ROMA','Romans'),('I KORINITO','1 Corinthians'),('II KORINITO','2 Corinthians'),('KALATIA','Galatians'),('EFESO','Ephesians'),('FILIPI','Philippians'),('KOLOSE','Colossians'),('I TESALONIA','1 Thessalonians'),('II TESALONIA','2 Thessalonians'),('I TIMOTEO','1 Timothy'),('II TIMOTEO','2 Timothy'),('TITO','Titus'),('FILEMONI','Philemon'),('EPERU','Hebrews'),('IAKOPO','James'),('I PETERU','1 Peter'),('II PETERU','2 Peter'),('I IOANE','1 John'),('II IOANE','2 John'),('III IOANE','3 John'),('IUTA','Jude'),('FAAALIGA','Revelation')]
BOOKS=OT+NT
for s,e in BOOKS: assert e in KC, e
# title phrases that open a book in this edition
TITLE_KEY={'MOSE':None,'SAMUELU':None,'TUPU':None,'NOFOAIGA':None}
CYR={'о':'o','а':'a','е':'e','і':'i','п':'n','т':'t','А':'A','и':'u','ш':'w','р':'p','О':'O','й':'u','у':'y','с':'c','г':'r','І':'I','ї':'i','ё':'e','Т':'T','д':'d','ч':'4','л':'n','ќ':'k','Ш':'W','ә':'e','ѕ':'s','П':'P','Е':'E','ј':'j','М':'M','б':'6','з':'3','ц':'u','€':'E','Н':'H','К':'K','С':'C','В':'B','Р':'P','х':'x','к':'k','в':'v','н':'n','ь':'b','м':'m','Х':'X','У':'Y','Ј':'J','Ѕ':'S','Ф':'F','Л':'L','Д':'D','Б':'B','Г':'G','З':'3','И':'U'}
def latin(s): return ''.join(CYR.get(c,c) for c in s)
t=open(D/'tusi_paia_numbered_pages.txt',encoding='utf8').read()
pages=re.split(r'\n@@PAGE page_(\d+)\.html\n',t)[1:]
P=sorted((int(pages[i]),latin(pages[i+1])) for i in range(0,len(pages),2))
HEAD=re.compile(r'^\s*((?:I{1,3}\s+)?[A-Z][A-Z]+(?:\s+[A-Z]{2,})*)\s+(\d+)(?:\s*[,.]\s*\d+)*\s*')
def head_book(s):
    m=HEAD.match(s)
    if not m: return None,0
    name=m.group(1).strip(); best=max(((difflib.SequenceMatcher(None,name,sn).ratio(),i) for i,(sn,en) in enumerate(BOOKS)))
    return (best[1] if best[0]>=0.72 else None), m.end()
toks=[]
for pn,txt in P:
    bi,end=head_book(txt)
    body=txt[end:] if bi is not None else txt
    body=re.sub(r'\s+\d{1,4}\s*$','',body)
    toks.extend(body.split())
# ---- pass 1: find title runs (>=3 consecutive uppercase tokens, allowing numerals/parens) and verse numbers
def isup(w): return bool(re.fullmatch(r"[A-Z][A-Z'’]+|[IVX]+|\(?\d+\)?|[A-Z]",w)) and not re.fullmatch(r'\d+',w)
def isnum(w):
    w=w.replace('$','5'); return int(w) if re.fullmatch(r'\d{1,3}',w) else None
N=len(toks)
titles={}  # start index -> (end index, kind, book index or psalm no)
i=0
while i<N:
    if toks[i]=='O' and i+2<N and toks[i+1]=='LE' and isup(toks[i+2]):
        j=i+2
        while j<N and (isup(toks[j]) or re.fullmatch(r'\(?\d+\)?[,.]?',toks[j])): j+=1
        run=' '.join(toks[i:j])
        if j-i>=3:
            m=re.search(r'SALAMO\s+(\d+)',run)
            if m: titles[i]=(j,'psalm',int(m.group(1)))
            else:
                # which book does this title open?
                names=run
                best=(0,None)
                for k,(sn,en) in enumerate(BOOKS):
                    r=difflib.SequenceMatcher(None,names,sn).ratio()
                    if sn in names: r=1.0
                    if r>best[0]: best=(r,k)
                titles[i]=(j,'title',best[1] if best[0]>=0.5 else None, run)
        i=j
    else: i+=1
# ---- pass 2: walk with state; emit runs (book, chapter, verse_anchor, tokens)
runs=[]      # dicts: b, c, v (anchored number, or None for a chapter head), toks, kind
bi=0; ch=1; v=1; cur=[]; kind='verse'
def emit(): 
    global cur
    runs.append({'b':bi,'c':ch,'v':v,'toks':cur,'kind':kind}); cur=[]
def exp(): return KC[BOOKS[bi][1]].get(str(ch),0)
def nch(): return len(KC[BOOKS[bi][1]])
i=0; notes=[]
# The book titles decide book order; explicit titles give the sequence. Chapter starts inside a book
# are recognised by the verse counter: a "2" (or "1") after the chapter's expected last verse.
while i<N:
    if i in titles:
        tinfo=titles[i]; j=tinfo[0]
        emit()
        if tinfo[1]=='psalm':
            if bi!=18: notes.append(f'psalm heading outside Psalms at {i}')
            bi=18; ch=tinfo[2]; v=1; kind='head'
        else:
            k=tinfo[2]
            if k is not None and k!=bi:
                if k<bi or k>bi+2: notes.append(f'title jump {BOOKS[bi][1]} -> {BOOKS[k][1]}: {tinfo[3]}')
                bi=k; ch=1
            elif k is None: notes.append(f'unknown title: {tinfo[3]}')
            else: notes.append(f'repeat title in {BOOKS[bi][1]}: {tinfo[3]}')
            v=1; kind='head'
        i=j; continue
    n=isnum(toks[i])
    if n is not None:
        if n==v+1 or (n==v+2 and n<=exp()):
            emit(); v=n; kind='verse'
            if n==v+2: notes.append(f'{BOOKS[bi][1]} {ch}: verse {v-1} number missing')
        elif n in (1,2) and v>=max(2,exp()-2):
            # chapter boundary without a title: the run holds verse v + summary + verse 1
            emit()
            if ch>=nch():
                if bi+1<len(BOOKS): notes.append(f'book end without title: {BOOKS[bi][1]} -> {BOOKS[bi+1][1]}'); bi+=1; ch=1
                else: break
            else: ch+=1
            v=1; kind='head' if n==2 else 'verse'
            if n==1: kind='head'; runs.append({'b':bi,'c':ch,'v':1,'toks':[],'kind':'head'}); kind='verse'
        i+=1; continue
    cur.append(toks[i]); i+=1
emit()
json.dump({'runs':runs,'notes':notes,'books':[e for s,e in BOOKS]},open(D/'segment_runs.json','w',encoding='utf8'),ensure_ascii=False)
# ---- report
seen=collections.defaultdict(lambda:collections.defaultdict(set))
for r in runs: seen[BOOKS[r['b']][1]][r['c']].add(r['v'])
for s,e in BOOKS:
    chs=KC[e]; ok=sum(1 for c in chs if len(seen[e].get(int(c),()))>=chs[c]-1)
    print(f'{e:18} chapters {len(seen[e]):3}/{len(chs):3}  chapters with (nearly) all verse numbers {ok:3}')
print(len(notes),'notes'); print('\n'.join(notes[:40]))
