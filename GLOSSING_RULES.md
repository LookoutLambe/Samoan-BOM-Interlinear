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

## 17. `na` is the past-tense marker, and position decides its other jobs

`na` sits in three tables — the TAM (past), the bound pronoun (`ua na fai`
"he did", `na te fai` "he does"), and the curation's relative readings
which/who/that — and left to the readings a clause-initial `Na alu` came out
"that": 410 main-clause past markers in the Bible glossed as relatives, and
`Na faia e le Atua` firing for nothing (user, 2026-09-05: *"the past tense
particle... na faia is not firing"*). The rule, in `samoan_grammar.
contextual_reading`:

- clause-initial, or after a conjunction / clause linker / the fronted
  subject pronoun (`ma`, `ona`, `a`, `ae`, `aua`, `ina`, `lea`, `ia`, `foi`,
  `afai`, `peitai`): the past marker — silent (`·`), the tense rides on the
  verb;
- after a TAM or `te`: the pronoun "he";
- before `te`: the inventory's `na te` frame decides;
- after a noun: it may open a relative clause, where the curation's
  which/who/that still stand.

And the verb it marks says its word: under an explicit tense marker, a verb
with no verse-confirmed reading takes the curation's plurality reading in
that tense (`na faia` → "made" where the KJV has "created"). The word is the
curation's, the tense is the marker's; nothing is invented. Generator:
`tensed-plurality` in `gloss_corpus.py` (formerly generate_overrides_dc_pgp.py).

## 18. The tool learns the Bible's words, and the frames the Book of Mormon never showed

User, 2026-09-05: *"these are real Samoan words in genesis that are not in the
dictionary side.... you're to be proactive to add them, make the tool work for
you not you for the tool"*; and on `ona malamalama ai lea`: *"it's a grouping
that means and there was light.... ona you're not following grammar at all...
neither with ai lea"*; *"po means night, pouliuli dark, standard typical Samoan
words"*.

- **A learned lexicon** (`scripts/learn_bible_lexicon.py` →
  `Resources/samoan_dictionary_bible.json`): a Samoan word's English is the
  content word that keeps turning up in its verses far beyond chance, over the
  42,000 aligned verses (O le Tusi Paia beside the KJV, the Book of Mormon
  volumes beside their English); inflections stem-merged, thin evidence held
  to a stricter bar; names learn too (Paulo → Paul). 95% agreement with the
  hand-curated lexicon. Merged after Pratt and EALD, so a dictionary sense is
  tried first. Words too rare to learn go by hand into `VOCABULARY`
  (nunumi = without form).
- **Every word reaches the dictionaries.** A token nothing frames stands as
  its own unit; a unit of particles round one content word is looked up by
  that word; in the Bible a unanimous curated reading the verse does not carry
  is provisional and yields to a verse-confirmed sense, else stands (gaogao
  keeps "empty" beside "void"); a strongly attested word says its plurality
  reading rather than nothing; a registered idiom outranks memory (`i le ua
  faapea lava` = "and it was so"); one leftover Samoan word pairs with one
  leftover English word, and in the Bible n leftovers pair by position.
- **Frames.** `ona VERB (ai) lea` is the sequential "then / and" (the
  curation: then 75, and 13); `ai lea` closes it silently and may not be
  swallowed by the verb's unit. Clause-initial `Ia` is the optative "let".
  `po` after a determiner is the noun night. A unit never crosses a sentence
  stop (`po. O le` is not `po o` "or"). In the Bible a particle with a frame
  reading opens its own unit even where the curation recorded a longer one;
  in the Book of Mormon the curated unit stands whole (splitting cost 0.3 F1).
- The Book of Mormon score against its curation is unchanged through all of
  this (F1 85.0 all / 86.1 content); the Bible runs at 94.2% tokens carrying
  text.

## 19. `ma` is *and / with* — never *from*

User, 2026-09-05: *"ma can also mean embarrassed... but mai is from"* and
*"ma is with and not from"*. The alternatives table gave `ma` the reading
*from* whenever the English had one nearby (the divide constructions in
Genesis 1, 47 Bible sites). `ma` reads **and** or **with**; **from** is
always `mai`. In *va aʻi X ma Y* the English "divide X from Y" is rendered by
the construction, and `ma` still glosses *and*.

## 20. The text is the 1887 edition; the later revision is the fallback

User, 2026-09-05: *"you didn't use the Samoan in the internet archives... Lokou
logos... it has to match it."* The Bible the app carries is the 1887 BFBS printing
(archive.org `oletusipaiaole00lond`, the PDF on the Desktop), segmented from the
PDF's text layer by `scripts/segment_1887_pdf.py` (verse numerals are read from
the page margins). The later revision (`Upu`, `le ALII`) stands in only where an
1887 verse is missing or fails the KJV-length check, and the index lists every
such verse under `fallback`. `Lokou` is the Word (Christ).

## 21. Simple sentences: the marker's phrase carries the copula

User, 2026-09-05, on John 1: *"Sa i le amataga - in the beginning was... its pretty
simple"*; *"sa i le Atua le Lokou ... the word was with God"*; *"O le Atua foi le
Lokou - God is the word"*; *"Sa ia te ia le ola - in him was life"*; *"o le
malamalama lea - which is the light"*; *"Na sau o ia - he came"*; *"ina ia
molimau - to witness"*; *"E le'o le malamalama ia - he was not the light"*;
*"i lea lava malamalama - of that light"*; *"lona igoa - his name"*; *"o ia - he"*.
Read in Samoan order, no smoothing. `simple_sentences()` in the generator (Bible
only) does this:

- **TAM + phrase + subject** (`Sa i le amataga | le Lokou`): the phrase says its
  English with the copula -- placed where the KJV clause places it ("in the
  beginning was", "was with God") -- and the subject says its own. The marker is
  NOT silent: its "was" is in the phrase's gloss; the dot only means the word
  belongs to the unit whose gloss follows. The English clause supplies the
  copula's tense, the preposition the memory dropped ("with God", "in him"), and
  the "and" that opens it.
- **`o` + noun (+ foi) + noun**: the equative, "God is" | "also" | "the Word".
- **`E le o` + noun + pronoun**: the negative equative, "he was not the light".
- **`i/o lea (lava)` + noun**: "of that light" -- preposition from the English.
- **verb + `o ia` / `o i latou`**: "he came" -- the pronoun unit takes the verb,
  nominative first; a copular predicate keeps its subject apart ("was in the
  world" | "he").
- **`ina ia` + verb**: purposive, "to witness".
- **possessive + noun** (`lona igoa`): "his name", whatever memory offered.
- a trailing `foi` says "also" on its own; a clause-opening `o le X` is the noun,
  not "of X"; every `i`-phrase takes the English's preposition.
- `o ia lava` = "he also" (Bible-only vocabulary; the BOM curation has "himself").

### 21b. More from John 1 (2026-09-05, same session)

- `a e` is the printed spacing of aʻe, "but" (`a e lei talia` "but ... not received").
- `e lei VERB` folds into the verb: "not made", "not received" -- as the user groups it.
- The ergative agent after a verb is its own unit and says "by": `e ia` "by him",
  `e ona lava tagata` "by his own people"; a remembered span may not swallow it.
- When an agent phrase follows in the clause, the `o ia` after the verb is the
  OBJECT ("received him not"), so the verb + subject inversion stands down.
- `ina ia talitonu i ai` is ONE unit: the anaphoric `i ai` folds into the purposive
  verb; the explicit `ia te ia` later says "in him".
- Registered terms take the marker's tense too (`ua maliu mai` -> came).
- A rule-derived past needs the verse to show the verb CONJUGATED (-eth / -s); the
  bare word proves nothing ("grace", "priest" are nouns).
- The simple-sentence rule never fires on the ergative `e i tatou` ("by us") or
  after a verb in the same clause.

### 21c. The order is threefold, and the pass adapts per clause

User, 2026-09-05: *"its mixed the grammar its three fold... there is no set so it
needs to adapt... the language can be spoke like english, like TAM, or backwards."*
Every clause is read for its OWN shape; nothing assumes one order:

| shape | Samoan | read as |
|---|---|---|
| English-like (subject first) | `O ia lava \| sa i le Atua \| i le amataga` | he also \| was with God \| in the beginning |
| marker-first (TAM leads) | `Na sau o ia`; `Sa i le amataga \| le Lokou` | he came; in the beginning was \| the Word |
| inverted / predicate-first | `O le Atua foi \| le Lokou`; `E le o le malamalama ia` | God is \| also \| the Word; he was not the light |

The shape is decided from where the marker and the subject stand relative to the
predicate; the KJV clause decides where the copula or verb sits inside the unit
("in the beginning WAS" after the phrase, "WAS with God" before it). Units keep
Samoan order and are never re-sorted into English.

Also this round: the Bible keeps the KJV's forms -- no modernising of its English
or its glosses ("lighteth", "cometh"); a possessive before a verb is the gerund
(`i lona maliu mai` "in his coming"); the quantifier `uma` surfaces as every / all as
the verse has it (`tagata uma lava` "every man"); a carried preposition brings the
English's article ("of the light").

### 21d. Grammar, not patches (2026-09-05, user: "because you're not teaching the tool GRAMMAR!")

Each of these is a rule about the language, placed where the tool decides that
kind of thing; none names a verse.

- **Fused directionals** (`morph_gloss`): a verb and its directional particle fuse
  with the verb's final vowel elided -- `ave` + `atu` = `avatu` (give), `au` +
  `mai` = `aumai` (bring). The morphology restores the vowel and looks the verb up.
- **The ergative agent** is a noun phrase: `e le pouliuli` "by the darkness", `e
  ia` "by him"; `e` says "by" whatever the memory dropped, and the English tense
  test has no say over a noun phrase.
- **Tense of the clause**: the nearest marker WITH a tense; `ia` (optative) and
  `e` (general / ergative) are passed over (`na ia avatu` -> gave).
- **A noun is not a verb**: an English word in -s after a determiner or a
  preposition, or ending in -ss / -us / -is / -ness / -ous, carries no tense
  ("the darkness", "in darkness", "his witness"); the tense step never inflects a
  word after a determiner or a preposition ("the light", never "the lit").
- **Subject inversion only for intransitives**: `Na sau o ia` "he came", but with a
  transitive verb the absolutive `o ia` is the object -- `e na talia o ia`
  "received him".
- **After `e lei` the word is a verb**, and the negative is past: a bare form takes
  the past even where the KJV chose another word ("not received" beside
  "comprehended it not").

### 21e. Article and number (user, 2026-09-05)

- `le` is the definite singular and says "the" in every unit that carries it
  (`i le malamalama` "of THE light"); `se` is "a". The negator `le` (`e le o`) is
  not the article.
- No determiner is plural: `o le tagata` the man, `o se tagata` a man, `ni tagata`
  some men, bare `tagata` men. A bare noun unit takes the plural the verse has
  (man -> men) or a regular one; mass nouns and names stay.
- `ia` right after a tense marker is the pronoun: `na ia avatu` "he gave".
- Morphology only for forms the lexicons do not hold at all: `manuia` is a word
  (blessing), not manu + ia.
- Reference the user pointed to: *Samoan for Missionaries* (Scott C. Dunn, 1983,
  BYU thesis) -- for the particle and TAM tables; read it from the Desktop when
  the user puts it there.

## 22. The grammar of the language (from Dunn, *Samoan for Missionaries*, 1983)

User, 2026-09-05: *"you werent teaching the full grammar rules of the language to
the tool"*; *"its the grammar rules you need from it so its not copywrite its
facts"*; *"the grammar rule book should also explain redundancy words /
multiplying"*; *"this tool should not be just dc_pgp but the entire corpus even
the BOM"*; *"the tool should include all 5... OT, NT, BOM, DC, PGP"*.

The tool is `scripts/gloss_corpus.py` (the old name `generate_overrides_dc_pgp.py`
is a shim that runs it). One grammar, five volumes: the default run glosses the
Book of Mormon, D&C and Pearl of Great Price; `--bible` the Old and New
Testaments; `--all` everything. The sentence pass (`simple_sentences`) runs on
every volume; the curated units are consulted first and stand where no rule
speaks. `SS_TRACE="<words of the verse>"` prints the gloss line after each stage
of the sentence pass. The facts below are Dunn's; the code location follows each.

### 22a. Tense-aspect-mood markers (`TAM`, `TENSE_OF_TAM`, `TAM_SEMANTICS` in samoan_grammar.py)

| marker | Dunn | English of the verb |
|---|---|---|
| `e` | non-past: habitual, permanent, future | present ("is", "-eth") |
| `te` | `e` after a clitic doer (`ou te`, `latou te`) | present |
| `ua` | determinate present, "has become", the state reached | perfect / "is (now)" |
| `o loo` | indeterminate present, progressive | "is …ing", the copula of a locative |
| `sa` | indeterminate past | past |
| `na` | determinate past | past |
| `o le a` | future | "shall" |
| `a` (clause-initial), `pe a` (mid) | future / "when" | the clause takes no other marker |
| `ia` | insistent imperative, optative | "let", or the bare verb |
| `sei` / `seia` | deferential imperative; "until" | "let"; "until" |
| `ina ia` | purposive | "to VERB" |

After `ina ia`, `ia`, `sei`, `ne’i`, `aua` the verb is bare (`BARE_AFTER`). A
unit's own marker outranks the one before it (`e | na talia` is past). The
marker is not glossed; its tense is written on the verb in the verse's own form.

### 22b. Word order and the two kinds of doer

Neutral order: MARKER – PREDICATE – DOER – DONE-TO – PREPOSITIONAL PHRASES. The
language then speaks three ways (rule 21c) and every clause is read for its own
shape.

- **Descriptive (clitic) doers** stand between the marker and the verb and take
  no `e`: `sa ia faitauina le tusi` "he read the book", `ua latou o mai` "they
  have come". Table `DESCRIPTIVE_PRONOUNS`; every `sa / na / ua / ia / o le a` +
  pronoun is a generated frame in `PRONOUNS` (`sa ou` = I, `o le a latou` = they
  shall). Before this the doer vanished into the verb.
- **Emphatic doers** (`o ia`, `i latou`, `a’u`, `oe`) stand where a noun would,
  after the verb; with a transitive verb they take the ergative `e` ("by").
  After a directional the `o` is dropped in practice: `ua silasila atu ia`
  "he looked" (`contextual_reading`, `ia` after a verb).
- **Doer omission**: the 3sg is dropped once introduced; a possessive implies
  the doer (`ua le iloa la’u peni` "I lost my pen"); a transitive verb needs no
  doer at all when it is unknown, unimportant or obvious — which is where the
  KJV has a passive: `ua saunia le meaai` "the food is prepared", `na tuuina mai
  e Mose le tulafono` "the law was given by Moses". The sentence pass writes
  the copula the verse sets beside the word ("were made", "was given").

### 22c. Nominal sentences (rule 21, `simple_sentences`)

Presentative `O NP` = "(it) is NP"; equative `O NP-pred NP-subj` = "subject is
predicate", predicate first and tenseless — "God is | also | the Word", "John is
| his name"; `O ia lenei` "he was | this". Stative predicate `E poto le tama`
"is smart | the boy": the copula from the English. Existential `E i ai se X`
"there is an X", `sa i ai` "there was", `e leai se X` "there is no X"
(`EXISTENTIAL`). Negative nominal `E le o NP` "is not NP" (frame `e le o` =
"not"; the pass supplies the copula: "he was not that light").

### 22d. Articles and number (rule 21e)

`le` specific singular "the"; `se` non-specific "a"; `ni` non-specific plural
"some"; **no article = plural** (`o tagata` "men"). Adjectives FOLLOW the noun
and agree in number by reduplication (22k). Numbers are predicates with `e`
(`e lua au tusi` "I have two books").

### 22e. Demonstratives (`DEMONSTRATIVES`, `contextual_reading`)

lenei / nei "this / these"; lea / ia "this, that / these, those"; lena / na
"that / those"; lela / la "that yonder"; the regional lenaʻe, lele, lale, nae.
The plurals follow the noun, which is how `na` "those" is told from the past
marker: after a noun with nothing verbal following it is "those"; with a verb
following it opens a relative clause ("the man who came"). `o lea` before a
noun is "that", before a marker "therefore".

### 22f. Prepositions

`i` before common nouns and places; `ia` before personal names and plural
pronouns; `ia te` before singular pronouns. So `ia Iesu` is a preposition,
never "him" (`FRAME_READINGS[('ia', 'NAME')]`). `i` = to / in / into
(direction) and at / on / in (location); the verse chooses. **Accompaniment
is `ma`, instrument is `i`**: `ma le teine` "with the girl", `i le penitala`
"with a pencil". `mo` / `ma` "for" (benefit), `i` "for" (duration).

**The object-marking `i`** (`OBJECT_I_VERBS`): alofa, vaai, silasila, faatali,
fesoasoani, manao, aoao, tali, valaau, fesili, faalogo, talitonu, fiafia,
inoino, musu, fefe, iloa … are intransitive in Samoan where their English is
transitive, and their object takes `i`. That `i` says no preposition when the
English has a plain object ("loved the world", "taught them") and keeps one
when the English has one ("believe ON his name").

**Predicate phrases as prepositions** (`COMPLEX_PREPOSITIONS`): e aunoa ma
"without", e uiga i "about", e tusa ma "according to", e faasaga i "facing /
against", e faafeagai ma "opposite", e latalata i "near", e sosoo ane i
"adjoining", e pito ane i "next to", e tupito atu i "furthest from".

### 22g. Possession (`POSSESSIVES`, the possessive rules of the pass)

`o`-class for what is not controlled (parts, relations, dwelling); `a`-class
for what is (food, tools, behaviour, speech). Both are "his / her / their".
A possessive before a verb makes it a noun (`lona maliu mai` "his coming");
before an adjective the -ness noun (`lona tumu` "his fulness"). A possessive
and its noun are one phrase even when the memory split them ("of his
fulness"). `avea ma` "become", `fai ma` "act as": the `ma` marks the
complement.

### 22h. Directionals (`DIRECTIONALS`, `morph_gloss`)

`atu` away from the speaker, `mai` toward, `ane` along / aside, `a’e` up,
`ifo` down, `ese` away. They follow the verb and English carries them in the
verb ("came", "gave"). A verb and its directional fuse with the vowel elided
(`ave` + `atu` = `avatu`, `au` + `mai` = `aumai`), and a perfective suffix then
follows the directional (`aveesea`). `mai` before a noun phrase is the
preposition "from"; after a verb with nothing following, or before the agent
`e` (`auina mai e le Atua` "sent by God"), it is the directional.

### 22i. The perfective suffixes

`-ina`, `-a`, `-ia`, `-gia`, `-mia`, `-sia` make a verb transitive / perfective:
they appear in negatives (`sa le faia`), with clitic doers (`sa ia faitauina`),
and shift sense (`tali` answer → `talia` accept; `vaai` look → `vaaia` see).
Verbs of motion and statives do not take them. `-ina` with no doer is the
passive the KJV writes (22b).

### 22j. Negation (`NEGATION`, `NEG_UNITS`, the fold in the pass)

`e le` general negative (also of adjectives: `e le lelei` "is not good");
`e lei` / `te lei` past ("not", the traditional "not yet" only where the verse
says yet); `leai` = `e le i ai`, "there is not / no"; `e le o` before a
nominal or progressive predicate; imperatives `aua`, `aua nei`, `soia`; `ne’i`
"lest". The negative folds into its verb: `e lei talia` "not received", `te
le oti` "not die". A remembered span may not begin on the negator (`lua te |
le oti lava`).

### 22k. Redundancy: reduplication ("multiplying", the user's word)

Two doublings, two meanings, one root — and the tool never collapses a
doubled form it already knows:

| pattern | example | meaning |
|---|---|---|
| one syllable doubled | nofo → nonofo, moe → momoe, galue → galulue, poto → popoto, malosi → malolosi, umi → uumi | PLURAL — the verb or adjective agrees with a plural doer or noun |
| the whole root doubled | mata "eye, see" → matamata "look at, behold"; savali → savalivali "walk about"; fai → faifai "keep doing"; tagi → tagitagi | repeated, continued or intensified action; often a distinct word |

The user's pair: **malu** "shelter, shade" → **mamalu** "dignity, glory" (syllable
doubling) and **mālumalu** "temple, the sheltered place" (root doubling). Three
words. `_dereduplicate` in gloss_corpus.py strips a doubled root or syllable
only for a form no lexicon holds, so the known words stay themselves; a
plural form glosses as its base (the number rides on the subject).

### 22l. Verbs as nouns (`morph_gloss` frame "noun", the article and possessive rules)

The suffix `-ga` (amata → amataga "beginning", faaali → faaaliga
"revelation", galue → galuega "work"; some lengthen the first vowel: taalo →
taaloga "game"; a few take `-aga`: nofo → nofoaga "dwelling"). And a verb is
a noun without any change under an article or possessive: `lana sau` "his
coming", `le faalogo` "the hearing", `o le mu o le fale` "the burning of the
house". The pass writes the verse's gerund or -ness noun when it has one.

### 22m. Numerals and their prefixes (`NUMERALS`, `ORDINALS`, `numeral_derived`)

`lona` + number = ordinal (`lona lua` second; "first" is `muamua`); `faa-` +
number = times (`faalua` twice); `toa-` counts people (`toalua` two persons,
`toatele` many, `toaitiiti` few); `tai-` = each (`taitasi` each one,
`taisefulu` ten each). The derivations are dictionary senses, written when the
verse carries them — `e toatasi` stays the curated "only".

### 22n. Relative clauses and the emphatic antecedent (`DEMONSTRATIVES`, rule 21)

Samoan omits the relative word: `le tagata na sau` "the man who came", `le aso
na e sau ai` "the day thou camest". When the omitted phrase is one of place,
instrument, time or reason, `ai` follows the predicate; of direction, `i ai`
(22o). A whole sentence can be a relative clause for "whose" and "with whom"
(`le teine ua leaga lana uati` "the girl whose watch is broken"). The emphatic
antecedents `o le`, `o se`, `o e` before a relative clause are "he who",
"anyone who", "those who" (`o le na`, `o le ua`, `o le e`, `o se e`, `o e
ua` …); `o le` before a bare verb is "he that" (`O le mulimuli mai` "he that
cometh after").

### 22o. `ai` and `i ai`, the pro-phrases

`ai` stands for a phrase of location or instrument already named ("in it, with
it, there"); `i ai` for one of direction ("to it, to him, about it"). Both
follow the predicate. Where the KJV has a compound the particle says it
(therein, thereby, wherein, whereby …); where the KJV names the object after
the verb it says that ("touch it"); otherwise the English carries it inside
the verb and the particle folds into the verb's unit.

### 22p. Conjunctions (`SUBORDINATORS`, `COORDINATORS`, `DISCOURSE`)

| sense | Samoan |
|---|---|
| and, with | ma; atoa ma "together with"; atoa foi ma "as well as"; aemaise "especially" (before a noun phrase only) |
| but | a (before o / ua / ia / a negator), ae (before anything) |
| however | peitai, ae peitai, peitai ane |
| then | ona … lea; ona … ai lea when the first clause is the reason |
| if | afai (sentence-initial), pe afai (mid); ana / pe ana counterfactual |
| when | a / pe a (future); ina ua (past); a o / ao "while" |
| before | o lei, ae lei ("while not yet"), o lei oo i + noun |
| after | ina ua uma, a uma, pe a uma ("when finished") |
| because | aua, leaga, ona ua / ona sa / ona e; ona o + noun "because of"; talu ai "on account of" |
| since | talu, talu ona, talu mai |
| until | seia, seia oo i / ina; sei "wait until" |
| unless / except | seiloga, vagana (ai) |
| although | e ui ina, e ui lava ina; ae ui i lea "nevertheless" |
| like, as | e pei (o), faapei (o), e pei ona + clause |
| in order to, lest | ina ia; ne’i |
| therefore | o lea, o le mea lea |

### 22q. Phrases are constituents

Preposition + determiner + noun, and determiner + noun, are one unit even where
the memory held no span for them (`i | le | motu` → `i le motu` "the
multitudes"); the phrase rules (the English's preposition, the object-marking
`i`, the article) read the joined unit.

### 22r. What it measured

`measure_pass.py` scores the generated Book of Mormon against the curated units.
Before the grammar ran on the BOM it read ALL F1 85.0 / content 86.1; with Dunn's
rules on every volume it reads 84.9 / 85.9, and the differences that remain are
the grammar's own (clitic doers "I shall", "they"; agents "by the Lord"; "also";
"it came to pass"; `le` = "the"; "when", "after", "none"). The user's ruling
(2026-09-05): *"forget my rules use the samoanformissionaries as source here"* —
the score is a diagnostic now, not a gate. Every misfire found on the way was
fixed as a rule about the language, never a verse: `o le mea lea` is one word,
`ona` before a marker is "because" not "his", `e le vaaia` is the negative not an
agent, a frame never runs across a comma, `i latou` as a plain object takes no
preposition, a curated imperative's capital is lowercased mid-sentence.

### 22s. The Bible pipeline, in order

`segment_1887_pdf.py --all` (the PDF on the Desktop → `corpus/tusi_paia/tusi_paia_verses_1887.json`;
`--book` never writes the file) → `build_tusi_paia_dual.py` (tokens, fallbacks, hand layer,
text fixes → `corpus/tusi_paia/dual/`, THE TOKEN MASTER) → `gloss_corpus.py --bible` (reads
the dual tokens, syncs the dual index and English into Resources, writes the glossed
`Resources/book_<id>.json`) → `build_web_data.py` → the iOS build. The glosser used to read
its own last output in Resources and overwrite the dual files, so a rebuilt text never
reached the app; it reads the dual build now.
