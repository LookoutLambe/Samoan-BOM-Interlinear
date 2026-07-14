"""
Scrape the Samoan Book of Mormon from churchofjesuschrist.org (lang=smo)
and emit `bom_books.json` matching the Swift `BookOfMormon` model:

    {
      "books": [
        {
          "id": "1nephi", "nameSm": "1 Nifae", "nameEn": "1 Nephi",
          "chapters": [
            { "num": 1, "verses": [ { "num": 1, "words": [ {"sm":"...", "en":""}, ... ] } ] }
          ]
        }
      ]
    }

Glosses are intentionally left empty (`"en": ""`). They will be filled in
later by hand-curated TAM-phrase passes (see the project memory note on
Samoan glossing).

Run:  python3 scrape_samoan_bom.py
"""

from __future__ import annotations

import html as html_module
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

# (id, url-slug, nameSm, nameEn, chapter_count)
BOOKS = [
    ("1nephi",  "1-ne",   "1 Nifae",       "1 Nephi",          22),
    ("2nephi",  "2-ne",   "2 Nifae",       "2 Nephi",          33),
    ("jacob",   "jacob",  "Iakopo",        "Jacob",             7),
    ("enos",    "enos",   "Enosa",         "Enos",              1),
    ("jarom",   "jarom",  "Iaroma",        "Jarom",             1),
    ("omni",    "omni",   "Ominae",        "Omni",              1),
    ("wom",     "w-of-m", "Upu a Mamona",  "Words of Mormon",   1),
    ("mosiah",  "mosiah", "Mosaea",        "Mosiah",           29),
    ("alma",    "alma",   "Alema",         "Alma",             63),
    ("helaman", "hel",    "Helamana",      "Helaman",          16),
    ("3nephi",  "3-ne",   "3 Nifae",       "3 Nephi",          30),
    ("4nephi",  "4-ne",   "4 Nifae",       "4 Nephi",           1),
    ("mormon",  "morm",   "Mamona",        "Mormon",            9),
    ("ether",   "ether",  "Eteru",         "Ether",            15),
    ("moroni",  "moro",   "Moronae",       "Moroni",           10),
]

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT_PATH = Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"


def fetch(url: str, retries: int = 3) -> str:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "smo"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


# A verse is `<p id="pN" ...>...</p>` containing a `<span class="verse-number">N </span>`.
# We extract the inner text, strip footnote-marker <sup>s and other tags, decode entities.
VERSE_BLOCK_RE = re.compile(
    r'<p[^>]*id="p(\d+)"[^>]*>(.*?)</p>',
    re.DOTALL,
)
VERSE_NUM_RE = re.compile(r'<span class="verse-number">[^<]*</span>')
SUP_RE = re.compile(r'<sup\b[^>]*>.*?</sup>', re.DOTALL)
TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')


def parse_verses(html: str) -> list[tuple[int, str]]:
    verses: list[tuple[int, str]] = []
    for m in VERSE_BLOCK_RE.finditer(html):
        num = int(m.group(1))
        body = m.group(2)
        body = VERSE_NUM_RE.sub("", body)
        body = SUP_RE.sub("", body)
        body = TAG_RE.sub("", body)
        body = html_module.unescape(body)
        body = WS_RE.sub(" ", body).strip()
        if body:
            verses.append((num, body))
    return verses


# Tokenize Samoan into surface-form words, keeping trailing punctuation
# attached so the original prose round-trips when joined with spaces.
# This is intentionally simple: glosses (TAM-phrase) are curated later.
TOKEN_RE = re.compile(r"\S+")


def tokenize_samoan(text: str) -> list[dict[str, str]]:
    return [{"sm": tok, "en": ""} for tok in TOKEN_RE.findall(text)]


def scrape_chapter(slug: str, chapter: int) -> list[dict]:
    url = f"https://www.churchofjesuschrist.org/study/scriptures/bofm/{slug}/{chapter}?lang=smo"
    html = fetch(url)
    parsed = parse_verses(html)
    if not parsed:
        print(f"  ! no verses parsed for {slug}/{chapter}", file=sys.stderr)
    return [
        {"num": num, "words": tokenize_samoan(text)}
        for num, text in parsed
    ]


def main() -> None:
    books_out = []
    for book_id, slug, name_sm, name_en, ch_count in BOOKS:
        print(f"[{book_id}] {name_en} — {ch_count} chapter(s)")
        chapters = []
        for ch in range(1, ch_count + 1):
            verses = scrape_chapter(slug, ch)
            chapters.append({"num": ch, "verses": verses})
            print(f"  {name_en} {ch}: {len(verses)} verses")
            time.sleep(0.15)
        books_out.append(
            {
                "id": book_id,
                "nameSm": name_sm,
                "nameEn": name_en,
                "chapters": chapters,
            }
        )
    payload = {"books": books_out}
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    total_verses = sum(len(c["verses"]) for b in books_out for c in b["chapters"])
    print(f"\nwrote {OUT_PATH} — {len(books_out)} books, {total_verses} verses")


if __name__ == "__main__":
    main()
