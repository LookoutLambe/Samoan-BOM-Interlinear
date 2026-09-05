#!/usr/bin/env python3
"""Apply scrape_samoan_scriptures.TEXT_CORRECTIONS to the text already on disk.

The corrections belong to the scraper, because that is where the text is
produced and a re-scrape has to keep them. This just brings the existing
bom_books.json up to the same state without going back to the network.

Idempotent: it re-joins each verse's tokens, applies the table, re-tokenises,
and writes only where the token list actually changed.

    python3 apply_text_corrections.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import scrape_samoan_scriptures as SS

RES = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    path = RES / "bom_books.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    hits = 0

    for b in data["books"]:
        for ch in b["chapters"]:
            for v in ch["verses"]:
                ref = f"{b['id']}|{ch['num']}|{v['num']}"
                if ref not in SS.TEXT_CORRECTIONS:
                    continue
                old = [w["sm"] for w in v["words"]]
                new = SS.tokenise(" ".join(old), ref)
                if new == old:
                    continue
                hits += 1
                print(f"  {ref}: {len(old)} -> {len(new)} tokens")
                print(f"    {' '.join(old[:6])}")
                print(f"    {' '.join(new[:6])}")
                v["words"] = [{"sm": t, "en": ""} for t in new]

    print(f"verses corrected {hits}")
    if a.dry_run:
        print("(dry run, nothing written)")
        return 0
    if hits:
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {path}")
        print("NOW RE-RUN: gloss_corpus.py, then build_web_data.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
