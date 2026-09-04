#!/usr/bin/env python3
"""Invert the EALD Bilingual Dictionary (English-Samoan) into Samoan-English.

The second of the two lexicons, and the complement of Pratt: Pratt is
Samoan-English, 1893, and OCR-damaged; this is English-Samoan, modern, and
clean digital text. Together they cover both the archaic vocabulary of the
scripture register and the ordinary modern words Pratt's scan mangles.

    Bilingual Dictionary for ESL Beginners (Samoan), EALD.
    Supplied by the translator: ~/Desktop/eald-bilingual-dictionary-samoan.pdf

ONLY THE UNAMBIGUOUS LINES ARE TAKEN. The simple entry is

    n body tino          ->  tino = body
    v borrow nonó        ->  nonó = borrow

where the English is the single token after the part of speech and everything
after it is Samoan. The numbered senses are NOT taken --

    n 1. of car vaega i tua o le taavale e tu’u ai uta

-- because "of car" is a qualifier in English and there is no reliable way to
say where the English stops and the Samoan starts. Guessing there would put
English words into the Samoan side of a dictionary, which is worse than a
smaller dictionary.

    python3 build_dictionary_eald.py --pdf <path> [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"
OUT = RES / "samoan_dictionary_eald.json"

POS = r"(?:n|v|adj|adv|pron|prep|conj|interj|det|art|num|pt\s+v|pp\s+v)"
SIMPLE = re.compile(r"^(" + POS + r")\s+([a-z][a-z'\-]{1,20})\s+(.+)$", re.I)
SAMOAN_OK = re.compile(r"^[a-zA-Z’'‘áàéèíìóòúùāēīōū\s/()\-,\.]+$")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    import pypdf
    reader = pypdf.PdfReader(a.pdf)
    text = "\n".join((p.extract_text() or "") for p in reader.pages)

    entries: dict[str, list] = defaultdict(list)
    tally = Counter()
    for raw in text.splitlines():
        ln = raw.strip()
        m = SIMPLE.match(ln)
        if not m:
            tally["not a simple entry"] += 1
            continue
        english, samoan = m.group(2).lower(), m.group(3).strip()
        if not SAMOAN_OK.match(samoan) or "*see" in samoan:
            tally["samoan side unusable"] += 1
            continue
        # a Samoan side may list alternatives: `la’ua uma, toalua`
        for alt in re.split(r"[,/]", samoan):
            alt = alt.strip().strip(".")
            # a whole clause is a definition, not a headword
            if not alt or len(alt.split()) > 3:
                continue
            key = alt.lower()
            if english not in entries[key]:
                entries[key].append(english)
                tally["kept"] += 1

    entries = {k: v for k, v in entries.items() if re.match(r"^[a-z’‘áéíóúāēīōū]", k)}
    print("senses kept   %d across %d Samoan headwords" % (tally["kept"], len(entries)))
    for k, v in tally.most_common():
        if k != "kept":
            print("  dropped: %-24s %d" % (k, v))
    for probe in ("tino", "tusi", "fale", "alu", "sau", "loto", "mea", "atua"):
        if probe in entries:
            print("   %-10s %s" % (probe, entries[probe][:5]))
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    OUT.write_text(json.dumps({
        "source": "Bilingual Dictionary for ESL Beginners (Samoan), EALD — "
                  "English-Samoan, inverted to Samoan-English",
        "note": "Only unambiguous `<pos> <english> <samoan>` lines are taken; "
                "numbered senses with English qualifiers are skipped.",
        "entries": entries,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
