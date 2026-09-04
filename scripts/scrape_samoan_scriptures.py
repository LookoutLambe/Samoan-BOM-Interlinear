"""
THE ONE SCRAPER for the Samoan scriptures on churchofjesuschrist.org.

Supersedes scrape_samoan_bom.py and the short-lived scrape_samoan_dc_pgp.py.
There is one volume table, one parser and one output file, because the reader,
the gloss overrides, the web build and the iOS app all read a single corpus and
a second scraper writing a second file would put them out of step the first
time either changed.

    python3 scrape_samoan_scriptures.py --volume dc pgp     # add volumes
    python3 scrape_samoan_scriptures.py --list              # what is known
    python3 scrape_samoan_scriptures.py --volume bom --force  # re-fetch the BoM

OUTPUT is Resources/bom_books.json -- the same file, holding all three volumes,
with every book carrying a `volume` field. The name is historical: 240 build
scripts and the Swift model read it, so renaming it would be a 240-file change
for a filename, and the file always was "the books".

THE BOOK OF MORMON IS PROTECTED. Its 6,604 verses are the base for 239
hand-curated override scripts, every one of which asserts its token count
against this file. A re-fetch that differed by a single token -- the site is
edited -- would break those specs and silently invalidate the curation. So a
book that is already present is never overwritten without --force, and --force
prints what it is about to replace.

A VERSE IS A PARAGRAPH THE SITE ITSELF NUMBERS. The old BoM scraper took every
`<p id="pN">`, which is right nearly everywhere and wrong on Joseph
Smith-History: that page has 82 such paragraphs and 75 verses, the last seven
being the unnumbered Oliver Cowdery letter. Requiring a
`<span class="verse-number">` inside the paragraph uses the site's own
statement about what is a verse, and gives 75.

Not collected, because they carry no numbered verses and need a different
container: the two Official Declarations (dc-testament/od/1, od/2), and the
three Facsimiles in Abraham, which are images with captions.

Glosses are left empty. They are filled in afterwards by hand-curated
TAM-phrase passes, exactly as the Book of Mormon was; see GLOSSING_RULES.md.
"""

from __future__ import annotations

import argparse
import html as html_module
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# volume -> (label_sm, label_en, [(book_id, url_path, nameSm, nameEn, chapters)])
VOLUMES: dict[str, tuple[str, str, list[tuple[str, str, str, str, int]]]] = {
    "bom": ("O le Tusi a Mamona", "Book of Mormon", [
        ("1nephi",  "bofm/1-ne",   "1 Nifae",      "1 Nephi",         22),
        ("2nephi",  "bofm/2-ne",   "2 Nifae",      "2 Nephi",         33),
        ("jacob",   "bofm/jacob",  "Iakopo",       "Jacob",            7),
        ("enos",    "bofm/enos",   "Enosa",        "Enos",             1),
        ("jarom",   "bofm/jarom",  "Iaroma",       "Jarom",            1),
        ("omni",    "bofm/omni",   "Ominae",       "Omni",             1),
        ("wom",     "bofm/w-of-m", "Upu a Mamona", "Words of Mormon",  1),
        ("mosiah",  "bofm/mosiah", "Mosaea",       "Mosiah",          29),
        ("alma",    "bofm/alma",   "Alema",        "Alma",            63),
        ("helaman", "bofm/hel",    "Helamana",     "Helaman",         16),
        ("3nephi",  "bofm/3-ne",   "3 Nifae",      "3 Nephi",         30),
        ("4nephi",  "bofm/4-ne",   "4 Nifae",      "4 Nephi",          1),
        ("mormon",  "bofm/morm",   "Mamona",       "Mormon",           9),
        ("ether",   "bofm/ether",  "Eteru",        "Ether",           15),
        ("moroni",  "bofm/moro",   "Moronae",      "Moroni",          10),
    ]),
    "dc": ("Mataupu Faavae ma Feagaiga", "Doctrine and Covenants", [
        ("dc", "dc-testament/dc", "Mataupu Faavae ma Feagaiga",
         "Doctrine and Covenants", 138),
    ]),
    "pgp": ("Le Penina Silisili Ona Taua", "Pearl of Great Price", [
        ("moses",  "pgp/moses",  "Mose",     "Moses",    8),
        ("abr",    "pgp/abr",    "Aperaamo", "Abraham",  5),
        ("js-m",   "pgp/js-m",   "Iosefa Samita—Mataio",          "Joseph Smith—Matthew", 1),
        ("js-h",   "pgp/js-h",   "Iosefa Samita—Talafaasolopito", "Joseph Smith—History", 1),
        ("a-of-f", "pgp/a-of-f", "Mataupu Faavae",                "Articles of Faith",    1),
    ]),
}

VERSE_BLOCK_RE = re.compile(r'<p[^>]*id="p(\d+)"[^>]*>(.*?)</p>', re.DOTALL)
VERSE_NUM_RE = re.compile(r'<span class="verse-number">[^<]*</span>')
SUP_RE = re.compile(r'<sup\b[^>]*>.*?</sup>', re.DOTALL)
TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')
TOKEN_RE = re.compile(r"\S+")

