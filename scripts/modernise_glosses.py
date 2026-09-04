#!/usr/bin/env python3
"""Modern English across the whole gloss layer, in one pass.

The user's ruling: the glossing does not have to follow the archaic ye/thee/
thou/thine. The D&C and PGP are generated and come out modern already, from
english_register.modernise(). The Book of Mormon's 6,604 verses are curated by
hand in the KJV register, and leaving them there means the app reads "thee" in
Alma and "you" in section 1 -- one book, two Englishes.

This is the master for that operation rather than a one-off edit, because the
per-chapter build_overrides_<book><n>.py scripts still write archaic glosses
when they are re-run. Run this after any of them. It is idempotent: a second
run changes nothing.

WHAT IT DOES NOT TOUCH: bom_english.json. That is the official English of the
canon, it is quoted, and it stays exactly as published.

    python3 modernise_glosses.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import english_register as ER

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"
CONT = "·"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    path = RES / "bom_overrides.json"
    ov = json.loads(path.read_text(encoding="utf-8"))
    pairs: Counter = Counter()
    changed = 0

    for words in ov["verses"].values():
        for w in words:
            e = w.get("en") or ""
            if not e or e == CONT:
                continue
            m = ER.modernise(e)
            if m != e:
                changed += 1
                for x, y in zip(re.findall(r"[A-Za-z]+", e),
                                re.findall(r"[A-Za-z]+", m)):
                    if x != y:
                        pairs[(x, y)] += 1
                w["en"] = m

    print(f"glosses modernised  {changed}")
    print(f"distinct changes    {len(pairs)}")
    for (x, y), n in pairs.most_common(20):
        print("  %6d  %-14s -> %s" % (n, x, y))
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    path.write_text(json.dumps(ov, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
