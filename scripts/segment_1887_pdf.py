#!/usr/bin/env python3
"""Segment the 1887 O le Tusi Paia (BFBS, Blackfriars, MDCCCLXXXVII) into verses
from the archive.org PDF's text layer -- the edition the user wants the app to
carry ("Lokou", "Ieova"), not the later revision (`Upu`, `le ALII`) that
segment_tusi_paia.py cut from the other scan.

Why the PDF: the plain OCR text of this edition lost the verse numbers, which
are printed in the outer margins, into a junk run at each page's edge. The
PDF's text layer keeps every word's position, so a margin number can be tied
to the line it sits beside, and the 1887 text is cut on its own evidence.

Layout facts (measured on the John 1 page, 283x446 pt):
  - two columns, gutter near x=133; running head "IOANE, 1." at the top; the
    page number and signature at the foot
  - verse numbers in the LEFT margin (x 10-13) for the left column, in the
    RIGHT margin (x 255+) for the right column, each beside its verse's FIRST
    line; a verse that starts mid-line follows a sentence end
  - a chapter opens with an indented italic summary ("Ua liu tino tagata le
    Lokou.") and its first word in small caps ("SA i le amataga"); a book opens
    with centred caps title lines ("O LE EVAGELIA A IOANE.")
  - verse 1 has a drop-cap numeral the OCR reads as junk ("J"), so chapter
    starts are inferred from the summary/caps lines and the count restarting
  - hyphenated line ends ("faa-" / "malamalamaina") are rejoined

The KJV verse counts (english_ot_nt.json) say how many verses each chapter has;
the later edition's verses (tusi_paia_verses.json) are the check, verse by
verse, and the spelling reference for one- or two-letter OCR slips.

    python3 scripts/segment_1887_pdf.py --pages 968          lines + markers of a page
    python3 scripts/segment_1887_pdf.py --book john          one book, with the check
    python3 scripts/segment_1887_pdf.py --all                every book -> tusi_paia_verses_1887.json
"""
from __future__ import annotations

import argparse
import ast
import os
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "corpus" / "tusi_paia"
PDF = Path("/Users/chrislambe/Desktop/oletusipaiaole00lond.pdf")
OUT = D / "tusi_paia_verses_1887.json"

K = json.load(open(D / "english_ot_nt.json", encoding="utf8"))
KC = K["counts"]                                   # {"John": {"1": 51, ...}}
NUMBERED = json.load(open(D / "tusi_paia_verses.json", encoding="utf8"))["verses"]
# THE TYPED 1887 TEXT, where the user has pasted a chapter (corpus/tusi_paia/sov/):
# the better reference -- same words as the print -- for the boundary guide, the
# aligned word in repair, and the known-word set. See sov_reference.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sov_reference import load_sov  # noqa: E402
SOV = load_sov()


def reference(key: str) -> str:
    """The reference text for a verse: the typed 1887 chapter when pasted, else the later edition."""
    return SOV.get(key) or NUMBERED.get(key, {}).get("sm", "")


