#!/usr/bin/env python3
"""Repair dash damage in the English canon, and nothing else.

The English of bom_english.json is quoted scripture and its WORDS are never
touched. Its punctuation arrived damaged from the import, and the damage is
not cosmetic: `judgment– seat` broke Helaman 8:27's text into a form that no
longer matched Helaman 8:7's copy of it, and every gloss test that asks
whether a verse contains a word was reading `olive– tree` as two words, one
of them `tree` with a stray dash welded on.

Four repairs, all of them punctuation only:

  word– word   ->  word-word    317   an en dash standing in for a hyphen,
                                      with a space that does not belong
  word–word    ->  word-word     26   the same, without the stray space
  word – word  ->  word-word      3
  word - word  ->  word-word      1
  word — word  ->  word—word      2   an em dash never takes spaces here
  word—  word  ->  word—word      1

The en dash at the END of a clause is a real em dash and is converted too.
`-ites` in 4 Nephi 1:17 is a real hyphen in the published text ("nor any
manner of -ites") and gets one.

    python3 fix_english_punctuation.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"

W = r"[A-Za-z’']"

# TWO KINDS OF BROKEN DASH, and they take opposite repairs.
#
#   olive– tree      a real compound in the published text     -> olive-tree
#   righteous– ness  a LINE-BREAK hyphen from the typesetting  -> righteousness
#
# Guessing wrong makes up a word either way. The canon decides: `righteousness`
# and `insomuch` occur whole in verses that were not broken, `olivetree` and
# `judgmentseat` occur nowhere. Same method that settled `comes` over `coms`.
_VOCAB = None


def vocabulary():
    global _VOCAB
    if _VOCAB is None:
        raw = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
        _VOCAB = set()
        for t in raw.values():
            _VOCAB.update(w.lower() for w in re.findall(r"[A-Za-z']+", t))
    return _VOCAB


def _join(m, tally):
    a, b = m.group(1), m.group(2)
    whole = (a + b)
    if whole.lower() in vocabulary():
        tally["line-break hyphen, rejoined"] += 1
        return whole
    tally["compound, hyphenated"] += 1
    return a + "-" + b


BROKEN = re.compile(rf"({W}+)\s*[–‐‑‒-]\s*({W}+)")

REPAIRS = [
    # an em dash joins clauses and takes no spaces either side
    (re.compile(rf"({W}|[,;:?!])\s*—\s+({W})"),              r"\1—\2", "em dash + space"),
    (re.compile(rf"({W}|[,;:?!])\s+—\s*({W})"),              r"\1—\2", "space + em dash"),
    # "nor any manner of -ites": a real hyphen, not an em dash
    (re.compile(r"of\s+—ites"),                              "of -ites", "-ites"),
    # an en dash closing a clause is an em dash
    (re.compile(r"–(\s*)$"),                                 r"—\1", "en dash at end"),
]


def repair(text: str, tally: Counter) -> str:
    # only where the dash is DAMAGED -- a stray space on one side or the wrong
    # character. A correctly written "judgment-seat" is left exactly as it is.
    def one(m):
        if m.group(0) == m.group(1) + "-" + m.group(2):
            return m.group(0)
        return _join(m, tally)
    text = BROKEN.sub(one, text)
    for rx, sub, name in REPAIRS:
        text, n = rx.subn(sub, text)
        if n:
            tally[name] += n
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    path = RES / "bom_english.json"
    en = json.loads(path.read_text(encoding="utf-8"))
    tally: Counter = Counter()
    changed = 0
    examples = []
    for k, v in en.items():
        fixed = repair(v, tally)
        if fixed != v:
            changed += 1
            if len(examples) < 8:
                i = next((n for n, (x, y) in enumerate(zip(v, fixed)) if x != y), 0)
                examples.append((k, v[max(0, i-26):i+26], fixed[max(0, i-26):i+26]))
            en[k] = fixed

    print(f"verses repaired {changed}")
    for name, n in tally.most_common():
        print("   %-22s %5d" % (name, n))
    print()
    for k, before, after in examples:
        print("   %-26s %r\n   %-26s %r" % (k, before, "", after))

    # WORDS ARE NEVER TOUCHED -- prove it
    words_before = sum(len(re.findall(r"[A-Za-z']+", v)) for v in
                       json.loads(path.read_text(encoding="utf-8")).values())
    words_after = sum(len(re.findall(r"[A-Za-z']+", v)) for v in en.values())
    print(f"\nletter-runs before {words_before}  after {words_after}"
          f"   (a hyphen JOINS two, so after should be lower by the repair count)")

    if a.dry_run:
        print("(dry run, nothing written)")
        return 0
    path.write_text(json.dumps(en, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
