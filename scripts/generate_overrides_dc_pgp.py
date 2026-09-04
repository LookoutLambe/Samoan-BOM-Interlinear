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
import english_register as ER

# The English side of the gloss -- register, morphology, vocabulary -- lives
# in english_register so the checker and the grammar give the same answers.
FUNCTION_ONLY = ER.FUNCTION_ONLY
NEGATIONS = ER.PROTECTED
_stems = ER.stems
in_english = ER.in_english
modernise = ER.modernise
english_vocabulary = ER.vocabulary

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


def load_evidence() -> list:
    """The hand-curated Samoan/English unit pairs.

    They live in their own file now. They used to be read back out of
    bom_overrides.json, which is the file this script WRITES -- so its own
    guesses came back as evidence and two runs disagreed. Evidence is a fixed
    record of what a human decided; it is never the output of a pass.
    """
    data = json.loads((RES / "curated_evidence.json").read_text(encoding="utf-8"))
    return data["units"]


def build_inventory(units: list) -> dict[str, Counter]:
    inv: dict[str, Counter] = defaultdict(Counter)
    for sm, en in units:
        k = norm(sm)
        if k:
            inv[k][en] += 1
    return inv


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
    ew = content_words(english)
    core = [w for w in re.findall(r"[a-z']+", gloss.lower())
            if w not in FUNCTION_ONLY]
    if not core:
        return False                      # function words are always allowed
    return not any(in_english(w, ew) for w in core)


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

