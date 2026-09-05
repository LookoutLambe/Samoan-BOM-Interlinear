"""Segment the OCR'd Samoan Bible (page-ordered text) into KJV-numbered verses.

Sources: corpus/tusi_paia/tusi_paia_numbered_pages.txt (the verse-numbered edition) and
corpus/tusi_paia/english_ot_nt.json (the 31,161-verse English column from the Hebrew app,
with per-chapter verse counts). Output: corpus/tusi_paia/tusi_paia_verses.json.

Two passes, so that a miscounted chapter can never spill into the next book:
  PASS A — books. Every maximal uppercase run is a title candidate ("O LE TUSI E LUA A MOSE",
     "TUSI I FAAMASINO", "o GALUEGA A LE AU APOSETOLO", "0 SALAMO"); keywords assign it to the
     next book in canonical order. A book with no title starts at the first page whose running
     head names it (flagged).
  PASS B — chapters inside each book span. Inline verse numbers anchor verses (the OCR's l/I for 1,
     O/o for 0, $ for 5; "lo" is 10 unless it is the possessive particle). A chapter opens at a
     title, at a Psalm heading ("O LE SALAMO", numbered or not), at a "1"/"2" after the chapter's
     last expected verse, or wherever the numbers restart (a 1..5 smaller than the counter whose
     look-ahead continues n+1, n+2). A chapter head = summary line + unnumbered verse 1; the
     summary is cut off by the English verse-1 length. Unnumbered spans are filled proportionally
     to the English verse lengths at punctuation and flagged est.
Footnotes (numbered 1, 2, 3 at a page's end — "1 O le upu Eperu, ...") are stripped first.
"""
import re, json, sys, difflib, collections, statistics
from pathlib import Path
D = Path(__file__).resolve().parent.parent / 'corpus' / 'tusi_paia'
K = json.load(open(D / 'english_ot_nt.json', encoding='utf8')); KV = K['verses']; KC = K['counts']

