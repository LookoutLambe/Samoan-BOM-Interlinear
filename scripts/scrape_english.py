#!/usr/bin/env python3
"""Re-fetch the ENGLISH canon from churchofjesuschrist.org.

bom_english.json arrived damaged. Its dashes were mangled -- 310 verses had an
en dash with a stray space standing in for a hyphen, so `judgment– seat` and
`righteous– ness` -- and at least one verse held the wrong text entirely
(Helaman 8:7 carried a copy of 8:27). Repairing that by rule means guessing
which broken pair is a compound and which is a line-break hyphen, and guessing
wrong invents a word in quoted scripture.

The text is published. Fetching it again is not a repair, it is the source.

Shares the VOLUMES table, the fetcher and the verse parser with
scrape_samoan_scriptures.py, so the two languages can never drift into
different books, chapter counts or ideas of what a verse is. Only the language
and the output file differ.

    python3 scrape_english.py --volume bom dc pgp
    python3 scrape_english.py --volume bom --compare     # fetch, report, write nothing

Keys are `<nameEn>|<chapter>|<verse>`, matching the existing file.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scrape_samoan_scriptures as SS      # noqa: E402

OUT_PATH = SS.ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_english.json"


def fetch_english(url: str, retries: int = 3) -> str:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": SS.USER_AGENT, "Accept-Language": "eng"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as exc:            # noqa: BLE001
            last = exc
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", nargs="+", default=["bom", "dc", "pgp"],
                    choices=sorted(SS.VOLUMES))
    ap.add_argument("--compare", action="store_true",
                    help="fetch and report differences, write nothing")
    ap.add_argument("--book", nargs="*", help="limit to these book ids")
    a = ap.parse_args(argv)

    have = json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}
    fresh: dict[str, str] = {}

    for vol in a.volume:
        _sm, _en, books = SS.VOLUMES[vol]
        for bid, path, _nsm, nen, count in books:
            if a.book and bid not in a.book:
                continue
            print(f"[{bid}] {nen} — {count} chapter(s)")
            for ch in range(1, count + 1):
                url = (f"https://www.churchofjesuschrist.org/study/scriptures/"
                       f"{path}/{ch}?lang=eng")
                verses = SS.parse_verses(fetch_english(url))
                if not verses:
                    print(f"  ! no verses parsed for {path}/{ch}", file=sys.stderr)
                for n, txt in verses:
                    fresh[f"{nen}|{ch}|{n}"] = txt
                print(f"  {nen} {ch}: {len(verses)} verses")
                time.sleep(0.15)

    scope = set(fresh)
    added = sorted(scope - set(have))
    removed = sorted(k for k in have if k.split("|")[0] in
                     {k2.split("|")[0] for k2 in scope} and k not in scope)
    changed = [k for k in sorted(scope & set(have)) if have[k].strip() != fresh[k].strip()]

    print(f"\nfetched {len(fresh)} verses")
    print(f"  new      {len(added)}")
    print(f"  missing  {len(removed)}   {removed[:6]}")
    print(f"  changed  {len(changed)}")

    # what KIND of change: punctuation only, or different words?
    wordy = []
    for k in changed:
        w_old = re.findall(r"[A-Za-z']+", have[k])
        w_new = re.findall(r"[A-Za-z']+", fresh[k])
        if w_old != w_new:
            wordy.append(k)
    print(f"    of which the WORDS differ: {len(wordy)}")
    for k in wordy[:10]:
        d = difflib.unified_diff(re.findall(r"[A-Za-z']+", have[k]),
                                 re.findall(r"[A-Za-z']+", fresh[k]), lineterm="", n=0)
        diff = " ".join(x for x in list(d)[2:][:14])
        print(f"      {k:28} {diff[:120]}")

    if a.compare:
        print("\n(--compare, nothing written)")
        return 0
    have.update(fresh)
    OUT_PATH.write_text(json.dumps(have, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {OUT_PATH.name} — {len(have)} verses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
