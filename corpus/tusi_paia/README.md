# O le Tusi Paia — the Samoan Bible as Dual volumes and as evidence

Pulled 2026-09-04, segmented 2026-09-05. The goal: the Old and New Testament in this app's Dual
structure, Samoan verse beside the English, the way the Spanish iOS app carries them
(`book_<id>.json` per book with `volume: "ot" | "nt"`, one English map keyed
`Book|chapter|verse`). Wired into the app 2026-09-05: the 68 files of `dual/` are copied into
`O le Tusi a Mamona Interlinear/Resources/`; `ScriptureLibrary` reads `tusi_paia_index.json` at
launch, decodes a `book_<id>.json` on first open (cached), and falls back to
`tusi_paia_english.json` for the Dual English; the drawer lists the two volumes after the Pearl of
Great Price, and the landing page carries one cover card per volume (Book of Mormon, D&C, Pearl of
Great Price, Old Testament, New Testament), each opening the drawer at its books — in the iOS app
and in the web reader (`docs/`, built by `build_web_data.py`, which fans the Bible into 1,189
per-chapter files outside the precache). Search still covers the Book of Mormon volumes only (the Bible needs a prebuilt folded
index, as the Spanish app has). Regenerate the data with `segment_tusi_paia.py` →
`build_tusi_paia_dual.py` → copy `dual/*.json` into Resources.

## What is here

| file | what |
|---|---|
| `dual/book_<id>.json` (66) | the built Dual data: `{id, volume, nameSm, nameEn, chapters:[{num, verses:[{num, words:[{sm, en:""}]}]}]}` — glosses empty for now |
| `dual/tusi_paia_english.json` | the English column, 31,102 verses keyed `Book|chapter|verse` |
| `dual/tusi_paia_index.json` | volumes, books (id, nameSm, nameEn, volume, chapters), the `estimated` verse keys (4,320) and the `missing` ones (2) |
| `english_ot_nt.json` | the English source + per-chapter verse counts. **KJV in KJV versification, from the Spanish app's `spa_english.json`.** It replaced the Hebrew app's OT column, which is Masoretic-numbered (Joel 4 chapters, Malachi 3, Psalm 3 = 9 verses); the Samoan Bible follows the Protestant numbering (Malachi 4, Joel 3), so the Hebrew app's column cannot be its Dual partner. |
| `tusi_paia_numbered_pages.txt` + `.epub` | archive.org `samoan-bible` (undated later revision, `le ALII`, inline verse numbers) — the edition segmented |
| `tusi_paia_1887_*` | archive.org `SMOOLD_DBS_HS`, the 1887 BFBS/LMS edition (`Ieova`, public domain); its verse numbers sit in the margins and the OCR lost them (the 84 MB djvu.xml with word coordinates, not committed, could recover them) |

Copyright: O le Tusi Paia is the London Missionary Society translation, which is in the public
domain. The numbered edition segmented here is, per the user (2026-09-05), the Church's own printing
of that same LMS text, distributed and sold by the Church; it ships, and the landing pages of both
apps carry a source notice saying so under the license notice (`SourceNotice` in BookListView.swift).

## How it was segmented — `scripts/segment_tusi_paia.py`

Two passes so a miscounted chapter can never spill into the next book:

1. **Books from titles.** Every maximal uppercase run is a title candidate (`O LE TUSI E LUA A
   MOSE`, `TUSI I FAAMASINO`, `o GALUEGA A LE AU APOSETOLO`, `0 SALAMO`); keyword tables assign
   it to the next book in canonical order. All 66 start by title.