# (running-head name, English, title keywords — every keyword must appear (fuzzily) in the title run;
#  '+1' = MUAMUA or ULUAI; '-X' = X must be absent)
BOOKS = [
 ('KENESE','Genesis',['MUAMUA','MOSE']), ('ESOTO','Exodus',['LUA','MOSE']), ('LEVITIKO','Leviticus',['TOLU','MOSE']),
 ('NUMERA','Numbers',['FA','MOSE']), ('TEUTERONOME','Deuteronomy',['LIMA','MOSE']), ('IOSUA','Joshua',['IOSUA']),
 ('FAAMASINO','Judges',['FAAMASINO']), ('RUTA','Ruth',['RUTA']), ('I SAMUELU','1 Samuel',['MUAMUA','SAMUELU']),
 ('II SAMUELU','2 Samuel',['LUA','SAMUELU']), ('I TUPU','1 Kings',['TUPU','+1','-NOFOAIGA']), ('II TUPU','2 Kings',['LUA','TUPU','-NOFOAIGA']),
 ('I NOFOAIGA A TUPU','1 Chronicles',['MUAMUA','NOFOAIGA']), ('II NOFOAIGA A TUPU','2 Chronicles',['LUA','NOFOAIGA']),
 ('ESERA','Ezra',['ESERA']), ('NEEMIA','Nehemiah',['NEEMIA']), ('ESETA','Esther',['ESETA']), ('IOPU','Job',['IOPU']),
 ('SALAMO','Psalms',['SALAMO']), ('FAATAOTO','Proverbs',['FAATAOTO']), ('FAILAUGA','Ecclesiastes',['FAILAUGA']),
 ('LE PESE A SOLOMONA','Song of Solomon',['PESE']), ('ISAIA','Isaiah',['ISAIA']), ('IEREMIA','Jeremiah',['PEROFETA','IEREMIA','-AUEGA']),
 ('AUEGA','Lamentations',['AUEGA']), ('ESEKIELU','Ezekiel',['ESEKIELU']), ('TANIELU','Daniel',['TANIELU']), ('HOSEA','Hosea',['HOSEA']),
 ('IOELU','Joel',['IOELU']), ('AMOSA','Amos',['AMOSA']), ('OPETAIA','Obadiah',['OPETAIA']), ('IONA','Jonah',['IONA']),
 ('MIKA','Micah',['MIKA']), ('NAUMA','Nahum',['NAUMA']), ('SAPAKUKA','Habakkuk',['SAPAKUKA']), ('SEFANAIA','Zephaniah',['SEFANAIA']),
 ('HAKAI','Haggai',['HAKAI']), ('SAKARIA','Zechariah',['SAKARIA']), ('MALAKI','Malachi',['MALAKI']),
 ('MATAIO','Matthew',['MATAIO']), ('MAREKO','Mark',['MAREKO']), ('LUKA','Luke',['LUKA']), ('IOANE','John',['EVAGELIA','IOANE']),
 ('GALUEGA','Acts',['GALUEGA']), ('ROMA','Romans',['ROMA']), ('I KORINITO','1 Corinthians',['MUAMUA','KORINITO']),
 ('II KORINITO','2 Corinthians',['LUA','KORINITO']), ('KALATIA','Galatians',['KALATIA']), ('EFESO','Ephesians',['EFESO']),
 ('FILIPI','Philippians',['FILIPI']), ('KOLOSE','Colossians',['KOLOSE']), ('I TESALONIA','1 Thessalonians',['MUAMUA','TESALONIA']),
 ('II TESALONIA','2 Thessalonians',['LUA','TESALONIA']), ('I TIMOTEO','1 Timothy',['TIMOTEO','+1']), ('II TIMOTEO','2 Timothy',['LUA','TIMOTEO']),
 ('TITO','Titus',['TITO']), ('FILEMONI','Philemon',['FILEMONI']), ('EPERU','Hebrews',['EPERU']), ('IAKOPO','James',['IAKOPO']),
 ('I PETERU','1 Peter',['MUAMUA','PETERU']), ('II PETERU','2 Peter',['LUA','PETERU']), ('I IOANE','1 John',['IOANE','+1','-EVAGELIA','-FAAALIGA']),
 ('II IOANE','2 John',['LUA','IOANE']), ('III IOANE','3 John',['TOLU','IOANE']), ('IUTA','Jude',['IUTA']), ('FAAALIGA','Revelation',['FAAALIGA']),
]
for s, e, _ in BOOKS: assert e in KC, e
ENG = [e for s, e, _ in BOOKS]; PSALMS = ENG.index('Psalms')
CYR = {'о':'o','а':'a','е':'e','і':'i','п':'n','т':'t','А':'A','и':'u','ш':'w','р':'p','О':'O','й':'u','у':'u','с':'c','г':'r','І':'I','ї':'i','ё':'e','Т':'T','д':'d','ч':'4','л':'n','ќ':'k','Ш':'W','ә':'e','ѕ':'s','П':'P','Е':'E','ј':'j','М':'M','б':'6','з':'3','ц':'u','€':'E','Н':'H','К':'K','С':'C','В':'B','Р':'P','х':'x','к':'k','в':'v','н':'n','ь':'b','м':'m','Х':'X','У':'Y','Ј':'J','Ѕ':'S','Ф':'F','Л':'L','Д':'D','Б':'B','Г':'G','З':'3','И':'U'}
def latin(s): return ''.join(CYR.get(c, c) for c in s)

# ---------------------------------------------------------------- pages -> tokens
t = open(D / 'tusi_paia_numbered_pages.txt', encoding='utf8').read()
pages = re.split(r'\n@@PAGE page_(\d+)\.html\n', t)[1:]
P = sorted((int(pages[i]), latin(pages[i + 1])) for i in range(0, len(pages), 2))
HEAD = re.compile(r'^\s*(?:(?:I{1,3}|\d)\.?\s+)?([A-Z][A-Z]+(?:\s+[A-Z]+)*)(?:\s+\d+(?:\s*[,.]\s*\d+)*)?(?:\s+\[[^\]]*\])?\s+')
def head_of(s):
    m = HEAD.match(s)
    if not m: return None, 0, []
    name = m.group(1).strip()
    if name in ('O', 'LE', 'TUSI'): return None, 0, []
    chs = [int(x) for x in re.findall(r'\d+', m.group(0)[len(name):])] if m.group(0).strip() else []
    best = max(((max(difflib.SequenceMatcher(None, name, sn).ratio(), difflib.SequenceMatcher(None, name, sn.split()[-1]).ratio(), difflib.SequenceMatcher(None, name.split()[-1], sn.split()[-1]).ratio()), i) for i, (sn, en, _) in enumerate(BOOKS)))
    return (best[1] if best[0] >= 0.72 else None), m.end(), chs
