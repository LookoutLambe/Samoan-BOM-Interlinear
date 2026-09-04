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
