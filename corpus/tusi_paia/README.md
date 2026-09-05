# O le Tusi Paia — the Samoan Bible as evidence and as the next Dual volumes

Pulled 2026-09-04. The goal is the Old and New Testament in this app's Dual
structure — Samoan verse beside the English — the way the Spanish iOS app
already carries them (`book_<id>.json` per book with `volume: "ot" | "nt"`,
one English map keyed `Book|chapter|verse`). The English column is here
already: `english_ot_nt.json` is the 31,161-verse OT+NT English column lifted
from the Hebrew app (`ot_english.js`, `nt_english.js`; 66 books, Song of
Songs under that name). Nothing in this folder ships in the app yet.

## Sources (both are archive.org OCR of scanned pages — no clean text file
of the Samoan Bible exists anywhere online: eBible.org has no Samoan edition,
bible.com is JavaScript-gated, the Church sells the Bible only in its store)

| file | archive.org item | what it is |
|---|---|---|
| `tusi_paia_1887_SMOOLD_DBS_HS.epub`, `tusi_paia_1887_pages.txt`, `tusi_paia_1887_djvu.txt` | `SMOOLD_DBS_HS` (Digital Bible Society upload, 2022) | the 1887 British and Foreign Bible Society edition — the LMS text, `Ieova`. Public domain. Its verse numbers sit in the page margins and the OCR text lost them (they surface as number columns at page tops). The word-coordinate XML (`…_djvu.xml`, 84 MB, not committed) could recover them: margin numerals are at the y of each verse's first line. |
| `tusi_paia_numbered_samoan-bible.epub`, `tusi_paia_numbered_pages.txt` | `samoan-bible` (uploaded 2021, no date) | a later revision: `le ALII` for the LORD, chapter summaries, Psalm headings `O LE SALAMO 24 (23)`. Inline verse numbers on 1,537 of 1,710 pages, running heads for all 66 books. Edition and copyright status unknown — use as structure and evidence, do not ship its text without the user's decision. |

`*_pages.txt` are the EPUB page files concatenated in order, each page
prefixed `@@PAGE page_N.html`. OCR noise: Cyrillic look-alikes for Latin
letters (о а е і п т …), `$` for 5, `€` for E; `scripts/segment_tusi_paia.py`
maps them.

## State of the segmenter (`scripts/segment_tusi_paia.py`)

First pass. It walks the numbered edition with the English verse counts as
the constraint: running heads give the book, inline numbers anchor verses,
uppercase title runs (`O LE TUSI E LUA A MOSE`, `O LE SALAMO N`) open books
and Psalms, and a chapter break without a title is recognised when `2` (or
`1`) follows the chapter's expected last verse. Output `segment_runs.json`
(not committed; regenerate). Recovered whole: Joshua, Judges, Ruth, Esther,
Amos, Obadiah, Jonah, Micah, Habakkuk, Haggai, Malachi, John, Romans,
Colossians, 1 Thessalonians, Titus, Hebrews, James, Jude; 148/150 Psalms by
heading. Short elsewhere for three known reasons, all fixable:

1. a chapter break is only seen when the verse counter reaches the chapter's
   end, so one OCR-dropped number breaks the chain for the rest of the book
   (Numbers 7/36, 2 Samuel 0/24, Revelation 0/22) — resynchronise on the
   running-head chapter number and on the next `2`;
2. the book-title matcher misreads the epistles (`O LE ULUAI TUSI A PAULO IA
   TIMOTEO`, and 1–3 John collide with the Gospel) — match `ULUAI`/`MUAMUA`/
   `E LUA`/`E TOLU` + the name, not the whole run;
3. unnumbered poetry (Psalms, parts of Job/Proverbs) needs the proportional
   fill at punctuation against the English verse lengths, flagged `est`.

Chapter starts carry a summary line and an unnumbered verse 1; the split
between them is by expected verse-1 length (flag it). Genesis 2 shows the
shape: `…o le aso ono lea. O le uluai aso sa; o le faatoaga i Etena; o le
tala i le uluai fafine Ua uma lava ona faia o le lagi…`.

## The other use: evidence for the D&C / PGP blanks

`scripts/diag_blanks_dc_pgp.py` replays the generator's decision loop over
dc/pgp and says why every blank unit stayed blank (the closed-class blanks
are multi-token inventory units the verse veto kills with no per-token
fallback: `ia te oulua`, `e uiga`, `po o`, `o lē ua`). `scripts/
name_matcher_proto.py` is the consonant-skeleton name matcher (Samita→Smith,
Kaotui→Cowdery, Rikitone→Rigdon …), 88% raw on the curated BOM names with the
errors being common nouns, not names. Names like Enoka, Lameko, Metusela,
Peteru, Paulo, Mekaeli have direct witnesses in the Bible text above.
