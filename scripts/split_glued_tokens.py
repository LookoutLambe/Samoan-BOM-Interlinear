#!/usr/bin/env python3
"""Split the Book of Mormon's glued tokens, and move the curation with them.

An em dash, semicolon or colon between two letters is a word boundary that
carries no space, so splitting on whitespace glues the words either side into
one token -- `Atua—ma`, `nuu;Ma`. A glued token is two words wearing one label
and can never be glossed: `Atua—ma` printed blank where the verse says "God"
and "and" (1 Nephi 10:17).

`scrape_samoan_scriptures.GLUE_RE` has split these since the D&C and the Pearl
of Great Price were scraped; the Book of Mormon's 37 were left because the
hand-curated specs are written against the current token indices. This moves
the indices with the text, so the wall comes down:

    an index after the split shifts by one, and the span that held the glued
    token grows by one, keeping both halves and its English.

The punctuation stays on the LEFT token, as the corpus writes it everywhere the
space is present, so joining the tokens with spaces still round-trips the prose.

Idempotent.  python3 split_glued_tokens.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import scrape_samoan_scriptures as SS

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "O le Tusi a Mamona Interlinear" / "Resources"
SPEC_RE = re.compile(r'\((\d+),\s*(\d+),\s*"((?:[^"\\]|\\.)*)"\)')


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    books = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))
    # verse ref -> the token indices split, lowest first
    splits: dict[str, list[int]] = {}
    for b in books["books"]:
        for ch in b["chapters"]:
            for v in ch["verses"]:
                ref = f"{b['id']}|{ch['num']}|{v['num']}"
                out, cut = [], []
                for w in v["words"]:
                    parts = SS.GLUE_RE.sub(r"\1\2 ", w["sm"]).split()
                    if len(parts) > 1:
                        cut.append(len(out))          # index of the LEFT half
                        out.extend({**w, "sm": p} for p in parts)
                    else:
                        out.append(w)
                if cut:
                    splits[ref] = cut
                    v["words"] = out
    print(f"verses retokenised: {len(splits)}   tokens split: {sum(len(c) for c in splits.values())}")
    if not splits:
        return 0

    # the curation's indices move with the text
    moved = 0
    for path in sorted((ROOT / "scripts").glob("build_overrides_*.py")):
        src = open(path, encoding="utf-8").read()
        mb = re.search(r'BOOK_ID\s*=\s*"([^"]+)"', src)
        mc = re.search(r'CHAPTER_NUM\s*=\s*(\d+)', src)
        if not (mb and mc):
            continue
        book, chap, new = mb.group(1), int(mc.group(1)), src
        for vm in re.finditer(r'\n    (\d+): \[(.*?)\n    \],', src, re.S):
            cuts = splits.get(f"{book}|{chap}|{int(vm.group(1))}")
            if not cuts:
                continue
            def shift(m):
                x, y = int(m.group(1)), int(m.group(2))
                # every cut at or before the index pushes it along
                return '({}, {}, "{}")'.format(
                    x + sum(1 for k in cuts if k < x),
                    y + sum(1 for k in cuts if k <= y),
                    m.group(3))
            new = new.replace(vm.group(2), SPEC_RE.sub(shift, vm.group(2)), 1)
        if new != src:
            moved += 1
            if not a.dry_run:
                open(path, "w", encoding="utf-8").write(new)
    print(f"curation files whose indices moved: {moved}")

    if a.dry_run:
        print("(dry run, nothing written)")
        return 0
    # the file is written compact; indenting it here would rewrite 20MB and
    # bury the 37 real changes in a million-line diff
    (RES / "bom_books.json").write_text(
        json.dumps(books, ensure_ascii=False), encoding="utf-8")
    print("bom_books.json rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
