# Samoan TAM Glossing Rules — O le Tusi a Mamona Interlinear

Canonical rules for hand-curating English interlinear gloss overrides for the Samoan
Book of Mormon Interlinear app. This is the version-controlled source of truth (kept in
the project so it survives config resets). The per-chapter specs live in
`scripts/build_overrides_<book><n>.py`; the compiled output is
`O le Tusi a Mamona Interlinear/Resources/bom_overrides.json` keyed `bookId|chapter|verse`.

Gloss into English by **atomic linguistic units** of 2–5 tokens — *not* a fixed length and
*not* sprawling multi-clause chunks. The grouping is dynamic; size depends on what is a
single linguistic unit. The `·` continuation-marker mechanism (see
`Views/WordUnitView.swift` `groupIdiomSpans`) is reused:
`[{sm:"sa", en:"·"}, {sm:"oo", en:"came to pass"}]`.

**Why:** Samoan grammar groups TAM markers tightly with their verb, articles tightly with
their noun, but each NP / PP / TAM-verb-cluster is its own atomic unit. Sprawling glosses
(8+ tokens for one English phrase) lose the linguistic structure and read as English
summaries rather than interlinear.

---

## Rules (priority order)

**1. TAM verb cluster (atomic, 2–5 tokens).** `sa oo` → "came to pass" | `ma sa oo` → "and
it came to pass" | `sa oo ina` and `ma sa oo ina` → same idiom (the `ina` belongs to the
idiom). `e mafai` → "could" by itself; `e mafai ona` is NOT one unit — split `e mafai` +
`ona`. TAM particles `e`, `sa`, `na`, `ua`, `ma sa`, `o le a` each get atomic glosses.
`sa` and `na` are interchangeable past-tense TAM markers (same meaning, dialectal/stylistic
variation): `sa ou aluese ai` = `na ou aluese ai` = "I came out". When `ai` (anaphoric)
caps a verb cluster AND a source/destination PP (`mai X`, `i X`) follows in the same clause,
the `ai` refers to that PP — don't echo it as "thereto".

**2. Subject `o ia` and agent `e ia` are absorbed into the verb cluster.** `usitai o ia` →
"he obeyed", `na faia ai e ia` → "he did", `sa tatalo atu o ia` → "he prayed". Do NOT split
them off as standalone "he".

**3. NP atoms (article + head, 2–3 tokens).** `le Tamai Mamoe` → "the Lamb" / `a le Atua` →
"of God" / `le tinā lea` → "the mother" / `le agelu` → "the angel" / `o le Alii` → "of the
Lord" / `o mea` → "the things". Always split these even in compound constructions like "the
Lamb of God" — render as `the Lamb | of God`. **Adjective phrases split from their NP head**
when the modifier is free-composition: `le fuafuaga | alofa mutimutivale` → "the plan |
merciful" / `le sauai | leaga | mata'utia` → "the monster | evil | terrible".
  - **EXCEPTION A — idiomatic compound nouns** (single atomic NP, do NOT split): `alofa
    tunoa` → "grace" / `alofa mutimutivale` → "tender mercy" (standing alone) / `alofa mamā`
    → "charity" / `faitaulaga pepelo` → "priestcrafts" / `tagata malosi` → "mighty man" /
    `tagata o taua` → "man of war" / `tagata faautauta` → "prudent man" / `tagata mamalu` →
    "honorable man" / `tagata matua` → "the ancient" / `tagata malolosi` → "mighty men" /
    `tufuga tomai` → "cunning artificer" / `failauga poto` → "eloquent orator" / and fixed
    titles/objects where the modifier is part of the canonical name.
  - **EXCEPTION B — possessive prefix splits**: `lona alofa tunoa` → "his grace" splits as
    `lona | alofa tunoa`; `lona alofa mutimutivale` → `his | tender mercy`.
  - **EXCEPTION C — vocative `e` overrides everything** (see rule 12): `o'u uso pele e`
    stays as one cell "O my beloved brethren".

**4. Definite-singular vs plural** distinguished by `le`: `ona o le mea` → "because of the
thing" (singular); `ona o mea` → "because of things" (plural).

**5. Conjunctions: `ma` is "and"** — its own atomic unit when it starts a clause connector.
`ma faalogo` → "and heard". When `ma` is "with" (accompaniment after a verb), gloss "with".

**6. Verb-list TAM threading.** `sa vaai, ma faalogo, ma tautala` — the `sa` carries
through. Gloss as `saw, | and heard, | and spake`. Don't re-mark `sa` on later verbs.

**7. Verb + directional `atu/mai/ifo/a'e/ane` + anaphoric `ai` stay in the cluster.**
`fetalai mai` → "spake", `ou tautala atu` → "I spake", `na faia ai` → "did". The five
directional/respect particles: `mai` toward speaker; `atu` away; `ifo` downward + formal/
respectful register (deity, elders); `a'e` upward; `ane` sideways/in passing. When `ifo`
appears with sacred beings it carries respectful nuance — keep it in the cluster.
  - **Future TAM `o le a` MUST stay bundled with its verb AND its directional** as one
    atomic 4–5-token cluster. NEVER split `o le a X` from a following directional. E.g.
    `o le a afio mai` → "shall come" / `o le a pa'ū ifo` → "shall fall down".
  - **`mai` is a homonym**: also the preposition **"from"**. If `mai` is followed by a
    noun/proper-name phrase (`mai ia Ierusalema`, `mai Siona`, `mai lea taimi`), it's "from"
    and starts a new PP — NOT part of the prior verb cluster. Treat `mai` as directional
    only when it caps a verb cluster with no NP following.