FOOT = []
def strip_footnotes(body):
    L = len(body)
    for m in re.finditer(r'(?<!\S)1 (?=[A-Z“‘])', body):
        if m.start() < int(L * 0.72): continue
        tail = body[m.start():]
        nums = [int(x) for x in re.findall(r'(?<!\S)(\d+)(?!\S)', tail)]
        if not nums or nums != sorted(nums) or max(nums) > 5 or len(set(nums)) != len(nums): continue
        if re.search(r'O le upu|o lona uiga|gagana (Eperu|Eleni)|, o Ise|ta[‘’]ua', tail) or len(tail) < 70:
            FOOT.append(tail); return body[:m.start()].rstrip()
    return body
toks = []; page_of_tok = []; head_bk = {}; first_tok_of_page = {}; head_chs_at = {}
for pn, txt in P:
    bi, end, chs = head_of(txt)
    body = txt[end:] if bi is not None else txt
    body = re.sub(r'\s+\d{1,4}\s*$', '', body)
    body = strip_footnotes(body)
    head_bk[pn] = bi; first_tok_of_page[pn] = len(toks)
    if bi is not None and chs: head_chs_at[len(toks)] = (bi, [c for c in chs if 1 <= c <= 176])
    ws = body.split(); toks.extend(ws); page_of_tok.extend([pn] * len(ws))
N = len(toks)

PRON_AFTER_LO = {'latou','matou','tatou','outou','laua','maua','taua','oulua','la','ma','ta','u','’u',"'u"}
def isnum(w, nxt=''):
    if w == 'lo' and nxt.lower().strip('.,;:') in PRON_AFTER_LO: return None
    if not re.fullmatch(r"[0-9lIO$o]{1,3}", w): return None
    if not (re.search(r'[\d$]', w) or w in ('lo','IO','ll','Il','lI','lO','II')): return None
    d = w.replace('$', '5').replace('l', '1').replace('I', '1').replace('O', '0').replace('o', '0')
    if not re.fullmatch(r'\d{1,3}', d): return None
    n = int(d); return n if 1 <= n <= 176 else None
def at_boundary(i):
    """a verse number sits at a verse boundary: capitalised next word, or punctuation before"""
    j = i + 1
    while j < N and toks[j] in ('“','‘','"',"'",'’','(','—','-'): j += 1
    if j < N and re.match(r"[“‘\"'’(]*[A-Z]", toks[j]): return True
    return i > 0 and bool(re.search(r"[.,;:?!][”’\"')]*$", toks[i - 1]))
def num_at(i):
    n = isnum(toks[i], toks[i + 1] if i + 1 < N else '')
    return n if (n is not None and at_boundary(i)) else None
def lookahead_ok(i, n, need=2, limit=None):
    """the next `need` verse-number tokens after i continue n+1, n+2 ... in sequence; ONE number may
    be skipped (an OCR-damaged verse number), but a number out of sequence fails outright"""
    want = n + 1; got = 0; j = i + 1; skipped = False; stop = min(N, i + 900, limit if limit else N)
    while j < stop and got < need:
        m = num_at(j)
        if m is not None:
            if m == want: got += 1; want += 1
            elif m == want + 1 and not skipped: skipped = True; got += 1; want = m + 1
            else: return False
        j += 1
    return got >= need
def isup(w): return bool(re.fullmatch(r"[A-Z][A-Z'’]+|[IVX]+\.?|\(?\d+\)?[,.]?|[A-Z]|0|o", w))

# ---------------------------------------------------------------- PASS A: books from titles
def kw_in(kw, run): return any(kw == w or (len(w) >= 4 and difflib.SequenceMatcher(None, kw, w).ratio() >= 0.8) for w in run)
TITLE_WORDS = {'TUSI','EVAGELIA','PEROFETA','PESE','SALAMO','GALUEGA','FAAALIGA','FAATAOTO','AUEGA','FAILAUGA'}
def title_shaped(run):
    ws = [w.strip('.,()') for w in run]
    return bool(TITLE_WORDS & set(ws)) or any(difflib.SequenceMatcher(None, w, 'TUSI').ratio() >= 0.75 for w in ws) or ws[:2] in (['O','LE'],['0','LE'])
