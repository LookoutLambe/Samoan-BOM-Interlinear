#!/usr/bin/env python3
"""Fan the app's bundled JSON out into per-chapter files for the web reader.

The iOS app loads 21 MB of `bom_books.json` plus a 20 MB override layer into
memory at launch; a browser can't. This splits the same content into one file
per chapter (~40-200 KB each) under `docs/data/`, merges the gloss overrides in
at build time, and writes an asset manifest the service worker precaches so the
installed PWA works offline.

Output is deterministic — rerunning with unchanged inputs rewrites identical
bytes, so it stays quiet in `git status`.

Usage:  python3 scripts/build_web_data.py
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "O le Tusi a Mamona Interlinear"
RES = APP / "Resources"
OUT = ROOT / "docs" / "data"
BOOKLIST = APP / "Views" / "BookListView.swift"


def load(name: str) -> dict:
    with (RES / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def write(path: Path, payload) -> int:
    """Write compact JSON and return the byte count."""
    path.parent.mkdir(parents=True, exist_ok=True)
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    path.write_text(blob, encoding="utf-8")
    return len(blob.encode("utf-8"))


def swift_unescape(text: str) -> str:
    r"""Resolve `\u{...}` escapes and the `\`-newline continuations Swift uses
    in multi-line string literals."""
    text = re.sub(r"\\\n\s*", "", text)
    text = re.sub(r"\\u\{([0-9A-Fa-f]+)\}", lambda m: chr(int(m.group(1), 16)), text)
    return text.strip()


def extract_disclaimer() -> dict:
    """Pull the license notice straight out of BookListView.swift.

    The English wording is prescribed verbatim by the Standard Scripture License
    Agreement, and the landing page has to carry it exactly as the app does.
    Reading it from the Swift source instead of retyping it means the two can't
    drift apart — and a rename or edit here fails loudly rather than silently
    publishing stale license text.
    """
    src = BOOKLIST.read_text(encoding="utf-8")

    def block(name: str) -> str:
        match = re.search(rf'private let {name} = """(.*?)"""', src, re.S)
        if not match:
            raise SystemExit(f"build_web_data: no `{name}` block in {BOOKLIST.name}")
        return swift_unescape(match.group(1))

    gloss_match = re.search(
        r"private let gloss: \[\(String, String\)\] = \[(.*?)\n    \]", src, re.S
    )
    if not gloss_match:
        raise SystemExit(f"build_web_data: no `gloss` table in {BOOKLIST.name}")

    pairs = [
        [swift_unescape(sm), swift_unescape(en)]
        for sm, en in re.findall(r'\("((?:[^"\\]|\\.)*)",\s*"((?:[^"\\]|\\.)*)"\)', gloss_match.group(1))
    ]
    if not pairs:
        raise SystemExit("build_web_data: gloss table parsed empty")

    return {"english": block("english"), "samoan": block("samoan"), "gloss": pairs}


def main() -> None:
    books = load("bom_books.json")["books"]
    overrides = load("bom_overrides.json")["verses"]
    headings = load("bom_headings.json")["headings"]
    colophons = load("bom_colophons.json")["colophons"]
    frontmatter = load("bom_frontmatter.json")["sections"]
    diacritics = load("bom_diacritics.json")

    # Rebuild from scratch so chapters dropped upstream don't linger as stale
    # files that the service worker would keep serving.
    if OUT.exists():
        shutil.rmtree(OUT)

    assets: list[str] = []
    index_books = []
    total = 0

    for book in books:
        bid = book["id"]
        for chapter in book["chapters"]:
            num = chapter["num"]
            ckey = f"{bid}|{num}"
            verses = []
            for verse in chapter["verses"]:
                vkey = f"{bid}|{num}|{verse['num']}"
                # The override layer carries the curated glosses; bom_books.json
                # only has the Samoan surface forms with empty `en` fields.
                words = overrides.get(vkey) or verse["words"]
                verses.append({"n": verse["num"], "w": words})

            payload = {"book": bid, "num": num, "verses": verses}
            if ckey in headings:
                payload["heading"] = headings[ckey]
            if ckey in colophons:
                payload["colophon"] = colophons[ckey]

            rel = f"data/ch/{bid}-{num}.json"
            total += write(OUT / "ch" / f"{bid}-{num}.json", payload)
            assets.append(rel)

        index_books.append(
            {
                "id": bid,
                "nameSm": book["nameSm"],
                "nameEn": book["nameEn"],
                "chapters": [c["num"] for c in book["chapters"]],
            }
        )

    for section in frontmatter:
        rel = f"data/front/{section['id']}.json"
        total += write(OUT / "front" / f"{section['id']}.json", section)
        assets.append(rel)

    total += write(
        OUT / "diacritics.json",
        {"types": diacritics["types"], "exceptions": diacritics["exceptions"]},
    )
    assets.append("data/diacritics.json")

    disclaimer = extract_disclaimer()
    total += write(
        OUT / "index.json",
        {
            "books": index_books,
            "frontmatter": [
                {"id": s["id"], "titleEn": s["titleEn"], "titleSm": s["titleSm"]}
                for s in frontmatter
            ],
            "disclaimer": disclaimer,
        },
    )
    assets.append("data/index.json")

    # Shell files are precached alongside the data. Kept here rather than in the
    # service worker so one build step owns the whole offline payload.
    shell = [
        "./",
        "index.html",
        "styles.css",
        "app.js",
        "manifest.webmanifest",
        "icons/icon-192.png",
        "icons/icon-512.png",
        "icons/maskable-512.png",
    ]
    write(ROOT / "docs" / "assets.json", {"shell": shell, "data": assets})

    chapters = sum(len(b["chapters"]) for b in index_books)
    print(f"books      {len(index_books)}")
    print(f"chapters   {chapters}")
    print(f"front      {len(frontmatter)}")
    print(f"data size  {total / 1_048_576:.1f} MB across {len(assets)} files")
    print(f"disclaimer {len(disclaimer['gloss'])} gloss pairs, verbatim from {BOOKLIST.name}")


if __name__ == "__main__":
    main()
