"""
Give the Doctrine and Covenants and the Pearl of Great Price their official
English, so Dual mode works for them as it does for the Book of Mormon.

The English was NOT scraped. It already existed, in the sibling Hebrew
interlinear project (LookoutLambe/StandardWorks) as dc_english.js and
pgp_english.js, both keyed by book/chapter/verse. Re-fetching text that is
already on this machine, verified and in use, would have been the worse of two
options: a second copy that can drift.

ALIGNMENT IS ASSERTED, NOT ASSUMED. The two sources are independent -- the
Samoan came from churchofjesuschrist.org at lang=smo, the English from a
project built months earlier -- so agreement between them is evidence, and
disagreement is a bug in one of them. Every chapter's verse count must match
on both sides or this refuses to write. They do: D&C 3,654 verses and PGP 635
on both sides, chapter for chapter.

Not imported, because the Samoan side has no numbered verses for them:
the two Official Declarations (43 English verses), the three Abraham
facsimiles (42), and the Pearl of Great Price introduction (20).

    python3 import_english_dc_pgp.py [--source PATH] [--dry-run]
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "O le Tusi a Mamona Interlinear" / "Resources"
DEFAULT_SOURCE = Path.home() / "Desktop" / "untitled folder" / "Escrituras"

# the English project's book name -> this corpus's nameEn
BOOK_MAP = {
    "D&C": "Doctrine and Covenants",
    "Moses": "Moses",
    "Abraham": "Abraham",
    "JS-Matthew": "Joseph Smith—Matthew",
    "JS-History": "Joseph Smith—History",
    "Articles of Faith": "Articles of Faith",
}


def load_js_array(path: Path) -> list[dict]:
    """These are `window._xEnglishData = [ ... ];` — take the array."""
    s = io.open(path, encoding="utf-8").read()
    return json.loads(s[s.index("["):].rstrip().rstrip(";"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                    help="the Hebrew Standard Works checkout")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    for name in ("dc_english.js", "pgp_english.js"):
        if not (a.source / name).exists():
            print(f"missing {a.source / name}", file=sys.stderr)
            return 1

    rows = load_js_array(a.source / "dc_english.js") + \
           load_js_array(a.source / "pgp_english.js")

    english = defaultdict(dict)
    for r in rows:
        book = BOOK_MAP.get(r["book"])
        if not book:
            continue                       # OD, facsimiles, introduction
        english[book][(int(r["chapter"]), int(r["verse"]))] = r["english"]

    books = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))["books"]
    wanted = {b["nameEn"]: b for b in books if b.get("volume") in ("dc", "pgp")}

    problems: list[str] = []
    for name, book in wanted.items():
        have = english.get(name)
        if not have:
            problems.append(f"{name}: no English at all")
            continue
        for ch in book["chapters"]:
            sm_nums = {v["num"] for v in ch["verses"]}
            en_nums = {v for (c, v) in have if c == ch["num"]}
            if sm_nums != en_nums:
                miss = sorted(sm_nums - en_nums)[:6]
                extra = sorted(en_nums - sm_nums)[:6]
                problems.append(
                    f"{name} {ch['num']}: Samoan {len(sm_nums)} vs English "
                    f"{len(en_nums)}; missing {miss} extra {extra}")
    if problems:
        print("ALIGNMENT FAILED — nothing written:", file=sys.stderr)
        for p in problems[:20]:
            print("   " + p, file=sys.stderr)
        return 1

    out = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
    before = len(out)
    added = 0
    for name, have in english.items():
        if name not in wanted:
            continue
        for (ch, v), text in have.items():
            key = f"{name}|{ch}|{v}"
            if key not in out:
                added += 1
            out[key] = text

    print(f"alignment OK — every chapter matches verse for verse")
    print(f"bom_english.json {before} -> {before + added} entries (+{added})")
    if a.dry_run:
        print("(dry run, nothing written)")
        return 0
    (RES / "bom_english.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {RES / 'bom_english.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
