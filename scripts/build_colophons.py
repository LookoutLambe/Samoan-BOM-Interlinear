#!/usr/bin/env python3
"""
Build `bom_colophons.json` — the record-keeper colophons/prefaces that precede
certain chapters (e.g. "O poloaiga a Alema i lona atalii o Helamana. E aofia ai
mataupu 36 ma le 37."). These are displayed ABOVE the chapter summary on the
chapter where the colophon appears in the printed edition.

Same pipeline as build_headings.py: keyed "bookId|chapter"; each entry carries
verbatim English, verbatim Samoan, and an interlinear `words` array built from
hand `cells:[(sm_phrase, en_gloss)]`. Colophons have no date footer.

Run:  python3 scripts/build_colophons.py
Out:  O le Tusi a Mamona Interlinear/Resources/bom_colophons.json
"""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "O le Tusi a Mamona Interlinear", "Resources", "bom_colophons.json")

EMDASH = "—"

COLOPHONS: dict[str, dict] = {
    "mosiah|9": {
        "en": "The Record of Zeniff—An account of his people, from the time "
              "they left the land of Zarahemla until the time they were "
              "delivered out of the hands of the Lamanites.",
        "sm": "O le Talafaamaumau a Senifa—O se tala i lona nuu, mai le taimi na "
              "latou tuua ai le laueleele o Sara'emila seia oo mai i le taimi na "
              "laveaiina ai i latou mai lima o sa Lamanā.",
        "cells": [
            ("O le Talafaamaumau a Senifa—", "The Record of Zeniff—"),
            ("O se tala", "An account"),
            ("i lona nuu,", "of his people,"),
            ("mai le taimi", "from the time"),
            ("na latou tuua ai", "they left"),
            ("le laueleele o Sara'emila", "the land of Zarahemla"),
            ("seia oo mai", "until"),
            ("i le taimi", "the time"),
            ("na laveaiina ai i latou", "they were delivered"),
            ("mai lima o sa Lamanā.", "out of the hands of the Lamanites."),
        ],
    },
    "mosiah|23": {
        "en": "An account of Alma and the people of the Lord, who were driven "
              "into the wilderness by the people of King Noah. Comprising "
              "chapters 23 and 24.",
        "sm": "O se tala ia Alema ma tagata o le Alii, o ē na tutuli i le vao e "
              "le nuu o le Tupu o Noa. E aofia ai le mataupu 23 ma le 24.",
        "cells": [
            ("O se tala ia Alema", "An account of Alma"),
            ("ma tagata o le Alii,", "and the people of the Lord,"),
            ("o ē na tutuli", "who were driven"),
            ("i le vao", "into the wilderness"),
            ("e le nuu", "by the people"),
            ("o le Tupu o Noa.", "of King Noah."),
            ("E aofia ai", "Comprising"),
            ("le mataupu 23 ma le 24.", "chapters 23 and 24."),
        ],
    },
    "alma|9": {
        "en": "The words of Alma, and also the words of Amulek, which were "
              "declared unto the people who were in the land of Ammonihah. And "
              "also they are cast into prison, and delivered by the miraculous "
              "power of God which was in them, according to the record of Alma. "
              "Comprising chapters 9 through 14.",
        "sm": "O upu a Alema, ma upu foi a Amoleka, ia sa alaga atu i tagata o e "
              "sa i le laueleele o Amonaea. Ma ua lafoina foi i la'ua i le "
              "falepuipui, ma lavea'iina e le mana faavavega o le Atua lea sa ia "
              "te i la'ua, e tusa ma le talafaamaumau a Alema. E aofia ai le "
              "mataupu 9 e oo atu i le 14.",
        "cells": [
            ("O upu a Alema,", "The words of Alma,"),
            ("ma upu foi a Amoleka,", "and also the words of Amulek,"),
            ("ia sa alaga atu", "which were declared"),
            ("i tagata", "unto the people"),
            ("o e sa", "who were"),
            ("i le laueleele o Amonaea.", "in the land of Ammonihah."),
            ("Ma ua lafoina foi", "And also they are cast"),
            ("i la'ua", "the two of them"),
            ("i le falepuipui,", "into prison,"),
            ("ma lavea'iina", "and delivered"),
            ("e le mana faavavega", "by the miraculous power"),
            ("o le Atua", "of God"),
            ("lea sa", "which was"),
            ("ia te i la'ua,", "in them,"),
            ("e tusa ma", "according to"),
            ("le talafaamaumau a Alema.", "the record of Alma."),
            ("E aofia ai", "Comprising"),
            ("le mataupu 9", "chapters 9"),
            ("e oo atu", "through"),
            ("i le 14.", "to 14."),
        ],
    },
    "alma|17": {
        "en": "An account of the sons of Mosiah, who rejected their rights to "
              "the kingdom for the word of God, and went up to the land of "
              "Nephi to preach to the Lamanites; their sufferings and "
              "deliverance—according to the record of Alma. Comprising chapters "
              "17 through 27.",
        "sm": "O se tala i atalii o Mosaea, o e sa teena a latou aiā i le malo "
              "mo le afioga a le Atua, ma o a'e i le laueleele o Nifae e talai "
              "atu ia sa Lamanā; o o latou mafatiaga ma laveaiina—e tusa ma le "
              "talafaamaumau a Alema. E aofia ai le mataupu 17 e oo atu i le 27.",
        "cells": [
            ("O se tala", "An account"),
            ("i atalii o Mosaea,", "of the sons of Mosiah,"),
            ("o e sa teena", "who rejected"),
            ("a latou aiā", "their rights"),
            ("i le malo", "to the kingdom"),
            ("mo le afioga", "for the word"),
            ("a le Atua,", "of God,"),
            ("ma o a'e", "and went up"),
            ("i le laueleele o Nifae", "to the land of Nephi"),
            ("e talai atu", "to preach"),
            ("ia sa Lamanā;", "to the Lamanites;"),
            ("o o latou mafatiaga", "their sufferings"),
            ("ma laveaiina—", "and deliverance—"),
            ("e tusa ma", "according to"),
            ("le talafaamaumau a Alema.", "the record of Alma."),
            ("E aofia ai", "Comprising"),
            ("le mataupu 17", "chapters 17"),
            ("e oo atu", "through"),
            ("i le 27.", "to 27."),
        ],
    },
    "alma|21": {
        "en": "An account of the preaching of Aaron, and Muloki, and their "
              "brethren, to the Lamanites. Comprising chapters 21 through 25.",
        "sm": "O se tala o le tala'iga a Arona, ma Muloki, ma o la'ua uso, i sa "
              "Lamanā. E aofia ai le mataupu 21 e oo atu i le 25.",
        "cells": [
            ("O se tala", "An account"),
            ("o le tala'iga a Arona,", "of the preaching of Aaron,"),
            ("ma Muloki,", "and Muloki,"),
            ("ma o la'ua uso,", "and their brethren,"),
            ("i sa Lamanā.", "to the Lamanites."),
            ("E aofia ai", "Comprising"),
            ("le mataupu 21", "chapters 21"),
            ("e oo atu", "through"),
            ("i le 25.", "to 25."),
        ],
    },
    "alma|36": {
        "en": "The commandments of Alma to his son Helaman. Comprising chapters "
              "36 and 37.",
        "sm": "O poloaiga a Alema i lona atalii o Helamana. E aofia ai mataupu "
              "36 ma le 37.",
        "cells": [
            ("O poloaiga a Alema", "The commandments of Alma"),
            ("i lona atalii o Helamana.", "to his son Helaman."),
            ("E aofia ai", "Comprising"),
            ("mataupu 36 ma le 37.", "chapters 36 and 37."),
        ],
    },
    "alma|38": {
        "en": "The commandments of Alma to his son Shiblon. Comprising chapter "
              "38.",
        "sm": "O poloaiga a Alema i lona atalii o Sepulona. E aofia ai le "
              "mataupu 38.",
        "cells": [
            ("O poloaiga a Alema", "The commandments of Alma"),
            ("i lona atalii o Sepulona.", "to his son Shiblon."),
            ("E aofia ai", "Comprising"),
            ("le mataupu 38.", "chapter 38."),
        ],
    },
    "alma|39": {
        "en": "The commandments of Alma to his son Corianton. Comprising "
              "chapters 39 through 42.",
        "sm": "O poloaiga a Alema i lona atalii o Korianetona. E aofia ai "
              "mataupu 39 e oo atu i le 42.",
        "cells": [
            ("O poloaiga a Alema", "The commandments of Alma"),
            ("i lona atalii o Korianetona.", "to his son Corianton."),
            ("E aofia ai", "Comprising"),
            ("mataupu 39", "chapters 39"),
            ("e oo atu", "through"),
            ("i le 42.", "to 42."),
        ],
    },
    "alma|45": {
        "en": "An account of the people of Nephi, and their wars and "
              "dissensions, in the days of Helaman, according to the record of "
              "Helaman, which he kept in his days. Comprising chapters 45 "
              "through 62.",
        "sm": "O le tala i le nuu o Nifae, ma a latou taua ma a latou "
              "faatuiesega, i aso o Helamana, e tusa ai ma le talafaamaumau a "
              "Helamana, lea sa ia tausia i ona aso. E aofia ai mataupu 45 e oo "
              "atu i le 62.",
        "cells": [
            ("O le tala", "An account"),
            ("i le nuu o Nifae,", "of the people of Nephi,"),
            ("ma a latou taua", "and their wars"),
            ("ma a latou faatuiesega,", "and their dissensions,"),
            ("i aso o Helamana,", "in the days of Helaman,"),
            ("e tusa ai ma", "according to"),
            ("le talafaamaumau a Helamana,", "the record of Helaman,"),
            ("lea sa ia tausia", "which he kept"),
            ("i ona aso.", "in his days."),
            ("E aofia ai", "Comprising"),
            ("mataupu 45", "chapters 45"),
            ("e oo atu", "through"),
            ("i le 62.", "to 62."),
        ],
    },
    "helaman|1": {
        "en": "An account of the Nephites. Their wars and contentions, and "
              "their dissensions. And also the prophecies of many holy "
              "prophets, before the coming of Christ, according to the records "
              "of Helaman, who was the son of Helaman, and also according to "
              "the records of his sons, even down to the coming of Christ. And "
              "also many of the Lamanites are converted. An account of their "
              "conversion. An account of the righteousness of the Lamanites, "
              "and the wickedness and abominations of the Nephites, according "
              "to the record of Helaman and his sons, even down to the coming "
              "of Christ, which is called the book of Helaman, and so forth.",
        "sm": "O se tala ia sa Nifaē. O a latou taua ma finauga, ma a latou "
              "faatuiesega. Ma valoaga foi a perofeta paia e toatele, ae lei "
              "afio mai Keriso, e tusa ma talafaamaumau a Helamana, o le atalii "
              "ia o Helamana, ma e tusa foi ma talafaamaumau a ona atalii, seia "
              "oo mai lava i le afio mai o Keriso. Ma e toatele foi sa Lamanā na "
              "liliu mai. O se tala i lo latou liliu mai. O se tala i le "
              "amiotonu o sa Lamanā ma le amioleaga ma mea inosia a sa Nifaē, e "
              "tusa ai ma le talafaamaumau a Helamana ma ona atalii, e oo mai "
              "lava i le afio mai o Keriso, lea ua ta'ua o le tusi a Helamana, "
              "ma isi mea.",
        "cells": [
            ("O se tala", "An account"),
            ("ia sa Nifaē.", "of the Nephites."),
            ("O a latou taua", "Their wars"),
            ("ma finauga,", "and contentions,"),
            ("ma a latou faatuiesega.", "and their dissensions."),
            ("Ma valoaga foi", "And also the prophecies"),
            ("a perofeta paia e toatele,", "of many holy prophets,"),
            ("ae lei afio mai Keriso,", "before Christ came,"),
            ("e tusa ma", "according to"),
            ("talafaamaumau a Helamana,", "the records of Helaman,"),
            ("o le atalii ia", "who was the son"),
            ("o Helamana,", "of Helaman,"),
            ("ma e tusa foi ma", "and also according to"),
            ("talafaamaumau a ona atalii,", "the records of his sons,"),
            ("seia oo mai lava", "even down"),
            ("i le afio mai", "to the coming"),
            ("o Keriso.", "of Christ."),
            ("Ma e toatele foi", "And also many"),
            ("sa Lamanā", "of the Lamanites"),
            ("na liliu mai.", "are converted."),
            ("O se tala", "An account"),
            ("i lo latou liliu mai.", "of their conversion."),
            ("O se tala", "An account"),
            ("i le amiotonu", "of the righteousness"),
            ("o sa Lamanā", "of the Lamanites"),
            ("ma le amioleaga", "and the wickedness"),
            ("ma mea inosia", "and abominations"),
            ("a sa Nifaē,", "of the Nephites,"),
            ("e tusa ai ma", "according to"),
            ("le talafaamaumau a Helamana", "the record of Helaman"),
            ("ma ona atalii,", "and his sons,"),
            ("e oo mai lava", "even down"),
            ("i le afio mai", "to the coming"),
            ("o Keriso,", "of Christ,"),
            ("lea ua ta'ua", "which is called"),
            ("o le tusi a Helamana,", "the book of Helaman,"),
            ("ma isi mea.", "and so forth."),
        ],
    },
    "1nephi|1": {
        "en": "An account of Lehi and his wife Sariah, and his four sons, being "
              "called, (beginning at the eldest) Laman, Lemuel, Sam, and Nephi. "
              "The Lord warns Lehi to depart out of the land of Jerusalem, "
              "because he prophesieth unto the people concerning their iniquity "
              "and they seek to destroy his life. He taketh three days' journey "
              "into the wilderness with his family. Nephi taketh his brethren "
              "and returneth to the land of Jerusalem after the record of the "
              "Jews. The account of their sufferings. They take the daughters "
              "of Ishmael to wife. They take their families and depart into the "
              "wilderness. Their sufferings and afflictions in the wilderness. "
              "The course of their travels. They come to the large waters. "
              "Nephi's brethren rebel against him. He confoundeth them, and "
              "buildeth a ship. They call the name of the place Bountiful. They "
              "cross the large waters into the promised land, and so forth. "
              "This is according to the account of Nephi; or in other words, I, "
              "Nephi, wrote this record.",
        "sm": "O se tala ia Liae ma lana ava o Sarai, ma ona atalii e toafa, e "
              "igoa (e amata mai i le ulumatua) ia Lamana, Lemuelu, Sama, ma "
              "Nifae. Ua lapataia Liae e le Alii ia alu ese atu mai le laueleele "
              "o Ierusalema, ona sa vavalo atu o ia i tagata e uiga i lo latou "
              "amioletonu ma ua latou saili ai e faaumatia lona ola. Ua malaga "
              "atu o ia i le vao i aso e tolu faatasi ma lona aiga. Ua ave e "
              "Nifae ona uso ma foi atu i le laueleele o Ierusalema ina ia maua "
              "mai le talafaamaumau o tagata Iutaia. O le tala i o latou "
              "mafatiaga. Ua latou ave afafine o Isamaeli ma faiavā i ai. Ua "
              "latou ave o latou aiga ma o ese atu i le vao. O o latou mafatiaga "
              "ma puapuaga i le vao. O le ala na ui ai la latou malaga. Ua latou "
              "tau atu i vai tetele. Ua fouvale uso o Nifae ia te ia. Ua ia "
              "faafememeaiina i laua, ma fausia se vaa. Ua latou faaigoaina le "
              "nofoaga o Nuumau. Ua latou sopo atu i vai tetele i le laueleele "
              "na folafolaina, ma isi mea. O lenei ua tusa ai ma le tala a "
              "Nifae; po o i ni isi upu, o a'u, o Nifae, na tusia lenei tala.",
        "cells": [
            ("O se tala ia Liae", "An account of Lehi"),
            ("ma lana ava o Sarai,", "and his wife Sariah,"),
            ("ma ona atalii e toafa,", "and his four sons,"),
            ("e igoa", "being called"),
            ("(e amata mai i le ulumatua)", "(beginning at the eldest)"),
            ("ia Lamana, Lemuelu,", "Laman, Lemuel,"),
            ("Sama, ma Nifae.", "Sam, and Nephi."),
            ("Ua lapataia Liae e le Alii", "The Lord warns Lehi"),
            ("ia alu ese atu", "to depart"),
            ("mai le laueleele o Ierusalema,", "out of the land of Jerusalem,"),
            ("ona sa vavalo atu o ia", "because he prophesied"),
            ("i tagata", "unto the people"),
            ("e uiga i", "concerning"),
            ("lo latou amioletonu", "their iniquity"),
            ("ma ua latou saili ai", "and they sought"),
            ("e faaumatia lona ola.", "to destroy his life."),
            ("Ua malaga atu o ia", "He journeys"),
            ("i le vao", "into the wilderness"),
            ("i aso e tolu", "for three days"),
            ("faatasi ma lona aiga.", "with his family."),
            ("Ua ave e Nifae", "Nephi takes"),
            ("ona uso", "his brethren"),
            ("ma foi atu", "and returns"),
            ("i le laueleele o Ierusalema", "to the land of Jerusalem"),
            ("ina ia maua mai", "to obtain"),
            ("le talafaamaumau o tagata Iutaia.", "the record of the Jews."),
            ("O le tala", "The account"),
            ("i o latou mafatiaga.", "of their sufferings."),
            ("Ua latou ave", "They take"),
            ("afafine o Isamaeli", "the daughters of Ishmael"),
            ("ma faiavā i ai.", "to wife."),
            ("Ua latou ave", "They take"),
            ("o latou aiga", "their families"),
            ("ma o ese atu", "and depart"),
            ("i le vao.", "into the wilderness."),
            ("O o latou mafatiaga", "Their sufferings"),
            ("ma puapuaga i le vao.", "and afflictions in the wilderness."),
            ("O le ala", "The course"),
            ("na ui ai", "that went"),
            ("la latou malaga.", "of their travels."),
            ("Ua latou tau atu", "They come"),
            ("i vai tetele.", "to the large waters."),
            ("Ua fouvale uso o Nifae", "Nephi's brethren rebel"),
            ("ia te ia.", "against him."),
            ("Ua ia faafememeaiina i laua,", "He confounds them,"),
            ("ma fausia se vaa.", "and builds a ship."),
            ("Ua latou faaigoaina", "They name"),
            ("le nofoaga o Nuumau.", "the place Bountiful."),
            ("Ua latou sopo atu", "They cross"),
            ("i vai tetele", "the large waters"),
            ("i le laueleele na folafolaina,", "into the promised land,"),
            ("ma isi mea.", "and so forth."),
            ("O lenei ua tusa ai ma", "This is according to"),
            ("le tala a Nifae;", "the account of Nephi;"),
            ("po o i", "or in"),
            ("ni isi upu,", "other words,"),
            ("o a'u, o Nifae,", "I, Nephi,"),
            ("na tusia lenei tala.", "wrote this record."),
        ],
    },
    "2nephi|1": {
        "en": "An account of the death of Lehi. Nephi's brethren rebel against "
              "him. He is warned of the Lord to depart into the wilderness. His "
              "travels in the wilderness, and so forth.",
        "sm": "O se tala i le maliu o Liae. Ua fouvale uso o Nifae ia te ia. Ua "
              "lapataia Nifae e le Alii ia alu ese atu i le vao. O ana malaga i "
              "le vao, ma isi mea faapena.",
        "cells": [
            ("O se tala", "An account"),
            ("i le maliu o Liae.", "of the death of Lehi."),
            ("Ua fouvale uso o Nifae", "Nephi's brethren rebel"),
            ("ia te ia.", "against him."),
            ("Ua lapataia Nifae e le Alii", "Nephi is warned of the Lord"),
            ("ia alu ese atu", "to depart"),
            ("i le vao.", "into the wilderness."),
            ("O ana malaga", "His travels"),
            ("i le vao,", "in the wilderness,"),
            ("ma isi mea faapena.", "and so forth."),
        ],
    },
    "jacob|1": {
        "en": "The words of his preaching unto his brethren. He confoundeth a "
              "man who seeketh to overthrow the doctrine of Christ. A few words "
              "concerning the history of the people of Nephi.",
        "sm": "O upu o lana lauga i ona uso. Ua faafememea'iina e ia se alii na "
              "saili e lepeti le aoaoga faavae a Keriso. O nai upu itiiti e uiga "
              "i le talafaasolopito o le nuu o Nifae.",
        "cells": [
            ("O upu o lana lauga", "The words of his preaching"),
            ("i ona uso.", "unto his brethren."),
            ("Ua faafememea'iina e ia", "He confounds"),
            ("se alii", "a man"),
            ("na saili e lepeti", "who sought to overthrow"),
            ("le aoaoga faavae a Keriso.", "the doctrine of Christ."),
            ("O nai upu itiiti", "A few words"),
            ("e uiga i le talafaasolopito", "concerning the history"),
            ("o le nuu o Nifae.", "of the people of Nephi."),
        ],
    },
    "alma|1": {
        "en": "The account of Alma, who was the son of Alma, the first and "
              "chief judge over the people of Nephi, and also the high priest "
              "over the Church. An account of the reign of the judges, and the "
              "wars and contentions among the people. And also an account of a "
              "war between the Nephites and the Lamanites, according to the "
              "record of Alma, the first and chief judge.",
        "sm": "O le tala a Alema, o ia o le atalii o Alema, le uluai faamasino "
              "ma le faamasino sili i le nuu o Nifae, ma o le faitaulaga sili "
              "foi i le Ekalesia. O se tala o le nofoaiga a faamasino, ma taua "
              "ma finauga i totonu o le nuu. Ma o se tala foi o se taua i le va "
              "o sa Nifaē ma sa Lamanā, e tusa ma le talafaamaumau a Alema, o le "
              "uluai faamasino ma le faamasino sili.",
        "cells": [
            ("O le tala a Alema,", "The account of Alma,"),
            ("o ia o le atalii", "who was the son"),
            ("o Alema,", "of Alma,"),
            ("le uluai faamasino", "the first judge"),
            ("ma le faamasino sili", "and chief judge"),
            ("i le nuu o Nifae,", "over the people of Nephi,"),
            ("ma o", "and"),
            ("le faitaulaga sili foi", "also the high priest"),
            ("i le Ekalesia.", "over the Church."),
            ("O se tala", "An account"),
            ("o le nofoaiga a faamasino,", "of the reign of the judges,"),
            ("ma taua ma finauga", "and the wars and contentions"),
            ("i totonu o le nuu.", "among the people."),
            ("Ma o se tala foi", "And also an account"),
            ("o se taua", "of a war"),
            ("i le va", "between"),
            ("o sa Nifaē", "the Nephites"),
            ("ma sa Lamanā,", "and the Lamanites,"),
            ("e tusa ma", "according to"),
            ("le talafaamaumau a Alema,", "the record of Alma,"),
            ("o le uluai faamasino", "the first judge"),
            ("ma le faamasino sili.", "and chief judge."),
        ],
    },
    "4nephi|1": {
        "en": "An account of the people of Nephi, according to his record.",
        "sm": "O se tala o le nuu o Nifae, e tusa ma lana talafaamaumau.",
        "cells": [
            ("O se tala", "An account"),
            ("o le nuu o Nifae,", "of the people of Nephi,"),
            ("e tusa ma lana talafaamaumau.", "according to his record."),
        ],
    },
    "ether|1": {
        "en": "The record of the Jaredites, taken from the twenty-four plates "
              "found by the people of Limhi in the days of King Mosiah.",
        "sm": "O le talafaamaumau o sa Iaretō, na sii mai papatusi e luasefulu "
              "ma le fa ia na maua e tagata o Limae i aso le Tupu o Mosaea.",
        "cells": [
            ("O le talafaamaumau", "The record"),
            ("o sa Iaretō,", "of the Jaredites,"),
            ("na sii mai papatusi", "taken from the plates"),
            ("e luasefulu ma le fa", "twenty-four"),
            ("ia na maua", "found"),
            ("e tagata o Limae", "by the people of Limhi"),
            ("i aso", "in the days"),
            ("le Tupu o Mosaea.", "of King Mosiah."),
        ],
    },
    "3nephi|1": {
        "en": "The Book of Nephi, the son of Nephi, who was the son of Helaman. "
              "And Helaman was the son of Helaman, who was the son of Alma, who "
              "was the son of Alma, being a descendant of Nephi who was the son "
              "of Lehi, who came out of Jerusalem in the first year of the "
              "reign of Zedekiah, the king of Judah.",
        "sm": "O le Tusi a Nifae, o le atalii o Nifae, o le atalii ia o "
              "Helamana. Ma o Helamana o le atalii o Helamana, o le atalii ia o "
              "Alema, o le atalii ia o Alema, o se e tupuga mai ia Nifae o le "
              "atalii o Liae, o le na alu a'e mai Ierusalema i le tausaga "
              "muamua o le nofoaiga a Setekaia, le tupu o Iuta.",
        "cells": [
            ("O le Tusi a Nifae,", "The Book of Nephi,"),
            ("o le atalii o Nifae,", "the son of Nephi,"),
            ("o le atalii ia", "who was the son"),
            ("o Helamana.", "of Helaman."),
            ("Ma o Helamana", "And Helaman"),
            ("o le atalii o Helamana,", "was the son of Helaman,"),
            ("o le atalii ia", "who was the son"),
            ("o Alema,", "of Alma,"),
            ("o le atalii ia", "who was the son"),
            ("o Alema,", "of Alma,"),
            ("o se e tupuga mai", "being a descendant"),
            ("ia Nifae", "of Nephi"),
            ("o le atalii o Liae,", "who was the son of Lehi,"),
            ("o le na alu a'e", "who came out"),
            ("mai Ierusalema", "of Jerusalem"),
            ("i le tausaga muamua", "in the first year"),
            ("o le nofoaiga a Setekaia,", "of the reign of Zedekiah,"),
            ("le tupu o Iuta.", "the king of Judah."),
        ],
    },
    "helaman|7": {
        "en": "The prophecy of Nephi, the son of Helaman—God threatens the "
              "people of Nephi that he will visit them in his anger, to their "
              "utter destruction except they repent of their wickedness. God "
              "smiteth the people of Nephi with pestilence; they repent and "
              "turn unto him. Samuel, a Lamanite, prophesies unto the Nephites. "
              "Comprising chapters 7 through 16.",
        "sm": "O le valoaga a Nifae, le atalii o Helamana—Ua faamata'uina e le "
              "Atua le nuu o Nifae o le a ia asiasi mai ia te i latou i lona "
              "toasa, i le faaumatiaina atoa o i latou, vagana ai ua latou "
              "salamo ia latou amioleaga. Ua taia e le Atua le nuu o Nifae i le "
              "faama'i; ua latou salamo ma liliu mai ia te ia. O Samuelu, o se "
              "sa Lamanā, ua vavalo atu i tagata sa Nifaē. E aofia ai mataupu 7 "
              "e oo atu i le 16.",
        "cells": [
            ("O le valoaga a Nifae,", "The prophecy of Nephi,"),
            ("le atalii o Helamana—", "the son of Helaman—"),
            ("Ua faamata'uina e le Atua", "God threatens"),
            ("le nuu o Nifae", "the people of Nephi"),
            ("o le a ia asiasi mai", "that he will visit"),
            ("ia te i latou", "them"),
            ("i lona toasa,", "in his anger,"),
            ("i le faaumatiaina atoa", "to the utter destruction"),
            ("o i latou,", "of them,"),
            ("vagana ai ua latou salamo", "except they repent"),
            ("ia latou amioleaga.", "of their wickedness."),
            ("Ua taia e le Atua", "God smites"),
            ("le nuu o Nifae", "the people of Nephi"),
            ("i le faama'i;", "with pestilence;"),
            ("ua latou salamo", "they repent"),
            ("ma liliu mai ia te ia.", "and turn unto him."),
            ("O Samuelu,", "Samuel,"),
            ("o se sa Lamanā,", "a Lamanite,"),
            ("ua vavalo atu", "prophesies"),
            ("i tagata sa Nifaē.", "unto the Nephites."),
            ("E aofia ai", "Comprising"),
            ("mataupu 7", "chapters 7"),
            ("e oo atu", "through"),
            ("i le 16.", "to 16."),
        ],
    },
    "helaman|13": {
        "en": "The prophecy of Samuel, the Lamanite, to the Nephites. "
              "Comprising chapters 13 through 15.",
        "sm": "O le valoaga a Samuelu, le sa Lamanā, ia sa Nifaē. E aofia ai "
              "mataupu 13 e oo atu i le 15.",
        "cells": [
            ("O le valoaga a Samuelu,", "The prophecy of Samuel,"),
            ("le sa Lamanā,", "the Lamanite,"),
            ("ia sa Nifaē.", "to the Nephites."),
            ("E aofia ai", "Comprising"),
            ("mataupu 13", "chapters 13"),
            ("e oo atu", "through"),
            ("i le 15.", "to 15."),
        ],
    },
    "3nephi|11": {
        "en": "Jesus Christ did show himself unto the people of Nephi, as the "
              "multitude were gathered together in the land Bountiful, and did "
              "minister unto them; and on this wise did he show himself unto "
              "them. Comprising chapters 11 through 26.",
        "sm": "Na faaali mai e Iesu Keriso o ia lava i le nuu o Nifae, ao "
              "faapotopoto faatasi le motu o tagata i le laueleele o Nuumau, ma "
              "sa ia auauna atu ia te i latou; ma sa faapenei ona ia faaali mai "
              "o ia lava ia te i latou. E aofia ai mataupu 11 e oo atu i le 26.",
        "cells": [
            ("Na faaali mai e Iesu Keriso", "Jesus Christ did show"),
            ("o ia lava", "himself"),
            ("i le nuu o Nifae,", "unto the people of Nephi,"),
            ("ao faapotopoto faatasi", "as gathered together"),
            ("le motu o tagata", "the multitude"),
            ("i le laueleele o Nuumau,", "in the land Bountiful,"),
            ("ma sa ia auauna atu", "and did minister"),
            ("ia te i latou;", "unto them;"),
            ("ma sa faapenei", "and on this wise"),
            ("ona ia faaali mai", "did he show"),
            ("o ia lava", "himself"),
            ("ia te i latou.", "unto them."),
            ("E aofia ai", "Comprising"),
            ("mataupu 11", "chapters 11"),
            ("e oo atu", "through"),
            ("i le 26.", "to 26."),
        ],
    },
    "moroni|9": {
        "en": "The second epistle of Mormon to his son Moroni. Comprising "
              "chapter 9.",
        "sm": "O le tusi lona lua a Mamona i lona atalii o Moronae. Ua aofia ai "
              "le mataupu lona 9.",
        "cells": [
            ("O le tusi lona lua", "The second epistle"),
            ("a Mamona", "of Mormon"),
            ("i lona atalii o Moronae.", "to his son Moroni."),
            ("Ua aofia ai", "Comprising"),
            ("le mataupu lona 9.", "chapter 9."),
        ],
    },
}


def cells_to_words(cells: list[tuple[str, str]]) -> list[dict]:
    words: list[dict] = []
    for sm_phrase, gloss in cells:
        tokens = sm_phrase.split(" ")
        for t in tokens[:-1]:
            words.append({"sm": t, "en": "·"})
        words.append({"sm": tokens[-1], "en": gloss})
    return words


def emdash_split(text: str) -> list[str]:
    spaced = re.sub(EMDASH + r"(?=\S)", EMDASH + " ", text)
    return spaced.split()


def main() -> None:
    out = {"version": 1, "colophons": {}}
    for key, entry in COLOPHONS.items():
        words = cells_to_words(entry["cells"])
        recon = [w["sm"] for w in words]
        expected = emdash_split(entry["sm"])
        if recon != expected:
            for i, (a, b) in enumerate(zip(recon, expected)):
                if a != b:
                    raise SystemExit(f"[{key}] token {i} mismatch: cells={a!r} source={b!r}")
            raise SystemExit(
                f"[{key}] length mismatch: cells={len(recon)} source={len(expected)}"
            )
        out["colophons"][key] = {"en": entry["en"], "sm": entry["sm"], "words": words}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out['colophons'])} colophons -> {OUT}")


if __name__ == "__main__":
    main()
