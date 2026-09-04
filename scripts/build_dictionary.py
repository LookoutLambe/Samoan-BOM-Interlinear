#!/usr/bin/env python3
"""Build a Samoan-English dictionary from Pratt (1893), public domain.

THE TOOL HAD NO DICTIONARY. Its whole lexicon was the curated Book of Mormon --
111,683 unit pairs -- so everything it knew about a word it had inferred from
how that word was glossed somewhere in that one book. Which meant a word the
Book of Mormon never uses had no meaning at all (`perisitua`, `epikopo`,
`korama` were blank until they were written in by hand), and a word with more
senses than the Book of Mormon happens to show could only ever be read the way
it appears there: `sau` has ~90 witnesses, all "come", and exactly one "dew".

George Pratt, `A Grammar and Dictionary of the Samoan Language`, 3rd edition
1893 (archive.org agrammaranddict00pratgoog) -- out of copyright, and the
standard historical lexicon. The Samoan-English vocabulary runs from the
"SAMOAN AND ENGLISH VOCABULARY" heading to the English-Samoan one.

THE SCAN IS OCR AND IT IS ROUGH. The glottal is printed as `*` or `^`, small
capitals run into the text, and the running heads land mid-entry. So this is
deliberately timid: an entry is kept only when the headword is clean Samoan
letters and the definition yields English that is actually English. What it
cannot parse it drops rather than guessing -- a wrong dictionary entry is worse
than a missing one, because it would be believed.

    python3 build_dictionary.py --source <djvu.txt> [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"
OUT = RES / "samoan_dictionary.json"

START = "SAMOAN AND ENGLISH VOCABULARY"
END = "ENGLISH AND SAMOAN VOCABULARY"

# THE PART OF SPEECH IS HOW AN ENTRY IS RECOGNISED, and the scan mangles it.
# Pratt sets headwords in SMALL CAPS, which OCRs as all-caps, and the
# abbreviations come through damaged in a small number of fixed ways:
#
#     s.  (substantive)  ->  8.  or  a.
#     v.  (verb)         ->  V,  or  v,
#     pl. (plural)       ->  pi.
#     pass.              ->  pcus.  paso.
#
# Accepting those recovers most of the dictionary: the strict pattern found
# 3,668 entry lines, this one finds far more.
POS = (r"(?:v|s|8|a|ad|adv|prep|conj|pron|interj|art|num|pl|pi|pass|pcus|"
       r"paso|imp|part|dual|sing)")
ENTRY = re.compile(r"^([A-Za-z][A-Za-z'’*^`āēīōū]{1,24})\s*[,.]\s*"
                   r"(" + POS + r")\s*[,.]\s*(.+)$", re.I)

CLEAN_HEAD = re.compile(r"^[a-z’āēīōū]{2,24}$")


def fix_glottal(s: str) -> str:
    """The scan prints the glottal as * or ^ or a backtick."""
    return s.replace("*", "’").replace("^", "’").replace("`", "’")


def first_sense(defn: str) -> str:
    """The first English sense, without the Samoan illustration that follows.

    Pratt gives a definition then an example sentence IN SAMOAN. The example
    is not a gloss and must not become one, so the sense stops at the first
    sentence end or numbered sub-sense.
    """
    d = defn.strip()
    d = re.split(r"\s+\d\.\s", d)[0]           # 1. ... 2. ...
    d = re.split(r"[.;]", d)[0]
    d = re.sub(r"\bto\s+", "", d, count=1)     # "to eat food" -> "eat food"
    d = re.sub(r"[^A-Za-z ,\-]", " ", d)
    d = re.sub(r"\s+", " ", d).strip(" ,-")
    return d


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    text = Path(a.source).read_text(encoding="utf-8", errors="replace")
    i, j = text.find(START), text.find(END)
    if i < 0 or j < 0:
        print("could not find the vocabulary section")
        return 1
    body = text[i + len(START):j]

    # join an entry's continuation lines back onto it
    lines, buf = [], ""
    for raw in body.splitlines():
        ln = raw.rstrip()
        if not ln.strip():
            if buf:
                lines.append(buf); buf = ""
            continue
        if ENTRY.match(ln.strip()):
            if buf:
                lines.append(buf)
            buf = ln.strip()
        elif buf:
            buf += " " + ln.strip()
    if buf:
        lines.append(buf)

    entries: dict[str, list] = {}
    tally = Counter()
    for ln in lines:
        m = ENTRY.match(ln)
        if not m:
            tally["no entry pattern"] += 1
            continue
        head = fix_glottal(m.group(1)).lower()
        if not CLEAN_HEAD.match(head):
            tally["headword not clean Samoan"] += 1
            continue
        sense = first_sense(m.group(3))
        words = sense.split()
        # a usable sense is short English. Long ones are Pratt's Samoan
        # examples bleeding in, and one-word junk is OCR.
        if not (1 <= len(words) <= 8):
            tally["sense unusable"] += 1
            continue
        letters = sum(len(w) for w in words if w.isalpha())
        if letters < 3:
            tally["sense unusable"] += 1
            continue
        entries.setdefault(head, [])
        if sense not in entries[head]:
            entries[head].append(sense)
        tally["kept"] += 1

    print("entries kept        %d senses across %d headwords" % (tally["kept"], len(entries)))
    for k, v in tally.most_common():
        if k != "kept":
            print("  dropped: %-28s %d" % (k, v))
    for probe in ("sau", "alu", "maua", "taua", "loto", "atoa", "perisitua", "mea"):
        if probe in entries:
            print("   %-12s %s" % (probe, entries[probe][:4]))
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    OUT.write_text(json.dumps({
        "source": "George Pratt, A Grammar and Dictionary of the Samoan Language, "
                  "3rd ed. 1893 (public domain; archive.org agrammaranddict00pratgoog)",
        "note": "Parsed from the OCR by build_dictionary.py. Senses are the FIRST "
                "definition of each numbered sense, with Pratt's Samoan example "
                "sentences excluded.",
        "entries": entries,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