def title_book(run_tokens, bi, reach=4):
    run = [w.strip('.,()') for w in run_tokens]
    for k in range(bi + 1, min(bi + 1 + reach, len(BOOKS))):
        ok = True
        for kw in BOOKS[k][2]:
            if kw == '+1': ok &= (kw_in('MUAMUA', run) or kw_in('ULUAI', run))
            elif kw.startswith('-'): ok &= not kw_in(kw[1:], run)
            else: ok &= kw_in(kw, run)
        if ok: return k
    return None
upruns = []   # (start, end) maximal uppercase runs of >= 2 tokens
i = 0
while i < N:
    if isup(toks[i]) and not re.fullmatch(r'\(?\d+\)?[,.]?', toks[i]):
        j = i
        while j < N and isup(toks[j]): j += 1
        if j - i >= 2: upruns.append((i, j))
        i = j
    else: i += 1
book_start = {}   # k -> (start_tok, text_start_tok, how)
bi = -1; notes = []
for (a, b) in upruns:
    run = toks[a:b]
    if not title_shaped(run): continue
    if bi < PSALMS <= bi + 4 and kw_in('SALAMO', run):
        book_start[PSALMS] = (a, a, 'title'); bi = PSALMS; continue   # the heading stays: pass B reads it
    k = title_book(run, bi)
    if k is None and run[-2:] == ['TUSI', 'A'] and b < N:
        k = title_book(run + [toks[b].upper()], bi)
        if k is not None: b += 1
    if k is None: continue
    if k != bi + 1: notes.append(f'title skipped {k - bi - 1} book(s): {ENG[bi] if bi >= 0 else "-"} -> {ENG[k]} ({" ".join(run)})')
    book_start[k] = (a, b, 'title'); bi = k
for k in range(len(BOOKS)):
    if k in book_start: continue
    pn = next((p for p, h in sorted(head_bk.items()) if h == k), None)
    if pn is None: notes.append(f'NO START for {ENG[k]}'); continue
    s = first_tok_of_page[pn]; book_start[k] = (s, s, 'head'); notes.append(f'{ENG[k]} starts at page {pn} by running head (no title)')
order = sorted(book_start.items(), key=lambda kv: kv[1][0])
spans = []
for idx, (k, (a, b, how)) in enumerate(order):
    end = order[idx + 1][1][0] if idx + 1 < len(order) else N
    spans.append((k, b, end, how))
if [k for k, *_ in spans] != sorted(k for k, *_ in spans): notes.append('BOOK ORDER VIOLATION ' + str([ENG[k] for k, *_ in spans]))

