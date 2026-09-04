#!/usr/bin/env python3
"""Learn EVERY closed-class form's positional readings at once.

The hand-written frames in samoan_grammar.contextual_reading were each found
the same way: take a particle, split its curated witnesses by the CLASS of the
token in front of it, and see which English goes with which class. `lava` is
the reflexive after a pronoun and "own" after a possessive and "even" after a
degree word; `tele` is "many" after a particle and "exceedingly" after a verb;
`le` is the article after a preposition and the negative after a tense marker.

That is one procedure, and doing it by hand one form at a time is the wrong
way to use a 111,683-unit record. This runs it over every closed-class form
the grammar knows and writes what it finds.

WHAT IT WILL NOT DO. It reports a (form, class) pair only when the curation is
both plentiful and agreed -- MIN_WITNESS units and MIN_SHARE of them on one
reading. Anything short of that is left to the existing machinery, because a
positional rule guessed from four examples is worse than no rule.

The hand-written frames WIN over anything found here: they were checked
against the text one by one and this has not been.

    python3 build_positional.py [--min-witness 20] [--min-share 0.60]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import generate_overrides_dc_pgp as G
import samoan_grammar as SG

OUT = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" \
      / "Resources" / "positional_readings.json"


def token_class(tok: str) -> str:
    """What KIND of word precedes the particle. The classes are the ones the
    hand-written frames turned out to need."""
    if not tok:
        return "START"
    if tok in SG.TAM:
        return "TAM"
    if tok in SG.POSSESSIVES:
        return "POSSESSIVE"
    if tok in SG.PRONOUNS:
        return "PRONOUN"
    if tok in SG.ARTICLE_HEADS:
        return "ARTICLE"
    if tok in SG.PREPOSITIONS or tok in SG.COMPLEX_PREPOSITIONS:
        return "PREP"
    if tok in SG.DEGREE or tok in SG.COMPARATIVE:
        return "DEGREE"
    if tok in SG.CLOSED_CLASS or tok in SG.AMBIGUOUS:
        return "PARTICLE"
    return "OPEN"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-witness", type=int, default=20)
    ap.add_argument("--min-share", type=float, default=0.60)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    units = G.load_evidence()
    # every closed-class form that could take more than one reading
    forms = set(SG.CLOSED_CLASS) | set(SG.AMBIGUOUS) | set(SG.READINGS)
    forms = {f for f in forms if len(f.split()) == 1}

    seen: dict = defaultdict(lambda: defaultdict(Counter))
    for sm, en in units:
        toks = G.norm(sm).split()
        words = re.findall(r"[a-z']+", (en or "").lower())
        if not toks or not words:
            continue
        # the form must END the unit, so the unit's last English word is the
        # one that belongs to it -- the same alignment the hand frames used
        f = toks[-1]
        if f not in forms or len(toks) < 2:
            continue
        seen[f][token_class(toks[-2])][words[-1]] += 1

    table: dict = {}
    rows = []
    for f, byclass in seen.items():
        for cls, dist in byclass.items():
            total = sum(dist.values())
            if total < a.min_witness:
                continue
            word, n = dist.most_common(1)[0]
            share = n / total
            if share < a.min_share:
                continue
            hand = SG.contextual_reading(f, "", "")
            table.setdefault(f, {})[cls] = word
            rows.append((total, share, f, cls, word, dist.most_common(3)))

    rows.sort(reverse=True)
    print("(form, preceding class) pairs the curation actually settles: %d"
          % len(rows))
    print("%-10s %-11s %-14s %6s %6s   runners-up" %
          ("form", "after", "reads", "n", "share"))
    for total, share, f, cls, word, top in rows[:40]:
        print("%-10s %-11s %-14s %6d %5.0f%%   %s" %
              (f, cls, word, total, 100 * share, top[1:]))

    if a.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    OUT.write_text(json.dumps({
        "note": ("Learned by build_positional.py from the curated units: the "
                 "dominant English for a closed-class form, split by the CLASS "
                 "of the token before it. The hand-written frames in "
                 "samoan_grammar.contextual_reading override anything here."),
        "min_witness": a.min_witness, "min_share": a.min_share,
        "readings": table,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s — %d forms" % (OUT.name, len(table)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
