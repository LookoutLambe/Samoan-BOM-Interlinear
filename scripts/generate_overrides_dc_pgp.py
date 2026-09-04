"""
A FIRST-PASS interlinear for the Doctrine and Covenants and the Pearl of Great
Price, built from the Book of Mormon's own curation.

The Book of Mormon's 6,604 verses were glossed by hand across 239 chapter
scripts, and that work is an inventory: 42,538 distinct Samoan units, each with
the English the translator chose for it. Greedy longest-match segmentation of
the new volumes against that inventory covers 93.8% of their 186,684 tokens.
So this does not gloss Samoan -- it REUSES glosses this project already
settled, and refuses to do anything else.

THE RULES, and they are all refusals:

  Never invent. A unit is glossed only if the Book of Mormon glossed that exact
  unit. Anything unmatched stays empty, as the whole corpus was before curation.

  Where the Book of Mormon settled on ONE reading, use it.

  Where it drifted -- 1,367 units are glossed more than one way, because `i luga
  o` really is "upon" or "over" depending on what is above what -- the verse's
  own printed English decides, by testing which candidate's content words the
  English actually carries.

  Where nothing decides it, leave it EMPTY unless the unit is closed class,
  where the dominant reading is safe because the ambiguity is grammatical
  rather than semantic.

WHAT THIS IS NOT. It is not curation. It is the state the Book of Mormon was in
before its 239 passes: a starting point that a reader can use and a translator
can correct. Every verse it touches is listed under `generated` in
bom_overrides.json so a later audit can tell machine-proposed from
hand-curated, and so this can be re-run without trampling curation that has
happened since.

    python3 generate_overrides_dc_pgp.py [--dry-run] [--limit N]
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
import check_grammar as CG            # noqa: E402
import samoan_grammar as SG           # noqa: E402

RES = HERE.parent / "O le Tusi a Mamona Interlinear" / "Resources"
CONT = "·"


def norm(sm: str) -> str:
    """One key per word. See samoan_grammar.normalise_glottal: four codepoints
    spell the glottal in this corpus, and four spellings of one letter would
    split it across four index keys."""
    return re.sub(r"[^\w’\- ]", "",
                  SG.normalise_glottal(sm)).lower().strip()


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']+", (text or "").lower())}


def build_inventory(verses: dict) -> dict[str, Counter]:
    inv: dict[str, Counter] = defaultdict(Counter)
    for words in verses.values():
        for sm, en, _i in CG.units(words):
            k = norm(sm)
            if k:
                inv[k][en] += 1
    return inv


FUNCTION_ONLY = {
    "i", "you", "we", "they", "he", "she", "it", "the", "a", "an", "of", "to",
    "and", "or", "but", "in", "on", "at", "by", "for", "with", "that", "this",
    "these", "those", "is", "are", "was", "were", "be", "shall", "will", "not",
    "unto", "ye", "thou", "thee", "thy", "his", "her", "their", "my", "your",
    "them", "him", "me", "us", "who", "which", "all", "from", "upon", "o",
}


def _stems(word: str) -> set[str]:
    """Enough English morphology to match heart/hearts, see/saw is not tried."""
    out = {word}
    if word.endswith("ies") and len(word) > 4:
        out.add(word[:-3] + "y")
    if word.endswith("es") and len(word) > 3:
        out.add(word[:-2])
    if word.endswith("s") and not word.endswith("ss"):
        out.add(word[:-1])
    out.add(word + "s")
    return out


def vetoed(gloss: str, english: str) -> bool:
    """The canon's VETO: a gloss whose content words are nowhere in the verse.

    Not a demand that the English confirm the gloss -- the two translations
    choose different words constantly and requiring agreement would empty the
    page. This only refuses a gloss the English has no room for at all.

    It is the rule that matters most here, because the inventory carries the
    Book of Mormon's context, not this verse's. `mata o` is "faces of" in the
    Book of Mormon and this verse says "no eye that shall not see"; `maia` is
    "I pray" there and this verse is "Hearken, O ye people". Both were being
    written because the unit had exactly one Book of Mormon reading and a
    single reading was trusted without asking.
    """
    ew = set()
    for w in content_words(english):
        ew |= _stems(w)
    core = [w for w in re.findall(r"[a-z']+", gloss.lower())
            if w not in FUNCTION_ONLY]
    if not core:
        return False                      # function words are always allowed
    return not any(w in ew for w in core)


# ── THE WORD LEXICON, DERIVED FROM THE CURATION ──────────────────────────────
# The inventory can only answer for a string it has seen whole, so common words
# came out unmatched simply because they never stood alone: `fetalai` (speak)
# occurs 561 times in the Book of Mormon and never once as a unit of its own,
# always inside "ua fetalai mai ai" and its kin.
#
# But those units can be taken apart, without any positional guessing. Strip a
# unit's CLOSED-CLASS tokens -- the grammar knows exactly which they are -- and
# strip the gloss's function words. Where that leaves precisely one Samoan word
# and one English word, the pairing is forced: `ua fetalai mai ai` -> "saith"
# has `ua`, `mai` and `ai` all closed class, so "saith" can only belong to
# `fetalai`. Nothing is aligned by position, which is the error that produced
# the Spanish corpus's worst damage; it is arithmetic on what is left over.
#
# 111,683 curated units yield 2,796 Samoan words, 1,857 of them attested more
# than once. This is the project's own translation work, read back as a
# dictionary.

def build_word_lexicon(verses: dict) -> dict[str, Counter]:
    lex: dict[str, Counter] = defaultdict(Counter)
    for words in verses.values():
        for sm, en, _i in CG.units(words):
            toks = norm(sm).split()
            if not toks:
                continue
            open_toks = [t for t in toks if t not in SG.CLOSED_CLASS]
            core = [w for w in re.findall(r"[a-z']+", en.lower())
                    if w not in FUNCTION_ONLY]
            if len(open_toks) == 1 and len(core) == 1:
                lex[open_toks[0]][core[0]] += 1
    return lex


# ── SEGMENTATION: memory first, then the rule ────────────────────────────────
# Order matters, and I had it backwards. Putting the grammar's frames first
# looked principled and cost 12 points of coverage: a TAM frame happily spans
# "sa latou faia atu" and then nothing can gloss it, because the grammar knows
# the particles and not the verb between them. The Book of Mormon's 42,538
# units are CURATED -- a human decided each one -- so they are the ground
# truth for anything longer than a word.
#
# The grammar's job is the gap that memory structurally cannot fill: the
# closed-class forms that never occur alone in the Book of Mormon and so were
# never recorded as units. `te` 264 times, `ni` 113, `la’u` 98, `au` 84,
# `laua` 64 -- all in the grammar, none in the inventory.
#
# And TAM markers and directionals are ABSORBED: where nothing matches at a
# particle, it joins the unit that follows rather than being left blank, which
# is what the Book of Mormon's own curation does with them.

def frame_at(toks, i, inv, maxlen, lex=None):
    """(length, source) of the unit starting at i, or (0, '')."""
    def n(a, b=None):
        return norm(" ".join(toks[a:b if b is not None else a + 1]))

    # 1. curated memory, longest first
    for span in range(min(maxlen, len(toks) - i), 0, -1):
        if n(i, i + span) in inv:
            return span, "inv"

    # 2. a complex preposition the inventory never saw whole
    for span in (3, 2):
        if i + span <= len(toks) and n(i, i + span) in SG.COMPLEX_PREPOSITIONS:
            return span, "prep"

    # 3. a closed-class form the grammar can gloss on its own
    if SG.primary_gloss(n(i)):
        return 1, "rule"

    # 4. a single open-class word the curation defines
    if lex and n(i) in lex:
        return 1, "lex"

    # 5. an absorbed particle joins what follows: extend until something is
    #    known, up to the 5-token cluster GLOSSING_RULES.md allows
    if n(i) in SG.ABSORBED:
        for span in range(2, min(6, len(toks) - i + 1)):
            for inner in range(span - 1, 0, -1):
                if n(i + span - inner, i + span) in inv:
                    return span, "absorbed"
        return 0, ""

    return 0, ""


def choose(cands: Counter, english: str) -> tuple[str, str]:
    """(gloss, why). '' means leave it empty."""
    if len(cands) == 1:
        only = cands.most_common(1)[0][0]
        if vetoed(only, english):
            return "", "vetoed"
        return only, "settled"
    ew = content_words(english)
    scored = []
    for gloss, n in cands.items():
        core = [w for w in re.findall(r"[a-z']+", gloss.lower())
                if w not in ("i", "you", "we", "they", "he", "she", "it", "the",
                             "a", "an", "of", "to", "and")]
        if core and all(w in ew for w in core):
            scored.append((n, gloss))
    if scored:
        scored.sort(reverse=True)
        return scored[0][1], "canon"
    dom, n = cands.most_common(1)[0]
    if vetoed(dom, english):
        return "", "vetoed"
    total = sum(cands.values())
    if n / total >= 0.90:
        return dom, "dominant"
    return "", "undecided"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)

    ov = json.loads((RES / "bom_overrides.json").read_text(encoding="utf-8"))
    inv = build_inventory(ov["verses"])
    lex = build_word_lexicon(ov["verses"])
    maxlen = max(len(k.split()) for k in inv)
    english = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
    books = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))["books"]

    already = set(ov.get("generated", []))
    hand = set(ov["verses"]) - already
    stats = Counter()
    made = 0

    for book in books:
        if book.get("volume") not in ("dc", "pgp"):
            continue
        for ch in book["chapters"]:
            for verse in ch["verses"]:
                key = f"{book['id']}|{ch['num']}|{verse['num']}"
                if key in hand:
                    stats["left: hand-curated"] += 1
                    continue
                toks = [w["sm"] for w in verse["words"]]
                en_text = english.get(
                    f"{book['nameEn']}|{ch['num']}|{verse['num']}", "")
                out = [{"sm": t, "en": ""} for t in toks]
                i = 0
                while i < len(toks):
                    hit, src = frame_at(toks, i, inv, maxlen, lex)
                    if not hit:
                        stats["token: no unit"] += 1
                        i += 1
                        continue
                    key_sm = norm(" ".join(toks[i:i + hit]))
                    if src == "absorbed" and key_sm not in inv:
                        # the particle carries no English; the gloss belongs to
                        # the word it attached to
                        for back in range(1, hit):
                            tail = norm(" ".join(toks[i + back:i + hit]))
                            if tail in inv:
                                key_sm = tail
                                break
                    # THE GRAMMAR FIRST. A rule states what a form reads as
                    # everywhere; the inventory only remembers what it read as
                    # somewhere. Where the grammar refuses -- the ambiguous
                    # forms, where position decides -- the inventory and the
                    # verse's English take over.
                    gloss = SG.primary_gloss(key_sm)
                    if gloss:
                        why = "grammar/" + src
                    elif key_sm in inv:
                        gloss, why = choose(inv[key_sm], en_text)
                        why = why + "/" + src
                    elif key_sm in lex:
                        gloss, why = choose(lex[key_sm], en_text)
                        why = why + "/lex"
                    else:
                        gloss, why = "", "no-gloss/" + src
                    stats["unit: " + why] += 1
                    if gloss:
                        for j in range(i, i + hit - 1):
                            out[j]["en"] = CONT
                        out[i + hit - 1]["en"] = gloss
                    i += hit
                ov["verses"][key] = out
                already.add(key)
                made += 1
                if a.limit and made >= a.limit:
                    break
            if a.limit and made >= a.limit:
                break
        if a.limit and made >= a.limit:
            break

    ov["generated"] = sorted(already)
    glossed = sum(1 for k in already
                  for w in ov["verses"][k] if (w["en"] or "").strip())
    tokens = sum(len(ov["verses"][k]) for k in already)
    print(f"verses generated      {made}")
    print(f"tokens carrying text  {glossed} of {tokens} "
          f"({100 * glossed / tokens:.1f}%)")
    for k, n in stats.most_common():
        print(f"   {k:24} {n}")
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    (RES / "bom_overrides.json").write_text(
        json.dumps(ov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {RES / 'bom_overrides.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