# ---------------------------------------------------------------- PASS B: chapters inside each book
SENT_RE = re.compile(r'[.?!]["’”)]?\s')
R_EST = 1.05   # Samoan chars per English char, measured on the clean anchored verses
runs = []
def walk_book(bi, start, end):
    book = ENG[bi]; count = len(KC[book])
    ch = 1; v = 0; cur = []; kind = 'head'
    def exp(): return KC[book].get(str(ch), 0)
    def emit(k=None):
        nonlocal cur
        runs.append({'b': bi, 'c': ch, 'v': v, 'toks': cur, 'kind': k or kind}); cur = []
    i = start; cur_start = start; ch_chars = 0; ch_of_chars = ch
    def emit2(k=None):
        nonlocal cur_start, ch_chars, ch_of_chars
        if ch != ch_of_chars: ch_chars = 0; ch_of_chars = ch
        ch_chars += len(' '.join(cur)) + 1
        emit(k); cur_start = i
    def expected_chapter_chars():
        return sum(len(KV.get(f'{book}|{ch}|{q}', '')) or 60 for q in range(1, KC[book].get(str(ch), 0) + 1)) * R_EST
    while i < end:
        if i in head_chs_at and book != 'Psalms':
            hb, hchs = head_chs_at[i]
            if hb == bi and hchs and ch < min(hchs) <= ch + 2 and v >= 1:
                # the running head says a later chapter has begun. Trust it only when this chapter's text
                # has already reached its expected length (a head that lost its first number reads the same)
                have = (ch_chars if ch == ch_of_chars else 0) + len(' '.join(cur))
                want_all = expected_chapter_chars()
                if have >= 0.9 * want_all:
                    over = have - want_all
                    txt = ' '.join(cur)
                    cut_chars = max(0, len(txt) - int(over)) if over > 0 else len(txt)
                    min_keep = int(sum(len(KV.get(f'{book}|{ch}|{q}', '')) or 60 for q in range(v, KC[book].get(str(ch), 0) + 1)) * R_EST * 0.9)
                    cut_chars = max(cut_chars, min(len(txt), min_keep))
                    pts = [m.end() for m in SENT_RE.finditer(txt)]
                    p = min(pts, key=lambda p: abs(p - cut_chars)) if pts else cut_chars
                    if abs(p - cut_chars) > 0.25 * max(1, len(txt)): p = cut_chars
                    head_toks = txt[:p].split(); tail_toks = txt[p:].split()
                    runs.append({'b': bi, 'c': ch, 'v': v, 'toks': head_toks, 'kind': 'tailhead'})
                    notes.append(f'{book}: running head says chapter {min(hchs)} at a page start while at {ch} (chapter {have / max(1, want_all):.2f} full) -> size-cut break')
                    cur = tail_toks; ch = min(hchs); v = 0; kind = 'head'; cur_start = i; ch_chars = 0; ch_of_chars = ch
        if book == 'Psalms' and toks[i] in ('O', '0', 'o') and i + 2 < end and toks[i + 1] == 'LE' and toks[i + 2].startswith('SALAMO'):
            j = i + 3; num = None
            while j < end and re.fullmatch(r'\(?\d+\)?[,.]?|[IVX]+', toks[j]):
                m = re.fullmatch(r'(\d+)', toks[j])
                if m and num is None: num = int(m.group(1))
                j += 1
            had_text = bool(cur) or v > 0
            emit2()
            if num is not None and ch <= num <= ch + 3: ch = num
            elif had_text: ch += 1
            v = 0; kind = 'head'; i = j; continue
        n = num_at(i)
        if n is not None:
            e = exp()
            if v == 0 and 2 <= n <= e and (n == 2 or lookahead_ok(i, n, 1, end)):
                emit2('head'); v = n; kind = 'verse'; i += 1; continue
            if v >= 1 and n == v + 1 and n <= e:
                emit2('verse'); v = n; i += 1; continue
            if v >= 1 and v + 1 < n <= e and lookahead_ok(i, n, 1, end):
                notes.append(f'{book} {ch}: verse numbers {v + 1}-{n - 1} missing'); emit2('verse'); v = n; i += 1; continue
            # a chapter break needs the numbers to RESTART and continue: a bare "1" is usually the
            # OCR's reading of the particle "i", so it never opens a chapter on its own
            opens = bool(re.match(r"[“‘\"'’(]*[A-Z]", toks[i + 1])) if i + 1 < N else False
            opens = opens or (i > 0 and bool(re.search(r"[.?!;:][”’\"')]*$", toks[i - 1])))
            restart = opens and ((n <= 5 and n < v and lookahead_ok(i, n, 2, end)) or
                                 (n == 2 and v >= e - 2 and lookahead_ok(i, n, 2, end)) or
                                 (n == 1 and v >= e - 2 and lookahead_ok(i, n, 2, end)))
            if v >= 1 and restart:
                emit2('tailhead'); ch += 1
                if ch > count: notes.append(f'{book}: chapter {ch} beyond its {count}')
                v = n if n >= 2 else 0; kind = 'verse' if n >= 2 else 'head'; i += 1; continue
            i += 1; continue
        cur.append(toks[i]); i += 1
    emit()
    if ch < count: notes.append(f'{book}: only {ch} of {count} chapters found')
for (k, b, end, how) in spans: walk_book(k, b, end)

if '--find' in sys.argv:
    needle = sys.argv[sys.argv.index('--find') + 1]
    for r in runs:
        txt = ' '.join(r['toks'])
        if needle in txt:
            q = txt.find(needle); print(f"{ENG[r['b']]} {r['c']}:{r['v']} {r['kind']} [{len(r['toks'])} toks] ...{txt[max(0, q - 200):q + 120]}...")
    sys.exit(0)
if '--text' in sys.argv:
    a = sys.argv.index('--text'); bk = sys.argv[a + 1]; chs = set(int(x) for x in sys.argv[a + 2:])
    for r in runs:
        if ENG[r['b']] == bk and r['c'] in chs and (r['kind'] != 'verse' or len(r['toks']) > 120):
            txt = ' '.join(r['toks']); print(f"\n{bk} {r['c']} v={r['v']} {r['kind']} [{len(r['toks'])} toks]\n{txt[:1100]}")
    sys.exit(0)
