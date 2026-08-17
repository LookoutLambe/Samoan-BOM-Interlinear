#!/usr/bin/env python3
"""
Build `bom_headings.json` — the interlinear chapter summaries/headings that sit
at the top of each chapter, mirroring the verse override pipeline.

Each entry is keyed "bookId|chapter" and carries three registers:
  - en:    the verbatim English chapter heading (from churchofjesuschrist.org)
  - sm:    the verbatim Samoan chapter heading
  - words: the interlinear gloss — a [{sm, en}] array using the same `·`
           continuation-marker convention as bom_overrides.json (see
           Views/WordUnitView.swift `groupIdiomSpans`), curated per GLOSSING_RULES.md

`CELLS` holds hand-curated (samoan_phrase, english_gloss) pairs. The builder
tokenizes each Samoan phrase on spaces; the final token carries the gloss and
the preceding tokens are marked "·". It then asserts that the reconstructed
token stream equals the em-dash-split source text, so no word can be dropped,
duplicated, or misaligned.

Run:  python3 scripts/build_headings.py
Out:  O le Tusi a Mamona Interlinear/Resources/bom_headings.json
"""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "O le Tusi a Mamona Interlinear", "Resources", "bom_headings.json")

EMDASH = "—"  # — (clause separator; split for tokenizing)

# ---------------------------------------------------------------------------
# Hand-curated headings.  Add chapters here in batches; the builder validates
# every one against its source Samoan before writing.
#
# Shape:  "bookId|chapter": { "en": ..., "sm": ..., "cells": [(sm, en), ...] }
# ---------------------------------------------------------------------------

HEADINGS: dict[str, dict] = {
    "1nephi|1": {
        "en": "Nephi begins the record of his people—Lehi sees in vision a "
              "pillar of fire and reads from a book of prophecy—He praises "
              "God, foretells the coming of the Messiah, and prophesies the "
              "destruction of Jerusalem—He is persecuted by the Jews. "
              "About 600 B.C.",
        "sm": "Ua amata e Nifae le talafaamaumau o lona nuu—Ua vaai Liae i se "
              "afi faaniutu i se faaaliga vaaia ma ua faitau mai i se tusi o "
              "valoaga—Ua viia e ia le Atua, valoia le afio mai o le Mesia, "
              "ma valoia le faafanoga o Ierusalema—Ua sauaina o ia e tagata "
              "Iutaia. E tusa o le 600 T.L.M.",
        "cells": [
            ("Ua amata", "begins"),
            ("e Nifae", "Nephi"),
            ("le talafaamaumau", "the record"),
            ("o lona nuu—", "of his people—"),
            ("Ua vaai", "sees"),
            ("Liae", "Lehi"),
            ("i se afi faaniutu", "a pillar of fire"),
            ("i se faaaliga vaaia", "in a vision"),
            ("ma ua faitau", "and reads"),
            ("mai", "from"),
            ("i se tusi", "a book"),
            ("o valoaga—", "of prophecy—"),
            ("Ua viia e ia", "he praises"),
            ("le Atua,", "God,"),
            ("valoia", "foretells"),
            ("le afio mai", "the coming"),
            ("o le Mesia,", "of the Messiah,"),
            ("ma valoia", "and prophesies"),
            ("le faafanoga", "the destruction"),
            ("o Ierusalema—", "of Jerusalem—"),
            ("Ua sauaina o ia", "he is persecuted"),
            ("e tagata Iutaia.", "by the Jews."),
            ("E tusa o le", "about"),
            ("600", "600"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|2": {
        "en": "Lehi takes his family into the wilderness by the Red Sea—They "
              "leave their property—Lehi offers a sacrifice to the Lord and "
              "teaches his sons to keep the commandments—Laman and Lemuel "
              "murmur against their father—Nephi is obedient and prays in "
              "faith; the Lord speaks to him, and he is chosen to rule over his "
              "brethren. About 600 B.C.",
        "sm": "Ua ave e Liae lona aiga i le vao i tafatafa o le Sami "
              "Ulaula—Ua latou tuua a latou meatotino—Ua osi e Liae se "
              "taulaga i le Alii ma aoao ona atalii ia tausi i "
              "poloaiga—Ua muimui Lamana ma Lemuelu i lo laua "
              "tamā—Ua usiusitai Nifae ma tatalo i le faatuatua; ua "
              "fetalai mai le Alii ia te ia, ma ua filifilia o ia e pule i ona "
              "uso. E tusa o le 600 T.L.M.",
        "cells": [
            ("Ua ave", "takes"),
            ("e Liae", "Lehi"),
            ("lona aiga", "his family"),
            ("i le vao", "into the wilderness"),
            ("i tafatafa o", "beside"),
            ("le Sami Ulaula—", "the Red Sea—"),
            ("Ua latou tuua", "they leave"),
            ("a latou meatotino—", "their property—"),
            ("Ua osi", "offers"),
            ("e Liae", "Lehi"),
            ("se taulaga", "a sacrifice"),
            ("i le Alii", "to the Lord"),
            ("ma aoao", "and teaches"),
            ("ona atalii", "his sons"),
            ("ia tausi", "to keep"),
            ("i poloaiga—", "the commandments—"),
            ("Ua muimui", "murmur"),
            ("Lamana", "Laman"),
            ("ma Lemuelu", "and Lemuel"),
            ("i lo laua tamā—", "against their father—"),
            ("Ua usiusitai", "is obedient"),
            ("Nifae", "Nephi"),
            ("ma tatalo", "and prays"),
            ("i le faatuatua;", "in faith;"),
            ("ua fetalai mai", "speaks"),
            ("le Alii", "the Lord"),
            ("ia te ia,", "to him,"),
            ("ma ua filifilia o ia", "and he is chosen"),
            ("e pule", "to rule"),
            ("i ona uso.", "over his brethren."),
            ("E tusa o le", "about"),
            ("600", "600"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|3": {
        "en": "Lehi's sons return to Jerusalem to obtain the plates of "
              "brass—Laban refuses to give the plates up—Nephi exhorts "
              "and encourages his brethren—Laban steals their property and "
              "attempts to slay them—Laman and Lemuel smite Nephi and Sam "
              "and are reproved by an angel. About 600–592 B.C.",
        "sm": "Ua foi atu atalii o Liae i Ierusalema ina ia maua mai papatusi "
              "apamemea—Ua musu Lapana e tuu mai papatusi—Ua apoapoai ma "
              "faamalosi'au atu Nifae i ona uso—Ua fao e Lapana a latou "
              "meatotino ma taumafai e fasioti i latou—Ua fasi e Lamana ma "
              "Lemuelu Nifae ma Sama, ma ua a'oa'i i laua e se agelu. E tusa o "
              "le 600–592 T.L.M.",
        "cells": [
            ("Ua foi atu", "return"),
            ("atalii o Liae", "Lehi's sons"),
            ("i Ierusalema", "to Jerusalem"),
            ("ina ia", "to"),
            ("maua mai", "obtain"),
            ("papatusi apamemea—", "the plates of brass—"),
            ("Ua musu", "refuses"),
            ("Lapana", "Laban"),
            ("e tuu mai", "to give up"),
            ("papatusi—", "the plates—"),
            ("Ua apoapoai", "exhorts"),
            ("ma faamalosi'au atu", "and encourages"),
            ("Nifae", "Nephi"),
            ("i ona uso—", "his brethren—"),
            ("Ua fao", "steals"),
            ("e Lapana", "Laban"),
            ("a latou meatotino", "their property"),
            ("ma taumafai", "and attempts"),
            ("e fasioti", "to slay"),
            ("i latou—", "them—"),
            ("Ua fasi", "smite"),
            ("e Lamana", "Laman"),
            ("ma Lemuelu", "and Lemuel"),
            ("Nifae", "Nephi"),
            ("ma Sama,", "and Sam,"),
            ("ma ua a'oa'i", "and are reproved"),
            ("i laua", "them"),
            ("e se agelu.", "by an angel."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|4": {
        "en": "Nephi slays Laban at the Lord's command and then secures the "
              "plates of brass by stratagem—Zoram chooses to join Lehi's "
              "family in the wilderness. About 600–592 B.C.",
        "sm": "Ua fasioti Lapana e Nifae i le poloaiga a le Alii ma maua ai e "
              "ia papatusi apamemea i se togafiti—Ua filifili Sorama e faatasi "
              "atu ma le aiga o Liae i le vao. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua fasioti", "slays"),
            ("Lapana", "Laban"),
            ("e Nifae", "Nephi"),
            ("i le poloaiga", "at the command"),
            ("a le Alii", "of the Lord"),
            ("ma maua ai e ia", "and he secures"),
            ("papatusi apamemea", "the plates of brass"),
            ("i se togafiti—", "by stratagem—"),
            ("Ua filifili", "chooses"),
            ("Sorama", "Zoram"),
            ("e faatasi atu", "to join"),
            ("ma le aiga o Liae", "with Lehi's family"),
            ("i le vao.", "in the wilderness."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|5": {
        "en": "Sariah complains against Lehi—Both rejoice over the return of "
              "their sons—They offer sacrifices—The plates of brass contain "
              "writings of Moses and the prophets—The plates identify Lehi as "
              "a descendant of Joseph—Lehi prophesies concerning his seed and "
              "the preservation of the plates. About 600–592 B.C.",
        "sm": "Ua muimui Sarai ia Liae—Ua fiafia i laua uma i le foi mai o o "
              "laua atalii—Ua laua osia ni taulaga—Ua i ai i papatusi apamemea "
              "tusitusiga a Mose ma le au perofeta—Ua faailoa mai i papatusi o "
              "Liae o se e tupuga mai ia Iosefa—Ua vavalo Liae e uiga i ana "
              "fanau ma le faasaoina o papatusi. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua muimui", "complains"),
            ("Sarai", "Sariah"),
            ("ia Liae—", "against Lehi—"),
            ("Ua fiafia", "rejoice"),
            ("i laua uma", "both"),
            ("i le foi mai", "over the return"),
            ("o o laua atalii—", "of their sons—"),
            ("Ua laua osia", "they offer"),
            ("ni taulaga—", "sacrifices—"),
            ("Ua i ai", "contain"),
            ("i papatusi apamemea", "in the plates of brass"),
            ("tusitusiga", "writings"),
            ("a Mose", "of Moses"),
            ("ma le au perofeta—", "and the prophets—"),
            ("Ua faailoa mai", "identify"),
            ("i papatusi", "the plates"),
            ("o Liae", "Lehi"),
            ("o se e tupuga mai", "as a descendant"),
            ("ia Iosefa—", "of Joseph—"),
            ("Ua vavalo", "prophesies"),
            ("Liae", "Lehi"),
            ("e uiga i", "concerning"),
            ("ana fanau", "his seed"),
            ("ma le faasaoina", "and the preservation"),
            ("o papatusi.", "of the plates."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|6": {
        "en": "Nephi writes of the things of God—Nephi's purpose is to "
              "persuade men to come unto the God of Abraham and be saved. "
              "About 600–592 B.C.",
        "sm": "Ua tusi e Nifae mea a le Atua—O le faamoemoe o Nifae o le "
              "faatauanau atu i tagata ia o mai i le Atua o Aperaamo ma "
              "faaolaina ai. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua tusi", "writes"),
            ("e Nifae", "Nephi"),
            ("mea a le Atua—", "the things of God—"),
            ("O le faamoemoe o Nifae", "Nephi's purpose"),
            ("o le faatauanau atu", "is to persuade"),
            ("i tagata", "men"),
            ("ia o mai", "to come"),
            ("i le Atua o Aperaamo", "unto the God of Abraham"),
            ("ma faaolaina ai.", "and be saved."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|7": {
        "en": "Lehi's sons return to Jerusalem and invite Ishmael and his "
              "household to join them in their journey—Laman and others "
              "rebel—Nephi exhorts his brethren to have faith in the "
              "Lord—They bind him with cords and plan his destruction—He is "
              "freed by the power of faith—His brethren ask forgiveness—Lehi "
              "and his company offer sacrifice and burnt offerings. "
              "About 600–592 B.C.",
        "sm": "Ua toe foi atu atalii o Liae i Ierusalema ma valaaulia Isamaeli "
              "ma lona auaiga ia latou auai faatasi ma i latou i la latou "
              "malaga—Ua fouvale Lamana ma isi—Ua apoapoai atu Nifae i ona uso "
              "ia faatuatua i le Alii—Ua latou saisai o ia i maea ma fuafua e "
              "faaumatia o ia—Ua tatalaina o ia i le mana o le faatuatua—Ua "
              "talosaga ona uso mo se faamagaloga—Ua osi e Liae ma lana "
              "aumalaga taulaga ma taulaga mu. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua toe foi atu", "return"),
            ("atalii o Liae", "Lehi's sons"),
            ("i Ierusalema", "to Jerusalem"),
            ("ma valaaulia", "and invite"),
            ("Isamaeli", "Ishmael"),
            ("ma lona auaiga", "and his household"),
            ("ia latou auai faatasi", "to join"),
            ("ma i latou", "with them"),
            ("i la latou malaga—", "in their journey—"),
            ("Ua fouvale", "rebel"),
            ("Lamana", "Laman"),
            ("ma isi—", "and others—"),
            ("Ua apoapoai atu", "exhorts"),
            ("Nifae", "Nephi"),
            ("i ona uso", "his brethren"),
            ("ia faatuatua", "to have faith"),
            ("i le Alii—", "in the Lord—"),
            ("Ua latou saisai o ia", "they bind him"),
            ("i maea", "with cords"),
            ("ma fuafua", "and plan"),
            ("e faaumatia o ia—", "to destroy him—"),
            ("Ua tatalaina o ia", "he is freed"),
            ("i le mana", "by the power"),
            ("o le faatuatua—", "of faith—"),
            ("Ua talosaga", "ask"),
            ("ona uso", "his brethren"),
            ("mo se faamagaloga—", "for forgiveness—"),
            ("Ua osi", "offer"),
            ("e Liae", "Lehi"),
            ("ma lana aumalaga", "and his company"),
            ("taulaga", "sacrifice"),
            ("ma taulaga mu.", "and burnt offerings."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|8": {
        "en": "Lehi sees a vision of the tree of life—He partakes of its "
              "fruit and desires his family to do likewise—He sees a rod of "
              "iron, a strait and narrow path, and the mists of darkness that "
              "enshroud men—Sariah, Nephi, and Sam partake of the fruit, but "
              "Laman and Lemuel refuse. About 600–592 B.C.",
        "sm": "Ua vaai Liae i se faaaliga o le laau o le ola—Ua 'ai o ia i "
              "lona fua ma ua manao ia faapea ona faia e lona aiga—Ua vaai o "
              "ia i se āi u'amea, se ala lauitiiti ma le vaapiapi, ma le puao "
              "o le pogisa ua siomia ai tagata—Ua aai Sarai, Nifae, ma Sama i "
              "le fua o le laau, ae ua mumusu Lamana ma Lemuelu. E tusa o le "
              "600–592 T.L.M.",
        "cells": [
            ("Ua vaai", "sees"),
            ("Liae", "Lehi"),
            ("i se faaaliga", "a vision"),
            ("o le laau", "of the tree"),
            ("o le ola—", "of life—"),
            ("Ua 'ai o ia", "he partakes"),
            ("i lona fua", "of its fruit"),
            ("ma ua manao", "and desires"),
            ("ia faapea ona faia", "to do likewise"),
            ("e lona aiga—", "his family—"),
            ("Ua vaai o ia", "he sees"),
            ("i se āi u'amea,", "a rod of iron,"),
            ("se ala lauitiiti", "a strait path"),
            ("ma le vaapiapi,", "and narrow,"),
            ("ma le puao", "and the mists"),
            ("o le pogisa", "of darkness"),
            ("ua siomia ai tagata—", "that enshroud men—"),
            ("Ua aai", "partake"),
            ("Sarai,", "Sariah,"),
            ("Nifae,", "Nephi,"),
            ("ma Sama", "and Sam"),
            ("i le fua", "of the fruit"),
            ("o le laau,", "of the tree,"),
            ("ae ua mumusu", "but refuse"),
            ("Lamana", "Laman"),
            ("ma Lemuelu.", "and Lemuel."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|9": {
        "en": "Nephi makes two sets of records—Each is called the plates of "
              "Nephi—The larger plates contain a secular history; the smaller "
              "ones deal primarily with sacred things. About 600–592 B.C.",
        "sm": "Ua fai e Nifae ni tuufaatasiga se lua o talafaamaumau—Ua ta'ua "
              "tuufaatasiga taitasi o papatusi a Nifae—O papatusi tetele ua i "
              "ai se talafaasolopito o mea faaletino; o papatusi laiti ua "
              "faapitoa mo mea paia. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua fai", "makes"),
            ("e Nifae", "Nephi"),
            ("ni tuufaatasiga se lua", "two sets"),
            ("o talafaamaumau—", "of records—"),
            ("Ua ta'ua", "is called"),
            ("tuufaatasiga taitasi", "each set"),
            ("o papatusi a Nifae—", "the plates of Nephi—"),
            ("O papatusi tetele", "The larger plates"),
            ("ua i ai", "contain"),
            ("se talafaasolopito", "a history"),
            ("o mea faaletino;", "of temporal things;"),
            ("o papatusi laiti", "the smaller plates"),
            ("ua faapitoa", "deal primarily"),
            ("mo mea paia.", "with sacred things."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|10": {
        "en": "Lehi predicts that the Jews will be taken captive by the "
              "Babylonians—He tells of the coming among the Jews of a Messiah, "
              "a Savior, a Redeemer—Lehi tells also of the coming of the one "
              "who should baptize the Lamb of God—Lehi tells of the death and "
              "resurrection of the Messiah—He compares the scattering and "
              "gathering of Israel to an olive tree—Nephi speaks of the Son of "
              "God, of the gift of the Holy Ghost, and of the need for "
              "righteousness. About 600–592 B.C.",
        "sm": "Ua vavalo Liae o le a ave faatagataotauaina tagata Iutaia e "
              "Papelonia—Ua ta'u mai e ia le afio mai o se Mesia, se Faaola, "
              "se Togiola, i totonu o tagata Iutaia—Ua ta'u mai foi e Liae le "
              "oo mai o lē o le a ia papatisoina le Tamai Mamoe a le Atua—Ua "
              "ta'u mai e Liae le maliu ma le toetu mai o le Mesia—Ua "
              "faatusaina e ia i se laau olive le faataapeapeina ma le "
              "faapotopotoina o Isaraelu—Ua tautala Nifae e uiga i le Alo o le "
              "Atua, le meaalofa o le Agaga Paia, ma le manaomia o le "
              "amiotonu. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua vavalo", "predicts"),
            ("Liae", "Lehi"),
            ("o le a ave faatagataotauaina", "shall be taken captive"),
            ("tagata Iutaia", "the Jews"),
            ("e Papelonia—", "by the Babylonians—"),
            ("Ua ta'u mai e ia", "he tells"),
            ("le afio mai", "of the coming"),
            ("o se Mesia,", "of a Messiah,"),
            ("se Faaola,", "a Savior,"),
            ("se Togiola,", "a Redeemer,"),
            ("i totonu o tagata Iutaia—", "among the Jews—"),
            ("Ua ta'u mai foi", "tells also"),
            ("e Liae", "Lehi"),
            ("le oo mai", "of the coming"),
            ("o lē", "of the one"),
            ("o le a ia papatisoina", "who shall baptize"),
            ("le Tamai Mamoe", "the Lamb"),
            ("a le Atua—", "of God—"),
            ("Ua ta'u mai e Liae", "Lehi tells"),
            ("le maliu", "of the death"),
            ("ma le toetu mai", "and resurrection"),
            ("o le Mesia—", "of the Messiah—"),
            ("Ua faatusaina e ia", "he compares"),
            ("i se laau olive", "to an olive tree"),
            ("le faataapeapeina", "the scattering"),
            ("ma le faapotopotoina", "and gathering"),
            ("o Isaraelu—", "of Israel—"),
            ("Ua tautala", "speaks"),
            ("Nifae", "Nephi"),
            ("e uiga i", "of"),
            ("le Alo o le Atua,", "the Son of God,"),
            ("le meaalofa", "the gift"),
            ("o le Agaga Paia,", "of the Holy Ghost,"),
            ("ma le manaomia", "and the need"),
            ("o le amiotonu.", "for righteousness."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|11": {
        "en": "Nephi sees the Spirit of the Lord and is shown in vision the "
              "tree of life—He sees the mother of the Son of God and learns of "
              "the condescension of God—He sees the baptism, ministry, and "
              "crucifixion of the Lamb of God—He sees also the call and "
              "ministry of the Twelve Apostles of the Lamb. About 600–592 B.C.",
        "sm": "Ua vaai Nifae i le Agaga o le Alii ma ua faaali mai ia te ia le "
              "laau o le ola i se faaaliga vaaia—Ua vaai o ia i le tinā o le "
              "Alo o le Atua ma iloa ai e uiga i le faamaualalo o le Atua—Ua "
              "vaai o ia i le papatisoga, auaunaga, ma le faasatauroga o le "
              "Tamai Mamoe a le Atua—Ua vaai foi o ia i le valaauga ma "
              "auaunaga a Aposetolo e Toasefululua a le Tamai Mamoe. E tusa o "
              "le 600–592 T.L.M.",
        "cells": [
            ("Ua vaai", "sees"),
            ("Nifae", "Nephi"),
            ("i le Agaga", "the Spirit"),
            ("o le Alii", "of the Lord"),
            ("ma ua faaali mai", "and is shown"),
            ("ia te ia", "to him"),
            ("le laau", "the tree"),
            ("o le ola", "of life"),
            ("i se faaaliga vaaia—", "in a vision—"),
            ("Ua vaai o ia", "he sees"),
            ("i le tinā", "the mother"),
            ("o le Alo", "of the Son"),
            ("o le Atua", "of God"),
            ("ma iloa ai", "and learns"),
            ("e uiga i", "of"),
            ("le faamaualalo", "the condescension"),
            ("o le Atua—", "of God—"),
            ("Ua vaai o ia", "he sees"),
            ("i le papatisoga,", "the baptism,"),
            ("auaunaga,", "ministry,"),
            ("ma le faasatauroga", "and crucifixion"),
            ("o le Tamai Mamoe", "of the Lamb"),
            ("a le Atua—", "of God—"),
            ("Ua vaai foi o ia", "he sees also"),
            ("i le valaauga", "the call"),
            ("ma auaunaga", "and ministry"),
            ("a Aposetolo e Toasefululua", "of the Twelve Apostles"),
            ("a le Tamai Mamoe.", "of the Lamb."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|12": {
        "en": "Nephi sees in vision the land of promise; the righteousness, "
              "iniquity, and downfall of its inhabitants; the coming of the "
              "Lamb of God among them; how the Twelve Disciples and the Twelve "
              "Apostles will judge Israel; and the loathsome and filthy state "
              "of those who dwindle in unbelief. About 600–592 B.C.",
        "sm": "Ua vaai Nifae i le laueleele o le folafolaga i se faaaliga "
              "vaaia; o le amiotonu, amioletonu, ma le pa'u'ū o e e nonofo ai; "
              "o le afio mai o le Tamai Mamoe a le Atua ia te i latou; o le ala "
              "o le a faamasino ai Isaraelu e Soo e Toasefululua ma Aposetolo e "
              "Toasefululua; ma le tulaga inosia ma eleelea o e e faaitiitia i "
              "le lē talitonu. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua vaai", "sees"),
            ("Nifae", "Nephi"),
            ("i le laueleele", "the land"),
            ("o le folafolaga", "of promise"),
            ("i se faaaliga vaaia;", "in vision;"),
            ("o le amiotonu,", "the righteousness,"),
            ("amioletonu,", "iniquity,"),
            ("ma le pa'u'ū", "and downfall"),
            ("o e e nonofo ai;", "of its inhabitants;"),
            ("o le afio mai", "the coming"),
            ("o le Tamai Mamoe", "of the Lamb"),
            ("a le Atua", "of God"),
            ("ia te i latou;", "among them;"),
            ("o le ala", "the way"),
            ("o le a faamasino ai", "shall judge"),
            ("Isaraelu", "Israel"),
            ("e Soo e Toasefululua", "by the Twelve Disciples"),
            ("ma Aposetolo e Toasefululua;", "and the Twelve Apostles;"),
            ("ma le tulaga", "and the state"),
            ("inosia", "loathsome"),
            ("ma eleelea", "and filthy"),
            ("o e e faaitiitia", "of those who dwindle"),
            ("i le lē talitonu.", "in unbelief."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|13": {
        "en": "Nephi sees in vision the church of the devil set up among the "
              "Gentiles, the discovery and colonizing of America, the loss of "
              "many plain and precious parts of the Bible, the resultant state "
              "of gentile apostasy, the restoration of the gospel, the coming "
              "forth of latter-day scripture, and the building up of Zion. "
              "About 600–592 B.C.",
        "sm": "Ua vaaia e Nifae i se faaaliga vaaia le ekalesia a le tiapolo "
              "ua faatuina i Nuuese, le mauaina ma le 'aināina o Amerika, le "
              "leiloa o le tele o vaega manino ma pele o le Tusi Paia, le "
              "tulaga o le liliuese o nuuese, le toefuataiga o le talalelei, le "
              "oo mai o tusitusiga paia o aso e gata ai, ma le atiina ae o "
              "Siona. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("Ua vaaia e Nifae", "Nephi sees"),
            ("i se faaaliga vaaia", "in vision"),
            ("le ekalesia", "the church"),
            ("a le tiapolo", "of the devil"),
            ("ua faatuina", "set up"),
            ("i Nuuese,", "among the Gentiles,"),
            ("le mauaina", "the discovery"),
            ("ma le 'aināina", "and colonizing"),
            ("o Amerika,", "of America,"),
            ("le leiloa", "the loss"),
            ("o le tele", "of many"),
            ("o vaega manino", "of plain parts"),
            ("ma pele", "and precious"),
            ("o le Tusi Paia,", "of the Bible,"),
            ("le tulaga", "the state"),
            ("o le liliuese", "of the apostasy"),
            ("o nuuese,", "of the Gentiles,"),
            ("le toefuataiga", "the restoration"),
            ("o le talalelei,", "of the gospel,"),
            ("le oo mai", "the coming"),
            ("o tusitusiga paia", "of scripture"),
            ("o aso e gata ai,", "of the latter days,"),
            ("ma le atiina ae", "and the building up"),
            ("o Siona.", "of Zion."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|14": {
        "en": "An angel tells Nephi of the blessings and cursings to fall upon "
              "the Gentiles—There are only two churches: the Church of the "
              "Lamb of God and the church of the devil—The Saints of God in "
              "all nations are persecuted by the great and abominable "
              "church—The Apostle John will write concerning the end of the "
              "world. About 600–592 B.C.",
        "sm": "Ua faamatala mai e se agelu ia Nifae e uiga i faamanuiaga ma "
              "fetuu o le a pa'u'ū ifo i luga o Nuuese—Ua na o le lua lava "
              "ekalesia; o le Ekalesia a le Tamai Mamoe a le Atua ma le "
              "ekalesia a le tiapolo—O le Au Paia a le Atua i atunuu uma ua "
              "sauaina e le ekalesia tele ma le inosia—O le a tusi le aposetolo "
              "o Ioane e uiga i le iuga o le lalolagi. E tusa o le 600–592 "
              "T.L.M.",
        "cells": [
            ("Ua faamatala mai", "tells"),
            ("e se agelu", "an angel"),
            ("ia Nifae", "Nephi"),
            ("e uiga i", "of"),
            ("faamanuiaga", "the blessings"),
            ("ma fetuu", "and cursings"),
            ("o le a pa'u'ū ifo", "to fall"),
            ("i luga o Nuuese—", "upon the Gentiles—"),
            ("Ua na o", "there are only"),
            ("le lua lava ekalesia;", "two churches;"),
            ("o le Ekalesia", "the Church"),
            ("a le Tamai Mamoe", "of the Lamb"),
            ("a le Atua", "of God"),
            ("ma le ekalesia", "and the church"),
            ("a le tiapolo—", "of the devil—"),
            ("O le Au Paia", "The Saints"),
            ("a le Atua", "of God"),
            ("i atunuu uma", "in all nations"),
            ("ua sauaina", "are persecuted"),
            ("e le ekalesia tele", "by the great church"),
            ("ma le inosia—", "and abominable—"),
            ("O le a tusi", "will write"),
            ("le aposetolo o Ioane", "the Apostle John"),
            ("e uiga i", "concerning"),
            ("le iuga o le lalolagi.", "the end of the world."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|15": {
        "en": "Lehi's seed are to receive the gospel from the Gentiles in the "
              "latter days—The gathering of Israel is likened unto an olive "
              "tree whose natural branches will be grafted in again—Nephi "
              "interprets the vision of the tree of life and speaks of the "
              "justice of God in dividing the wicked from the righteous. "
              "About 600–592 B.C.",
        "sm": "O le a maua e fanau a Liae le talalelei mai Nuuese i aso e gata "
              "ai—O le faapotopotoina o Isaraelu ua faatusa i se laau olive o "
              "le a toe sulu i totonu ona lala moni—Ua faamatala mai e Nifae le "
              "faaaliga vaaia o le laau o le ola ma tautala mai e uiga i le "
              "faamasinotonu o le Atua i le vavaeeseina o e amioleaga mai e "
              "amiotonu. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("O le a maua", "shall receive"),
            ("e fanau a Liae", "Lehi's seed"),
            ("le talalelei", "the gospel"),
            ("mai Nuuese", "from the Gentiles"),
            ("i aso e gata ai—", "in the latter days—"),
            ("O le faapotopotoina", "The gathering"),
            ("o Isaraelu", "of Israel"),
            ("ua faatusa", "is likened"),
            ("i se laau olive", "unto an olive tree"),
            ("o le a toe sulu", "shall be grafted again"),
            ("i totonu", "in"),
            ("ona lala moni—", "its natural branches—"),
            ("Ua faamatala mai e Nifae", "Nephi interprets"),
            ("le faaaliga vaaia", "the vision"),
            ("o le laau", "of the tree"),
            ("o le ola", "of life"),
            ("ma tautala mai", "and speaks"),
            ("e uiga i", "of"),
            ("le faamasinotonu", "the justice"),
            ("o le Atua", "of God"),
            ("i le vavaeeseina", "in dividing"),
            ("o e amioleaga", "the wicked"),
            ("mai e amiotonu.", "from the righteous."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|16": {
        "en": "The wicked take the truth to be hard—Lehi's sons marry the "
              "daughters of Ishmael—The Liahona guides their course in the "
              "wilderness—Messages from the Lord are written on the Liahona "
              "from time to time—Ishmael dies; his family murmurs because of "
              "afflictions. About 600–592 B.C.",
        "sm": "E ave e e amioleaga le upumoni o se mea faigata—Ua faaipoipo "
              "atalii o Liae i afafine o Isamaeli—Ua taitai e le Liahona lo "
              "latou ala i le vao—Ua tusia i le Liahona savali mai le Alii mai "
              "lea taimi i lea taimi—Ua oti Isamaeli; ua muimui lona aiga ona o "
              "puapuaga. E tusa o le 600–592 T.L.M.",
        "cells": [
            ("E ave e e amioleaga", "the wicked take"),
            ("le upumoni", "the truth"),
            ("o se mea faigata—", "to be hard—"),
            ("Ua faaipoipo", "marry"),
            ("atalii o Liae", "Lehi's sons"),
            ("i afafine o Isamaeli—", "the daughters of Ishmael—"),
            ("Ua taitai", "guides"),
            ("e le Liahona", "the Liahona"),
            ("lo latou ala", "their course"),
            ("i le vao—", "in the wilderness—"),
            ("Ua tusia", "are written"),
            ("i le Liahona", "on the Liahona"),
            ("savali mai le Alii", "messages from the Lord"),
            ("mai lea taimi", "from time"),
            ("i lea taimi—", "to time—"),
            ("Ua oti", "dies"),
            ("Isamaeli;", "Ishmael;"),
            ("ua muimui", "murmurs"),
            ("lona aiga", "his family"),
            ("ona o puapuaga.", "because of afflictions."),
            ("E tusa o le", "about"),
            ("600–592", "600–592"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|17": {
        "en": "Nephi is commanded to build a ship—His brethren oppose him—He "
              "exhorts them by recounting the history of God's dealings with "
              "Israel—Nephi is filled with the power of God—His brethren are "
              "forbidden to touch him, lest they wither as a dried reed. "
              "About 592–591 B.C.",
        "sm": "Ua poloaiina Nifae e fau se vaa—Ua tetee ona uso ia te ia—Ua ia "
              "apoapoa'ia i laua i le toe faamatala atu o le talafaasolopito o "
              "fealoaiga a le Atua ma Isaraelu—Ua faatumulia Nifae i le mana o "
              "le Atua—Ua faasa ona uso ona pa'i mai ia te ia, ina ne'i mamae i "
              "laua e pei o se vaoutuutu mago. E tusa o le 592–591 T.L.M.",
        "cells": [
            ("Ua poloaiina", "is commanded"),
            ("Nifae", "Nephi"),
            ("e fau se vaa—", "to build a ship—"),
            ("Ua tetee", "oppose"),
            ("ona uso", "his brethren"),
            ("ia te ia—", "him—"),
            ("Ua ia apoapoa'ia i laua", "he exhorts them"),
            ("i le toe faamatala atu", "by recounting"),
            ("o le talafaasolopito", "the history"),
            ("o fealoaiga", "of the dealings"),
            ("a le Atua", "of God"),
            ("ma Isaraelu—", "with Israel—"),
            ("Ua faatumulia", "is filled"),
            ("Nifae", "Nephi"),
            ("i le mana", "with the power"),
            ("o le Atua—", "of God—"),
            ("Ua faasa", "are forbidden"),
            ("ona uso", "his brethren"),
            ("ona pa'i mai", "to touch"),
            ("ia te ia,", "him,"),
            ("ina ne'i", "lest"),
            ("mamae i laua", "they wither"),
            ("e pei o", "as"),
            ("se vaoutuutu mago.", "a dried reed."),
            ("E tusa o le", "about"),
            ("592–591", "592–591"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|18": {
        "en": "The ship is finished—The births of Jacob and Joseph are "
              "mentioned—The company embarks for the promised land—The sons of "
              "Ishmael and their wives join in revelry and rebellion—Nephi is "
              "bound, and the ship is driven back by a terrible tempest—Nephi "
              "is freed, and by his prayer the storm ceases—The people arrive "
              "in the promised land. About 591–589 B.C.",
        "sm": "Ua uma le vaa—Ua ta'u mai le fananau mai o Iakopo ma Iosefa—Ua "
              "folau atu le malaga i le laueleele na folafolaina—Ua auai atalii "
              "o Isamaeli ma a latou ava i fiafiaga ma fouvalega—Ua noatia "
              "Nifae, ma ua toe tafea i tua le vaa i le afā malosi—Ua tatala "
              "Nifae, ma ua taofia le afā i lana tatalo—Ua taunuu le nuu i le "
              "laueleele na folafolaina. E tusa o le 591–589 T.L.M.",
        "cells": [
            ("Ua uma", "is finished"),
            ("le vaa—", "the ship—"),
            ("Ua ta'u mai", "are mentioned"),
            ("le fananau mai", "the births"),
            ("o Iakopo", "of Jacob"),
            ("ma Iosefa—", "and Joseph—"),
            ("Ua folau atu", "embarks"),
            ("le malaga", "the company"),
            ("i le laueleele na folafolaina—", "for the promised land—"),
            ("Ua auai", "join"),
            ("atalii o Isamaeli", "the sons of Ishmael"),
            ("ma a latou ava", "and their wives"),
            ("i fiafiaga", "in revelry"),
            ("ma fouvalega—", "and rebellion—"),
            ("Ua noatia", "is bound"),
            ("Nifae,", "Nephi,"),
            ("ma ua toe tafea", "and is driven"),
            ("i tua", "back"),
            ("le vaa", "the ship"),
            ("i le afā malosi—", "by a terrible tempest—"),
            ("Ua tatala", "is freed"),
            ("Nifae,", "Nephi,"),
            ("ma ua taofia", "and ceases"),
            ("le afā", "the storm"),
            ("i lana tatalo—", "by his prayer—"),
            ("Ua taunuu", "arrive"),
            ("le nuu", "the people"),
            ("i le laueleele na folafolaina.", "in the promised land."),
            ("E tusa o le", "about"),
            ("591–589", "591–589"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|19": {
        "en": "Nephi makes plates of ore and records the history of his "
              "people—The God of Israel will come six hundred years from the "
              "time Lehi left Jerusalem—Nephi tells of His sufferings and "
              "crucifixion—The Jews will be despised and scattered until the "
              "latter days, when they will return unto the Lord. "
              "About 588–570 B.C.",
        "sm": "Ua fai e Nifae ni papatusi mai minerale u'amea ma faamaumau le "
              "talafaasolopito o ona tagata—O le a afio mai le Atua o Isaraelu "
              "i le ono selau tausaga mai le taimi na tu'ua ai e Liae "
              "Ierusalema—Ua faamatala mai e Nifae e uiga i Ona mafatiaga ma "
              "Lona faasatauroga—O le a inosia ma faataapeapeina tagata Iutaia "
              "e oo i aso e gata ai, i le na taimi latou te toe foi mai ai i le "
              "Alii. E tusa o le 588–570 T.L.M.",
        "cells": [
            ("Ua fai", "makes"),
            ("e Nifae", "Nephi"),
            ("ni papatusi", "plates"),
            ("mai minerale u'amea", "of ore"),
            ("ma faamaumau", "and records"),
            ("le talafaasolopito", "the history"),
            ("o ona tagata—", "of his people—"),
            ("O le a afio mai", "will come"),
            ("le Atua o Isaraelu", "the God of Israel"),
            ("i le ono selau tausaga", "six hundred years"),
            ("mai le taimi", "from the time"),
            ("na tu'ua ai e Liae", "Lehi left"),
            ("Ierusalema—", "Jerusalem—"),
            ("Ua faamatala mai e Nifae", "Nephi tells"),
            ("e uiga i", "of"),
            ("Ona mafatiaga", "His sufferings"),
            ("ma Lona faasatauroga—", "and His crucifixion—"),
            ("O le a inosia", "will be despised"),
            ("ma faataapeapeina", "and scattered"),
            ("tagata Iutaia", "the Jews"),
            ("e oo", "until"),
            ("i aso e gata ai,", "the latter days,"),
            ("i le na taimi", "when"),
            ("latou te toe foi mai ai", "they will return"),
            ("i le Alii.", "unto the Lord."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|20": {
        "en": "The Lord reveals His purposes to Israel—Israel has been chosen "
              "in the furnace of affliction and is to go forth from "
              "Babylon—Compare Isaiah 48. About 588–570 B.C.",
        "sm": "Ua faaali mai e le Alii Ona faamoemoega ia Isaraelu—Ua "
              "filifilia Isaraelu mai le ogaumu o puapuaga ma ua poloaiina ia "
              "alu ese atu mai Papelonia—Faatusatusa i le Isaia 48. E tusa o le "
              "588–570 T.L.M.",
        "cells": [
            ("Ua faaali mai", "reveals"),
            ("e le Alii", "the Lord"),
            ("Ona faamoemoega", "His purposes"),
            ("ia Isaraelu—", "to Israel—"),
            ("Ua filifilia", "has been chosen"),
            ("Isaraelu", "Israel"),
            ("mai le ogaumu", "from the furnace"),
            ("o puapuaga", "of affliction"),
            ("ma ua poloaiina", "and is commanded"),
            ("ia alu ese atu", "to go forth"),
            ("mai Papelonia—", "from Babylon—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 48.", "Isaiah 48."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|21": {
        "en": "The Messiah will be a light to the Gentiles and will free the "
              "prisoners—Israel will be gathered with power in the last "
              "days—Kings will be their nursing fathers—Compare Isaiah 49.",
        "sm": "O le a avea le Mesia o se malamalama i Nuuese ma o le a "
              "faasaoloto e ia pagota—O le a faapotopotoina Isaraelu ma le mana "
              "i aso e gata ai—O le a avea tupu ma o latou tamā "
              "tausitama—Faatusatusa i le Isaia 49. E tusa o le 588–570 T.L.M.",
        "cells": [
            ("O le a avea", "will be"),
            ("le Mesia", "the Messiah"),
            ("o se malamalama", "a light"),
            ("i Nuuese", "to the Gentiles"),
            ("ma o le a faasaoloto e ia", "and he will free"),
            ("pagota—", "the prisoners—"),
            ("O le a faapotopotoina", "will be gathered"),
            ("Isaraelu", "Israel"),
            ("ma le mana", "with power"),
            ("i aso e gata ai—", "in the last days—"),
            ("O le a avea", "will be"),
            ("tupu", "kings"),
            ("ma o latou tamā tausitama—", "their nursing fathers—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 49.", "Isaiah 49."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "1nephi|22": {
        "en": "Israel will be scattered upon all the face of the earth—The "
              "Gentiles will nurse and nourish Israel with the gospel in the "
              "last days—Israel will be gathered and saved, and the wicked "
              "will burn as stubble—The kingdom of the devil will be "
              "destroyed, and Satan will be bound. About 588–570 B.C.",
        "sm": "O le a faataapeapeina Isaraelu i luga o le fogaeleele uma—O le a "
              "faafailele ma tausi Isaraelu e Nuuese i le talalelei i aso e "
              "gata ai—O le a faapotopotoina ma laveaiina Isaraelu, ma o e "
              "amioleaga o le a mu e pei o tagutugutu o saito—O le a faaumatia "
              "le malo o le tiapolo, ma o le a noatia Satani. E tusa o le "
              "588–570 T.L.M.",
        "cells": [
            ("O le a faataapeapeina", "will be scattered"),
            ("Isaraelu", "Israel"),
            ("i luga o", "upon"),
            ("le fogaeleele uma—", "all the earth—"),
            ("O le a faafailele", "will nurse"),
            ("ma tausi", "and nourish"),
            ("Isaraelu", "Israel"),
            ("e Nuuese", "the Gentiles"),
            ("i le talalelei", "with the gospel"),
            ("i aso e gata ai—", "in the last days—"),
            ("O le a faapotopotoina", "will be gathered"),
            ("ma laveaiina", "and saved"),
            ("Isaraelu,", "Israel,"),
            ("ma o e amioleaga", "and the wicked"),
            ("o le a mu", "will burn"),
            ("e pei o", "as"),
            ("tagutugutu o saito—", "stubble—"),
            ("O le a faaumatia", "will be destroyed"),
            ("le malo", "the kingdom"),
            ("o le tiapolo,", "of the devil,"),
            ("ma o le a noatia", "and will be bound"),
            ("Satani.", "Satan."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    # NOTE: 2nephi|1 pending — Church page exposes only the book preface
    # ("O se tala i le maliu o Liae...") before verse 1, not the chapter
    # heading. Needs a manual grab of the Samoan summary.
    "2nephi|2": {
        "en": "Redemption comes through the Holy Messiah—Freedom of choice "
              "(agency) is essential to existence and progression—Adam fell "
              "that men might be—Men are free to choose liberty and eternal "
              "life. About 588–570 B.C.",
        "sm": "O le togiolaina e oo mai e ala i le Mesia Paia—O le filifiliga "
              "saoloto (faitalia) ua taua i le olaga ma le alualu i luma—Na "
              "pa'ū Atamu ina ia i ai le tagata—Ua saoloto tagata e filifili le "
              "saolotoga ma le ola e faavavau. E tusa o le 588–570 T.L.M.",
        "cells": [
            ("O le togiolaina", "Redemption"),
            ("e oo mai", "comes"),
            ("e ala i", "through"),
            ("le Mesia Paia—", "the Holy Messiah—"),
            ("O le filifiliga saoloto", "Freedom of choice"),
            ("(faitalia)", "(agency)"),
            ("ua taua", "is essential"),
            ("i le olaga", "to existence"),
            ("ma le alualu i luma—", "and progression—"),
            ("Na pa'ū Atamu", "Adam fell"),
            ("ina ia", "that"),
            ("i ai le tagata—", "men might be—"),
            ("Ua saoloto tagata", "Men are free"),
            ("e filifili", "to choose"),
            ("le saolotoga", "liberty"),
            ("ma le ola e faavavau.", "and eternal life."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|3": {
        "en": "Joseph in Egypt saw the Nephites in vision—He prophesied of "
              "Joseph Smith, the latter-day seer; of Moses, who would deliver "
              "Israel; and of the coming forth of the Book of Mormon. "
              "About 588–570 B.C.",
        "sm": "Sa vaai Iosefa i Aikupito i tagata sa Nifaē i se faaaliga "
              "vaaia—Sa vavalo o ia e uiga ia Iosefa Samita, le tagatavāai o "
              "aso e gata ai; e uiga ia Mose o lē o le a laveaia Isaraelu; ma e "
              "uiga i le oo mai o le Tusi a Mamona. E tusa o le 588–570 T.L.M.",
        "cells": [
            ("Sa vaai", "saw"),
            ("Iosefa i Aikupito", "Joseph in Egypt"),
            ("i tagata sa Nifaē", "the Nephites"),
            ("i se faaaliga vaaia—", "in vision—"),
            ("Sa vavalo o ia", "he prophesied"),
            ("e uiga ia Iosefa Samita,", "of Joseph Smith,"),
            ("le tagatavāai", "the seer"),
            ("o aso e gata ai;", "of the latter days;"),
            ("e uiga ia Mose", "of Moses"),
            ("o lē", "who"),
            ("o le a laveaia", "would deliver"),
            ("Isaraelu;", "Israel;"),
            ("ma e uiga i", "and of"),
            ("le oo mai", "the coming forth"),
            ("o le Tusi a Mamona.", "of the Book of Mormon."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|4": {
        "en": "Lehi counsels and blesses his posterity—He dies and is "
              "buried—Nephi glories in the goodness of God—Nephi puts his "
              "trust in the Lord forever. About 588–570 B.C.",
        "sm": "Ua fautua ma faamanuia atu Liae i ana fanau—Ua maliu o ia ma ua "
              "tanumia—Ua viia e Nifae le agalelei o le Atua—Ua tuu atu e Nifae "
              "lona faalagolago i le Alii e faavavau. E tusa o le 588–570 "
              "T.L.M.",
        "cells": [
            ("Ua fautua", "counsels"),
            ("ma faamanuia atu", "and blesses"),
            ("Liae", "Lehi"),
            ("i ana fanau—", "his posterity—"),
            ("Ua maliu o ia", "he dies"),
            ("ma ua tanumia—", "and is buried—"),
            ("Ua viia e Nifae", "Nephi glories in"),
            ("le agalelei", "the goodness"),
            ("o le Atua—", "of God—"),
            ("Ua tuu atu e Nifae", "Nephi puts"),
            ("lona faalagolago", "his trust"),
            ("i le Alii", "in the Lord"),
            ("e faavavau.", "forever."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|5": {
        "en": "The Nephites separate themselves from the Lamanites, keep the "
              "law of Moses, and build a temple—Because of their unbelief, the "
              "Lamanites are cut off from the presence of the Lord, are cursed, "
              "and become a scourge unto the Nephites. About 588–559 B.C.",
        "sm": "Ua vavae ese e sa Nifaē i latou lava mai ia sa Lamanā, ua latou "
              "tausia le tulafono a Mose, ma fausia se malumalu—Ona o lo latou "
              "lē talitonu, ua vavae ese ai sa Lamanā mai luma o le Alii, ua "
              "fetuuina, ma ua avea ma sasa ia sa Nifaē. E tusa o le 588–559 "
              "T.L.M.",
        "cells": [
            ("Ua vavae ese", "separate"),
            ("e sa Nifaē", "the Nephites"),
            ("i latou lava", "themselves"),
            ("mai ia sa Lamanā,", "from the Lamanites,"),
            ("ua latou tausia", "they keep"),
            ("le tulafono a Mose,", "the law of Moses,"),
            ("ma fausia", "and build"),
            ("se malumalu—", "a temple—"),
            ("Ona o", "Because of"),
            ("lo latou lē talitonu,", "their unbelief,"),
            ("ua vavae ese ai", "are cut off"),
            ("sa Lamanā", "the Lamanites"),
            ("mai luma o le Alii,", "from the presence of the Lord,"),
            ("ua fetuuina,", "are cursed,"),
            ("ma ua avea ma sasa", "and become a scourge"),
            ("ia sa Nifaē.", "unto the Nephites."),
            ("E tusa o le", "about"),
            ("588–559", "588–559"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|6": {
        "en": "Jacob recounts Jewish history: The Babylonian captivity and "
              "return; the ministry and crucifixion of the Holy One of Israel; "
              "the help received from the Gentiles; and the Jews' latter-day "
              "restoration when they believe in the Messiah. About 559–545 B.C.",
        "sm": "Ua toe faamatala mai e Iakopo le talafaasolopito o tagata "
              "Iutaia: O le faatagataotauaina i Papelonia ma le toe foi mai; o "
              "le auaunaga ma le faasatauroga o le Paia e Toatasi o Isaraelu; o "
              "le fesoasoani na maua mai i Nuuese; ma le toefuataiga o tagata "
              "Iutaia i aso e gata ai pe a latou talitonu i le Mesia. E tusa o "
              "le 559–545 T.L.M.",
        "cells": [
            ("Ua toe faamatala mai", "recounts"),
            ("e Iakopo", "Jacob"),
            ("le talafaasolopito", "the history"),
            ("o tagata Iutaia:", "of the Jews:"),
            ("O le faatagataotauaina", "The captivity"),
            ("i Papelonia", "in Babylon"),
            ("ma le toe foi mai;", "and return;"),
            ("o le auaunaga", "the ministry"),
            ("ma le faasatauroga", "and crucifixion"),
            ("o le Paia e Toatasi", "of the Holy One"),
            ("o Isaraelu;", "of Israel;"),
            ("o le fesoasoani", "the help"),
            ("na maua mai", "received"),
            ("i Nuuese;", "from the Gentiles;"),
            ("ma le toefuataiga", "and the restoration"),
            ("o tagata Iutaia", "of the Jews"),
            ("i aso e gata ai", "in the latter days"),
            ("pe a latou talitonu", "when they believe"),
            ("i le Mesia.", "in the Messiah."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|7": {
        "en": "Jacob continues reading from Isaiah: Isaiah speaks "
              "messianically—The Messiah will have the tongue of the "
              "learned—He will give His back to the smiters—He will not be "
              "confounded—Compare Isaiah 50.",
        "sm": "Ua faaauau le faitauina e Iakopo mai le tusi a Isaia: Ua tautala "
              "Isaia faale-Mesia—O le a i ai i le Mesia le laulaufaiva o lē ua "
              "aoaoina—O le a tuu atu e ia Lona tua i e e sasa mai—O le a lē "
              "maasiasi o ia—Faatusatusa i le Isaia 50. E tusa o le 559–545 "
              "T.L.M.",
        "cells": [
            ("Ua faaauau le faitauina", "continues reading"),
            ("e Iakopo", "Jacob"),
            ("mai le tusi a Isaia:", "from the book of Isaiah:"),
            ("Ua tautala Isaia", "Isaiah speaks"),
            ("faale-Mesia—", "messianically—"),
            ("O le a i ai", "there will be"),
            ("i le Mesia", "to the Messiah"),
            ("le laulaufaiva", "the tongue"),
            ("o lē ua aoaoina—", "of the learned—"),
            ("O le a tuu atu e ia", "he will give"),
            ("Lona tua", "His back"),
            ("i e e sasa mai—", "to the smiters—"),
            ("O le a lē maasiasi o ia—", "he will not be confounded—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 50.", "Isaiah 50."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|8": {
        "en": "Jacob continues reading from Isaiah: In the last days, the Lord "
              "will comfort Zion and gather Israel—The redeemed will come to "
              "Zion amid great joy—Compare Isaiah 51 and 52:1–2. "
              "About 559–545 B.C.",
        "sm": "Ua faaauau le faitauina e Iakopo mai le tusi a Isaia: I aso e "
              "gata ai, o le a faamafanafanaina Siona e le Alii ma faapotopoto "
              "Isaraelu—O le a o mai i Siona e ua togiolaina i le lotolotoi o le "
              "olioli tele—Faatusatusa i le Isaia 51 ma le 52:1–2. E tusa o le "
              "559–545 T.L.M.",
        "cells": [
            ("Ua faaauau le faitauina", "continues reading"),
            ("e Iakopo", "Jacob"),
            ("mai le tusi a Isaia:", "from the book of Isaiah:"),
            ("I aso e gata ai,", "In the last days,"),
            ("o le a faamafanafanaina", "will comfort"),
            ("Siona", "Zion"),
            ("e le Alii", "the Lord"),
            ("ma faapotopoto", "and gather"),
            ("Isaraelu—", "Israel—"),
            ("O le a o mai", "will come"),
            ("i Siona", "to Zion"),
            ("e ua togiolaina", "the redeemed"),
            ("i le lotolotoi", "amid"),
            ("o le olioli tele—", "of great joy—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 51", "Isaiah 51"),
            ("ma le 52:1–2.", "and 52:1–2."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|9": {
        "en": "Jacob explains that the Jews will be gathered in all their "
              "lands of promise—The Atonement ransoms man from the Fall—The "
              "bodies of the dead will come forth from the grave, and their "
              "spirits from hell and from paradise—They will be judged—The "
              "Atonement saves from death, hell, the devil, and endless "
              "torment—The righteous are to be saved in the kingdom of "
              "God—Penalties for sins are set forth—The Holy One of Israel is "
              "the keeper of the gate. About 559–545 B.C.",
        "sm": "Ua faamalamalama mai e Iakopo faapea o le a faapotopotoina "
              "tagata Iutaia i o latou laueleele uma o le folafolaga—O le "
              "Togiola e togiola ai tagata mai le Pa'ū—O le a o a'e tino o e ua "
              "oti mai le tuugamau, ma o latou agaga mai seoli ma mai le "
              "parataiso—O le a faamasinoina i latou—O le Togiola e laveai ai "
              "mai le oti, seoli, le tiapolo, ma le mafatiaga e lē gata—O le a "
              "faaolaina e amiotonu i le malo o le Atua—Ua faatutu mai faasalaga "
              "mo agasala—O le Paia e Toatasi o Isaraelu o le leoleo lea o le "
              "faitotoa. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua faamalamalama mai e Iakopo", "Jacob explains"),
            ("faapea", "that"),
            ("o le a faapotopotoina", "will be gathered"),
            ("tagata Iutaia", "the Jews"),
            ("i o latou laueleele uma", "in all their lands"),
            ("o le folafolaga—", "of promise—"),
            ("O le Togiola", "The Atonement"),
            ("e togiola ai tagata", "ransoms man"),
            ("mai le Pa'ū—", "from the Fall—"),
            ("O le a o a'e", "will come forth"),
            ("tino", "the bodies"),
            ("o e ua oti", "of the dead"),
            ("mai le tuugamau,", "from the grave,"),
            ("ma o latou agaga", "and their spirits"),
            ("mai seoli", "from hell"),
            ("ma mai le parataiso—", "and from paradise—"),
            ("O le a faamasinoina", "will be judged"),
            ("i latou—", "them—"),
            ("O le Togiola", "The Atonement"),
            ("e laveai ai", "saves"),
            ("mai le oti,", "from death,"),
            ("seoli,", "hell,"),
            ("le tiapolo,", "the devil,"),
            ("ma le mafatiaga", "and torment"),
            ("e lē gata—", "endless—"),
            ("O le a faaolaina", "are to be saved"),
            ("e amiotonu", "the righteous"),
            ("i le malo", "in the kingdom"),
            ("o le Atua—", "of God—"),
            ("Ua faatutu mai faasalaga", "penalties are set forth"),
            ("mo agasala—", "for sins—"),
            ("O le Paia e Toatasi", "The Holy One"),
            ("o Isaraelu", "of Israel"),
            ("o le leoleo lea", "is the keeper"),
            ("o le faitotoa.", "of the gate."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|10": {
        "en": "Jacob explains that the Jews will crucify their God—They will "
              "be scattered until they begin to believe in Him—America will be "
              "a land of liberty where no king will rule—Reconcile yourselves "
              "to God and gain salvation through His grace. About 559–545 B.C.",
        "sm": "Ua faamalamalama mai e Iakopo faapea o le a faasatauroina e "
              "tagata Iutaia lo latou Atua—O le a faataapeapeina i latou seia "
              "oo ina amata ona latou talitonu ia te Ia—O le a avea Amerika ma "
              "se laueleele o le saolotoga e lē pule ai se tupu—Ia outou "
              "faalelei outou lava ma le Atua ma maua le olataga e ala i Lona "
              "alofa tunoa. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua faamalamalama mai e Iakopo", "Jacob explains"),
            ("faapea", "that"),
            ("o le a faasatauroina", "will crucify"),
            ("e tagata Iutaia", "the Jews"),
            ("lo latou Atua—", "their God—"),
            ("O le a faataapeapeina", "will be scattered"),
            ("i latou", "them"),
            ("seia oo", "until"),
            ("ina amata ona", "begin to"),
            ("latou talitonu", "they believe"),
            ("ia te Ia—", "in Him—"),
            ("O le a avea Amerika", "America will be"),
            ("ma se laueleele", "a land"),
            ("o le saolotoga", "of liberty"),
            ("e lē pule ai", "shall not rule"),
            ("se tupu—", "a king—"),
            ("Ia outou faalelei outou lava", "Reconcile yourselves"),
            ("ma le Atua", "to God"),
            ("ma maua", "and gain"),
            ("le olataga", "salvation"),
            ("e ala i", "through"),
            ("Lona alofa tunoa.", "His grace."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|11": {
        "en": "Jacob saw his Redeemer—The law of Moses typifies Christ and "
              "proves He will come. About 559–545 B.C.",
        "sm": "Sa vaai Iakopo i lona Togiola—O le tulafono a Mose o se faatusa "
              "o Keriso ma ua faamaonia ai o le a afio mai o Ia. E tusa o le "
              "559–545 T.L.M.",
        "cells": [
            ("Sa vaai Iakopo", "Jacob saw"),
            ("i lona Togiola—", "his Redeemer—"),
            ("O le tulafono a Mose", "The law of Moses"),
            ("o se faatusa o Keriso", "typifies Christ"),
            ("ma ua faamaonia ai", "and proves"),
            ("o le a afio mai o Ia.", "He will come."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|12": {
        "en": "Isaiah sees the latter-day temple, gathering of Israel, and "
              "millennial judgment and peace—The proud and wicked will be "
              "brought low at the Second Coming—Compare Isaiah 2. "
              "About 559–545 B.C.",
        "sm": "Ua vaai Isaia i le malumalu o aso e gata ai, le faapotopotoina o "
              "Isaraelu, ma le faamasinoga i le meleniuma ma le filemu—O e "
              "faamaualuluga ma e amioleaga o le a ave ifo maualalo i le Afio "
              "Mai Faalua—Faatusatusa i le Isaia 2. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua vaai Isaia", "Isaiah sees"),
            ("i le malumalu", "the temple"),
            ("o aso e gata ai,", "of the latter days,"),
            ("le faapotopotoina", "the gathering"),
            ("o Isaraelu,", "of Israel,"),
            ("ma le faamasinoga", "and the judgment"),
            ("i le meleniuma", "in the millennium"),
            ("ma le filemu—", "and peace—"),
            ("O e faamaualuluga", "The proud"),
            ("ma e amioleaga", "and the wicked"),
            ("o le a ave ifo maualalo", "will be brought low"),
            ("i le Afio Mai Faalua—", "at the Second Coming—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 2.", "Isaiah 2."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|13": {
        "en": "Judah and Jerusalem will be punished for their disobedience—The "
              "Lord pleads for and judges His people—The daughters of Zion are "
              "cursed and tormented for their worldliness—Compare Isaiah 3. "
              "About 559–545 B.C.",
        "sm": "O le a faasalaina Iuta ma Ierusalema ona o lo laua lē "
              "usiusitai—Ua aioi le Alii mo ona tagata ma Ia faamasinoina i "
              "latou—Ua fetuu ma faamafatia afafine o Siona ona o lo latou "
              "faalelalolagi—Faatusatusa i le Isaia 3. E tusa o le 559–545 "
              "T.L.M.",
        "cells": [
            ("O le a faasalaina", "will be punished"),
            ("Iuta ma Ierusalema", "Judah and Jerusalem"),
            ("ona o", "for"),
            ("lo laua lē usiusitai—", "their disobedience—"),
            ("Ua aioi le Alii", "The Lord pleads"),
            ("mo ona tagata", "for His people"),
            ("ma Ia faamasinoina i latou—", "and judges them—"),
            ("Ua fetuu ma faamafatia", "are cursed and tormented"),
            ("afafine o Siona", "the daughters of Zion"),
            ("ona o", "for"),
            ("lo latou faalelalolagi—", "their worldliness—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 3.", "Isaiah 3."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|14": {
        "en": "Zion and her daughters will be redeemed and cleansed in the "
              "millennial day—Compare Isaiah 4. About 559–545 B.C.",
        "sm": "O le a togiola ma faamamāina Siona ma ona afafine i le aso o le "
              "meleniuma—Faatusatusa i le Isaia 4. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le a togiola", "will be redeemed"),
            ("ma faamamāina", "and cleansed"),
            ("Siona", "Zion"),
            ("ma ona afafine", "and her daughters"),
            ("i le aso", "in the day"),
            ("o le meleniuma—", "of the millennium—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 4.", "Isaiah 4."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|15": {
        "en": "The Lord's vineyard (Israel) will become desolate, and His "
              "people will be scattered—Woes will come upon them in their "
              "apostate and scattered state—The Lord will lift an ensign and "
              "gather Israel—Compare Isaiah 5. About 559–545 B.C.",
        "sm": "O le tovine o le Alii (o Isaraelu) o le a tuufua, ma o le a "
              "faataapeapeina Ona tagata—O le a oo mai mala ia te i latou i lo "
              "latou tulaga liliuese ma faataapeapeina—O le a sisi i luga e le "
              "Alii se tagavai ma faapotopoto Isaraelu—Faatusatusa i le Isaia "
              "5. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le tovine", "The vineyard"),
            ("o le Alii", "of the Lord"),
            ("(o Isaraelu)", "(Israel)"),
            ("o le a tuufua,", "will become desolate,"),
            ("ma o le a faataapeapeina", "and will be scattered"),
            ("Ona tagata—", "His people—"),
            ("O le a oo mai", "will come"),
            ("mala", "woes"),
            ("ia te i latou", "upon them"),
            ("i lo latou tulaga", "in their state"),
            ("liliuese ma faataapeapeina—", "apostate and scattered—"),
            ("O le a sisi i luga", "will lift up"),
            ("e le Alii", "the Lord"),
            ("se tagavai", "an ensign"),
            ("ma faapotopoto", "and gather"),
            ("Isaraelu—", "Israel—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 5.", "Isaiah 5."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|16": {
        "en": "Isaiah sees the Lord—Isaiah's sins are forgiven—He is called to "
              "prophesy—He prophesies of the rejection by the Jews of Christ's "
              "teachings—A remnant will return—Compare Isaiah 6. "
              "About 559–545 B.C.",
        "sm": "Ua vaai Isaia i le Alii—Ua faamagaloina agasala a Isaia—Ua "
              "valaauina o ia e vavalo atu—Ua ia valoia le teena e Iutaia o "
              "aoaoga a Keriso—O le a toe foi mai se vaega o totoe—Faatusatusa "
              "i le Isaia 6. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua vaai Isaia", "Isaiah sees"),
            ("i le Alii—", "the Lord—"),
            ("Ua faamagaloina", "are forgiven"),
            ("agasala a Isaia—", "Isaiah's sins—"),
            ("Ua valaauina o ia", "he is called"),
            ("e vavalo atu—", "to prophesy—"),
            ("Ua ia valoia", "he prophesies"),
            ("le teena e Iutaia", "the rejection by the Jews"),
            ("o aoaoga a Keriso—", "of Christ's teachings—"),
            ("O le a toe foi mai", "will return"),
            ("se vaega o totoe—", "a remnant—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 6.", "Isaiah 6."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|17": {
        "en": "Ephraim and Syria wage war against Judah—Christ will be born of "
              "a virgin—Compare Isaiah 7. About 559–545 B.C.",
        "sm": "E si'i taua Efaraima ma Suria ia Iuta—O le a fanau mai Keriso i "
              "se taupou—Faatusatusa i le Isaia 7. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("E si'i taua", "wage war"),
            ("Efaraima ma Suria", "Ephraim and Syria"),
            ("ia Iuta—", "against Judah—"),
            ("O le a fanau mai Keriso", "Christ will be born"),
            ("i se taupou—", "of a virgin—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 7.", "Isaiah 7."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|18": {
        "en": "Christ will be as a stone of stumbling and a rock of "
              "offense—Seek the Lord, not peeping wizards—Turn to the law and "
              "to the testimony for guidance—Compare Isaiah 8. "
              "About 559–545 B.C.",
        "sm": "O le a avea Keriso e pei o se maa tu'ia ma se papa "
              "faatausuai—Ia saili i le Alii, a e lē o taulaitu vavalo—Liliu "
              "atu i le tulafono ma le molimau mo le taitaiga—Faatusatusa i le "
              "Isaia 8. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le a avea Keriso", "Christ will be"),
            ("e pei o", "as"),
            ("se maa tu'ia", "a stone of stumbling"),
            ("ma se papa faatausuai—", "and a rock of offense—"),
            ("Ia saili i le Alii,", "Seek the Lord,"),
            ("a e lē o", "not"),
            ("taulaitu vavalo—", "peeping wizards—"),
            ("Liliu atu", "Turn"),
            ("i le tulafono", "to the law"),
            ("ma le molimau", "and to the testimony"),
            ("mo le taitaiga—", "for guidance—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 8.", "Isaiah 8."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|19": {
        "en": "Isaiah speaks messianically—The people in darkness will see a "
              "great light—Unto us a child is born—He will be the Prince of "
              "Peace and will reign on David's throne—Compare Isaiah 9. "
              "About 559–545 B.C.",
        "sm": "Ua tautala Isaia faaMesia—O le a vaai tagata ua i le pouliuli i "
              "se malamalama tele—Ua fanau mai mo i tatou se tama—O le a avea o "
              "ia ma Aloalii o le Filemu ma o le a nofotupu i le nofoalii o "
              "Tavita—Faatusatusa i le Isaia 9. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua tautala Isaia", "Isaiah speaks"),
            ("faaMesia—", "messianically—"),
            ("O le a vaai tagata", "the people will see"),
            ("ua i le pouliuli", "in darkness"),
            ("i se malamalama tele—", "a great light—"),
            ("Ua fanau mai", "is born"),
            ("mo i tatou", "unto us"),
            ("se tama—", "a child—"),
            ("O le a avea o ia", "he will be"),
            ("ma Aloalii o le Filemu", "the Prince of Peace"),
            ("ma o le a nofotupu", "and will reign"),
            ("i le nofoalii o Tavita—", "on David's throne—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 9.", "Isaiah 9."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|20": {
        "en": "The destruction of Assyria is a type of the destruction of the "
              "wicked at the Second Coming—Few people will be left after the "
              "Lord comes again—The remnant of Jacob will return in that "
              "day—Compare Isaiah 10. About 559–545 B.C.",
        "sm": "O le faaumatiaga o Asuria o se faatusa o le faaumatiaga o e "
              "amioleaga i le taimi o le Afio Mai Faalua—E toaitiiti tagata o "
              "le a totoe pe a mavae le toe afio mai o le Alii—O le a toe foi "
              "mai i lena aso le vaega o totoe o Iakopo—Faatusatusa i le Isaia "
              "10. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le faaumatiaga o Asuria", "The destruction of Assyria"),
            ("o se faatusa", "is a type"),
            ("o le faaumatiaga", "of the destruction"),
            ("o e amioleaga", "of the wicked"),
            ("i le taimi", "at the time"),
            ("o le Afio Mai Faalua—", "of the Second Coming—"),
            ("E toaitiiti tagata", "Few people"),
            ("o le a totoe", "will be left"),
            ("pe a mavae", "after"),
            ("le toe afio mai", "comes again"),
            ("o le Alii—", "of the Lord—"),
            ("O le a toe foi mai", "will return"),
            ("i lena aso", "in that day"),
            ("le vaega o totoe", "the remnant"),
            ("o Iakopo—", "of Jacob—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 10.", "Isaiah 10."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|1": {
        "en": "Lehi prophesies of a land of liberty—His seed will be scattered "
              "and smitten if they reject the Holy One of Israel—He exhorts his "
              "sons to put on the armor of righteousness. About 588–570 B.C.",
        "sm": "Ua vavalo Liae e uiga i se laueleele o le saolotoga—O le a "
              "faataapeapeina ma fasia ana fanau pe afai latou te teena le Paia "
              "e Toatasi o Isaraelu—Ua ia apoapoai i ona atalii ia oofu i le "
              "ofutau o le amiotonu. E tusa o le 588–570 T.L.M.",
        "cells": [
            ("Ua vavalo Liae", "Lehi prophesies"),
            ("e uiga i", "of"),
            ("se laueleele o le saolotoga—", "a land of liberty—"),
            ("O le a faataapeapeina", "will be scattered"),
            ("ma fasia", "and smitten"),
            ("ana fanau", "his seed"),
            ("pe afai latou te teena", "if they reject"),
            ("le Paia e Toatasi", "the Holy One"),
            ("o Isaraelu—", "of Israel—"),
            ("Ua ia apoapoai", "he exhorts"),
            ("i ona atalii", "his sons"),
            ("ia oofu", "to put on"),
            ("i le ofutau", "the armor"),
            ("o le amiotonu.", "of righteousness."),
            ("E tusa o le", "about"),
            ("588–570", "588–570"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|21": {
        "en": "The stem of Jesse (Christ) will judge in righteousness—The "
              "knowledge of God will cover the earth in the Millennium—The Lord "
              "will raise an ensign and gather Israel—Compare Isaiah 11. "
              "About 559–545 B.C.",
        "sm": "O le pogai o Iese (Keriso) o le a faamasino ma le amiotonu—O le "
              "malamalama i le Atua o le a ufitia ai le lalolagi i le "
              "Meleniuma—O le a sisi i luga e le Alii se tagavai ma faapotopoto "
              "Isaraelu—Faatusatusa i le Isaia 11. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le pogai o Iese", "The stem of Jesse"),
            ("(Keriso)", "(Christ)"),
            ("o le a faamasino", "will judge"),
            ("ma le amiotonu—", "in righteousness—"),
            ("O le malamalama", "The knowledge"),
            ("i le Atua", "of God"),
            ("o le a ufitia ai", "will cover"),
            ("le lalolagi", "the earth"),
            ("i le Meleniuma—", "in the Millennium—"),
            ("O le a sisi i luga", "will raise"),
            ("e le Alii", "the Lord"),
            ("se tagavai", "an ensign"),
            ("ma faapotopoto", "and gather"),
            ("Isaraelu—", "Israel—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 11.", "Isaiah 11."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|22": {
        "en": "In the millennial day all men will praise the Lord—He will "
              "dwell among them—Compare Isaiah 12. About 559–545 B.C.",
        "sm": "I le aso o le Meleniuma o le a vivii ai tagata uma i le Alii—O "
              "le a afio o ia faatasi ma i latou—Faatusatusa i le Isaia 12. E "
              "tusa o le 559–545 T.L.M.",
        "cells": [
            ("I le aso", "In the day"),
            ("o le Meleniuma", "of the Millennium"),
            ("o le a vivii ai", "will praise"),
            ("tagata uma", "all men"),
            ("i le Alii—", "the Lord—"),
            ("O le a afio o ia", "He will dwell"),
            ("faatasi ma i latou—", "among them—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 12.", "Isaiah 12."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|23": {
        "en": "The destruction of Babylon is a type of the destruction at the "
              "Second Coming—It will be a day of wrath and vengeance—Babylon "
              "(the world) will fall forever—Compare Isaiah 13. "
              "About 559–545 B.C.",
        "sm": "O le faaumatiaga o Papelonia o se faatusa o le faaumatiaga i le "
              "taimi o le Afio Mai Faalua—O le a avea o se aso o le toasa ma le "
              "tauimasui—O Papelonia (le lalolagi) o le a pa'ū e "
              "faavavau—Faatusatusa i le Isaia 13. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le faaumatiaga o Papelonia", "The destruction of Babylon"),
            ("o se faatusa", "is a type"),
            ("o le faaumatiaga", "of the destruction"),
            ("i le taimi", "at the time"),
            ("o le Afio Mai Faalua—", "of the Second Coming—"),
            ("O le a avea", "It will be"),
            ("o se aso", "a day"),
            ("o le toasa", "of wrath"),
            ("ma le tauimasui—", "and vengeance—"),
            ("O Papelonia", "Babylon"),
            ("(le lalolagi)", "(the world)"),
            ("o le a pa'ū", "will fall"),
            ("e faavavau—", "forever—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 13.", "Isaiah 13."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|24": {
        "en": "Israel will be gathered and will enjoy millennial rest—Lucifer "
              "was cast out of heaven for rebellion—Israel will triumph over "
              "Babylon (the world)—Compare Isaiah 14. About 559–545 B.C.",
        "sm": "O le a faapotopotoina Isaraelu ma o le a fiafia i le malologa "
              "faameleniuma—Sa tuli ese Lusifelo mai le lagi ona o le "
              "fouvale—O le a manumalo Isaraelu ia Papelonia (le "
              "lalolagi)—Faatusatusa i le Isaia 14. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le a faapotopotoina", "will be gathered"),
            ("Isaraelu", "Israel"),
            ("ma o le a fiafia", "and will enjoy"),
            ("i le malologa faameleniuma—", "millennial rest—"),
            ("Sa tuli ese Lusifelo", "Lucifer was cast out"),
            ("mai le lagi", "of heaven"),
            ("ona o le fouvale—", "for rebellion—"),
            ("O le a manumalo", "will triumph"),
            ("Isaraelu", "Israel"),
            ("ia Papelonia", "over Babylon"),
            ("(le lalolagi)—", "(the world)—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 14.", "Isaiah 14."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|25": {
        "en": "Nephi glories in plainness—Isaiah's prophecies will be "
              "understood in the last days—The Jews will return from Babylon, "
              "crucify the Messiah, and be scattered and scourged—They will be "
              "restored when they believe in the Messiah—He will first come six "
              "hundred years after Lehi left Jerusalem—The Nephites keep the "
              "law of Moses and believe in Christ, who is the Holy One of "
              "Israel. About 559–545 B.C.",
        "sm": "Ua fiafia Nifae i le manino—O valoaga a Isaia o le a malamalama i "
              "aso e gata ai—O le a toe foi mai tagata Iutaia mai Papelonia, "
              "faasatauro le Mesia, ma faataapeapeina ma sasaina i latou—O le a "
              "toefuataiina i latou pe a latou talitonu i le Mesia—O le a afio "
              "mai o ia i le taimi muamua pe a mavae le ono selau tausaga talu "
              "ona tuua e Liae Ierusalema—Ua tausia e sa Nifaē tulafono a Mose "
              "ma talitonu ia Keriso, o lē o le Paia e Toatasi o Isaraelu. E "
              "tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua fiafia Nifae", "Nephi glories"),
            ("i le manino—", "in plainness—"),
            ("O valoaga a Isaia", "Isaiah's prophecies"),
            ("o le a malamalama", "will be understood"),
            ("i aso e gata ai—", "in the last days—"),
            ("O le a toe foi mai", "will return"),
            ("tagata Iutaia", "the Jews"),
            ("mai Papelonia,", "from Babylon,"),
            ("faasatauro le Mesia,", "crucify the Messiah,"),
            ("ma faataapeapeina ma sasaina", "and be scattered and scourged"),
            ("i latou—", "them—"),
            ("O le a toefuataiina", "They will be restored"),
            ("i latou", "them"),
            ("pe a latou talitonu", "when they believe"),
            ("i le Mesia—", "in the Messiah—"),
            ("O le a afio mai o ia", "He will come"),
            ("i le taimi muamua", "first"),
            ("pe a mavae", "after"),
            ("le ono selau tausaga", "six hundred years"),
            ("talu ona tuua e Liae", "Lehi left"),
            ("Ierusalema—", "Jerusalem—"),
            ("Ua tausia e sa Nifaē", "The Nephites keep"),
            ("tulafono a Mose", "the law of Moses"),
            ("ma talitonu", "and believe"),
            ("ia Keriso,", "in Christ,"),
            ("o lē", "who"),
            ("o le Paia e Toatasi", "is the Holy One"),
            ("o Isaraelu.", "of Israel."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|26": {
        "en": "Christ will minister to the Nephites—Nephi foresees the "
              "destruction of his people—They will speak from the dust—The "
              "Gentiles will build up false churches and secret "
              "combinations—The Lord forbids men to practice priestcrafts. "
              "About 559–545 B.C.",
        "sm": "O le a auauna atu Keriso ia sa Nifaē—Ua vaai Nifae i le faafanoga "
              "o ona tagata—O le a tautatala mai i latou mai le efuefu—O le a "
              "fausia a'e e Nuuese ekalesia pepelo ma faapotopotoga "
              "faalilolilo—Ua poloaiina e le Alii tagata e taofia ona faia o "
              "taulaga pepelo. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le a auauna atu Keriso", "Christ will minister"),
            ("ia sa Nifaē—", "to the Nephites—"),
            ("Ua vaai Nifae", "Nephi foresees"),
            ("i le faafanoga", "the destruction"),
            ("o ona tagata—", "of his people—"),
            ("O le a tautatala mai", "will speak"),
            ("i latou", "they"),
            ("mai le efuefu—", "from the dust—"),
            ("O le a fausia a'e", "will build up"),
            ("e Nuuese", "the Gentiles"),
            ("ekalesia pepelo", "false churches"),
            ("ma faapotopotoga faalilolilo—", "and secret combinations—"),
            ("Ua poloaiina e le Alii", "The Lord forbids"),
            ("tagata", "men"),
            ("e taofia", "to refrain"),
            ("ona faia o taulaga pepelo.", "from practicing priestcrafts."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|27": {
        "en": "Darkness and apostasy will cover the earth in the last days—The "
              "Book of Mormon will come forth—Three witnesses will testify of "
              "the book—The learned man will say he cannot read the sealed "
              "book—The Lord will do a marvelous work and a wonder—Compare "
              "Isaiah 29. About 559–545 B.C.",
        "sm": "O le a ufitia le lalolagi i le pogisa ma le liliuese i aso e gata "
              "ai—O le a oo mai le Tusi a Mamona—E toatolu molimau o le a "
              "molimau i le tusi—O le a fai mai le tagata ua aoaoina e lē mafai "
              "ona ia faitauina le tusi ua faamauina—O le a faia e le Alii se "
              "galuega ofoofogia ma le mea e ofo ai—Faatusatusa i le Isaia 29. "
              "E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le a ufitia le lalolagi", "will cover the earth"),
            ("i le pogisa", "with darkness"),
            ("ma le liliuese", "and apostasy"),
            ("i aso e gata ai—", "in the last days—"),
            ("O le a oo mai", "will come forth"),
            ("le Tusi a Mamona—", "the Book of Mormon—"),
            ("E toatolu molimau", "Three witnesses"),
            ("o le a molimau", "will testify"),
            ("i le tusi—", "of the book—"),
            ("O le a fai mai", "will say"),
            ("le tagata ua aoaoina", "the learned man"),
            ("e lē mafai ona", "cannot"),
            ("ia faitauina", "he read"),
            ("le tusi ua faamauina—", "the sealed book—"),
            ("O le a faia e le Alii", "The Lord will do"),
            ("se galuega ofoofogia", "a marvelous work"),
            ("ma le mea", "and a thing"),
            ("e ofo ai—", "of wonder—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 29.", "Isaiah 29."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|28": {
        "en": "Many false churches will be built up in the last days—They will "
              "teach false, vain, and foolish doctrines—Apostasy will abound "
              "because of false teachers—The devil will rage in the hearts of "
              "men—He will teach all manner of false doctrines. "
              "About 559–545 B.C.",
        "sm": "E tele ekalesia sese o le a ati a'e i aso e gata ai—O le a latou "
              "aoao atu mataupu faavae sese, lē aoga, ma valea—O le a tele le "
              "liliuese ona o aoao pepelo—O le a sasao le tiapolo i loto o "
              "tagata—O le a aoao atu e ia ituaiga uma o mataupu faavae sese. E "
              "tusa o le 559–545 T.L.M.",
        "cells": [
            ("E tele ekalesia sese", "Many false churches"),
            ("o le a ati a'e", "will be built up"),
            ("i aso e gata ai—", "in the last days—"),
            ("O le a latou aoao atu", "They will teach"),
            ("mataupu faavae sese,", "false doctrines,"),
            ("lē aoga,", "vain,"),
            ("ma valea—", "and foolish—"),
            ("O le a tele le liliuese", "Apostasy will abound"),
            ("ona o aoao pepelo—", "because of false teachers—"),
            ("O le a sasao le tiapolo", "The devil will rage"),
            ("i loto o tagata—", "in the hearts of men—"),
            ("O le a aoao atu e ia", "He will teach"),
            ("ituaiga uma", "all manner"),
            ("o mataupu faavae sese.", "of false doctrines."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|29": {
        "en": "Many Gentiles will reject the Book of Mormon—They will say, We "
              "need no more Bible—The Lord speaks to many nations—He will judge "
              "the world out of the books which will be written. "
              "About 559–545 B.C.",
        "sm": "E toatele Nuuese o le a teena le Tusi a Mamona—O le a latou fai "
              "mai, Matou te lē manaomia se isi Tusi Paia—E fetalai le Alii i "
              "atunuu e tele—O le a faamasino e ia le lalolagi mai tusi o le a "
              "tusia. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("E toatele Nuuese", "Many Gentiles"),
            ("o le a teena", "will reject"),
            ("le Tusi a Mamona—", "the Book of Mormon—"),
            ("O le a latou fai mai,", "They will say,"),
            ("Matou te lē manaomia", "We need no"),
            ("se isi Tusi Paia—", "more Bible—"),
            ("E fetalai le Alii", "The Lord speaks"),
            ("i atunuu e tele—", "to many nations—"),
            ("O le a faamasino e ia", "He will judge"),
            ("le lalolagi", "the world"),
            ("mai tusi", "out of the books"),
            ("o le a tusia.", "which will be written."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|30": {
        "en": "Converted Gentiles will be numbered with the covenant "
              "people—Many Lamanites and Jews will believe the word and become "
              "delightsome—Israel will be restored and the wicked destroyed. "
              "About 559–545 B.C.",
        "sm": "O le a faitauina faatasi ma tagata o le feagaiga o Nuuese e "
              "liliu mai—E toatele sa Lamanā ma tagata Iutaia o le a talitonu i "
              "le upu ma avea ma tagata moomia—O le a toefuatai Isaraelu ma "
              "faaumatia e amioleaga. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("O le a faitauina faatasi", "will be numbered"),
            ("ma tagata o le feagaiga", "with the covenant people"),
            ("o Nuuese e liliu mai—", "Converted Gentiles—"),
            ("E toatele sa Lamanā", "Many Lamanites"),
            ("ma tagata Iutaia", "and Jews"),
            ("o le a talitonu", "will believe"),
            ("i le upu", "the word"),
            ("ma avea ma tagata moomia—", "and become delightsome—"),
            ("O le a toefuatai Isaraelu", "Israel will be restored"),
            ("ma faaumatia e amioleaga.", "and the wicked destroyed."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|31": {
        "en": "Nephi tells why Christ was baptized—Men must follow Christ, be "
              "baptized, receive the Holy Ghost, and endure to the end to be "
              "saved—Repentance and baptism are the gate to the strait and "
              "narrow path—Eternal life comes to those who keep the "
              "commandments after baptism. About 559–545 B.C.",
        "sm": "Ua faamatala mai e Nifae le pogai na papatiso ai Keriso—E ao i "
              "tagata ona mulimuli atu ia Keriso, ma papatiso, maua le Agaga "
              "Paia, ma tumau e oo i le iuga ina ia faaolaina—O le salamo ma le "
              "papatisoga o le faitotoa lea i le ala lauitiiti ma le "
              "vaapiapi—E oo mai le ola e faavavau ia i latou o e e tausia "
              "poloaiga pe a uma ona papatiso. E tusa o le 559–545 T.L.M.",
        "cells": [
            ("Ua faamatala mai e Nifae", "Nephi tells"),
            ("le pogai", "why"),
            ("na papatiso ai Keriso—", "Christ was baptized—"),
            ("E ao i tagata", "Men must"),
            ("ona mulimuli atu", "follow"),
            ("ia Keriso,", "Christ,"),
            ("ma papatiso,", "be baptized,"),
            ("maua le Agaga Paia,", "receive the Holy Ghost,"),
            ("ma tumau", "and endure"),
            ("e oo i le iuga", "to the end"),
            ("ina ia faaolaina—", "to be saved—"),
            ("O le salamo", "Repentance"),
            ("ma le papatisoga", "and baptism"),
            ("o le faitotoa lea", "are the gate"),
            ("i le ala lauitiiti", "to the strait path"),
            ("ma le vaapiapi—", "and narrow—"),
            ("E oo mai", "comes"),
            ("le ola e faavavau", "eternal life"),
            ("ia i latou", "to those"),
            ("o e e tausia poloaiga", "who keep the commandments"),
            ("pe a uma ona papatiso.", "after baptism."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|32": {
        "en": "Angels speak by the power of the Holy Ghost—Men must pray and "
              "gain knowledge for themselves from the Holy Ghost. "
              "About 559–545 B.C.",
        "sm": "E tautatala agelu i le mana o le Agaga Paia—E tatau i tagata ona "
              "tatalo ma maua le malamalama mo i latou lava mai le Agaga Paia. "
              "E tusa o le 559–545 T.L.M.",
        "cells": [
            ("E tautatala agelu", "Angels speak"),
            ("i le mana", "by the power"),
            ("o le Agaga Paia—", "of the Holy Ghost—"),
            ("E tatau i tagata", "Men must"),
            ("ona tatalo", "pray"),
            ("ma maua le malamalama", "and gain knowledge"),
            ("mo i latou lava", "for themselves"),
            ("mai le Agaga Paia.", "from the Holy Ghost."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "2nephi|33": {
        "en": "Nephi's words are true—They testify of Christ—Those who believe "
              "in Christ will believe Nephi's words, which will stand as a "
              "witness before the judgment bar. About 559–545 B.C.",
        "sm": "Ua moni upu a Nifae—Ua latou molimau ia Keriso—O i latou o e e "
              "talitonu ia Keriso o le a talitonu i upu a Nifae, ia o le a tutu "
              "e avea ma molimau i luma o le pa faamasino. E tusa o le 559–545 "
              "T.L.M.",
        "cells": [
            ("Ua moni upu a Nifae—", "Nephi's words are true—"),
            ("Ua latou molimau", "They testify"),
            ("ia Keriso—", "of Christ—"),
            ("O i latou", "Those"),
            ("o e e talitonu", "who believe"),
            ("ia Keriso", "in Christ"),
            ("o le a talitonu", "will believe"),
            ("i upu a Nifae,", "Nephi's words,"),
            ("ia o le a tutu", "which will stand"),
            ("e avea ma molimau", "as a witness"),
            ("i luma o", "before"),
            ("le pa faamasino.", "the judgment bar."),
            ("E tusa o le", "about"),
            ("559–545", "559–545"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|1": {
        "en": "Jacob and Joseph seek to persuade men to believe in Christ and "
              "keep His commandments—Nephi dies—Wickedness prevails among the "
              "Nephites. About 544–421 B.C.",
        "sm": "Ua saili Iakopo ma Iosefa e faatauanau tagata ia talitonu ia "
              "Keriso ma tausi i Ana poloaiga—Ua maliu Nifae—Ua faateleina le "
              "amioleaga i totonu o sa Nifaē. E tusa o le 544–421 T.L.M.",
        "cells": [
            ("Ua saili", "seek"),
            ("Iakopo ma Iosefa", "Jacob and Joseph"),
            ("e faatauanau tagata", "to persuade men"),
            ("ia talitonu ia Keriso", "to believe in Christ"),
            ("ma tausi", "and keep"),
            ("i Ana poloaiga—", "His commandments—"),
            ("Ua maliu Nifae—", "Nephi dies—"),
            ("Ua faateleina", "prevails"),
            ("le amioleaga", "wickedness"),
            ("i totonu o sa Nifaē.", "among the Nephites."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|2": {
        "en": "Jacob denounces the love of riches, pride, and unchastity—Men "
              "may seek riches to help their fellowmen—The Lord commands that "
              "no man among the Nephites may have more than one wife—The Lord "
              "delights in the chastity of women. About 544–421 B.C.",
        "sm": "Ua ta'uleaga e Iakopo le naunau i 'oa, le faamaualuga, ma le ola "
              "lē mamā—E mafai e tagata ona saili le 'oa e fesoasoani ai i o "
              "latou uso-a-tagata—Ua poloai le Alii ina ia leai se alii i sa "
              "Nifaē e mafai ona sili atu i le tasi le avā—Ua fiafia le Alii i "
              "le ola mamā o fafine. E tusa o le 544–421 T.L.M.",
        "cells": [
            ("Ua ta'uleaga e Iakopo", "Jacob denounces"),
            ("le naunau i 'oa,", "the love of riches,"),
            ("le faamaualuga,", "pride,"),
            ("ma le ola lē mamā—", "and unchastity—"),
            ("E mafai e tagata", "Men may"),
            ("ona saili le 'oa", "seek riches"),
            ("e fesoasoani ai", "to help"),
            ("i o latou uso-a-tagata—", "their fellowmen—"),
            ("Ua poloai le Alii", "The Lord commands"),
            ("ina ia leai se alii", "that no man"),
            ("i sa Nifaē", "among the Nephites"),
            ("e mafai ona sili atu", "may have more"),
            ("i le tasi le avā—", "than one wife—"),
            ("Ua fiafia le Alii", "The Lord delights"),
            ("i le ola mamā", "in the chastity"),
            ("o fafine.", "of women."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|3": {
        "en": "The pure in heart receive the pleasing word of God—Lamanite "
              "righteousness exceeds that of the Nephites—Jacob warns against "
              "fornication, lasciviousness, and every sin. About 544–421 B.C.",
        "sm": "E talia e e loto mamā le afioga fimalie a le Atua—Ua sili atu le "
              "amiotonu o sa Lamanā i lo sa Nifaē—Ua lapatai atu Iakopo e "
              "faasaga i le faitaaga, mataaitu, ma isi agasala uma. E tusa o le "
              "544–421 T.L.M.",
        "cells": [
            ("E talia", "receive"),
            ("e e loto mamā", "the pure in heart"),
            ("le afioga fimalie", "the pleasing word"),
            ("a le Atua—", "of God—"),
            ("Ua sili atu le amiotonu", "righteousness exceeds"),
            ("o sa Lamanā", "of the Lamanites"),
            ("i lo sa Nifaē—", "that of the Nephites—"),
            ("Ua lapatai atu Iakopo", "Jacob warns"),
            ("e faasaga i le faitaaga,", "against fornication,"),
            ("mataaitu,", "lasciviousness,"),
            ("ma isi agasala uma.", "and every sin."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|4": {
        "en": "All the prophets worshiped the Father in the name of "
              "Christ—Abraham's offering of Isaac was in similitude of God and "
              "His Only Begotten—Men should reconcile themselves to God through "
              "the Atonement—The Jews will reject the foundation stone. "
              "About 544–421 B.C.",
        "sm": "Sa tapuai atu perofeta uma i le Tamā i le suafa o Keriso—O le "
              "tuuina atu o Isaako e Aperaamo o le faatusa lea o le Atua ma Lona "
              "Alo e Toatasi na Fanaua—E tatau ona faaleleia e tagata i latou "
              "lava ma le Atua e ala i le Togiola—O le a teena e tagata Iutaia "
              "le maa faavae. E tusa o le 544–421 T.L.M.",
        "cells": [
            ("Sa tapuai atu perofeta uma", "All the prophets worshiped"),
            ("i le Tamā", "the Father"),
            ("i le suafa o Keriso—", "in the name of Christ—"),
            ("O le tuuina atu", "The offering"),
            ("o Isaako", "of Isaac"),
            ("e Aperaamo", "by Abraham"),
            ("o le faatusa lea", "was in similitude"),
            ("o le Atua", "of God"),
            ("ma Lona Alo", "and His Son"),
            ("e Toatasi na Fanaua—", "the Only Begotten—"),
            ("E tatau ona faaleleia", "should reconcile"),
            ("e tagata", "men"),
            ("i latou lava", "themselves"),
            ("ma le Atua", "to God"),
            ("e ala i le Togiola—", "through the Atonement—"),
            ("O le a teena e tagata Iutaia", "The Jews will reject"),
            ("le maa faavae.", "the foundation stone."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|5": {
        "en": "Jacob quotes Zenos relative to the allegory of the tame and wild "
              "olive trees—They are a likeness of Israel and the Gentiles—The "
              "scattering and gathering of Israel are prefigured—Allusions are "
              "made to the Nephites and Lamanites and all the house of "
              "Israel—The Gentiles will be grafted into Israel—Eventually the "
              "vineyard will be burned. About 544–421 B.C.",
        "sm": "Ua sii mai e Iakopo upu a Senosa e uiga i le talafaatusa i le "
              "olive fanua ma le olive vao—Ua faatusa ia laau ia Isaraelu ma "
              "Nuuese—Ua faaataata mai le faataapeapeina ma le faapotopotoina o "
              "Isaraelu—Ua faia ni talafaatatau e uiga i sa Nifaē ma sa Lamanā "
              "ma le aiga uma o Isaraelu—O le a sulu Nuuese ia Isaraelu—E oo "
              "lava ina susunuina le togāolive. E tusa o le 544–421 T.L.M.",
        "cells": [
            ("Ua sii mai e Iakopo", "Jacob quotes"),
            ("upu a Senosa", "Zenos"),
            ("e uiga i le talafaatusa", "relative to the allegory"),
            ("i le olive fanua", "of the tame olive tree"),
            ("ma le olive vao—", "and wild olive—"),
            ("Ua faatusa ia laau", "They are a likeness"),
            ("ia Isaraelu ma Nuuese—", "of Israel and the Gentiles—"),
            ("Ua faaataata mai", "are prefigured"),
            ("le faataapeapeina", "the scattering"),
            ("ma le faapotopotoina", "and gathering"),
            ("o Isaraelu—", "of Israel—"),
            ("Ua faia ni talafaatatau", "Allusions are made"),
            ("e uiga i sa Nifaē", "to the Nephites"),
            ("ma sa Lamanā", "and Lamanites"),
            ("ma le aiga uma", "and all the house"),
            ("o Isaraelu—", "of Israel—"),
            ("O le a sulu Nuuese", "The Gentiles will be grafted"),
            ("ia Isaraelu—", "into Israel—"),
            ("E oo lava ina susunuina", "Eventually will be burned"),
            ("le togāolive.", "the vineyard."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|6": {
        "en": "The Lord will recover Israel in the last days—The world will be "
              "burned with fire—Men must follow Christ to avoid the lake of "
              "fire and brimstone. About 544–421 B.C.",
        "sm": "O le a toe faapotopoto e le Alii ia Isaraelu i aso e gata ai—O "
              "le a susunuina le lalolagi i le afi—E ao i tagata ona mulimuli "
              "ia Keriso e aloese ai mai le lepa afi ma le teio. E tusa o le "
              "544–421 T.L.M.",
        "cells": [
            ("O le a toe faapotopoto", "will recover"),
            ("e le Alii", "the Lord"),
            ("ia Isaraelu", "Israel"),
            ("i aso e gata ai—", "in the last days—"),
            ("O le a susunuina le lalolagi", "The world will be burned"),
            ("i le afi—", "with fire—"),
            ("E ao i tagata", "Men must"),
            ("ona mulimuli ia Keriso", "follow Christ"),
            ("e aloese ai", "to avoid"),
            ("mai le lepa afi", "the lake of fire"),
            ("ma le teio.", "and brimstone."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jacob|7": {
        "en": "Sherem denies Christ, contends with Jacob, demands a sign, and "
              "is smitten of God—All of the prophets have spoken of Christ and "
              "His Atonement—The Nephites lived out their days as wanderers, "
              "born in tribulation, and hated by the Lamanites. "
              "About 544–421 B.C.",
        "sm": "Ua faafitia e Serema le Keriso, ma finau ma Iakopo, ma manao i "
              "se faailoga, ma ua taia e le Atua—Ua fetalai mai perofeta uma "
              "lava e uiga ia Keriso ma Lana Togiola—Ua ola tagata sa Nifaē i o "
              "latou aso uma e pei o ni tagata maumausolo, na fananau mai i "
              "puapuaga, ma itagia e sa Lamanā. E tusa o le 544–421 T.L.M.",
        "cells": [
            ("Ua faafitia e Serema", "Sherem denies"),
            ("le Keriso,", "Christ,"),
            ("ma finau ma Iakopo,", "contends with Jacob,"),
            ("ma manao i se faailoga,", "demands a sign,"),
            ("ma ua taia", "and is smitten"),
            ("e le Atua—", "of God—"),
            ("Ua fetalai mai", "have spoken"),
            ("perofeta uma lava", "all the prophets"),
            ("e uiga ia Keriso", "of Christ"),
            ("ma Lana Togiola—", "and His Atonement—"),
            ("Ua ola tagata sa Nifaē", "The Nephites lived"),
            ("i o latou aso uma", "out their days"),
            ("e pei o", "as"),
            ("ni tagata maumausolo,", "wanderers,"),
            ("na fananau mai i puapuaga,", "born in tribulation,"),
            ("ma itagia e sa Lamanā.", "and hated by the Lamanites."),
            ("E tusa o le", "about"),
            ("544–421", "544–421"),
            ("T.L.M.", "B.C."),
        ],
    },
    "enos|1": {
        "en": "Enos prays mightily and gains a remission of his sins—The voice "
              "of the Lord comes into his mind, promising salvation for the "
              "Lamanites in a future day—The Nephites sought to reclaim the "
              "Lamanites—Enos rejoices in his Redeemer. About 420 B.C.",
        "sm": "Ua tatalo faatauanau Enosa ma ua maua e ia se faamagaloga o ana "
              "agasala—Ua oo mai le siufofoga o le Alii i lona mafaufau, ua "
              "folafola mai ai le olataga mo sa Lamanā i se aso lumanai—Ua "
              "saili sa Nifaē e toe aumai sa Lamanā—Ua olioli Enosa i lona "
              "Togiola. E tusa o le 420 T.L.M.",
        "cells": [
            ("Ua tatalo faatauanau Enosa", "Enos prays mightily"),
            ("ma ua maua e ia", "and gains"),
            ("se faamagaloga o ana agasala—", "a remission of his sins—"),
            ("Ua oo mai le siufofoga", "The voice comes"),
            ("o le Alii", "of the Lord"),
            ("i lona mafaufau,", "into his mind,"),
            ("ua folafola mai ai", "promising"),
            ("le olataga", "salvation"),
            ("mo sa Lamanā", "for the Lamanites"),
            ("i se aso lumanai—", "in a future day—"),
            ("Ua saili sa Nifaē", "The Nephites sought"),
            ("e toe aumai sa Lamanā—", "to reclaim the Lamanites—"),
            ("Ua olioli Enosa", "Enos rejoices"),
            ("i lona Togiola.", "in his Redeemer."),
            ("E tusa o le", "about"),
            ("420", "420"),
            ("T.L.M.", "B.C."),
        ],
    },
    "jarom|1": {
        "en": "The Nephites keep the law of Moses, look forward to the coming "
              "of Christ, and prosper in the land—Many prophets labor to keep "
              "the people in the way of truth. About 399–361 B.C.",
        "sm": "Ua tausia e sa Nifaē le tulafono a Mose, ua latou tulimatai atu "
              "i le afio mai o Keriso, ma ua manuia i le laueleele—E toatele "
              "perofeta ua galulue e tausia le nuu i le ala o le upumoni. E "
              "tusa o le 399–361 T.L.M.",
        "cells": [
            ("Ua tausia e sa Nifaē", "The Nephites keep"),
            ("le tulafono a Mose,", "the law of Moses,"),
            ("ua latou tulimatai atu", "look forward"),
            ("i le afio mai", "to the coming"),
            ("o Keriso,", "of Christ,"),
            ("ma ua manuia", "and prosper"),
            ("i le laueleele—", "in the land—"),
            ("E toatele perofeta", "Many prophets"),
            ("ua galulue", "labor"),
            ("e tausia le nuu", "to keep the people"),
            ("i le ala", "in the way"),
            ("o le upumoni.", "of truth."),
            ("E tusa o le", "about"),
            ("399–361", "399–361"),
            ("T.L.M.", "B.C."),
        ],
    },
    "omni|1": {
        "en": "Omni, Amaron, Chemish, Abinadom, and Amaleki, each in turn, keep "
              "the records—Mosiah discovers the people of Zarahemla, who came "
              "from Jerusalem in the days of Zedekiah—Mosiah is made king over "
              "them—The descendants of Mulek at Zarahemla had discovered "
              "Coriantumr, the last of the Jaredites—King Benjamin succeeds "
              "Mosiah—Men should offer their souls as an offering to Christ. "
              "About 323–130 B.C.",
        "sm": "O Ominae, Emarona, Kemiso, Apinatome, ma Amaleki, na tausia e i "
              "latou uma taitoatasi talafaamaumau—Ua maua e Mosaea le nuu o "
              "Sara'emila, o e na o mai mai Ierusalema i ona po o Setekaia—Ua "
              "avea Mosaea ma tupu ia te i latou—Ua maua e e na tupuga mai ia "
              "Moleka sa i Sara'emila, Korianetuma, le toe tagata o sa "
              "Iaretō—Ua suitulaga le Tupu o Peniamina ia Mosaea—E tatau i "
              "tagata ona tuu atu o latou agaga e fai ma taulaga ia Keriso. E "
              "tusa o le 323–130 T.L.M.",
        "cells": [
            ("O Ominae, Emarona,", "Omni, Amaron,"),
            ("Kemiso, Apinatome,", "Chemish, Abinadom,"),
            ("ma Amaleki,", "and Amaleki,"),
            ("na tausia", "keep"),
            ("e i latou uma taitoatasi", "each of them in turn"),
            ("talafaamaumau—", "the records—"),
            ("Ua maua e Mosaea", "Mosiah discovers"),
            ("le nuu o Sara'emila,", "the people of Zarahemla,"),
            ("o e na o mai", "who came"),
            ("mai Ierusalema", "from Jerusalem"),
            ("i ona po o Setekaia—", "in the days of Zedekiah—"),
            ("Ua avea Mosaea ma tupu", "Mosiah is made king"),
            ("ia te i latou—", "over them—"),
            ("Ua maua", "had discovered"),
            ("e e na tupuga mai", "by those descended"),
            ("ia Moleka", "of Mulek"),
            ("sa i Sara'emila,", "at Zarahemla,"),
            ("Korianetuma,", "Coriantumr,"),
            ("le toe tagata", "the last"),
            ("o sa Iaretō—", "of the Jaredites—"),
            ("Ua suitulaga", "succeeds"),
            ("le Tupu o Peniamina", "King Benjamin"),
            ("ia Mosaea—", "Mosiah—"),
            ("E tatau i tagata", "Men should"),
            ("ona tuu atu", "offer"),
            ("o latou agaga", "their souls"),
            ("e fai ma taulaga", "as an offering"),
            ("ia Keriso.", "to Christ."),
            ("E tusa o le", "about"),
            ("323–130", "323–130"),
            ("T.L.M.", "B.C."),
        ],
    },
    "wom|1": {
        "en": "Mormon abridges the large plates of Nephi—He puts the small "
              "plates with the other plates—King Benjamin establishes peace in "
              "the land. About A.D. 385.",
        "sm": "Ua otooto e Mamona papatusi tetele a Nifae—Ua tuu e ia papatusi "
              "laiti faatasi ma isi papatusi—Ua faatupuina e le Tupu o Peniamina "
              "le filemu i le laueleele. E tusa o le 385 T.A.",
        "cells": [
            ("Ua otooto e Mamona", "Mormon abridges"),
            ("papatusi tetele a Nifae—", "the large plates of Nephi—"),
            ("Ua tuu e ia", "He puts"),
            ("papatusi laiti", "the small plates"),
            ("faatasi ma isi papatusi—", "with the other plates—"),
            ("Ua faatupuina", "establishes"),
            ("e le Tupu o Peniamina", "King Benjamin"),
            ("le filemu", "peace"),
            ("i le laueleele.", "in the land."),
            ("E tusa o le", "about"),
            ("385", "385"),
            ("T.A.", "A.D."),
        ],
    },
    "mosiah|1": {
        "en": "King Benjamin teaches his sons the language and prophecies of "
              "their fathers—Their religion and civilization have been "
              "preserved because of the records kept on the various "
              "plates—Mosiah is chosen as king and is given custody of the "
              "records and other things. About 130–124 B.C.",
        "sm": "Ua aoao e le Tupu o Peniamina ona atalii i le gagana ma valoaga a "
              "o latou tamā—Ua faasaoina la latou tapuaiga ma a latou "
              "tumalamalama ona o talafaamaumau sa tusia i papatusi eseese—Ua "
              "filifilia Mosaea e avea ma tupu ma ua tuu atu i ai le tausiga o "
              "talafaamaumau ma isi mea. E tusa o le 130–124 T.L.M.",
        "cells": [
            ("Ua aoao", "teaches"),
            ("e le Tupu o Peniamina", "King Benjamin"),
            ("ona atalii", "his sons"),
            ("i le gagana", "the language"),
            ("ma valoaga", "and prophecies"),
            ("a o latou tamā—", "of their fathers—"),
            ("Ua faasaoina", "have been preserved"),
            ("la latou tapuaiga", "their religion"),
            ("ma a latou tumalamalama", "and civilization"),
            ("ona o talafaamaumau", "because of the records"),
            ("sa tusia", "kept"),
            ("i papatusi eseese—", "on the various plates—"),
            ("Ua filifilia Mosaea", "Mosiah is chosen"),
            ("e avea ma tupu", "as king"),
            ("ma ua tuu atu", "and is given"),
            ("i ai", "to him"),
            ("le tausiga o talafaamaumau", "custody of the records"),
            ("ma isi mea.", "and other things."),
            ("E tusa o le", "about"),
            ("130–124", "130–124"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|2": {
        "en": "King Benjamin addresses his people—He recounts the equity, "
              "fairness, and spirituality of his reign—He counsels them to "
              "serve their Heavenly King—Those who rebel against God will "
              "suffer anguish like unquenchable fire. About 124 B.C.",
        "sm": "Ua lauga atu le Tupu o Peniamina i lona nuu—Ua toe faamatala mai "
              "e ia le tutusa, le sa'o, ma le faaleagaga o lana nofoaiga—Ua "
              "fautuaina e ia i latou ia auauna atu i lo latou Tupu Faalelagi—O "
              "i latou o e e fouvale faatautee i le Atua o le a mafatia i le "
              "mafatia e pei o le afi e lē matineia. E tusa o le 124 T.L.M.",
        "cells": [
            ("Ua lauga atu", "addresses"),
            ("le Tupu o Peniamina", "King Benjamin"),
            ("i lona nuu—", "his people—"),
            ("Ua toe faamatala mai e ia", "He recounts"),
            ("le tutusa,", "the equity,"),
            ("le sa'o,", "fairness,"),
            ("ma le faaleagaga", "and spirituality"),
            ("o lana nofoaiga—", "of his reign—"),
            ("Ua fautuaina e ia i latou", "He counsels them"),
            ("ia auauna atu", "to serve"),
            ("i lo latou Tupu Faalelagi—", "their Heavenly King—"),
            ("O i latou", "Those"),
            ("o e e fouvale faatautee", "who rebel"),
            ("i le Atua", "against God"),
            ("o le a mafatia", "will suffer"),
            ("i le mafatia", "anguish"),
            ("e pei o le afi", "like fire"),
            ("e lē matineia.", "unquenchable."),
            ("E tusa o le", "about"),
            ("124", "124"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|3": {
        "en": "King Benjamin continues his address—The Lord Omnipotent will "
              "minister among men in a tabernacle of clay—Blood will come from "
              "every pore as He atones for the sins of the world—His is the "
              "only name whereby salvation comes—Men can put off the natural "
              "man and become Saints through the Atonement—The torment of the "
              "wicked will be as a lake of fire and brimstone. About 124 B.C.",
        "sm": "Ua faaauau pea e le Tupu o Peniamina lana lauga—O le a auauna atu "
              "le Alii Mamana Aoao i totonu o tagata i se fale apitaga omea—O le "
              "a puna mai le toto mai pu afu uma a'o togiola o Ia mo agasala a "
              "le lalolagi—Ua na'o lona suafa lava e oo mai ai le olataga—E "
              "mafai e tagata ona tuu ese le tagata natura ma avea ma Tagata "
              "Paia e ala i le Togiola—O le mafatia o e amioleaga o le a pei o "
              "se lepa afi ma le teiō. E tusa o le 124 T.L.M.",
        "cells": [
            ("Ua faaauau pea", "continues"),
            ("e le Tupu o Peniamina", "King Benjamin"),
            ("lana lauga—", "his address—"),
            ("O le a auauna atu", "will minister"),
            ("le Alii Mamana Aoao", "the Lord Omnipotent"),
            ("i totonu o tagata", "among men"),
            ("i se fale apitaga omea—", "in a tabernacle of clay—"),
            ("O le a puna mai", "will come"),
            ("le toto", "Blood"),
            ("mai pu afu uma", "from every pore"),
            ("a'o togiola o Ia", "as He atones"),
            ("mo agasala a le lalolagi—", "for the sins of the world—"),
            ("Ua na'o lona suafa lava", "His is the only name"),
            ("e oo mai ai", "whereby comes"),
            ("le olataga—", "salvation—"),
            ("E mafai e tagata", "Men can"),
            ("ona tuu ese", "put off"),
            ("le tagata natura", "the natural man"),
            ("ma avea ma Tagata Paia", "and become Saints"),
            ("e ala i le Togiola—", "through the Atonement—"),
            ("O le mafatia", "The torment"),
            ("o e amioleaga", "of the wicked"),
            ("o le a pei", "will be as"),
            ("o se lepa afi", "a lake of fire"),
            ("ma le teiō.", "and brimstone."),
            ("E tusa o le", "about"),
            ("124", "124"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|4": {
        "en": "King Benjamin continues his address—Salvation comes because of "
              "the Atonement—Believe in God to be saved—Retain a remission of "
              "your sins through faithfulness—Impart of your substance to the "
              "poor—Do all things in wisdom and order. About 124 B.C.",
        "sm": "Ua faaauau pea e le Tupu o Peniamina lana lauga—E oo mai le "
              "olataga ona o le Togiola—Ia talitonu i le Atua ina ia faaolaina "
              "ai—Ia tumau i le faamagaloina o au agasala e ala i le "
              "faamaoni—Faasoa atu au mea i e matitiva—Ia fai mea uma i le poto "
              "ma le faatulagaga tatau. E tusa o le 124 T.L.M.",
        "cells": [
            ("Ua faaauau pea", "continues"),
            ("e le Tupu o Peniamina", "King Benjamin"),
            ("lana lauga—", "his address—"),
            ("E oo mai le olataga", "Salvation comes"),
            ("ona o le Togiola—", "because of the Atonement—"),
            ("Ia talitonu i le Atua", "Believe in God"),
            ("ina ia faaolaina ai—", "to be saved—"),
            ("Ia tumau", "Retain"),
            ("i le faamagaloina", "a remission"),
            ("o au agasala", "of your sins"),
            ("e ala i le faamaoni—", "through faithfulness—"),
            ("Faasoa atu au mea", "Impart of your substance"),
            ("i e matitiva—", "to the poor—"),
            ("Ia fai mea uma", "Do all things"),
            ("i le poto", "in wisdom"),
            ("ma le faatulagaga tatau.", "and order."),
            ("E tusa o le", "about"),
            ("124", "124"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|5": {
        "en": "The Saints become the sons and daughters of Christ through "
              "faith—They are then called by the name of Christ—King Benjamin "
              "exhorts them to be steadfast and immovable in good works. "
              "About 124 B.C.",
        "sm": "E avea le Au Paia ma atalii ma afafine o Keriso e ala i le "
              "faatuatua—Ona valaauina ai lea o i latou i le suafa o Keriso—Ua "
              "apoapoai atu le Tupu o Peniamina ia te i latou ia tutumau ma lē "
              "masi'i'ese mai galuega lelei. E tusa o le 124 T.L.M.",
        "cells": [
            ("E avea le Au Paia", "The Saints become"),
            ("ma atalii ma afafine", "the sons and daughters"),
            ("o Keriso", "of Christ"),
            ("e ala i le faatuatua—", "through faith—"),
            ("Ona valaauina ai lea", "They are then called"),
            ("o i latou", "them"),
            ("i le suafa o Keriso—", "by the name of Christ—"),
            ("Ua apoapoai atu", "exhorts"),
            ("le Tupu o Peniamina", "King Benjamin"),
            ("ia te i latou", "them"),
            ("ia tutumau", "to be steadfast"),
            ("ma lē masi'i'ese", "and immovable"),
            ("mai galuega lelei.", "in good works."),
            ("E tusa o le", "about"),
            ("124", "124"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|6": {
        "en": "King Benjamin records the names of the people and appoints "
              "priests to teach them—Mosiah reigns as a righteous king. "
              "About 124–121 B.C.",
        "sm": "Ua faamaumau e le Tupu o Peniamina igoa o tagata o le nuu ma "
              "tofia faitaulaga e a'oa'o i latou—Ua nofotupu Mosaea o se tupu "
              "amiotonu. E tusa o le 124–121 T.L.M.",
        "cells": [
            ("Ua faamaumau", "records"),
            ("e le Tupu o Peniamina", "King Benjamin"),
            ("igoa o tagata", "the names of the people"),
            ("o le nuu", "of the land"),
            ("ma tofia faitaulaga", "and appoints priests"),
            ("e a'oa'o i latou—", "to teach them—"),
            ("Ua nofotupu Mosaea", "Mosiah reigns"),
            ("o se tupu amiotonu.", "as a righteous king."),
            ("E tusa o le", "about"),
            ("124–121", "124–121"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|7": {
        "en": "Ammon finds the land of Lehi-Nephi, where Limhi is king—Limhi's "
              "people are in bondage to the Lamanites—Limhi recounts their "
              "history—A prophet (Abinadi) had testified that Christ is the God "
              "and Father of all things—Those who sow filthiness reap the "
              "whirlwind, and those who put their trust in the Lord will be "
              "delivered. About 121 B.C.",
        "sm": "Ua maua e Amona le nuu o Liae-Nifae, lea o loo avea ai Limae ma "
              "tupu—Ua pologa le nuu o Limae ia sa Lamanā—Ua faamatala mai e "
              "Limae lo latou talafaasolopito—Sa molimau mai se perofeta (o "
              "Apinati) o Keriso o le Atua ma le Tamā o mea uma—O i latou o e "
              "luluina le eleelea e seleseleina le asiosio, ae o i latou o e tuu "
              "atu lo latou faalagolago i le Alii o le a laveaiina. E tusa o le "
              "121 T.L.M.",
        "cells": [
            ("Ua maua e Amona", "Ammon finds"),
            ("le nuu o Liae-Nifae,", "the land of Lehi-Nephi,"),
            ("lea o loo avea ai", "where is"),
            ("Limae ma tupu—", "Limhi king—"),
            ("Ua pologa", "are in bondage"),
            ("le nuu o Limae", "Limhi's people"),
            ("ia sa Lamanā—", "to the Lamanites—"),
            ("Ua faamatala mai e Limae", "Limhi recounts"),
            ("lo latou talafaasolopito—", "their history—"),
            ("Sa molimau mai se perofeta", "A prophet had testified"),
            ("(o Apinati)", "(Abinadi)"),
            ("o Keriso o le Atua", "that Christ is the God"),
            ("ma le Tamā", "and the Father"),
            ("o mea uma—", "of all things—"),
            ("O i latou o e luluina", "Those who sow"),
            ("le eleelea", "filthiness"),
            ("e seleseleina le asiosio,", "reap the whirlwind,"),
            ("ae o i latou", "and those"),
            ("o e tuu atu", "who put"),
            ("lo latou faalagolago", "their trust"),
            ("i le Alii", "in the Lord"),
            ("o le a laveaiina.", "will be delivered."),
            ("E tusa o le", "about"),
            ("121", "121"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|8": {
        "en": "Ammon teaches the people of Limhi—He learns of the twenty-four "
              "Jaredite plates—Ancient records can be translated by seers—No "
              "gift is greater than seership. About 121 B.C.",
        "sm": "Ua aoao e Amona le nuu o Limae—Ua iloa e ia e uiga i papatusi a "
              "sa Iaretō e lua sefulu fa—E mafai ona faaliliu e tagatavāai "
              "talafaamaumau anamua—E leai se meaalofa e sili atu nai lo le "
              "tagatavāai. E tusa o le 121 T.L.M.",
        "cells": [
            ("Ua aoao e Amona", "Ammon teaches"),
            ("le nuu o Limae—", "the people of Limhi—"),
            ("Ua iloa e ia", "He learns"),
            ("e uiga i papatusi", "of the plates"),
            ("a sa Iaretō", "of the Jaredites"),
            ("e lua sefulu fa—", "twenty-four—"),
            ("E mafai ona faaliliu", "can be translated"),
            ("e tagatavāai", "by seers"),
            ("talafaamaumau anamua—", "ancient records—"),
            ("E leai se meaalofa", "No gift"),
            ("e sili atu", "is greater"),
            ("nai lo le tagatavāai.", "than seership."),
            ("E tusa o le", "about"),
            ("121", "121"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|10": {
        "en": "King Laman dies—His people are wild and ferocious and believe in "
              "false traditions—Zeniff and his people prevail against them. "
              "About 187–160 B.C.",
        "sm": "Ua oti le tupu o Lamana—Ua 'aivao ma fe'ai ma talitonu ona "
              "tagata i uputuu sese—Ua manumalo Senifa ma lona nuu e faasaga ia "
              "te i latou. E tusa o le 187–160 T.L.M.",
        "cells": [
            ("Ua oti", "dies"),
            ("le tupu o Lamana—", "King Laman—"),
            ("Ua 'aivao ma fe'ai", "are wild and ferocious"),
            ("ma talitonu ona tagata", "and his people believe"),
            ("i uputuu sese—", "in false traditions—"),
            ("Ua manumalo Senifa", "Zeniff prevails"),
            ("ma lona nuu", "and his people"),
            ("e faasaga", "against"),
            ("ia te i latou.", "them."),
            ("E tusa o le", "about"),
            ("187–160", "187–160"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|11": {
        "en": "King Noah rules in wickedness—He revels in riotous living with "
              "his wives and concubines—Abinadi prophesies that the people will "
              "be taken into bondage—His life is sought by King Noah. "
              "About 160–150 B.C.",
        "sm": "Ua pule le Tupu o Noa i le amioleaga—Ua fiafia o ia i le olaga "
              "faasoesā ma ana avā ma ana palake—Ua vavalo Apinati o le a ave le "
              "nuu e fai ma pologa—Ua sailia lona ola e le Tupu o Noa. E tusa o "
              "le 160–150 T.L.M.",
        "cells": [
            ("Ua pule", "rules"),
            ("le Tupu o Noa", "King Noah"),
            ("i le amioleaga—", "in wickedness—"),
            ("Ua fiafia o ia", "He revels"),
            ("i le olaga faasoesā", "in riotous living"),
            ("ma ana avā", "with his wives"),
            ("ma ana palake—", "and concubines—"),
            ("Ua vavalo Apinati", "Abinadi prophesies"),
            ("o le a ave le nuu", "the people will be taken"),
            ("e fai ma pologa—", "into bondage—"),
            ("Ua sailia lona ola", "His life is sought"),
            ("e le Tupu o Noa.", "by King Noah."),
            ("E tusa o le", "about"),
            ("160–150", "160–150"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|12": {
        "en": "Abinadi is imprisoned for prophesying the destruction of the "
              "people and the death of King Noah—The false priests quote the "
              "scriptures and pretend to keep the law of Moses—Abinadi begins "
              "to teach them the Ten Commandments. About 148 B.C.",
        "sm": "Ua falepuipui Apinati ona o lona vavalo atu o le faafanoga o le "
              "nuu ma le oti o le Tupu o Noa—Ua sii mai e faitaulaga pepelo "
              "tusitusiga paia ma faafoliga mai o loo latou tausia tulafono a "
              "Mose—Ua amata e Apinati ona a'oa'o atu i latou i Tulafono e "
              "Sefulu. E tusa o le 148 T.L.M.",
        "cells": [
            ("Ua falepuipui Apinati", "Abinadi is imprisoned"),
            ("ona o lona vavalo atu", "for prophesying"),
            ("o le faafanoga", "the destruction"),
            ("o le nuu", "of the people"),
            ("ma le oti", "and the death"),
            ("o le Tupu o Noa—", "of King Noah—"),
            ("Ua sii mai", "quote"),
            ("e faitaulaga pepelo", "the false priests"),
            ("tusitusiga paia", "the scriptures"),
            ("ma faafoliga mai", "and pretend"),
            ("o loo latou tausia", "to keep"),
            ("tulafono a Mose—", "the law of Moses—"),
            ("Ua amata e Apinati", "Abinadi begins"),
            ("ona a'oa'o atu i latou", "to teach them"),
            ("i Tulafono e Sefulu.", "the Ten Commandments."),
            ("E tusa o le", "about"),
            ("148", "148"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|13": {
        "en": "Abinadi is protected by divine power—He teaches the Ten "
              "Commandments—Salvation does not come by the law of Moses "
              "alone—God Himself will make an atonement and redeem His people. "
              "About 148 B.C.",
        "sm": "Ua puipuia Apinati i se mana paia—Ua aoao atu e ia Tulafono e "
              "Sefulu—E le na'o le tulafono a Mose e ala mai ai le faaolataga—O "
              "le a faia e le Atua lava Ia se togiola ma togiolaina Ona tagata. "
              "E tusa o le 148 T.L.M.",
        "cells": [
            ("Ua puipuia Apinati", "Abinadi is protected"),
            ("i se mana paia—", "by divine power—"),
            ("Ua aoao atu e ia", "He teaches"),
            ("Tulafono e Sefulu—", "the Ten Commandments—"),
            ("E le na'o", "not alone"),
            ("le tulafono a Mose", "the law of Moses"),
            ("e ala mai ai", "comes"),
            ("le faaolataga—", "salvation—"),
            ("O le a faia", "will make"),
            ("e le Atua lava Ia", "God Himself"),
            ("se togiola", "an atonement"),
            ("ma togiolaina Ona tagata.", "and redeem His people."),
            ("E tusa o le", "about"),
            ("148", "148"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|14": {
        "en": "Isaiah speaks messianically—The Messiah's humiliation and "
              "sufferings are set forth—He makes His soul an offering for sin "
              "and makes intercession for transgressors—Compare Isaiah 53.",
        "sm": "Ua tautala Isaia e uiga i le Mesia—Ua faamatala mai le "
              "faamaasiasiina ma mafatiaga o le Mesia—Ua tuu atu e Ia Lona agaga "
              "o se taulaga mo agasala ma faia le puluvaga mo e "
              "solitulafono—Faatusatusa i le Isaia 53. E tusa o le 148 T.L.M.",
        "cells": [
            ("Ua tautala Isaia", "Isaiah speaks"),
            ("e uiga i le Mesia—", "messianically—"),
            ("Ua faamatala mai", "are set forth"),
            ("le faamaasiasiina", "the humiliation"),
            ("ma mafatiaga o le Mesia—", "and sufferings of the Messiah—"),
            ("Ua tuu atu e Ia", "He makes"),
            ("Lona agaga", "His soul"),
            ("o se taulaga mo agasala", "an offering for sin"),
            ("ma faia le puluvaga", "and makes intercession"),
            ("mo e solitulafono—", "for transgressors—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 53.", "Isaiah 53."),
            ("E tusa o le", "about"),
            ("148", "148"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|9": {
        "en": "Zeniff leads a group from Zarahemla to possess the land of "
              "Lehi-Nephi—The Lamanite king permits them to inherit the "
              "land—There is war between the Lamanites and Zeniff's people. "
              "About 200–187 B.C.",
        "sm": "Ua taitai atu e Senifa se vaega o tagata mai Sara'emila e nonofo "
              "i le laueleele o Liae-Nifae—Ua faataga i latou e le tupu o sa "
              "Lamanā e fai mo o latou tofi le laueleele—Ua faia se taua i le va "
              "o sa Lamanā ma le nuu o Senifa. E tusa o le 200–187 T.L.M.",
        "cells": [
            ("Ua taitai atu e Senifa", "Zeniff leads"),
            ("se vaega o tagata", "a group"),
            ("mai Sara'emila", "from Zarahemla"),
            ("e nonofo i le laueleele", "to possess the land"),
            ("o Liae-Nifae—", "of Lehi-Nephi—"),
            ("Ua faataga i latou", "permits them"),
            ("e le tupu", "the king"),
            ("o sa Lamanā", "of the Lamanites"),
            ("e fai mo o latou tofi", "to inherit"),
            ("le laueleele—", "the land—"),
            ("Ua faia se taua", "There is war"),
            ("i le va", "between"),
            ("o sa Lamanā", "the Lamanites"),
            ("ma le nuu o Senifa.", "and Zeniff's people."),
            ("E tusa o le", "about"),
            ("200–187", "200–187"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|15": {
        "en": "How Christ is both the Father and the Son—He will make "
              "intercession and bear the transgressions of His people—They and "
              "all the holy prophets are His seed—He brings to pass the "
              "Resurrection—Little children have eternal life. About 148 B.C.",
        "sm": "O le ala ua avea ai Keriso o le Tamā ma le Alo—O le a faia e ia "
              "le 'ai'oiga ma tauave solitulafono a Ona tagata—O i latou ma "
              "perofeta paia uma lava o Ana fanau ia—Ua faataunuu e ia le "
              "Toetutu—E maua e fanau laiti le ola e faavavau. E tusa o le 148 "
              "T.L.M.",
        "cells": [
            ("O le ala", "How"),
            ("ua avea ai Keriso", "Christ is"),
            ("o le Tamā", "the Father"),
            ("ma le Alo—", "and the Son—"),
            ("O le a faia e ia", "He will make"),
            ("le 'ai'oiga", "intercession"),
            ("ma tauave solitulafono", "and bear the transgressions"),
            ("a Ona tagata—", "of His people—"),
            ("O i latou", "They"),
            ("ma perofeta paia uma lava", "and all the holy prophets"),
            ("o Ana fanau ia—", "are His seed—"),
            ("Ua faataunuu e ia", "He brings to pass"),
            ("le Toetutu—", "the Resurrection—"),
            ("E maua e fanau laiti", "Little children have"),
            ("le ola e faavavau.", "eternal life."),
            ("E tusa o le", "about"),
            ("148", "148"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|16": {
        "en": "God redeems men from their lost and fallen state—Those who are "
              "carnal remain as though there were no redemption—Christ brings "
              "to pass a resurrection to endless life or to endless damnation. "
              "About 148 B.C.",
        "sm": "E togiola e le Atua tagata mai lo latou tulaga leiloa ma le "
              "pa'ū—O i latou o e ua faaletino e tumau pea e peiseai ua leai se "
              "togiola—Ua aumai e Keriso se toetu i le ola e le gata po o i le "
              "malaia e le gata. E tusa o le 148 T.L.M.",
        "cells": [
            ("E togiola e le Atua", "God redeems"),
            ("tagata", "men"),
            ("mai lo latou tulaga leiloa", "from their lost state"),
            ("ma le pa'ū—", "and fallen—"),
            ("O i latou o e", "Those who"),
            ("ua faaletino", "are carnal"),
            ("e tumau pea", "remain"),
            ("e peiseai", "as though"),
            ("ua leai se togiola—", "there were no redemption—"),
            ("Ua aumai e Keriso", "Christ brings"),
            ("se toetu", "a resurrection"),
            ("i le ola", "to life"),
            ("e le gata", "endless"),
            ("po o i le malaia", "or to damnation"),
            ("e le gata.", "endless."),
            ("E tusa o le", "about"),
            ("148", "148"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|17": {
        "en": "Alma believes and writes the words of Abinadi—Abinadi suffers "
              "death by fire—He prophesies disease and death by fire upon his "
              "murderers. About 148 B.C.",
        "sm": "Ua talitonu Alema ma ua tusi e ia upu a Apinati—Ua mafatia "
              "Apinati i le oti i le afi—Ua valoia e ia faama'i ma le oti i le "
              "afi i luga o e na fasiotia o ia. E tusa o le 148 T.L.M.",
        "cells": [
            ("Ua talitonu Alema", "Alma believes"),
            ("ma ua tusi e ia", "and writes"),
            ("upu a Apinati—", "the words of Abinadi—"),
            ("Ua mafatia Apinati", "Abinadi suffers"),
            ("i le oti", "death"),
            ("i le afi—", "by fire—"),
            ("Ua valoia e ia", "He prophesies"),
            ("faama'i ma le oti", "disease and death"),
            ("i le afi", "by fire"),
            ("i luga o e", "upon those"),
            ("na fasiotia o ia.", "who slew him."),
            ("E tusa o le", "about"),
            ("148", "148"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|18": {
        "en": "Alma preaches in private—He sets forth the covenant of baptism "
              "and baptizes at the waters of Mormon—He organizes the Church of "
              "Christ and ordains priests—They support themselves and teach the "
              "people—Alma and his people flee from King Noah into the "
              "wilderness. About 147–145 B.C.",
        "sm": "Ua tala'i atu faalilolilo Alema—Ua faatu mai e ia le feagaiga o "
              "le papatisoga ma faia papatisoga i vai o Mamona—Ua faatulaga e ia "
              "le Ekalesia a Keriso ma faauu faitaulaga—Ua latou faalagolago ia "
              "i latou lava ma a'oa'o le nuu—Ua sosola Alema ma ona tagata i le "
              "vao mai le Tupu o Noa. E tusa o le 147–145 T.L.M.",
        "cells": [
            ("Ua tala'i atu faalilolilo Alema—", "Alma preaches in private—"),
            ("Ua faatu mai e ia", "He sets forth"),
            ("le feagaiga o le papatisoga", "the covenant of baptism"),
            ("ma faia papatisoga", "and baptizes"),
            ("i vai o Mamona—", "at the waters of Mormon—"),
            ("Ua faatulaga e ia", "He organizes"),
            ("le Ekalesia a Keriso", "the Church of Christ"),
            ("ma faauu faitaulaga—", "and ordains priests—"),
            ("Ua latou faalagolago", "They support"),
            ("ia i latou lava", "themselves"),
            ("ma a'oa'o le nuu—", "and teach the people—"),
            ("Ua sosola Alema", "Alma flees"),
            ("ma ona tagata", "and his people"),
            ("i le vao", "into the wilderness"),
            ("mai le Tupu o Noa.", "from King Noah."),
            ("E tusa o le", "about"),
            ("147–145", "147–145"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|19": {
        "en": "Gideon seeks to slay King Noah—The Lamanites invade the "
              "land—King Noah suffers death by fire—Limhi rules as a tributary "
              "monarch. About 145–121 B.C.",
        "sm": "Ua saili Kitiona e fasioti le Tupu o Noa—Ua osofaia e sa Lamanā "
              "le laueleele—Ua oti le Tupu o Noa i le afi—Ua nofotupu Limae o se "
              "monaki puleesea. E tusa o le 145–121 T.L.M.",
        "cells": [
            ("Ua saili Kitiona", "Gideon seeks"),
            ("e fasioti", "to slay"),
            ("le Tupu o Noa—", "King Noah—"),
            ("Ua osofaia e sa Lamanā", "The Lamanites invade"),
            ("le laueleele—", "the land—"),
            ("Ua oti", "suffers death"),
            ("le Tupu o Noa", "King Noah"),
            ("i le afi—", "by fire—"),
            ("Ua nofotupu Limae", "Limhi rules"),
            ("o se monaki puleesea.", "as a tributary monarch."),
            ("E tusa o le", "about"),
            ("145–121", "145–121"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|20": {
        "en": "Some Lamanite daughters are abducted by the priests of Noah—The "
              "Lamanites wage war upon Limhi and his people—The Lamanite hosts "
              "are repulsed and pacified. About 145–123 B.C.",
        "sm": "Ua ave faamalosi e faitaulaga a Noa ni isi o afafine o sa "
              "Lamanā—Ua sii taua mai sa Lamanā i luga o Limae ma lona nuu—Ua "
              "teena ma faafilemuina autau a sa Lamanā. E tusa o le 145–143 "
              "T.L.M.",
        "cells": [
            ("Ua ave faamalosi", "are abducted"),
            ("e faitaulaga a Noa", "by the priests of Noah"),
            ("ni isi o afafine", "Some daughters"),
            ("o sa Lamanā—", "of the Lamanites—"),
            ("Ua sii taua mai", "wage war"),
            ("sa Lamanā", "the Lamanites"),
            ("i luga o Limae", "upon Limhi"),
            ("ma lona nuu—", "and his people—"),
            ("Ua teena ma faafilemuina", "are repulsed and pacified"),
            ("autau a sa Lamanā.", "The Lamanite hosts."),
            ("E tusa o le", "about"),
            ("145–143", "145–143"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|21": {
        "en": "Limhi's people are smitten and defeated by the Lamanites—Limhi's "
              "people meet Ammon and are converted—They tell Ammon of the "
              "twenty-four Jaredite plates. About 122–121 B.C.",
        "sm": "Ua taia ma faatoilaloina le nuu o Limae e sa Lamanā—Ua feiloa'i "
              "le nuu o Limae ma Amona ma ua faaliliuina—Ua latou ta'u atu ia "
              "Amona e uiga i papatusi e lua sefulu fa o sa Iaretō. E tusa o le "
              "122–121 T.L.M.",
        "cells": [
            ("Ua taia ma faatoilaloina", "are smitten and defeated"),
            ("le nuu o Limae", "Limhi's people"),
            ("e sa Lamanā—", "by the Lamanites—"),
            ("Ua feiloa'i le nuu o Limae", "Limhi's people meet"),
            ("ma Amona", "Ammon"),
            ("ma ua faaliliuina—", "and are converted—"),
            ("Ua latou ta'u atu", "They tell"),
            ("ia Amona", "Ammon"),
            ("e uiga i papatusi", "of the plates"),
            ("e lua sefulu fa", "twenty-four"),
            ("o sa Iaretō.", "of the Jaredites."),
            ("E tusa o le", "about"),
            ("122–121", "122–121"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|22": {
        "en": "Plans are made for the people to escape from Lamanite "
              "bondage—The Lamanites are made drunk—The people escape, return "
              "to Zarahemla, and become subject to King Mosiah. "
              "About 121–120 B.C.",
        "sm": "Ua faia fuafuaga mo le nuu e sosola ese ai mai le pologa ia sa "
              "Lamanā—Ua faaonanā sa Lamanā—Ua sosola le nuu, ua toe foi atu i "
              "Sara'emila, ma ua i lalo o le pule a le Tupu o Mosaea. E tusa o "
              "le 121–120 T.L.M.",
        "cells": [
            ("Ua faia fuafuaga", "Plans are made"),
            ("mo le nuu", "for the people"),
            ("e sosola ese ai", "to escape"),
            ("mai le pologa", "from bondage"),
            ("ia sa Lamanā—", "to the Lamanites—"),
            ("Ua faaonanā sa Lamanā—", "The Lamanites are made drunk—"),
            ("Ua sosola le nuu,", "The people escape,"),
            ("ua toe foi atu", "return"),
            ("i Sara'emila,", "to Zarahemla,"),
            ("ma ua i lalo", "and become subject"),
            ("o le pule", "to the rule"),
            ("a le Tupu o Mosaea.", "of King Mosiah."),
            ("E tusa o le", "about"),
            ("121–120", "121–120"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|24": {
        "en": "Amulon persecutes Alma and his people—They are to be put to "
              "death if they pray—The Lord makes their burdens seem light—He "
              "delivers them from bondage, and they return to Zarahemla. "
              "About 145–120 B.C.",
        "sm": "Ua sauāina e Amulona ia Alema ma lona nuu—O le a fasiotia i latou "
              "pe a latou tatalo—Ua faia e le Alii a latou avega e pei ua "
              "māmā—Ua lavea'i e ia i latou mai le pologa, ma ua latou foi atu i "
              "Sara'emila. E tusa o le 145–120 T.L.M.",
        "cells": [
            ("Ua sauāina e Amulona", "Amulon persecutes"),
            ("ia Alema ma lona nuu—", "Alma and his people—"),
            ("O le a fasiotia i latou", "They are to be put to death"),
            ("pe a latou tatalo—", "if they pray—"),
            ("Ua faia e le Alii", "The Lord makes"),
            ("a latou avega", "their burdens"),
            ("e pei ua māmā—", "seem light—"),
            ("Ua lavea'i e ia", "He delivers"),
            ("i latou", "them"),
            ("mai le pologa,", "from bondage,"),
            ("ma ua latou foi atu", "and they return"),
            ("i Sara'emila.", "to Zarahemla."),
            ("E tusa o le", "about"),
            ("145–120", "145–120"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|25": {
        "en": "The descendants of Mulek at Zarahemla become Nephites—They learn "
              "of the people of Alma and of Zeniff—Alma baptizes Limhi and all "
              "his people—Mosiah authorizes Alma to organize the Church of God. "
              "About 120 B.C.",
        "sm": "O e na tupuga mai ia Moleka sa i Sara'emila ua avea ma sa "
              "Nifaē—Ua latou malamalama i le nuu o Alema ma le nuu o Senifa—Ua "
              "papatiso Limae ma lona nuu uma e Alema—Ua tuu atu e Mosaea le "
              "pule ia Alema e faatu ai le Ekalesia a le Atua. E tusa o le 120 "
              "T.L.M.",
        "cells": [
            ("O e na tupuga mai", "The descendants"),
            ("ia Moleka", "of Mulek"),
            ("sa i Sara'emila", "at Zarahemla"),
            ("ua avea ma sa Nifaē—", "become Nephites—"),
            ("Ua latou malamalama", "They learn"),
            ("i le nuu o Alema", "of the people of Alma"),
            ("ma le nuu o Senifa—", "and of Zeniff—"),
            ("Ua papatiso Limae", "baptizes Limhi"),
            ("ma lona nuu uma", "and all his people"),
            ("e Alema—", "Alma—"),
            ("Ua tuu atu e Mosaea", "Mosiah authorizes"),
            ("le pule", "power"),
            ("ia Alema", "Alma"),
            ("e faatu ai le Ekalesia", "to organize the Church"),
            ("a le Atua.", "of God."),
            ("E tusa o le", "about"),
            ("120", "120"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|26": {
        "en": "Many members of the Church are led into sin by unbelievers—Alma "
              "is promised eternal life—Those who repent and are baptized gain "
              "forgiveness—Church members in sin who repent and confess to Alma "
              "and to the Lord will be forgiven; otherwise, they will not be "
              "numbered among the people of the Church. About 120–100 B.C.",
        "sm": "E toatele tagata o le Ekalesia ua ta'ita'i atu i le agasala e "
              "tagata lē talitonu—Ua folafola mai ia Alema le ola e faavavau—O i "
              "latou o ē salamo ma papatiso latou te maua le faamagaloga—O "
              "tagata agasala o le Ekalesia o ē ua salamo ma ta'utino atu a "
              "latou agasala ia Alema ma le Alii o le a faamagaloina; a lē o "
              "lea, o le a lē faitauina i latou faatasi ma tagata o le Ekalesia. "
              "E tusa o le 120–100 T.L.M.",
        "cells": [
            ("E toatele tagata", "Many members"),
            ("o le Ekalesia", "of the Church"),
            ("ua ta'ita'i atu", "are led"),
            ("i le agasala", "into sin"),
            ("e tagata lē talitonu—", "by unbelievers—"),
            ("Ua folafola mai ia Alema", "Alma is promised"),
            ("le ola e faavavau—", "eternal life—"),
            ("O i latou o ē", "Those who"),
            ("salamo", "repent"),
            ("ma papatiso", "and are baptized"),
            ("latou te maua le faamagaloga—", "gain forgiveness—"),
            ("O tagata agasala", "Members in sin"),
            ("o le Ekalesia", "of the Church"),
            ("o ē ua salamo", "who repent"),
            ("ma ta'utino atu", "and confess"),
            ("a latou agasala", "their sins"),
            ("ia Alema ma le Alii", "to Alma and to the Lord"),
            ("o le a faamagaloina;", "will be forgiven;"),
            ("a lē o lea,", "otherwise,"),
            ("o le a lē faitauina", "will not be numbered"),
            ("i latou", "them"),
            ("faatasi ma tagata", "among the people"),
            ("o le Ekalesia.", "of the Church."),
            ("E tusa o le", "about"),
            ("120–100", "120–100"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|27": {
        "en": "Mosiah forbids persecution and enjoins equality—Alma the "
              "younger and the four sons of Mosiah seek to destroy the "
              "Church—An angel appears and commands them to cease their evil "
              "course—Alma is struck dumb—All mankind must be born again to "
              "gain salvation—Alma and the sons of Mosiah declare glad tidings. "
              "About 100–92 B.C.",
        "sm": "Ua faasa e Mosaea sauaga ma poloa'iina le tutusa—Ua saili Alema "
              "le itiiti, ma atalii e toafa o Mosaea, e lepeti le Ekalesia—Ua "
              "afio mai se agelu ma poloa'iina i latou ia tuu lo latou ala "
              "leaga—Ua taia Alema ma ua gūgū—E ao ona toe fanauina tagata uma "
              "ina ia latou maua le faaolataga—Ua folafola atu e Alema ma atalii "
              "o Mosaea tala fiafia. E tusa o le 100–92 T.L.M.",
        "cells": [
            ("Ua faasa e Mosaea sauaga", "Mosiah forbids persecution"),
            ("ma poloa'iina le tutusa—", "and enjoins equality—"),
            ("Ua saili Alema le itiiti,", "Alma the younger seeks"),
            ("ma atalii e toafa", "and the four sons"),
            ("o Mosaea,", "of Mosiah,"),
            ("e lepeti le Ekalesia—", "to destroy the Church—"),
            ("Ua afio mai se agelu", "An angel appears"),
            ("ma poloa'iina i latou", "and commands them"),
            ("ia tuu", "to cease"),
            ("lo latou ala leaga—", "their evil course—"),
            ("Ua taia Alema", "Alma is struck"),
            ("ma ua gūgū—", "and made dumb—"),
            ("E ao ona toe fanauina", "must be born again"),
            ("tagata uma", "all mankind"),
            ("ina ia latou maua", "that they gain"),
            ("le faaolataga—", "salvation—"),
            ("Ua folafola atu e Alema", "Alma declares"),
            ("ma atalii o Mosaea", "and the sons of Mosiah"),
            ("tala fiafia.", "glad tidings."),
            ("E tusa o le", "about"),
            ("100–92", "100–92"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|28": {
        "en": "The sons of Mosiah go to preach to the Lamanites—Using the two "
              "seer stones, Mosiah translates the Jaredite plates. About 92 B.C.",
        "sm": "Ua o atu atalii o Mosaea e tala'i i sa Lamanā—Ua faaliliu e "
              "Mosaea papatusi o sa Iaretō i ma'a vaai e lua. E tusa o le 92 "
              "T.L.M.",
        "cells": [
            ("Ua o atu", "go"),
            ("atalii o Mosaea", "The sons of Mosiah"),
            ("e tala'i i sa Lamanā—", "to preach to the Lamanites—"),
            ("Ua faaliliu e Mosaea", "Mosiah translates"),
            ("papatusi o sa Iaretō", "the Jaredite plates"),
            ("i ma'a vaai e lua.", "using the two seer stones."),
            ("E tusa o le", "about"),
            ("92", "92"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|29": {
        "en": "Mosiah proposes that judges be chosen in place of a "
              "king—Unrighteous kings lead their people into sin—Alma the "
              "younger is chosen chief judge by the voice of the people—He is "
              "also the high priest over the Church—Alma the elder and Mosiah "
              "die. About 92–91 B.C.",
        "sm": "Ua fautua mai e Mosaea ia filifilia ni faamasino e sui i le "
              "tulaga o se tupu—O tupu e lē amiotonu latou te ta'ita'ia o latou "
              "nuu i le agasala—Ua filifilia Alema le itiiti e fai ma faamasino "
              "sili e ala i le leo o le nuu—O ia foi o le faitaulaga sili i le "
              "Ekalesia—Ua maliliu Alema le matua ma Mosaea. E tusa o le 92–91 "
              "T.L.M.",
        "cells": [
            ("Ua fautua mai e Mosaea", "Mosiah proposes"),
            ("ia filifilia ni faamasino", "that judges be chosen"),
            ("e sui i le tulaga", "in place"),
            ("o se tupu—", "of a king—"),
            ("O tupu e lē amiotonu", "Unrighteous kings"),
            ("latou te ta'ita'ia", "lead"),
            ("o latou nuu", "their people"),
            ("i le agasala—", "into sin—"),
            ("Ua filifilia Alema le itiiti", "Alma the younger is chosen"),
            ("e fai ma faamasino sili", "chief judge"),
            ("e ala i le leo", "by the voice"),
            ("o le nuu—", "of the people—"),
            ("O ia foi", "He is also"),
            ("o le faitaulaga sili", "the high priest"),
            ("i le Ekalesia—", "over the Church—"),
            ("Ua maliliu Alema le matua", "Alma the elder dies"),
            ("ma Mosaea.", "and Mosiah."),
            ("E tusa o le", "about"),
            ("92–91", "92–91"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|1": {
        "en": "Nehor teaches false doctrines, establishes a church, introduces "
              "priestcraft, and slays Gideon—Nehor is executed for his "
              "crimes—Priestcrafts and persecutions spread among the "
              "people—The priests support themselves, the people care for the "
              "poor, and the Church prospers. About 91–88 B.C.",
        "sm": "Ua a'oa'o atu e Ne'oa aoaoga faavae sese, faatuina se ekalesia, "
              "amata faitaulaga pepelo, ma fasioti Kitiona—Ua fasiotia Ne'oa mo "
              "ana solitulafono—Ua faateleina faitaulaga pepelo ma sauaga i "
              "totonu o le nuu—Ua tausi e faitaulaga i latou lava, ua tausi e le "
              "nuu e matitiva, ma ua manuia le Ekalesia. E tusa o le 91–88 "
              "T.L.M.",
        "cells": [
            ("Ua a'oa'o atu e Ne'oa", "Nehor teaches"),
            ("aoaoga faavae sese,", "false doctrines,"),
            ("faatuina se ekalesia,", "establishes a church,"),
            ("amata faitaulaga pepelo,", "introduces priestcraft,"),
            ("ma fasioti Kitiona—", "and slays Gideon—"),
            ("Ua fasiotia Ne'oa", "Nehor is executed"),
            ("mo ana solitulafono—", "for his crimes—"),
            ("Ua faateleina faitaulaga pepelo", "Priestcrafts spread"),
            ("ma sauaga", "and persecutions"),
            ("i totonu o le nuu—", "among the people—"),
            ("Ua tausi e faitaulaga", "The priests support"),
            ("i latou lava,", "themselves,"),
            ("ua tausi e le nuu", "the people care for"),
            ("e matitiva,", "the poor,"),
            ("ma ua manuia le Ekalesia.", "and the Church prospers."),
            ("E tusa o le", "about"),
            ("91–88", "91–88"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|2": {
        "en": "Amlici seeks to be king and is rejected by the voice of the "
              "people—His followers make him king—The Amlicites make war on the "
              "Nephites and are defeated—The Lamanites and Amlicites join "
              "forces and are defeated—Alma slays Amlici. About 87 B.C.",
        "sm": "Ua saili Amiliki ia avea ma tupu ma ua teena e le leo o le nuu—Ua "
              "fai o ia ma tupu e i latou o e na mulimuli ia te ia—Ua sii taua "
              "mai sa Amilikī ia sa Nifaē ma ua faatoilaloina i latou e sa "
              "Nifaē—Ua aufaatasi autau a sa Lamanā ma sa Amilikī ma ua "
              "faatoilaloina—Ua fasiotia Amiliki e Alema. E tusa o le 87 T.L.M.",
        "cells": [
            ("Ua saili Amiliki", "Amlici seeks"),
            ("ia avea ma tupu", "to be king"),
            ("ma ua teena", "and is rejected"),
            ("e le leo", "by the voice"),
            ("o le nuu—", "of the people—"),
            ("Ua fai o ia ma tupu", "make him king"),
            ("e i latou o e", "by those"),
            ("na mulimuli ia te ia—", "who followed him—"),
            ("Ua sii taua mai", "make war"),
            ("sa Amilikī", "The Amlicites"),
            ("ia sa Nifaē", "on the Nephites"),
            ("ma ua faatoilaloina i latou", "and are defeated"),
            ("e sa Nifaē—", "by the Nephites—"),
            ("Ua aufaatasi autau", "join forces"),
            ("a sa Lamanā ma sa Amilikī", "The Lamanites and Amlicites"),
            ("ma ua faatoilaloina—", "and are defeated—"),
            ("Ua fasiotia Amiliki e Alema.", "Alma slays Amlici."),
            ("E tusa o le", "about"),
            ("87", "87"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|3": {
        "en": "The Amlicites had marked themselves according to the prophetic "
              "word—The Lamanites had been cursed for their rebellion—Men bring "
              "their own curses upon themselves—The Nephites defeat another "
              "Lamanite army. About 87–86 B.C.",
        "sm": "Ua faailoga e sa Amilikī i latou lava e tusa ma le upu "
              "faaperofeta—Ua fetuuina sa Lamanā ona o lo latou fouvale—E aumai "
              "e tagata o latou lava malaia i o latou lava luga—Ua faatoilaloina "
              "e sa Nifaē se tasi autau a sa Lamanā. E tusa o le 87–86 T.L.M.",
        "cells": [
            ("Ua faailoga e sa Amilikī", "The Amlicites had marked"),
            ("i latou lava", "themselves"),
            ("e tusa ma", "according to"),
            ("le upu faaperofeta—", "the prophetic word—"),
            ("Ua fetuuina sa Lamanā", "The Lamanites had been cursed"),
            ("ona o lo latou fouvale—", "for their rebellion—"),
            ("E aumai e tagata", "Men bring"),
            ("o latou lava malaia", "their own curses"),
            ("i o latou lava luga—", "upon themselves—"),
            ("Ua faatoilaloina e sa Nifaē", "The Nephites defeat"),
            ("se tasi autau", "another army"),
            ("a sa Lamanā.", "of the Lamanites."),
            ("E tusa o le", "about"),
            ("87–86", "87–86"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|4": {
        "en": "Alma baptizes thousands of converts—Iniquity enters the Church, "
              "and the Church's progress is hindered—Nephihah is appointed "
              "chief judge—Alma, as high priest, devotes himself to the "
              "ministry. About 86–83 B.C.",
        "sm": "Ua papatiso e Alema le afe ma afe o tagata liliu mai—Ua ulufale "
              "mai le amioletonu i le Ekalesia, ma ua ponatia ai le alualu i "
              "luma o le Ekalesia—Ua tofia Nifaea e avea ma faamasino sili—O "
              "Alema, o ia o le faitaulaga sili, ua tuuina atu o ia lava i le "
              "auaunaga. E tusa o le 86–83 T.L.M.",
        "cells": [
            ("Ua papatiso e Alema", "Alma baptizes"),
            ("le afe ma afe", "thousands"),
            ("o tagata liliu mai—", "of converts—"),
            ("Ua ulufale mai le amioletonu", "Iniquity enters"),
            ("i le Ekalesia,", "the Church,"),
            ("ma ua ponatia ai", "and is hindered"),
            ("le alualu i luma", "the progress"),
            ("o le Ekalesia—", "of the Church—"),
            ("Ua tofia Nifaea", "Nephihah is appointed"),
            ("e avea ma faamasino sili—", "chief judge—"),
            ("O Alema,", "Alma,"),
            ("o ia", "he,"),
            ("o le faitaulaga sili,", "the high priest,"),
            ("ua tuuina atu o ia lava", "devotes himself"),
            ("i le auaunaga.", "to the ministry."),
            ("E tusa o le", "about"),
            ("86–83", "86–83"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|5": {
        "en": "The words which Alma, the high priest according to the holy "
              "order of God, delivered to the people in their cities and "
              "villages throughout the land—To gain salvation, men must repent "
              "and keep the commandments, be born again, cleanse their garments "
              "through the blood of Christ, be humble and strip themselves of "
              "pride and envy, and do the works of righteousness—The Good "
              "Shepherd calls His people—Those who do evil works are children "
              "of the devil—Alma testifies of the truth of his doctrine and "
              "commands men to repent—The names of the righteous will be "
              "written in the book of life. About 83 B.C.",
        "sm": "O upu a Alema, le Faitaulaga Sili e tusa ma le faatulagaga paia a "
              "le Atua, sa tuuina atu i tagata i o latou aai ma nuu i le "
              "laueleele atoa—Ina ia maua le faaolataga, e ao i tagata ona "
              "salamo ma tausi poloaiga, toe fanau fouina, faamama o latou ofu e "
              "ala i le toto o Keriso, faamaualalalo ma tafi ese mai ia te i "
              "latou lava le faamaualuga ma le matau'a, ma fai galuega o le "
              "amiotonu—Ua fetalai mai le Leoleo Mamoe Lelei i Ona tagata—O i "
              "latou o e e faia galuega leaga, o fanau ia a le tiapolo—Ua "
              "molimau mai Alema i le moni o lana aoaoga ma poloai mai i tagata "
              "ia salamo—O le a tusia i le tusi o le ola igoa o e e amiotonu. E "
              "tusa o le 83 T.L.M.",
        "cells": [
            ("O upu a Alema,", "The words of Alma,"),
            ("le Faitaulaga Sili", "the High Priest"),
            ("e tusa ma", "according to"),
            ("le faatulagaga paia", "the holy order"),
            ("a le Atua,", "of God,"),
            ("sa tuuina atu i tagata", "delivered to the people"),
            ("i o latou aai", "in their cities"),
            ("ma nuu", "and villages"),
            ("i le laueleele atoa—", "throughout the land—"),
            ("Ina ia maua le faaolataga,", "To gain salvation,"),
            ("e ao i tagata", "men must"),
            ("ona salamo", "repent"),
            ("ma tausi poloaiga,", "and keep the commandments,"),
            ("toe fanau fouina,", "be born again,"),
            ("faamama o latou ofu", "cleanse their garments"),
            ("e ala i le toto", "through the blood"),
            ("o Keriso,", "of Christ,"),
            ("faamaualalalo", "be humble"),
            ("ma tafi ese mai", "and strip away"),
            ("ia te i latou lava", "from themselves"),
            ("le faamaualuga ma le matau'a,", "pride and envy,"),
            ("ma fai galuega", "and do the works"),
            ("o le amiotonu—", "of righteousness—"),
            ("Ua fetalai mai", "calls"),
            ("le Leoleo Mamoe Lelei", "The Good Shepherd"),
            ("i Ona tagata—", "His people—"),
            ("O i latou o e", "Those who"),
            ("e faia galuega leaga,", "do evil works,"),
            ("o fanau ia", "are children"),
            ("a le tiapolo—", "of the devil—"),
            ("Ua molimau mai Alema", "Alma testifies"),
            ("i le moni", "of the truth"),
            ("o lana aoaoga", "of his doctrine"),
            ("ma poloai mai i tagata", "and commands men"),
            ("ia salamo—", "to repent—"),
            ("O le a tusia", "will be written"),
            ("i le tusi", "in the book"),
            ("o le ola", "of life"),
            ("igoa o e e amiotonu.", "The names of the righteous."),
            ("E tusa o le", "about"),
            ("83", "83"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|6": {
        "en": "The Church in Zarahemla is cleansed and set in order—Alma goes "
              "to Gideon to preach. About 83 B.C.",
        "sm": "Ua faamamāina le Ekalesia i Sara'emila ma ua faatulaga maopoopo—Ua "
              "alu atu Alema i Kitiona e talai ai. E tusa o le 83 T.L.M.",
        "cells": [
            ("Ua faamamāina le Ekalesia", "The Church is cleansed"),
            ("i Sara'emila", "in Zarahemla"),
            ("ma ua faatulaga maopoopo—", "and set in order—"),
            ("Ua alu atu Alema", "Alma goes"),
            ("i Kitiona", "to Gideon"),
            ("e talai ai.", "to preach."),
            ("E tusa o le", "about"),
            ("83", "83"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|7": {
        "en": "Christ will be born of Mary—He will loose the bands of death and "
              "bear the sins of His people—Those who repent, are baptized, and "
              "keep the commandments will have eternal life—Filthiness cannot "
              "inherit the kingdom of God—Humility, faith, hope, and charity "
              "are required. About 83 B.C.",
        "sm": "O le a fanau mai Keriso ia Maria—O le a ia tatalaina fusi o le "
              "oti ma tauave agasala a Ona tagata—O i latou o e salamo, ma "
              "papatisoina, ma tausi i poloaiga o le a maua e i latou le ola e "
              "faavavau—E le mafai e se mea eleelea ona mautofi i le malo o le "
              "Atua—E manaomia le lotomaualalo, faatuatua, faamoemoe, ma le "
              "alofa mama. E tusa o le 83 T.L.M.",
        "cells": [
            ("O le a fanau mai Keriso", "Christ will be born"),
            ("ia Maria—", "of Mary—"),
            ("O le a ia tatalaina", "He will loose"),
            ("fusi o le oti", "the bands of death"),
            ("ma tauave agasala", "and bear the sins"),
            ("a Ona tagata—", "of His people—"),
            ("O i latou o e", "Those who"),
            ("salamo,", "repent,"),
            ("ma papatisoina,", "are baptized,"),
            ("ma tausi i poloaiga", "and keep the commandments"),
            ("o le a maua e i latou", "will have"),
            ("le ola e faavavau—", "eternal life—"),
            ("E le mafai", "cannot"),
            ("e se mea eleelea", "Filthiness"),
            ("ona mautofi", "inherit"),
            ("i le malo", "the kingdom"),
            ("o le Atua—", "of God—"),
            ("E manaomia le lotomaualalo,", "Humility is required,"),
            ("faatuatua,", "faith,"),
            ("faamoemoe,", "hope,"),
            ("ma le alofa mama.", "and charity."),
            ("E tusa o le", "about"),
            ("83", "83"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|8": {
        "en": "Alma preaches and baptizes in Melek—He is rejected in Ammonihah "
              "and leaves—An angel commands him to return and cry repentance "
              "unto the people—He is received by Amulek, and the two of them "
              "preach in Ammonihah. About 82 B.C.",
        "sm": "Ua tala'i ma papatiso atu Alema i Meleka—Ua teena o ia i Amonaea "
              "ma ua alu ese atu—Ua poloaiina o ia e le agelu ia toe foi atu ma "
              "alaga atu le salamo i le nuu—Ua talia o ia e Amoleka, ma ua la "
              "tala'i atu uma i Amonaea. E tusa o le 82 T.L.M.",
        "cells": [
            ("Ua tala'i ma papatiso atu", "preaches and baptizes"),
            ("Alema", "Alma"),
            ("i Meleka—", "in Melek—"),
            ("Ua teena o ia", "He is rejected"),
            ("i Amonaea", "in Ammonihah"),
            ("ma ua alu ese atu—", "and leaves—"),
            ("Ua poloaiina o ia", "He is commanded"),
            ("e le agelu", "by an angel"),
            ("ia toe foi atu", "to return"),
            ("ma alaga atu le salamo", "and cry repentance"),
            ("i le nuu—", "unto the people—"),
            ("Ua talia o ia", "He is received"),
            ("e Amoleka,", "by Amulek,"),
            ("ma ua la tala'i atu uma", "and the two preach"),
            ("i Amonaea.", "in Ammonihah."),
            ("E tusa o le", "about"),
            ("82", "82"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|10": {
        "en": "Lehi descended from Manasseh—Amulek recounts the angelic command "
              "that he care for Alma—The prayers of the righteous cause the "
              "people to be spared—Unrighteous lawyers and judges lay the "
              "foundation of the destruction of the people. About 82 B.C.",
        "sm": "O Liae o sē e tupuga mai ia Manase—Ua ta'u mai e Amoleka le "
              "poloaiga a le agelu ia tausi o ia ia Alema—O tatalo a e amiotonu "
              "na faasaoina ai le nuu—Ua faataatitia e loia ma faamasino "
              "amioleaga le faavae o le faafanoga o le nuu. E tusa o le 82 "
              "T.L.M.",
        "cells": [
            ("O Liae", "Lehi"),
            ("o sē e tupuga mai", "descended"),
            ("ia Manase—", "from Manasseh—"),
            ("Ua ta'u mai e Amoleka", "Amulek recounts"),
            ("le poloaiga a le agelu", "the angelic command"),
            ("ia tausi o ia", "that he care"),
            ("ia Alema—", "for Alma—"),
            ("O tatalo a e amiotonu", "The prayers of the righteous"),
            ("na faasaoina ai le nuu—", "cause the people to be spared—"),
            ("Ua faataatitia", "lay"),
            ("e loia ma faamasino amioleaga", "Unrighteous lawyers and judges"),
            ("le faavae o le faafanoga", "the foundation of the destruction"),
            ("o le nuu.", "of the people."),
            ("E tusa o le", "about"),
            ("82", "82"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|11": {
        "en": "The Nephite monetary system is set forth—Amulek contends with "
              "Zeezrom—Christ will not save people in their sins—Only those who "
              "inherit the kingdom of heaven are saved—All men will rise in "
              "immortality—There is no death after the Resurrection. "
              "About 82 B.C.",
        "sm": "Ua faamatala mai le faatulagaga o tupe a sa Nifaē—Ua finau "
              "Amoleka ma Seseroma—O le a lē faaolaina e Keriso tagata ia latou "
              "agasala—E na'o i latou o e mautofi i le malo o le lagi e "
              "faaolaina—O le a toetutu mai tagata uma lava i le tino ola pea—E "
              "lē toe i ai se oti pe a mavae le Toetutu. E tusa o le 82 T.L.M.",
        "cells": [
            ("Ua faamatala mai", "is set forth"),
            ("le faatulagaga o tupe", "the monetary system"),
            ("a sa Nifaē—", "of the Nephites—"),
            ("Ua finau Amoleka ma Seseroma—", "Amulek contends with Zeezrom—"),
            ("O le a lē faaolaina e Keriso", "Christ will not save"),
            ("tagata", "people"),
            ("ia latou agasala—", "in their sins—"),
            ("E na'o i latou o e", "Only those who"),
            ("mautofi", "inherit"),
            ("i le malo", "the kingdom"),
            ("o le lagi", "of heaven"),
            ("e faaolaina—", "are saved—"),
            ("O le a toetutu mai", "will rise"),
            ("tagata uma lava", "all men"),
            ("i le tino ola pea—", "in immortality—"),
            ("E lē toe i ai", "There is no more"),
            ("se oti", "death"),
            ("pe a mavae le Toetutu.", "after the Resurrection."),
            ("E tusa o le", "about"),
            ("82", "82"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|12": {
        "en": "Alma speaks to Zeezrom—The mysteries of God can be given only to "
              "the faithful—Men are judged by their thoughts, beliefs, words, "
              "and works—The wicked will suffer a spiritual death—This mortal "
              "life is a probationary state—The plan of redemption brings to "
              "pass the Resurrection and, through faith, a remission of "
              "sins—The repentant have a claim on mercy through the Only "
              "Begotten Son. About 82 B.C.",
        "sm": "Ua tautala atu Alema ia Seseroma—O mealilo a le Atua e na o i "
              "latou o e faamaoni e mafai ona faaali i ai—E faamasinoina tagata "
              "i o latou mafaufauga, talitonuga, upu, ma galuega—O le a mafatia "
              "e e amioleaga i se oti faaleagaga—O lenei olaga faaletino o se "
              "tulaga e nofo vaavaaia ai—O le fuafuaga o le togiolaina ua aumai "
              "ai le Toetutu, ma se faamagaloga o agasala, e ala i le "
              "faatuatua—O e e salamo e i ai ia i latou se aiā e maua ai le "
              "alofa mutimutivale e ala i le Atalii Pele e Toatasi. E tusa o le "
              "82 T.L.M.",
        "cells": [
            ("Ua tautala atu Alema", "Alma speaks"),
            ("ia Seseroma—", "to Zeezrom—"),
            ("O mealilo a le Atua", "The mysteries of God"),
            ("e na o", "only"),
            ("i latou o e faamaoni", "the faithful"),
            ("e mafai ona faaali", "can be given"),
            ("i ai—", "to them—"),
            ("E faamasinoina tagata", "Men are judged"),
            ("i o latou mafaufauga,", "by their thoughts,"),
            ("talitonuga,", "beliefs,"),
            ("upu,", "words,"),
            ("ma galuega—", "and works—"),
            ("O le a mafatia", "will suffer"),
            ("e e amioleaga", "The wicked"),
            ("i se oti faaleagaga—", "a spiritual death—"),
            ("O lenei olaga faaletino", "This mortal life"),
            ("o se tulaga", "is a state"),
            ("e nofo vaavaaia ai—", "of probation—"),
            ("O le fuafuaga", "The plan"),
            ("o le togiolaina", "of redemption"),
            ("ua aumai ai le Toetutu,", "brings to pass the Resurrection,"),
            ("ma se faamagaloga o agasala,", "and a remission of sins,"),
            ("e ala i le faatuatua—", "through faith—"),
            ("O e e salamo", "The repentant"),
            ("e i ai ia i latou", "have"),
            ("se aiā", "a claim"),
            ("e maua ai", "to obtain"),
            ("le alofa mutimutivale", "mercy"),
            ("e ala i le Atalii Pele", "through the Beloved Son"),
            ("e Toatasi.", "the Only Begotten."),
            ("E tusa o le", "about"),
            ("82", "82"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|13": {
        "en": "Men are called as high priests because of their exceeding faith "
              "and good works—They are to teach the commandments—Through "
              "righteousness they are sanctified and enter into the rest of the "
              "Lord—Melchizedek was one of these—Angels are declaring glad "
              "tidings throughout the land—They will declare the actual coming "
              "of Christ. About 82 B.C.",
        "sm": "E valaauina alii e avea ma faitaulaga sili ona o lo latou "
              "faatuatua tele ma a latou galuega lelei—E tatau ona latou a'oa'o "
              "atu poloaiga—E faapaiaina i latou ma ulufale atu i le malologa o "
              "le Alii e ala i le amiotonu—O Mekisateko o se tasi o i latou "
              "ia—O loo tala'i atu e agelu tala fiafia i le laueleele atoa—O le "
              "a latou folafola le afio mai tonu o Keriso. E tusa o le 82 "
              "T.L.M.",
        "cells": [
            ("E valaauina alii", "Men are called"),
            ("e avea ma faitaulaga sili", "as high priests"),
            ("ona o lo latou", "because of their"),
            ("faatuatua tele", "exceeding faith"),
            ("ma a latou galuega lelei—", "and good works—"),
            ("E tatau ona latou a'oa'o atu", "They are to teach"),
            ("poloaiga—", "the commandments—"),
            ("E faapaiaina i latou", "they are sanctified"),
            ("ma ulufale atu", "and enter into"),
            ("i le malologa", "the rest"),
            ("o le Alii", "of the Lord"),
            ("e ala i le amiotonu—", "through righteousness—"),
            ("O Mekisateko", "Melchizedek"),
            ("o se tasi", "was one"),
            ("o i latou ia—", "of these—"),
            ("O loo tala'i atu", "are declaring"),
            ("e agelu", "Angels"),
            ("tala fiafia", "glad tidings"),
            ("i le laueleele atoa—", "throughout the land—"),
            ("O le a latou folafola", "They will declare"),
            ("le afio mai tonu", "the actual coming"),
            ("o Keriso.", "of Christ."),
            ("E tusa o le", "about"),
            ("82", "82"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|14": {
        "en": "Alma and Amulek are imprisoned and smitten—The believers and "
              "their holy scriptures are burned by fire—These martyrs are "
              "received by the Lord in glory—The prison walls are rent and "
              "fall—Alma and Amulek are delivered, and their persecutors are "
              "slain. About 82–81 B.C.",
        "sm": "Ua falepuipui ma sasaina Alema ma Amoleka—Ua susunu i le afi e na "
              "talitonu faatasi ma a latou tusitusiga paia—Ua talia e le Alii "
              "nei maturo i le mamalu—Ua vete ma pa'u'ū i lalo pa o le "
              "falepuipui—Ua lavea'iina Alema ma Amoleka, ma ua fasiotia e na "
              "sauaina i laua. E tusa o le 82–81 T.L.M.",
        "cells": [
            ("Ua falepuipui ma sasaina", "are imprisoned and smitten"),
            ("Alema ma Amoleka—", "Alma and Amulek—"),
            ("Ua susunu i le afi", "are burned by fire"),
            ("e na talitonu", "The believers"),
            ("faatasi ma a latou", "along with their"),
            ("tusitusiga paia—", "holy scriptures—"),
            ("Ua talia e le Alii", "are received by the Lord"),
            ("nei maturo", "These martyrs"),
            ("i le mamalu—", "in glory—"),
            ("Ua vete", "are rent"),
            ("ma pa'u'ū i lalo", "and fall down"),
            ("pa o le falepuipui—", "The prison walls—"),
            ("Ua lavea'iina Alema ma Amoleka,", "Alma and Amulek are delivered,"),
            ("ma ua fasiotia", "and are slain"),
            ("e na sauaina i laua.", "their persecutors."),
            ("E tusa o le", "about"),
            ("82–81", "82–81"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|15": {
        "en": "Alma and Amulek go to Sidom and establish a church—Alma heals "
              "Zeezrom, who joins the Church—Many are baptized, and the Church "
              "prospers—Alma and Amulek go to Zarahemla. About 81 B.C.",
        "sm": "Ua o atu Alema ma Amoleka i Saitoma ma faatuina ai se ekalesia—Ua "
              "faamaloloina e Alema o Seseroma, o lē ua auai i le Ekalesia—E "
              "toatele ua papatisoina, ma ua uluuluola le ekalesia—Ua o atu "
              "Alema ma Amoleka i Sara'emila. E tusa o le 81 T.L.M.",
        "cells": [
            ("Ua o atu", "go"),
            ("Alema ma Amoleka", "Alma and Amulek"),
            ("i Saitoma", "to Sidom"),
            ("ma faatuina ai se ekalesia—", "and establish a church—"),
            ("Ua faamaloloina e Alema", "Alma heals"),
            ("o Seseroma,", "Zeezrom,"),
            ("o lē ua auai", "who joins"),
            ("i le Ekalesia—", "the Church—"),
            ("E toatele ua papatisoina,", "Many are baptized,"),
            ("ma ua uluuluola le ekalesia—", "and the Church prospers—"),
            ("Ua o atu", "go"),
            ("Alema ma Amoleka", "Alma and Amulek"),
            ("i Sara'emila.", "to Zarahemla."),
            ("E tusa o le", "about"),
            ("81", "81"),
            ("T.L.M.", "B.C."),
        ],
    },
    "mosiah|23": {
        "en": "Alma refuses to be king—He serves as high priest—The Lord "
              "chastens His people, and the Lamanites conquer the land of "
              "Helam—Amulon, leader of King Noah's wicked priests, rules "
              "subject to the Lamanite monarch. About 145–121 B.C.",
        "sm": "Ua teena e Alema le avea o ia ma tupu—Ua auauna atu o ia o se "
              "faitaulaga sili—Ua a'oa'i e le Alii Lona nuu, ma ua manumalo sa "
              "Lamanā i le laueleele o Helama—O Amulona, le taitai o faitaulaga "
              "amioleaga a Noa, ua pule o ia i lalo o le pulega a le monaki sa "
              "Lamanā. E tusa o le 145–121 T.L.M.",
        "cells": [
            ("Ua teena e Alema", "Alma refuses"),
            ("le avea o ia ma tupu—", "to be king—"),
            ("Ua auauna atu o ia", "He serves"),
            ("o se faitaulaga sili—", "as high priest—"),
            ("Ua a'oa'i e le Alii", "The Lord chastens"),
            ("Lona nuu,", "His people,"),
            ("ma ua manumalo sa Lamanā", "and the Lamanites conquer"),
            ("i le laueleele o Helama—", "the land of Helam—"),
            ("O Amulona,", "Amulon,"),
            ("le taitai o faitaulaga amioleaga", "leader of the wicked priests"),
            ("a Noa,", "of Noah,"),
            ("ua pule o ia", "rules"),
            ("i lalo o le pulega", "subject to"),
            ("a le monaki sa Lamanā.", "of the Lamanite monarch."),
            ("E tusa o le", "about"),
            ("145–121", "145–121"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|9": {
        "en": "Alma commands the people of Ammonihah to repent—The Lord will be "
              "merciful to the Lamanites in the last days—If the Nephites "
              "forsake the light, they will be destroyed by the Lamanites—The "
              "Son of God will come soon—He will redeem those who repent, are "
              "baptized, and have faith in His name. About 82 B.C.",
        "sm": "Ua poloai atu Alema i tagata o Amonaea ia salamo—O le a alofa "
              "mutimutivale le Alii ia sa Lamanā i aso gataaga—Afai e lafoai e "
              "sa Nifaē le malamalama, o le a faaumatia i latou e sa Lamanā—Ua "
              "lata ona afio mai le Alo o le Atua—O le a Ia togiolaina i latou o "
              "e e salamo, ma papatisoina, ma faatuatua i Lona suafa. E tusa o "
              "le 82 T.L.M.",
        "cells": [
            ("Ua poloai atu Alema", "Alma commands"),
            ("i tagata o Amonaea", "the people of Ammonihah"),
            ("ia salamo—", "to repent—"),
            ("O le a alofa mutimutivale", "will be merciful"),
            ("le Alii", "The Lord"),
            ("ia sa Lamanā", "to the Lamanites"),
            ("i aso gataaga—", "in the last days—"),
            ("Afai e lafoai e sa Nifaē", "If the Nephites forsake"),
            ("le malamalama,", "the light,"),
            ("o le a faaumatia i latou", "they will be destroyed"),
            ("e sa Lamanā—", "by the Lamanites—"),
            ("Ua lata ona afio mai", "will come soon"),
            ("le Alo o le Atua—", "The Son of God—"),
            ("O le a Ia togiolaina", "He will redeem"),
            ("i latou", "those"),
            ("o e e salamo,", "who repent,"),
            ("ma papatisoina,", "are baptized,"),
            ("ma faatuatua i Lona suafa.", "and have faith in His name."),
            ("E tusa o le", "about"),
            ("82", "82"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|16": {
        "en": "The Lamanites destroy the people of Ammonihah—Zoram leads the "
              "Nephites to victory over the Lamanites—Alma and Amulek and many "
              "others preach the word—They teach that after His Resurrection "
              "Christ will appear to the Nephites. About 81–77 B.C.",
        "sm": "Ua faaumatia e sa Lamanā le nuu o Amonaea—Ua taitai e Sorama sa "
              "Nifaē i le manumalo i luga o sa Lamanā—Ua tala'i atu e Alema ma "
              "Amoleka ma isi e toatele ana afioga—Ua latou a'oa'o atu a mavae "
              "Lona Toetu mai o le a afio mai Keriso i sa Nifaē. E tusa o le "
              "81–77 T.L.M.",
        "cells": [
            ("Ua faaumatia e sa Lamanā", "The Lamanites destroy"),
            ("le nuu o Amonaea—", "the people of Ammonihah—"),
            ("Ua taitai e Sorama", "Zoram leads"),
            ("sa Nifaē", "the Nephites"),
            ("i le manumalo", "to victory"),
            ("i luga o sa Lamanā—", "over the Lamanites—"),
            ("Ua tala'i atu", "preach"),
            ("e Alema ma Amoleka", "Alma and Amulek"),
            ("ma isi e toatele", "and many others"),
            ("ana afioga—", "the word—"),
            ("Ua latou a'oa'o atu", "They teach"),
            ("a mavae Lona Toetu mai", "that after His Resurrection"),
            ("o le a afio mai Keriso", "Christ will appear"),
            ("i sa Nifaē.", "to the Nephites."),
            ("E tusa o le", "about"),
            ("81–77", "81–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|18": {
        "en": "King Lamoni supposes that Ammon is the Great Spirit—Ammon "
              "teaches the king about the Creation, God's dealings with men, "
              "and the redemption that comes through Christ—Lamoni believes and "
              "falls to the earth as if dead. About 90 B.C.",
        "sm": "Ua manatu le Tupu o Lamonae o Amona o le Agaga Silisili lea—Ua "
              "a'oa'o atu e Amona le tupu e uiga i le Foafoaga, o feutaga'iga a "
              "le Atua ma tagata, ma le togiola e oo mai e ala mai ia Keriso—Ua "
              "talitonu Lamonae ma ua pa'ū ifo i le eleele e pei ua oti. E tusa "
              "o le 90 T.L.M.",
        "cells": [
            ("Ua manatu", "supposes"),
            ("le Tupu o Lamonae", "King Lamoni"),
            ("o Amona", "that Ammon"),
            ("o le Agaga Silisili lea—", "is the Great Spirit—"),
            ("Ua a'oa'o atu e Amona", "Ammon teaches"),
            ("le tupu", "the king"),
            ("e uiga i le Foafoaga,", "about the Creation,"),
            ("o feutaga'iga a le Atua", "God's dealings"),
            ("ma tagata,", "with men,"),
            ("ma le togiola", "and the redemption"),
            ("e oo mai", "that comes"),
            ("e ala mai ia Keriso—", "through Christ—"),
            ("Ua talitonu Lamonae", "Lamoni believes"),
            ("ma ua pa'ū ifo", "and falls down"),
            ("i le eleele", "to the earth"),
            ("e pei ua oti.", "as if dead."),
            ("E tusa o le", "about"),
            ("90", "90"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|19": {
        "en": "Lamoni receives the light of everlasting life and sees the "
              "Redeemer—His household falls into a trance, and many see "
              "angels—Ammon is preserved miraculously—He baptizes many and "
              "establishes a church among them. About 90 B.C.",
        "sm": "Ua maua e Lamonae le malamalama o le ola faavavau ma ua vaai i le "
              "Togiola—Ua pa'u'ū lona auaiga i se tulaga lofituina, ma ua vaai "
              "le toatele i agelu—Ua faasaoina Amona i se ala faavavega—Ua ia "
              "papatisoina tagata e toatele ma faatuina se ekalesia i totonu o i "
              "latou. E tusa o le 90 T.L.M.",
        "cells": [
            ("Ua maua e Lamonae", "Lamoni receives"),
            ("le malamalama", "the light"),
            ("o le ola faavavau", "of everlasting life"),
            ("ma ua vaai i le Togiola—", "and sees the Redeemer—"),
            ("Ua pa'u'ū lona auaiga", "His household falls"),
            ("i se tulaga lofituina,", "into a trance,"),
            ("ma ua vaai le toatele", "and many see"),
            ("i agelu—", "angels—"),
            ("Ua faasaoina Amona", "Ammon is preserved"),
            ("i se ala faavavega—", "miraculously—"),
            ("Ua ia papatisoina", "He baptizes"),
            ("tagata e toatele", "many"),
            ("ma faatuina se ekalesia", "and establishes a church"),
            ("i totonu o i latou.", "among them."),
            ("E tusa o le", "about"),
            ("90", "90"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|20": {
        "en": "The Lord sends Ammon to Middoni to deliver his imprisoned "
              "brethren—Ammon and Lamoni meet Lamoni's father, who is king over "
              "all the land—Ammon compels the old king to approve the release "
              "of his brethren. About 90 B.C.",
        "sm": "Ua auina atu e le Alii Amona i Mitonae e laveai ona uso sa "
              "falepuipui—Ua feiloai Amona ma Lamonae ma le tamā o Lamonae, o lē "
              "o le tupu i le laueleele uma—Ua faaamalosi e Amona le tupu matua "
              "ia faataga mai le tatalaina o ona uso. E tusa o le 90 T.L.M.",
        "cells": [
            ("Ua auina atu e le Alii", "The Lord sends"),
            ("Amona", "Ammon"),
            ("i Mitonae", "to Middoni"),
            ("e laveai ona uso", "to deliver his brethren"),
            ("sa falepuipui—", "imprisoned—"),
            ("Ua feiloai Amona ma Lamonae", "Ammon and Lamoni meet"),
            ("ma le tamā o Lamonae,", "Lamoni's father,"),
            ("o lē o le tupu", "who is king"),
            ("i le laueleele uma—", "over all the land—"),
            ("Ua faaamalosi e Amona", "Ammon compels"),
            ("le tupu matua", "the old king"),
            ("ia faataga mai", "to approve"),
            ("le tatalaina o ona uso.", "the release of his brethren."),
            ("E tusa o le", "about"),
            ("90", "90"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|22": {
        "en": "Aaron teaches Lamoni's father about the Creation, the Fall of "
              "Adam, and the plan of redemption through Christ—The king and all "
              "his household are converted—The division of the land between the "
              "Nephites and the Lamanites is explained. About 90–77 B.C.",
        "sm": "Ua a'oa'o e Arona le tamā o Lamonae e uiga i le Foafoaga, le Pa'ū "
              "o Atamu, ma le fuafuaga o le togiola e ala ia Keriso—Ua liua le "
              "tupu ma lona auaiga atoa—Ua faamatala mai le vaevaega o le "
              "laueleele i le va o sa Nifaē ma sa Lamanā. E tusa o le 90–77 "
              "T.L.M.",
        "cells": [
            ("Ua a'oa'o e Arona", "Aaron teaches"),
            ("le tamā o Lamonae", "Lamoni's father"),
            ("e uiga i le Foafoaga,", "about the Creation,"),
            ("le Pa'ū o Atamu,", "the Fall of Adam,"),
            ("ma le fuafuaga", "and the plan"),
            ("o le togiola", "of redemption"),
            ("e ala ia Keriso—", "through Christ—"),
            ("Ua liua le tupu", "The king is converted"),
            ("ma lona auaiga atoa—", "and all his household—"),
            ("Ua faamatala mai", "is explained"),
            ("le vaevaega o le laueleele", "the division of the land"),
            ("i le va o sa Nifaē", "between the Nephites"),
            ("ma sa Lamanā.", "and the Lamanites."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|23": {
        "en": "Religious freedom is proclaimed—The Lamanites in seven lands and "
              "cities are converted—They call themselves Anti-Nephi-Lehies and "
              "are freed from the curse—The Amalekites and the Amulonites "
              "reject the truth. About 90–77 B.C.",
        "sm": "Ua folafola atu le saolotoga e tapuai ai—Ua faaliliuina sa Lamanā "
              "i laueleele ma aai e fitu—Ua latou ta'ua i latou lava o "
              "Aneti-Nifae-Liae ma ua tatala mai le fetuu—Ua tetee e sa Amalekā "
              "ma sa Amulonā le upumoni. E tusa o le 90–77 T.L.M.",
        "cells": [
            ("Ua folafola atu", "is proclaimed"),
            ("le saolotoga e tapuai ai—", "religious freedom—"),
            ("Ua faaliliuina sa Lamanā", "The Lamanites are converted"),
            ("i laueleele ma aai", "in lands and cities"),
            ("e fitu—", "seven—"),
            ("Ua latou ta'ua", "They call"),
            ("i latou lava", "themselves"),
            ("o Aneti-Nifae-Liae", "Anti-Nephi-Lehies"),
            ("ma ua tatala mai", "and are freed"),
            ("le fetuu—", "from the curse—"),
            ("Ua tetee", "reject"),
            ("e sa Amalekā ma sa Amulonā", "The Amalekites and Amulonites"),
            ("le upumoni.", "the truth."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|24": {
        "en": "The Lamanites come against the people of God—The "
              "Anti-Nephi-Lehies rejoice in Christ and are visited by "
              "angels—They choose to suffer death rather than to defend "
              "themselves—More Lamanites are converted. About 90–77 B.C.",
        "sm": "Ua o mai sa Lamanā e faasagatau i tagata o le Atua—Ua olioli sa "
              "Aneti-Nifae-Liae ia Keriso ma ua asiasi mai agelu ia te i "
              "latou—Ua latou filifili e mafatia i le oti nai lo le puipuia o i "
              "latou lava—Ua liua isi sa Lamanā e toatele. E tusa o le 90–77 "
              "T.L.M.",
        "cells": [
            ("Ua o mai sa Lamanā", "The Lamanites come"),
            ("e faasagatau", "against"),
            ("i tagata o le Atua—", "the people of God—"),
            ("Ua olioli sa Aneti-Nifae-Liae", "The Anti-Nephi-Lehies rejoice"),
            ("ia Keriso", "in Christ"),
            ("ma ua asiasi mai agelu", "and are visited by angels"),
            ("ia te i latou—", "unto them—"),
            ("Ua latou filifili", "They choose"),
            ("e mafatia i le oti", "to suffer death"),
            ("nai lo le puipuia", "rather than defend"),
            ("o i latou lava—", "themselves—"),
            ("Ua liua isi sa Lamanā", "More Lamanites are converted"),
            ("e toatele.", "many."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|25": {
        "en": "Lamanite aggressions spread—The seed of the priests of Noah "
              "perish as Abinadi prophesied—Many Lamanites are converted and "
              "join the people of Anti-Nephi-Lehi—They believe in Christ and "
              "keep the law of Moses. About 90–77 B.C.",
        "sm": "Ua faatetele osofaiga a sa Lamanā—Ua fano fanau a faitaulaga a "
              "Noa e pei ona sa valoia e Apinati—E toatele sa Lamanā ua liua ma "
              "aufaatasi ma le nuu o Aneti-Nifae-Liae—Ua latou talitonu ia "
              "Keriso ma tausi i le tulafono a Mose. E tusa o le 90–77 T.L.M.",
        "cells": [
            ("Ua faatetele osofaiga", "aggressions spread"),
            ("a sa Lamanā—", "of the Lamanites—"),
            ("Ua fano", "perish"),
            ("fanau a faitaulaga a Noa", "the seed of Noah's priests"),
            ("e pei ona", "as"),
            ("sa valoia e Apinati—", "Abinadi prophesied—"),
            ("E toatele sa Lamanā", "Many Lamanites"),
            ("ua liua", "are converted"),
            ("ma aufaatasi", "and join"),
            ("ma le nuu o Aneti-Nifae-Liae—", "the people of Anti-Nephi-Lehi—"),
            ("Ua latou talitonu ia Keriso", "They believe in Christ"),
            ("ma tausi", "and keep"),
            ("i le tulafono a Mose.", "the law of Moses."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|17": {
        "en": "The sons of Mosiah have the spirit of prophecy and of "
              "revelation—They go their several ways to declare the word to the "
              "Lamanites—Ammon goes to the land of Ishmael and becomes the "
              "servant of King Lamoni—Ammon saves the king's flocks and slays "
              "his enemies at the water of Sebus. Verses 1–3, about 77 B.C.; "
              "verse 4, about 91–77 B.C.; and verses 5–39, about 91 B.C.",
        "sm": "Ua i ai i atalii o Mosaea le agaga o valoaga ma faaaliga—Ua latou "
              "o atu i o latou ala eseese e tala'i atu le afioga i sa Lamanā—Ua "
              "alu atu Amona i le laueleele o Isamaeli ma ua avea o se auauna a "
              "le Tupu o Lamonae—Ua laveai e Amona lafu a le tupu ma fasiotia "
              "ona fili i vai o Sevusa. Fuaiupu 1–3 e tusa o le 77 T.L.M.; "
              "fuaiupu 4, e tusa o le 91–77 T.L.M.; ma o fuaiupu 5–39, e tusa o "
              "le 91 T.L.M.",
        "cells": [
            ("Ua i ai", "have"),
            ("i atalii o Mosaea", "the sons of Mosiah"),
            ("le agaga o valoaga", "the spirit of prophecy"),
            ("ma faaaliga—", "and of revelation—"),
            ("Ua latou o atu", "They go"),
            ("i o latou ala eseese", "their several ways"),
            ("e tala'i atu le afioga", "to declare the word"),
            ("i sa Lamanā—", "to the Lamanites—"),
            ("Ua alu atu Amona", "Ammon goes"),
            ("i le laueleele o Isamaeli", "to the land of Ishmael"),
            ("ma ua avea", "and becomes"),
            ("o se auauna", "the servant"),
            ("a le Tupu o Lamonae—", "of King Lamoni—"),
            ("Ua laveai e Amona", "Ammon saves"),
            ("lafu a le tupu", "the king's flocks"),
            ("ma fasiotia ona fili", "and slays his enemies"),
            ("i vai o Sevusa.", "at the water of Sebus."),
            ("Fuaiupu 1–3", "Verses 1–3"),
            ("e tusa o le", "about"),
            ("77 T.L.M.;", "77 B.C.;"),
            ("fuaiupu 4,", "verse 4,"),
            ("e tusa o le", "about"),
            ("91–77 T.L.M.;", "91–77 B.C.;"),
            ("ma o fuaiupu 5–39,", "and verses 5–39,"),
            ("e tusa o le", "about"),
            ("91 T.L.M.", "91 B.C."),
        ],
    },
    "alma|21": {
        "en": "Aaron teaches the Amalekites about Christ and His "
              "Atonement—Aaron and his brethren are imprisoned in "
              "Middoni—After their deliverance, they teach in the synagogues "
              "and make many converts—Lamoni grants religious freedom to the "
              "people in the land of Ishmael. About 90–77 B.C.",
        "sm": "Ua a'oa'o atu e Arona sa Amalekā e uiga ia Keriso ma Lana "
              "Togiola—Ua falepuipui Arona ma ona uso i Mitonae—Ina ua mavae le "
              "lavea'iina o i latou, ua latou a'oa'o atu i sunako ma faaliliu "
              "tagata e toatele—Ua tuu atu e Lamonae le saolotoga i tagata e "
              "tapuai ai i le laueleele o Isamaeli. E tusa o le 90–77 T.L.M.",
        "cells": [
            ("Ua a'oa'o atu e Arona", "Aaron teaches"),
            ("sa Amalekā", "the Amalekites"),
            ("e uiga ia Keriso", "about Christ"),
            ("ma Lana Togiola—", "and His Atonement—"),
            ("Ua falepuipui Arona", "Aaron is imprisoned"),
            ("ma ona uso", "and his brethren"),
            ("i Mitonae—", "in Middoni—"),
            ("Ina ua mavae", "After"),
            ("le lavea'iina o i latou,", "their deliverance,"),
            ("ua latou a'oa'o atu", "they teach"),
            ("i sunako", "in the synagogues"),
            ("ma faaliliu tagata e toatele—", "and make many converts—"),
            ("Ua tuu atu e Lamonae", "Lamoni grants"),
            ("le saolotoga", "freedom"),
            ("i tagata e tapuai ai", "to the people to worship"),
            ("i le laueleele o Isamaeli.", "in the land of Ishmael."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|26": {
        "en": "Ammon glories in the Lord—The faithful are strengthened by the "
              "Lord and are given knowledge—By faith men may bring thousands of "
              "souls unto repentance—God has all power and comprehends all "
              "things. About 90–77 B.C.",
        "sm": "Ua olioli Amona i le Alii—E faamalosi e le Alii ē faamaoni ma "
              "tuuina mai ia te i latou le malamalama—O le faatuatua e mafai ai "
              "e tagata ona aumaia le afe ma afe o agaga i le salamo—Ua i ai i "
              "le Atua le mana uma ma ua ia silafia mea uma. E tusa o le 90–77 "
              "T.L.M.",
        "cells": [
            ("Ua olioli Amona", "Ammon glories"),
            ("i le Alii—", "in the Lord—"),
            ("E faamalosi e le Alii", "are strengthened by the Lord"),
            ("ē faamaoni", "The faithful"),
            ("ma tuuina mai ia te i latou", "and given unto them"),
            ("le malamalama—", "knowledge—"),
            ("O le faatuatua", "By faith"),
            ("e mafai ai e tagata", "men may"),
            ("ona aumaia", "bring"),
            ("le afe ma afe", "thousands"),
            ("o agaga", "of souls"),
            ("i le salamo—", "unto repentance—"),
            ("Ua i ai i le Atua", "God has"),
            ("le mana uma", "all power"),
            ("ma ua ia silafia", "and comprehends"),
            ("mea uma.", "all things."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|27": {
        "en": "The Lord commands Ammon to lead the people of Anti-Nephi-Lehi to "
              "safety—Upon meeting Alma, Ammon's joy exhausts his strength—The "
              "Nephites give the Anti-Nephi-Lehies the land of Jershon—They are "
              "called the people of Ammon. About 90–77 B.C.",
        "sm": "Ua poloaiina e le Alii Amona e taitai atu le nuu o "
              "Aneti-Nifae-Liae i le saogalemu—Ina ua feiloai ma Alema, sa alu "
              "uma le malosi o Amona i lona olioli tele—Ua tuu mai e sa Nifaē i "
              "le nuu o Aneti-Nifae-Liae le laueleele o Seasona—Ua ta'ua i latou "
              "o le nuu o Amona. E tusa o le 90–77 T.L.M.",
        "cells": [
            ("Ua poloaiina e le Alii", "The Lord commands"),
            ("Amona", "Ammon"),
            ("e taitai atu le nuu", "to lead the people"),
            ("o Aneti-Nifae-Liae", "of Anti-Nephi-Lehi"),
            ("i le saogalemu—", "to safety—"),
            ("Ina ua feiloai ma Alema,", "Upon meeting Alma,"),
            ("sa alu uma le malosi", "the strength is exhausted"),
            ("o Amona", "of Ammon"),
            ("i lona olioli tele—", "by his great joy—"),
            ("Ua tuu mai", "give"),
            ("e sa Nifaē", "The Nephites"),
            ("i le nuu o Aneti-Nifae-Liae", "to the Anti-Nephi-Lehies"),
            ("le laueleele o Seasona—", "the land of Jershon—"),
            ("Ua ta'ua i latou", "They are called"),
            ("o le nuu o Amona.", "the people of Ammon."),
            ("E tusa o le", "about"),
            ("90–77", "90–77"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|28": {
        "en": "The Lamanites are defeated in a tremendous battle—Tens of "
              "thousands are slain—The wicked are consigned to a state of "
              "endless woe; the righteous attain a never-ending happiness. "
              "About 77–76 B.C.",
        "sm": "Ua faatoilaloina sa Lamanā i se taua matautia tele—Ua fasiotia le "
              "tai sefulu o afe—Ua tuu e amioleaga i se tulaga o le malaia e le "
              "gata; e maua e e amiotonu se fiafia e le gata. E tusa o le 77–76 "
              "T.L.M.",
        "cells": [
            ("Ua faatoilaloina sa Lamanā", "The Lamanites are defeated"),
            ("i se taua matautia tele—", "in a tremendous battle—"),
            ("Ua fasiotia", "are slain"),
            ("le tai sefulu o afe—", "tens of thousands—"),
            ("Ua tuu e amioleaga", "The wicked are consigned"),
            ("i se tulaga o le malaia", "to a state of woe"),
            ("e le gata;", "endless;"),
            ("e maua e e amiotonu", "the righteous attain"),
            ("se fiafia e le gata.", "a never-ending happiness."),
            ("E tusa o le", "about"),
            ("77–76", "77–76"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|29": {
        "en": "Alma desires to cry repentance with angelic zeal—The Lord grants "
              "teachers for all nations—Alma glories in the Lord's work and in "
              "the success of Ammon and his brethren. About 76 B.C.",
        "sm": "Ua manao Alema e tala'i atu le salamo ma le finafinau tele "
              "faaagelu—Ua tuuina mai e le Alii faiaoga mo atunuu uma—Ua "
              "mitamita Alema i le galuega a le Alii ma le manuia o le galuega a "
              "Amona ma ona uso. E tusa o le 76 T.L.M.",
        "cells": [
            ("Ua manao Alema", "Alma desires"),
            ("e tala'i atu le salamo", "to cry repentance"),
            ("ma le finafinau tele faaagelu—", "with angelic zeal—"),
            ("Ua tuuina mai e le Alii", "The Lord grants"),
            ("faiaoga", "teachers"),
            ("mo atunuu uma—", "for all nations—"),
            ("Ua mitamita Alema", "Alma glories"),
            ("i le galuega", "in the work"),
            ("a le Alii", "of the Lord"),
            ("ma le manuia", "and in the success"),
            ("o le galuega", "of the work"),
            ("a Amona ma ona uso.", "of Ammon and his brethren."),
            ("E tusa o le", "about"),
            ("76", "76"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|30": {
        "en": "Korihor, the anti-Christ, ridicules Christ, the Atonement, and "
              "the spirit of prophecy—He teaches that there is no God, no fall "
              "of man, no penalty for sin, and no Christ—Alma testifies that "
              "Christ will come and that all things denote there is a "
              "God—Korihor demands a sign and is struck dumb—The devil had "
              "appeared to Korihor as an angel and taught him what to "
              "say—Korihor is trodden down and dies. About 76–74 B.C.",
        "sm": "Ua faatauemu Kori'oa, le aneti-Keriso ia Keriso, le Togiola, ma "
              "le agaga o valoaga—Ua ia a'oa'o atu faapea e leai se Atua, leai "
              "se pa'ū o le tagata, leai se faasalaga mo le agasala, ma e leai "
              "foi se Keriso—Ua molimau atu Alema o le a afio mai Keriso ma ua "
              "faaali mai i mea uma o loo i ai se Atua—Ua manao mai Kori'oa i se "
              "faailoga ma ua taia o ia ua gugū—Sa alu ane le tiapolo ia Kori'oa "
              "e pei o se agelu ma a'oa'o ia te ia mea e fai atu ai—Ua solia "
              "Kori'oa i lalo ma oti ai. E tusa o le 76–74 T.L.M.",
        "cells": [
            ("Ua faatauemu Kori'oa,", "Korihor ridicules,"),
            ("le aneti-Keriso", "the anti-Christ"),
            ("ia Keriso, le Togiola,", "Christ, the Atonement,"),
            ("ma le agaga o valoaga—", "and the spirit of prophecy—"),
            ("Ua ia a'oa'o atu faapea", "He teaches that"),
            ("e leai se Atua,", "there is no God,"),
            ("leai se pa'ū", "no fall"),
            ("o le tagata,", "of man,"),
            ("leai se faasalaga", "no penalty"),
            ("mo le agasala,", "for sin,"),
            ("ma e leai foi", "and no"),
            ("se Keriso—", "Christ—"),
            ("Ua molimau atu Alema", "Alma testifies"),
            ("o le a afio mai Keriso", "that Christ will come"),
            ("ma ua faaali mai", "and shows"),
            ("i mea uma", "in all things"),
            ("o loo i ai se Atua—", "there is a God—"),
            ("Ua manao mai Kori'oa", "Korihor demands"),
            ("i se faailoga", "a sign"),
            ("ma ua taia o ia", "and is struck"),
            ("ua gugū—", "dumb—"),
            ("Sa alu ane le tiapolo", "The devil had come"),
            ("ia Kori'oa", "to Korihor"),
            ("e pei o se agelu", "as an angel"),
            ("ma a'oa'o ia te ia", "and taught him"),
            ("mea e fai atu ai—", "what to say—"),
            ("Ua solia Kori'oa i lalo", "Korihor is trodden down"),
            ("ma oti ai.", "and dies."),
            ("E tusa o le", "about"),
            ("76–74", "76–74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|31": {
        "en": "Alma heads a mission to reclaim the apostate Zoramites—The "
              "Zoramites deny Christ, believe in a false concept of election, "
              "and worship with set prayers—The missionaries are filled with "
              "the Holy Spirit—Their afflictions are swallowed up in the joy of "
              "Christ. About 74 B.C.",
        "sm": "Ua ta'ita'i e Alema se misiona e toe aumai sa Soramā ua "
              "liliuese—Ua teena e sa Soramā Keriso, ua talitonu i se manatu "
              "sesē e uiga i filifiliga, ma tapuaiga i ni tatalo tauloto—Ua "
              "faatumulia faifeautalai i le Agaga Paia—Ua faatoilaloina o latou "
              "puapuaga i le olioli ia Keriso. E tusa o le 74 T.L.M.",
        "cells": [
            ("Ua ta'ita'i e Alema", "Alma heads"),
            ("se misiona", "a mission"),
            ("e toe aumai sa Soramā", "to reclaim the Zoramites"),
            ("ua liliuese—", "the apostate—"),
            ("Ua teena e sa Soramā", "The Zoramites deny"),
            ("Keriso,", "Christ,"),
            ("ua talitonu", "believe"),
            ("i se manatu sesē", "in a false concept"),
            ("e uiga i filifiliga,", "of election,"),
            ("ma tapuaiga", "and worship"),
            ("i ni tatalo tauloto—", "with set prayers—"),
            ("Ua faatumulia faifeautalai", "The missionaries are filled"),
            ("i le Agaga Paia—", "with the Holy Spirit—"),
            ("Ua faatoilaloina o latou puapuaga", "Their afflictions are swallowed up"),
            ("i le olioli ia Keriso.", "in the joy of Christ."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|32": {
        "en": "Alma teaches the poor whose afflictions had humbled them—Faith "
              "is a hope in that which is not seen which is true—Alma testifies "
              "that angels minister to men, women, and children—Alma compares "
              "the word unto a seed—It must be planted and nourished—Then it "
              "grows into a tree from which the fruit of eternal life is "
              "picked. About 74 B.C.",
        "sm": "Ua a'oa'o atu Alema i e matitiva o e na faalotomaualalaloina e o "
              "latou puapuaga—O le faatuatua o le faamoemoe lea i mea e le vaaia "
              "a ua moni—Ua molimau atu Alema e auauna mai agelu i tane, fafine, "
              "ma tamaiti—Ua faatusa e Alema le afioga i se fatu—E ao ina totō "
              "ma tausia—Ona tupu lea ma avea ma laau e tau mai ai le fua o le "
              "ola e faavavau. E tusa o le 74 T.L.M.",
        "cells": [
            ("Ua a'oa'o atu Alema", "Alma teaches"),
            ("i e matitiva", "the poor"),
            ("o e na faalotomaualalaloina", "who were humbled"),
            ("e o latou puapuaga—", "by their afflictions—"),
            ("O le faatuatua", "Faith"),
            ("o le faamoemoe lea", "is a hope"),
            ("i mea e le vaaia", "in that which is not seen"),
            ("a ua moni—", "which is true—"),
            ("Ua molimau atu Alema", "Alma testifies"),
            ("e auauna mai agelu", "that angels minister"),
            ("i tane, fafine, ma tamaiti—", "to men, women, and children—"),
            ("Ua faatusa e Alema", "Alma compares"),
            ("le afioga", "the word"),
            ("i se fatu—", "unto a seed—"),
            ("E ao ina totō", "It must be planted"),
            ("ma tausia—", "and nourished—"),
            ("Ona tupu lea", "Then it grows"),
            ("ma avea ma laau", "into a tree"),
            ("e tau mai ai", "from which is picked"),
            ("le fua", "the fruit"),
            ("o le ola e faavavau.", "of eternal life."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|33": {
        "en": "Zenos taught that men should pray and worship in all places, and "
              "that judgments are turned away because of the Son—Zenock taught "
              "that mercy is bestowed because of the Son—Moses had lifted up in "
              "the wilderness a type of the Son of God. About 74 B.C.",
        "sm": "Ua a'oa'o mai Senosa e tatau i tagata ona tatalo ma tapuai atu i "
              "mea uma, ma e liliu ese faamasinoga ona o le Alo—Ua a'oa'o mai "
              "Senoka e tuuina mai le alofa mutimutivale ona o le Alo—Sa sii "
              "a'e i luga e Mose i le vao se faatusa o le Alo o le Atua. E tusa "
              "o le 74 T.L.M.",
        "cells": [
            ("Ua a'oa'o mai Senosa", "Zenos taught"),
            ("e tatau i tagata", "that men should"),
            ("ona tatalo", "pray"),
            ("ma tapuai atu", "and worship"),
            ("i mea uma,", "in all places,"),
            ("ma e liliu ese faamasinoga", "and that judgments are turned away"),
            ("ona o le Alo—", "because of the Son—"),
            ("Ua a'oa'o mai Senoka", "Zenock taught"),
            ("e tuuina mai", "is bestowed"),
            ("le alofa mutimutivale", "mercy"),
            ("ona o le Alo—", "because of the Son—"),
            ("Sa sii a'e i luga", "had lifted up"),
            ("e Mose", "Moses"),
            ("i le vao", "in the wilderness"),
            ("se faatusa", "a type"),
            ("o le Alo", "of the Son"),
            ("o le Atua.", "of God."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|34": {
        "en": "Amulek testifies that the word is in Christ unto salvation—Unless "
              "an atonement is made, all mankind must perish—The whole law of "
              "Moses points toward the sacrifice of the Son of God—The eternal "
              "plan of redemption is based on faith and repentance—Pray for "
              "temporal and spiritual blessings—This life is the time for men "
              "to prepare to meet God—Work out your salvation with fear before "
              "God. About 74 B.C.",
        "sm": "Ua molimau Amoleka ua i ai ia Keriso le afioga mo le "
              "faaolataga—A le i ai se togiola, o le a fano tagata uma—Ua "
              "faasino atu le tulafono atoa a Mose i le taulaga a le Alo o le "
              "Atua—Ua faavae le fuafuaga faavavau o le togiolaina i le "
              "faatuatua ma le salamo—Ia tatalo mo faamanuiaga faaletino ma "
              "faaleagaga—O le olaga lenei o le taimi lea mo tagata e sauniuni "
              "ai e feiloai ma le Atua—Ia galueaiina lou faaolataga ma le mata'u "
              "i luma o le Atua. E tusa o le 74 T.L.M.",
        "cells": [
            ("Ua molimau Amoleka", "Amulek testifies"),
            ("ua i ai ia Keriso", "is in Christ"),
            ("le afioga", "the word"),
            ("mo le faaolataga—", "unto salvation—"),
            ("A le i ai", "Unless there is"),
            ("se togiola,", "an atonement,"),
            ("o le a fano tagata uma—", "all mankind must perish—"),
            ("Ua faasino atu", "points"),
            ("le tulafono atoa a Mose", "the whole law of Moses"),
            ("i le taulaga", "toward the sacrifice"),
            ("a le Alo", "of the Son"),
            ("o le Atua—", "of God—"),
            ("Ua faavae", "is based"),
            ("le fuafuaga faavavau", "the eternal plan"),
            ("o le togiolaina", "of redemption"),
            ("i le faatuatua", "on faith"),
            ("ma le salamo—", "and repentance—"),
            ("Ia tatalo mo faamanuiaga", "Pray for blessings"),
            ("faaletino ma faaleagaga—", "temporal and spiritual—"),
            ("O le olaga lenei", "This life"),
            ("o le taimi lea", "is the time"),
            ("mo tagata", "for men"),
            ("e sauniuni ai", "to prepare"),
            ("e feiloai ma le Atua—", "to meet God—"),
            ("Ia galueaiina lou faaolataga", "Work out your salvation"),
            ("ma le mata'u", "with fear"),
            ("i luma o le Atua.", "before God."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|35": {
        "en": "The preaching of the word destroys the craft of the "
              "Zoramites—They expel the converts, who then join the people of "
              "Ammon in Jershon—Alma sorrows because of the wickedness of the "
              "people. About 74 B.C.",
        "sm": "Ua faaumatia e le talaiga o le upu ia a'oa'oga sese a sa "
              "Soramā—Ua latou tutuli ese i latou o e na liliu, o e na aufaatasi "
              "ma le nuu o Amona i Season—Ua faanoanoa Alema ona o le amioleaga "
              "o le nuu. E tusa o le 74 T.L.M.",
        "cells": [
            ("Ua faaumatia", "destroys"),
            ("e le talaiga", "the preaching"),
            ("o le upu", "of the word"),
            ("ia a'oa'oga sese", "the false teachings"),
            ("a sa Soramā—", "of the Zoramites—"),
            ("Ua latou tutuli ese", "They expel"),
            ("i latou", "them"),
            ("o e na liliu,", "who were converted,"),
            ("o e na aufaatasi", "who join"),
            ("ma le nuu o Amona", "the people of Ammon"),
            ("i Season—", "in Jershon—"),
            ("Ua faanoanoa Alema", "Alma sorrows"),
            ("ona o le amioleaga", "because of the wickedness"),
            ("o le nuu.", "of the people."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|36": {
        "en": "Alma testifies to Helaman of his conversion after seeing an "
              "angel—He suffered the pains of a damned soul; he called upon the "
              "name of Jesus, and was then born of God—Sweet joy filled his "
              "soul—He saw concourses of angels praising God—Many converts have "
              "tasted and seen as he tasted and saw. About 74 B.C.",
        "sm": "Ua molimau atu Alema ia Helamana e uiga i lona liliu mai ina ua "
              "mavae ona ia vaai i se agelu—Sa mafatia o ia i tiga o se agaga ua "
              "faasalaina; sa valaau atu o ia i le suafa o Iesu, ma faapea ona "
              "fanauina ai o ia i la le Atua—Ua faatumulia lona agaga i le "
              "olioli logomalie—Ua vaai o ia i au agelu o loo vivii atu i le "
              "Atua—E toatele e na liua mai ua tofo ma vaai e pei ona ia tofo ma "
              "vaai. E tusa o le 74 T.L.M.",
        "cells": [
            ("Ua molimau atu Alema", "Alma testifies"),
            ("ia Helamana", "to Helaman"),
            ("e uiga i", "of"),
            ("lona liliu mai", "his conversion"),
            ("ina ua mavae", "after"),
            ("ona ia vaai", "he saw"),
            ("i se agelu—", "an angel—"),
            ("Sa mafatia o ia", "He suffered"),
            ("i tiga o se agaga", "the pains of a soul"),
            ("ua faasalaina;", "damned;"),
            ("sa valaau atu o ia", "he called upon"),
            ("i le suafa o Iesu,", "the name of Jesus,"),
            ("ma faapea", "and thus"),
            ("ona fanauina ai o ia", "he was born"),
            ("i la le Atua—", "of God—"),
            ("Ua faatumulia lona agaga", "filled his soul"),
            ("i le olioli logomalie—", "Sweet joy—"),
            ("Ua vaai o ia", "He saw"),
            ("i au agelu", "concourses of angels"),
            ("o loo vivii atu", "praising"),
            ("i le Atua—", "God—"),
            ("E toatele", "Many"),
            ("e na liua mai", "converts"),
            ("ua tofo ma vaai", "have tasted and seen"),
            ("e pei ona ia", "as he"),
            ("tofo ma vaai.", "tasted and saw."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|38": {
        "en": "Shiblon was persecuted for righteousness' sake—Salvation is in "
              "Christ, who is the life and the light of the world—Bridle all "
              "your passions. About 74 B.C.",
        "sm": "Sa sauaina Sepulona ona o le amiotonu—Ua ia Keriso le faaolataga, "
              "o lē o le ola ma le malamalama o le lalolagi—Ia pulea ou tuinanau "
              "uma. E tusa o le 74 T.L.M.",
        "cells": [
            ("Sa sauaina Sepulona", "Shiblon was persecuted"),
            ("ona o le amiotonu—", "for righteousness—"),
            ("Ua ia Keriso le faaolataga,", "Salvation is in Christ,"),
            ("o lē o le ola", "who is the life"),
            ("ma le malamalama", "and the light"),
            ("o le lalolagi—", "of the world—"),
            ("Ia pulea ou tuinanau uma.", "Bridle all your passions."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|37": {
        "en": "The plates of brass and other scriptures are preserved to bring "
              "souls to salvation—The Jaredites were destroyed because of their "
              "wickedness—Their secret oaths and covenants must be kept from "
              "the people—Counsel with the Lord in all your doings—As the "
              "Liahona guided the Nephites, so the word of Christ leads men to "
              "eternal life. About 74 B.C.",
        "sm": "Ua faasaoina papatusi apamemea ma isi tusitusiga paia e aumai ai "
              "agaga i le faaolataga—Sa faaumatia sa Iaretō ona o lo latou "
              "amioleaga—E ao ina taofia a latou tautoga ma feagaiga faalilolilo "
              "mai tagata—Filifili faatasi ma le Alii i mea uma e te faia—E pei "
              "ona sa taitaia sa Nifaē e le Liahona, e faapea foi ona taitai atu "
              "o tagata e le afioga a Keriso i le ola e faavavau. E tusa o le 74 "
              "T.L.M.",
        "cells": [
            ("Ua faasaoina papatusi apamemea", "The plates of brass are preserved"),
            ("ma isi tusitusiga paia", "and other scriptures"),
            ("e aumai ai agaga", "to bring souls"),
            ("i le faaolataga—", "to salvation—"),
            ("Sa faaumatia sa Iaretō", "The Jaredites were destroyed"),
            ("ona o lo latou amioleaga—", "because of their wickedness—"),
            ("E ao ina taofia", "must be kept"),
            ("a latou tautoga", "their oaths"),
            ("ma feagaiga faalilolilo", "and secret covenants"),
            ("mai tagata—", "from the people—"),
            ("Filifili faatasi ma le Alii", "Counsel with the Lord"),
            ("i mea uma", "in all things"),
            ("e te faia—", "you do—"),
            ("E pei ona", "As"),
            ("sa taitaia sa Nifaē", "the Nephites were guided"),
            ("e le Liahona,", "by the Liahona,"),
            ("e faapea foi", "so also"),
            ("ona taitai atu o tagata", "men are led"),
            ("e le afioga a Keriso", "by the word of Christ"),
            ("i le ola e faavavau.", "to eternal life."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|39": {
        "en": "Sexual sin is an abomination—Corianton's sins kept the Zoramites "
              "from receiving the word—Christ's redemption is retroactive in "
              "saving the faithful who preceded it. About 74 B.C.",
        "sm": "O le agasala o le feusuai o se mea inosia—O agasala a Korianetona "
              "ua taofia ai sa Soramā mai le taliaina o le upu—O le togiola a "
              "Keriso e aofia ai le faaolaina o e faamaoni na muamua mai a o "
              "le'i iai le togiola. E tusa o le 74 T.L.M.",
        "cells": [
            ("O le agasala o le feusuai", "The sin of sexual immorality"),
            ("o se mea inosia—", "is an abomination—"),
            ("O agasala a Korianetona", "Corianton's sins"),
            ("ua taofia ai sa Soramā", "kept the Zoramites"),
            ("mai le taliaina", "from receiving"),
            ("o le upu—", "the word—"),
            ("O le togiola a Keriso", "The redemption of Christ"),
            ("e aofia ai le faaolaina", "makes possible the salvation"),
            ("o e faamaoni", "of the faithful"),
            ("na muamua mai", "who came before"),
            ("a o le'i iai", "before there was"),
            ("le togiola.", "the redemption."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|40": {
        "en": "Christ brings to pass the resurrection of all men—The righteous "
              "dead go to paradise and the wicked to outer darkness to await "
              "the day of their resurrection—All things will be restored to "
              "their proper and perfect frame in the Resurrection. "
              "About 74 B.C.",
        "sm": "Ua aumai e Keriso le toetutu o tagata uma—O tagata amiotonu ua "
              "oti e o i le parataiso ae o ē ua amioleaga e o i le pogisa i fafo "
              "e faatalitali ai le aso o lo latou toetutū—O le a toefuatai mea "
              "uma lava i o latou tino tatau ai ma atoatoa i le Toetutu. E tusa "
              "o le 74 T.L.M.",
        "cells": [
            ("Ua aumai e Keriso", "Christ brings to pass"),
            ("le toetutu", "the resurrection"),
            ("o tagata uma—", "of all men—"),
            ("O tagata amiotonu ua oti", "The righteous dead"),
            ("e o i le parataiso", "go to paradise"),
            ("ae o ē ua amioleaga", "and the wicked"),
            ("e o i le pogisa", "to the darkness"),
            ("i fafo", "outer"),
            ("e faatalitali ai le aso", "to await the day"),
            ("o lo latou toetutū—", "of their resurrection—"),
            ("O le a toefuatai", "will be restored"),
            ("mea uma lava", "All things"),
            ("i o latou tino tatau ai", "to their proper frame"),
            ("ma atoatoa", "and perfect"),
            ("i le Toetutu.", "in the Resurrection."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|41": {
        "en": "In the Resurrection men come forth to a state of endless "
              "happiness or endless misery—Wickedness never was "
              "happiness—Carnal men are without God in the world—Every person "
              "receives again in the Restoration the characteristics and "
              "attributes acquired in mortality. About 74 B.C.",
        "sm": "I le Toetutū o le a tutula'i mai tagata i se tulaga o le fiafia e "
              "le gata po o le pagatia e le gata—E le'i avea lava le amioleaga "
              "ma fiafia—O tagata faaletino e aunoa ma le Atua i le lalolagi—E "
              "toe maua e tagata taitoatasi i le Toefuataiga uiga ma amioga na "
              "ia te ia i le olaga faaletino. E tusa o le 74 T.L.M.",
        "cells": [
            ("I le Toetutū", "In the Resurrection"),
            ("o le a tutula'i mai tagata", "men come forth"),
            ("i se tulaga", "to a state"),
            ("o le fiafia", "of happiness"),
            ("e le gata", "endless"),
            ("po o le pagatia", "or misery"),
            ("e le gata—", "endless—"),
            ("E le'i avea lava le amioleaga", "Wickedness never was"),
            ("ma fiafia—", "happiness—"),
            ("O tagata faaletino", "Carnal men"),
            ("e aunoa ma le Atua", "are without God"),
            ("i le lalolagi—", "in the world—"),
            ("E toe maua", "receives again"),
            ("e tagata taitoatasi", "Every person"),
            ("i le Toefuataiga", "in the Restoration"),
            ("uiga ma amioga", "the characteristics and attributes"),
            ("na ia te ia", "he had"),
            ("i le olaga faaletino.", "in mortality."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|42": {
        "en": "Mortality is a probationary time to enable man to repent and "
              "serve God—The Fall brought temporal and spiritual death upon all "
              "mankind—Redemption comes through repentance—God Himself atones "
              "for the sins of the world—Mercy is for those who repent—All "
              "others are subject to God's justice—Mercy comes because of the "
              "Atonement—Only the truly penitent are saved. About 74 B.C.",
        "sm": "O le olaga faaletino o se taimi e nofo vaavaaia ai e mafai ai e "
              "le tagata ona salamo ma auauna atu ai i le Atua—O le Pa'ū na oo "
              "mai ai le oti faaletino ma le oti faaleagaga i tagata uma—E oo "
              "mai le togiola e ala i le salamo—O le Atua lava Ia e togiola mo "
              "agasala a le lalolagi—O le alofa mutimutivale e mo i latou o e e "
              "salamo—O isi tagata uma o le a i lalo o le faamasinotonu o le "
              "Atua—E oo mai le alofa mutimutivale ona o le Togiola—Ua na'o e ua "
              "salamo faamaoni e faaolaina. E tusa o le 74 T.L.M.",
        "cells": [
            ("O le olaga faaletino", "Mortality"),
            ("o se taimi", "is a time"),
            ("e nofo vaavaaia ai", "of probation"),
            ("e mafai ai e le tagata", "to enable man"),
            ("ona salamo", "to repent"),
            ("ma auauna atu ai", "and serve"),
            ("i le Atua—", "God—"),
            ("O le Pa'ū", "The Fall"),
            ("na oo mai ai", "brought"),
            ("le oti faaletino", "temporal death"),
            ("ma le oti faaleagaga", "and spiritual death"),
            ("i tagata uma—", "upon all mankind—"),
            ("E oo mai le togiola", "Redemption comes"),
            ("e ala i le salamo—", "through repentance—"),
            ("O le Atua lava Ia", "God Himself"),
            ("e togiola mo agasala", "atones for the sins"),
            ("a le lalolagi—", "of the world—"),
            ("O le alofa mutimutivale", "Mercy"),
            ("e mo i latou", "is for those"),
            ("o e e salamo—", "who repent—"),
            ("O isi tagata uma", "All others"),
            ("o le a i lalo", "are subject to"),
            ("o le faamasinotonu", "the justice"),
            ("o le Atua—", "of God—"),
            ("E oo mai", "comes"),
            ("le alofa mutimutivale", "Mercy"),
            ("ona o le Togiola—", "because of the Atonement—"),
            ("Ua na'o", "Only"),
            ("e ua salamo faamaoni", "the truly penitent"),
            ("e faaolaina.", "are saved."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|43": {
        "en": "Alma and his sons preach the word—The Zoramites and other "
              "Nephite dissenters become Lamanites—The Lamanites come against "
              "the Nephites in war—Moroni arms the Nephites with defensive "
              "armor—The Lord reveals to Alma the strategy of the "
              "Lamanites—The Nephites defend their homes, liberties, families, "
              "and religion—The armies of Moroni and Lehi surround the "
              "Lamanites. About 74 B.C.",
        "sm": "Ua tala'i atu e Alema ma ona atalii le upu—Ua avea sa Soramā ma "
              "isi tagata faatuiese o sa Nifaē ma ni sa Lamanā—Ua o mai sa "
              "Lamanā e faasaga ia sa Nifaē i le taua—Ua faaauupega e Moronae sa "
              "Nifaē i ofutau puipui—Ua faaali e le Alii ia Alema le fuafuaga a "
              "sa Lamanā—Ua puipui e sa Nifaē o latou fale, saolotoga, aiga, ma "
              "la latou tapuaiga—Ua siomia sa Lamanā e autau a Moronae ma Liae. "
              "E tusa o le 74 T.L.M.",
        "cells": [
            ("Ua tala'i atu", "preach"),
            ("e Alema ma ona atalii", "Alma and his sons"),
            ("le upu—", "the word—"),
            ("Ua avea sa Soramā", "The Zoramites become"),
            ("ma isi tagata faatuiese", "and other dissenters"),
            ("o sa Nifaē", "of the Nephites"),
            ("ma ni sa Lamanā—", "into Lamanites—"),
            ("Ua o mai sa Lamanā", "The Lamanites come"),
            ("e faasaga ia sa Nifaē", "against the Nephites"),
            ("i le taua—", "in war—"),
            ("Ua faaauupega e Moronae", "Moroni arms"),
            ("sa Nifaē", "the Nephites"),
            ("i ofutau puipui—", "with defensive armor—"),
            ("Ua faaali e le Alii", "The Lord reveals"),
            ("ia Alema", "to Alma"),
            ("le fuafuaga a sa Lamanā—", "the strategy of the Lamanites—"),
            ("Ua puipui e sa Nifaē", "The Nephites defend"),
            ("o latou fale, saolotoga, aiga,", "their homes, liberties, families,"),
            ("ma la latou tapuaiga—", "and religion—"),
            ("Ua siomia sa Lamanā", "The Lamanites are surrounded"),
            ("e autau a Moronae", "by the armies of Moroni"),
            ("ma Liae.", "and Lehi."),
            ("E tusa o le", "about"),
            ("74", "74"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|44": {
        "en": "Moroni commands the Lamanites to make a covenant of peace or be "
              "destroyed—Zerahemnah rejects the offer, and the battle "
              "resumes—Moroni's armies defeat the Lamanites. About 74–73 B.C.",
        "sm": "Ua faatonu atu Moronae ia sa Lamanā ia faia se feagaiga o le "
              "filemu a leai o le a faaumatia i latou—Ua teena e Sera'emina le "
              "ofo, ma ua toe fai le taua—Ua faatoilalo e autau a Moronae sa "
              "Lamanā. E tusa o le 74–73 T.L.M.",
        "cells": [
            ("Ua faatonu atu Moronae", "Moroni commands"),
            ("ia sa Lamanā", "the Lamanites"),
            ("ia faia se feagaiga", "to make a covenant"),
            ("o le filemu", "of peace"),
            ("a leai", "or"),
            ("o le a faaumatia i latou—", "they will be destroyed—"),
            ("Ua teena e Sera'emina", "Zerahemnah rejects"),
            ("le ofo,", "the offer,"),
            ("ma ua toe fai", "and resumes"),
            ("le taua—", "the battle—"),
            ("Ua faatoilalo e autau a Moronae", "Moroni's armies defeat"),
            ("sa Lamanā.", "the Lamanites."),
            ("E tusa o le", "about"),
            ("74–73", "74–73"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|45": {
        "en": "Helaman believes the words of Alma—Alma prophesies the "
              "destruction of the Nephites—He blesses and curses the land—Alma "
              "may have been taken up by the Spirit, even as Moses—Dissension "
              "grows in the Church. About 73 B.C.",
        "sm": "Ua talitonu Helamana i upu a Alema—Ua valoia e Alema le faafanoga "
              "o sa Nifaē—Ua ia faamanuia ma fetuu le laueleele—Atonu na aveina "
              "a'e Alema e le Agaga, e pei lava o Mose—Ua tutupu tele "
              "faatuiesega i le Ekalesia. E tusa o le 73 T.L.M.",
        "cells": [
            ("Ua talitonu Helamana", "Helaman believes"),
            ("i upu a Alema—", "the words of Alma—"),
            ("Ua valoia e Alema", "Alma prophesies"),
            ("le faafanoga", "the destruction"),
            ("o sa Nifaē—", "of the Nephites—"),
            ("Ua ia faamanuia ma fetuu", "He blesses and curses"),
            ("le laueleele—", "the land—"),
            ("Atonu na aveina a'e Alema", "Alma may have been taken up"),
            ("e le Agaga,", "by the Spirit,"),
            ("e pei lava o Mose—", "even as Moses—"),
            ("Ua tutupu tele faatuiesega", "Dissension grows"),
            ("i le Ekalesia.", "in the Church."),
            ("E tusa o le", "about"),
            ("73", "73"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|46": {
        "en": "Amalickiah conspires to be king—Moroni raises the title of "
              "liberty—He rallies the people to defend their religion—True "
              "believers are called Christians—A remnant of Joseph will be "
              "preserved—Amalickiah and the dissenters flee to the land of "
              "Nephi—Those who will not support the cause of freedom are put to "
              "death. About 73–72 B.C.",
        "sm": "Ua faufau leaga Amalekia ia avea ma tupu—Ua sisi a'e e Moronae le "
              "tagavai o le saolotoga—Ua ia tomatauina le nuu ia puipui la latou "
              "tapuaiga—O e ua talitonu faamaoni ua ta'ua o Kerisiano—O le a "
              "faasaoina se vaega o totoe o Iosefa—Ua sosola Amalekia ma e "
              "faatuiese i le laueleele o Nifae—O i latou o ē e lē lagolagoina "
              "le faamoemoe o le saolotoga o le a fasiotia. E tusa o le 73–72 "
              "T.L.M.",
        "cells": [
            ("Ua faufau leaga Amalekia", "Amalickiah conspires"),
            ("ia avea ma tupu—", "to be king—"),
            ("Ua sisi a'e e Moronae", "Moroni raises"),
            ("le tagavai", "the title"),
            ("o le saolotoga—", "of liberty—"),
            ("Ua ia tomatauina le nuu", "He rallies the people"),
            ("ia puipui la latou tapuaiga—", "to defend their religion—"),
            ("O e ua talitonu faamaoni", "True believers"),
            ("ua ta'ua o Kerisiano—", "are called Christians—"),
            ("O le a faasaoina", "will be preserved"),
            ("se vaega o totoe", "A remnant"),
            ("o Iosefa—", "of Joseph—"),
            ("Ua sosola Amalekia", "Amalickiah flees"),
            ("ma e faatuiese", "and the dissenters"),
            ("i le laueleele o Nifae—", "to the land of Nephi—"),
            ("O i latou o ē", "Those who"),
            ("e lē lagolagoina", "will not support"),
            ("le faamoemoe o le saolotoga", "the cause of freedom"),
            ("o le a fasiotia.", "are put to death."),
            ("E tusa o le", "about"),
            ("73–72", "73–72"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|47": {
        "en": "Amalickiah uses treachery, murder, and intrigue to become king "
              "of the Lamanites—The Nephite dissenters are more wicked and "
              "ferocious than the Lamanites. About 72 B.C.",
        "sm": "Ua faaaoga e Amalekia le taufaalata, le fasioti tagata, ma "
              "fuafuaga faalilolilo ia avea ai ma tupu o sa Lamanā—O tagata "
              "faatuiese o sa Nifaē ua sili atu ona amioleaga ma fe'ai nai lo sa "
              "Lamanā. E tusa o le 72 T.L.M.",
        "cells": [
            ("Ua faaaoga e Amalekia", "Amalickiah uses"),
            ("le taufaalata,", "treachery,"),
            ("le fasioti tagata,", "murder,"),
            ("ma fuafuaga faalilolilo", "and intrigue"),
            ("ia avea ai ma tupu", "to become king"),
            ("o sa Lamanā—", "of the Lamanites—"),
            ("O tagata faatuiese", "The dissenters"),
            ("o sa Nifaē", "of the Nephites"),
            ("ua sili atu ona amioleaga", "are more wicked"),
            ("ma fe'ai", "and ferocious"),
            ("nai lo sa Lamanā.", "than the Lamanites."),
            ("E tusa o le", "about"),
            ("72", "72"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|48": {
        "en": "Amalickiah incites the Lamanites against the Nephites—Moroni "
              "prepares his people to defend the cause of the Christians—He "
              "rejoices in liberty and freedom and is a mighty man of God. "
              "About 72 B.C.",
        "sm": "Ua faaoso e Amalekia sa Lamanā e faasaga ia sa Nifaē—Ua saunia e "
              "Moronae ona tagata e puipui le faamoemoe o tagata Kerisiano—Ua "
              "olioli o ia i le filifiliga saoloto ma le saolotoga ma o ia o se "
              "tagata malosi o le Atua. E tusa o le 72 T.L.M.",
        "cells": [
            ("Ua faaoso e Amalekia", "Amalickiah incites"),
            ("sa Lamanā", "the Lamanites"),
            ("e faasaga ia sa Nifaē—", "against the Nephites—"),
            ("Ua saunia e Moronae", "Moroni prepares"),
            ("ona tagata", "his people"),
            ("e puipui le faamoemoe", "to defend the cause"),
            ("o tagata Kerisiano—", "of the Christians—"),
            ("Ua olioli o ia", "He rejoices"),
            ("i le filifiliga saoloto", "in liberty"),
            ("ma le saolotoga", "and freedom"),
            ("ma o ia", "and he is"),
            ("o se tagata malosi", "a mighty man"),
            ("o le Atua.", "of God."),
            ("E tusa o le", "about"),
            ("72", "72"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|49": {
        "en": "The invading Lamanites are unable to take the fortified cities "
              "of Ammonihah and Noah—Amalickiah curses God and swears to drink "
              "the blood of Moroni—Helaman and his brethren continue to "
              "strengthen the Church. About 72 B.C.",
        "sm": "Ua le mafai e osofaiga a sa Lamanā ona faatoilalo aai tu'iolo o "
              "Amonaea ma Noa—Ua upuleaga e Amalekia le Atua ma ua tauto na te "
              "inuina le toto o Moronae—Ua faaauau e Helamana ma ona uso ona "
              "faamalosi le Ekalesia. E tusa o le 72 T.L.M.",
        "cells": [
            ("Ua le mafai", "are unable"),
            ("e osofaiga a sa Lamanā", "the invading Lamanites"),
            ("ona faatoilalo aai tu'iolo", "to take the fortified cities"),
            ("o Amonaea ma Noa—", "of Ammonihah and Noah—"),
            ("Ua upuleaga e Amalekia", "Amalickiah curses"),
            ("le Atua", "God"),
            ("ma ua tauto", "and swears"),
            ("na te inuina le toto", "to drink the blood"),
            ("o Moronae—", "of Moroni—"),
            ("Ua faaauau e Helamana", "Helaman continues"),
            ("ma ona uso", "and his brethren"),
            ("ona faamalosi le Ekalesia.", "to strengthen the Church."),
            ("E tusa o le", "about"),
            ("72", "72"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|50": {
        "en": "Moroni fortifies the lands of the Nephites—They build many new "
              "cities—Wars and destructions befell the Nephites in the days of "
              "their wickedness and abominations—Morianton and his dissenters "
              "are defeated by Teancum—Nephihah dies, and his son Pahoran fills "
              "the judgment seat. About 72–67 B.C.",
        "sm": "Ua tu'iolo e Moronae laueleele o sa Nifaē—Ua latou fausia ni aai "
              "fou e tele—E pa'u'ū ifo taua ma faafanoga i luga o sa Nifaē i aso "
              "o lo latou amioleaga ma fai mea inosia—Ua faatoilaloina "
              "Morianetona ma ona tagata faatuiese e Teanekuma—Ua maliu Nifaea, "
              "ma ua nofo lona atalii o Paorana i le nofoa-faamasino. E tusa o "
              "le 72–67 T.L.M.",
        "cells": [
            ("Ua tu'iolo e Moronae", "Moroni fortifies"),
            ("laueleele o sa Nifaē—", "the lands of the Nephites—"),
            ("Ua latou fausia", "They build"),
            ("ni aai fou e tele—", "many new cities—"),
            ("E pa'u'ū ifo", "befall"),
            ("taua ma faafanoga", "Wars and destructions"),
            ("i luga o sa Nifaē", "upon the Nephites"),
            ("i aso o lo latou", "in the days of their"),
            ("amioleaga", "wickedness"),
            ("ma fai mea inosia—", "and abominations—"),
            ("Ua faatoilaloina Morianetona", "Morianton is defeated"),
            ("ma ona tagata faatuiese", "and his dissenters"),
            ("e Teanekuma—", "by Teancum—"),
            ("Ua maliu Nifaea,", "Nephihah dies,"),
            ("ma ua nofo", "and fills"),
            ("lona atalii o Paorana", "his son Pahoran"),
            ("i le nofoa-faamasino.", "the judgment seat."),
            ("E tusa o le", "about"),
            ("72–67", "72–67"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|51": {
        "en": "The king-men seek to change the law and set up a king—Pahoran "
              "and the freemen are supported by the voice of the people—Moroni "
              "compels the king-men to defend their country or be put to "
              "death—Amalickiah and the Lamanites capture many fortified "
              "cities—Teancum repels the Lamanite invasion and slays Amalickiah "
              "in his tent. About 67–66 B.C.",
        "sm": "Ua saili tagata-o-tupu e sui le tulafono ma faatuina se tupu—Ua "
              "lagolagoina Paorana ma tagata-saoloto e le leo o le nuu—Ua "
              "faamalosi e Moronae tagata-o-tupu ia latou puipui lo latou atunuu "
              "a leai o le a fasioti i latou—Ua maua e Amalekia ma sa Lamanā le "
              "tele o aai tu'iolo—Ua faatoilalo e Teanekuma osofaiga a sa Lamanā "
              "ma fasioti Amalekia i lona faleie. E tusa o le 67–66 T.L.M.",
        "cells": [
            ("Ua saili tagata-o-tupu", "The king-men seek"),
            ("e sui le tulafono", "to change the law"),
            ("ma faatuina se tupu—", "and set up a king—"),
            ("Ua lagolagoina Paorana ma tagata-saoloto", "Pahoran and the freemen are supported"),
            ("e le leo", "by the voice"),
            ("o le nuu—", "of the people—"),
            ("Ua faamalosi e Moronae tagata-o-tupu", "Moroni compels the king-men"),
            ("ia latou puipui", "to defend"),
            ("lo latou atunuu", "their country"),
            ("a leai", "or"),
            ("o le a fasioti i latou—", "they will be slain—"),
            ("Ua maua e Amalekia", "Amalickiah captures"),
            ("ma sa Lamanā", "and the Lamanites"),
            ("le tele o aai tu'iolo—", "many fortified cities—"),
            ("Ua faatoilalo e Teanekuma", "Teancum repels"),
            ("osofaiga a sa Lamanā", "the Lamanite invasion"),
            ("ma fasioti Amalekia", "and slays Amalickiah"),
            ("i lona faleie.", "in his tent."),
            ("E tusa o le", "about"),
            ("67–66", "67–66"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|52": {
        "en": "Ammoron succeeds Amalickiah as king of the Lamanites—Moroni, "
              "Teancum, and Lehi lead the Nephites in a victorious war against "
              "the Lamanites—The city of Mulek is retaken, and Jacob the "
              "Zoramite is slain. About 66–64 B.C.",
        "sm": "Ua sui Amorona ia Amalekia i le avea ma tupu o sa Lamanā—Ua "
              "taitai e Moronae, Teanekuma, ma Liae, sa Nifaē i se taua manumalo "
              "e faasaga ia sa Lamanā—Ua toe maua mai le aai o Moleka, ma ua "
              "fasiotia Iakopo le sa Soramā. E tusa o le 66–64 T.L.M.",
        "cells": [
            ("Ua sui Amorona ia Amalekia", "Ammoron succeeds Amalickiah"),
            ("i le avea ma tupu", "as king"),
            ("o sa Lamanā—", "of the Lamanites—"),
            ("Ua taitai", "lead"),
            ("e Moronae, Teanekuma, ma Liae,", "Moroni, Teancum, and Lehi"),
            ("sa Nifaē", "the Nephites"),
            ("i se taua manumalo", "in a victorious war"),
            ("e faasaga ia sa Lamanā—", "against the Lamanites—"),
            ("Ua toe maua mai", "is retaken"),
            ("le aai o Moleka,", "The city of Mulek,"),
            ("ma ua fasiotia Iakopo", "and Jacob is slain"),
            ("le sa Soramā.", "the Zoramite."),
            ("E tusa o le", "about"),
            ("66–64", "66–64"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|53": {
        "en": "The Lamanite prisoners are used to fortify the city "
              "Bountiful—Dissensions among the Nephites give rise to Lamanite "
              "victories—Helaman takes command of the two thousand stripling "
              "sons of the people of Ammon. About 64–63 B.C.",
        "sm": "Ua faaaoga pagotā sa Lamanā e tu'iolo le aai o Nuumau—O "
              "faatuiesega i totonu o sa Nifaē ua oo ai ina manumalo ia sa "
              "Lamanā—Ua taitai Helamana i atalii talavou e lua afe o le nuu o "
              "Amona. E tusa o le 64–63 T.L.M.",
        "cells": [
            ("Ua faaaoga pagotā sa Lamanā", "The Lamanite prisoners are used"),
            ("e tu'iolo", "to fortify"),
            ("le aai o Nuumau—", "the city Bountiful—"),
            ("O faatuiesega", "Dissensions"),
            ("i totonu o sa Nifaē", "among the Nephites"),
            ("ua oo ai ina manumalo", "give rise to victories"),
            ("ia sa Lamanā—", "for the Lamanites—"),
            ("Ua taitai Helamana", "Helaman takes command"),
            ("i atalii talavou", "of the stripling sons"),
            ("e lua afe", "two thousand"),
            ("o le nuu o Amona.", "of the people of Ammon."),
            ("E tusa o le", "about"),
            ("64–63", "64–63"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|54": {
        "en": "Ammoron and Moroni negotiate for the exchange of "
              "prisoners—Moroni demands that the Lamanites withdraw and cease "
              "their murderous attacks—Ammoron demands that the Nephites lay "
              "down their arms and become subject to the Lamanites. "
              "About 63 B.C.",
        "sm": "Ua feutagai Amorona ma Moronae mo le fesuiaiga o pagota—Ua "
              "faatonu atu Moronae ia sa Lamanā ia solomuli ma tuu a latou "
              "osofaiga fasioti tagata—Ua faatonu mai Amorona ia sa Nifaē ia tuu "
              "i lalo a latou auupega ma ia tuu atu i latou lava i le pulega a "
              "sa Lamanā. E tusa o le 63 T.L.M.",
        "cells": [
            ("Ua feutagai Amorona ma Moronae", "Ammoron and Moroni negotiate"),
            ("mo le fesuiaiga o pagota—", "for the exchange of prisoners—"),
            ("Ua faatonu atu Moronae", "Moroni demands"),
            ("ia sa Lamanā", "that the Lamanites"),
            ("ia solomuli", "withdraw"),
            ("ma tuu a latou osofaiga", "and cease their attacks"),
            ("fasioti tagata—", "murderous—"),
            ("Ua faatonu mai Amorona", "Ammoron demands"),
            ("ia sa Nifaē", "that the Nephites"),
            ("ia tuu i lalo", "lay down"),
            ("a latou auupega", "their arms"),
            ("ma ia tuu atu", "and submit"),
            ("i latou lava", "themselves"),
            ("i le pulega", "to the rule"),
            ("a sa Lamanā.", "of the Lamanites."),
            ("E tusa o le", "about"),
            ("63", "63"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|55": {
        "en": "Moroni refuses to exchange prisoners—The Lamanite guards are "
              "enticed to become drunk, and the Nephite prisoners are "
              "freed—The city of Gid is taken without bloodshed. About 63–62 "
              "B.C.",
        "sm": "Ua musu Moronae e faafesuiai pagota—Ua faalata leoleo sa Lamanā "
              "ia onana, ma ua tatala saoloto pagota sa Nifaē—Ua ave le aai o "
              "Kita e aunoa ma se totomasaa. E tusa o le 63–62 T.L.M.",
        "cells": [
            ("Ua musu Moronae", "Moroni refuses"),
            ("e faafesuiai pagota—", "to exchange prisoners—"),
            ("Ua faalata leoleo sa Lamanā", "The Lamanite guards are enticed"),
            ("ia onana,", "to become drunk,"),
            ("ma ua tatala saoloto", "and are freed"),
            ("pagota sa Nifaē—", "the Nephite prisoners—"),
            ("Ua ave", "is taken"),
            ("le aai o Kita", "The city of Gid"),
            ("e aunoa ma se totomasaa.", "without bloodshed."),
            ("E tusa o le", "about"),
            ("63–62", "63–62"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|56": {
        "en": "Helaman sends an epistle to Moroni, recounting the state of the "
              "war with the Lamanites—Antipus and Helaman gain a great victory "
              "over the Lamanites—Helaman's two thousand stripling sons fight "
              "with miraculous power, and none of them are slain.",
        "sm": "Ua auina atu e Helamana se tusi ia Moronae, ua faamatala atu ai "
              "le tulaga o le taua ma sa Lamanā—Ua maua e Anetipa ma Helamana se "
              "manumalo tele ia sa Lamanā—Ua tau atalii talavou e lua afe a "
              "Helamana ma se mana faavavega, ma ua leai se tasi o i latou ua "
              "fasiotia.",
        "cells": [
            ("Ua auina atu e Helamana", "Helaman sends"),
            ("se tusi", "an epistle"),
            ("ia Moronae,", "to Moroni,"),
            ("ua faamatala atu ai", "recounting"),
            ("le tulaga o le taua", "the state of the war"),
            ("ma sa Lamanā—", "with the Lamanites—"),
            ("Ua maua e Anetipa ma Helamana", "Antipus and Helaman gain"),
            ("se manumalo tele", "a great victory"),
            ("ia sa Lamanā—", "over the Lamanites—"),
            ("Ua tau atalii talavou", "the stripling sons fight"),
            ("e lua afe a Helamana", "Helaman's two thousand"),
            ("ma se mana faavavega,", "with miraculous power,"),
            ("ma ua leai se tasi", "and none"),
            ("o i latou", "of them"),
            ("ua fasiotia.", "are slain."),
        ],
    },
    "alma|57": {
        "en": "Helaman recounts the taking of Antiparah and the surrender and "
              "later the defense of Cumeni—His Ammonite striplings fight "
              "valiantly; all are wounded, but none are slain—Gid reports the "
              "slaying and the escape of the Lamanite prisoners. About 63 B.C.",
        "sm": "Ua faamatala mai e Helamana le aveina o Anetipara ma le toilalo "
              "ma le puipuiga mulimuli ane ai o Kumenae—Ua tau ma le totoa lana "
              "autalavou sa Amonā; ua manunua uma, ae ua leai se tasi na "
              "fasiotia—Ua lipoti mai e Kita le fasiotiga ma le sola'aga o "
              "pagota sa Lamanā. E tusa o le 63 T.L.M.",
        "cells": [
            ("Ua faamatala mai e Helamana", "Helaman recounts"),
            ("le aveina o Anetipara", "the taking of Antiparah"),
            ("ma le toilalo", "and the surrender"),
            ("ma le puipuiga", "and the defense"),
            ("mulimuli ane ai o Kumenae—", "later of Cumeni—"),
            ("Ua tau ma le totoa", "fight valiantly"),
            ("lana autalavou sa Amonā;", "His Ammonite striplings;"),
            ("ua manunua uma,", "all are wounded,"),
            ("ae ua leai se tasi", "but none"),
            ("na fasiotia—", "are slain—"),
            ("Ua lipoti mai e Kita", "Gid reports"),
            ("le fasiotiga ma le sola'aga", "the slaying and the escape"),
            ("o pagota sa Lamanā.", "of the Lamanite prisoners."),
            ("E tusa o le", "about"),
            ("63", "63"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|58": {
        "en": "Helaman, Gid, and Teomner take the city of Manti by a "
              "stratagem—The Lamanites withdraw—The sons of the people of Ammon "
              "are preserved as they stand fast in defense of their liberty and "
              "faith. About 63–62 B.C.",
        "sm": "Ua maua e Helamana, Kita, ma Teominea le aai o Maneti i se "
              "togafiti—Ua tuumuli sa Lamanā—Ua faasaoina atalii o le nuu o "
              "Amona ao latou tutulai mausali i le puipuiga o lo latou saolotoga "
              "ma lo latou faatuatuaga. E tusa o le 63–62 T.L.M.",
        "cells": [
            ("Ua maua", "take"),
            ("e Helamana, Kita, ma Teominea", "Helaman, Gid, and Teomner"),
            ("le aai o Maneti", "the city of Manti"),
            ("i se togafiti—", "by a stratagem—"),
            ("Ua tuumuli sa Lamanā—", "The Lamanites withdraw—"),
            ("Ua faasaoina atalii", "The sons are preserved"),
            ("o le nuu o Amona", "of the people of Ammon"),
            ("ao latou tutulai mausali", "as they stand fast"),
            ("i le puipuiga", "in defense"),
            ("o lo latou saolotoga", "of their liberty"),
            ("ma lo latou faatuatuaga.", "and faith."),
            ("E tusa o le", "about"),
            ("63–62", "63–62"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|59": {
        "en": "Moroni asks Pahoran to strengthen the forces of Helaman—The "
              "Lamanites take the city of Nephihah—Moroni is angry with the "
              "government. About 62 B.C.",
        "sm": "Ua talosaga atu Moronae ia Paorana ia faamalosia le autau a "
              "Helamana—Ua ave e sa Lamanā le aai o Nifaea—Ua ita Moronae i le "
              "malo. E tusa o le 62 T.L.M.",
        "cells": [
            ("Ua talosaga atu Moronae", "Moroni asks"),
            ("ia Paorana", "Pahoran"),
            ("ia faamalosia", "to strengthen"),
            ("le autau a Helamana—", "the forces of Helaman—"),
            ("Ua ave e sa Lamanā", "The Lamanites take"),
            ("le aai o Nifaea—", "the city of Nephihah—"),
            ("Ua ita Moronae", "Moroni is angry"),
            ("i le malo.", "with the government."),
            ("E tusa o le", "about"),
            ("62", "62"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|60": {
        "en": "Moroni complains to Pahoran of the government's neglect of the "
              "armies—The Lord suffers the righteous to be slain—The Nephites "
              "must use all of their power and means to deliver themselves from "
              "their enemies—Moroni threatens to fight against the government "
              "unless help is supplied to his armies. About 62 B.C.",
        "sm": "Ua muimui atu Moronae ia Paorana e uiga i le faatamala o le malo "
              "i autau—E tuu e le Alii tagata amiotonu ia fasiotia—E ao ia sa "
              "Nifaē ona faaaoga lo latou malosi ma mea e laveai ai i latou lava "
              "mai i o latou fili—Ua faamata'u atu Moronae e alu atu e tau "
              "faasaga i le malo vagana ai ua tuuina mai se fesoasoani i ana "
              "autau. E tusa o le 62 T.L.M.",
        "cells": [
            ("Ua muimui atu Moronae", "Moroni complains"),
            ("ia Paorana", "to Pahoran"),
            ("e uiga i le faatamala", "of the neglect"),
            ("o le malo i autau—", "by the government of the armies—"),
            ("E tuu e le Alii", "The Lord suffers"),
            ("tagata amiotonu ia fasiotia—", "the righteous to be slain—"),
            ("E ao ia sa Nifaē", "The Nephites must"),
            ("ona faaaoga lo latou malosi", "use their power"),
            ("ma mea e laveai ai", "and means to deliver"),
            ("i latou lava", "themselves"),
            ("mai i o latou fili—", "from their enemies—"),
            ("Ua faamata'u atu Moronae", "Moroni threatens"),
            ("e alu atu", "to go"),
            ("e tau faasaga", "to fight against"),
            ("i le malo", "the government"),
            ("vagana ai", "unless"),
            ("ua tuuina mai se fesoasoani", "help is supplied"),
            ("i ana autau.", "to his armies."),
            ("E tusa o le", "about"),
            ("62", "62"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|61": {
        "en": "Pahoran tells Moroni of the insurrection and rebellion against "
              "the government—The king-men take Zarahemla and are in league "
              "with the Lamanites—Pahoran asks for military aid against the "
              "rebels. About 62 B.C.",
        "sm": "Ua ta'u atu e Paorana ia Moronae e uiga i le faatu'iesega ma le "
              "fouvalega e faasaga i le malo—Ua ave e tagata-o-tupu Sara'emila "
              "ma ua aufaatasi ma sa Lamanā—Ua talosaga mai Paorana mo se "
              "fesoasoani faaleautau e faasaga i e ua fouvale. E tusa o le 62 "
              "T.L.M.",
        "cells": [
            ("Ua ta'u atu e Paorana", "Pahoran tells"),
            ("ia Moronae", "Moroni"),
            ("e uiga i le faatu'iesega", "of the insurrection"),
            ("ma le fouvalega", "and rebellion"),
            ("e faasaga i le malo—", "against the government—"),
            ("Ua ave e tagata-o-tupu Sara'emila", "The king-men take Zarahemla"),
            ("ma ua aufaatasi", "and are in league"),
            ("ma sa Lamanā—", "with the Lamanites—"),
            ("Ua talosaga mai Paorana", "Pahoran asks"),
            ("mo se fesoasoani faaleautau", "for military aid"),
            ("e faasaga", "against"),
            ("i e ua fouvale.", "the rebels."),
            ("E tusa o le", "about"),
            ("62", "62"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|62": {
        "en": "Moroni marches to the aid of Pahoran in the land of Gideon—The "
              "king-men who refuse to defend their country are put to "
              "death—Pahoran and Moroni retake Nephihah—Many Lamanites join the "
              "people of Ammon—Teancum slays Ammoron and is in turn slain—The "
              "Lamanites are driven from the land, and peace is "
              "established—Helaman returns to the ministry and builds up the "
              "Church. About 62–57 B.C.",
        "sm": "Ua savali atu Moronae e fesoasoani ia Paorana i le laueleele o "
              "Kitiona—Ua fasiotia tagata-o-tupu o e na mumusu e puipui lo latou "
              "atunuu—Ua toe ave e Paorana ma Moronae le aai o Nifaea—E toatele "
              "sa Lamanā ua aufaatasi ma le nuu o Amona—Ua fasioti e Teanekuma o "
              "Amorona ma ua fasiotia ai foi o ia—Ua tulia sa Lamanā mai le "
              "laueleele, ma ua faatuina le filemu—Ua toe foi atu Helamana i le "
              "auaunaga ma atiae le Ekalesia. E tusa o le 62–57 T.L.M.",
        "cells": [
            ("Ua savali atu Moronae", "Moroni marches"),
            ("e fesoasoani ia Paorana", "to the aid of Pahoran"),
            ("i le laueleele o Kitiona—", "in the land of Gideon—"),
            ("Ua fasiotia tagata-o-tupu", "The king-men are put to death"),
            ("o e na mumusu", "who refuse"),
            ("e puipui lo latou atunuu—", "to defend their country—"),
            ("Ua toe ave", "retake"),
            ("e Paorana ma Moronae", "Pahoran and Moroni"),
            ("le aai o Nifaea—", "Nephihah—"),
            ("E toatele sa Lamanā", "Many Lamanites"),
            ("ua aufaatasi", "join"),
            ("ma le nuu o Amona—", "the people of Ammon—"),
            ("Ua fasioti e Teanekuma o Amorona", "Teancum slays Ammoron"),
            ("ma ua fasiotia ai foi o ia—", "and is in turn slain—"),
            ("Ua tulia sa Lamanā", "The Lamanites are driven"),
            ("mai le laueleele,", "from the land,"),
            ("ma ua faatuina le filemu—", "and peace is established—"),
            ("Ua toe foi atu Helamana", "Helaman returns"),
            ("i le auaunaga", "to the ministry"),
            ("ma atiae le Ekalesia.", "and builds up the Church."),
            ("E tusa o le", "about"),
            ("62–57", "62–57"),
            ("T.L.M.", "B.C."),
        ],
    },
    "alma|63": {
        "en": "Shiblon and later Helaman take possession of the sacred "
              "records—Many Nephites travel to the land northward—Hagoth builds "
              "ships, which sail forth in the west sea—Moronihah defeats the "
              "Lamanites in battle. About 56–52 B.C.",
        "sm": "Ua ave e Sepulona le tausiga o talafaamaumau ae mulimuli ane ave "
              "e Helamana—Ua malaga atu le toatele o sa Nifaē i le laueleele i "
              "matu—Ua fau e Hakota ni vaa, ia na folau atu i le sami i "
              "sisifo—Ua faatoilalo e Moronaea sa Lamanā i le taua. E tusa o le "
              "56–52 T.L.M.",
        "cells": [
            ("Ua ave e Sepulona", "Shiblon takes"),
            ("le tausiga o talafaamaumau", "the sacred records"),
            ("ae mulimuli ane", "and later"),
            ("ave e Helamana—", "Helaman takes—"),
            ("Ua malaga atu", "travel"),
            ("le toatele o sa Nifaē", "Many Nephites"),
            ("i le laueleele i matu—", "to the land northward—"),
            ("Ua fau e Hakota", "Hagoth builds"),
            ("ni vaa,", "ships,"),
            ("ia na folau atu", "which sail forth"),
            ("i le sami i sisifo—", "in the west sea—"),
            ("Ua faatoilalo e Moronaea sa Lamanā", "Moronihah defeats the Lamanites"),
            ("i le taua.", "in battle."),
            ("E tusa o le", "about"),
            ("56–52", "56–52"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|1": {
        "en": "Pahoran the second becomes chief judge and is murdered by "
              "Kishkumen—Pacumeni fills the judgment seat—Coriantumr leads the "
              "Lamanite armies, takes Zarahemla, and slays Pacumeni—Moronihah "
              "defeats the Lamanites and retakes Zarahemla, and Coriantumr is "
              "slain. About 52–50 B.C.",
        "sm": "Ua avea Paorana le lua ma faamasino sili ma ua fasiotia e "
              "Kisakumena—Ua nofoia e Pakumenae le nofoa-faamasino—Ua ta'ita'i e "
              "Korianetuma autau a sa Lamanā, ua avea Sara'emila, ma ua fasiotia "
              "Pakumenae—Ua faatoilaloina e Moronaea sa Lamanā ma toe ave "
              "Sara'emila, ma ua fasiotia Korianetuma. E tusa o le 52–50 T.L.M.",
        "cells": [
            ("Ua avea Paorana le lua", "Pahoran the second becomes"),
            ("ma faamasino sili", "chief judge"),
            ("ma ua fasiotia e Kisakumena—", "and is murdered by Kishkumen—"),
            ("Ua nofoia e Pakumenae le nofoa-faamasino—", "Pacumeni fills the judgment seat—"),
            ("Ua ta'ita'i e Korianetuma", "Coriantumr leads"),
            ("autau a sa Lamanā,", "the Lamanite armies,"),
            ("ua avea Sara'emila,", "takes Zarahemla,"),
            ("ma ua fasiotia Pakumenae—", "and slays Pacumeni—"),
            ("Ua faatoilaloina e Moronaea sa Lamanā", "Moronihah defeats the Lamanites"),
            ("ma toe ave Sara'emila,", "and retakes Zarahemla,"),
            ("ma ua fasiotia Korianetuma.", "and Coriantumr is slain."),
            ("E tusa o le", "about"),
            ("52–50", "52–50"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|2": {
        "en": "Helaman, the son of Helaman, becomes chief judge—Gadianton "
              "leads the band of Kishkumen—Helaman's servant slays Kishkumen, "
              "and the Gadianton band flees into the wilderness. "
              "About 50–49 B.C.",
        "sm": "Ua avea Helamana, le atalii o Helamana, ma faamasino sili—Ua "
              "ta'ita'i e Katianetona le vaega a Kisakumena—Ua fasiotia "
              "Kisakumena e le auauna a Helamana, ma ua sosola i le vao le vaega "
              "a Katianetona. E tusa o le 50–49 T.L.M.",
        "cells": [
            ("Ua avea Helamana,", "Helaman becomes"),
            ("le atalii o Helamana,", "the son of Helaman,"),
            ("ma faamasino sili—", "chief judge—"),
            ("Ua ta'ita'i e Katianetona", "Gadianton leads"),
            ("le vaega a Kisakumena—", "the band of Kishkumen—"),
            ("Ua fasiotia Kisakumena", "Kishkumen is slain"),
            ("e le auauna a Helamana,", "by Helaman's servant,"),
            ("ma ua sosola", "and flees"),
            ("i le vao", "into the wilderness"),
            ("le vaega a Katianetona.", "the Gadianton band."),
            ("E tusa o le", "about"),
            ("50–49", "50–49"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|3": {
        "en": "Many Nephites migrate to the land northward—They build houses of "
              "cement and keep many records—Tens of thousands are converted and "
              "baptized—The word of God leads men to salvation—Nephi the son of "
              "Helaman fills the judgment seat. About 49–39 B.C.",
        "sm": "Ua malaga atu le toatele o sa Nifaē i le laueleele i matu—Ua "
              "latou fausia fale sima ma tausia talafaamaumau e tele—Ua faaliliu "
              "mai ma papatisoina le sefulu o afe ma afe—O le afioga a le Atua e "
              "taitai atu ai tagata i le olataga—Ua nofo Nifae, le atalii o "
              "Helamana, i le nofoa-faamasino. E tusa o le 49–39 T.L.M.",
        "cells": [
            ("Ua malaga atu", "migrate"),
            ("le toatele o sa Nifaē", "Many Nephites"),
            ("i le laueleele i matu—", "to the land northward—"),
            ("Ua latou fausia fale sima", "They build houses of cement"),
            ("ma tausia talafaamaumau e tele—", "and keep many records—"),
            ("Ua faaliliu mai ma papatisoina", "are converted and baptized"),
            ("le sefulu o afe", "Tens of thousands"),
            ("ma afe—", "upon thousands—"),
            ("O le afioga a le Atua", "The word of God"),
            ("e taitai atu ai tagata", "leads men"),
            ("i le olataga—", "to salvation—"),
            ("Ua nofo Nifae,", "Nephi fills"),
            ("le atalii o Helamana,", "the son of Helaman,"),
            ("i le nofoa-faamasino.", "the judgment seat."),
            ("E tusa o le", "about"),
            ("49–39", "49–39"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|4": {
        "en": "Nephite dissenters and the Lamanites join forces and take the "
              "land of Zarahemla—The Nephites' defeats come because of their "
              "wickedness—The Church dwindles, and the people become weak like "
              "the Lamanites. About 38–30 B.C.",
        "sm": "Ua aufaatasi autau a tagata faatuiese o sa Nifaē ma sa Lamanā ma "
              "ua aveina le laueleele o Sara'emila—Ua oo mai toilalo ia sa Nifaē "
              "ona o lo latou amioleaga—Ua faaitiitia le ekalesia, ma ua vaivai "
              "tagata e pei o sa Lamanā. E tusa o le 38–30 T.L.M.",
        "cells": [
            ("Ua aufaatasi autau", "the armies join forces"),
            ("a tagata faatuiese", "of dissenters"),
            ("o sa Nifaē", "of the Nephites"),
            ("ma sa Lamanā", "and the Lamanites"),
            ("ma ua aveina", "and take"),
            ("le laueleele o Sara'emila—", "the land of Zarahemla—"),
            ("Ua oo mai toilalo", "defeats come"),
            ("ia sa Nifaē", "to the Nephites"),
            ("ona o lo latou amioleaga—", "because of their wickedness—"),
            ("Ua faaitiitia le ekalesia,", "The Church dwindles,"),
            ("ma ua vaivai tagata", "and the people become weak"),
            ("e pei o sa Lamanā.", "like the Lamanites."),
            ("E tusa o le", "about"),
            ("38–30", "38–30"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|5": {
        "en": "Nephi and Lehi devote themselves to preaching—Their names invite "
              "them to pattern their lives after their forebears—Christ redeems "
              "those who repent—Nephi and Lehi make many converts and are "
              "imprisoned, and fire encircles them—A cloud of darkness "
              "overshadows three hundred people—The earth shakes, and a voice "
              "commands men to repent—Nephi and Lehi converse with angels, and "
              "the multitude is encircled by fire. About 30 B.C.",
        "sm": "Ua tuu atu e Nifae ma Liae lo laua maelega i le talaiga—Ua tosina "
              "i laua e o laua igoa ia faataitai o laua olaga i o laua tamā na "
              "muamua—E togiola e Keriso i latou o ē e salamo—Ua faaliliu e "
              "Nifae ma Liae tagata e toatele ma ua faafalepuipuiina, ma ua "
              "siomia i laua i se afi—Ua ufitia tagata e tolu selau i se ao "
              "pogisa—Ua lūlūina le eleele, ma ua poloai mai se leo i tagata ia "
              "salamo—Ua fetautalatalaai Nifae ma Liae ma agelu, ma ua siomia le "
              "motu o tagata i le afi. E tusa o le 30 T.L.M.",
        "cells": [
            ("Ua tuu atu", "devote"),
            ("e Nifae ma Liae", "Nephi and Lehi"),
            ("lo laua maelega", "themselves"),
            ("i le talaiga—", "to preaching—"),
            ("Ua tosina i laua", "they are invited"),
            ("e o laua igoa", "by their names"),
            ("ia faataitai o laua olaga", "to pattern their lives"),
            ("i o laua tamā", "after their fathers"),
            ("na muamua—", "who came before—"),
            ("E togiola e Keriso i latou", "Christ redeems them"),
            ("o ē e salamo—", "who repent—"),
            ("Ua faaliliu e Nifae ma Liae", "Nephi and Lehi convert"),
            ("tagata e toatele", "many people"),
            ("ma ua faafalepuipuiina,", "and are imprisoned,"),
            ("ma ua siomia i laua", "and they are encircled"),
            ("i se afi—", "by fire—"),
            ("Ua ufitia tagata", "overshadows people"),
            ("e tolu selau", "three hundred"),
            ("i se ao pogisa—", "with a cloud of darkness—"),
            ("Ua lūlūina le eleele,", "The earth shakes,"),
            ("ma ua poloai mai se leo", "and a voice commands"),
            ("i tagata", "men"),
            ("ia salamo—", "to repent—"),
            ("Ua fetautalatalaai Nifae ma Liae", "Nephi and Lehi converse"),
            ("ma agelu,", "with angels,"),
            ("ma ua siomia le motu o tagata", "and the multitude is encircled"),
            ("i le afi.", "by fire."),
            ("E tusa o le", "about"),
            ("30", "30"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|6": {
        "en": "The righteous Lamanites preach to the wicked Nephites—Both "
              "peoples prosper during an era of peace and plenty—Lucifer, the "
              "author of sin, stirs up the hearts of the wicked and the "
              "Gadianton robbers in murder and wickedness—The robbers take over "
              "the Nephite government. About 29–23 B.C.",
        "sm": "Ua tala'i atu sa Lamanā amiotonu i sa Nifaē amioleaga—Ua manuia "
              "nuu uma e lua i se vaitaimi o le filemu ma le mau—Ua faaoso e "
              "Lusifelo, le pogai o le agasala, loto o tagata amioleaga ma le au "
              "faomea a Katianetona i le fasioti tagata ma le amioleaga—Ua pulea "
              "e le au faomea le malo o sa Nifaē. E tusa 29–23 T.L.M.",
        "cells": [
            ("Ua tala'i atu", "preach"),
            ("sa Lamanā amiotonu", "The righteous Lamanites"),
            ("i sa Nifaē amioleaga—", "to the wicked Nephites—"),
            ("Ua manuia", "prosper"),
            ("nuu uma e lua", "Both peoples"),
            ("i se vaitaimi", "during an era"),
            ("o le filemu", "of peace"),
            ("ma le mau—", "and plenty—"),
            ("Ua faaoso e Lusifelo,", "Lucifer stirs up,"),
            ("le pogai o le agasala,", "the author of sin,"),
            ("loto o tagata amioleaga", "the hearts of the wicked"),
            ("ma le au faomea", "and the robbers"),
            ("a Katianetona", "of Gadianton"),
            ("i le fasioti tagata", "in murder"),
            ("ma le amioleaga—", "and wickedness—"),
            ("Ua pulea", "take over"),
            ("e le au faomea", "The robbers"),
            ("le malo o sa Nifaē.", "the Nephite government."),
            ("E tusa", "about"),
            ("29–23", "29–23"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|8": {
        "en": "Corrupt judges seek to incite the people against "
              "Nephi—Abraham, Moses, Zenos, Zenock, Ezias, Isaiah, Jeremiah, "
              "Lehi, and Nephi all testified of Christ—By inspiration Nephi "
              "announces the murder of the chief judge. About 23–21 B.C.",
        "sm": "Ua saili faamasino amioleaga e faaoso tagata ia tetee ia "
              "Nifae—O Aperaamo, Mose, Senosa, Senoka, Esaia, Isaia, Ieremia, "
              "Liae, ma Nifae, na molimau uma ia Keriso—Ua ta'u atu e Nifae, e "
              "ala i musumusuga, le fasiotiga o le faamasino sili. E tusa o le "
              "23–21 T.L.M.",
        "cells": [
            ("Ua saili faamasino amioleaga", "Corrupt judges seek"),
            ("e faaoso tagata", "to incite the people"),
            ("ia tetee ia Nifae—", "against Nephi—"),
            ("O Aperaamo, Mose, Senosa,", "Abraham, Moses, Zenos,"),
            ("Senoka, Esaia, Isaia,", "Zenock, Ezias, Isaiah,"),
            ("Ieremia, Liae, ma Nifae,", "Jeremiah, Lehi, and Nephi,"),
            ("na molimau uma ia Keriso—", "all testified of Christ—"),
            ("Ua ta'u atu e Nifae,", "Nephi announces,"),
            ("e ala i musumusuga,", "by inspiration,"),
            ("le fasiotiga", "the murder"),
            ("o le faamasino sili.", "of the chief judge."),
            ("E tusa o le", "about"),
            ("23–21", "23–21"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|9": {
        "en": "Messengers find the chief judge dead at the judgment seat—They "
              "are imprisoned and later released—By inspiration Nephi "
              "identifies Seantum as the murderer—Nephi is accepted by some as "
              "a prophet. About 23–21 B.C.",
        "sm": "Ua maua e avefeau le faamasino sili ua maliu i le "
              "nofoa-faamasino—Ua faafalepuipuiina i latou ma toe tatala i se "
              "taimi mulimuli ane—Ua ta'u mai e Nifae, e ala i musumusuga, o "
              "Seanetuma o le fasioti tagata lena—Ua talia Nifae e ni isi, o se "
              "perofeta. E tusa o le 23–21 T.L.M.",
        "cells": [
            ("Ua maua e avefeau", "Messengers find"),
            ("le faamasino sili", "the chief judge"),
            ("ua maliu i le nofoa-faamasino—", "dead at the judgment seat—"),
            ("Ua faafalepuipuiina i latou", "They are imprisoned"),
            ("ma toe tatala", "and released"),
            ("i se taimi mulimuli ane—", "at a later time—"),
            ("Ua ta'u mai e Nifae,", "Nephi identifies,"),
            ("e ala i musumusuga,", "by inspiration,"),
            ("o Seanetuma", "Seantum"),
            ("o le fasioti tagata lena—", "as the murderer—"),
            ("Ua talia Nifae", "Nephi is accepted"),
            ("e ni isi,", "by some,"),
            ("o se perofeta.", "as a prophet."),
            ("E tusa o le", "about"),
            ("23–21", "23–21"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|10": {
        "en": "The Lord gives Nephi the sealing power—He is empowered to bind "
              "and loose on earth and in heaven—He commands the people to "
              "repent or perish—The Spirit carries him from multitude to "
              "multitude. About 21–20 B.C.",
        "sm": "Ua tuu mai e le Alii ia Nifae le mana faamau—Ua tuu mai ia te ia "
              "le mana e fusia ma tatala ai mea i le lalolagi ma le lagi—Ua ia "
              "poloai atu i tagata ia salamo pe fano—Ua aveina atu o ia e le "
              "Agaga mai lea motu o tagata i lea motu o tagata. E tusa o le "
              "21–20 T.L.M.",
        "cells": [
            ("Ua tuu mai e le Alii", "The Lord gives"),
            ("ia Nifae", "Nephi"),
            ("le mana faamau—", "the sealing power—"),
            ("Ua tuu mai ia te ia", "He is given"),
            ("le mana", "the power"),
            ("e fusia ma tatala ai", "to bind and loose"),
            ("mea", "things"),
            ("i le lalolagi", "on earth"),
            ("ma le lagi—", "and in heaven—"),
            ("Ua ia poloai atu", "He commands"),
            ("i tagata", "the people"),
            ("ia salamo pe fano—", "to repent or perish—"),
            ("Ua aveina atu o ia", "He is carried"),
            ("e le Agaga", "by the Spirit"),
            ("mai lea motu o tagata", "from multitude"),
            ("i lea motu o tagata.", "to multitude."),
            ("E tusa o le", "about"),
            ("21–20", "21–20"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|7": {
        "en": "Nephi is rejected in the north and returns to Zarahemla—He prays "
              "upon his garden tower and then calls upon the people to repent "
              "or perish. About 23–21 B.C.",
        "sm": "Ua teena Nifae i matu ma ua toe foi mai i Sara'emila—Ua tatalo o "
              "ia i luga o le 'olo i lana faatoaga ma ona ia valaau atu lea i "
              "tagata ia salamo po ua fano i latou. E tusa o le 23–21 T.L.M.",
        "cells": [
            ("Ua teena Nifae i matu", "Nephi is rejected in the north"),
            ("ma ua toe foi mai", "and returns"),
            ("i Sara'emila—", "to Zarahemla—"),
            ("Ua tatalo o ia", "He prays"),
            ("i luga o le 'olo", "upon the tower"),
            ("i lana faatoaga", "in his garden"),
            ("ma ona ia valaau atu lea", "and then he calls"),
            ("i tagata", "upon the people"),
            ("ia salamo", "to repent"),
            ("po ua fano i latou.", "or they perish."),
            ("E tusa o le", "about"),
            ("23–21", "23–21"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|11": {
        "en": "Nephi persuades the Lord to replace their war with a "
              "famine—Many people perish—They repent, and Nephi importunes the "
              "Lord for rain—Nephi and Lehi receive many revelations—The "
              "Gadianton robbers entrench themselves in the land. "
              "About 20–6 B.C.",
        "sm": "Ua faatauanau e Nifae le Alii ia suia la latou taua i se oge—E "
              "toatele tagata ua fano—Ua latou salamo, ma ua aioi atu Nifae i le "
              "Alii mo le timu—Ua maua e Nifae ma Liae faaaliga e tele—Ua "
              "faamausali e le au faomea a Katianetona i latou lava i le "
              "laueleele. E tusa o le 20–6 T.L.M.",
        "cells": [
            ("Ua faatauanau e Nifae", "Nephi persuades"),
            ("le Alii", "the Lord"),
            ("ia suia la latou taua", "to replace their war"),
            ("i se oge—", "with a famine—"),
            ("E toatele tagata ua fano—", "Many people perish—"),
            ("Ua latou salamo,", "They repent,"),
            ("ma ua aioi atu Nifae", "and Nephi importunes"),
            ("i le Alii", "the Lord"),
            ("mo le timu—", "for rain—"),
            ("Ua maua e Nifae ma Liae", "Nephi and Lehi receive"),
            ("faaaliga e tele—", "many revelations—"),
            ("Ua faamausali", "entrench"),
            ("e le au faomea", "The robbers"),
            ("a Katianetona", "of Gadianton"),
            ("i latou lava", "themselves"),
            ("i le laueleele.", "in the land."),
            ("E tusa o le", "about"),
            ("20–6", "20–6"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|12": {
        "en": "Men are unstable and foolish and quick to do evil—The Lord "
              "chastens His people—The nothingness of men is compared with the "
              "power of God—In the day of judgment, men will gain everlasting "
              "life or everlasting damnation. About 6 B.C.",
        "sm": "Ua le maumaututu tagata ma ua valelea ma televavave e fai le "
              "leaga—Ua aoai e le Alii Ona tagata—Ua faatusatusa le noa o tagata "
              "ma le mana o le Atua—O le a maua e tagata i le aso faamasino le "
              "ola tumau e faavavau po o le malaia tumau e faavavau. E tusa o le "
              "6 T.L.M.",
        "cells": [
            ("Ua le maumaututu tagata", "Men are unstable"),
            ("ma ua valelea", "and foolish"),
            ("ma televavave", "and quick"),
            ("e fai le leaga—", "to do evil—"),
            ("Ua aoai e le Alii", "The Lord chastens"),
            ("Ona tagata—", "His people—"),
            ("Ua faatusatusa", "is compared"),
            ("le noa o tagata", "the nothingness of men"),
            ("ma le mana", "with the power"),
            ("o le Atua—", "of God—"),
            ("O le a maua e tagata", "men will gain"),
            ("i le aso faamasino", "in the day of judgment"),
            ("le ola tumau e faavavau", "everlasting life"),
            ("po o le malaia tumau", "or everlasting damnation"),
            ("e faavavau.", "eternal."),
            ("E tusa o le", "about"),
            ("6", "6"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|13": {
        "en": "Samuel the Lamanite prophesies the destruction of the Nephites "
              "unless they repent—They and their riches are cursed—They reject "
              "and stone the prophets, are encircled about by demons, and seek "
              "for happiness in doing iniquity. About 6 B.C.",
        "sm": "Ua valoia e Samuelu le sa Lamanā le faaumatiaga o sa Nifaē vagana "
              "ai ua latou salamo—Ua fetuuina i latou ma a latou oa—Ua latou "
              "teena perofeta ma fetogi i latou, ua siomia i latou e temoni, ma "
              "ua latou saili le fiafia i le fai o le amioletonu. E tusa o le 6 "
              "T.L.M.",
        "cells": [
            ("Ua valoia e Samuelu", "Samuel prophesies"),
            ("le sa Lamanā", "the Lamanite"),
            ("le faaumatiaga o sa Nifaē", "the destruction of the Nephites"),
            ("vagana ai ua latou salamo—", "unless they repent—"),
            ("Ua fetuuina i latou", "They are cursed"),
            ("ma a latou oa—", "and their riches—"),
            ("Ua latou teena perofeta", "They reject the prophets"),
            ("ma fetogi i latou,", "and stone them,"),
            ("ua siomia i latou", "are encircled"),
            ("e temoni,", "by demons,"),
            ("ma ua latou saili", "and seek"),
            ("le fiafia", "happiness"),
            ("i le fai", "in doing"),
            ("o le amioletonu.", "iniquity."),
            ("E tusa o le", "about"),
            ("6", "6"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|14": {
        "en": "Samuel predicts light during the night and a new star at "
              "Christ's birth—Christ redeems men from temporal and spiritual "
              "death—The signs of His death include three days of darkness, the "
              "rending of the rocks, and great upheavals of nature. "
              "About 6 B.C.",
        "sm": "Ua valoia e Samuelu se malamalama i le po ma se fetu fou i le "
              "fanau mai o Keriso—E togiola e Keriso tagata mai le oti faaletino "
              "ma le oti faaleagaga—O faailoga o Lona maliu e aofia ai aso e tolu "
              "o le pogisa, le mavaevae o papa, ma vesiga o le natura. E tusa o "
              "le 6 T.L.M.",
        "cells": [
            ("Ua valoia e Samuelu", "Samuel predicts"),
            ("se malamalama i le po", "light during the night"),
            ("ma se fetu fou", "and a new star"),
            ("i le fanau mai", "at the birth"),
            ("o Keriso—", "of Christ—"),
            ("E togiola e Keriso tagata", "Christ redeems men"),
            ("mai le oti faaletino", "from temporal death"),
            ("ma le oti faaleagaga—", "and spiritual death—"),
            ("O faailoga o Lona maliu", "The signs of His death"),
            ("e aofia ai", "include"),
            ("aso e tolu", "three days"),
            ("o le pogisa,", "of darkness,"),
            ("le mavaevae o papa,", "the rending of the rocks,"),
            ("ma vesiga o le natura.", "and great upheavals of nature."),
            ("E tusa o le", "about"),
            ("6", "6"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|15": {
        "en": "The Lord chastened the Nephites because He loved them—Converted "
              "Lamanites are firm and steadfast in the faith—The Lord will be "
              "merciful unto the Lamanites in the latter days. About 6 B.C.",
        "sm": "Ua aoai e le Alii sa Nifaē ona o Lona alofa ia te i latou—O "
              "tagata sa Lamanā ua liua ua tutumau ma mausali i le "
              "faatuatuaga—O le a alofa mutimutivale le Alii ia sa Lamanā i aso "
              "e gata ai. E tusa o le 6 T.L.M.",
        "cells": [
            ("Ua aoai e le Alii", "The Lord chastened"),
            ("sa Nifaē", "the Nephites"),
            ("ona o Lona alofa", "because of His love"),
            ("ia te i latou—", "for them—"),
            ("O tagata sa Lamanā", "The Lamanites"),
            ("ua liua", "converted"),
            ("ua tutumau ma mausali", "are firm and steadfast"),
            ("i le faatuatuaga—", "in the faith—"),
            ("O le a alofa mutimutivale", "will be merciful"),
            ("le Alii", "The Lord"),
            ("ia sa Lamanā", "unto the Lamanites"),
            ("i aso e gata ai.", "in the latter days."),
            ("E tusa o le", "about"),
            ("6", "6"),
            ("T.L.M.", "B.C."),
        ],
    },
    "helaman|16": {
        "en": "The Nephites who believe Samuel are baptized by Nephi—Samuel "
              "cannot be slain with the arrows and stones of the unrepentant "
              "Nephites—Some harden their hearts, and others see angels—The "
              "unbelievers say it is not reasonable to believe in Christ and "
              "His coming in Jerusalem. About 6–1 B.C.",
        "sm": "Ua papatiso e Nifae tagata sa Nifaē na talitonu ia Samuelu—Ua le "
              "mafai ona fasiotia o Samuelu i ufanafana ma maa a sa Nifaē le "
              "salamo—O ni isi ua faamaaa o latou loto, a o isi ua vaai i "
              "agelu—Ua fai mai e ua le talitonu e le o se mea tonu ai i le "
              "mafaufau le talitonu ia Keriso ma Lona afio mai i Ierusalema. E "
              "tusa o le 6–1 T.L.M.",
        "cells": [
            ("Ua papatiso e Nifae", "Nephi baptizes"),
            ("tagata sa Nifaē", "the Nephites"),
            ("na talitonu ia Samuelu—", "who believe Samuel—"),
            ("Ua le mafai ona fasiotia", "cannot be slain"),
            ("o Samuelu", "Samuel"),
            ("i ufanafana ma maa", "with arrows and stones"),
            ("a sa Nifaē", "of the Nephites"),
            ("le salamo—", "unrepentant—"),
            ("O ni isi ua faamaaa", "Some harden"),
            ("o latou loto,", "their hearts,"),
            ("a o isi", "and others"),
            ("ua vaai i agelu—", "see angels—"),
            ("Ua fai mai", "say"),
            ("e ua le talitonu", "The unbelievers"),
            ("e le o se mea", "it is not a thing"),
            ("tonu ai i le mafaufau", "reasonable to the mind"),
            ("le talitonu ia Keriso", "to believe in Christ"),
            ("ma Lona afio mai", "and His coming"),
            ("i Ierusalema.", "in Jerusalem."),
            ("E tusa o le", "about"),
            ("6–1", "6–1"),
            ("T.L.M.", "B.C."),
        ],
    },
    "3nephi|1": {
        "en": "Nephi, the son of Helaman, departs out of the land, and his son "
              "Nephi keeps the records—Though signs and wonders abound, the "
              "wicked plan to slay the righteous—The night of Christ's birth "
              "arrives—The sign is given, and a new star arises—Lyings and "
              "deceivings increase, and the Gadianton robbers slaughter many. "
              "About A.D. 1–4.",
        "sm": "Ua tuua e Nifae, le atalii o Helamana, le laueleele, ma ua tausia "
              "e lona atalii o Nifae talafaamaumau—E ui ina tele faailoga ma mea "
              "ofoofogia, ua fuafua tagata amioleaga e fasioti i e ua "
              "amiotonu—Ua oo mai le po o le soifua mai o Keriso—Ua tuuina mai "
              "le faailoga, ma ua oso mai se fetu fou—Ua faateleina le pepelo ma "
              "le taufaasese, ma ua fasioti e faomea a Katianetona tagata e "
              "toatele. E tusa o le 1–4 T.A.",
        "cells": [
            ("Ua tuua e Nifae,", "Nephi departs,"),
            ("le atalii o Helamana,", "the son of Helaman,"),
            ("le laueleele,", "the land,"),
            ("ma ua tausia", "and keeps"),
            ("e lona atalii o Nifae", "his son Nephi"),
            ("talafaamaumau—", "the records—"),
            ("E ui ina tele", "Though abound"),
            ("faailoga ma mea ofoofogia,", "signs and wonders,"),
            ("ua fuafua tagata amioleaga", "the wicked plan"),
            ("e fasioti", "to slay"),
            ("i e ua amiotonu—", "the righteous—"),
            ("Ua oo mai le po", "The night arrives"),
            ("o le soifua mai", "of the birth"),
            ("o Keriso—", "of Christ—"),
            ("Ua tuuina mai le faailoga,", "The sign is given,"),
            ("ma ua oso mai", "and arises"),
            ("se fetu fou—", "a new star—"),
            ("Ua faateleina", "increase"),
            ("le pepelo ma le taufaasese,", "Lyings and deceivings,"),
            ("ma ua fasioti", "and slaughter"),
            ("e faomea a Katianetona", "the Gadianton robbers"),
            ("tagata e toatele.", "many people."),
            ("E tusa o le", "about"),
            ("1–4", "1–4"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|2": {
        "en": "Wickedness and abominations increase among the people—The "
              "Nephites and Lamanites unite to defend themselves against the "
              "Gadianton robbers—Converted Lamanites become white and are "
              "called Nephites. About A.D. 5–16.",
        "sm": "Ua faateleina le amioleaga ma mea inosia i totonu o tagata—Ua "
              "aufaatasi sa Nifaē ma sa Lamanā e puipuia i latou lava e faasaga "
              "i le au faomea a Katianetona—O sa Lamanā na liliu mai ua papa'e "
              "ma ua ta'ua o sa Nifaē. E tusa o le 5–16 T.A.",
        "cells": [
            ("Ua faateleina", "increase"),
            ("le amioleaga ma mea inosia", "Wickedness and abominations"),
            ("i totonu o tagata—", "among the people—"),
            ("Ua aufaatasi", "unite"),
            ("sa Nifaē ma sa Lamanā", "The Nephites and Lamanites"),
            ("e puipuia i latou lava", "to defend themselves"),
            ("e faasaga", "against"),
            ("i le au faomea", "the robbers"),
            ("a Katianetona—", "of Gadianton—"),
            ("O sa Lamanā", "The Lamanites"),
            ("na liliu mai", "who converted"),
            ("ua papa'e", "become white"),
            ("ma ua ta'ua", "and are called"),
            ("o sa Nifaē.", "Nephites."),
            ("E tusa o le", "about"),
            ("5–16", "5–16"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|3": {
        "en": "Giddianhi, the Gadianton leader, demands that Lachoneus and the "
              "Nephites surrender themselves and their lands—Lachoneus appoints "
              "Gidgiddoni as chief captain of the armies—The Nephites assemble "
              "in Zarahemla and Bountiful to defend themselves. "
              "About A.D. 16–18.",
        "sm": "Ua faatonu mai Kitianae, le taitai o le au faomea a Katianetona, "
              "ia Lakoneu ma tagata sa Nifaē ia latou siilima ma tuu atu o latou "
              "laueleele ia te i latou—Ua tofia Kitekitonae e Lakoneu e avea ma "
              "kapeteni sili o autau—Ua faapotopoto fatasi tagata sa Nifaē i "
              "Sara'emila ma Nuumau e puipuia i latou lava. E tusa o le 16–18 "
              "T.A.",
        "cells": [
            ("Ua faatonu mai Kitianae,", "Giddianhi demands,"),
            ("le taitai", "the leader"),
            ("o le au faomea", "of the robbers"),
            ("a Katianetona,", "of Gadianton,"),
            ("ia Lakoneu", "that Lachoneus"),
            ("ma tagata sa Nifaē", "and the Nephites"),
            ("ia latou siilima", "surrender"),
            ("ma tuu atu", "and give up"),
            ("o latou laueleele", "their lands"),
            ("ia te i latou—", "to them—"),
            ("Ua tofia Kitekitonae e Lakoneu", "Lachoneus appoints Gidgiddoni"),
            ("e avea ma kapeteni sili", "as chief captain"),
            ("o autau—", "of the armies—"),
            ("Ua faapotopoto fatasi", "assemble together"),
            ("tagata sa Nifaē", "The Nephites"),
            ("i Sara'emila ma Nuumau", "in Zarahemla and Bountiful"),
            ("e puipuia i latou lava.", "to defend themselves."),
            ("E tusa o le", "about"),
            ("16–18", "16–18"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|4": {
        "en": "The Nephite armies defeat the Gadianton robbers—Giddianhi is "
              "slain, and his successor, Zemnarihah, is hanged—The Nephites "
              "praise the Lord for their victories. About A.D. 19–22.",
        "sm": "Ua faatoilalo e autau a sa Nifaē le au faomea a Katianetona—Ua "
              "fasiotia Kitianae, ma lona sui, o Seminaraea, ua sisi—Ua viia e "
              "sa Nifaē le Alii mo lo latou manumalo. E tusa o le 19–22 T.A.",
        "cells": [
            ("Ua faatoilalo", "defeat"),
            ("e autau a sa Nifaē", "The Nephite armies"),
            ("le au faomea a Katianetona—", "the Gadianton robbers—"),
            ("Ua fasiotia Kitianae,", "Giddianhi is slain,"),
            ("ma lona sui, o Seminaraea,", "and his successor, Zemnarihah,"),
            ("ua sisi—", "is hanged—"),
            ("Ua viia e sa Nifaē", "The Nephites praise"),
            ("le Alii", "the Lord"),
            ("mo lo latou manumalo.", "for their victories."),
            ("E tusa o le", "about"),
            ("19–22", "19–22"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|5": {
        "en": "The Nephites repent and forsake their sins—Mormon writes the "
              "history of his people and declares the everlasting word to "
              "them—Israel will be gathered in from her long dispersion. "
              "About A.D. 22–26.",
        "sm": "Ua salamo sa Nifaē ma ua lafoai a latou agasala—Ua tusi e Mamona "
              "le talafaasolopito o ona tagata ma ia tala'i atu le afioga tumau "
              "e faavavau ia te i latou—O le a faapotopotoina Isaraelu mai lona "
              "faataapeapeina umi. E tusa o le 22–26 T.A.",
        "cells": [
            ("Ua salamo sa Nifaē", "The Nephites repent"),
            ("ma ua lafoai", "and forsake"),
            ("a latou agasala—", "their sins—"),
            ("Ua tusi e Mamona", "Mormon writes"),
            ("le talafaasolopito", "the history"),
            ("o ona tagata", "of his people"),
            ("ma ia tala'i atu", "and declares"),
            ("le afioga tumau e faavavau", "the everlasting word"),
            ("ia te i latou—", "to them—"),
            ("O le a faapotopotoina Isaraelu", "Israel will be gathered in"),
            ("mai lona faataapeapeina umi.", "from her long dispersion."),
            ("E tusa o le", "about"),
            ("22–26", "22–26"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|6": {
        "en": "The Nephites prosper—Pride, wealth, and class distinctions "
              "arise—The Church is rent with dissensions—Satan leads the people "
              "in open rebellion—Many prophets cry repentance and are "
              "slain—Their murderers conspire to take over the government. "
              "About A.D. 26–30.",
        "sm": "Ua manuia sa Nifaē—Ua tupu a'e le faamaualuga, le mauoa, ma le "
              "faailoga tagana—Ua vaevaeina le Ekalesia ona o fefinauaiga—Ua "
              "taitai e Satani tagata i fouvalega e lē faalilolilo—E toatele "
              "perofeta ua latou alalaga atu le salamo ma ua fasiotia—Ua "
              "taupulepule e na fasiotia i latou e pulea faamalosi le malo. E "
              "tusa o le 26–30 T.A.",
        "cells": [
            ("Ua manuia sa Nifaē—", "The Nephites prosper—"),
            ("Ua tupu a'e le faamaualuga,", "Pride arises,"),
            ("le mauoa,", "wealth,"),
            ("ma le faailoga tagana—", "and class distinctions—"),
            ("Ua vaevaeina le Ekalesia", "The Church is rent"),
            ("ona o fefinauaiga—", "with dissensions—"),
            ("Ua taitai e Satani tagata", "Satan leads the people"),
            ("i fouvalega e lē faalilolilo—", "in open rebellion—"),
            ("E toatele perofeta", "Many prophets"),
            ("ua latou alalaga atu", "cry"),
            ("le salamo", "repentance"),
            ("ma ua fasiotia—", "and are slain—"),
            ("Ua taupulepule", "conspire"),
            ("e na fasiotia i latou", "those who slew them"),
            ("e pulea faamalosi le malo.", "to take over the government."),
            ("E tusa o le", "about"),
            ("26–30", "26–30"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|7": {
        "en": "The chief judge is murdered, the government is destroyed, and "
              "the people divide into tribes—Jacob, an anti-Christ, becomes "
              "king of a secret combination—Nephi preaches repentance and faith "
              "in Christ—Angels minister to him daily, and he raises his "
              "brother from the dead—Many repent and are baptized. "
              "About A.D. 30–33.",
        "sm": "Ua fasiotia le faamasino sili, ua lepetia le malo, ma ua vaevae "
              "tagata i ituaiga—Ua avea Iakopo, le aneti-Keriso, ma tupu o se "
              "faapotopotoga faalilolilo—Ua tala'i atu e Nifae le salamo ma le "
              "faatuatua ia Keriso—Ua auauna mai agelu ia te ia i aso taitasi, "
              "ma ia faatulai mai lona uso mai le oti—E toatele ua salamo ma "
              "papatisoina. E tusa o le 30–33 T.A.",
        "cells": [
            ("Ua fasiotia le faamasino sili,", "The chief judge is murdered,"),
            ("ua lepetia le malo,", "the government is destroyed,"),
            ("ma ua vaevae tagata", "and the people divide"),
            ("i ituaiga—", "into tribes—"),
            ("Ua avea Iakopo,", "Jacob becomes"),
            ("le aneti-Keriso,", "an anti-Christ,"),
            ("ma tupu", "king"),
            ("o se faapotopotoga faalilolilo—", "of a secret combination—"),
            ("Ua tala'i atu e Nifae", "Nephi preaches"),
            ("le salamo", "repentance"),
            ("ma le faatuatua ia Keriso—", "and faith in Christ—"),
            ("Ua auauna mai agelu", "Angels minister"),
            ("ia te ia", "to him"),
            ("i aso taitasi,", "daily,"),
            ("ma ia faatulai mai lona uso", "and he raises his brother"),
            ("mai le oti—", "from the dead—"),
            ("E toatele ua salamo", "Many repent"),
            ("ma papatisoina.", "and are baptized."),
            ("E tusa o le", "about"),
            ("30–33", "30–33"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|8": {
        "en": "Tempests, earthquakes, fires, whirlwinds, and physical upheavals "
              "attest the crucifixion of Christ—Many people are "
              "destroyed—Darkness covers the land for three days—Those who "
              "remain bemoan their fate. About A.D. 33–34.",
        "sm": "Ua faamaonia e afā, mafuie, afi, asiosio, ma isi mala faalenatura "
              "le faasatauroga o Keriso—E toatele tagata na faaumatia—Ua ufitia "
              "le laueleele i le pogisa mo aso e tolu—O i latou o e na totoe ua "
              "laue i le mea ua oo mai ia te i latou. E tusa o le 33–34 T.A.",
        "cells": [
            ("Ua faamaonia", "attest"),
            ("e afā, mafuie, afi, asiosio,", "tempests, earthquakes, fires, whirlwinds,"),
            ("ma isi mala faalenatura", "and physical upheavals"),
            ("le faasatauroga o Keriso—", "the crucifixion of Christ—"),
            ("E toatele tagata na faaumatia—", "Many people are destroyed—"),
            ("Ua ufitia le laueleele", "covers the land"),
            ("i le pogisa", "with darkness"),
            ("mo aso e tolu—", "for three days—"),
            ("O i latou o e", "Those who"),
            ("na totoe", "remain"),
            ("ua laue", "bemoan"),
            ("i le mea ua oo mai", "what has come"),
            ("ia te i latou.", "upon them."),
            ("E tusa o le", "about"),
            ("33–34", "33–34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|9": {
        "en": "In the darkness, the voice of Christ proclaims the destruction "
              "of many people and cities for their wickedness—He also proclaims "
              "His divinity, announces that the law of Moses is fulfilled, and "
              "invites men to come unto Him and be saved. About A.D. 34.",
        "sm": "I le pogisa, ua tautino mai ai e le siufofoga o Keriso le "
              "faafanoga o le toatele o tagata ma aai ona o lo latou "
              "amioleaga—Ua Ia tautino mai foi Lona paia, ma fetalai mai ua "
              "faataunuuina le tulafono a Mose, ma valaaulia tagata ia o mai ia "
              "te Ia ma faaolaina. E tusa o le 34 T.A.",
        "cells": [
            ("I le pogisa,", "In the darkness,"),
            ("ua tautino mai ai", "proclaims"),
            ("e le siufofoga o Keriso", "the voice of Christ"),
            ("le faafanoga", "the destruction"),
            ("o le toatele o tagata", "of many people"),
            ("ma aai", "and cities"),
            ("ona o lo latou amioleaga—", "for their wickedness—"),
            ("Ua Ia tautino mai foi", "He also proclaims"),
            ("Lona paia,", "His divinity,"),
            ("ma fetalai mai", "announces"),
            ("ua faataunuuina", "is fulfilled"),
            ("le tulafono a Mose,", "the law of Moses,"),
            ("ma valaaulia tagata", "and invites men"),
            ("ia o mai", "to come"),
            ("ia te Ia", "unto Him"),
            ("ma faaolaina.", "and be saved."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|10": {
        "en": "There is silence in the land for many hours—The voice of Christ "
              "promises to gather His people as a hen gathers her chickens—The "
              "more righteous part of the people have been preserved. "
              "About A.D. 34–35.",
        "sm": "Ua taaligoligoa le laueleele mo itula e tele—Ua folafola mai e le "
              "siufofoga o Keriso le faapotopotoina o Ona tagata e pei ona "
              "ofaofatai mai e se matuamoa lana toloai—Ua faasaoina le vaega o "
              "tagata sa sili atu ona amiotonu. E tusa o le 34–35 T.A.",
        "cells": [
            ("Ua taaligoligoa le laueleele", "There is silence in the land"),
            ("mo itula e tele—", "for many hours—"),
            ("Ua folafola mai", "promises"),
            ("e le siufofoga o Keriso", "The voice of Christ"),
            ("le faapotopotoina o Ona tagata", "to gather His people"),
            ("e pei ona ofaofatai mai", "as gathers"),
            ("e se matuamoa lana toloai—", "a hen her chickens—"),
            ("Ua faasaoina", "have been preserved"),
            ("le vaega o tagata", "the part of the people"),
            ("sa sili atu ona amiotonu.", "the more righteous."),
            ("E tusa o le", "about"),
            ("34–35", "34–35"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|11": {
        "en": "The Father testifies of His Beloved Son—Christ appears and "
              "proclaims His Atonement—The people feel the wound marks in His "
              "hands and feet and side—They cry Hosanna—He sets forth the mode "
              "and manner of baptism—The spirit of contention is of the "
              "devil—Christ's doctrine is that men should believe and be "
              "baptized and receive the Holy Ghost. About A.D. 34.",
        "sm": "Ua molimau le Tamā i Lona Alo Pele—Ua afio mai Keriso ma tautino "
              "mai Lana Togiola—Ua pai atu tagata i manua i Ona lima, ma vae, ma "
              "lona itu—Ua latou alalaga, Osana—Ua ia faatuina le ala ma le "
              "faiga o le papatisoga—O le agaga o le finau e mai le tiapolo—O le "
              "mataupu a Keriso o le tatau lea i tagata ona salamo ma papatiso "
              "ma talia le Agaga Paia. E tusa o le 34 T.A.",
        "cells": [
            ("Ua molimau le Tamā", "The Father testifies"),
            ("i Lona Alo Pele—", "of His Beloved Son—"),
            ("Ua afio mai Keriso", "Christ appears"),
            ("ma tautino mai Lana Togiola—", "and proclaims His Atonement—"),
            ("Ua pai atu tagata", "The people feel"),
            ("i manua", "the wounds"),
            ("i Ona lima,", "in His hands,"),
            ("ma vae, ma lona itu—", "and feet, and side—"),
            ("Ua latou alalaga, Osana—", "They cry, Hosanna—"),
            ("Ua ia faatuina", "He sets forth"),
            ("le ala ma le faiga", "the mode and manner"),
            ("o le papatisoga—", "of baptism—"),
            ("O le agaga o le finau", "The spirit of contention"),
            ("e mai le tiapolo—", "is of the devil—"),
            ("O le mataupu a Keriso", "Christ's doctrine"),
            ("o le tatau lea", "is that should"),
            ("i tagata", "men"),
            ("ona salamo ma papatiso", "repent and be baptized"),
            ("ma talia le Agaga Paia.", "and receive the Holy Ghost."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|12": {
        "en": "Jesus calls and commissions the twelve disciples—He delivers to "
              "the Nephites a discourse similar to the Sermon on the Mount—He "
              "speaks the Beatitudes—His teachings transcend and take "
              "precedence over the law of Moses—Men are commanded to be perfect "
              "even as He and His Father are perfect—Compare Matthew 5. "
              "About A.D. 34.",
        "sm": "Ua valaauina ma tofia e Iesu soo e toasefululua—Ua ia tuuina atu "
              "i tagata sa Nifaē se lauga e pei o le Lauga i le Mauga—Ua Ia "
              "fofogaina Faaamuia—Ua sili ma taua atu ana aoaoga nai lo le "
              "tulafono a Mose—Ua poloaiina tagata ia atoatoa i latou e pei ona "
              "atoatoa o Ia ma Lona Tamā—Faatusatusa i le Mataio 5. E tusa o le "
              "34 T.A.",
        "cells": [
            ("Ua valaauina ma tofia", "calls and commissions"),
            ("e Iesu", "Jesus"),
            ("soo e toasefululua—", "the twelve disciples—"),
            ("Ua ia tuuina atu", "He delivers"),
            ("i tagata sa Nifaē", "to the Nephites"),
            ("se lauga", "a discourse"),
            ("e pei o", "similar to"),
            ("le Lauga i le Mauga—", "the Sermon on the Mount—"),
            ("Ua Ia fofogaina Faaamuia—", "He speaks the Beatitudes—"),
            ("Ua sili ma taua atu", "transcend and take precedence"),
            ("ana aoaoga", "His teachings"),
            ("nai lo", "over"),
            ("le tulafono a Mose—", "the law of Moses—"),
            ("Ua poloaiina tagata", "Men are commanded"),
            ("ia atoatoa i latou", "to be perfect"),
            ("e pei ona atoatoa", "even as perfect"),
            ("o Ia ma Lona Tamā—", "are He and His Father—"),
            ("Faatusatusa", "Compare"),
            ("i le Mataio 5.", "Matthew 5."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|13": {
        "en": "Jesus teaches the Nephites the Lord's Prayer—They are to lay up "
              "treasures in heaven—The twelve disciples in their ministry are "
              "commanded to take no thought for temporal things—Compare "
              "Matthew 6. About A.D. 34.",
        "sm": "Ua aoao mai e Iesu le Tatalo a le Alii i tagata sa Nifaē—E tatau "
              "ona latou teuina oa i le lagi—Ua poloaiina soo e toasefululua e "
              "aua nei mafaufau i mea faaletino i la latou auaunaga "
              "faaleagaga—Faatusatusa i le Mataio 6. E tusa o le 34 T.A.",
        "cells": [
            ("Ua aoao mai e Iesu", "Jesus teaches"),
            ("le Tatalo a le Alii", "the Lord's Prayer"),
            ("i tagata sa Nifaē—", "the Nephites—"),
            ("E tatau ona latou teuina", "They are to lay up"),
            ("oa", "treasures"),
            ("i le lagi—", "in heaven—"),
            ("Ua poloaiina soo e toasefululua", "The twelve disciples are commanded"),
            ("e aua nei mafaufau", "to take no thought"),
            ("i mea faaletino", "for temporal things"),
            ("i la latou auaunaga faaleagaga—", "in their spiritual ministry—"),
            ("Faatusatusa", "Compare"),
            ("i le Mataio 6.", "Matthew 6."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|14": {
        "en": "Jesus commands: Judge not; ask of God; beware of false "
              "prophets—He promises salvation to those who do the will of the "
              "Father—Compare Matthew 7. About A.D. 34.",
        "sm": "Ua poloai mai Iesu: Aua le faamasino atu; ole atu i le Atua; ia "
              "faaeteete i perofeta pepelo—Ua ia folafola mai le faaolataga i ē "
              "e faia le finagalo o le Tamā—Ia faatusatusa i le Mataio 7. E tusa "
              "o le 34 T.A.",
        "cells": [
            ("Ua poloai mai Iesu:", "Jesus commands:"),
            ("Aua le faamasino atu;", "Judge not;"),
            ("ole atu i le Atua;", "ask of God;"),
            ("ia faaeteete i perofeta pepelo—", "beware of false prophets—"),
            ("Ua ia folafola mai", "He promises"),
            ("le faaolataga", "salvation"),
            ("i ē e faia", "to those who do"),
            ("le finagalo o le Tamā—", "the will of the Father—"),
            ("Ia faatusatusa", "Compare"),
            ("i le Mataio 7.", "Matthew 7."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|15": {
        "en": "Jesus announces that the law of Moses is fulfilled in Him—The "
              "Nephites are the other sheep of whom He spoke in "
              "Jerusalem—Because of iniquity, the Lord's people in Jerusalem do "
              "not know of the scattered sheep of Israel. About A.D. 34.",
        "sm": "Ua faailoa mai e Iesu ua faataunuuina ia te Ia le tulafono a "
              "Mose—O tagata sa Nifaē o isi mamoe ia na Ia fetalai atu ai i "
              "Ierusalema—Ona o le amioletonu, ua le iloa ai e tagata o le Alii "
              "i Ierusalema e uiga i mamoe o Isaraelu ua faasalalauina. E tusa o "
              "le 34 T.A.",
        "cells": [
            ("Ua faailoa mai e Iesu", "Jesus announces"),
            ("ua faataunuuina ia te Ia", "is fulfilled in Him"),
            ("le tulafono a Mose—", "the law of Moses—"),
            ("O tagata sa Nifaē", "The Nephites"),
            ("o isi mamoe", "are the other sheep"),
            ("ia na Ia fetalai atu ai", "of whom He spoke"),
            ("i Ierusalema—", "in Jerusalem—"),
            ("Ona o le amioletonu,", "Because of iniquity,"),
            ("ua le iloa ai", "do not know"),
            ("e tagata o le Alii", "the Lord's people"),
            ("i Ierusalema", "in Jerusalem"),
            ("e uiga i mamoe o Isaraelu", "of the sheep of Israel"),
            ("ua faasalalauina.", "who are scattered."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|16": {
        "en": "Jesus will visit others of the lost sheep of Israel—In the "
              "latter days the gospel will go to the Gentiles and then to the "
              "house of Israel—The Lord's people will see eye to eye when He "
              "brings again Zion. About A.D. 34.",
        "sm": "O le a asiasi atu Iesu i isi mamoe o le aiga o Isaraelu ua "
              "leiloloa—I aso e gata ai o le a alu atu le talalelei i Nuuese ona "
              "oo atu ai lea i le aiga o Isaraelu—O le nuu o le Alii o le a vaai "
              "i latou lava pe a Ia toe aumai Siona. E tusa o le 34 T.A.",
        "cells": [
            ("O le a asiasi atu Iesu", "Jesus will visit"),
            ("i isi mamoe", "others of the sheep"),
            ("o le aiga o Isaraelu", "of the house of Israel"),
            ("ua leiloloa—", "who are lost—"),
            ("I aso e gata ai", "In the latter days"),
            ("o le a alu atu le talalelei", "the gospel will go"),
            ("i Nuuese", "to the Gentiles"),
            ("ona oo atu ai lea", "and then"),
            ("i le aiga o Isaraelu—", "to the house of Israel—"),
            ("O le nuu o le Alii", "The Lord's people"),
            ("o le a vaai", "will see"),
            ("i latou lava", "eye to eye"),
            ("pe a Ia toe aumai", "when He brings again"),
            ("Siona.", "Zion."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|17": {
        "en": "Jesus directs the people to ponder His words and pray for "
              "understanding—He heals their sick—He prays for the people, using "
              "language that cannot be written—Angels minister to and fire "
              "encircles their little ones. About A.D. 34.",
        "sm": "Ua poloai Iesu i tagata ia mafaufau i Ana upu ma tatalo mo le "
              "malamalama—Ua ia faamaloloina ē ua mamai—Ua tatalo o ia mo "
              "tagata, ua faaaoga ai le gagana e le mafai ona tusia—Ua auauna "
              "mai agelu ma ua siosiomia o latou tamaiti laiti i le afi. E tusa "
              "o le 34 T.A.",
        "cells": [
            ("Ua poloai Iesu i tagata", "Jesus directs the people"),
            ("ia mafaufau i Ana upu", "to ponder His words"),
            ("ma tatalo mo le malamalama—", "and pray for understanding—"),
            ("Ua ia faamaloloina", "He heals"),
            ("ē ua mamai—", "the sick—"),
            ("Ua tatalo o ia", "He prays"),
            ("mo tagata,", "for the people,"),
            ("ua faaaoga ai le gagana", "using language"),
            ("e le mafai ona tusia—", "that cannot be written—"),
            ("Ua auauna mai agelu", "Angels minister"),
            ("ma ua siosiomia", "and encircles"),
            ("o latou tamaiti laiti", "their little ones"),
            ("i le afi.", "with fire."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|18": {
        "en": "Jesus institutes the sacrament among the Nephites—They are "
              "commanded to pray always in His name—Those who eat His flesh and "
              "drink His blood unworthily are damned—The disciples are given "
              "power to confer the Holy Ghost. About A.D. 34.",
        "sm": "Ua faatuina e Iesu le faamanatuga i totonu o tagata sa Nifaē—Ua "
              "poloaiina i latou ia tatalo e le aunoa i Lona suafa—Ua tausalaina "
              "i latou o e e aai i Lona tino ma feinu i Lona toto ma le "
              "faaletatau—Ua tuuina mai le mana i soo e faaee atu ai le Agaga "
              "Paia. E tusa o le 34 T.A.",
        "cells": [
            ("Ua faatuina e Iesu", "Jesus institutes"),
            ("le faamanatuga", "the sacrament"),
            ("i totonu o", "among"),
            ("tagata sa Nifaē—", "the Nephites—"),
            ("Ua poloaiina i latou", "They are commanded"),
            ("ia tatalo e le aunoa", "to pray always"),
            ("i Lona suafa—", "in His name—"),
            ("Ua tausalaina i latou", "damned are those"),
            ("o e e aai", "who eat"),
            ("i Lona tino", "His flesh"),
            ("ma feinu i Lona toto", "and drink His blood"),
            ("ma le faaletatau—", "unworthily—"),
            ("Ua tuuina mai le mana", "power is given"),
            ("i soo", "to the disciples"),
            ("e faaee atu ai", "to confer"),
            ("le Agaga Paia.", "the Holy Ghost."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|20": {
        "en": "Jesus provides bread and wine miraculously and again administers "
              "the sacrament unto the people—The remnant of Jacob will come to "
              "the knowledge of the Lord their God and will inherit the "
              "Americas—Jesus is the prophet like unto Moses, and the Nephites "
              "are children of the prophets—Others of the Lord's people will be "
              "gathered to Jerusalem. About A.D. 34.",
        "sm": "Ua saunia e Iesu le areto ma le uaina i se ala faavavega ma ua "
              "toe faamanuia ma tufatufa atu le faamanatuga i tagata—O le a "
              "aumai le vaega o totoe o Iakopo i le malamalama o le Alii lo "
              "latou Atua, ma o le a fai mo o latou tofi le laueleele o "
              "Amerika—O Iesu o le perofeta e pei o Mose, ma o tagata sa Nifaē o "
              "fanau a perofeta—O isi o tagata o le Alii o le a faapotopotoina i "
              "Ierusalema. E tusa o le 34 T.A.",
        "cells": [
            ("Ua saunia e Iesu", "Jesus provides"),
            ("le areto ma le uaina", "bread and wine"),
            ("i se ala faavavega", "miraculously"),
            ("ma ua toe faamanuia", "and again blesses"),
            ("ma tufatufa atu le faamanatuga", "and administers the sacrament"),
            ("i tagata—", "unto the people—"),
            ("O le a aumai", "will come"),
            ("le vaega o totoe o Iakopo", "the remnant of Jacob"),
            ("i le malamalama", "to the knowledge"),
            ("o le Alii", "of the Lord"),
            ("lo latou Atua,", "their God,"),
            ("ma o le a fai", "and will be made"),
            ("mo o latou tofi", "their inheritance"),
            ("le laueleele o Amerika—", "the land of America—"),
            ("O Iesu o le perofeta", "Jesus is the prophet"),
            ("e pei o Mose,", "like unto Moses,"),
            ("ma o tagata sa Nifaē", "and the Nephites"),
            ("o fanau a perofeta—", "are children of the prophets—"),
            ("O isi o tagata", "Others of the people"),
            ("o le Alii", "of the Lord"),
            ("o le a faapotopotoina", "will be gathered"),
            ("i Ierusalema.", "to Jerusalem."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|19": {
        "en": "The twelve disciples minister unto the people and pray for the "
              "Holy Ghost—The disciples are baptized and receive the Holy Ghost "
              "and the ministering of angels—Jesus prays using words that "
              "cannot be written—He attests to the exceedingly great faith of "
              "these Nephites. About A.D. 34.",
        "sm": "Ua auauna atu le au soo e toasefululua i tagata ma ua tatalo atu "
              "mo le Agaga Paia—Ua papatisoina le au soo ma ua latou maua le "
              "Agaga Paia ma le auaunaga a agelu—Ua tatalo Iesu ma ia "
              "faaaogaina upu e le mafai ona tusia—Ua molimau mai o ia i le "
              "faatuatua tele naua o nei tagata sa Nifaē. E tusa o le 34 T.A.",
        "cells": [
            ("Ua auauna atu", "minister"),
            ("le au soo e toasefululua", "The twelve disciples"),
            ("i tagata", "unto the people"),
            ("ma ua tatalo atu", "and pray"),
            ("mo le Agaga Paia—", "for the Holy Ghost—"),
            ("Ua papatisoina le au soo", "The disciples are baptized"),
            ("ma ua latou maua", "and receive"),
            ("le Agaga Paia", "the Holy Ghost"),
            ("ma le auaunaga a agelu—", "and the ministering of angels—"),
            ("Ua tatalo Iesu", "Jesus prays"),
            ("ma ia faaaogaina upu", "using words"),
            ("e le mafai ona tusia—", "that cannot be written—"),
            ("Ua molimau mai o ia", "He attests"),
            ("i le faatuatua tele naua", "to the exceedingly great faith"),
            ("o nei tagata sa Nifaē.", "of these Nephites."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|21": {
        "en": "Israel will be gathered when the Book of Mormon comes forth—The "
              "Gentiles will be established as a free people in America—They "
              "will be saved if they believe and obey; otherwise, they will be "
              "cut off and destroyed—Israel will build the New Jerusalem, and "
              "the lost tribes will return. About A.D. 34.",
        "sm": "O le a faapotopotoina Isaraelu pe a oo mai le Tusi a Mamona—O le "
              "a faatuina Nuuese i Amerika o ni tagata saoloto—O le a faaolaina "
              "i latou pe a fai latou te talitonu ma usiusitai; a leai, o le a "
              "vavaeeseina i latou ma faaumatia—O le a faatuina e Isaraelu le "
              "Ierusalema Fou, ma o le a toe foi mai ituaiga ua leiloloa. E tusa "
              "o le 34 T.A.",
        "cells": [
            ("O le a faapotopotoina Isaraelu", "Israel will be gathered"),
            ("pe a oo mai", "when comes forth"),
            ("le Tusi a Mamona—", "the Book of Mormon—"),
            ("O le a faatuina Nuuese", "The Gentiles will be established"),
            ("i Amerika", "in America"),
            ("o ni tagata saoloto—", "as a free people—"),
            ("O le a faaolaina", "will be saved"),
            ("i latou", "they"),
            ("pe a fai", "if"),
            ("latou te talitonu ma usiusitai;", "they believe and obey;"),
            ("a leai,", "otherwise,"),
            ("o le a vavaeeseina i latou", "they will be cut off"),
            ("ma faaumatia—", "and destroyed—"),
            ("O le a faatuina", "will build"),
            ("e Isaraelu", "Israel"),
            ("le Ierusalema Fou,", "the New Jerusalem,"),
            ("ma o le a toe foi mai", "and will return"),
            ("ituaiga ua leiloloa.", "the lost tribes."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|22": {
        "en": "In the last days, Zion and her stakes will be established, and "
              "Israel will be gathered in mercy and tenderness—They will "
              "triumph—Compare Isaiah 54. About A.D. 34.",
        "sm": "I aso e gata ai, o le a faatuina Siona ma ona siteki, ma o le a "
              "faapotopotoina Isaraelu i le alofa mutimutivale ma le agamalu—O "
              "le a latou manumalo—Faatusatusa i le Isaia 54. E tusa o le 34 "
              "T.A.",
        "cells": [
            ("I aso e gata ai,", "In the last days,"),
            ("o le a faatuina Siona", "Zion will be established"),
            ("ma ona siteki,", "and her stakes,"),
            ("ma o le a faapotopotoina", "and will be gathered"),
            ("Isaraelu", "Israel"),
            ("i le alofa mutimutivale", "in mercy"),
            ("ma le agamalu—", "and tenderness—"),
            ("O le a latou manumalo—", "They will triumph—"),
            ("Faatusatusa", "Compare"),
            ("i le Isaia 54.", "Isaiah 54."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|23": {
        "en": "Jesus approves the words of Isaiah—He commands the people to "
              "search the prophets—The words of Samuel the Lamanite concerning "
              "the Resurrection are added to their records. About A.D. 34.",
        "sm": "Ua faamaonia e Iesu upu a Isaia—Ua ia poloaiina tagata ia suesue "
              "i perofeta—Ua faaopoopo ia latou talafaamaumau upu a Samuelu le "
              "sa Lamanā e uiga i le Toetutu. E tusa o le 34 T.A.",
        "cells": [
            ("Ua faamaonia e Iesu", "Jesus approves"),
            ("upu a Isaia—", "the words of Isaiah—"),
            ("Ua ia poloaiina tagata", "He commands the people"),
            ("ia suesue i perofeta—", "to search the prophets—"),
            ("Ua faaopoopo ia latou talafaamaumau", "are added to their records"),
            ("upu a Samuelu", "the words of Samuel"),
            ("le sa Lamanā", "the Lamanite"),
            ("e uiga i le Toetutu.", "concerning the Resurrection."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|24": {
        "en": "The Lord's messenger will prepare the way for the Second "
              "Coming—Christ will sit in judgment—Israel is commanded to pay "
              "tithes and offerings—A book of remembrance is kept—Compare "
              "Malachi 3. About A.D. 34.",
        "sm": "O le a saunia e le avefeau a le Alii le ala mo le Afio Mai "
              "Faalua—O le a afio Keriso e faamasino—Ua poloaiina Isaraelu ia "
              "totogi sefuluai ma taulaga—Ua tausia se tusi faamanatu—Faatusatusa "
              "i le Malaki 3.",
        "cells": [
            ("O le a saunia", "will prepare"),
            ("e le avefeau a le Alii", "the Lord's messenger"),
            ("le ala", "the way"),
            ("mo le Afio Mai Faalua—", "for the Second Coming—"),
            ("O le a afio Keriso", "Christ will come"),
            ("e faamasino—", "to judge—"),
            ("Ua poloaiina Isaraelu", "Israel is commanded"),
            ("ia totogi sefuluai", "to pay tithes"),
            ("ma taulaga—", "and offerings—"),
            ("Ua tausia se tusi faamanatu—", "A book of remembrance is kept—"),
            ("Faatusatusa", "Compare"),
            ("i le Malaki 3.", "Malachi 3."),
        ],
    },
    "3nephi|25": {
        "en": "At the Second Coming, the proud and wicked will be burned as "
              "stubble—Elijah will return before that great and dreadful "
              "day—Compare Malachi 4. About A.D. 34.",
        "sm": "O le a susunuina i le Afio Mai Faalua e pei o tagutugutu o saito "
              "ē e faamaualuluga ma ē e amioleaga—O le a toe foi mai Elia ae lei "
              "oo i lena aso tele ma le matautia—Faatusatusa i le Malaki 4. E "
              "tusa o le 34 T.A.",
        "cells": [
            ("O le a susunuina", "will be burned"),
            ("i le Afio Mai Faalua", "at the Second Coming"),
            ("e pei o", "as"),
            ("tagutugutu o saito", "stubble"),
            ("ē e faamaualuluga", "the proud"),
            ("ma ē e amioleaga—", "and the wicked—"),
            ("O le a toe foi mai", "will return"),
            ("Elia", "Elijah"),
            ("ae lei oo", "before comes"),
            ("i lena aso tele", "that great day"),
            ("ma le matautia—", "and dreadful—"),
            ("Faatusatusa", "Compare"),
            ("i le Malaki 4.", "Malachi 4."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|26": {
        "en": "Jesus expounds all things from the beginning to the end—Babes "
              "and children utter marvelous things that cannot be written—Those "
              "in the Church of Christ have all things in common among them. "
              "About A.D. 34.",
        "sm": "Ua auiliili atoatoa mai e Iesu mea uma mai le amataga e oo i le "
              "iuga—Ua tautala mai pepe ma tamaiti i mea ofoofogia e le mafai "
              "ona tusia—O i latou e i ai i totonu o le Ekalesia a Keriso ua "
              "taatele mea uma i totonu ia te i latou. E tusa o le 34 T.A.",
        "cells": [
            ("Ua auiliili atoatoa mai", "expounds fully"),
            ("e Iesu", "Jesus"),
            ("mea uma", "all things"),
            ("mai le amataga", "from the beginning"),
            ("e oo i le iuga—", "to the end—"),
            ("Ua tautala mai", "utter"),
            ("pepe ma tamaiti", "Babes and children"),
            ("i mea ofoofogia", "marvelous things"),
            ("e le mafai ona tusia—", "that cannot be written—"),
            ("O i latou e i ai", "Those who are"),
            ("i totonu o le Ekalesia", "in the Church"),
            ("a Keriso", "of Christ"),
            ("ua taatele mea uma", "have all things in common"),
            ("i totonu ia te i latou.", "among them."),
            ("E tusa o le", "about"),
            ("34", "34"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|27": {
        "en": "Jesus commands that the Church be called in His name—His mission "
              "and atoning sacrifice constitute His gospel—Men are commanded to "
              "repent and be baptized that they may be sanctified by the Holy "
              "Ghost—They are to be even as Jesus is. About A.D. 34–35.",
        "sm": "Ua poloaiina i latou e Iesu ia faaigoa le ekalesia i Lona "
              "igoa—O lana misiona ma lana taulaga togiola o Lana talalelei "
              "lea—Ua poloaiina tagata ia salamo ma papatisoina ina ia mafai ona "
              "faapaiaina i latou e le Agaga Paia—Ia avea i latou ia pei lava o "
              "Iesu ia. E tusa o le 34–35 T.A.",
        "cells": [
            ("Ua poloaiina i latou", "commands them"),
            ("e Iesu", "Jesus"),
            ("ia faaigoa le ekalesia", "that the Church be called"),
            ("i Lona igoa—", "in His name—"),
            ("O lana misiona", "His mission"),
            ("ma lana taulaga togiola", "and atoning sacrifice"),
            ("o Lana talalelei lea—", "constitute His gospel—"),
            ("Ua poloaiina tagata", "Men are commanded"),
            ("ia salamo ma papatisoina", "to repent and be baptized"),
            ("ina ia mafai ona faapaiaina", "that they may be sanctified"),
            ("i latou", "them"),
            ("e le Agaga Paia—", "by the Holy Ghost—"),
            ("Ia avea i latou", "They are to be"),
            ("ia pei lava", "even as"),
            ("o Iesu ia.", "Jesus is."),
            ("E tusa o le", "about"),
            ("34–35", "34–35"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|28": {
        "en": "Nine of the twelve disciples desire and are promised an "
              "inheritance in Christ's kingdom when they die—The Three Nephites "
              "desire and are given power over death so as to remain on the "
              "earth until Jesus comes again—They are translated and see things "
              "not lawful to utter, and they are now ministering among men. "
              "About A.D. 34–35.",
        "sm": "Ua molimanao le toaiva o soo e toasefululua mo se tofi i le malo o "
              "Keriso pe a latou feoti ma ua folafola mai ia te i latou—Ua "
              "molimanao ma tuuina mai i sa Nifaē e Toatolu le mana e le feoti "
              "ai ae nonofo pea i le lalolagi seia toe afio mai Iesu—Sa liua i "
              "latou ma vaai i mea ua le faatagaina ona tautala i ai, ma o loo "
              "auauna atu nei i latou i totonu o tagata. E tusa o le 34–35 "
              "T.A.",
        "cells": [
            ("Ua molimanao", "desire"),
            ("le toaiva o soo e toasefululua", "Nine of the twelve disciples"),
            ("mo se tofi", "an inheritance"),
            ("i le malo o Keriso", "in Christ's kingdom"),
            ("pe a latou feoti", "when they die"),
            ("ma ua folafola mai", "and are promised"),
            ("ia te i latou—", "unto them—"),
            ("Ua molimanao", "desire"),
            ("ma tuuina mai", "and are given"),
            ("i sa Nifaē e Toatolu", "to the Three Nephites"),
            ("le mana", "power"),
            ("e le feoti ai", "over death"),
            ("ae nonofo pea", "but to remain"),
            ("i le lalolagi", "on the earth"),
            ("seia toe afio mai Iesu—", "until Jesus comes again—"),
            ("Sa liua i latou", "They are translated"),
            ("ma vaai i mea", "and see things"),
            ("ua le faatagaina", "not lawful"),
            ("ona tautala i ai,", "to utter,"),
            ("ma o loo auauna atu nei", "and are now ministering"),
            ("i latou", "they"),
            ("i totonu o tagata.", "among men."),
            ("E tusa o le", "about"),
            ("34–35", "34–35"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|29": {
        "en": "The coming forth of the Book of Mormon is a sign that the Lord "
              "has commenced to gather Israel and fulfill His covenants—Those "
              "who reject His latter-day revelations and gifts will be cursed. "
              "About A.D. 34–35.",
        "sm": "O le oo mai o le Tusi a Mamona o se faailoga lea ua amataina e le "
              "Alii le faapotopotoina o Isaraelu ma faataunuu Ana feagaiga—O i "
              "latou o ē e teena Ana faaaliga ma meaalofa o aso e gata ai o le a "
              "fetuuina. E tusa o le 34–35 T.A.",
        "cells": [
            ("O le oo mai", "The coming forth"),
            ("o le Tusi a Mamona", "of the Book of Mormon"),
            ("o se faailoga lea", "is a sign"),
            ("ua amataina e le Alii", "that the Lord has commenced"),
            ("le faapotopotoina o Isaraelu", "to gather Israel"),
            ("ma faataunuu Ana feagaiga—", "and fulfill His covenants—"),
            ("O i latou o ē", "Those who"),
            ("e teena", "reject"),
            ("Ana faaaliga ma meaalofa", "His revelations and gifts"),
            ("o aso e gata ai", "of the latter days"),
            ("o le a fetuuina.", "will be cursed."),
            ("E tusa o le", "about"),
            ("34–35", "34–35"),
            ("T.A.", "A.D."),
        ],
    },
    "3nephi|30": {
        "en": "The latter-day Gentiles are commanded to repent, come unto "
              "Christ, and be numbered with the house of Israel. "
              "About A.D. 34–35.",
        "sm": "Ua poloaiina Nuuese o aso e gata ai ia salamo, o mai ia Keriso, "
              "ma faitauina faatasi ma le aiga o Isaraelu. E tusa o le 34–35 "
              "T.A.",
        "cells": [
            ("Ua poloaiina Nuuese", "The Gentiles are commanded"),
            ("o aso e gata ai", "of the latter days"),
            ("ia salamo,", "to repent,"),
            ("o mai ia Keriso,", "come unto Christ,"),
            ("ma faitauina faatasi", "and be numbered"),
            ("ma le aiga o Isaraelu.", "with the house of Israel."),
            ("E tusa o le", "about"),
            ("34–35", "34–35"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|1": {
        "en": "Ammaron instructs Mormon concerning the sacred records—War "
              "commences between the Nephites and the Lamanites—The Three "
              "Nephites are taken away—Wickedness, unbelief, sorceries, and "
              "witchcraft prevail. About A.D. 321–26.",
        "sm": "Ua faatonu Mamona e Amorona e uiga i talafaamaumau paia—Ua amata "
              "le taua i le va o sa Nifaē ma sa Lamanā—Ua aveese sa Nifaē e "
              "toatolu—Ua tumau le amioleaga, le lē talitonu, tagata iite, ma "
              "faataulaitu. E tusa o le 321–326 T.A.",
        "cells": [
            ("Ua faatonu Mamona e Amorona", "Ammaron instructs Mormon"),
            ("e uiga i talafaamaumau paia—", "concerning the sacred records—"),
            ("Ua amata le taua", "War commences"),
            ("i le va o sa Nifaē", "between the Nephites"),
            ("ma sa Lamanā—", "and the Lamanites—"),
            ("Ua aveese sa Nifaē e toatolu—", "The Three Nephites are taken away—"),
            ("Ua tumau le amioleaga,", "Wickedness prevails,"),
            ("le lē talitonu,", "unbelief,"),
            ("tagata iite,", "sorceries,"),
            ("ma faataulaitu.", "and witchcraft."),
            ("E tusa o le", "about"),
            ("321–326", "321–326"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|2": {
        "en": "Mormon leads the Nephite armies—Blood and carnage sweep the "
              "land—The Nephites lament and mourn with the sorrowing of the "
              "damned—Their day of grace is passed—Mormon obtains the plates of "
              "Nephi—Wars continue. About A.D. 327–50.",
        "sm": "Ua ta'ita'i e Mamona autau a sa Nifaē—Ua lofia le laueleele atoa "
              "i le toto ma tagata oti—Ua tagiaue ma faavauvau sa Nifaē i le "
              "faanoanoa o e ua tausalaina—Ua mavae atu lo latou aso o le alofa "
              "tunoa—Ua maua e Mamona papatusi a Nifae—Ua faaauau pea taua. E "
              "tusa o le 327–350 T.A.",
        "cells": [
            ("Ua ta'ita'i e Mamona", "Mormon leads"),
            ("autau a sa Nifaē—", "the Nephite armies—"),
            ("Ua lofia le laueleele atoa", "sweep the whole land"),
            ("i le toto", "with blood"),
            ("ma tagata oti—", "and carnage—"),
            ("Ua tagiaue ma faavauvau sa Nifaē", "The Nephites lament and mourn"),
            ("i le faanoanoa", "with the sorrowing"),
            ("o e ua tausalaina—", "of the damned—"),
            ("Ua mavae atu", "is passed"),
            ("lo latou aso", "their day"),
            ("o le alofa tunoa—", "of grace—"),
            ("Ua maua e Mamona", "Mormon obtains"),
            ("papatusi a Nifae—", "the plates of Nephi—"),
            ("Ua faaauau pea taua.", "Wars continue."),
            ("E tusa o le", "about"),
            ("327–350", "327–350"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|3": {
        "en": "Mormon cries repentance unto the Nephites—They gain a great "
              "victory and glory in their own strength—Mormon refuses to lead "
              "them, and his prayers for them are without faith—The Book of "
              "Mormon invites the twelve tribes of Israel to believe the "
              "gospel. About A.D. 360–62.",
        "sm": "Ua alaga atu e Mamona le salamo ia sa Nifaē—Ua latou maua se "
              "manumalo tele ma le mamalu i lo latou lava malosi—Ua musu Mamona "
              "e ta'ita'i i latou, ma o ana tatalo mo i latou ua aunoa ma le "
              "faatuatua—Ua valaauina e le Tusi a Mamona ituaiga e sefululua o "
              "Isaraelu ia talitonu i le talalelei. E tusa i le 360–362 T.A.",
        "cells": [
            ("Ua alaga atu e Mamona", "Mormon cries"),
            ("le salamo", "repentance"),
            ("ia sa Nifaē—", "unto the Nephites—"),
            ("Ua latou maua", "They gain"),
            ("se manumalo tele", "a great victory"),
            ("ma le mamalu", "and glory"),
            ("i lo latou lava malosi—", "in their own strength—"),
            ("Ua musu Mamona", "Mormon refuses"),
            ("e ta'ita'i i latou,", "to lead them,"),
            ("ma o ana tatalo", "and his prayers"),
            ("mo i latou", "for them"),
            ("ua aunoa ma le faatuatua—", "are without faith—"),
            ("Ua valaauina e le Tusi a Mamona", "The Book of Mormon invites"),
            ("ituaiga e sefululua o Isaraelu", "the twelve tribes of Israel"),
            ("ia talitonu i le talalelei.", "to believe the gospel."),
            ("E tusa i le", "about"),
            ("360–362", "360–362"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|4": {
        "en": "War and carnage continue—The wicked punish the wicked—Greater "
              "wickedness prevails than ever before in all Israel—Women and "
              "children are sacrificed to idols—The Lamanites begin to sweep "
              "the Nephites before them. About A.D. 363–75.",
        "sm": "Ua faaauau pea taua ma le tele o tagata fasiotia—Ua faasalaina e "
              "e ua amioleaga e ua amioleaga—Ua faateleina atili le amioleaga "
              "nai lo taimi muamua ia Isaraelu uma—Ua ositaulagaina fafine ma "
              "tamaiti i tupua—Ua amata ona aveeseina e sa Lamanā sa Nifaē mai o "
              "latou luma. E tusa o le 363–375 T.A.",
        "cells": [
            ("Ua faaauau pea taua", "War continues"),
            ("ma le tele", "and much"),
            ("o tagata fasiotia—", "of the slain—"),
            ("Ua faasalaina e e ua amioleaga", "The wicked punish"),
            ("e ua amioleaga—", "the wicked—"),
            ("Ua faateleina atili le amioleaga", "Greater wickedness prevails"),
            ("nai lo taimi muamua", "than ever before"),
            ("ia Isaraelu uma—", "in all Israel—"),
            ("Ua ositaulagaina fafine ma tamaiti", "Women and children are sacrificed"),
            ("i tupua—", "to idols—"),
            ("Ua amata ona aveeseina", "begin to sweep away"),
            ("e sa Lamanā", "The Lamanites"),
            ("sa Nifaē", "the Nephites"),
            ("mai o latou luma.", "before them."),
            ("E tusa o le", "about"),
            ("363–375", "363–375"),
            ("T.A.", "A.D."),
        ],
    },
    "4nephi|1": {
        "en": "The Nephites and the Lamanites are all converted unto the "
              "Lord—They have all things in common, work miracles, and prosper "
              "in the land—After two centuries, divisions, evils, false "
              "churches, and persecutions arise—After three hundred years, both "
              "the Nephites and the Lamanites are wicked—Ammaron hides up the "
              "sacred records. About A.D. 35–321.",
        "sm": "Ua faaliliuina uma sa Nifaē ma sa Lamanā i le Alii—Ua tutusa pau "
              "i latou i mea uma, fai vavega, ma manuia i le laueleele—Ina ua "
              "mavae le lua seneturi, sa oo ina tutupu a'e fevaevaeaiga, mea "
              "leaga, ekalesia pepelo, ma sauaga—Ina ua mavae le tolu selau "
              "tausaga, sa oo ina amioleaga uma sa Nifaē ma sa Lamanā—Ua natia e "
              "Amorona talafaamaumau paia. E tusa o le 35–321 T.A.",
        "cells": [
            ("Ua faaliliuina uma", "are all converted"),
            ("sa Nifaē ma sa Lamanā", "The Nephites and the Lamanites"),
            ("i le Alii—", "unto the Lord—"),
            ("Ua tutusa pau i latou", "They have in common"),
            ("i mea uma,", "all things,"),
            ("fai vavega,", "work miracles,"),
            ("ma manuia i le laueleele—", "and prosper in the land—"),
            ("Ina ua mavae", "After"),
            ("le lua seneturi,", "two centuries,"),
            ("sa oo ina tutupu a'e", "arise"),
            ("fevaevaeaiga,", "divisions,"),
            ("mea leaga,", "evils,"),
            ("ekalesia pepelo,", "false churches,"),
            ("ma sauaga—", "and persecutions—"),
            ("Ina ua mavae", "After"),
            ("le tolu selau tausaga,", "three hundred years,"),
            ("sa oo ina amioleaga uma", "all become wicked"),
            ("sa Nifaē ma sa Lamanā—", "the Nephites and the Lamanites—"),
            ("Ua natia e Amorona", "Ammaron hides up"),
            ("talafaamaumau paia.", "the sacred records."),
            ("E tusa o le", "about"),
            ("35–321", "35–321"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|5": {
        "en": "Mormon again leads the Nephite armies in battles of blood and "
              "carnage—The Book of Mormon will come forth to convince all Israel "
              "that Jesus is the Christ—Because of their unbelief, the Lamanites "
              "will be scattered, and the Spirit will cease to strive with "
              "them—They will receive the gospel from the Gentiles in the latter "
              "days. About A.D. 375–84.",
        "sm": "Ua toe taitaia e Mamona autau a sa Nifaē i taua o le toto ma le "
              "tele o tagata oti—O le a oo mai le Tusi a Mamona e faatalitonu "
              "Isaraelu uma o Iesu o le Keriso—Ona o lo latou le talitonu o lea "
              "o le a faataapeapeina ai sa Lamanā, ma o le a le toe finau le "
              "Agaga ia te i latou—O le a latou maua le talalelei mai Nuuese i "
              "aso e gata ai. E tusa o le 375–384 T.A.",
        "cells": [
            ("Ua toe taitaia e Mamona", "Mormon again leads"),
            ("autau a sa Nifaē", "the Nephite armies"),
            ("i taua o le toto", "in battles of blood"),
            ("ma le tele", "and much"),
            ("o tagata oti—", "carnage—"),
            ("O le a oo mai", "will come forth"),
            ("le Tusi a Mamona", "the Book of Mormon"),
            ("e faatalitonu Isaraelu uma", "to convince all Israel"),
            ("o Iesu o le Keriso—", "that Jesus is the Christ—"),
            ("Ona o", "Because of"),
            ("lo latou le talitonu", "their unbelief"),
            ("o lea", "therefore"),
            ("o le a faataapeapeina ai", "will be scattered"),
            ("sa Lamanā,", "the Lamanites,"),
            ("ma o le a", "and will"),
            ("le toe finau le Agaga", "the Spirit no more strive"),
            ("ia te i latou—", "with them—"),
            ("O le a latou maua", "They will receive"),
            ("le talalelei", "the gospel"),
            ("mai Nuuese", "from the Gentiles"),
            ("i aso e gata ai.", "in the latter days."),
            ("E tusa o le", "about"),
            ("375–384", "375–384"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|6": {
        "en": "The Nephites gather to the land of Cumorah for the final "
              "battles—Mormon hides the sacred records in the hill "
              "Cumorah—The Lamanites are victorious, and the Nephite nation is "
              "destroyed—Hundreds of thousands are slain with the sword. "
              "About A.D. 385.",
        "sm": "Ua faapotopoto faatasi sa Nifaē i le laueleele o Kumora mo le taua "
              "faaiu—Ua natia e Mamona talafaamaumau paia i le Mauga o Kumora—Ua "
              "manumalo sa Lamanā, ma ua faaumatia le malo o sa Nifaē—Ua fasiotia "
              "selau o afe i le pelu. E tusa o le 385 T.A.",
        "cells": [
            ("Ua faapotopoto faatasi sa Nifaē", "The Nephites gather"),
            ("i le laueleele o Kumora", "to the land of Cumorah"),
            ("mo le taua faaiu—", "for the final battles—"),
            ("Ua natia e Mamona", "Mormon hides"),
            ("talafaamaumau paia", "the sacred records"),
            ("i le Mauga o Kumora—", "in the hill Cumorah—"),
            ("Ua manumalo sa Lamanā,", "The Lamanites are victorious,"),
            ("ma ua faaumatia", "and is destroyed"),
            ("le malo o sa Nifaē—", "the Nephite nation—"),
            ("Ua fasiotia selau o afe", "Hundreds of thousands are slain"),
            ("i le pelu.", "with the sword."),
            ("E tusa o le", "about"),
            ("385", "385"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|7": {
        "en": "Mormon invites the Lamanites of the latter days to believe in "
              "Christ, accept His gospel, and be saved—All who believe the Bible "
              "will also believe the Book of Mormon. About A.D. 385.",
        "sm": "Ua valaaulia e Mamona sa Lamanā i aso e gata ai ia talitonu ia "
              "Keriso, talia Lana talalelei, ma faaolaina—O i latou uma o e e "
              "talitonu i le Tusi Paia o le a talitonu foi i le Tusi a Mamona. E "
              "tusa o le 385 T.A.",
        "cells": [
            ("Ua valaaulia e Mamona sa Lamanā", "Mormon invites the Lamanites"),
            ("i aso e gata ai", "of the latter days"),
            ("ia talitonu ia Keriso,", "to believe in Christ,"),
            ("talia Lana talalelei,", "accept His gospel,"),
            ("ma faaolaina—", "and be saved—"),
            ("O i latou uma", "All"),
            ("o e e talitonu", "who believe"),
            ("i le Tusi Paia", "the Bible"),
            ("o le a talitonu foi", "will also believe"),
            ("i le Tusi a Mamona.", "the Book of Mormon."),
            ("E tusa o le", "about"),
            ("385", "385"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|8": {
        "en": "The Lamanites seek out and destroy the Nephites—The Book of "
              "Mormon will come forth by the power of God—Woes pronounced upon "
              "those who breathe out wrath and strife against the work of the "
              "Lord—The Nephite record will come forth in a day of wickedness, "
              "degeneracy, and apostasy. About A.D. 400–421.",
        "sm": "Ua saili e sa Lamanā sa Nifaē ma faaumatia i latou—O le a oo mai "
              "le Tusi a Mamona e ala i le mana o le Atua—Ua folafola mai malaia "
              "i luga o i latou o e e manavaina le ita ma i e fetaua'i e faasaga "
              "i le galuega a le Alii—O le a oo mai le talafaamaumau a sa Nifaē i "
              "se aso o le amioleaga, tu mataga, ma le liliuese. E tusa o le "
              "400–421 T.A.",
        "cells": [
            ("Ua saili e sa Lamanā", "The Lamanites seek out"),
            ("sa Nifaē", "the Nephites"),
            ("ma faaumatia i latou—", "and destroy them—"),
            ("O le a oo mai", "will come forth"),
            ("le Tusi a Mamona", "the Book of Mormon"),
            ("e ala i le mana", "by the power"),
            ("o le Atua—", "of God—"),
            ("Ua folafola mai malaia", "Woes pronounced"),
            ("i luga o i latou", "upon those"),
            ("o e e manavaina", "who breathe out"),
            ("le ita", "wrath"),
            ("ma i e fetaua'i", "and strife"),
            ("e faasaga i le galuega", "against the work"),
            ("a le Alii—", "of the Lord—"),
            ("O le a oo mai", "will come forth"),
            ("le talafaamaumau a sa Nifaē", "The Nephite record"),
            ("i se aso", "in a day"),
            ("o le amioleaga,", "of wickedness,"),
            ("tu mataga,", "degeneracy,"),
            ("ma le liliuese.", "and apostasy."),
            ("E tusa o le", "about"),
            ("400–421", "400–421"),
            ("T.A.", "A.D."),
        ],
    },
    "mormon|9": {
        "en": "Moroni calls upon those who do not believe in Christ to "
              "repent—He proclaims a God of miracles, who gives revelations and "
              "pours out gifts and signs upon the faithful—Miracles cease "
              "because of unbelief—Signs follow those who believe—Men are "
              "exhorted to be wise and keep the commandments. About A.D. 401–21.",
        "sm": "Ua valaau atu Moronae i e ua le talitonu ia Keriso ia salamo—Ua "
              "ia tala'i atu se Atua o vavega, o le na te tuuina mai faaaliga ma "
              "liligi ifo meaalofa ma faailoga i luga o e e faatuatua—E taofia "
              "vavega ona o le le talitonu—E mulimuli atu faailoga ia te i latou "
              "o e e talitonu—Ua fautuaina tagata ia popoto ma tausia poloaiga. "
              "E tusa o le 401–421 T.A.",
        "cells": [
            ("Ua valaau atu Moronae", "Moroni calls"),
            ("i e ua le talitonu", "upon those who disbelieve"),
            ("ia Keriso", "in Christ"),
            ("ia salamo—", "to repent—"),
            ("Ua ia tala'i atu", "He proclaims"),
            ("se Atua o vavega,", "a God of miracles,"),
            ("o le na te tuuina mai", "who gives"),
            ("faaaliga", "revelations"),
            ("ma liligi ifo", "and pours out"),
            ("meaalofa ma faailoga", "gifts and signs"),
            ("i luga o", "upon"),
            ("e e faatuatua—", "the faithful—"),
            ("E taofia vavega", "Miracles cease"),
            ("ona o le le talitonu—", "because of unbelief—"),
            ("E mulimuli atu faailoga", "Signs follow"),
            ("ia te i latou", "them"),
            ("o e e talitonu—", "who believe—"),
            ("Ua fautuaina tagata ia popoto", "Men are exhorted to be wise"),
            ("ma tausia poloaiga.", "and keep the commandments."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "ether|1": {
        "en": "Moroni abridges the writings of Ether—Ether's genealogy is set "
              "forth—The language of the Jaredites is not confounded at the "
              "Tower of Babel—The Lord promises to lead them to a choice land "
              "and make them a great nation.",
        "sm": "Ua otooto e Moronae tusitusiga a Eteru—Ua faamatala mai le gafa o "
              "Eteru—Sa lei faaeseeseina le gagana a sa Iaretō i le Olo o "
              "Papelu—Ua folafola mai e le Alii o le a ia taitaia i latou i se "
              "laueleele filifilia ma faia i latou ia avea ma se malo tele.",
        "cells": [
            ("Ua otooto e Moronae", "Moroni abridges"),
            ("tusitusiga a Eteru—", "the writings of Ether—"),
            ("Ua faamatala mai", "is set forth"),
            ("le gafa o Eteru—", "Ether's genealogy—"),
            ("Sa lei faaeseeseina", "is not confounded"),
            ("le gagana a sa Iaretō", "the language of the Jaredites"),
            ("i le Olo o Papelu—", "at the Tower of Babel—"),
            ("Ua folafola mai e le Alii", "The Lord promises"),
            ("o le a ia taitaia", "He will lead"),
            ("i latou", "them"),
            ("i se laueleele filifilia", "to a choice land"),
            ("ma faia i latou", "and make them"),
            ("ia avea ma", "to become"),
            ("se malo tele.", "a great nation."),
        ],
    },
    "ether|2": {
        "en": "The Jaredites prepare for their journey to a promised land—It is "
              "a choice land whereon men must serve Christ or be swept off—The "
              "Lord talks to the brother of Jared for three hours—The Jaredites "
              "build barges—The Lord asks the brother of Jared to propose how "
              "the barges will be lighted.",
        "sm": "Ua sauni sa Iareto mo la latou malaga i se laueleele na "
              "folafolaina—O lea laueleele o se laueleele filifilia e ao ina "
              "auauna atu ai ia Keriso e o nonofo ai a leai o le a tafiesea i "
              "latou—Ua fetalai mai le Alii i le uso o Iareto mo le tolu itula—Ua "
              "fausia e sa Iareto ni vaa—Ua fetalai le Alii i le uso o Iareto e "
              "fautua atu se ala e faamalamalama ai vaa.",
        "cells": [
            ("Ua sauni sa Iareto", "The Jaredites prepare"),
            ("mo la latou malaga", "for their journey"),
            ("i se laueleele na folafolaina—", "to a promised land—"),
            ("O lea laueleele", "This land"),
            ("o se laueleele filifilia", "is a choice land"),
            ("e ao ina auauna atu ai", "must serve"),
            ("ia Keriso", "Christ"),
            ("e o nonofo ai", "who dwell there"),
            ("a leai", "or"),
            ("o le a tafiesea i latou—", "they will be swept off—"),
            ("Ua fetalai mai le Alii", "The Lord talks"),
            ("i le uso o Iareto", "to the brother of Jared"),
            ("mo le tolu itula—", "for three hours—"),
            ("Ua fausia e sa Iareto", "The Jaredites build"),
            ("ni vaa—", "barges—"),
            ("Ua fetalai le Alii", "The Lord asks"),
            ("i le uso o Iareto", "the brother of Jared"),
            ("e fautua atu se ala", "to propose how"),
            ("e faamalamalama ai vaa.", "the barges will be lighted."),
        ],
    },
    "ether|3": {
        "en": "The brother of Jared sees the finger of the Lord as He touches "
              "sixteen stones—Christ shows His spirit body to the brother of "
              "Jared—Those who have a perfect knowledge cannot be kept from "
              "within the veil—Interpreters are provided to bring the Jaredite "
              "record to light.",
        "sm": "Ua vaai le uso o Iareto i le tamatamaiaao o le Alii a'o pa'i ane o "
              "Ia i maa e sefuluono—Ua faaali mai e Keriso Lona tino agaga i le "
              "uso o Iareto—O i latou o e ua mauaina se malamalama atoatoa e le "
              "mafai ona taofia mai totonu o le veli—Ua saunia maa-faamatala "
              "gagana e aumai ai le talafaamaumau a sa Iaretō i le malamalama.",
        "cells": [
            ("Ua vaai", "sees"),
            ("le uso o Iareto", "the brother of Jared"),
            ("i le tamatamaiaao", "the finger"),
            ("o le Alii", "of the Lord"),
            ("a'o pa'i ane o Ia", "as He touches"),
            ("i maa e sefuluono—", "sixteen stones—"),
            ("Ua faaali mai e Keriso", "Christ shows"),
            ("Lona tino agaga", "His spirit body"),
            ("i le uso o Iareto—", "to the brother of Jared—"),
            ("O i latou o e", "Those who"),
            ("ua mauaina se malamalama atoatoa", "have a perfect knowledge"),
            ("e le mafai ona taofia", "cannot be kept"),
            ("mai totonu o le veli—", "from within the veil—"),
            ("Ua saunia maa-faamatala gagana", "Interpreters are provided"),
            ("e aumai ai", "to bring"),
            ("le talafaamaumau a sa Iaretō", "the Jaredite record"),
            ("i le malamalama.", "to light."),
        ],
    },
    "ether|4": {
        "en": "Moroni is commanded to seal up the writings of the brother of "
              "Jared—They will not be revealed until men have faith even as the "
              "brother of Jared—Christ commands men to believe His words and "
              "those of His disciples—Men are commanded to repent, believe the "
              "gospel, and be saved.",
        "sm": "Ua poloaiina Moronae e faamaufaailoga tusitusiga a le uso o "
              "Iareto—O le a lē faaalia ia mea seia maua e tagata le faatuatua e "
              "pei lava o le uso o Iareto—Ua poloaiina tagata e Keriso ia "
              "talitonu i Ana upu ma upu a Ona soo—Ua poloaiina tagata ia "
              "salamo, talitonu i le talalelei, ma faaolaina.",
        "cells": [
            ("Ua poloaiina Moronae", "Moroni is commanded"),
            ("e faamaufaailoga tusitusiga", "to seal up the writings"),
            ("a le uso o Iareto—", "of the brother of Jared—"),
            ("O le a lē faaalia", "will not be revealed"),
            ("ia mea", "these things"),
            ("seia maua e tagata", "until men have"),
            ("le faatuatua", "faith"),
            ("e pei lava", "even as"),
            ("o le uso o Iareto—", "the brother of Jared—"),
            ("Ua poloaiina tagata e Keriso", "Christ commands men"),
            ("ia talitonu i Ana upu", "to believe His words"),
            ("ma upu a Ona soo—", "and those of His disciples—"),
            ("Ua poloaiina tagata", "Men are commanded"),
            ("ia salamo,", "to repent,"),
            ("talitonu i le talalelei,", "believe the gospel,"),
            ("ma faaolaina.", "and be saved."),
        ],
    },
    "ether|5": {
        "en": "Three witnesses and the work itself will stand as a testimony of "
              "the truthfulness of the Book of Mormon.",
        "sm": "O molimau e toatolu ma le galuega lava ia o le a tutulai o se "
              "molimau i le moni o le Tusi a Mamona.",
        "cells": [
            ("O molimau e toatolu", "Three witnesses"),
            ("ma le galuega lava ia", "and the work itself"),
            ("o le a tutulai", "will stand"),
            ("o se molimau", "as a testimony"),
            ("i le moni", "of the truthfulness"),
            ("o le Tusi a Mamona.", "of the Book of Mormon."),
        ],
    },
    "ether|6": {
        "en": "The Jaredite barges are driven by the winds to the promised "
              "land—The people praise the Lord for His goodness—Orihah is "
              "appointed king over them—Jared and his brother die.",
        "sm": "Ua uunai atu vaa o sa Iaretō e le matagi agai i le laueleele na "
              "folafolaina—Ua vivii atu le nuu i le Alii mo Lona agalelei—Ua "
              "tofia Oraea e avea ma tupu i luga o i latou—Ua maliliu Iareto ma "
              "lona uso.",
        "cells": [
            ("Ua uunai atu", "are driven"),
            ("vaa o sa Iaretō", "The Jaredite barges"),
            ("e le matagi", "by the winds"),
            ("agai i le laueleele", "to the land"),
            ("na folafolaina—", "promised—"),
            ("Ua vivii atu le nuu", "The people praise"),
            ("i le Alii", "the Lord"),
            ("mo Lona agalelei—", "for His goodness—"),
            ("Ua tofia Oraea", "Orihah is appointed"),
            ("e avea ma tupu", "as king"),
            ("i luga o i latou—", "over them—"),
            ("Ua maliliu Iareto", "Jared dies"),
            ("ma lona uso.", "and his brother."),
        ],
    },
    "ether|7": {
        "en": "Orihah reigns in righteousness—Amid usurpation and strife, the "
              "rival kingdoms of Shule and Cohor are set up—Prophets condemn the "
              "wickedness and idolatry of the people, who then repent.",
        "sm": "Ua nofotupu Oraea i le amiotonu—Ua faatutūina malo vatau o Sulē ma "
              "Ko'oro i le lotolotoi o fouvalega ma fetaua'iga—Ua tausalaina e "
              "perofeta le amioleaga ma le ifo i tupua o tagata, o ē na salamo "
              "ai.",
        "cells": [
            ("Ua nofotupu Oraea", "Orihah reigns"),
            ("i le amiotonu—", "in righteousness—"),
            ("Ua faatutūina malo vatau", "rival kingdoms are set up"),
            ("o Sulē ma Ko'oro", "of Shule and Cohor"),
            ("i le lotolotoi o fouvalega", "amid usurpation"),
            ("ma fetaua'iga—", "and strife—"),
            ("Ua tausalaina e perofeta", "Prophets condemn"),
            ("le amioleaga", "the wickedness"),
            ("ma le ifo i tupua", "and idolatry"),
            ("o tagata,", "of the people,"),
            ("o ē na salamo ai.", "who then repent."),
        ],
    },
    "ether|8": {
        "en": "There is strife and contention over the kingdom—Akish forms an "
              "oath-bound secret combination to slay the king—Secret "
              "combinations are of the devil and result in the destruction of "
              "nations—Modern Gentiles are warned against the secret "
              "combination that will seek to overthrow the freedom of all "
              "lands, nations, and countries.",
        "sm": "Ua i ai feteenaiga ma finauga i le malo—Ua faatu e Akiso se "
              "faapotopotoga faalilolilo ua fusia i se tautoga e fasioti le "
              "tupu—O faapotopotoga faalilolilo e mai le tiapolo ma e 'u i le "
              "faaumatiaina o malo—Ua lapata'ia Nuuese o ona po nei e faasaga i "
              "le faapotopotoga faalilolilo lea o le a saili e faatoilalo le "
              "saolotoga o laueleele uma, malo, ma atunuu.",
        "cells": [
            ("Ua i ai", "There is"),
            ("feteenaiga ma finauga", "strife and contention"),
            ("i le malo—", "over the kingdom—"),
            ("Ua faatu e Akiso", "Akish forms"),
            ("se faapotopotoga faalilolilo", "a secret combination"),
            ("ua fusia i se tautoga", "oath-bound"),
            ("e fasioti le tupu—", "to slay the king—"),
            ("O faapotopotoga faalilolilo", "Secret combinations"),
            ("e mai le tiapolo", "are of the devil"),
            ("ma e 'u i le faaumatiaina", "and result in the destruction"),
            ("o malo—", "of nations—"),
            ("Ua lapata'ia Nuuese", "Gentiles are warned"),
            ("o ona po nei", "of these days"),
            ("e faasaga i le faapotopotoga faalilolilo", "against the secret combination"),
            ("lea", "which"),
            ("o le a saili e faatoilalo", "that will seek to overthrow"),
            ("le saolotoga", "the freedom"),
            ("o laueleele uma,", "of all lands,"),
            ("malo, ma atunuu.", "nations, and countries."),
        ],
    },
    "ether|9": {
        "en": "The kingdom passes from one to another by descent, intrigue, and "
              "murder—Emer saw the Son of Righteousness—Many prophets cry "
              "repentance—A famine and poisonous serpents plague the people.",
        "sm": "E faasolo atu le malo mai le tasi i le isi e ala i le gafa, "
              "togafiti, ma le fasioti tagata—Sa vaai Emera i le Atalii o le "
              "Amiotonu—E toatele perofeta ua latou alaga atu le salamo—Ua "
              "malaia tagata i se oge ma gata uogo.",
        "cells": [
            ("E faasolo atu le malo", "The kingdom passes"),
            ("mai le tasi", "from one"),
            ("i le isi", "to another"),
            ("e ala i le gafa,", "by descent,"),
            ("togafiti,", "intrigue,"),
            ("ma le fasioti tagata—", "and murder—"),
            ("Sa vaai Emera", "Emer saw"),
            ("i le Atalii", "the Son"),
            ("o le Amiotonu—", "of Righteousness—"),
            ("E toatele perofeta", "Many prophets"),
            ("ua latou alaga atu", "cry"),
            ("le salamo—", "repentance—"),
            ("Ua malaia tagata", "plague the people"),
            ("i se oge", "a famine"),
            ("ma gata uogo.", "and poisonous serpents."),
        ],
    },
    "ether|10": {
        "en": "One king succeeds another—Some of the kings are righteous; others "
              "are wicked—When righteousness prevails, the people are blessed "
              "and prospered by the Lord.",
        "sm": "Ua suitulaga le tasi tupu i le isi tupu—O ni isi o tupu ua "
              "amiotonu; o ni isi ua amioleaga—A manumalo le amiotonu, e "
              "faamanuia ma faatamaoaiga e le Alii tagata.",
        "cells": [
            ("Ua suitulaga le tasi tupu", "One king succeeds"),
            ("i le isi tupu—", "another—"),
            ("O ni isi o tupu", "Some of the kings"),
            ("ua amiotonu;", "are righteous;"),
            ("o ni isi ua amioleaga—", "others are wicked—"),
            ("A manumalo le amiotonu,", "When righteousness prevails,"),
            ("e faamanuia ma faatamaoaiga", "are blessed and prospered"),
            ("e le Alii", "by the Lord"),
            ("tagata.", "the people."),
        ],
    },
    "ether|11": {
        "en": "Wars, dissensions, and wickedness dominate Jaredite "
              "life—Prophets predict the utter destruction of the Jaredites "
              "unless they repent—The people reject the words of the prophets.",
        "sm": "O taua, fevaevaeaiga, ma le amioleaga ua pulea olaga o tagata sa "
              "Iaretō—Ua valoia e perofeta le faaumatiaina atoa o sa Iaretō "
              "vagana ai ua latou salamo—Ua teena e tagata upu a perofeta.",
        "cells": [
            ("O taua, fevaevaeaiga,", "Wars, dissensions,"),
            ("ma le amioleaga", "and wickedness"),
            ("ua pulea olaga", "dominate the lives"),
            ("o tagata sa Iaretō—", "of the Jaredites—"),
            ("Ua valoia e perofeta", "Prophets predict"),
            ("le faaumatiaina atoa", "the utter destruction"),
            ("o sa Iaretō", "of the Jaredites"),
            ("vagana ai ua latou salamo—", "unless they repent—"),
            ("Ua teena e tagata", "The people reject"),
            ("upu a perofeta.", "the words of the prophets."),
        ],
    },
    "ether|12": {
        "en": "The prophet Ether exhorts the people to believe in God—Moroni "
              "recounts the wonders and marvels done by faith—Faith enabled the "
              "brother of Jared to see Christ—The Lord gives men weakness that "
              "they may be humble—The brother of Jared moved Mount Zerin by "
              "faith—Faith, hope, and charity are essential to salvation—Moroni "
              "saw Jesus face to face.",
        "sm": "Ua apoapoai atu le perofeta o Eteru i tagata ia talitonu i le "
              "Atua—Ua toe faamatala mai e Moronae mea ofoofogia ma maoae na "
              "faia i le faatuatua—O le faatuatua na mafai ai e le uso o Iareto "
              "ona vaai ia Keriso—E tuuina mai e le Alii i tagata vaivaiga ina ia "
              "faalotomaualalalo ai i latou—Sa aveese e le uso o Iareto le Mauga "
              "o Serima i le faatuatua—Ua taua mo le faaolataga le faatuatua, "
              "faamoemoe, ma le alofa mamā—Sa vaai faafesaga'i Moronae ia Iesu.",
        "cells": [
            ("Ua apoapoai atu", "exhorts"),
            ("le perofeta o Eteru", "The prophet Ether"),
            ("i tagata", "the people"),
            ("ia talitonu i le Atua—", "to believe in God—"),
            ("Ua toe faamatala mai e Moronae", "Moroni recounts"),
            ("mea ofoofogia ma maoae", "the wonders and marvels"),
            ("na faia i le faatuatua—", "done by faith—"),
            ("O le faatuatua", "Faith"),
            ("na mafai ai", "enabled"),
            ("e le uso o Iareto", "the brother of Jared"),
            ("ona vaai ia Keriso—", "to see Christ—"),
            ("E tuuina mai e le Alii", "The Lord gives"),
            ("i tagata vaivaiga", "men weakness"),
            ("ina ia faalotomaualalalo ai", "that they may be humble"),
            ("i latou—", "them—"),
            ("Sa aveese e le uso o Iareto", "The brother of Jared moved"),
            ("le Mauga o Serima", "Mount Zerin"),
            ("i le faatuatua—", "by faith—"),
            ("Ua taua mo le faaolataga", "are essential to salvation"),
            ("le faatuatua, faamoemoe,", "Faith, hope,"),
            ("ma le alofa mamā—", "and charity—"),
            ("Sa vaai faafesaga'i Moronae", "Moroni saw face to face"),
            ("ia Iesu.", "Jesus."),
        ],
    },
    "ether|13": {
        "en": "Ether speaks of a New Jerusalem to be built in America by the "
              "seed of Joseph—He prophesies, is cast out, writes the Jaredite "
              "history, and foretells the destruction of the Jaredites—War "
              "rages over all the land.",
        "sm": "Ua tautala Eteru e uiga i se Ierusalema Fou o le a faatuina i "
              "Amerika e fanau a Iosefa—Ua vavalo atu o ia, ua tuli ese i fafo, "
              "tusia le talafaasolopito o sa Iaretō, ma valoia le faaumatiaga o "
              "sa Iaretō—Ua sasao malosi taua i luga o le laueleele atoa.",
        "cells": [
            ("Ua tautala Eteru", "Ether speaks"),
            ("e uiga i", "of"),
            ("se Ierusalema Fou", "a New Jerusalem"),
            ("o le a faatuina", "to be built"),
            ("i Amerika", "in America"),
            ("e fanau a Iosefa—", "by the seed of Joseph—"),
            ("Ua vavalo atu o ia,", "He prophesies,"),
            ("ua tuli ese i fafo,", "is cast out,"),
            ("tusia le talafaasolopito", "writes the history"),
            ("o sa Iaretō,", "of the Jaredites,"),
            ("ma valoia le faaumatiaga", "and foretells the destruction"),
            ("o sa Iaretō—", "of the Jaredites—"),
            ("Ua sasao malosi taua", "War rages"),
            ("i luga o", "over"),
            ("le laueleele atoa.", "all the land."),
        ],
    },
    "ether|14": {
        "en": "The iniquity of the people brings a curse upon the "
              "land—Coriantumr engages in warfare against Gilead, then Lib, and "
              "then Shiz—Blood and carnage cover the land.",
        "sm": "O le amioleaga o tagata ua aumai ai se fetuu i luga o le "
              "laueleele—Ua tau e Korianetuma se taua e faasaga ia Kiliata, "
              "sosoo ai ma Lipi, ona sosoo ai lea ma Sesa—Ua lofia le laueleele "
              "i le toto ma tagata oti.",
        "cells": [
            ("O le amioleaga o tagata", "The iniquity of the people"),
            ("ua aumai ai se fetuu", "brings a curse"),
            ("i luga o le laueleele—", "upon the land—"),
            ("Ua tau e Korianetuma", "Coriantumr wages"),
            ("se taua", "war"),
            ("e faasaga ia Kiliata,", "against Gilead,"),
            ("sosoo ai ma Lipi,", "then Lib,"),
            ("ona sosoo ai lea", "and then"),
            ("ma Sesa—", "Shiz—"),
            ("Ua lofia le laueleele", "cover the land"),
            ("i le toto", "with blood"),
            ("ma tagata oti.", "and carnage."),
        ],
    },
    "ether|15": {
        "en": "Millions of the Jaredites are slain in battle—Shiz and "
              "Coriantumr assemble all the people to mortal combat—The Spirit of "
              "the Lord ceases to strive with them—The Jaredite nation is "
              "utterly destroyed—Only Coriantumr remains.",
        "sm": "E miliona ma miliona sa Iaretō ua fasiotia i taua—Ua faapotopoto e "
              "Sesa ma Korianetuma tagata uma e tau seia oo i le oti—Ua le toe "
              "finau le Agaga o le Alii ma i latou—Ua matuā faaumatia lava le "
              "malo o sa Iaretō—Ua na'o Korianetuma ua totoe.",
        "cells": [
            ("E miliona ma miliona", "Millions"),
            ("sa Iaretō", "of the Jaredites"),
            ("ua fasiotia i taua—", "are slain in battle—"),
            ("Ua faapotopoto e Sesa ma Korianetuma", "Shiz and Coriantumr assemble"),
            ("tagata uma", "all the people"),
            ("e tau", "to fight"),
            ("seia oo i le oti—", "unto death—"),
            ("Ua le toe finau", "ceases to strive"),
            ("le Agaga o le Alii", "The Spirit of the Lord"),
            ("ma i latou—", "with them—"),
            ("Ua matuā faaumatia lava", "is utterly destroyed"),
            ("le malo o sa Iaretō—", "The Jaredite nation—"),
            ("Ua na'o Korianetuma", "Only Coriantumr"),
            ("ua totoe.", "remains."),
        ],
    },
    "moroni|1": {
        "en": "Moroni writes for the benefit of the Lamanites—The Nephites who "
              "will not deny Christ are put to death. About A.D. 401–21.",
        "sm": "Ua tusi Moronae mo le manuia o sa Lamanā—O sa Nifaē o e sa le "
              "faafitia Keriso ua fasiotia. E tusa o le 401–421 T.A.",
        "cells": [
            ("Ua tusi Moronae", "Moroni writes"),
            ("mo le manuia", "for the benefit"),
            ("o sa Lamanā—", "of the Lamanites—"),
            ("O sa Nifaē", "The Nephites"),
            ("o e sa le faafitia", "who will not deny"),
            ("Keriso", "Christ"),
            ("ua fasiotia.", "are put to death."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|2": {
        "en": "Jesus gave the twelve Nephite disciples power to confer the gift "
              "of the Holy Ghost. About A.D. 401–21.",
        "sm": "Sa tuu atu e Iesu i soo sa Nifaē e toasefululua le mana e faae'e "
              "atu ai le meaalofa o le Agaga Paia. E tusa o le 401–421 T.A.",
        "cells": [
            ("Sa tuu atu e Iesu", "Jesus gave"),
            ("i soo sa Nifaē", "the Nephite disciples"),
            ("e toasefululua", "the twelve"),
            ("le mana", "power"),
            ("e faae'e atu ai", "to confer"),
            ("le meaalofa", "the gift"),
            ("o le Agaga Paia.", "of the Holy Ghost."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|3": {
        "en": "Elders ordain priests and teachers by the laying on of hands. "
              "About A.D. 401–21.",
        "sm": "E faauu e toeaina faitaulaga ma a'oa'o i le faaee atu o lima. E "
              "tusa o le 401–421 T.A.",
        "cells": [
            ("E faauu e toeaina", "Elders ordain"),
            ("faitaulaga ma a'oa'o", "priests and teachers"),
            ("i le faaee atu", "by the laying on"),
            ("o lima.", "of hands."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|4": {
        "en": "How elders and priests administer the sacramental bread is "
              "explained. About A.D. 401–21.",
        "sm": "Ua faamalamalama mai le ala e faamanuia ai e toeaina ma "
              "faitaulaga le areto o le faamanatuga. E tusa o le 401–421 T.A.",
        "cells": [
            ("Ua faamalamalama mai le ala", "How is explained"),
            ("e faamanuia ai", "administer"),
            ("e toeaina ma faitaulaga", "elders and priests"),
            ("le areto o le faamanatuga.", "the sacramental bread."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|5": {
        "en": "The mode of administering the sacramental wine is set forth. "
              "About A.D. 401–21.",
        "sm": "Ua faamalamalama mai le ala e faamanuia ai le uaina o le "
              "faamanatuga. E tusa o le 401–421 T.A.",
        "cells": [
            ("Ua faamalamalama mai le ala", "The mode is set forth"),
            ("e faamanuia ai le uaina", "of administering the wine"),
            ("o le faamanatuga.", "of the sacrament."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|6": {
        "en": "Repentant persons are baptized and fellowshipped—Church members "
              "who repent are forgiven—Meetings are conducted by the power of the "
              "Holy Ghost. About A.D. 401–21.",
        "sm": "O tagata e salamo ia papatisoina ma faaaumeaina—O tagata o le "
              "Ekalesia o e e salamo e faamagaloina—Ia taitaia sauniga i le mana "
              "o le Agaga Paia. E tusa o le 401–421 T.A.",
        "cells": [
            ("O tagata e salamo", "Repentant persons"),
            ("ia papatisoina ma faaaumeaina—", "are baptized and fellowshipped—"),
            ("O tagata o le Ekalesia", "Church members"),
            ("o e e salamo", "who repent"),
            ("e faamagaloina—", "are forgiven—"),
            ("Ia taitaia sauniga", "Meetings are conducted"),
            ("i le mana", "by the power"),
            ("o le Agaga Paia.", "of the Holy Ghost."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|7": {
        "en": "An invitation is given to enter into the rest of the Lord—Pray "
              "with real intent—The Spirit of Christ enables men to know good "
              "from evil—Satan persuades men to deny Christ and do evil—The "
              "prophets manifest the coming of Christ—By faith, miracles are "
              "wrought and angels minister—Men should hope for eternal life and "
              "cleave unto charity. About A.D. 401–21.",
        "sm": "Ua tuuina mai se valaaulia ia ulu atu i le malologa o le Alii—"
              "Tatalo atu ma le loto faamaoni—O le Agaga o Keriso e mafai ai e "
              "tagata ona iloa le lelei mai le leaga—E tauanau e Satani tagata ia "
              "latou teena Keriso ma fai mea leaga—Ua faaali mai e perofeta le "
              "afio mai o Keriso—O le faatuatua e faia ai vavega ma auauna mai ai "
              "agelu—E tatau i tagata ona faamoemoe mo le ola e faavavau ma pipii "
              "i le alofa mamā. E tusa o le 401–421 T.A.",
        "cells": [
            ("Ua tuuina mai se valaaulia", "An invitation is given"),
            ("ia ulu atu", "to enter into"),
            ("i le malologa", "the rest"),
            ("o le Alii—", "of the Lord—"),
            ("Tatalo atu", "Pray"),
            ("ma le loto faamaoni—", "with real intent—"),
            ("O le Agaga o Keriso", "The Spirit of Christ"),
            ("e mafai ai e tagata", "enables men"),
            ("ona iloa le lelei", "to know good"),
            ("mai le leaga—", "from evil—"),
            ("E tauanau e Satani tagata", "Satan persuades men"),
            ("ia latou teena Keriso", "to deny Christ"),
            ("ma fai mea leaga—", "and do evil—"),
            ("Ua faaali mai e perofeta", "The prophets manifest"),
            ("le afio mai o Keriso—", "the coming of Christ—"),
            ("O le faatuatua", "By faith"),
            ("e faia ai vavega", "miracles are wrought"),
            ("ma auauna mai ai agelu—", "and angels minister—"),
            ("E tatau i tagata", "Men should"),
            ("ona faamoemoe", "hope"),
            ("mo le ola e faavavau", "for eternal life"),
            ("ma pipii", "and cleave"),
            ("i le alofa mamā.", "unto charity."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|8": {
        "en": "The baptism of little children is an evil abomination—Little "
              "children are alive in Christ because of the Atonement—Faith, "
              "repentance, meekness and lowliness of heart, receiving the Holy "
              "Ghost, and enduring to the end lead to salvation. About A.D. "
              "401–21.",
        "sm": "O le papatisoina o tamaiti laiti o se mea leaga inosia—Ua ola "
              "tamaiti laiti ia Keriso ona o le Togiola—O le faatuatua, salamo, "
              "agamalu ma le maualalo o le loto, mauaina o le Agaga Paia, ma le "
              "tumau e oo i le iuga, e tau atu i le faaolataga. E tusa o le "
              "401–421 T.A.",
        "cells": [
            ("O le papatisoina", "The baptism"),
            ("o tamaiti laiti", "of little children"),
            ("o se mea leaga inosia—", "is an evil abomination—"),
            ("Ua ola tamaiti laiti", "Little children are alive"),
            ("ia Keriso", "in Christ"),
            ("ona o le Togiola—", "because of the Atonement—"),
            ("O le faatuatua, salamo,", "Faith, repentance,"),
            ("agamalu", "meekness"),
            ("ma le maualalo", "and lowliness"),
            ("o le loto,", "of heart,"),
            ("mauaina", "receiving"),
            ("o le Agaga Paia,", "the Holy Ghost,"),
            ("ma le tumau", "and enduring"),
            ("e oo i le iuga,", "to the end,"),
            ("e tau atu", "lead"),
            ("i le faaolataga.", "to salvation."),
            ("E tusa o le", "about"),
            ("401–421", "401–421"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|9": {
        "en": "Both the Nephites and the Lamanites are depraved and "
              "degenerate—They torture and murder each other—Mormon prays that "
              "grace and goodness may rest upon Moroni forever. About A.D. 401.",
        "sm": "O uiga leaga ma le mataga o sa Nifaē ma sa Lamanā—Ua latou "
              "faasaua ma fasioti le tasi i le isi—Ua tatalo Mamona ia oo mai le "
              "alofa tunoa ma le agalelei i luga o Moronae e faavavau. E tusa o le "
              "401 T.A.",
        "cells": [
            ("O uiga leaga", "depraved"),
            ("ma le mataga", "and degenerate"),
            ("o sa Nifaē", "Both the Nephites"),
            ("ma sa Lamanā—", "and the Lamanites—"),
            ("Ua latou faasaua ma fasioti", "They torture and murder"),
            ("le tasi i le isi—", "each other—"),
            ("Ua tatalo Mamona", "Mormon prays"),
            ("ia oo mai", "that may rest"),
            ("le alofa tunoa", "grace"),
            ("ma le agalelei", "and goodness"),
            ("i luga o Moronae", "upon Moroni"),
            ("e faavavau.", "forever."),
            ("E tusa o le", "about"),
            ("401", "401"),
            ("T.A.", "A.D."),
        ],
    },
    "moroni|10": {
        "en": "A testimony of the Book of Mormon comes by the power of the Holy "
              "Ghost—The gifts of the Spirit are dispensed to the faithful—"
              "Spiritual gifts always accompany faith—Moroni's words speak from "
              "the dust—Come unto Christ, be perfected in Him, and sanctify your "
              "souls. About A.D. 421.",
        "sm": "O se molimau o le Tusi a Mamona e ala mai le mana o le Agaga "
              "Paia—O meaalofa a le Agaga e tuuina mai i ē ua faamaoni—O meaalofa "
              "faaleagaga e soa faatasi ma le faatuatua i taimi uma—Ua tautala "
              "mai le efuefu i upu a Moronae—O mai ia Keriso, ia faaatoatoaina ia "
              "te Ia, ma faapaia o outou agaga. E tusa o le 421 T.A.",
        "cells": [
            ("O se molimau", "A testimony"),
            ("o le Tusi a Mamona", "of the Book of Mormon"),
            ("e ala mai le mana", "comes by the power"),
            ("o le Agaga Paia—", "of the Holy Ghost—"),
            ("O meaalofa a le Agaga", "The gifts of the Spirit"),
            ("e tuuina mai", "are dispensed"),
            ("i ē ua faamaoni—", "to the faithful—"),
            ("O meaalofa faaleagaga", "Spiritual gifts"),
            ("e soa faatasi ma le faatuatua", "accompany faith"),
            ("i taimi uma—", "always—"),
            ("Ua tautala mai", "speak"),
            ("le efuefu", "from the dust"),
            ("i upu a Moronae—", "Moroni's words—"),
            ("O mai ia Keriso,", "Come unto Christ,"),
            ("ia faaatoatoaina ia te Ia,", "be perfected in Him,"),
            ("ma faapaia o outou agaga.", "and sanctify your souls."),
            ("E tusa o le", "about"),
            ("421", "421"),
            ("T.A.", "A.D."),
        ],
    },
}


def cells_to_words(cells: list[tuple[str, str]]) -> list[dict]:
    """Expand (samoan_phrase, gloss) cells into a `·`-marked word array."""
    words: list[dict] = []
    for sm_phrase, gloss in cells:
        tokens = sm_phrase.split(" ")
        for t in tokens[:-1]:
            words.append({"sm": t, "en": "·"})
        words.append({"sm": tokens[-1], "en": gloss})
    return words


def emdash_split(text: str) -> list[str]:
    """Tokenize like the app will: split on spaces, and split X—Y into X— , Y."""
    spaced = re.sub(EMDASH + r"(?=\S)", EMDASH + " ", text)
    return spaced.split()


def main() -> None:
    out = {"version": 1, "headings": {}}
    for key, entry in HEADINGS.items():
        words = cells_to_words(entry["cells"])
        recon = [w["sm"] for w in words]
        expected = emdash_split(entry["sm"])
        if recon != expected:
            # Show the first divergence to make fixing easy.
            for i, (a, b) in enumerate(zip(recon, expected)):
                if a != b:
                    raise SystemExit(
                        f"[{key}] token {i} mismatch: cells={a!r} source={b!r}"
                    )
            raise SystemExit(
                f"[{key}] length mismatch: cells={len(recon)} source={len(expected)}"
            )
        out["headings"][key] = {
            "en": entry["en"],
            "sm": entry["sm"],
            "words": words,
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out['headings'])} headings -> {OUT}")


if __name__ == "__main__":
    main()
