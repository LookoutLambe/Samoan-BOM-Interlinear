# Samoan linguistic sources

Facts of grammar are not copyrightable. `samoan_grammar.py` therefore *states*
the closed-class system rather than reproducing anyone's description of it, and
every entry in it is checked against this corpus's own usage counts, so nothing
is asserted that the text does not show.

## Public domain — usable in full

- **Pratt, George. _A Grammar and Dictionary of the Samoan Language_, 3rd ed.,
  London Missionary Society, 1893.** Public domain (published 1893; Pratt died
  1894). Full text: <https://archive.org/details/agrammaranddict00pratgoog>
  (`agrammaranddict00pratgoog_djvu.txt`, 1.2 MB).
  **Caveat: the OCR is poor** — a Google scan of a 130-year-old book whose
  macrons and glottals do not survive. `Ao, v. to search` comes out `Ac, «. to
  search`; *tagata* comes out `tagcUd`. Usable as a *check*, never as a source
  to generate from. Not vendored here for that reason.

- **NZETC's hand-corrected edition** (CC BY-SA 3.0 NZ) would be the clean
  version, but nzetc.victoria.ac.nz is no longer live — it now redirects into
  the National Library web archive.

## Free, clean, but thin

- **Wiktionary via kaikki.org**, CC BY-SA:
  <https://kaikki.org/dictionary/Samoan/kaikki.org-dictionary-Samoan.jsonl>
  Structured JSON with senses and part of speech, but only **669 entries** —
  too small to gloss a 346,933-token corpus, though fine for spot-checks.

## Consulted, not copied — the standard references

- **Mosel, Ulrike & Even Hovdhaugen. _Samoan Reference Grammar_.** Oslo, 1992.
  The scholarly descriptive grammar. Not open access.
- **Hunkin, Galumalemana Afeleti. _Gagana Samoa: A Samoan Language
  Coursebook_**, rev. ed., University of Hawaiʻi Press. This is the coursebook
  BYU uses for Samoan 100.
- The Samoan pronoun paradigm and the specificity-based article system as set
  out on Wikipedia (CC BY-SA).

## Why the closed classes are enough

This corpus has **3,741 distinct word types over 346,933 tokens, and the top 50
types are 71.6% of the text**. Samoan carries its grammar in particles, so a
particle inventory is most of the corpus — which is why `samoan_grammar.py`
covers the closed classes exhaustively and leaves the open vocabulary to the
per-chapter curation that already exists.


---

# The Samoan Bible: there is no clean, current, non-copyrighted text

Asked for a Samoan Old and New Testament that is **not copyrighted** and as
up to date as possible. The honest finding, after checking every route:

**Everything current is in copyright.** The Samoan Bible in print and in
Gospel Library is *O le Tusi Paia*, the 1884 edition published by the **Bible
Society in the South Pacific**, and the modern revisions are theirs. The
Church's Samoan downloads page offers the Book of Mormon, Doctrine and
Covenants and Pearl of Great Price as PDF/EPUB/MOBI but offers the Bible only
in print and through Gospel Library — there is no file to take, and
`/study/scriptures/ot/…` and `/nt/…` return 404 for `lang=smo`, so the site
does not host it as web text either.

**No machine-readable edition exists in the usual places.**
- eBible.org's catalogue is 1,550 translations and **none of them are Samoan**.
- No USFM/JSON Samoan Bible on the GitHub corpora (bibleapi, openenglishbible,
  BibleNLP/ebible, christos-c/bible-corpus).
- YouVersion carries two (SOV and a Roman Catholic edition); both are licensed,
  not redistributable.

**The public-domain editions are 19th-century scans, and the OCR is not
usable as scripture.** Both are British and Foreign Bible Society printings on
the Internet Archive:

- 1887 — `archive.org/details/oletusipaiaolefe00bibl` (5.8 MB of OCR)
- 1872 — `archive.org/details/oletusipaiaolef00lond` (6.9 MB of OCR)

Both are set in **two columns with words hyphenated across the column break**,
and the verse numbers interleave with the fragments, so a word is routinely
split across a verse boundary — Genesis 1 has `pouli-` ending one line and
`5 uli.` starting the next. On top of that the character damage is heavy and
systematic: the 1872 scan reads `o` as `0` throughout (`0 le lagi`, `01a`,
`n0`), plus `Pfaia`, `rfetu`, `Atga`, `spule`, `ya`; the 1887 gives `O 3e
afiafi`, `af.afi`, `i ]e va`, `Uafaia`.

**So the answer to "the most up-to-date one that is not copyrighted" is the
1887 BFBS edition** — and taking it would be a reconstruction project, not a
fetch: de-column, de-hyphenate across verse boundaries, repair the systematic
substitutions, then verify chapter and verse counts against a known
versification. Doable, and comparable to work already done on the Spanish
corpus, but it is its own piece of work and its output would need auditing
before anyone read it as scripture. Silent OCR errors in a scripture text are
the one failure mode that cannot be accepted quietly.

Not started. Recorded here so the next attempt does not re-derive it.

## Grammar

**Scott C. Dunn, *Samoan for Missionaries* (1983), BYU M.A. thesis.** The grammar the
tool encodes (GLOSSING_RULES.md §22): tense markers, the two kinds of doer, nominal and
existential sentences, the object-marking `i`, directionals, perfective suffixes and
doer omission, negation, reduplication, nominalisation, numeral prefixes, relative
clauses, `ai` / `i ai`, the unit-six conjunctions. Facts of the language, not text:
nothing of the book is reproduced. The PDF is on the user's Desktop
(`samoanformissionaries.pdf`), never in the repo. User, 2026-09-05: "forget my rules use
the samoanformissionaries as source here" -- where the curated readings and Dunn
disagree, Dunn stands.

**bible.com 2203 "SOV" (checked 2026-09-05).** The user pointed to
`bible.com/bible/2203/JHN.1.SOV` as the same 1887 text, cleanly typed. The page names it
"O LE TUSI PAIA - SOV (Samoan Edited Old Version)" and prints "© Bible Society of the
South Pacific, 2017": an EDITED old version under a current copyright claim, and
YouVersion's terms forbid scraping. So it is a searchlight, never a source (the same
standing as the IAS PDF on the Hebrew side). John 1:1-10 read against it: our scanned
1887 text matches word for word except 1:8, where the edited version has `i le lava
malamalama` for the 1887 `i lea lava malamalama` -- the edition's change, not our OCR.