2. **Chapters inside each book.** Inline verse numbers anchor verses — the OCR writes l/I for 1,
   O/o for 0, $ for 5; `lo` is 10 unless it is the possessive particle (lo latou …). A verse
   number must sit at a boundary (capitalised next word, or punctuation before). A chapter opens
   at a Psalm heading (`O LE SALAMO`, numbered or not), at a `2` after the chapter's last
   expected verse, or wherever the numbers restart (a 1..5 below the counter whose look-ahead
   continues n+1, n+2 — one skipped number tolerated, an out-of-sequence one fails; never after a
   comma into a lowercase word, because a bare `1` is usually the particle *i*). When a running
   head names a later chapter at a page start and the current chapter has already reached its
   expected length, the break is forced there (size-cut). Chapter heads = summary line +
   unnumbered verse 1; the summary is cut at the lowercase→Capital seam the print leaves.
   Unnumbered spans (Psalms, dropped numbers) are filled proportionally to the English verse
   lengths at punctuation and flagged `est`. Footnotes (`1 O le upu Eperu, …` at a page's end)
   are stripped; `1`/`0`/`l` for the particles *i*/*o* inside verses are cleaned.

Result: 31,100 / 31,102 verses placed (100.0%); 4,320 estimated (13.9% — chapter-1 verses and
the unnumbered Psalms); 53 anchored verses with an off-size ratio; Samoan/English char ratio
1.051. Random anchored verses check exactly against their English.

Known residue, for hand review: Job 25–27 (Job 25's `2` is damaged, so 25 and 26 are merged
and 27 short); Psalm 82:7 and Revelation 19:1 have no text (placeholder `—`); Psalm 119 is
unnumbered and proportionally filled; some chapter-1 verses still carry a piece of the summary
line. `--debug Book ch…` dumps a chapter's runs, `--text Book ch…` its long runs, `--find "…"`
locates a phrase.

## Next

A prebuilt folded search index for the Bible (the Spanish app's `spa_search.txt` pattern), a cover
or entry for the Bible on the landing page, hand review of the estimated verses; then use the
aligned Bible as evidence for the D&C/PGP blanks
(`scripts/diag_blanks_dc_pgp.py`, `scripts/name_matcher_proto.py`): names like Enoka, Lameko,
Metusela, Peteru, Paulo, Mekaeli now have direct witnesses.

## The 1887 edition is the text (2026-09-05)
The app's Samoan Bible is now the **1887 BFBS printing** (archive.org `oletusipaiaole00lond`,
the PDF on the user's Desktop, never in the repo): `scripts/segment_1887_pdf.py` reads the PDF's
text layer with word positions (PyMuPDF), ties the margin verse numerals to their lines, and cuts
verses on the edition's own evidence -> `tusi_paia_verses_1887.json` (with per-verse `sim` against
the later edition and `flags`). The later revision (`tusi_paia_verses.json`, `Upu`/`le ALII`) is now
only the boundary guide, the OCR spelling reference, and the FALLBACK where an 1887 verse is missing
or fails the KJV-length sanity check; `build_tusi_paia_dual.py` lists those in the index under
`fallback`. First pass: 99.0% of verses from the 1887 text. Known gaps: Psalms 18/37/78/119 (both
editions damaged there), a few chapter starts whose numeral the OCR swallowed.

**OCR: `ie` for `le` (2026-09-05).** The scan's text layer reads the article `le` as
`ie` in hundreds of places (`o ie Alo o le Atua`, John 1:49). `ie` is a real word
(cloth; `fale ie` a tent), so the known-word test kept it. `repair()` now reads `ie` as
`le` in ARTICLE position — after a phrase-heading particle (o, i, a, e, ma, mo, mai,
ia, ai) or a marker with a word following, or where the later edition's aligned word
is `le` — and leaves `le ie`, `se ie`, `fale ie`. 366 tokens in 348 verses; 464 `ie`
remain, the noun. Note `--book` never writes the corpus file; only `--all` does.

**The typed 1887 text (`sov/`, 2026-09-05, complete 2026-09-06).** bible.com's SOV (2203) and
the Bible Society of the South Pacific's own site (`oletusipaia.global.bible`, version
`a65a2238d5aefb75-01`, labelled "Samoan Edited Old Version") carry the same text: the 1887
words typed; the publisher claims copyright on the edition and layout, the words are the 1887
words (the user's ruling). Neither site offers a download; the text is served chapter by
chapter from api.bible. On the user's word ("so copy and paste ... you have the chapters you
know them") the 346 chapters where the scan had trouble were copied from the site's rendered
page in the in-app browser, one chapter per file, `corpus/tusi_paia/sov/<USFM>.<chapter>.txt`
(e.g. `PSA.119.txt`), verse numbers glued to the first word exactly as the page renders them.
Every file was verified on arrival: a hash of the text computed in the page against the
saved file, and the parsed verse count against the KJV numbering (346 of 346 match; Hosea 2
prints verses 1-2 as one range, which the parser drops).

`scripts/sov_reference.py` parses them: standalone all-caps lines (the site's banner, Psalm
119's acrostic names `ALEFA.`/`PETA.`) are never verse text; a glued range `1-2Ia` is dropped
and the count jumps past it. The segmenter uses a typed chapter as the boundary guide and the
aligned-word reference (`lesu` -> `Iesu`, glued words split, `ie` -> `le`) -- but the 1887 PDF
is no longer on the Desktop (2026-09-06), so `segment_1887_pdf.py --all` cannot run and the
scan stays as segmented on 2026-09-05. `build_tusi_paia_dual.py` therefore takes the typed
text for EVERY verse of a typed chapter (a scan verse that passes the length check can still
carry its neighbour's tail: Psalm 119:66 began with the end of 119:65), and iterates the KJV
verse universe rather than the later edition, whose own coverage lacked 99 verses (Psalm
18:31-46, 37:22-35, 78:51-67, 82:7, 108:11, 119:66-99, 119:141-157, Revelation 19:1) that the
scan and the typed text hold. Result: 8,982 verses typed, 22,120 from the scan, 0 from the
later edition, 0 missing; Bible glossing 94.6% of tokens (95.1% inside the typed verses).
The Desktop list (`Samoan Bible chapters to paste (SOV).txt`) is now historical.
