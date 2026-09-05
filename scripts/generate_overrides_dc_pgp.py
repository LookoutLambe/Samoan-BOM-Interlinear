#!/usr/bin/env python3
"""The old name of the glosser, kept so that every caller still works.

The tool is scripts/gloss_corpus.py. It was written to fill the D&C and Pearl
of Great Price from the curated Book of Mormon, hence this name; it glosses
the WHOLE corpus now -- Book of Mormon, D&C, Pearl of Great Price and O le
Tusi Paia -- with one grammar (user, 2026-09-05: "this tool should not be just
dc_pgp but the entire corpus even the BOM").
"""
import sys
import gloss_corpus as _gc

globals().update({k: v for k, v in vars(_gc).items() if not k.startswith("__")})

if __name__ == "__main__":
    sys.exit(_gc.main())
