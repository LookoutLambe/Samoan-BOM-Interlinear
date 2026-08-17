#!/usr/bin/env python3
"""Build Resources/bom_diacritics.json from the curated type table.

The bundled Samoan text follows the published (unmarked) orthography. This
script turns scripts/diacritics_types.tsv into a lookup the app can apply at
render time, so the reader can toggle a diacritically-marked register on
without the official text being rewritten.

Two layers are emitted:

  types      normalized lowercase form -> marked form. Applies everywhere.
  exceptions "bookId|chapter|verse|tokenIndex" -> marked form. Wins over
             `types`, for words whose marking depends on context (mai / ma’i).

Run from the repo root:

    python3 scripts/build_diacritics.py

Reports how much running text the table now covers. `--check` validates and
prints the report without writing the JSON.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "O le Tusi a Mamona Interlinear" / "Resources"
TABLE = ROOT / "scripts" / "diacritics_types.tsv"
OVERRIDES = RESOURCES / "bom_overrides.json"
OUTPUT = RESOURCES / "bom_diacritics.json"

# Hand-written exceptions, for one-off cases a rule can't express.
# Format: "bookId|chapter|verse|tokenIndex": "marked form"
EXCEPTIONS: dict[str, str] = {}

# Sense rules: same spelling, different word depending on meaning. The English
# gloss on the enclosing cluster tells us which sense is in play, so these
# expand at build time into explicit per-token exceptions.
#
#   form   normalized type the rule applies to
#   gloss  regex matched (case-insensitive) against the cluster's English gloss
#   marked the form to use when it matches; the type-level default applies otherwise
SENSE_RULES: list[dict[str, str]] = [
    {
        "form": "ona",
        "gloss": r"\bbecause\b",
        "marked": "onā",
        "note": "causal 'because'; possessive/particle ona stays bare",
    },
]

# Productive morphemes worth encoding as a rule instead of 669 separate rows.
# `faʻa-` is Samoan's causative/similative prefix, so essentially every
# word-initial "faa" is really "faʻa". Rules are expanded into explicit type
# entries at build time — the app stays a plain lookup, and the emitted JSON
# stays auditable. A row in the TSV always beats a rule.
PREFIX_RULES: list[tuple[str, str]] = [
    ("faa", "fa’a"),
]

GLOTTAL = "’"          # ’ — matches the existing a’u / lo’u spelling
WRONG_GLOTTAL = "ʻ"    # ʻ — rejected, so the two never mix in one corpus
MACRONS = "āēīōūĀĒĪŌŪ"

# A word's "core": what's left after trimming anything that isn't a letter or
# an intra-word glottal/hyphen. MUST match `normalizedCore` in ScriptureLibrary.swift.
_TRIM = re.compile(r"^[^\w’-]+|[^\w’-]+$")


def normalize(token: str) -> str:
    return _TRIM.sub("", token).lower()


def load_table() -> tuple[dict[str, str], set[str], list[str]]:
    """Returns (forms that change, every form reviewed, validation problems)."""
    if not TABLE.exists():
        sys.exit(f"missing curated table: {TABLE}")
    mapping: dict[str, str] = {}
    reviewed: set[str] = set()
    problems: list[str] = []
    for lineno, raw in enumerate(TABLE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            problems.append(f"line {lineno}: expected at least 2 tab-separated columns")
            continue
        form, marked = parts[0].strip(), parts[1].strip()
        if not form or not marked:
            problems.append(f"line {lineno}: empty form or marked value")
            continue
        if marked == "?":
            continue  # still awaiting a native check
        if WRONG_GLOTTAL in marked:
            problems.append(f"line {lineno}: {marked!r} uses U+02BB; use U+2019 ({GLOTTAL})")
            continue
        if form != normalize(form):
            problems.append(f"line {lineno}: form {form!r} is not normalized (want {normalize(form)!r})")
            continue
        # The marked form must differ only by diacritics, never by letters.
        if strip_diacritics(marked).lower().replace(GLOTTAL, "") != form.replace(GLOTTAL, ""):
            problems.append(
                f"line {lineno}: {form!r} -> {marked!r} changes letters, not just diacritics"
            )
            continue
        reviewed.add(form)
        # Case is reapplied from the original token at render time, so a row that
        # differs only in capitalization carries no diacritic information.
        if marked.lower() != form:
            if form in mapping and mapping[form] != marked.lower():
                problems.append(f"line {lineno}: conflicting entry for {form!r}")
                continue
            mapping[form] = marked.lower()
    print(f"table: {len(reviewed)} types reviewed, {len(mapping)} carry a diacritic change")
    return mapping, reviewed, problems


def strip_diacritics(s: str) -> str:
    """Remove macrons but keep the glottal, so we can compare letter skeletons."""
    decomposed = unicodedata.normalize("NFD", s)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def apply_sense_rules() -> tuple[dict[str, str], collections.Counter]:
    """Walk every cluster and emit per-token exceptions where a sense rule fires.

    A cluster runs from just after the previous gloss-bearing token through the
    next one; its English gloss sits on that last token (the `·` convention).
    Returns (exceptions keyed "bookId|chapter|verse|tokenIndex", near-miss glosses
    per rule form, so ambiguous senses can be reviewed rather than guessed).
    """
    data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    compiled = [(r, re.compile(r["gloss"], re.IGNORECASE)) for r in SENSE_RULES]
    exceptions: dict[str, str] = {}
    near_misses: collections.Counter = collections.Counter()

    for verse_key, words in data["verses"].items():
        start = 0
        for i, w in enumerate(words):
            gloss = w["en"].strip()
            if not gloss or gloss == "·":
                continue
            for offset in range(start, i + 1):
                core = normalize(words[offset]["sm"])
                for rule, pattern in compiled:
                    if core != rule["form"]:
                        continue
                    if pattern.search(gloss):
                        exceptions[f"{verse_key}|{offset}"] = rule["marked"]
                    else:
                        near_misses[(rule["form"], gloss)] += 1
            start = i + 1
    return exceptions, near_misses


def corpus_types() -> collections.Counter:
    data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    counts: collections.Counter = collections.Counter()
    for words in data["verses"].values():
        for w in words:
            core = normalize(w["sm"])
            if core:
                counts[core] += 1
    return counts


def is_marked_in_source(form: str) -> bool:
    return GLOTTAL in form or any(c in form for c in MACRONS)


def apply_prefix_rules(
    mapping: dict[str, str], counts: collections.Counter
) -> dict[str, str]:
    """Expand PREFIX_RULES over corpus types, returning only the rule-derived
    entries. Curated rows and words already marked in the source are left alone.
    """
    derived: dict[str, str] = {}
    for form in counts:
        if form in mapping or is_marked_in_source(form):
            continue
        for prefix, replacement in PREFIX_RULES:
            if form.startswith(prefix) and len(form) > len(prefix):
                derived[form] = replacement + form[len(prefix):]
                break
    return derived


def report(
    curated: dict[str, str],
    derived: dict[str, str],
    reviewed: set[str],
    counts: collections.Counter,
) -> None:
    total = sum(counts.values())
    tally = lambda forms: sum(counts[f] for f in forms if f in counts)  # noqa: E731

    restored = tally(curated)
    by_rule = tally(derived)
    already = sum(n for form, n in counts.items()
                  if form not in curated and form not in derived
                  and is_marked_in_source(form))
    confirmed = sum(n for form, n in counts.items()
                    if form in reviewed and form not in curated
                    and not is_marked_in_source(form))
    backlog = [(f, n) for f, n in counts.most_common()
               if f not in reviewed and f not in derived and not is_marked_in_source(f)]
    pending = sum(n for _, n in backlog)

    print(f"corpus: {len(counts)} types, {total} tokens")
    print(f"  marks restored by table     {restored:7d}  ({100 * restored / total:.1f}%)")
    print(f"  marks restored by rule      {by_rule:7d}  ({100 * by_rule / total:.1f}%)"
          f"  <- {len(derived)} types, spot-check these")
    print(f"  already marked in source    {already:7d}  ({100 * already / total:.1f}%)")
    print(f"  reviewed, correctly bare    {confirmed:7d}  ({100 * confirmed / total:.1f}%)")
    print(f"  NOT YET REVIEWED            {pending:7d}  ({100 * pending / total:.1f}%)"
          f"  <- {len(backlog)} types")
    verified = total - pending
    print(f"  => running text accounted   {verified:7d}  ({100 * verified / total:.1f}%)")

    if backlog:
        print("\n  highest-frequency types still to review:")
        for form, n in backlog[:15]:
            print(f"    {form:16s} {n:6d}x  ({100 * n / total:.2f}% of text)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only, don't write")
    args = ap.parse_args()

    mapping, reviewed, problems = load_table()
    if problems:
        print("\nVALIDATION FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    counts = corpus_types()
    derived = apply_prefix_rules(mapping, counts)
    report(mapping, derived, reviewed, counts)

    sense_exceptions, near_misses = apply_sense_rules()
    if SENSE_RULES:
        print("\nsense rules:")
        for rule in SENSE_RULES:
            hits = sum(1 for v in sense_exceptions.values() if v == rule["marked"])
            print(f"  {rule['form']} -> {rule['marked']}  when gloss matches "
                  f"/{rule['gloss']}/  : {hits} occurrences")
            print(f"    {rule['note']}")
        # Glosses that did NOT match are worth eyeballing — a causal sense the
        # regex misses would leave the word wrongly bare.
        print("\n  most common non-matching glosses (review for missed senses):")
        for (form, gloss), n in near_misses.most_common(8):
            print(f"    {form:6s} {n:5d}x  {gloss!r}")

    unused = sorted(set(mapping) - set(counts))
    if unused:
        print(f"\n  warning: {len(unused)} table entries never occur in the corpus: "
              f"{', '.join(unused[:8])}")

    if args.check:
        return 0

    combined = {**derived, **mapping}          # curated rows win over prefix rules
    all_exceptions = {**sense_exceptions, **EXCEPTIONS}  # hand-written wins over sense rules
    payload = {
        "version": 1,
        "glottal": GLOTTAL,
        "rules": [{"prefix": p, "marked": m} for p, m in PREFIX_RULES],
        "senseRules": SENSE_RULES,
        "curatedCount": len(mapping),
        "ruleDerivedCount": len(derived),
        "types": dict(sorted(combined.items())),
        "exceptions": dict(sorted(all_exceptions.items())),
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {OUTPUT.relative_to(ROOT)} "
          f"({len(payload['types'])} types, {len(payload['exceptions'])} exceptions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
