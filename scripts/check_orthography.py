#!/usr/bin/env python3
"""Find tokens that should be two words, using the grammar rather than guessing.

Two defects, and they are not the same shape:

  RUN-TOGETHER   the space is missing and every letter is present.
                 `aluese` for `alu ese`, `leiloa` for `le iloa`.

  HAPLOGRAPHY    the space is missing AND one of two identical letters at the
                 join has collapsed. `mai` + `ia` share an i, so `mai ia`
                 becomes `maia`, not `maiia`. The corpus writes it all three
                 ways -- `mai ia` 1330 times, `maia` 9, `maiia` 3 -- which is
                 what a collapsing join looks like.

WHY THE GRAMMAR AND NOT FREQUENCY. Splitting on frequency alone proposes any
cut whose halves are common, and the halves of a Samoan word are usually
common: it offered `te lē` for `telē` (great) and `ma faia` for `mafaia`
(able), both real words. The grammar constrains the cut to sequences Samoan
actually forms -- a verb followed by a directional, a TAM marker followed by a
pronoun, an article followed by a noun -- so a cut has to be grammatical before
it is even considered.

AND THE ENGLISH DECIDES. Every candidate is checked against the printed English
of its own verse: if the whole word's curated gloss is carried by the English
and the split's is not, the word stands. That is what keeps `telē` in "as great
as" and `mamai` in "any that are sick".

NOTHING IS FIXED HERE. This reports. `maia` is nine occurrences and only four
of them are the imperative `mai ia`; the other five are a directional plus a
pronoun phrase, and the translator has already glossed those correctly. One
form, two grammars, and only the verse tells you which -- so the output is a
list for a Samoan reader, not a patch.

    python3 check_orthography.py [--min-bigram N] [--all]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import samoan_grammar as SG            # noqa: E402
import check_grammar as CG             # noqa: E402
import generate_overrides_dc_pgp as G  # noqa: E402

RES = HERE.parent / "O le Tusi a Mamona Interlinear" / "Resources"


def norm(s: str) -> str:
    return re.sub(r"[^\w’\-]", "", SG.normalise_glottal(s)).lower()


# The sequences Samoan actually forms at a word boundary. A cut is only
# considered when its two halves stand in one of these relations.
def grammatical(a: str, b: str, lex) -> str | None:
    a_open = a not in SG.CLOSED_CLASS and (a in lex)
    if a_open and b in SG.DIRECTIONALS:
        return "verb + directional"
    if a in SG.DIRECTIONALS and (b in SG.TAM or b in SG.PRONOUNS):
        return "directional + particle"
    if a_open and (b in SG.TAM or b in SG.PRONOUNS):
        return "verb + particle"
    if a in SG.TAM and b in SG.PRONOUNS:
        return "TAM + pronoun"
    if a in SG.ARTICLES and (b in lex):
        return "article + noun"
    if a in SG.PREPOSITIONS and b in SG.ARTICLES:
        return "preposition + article"
    if a in SG.COORDINATORS and (b in lex or b in SG.CLOSED_CLASS):
        return "coordinator + word"
    if a_open and b in SG.CLOSED_CLASS:
        return "word + particle"
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-bigram", type=int, default=40)
    ap.add_argument("--all", action="store_true", help="include the ones the English keeps")
    a = ap.parse_args(argv)

    ov = CG.load()
    lex = G.build_word_lexicon(ov)
    inv = G.build_inventory(ov)
    english = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
    books = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))["books"]

    uni, bi = Counter(), Counter()
    for b in books:
        for ch in b["chapters"]:
            for v in ch["verses"]:
                ts = [t for t in (norm(w["sm"]) for w in v["words"]) if t]
                for i, t in enumerate(ts):
                    uni[t] += 1
                    if i + 1 < len(ts):
                        bi[t + " " + ts[i + 1]] += 1

    def candidates(w):
        """(bigram_count, a, b, kind, relation) for every grammatical cut."""
        out = []
        for k in range(2, len(w)):
            a_, b_ = w[:k], w[k:]
            for kind, aa, bb in (("run-together", a_, b_),
                                 ("haplography", a_, w[k - 1:])):
                if len(aa) < 2 or len(bb) < 2:
                    continue
                rel = grammatical(aa, bb, lex)
                if not rel:
                    continue
                n = bi.get(aa + " " + bb, 0)
                if n >= a.min_bigram:
                    out.append((n, aa, bb, kind, rel))
        out.sort(reverse=True)
        return out

    def gloss_words(word):
        out = set()
        if word in lex:
            out |= set(lex[word])
        if word in inv:
            for g in inv[word]:
                out |= set(re.findall(r"[a-z']+", g.lower()))
        p = SG.primary_gloss(word)
        if p:
            out |= set(re.findall(r"[a-z']+", p.lower()))
        return {g for g in out if g not in G.FUNCTION_ONLY}

    rows = []
    for b in books:
        for ch in b["chapters"]:
            for v in ch["verses"]:
                en = english.get(f"{b['nameEn']}|{ch['num']}|{v['num']}", "")
                ew = set(re.findall(r"[a-z']+", en.lower()))
                for w in v["words"]:
                    t = norm(w["sm"])
                    if len(t) < 4 or uni.get(t, 0) > 25:
                        continue
                    cands = candidates(t)
                    if not cands:
                        continue
                    n, aa, bb, kind, rel = cands[0]
                    whole_ok = any(g in ew for g in gloss_words(t))
                    split_ok = any(g in ew for g in (gloss_words(aa) | gloss_words(bb)))
                    if whole_ok and not split_ok and not a.all:
                        continue
                    rows.append({
                        "verdict": "SPLIT" if (split_ok and not whole_ok)
                                   else ("keep" if whole_ok else "review"),
                        "vol": b.get("volume"), "ref": f"{b['id']} {ch['num']}:{v['num']}",
                        "token": w["sm"], "split": f"{aa} {bb}", "kind": kind,
                        "rel": rel, "n": n, "en": en[:70],
                    })

    by = Counter(r["verdict"] for r in rows)
    print("tokens examined against the grammar and the verse's English")
    print("   %s\n" % dict(by))
    for verdict in ("SPLIT", "review", "keep"):
        sel = [r for r in rows if r["verdict"] == verdict]
        if not sel or (verdict == "keep" and not a.all):
            continue
        print(f"── {verdict} ({len(sel)})")
        for r in sel[:40]:
            print("   %-4s %-14s %-18s -> %-20s %-13s %-22s n=%d"
                  % (r["vol"], r["ref"], r["token"], r["split"], r["kind"],
                     r["rel"], r["n"]))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