if '--debug' in sys.argv:
    a = sys.argv.index('--debug'); bk = sys.argv[a + 1]; chs = set(int(x) for x in sys.argv[a + 2:])
    for r in runs:
        if ENG[r['b']] == bk and r['c'] in chs:
            print(f"{bk} {r['c']} v={r['v']:<3} {r['kind']:8} [{len(r['toks'])}] {' '.join(r['toks'][:9])} ... {' '.join(r['toks'][-4:])}")
    sys.exit(0)

# ---------------------------------------------------------------- assemble verses
SENT = re.compile(r'[.?!]["’”)]?\s'); SENT_RE = SENT; CLAUSE = re.compile(r'[;:,]["’”)]?\s')
def cut_points(text, strong=True): return [m.end() for m in (SENT if strong else CLAUSE).finditer(text) if 0 < m.end() < len(text)]
def cap_after_lower(text): return [m.start(1) for m in re.finditer(r"[a-z’'](?:\s+)([A-Z][a-z’']+)", text)]
def nearest(pts, target, tol):
    best = None
    for p in pts:
        if abs(p - target) <= tol and (best is None or abs(p - target) < abs(best - target)): best = p
    return best
def split_prop(text, weights):
    if len(weights) == 1: return [text]
    total = sum(weights) or 1; L = len(text); strong = cut_points(text); weak = cut_points(text, False)
    pieces = []; start = 0; acc = 0
    for w in weights[:-1]:
        acc += w; target = round(L * acc / total)
        p = nearest([x for x in strong if x > start + 1], target, max(12, int(0.25 * L * w / total)))
        if p is None: p = nearest([x for x in weak if x > start + 1], target, max(12, int(0.35 * L * w / total)))
        if p is None: p = max(start + 1, min(L - 1, target))
        pieces.append(text[start:p].strip()); start = p
    pieces.append(text[start:].strip())
    # a piece that is a bare number or a letter or two is a margin numeral or
    # OCR grit, not a verse: it joins its neighbour
    for k in range(len(pieces)):
        if pieces[k] and (len(pieces[k]) < 4 or re.fullmatch(r'[\d\W]+', pieces[k])):
            if k + 1 < len(pieces): pieces[k + 1] = (pieces[k] + ' ' + pieces[k + 1]).strip() if not re.fullmatch(r'[\d\W]+', pieces[k]) else pieces[k + 1]
            elif k: pieces[k - 1] = (pieces[k - 1] + ' ' + pieces[k]).strip() if not re.fullmatch(r'[\d\W]+', pieces[k]) else pieces[k - 1]
            pieces[k] = ''
    if any(not p for p in pieces):
        words = text.split(); n = len(weights); total = sum(weights) or 1
        if len(words) < n: return [text] + [''] * (n - 1)
        cuts = [0]; acc = 0
        for w in weights[:-1]:
            acc += w; cuts.append(max(cuts[-1] + 1, min(len(words) - (n - len(cuts)), round(len(words) * acc / total))))
        cuts.append(len(words))
        pieces = [' '.join(words[a:b]) for a, b in zip(cuts, cuts[1:])]
    return pieces
def strip_title(text):
    m = re.match(r"^(?:(?:[A-Z][A-Z'’]+|[IVX]+|\(?\d+\)?[,.]?|O|LE|A|E|I|0|o)\s+){2,}", text)
    return text[m.end():] if m else text
def en_len(b, c, v): return len(KV.get(f'{b}|{c}|{v}', '')) or 60
def cut_summary(text, want):
    """a chapter head is [summary line] + verse text. The print sets the summary as a line with no
    final stop, so the seam is a lowercase word followed by a capitalised one; the candidate seam
    that leaves the verse text closest to its wanted length wins, sentence ends as the fallback"""
    L = len(text)
    seams = [p for p in cap_after_lower(text) if p <= 320]
    if seams:
        p = min(seams, key=lambda p: abs((L - p) - want))
        if 0.6 * want <= L - p <= 1.7 * want and (L - p) < L: return text[p:].strip()
    if L > want * 1.15:
        cands = [p for p in cut_points(text) if p <= 260]
        if cands:
            p = min(cands, key=lambda p: abs((L - p) - want))
            if abs((L - p) - want) < abs(L - want): return text[p:].strip()
    return text