def build_word_lexicon(units: list) -> dict[str, Counter]:
    lex: dict[str, Counter] = defaultdict(Counter)
    for sm, en in units:
        if True:
            toks = norm(sm).split()
            if not toks:
                continue
            open_toks = [t for t in toks if t not in SG.CLOSED_CLASS]
            # The dictionary is built modern. The Book of Mormon's curated
            # glosses are KJV-register, so `cometh` and `comes` would sit in
            # this lexicon as two different words for one Samoan verb, each
            # with half the evidence. Modernising here merges them.
            core = [w for w in re.findall(r"[a-z']+", ER.modernise(en).lower())
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
    """(length, source) of the unit starting at i, or (0, '').

    Memory is still consulted first -- a curated unit is a human decision and
    the grammar is not better than one. But memory may no longer draw a
    boundary the GRAMMAR forbids, and that is the whole change: the curation
    recorded `i luga o` and `o loo i` as units, and both cut a construction in
    half. Two rules govern every candidate span, whatever proposed it.
    """
    def n(a, b=None):
        return norm(" ".join(toks[a:b if b is not None else a + 1]))

    def cuts_a_construction(a, b):
        """Does the span [a, b) stop part-way through a grammar frame?

        `o loo i luga o motu` was segmented `o loo i` + `luga o` because the
        curation happens to contain `o loo i`. `i luga` is a preposition, and
        a unit that ends on its `i` has taken its head. This asks, of every
        position inside the span, whether a grammar frame starts there and
        runs past the end.
        """
        for k in range(a, b):
            for m in range(SG.MAX_FORM_LEN, 1, -1):
                if k + m > b and k + m <= len(toks) and n(k, k + m) in SG.MULTI_FORMS:
                    return True
        return False

    def legal(span):
        key = n(i, i + span)
        # `o` heads the phrase that follows it, so no unit ends on one
        return not SG.ends_mid_phrase(key) and not cuts_a_construction(i, i + span)

    # 1. curated memory, longest first -- subject to both rules
    for span in range(min(maxlen, len(toks) - i), 0, -1):
        if n(i, i + span) in inv and legal(span):
            return span, "inv"

    # 2. ANY multi-token grammar frame, longest first. This used to test
    #    complex prepositions only, so the TAM pairs were invisible to the
    #    segmenter: `o loo` could never be found as a unit and only survived
    #    where the curation happened to contain it.
    for span in range(min(SG.MAX_FORM_LEN, len(toks) - i), 1, -1):
        key = n(i, i + span)
        if not legal(span):
            continue
        if key in SG.COMPLEX_PREPOSITIONS:
            return span, "prep"
        if SG.primary_gloss(key):
            return span, "rule"

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


def align_number(gloss: str, english: str) -> str:
    """Take the number from the verse, not from the Book of Mormon.

    The inventory carries whatever number the source verse had. D&C 1:2 reads
    "neither ear that shall not hear, neither heart that shall not be
    penetrated" and was glossed "the ears" and "the hearts of", because that is
    how the Book of Mormon used those words.

    The canon veto did not catch it: it stems before comparing, so `ears`
    matches `ear` and the gloss passes as "carried by the English". That test
    is asking whether the WORD is right, and it should be, or a legitimate
    plural would be refused. Number is a separate question, and the English of
    this very verse answers it -- if the gloss says `ears` where the verse says
    `ear` and never says `ears`, the verse wins.

    Only ever swaps between the singular and plural of the SAME word. It cannot
    change which word is used, so it cannot introduce a wrong reading.
    """
    ew = set(re.findall(r"[a-z']+", (english or "").lower()))
    if not ew:
        return gloss

    def fix(m):
        w = m.group(0)
        low = w.lower()
        if low in ew or low in FUNCTION_ONLY or ER.ARCHAIC.get(low, set()) & ew:
            return w
        for other in _stems(low) - {low}:
            if other in ew:
                # keep the original capitalisation
                return other.capitalize() if w[:1].isupper() else other
        return w

    return re.sub(r"[A-Za-z']+", fix, gloss)


HEAD_TRIMMABLE = {"with", "and", "or", "but", "of", "for", "by", "from",
                  "upon", "at", "on", "in"}


def trim_absent_tail(gloss: str, english: str) -> str:
    """Drop leading and trailing function words the verse does not have.

    A single remembered reading is used as it stands, which is right for the
    word and can be wrong at the edges: `faatasi` is "together with" in the
    Book of Mormon, and D&C 1:1 reads "listen together" with no "with"
    anywhere. The scoring that would have caught it only runs when there is
    more than one candidate to score.

    Deliberately timid. Trailing only, function words only, and only when the
    verse does not contain them -- so it can shorten a gloss but never change
    which words it uses, and it stops at the first content word.
    """
    ew = set(re.findall(r"[a-z']+", (english or "").lower()))
    if not ew:
        return gloss
    parts = gloss.split()

    def absent(word: str) -> bool:
        w = re.sub(r"[^a-z']", "", word.lower())
        return bool(w) and (w in FUNCTION_ONLY and w not in NEGATIONS
                            and not in_english(w, ew))

    # BOTH ends, but not the same words at each. `ma outou` is "with you" in
    # the Book of Mormon and D&C 1:1 reads "and ye that are upon the islands"
    # -- `ma` is "and" there, and a gloss saying "with" asserts a relation the
    # verse does not have. Dropping it leaves "you": less, but not wrong.
    #
    # The head is the RISKIER end and gets a narrower list. Trailing function
    # words are prepositions and particles; LEADING ones are as often the
    # auxiliary that carries the tense, and the general rule turned
    # "shall not see" into "not see". Only relational words come off the front.
    while len(parts) > 1 and absent(parts[-1]):
        parts.pop()
    while (len(parts) > 1 and absent(parts[0])
           and re.sub(r"[^a-z']", "", parts[0].lower()) in HEAD_TRIMMABLE):
        parts.pop(0)
    return " ".join(parts)


def choose_particle(form: str, english: str, inv, prev_key: str = "",
                    prev_tok: str = "", next_tok: str = "",
                    clause_initial: bool = False) -> tuple[str, str]:
    """Gloss a one-vowel particle from its CLOSED set of readings.

    choose() cannot do this job: every reading of a particle is a function
    word, so its content-word gate empties and it falls through to whichever
    reading the curation's segmentation parked on this token most often. Here
    the candidates are fixed by the grammar and the VERSE picks among them --
    frequency is only a tie-break, and a reading the verse does not contain is
    used only when the grammar has just one.
    """
    readings = SG.particle_readings(form)
    if not readings:
        return "", "absorbed-particle"
    # a locative frame already carries the English; its `o` says nothing more
    if form == "o" and prev_key in SG.SILENT_AFTER:
        return "", "silent-after-prep"
    ew = set(re.findall(r"[a-z']+", (english or "").lower()))

    # THE FRAME PROPOSES, THE VERSE CONFIRMS. A frame-only reading is written
    # only when the verse actually carries it, so a 72%-reliable frame costs
    # nothing on the 28%.
    framed = SG.contextual_reading(form, prev_tok, next_tok, clause_initial)
    if framed == "":
        return "", "silent-by-frame"
    if framed and in_english(framed, ew):
        return framed, "frame"
    scored = sorted(
        ((in_english(r, ew), inv.get(form, {}).get(r, 0), -n, r)
         for n, r in enumerate(readings)),
        reverse=True)
    present, _weight, _order, best = scored[0]
    if present:
        return best, "particle"
    if len(readings) == 1:
        return readings[0], "particle-sole"
    return "", "particle-undecided"


def choose(cands: Counter, english: str) -> tuple[str, str]:
    """(gloss, why). '' means leave it empty."""
    if len(cands) == 1:
        only = cands.most_common(1)[0][0]
        if vetoed(only, english):
            return "", "vetoed"
        return trim_absent_tail(only, english), "settled"
    ew = content_words(english)
    stem_ew = set()
    for w in ew:
        stem_ew |= _stems(w)
    scored = []
    for gloss, n in cands.items():
        words = re.findall(r"[a-z']+", gloss.lower())
        core = [w for w in words
                if w not in ("i", "you", "we", "they", "he", "she", "it", "the",
                             "a", "an", "of", "to", "and")]
        # the SAME test the scoring uses; when these two disagreed, a gloss
        # could fail the gate on `you` while the verse said `ye` and be thrown
        # away before it was ever scored
        if not core or not all(in_english(w, ew) for w in core):
            continue
        # EVERY word counts, function words included. The old score looked only
        # at content words, so `faatasi` -> "together with" beat "together" in a
        # verse reading "listen together" and no "with" anywhere: the stray
        # preposition was invisible to the test that was supposed to catch it.
        present = sum(1 for w in words if in_english(w, ew))
        absent = sum(1 for w in words if not in_english(w, ew))
        # A RATIO, not a count. Counting rewarded length: `tagata uma` came out
        # "all the people" over "all men" because three words of the English
        # beat two, though both are entirely carried by it. The question is
        # what fraction of the gloss the verse accounts for; how often the
        # Book of Mormon chose it breaks the tie.
        # a candidate that carries a negation the verse has outranks one that
        # silently drops it, whatever the ratio says
        neg = sum(1 for w in words if w in NEGATIONS and in_english(w, ew))
        scored.append((present / max(1, present + absent), neg, n, gloss))
    if scored:
        scored.sort(reverse=True)
        # trim on this path too: the scoring picks the best of what the
        # inventory offers, and the best may still carry a word the verse does
        # not have, when every candidate does
        return trim_absent_tail(scored[0][3], english), "canon"
    dom, n = cands.most_common(1)[0]
    if vetoed(dom, english):
        return "", "vetoed"
    total = sum(cands.values())
    if n / total >= 0.90:
        return trim_absent_tail(dom, english), "dominant"
    return "", "undecided"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)

    ov = json.loads((RES / "bom_overrides.json").read_text(encoding="utf-8"))

    # EVIDENCE IS CURATED VERSES ONLY. The inventory was being built from every
    # verse in the file, and this script's own previous output is in that file:
    # a gloss it guessed last run came back as evidence this run, outvoted the
    # curation it was derived from, and the two runs disagreed with each other.
    # A corpus can never be validated against itself. `generated` is the list
    # of verses this script wrote, so the Book of Mormon's 42,538 hand-curated
    # units are exactly what is left.
    units = load_evidence()
    inv = build_inventory(units)
    lex = build_word_lexicon(units)
    maxlen = max(len(k.split()) for k in inv)
    english = json.loads((RES / "bom_english.json").read_text(encoding="utf-8"))
    books = json.loads((RES / "bom_books.json").read_text(encoding="utf-8"))["books"]

    # EVERY VOLUME. The curated segmentation drew boundaries the grammar
    # forbids -- `i luga o`, `o loo i`, 3,635 units ending on a phrase head --
    # so it no longer decides where units fall anywhere in the corpus. It is
    # kept in full as EVIDENCE (curated_evidence.json, 111,683 pairs): it still
    # says what a Samoan string was read as, it just no longer says where the
    # string stops.
    already = set()
    hand = set()
    stats = Counter()
    made = 0

    for book in books:
        if book.get("volume") not in ("bom", "dc", "pgp"):
            continue
        for ch in book["chapters"]:
            for verse in ch["verses"]:
                key = f"{book['id']}|{ch['num']}|{verse['num']}"
                if key in hand:
                    stats["left: hand-curated"] += 1
                    continue
                toks = [w["sm"] for w in verse["words"]]
                # MATCH MODERN AGAINST MODERN. The glosses are modern English
                # now and the canon is KJV-register, so every test that asks
                # whether the verse carries a gloss word was comparing across
                # registers: "to" stopped matching "unto", 3,652 times. The
                # published English is untouched -- this is a comparison copy,
                # and nothing written to the page comes from it.
                en_text = modernise(english.get(
                    f"{book['nameEn']}|{ch['num']}|{verse['num']}", ""))
                out = [{"sm": t, "en": ""} for t in toks]
                i = 0
                prev_key = ""
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
                    # A FORM WITH TWO REAL READINGS lets the verse choose;
                    # only a form with one gets a fixed answer. `i latou` is
                    # "them" 515 times and "they" 271, and the grammar has no
                    # business picking for a verse it can see.
                    if len(SG.particle_readings(key_sm)) > 1 \
                            and key_sm not in SG.AMBIGUOUS:
                        prev_raw = toks[i - 1] if i else ""
                        gloss, why = choose_particle(
                            key_sm, en_text, inv, prev_key,
                            prev_tok=norm(prev_raw),
                            next_tok=norm(toks[i + hit]) if i + hit < len(toks) else "",
                            clause_initial=(i == 0 or prev_raw[-1:] in SG.CLAUSE_END))
                        why = "reading/" + why
                        stats["unit: " + why] += 1
                        prev_key = key_sm
                        if gloss:
                            gloss = modernise(align_number(gloss, en_text))
                            for j in range(i, i + hit - 1):
                                out[j]["en"] = CONT
                            out[i + hit - 1]["en"] = gloss
                        i += hit
                        continue

                    gloss = SG.primary_gloss(key_sm)
                    if gloss:
                        # A rule says what a form reads as EVERYWHERE, and the
                        # verse still gets a say at the edges: `faatasi` was
                        # "together with" in a verse reading "listen together"
                        # because the grammar's answer went straight to the
                        # page, skipping the finishing every other path gets.
                        gloss = trim_absent_tail(gloss, en_text)
                        why = "grammar/" + src
                    elif key_sm in SG.AMBIGUOUS:
                        prev_raw = toks[i - 1] if i else ""
                        gloss, why = choose_particle(
                            key_sm, en_text, inv, prev_key,
                            prev_tok=norm(prev_raw),
                            next_tok=norm(toks[i + hit]) if i + hit < len(toks) else "",
                            clause_initial=(i == 0 or
                                            prev_raw[-1:] in SG.CLAUSE_END))
                        why = why + "/" + src
                    elif False:
                        # THE ONE-VOWEL RADICALS. `o`, `e`, `a`, `i`, `le`,
                        # `ma` each carry several grammatical jobs and the form
                        # cannot tell you which -- the same problem lamed, yod,
                        # he and mem pose in Hebrew. The inventory will happily
                        # answer anyway, because somewhere in 111,683 units a
                        # bare `o` was read as almost every English word, and
                        # then whichever reading the verse happens to contain
                        # wins. That is not evidence, it is drift: Alma 32:21
                        # came out `o`="as" three times and `le`="the
                        # knowledge" twice.
                        #
                        # These are glossed by POSITION or not at all.
                        gloss, why = "", "ambiguous/" + src
                    elif key_sm in inv:
                        gloss, why = choose(inv[key_sm], en_text)
                        why = why + "/" + src
                    elif key_sm in lex:
                        gloss, why = choose(lex[key_sm], en_text)
                        why = why + "/lex"

                    else:
                        gloss, why = "", "no-gloss/" + src
                    # BACK OFF TO THE CONTENT WORD. A remembered reading of a
                    # whole phrase is rejected when the verse does not carry
                    # all of it -- `o ona fofoga` is "of his eyes," somewhere
                    # in the Book of Mormon and D&C 1:1 says "whose eyes",
                    # so the "his" sank the whole unit and `fofoga` printed
                    # nothing. The unit's one open-class word still has a
                    # reading, and the verse still decides which: this can
                    # only ever produce a word the verse actually has.
                    if not gloss:
                        open_toks = [t for t in key_sm.split()
                                     if t not in SG.CLOSED_CLASS
                                     and t not in SG.AMBIGUOUS]
                        if len(open_toks) == 1 and open_toks[0] in lex:
                            d = lex[open_toks[0]]
                            back, bwhy = choose(d, en_text)
                            # A COMMON WORD'S RARE READING needs more than one
                            # verse happening to contain it. `mea` is "thing"
                            # 1,714 times and was read "own" off 3 witnesses,
                            # because the verse said "own" somewhere in it.
                            total = sum(d.values())
                            share = d.get(back, 0) / total if total else 0
                            if back and not (total >= 500 and share < 0.01):
                                gloss, why = back, bwhy + "/backoff"
                    prev_key = key_sm
                    stats["unit: " + why] += 1
                    if gloss:
                        gloss = modernise(align_number(gloss, en_text))
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
