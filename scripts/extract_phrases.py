"""
Extract a corpus-wide Samoan→English phrase dictionary from existing
hand-curated 1 Nephi 1 overrides, plus seed phrases the user dictated.

Output: scripts/samoan_phrases.json — sorted longest-first so the greedy
matcher in build_phrase_overrides.py prefers fuller phrases.

Each entry:  { "sm": ["sa", "oo", "ina"], "en": "it came to pass" }

The `sm` field stores the *normalized* tokens (lowercased, trailing punctuation
stripped) so the matcher can compare apples-to-apples against the corpus.
"""

from __future__ import annotations

import json
import re
import string
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES_PATH = ROOT / "O le Tusi a Mamona Interlinear" / "Resources" / "bom_overrides.json"
OUT_PATH = Path(__file__).resolve().parent / "samoan_phrases.json"


# Phrases dictated explicitly by the user. These take precedence over phrases
# auto-extracted from per-verse overrides (so the user's authoritative glosses
# always win against any stale or context-specific gloss that happened to land
# in 1 Nephi 1 hand-curation). Format: (sm, en).
USER_SEED_PHRASES: list[tuple[str, str]] = [
    # Connectives / set phrases
    ("e tusa ma", "according to"),
    ("o le tulafono", "the law"),
    ("faauta", "behold"),
    ("aua faauta", "for behold"),
    ("ioe", "yea"),
    ("o le mea lea", "wherefore"),
    ("ma ona", "because"),
    ("o lea", "therefore"),
    # "It came to pass" family
    ("ma sa oo ina", "and it came to pass"),
    ("ma sa oo", "and it came to pass"),
    ("sa oo ina", "it came to pass"),
    ("sa oo", "it came to pass"),
    # Knowing / saying
    ("ma ua ou iloa", "and I knew"),
    ("ua ou iloa", "I knew"),
    ("fetalai mai", "spoke"),
    ("ma tautino atu", "and declared"),
    # Quantifiers
    ("e tele", "many"),
    ("e toatele", "many"),
    ("perofeta", "prophets"),
    # Proper nouns / titles
    ("le Alii", "the Lord"),
    ("Liae", "Lehi"),
    # Pronoun + verb patterns
    ("amuia oe", "you are blessed"),
    ("ua e faia", "you have done"),
    ("sa e faamaoni", "you have been faithful"),
    # Settings
    ("i se miti lava", "in a dream"),
    # Modal "should/must" — `e tatau ia te <DAT> ona <V>` construction
    ("e tatau ia te ia ona", "he should"),
    ("e tatau ia te a'u ona", "I should"),
    ("e tatau ia te oe ona", "you should"),
    ("e tatau ia te outou ona", "ye should"),
    ("e tatau ia te i latou ona", "they should"),
    ("e tatau ona", "should"),
    # Verb + subject/agent pronoun absorbed into the verb gloss.
    # The Samoan subject `o ia` and the agent `e ia` follow the verb but in
    # English the pronoun is naturally part of the verb phrase ("he VERB"),
    # so they get pulled into one TAM block rather than glossed standalone.
    ("usitai o ia", "he obeyed"),
    ("na faia ai e ia", "he did"),
    ("sa alu ifo o ia", "he went down"),
    ("sa malaga o ia", "he traveled"),
    ("sa tautala atu o ia", "he spake"),
    ("sa asiasi mai o ia", "he did visit"),
    ("talitonu o ia", "he believed"),
    ("sa tatalo atu o ia", "he prayed"),
    # Hortative "let us" — `ma ia tatou <V>` (conjunction absorbed)
    ("ma ia tatou faamaoni", "let us be faithful"),
    ("ia tatou faamaoni", "let us be faithful"),
    ("ia tatou o a'e", "let us go up"),
    ("ia tatou o ifo", "let us go down"),
    # Proper nouns / honorific references
    ("i se alona malosi", "His strength"),  # capital-H, referring to God
    # Quantities
    ("po o ana", "or his"),
    ("sefulu o afe", "tens of thousands"),
    # Tree of Life vision phrasing
    ("e ala mai", "through"),
    ("i le puao", "the mist"),
    ("o le pogisa", "of darkness"),
    # "I would that ye should know" decomposition
    ("ou te manao", "I would that"),
    ("ia outou iloa", "ye should know"),
    # Definite-singular vs plural distinction with `le`
    ("ona o le mea", "because of the thing"),  # singular — `le` is the definite singular article
    ("ona o mea", "because of things"),  # plural
    ("o le mea", "the thing"),  # singular
    # Other patterns from v3
    ("ua ia te a'u", "I have"),
    ("se mafuaaga", "reason"),
    ("ou te olioli ai", "to rejoice"),
    ("ua ou manatu ai", "to suppose"),
    ("o i laua", "that they"),
    ("ona", "because"),
    # Connectives / verb-list TAM principle
    ("ma", "and"),
    ("o mea uma nei", "all these things"),
    ("sa vaai", "saw"),
    ("ma faalogo", "and heard"),
    ("ma tautala i ai", "and spake"),
    ("a'o", "while"),
    ("nofo o ia", "he dwelt"),
    ("i se faleie", "in a tent"),
    ("e le o papatusi nei", "not on these plates"),
    ("o le talafaasolopito", "of the history"),
    ("o lo'u nuu", "of my people"),
    ("o nisi mea", "other things"),
    ("e pei ona", "as"),
    # Comparative idiom: `e pei lava` introduces a simile and stays atomic
    # (3 tokens), then any NP that follows must split per rule 3.
    # e.g. `e pei lava o le Tamai Mamoe a le Atua` →
    #   `e pei lava` (like) | `o le Tamai Mamoe` (the Lamb) | `a le Atua` (of God)
    ("e pei lava", "like"),
    ("o le Tamai Mamoe", "the Lamb"),
    # Locative atoms — split don't smear. `i luga` always its own cell when
    # comparative ("over"); pair with NP atom for the object.
    # e.g. `o le Atua i luga o le lalolagi atoa` →
    #   `o le Atua` (God) | `i luga` (over) | `o le lalolagi atoa` (all the earth)
    ("i luga", "over"),
    ("o le lalolagi atoa", "all the earth"),
    # `ma i totonu` introduces a locative — three TAMs:
    # `ma i totonu` (and within) | `o le aai` (the city) | `o Nasareta` (of Nazareth)
    ("ma i totonu", "and within"),
    ("o le aai", "the city"),
    ("o Nasareta", "of Nazareth"),
    ("ou tautala atu", "I spake"),
    ("e uiga i", "concerning"),
    ("papatusi nei", "these plates"),
    ("ou faia", "I make"),
    ("ma ave", "and taken"),
    ("faatagataotauaina", "captive"),
    ("o le a toe foi mai", "should return again"),
    ("i latou", "they"),
    ("mai", "from"),
    ("le faatagataotauaina", "captivity"),
    # Modal phrasing — atomic particles
    ("e mafai", "could"),
    ("e le Alii", "the Lord"),
    ("faailoa mai", "make known"),
    ("ou te lei vaai", "I had not seen"),
    ("muamua i ai", "before"),
    ("o mea", "the things"),
    ("sa vaai i ai", "which was seen"),
    # 3-word atomic groupings
    ("ma fanau foi", "and the seed also"),
    ("a ou uso", "of thy brothers"),
    ("le laueleele", "the land"),
    ("o le folafolaga", "of promise"),
    ("fetalai mai", "spake"),
    ("le agelu", "the angel"),
    # NP atoms — the Lamb of God / mother of harlots family
    ("le Tamai Mamoe", "the Lamb"),
    ("a le Atua", "of God"),
    ("le tinā lea", "the mother"),
    ("o fafine talitane", "of harlots"),
    ("o atunuu", "the nations"),
    ("ma malo ia", "and kingdoms"),
    ("o nuuese", "of the Gentiles"),
    ("maa tu'ia", "stumbling blocks"),
    ("ma sa latou", "and they"),
    ("fefinaua'i", "disputing"),
    ("o le tasi ma le isi", "with one another"),
    ("ua ole atu", "inquire"),
    ("le tagata", "a man"),
    ("i le Alii", "unto the Lord"),
]