**8. PP atoms (preposition + NP, 2–4 tokens).** `i le Alii` → "unto the Lord" / `mai le
faatagataotauaina` → "from captivity" / `i o'u luma` → "before me" / `i totonu o tagata
Iutaia` → "among the Jews".

**9. Idiom-style set phrases stay together at natural length.** `o le mea lea` → "wherefore"
/ `e tusa ma` and `e tusa ai ma` → "according to" / `aua faauta` → "for behold" / `faauta` →
"behold" / `ioe` → "yea" / `e pei ona` → "as" / `e uiga i` → "concerning" / `e tatau ona` →
"should/must" / `e ao ina` → "must" / `i ai` → "be" (existential) / `vagana` → "save" /
`talu ai ona` / `ma talu ai ona` → "because/and because" / `ona o` → "because of" / `ona o
le mea lea` → "wherefore" / `se togiola aoao e lē gata` → "infinite atonement".

**10. Hand-curated per-verse specs override the auto-glosser** — but each hand-spec must
also follow rules 1–9. Split "the Lamb of God" per rule 3 even if the seed dict doesn't.

**11. Em-dash baked-in tokens (`X—Y`) — SPLIT THE SOURCE TOKEN.** When a token has an
em-dash with a TAM particle on the trailing side (`Atua—o`, `tovine—o`, `polo-teuvine—e`),
the trailing particle (`e`/`o`/`a`) belongs to the NEXT TAM cluster. **Fix: split the source
token in `bom_books.json`** — replace `X—Y` with two entries `X—` and `Y`. Then all
subsequent tokens shift +1, so update the per-verse spec. Example: `Atua—o` → `Atua—` + `o`,
then `(matata'u i le Atua—, "Fear God") + (o le a ta'uamiotonuina e ia, "he shall justify")`.
NEVER split `o le a` — if em-dash baking traps it, fix the source data.

**12a. Directionals `atu` / `mai` on verbs — DROP "forth" in English gloss.** Do NOT add
"forth" to a verb cluster ending in `atu`/`mai`. `ou te fai atu` → "I say" / `ua fetalai
mai` → "saith" / `o le a faaali mai` → "shall show" / `Aumai` → "Bring". Exception: when the
directional does genuine locative work ("come forth from the dust"). Applied retroactively.

**13. `ina ia` is one atomic unit** = "that / so that / in order to". NEVER split `ina` from
`ia`. `ina ia mafai ona X` → "that X may". Distinct from `ina ua` (temporal "when", also
atomic, also never split): `ina ua Ou manatu` → "when I thought".

**14. The `o` particle is load-bearing — NEVER silence or drop it.** Roles: (a) topic
marker / subject-pronoun introducer: `o a'u` → "I am"/"as for I", `o ia` → "he is",
`o i latou` → "they are"; (b) predicate copula: `o se tagata` → "(is) a man", `o Keriso` →
"is Christ"; (c) genitive/possessive: `le Alii o 'Au` → "the Lord of Hosts". Pattern
`o X o Y`: `o a'u o se tagata` = "I am a man" → `o a'u` "I am" + `o se tagata` "a man".

**15. `mafai ona` cluster — `ona` is bound to `mafai`, never split off.** `e mafai ona` →
"may/can" / `ua mafai ona` → "could" / `o le a mafai ona` → "shall be able to" / `e lē mafai
ona` → "cannot" / `ua lē mafai ona` → "could not" / `o le a lē mafai ona` → "shall not be
able to". Same for `e tatau ona` → "should" and similar bound modal complementizers.

**16. Imperative `Ia/Inā ... ia` envelope (with verb between) is one atomic unit** = "Verb
ye/thou". EVERYTHING between `Ia/Inā` and the closing `ia` belongs to the bundled imperative.
`Inā sisi a'e ia` → "lift ye up" / `Ia outou faalogo mai` → "hearken ye" / `Ia e tago` →
"take thou" / `Ia outou liliu ese` → "turn ye away" / `Ia tatou o a'e` → "let us go up" /
`Ia faia` → "do/make". An agent like `e outou` following the envelope is a separate span.

**12 (vocative). Vocative `e` (post-noun) — bundle as "O X".** A trailing `e` after a noun
phrase is the vocative particle. Bundle the whole vocative NP into one cell: `le Alii e,` →
"O Lord," / `Atua e` → "O God" / `lo'u nuu e,` → "O my people," / `o'u uso pele e,` → "O my
beloved brethren," (rule 3 split suspended for vocatives) / `outou e amioleaga` → `O ye |
wicked` (vocative `outou e` one cell, post-modifier separate). With a leading `E,`
interjection AND trailing `e`, fold the whole envelope: `E, le aiga e` → "O house".

---

## Pipeline

Seed phrases in `extract_phrases.py:USER_SEED_PHRASES` win against extracted ones. Run
order: `extract_phrases.py` → `build_phrase_overrides.py` → per-verse
`build_overrides_<book><n>.py`. Each per-verse script validates alignment (no gaps, spec
covers exactly the source-token count) before writing to `bom_overrides.json`.