by_ch = collections.OrderedDict()
for r in runs: by_ch.setdefault((r['b'], r['c']), []).append(r)
ratios = []
for (b, c), rs in by_ch.items():
    for a, nxt in zip(rs, rs[1:]):
        if a['kind'] == 'verse' and nxt['kind'] == 'verse' and nxt['v'] == a['v'] + 1 and a['v'] >= 1:
            e = en_len(ENG[b], c, a['v'])
            if e > 40 and a['toks']: ratios.append(len(' '.join(a['toks'])) / e)
R = statistics.median(ratios) if ratios else 1.1
verses = {}; est_keys = set(); flags = collections.Counter()
def put(b, c, vv, text, est):
    if not text.strip(): return
    key = f'{ENG[b]}|{c}|{vv}'
    verses[key] = (verses[key] + ' ' + text).strip() if key in verses else text.strip()
    if est: est_keys.add(key)
def fill_head(b, c, rest, rs_after):
    book = ENG[b]; e = KC[book].get(str(c), 0)
    if e == 0: return
    first_anchor = next((x['v'] for x in rs_after if x['kind'] == 'verse' and x['v'] >= 1 and x['toks']), e + 1)
    k = max(1, min(first_anchor - 1, e))
    want = sum(en_len(book, c, q) for q in range(1, k + 1)) * R
    body = cut_summary(rest, want)
    for q, piece in zip(range(1, k + 1), split_prop(body, [en_len(book, c, q) for q in range(1, k + 1)])): put(b, c, q, piece, est=True)
keys_order = list(by_ch.keys())
for idx, ((b, c), rs) in enumerate(by_ch.items()):
    book = ENG[b]; e = KC[book].get(str(c), 0)
    if e == 0: flags['chapter beyond count'] += 1; continue
    rs = [r for r in rs if r['kind'] != 'verse' or r['toks']]   # an anchor with no text is a clumped margin number
    for j, r in enumerate(rs):
        text = ' '.join(r['toks']).strip()
        if r['kind'] == 'head':
            fill_head(b, c, strip_title(text), rs[j + 1:]); flags['heads'] += 1
        elif r['v'] >= 1:
            vv = r['v']
            nxt_anchor = next((x['v'] for x in rs[j + 1:] if x['kind'] == 'verse' and x['v'] >= 1 and x['toks']), None)
            if r['kind'] == 'tailhead':
                old_ws = [en_len(book, c, q) for q in range(vv, e + 1)]
                old_want = sum(old_ws) * R
                pts = sorted(set(cut_points(text) + cap_after_lower(text)))
                p = nearest(pts, int(old_want), max(40, int(0.35 * old_want)))
                if p is None: p = min(len(text), int(old_want))
                for q, piece in zip(range(vv, e + 1), split_prop(text[:p], old_ws)): put(b, c, q, piece, est=(q != vv or len(old_ws) > 1))
                rest = strip_title(text[p:].strip())
                if idx + 1 < len(keys_order) and rest:
                    nb, nc = keys_order[idx + 1]
                    if nb == b: fill_head(nb, nc, rest, by_ch[(nb, nc)]); flags['tailheads'] += 1
            elif nxt_anchor is not None and nxt_anchor > vv + 1:
                for q, piece in zip(range(vv, nxt_anchor), split_prop(text, [en_len(book, c, q) for q in range(vv, nxt_anchor)])): put(b, c, q, piece, est=True)
                flags['filled gaps'] += 1
            elif nxt_anchor is None and vv < e and j == len(rs) - 1:
                for q, piece in zip(range(vv, e + 1), split_prop(text, [en_len(book, c, q) for q in range(vv, e + 1)])): put(b, c, q, piece, est=(q != vv))
                flags['filled tails'] += 1
            else: put(b, c, vv, text, est=False)