def _books():
    """The 66 (SAMOAN TITLE, English, keywords) rows of segment_tusi_paia.py,
    read from its source: importing it would run its main."""
    src = (ROOT / "scripts" / "segment_tusi_paia.py").read_text(encoding="utf8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "BOOKS":
            return ast.literal_eval(node.value)
    raise SystemExit("no BOOKS table in segment_tusi_paia.py")


BOOKS = _books()
assert len(BOOKS) == 66
SM_NAME = [b[0] for b in BOOKS]                    # 'KENESE', ..., 'FAAALIGA'
EN_NAME = [b[1] for b in BOOKS]                    # 'Genesis', ..., 'Revelation'
BOOK_ID = [e.lower().replace(" ", "") for e in EN_NAME]

# OCR shapes of margin numerals
DIGIT_SHAPE = {"l": "1", "I": "1", "J": "1", "i": "1", "|": "1", "O": "0", "o": "0", "S": "5",
               "$": "5", "G": "6", "B": "8", "Z": "2", "ö": "6", "ä": "4", "b": "6", "q": "9"}
END = re.compile(r"[.?!][”’\"')\]]*$")
PUNCT = re.compile(r"[.,;:?!][”’\"')\]]*$")     # a verse begins after ANY of these
CAPS_WORD_RX = re.compile(r"^[A-ZĀĒĪŌŪl01’]{2,}[,.;:]?$")


class _CapsWord:
    """A caps word, tolerating the OCR's l / 0 / 1 inside it (lOPU, ESE1A):
    at least two real capitals and nothing lower-case but l."""
    @staticmethod
    def match(t):
        return CAPS_WORD_RX.match(t) and len(re.findall(r"[A-ZĀĒĪŌŪ]", t)) >= 2


CAPS_WORD = _CapsWord


def marker_value(tok: str):
    """A margin token as a verse number, or None if it is not digit-shaped."""
    t = tok.strip(".,;:")
    if not t or len(t) > 3:
        return None
    digits = "".join(DIGIT_SHAPE.get(ch, ch) for ch in t)
    if not digits.isdigit() or int(digits) == 0:
        return None          # 0 is never a verse or chapter: an unreadable numeral
    return int(digits)


def marker_value_loose(tok: str):
    """The numeral in a margin token with OCR junk glued on: `15m`, `2S`, `x3`."""
    v = marker_value(tok)
    if v is not None:
        return v
    t = tok.strip(".,;:")
    m = re.match(r"^[a-z]{0,2}([0-9lIJOoSGBZöä]{1,3})[a-z]{0,2}$", t)
    return marker_value(m.group(1)) if m else None


# ── page geometry ─────────────────────────────────────────────────────────────

def parse_page(page):
    """The page as two columns of lines; each line: tokens, indent, marker.

    Returns (head_text, [column_L_lines, column_R_lines]); a line is a dict
    {toks, x0, indent, marker (int|None), marker_raw, caps_title}."""
    words = page.get_text("words")
    H, W = page.rect.height, page.rect.width
    yc = lambda w: (w[1] + w[3]) / 2
    head = " ".join(w[4] for w in sorted(words, key=lambda w: w[0]) if yc(w) < 22)
    body = [w for w in words if 22 <= yc(w) <= H - 26]
    if not body:
        return head, [[], [], []]
    # the gutter: the widest x gap between word centres in the middle band --
    # measured without the words of page-wide caps lines (a title set across
    # both columns fills the gutter, the gap landed inside a column, and the
    # two columns' lines interleaved: Joel 1 came out shuffled with Hosea 13)
    def gutter_of(ws):
        xs = sorted((w[0] + w[2]) / 2 for w in ws if len(w[4]) > 1)
        gaps = [(b - a, (a + b) / 2) for a, b in zip(xs, xs[1:]) if 0.36 * W < (a + b) / 2 < 0.64 * W]
        return max(gaps)[1] if gaps else W / 2
    gutter = gutter_of(body)

    def cluster(ws):
        ws = sorted(ws, key=yc)
        lines = []
        for w in ws:
            if lines and abs(yc(w) - lines[-1]["y"]) <= 3.2:
                lines[-1]["w"].append(w)
                n = len(lines[-1]["w"])
                lines[-1]["y"] += (yc(w) - lines[-1]["y"]) / n
            else:
                lines.append({"y": yc(w), "w": [w]})
        return lines

    def caps_tok(t):
        return CAPS_WORD.match(t) or t in ("A", "O", "E", "I") or re.fullmatch(r"[0-9OlI]{1,3}[.,]?", t)

    # A BOOK TITLE IS SET ACROSS THE WHOLE PAGE ("O LE EVAGELIA A IOANE" over
    # both columns), so it is read here, before the columns, and streamed
    # first: read per column it surfaced only after the left column's verses.
    title_lines, title_ids = [], set()
    for ln in cluster(body):
        toks = [w[4] for w in sorted(ln["w"], key=lambda w: w[0])]
        alpha = [t for t in toks if re.search(r"[A-Za-z]{2}", t)]
        xs0, xs1 = min(w[0] for w in ln["w"]), max(w[2] for w in ln["w"])
        centred = abs((xs0 + xs1) / 2 - gutter) < 30 and (xs1 - xs0) < 0.7 * W
        if alpha and all(caps_tok(t) for t in toks) and (xs0 < gutter < xs1 or centred):
            title_lines.append({"toks": toks, "x0": xs0, "indent": None, "marker": None,
                                "marker_raw": "", "y": ln["y"], "caps_title": True})
            title_ids |= {id(w) for w in ln["w"]}
    body = [w for w in body if id(w) not in title_ids]
    if title_ids:
        gutter = gutter_of(body)
    columns = []
    for side in ("L", "R"):
        ws = [w for w in body if (((w[0] + w[2]) / 2) < gutter) == (side == "L")]
        lines = cluster(ws)
        if not lines:
            columns.append([])
            continue
        # the text block's edge: the x where line starts pile up (markers are
        # few and sit outside it)
        # the block edge is measured on WORDS, never on the numerals: on a page
        # with many verses the markers are a quarter of the line ends and
        # dragged the right edge out to themselves, so none was a marker
        def wordish(w):
            return marker_value(w[4]) is None and re.search(r"[A-Za-z]{2}", w[4])
        if side == "L":
            starts = Counter(round(min(w[0] for w in ln["w"] if wordish(w))) for ln in lines if any(wordish(w) for w in ln["w"]))
            edge = None
            for x in sorted(starts):
                if sum(starts[k] for k in range(x - 1, x + 3)) >= max(3, 0.25 * len(lines)):
                    edge = x
                    break
            if edge is None:
                edge = min(starts) if starts else min(round(w[0]) for w in ws)
        else:
            ends = Counter(round(max(w[2] for w in ln["w"] if wordish(w))) for ln in lines if any(wordish(w) for w in ln["w"]))
            edge = None
            for x in sorted(ends, reverse=True):
                if sum(ends[k] for k in range(x - 2, x + 2)) >= max(3, 0.25 * len(lines)):
                    edge = x
                    break
            if edge is None:
                edge = max(ends) if ends else max(round(w[2]) for w in ws)
        # a line holding only marker-shaped words is a numeral the clustering
        # set apart (the drop cap's centre lies between its two lines): it
        # joins the nearest text line, the earlier one on a tie
        def only_markers(ln):
            return all(marker_value_loose(w[4]) is not None or not re.search(r"[A-Za-z]{2}", w[4]) for w in ln["w"]) \
                and any(marker_value_loose(w[4]) is not None for w in ln["w"])
        merged = []
        pending = []
        for ln in lines:
            if not os.environ.get("NO_MERGE") and only_markers(ln) and len(ln["w"]) <= 2:
                pending.append(ln)
                continue
            for pl in pending:
                if merged and abs(pl["y"] - merged[-1]["y"]) <= abs(pl["y"] - ln["y"]) + 0.5:
                    merged[-1]["w"].extend(pl["w"])
                else:
                    ln["w"].extend(pl["w"])
            pending = []
            merged.append(ln)
        for pl in pending:
            if merged:
                merged[-1]["w"].extend(pl["w"])
        lines = merged
        out = []
        for ln in lines:
            ws_ = sorted(ln["w"], key=lambda w: w[0])
            # a marker is a numeral standing clear of the text block: a
            # two-digit number's right edge nearly touches the block, so it is
            # its START that is measured
            # In some columns the numerals hang only 3-4 pt into the margin
            # (`2 ia. Pe afai foi`): a token of REAL digits that starts even a
            # little outside the block is a marker there; letter-shaped
            # numerals (l, O, S) need the full clearance, or `O le` at a line
            # start would become one.
            REAL = re.compile(r"^[0-9]{1,3}[a-z]{0,2}[.,]?$")
            if side == "L":
                marks = [w for w in ws_ if w[2] <= edge - 2.5
                         or (w[0] <= edge - 4 and marker_value_loose(w[4]) is not None)
                         or (w[0] <= edge - 2.2 and REAL.match(w[4]) and w is ws_[0])]
            else:
                marks = [w for w in ws_ if w[0] >= edge + 2.5
                         or (w[2] >= edge + 4 and marker_value_loose(w[4]) is not None)
                         or (w[2] >= edge + 2.2 and REAL.match(w[4]) and w is ws_[-1])]
            toks_w = [w for w in ws_ if w not in marks]
            if not toks_w and not marks:
                continue
            marker_raw = " ".join(w[4] for w in marks)
            mv = None
            if marks:
                joined = "".join(w[4] for w in marks)
                mv = marker_value(joined)
                if mv is None:
                    mv = marker_value_loose(joined)
            toks = [w[4] for w in toks_w]
            x0 = toks_w[0][0] if toks_w else None
            indent = (x0 - edge) if (side == "L" and x0 is not None) else None
            if side == "R" and toks_w:
                # right column: its own left edge is the modal line start
                indent = None
            out.append({"toks": toks, "x0": x0, "indent": indent, "marker": mv,
                        "marker_raw": marker_raw, "y": ln["y"],
                        "caps_title": bool(toks) and all(caps_tok(t) for t in toks)
                        and any(len(re.sub(r"[^A-Za-z]", "", t)) >= 3 for t in toks)})
        # right column indentation from its own line-start distribution
        if side == "R" and out:
            starts = Counter(round(l["x0"]) for l in out if l["x0"] is not None)
            base = None
            for x in sorted(starts):
                if sum(starts[k] for k in range(x - 1, x + 3)) >= max(3, 0.25 * len(out)):
                    base = x
                    break
            if base is None:
                base = min(starts) if starts else 0
            for l in out:
                l["indent"] = (l["x0"] - base) if l["x0"] is not None else None
        columns.append(out)
    return head, [title_lines] + columns


def parse_head(head: str):
    """('IOANE', [1]) from 'IOANE, 1.'; ('FILEMONI', []) from a one-chapter
    book's bare name -- fuzzy on the name, or (None, [])."""
    m = re.search(r"([A-Z][A-Z0-9\.\s'’]{2,}?),\s*([0-9lIO,\s]+)\.?", head)
    if not m:
        m2 = re.search(r"^\s*((?:I{1,3}\.?\s+)?[A-Z][A-Z0-9]{3,})\.?\s*$", head.strip())
        if not m2:
            return None, []
        name = re.sub(r"[.\s]+", " ", m2.group(1)).strip()
        name = re.sub(r"^(IL|1I|I1|11)\b", "II", name)
        return name, []
    name = re.sub(r"[.\s]+", " ", m.group(1)).strip()
    name = re.sub(r"^(IL|1I|I1|11)\b", "II", name)
    name = re.sub(r"^(1|J|L)\b", "I", name)
    chapters = []
    for c in re.split(r"[,\s]+", m.group(2)):
        v = marker_value(c) if c else None
        if v:
            chapters.append(v)
    return name, chapters


def match_book(name: str, at_least: int = 0, window: int = 66) -> int | None:
    """Index of the book a running-head name means, searched from `at_least`."""
    if not name:
        return None
    best, score = None, 0.0
    for idx in range(at_least, min(at_least + window, 66)):
        r = difflib.SequenceMatcher(None, name, SM_NAME[idx]).ratio()
        if r > score:
            best, score = idx, r
    return best if score >= 0.72 else None


def head_book(name: str):
    """(book index, confidence) for a head name over all 66 books."""
    if not name:
        return None, 0.0
    best, score = None, 0.0
    for idx in range(66):
        r = difflib.SequenceMatcher(None, name, SM_NAME[idx]).ratio()
        if r > score:
            best, score = idx, r
    return (best, score) if score >= 0.72 else (None, 0.0)


# ── the stream of lines, book by book ──────────────────────────────────────────

def page_range_by_book(doc, first_page=6):
    """[(book_index, page_index)] for every page.

    Books run in order, so the assignment is the NON-DECREASING sequence that
    agrees with the most running heads (a small dynamic programme over pages x
    books). A greedy walk was thrown by single misreads: one bad head jumped it
    to Joel and every Hosea page followed; the one-chapter epistles' heads have
    no chapter number, so it never left 1 John and Revelation went with it."""
    pages = list(range(first_page, len(doc)))
    votes = []
    for pi in pages:
        head, _ = parse_page(doc[pi])
        name, _ch = parse_head(head)
        b, conf = head_book(name)
        votes.append((b, conf))
    n = len(pages)
    NEG = float("-inf")
    score = [[NEG] * 66 for _ in range(n)]
    back = [[0] * 66 for _ in range(n)]
    for p in range(n):
        b_vote, conf = votes[p]
        for b in range(66):
            gain = conf if b_vote == b else 0.0
            if p == 0:
                score[p][b] = gain if b == 0 else NEG
                continue
            best_prev, best_b = NEG, b
            for bp in range(0, b + 1):
                if score[p - 1][bp] > best_prev:
                    best_prev, best_b = score[p - 1][bp], bp
            score[p][b] = best_prev + gain
            back[p][b] = best_b
    b = max(range(66), key=lambda x: score[n - 1][x])
    assign = [None] * n
    for p in range(n - 1, -1, -1):
        assign[p] = b
        b = back[p][b]
    global CONFIDENT
    CONFIDENT = defaultdict(list)
    for i in range(n):
        if votes[i][0] is not None and votes[i][0] == assign[i] and votes[i][1] >= 0.8:
            CONFIDENT[assign[i]].append(pages[i])
    return [(assign[i], pages[i]) for i in range(n)]


CONFIDENT = defaultdict(list)


def book_pages(bidx, pages_of, npages):
    """The pages a book may run over: from the last page a running head
    confidently gives to an EARLIER book, to the first page confidently given
    to a LATER one. Pages nobody's head claims (title pages, garbled heads)
    are offered to both neighbours; the title gate and the next book's title
    decide inside the stream. Before this, 2 John's text lay on pages the
    assignment had handed to 1 John and its stream started after its own end."""
    earlier = [p for b in range(bidx) for p in CONFIDENT.get(b, [])]
    later = [p for b in range(bidx + 1, 66) for p in CONFIDENT.get(b, [])]
    lo = max(earlier) if earlier else 6
    hi = min(later) if later else npages - 1
    own = pages_of.get(bidx, [])
    if own:
        lo = min(lo, own[0])
        hi = max(hi, own[-1])
    return list(range(lo, hi + 1))


def norm_tokens(text: str):
    return [re.sub(r"[^a-z’ʻ‘']", "", t.lower()) for t in text.split() if re.sub(r"[^a-z]", "", t.lower())]


def similarity(a: str, b: str) -> float:
    ta, tb = norm_tokens(a), norm_tokens(b)
    if not ta or not tb:
        return 0.0
    return difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()


def join_lines(lines_toks):
    """Tokens of several lines as one list, rejoining hyphenated line ends."""
    out = []
    for toks in lines_toks:
        toks = list(toks)
        if out and out[-1].endswith("-") and toks and toks[0][:1].islower():
            out[-1] = out[-1][:-1] + toks[0]
            toks = toks[1:]
        out.extend(toks)
    return out


def _norm_tok(t: str) -> str:
    return re.sub(r"[^a-zāēīōū’ʻ‘]", "", t.lower())


def split_point(toks, prev_ended: bool, ref_start=None) -> int:
    """Where a new verse begins inside a marked line.

    A verse begins after a punctuation mark -- full stop, comma, semicolon,
    colon -- and may begin in lower case (`o le tasi | 2 lea faipule o
    Iutaia; ua alu ane o ia`: verse 2 opens at "ua"). So every punctuation
    mark in the line is a candidate, and the line start when the previous
    line ended with one. The later edition's opening words for the verse pick
    among them; without that, the first candidate followed by a capital, else
    the first candidate, else the line start."""
    cands = []
    if prev_ended and toks:
        cands.append(0)
    for k in range(1, len(toks)):
        if PUNCT.search(toks[k - 1]):
            cands.append(k)
    if not cands:
        return 0
    if ref_start:
        ref = [_norm_tok(t) for t in ref_start[:4]]
        best, score = None, -1.0
        for k in cands:
            here = [_norm_tok(t) for t in toks[k:k + 4]]
            n = sum(1 for a, b in zip(here, ref) if a and a == b)
            # a run from the first word counts more than scattered hits
            run = 0
            for a, b in zip(here, ref):
                if a and a == b:
                    run += 1
                else:
                    break
            sc = run * 2 + n
            if sc > score:
                best, score = k, sc
        if score >= 2:
            return best
    for k in cands:
        if k < len(toks) and toks[k][:1].isupper():
            return k
    return cands[0]


def ref_start(en: str, chapter: int, verse: int):
    """The later edition's opening tokens of a verse, the boundary guide."""
    sm = reference(f"{en}|{chapter}|{verse}")
    return sm.split()[:4] if sm else None


def page_stream(cols):
    """The page's lines in reading order.

    A book title set across both columns (Joel's, in the lower third of the
    page that ends Hosea) splits the page into horizontal bands, each read
    left column then right column; the title block stands between the bands.
    Reading the whole left column first shuffled Joel 1 into Hosea 13."""
    titles, left, right = cols[0], cols[1], cols[2]
    if not titles:
        return list(left) + list(right)
    # title blocks: title lines within 40 pt of each other
    blocks = []
    for t in sorted(titles, key=lambda l: l["y"]):
        if blocks and t["y"] - blocks[-1][-1]["y"] <= 40:
            blocks[-1].append(t)
        else:
            blocks.append([t])
    out = []
    lo = -1.0
    for blk in blocks:
        top = min(t["y"] for t in blk)
        out += [l for l in left if lo <= l["y"] < top - 3] + [l for l in right if lo <= l["y"] < top - 3]
        out += blk
        lo = max(t["y"] for t in blk) + 3
    out += [l for l in left if l["y"] >= lo] + [l for l in right if l["y"] >= lo]
    return out


class Segmenter:
    """The state machine over a book's lines.

    A chapter begins where the margin shows the CHAPTER numeral (it is the
    drop cap beside verse 1) and the next marker is 2; an indented summary
    line stands just above. A verse begins where the margin shows verse+1.
    Lost markers are bridged when the sequence resumes; the buffered text is
    then split at sentence ends. Everything else is the current verse."""

    def __init__(self, doc, verbose=False):
        self.doc = doc
        self.verbose = verbose
        self.verses = {}       # "John|1|1" -> {"sm": ..., "flags": [...]}
        self.notes = []

    def run_book(self, bidx: int, pages: list[int]):
        self.en = EN_NAME[bidx]
        self.counts = KC[self.en]
        self.nchap = len(self.counts)
        self.keywords = [w for w in BOOKS[bidx][2] if not w.startswith(("+", "-"))] or SM_NAME[bidx].split()
        self.prev_keywords = ([w for w in BOOKS[bidx - 1][2] if not w.startswith(("+", "-"))] or SM_NAME[bidx - 1].split()) if bidx else []
        self.forbidden = [w[1:] for w in BOOKS[bidx][2] if w.startswith("-")]
        self.title_buf = []       # tokens of the caps lines seen in a row
        self.title_lines = 0
        self.head_started = False # chapter 1 opened on the page head alone
        self.prev_title_seen = False  # the previous book's title passed in this stream
        self.block_near_here = False
        self.prev_display = False # the previous line was an indented summary
        self.chapter = 0          # 0 = before the first chapter
        self.verse = 0
        self.buf = []             # lines of the current verse: {"toks", "indent"}
        self.book_done = False
        self.prev_ended = True
        self.seen_title = False
        next_name = SM_NAME[bidx + 1].split()[-1] if bidx + 1 < 66 else None
        self.lines = []
        parsed = []
        for pi in pages:
            head, cols = parse_page(self.doc[pi])
            hname, hch = parse_head(head)
            hb = head_book(hname)[0] if hname else None
            if hb is None and hname and difflib.SequenceMatcher(None, hname, SM_NAME[bidx]).ratio() >= 0.62:
                hb = bidx          # `IOPTT` for IOPU: the expected book, read loosely
            here = hb == bidx
            parsed.append((pi, cols, here, hch, hb))
        for k, (pi, cols, here, hch, hb) in enumerate(parsed):
            nxt_here = k + 1 < len(parsed) and parsed[k + 1][2] and (not parsed[k + 1][3] or min(parsed[k + 1][3]) <= 2)
            for ln in page_stream(cols):
                ln["page"] = pi
                ln["head_ch"] = hch if here else []
                # the head of THIS page names the book; the next page's
                # head must not vouch for a chapter start -- it let Luke 1
                # start on Mark 16 -- but it may vouch for a TITLE block
                ln["book_here"] = here
                ln["near_here"] = here or nxt_here
                ln["other_head"] = hb is not None and hb < bidx
                self.lines.append(ln)
        for idx, ln in enumerate(self.lines):
            if self.book_done:
                break
            self.feed(ln, next_name, idx)
        if not self.book_done:
            self.close_book()

    # -- helpers ------------------------------------------------------------
    def expected(self):
        return self.counts.get(str(self.chapter), 0)

    def _next_marker_after(self, idx):
        for ln in self.lines[idx + 1: idx + 60]:
            if ln["marker"] is not None:
                return ln["marker"]
        return None

    def _next_markers_after(self, idx, n=2):
        out = []
        for ln in self.lines[idx + 1: idx + 80]:
            if ln["marker"] is not None:
                out.append(ln["marker"])
                if len(out) == n:
                    break
        return out

    @staticmethod
    def _caps_start(toks) -> bool:
        """`SA i le amataga`, `O LE tasi tagata`, `O A‘U nei`: the chapter's
        first word in small caps, allowing a one-letter particle before it and
        the drop-cap junk the OCR leaves."""
        # skip the drop-cap junk and one-letter particles (`0 A‘U`, `J SA`,
        # `O LE`): the first token with two or more letters decides. A first
        # token of digit shapes alone (`01 talofa` for OI talofa) is the small
        # caps word itself misread, and counts.
        if toks and re.fullmatch(r"[0-9OlI]{2,3}", toks[0]) and len(toks) > 1 and toks[1][:1].islower():
            return True
        # two one-letter capitals in a row are the small caps themselves: `A O oe`
        if len(toks) >= 2 and re.fullmatch(r"[A-Z]", toks[0]) and re.fullmatch(r"[A-Z][,.;]?", toks[1]):
            return True
        cand = None
        for x in toks[:3]:
            letters = re.sub(r"[^A-Za-zĀĒĪŌŪāēīōū]", "", x)
            if len(letters) >= 2:
                cand = x
                break
        if cand is None:
            return False
        w = re.sub(r"[^A-Za-zĀĒĪŌŪāēīōū’ʻ‘]", "", cand)
        return len(w) >= 2 and w.isupper()

    @staticmethod
    def _strip_dropcap(toks):
        toks = list(toks)
        while len(toks) > 1 and (toks[0] in ("J", "|", "l", "I", "1") or (len(toks[0]) <= 3 and marker_value(toks[0]) is not None)
                                 or (len(toks[0]) <= 2 and not toks[0].isalpha())):
            toks = toks[1:]
        return toks

    # -- the machine --------------------------------------------------------
    def feed(self, ln, next_name, idx):
        toks = ln["toks"]
        m = ln["marker"]
        joined = " ".join(toks)
        if ln["caps_title"]:
            # the next book's title ends this one; this book's own title
            # (or its repeat at a column top) is display
            if next_name and self.chapter >= 1 and (next_name in joined
                    or difflib.SequenceMatcher(None, next_name, joined.split()[-1].strip(".")).ratio() > 0.8):
                self.close_book()
                return
            self.title_buf += joined.replace(".", " ").replace(",", " ").split()
            self.title_lines += 1
            # two or more caps lines in a row before chapter 1 are this book's
            # title even when the OCR garbles every keyword (Esther, Amos) --
            # only on the book's own pages: Philemon's title sits in Hebrews'
            # stream too, and made Hebrews 1 of Philemon
            if self.chapter == 0 and self._title_matches(self.prev_keywords):
                self.prev_title_seen = True
            self.block_near_here = bool(ln.get("near_here"))
            if self._title_matches():
                if self.chapter == 1 and self.head_started:
                    # the title arrives after a start the page head alone
                    # allowed: that start was the previous book's tail
                    self.notes.append(f"{self.en}: title found after a head-based start at 1:{self.verse} -> restarted")
                    for key in [k for k in self.verses if k.startswith(f"{self.en}|")]:
                        del self.verses[key]
                    self.chapter = 0
                    self.verse = 0
                    self.buf = []
                self.seen_title = True
            return
        if not toks:
            return
        # the caps block has ended: judged whole, two or more caps lines before
        # chapter 1 are this book's title -- unless the block is the previous
        # book's (judging it line by line let Philemon's title pass as
        # Hebrews' before its own name arrived on the third line)
        if self.chapter == 0 and self.title_lines >= 2 and not self.seen_title and self.block_near_here \
                and not self._title_matches(self.prev_keywords):
            self.seen_title = True
        self.title_buf = []
        self.title_lines = 0
        nxt = self._next_marker_after(idx)
        nxt2 = self._next_markers_after(idx, 2)
        opens = 2 in nxt2 or 3 in nxt2     # a chapter's second or third verse follows
        if self.verbose:
            print(f"    c{self.chapter}:v{self.verse} p{ln.get('page')} m={m!r} raw={ln['marker_raw']!r} nxt={nxt} ind={(ln['indent'] or 0):+.1f} | {' '.join(toks)[:60]}")

        if self.chapter == 0:
            if not (self.seen_title or ln.get("book_here")):
                return
            # after the title, the first small-caps line with a 2 or 3 to follow
            # is verse 1 whatever the drop cap was read as (Luke's "1" read "2")
            # once the previous book's title has passed, only this book's own
            # title or this page's head may vouch (Philemon's summary and
            # numeral 1 sat right where Hebrews' stream begins)
            vouched = self.seen_title or ln.get("book_here") \
                or (ln.get("near_here") and self.prev_display and not self.prev_title_seen and not ln.get("other_head"))
            if (m == 1 and opens and vouched) or (self.seen_title and opens and self._caps_start(toks) and (ln["indent"] or 0) < 20) \
                    or (m is None and ln["marker_raw"] and opens and self._caps_start(toks) and (self.seen_title or ln.get("book_here"))) \
                    or (ln.get("book_here") and opens and self._caps_start(toks) and self.prev_display and 4 <= (ln["indent"] or 0) < 20):
                hch = ln.get("head_ch") or []
                if not self.seen_title and hch and 1 not in hch and min(hch) > 1:
                    # the page head says a later chapter: chapter 1 (and any
                    # before this) lie on pages whose title the OCR lost
                    self.notes.append(f"{self.en}: first chapter found is {min(hch)} (head); chapters 1-{min(hch) - 1} missing")
                    self.chapter = min(hch) - 1
                self._start_chapter(toks, book_here=bool(ln.get("book_here")))
            self.prev_display = (ln["indent"] or 0) >= 6 and len(toks) <= 10 and bool(END.search(toks[-1]))
            return

        # A NEW CHAPTER: its numeral in the margin, a 2 (or 3) to follow
        if self.chapter < self.nchap and m == self.chapter + 1 and opens and self.verse >= 2 \
                and not (m == self.verse + 1 and self.verse + 1 < self.expected() - 1 and not self._caps_start(toks)):
            if self.verse < self.expected():
                self.notes.append(f"{self.en} {self.chapter}: verses {self.verse + 1}-{self.expected()} never marked before chapter {self.chapter + 1} -> missing")
            self._close_verse(trim_summary=True)
            self._start_chapter(toks)
            return
        # the numeral says a LATER chapter and the running head agrees: a
        # chapter start was missed; resync on the numeral
        if self.chapter < self.nchap and m is not None and self.chapter + 1 < m <= self.nchap and opens \
                and m in ln.get("head_ch", []) and self._caps_start(toks):
            self.notes.append(f"{self.en}: chapter numeral {m} while at {self.chapter}:{self.verse}; chapter(s) {self.chapter + 1}-{m - 1} were missed -> resync")
            self._close_verse(trim_summary=True)
            self.chapter = m - 1
            self._start_chapter(toks)
            return
        if self.chapter < self.nchap and m is None and ln["marker_raw"] and opens and self._caps_start(toks) \
                and self.verse >= max(2, self.expected() - 3):
            # the chapter numeral unreadable, the caps first word says it
            self._close_verse(trim_summary=True)
            self._start_chapter(toks, ln.get("head_ch"))
            return

        if m is not None and m != self.verse:
            if m == self.verse + 1 and m <= self.expected():
                self._new_verse(toks, m)
                return
            if m == 2 and self.verse >= 2 and self.chapter < self.nchap and nxt in (3, 4) and self.expected() - self.verse <= 12:
                # the count restarted without a readable chapter numeral:
                # the chapter break lies inside the buffer
                if self.verse < self.expected():
                    self.notes.append(f"{self.en} {self.chapter}: verses {self.verse + 1}-{self.expected()} not marked before the chapter break -> missing")
                self._chapter_break_then(toks)
                return
            if self.verse + 1 < m <= self.expected() and (m <= self.verse + 3 or nxt in (m + 1, m + 2)):
                self._new_verse(toks, m, skipped=m - self.verse - 1)
                return
            if nxt == self.verse + 2 and self.verse + 1 <= self.expected():
                # misread numeral (2 -> 9, 7 -> 1): the next one is verse+2
                self._new_verse(toks, self.verse + 1)
                return
            self.notes.append(f"{self.en} {self.chapter}:{self.verse} p{ln['page']}: stray margin {ln['marker_raw']!r} -> ignored")
        elif m is None and ln["marker_raw"] and nxt == self.verse + 2 and self.verse + 1 <= self.expected():
            # unreadable numeral in the margin, in sequence: it is verse+1
            self._new_verse(toks, self.verse + 1)
            return

        # a plain line of the current verse; the caps first word after a
        # complete chapter is the fallback for a chapter numeral lost entirely
        if self.chapter < self.nchap and self.verse == self.expected() and self._caps_start(toks) and nxt in (2, 3) \
                and (ln["indent"] or 0) < 20 and m is None and not ln["marker_raw"]:
            self._close_verse(trim_summary=True)
            self._start_chapter(toks, ln.get("head_ch"))   # the head numbers the chapter when the numeral is lost
            self.prev_display = False
            return
        # A CHAPTER START BY SHAPE: an indented summary line just before, a
        # small-caps first word, and the first line pushed right by the drop
        # cap (4-20 pt) -- for a numeral the OCR swallowed into the text
        # (`ua maona foi Q`) or lost. Verses the marker count did not reach are
        # reported missing rather than guessed.
        if self.chapter < self.nchap and self.prev_display and self._caps_start(toks) and opens \
                and 4 <= (ln["indent"] or 0) < 20 and self.verse >= 2 and (m is None or m > self.expected()) \
                and (self.verse + 1) not in nxt2:
            if self.verse < self.expected():
                self.notes.append(f"{self.en} {self.chapter}: verses {self.verse + 1}-{self.expected()} not marked before a chapter start by shape -> missing")
            self._close_verse(trim_summary=True)
            self._start_chapter(toks, ln.get("head_ch"))
            self.prev_display = False
            return
        self.prev_display = (ln["indent"] or 0) >= 6 and len(toks) <= 10 and bool(END.search(toks[-1]))
        self.buf.append({"toks": toks, "indent": ln["indent"] or 0})
        self.prev_ended = bool(PUNCT.search(toks[-1]))

    def _title_matches(self, keywords=None) -> bool:
        """Every keyword of this book's title, fuzzily, in the caps block --
        `LUA` and `IOANE` for 2 John, so 1 John's title does not pass."""
        toks = self.title_buf
        keywords = self.keywords if keywords is None else keywords
        if not toks or not keywords:
            return False
        cands = list(toks) + [a + b for a, b in zip(toks, toks[1:])]   # `IO PU` -> IOPU
        def has(k):
            return any(t == k or (len(t) >= 4 and difflib.SequenceMatcher(None, t, k).ratio() >= 0.75) for t in cands)
        return all(has(k) for k in keywords) and (keywords is not self.keywords or not any(has(f) for f in self.forbidden))

    def _start_chapter(self, toks, head_ch=None, book_here=False):
        if self.chapter == 0:
            # a start the page's own head vouched for is trusted; only a start
            # vouched by the NEXT page's head is provisional (Proverbs 1 was
            # thrown away when a caps line inside it matched the title)
            self.head_started = not self.seen_title and not book_here
        if head_ch and self.chapter >= 1:
            # the numeral was not read; the running head lists this page's
            # chapters, and the one after the current chapter is the new one
            later = [h for h in head_ch if h > self.chapter and h <= self.nchap]
            if later and min(later) > self.chapter + 1:
                self.notes.append(f"{self.en}: head says chapter {min(later)} after {self.chapter}; {self.chapter + 1}-{min(later) - 1} missing")
                self.chapter = min(later) - 1
        self.chapter += 1
        self.verse = 1
        toks = self._strip_dropcap(toks)
        # a lone letter Samoan does not use, at the end of the first line, is
        # the drop-cap numeral the OCR pushed into the text (`foi Q`)
        if len(toks) > 2 and re.fullmatch(r"[QXZJBCDWY]", toks[-1]):
            toks = toks[:-1]
        self.buf = [{"toks": toks, "indent": 0}]
        self.prev_ended = bool(PUNCT.search(toks[-1]))

    def _new_verse(self, toks, m, skipped=0):
        k = split_point(toks, self.prev_ended, ref_start(self.en, self.chapter, m))
        if k:
            self.buf.append({"toks": toks[:k], "indent": 0})
        self._close_verse(skipped=skipped)
        self.verse = m
        self.buf = [{"toks": toks[k:], "indent": 0}] if toks[k:] else []
        self.prev_ended = bool(PUNCT.search(toks[-1])) if toks else self.prev_ended

    def _chapter_break_then(self, toks):
        """Marker 2 after a chapter whose numeral was not read: the buffer holds
        the end of verse N, the summary, and verse 1 of the next chapter."""
        k = split_point(toks, self.prev_ended, ref_start(self.en, self.chapter + 1, 2))
        if k:
            self.buf.append({"toks": toks[:k], "indent": 0})
        start = None
        for j in range(1, len(self.buf)):
            if self._caps_start(self.buf[j]["toks"]):
                start = j
                break
        if start is None:
            self.notes.append(f"{self.en} {self.chapter}:{self.verse}: chapter break without a caps first word -> sentence split")
            flat = join_lines([b["toks"] for b in self.buf])
            cut = None
            for j in range(len(flat) - 1, 0, -1):
                if END.search(flat[j - 1]) and flat[j][:1].isupper():
                    cut = j
                    break
            cut = cut or max(1, int(len(flat) * 0.6))
            self.buf = [{"toks": flat[:cut], "indent": 0}]
            self._close_verse()
            self.chapter += 1
            self.verse = 1
            self.buf = [{"toks": flat[cut:], "indent": 0}]
        else:
            tail = self.buf[start:]
            self.buf = self.buf[:start]
            self._close_verse(trim_summary=True)
            self.chapter += 1
            self.verse = 1
            self.buf = [{"toks": self._strip_dropcap(tail[0]["toks"]), "indent": 0}] + tail[1:]
        self._close_verse()
        self.verse = 2
        self.buf = [{"toks": toks[k:], "indent": 0}] if toks[k:] else []
        self.prev_ended = bool(PUNCT.search(toks[-1])) if toks else True

    def _close_verse(self, skipped=0, trim_summary=False):
        if self.chapter == 0 or self.verse == 0:
            return
        buf = list(self.buf)
        if trim_summary:
            # the next chapter's summary: indented line(s) at the end of the
            # buffer, never the verse's own first line
            while len(buf) > 1 and buf[-1]["indent"] >= 3:
                buf.pop()
        flat = join_lines([b["toks"] for b in buf])
        if skipped:
            # the buffer holds `skipped`+1 verses: each inner verse begins after
            # a punctuation mark, where the later edition's opening words say
            n = skipped + 1
            bounds = [j for j in range(1, len(flat)) if PUNCT.search(flat[j - 1])]
            cuts = []
            for s_ in range(1, n):
                target = len(flat) * s_ / n
                ref = ref_start(self.en, self.chapter, self.verse + s_)
                pick = None
                if ref and bounds:
                    rn = [_norm_tok(t) for t in ref]
                    scored = []
                    for j in bounds:
                        here = [_norm_tok(t) for t in flat[j:j + 4]]
                        run = 0
                        for a_, b_ in zip(here, rn):
                            if a_ and a_ == b_:
                                run += 1
                            else:
                                break
                        scored.append((run, -abs(j - target), j))
                    scored.sort(reverse=True)
                    if scored and scored[0][0] >= 1:
                        pick = scored[0][2]
                if pick is None and bounds:
                    caps = [j for j in bounds if flat[j][:1].isupper()] or bounds
                    pick = min(caps, key=lambda j: abs(j - target))
                if pick is None:
                    pick = int(target)
                bounds = [x for x in bounds if x > pick]
                cuts.append(pick)
            cuts = sorted(set(cuts))
            pieces, prev = [], 0
            for c in cuts + [len(flat)]:
                pieces.append(flat[prev:c])
                prev = c
            while len(pieces) < n:
                pieces.append([])
            for off, piece in enumerate(pieces):
                self._emit(self.verse + off, piece, ["split"])
        else:
            self._emit(self.verse, flat, [])
        self.buf = []

    def _emit(self, v, toks, flags):
        key = f"{self.en}|{self.chapter}|{v}"
        text = " ".join(toks).strip()
        if key in self.verses:
            self.notes.append(f"{key}: emitted twice; second kept")
        self.verses[key] = {"sm": text, "flags": list(flags)}

    def close_book(self):
        if self.chapter and self.verse:
            self._close_verse()
        self.book_done = True


# ── OCR repair against the later edition ──────────────────────────────────────

# OCR letter confusions seen in this scan: each maps a misread run to what was
# printed. Applied to a token only when the result is a KNOWN word.
known_plain: set = set()
SOV_WORDS: set = set()
CAPITALISED: Counter = Counter()
LOWERCASED: Counter = Counter()
CONFUSIONS = [("rn", "m"), ("fc", "t"), ("ii", "li"), ("ll", "ll"), ("l", "i"), ("i", "l"), ("I", "l"),
              ("l", "I"), ("u", "n"), ("n", "u"), ("cl", "d"), ("0", "o"), ("1", "l"), ("5", "s"),
              ("j", "i"), ("vv", "w"), ("‘", "‘"), ("aa", "ā")]
JUNK = re.compile(r"[\^~|*_=<>{}\[\]#%&@\\/]+")


def _variants(tok: str):
    """Spellings this token could have been misread from, one confusion at a time
    (and two for the commonest, l/i), letters only."""
    out = set()
    for a, b in CONFUSIONS:
        if a in tok:
            for k in range(tok.count(a)):
                parts = tok.split(a)
                cand = a.join(parts[:k + 1]) + b + a.join(parts[k + 1:])
                out.add(cand)
            out.add(tok.replace(a, b))
    more = set()
    for v in out:
        for a, b in (("l", "i"), ("i", "l")):
            if a in v:
                more.add(v.replace(a, b, 1))
    return (out | more) - {tok}


def repair(text: str, reference: str, freq_1887: Counter, freq_ref: Counter, known: set) -> tuple[str, int]:
    """Correct the scan's OCR slips.

    A token that is a KNOWN Samoan word (the later edition, or common in the
    1887 text itself) is left alone. Otherwise, in order: the later edition's
    aligned word when it is close (Lokou / Upu are not close, and stay); a
    letter-confusion variant that is a known word (iava -> lava, rnaua -> maua,
    Levl -> Levi, lesu -> Iesu, monl -> moni); junk characters stripped. Case
    and punctuation of the 1887 token are kept."""
    a = text.split()
    b = reference.split()
    strip = lambda t: re.sub(r"[^A-Za-zāēīōūĀĒĪŌŪ’ʻ‘]", "", t)
    ka = [strip(t).lower() for t in a]
    kb = [strip(t).lower() for t in b]
    aligned = {}
    sm = difflib.SequenceMatcher(None, ka, kb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            for i, j in zip(range(i1, i2), range(j1, j2)):
                aligned[i] = j
    fixes = 0
    out = list(a)
    demacron = str.maketrans("āēīōūĀĒĪŌŪ", "aeiouAEIOU")

    def rebuild(orig: str, core_new: str) -> str:
        lead = re.match(r"^[^\wāēīōū’ʻ‘]*", orig).group(0)
        trail = re.search(r"[^\wāēīōū’ʻ‘]*$", orig).group(0)
        body = orig[len(lead):len(orig) - len(trail)] if trail else orig[len(lead):]
        if body[:1].isupper() and core_new[:1].islower():
            core_new = core_new[:1].upper() + core_new[1:]
        # a name the reference writes with a capital keeps it (leova -> Ieova)
        if core_new[:1].islower() and CAPITALISED.get(core_new.lower(), 0) >= 3 \
                and CAPITALISED.get(core_new.lower(), 0) > 3 * LOWERCASED.get(core_new.lower(), 0):
            core_new = core_new[:1].upper() + core_new[1:]
        return lead + core_new + trail

    for i, tok in enumerate(a):
        x = ka[i]
        if not x or len(x) < 2:
            continue
        cleaned = JUNK.sub("", tok)
        if cleaned != tok and cleaned:
            out[i] = cleaned
            tok = cleaned
            fixes += 1
            x = strip(tok).lower()
            if not x:
                continue
        # `ie` FOR `le` (user, 2026-09-05: "you have an i in for the le"). `ie`
        # is a word -- cloth; `fale ie` a tent -- so the known-word test kept
        # the misread article: `o ie Alo o le Atua` (John 1:49). In ARTICLE
        # position it is `le`: after a particle that heads a phrase (o, i, a, e,
        # ma, mo, mai, ia, ai) or a marker, with a word following; or where the
        # later edition's aligned word is `le`. `le ie`, `fale ie`, `se ie` --
        # the cloth -- keep their `ie`.
        if x == "ie" and i + 1 < len(a) and ka[i + 1]:
            prev = ka[i - 1] if i else ""
            j = aligned.get(i)
            if (prev in ("o", "i", "a", "e", "ma", "mo", "mai", "ia", "ai", "ua", "sa", "na", "ona", "ina", "pe", "po")
                    and not re.search(r"[,;:.?!]$", a[i - 1] if i else "")) or (j is not None and kb[j] == "le"):
                out[i] = rebuild(tok, "le")
                fixes += 1
                continue
        # `lesu` FOR `Iesu`: the capital I read as l. The misread is frequent enough
        # in the scan to pass as a known word, so it is caught by shape: a token
        # opening on lowercase l whose I-form is a name the references capitalise
        if x[:1] == "l" and x not in SOV_WORDS and CAPITALISED.get("i" + x[1:], 0) >= 3 \
                and CAPITALISED.get("i" + x[1:], 0) > 3 * LOWERCASED.get(x, 0) + 3 * CAPITALISED.get(x, 0):
            out[i] = rebuild(tok, "I" + strip(tok)[1:])
            fixes += 1
            continue
        if x in known or x.translate(demacron) in known_plain:
            continue          # a macron is spelling, never an OCR slip (māna / mana)
        # 0. GLUED WORDS: the OCR ran two or three words together, sometimes with
        #    a stray mark between (`uigapea`, `faamatalaina.le`, John 1:38). An
        #    unknown token that is exactly a run of reference words, joined, is
        #    that run.
        glued = None
        xs = re.sub(r"[^a-zāēīōū’ʻ‘]", "", x)
        for j0 in range(len(kb)):
            for L in (2, 3):
                run = kb[j0:j0 + L]
                if len(run) == L and all(run) and "".join(run) == xs:
                    glued = [strip(t) for t in b[j0:j0 + L]]
                    break
            if glued:
                break
        if glued:
            lead = re.match(r"^[^\wāēīōū’ʻ‘]*", tok).group(0)
            trail = re.search(r"[^\wāēīōū’ʻ‘]*$", tok).group(0)
            words = list(glued)
            if strip(tok)[:1].isupper():
                words[0] = words[0][:1].upper() + words[0][1:]
            out[i] = lead + " ".join(words) + trail
            fixes += 1
            continue
        # 1. the aligned word of the later edition, when close
        j = aligned.get(i)
        if j is not None:
            y = kb[j]
            if y and y in known and abs(len(x) - len(y)) <= 1 and difflib.SequenceMatcher(None, x, y).ratio() >= 0.7 \
                    and x.translate(demacron) != y.translate(demacron):
                out[i] = rebuild(tok, strip(b[j]))
                fixes += 1
                continue
        # 2. a letter-confusion variant that is a known word (the commonest wins)
        cands = [v for v in _variants(x) if v in known and v.translate(demacron) != x.translate(demacron)]
        if cands:
            best = max(cands, key=lambda v: (freq_ref.get(v, 0) + freq_1887.get(v, 0), -abs(len(v) - len(x))))
            # keep the original's capital letter positions where the length matches
            core = strip(tok)
            if len(core) == len(best):
                best = "".join(bc.upper() if oc.isupper() else bc for oc, bc in zip(core, best))
            out[i] = rebuild(tok, best)
            fixes += 1
    return " ".join(out), fixes


# ── main ──────────────────────────────────────────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", help="debug: print the lines and markers of these page indexes, e.g. 968 or 16-18")
    ap.add_argument("--book", help="one book id, e.g. john")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-repair", action="store_true")
    ap.add_argument("--trace", action="store_true", help="print every line decision")
    ap.add_argument("--chapter", help="with --book: print this chapter verse by verse")
    ap.add_argument("--show-low", type=int, default=0, help="with --book: print this many low-similarity verses")
    a = ap.parse_args(argv)
    doc = fitz.open(PDF)

    if a.pages:
        lo, _, hi = a.pages.partition("-")
        for pi in range(int(lo), int(hi or lo) + 1):
            head, cols = parse_page(doc[pi])
            print(f"=== page {pi}  head={head!r} -> {parse_head(head)}")
            for side, col in zip("TLR", cols):
                for ln in col:
                    mk = f"[{ln['marker_raw']}->{ln['marker']}]" if ln["marker_raw"] else ""
                    ind = f"{ln['indent']:+.0f}" if ln["indent"] is not None else "  "
                    print(f"  {side} {ln['y']:6.1f} {ind:>4} {mk:10} {'T' if ln['caps_title'] else ' '} {' '.join(ln['toks'])}")
        return 0

    assign = page_range_by_book(doc)
    pages_of = defaultdict(list)
    for bidx, pi in assign:
        pages_of[bidx].append(pi)
    targets = range(66) if a.all else [BOOK_ID.index(a.book)]
    seg = Segmenter(doc, verbose=a.trace)
    freq_1887, freq_ref = Counter(), Counter()
    for bidx in targets:
        pages = book_pages(bidx, pages_of, len(doc))
        seg.run_book(bidx, pages)
    for key, rec in seg.verses.items():
        for t in rec["sm"].split():
            freq_1887[re.sub(r"[^a-zāēīōū’ʻ‘]", "", t.lower())] += 1
    for key, rec in NUMBERED.items():
        for t in rec["sm"].split():
            freq_ref[re.sub(r"[^a-zāēīōū’ʻ‘]", "", t.lower())] += 1
    sov_words = Counter()
    for key, text in SOV.items():
        for t in text.split():
            w = re.sub(r"[^a-zāēīōū’ʻ‘]", "", t.lower())
            if w:
                sov_words[w] += 1
                freq_ref[w] += 1
    # KNOWN SAMOAN WORDS: anything the later edition writes twice, anything the
    # 1887 text itself writes often (a systematic misread is never that common
    # once the later edition disagrees), every word of the typed 1887 chapters,
    # and the curated Book of Mormon
    known = {w for w, n in freq_ref.items() if n >= 2 and w} | {w for w, n in freq_1887.items() if n >= 25 and w and freq_ref.get(w, 0) >= 3} | set(sov_words)
    try:
        bom = json.load(open(ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json", encoding="utf8"))
        for bk in bom["books"]:
            for ch in bk["chapters"]:
                for v in ch["verses"]:
                    for w in v["words"]:
                        k = re.sub(r"[^a-zāēīōū’ʻ‘]", "", w["sm"].lower())
                        if k:
                            known.add(k)
    except Exception as exc:   # the Book of Mormon file is a bonus, not a requirement
        print("bom_books.json not used for the known-word set:", exc)
    global known_plain, CAPITALISED, LOWERCASED
    known_plain = {w.translate(str.maketrans("āēīōū", "aeiou")) for w in known}
    # how the later edition capitalises each word, for repaired names
    CAPITALISED, LOWERCASED = Counter(), Counter()
    for text in [rec["sm"] for rec in NUMBERED.values()] + list(SOV.values()):
        for t in text.split():
            core = re.sub(r"[^A-Za-zāēīōūĀĒĪŌŪ’ʻ‘]", "", t)
            if len(core) >= 3:
                (CAPITALISED if core[0].isupper() else LOWERCASED)[core.lower()] += 1
    global SOV_WORDS
    SOV_WORDS = set(sov_words)
    print(f"typed 1887 chapters (sov/): {len(SOV)} verses")
    print(f"known Samoan words: {len(known)}")

    # report + repair
    report = []
    total = found = low = fixes = 0
    for bidx in targets:
        en = EN_NAME[bidx]
        nb = nf = nl = 0
        for c, n in KC[en].items():
            for v in range(1, n + 1):
                key = f"{en}|{c}|{v}"
                nb += 1
                rec = seg.verses.get(key)
                ref = reference(key)
                if rec and rec["sm"]:
                    nf += 1
                    if not a.no_repair:
                        rec["sm"], k = repair(rec["sm"], ref, freq_1887, freq_ref, known)
                        fixes += k
                    s = similarity(rec["sm"], ref) if ref else 1.0
                    rec["sim"] = round(s, 2)
                    if s < 0.45:
                        nl += 1
                        rec["flags"].append("low-sim")
        report.append((en, nb, nf, nl))
        total += nb; found += nf; low += nl
    print(f"{'book':18} {'verses':>7} {'found':>6} {'low-sim':>8}")
    for en, nb, nf, nl in report:
        print(f"{en:18} {nb:7} {nf:6} {nl:8}")
    print(f"TOTAL {total} found {found} ({100*found/max(1,total):.1f}%) low-sim {low}  OCR repairs {fixes}")
    print(f"{len(seg.notes)} notes")
    for n in seg.notes[:40]:
        print("  ", n)

    if a.book:
        en = EN_NAME[BOOK_ID.index(a.book)]
        # per chapter: found / low-sim, and the low-sim verses themselves
        print("chapter  found/verses  low-sim")
        for c, n in KC[en].items():
            recs = [seg.verses.get(f"{en}|{c}|{v}") for v in range(1, n + 1)]
            nf = sum(1 for r in recs if r and r["sm"]); nl = sum(1 for r in recs if r and "low-sim" in r["flags"])
            if nf < n or nl:
                print(f"  {c:>4}    {nf:3}/{n:<3}        {nl}")
        shown = 0
        for c, n in KC[en].items():
            for v in range(1, n + 1):
                key = f"{en}|{c}|{v}"; rec = seg.verses.get(key)
                if rec and "low-sim" in rec["flags"] and shown < (a.show_low or 0):
                    shown += 1
                    print(f"\n  LOW {c}:{v} sim={rec['sim']}\n   1887: {rec['sm'][:220]}\n   ref:   {reference(key)[:220]}")
        for c in ([a.chapter] if a.chapter else []):
            for v in range(1, KC[en][c] + 1):
                key = f"{en}|{c}|{v}"
                rec = seg.verses.get(key)
                print(f"\n[{c}:{v}] sim={rec['sim'] if rec else '-'} {rec['flags'] if rec else ''}")
                print("  1887:", rec["sm"] if rec else "(missing)")
                print("  ref:  ", reference(key))
    if a.all:
        json.dump({"source": "archive.org oletusipaiaole00lond (BFBS 1887), text layer of the PDF; segmented by scripts/segment_1887_pdf.py",
                   "verses": seg.verses, "notes": seg.notes},
                  open(OUT, "w", encoding="utf8"), ensure_ascii=False, indent=0)
        print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
