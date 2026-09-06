#!/usr/bin/env python3
"""The typed 1887 text, chapter by chapter, as a REFERENCE for the scan.

bible.com's "SOV" (2203) is the 1887 O le Tusi Paia typed out; the Bible Society of
the South Pacific claims 2017 copyright on its edition and layout, the words are the
1887 words (user, 2026-09-05: "SOV is 1887 though ... its copyright because how they
lay it out but its PD"). The user pastes the chapters where the scan has trouble --
never fetched by this tool -- into `corpus/tusi_paia/sov/<USFM>.<chapter>.txt`, in
the pasted shape: verse numbers glued to the first word ("1Sa i le amataga, ...
2O ia lava ..."), a heading line allowed before verse 1.

Used three ways, all of them as the later edition already is: the boundary guide when
a verse is split inside a line, the aligned word when the OCR misread one, and the
stand-in where the scan lost a verse (segment_1887_pdf.py, build_tusi_paia_dual.py).
"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "corpus" / "tusi_paia"
SOV_DIR = D / "sov"

USFM = {
    'GEN': 'Genesis', 'EXO': 'Exodus', 'LEV': 'Leviticus', 'NUM': 'Numbers', 'DEU': 'Deuteronomy',
    'JOS': 'Joshua', 'JDG': 'Judges', 'RUT': 'Ruth', '1SA': '1 Samuel', '2SA': '2 Samuel',
    '1KI': '1 Kings', '2KI': '2 Kings', '1CH': '1 Chronicles', '2CH': '2 Chronicles', 'EZR': 'Ezra',
    'NEH': 'Nehemiah', 'EST': 'Esther', 'JOB': 'Job', 'PSA': 'Psalms', 'PRO': 'Proverbs',
    'ECC': 'Ecclesiastes', 'SNG': 'Song of Solomon', 'ISA': 'Isaiah', 'JER': 'Jeremiah',
    'LAM': 'Lamentations', 'EZK': 'Ezekiel', 'DAN': 'Daniel', 'HOS': 'Hosea', 'JOL': 'Joel',
    'AMO': 'Amos', 'OBA': 'Obadiah', 'JON': 'Jonah', 'MIC': 'Micah', 'NAM': 'Nahum',
    'HAB': 'Habakkuk', 'ZEP': 'Zephaniah', 'HAG': 'Haggai', 'ZEC': 'Zechariah', 'MAL': 'Malachi',
    'MAT': 'Matthew', 'MRK': 'Mark', 'LUK': 'Luke', 'JHN': 'John', 'ACT': 'Acts', 'ROM': 'Romans',
    '1CO': '1 Corinthians', '2CO': '2 Corinthians', 'GAL': 'Galatians', 'EPH': 'Ephesians',
    'PHP': 'Philippians', 'COL': 'Colossians', '1TH': '1 Thessalonians', '2TH': '2 Thessalonians',
    '1TI': '1 Timothy', '2TI': '2 Timothy', 'TIT': 'Titus', 'PHM': 'Philemon', 'HEB': 'Hebrews',
    'JAS': 'James', '1PE': '1 Peter', '2PE': '2 Peter', '1JN': '1 John', '2JN': '2 John',
    '3JN': '3 John', 'JUD': 'Jude', 'REV': 'Revelation',
}

# a verse number: digits not glued to a letter before, a letter (any case, any mark)
# after -- "1Sa", "36ua", "19O". Samoan scripture writes its numbers as words, so a
# bare digit run inside a verse is the next verse's number.
_CAPS_LINE = re.compile(r"^[A-Z\u0100-\u016B\d ,.;:'\u2018\u2019\u02bb()-]{2,40}$")
_VNUM = re.compile(r"(?<![\w’‘ʻ])(\d{1,3})(?=[A-Za-zĀ-ūāēīōū’‘ʻ(\[])")


def parse_chapter(text: str) -> dict:
    """{verse number: text} from a pasted chapter; anything before verse 1 dropped."""
    # heading lines stand alone in the paste and are never verse text: the site's
    # "SALAMO, 119" / "O LE TUSI PAIA" banner, and the all-caps acrostic names
    # inside Psalm 119 ("ALEFA.", "PETA.") that would otherwise glue onto the verse
    # before them
    text = "\n".join(ln for ln in text.replace("\u00a0", " ").split("\n")
                     if not _CAPS_LINE.match(ln.strip()))
    text = re.sub(r"\s+", " ", text).strip()
    parts = _VNUM.split(text)
    out, expect = {}, 1
    for i in range(1, len(parts) - 1, 2):
        n = int(parts[i])
        body = parts[i + 1].strip()
        # numbers must climb by one; anything else is a digit inside the text
        if n == expect:
            out[n] = body
            expect += 1
        elif out:
            out[expect - 1] = (out[expect - 1] + " " + parts[i] + body).strip()
    return out


def load_sov() -> dict:
    """{'John|1|49': text, ...} for every pasted chapter file."""
    ref = {}
    if not SOV_DIR.exists():
        return ref
    for path in sorted(SOV_DIR.glob("*.txt")):
        m = re.match(r"^([1-3]?[A-Z]{2,3})\.(\d{1,3})$", path.stem)
        if not m or m.group(1) not in USFM:
            continue
        en, ch = USFM[m.group(1)], int(m.group(2))
        for v, body in parse_chapter(path.read_text(encoding="utf8")).items():
            if body:
                ref[f"{en}|{ch}|{v}"] = body
    return ref


if __name__ == "__main__":
    r = load_sov()
    print(len(r), "verses from", SOV_DIR)
    for k in list(r)[:3]:
        print(k, r[k][:90])