def clean(text):
    text = text.replace('|', ' ')
    text = re.sub(r'(?<=[a-z’ʻ,;])\s+1\s+(?=[a-z])', ' i ', text)     # "1" for the particle i
    text = re.sub(r'(?<=[a-z’ʻ,;])\s+0\s+(?=[a-z])', ' o ', text)     # "0" for the particle o
    text = re.sub(r'(?<=[a-z’ʻ,;])\s+l\s+(?=[a-z])', ' i ', text)
    text = re.sub(r'(^|[.;:,!?”]\s+)la(?=\s)', r'\1Ia', text)                # "la" for the marker Ia at a clause start
    text = re.sub(r'\b[Ii]le\b', lambda m: m.group(0)[0] + ' le', text)      # "ile" is the fused "i le"
    text = re.sub(r'\b([Ll]e) (?:Aw|Ash|Alii|ALn|ALu|Aln|ALIL|AL1I|ALll|Ali)\b', r'\1 ALII', text)   # the small-caps ALII (the LORD) as the OCR reads it
    # the app's text is the unmarked orthography (the diacritics layer restores
    # marks on demand): fold the edition's macrons and stray acutes
    text = text.translate(str.maketrans('āēīōūáéíóúÁĀ', 'aeiouaeiouAA'))
    return re.sub(r'\s+', ' ', text).strip()
out = {k: {'sm': clean(verses[k]), 'est': k in est_keys} for k in verses}
json.dump({'ratio': R, 'verses': out, 'notes': notes, 'spans': [(ENG[k], how) for k, b, e2, how in spans]},
          open(D / 'tusi_paia_verses.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)

# ---------------------------------------------------------------- report
print(f'ratio Samoan/English chars = {R:.3f} from {len(ratios)} clean verses; runs {len(runs)}; flags {dict(flags)}; footnotes stripped {len(FOOT)}')
print('book starts not by title:', ', '.join(f'{ENG[k]}' for k, b, e2, how in spans if how != 'title') or 'none')
print(f'{"book":18} {"chapters":>9} {"verses":>13} {"est":>5}  bad-ratio')
tot_e = tot_g = tot_est = tot_bad = 0
for s, e, _ in BOOKS:
    chs = KC[e]; ne = sum(chs.values())
    got = sum(1 for c in chs for vv in range(1, chs[c] + 1) if f'{e}|{c}|{vv}' in out)
    est = sum(1 for c in chs for vv in range(1, chs[c] + 1) if out.get(f'{e}|{c}|{vv}', {}).get('est'))
    chs_got = sum(1 for c in chs if any(f'{e}|{c}|{vv}' in out for vv in range(1, chs[c] + 1)))
    bad = 0
    for c in chs:
        for vv in range(1, chs[c] + 1):
            k = f'{e}|{c}|{vv}'
            if k in out and not out[k]['est']:
                r = len(out[k]['sm']) / max(20, len(KV.get(k, ''))) / R
                if r < 0.45 or r > 2.2: bad += 1
    tot_e += ne; tot_g += got; tot_est += est; tot_bad += bad
    print(f'{e:18} {chs_got:4}/{len(chs):<4} {got:6}/{ne:<6} {est:5}  {bad}')
print(f'TOTAL verses {tot_g}/{tot_e} ({100 * tot_g / tot_e:.1f}%), estimated {tot_est}, bad-ratio anchored {tot_bad}')
badch = []
for s_, e, _ in BOOKS:
    for c, m in KC[e].items():
        anchored = [vv for vv in range(1, m + 1) if f'{e}|{c}|{vv}' in out and not out[f'{e}|{c}|{vv}']['est']]
        if len(anchored) < 4: continue
        nbad = sum(1 for vv in anchored if not 0.45 <= len(out[f'{e}|{c}|{vv}']['sm']) / max(20, len(KV.get(f'{e}|{c}|{vv}', ''))) / R <= 2.2)
        if nbad / len(anchored) > 0.3: badch.append(f'{e} {c} ({nbad}/{len(anchored)})')
print(f'misaligned chapters (>30% of anchored verses off): {len(badch)}'); print('  ' + ', '.join(badch[:60]))
print(len(notes), 'notes (non-missing):'); print('\n'.join(n for n in notes if 'missing' not in n)[:3000])
for k in ('Genesis|3|1','Genesis|6|5','Psalms|23|1','Psalms|23|2','Job|37|1','Matthew|5|3','1 Chronicles|1|2','Revelation|22|21'):
    if k in out: print(f'{k} est={out[k]["est"]}\n   SM: {out[k]["sm"][:180]}\n   EN: {KV.get(k,"")[:180]}')
