#!/usr/bin/env python3
"""One-off repair of two defects in `bom_english.json`.

1. Mormon 1's verses are filed under chapter 0 (`Mormon|0|2` … `Mormon|0|19`).
   Mormon 2-9 and every other book key correctly, and `Mormon|1|*` is entirely
   absent, so the chapter is re-keyed with no risk of collision.

2. Three verses are missing outright. Their text is supplied here from the
   published English edition:
       Mormon 1:1, Helaman 8:27, Helaman 16:25
   In all three cases the neighbouring verses are present, so these are gaps in
   the extraction rather than a deliberate omission.

Both defects reach the iOS app as well — `ScriptureLibrary.englishText(for:)`
does a plain keyed lookup with no fallback — so repairing the source file fixes
the app's dual (Tutusa) mode along with the web reader.

Idempotent: rerunning on a repaired file changes nothing.

Usage:  python3 scripts/fix_english_gaps.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGLISH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_english.json"

MISSING = {
    "Mormon|1|1": (
        "And now I, Mormon, make a record of the things which I have both seen "
        "and heard, and call it the Book of Mormon."
    ),
    "Helaman|8|27": (
        "Yea, behold it is now even at your doors; yea, go ye in unto the "
        "judgment-seat, and search; and behold, your judge is murdered, and he "
        "lieth in his blood; and he hath been murdered by his brother, who "
        "seeketh to sit in the judgment-seat."
    ),
    "Helaman|16|25": (
        "And thus ended the book of Helaman, according to the record of Helaman "
        "and his sons."
    ),
}


def main() -> None:
    verses: dict[str, str] = json.loads(ENGLISH.read_text(encoding="utf-8"))
    before = len(verses)

    # 1. Re-key Mormon chapter 0 -> chapter 1.
    rekeyed = 0
    for key in [k for k in verses if k.startswith("Mormon|0|")]:
        verse = key.split("|")[2]
        target = f"Mormon|1|{verse}"
        if target in verses:
            raise SystemExit(f"refusing to overwrite existing {target}")
        verses[target] = verses.pop(key)
        rekeyed += 1

    # 2. Fill the three absent verses.
    added = 0
    for key, text in MISSING.items():
        if key not in verses:
            verses[key] = text
            added += 1

    ENGLISH.write_text(
        json.dumps(verses, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )
    print(f"re-keyed  {rekeyed} verses from Mormon|0| to Mormon|1|")
    print(f"added     {added} previously missing verses")
    print(f"total     {before} -> {len(verses)} keys")


if __name__ == "__main__":
    main()