# An em dash, semicolon or colon between two letters is a WORD BOUNDARY that
# carries no space. Splitting on whitespace alone glues the words either side
# into one token -- `Atua—ma`, `nuu;Ma`, `atu—Ia` -- and a glued token can
# never be glossed, because it is two words wearing one label. 213 of them in
# the Doctrine and Covenants and the Pearl of Great Price.
#
# The punctuation stays on the LEFT token, which is how the corpus writes it
# everywhere the space is present, so the prose still round-trips when the
# tokens are joined back with spaces.
GLUE_RE = re.compile(r"([A-Za-z\u0101\u0113\u012b\u014d\u016b\u2019])([\u2014;:])"
                     r"(?=[A-Za-z\u0101\u0113\u012b\u014d\u016b\u2019])")


def tokenise(text: str) -> list[str]:
    return TOKEN_RE.findall(GLUE_RE.sub(r"\1\2 ", text))


def fetch(url: str, retries: int = 3) -> str:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": USER_AGENT, "Accept-Language": "smo"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last}")


def parse_verses(html: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for m in VERSE_BLOCK_RE.finditer(html):
        body = m.group(2)
        if '<span class="verse-number">' not in body:
            continue                       # see the note at the top
        body = VERSE_NUM_RE.sub("", body)
        body = SUP_RE.sub("", body)
        body = TAG_RE.sub("", body)
        body = WS_RE.sub(" ", html_module.unescape(body)).strip()
        if body:
            out.append((int(m.group(1)), body))
    return out


def scrape_chapter(path: str, chapter: int) -> list[dict]:
    url = f"https://www.churchofjesuschrist.org/study/scriptures/{path}/{chapter}?lang=smo"
    verses = parse_verses(fetch(url))
    if not verses:
        print(f"  ! no verses parsed for {path}/{chapter}", file=sys.stderr)
    return [{"num": n, "words": [{"sm": t, "en": ""} for t in tokenise(txt)]}
            for n, txt in verses]


def load_existing() -> dict:
    if OUT_PATH.exists():
        return json.loads(OUT_PATH.read_text(encoding="utf-8"))
    return {"books": []}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", nargs="*", default=[], choices=sorted(VOLUMES))
    ap.add_argument("--force", action="store_true",
                    help="replace a book that is already present")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)

    data = load_existing()
    have = {b["id"]: b for b in data["books"]}

    if a.list or not a.volume:
        for vol, (sm, en, books) in VOLUMES.items():
            print(f"{vol:5} {en} — {sm}")
            for bid, _p, nsm, nen, ch in books:
                mark = "present" if bid in have else "MISSING"
                print(f"      {bid:8} {nen:24} {ch:3} ch   {mark}")
        if not a.volume:
            print("\nnothing fetched; pass --volume dc pgp")
        return 0

    for vol in a.volume:
        sm_label, en_label, books = VOLUMES[vol]
        for bid, path, nsm, nen, count in books:
            if bid in have and not a.force:
                print(f"[{bid}] already present ({sum(len(c['verses']) for c in have[bid]['chapters'])}"
                      f" verses) — skipping; --force to replace")
                have[bid].setdefault("volume", vol)
                continue
            if bid in have:
                print(f"[{bid}] REPLACING "
                      f"{sum(len(c['verses']) for c in have[bid]['chapters'])} existing verses")
            print(f"[{bid}] {nen} — {count} chapter(s)")
            chapters = []
            for ch in range(1, count + 1):
                verses = scrape_chapter(path, ch)
                chapters.append({"num": ch, "verses": verses})
                print(f"  {nen} {ch}: {len(verses)} verses")
                time.sleep(0.15)
            have[bid] = {"id": bid, "volume": vol, "nameSm": nsm, "nameEn": nen,
                         "chapters": chapters}

    # backfill the volume tag on everything, and keep VOLUMES' order
    order = [b[0] for v in VOLUMES.values() for b in v[2]]
    for vol, (_sm, _en, books) in VOLUMES.items():
        for bid, *_ in books:
            if bid in have:
                have[bid].setdefault("volume", vol)
                have[bid]["volume"] = have[bid].get("volume") or vol
    out = [have[b] for b in order if b in have] + \
          [b for k, b in have.items() if k not in order]
    OUT_PATH.write_text(json.dumps({"books": out}, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    nv = sum(len(c["verses"]) for b in out for c in b["chapters"])
    nw = sum(len(v["words"]) for b in out for c in b["chapters"] for v in c["verses"])
    print(f"\nwrote {OUT_PATH.name} — {len(out)} books, {nv} verses, {nw} words")
    for vol in VOLUMES:
        bs = [b for b in out if b.get("volume") == vol]
        if bs:
            print(f"   {vol:5} {len(bs):2} books  "
                  f"{sum(len(c['verses']) for b in bs for c in b['chapters']):6} verses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
