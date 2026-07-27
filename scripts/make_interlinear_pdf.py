#!/usr/bin/env python3
"""
Render the full Samoan–English interlinear Book of Mormon to a single
6 x 9 inch, Amazon KDP-ready PDF, laid out like the standard scriptures:

  * TWO columns per page
  * each VERSE is its own paragraph, opened by a bold verse number
  * a RUNNING HEAD on every page showing the book + chapter:verse range
  * mirrored gutter margins and a centered folio (page number)

Each interlinear unit is a Samoan surface form set above its English gloss,
flowing left-to-right and wrapping inside its column, exactly like the reader.
Continuation glosses (en == "·") group with the following real gloss into one
multi-word unit.

Run:  python3 scripts/make_interlinear_pdf.py
Out:  ~/Desktop/Samoan-English Interlinear Book of Mormon (6x9).pdf
"""

from __future__ import annotations

import json
import os
import sys
from fpdf import FPDF


def _parse_trim():
    """Trim size in inches from argv, e.g. `7x10` or `8.5x11`. Default 6x9."""
    for a in sys.argv[1:]:
        s = a.lower().replace("in", "").strip()
        if "x" in s:
            try:
                w, h = s.split("x")
                return float(w), float(h)
            except ValueError:
                pass
    return 6.0, 9.0


TRIM_W_IN, TRIM_H_IN = _parse_trim()

# ---- paths -----------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOKS = os.path.join(ROOT, "O le Tusi a Mamona Interlinear", "Resources", "bom_books.json")
OVERRIDES = os.path.join(ROOT, "O le Tusi a Mamona Interlinear", "Resources", "bom_overrides.json")
def _trim_label(w, h):
    def f(x):
        return str(int(x)) if float(x).is_integer() else str(x)
    return f"{f(w)}x{f(h)}"


OUT = os.path.join(os.path.expanduser("~"), "Desktop",
                   f"Samoan-English Interlinear Book of Mormon ({_trim_label(TRIM_W_IN, TRIM_H_IN)}).pdf")

FONT_DIR = "/System/Library/Fonts/Supplemental"
FONTS = {
    "": os.path.join(FONT_DIR, "Times New Roman.ttf"),
    "B": os.path.join(FONT_DIR, "Times New Roman Bold.ttf"),
    "I": os.path.join(FONT_DIR, "Times New Roman Italic.ttf"),
    "BI": os.path.join(FONT_DIR, "Times New Roman Bold Italic.ttf"),
}

# ---- geometry (points; 72 pt = 1 in) --------------------------------------

PAGE_W, PAGE_H = TRIM_W_IN * 72, TRIM_H_IN * 72
GUTTER = 0.875 * 72       # binding-side margin
OUTER = 0.5 * 72
TOP = 0.7 * 72            # a little extra room for the running head
BOTTOM = 0.6 * 72
COL_GAP = 18.0            # space between the two columns
CONTENT_BOTTOM = PAGE_H - BOTTOM

# ---- type sizes ------------------------------------------------------------

SM_SIZE = 9.5             # Samoan surface form
GL_SIZE = 7.0             # English gloss (italic)
NUM_SIZE = 8.5            # verse number (bold)

SM_LINE = 11.5
GL_LINE = 8.5
STACK_GAP = 1.0
ROW_GAP = 3.0            # between wrapped rows inside a verse
PARA_GAP = 4.0          # between verses (paragraph spacing)
UNIT_GAP = 6.0          # between units on a row
NUM_GAP = 3.0           # after a verse number before its first word

SM_ASCENT = SM_SIZE * 0.80
GL_ASCENT = GL_SIZE * 0.80
MIN_ROW = SM_LINE + STACK_GAP + GL_LINE

# Black-only interior (KDP B&W). Everything prints as solid black; the Samoan
# vs. gloss hierarchy comes from size + italic, not color.
INK = (0, 0, 0)
GLOSS_INK = (0, 0, 0)
ACCENT = (0, 0, 0)
RULE = (0, 0, 0)

# ---- data ------------------------------------------------------------------

def load_stream():
    books = json.load(open(BOOKS))["books"]
    ov = json.load(open(OVERRIDES))["verses"]
    stream = []
    for b in books:
        stream.append(("book", b["nameSm"], b["nameEn"]))
        for c in b["chapters"]:
            stream.append(("chapter", c["num"]))
            for v in c["verses"]:
                units = []
                ws = ov[f"{b['id']}|{c['num']}|{v['num']}"]
                i, n = 0, len(ws)
                while i < n:
                    if ws[i]["en"] == "·":
                        j = i
                        while j < n and ws[j]["en"] == "·":
                            j += 1
                        sm = " ".join(ws[k]["sm"] for k in range(i, min(j + 1, n)))
                        gl = ws[j]["en"] if j < n else ""
                        units.append((sm, gl))
                        i = j + 1
                    else:
                        units.append((ws[i]["sm"], ws[i]["en"]))
                        i += 1
                stream.append(("verse", c["num"], v["num"], units))
    return stream