# Normalize a Samoan surface token for matching: lowercase + strip a small
# set of trailing punctuation. The matcher uses normalized form on both
# sides so capitalization and verse-end punctuation don't fragment matches.
PUNCT_STRIP = ".,;:!?—()"


def normalize(token: str) -> str:
    return token.strip().lower().rstrip(PUNCT_STRIP)


def normalize_phrase(text: str) -> list[str]:
    return [normalize(t) for t in text.split() if t.strip()]


def extract_from_overrides(overrides_path: Path) -> list[tuple[tuple[str, ...], str]]:
    payload = json.loads(overrides_path.read_text(encoding="utf-8"))
    out: list[tuple[tuple[str, ...], str]] = []
    for key, words in payload["verses"].items():
        phrase: list[str] = []
        for w in words:
            phrase.append(w["sm"])
            if w["en"] != "·":
                # Skip empty glosses (unmapped tokens) — they aren't dictionary entries.
                if w["en"].strip():
                    normalized = tuple(normalize(t) for t in phrase)
                    # Skip entries where normalization wipes the phrase entirely.
                    if all(normalized):
                        out.append((normalized, w["en"]))
                phrase = []
    return out


def main() -> None:
    if not OVERRIDES_PATH.exists():
        print(f"!! {OVERRIDES_PATH} not found — run build_overrides_1nephi1.py first.", file=sys.stderr)
        sys.exit(1)

    extracted = extract_from_overrides(OVERRIDES_PATH)

    # USER_SEED_PHRASES wins: insert them first so they claim the dictionary
    # slot, then extracted entries fill in everything else they don't already cover.
    seen: dict[tuple[str, ...], str] = {}
    for sm, en in USER_SEED_PHRASES:
        normalized = tuple(normalize_phrase(sm))
        if normalized:
            seen[normalized] = en
    for sm_tokens, en in extracted:
        if sm_tokens and sm_tokens not in seen:
            seen[sm_tokens] = en

    # Emit sorted by length DESC so the greedy matcher tries longer phrases first.
    entries = sorted(
        ({"sm": list(k), "en": v} for k, v in seen.items()),
        key=lambda e: (-len(e["sm"]), e["sm"]),
    )

    OUT_PATH.write_text(
        json.dumps({"phrases": entries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {len(entries)} phrases to {OUT_PATH}")
    print(f"  longest: {' '.join(entries[0]['sm'])}  →  {entries[0]['en']}")
    print(f"  shortest: {' '.join(entries[-1]['sm'])}  →  {entries[-1]['en']}")


if __name__ == "__main__":
    main()
