#!/usr/bin/env python3
"""Score a generated pass against the hand curation it replaced.

The Book of Mormon was glossed by hand across 239 chapter scripts. That makes
it an ANSWER KEY: 346,933 tokens where a human already decided what the gloss
should be. Any rule added to the grammar can be measured against it instead of
argued about, and a rule that lowers agreement is wrong however good it looks.

    AGREE     same token, same gloss
    DIFFER    both glossed it, differently        <- read these
    LOST      curation glossed it, the pass did not
    ADDED     the pass glossed it, curation did not

`--differ WORD` and `--lost` print examples, which is how the next rule gets
found.

    python3 score_against_curation.py [--differ o] [--lost] [-n 25]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"
SCRATCH = Path("/private/tmp/claude-501/-Users-chrislambe-Desktop-untitled-folder"
               "/613c68df-5949-46cb-8611-81201268d964/scratchpad")
CONT = "·"


def norm_gloss(g):
    return re.sub(r"[^a-z ]", "", (g or "").lower()).strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--differ", help="show examples for this Samoan token")
    ap.add_argument("--lost", action="store_true")
    ap.add_argument("--added", action="store_true")
    ap.add_argument("-n", type=int, default=20)
    ap.add_argument("--baseline", default=str(SCRATCH / "bom_overrides.CURATED.json"))
    a = ap.parse_args(argv)

    new = json.loads((RES / "bom_overrides.json").read_text(encoding="utf-8"))
    old = json.loads(Path(a.baseline).read_text(encoding="utf-8"))
    curated = set(old["verses"]) - set(old.get("generated", []))

    tally = Counter()
    by_token = {"DIFFER": Counter(), "LOST": Counter(), "ADDED": Counter()}
    examples = {"DIFFER": [], "LOST": [], "ADDED": []}

    for key in sorted(curated):
        o, n = old["verses"][key], new["verses"].get(key)
        if not n or len(o) != len(n):
            tally["SKIPPED (token count changed)"] += 1
            continue
        for wo, wn in zip(o, n):
            go, gn = (wo.get("en") or ""), (wn.get("en") or "")
            if go == CONT and gn == CONT:
                tally["AGREE"] += 1
                continue
            ho, hn = go not in ("", CONT), gn not in ("", CONT)
            if ho and hn:
                verdict = "AGREE" if norm_gloss(go) == norm_gloss(gn) else "DIFFER"
            elif ho:
                verdict = "LOST"
            elif hn:
                verdict = "ADDED"
            else:
                verdict = "AGREE"
            tally[verdict] += 1
            if verdict != "AGREE":
                by_token[verdict][wo["sm"]] += 1
                if len(examples[verdict]) < 4000:
                    examples[verdict].append((key, wo["sm"], go, gn))

    total = sum(v for k, v in tally.items() if not k.startswith("SKIP"))
    print("curated tokens compared %d" % total)
    for k in ("AGREE", "DIFFER", "LOST", "ADDED"):
        print("  %-7s %8d  %5.1f%%" % (k, tally[k], 100 * tally[k] / max(1, total)))
    for k, v in tally.items():
        if k.startswith("SKIP"):
            print("  %s: %d verses" % (k, v))

    for verdict in ("DIFFER", "LOST", "ADDED"):
        print("\ntop tokens %s:" % verdict)
        for tok, c in by_token[verdict].most_common(12):
            print("   %6d  %s" % (c, tok))

    # ── CONTENT, not placement ───────────────────────────────────────────
    # Token agreement punishes a pass for MOVING a gloss. `le siufofoga o` was
    # curated as one unit reading "the voice of", with the gloss on the `o`;
    # the pass reads `le siufofoga` "the voice" + `o` "of" and scores LOST on
    # the `o` and ADDED on `siufofoga` for saying the same thing in the right
    # place. So also compare, per verse, the BAG of gloss words either side.
    kept = missing = spurious = 0
    per_verse = []
    for key in sorted(curated):
        o, n = old["verses"][key], new["verses"].get(key)
        if not n:
            continue
        def bag(ws):
            c = Counter()
            for w in ws:
                g = w.get("en") or ""
                if g and g != CONT:
                    c.update(re.findall(r"[a-z']+", g.lower()))
            return c
        bo, bn = bag(o), bag(n)
        inter = sum((bo & bn).values())
        kept += inter
        missing += sum(bo.values()) - inter
        spurious += sum(bn.values()) - inter
        d = sum(bo.values())
        if d:
            per_verse.append((inter / d, key))
    recall = kept / max(1, kept + missing)
    prec = kept / max(1, kept + spurious)
    print("\nGLOSS CONTENT, placement ignored")
    print("  recall    %5.1f%%  (of the curation's gloss words, how many the pass also says)" % (100 * recall))
    print("  precision %5.1f%%  (of the pass's gloss words, how many the curation also says)" % (100 * prec))
    print("  F1        %5.1f%%" % (100 * 2 * recall * prec / max(1e-9, recall + prec)))
    per_verse.sort()
    print("  worst verses:", ", ".join("%s %.0f%%" % (k, 100 * r) for r, k in per_verse[:6]))

    if a.differ:
        print("\nDIFFER examples for %r:" % a.differ)
        for key, sm, go, gn in examples["DIFFER"]:
            if sm.strip(",.;:") == a.differ:
                print("   %-16s curated=%-28r pass=%r" % (key, go, gn))
                a.n -= 1
                if a.n <= 0:
                    break
    if a.lost:
        print("\nLOST examples:")
        for key, sm, go, gn in examples["LOST"][:a.n]:
            print("   %-16s %-14s curated=%r" % (key, sm, go))
    if a.added:
        print("\nADDED examples:")
        for key, sm, go, gn in examples["ADDED"][:a.n]:
            print("   %-16s %-14s pass=%r" % (key, sm, gn))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