class Book(FPDF):
    def __init__(self):
        super().__init__(unit="pt", format=(PAGE_W, PAGE_H))
        self.set_auto_page_break(False)
        for style, path in FONTS.items():
            self.add_font("TNR", style, path)
        self.set_title("Samoan-English Interlinear Book of Mormon")
        self.set_author("Christopher Lambe")


def ref_range(book_en, first, last):
    """A running-head reference like '1 Nephi 3:5–4:2' or '1 Nephi 3:5–14'."""
    if not first:
        return book_en
    (c1, v1), (c2, v2) = first, last
    if c1 == c2 and v1 == v2:
        return f"{book_en} {c1}:{v1}"
    if c1 == c2:
        return f"{book_en} {c1}:{v1}–{v2}"
    return f"{book_en} {c1}:{v1}–{c2}:{v2}"


def main():
    stream = load_stream()
    pdf = Book()

    # ---- title page ----------------------------------------------------
    pdf.add_page()
    pdf.set_text_color(*INK)
    pdf.set_font("TNR", "B", 30)
    t = "O le Tusi a Mamona"
    pdf.text((PAGE_W - pdf.get_string_width(t)) / 2, 250, t)
    pdf.set_font("TNR", "", 15)
    s = "The Book of Mormon"
    pdf.text((PAGE_W - pdf.get_string_width(s)) / 2, 278, s)
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.8)
    pdf.line(PAGE_W / 2 - 90, 300, PAGE_W / 2 + 90, 300)
    pdf.set_font("TNR", "I", 13)
    for i, ln in enumerate(["Samoan – English", "Interlinear Edition"]):
        pdf.text((PAGE_W - pdf.get_string_width(ln)) / 2, 328 + i * 20, ln)
    pdf.add_page()  # blank verso so book 1 opens recto

    # ---- layout state --------------------------------------------------
    state = {
        "x0": 0.0, "x1": 0.0,          # page content bounds (mirrored)
        "col": 0, "cx0": 0.0, "cx1": 0.0,
        "col_top": TOP,
        "x": 0.0, "y": 0.0, "row_h": 0.0,
        "book_en": "", "book_sm": "",
        "first_ref": None, "last_ref": None,
        "book_open": False,            # suppress ref head on a book-title page
    }

    def page_bounds():
        recto = (pdf.page_no() % 2 == 1)
        x0 = GUTTER if recto else OUTER
        x1 = PAGE_W - (OUTER if recto else GUTTER)
        return x0, x1

    def col_width():
        return (state["x1"] - state["x0"] - COL_GAP) / 2.0

    def set_column(idx):
        cw = col_width()
        state["col"] = idx
        if idx == 0:
            state["cx0"] = state["x0"]
        else:
            state["cx0"] = state["x0"] + cw + COL_GAP
        state["cx1"] = state["cx0"] + cw
        state["x"] = state["cx0"]
        state["y"] = state["col_top"]
        state["row_h"] = 0.0

    def finalize_page():
        # nothing to draw on truly-blank front-matter / spacer pages
        if not (state["first_ref"] or state["book_open"]):
            return
        # centered folio
        pdf.set_font("TNR", "", 9)
        pdf.set_text_color(*INK)
        f = str(pdf.page_no())
        pdf.text((PAGE_W - pdf.get_string_width(f)) / 2, PAGE_H - 22, f)
        # vertical rule between the two columns
        if state["first_ref"]:
            midx = state["x0"] + col_width() + COL_GAP / 2
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(0.5)
            pdf.line(midx, state["col_top"], midx, CONTENT_BOTTOM)
        # dual running head — Samoan · English (skip on book-title pages)
        if state["first_ref"] and not state["book_open"]:
            sm_ref = ref_range(state["book_sm"], state["first_ref"], state["last_ref"])
            en_ref = ref_range(state["book_en"], state["first_ref"], state["last_ref"])
            head = f"{sm_ref}    ·    {en_ref}"
            pdf.set_font("TNR", "I", 8.5)
            pdf.set_text_color(*GLOSS_INK)
            pdf.text((PAGE_W - pdf.get_string_width(head)) / 2, TOP - 20, head)
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(0.5)
            pdf.line(state["x0"], TOP - 14, state["x1"], TOP - 14)
            # matching footer rule above the folio
            pdf.line(state["x0"], PAGE_H - 34, state["x1"], PAGE_H - 34)

    def new_page(book_open=False, col_top=TOP):
        finalize_page()
        pdf.add_page()
        state["x0"], state["x1"] = page_bounds()
        state["col_top"] = col_top
        state["book_open"] = book_open
        state["first_ref"] = None
        state["last_ref"] = None
        set_column(0)

    def next_column():
        if state["col"] == 0:
            set_column(1)
        else:
            new_page()

    def newline(gap=ROW_GAP):
        rh = state["row_h"] if state["row_h"] else MIN_ROW
        state["y"] += rh + gap
        state["x"] = state["cx0"]
        state["row_h"] = 0.0
        if state["y"] + MIN_ROW > CONTENT_BOTTOM:
            next_column()

    def place_unit(sm, gl, sm_style="", num=False):
        colw = state["cx1"] - state["cx0"]
        ssize = NUM_SIZE if num else SM_SIZE
        # wrap
        pdf.set_font("TNR", sm_style, ssize)
        sm_lines = _wrap(pdf, sm, colw)
        sm_w = max((pdf.get_string_width(l) for l in sm_lines), default=0.0)
        gl_lines = _wrap_font(pdf, gl, "I", GL_SIZE, colw) if gl else []
        pdf.set_font("TNR", "I", GL_SIZE)
        uw = max([sm_w] + [pdf.get_string_width(l) for l in gl_lines])
        sm_block = len(sm_lines) * SM_LINE
        uh = sm_block + ((STACK_GAP + len(gl_lines) * GL_LINE) if gl_lines else 0.0)

        trailing = (NUM_GAP if num else UNIT_GAP)
        if state["x"] + uw > state["cx1"] and state["x"] > state["cx0"]:
            newline()
        if state["y"] + uh > CONTENT_BOTTOM:
            next_column()

        x, y = state["x"], state["y"]
        pdf.set_text_color(*(ACCENT if num else INK))
        pdf.set_font("TNR", sm_style, ssize)
        by = y + SM_ASCENT
        for l in sm_lines:
            pdf.text(x + (uw - pdf.get_string_width(l)) / 2, by, l)
            by += SM_LINE
        if gl_lines:
            pdf.set_text_color(*GLOSS_INK)
            pdf.set_font("TNR", "I", GL_SIZE)
            by = y + sm_block + STACK_GAP + GL_ASCENT
            for l in gl_lines:
                pdf.text(x + (uw - pdf.get_string_width(l)) / 2, by, l)
                by += GL_LINE

        state["x"] += uw + trailing
        state["row_h"] = max(state["row_h"], uh)

    # ---- walk the stream ----------------------------------------------
    for tok in stream:
        kind = tok[0]

        if kind == "book":
            _, name_sm, name_en = tok
            # open each book on a fresh recto, below a centered title block
            finalize_page()
            pdf.add_page()
            if pdf.page_no() % 2 == 0:   # landed on a verso: leave it blank, jump to recto
                pdf.add_page()
            state["x0"], state["x1"] = page_bounds()
            state["book_open"] = True
            state["book_en"] = name_en
            state["book_sm"] = name_sm
            state["first_ref"] = None
            state["last_ref"] = None
            cx = (state["x0"] + state["x1"]) / 2
            ty = TOP + 30
            pdf.set_text_color(*INK)
            pdf.set_font("TNR", "B", 26)
            pdf.text(cx - pdf.get_string_width(name_sm) / 2, ty, name_sm)
            ty += 24
            pdf.set_font("TNR", "I", 14)
            pdf.set_text_color(*GLOSS_INK)
            pdf.text(cx - pdf.get_string_width(name_en) / 2, ty, name_en)
            ty += 12
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(1.0)
            pdf.line(cx - 70, ty, cx + 70, ty)
            state["col_top"] = ty + 22
            set_column(0)

        elif kind == "chapter":
            _, num = tok
            if state["x"] > state["cx0"]:
                newline(gap=PARA_GAP)
            # keep the heading with the start of its chapter: it needs room for
            # itself plus the first couple of interlinear rows, or it moves to
            # the next column / page (no stranded heading at a column foot).
            needed = 20 + PARA_GAP + 2 * MIN_ROW
            if state["y"] + needed > CONTENT_BOTTOM:
                next_column()
            cwmid = (state["cx0"] + state["cx1"]) / 2
            pdf.set_font("TNR", "B", 12)
            pdf.set_text_color(*ACCENT)
            head = f"Mataupu {num}"
            pdf.text(cwmid - pdf.get_string_width(head) / 2, state["y"] + 10, head)
            state["y"] += 20
            state["x"] = state["cx0"]
            state["row_h"] = 0.0

        elif kind == "verse":
            _, cnum, vnum, units = tok
            # start a new paragraph for the verse
            if state["x"] > state["cx0"]:
                newline(gap=PARA_GAP)
            if state["first_ref"] is None:
                state["first_ref"] = (cnum, vnum)
            state["last_ref"] = (cnum, vnum)
            place_unit(str(vnum), "", sm_style="B", num=True)
            for sm, gl in units:
                place_unit(sm, gl)

    finalize_page()
    pdf.output(OUT)
    print(f"pages: {pdf.page_no()}")
    print(f"wrote: {OUT}")
    print(f"size:  {os.path.getsize(OUT)/1_000_000:.1f} MB")


# ---- word-wrap helpers -----------------------------------------------------

def _wrap(pdf, text, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if pdf.get_string_width(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _wrap_font(pdf, text, style, size, max_w):
    pdf.set_font("TNR", style, size)
    return _wrap(pdf, text, max_w)


if __name__ == "__main__":
    main()
