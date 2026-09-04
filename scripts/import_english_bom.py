#!/usr/bin/env python3
"""Take the Book of Mormon English from the Hebrew app's curated 1920 edition.

THE SOURCE IS PUBLIC DOMAIN AND ALREADY CURATED. `Escrituras/bom/official_verses.js`
is the 1920 Library of Congress edition, rebuilt verse by verse in the Hebrew
repo: footnotes, running heads and page numbers stripped, line-break dashes
removed, OCR repaired against the previous text used only as an alignment
guide, and 57 verses the scan lost keeping the earlier text. Its 1920 readings
STAND and are not modernised -- `exceeding`, `defense`, `to-day`, `first-born`,
`white and delightsome`, `straight`, `plead`.

That is the text this interlinear should show, not a scrape of the current
edition, which is copyrighted.

WHAT THIS STILL REPAIRS. One OCR class survived that rebuild, and it is the
commonest error in the scan: the ligature `he` read as `lie`, 218 times, of
which most are the pronoun and the rest are the real verb ("lie down in
sorrow"). Position cannot tell them apart, and neither can frequency. Word-level
alignment against the current edition can: where the two texts agree everywhere
around a token and disagree only there, the 1920 token is damaged. The current
edition is used ONLY to locate damage -- never to import a reading. A difference
that is an edition variant rather than an OCR confusion is left alone, which is
why `exceeding` -> `exceedingly` and `defense` -> `defence` are not in the table.

    python3 import_english_bom.py [--dry-run] [--report]
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "O le Tusi a Mamona Interlinear" / "Resources"
HEBREW = Path.home() / "Desktop" / "untitled folder" / "Escrituras" / "bom" / "official_verses.js"

# OCR confusions only: pairs whose members are visually similar in a 1920
# letterpress scan. An affix change (exceeding/exceedingly), a spelling
# convention (defense/defence) or a real textual variant (straight/strait,
# plead/pled) is an EDITION difference and is never touched.
OCR_PAIRS = {
    ("lie", "he"), ("he", "be"), ("be", "he"), ("lie", "be"),
    ("bad", "had"), ("bath", "hath"), ("band", "hand"), ("beard", "heard"),
    ("and", "land"), ("band", "land"), ("lands", "land"), ("wall", "all"),
    ("fall", "all"), ("call", "all"), ("care", "are"), ("dearth", "earth"),
    ("fail", "fall"), ("tell", "fell"), ("lasting", "fasting"),
    ("how", "now"), ("bow", "now"), ("now", "how"), ("bow", "how"),
    ("oft", "off"), ("on", "off"), ("of", "off"), ("east", "cast"),
    ("com", "come"), ("game", "came"), ("moron", "moroni"),
    ("then", "thou"), ("than", "thou"), ("hen", "then"), ("win", "in"),
    ("turned", "burned"), ("hate", "have"), ("owe", "own"), ("down", "own"),
    ("every", "very"), ("very", "every"), ("net", "not"), ("nay", "my"),
    ("tear", "fear"), ("main", "slain"), ("stall", "shall"), ("sent", "went"),
    ("four", "our"), ("bright", "right"), ("gad", "god"), ("ll", "i"),
    ("relieved", "believed"), ("east", "feast"), ("banner", "manner"),
    ("cover", "over"), ("center", "enter"), ("at", "it"), ("it", "if"),
    ("light", "life"), ("seed", "need"), ("snever", "never"), ("roe", "me"),
    ("is", "his"), ("her", "his"), ("mark", "dark"), ("fore", "before"),
    ("old", "behold"), ("hid", "hide"), ("writ", "write"), ("ore", ""),
    ("accord", "according"), ("pointed", "appointed"), ("abound", "bound"),
    ("teeth", "brethren"), ("eight", "night"), ("seat", "sent"),
}
# a stray letter the scan inserted between words
STRAY = {"i", "a", "o", "n", "'", "ll", "see", "stiff", "die", "them", "howl",
         "must", "filth", "man", "john", "ye", "or", "much", "be", "to", "our"}


def load_1920() -> dict[str, str]:
    raw = HEBREW.read_text(encoding="utf-8")
    body = raw[raw.index("["):].rsplit("]", 1)[0] + "]"
    return {"%s|%d|%d" % (d["book"], d["chapter"], d["verse"]): d["english"]
            for d in json.loads(body)}


def repair(old: str, guide: str, tally: Counter, log: list) -> str:
    """Fix OCR-shaped single-word damage, located by alignment with `guide`."""
    a = re.findall(r"\S+", old)
    b = re.findall(r"\S+", guide)
    ka = [w.strip(".,;:!?——()“”").lower() for w in a]
    kb = [w.strip(".,;:!?——()“”").lower() for w in b]
    out = list(a)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ka, kb).get_opcodes():
        if tag == "replace" and i2 - i1 == 1 and j2 - j1 == 1:
            x, y = ka[i1], kb[j1]
            if (x, y) in OCR_PAIRS:
                out[i1] = a[i1].replace(x, y, 1) if x in a[i1] else \
                    re.sub(re.escape(x), y, a[i1], count=1, flags=re.I)
                tally[(x, y)] += 1
                log.append((x, y, " ".join(a[max(0, i1-4):i1+5])))
        elif tag == "delete" and i2 - i1 == 1 and ka[i1] in STRAY:
            out[i1] = None
            tally[(ka[i1], "∅")] += 1
            log.append((ka[i1], "∅", " ".join(a[max(0, i1-4):i1+5])))
    return " ".join(w for w in out if w is not None)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)

    src = load_1920()
    path = RES / "bom_english.json"
    en = json.loads(path.read_text(encoding="utf-8"))
    tally: Counter = Counter()
    log: list = []
    n = 0
    for k, text in src.items():
        fixed = repair(text, en.get(k, ""), tally, log)
        if a.dry_run or a.report:
            src[k] = fixed
        else:
            en[k] = fixed
        n += 1

    print(f"verses taken from the curated 1920: {n}")
    print(f"OCR repairs: {sum(tally.values())} in {len(tally)} classes")
    for (x, y), c in tally.most_common(20):
        print("   %5d  %-12s -> %s" % (c, x, y))
    if a.report:
        print()
        for x, y, ctx in log[:30]:
            print("   %-8s -> %-8s ...%s..." % (x, y, ctx))
    if a.dry_run or a.report:
        print("\n(nothing written)")
        return 0
    path.write_text(json.dumps(en, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
