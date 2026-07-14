"""
Auto-gloss the entire Samoan Book of Mormon corpus using the phrase
dictionary at `samoan_phrases.json`.

Algorithm: for each verse, walk token-by-token. At each position, try
the longest dictionary phrase first; if its normalized Samoan tokens
match the source, emit a TAM span (`{sm, en:"·"}` continuations followed
by the final word carrying the gloss). If nothing matches, emit a single
`{sm, en:""}` entry so the reader still shows the word.

The result is written to `bom_overrides.json`. Any per-verse hand-curated
specs (e.g. `build_overrides_1nephi1.py`) should be re-run AFTER this so
they overwrite the auto-glossed entries with the higher-fidelity ones.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_books.json"
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"
PHRASES_PATH = Path(__file__).resolve().parent / "samoan_phrases.json"

PUNCT_STRIP = ".,;:!?—()"


def normalize(token: str) -> str:
    return token.strip().lower().rstrip(PUNCT_STRIP)


def load_phrases() -> list[tuple[list[str], str]]:
    payload = json.loads(PHRASES_PATH.read_text(encoding="utf-8"))
    return [(entry["sm"], entry["en"]) for entry in payload["phrases"]]


def gloss_verse(source_words: list[dict], phrases: list[tuple[list[str], str]]) -> list[dict]:
    """Greedy longest-match phrase glosser. Phrases are pre-sorted long→short."""
    # Pre-normalize source tokens once.
    normalized_tokens = [normalize(w["sm"]) for w in source_words]
    n = len(source_words)

    # Index phrases by their first normalized token so per-position scan is cheap.
    by_first: dict[str, list[tuple[list[str], str]]] = {}
    for sm, en in phrases:
        if sm:
            by_first.setdefault(sm[0], []).append((sm, en))

    out: list[dict] = []
    i = 0
    while i < n:
        matched_span: int = 0
        matched_en: str | None = None
        candidates = by_first.get(normalized_tokens[i], ())
        for sm, en in candidates:
            span = len(sm)
            if i + span > n:
                continue
            if normalized_tokens[i:i + span] == sm:
                matched_span = span
                matched_en = en
                break  # phrases are length-sorted; first hit is longest
        if matched_en is not None and matched_span > 0:
            for k in range(matched_span - 1):
                out.append({"sm": source_words[i + k]["sm"], "en": "·"})
            out.append({"sm": source_words[i + matched_span - 1]["sm"], "en": matched_en})
            i += matched_span
        else:
            out.append({"sm": source_words[i]["sm"], "en": ""})
            i += 1
    return out


def main() -> None:
    if not PHRASES_PATH.exists():
        print(f"!! {PHRASES_PATH} not found — run extract_phrases.py first.", file=sys.stderr)
        sys.exit(1)

    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    phrases = load_phrases()

    payload: dict = {"version": 1, "verses": {}}
    if OVERRIDES_PATH.exists():
        existing = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
        payload["version"] = existing.get("version", 1)

    written = 0
    matched_total = 0
    span_total = 0
    for book in books["books"]:
        for chapter in book["chapters"]:
            for verse in chapter["verses"]:
                key = f"{book['id']}|{chapter['num']}|{verse['num']}"
                glossed = gloss_verse(verse["words"], phrases)
                payload["verses"][key] = glossed
                written += 1
                # Tally for sanity reporting.
                for w in glossed:
                    if w["en"] and w["en"] != "·":
                        matched_total += 1
                    if w["en"] == "·":
                        span_total += 1

    OVERRIDES_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {written} verse overrides to {OVERRIDES_PATH}")
    print(f"  phrase-glossed tokens: {matched_total + span_total}")
    print(f"  distinct phrase hits:  {matched_total}")


if __name__ == "__main__":
    main()
