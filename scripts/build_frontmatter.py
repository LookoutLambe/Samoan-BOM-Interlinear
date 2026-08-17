#!/usr/bin/env python3
"""
Build `bom_frontmatter.json` — the interlinear Book of Mormon front-matter
sections (Title Page, Introduction, the Witness testimonies, Testimony of
Joseph Smith, A Brief Explanation). Mirrors the chapter-heading pipeline:
each section holds hand-authored `cells:[(sm_phrase, en_gloss)]` that expand
to a `·`-marked word array, and a validation pass asserts the reconstructed
token stream equals the whitespace/em-dash-split source so no Samoan word can
be dropped or reordered. Sections without `cells` render as bilingual prose.
"""

import json
import os
import re

OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "O le Tusi a Mamona Interlinear",
    "Resources",
    "bom_frontmatter.json",
)

EMDASH = "—"  # — (clause separator; split for tokenizing)

# The Samoan source mixes several apostrophe glyphs for the glottal stop
# (U+02BC modifier letter, U+0027 straight, U+2018 left single). Fold them all
# to U+2019 so hand-authored cells never have to match the exact variant.
_APOS = {"ʼ": "’", "'": "’", "‘": "’", "`": "’"}


def norm(s: str) -> str:
    for k, v in _APOS.items():
        s = s.replace(k, v)
    return s

# ---------------------------------------------------------------------------
# Title Page
# ---------------------------------------------------------------------------

TITLE_EN = (
    "The Book of Mormon: An Account Written by the Hand of Mormon upon Plates "
    "Taken from the Plates of Nephi"
    "\n\n"
    "Wherefore, it is an abridgment of the record of the people of Nephi, and "
    "also of the Lamanites—Written to the Lamanites, who are a remnant of the "
    "house of Israel; and also to Jew and Gentile—Written by way of "
    "commandment, and also by the spirit of prophecy and of revelation—Written "
    "and sealed up, and hid up unto the Lord, that they might not be "
    "destroyed—To come forth by the gift and power of God unto the "
    "interpretation thereof—Sealed by the hand of Moroni, and hid up unto the "
    "Lord, to come forth in due time by way of the Gentile—The interpretation "
    "thereof by the gift of God."
    "\n\n"
    "An abridgment taken from the Book of Ether also, which is a record of the "
    "people of Jared, who were scattered at the time the Lord confounded the "
    "language of the people, when they were building a tower to get to "
    "heaven—Which is to show unto the remnant of the house of Israel what great "
    "things the Lord hath done for their fathers; and that they may know the "
    "covenants of the Lord, that they are not cast off forever—And also to the "
    "convincing of the Jew and Gentile that Jesus is the Christ, the Eternal "
    "God, manifesting himself unto all nations—And now, if there are faults "
    "they are the mistakes of men; wherefore, condemn not the things of God, "
    "that ye may be found spotless at the judgment-seat of Christ."
    "\n\n"
    "Translated by Joseph Smith, Jun."
)

TITLE_SM = (
    "O Le Tusi a Mamona: O Se Tala na Tusia e le Lima o Mamona i luga o "
    "Papatusi Na Sii mai Papatusi a Nifae"
    "\n\n"
    "O le mea lea, o se otootoga o le talafaamaumau o le nuu o Nifae, ma sa "
    "Lamanā foi—Ua tusi atu ia sa Lamanā, o ē o se vaega o totoe o le aiga o "
    "Isaraelu; ma Iutaia ma Nuuese foi—Ua tusia e ala i le poloa’iga, ma ala "
    "foi i le agaga o valo’aga ma faaaliga—Ua tusia ma faamaufaailogaina, ma "
    "natia i le Alii, ina ia le faaumatia i latou—Ina ia oo mai e ala i le "
    "meaalofa ma le mana o le Atua e faaliliu ai—Ua faamaufaailogaina e le lima "
    "o Moronae, ma natia i le Alii, ia oo mai i le taimi e tatau ai e ala mai i "
    "le Nuuese—O lona faaliliuga e ala mai i le meaalofa a le Atua."
    "\n\n"
    "O se otootoga na sii mai foi mai le Tusi a Eteru, o se talafaamaumau o le "
    "nuu o Iareto, o e na faataapeapeina i le taimi na faaeseeseina ai e le Alii "
    "le gagana a le nuu, a o latou fausia se olo e o ae ai i le lagi—Lea e "
    "faailoa atu ai i le vaega o totoe o le aiga o Isaraelu mea sili na faia e "
    "le Alii mo o latou tamā; ina ia latou iloa ai foi feagaiga a le Alii, ua lē "
    "lafoaiina ese i latou e faavavau—Ma mo le faatalitonuina foi o Iutaia ma "
    "Nuuese, o Iesu o le Keriso, o le Atua Faavavau, ua faaali mai o ia lava i "
    "atunuu uma—O lenei foi, afai o i ai ni sese, o sese ia o tagata; o le mea "
    "lea, aua le ta’uleagaina mea a le Atua, ina ia lē pona outou i le nofoa "
    "faamasino o Keriso."
    "\n\n"
    "O le uluai faaliliuga mai papatusi i le gagana Peretania, na faia e Iosefa "
    "Samita, Le Itiiti."
)

TITLE_CELLS = [
    # — Title block —
    ("O Le Tusi a Mamona:", "The Book of Mormon:"),
    ("O Se Tala na Tusia", "An Account Written"),
    ("e le Lima o Mamona", "by the Hand of Mormon"),
    ("i luga o Papatusi", "upon Plates"),
    ("Na Sii mai", "Taken from"),
    ("Papatusi a Nifae", "the Plates of Nephi"),
    # — Paragraph 1 —
    ("O le mea lea,", "Wherefore,"),
    ("o se otootoga", "it is an abridgment"),
    ("o le talafaamaumau", "of the record"),
    ("o le nuu o Nifae,", "of the people of Nephi,"),
    ("ma sa Lamanā foi—", "and also of the Lamanites—"),
    ("Ua tusi atu", "Written"),
    ("ia sa Lamanā,", "to the Lamanites,"),
    ("o ē", "who are"),
    ("o se vaega o totoe", "a remnant"),
    ("o le aiga o Isaraelu;", "of the house of Israel;"),
    ("ma Iutaia ma Nuuese foi—", "and also to Jew and Gentile—"),
    ("Ua tusia", "Written"),
    ("e ala i le poloa’iga,", "by way of commandment,"),
    ("ma ala foi", "and also"),
    ("i le agaga o valo’aga", "by the spirit of prophecy"),
    ("ma faaaliga—", "and of revelation—"),
    ("Ua tusia ma faamaufaailogaina,", "Written and sealed up,"),
    ("ma natia i le Alii,", "and hid up unto the Lord,"),
    ("ina ia", "that"),
    ("le faaumatia i latou—", "they might not be destroyed—"),
    ("Ina ia oo mai", "To come forth"),
    ("e ala i le meaalofa", "by the gift"),
    ("ma le mana", "and power"),
    ("o le Atua", "of God"),
    ("e faaliliu ai—", "unto the interpretation thereof—"),
    ("Ua faamaufaailogaina", "Sealed"),
    ("e le lima o Moronae,", "by the hand of Moroni,"),
    ("ma natia i le Alii,", "and hid up unto the Lord,"),
    ("ia oo mai", "to come forth"),
    ("i le taimi", "in the time"),
    ("e tatau ai", "that is due"),
    ("e ala mai", "by way of"),
    ("i le Nuuese—", "the Gentile—"),
    ("O lona faaliliuga", "The interpretation thereof"),
    ("e ala mai", "by"),
    ("i le meaalofa", "the gift"),
    ("a le Atua.", "of God."),
    # — Paragraph 2 —
    ("O se otootoga", "An abridgment"),
    ("na sii mai foi", "taken also"),
    ("mai le Tusi a Eteru,", "from the Book of Ether,"),
    ("o se talafaamaumau", "which is a record"),
    ("o le nuu o Iareto,", "of the people of Jared,"),
    ("o e na faataapeapeina", "who were scattered"),
    ("i le taimi", "at the time"),
    ("na faaeseeseina ai", "confounded"),
    ("e le Alii", "the Lord"),
    ("le gagana a le nuu,", "the language of the people,"),
    ("a o latou fausia", "when they were building"),
    ("se olo", "a tower"),
    ("e o ae ai", "to get up"),
    ("i le lagi—", "to heaven—"),
    ("Lea e faailoa atu ai", "Which is to show"),
    ("i le vaega o totoe", "unto the remnant"),
    ("o le aiga o Isaraelu", "of the house of Israel"),
    ("mea sili", "what great things"),
    ("na faia e le Alii", "the Lord hath done"),
    ("mo o latou tamā;", "for their fathers;"),
    ("ina ia latou iloa ai", "and that they may know"),
    ("foi", "also"),
    ("feagaiga a le Alii,", "the covenants of the Lord,"),
    ("ua lē lafoaiina ese i latou", "that they are not cast off"),
    ("e faavavau—", "forever—"),
    ("Ma mo le faatalitonuina foi", "And also to the convincing"),
    ("o Iutaia ma Nuuese,", "of the Jew and Gentile,"),
    ("o Iesu o le Keriso,", "that Jesus is the Christ,"),
    ("o le Atua Faavavau,", "the Eternal God,"),
    ("ua faaali mai", "manifesting"),
    ("o ia lava", "himself"),
    ("i atunuu uma—", "unto all nations—"),
    ("O lenei foi,", "And now,"),
    ("afai o i ai", "if there are"),
    ("ni sese,", "faults,"),
    ("o sese ia o tagata;", "they are the mistakes of men;"),
    ("o le mea lea,", "wherefore,"),
    ("aua le ta’uleagaina", "condemn not"),
    ("mea a le Atua,", "the things of God,"),
    ("ina ia lē pona outou", "that ye may be found spotless"),
    ("i le nofoa faamasino", "at the judgment-seat"),
    ("o Keriso.", "of Christ."),
    # — Translator line —
    ("O le uluai faaliliuga", "The first translation"),
    ("mai papatusi", "from the plates"),
    ("i le gagana Peretania,", "into the English language,"),
    ("na faia e Iosefa Samita,", "made by Joseph Smith,"),
    ("Le Itiiti.", "Jr."),
]

# ---------------------------------------------------------------------------
# Introduction
# ---------------------------------------------------------------------------

INTRO_EN = (
    "The Book of Mormon is a volume of holy scripture comparable to the Bible. "
    "It is a record of God's dealings with ancient inhabitants of the Americas "
    "and contains the fulness of the everlasting gospel."
    "\n\n"
    "The book was written by many ancient prophets by the spirit of prophecy "
    "and revelation. Their words, written on gold plates, were quoted and "
    "abridged by a prophet-historian named Mormon. The record gives an account "
    "of two great civilizations. One came from Jerusalem in 600 B.C. and "
    "afterward separated into two nations, known as the Nephites and the "
    "Lamanites. The other came much earlier when the Lord confounded the "
    "languages at the Tower of Babel. This group is known as the Jaredites. "
    "After thousands of years, all were destroyed except the Lamanites, and "
    "they are among the ancestors of the American Indians."
    "\n\n"
    "The crowning event recorded in the Book of Mormon is the personal ministry "
    "of the Lord Jesus Christ among the Nephites soon after His resurrection. It "
    "puts forth the doctrines of the gospel, outlines the plan of salvation, and "
    "tells men what they must do to gain peace in this life and eternal "
    "salvation in the life to come."
    "\n\n"
    "After Mormon completed his writings, he delivered the account to his son "
    "Moroni, who added a few words of his own and hid up the plates in the Hill "
    "Cumorah. On September 21, 1823, the same Moroni, then a glorified, "
    "resurrected being, appeared to the Prophet Joseph Smith and instructed him "
    "regarding the ancient record and its destined translation into the English "
    "language."
    "\n\n"
    "In due course the plates were delivered to Joseph Smith, who translated "
    "them by the gift and power of God. The record is now published in many "
    "languages as a new and additional witness that Jesus Christ is the Son of "
    "the living God and that all who will come unto Him and obey the laws and "
    "ordinances of His gospel may be saved."
    "\n\n"
    "Concerning this record the Prophet Joseph Smith said: “I told the brethren "
    "that the Book of Mormon was the most correct of any book on earth, and the "
    "keystone of our religion, and a man would get nearer to God by abiding by "
    "its precepts, than by any other book.”"
    "\n\n"
    "In addition to Joseph Smith, the Lord provided for eleven others to see the "
    "gold plates for themselves and to be special witnesses of the truth and "
    "divinity of the Book of Mormon. Their written testimonies are included "
    "herein as “The Testimony of Three Witnesses” and “The Testimony of Eight "
    "Witnesses.”"
    "\n\n"
    "We invite all men everywhere to read the Book of Mormon, to ponder in their "
    "hearts the message it contains, and then to ask God, the Eternal Father, in "
    "the name of Christ if the book is true. Those who pursue this course and ask "
    "in faith will gain a testimony of its truth and divinity by the power of the "
    "Holy Ghost. (See Moroni 10:3–5.)"
    "\n\n"
    "Those who gain this divine witness from the Holy Spirit will also come to "
    "know by the same power that Jesus Christ is the Savior of the world, that "
    "Joseph Smith is His revelator and prophet in these last days, and that The "
    "Church of Jesus Christ of Latter-day Saints is the Lord's kingdom once "
    "again established on the earth, preparatory to the Second Coming of the "
    "Messiah."
)

INTRO_SM = (
    "O le Tusi a Mamona o se tusi o tusitusiga paia e pei o le Tusi Paia. O se "
    "talafaamaumau o fegalegaleaiga a le Atua ma tagata sa nonofo i Amerika "
    "anamua, ma ua i ai le atoatoaga o le talalelei tumau faavavau."
    "\n\n"
    "O le tusi na tusia e le toatele o perofeta anamua e ala i le agaga o "
    "valoaga ma faaaliga. O a latou upu, na tusia i papatusi auro, na sii mai ma "
    "otooto e se perofeta tusitalafaasolopito e igoa ia Mamona. Ua tuuina mai i "
    "lea talafaamaumau se tala o ni faiganuu tetele se lua. O le tasi na o mai "
    "mai Ierusalema i le 600 T.L.M. ma sa mulimuli ane vaeluaina i ni malo se "
    "lua, ua ta’ua o sa Nifaē ma sa Lamanā. O le isi na o mai mamao i tua atu i "
    "le taimi na faaeseese ai e le Alii gagana i le Olo o Papelu. O le nuu lenei "
    "ua ta’ua o Sa Iaretō. Ina ua mavae le afe ma afe o tausaga, sa faaumatia "
    "nei malo uma e lua vagana ai sa Lamanā, ma o i latou o ni isi o tuaa o "
    "Initia Amerika."
    "\n\n"
    "O le mea aupito sili ona taua na tupu ua faamaumauina i le Tusi a Mamona, o "
    "le auaunaga patino lea a le Alii o Iesu Keriso i totonu o tagata sa Nifaē, "
    "ina ua mavae Lona toetu mai. Ua faamatala mai i le tusi mataupu faavae autu "
    "o le talalelei, ua otooto mai ai le fuafuaga o le faaolataga, ma ua taʼu "
    "mai ai foi i tagata mea e ao ona latou faia e maua ai le filemu i le olaga "
    "nei ma le olataga e faavavau i le olaga a sau."
    "\n\n"
    "Ina ua maea ona faia e Mamona ana tusitusiga, sa ia tuuina atu le "
    "talafaamaumau i lona atalii o Moronae, o lē sa faaopoopo i ai ana lava upu "
    "itiiti ona natia lea o papatusi i le Maupuepue o Kumora. I le aso 21 o "
    "Setema, 1823, o Moronae lava lea e tasi, ua avea nei ma tagata toetu ma le "
    "faamamaluina, na faaali mai i le Perofeta o Iosefa Samita ma faatonu o ia e "
    "uiga i le talafaamaumau anamua ma lona faaliliuga faamoemoeina i le gagana "
    "Peretania."
    "\n\n"
    "I le aso atofaina, na tuuina mai ai papatusi ia Iosefa Samita, o lē na "
    "faaliliuina i le meaalofa ma le mana o le Atua. O lenei talafaamaumau ua "
    "lomia nei ma faasalalauina i gagana e tele o se molimau fou ma faaopoopo o "
    "Iesu Keriso o le Alo o le Atua soifua, o i latou uma foi o le a o mai ia te "
    "Ia ma usiusitai i tulafono ma sauniga o Lana talalelei e mafai ona "
    "faaolaina."
    "\n\n"
    "E faatatau i lenei talafaamaumau na saunoa mai ai le Perofeta o Iosefa "
    "Samita: “Sa ou fai atu i le au uso o le Tusi a Mamona o le tusi aupito sili "
    "ona saʼo i soo se isi lava tusi i luga o le lalolagi, ma o le ma’aʼauʼau o "
    "la tatou tapuaiga, ma e sili ona latalata atu o se tagata i le Atua i lona "
    "ola ai i ona mataupu, nai lo se isi lava tusi.”"
    "\n\n"
    "E faaopoopo ia Iosefa Samita, sa saunia foi e le Alii ni isi e toasefulutasi "
    "e vaai i papatusi auro mo i latou lava ma avea ma molimau faapitoa o le moni "
    "ma le paia o le Tusi a Mamona. O a latou molimau tusia ua i totonu o lenei "
    "tusi, “O Le Mau a Molimau e Toatolu” ma le “O Le Mau a Molimau e Toavalu.”"
    "\n\n"
    "Matou te valaau atu i tagata uma e i soo se mea, ia faitau i le Tusi a "
    "Mamona, ia mafaufau loloto i ai i o latou loto le savali o i ai, ona ole atu "
    "lea i le Atua, le Tamā Faavavau, i le suafa o Keriso pe ua moni le tusi. O i "
    "latou o e e mulimuli i lenei ala ma ole atu i le faatuatua, o le a latou "
    "maua se molimau i le moni ma le paia o le tusi e ala i le mana o le Agaga "
    "Paia. (Tagai i le Moronae 10:3–5.)"
    "\n\n"
    "O i latou o e mauaina lenei molimau paia mai le Agaga Paia o le a latou iloa "
    "foi e ala i lea lava mana o Iesu Keriso o le Faaola o le lalolagi, o Iosefa "
    "Samita o Lana talifaaaliga ma le perofeta i aso nei e gata ai, ma O Le "
    "Ekalesia a Iesu Keriso o le Au Paia o Aso e Gata Ai o le malo o le Alii ua "
    "toe faatuina i luga o le lalolagi, e saunia ai mo le Afio Mai Faalua o le "
    "Mesia."
)

INTRO_CELLS = [
    # Paragraph 1
    ("O le Tusi a Mamona", "The Book of Mormon"),
    ("o se tusi", "is a volume"),
    ("o tusitusiga paia", "of holy scripture"),
    ("e pei o", "comparable to"),
    ("le Tusi Paia.", "the Bible."),
    ("O se talafaamaumau", "It is a record"),
    ("o fegalegaleaiga a le Atua", "of God's dealings"),
    ("ma tagata", "with people"),
    ("sa nonofo i Amerika anamua,", "who lived in ancient America,"),
    ("ma ua i ai", "and contains"),
    ("le atoatoaga", "the fulness"),
    ("o le talalelei tumau faavavau.", "of the everlasting gospel."),
    # Paragraph 2
    ("O le tusi na tusia", "The book was written"),
    ("e le toatele", "by many"),
    ("o perofeta anamua", "ancient prophets"),
    ("e ala i le agaga", "by the spirit"),
    ("o valoaga ma faaaliga.", "of prophecy and revelation."),
    ("O a latou upu,", "Their words,"),
    ("na tusia i papatusi auro,", "written on gold plates,"),
    ("na sii mai", "were quoted"),
    ("ma otooto", "and abridged"),
    ("e se perofeta tusitalafaasolopito", "by a prophet-historian"),
    ("e igoa ia Mamona.", "named Mormon."),
    ("Ua tuuina mai", "It gives"),
    ("i lea talafaamaumau", "in this record"),
    ("se tala", "an account"),
    ("o ni faiganuu tetele se lua.", "of two great civilizations."),
    ("O le tasi", "One"),
    ("na o mai mai Ierusalema", "came from Jerusalem"),
    ("i le 600", "in 600"),
    ("T.L.M.", "B.C."),
    ("ma sa mulimuli ane vaeluaina", "and afterward separated"),
    ("i ni malo se lua,", "into two nations,"),
    ("ua ta’ua", "known as"),
    ("o sa Nifaē", "the Nephites"),
    ("ma sa Lamanā.", "and Lamanites."),
    ("O le isi", "The other"),
    ("na o mai", "came"),
    ("mamao i tua atu", "much earlier"),
    ("i le taimi", "at the time"),
    ("na faaeseese ai e le Alii", "the Lord confounded"),
    ("gagana", "the languages"),
    ("i le Olo o Papelu.", "at the Tower of Babel."),
    ("O le nuu lenei", "This people"),
    ("ua ta’ua", "were known as"),
    ("o Sa Iaretō.", "the Jaredites."),
    ("Ina ua mavae", "After"),
    ("le afe ma afe", "thousands"),
    ("o tausaga,", "of years,"),
    ("sa faaumatia", "were destroyed"),
    ("nei malo uma e lua", "all these two nations"),
    ("vagana ai sa Lamanā,", "except the Lamanites,"),
    ("ma o i latou", "and they are"),
    ("o ni isi o tuaa", "among the ancestors"),
    ("o Initia Amerika.", "of the American Indians."),
    # Paragraph 3
    ("O le mea", "The event"),
    ("aupito sili ona taua", "most important"),
    ("na tupu", "that occurred"),
    ("ua faamaumauina", "recorded"),
    ("i le Tusi a Mamona,", "in the Book of Mormon,"),
    ("o le auaunaga patino lea", "is the personal ministry"),
    ("a le Alii", "of the Lord"),
    ("o Iesu Keriso", "Jesus Christ"),
    ("i totonu o", "among"),
    ("tagata sa Nifaē,", "the Nephite people,"),
    ("ina ua mavae", "soon after"),
    ("Lona toetu mai.", "His resurrection."),
    ("Ua faamatala mai", "It sets forth"),
    ("i le tusi", "in the book"),
    ("mataupu faavae autu", "the doctrines"),
    ("o le talalelei,", "of the gospel,"),
    ("ua otooto mai ai", "outlines"),
    ("le fuafuaga o le faaolataga,", "the plan of salvation,"),
    ("ma ua taʼu mai ai foi", "and also tells"),
    ("i tagata", "men"),
    ("mea e ao", "what they must"),
    ("ona latou faia", "do"),
    ("e maua ai le filemu", "to gain peace"),
    ("i le olaga nei", "in this life"),
    ("ma le olataga e faavavau", "and eternal salvation"),
    ("i le olaga a sau.", "in the life to come."),
    # Paragraph 4
    ("Ina ua maea ona faia", "When had finished"),
    ("e Mamona ana tusitusiga,", "Mormon his writings,"),
    ("sa ia tuuina atu", "he delivered"),
    ("le talafaamaumau", "the record"),
    ("i lona atalii o Moronae,", "to his son Moroni,"),
    ("o lē sa faaopoopo i ai", "who added"),
    ("ana lava upu itiiti", "a few words of his own"),
    ("ona natia lea", "and hid up"),
    ("o papatusi", "the plates"),
    ("i le Maupuepue o Kumora.", "in the Hill Cumorah."),
    ("I le aso 21", "On the 21st day"),
    ("o Setema, 1823,", "of September, 1823,"),
    ("o Moronae lava lea", "this same Moroni,"),
    ("e tasi,", "the one,"),
    ("ua avea nei", "now become"),
    ("ma tagata toetu", "a resurrected being"),
    ("ma le faamamaluina,", "and glorified,"),
    ("na faaali mai", "appeared"),
    ("i le Perofeta", "to the Prophet"),
    ("o Iosefa Samita", "Joseph Smith"),
    ("ma faatonu o ia", "and instructed him"),
    ("e uiga i", "concerning"),
    ("le talafaamaumau anamua", "the ancient record"),
    ("ma lona faaliliuga faamoemoeina", "and its destined translation"),
    ("i le gagana Peretania.", "into the English language."),
    # Paragraph 5
    ("I le aso atofaina,", "In due course,"),
    ("na tuuina mai ai", "were delivered"),
    ("papatusi", "the plates"),
    ("ia Iosefa Samita,", "to Joseph Smith,"),
    ("o lē na faaliliuina", "who translated them"),
    ("i le meaalofa", "by the gift"),
    ("ma le mana o le Atua.", "and power of God."),
    ("O lenei talafaamaumau", "This record"),
    ("ua lomia nei", "is now printed"),
    ("ma faasalalauina", "and distributed"),
    ("i gagana e tele", "in many languages"),
    ("o se molimau fou", "as a new witness"),
    ("ma faaopoopo", "and additional"),
    ("o Iesu Keriso", "of Jesus Christ"),
    ("o le Alo", "the Son"),
    ("o le Atua soifua,", "of the living God,"),
    ("o i latou uma foi", "and that all"),
    ("o le a o mai", "who will come"),
    ("ia te Ia", "unto Him"),
    ("ma usiusitai", "and obey"),
    ("i tulafono ma sauniga", "the laws and ordinances"),
    ("o Lana talalelei", "of His gospel"),
    ("e mafai ona faaolaina.", "may be saved."),
    # Paragraph 6 (Joseph Smith quotation)
    ("E faatatau i", "Concerning"),
    ("lenei talafaamaumau", "this record"),
    ("na saunoa mai ai", "said"),
    ("le Perofeta o Iosefa Samita:", "the Prophet Joseph Smith:"),
    ("“Sa ou fai atu", "“I told"),
    ("i le au uso", "the brethren"),
    ("o le Tusi a Mamona", "that the Book of Mormon"),
    ("o le tusi", "was the book"),
    ("aupito sili ona saʼo", "most correct"),
    ("i soo se", "of any"),
    ("isi lava tusi", "other book"),
    ("i luga o le lalolagi,", "on earth,"),
    ("ma o le ma’aʼauʼau", "and the keystone"),
    ("o la tatou tapuaiga,", "of our religion,"),
    ("ma e sili ona latalata atu", "and would draw nearer"),
    ("o se tagata i le Atua", "a man to God"),
    ("i lona ola ai", "by abiding"),
    ("i ona mataupu,", "by its precepts,"),
    ("nai lo", "than"),
    ("se isi lava tusi.”", "any other book.”"),
    # Paragraph 7
    ("E faaopoopo ia", "In addition to"),
    ("Iosefa Samita,", "Joseph Smith,"),
    ("sa saunia foi", "also provided"),
    ("e le Alii", "the Lord"),
    ("ni isi e toasefulutasi", "eleven others"),
    ("e vaai i", "to see"),
    ("papatusi auro", "the gold plates"),
    ("mo i latou lava", "for themselves"),
    ("ma avea", "and to be"),
    ("ma molimau faapitoa", "special witnesses"),
    ("o le moni", "of the truth"),
    ("ma le paia", "and divinity"),
    ("o le Tusi a Mamona.", "of the Book of Mormon."),
    ("O a latou molimau tusia", "Their written testimonies"),
    ("ua i totonu o", "are included in"),
    ("lenei tusi,", "this book,"),
    ("“O Le Mau", "“The Testimony"),
    ("a Molimau e Toatolu”", "of Three Witnesses”"),
    ("ma le “O Le Mau", "and “The Testimony"),
    ("a Molimau e Toavalu.”", "of Eight Witnesses.”"),
    # Paragraph 8
    ("Matou te valaau atu", "We invite"),
    ("i tagata uma", "all men"),
    ("e i soo se mea,", "everywhere,"),
    ("ia faitau i", "to read"),
    ("le Tusi a Mamona,", "the Book of Mormon,"),
    ("ia mafaufau loloto i ai", "to ponder"),
    ("i o latou loto", "in their hearts"),
    ("le savali o i ai,", "the message it contains,"),
    ("ona ole atu lea", "and then to ask"),
    ("i le Atua,", "God,"),
    ("le Tamā Faavavau,", "the Eternal Father,"),
    ("i le suafa o Keriso", "in the name of Christ"),
    ("pe ua moni", "if is true"),
    ("le tusi.", "the book."),
    ("O i latou o e", "Those who"),
    ("e mulimuli i lenei ala", "pursue this course"),
    ("ma ole atu", "and ask"),
    ("i le faatuatua,", "in faith,"),
    ("o le a latou maua", "will gain"),
    ("se molimau", "a testimony"),
    ("i le moni ma le paia", "of the truth and divinity"),
    ("o le tusi", "of the book"),
    ("e ala i le mana", "by the power"),
    ("o le Agaga Paia.", "of the Holy Ghost."),
    ("(Tagai i le", "(See"),
    ("Moronae 10:3–5.)", "Moroni 10:3–5.)"),
    # Paragraph 9
    ("O i latou o e", "Those who"),
    ("mauaina", "gain"),
    ("lenei molimau paia", "this divine witness"),
    ("mai le Agaga Paia", "from the Holy Spirit"),
    ("o le a latou iloa", "will know"),
    ("foi", "also"),
    ("e ala i lea lava mana", "by the same power"),
    ("o Iesu Keriso", "that Jesus Christ"),
    ("o le Faaola", "is the Savior"),
    ("o le lalolagi,", "of the world,"),
    ("o Iosefa Samita", "that Joseph Smith"),
    ("o Lana talifaaaliga", "is His revelator"),
    ("ma le perofeta", "and prophet"),
    ("i aso nei e gata ai,", "in these last days,"),
    ("ma O Le Ekalesia", "and The Church"),
    ("a Iesu Keriso", "of Jesus Christ"),
    ("o le Au Paia", "of the Saints"),
    ("o Aso e Gata Ai", "of Latter days"),
    ("o le malo o le Alii", "is the Lord's kingdom"),
    ("ua toe faatuina", "again established"),
    ("i luga o le lalolagi,", "on the earth,"),
    ("e saunia ai", "in preparation"),
    ("mo le Afio Mai Faalua", "for the Second Coming"),
    ("o le Mesia.", "of the Messiah."),
]

SECTIONS = [
    {
        "id": "title-page",
        "title_en": "Title Page",
        "title_sm": "Itulau Ulutala",
        "en": TITLE_EN,
        "sm": TITLE_SM,
        "cells": TITLE_CELLS,
    },
    {
        "id": "introduction",
        "title_en": "Introduction",
        "title_sm": "Faatomuaga",
        "en": INTRO_EN,
        "sm": INTRO_SM,
        "cells": INTRO_CELLS,
    },
]


def cells_to_words(cells: list[tuple[str, str]]) -> list[dict]:
    """Expand (samoan_phrase, gloss) cells into a `·`-marked word array."""
    words: list[dict] = []
    for sm_phrase, gloss in cells:
        tokens = sm_phrase.split(" ")
        for t in tokens[:-1]:
            words.append({"sm": t, "en": "·"})
        words.append({"sm": tokens[-1], "en": gloss})
    return words


def fm_split(text: str) -> list[str]:
    """Tokenize like the app will: split on any whitespace (incl. paragraph
    breaks), and split X—Y into X— , Y."""
    spaced = re.sub(EMDASH + r"(?=\S)", EMDASH + " ", text)
    return spaced.split()


def main() -> None:
    out = {"version": 1, "sections": []}
    for entry in SECTIONS:
        sm = norm(entry["sm"])
        words = None
        if entry.get("cells"):
            cells = [(norm(a), b) for a, b in entry["cells"]]
            words = cells_to_words(cells)
            recon = [w["sm"] for w in words]
            expected = fm_split(sm)
            if recon != expected:
                for i, (a, b) in enumerate(zip(recon, expected)):
                    if a != b:
                        raise SystemExit(
                            f"[{entry['id']}] token {i} mismatch: "
                            f"cells={a!r} source={b!r}"
                        )
                raise SystemExit(
                    f"[{entry['id']}] length mismatch: "
                    f"cells={len(recon)} source={len(expected)}"
                )
        out["sections"].append(
            {
                "id": entry["id"],
                "titleEn": entry["title_en"],
                "titleSm": entry["title_sm"],
                "en": entry["en"],
                "sm": sm,
                "words": words,
            }
        )
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out['sections'])} front-matter sections -> {OUT}")


# ---------------------------------------------------------------------------
# The Testimony of Three Witnesses
# ---------------------------------------------------------------------------
# (sections appended below; run guard moved to end of file)

THREE_EN = (
    "Be it known unto all nations, kindreds, tongues, and people, unto whom "
    "this work shall come: That we, through the grace of God the Father, and "
    "our Lord Jesus Christ, have seen the plates which contain this record, "
    "which is a record of the people of Nephi, and also of the Lamanites, "
    "their brethren, and also of the people of Jared, who came from the tower "
    "of which hath been spoken. And we also know that they have been "
    "translated by the gift and power of God, for his voice hath declared it "
    "unto us; wherefore we know of a surety that the work is true. And we "
    "also testify that we have seen the engravings which are upon the plates; "
    "and they have been shown unto us by the power of God, and not of man. "
    "And we declare with words of soberness, that an angel of God came down "
    "from heaven, and he brought and laid before our eyes, that we beheld and "
    "saw the plates, and the engravings thereon; and we know that it is by "
    "the grace of God the Father, and our Lord Jesus Christ, that we beheld "
    "and bear record that these things are true. And it is marvelous in our "
    "eyes. Nevertheless, the voice of the Lord commanded us that we should "
    "bear record of it; wherefore, to be obedient unto the commandments of "
    "God, we bear testimony of these things. And we know that if we are "
    "faithful in Christ, we shall rid our garments of the blood of all men, "
    "and be found spotless before the judgment-seat of Christ, and shall "
    "dwell with him eternally in the heavens. And the honor be to the Father, "
    "and to the Son, and to the Holy Ghost, which is one God. Amen."
    "\n\n"
    "Oliver Cowdery\nDavid Whitmer\nMartin Harris"
)

THREE_SM = (
    "Ina ia iloa e atunuu uma, ituaiga, gagana, ma nuu, e oo atu i ai lenei "
    "tusi: O i matou, e ala i le alofa tunoa o le Atua le Tamā, ma lo tatou "
    "Alii o Iesu Keriso, sa matou vaai ai i papatusi ua i ai lenei "
    "talafaamaumau, o le talafaamaumau lea o le nuu o Nifae, ma sa Lamanā "
    "foi, o o latou uso, ma le nuu foi o Iareto, o e na o mai mai le olo lea "
    "ua ta'ua. Ua matou iloa foi sa faaliliuina i le meaalofa ma le mana o le "
    "Atua, auā na tautino mai e lona siufofoga ia te i matou; o le mea lea ua "
    "matou iloa ai ma le mautinoa ua moni le galuega. Matou te molimau atu "
    "foi sa matou vaai i togitogiga ua i ai i luga o papatusi; sa faaali mai "
    "foi ia mea ia te i matou i le mana o le Atua, ae lē o se tagata. Matou "
    "te tautino atu foi i upu faamaoni, sa afio ifo se agelu a le Atua mai le "
    "lagi, sa ia aumaia foi ma faataatia i luma o o matou mata, sa matou vaai "
    "ma iloa ai papatusi, ma togitogiga ua i ai; ua matou iloa foi o le alofa "
    "tunoa o le Atua le Tamā, ma lo matou Alii o Iesu Keriso, ua matou vaai "
    "ma molimau atu ai ua moni ia mea. Ua ofoofogia foi i la matou vaai. Ae "
    "ui i lea, sa poloaiina i matou e le siufofoga o le Alii e tatau ona "
    "matou molimauina; o le mea lea, ina ia matou usiusitai i poloaiga a le "
    "Atua, ua matou molimau atu ai i ia mea. Ma ua matou iloa foi afai matou "
    "te faamaoni ia Keriso, o le a mamā o matou ofu mai le toto o tagata uma, "
    "ma o le a lē pōnā foi i luma o le nofoa faamasino o Keriso, o le a mau "
    "foi faatasi ma ia e faavavau i le lagi. Ma ia i ai pea le mamalu i le "
    "Tamā, ma le Alo, ma le Agaga Paia, o le Atua e tasi. Amene."
    "\n\n"
    "Oliva Kaotui\nTavita Uitimera\nMatini Harisi"
)

THREE_CELLS = [
    ("Ina ia iloa", "Be it known"),
    ("e atunuu uma,", "unto all nations,"),
    ("ituaiga,", "kindreds,"),
    ("gagana,", "tongues,"),
    ("ma nuu,", "and people,"),
    ("e oo atu i ai", "unto whom shall come"),
    ("lenei tusi:", "this work:"),
    ("O i matou,", "we,"),
    ("e ala i", "through"),
    ("le alofa tunoa", "the grace"),
    ("o le Atua", "of God"),
    ("le Tamā,", "the Father,"),
    ("ma lo tatou Alii", "and our Lord"),
    ("o Iesu Keriso,", "Jesus Christ,"),
    ("sa matou vaai ai", "have seen"),
    ("i papatusi", "the plates"),
    ("ua i ai lenei talafaamaumau,", "which contain this record,"),
    ("o le talafaamaumau lea", "which is a record"),
    ("o le nuu", "of the people"),
    ("o Nifae,", "of Nephi,"),
    ("ma sa Lamanā foi,", "and also the Lamanites,"),
    ("o o latou uso,", "their brethren,"),
    ("ma le nuu foi", "and also the people"),
    ("o Iareto,", "of Jared,"),
    ("o e na o mai", "who came"),
    ("mai le olo", "from the tower"),
    ("lea ua ta'ua.", "of which hath been spoken."),
    ("Ua matou iloa foi", "And we also know"),
    ("sa faaliliuina", "have been translated"),
    ("i le meaalofa", "by the gift"),
    ("ma le mana", "and power"),
    ("o le Atua,", "of God,"),
    ("auā na tautino mai", "for hath declared"),
    ("e lona siufofoga", "his voice"),
    ("ia te i matou;", "unto us;"),
    ("o le mea lea", "wherefore"),
    ("ua matou iloa ai", "we know"),
    ("ma le mautinoa", "of a surety"),
    ("ua moni", "is true"),
    ("le galuega.", "the work."),
    ("Matou te molimau atu foi", "And we also testify"),
    ("sa matou vaai", "we have seen"),
    ("i togitogiga", "the engravings"),
    ("ua i ai", "which are"),
    ("i luga o papatusi;", "upon the plates;"),
    ("sa faaali mai foi", "and also been shown"),
    ("ia mea", "these things"),
    ("ia te i matou", "unto us"),
    ("i le mana", "by the power"),
    ("o le Atua,", "of God,"),
    ("ae lē", "and not"),
    ("o se tagata.", "of man."),
    ("Matou te tautino atu foi", "And we declare"),
    ("i upu faamaoni,", "with words of soberness,"),
    ("sa afio ifo", "came down"),
    ("se agelu", "an angel"),
    ("a le Atua", "of God"),
    ("mai le lagi,", "from heaven,"),
    ("sa ia aumaia foi", "and he brought"),
    ("ma faataatia", "and laid"),
    ("i luma o", "before"),
    ("o matou mata,", "our eyes,"),
    ("sa matou vaai", "we beheld"),
    ("ma iloa ai", "and saw"),
    ("papatusi,", "the plates,"),
    ("ma togitogiga", "and the engravings"),
    ("ua i ai;", "thereon;"),
    ("ua matou iloa foi", "and we know"),
    ("o le alofa tunoa", "by the grace"),
    ("o le Atua", "of God"),
    ("le Tamā,", "the Father,"),
    ("ma lo matou Alii", "and our Lord"),
    ("o Iesu Keriso,", "Jesus Christ,"),
    ("ua matou vaai", "we beheld"),
    ("ma molimau atu ai", "and bear record"),
    ("ua moni ia mea.", "these things are true."),
    ("Ua ofoofogia foi", "And it is marvelous"),
    ("i la matou vaai.", "in our eyes."),
    ("Ae ui i lea,", "Nevertheless,"),
    ("sa poloaiina i matou", "commanded us"),
    ("e le siufofoga", "the voice"),
    ("o le Alii", "of the Lord"),
    ("e tatau ona", "should"),
    ("matou molimauina;", "we bear record;"),
    ("o le mea lea,", "wherefore,"),
    ("ina ia", "that"),
    ("matou usiusitai", "we be obedient"),
    ("i poloaiga", "unto the commandments"),
    ("a le Atua,", "of God,"),
    ("ua matou molimau atu ai", "we bear testimony"),
    ("i ia mea.", "of these things."),
    ("Ma ua matou iloa foi", "And we know"),
    ("afai", "that if"),
    ("matou te faamaoni", "we are faithful"),
    ("ia Keriso,", "in Christ,"),
    ("o le a mamā", "we shall be cleansed"),
    ("o matou ofu", "our garments"),
    ("mai le toto", "of the blood"),
    ("o tagata uma,", "of all men,"),
    ("ma", "and"),
    ("o le a lē pōnā", "shall not be found spotted"),
    ("foi", "also"),
    ("i luma o", "before"),
    ("le nofoa faamasino", "the judgment-seat"),
    ("o Keriso,", "of Christ,"),
    ("o le a mau foi", "and shall also dwell"),
    ("faatasi ma ia", "with him"),
    ("e faavavau", "eternally"),
    ("i le lagi.", "in the heavens."),
    ("Ma ia i ai pea", "And ever be"),
    ("le mamalu", "the honor"),
    ("i le Tamā,", "to the Father,"),
    ("ma le Alo,", "and to the Son,"),
    ("ma le Agaga Paia,", "and to the Holy Ghost,"),
    ("o le Atua e tasi.", "who is one God."),
    ("Amene.", "Amen."),
    ("Oliva Kaotui", "Oliver Cowdery"),
    ("Tavita Uitimera", "David Whitmer"),
    ("Matini Harisi", "Martin Harris"),
]

# ---------------------------------------------------------------------------
# The Testimony of Eight Witnesses
# ---------------------------------------------------------------------------

EIGHT_EN = (
    "Be it known unto all nations, kindreds, tongues, and people, unto whom "
    "this work shall come: That Joseph Smith, Jun., the translator of this "
    "work, has shown unto us the plates of which hath been spoken, which have "
    "the appearance of gold; and as many of the leaves as the said Smith has "
    "translated we did handle with our hands; and we also saw the engravings "
    "thereon, all of which has the appearance of ancient work, and of curious "
    "workmanship. And this we bear record with words of soberness, that the "
    "said Smith has shown unto us, for we have seen and hefted, and know of a "
    "surety that the said Smith has got the plates of which we have spoken. "
    "And we give our names unto the world, to witness unto the world that "
    "which we have seen. And we lie not, God bearing witness of it."
    "\n\n"
    "Christian Whitmer\nJacob Whitmer\nPeter Whitmer, Jun.\nJohn Whitmer\n"
    "Hiram Page\nJoseph Smith, Sen.\nHyrum Smith\nSamuel H. Smith"
)

EIGHT_SM = (
    "Ina ia iloa e atunuu uma, ituaiga, gagana, ma nuu, o e o le a oo atu i "
    "ai lenei tusi: Sa faaali mai ia te i matou e Iosefa Samita, Le Itiiti, o "
    "lē na faaliliuina lenei tusi, papatusi ua ta'ua, ia ua foliga mai i le "
    "auro; sa fetagofi foi o matou lima i le tele o itulau sa faaliliuina e "
    "Samita ua ta'ua; sa matou vaai foi i togitogiga ua i ai, sa foliga uma "
    "mai o ni mea mai anamua, ma o le gaosiga uiga ese foi. Ma o lenei matou "
    "te molimau atu ai i upu faamaoni, na faaali mai e Samita ua ta'ua ia te "
    "i matou, auā na matou vaai i ai ma siitia, ma iloa ai ma le mautinoa o "
    "loo ia Samita ua ta'ua o papatusi ua matou tautala atu ai. Ma matou te "
    "tuu atu foi o matou igoa i le lalolagi, e molimau atu i le lalolagi mea "
    "na matou vaai i ai. Ma matou te le faa'ole'ole lava, o loo molimau le "
    "Atua i ia mea."
    "\n\n"
    "Christian Uitimera\nJacob Uitimera\nPeter Uitimera, Le Itiiti\n"
    "Ioane Uitimera\nAilama Page\nIosefa Samita, Matua\nAilama Samita\n"
    "Samuel H. Samita"
)

EIGHT_CELLS = [
    ("Ina ia iloa", "Be it known"),
    ("e atunuu uma,", "unto all nations,"),
    ("ituaiga,", "kindreds,"),
    ("gagana,", "tongues,"),
    ("ma nuu,", "and people,"),
    ("o e", "unto whom"),
    ("o le a oo atu i ai", "shall come"),
    ("lenei tusi:", "this work:"),
    ("Sa faaali mai", "hath shown"),
    ("ia te i matou", "unto us"),
    ("e Iosefa Samita, Le Itiiti,", "by Joseph Smith, Jun.,"),
    ("o lē na faaliliuina", "who translated"),
    ("lenei tusi,", "this work,"),
    ("papatusi", "the plates"),
    ("ua ta'ua,", "spoken of,"),
    ("ia ua foliga mai", "which appeared"),
    ("i le auro;", "like gold;"),
    ("sa fetagofi foi", "we did also handle"),
    ("o matou lima", "with our hands"),
    ("i le tele", "as many"),
    ("o itulau", "of the leaves"),
    ("sa faaliliuina", "were translated"),
    ("e Samita", "by Smith"),
    ("ua ta'ua;", "aforesaid;"),
    ("sa matou vaai foi", "and we also saw"),
    ("i togitogiga", "the engravings"),
    ("ua i ai,", "thereon,"),
    ("sa foliga uma mai", "which all appeared"),
    ("o ni mea", "as things"),
    ("mai anamua,", "of ancient work,"),
    ("ma o le gaosiga", "and the workmanship"),
    ("uiga ese foi.", "curious."),
    ("Ma o lenei", "And now"),
    ("matou te molimau atu ai", "we bear record"),
    ("i upu faamaoni,", "with words of soberness,"),
    ("na faaali mai", "hath shown"),
    ("e Samita", "that Smith"),
    ("ua ta'ua", "aforesaid"),
    ("ia te i matou,", "unto us,"),
    ("auā", "for"),
    ("na matou vaai i ai", "we have seen it"),
    ("ma siitia,", "and hefted,"),
    ("ma iloa ai", "and know"),
    ("ma le mautinoa", "of a surety"),
    ("o loo ia Samita", "that the said Smith hath"),
    ("ua ta'ua", "aforesaid"),
    ("o papatusi", "the plates"),
    ("ua matou tautala atu ai.", "of which we have spoken."),
    ("Ma", "And"),
    ("matou te tuu atu foi", "we also give"),
    ("o matou igoa", "our names"),
    ("i le lalolagi,", "unto the world,"),
    ("e molimau atu", "to witness"),
    ("i le lalolagi", "unto the world"),
    ("mea", "that which"),
    ("na matou vaai i ai.", "we have seen."),
    ("Ma", "And"),
    ("matou te le faa'ole'ole lava,", "we lie not at all,"),
    ("o loo molimau", "bearing witness"),
    ("le Atua", "God"),
    ("i ia mea.", "of it."),
    ("Christian Uitimera", "Christian Whitmer"),
    ("Jacob Uitimera", "Jacob Whitmer"),
    ("Peter Uitimera, Le Itiiti", "Peter Whitmer, Jun."),
    ("Ioane Uitimera", "John Whitmer"),
    ("Ailama Page", "Hiram Page"),
    ("Iosefa Samita, Matua", "Joseph Smith, Sen."),
    ("Ailama Samita", "Hyrum Smith"),
    ("Samuel H. Samita", "Samuel H. Smith"),
]

# ---------------------------------------------------------------------------
# The Testimony of the Prophet Joseph Smith
# ---------------------------------------------------------------------------

JS_EN = (
    "The Prophet Joseph Smith's own words about the coming forth of the Book "
    "of Mormon are:"
    "\n\n"
    "“On the evening of the … twenty-first of September [1823] … I betook "
    "myself to prayer and supplication to Almighty God. …"
    "\n\n"
    "“While I was thus in the act of calling upon God, I discovered a light "
    "appearing in my room, which continued to increase until the room was "
    "lighter than at noonday, when immediately a personage appeared at my "
    "bedside, standing in the air, for his feet did not touch the floor."
    "\n\n"
    "“He had on a loose robe of most exquisite whiteness. It was a whiteness "
    "beyond anything earthly I had ever seen; nor do I believe that any "
    "earthly thing could be made to appear so exceedingly white and "
    "brilliant. His hands were naked, and his arms also, a little above the "
    "wrist; so, also, were his feet naked, as were his legs, a little above "
    "the ankles. His head and neck were also bare. I could discover that he "
    "had no other clothing on but this robe, as it was open, so that I could "
    "see into his bosom."
    "\n\n"
    "“Not only was his robe exceedingly white, but his whole person was "
    "glorious beyond description, and his countenance truly like lightning. "
    "The room was exceedingly light, but not so very bright as immediately "
    "around his person. When I first looked upon him, I was afraid; but the "
    "fear soon left me."
    "\n\n"
    "“He called me by name, and said unto me that he was a messenger sent "
    "from the presence of God to me, and that his name was Moroni; that God "
    "had a work for me to do; and that my name should be had for good and "
    "evil among all nations, kindreds, and tongues, or that it should be "
    "both good and evil spoken of among all people."
    "\n\n"
    "“He said there was a book deposited, written upon gold plates, giving "
    "an account of the former inhabitants of this continent, and the source "
    "from whence they sprang. He also said that the fulness of the "
    "everlasting Gospel was contained in it, as delivered by the Savior to "
    "the ancient inhabitants;"
    "\n\n"
    "“Also, that there were two stones in silver bows—and these stones, "
    "fastened to a breastplate, constituted what is called the Urim and "
    "Thummim—deposited with the plates; and the possession and use of these "
    "stones were what constituted ‘seers’ in ancient or former times; and "
    "that God had prepared them for the purpose of translating the book. …"
    "\n\n"
    "“Again, he told me, that when I got those plates of which he had "
    "spoken—for the time that they should be obtained was not yet "
    "fulfilled—I should not show them to any person; neither the breastplate "
    "with the Urim and Thummim; only to those to whom I should be commanded "
    "to show them; if I did I should be destroyed. While he was conversing "
    "with me about the plates, the vision was opened to my mind that I could "
    "see the place where the plates were deposited, and that so clearly and "
    "distinctly that I knew the place again when I visited it."
    "\n\n"
    "“After this communication, I saw the light in the room begin to gather "
    "immediately around the person of him who had been speaking to me, and "
    "it continued to do so until the room was again left dark, except just "
    "around him; when, instantly I saw, as it were, a conduit open right up "
    "into heaven, and he ascended till he entirely disappeared, and the room "
    "was left as it had been before this heavenly light had made its "
    "appearance."
    "\n\n"
    "“I lay musing on the singularity of the scene, and marveling greatly "
    "at what had been told to me by this extraordinary messenger; when, in "
    "the midst of my meditation, I suddenly discovered that my room was "
    "again beginning to get lighted, and in an instant, as it were, the same "
    "heavenly messenger was again by my bedside."
    "\n\n"
    "“He commenced, and again related the very same things which he had "
    "done at his first visit, without the least variation; which having "
    "done, he informed me of great judgments which were coming upon the "
    "earth, with great desolations by famine, sword, and pestilence; and "
    "that these grievous judgments would come on the earth in this "
    "generation. Having related these things, he again ascended as he had "
    "done before."
    "\n\n"
    "“By this time, so deep were the impressions made on my mind, that "
    "sleep had fled from my eyes, and I lay overwhelmed in astonishment at "
    "what I had both seen and heard. But what was my surprise when again I "
    "beheld the same messenger at my bedside, and heard him rehearse or "
    "repeat over again to me the same things as before; and added a caution "
    "to me, telling me that Satan would try to tempt me (in consequence of "
    "the indigent circumstances of my father's family), to get the plates "
    "for the purpose of getting rich. This he forbade me, saying that I must "
    "have no other object in view in getting the plates but to glorify God, "
    "and must not be influenced by any other motive than that of building "
    "his kingdom; otherwise I could not get them."
    "\n\n"
    "“After this third visit, he again ascended into heaven as before, and "
    "I was again left to ponder on the strangeness of what I had just "
    "experienced; when almost immediately after the heavenly messenger had "
    "ascended from me for the third time, the cock crowed, and I found that "
    "day was approaching, so that our interviews must have occupied the "
    "whole of that night."
    "\n\n"
    "“I shortly after arose from my bed, and, as usual, went to the "
    "necessary labors of the day; but, in attempting to work as at other "
    "times, I found my strength so exhausted as to render me entirely "
    "unable. My father, who was laboring along with me, discovered something "
    "to be wrong with me, and told me to go home. I started with the "
    "intention of going to the house; but, in attempting to cross the fence "
    "out of the field where we were, my strength entirely failed me, and I "
    "fell helpless on the ground, and for a time was quite unconscious of "
    "anything."
    "\n\n"
    "“The first thing that I can recollect was a voice speaking unto me, "
    "calling me by name. I looked up, and beheld the same messenger standing "
    "over my head, surrounded by light as before. He then again related unto "
    "me all that he had related to me the previous night, and commanded me "
    "to go to my father and tell him of the vision and commandments which I "
    "had received."
    "\n\n"
    "“I obeyed; I returned to my father in the field, and rehearsed the "
    "whole matter to him. He replied to me that it was of God, and told me "
    "to go and do as commanded by the messenger. I left the field, and went "
    "to the place where the messenger had told me the plates were deposited; "
    "and owing to the distinctness of the vision which I had had concerning "
    "it, I knew the place the instant that I arrived there."
    "\n\n"
    "“Convenient to the village of Manchester, Ontario county, New York, "
    "stands a hill of considerable size, and the most elevated of any in the "
    "neighborhood. On the west side of this hill, not far from the top, "
    "under a stone of considerable size, lay the plates, deposited in a "
    "stone box. This stone was thick and rounding in the middle on the upper "
    "side, and thinner towards the edges, so that the middle part of it was "
    "visible above the ground, but the edge all around was covered with "
    "earth."
    "\n\n"
    "“Having removed the earth, I obtained a lever, which I got fixed under "
    "the edge of the stone, and with a little exertion raised it up. I "
    "looked in, and there indeed did I behold the plates, the Urim and "
    "Thummim, and the breastplate, as stated by the messenger. The box in "
    "which they lay was formed by laying stones together in some kind of "
    "cement. In the bottom of the box were laid two stones crossways of the "
    "box, and on these stones lay the plates and the other things with them."
    "\n\n"
    "“I made an attempt to take them out, but was forbidden by the "
    "messenger, and was again informed that the time for bringing them forth "
    "had not yet arrived, neither would it, until four years from that time; "
    "but he told me that I should come to that place precisely in one year "
    "from that time, and that he would there meet with me, and that I should "
    "continue to do so until the time should come for obtaining the plates."
    "\n\n"
    "“Accordingly, as I had been commanded, I went at the end of each year, "
    "and at each time I found the same messenger there, and received "
    "instruction and intelligence from him at each of our interviews, "
    "respecting what the Lord was going to do, and how and in what manner "
    "his kingdom was to be conducted in the last days. …"
    "\n\n"
    "“At length the time arrived for obtaining the plates, the Urim and "
    "Thummim, and the breastplate. On the twenty-second day of September, "
    "one thousand eight hundred and twenty-seven, having gone as usual at "
    "the end of another year to the place where they were deposited, the "
    "same heavenly messenger delivered them up to me with this charge: that "
    "I should be responsible for them; that if I should let them go "
    "carelessly, or through any neglect of mine, I should be cut off; but "
    "that if I would use all my endeavors to preserve them, until he, the "
    "messenger, should call for them, they should be protected."
    "\n\n"
    "“I soon found out the reason why I had received such strict charges to "
    "keep them safe, and why it was that the messenger had said that when I "
    "had done what was required at my hand, he would call for them. For no "
    "sooner was it known that I had them, than the most strenuous exertions "
    "were used to get them from me. Every stratagem that could be invented "
    "was resorted to for that purpose. The persecution became more bitter "
    "and severe than before, and multitudes were on the alert continually to "
    "get them from me if possible. But by the wisdom of God, they remained "
    "safe in my hands, until I had accomplished by them what was required at "
    "my hand. When, according to arrangements, the messenger called for "
    "them, I delivered them up to him; and he has them in his charge until "
    "this day, being the second day of May, one thousand eight hundred and "
    "thirty-eight.”"
    "\n\n"
    "For a more complete account, see Joseph Smith—History in the Pearl of "
    "Great Price."
    "\n\n"
    "The ancient record thus brought forth from the earth as the voice of a "
    "people speaking from the dust, and translated into modern speech by the "
    "gift and power of God as attested by Divine affirmation, was first "
    "published to the world in the year 1830 as The Book of Mormon."
)

JS_SM = (
    "O upu nei a le Perofeta o Iosefa Samita lava ia, e uiga i le o'o mai o "
    "le Tusi a Mamona:"
    "\n\n"
    "“O le po o le … aso luasefulu-tasi o Setema [1823] … na ou tatalo ma "
    "aioi atu ai i le Atua Malosi Aoao. …"
    "\n\n"
    "“A o faapea ona ou valaau atu i le Atua, sa ou vaaia se malamalama ua "
    "o'o mai i lo'u potu, sa faaauau pea ona faateleina seia o'o ina sili "
    "atu le malamalama o le potu nai lo le aoauli, ae faafuasei loa ona "
    "faaali mai o se tagata i tafatafa o lo'u moega, ua tulai i le 'ea, ona "
    "sa lē papa'i ona vae i le fola."
    "\n\n"
    "“Sa ofu o ia i se ofu talaloa sa matuā pa'epa'e lava. O se pa'epa'e sa "
    "silisili atu nai lo soo se mea faalelalolagi ua ou vaai i ai; pe ou te "
    "talitonu foi e mafai ona faia o se mea faalelalolagi ia foliga mai "
    "faapea lona pa'epa'e tele ma iila. Sa aliali mai ona lima, ma ona "
    "ogalima foi, i luga a'e teisi o le tapulima; sa faapea foi, ona aliali "
    "mai o ona vae, faapea ma ona ogavae, i luga a'e teisi o tapuvae. Sa lē "
    "ufitia foi lona ao ma lona ua. Sa mafai ona ou iloaina, sa leai se isi "
    "ona ofu sa ofuina ae na o lea ofu talaloa, ona sa matala sa mafai ai "
    "ona ou vaai atu i lona fatafata."
    "\n\n"
    "“Sa le gata ina matuā pa'epa'e tele lona ofu talaloa, ae sa matuā "
    "mamalu tele lona tagata atoa e le mafai ona faamatalaina, ma o ona "
    "fofoga sa pei moni lava o le uilaemo. Sa matuā malamalama lava le potu, "
    "ae sa le sili atu le susulu e pei o lea na siomia ai lona tagata. O le "
    "taimi muamua lava na ou vaai atu ai ia te ia, sa ou fefe; peitai sa "
    "vave ona tea ese atu o le fefe mai ia te a'u."
    "\n\n"
    "“Sa ia fetalai mai ia te a'u i lo'u igoa, ma fai mai ia te a'u o ia o "
    "se avefeau na auina mai i le afioaga o le Atua ia te a'u, ma o lona "
    "igoa o Moronae; ma o loo i ai i le Atua se galuega mo a'u ou te faia; "
    "ma o le a tauleleia ma tauleagaina lo'u igoa i atunuu uma, ituaiga, ma "
    "gagana, pe o le a tauleleia ma tauleagaina i totonu o tagata uma."
    "\n\n"
    "“Sa ia fetalai mai o loo i ai se tusi ua teuina, ua tusia i luga o "
    "papatusi auro, o loo tuuina mai ai se tala o tagata muamua sa nonofo i "
    "le konetineta lenei, ma le mea na latou tupuga mai ai. Sa fetalai mai "
    "foi o ia o loo i ai i totonu le atoatoaga o le Talalelei tumau e "
    "faavavau, e pei ona tuuina atu e le Faaola i tagata anamua;"
    "\n\n"
    "“Faapea foi, sa i ai ni maa se lua ua i totonu o ni faavaa "
    "siliva—ma o ia maa, sa faapipii i se ufifatafata, ua ta'ua o le Urima "
    "ma le Tumena—ua teu faatasi ma papatusi; ma o le umia ma le faaaogaina "
    "o ia maa sa tā'ua ai tagata anamua po o taimi muamua o 'tagatavāai'; "
    "ma ua saunia e le Atua ia maa mo le faamoemoe o le faaliliuina o le "
    "tusi. …"
    "\n\n"
    "“Sa toe fetalai mai o ia ia te ā'u, a 'ou mauaina ia papatusi ua "
    "fetalai i ai o ia—ona e le i o'o i le taimi e tatau ona maua mai "
    "ai—ia aua ne'i ou faaalia atu i se tasi; po o le ufifatafata ma le "
    "Urima ma le Tumena; ae ia tau lava o i latou o le a poloaiina ai a'u ia "
    "faaali atu i ai; afai ou te faaalia atu i soo se tasi, o le a faaumatia "
    "a'u. A o fetalai mai o ia ia te a'u e uiga i papatusi, sa tatala mai se "
    "faaaliga i lo'u mafaufau sa mafai ai ona ou vaai i le mea sa teu ai "
    "papatusi, ma sa matua manino ma malamalama lelei le faaaliga vaaia sa "
    "ou toe iloa lelei ai lea mea ina ua ou asiasi atu i ai."
    "\n\n"
    "“Ina ua mavae lenei fesootaiga, sa ou vaai atu i le malamalama sa i "
    "totonu o le potu ua amata ona faapotopoto vave ane faataamilo i le tino "
    "o le tagata sa fetalai mai ia te a'u, ma sa faapea lava ona faia se'ia "
    "o'o ina toe tuua le potu i le pogisa, vagana ai le faataamilo latalata "
    "ane ia te ia; ae faafuasei loa, ona ou vaai, i le taimi lava lea, i se "
    "avanoa faaniutu ua matala sa'o a'e lava i le lagi ma sa afio a'e o ia "
    "se'ia o'o lava ina mou ese atu atoa o ia, ma tuua ai le potu e pei ona "
    "sa i ai ae lei o'o mai lea malamalama mai le lagi."
    "\n\n"
    "“Sa ou taoto ma mafaufau i le uiga ese o lenei mea na ou vaaia, ma le "
    "ofo tele i mea na ta'u mai ia te a'u e lenei avefeau uiga ese; ae, a o "
    "ou mafaufau loloto i ia mea, sa faafuasei ona ou iloa ua amata ona toe "
    "malamalama lo'u potu, ma sa le'i pine, i lea lava taimi, ae toe tu mai "
    "lea lava avefeau mai le lagi i tafatafa o lo'u moega."
    "\n\n"
    "“Sa ia amata, ma toe faamatala mai mea lava ia e tasi na ia faia i "
    "lana asiasiga muamua, e aunoa ma se eseesega tele; ina ua uma, sa ia "
    "ta'u mai ia te a'u e uiga i faamasinoga matautia o le a o'o mai i luga "
    "o le lalolagi, ma faafanoga tetele e ala mai i oge, le pelu, ma "
    "faama'i; ma o nei faamasinoga mamafa o le a o'o mai i luga o le "
    "lalolagi i le tupulaga lenei. Ina ua uma ona ia faamatala mai o nei "
    "mea, sa toe afio a'e o ia e pei ona ia faia muamua."
    "\n\n"
    "“E o'o mai i lea taimi, sa matua loloto lava uunaiga sa o'o mai i lo'u "
    "mafaufau, sa sola ese le fia moe mai i o'u mata, ma sa ou taoto ma le "
    "lofituina i le maofa tele i mea na ou vaaia ma faalogoina. Ae sa ou "
    "ofo, ina ua ou toe vaaia lea lava avefeau e tasi i tafatafa o lo'u "
    "moega, ma faalogo atu ia te ia ua toe faamatala pe ua toe ta'u mai ia "
    "te a'u mea uma lava ia e pei o taimi muamua; ma faaopoopo mai se "
    "lapataiga ia te a'u, ua fetalai mai ia te a'u o le a taumafai Satani e "
    "faaosooso a'u (ona o le tulaga mativa o le aiga o lo'u tamā), ia ou "
    "aumai papatusi mo le faamoemoe ia ou mauoa ai. O lenei mea sa faasa mai "
    "e ia ia te a'u, fai mai ia aua ne'i i ai ia te a'u se isi lava "
    "faamoemoe mo le mauaina mai o papatusi tau lava mo le viiga o le Atua, "
    "ma ia aua lava ne'i tosina a'u i se isi lava manatu nai lo le faatuina "
    "o lona malo; a leai e lē mafai ona ou mauaina papatusi."
    "\n\n"
    "“Ina ua mavae lenei asiasiga lona tolu, sa toe afio a'e o ia i le lagi "
    "e pei o taimi muamua, ma toe tuu ai a'u ou te mafaufau loloto i le uiga "
    "ese o mea na faatoa o'o mai nei ia te a'u; ae le'i umi lava ona mavae "
    "le afio a'e o le avefeau faalelagi mai ia te a'u mo le taimi lona tolu "
    "lea, ae vivini loa moa, ma ou iloa ai ua lata mai le ao, o lona uiga o "
    "a ma talanoaga atonu na alu ai lena po atoa."
    "\n\n"
    "“Sa lei umi ona mavae lena ae ou tu a'e mai lo'u moega, ma, e pei ona "
    "masani ai, sa ou alu atu i galuega tatau ai o le aso; peitai, a'o ou "
    "taumafai e galue e pei o i isi taimi, sa ou iloa ua matuā leai lava "
    "so'u malosi sa lē mafai ona ou faia o se mea. O lo'u tamā, o lē sa ma "
    "galulue faatasi, sa ia iloa mai e i ai se mea ua faaletonu ia te a'u, "
    "ma sa fai mai ia te a'u ou te alu i le fale. Sa ou amata loa ma le "
    "faamoemoe ou te alu i le fale; peitai, a'o ou taumafai e sopoia le pa "
    "ou te alu ese atu ai mai le fanua sa ma i ai, sa matuā leai lava so'u "
    "malosi, ma sa ou pa'ū ifo i le eleele, ma sa ou lē iloa ai se mea mo "
    "se taimi."
    "\n\n"
    "“O le mea muamua lava e mafai ona ou manatua o se leo na fetalai mai "
    "ia te a'u, ua fetalai mai ia te a'u i lo'u igoa. Sa ou tepa a'e i luga, "
    "ma ou vaai atu i lea lava avefeau e tasi o tulai mai i luga a'e o lo'u "
    "ulu, ua siomia i le malamalama e pei o taimi muamua. Ona ia toe "
    "faamatala mai foi lea ia te a'u o mea uma sa ia faamatala mai ia te a'u "
    "i le po ua mavae, ma poloai mai ia te a'u ia ou alu i lo'u tamā ma "
    "faamatala atu ia te ia e uiga i le faaaliga vaaia ma poloaiga na ou "
    "mauaina."
    "\n\n"
    "“Sa ou usitai; sa ou foi atu i lo'u tamā i le fanua, ma faamatala atu "
    "ia te ia le mea atoa. Sa tali mai o ia ia te a'u o se mea ua mai i le "
    "Atua, ma fai mai ia te a'u ou te alu ma fai e pei ona faatonuina ai e "
    "le avefeau. Sa ou tuua loa le fanua, ma ou alu i le mea na ta'u mai e "
    "le avefeau ia te a'u o loo teu ai papatusi; ma ona o le manino lelei o "
    "le faaaliga vaaia na o'o mai ia te a'u e uiga i lenei mea, sa ou iloa "
    "lelei lava le nofoaga i le taimi lava na ou taunuu i ai."
    "\n\n"
    "“E latalata i le nuu o Manaseta, i le itumalo o Onatario, i Niu Ioka, "
    "o loo tu ai se maupu'epu'e telē lava, ma ua sili ona maualuga i soo se "
    "maupu'epu'e i lena vaiaai. I le itu i sisifo o lenei maupu'epu'e, e le "
    "mamao mai le tumutumu, i lalo o se maa telē lava, sa taatitia ai "
    "papatusi, sa teuina i totonu o se pusa maa. O lenei maa sa mafiafia ma "
    "lapotopoto i le ogatotonu i le itu i luga, ma manifinifi i le faasolo "
    "atu i pito, ma aliali ai lona ogatotonu i luga o le eleele, ae o pito "
    "uma faataamilo sa ufitia i le eleele."
    "\n\n"
    "“Ina ua uma ona ou eli ese o le eleele, sa ou aveane se laau, ma ou "
    "sulu le isi pito i lalo o autafa o le maa, ma laga i luga i sina "
    "uunaiga itiiti. Sa ou tilotilo i totonu, ma o iina moni lava sa ou vaai "
    "ai i papatusi, le Urima ma le Tumena, ma le ufifatafata, e pei ona "
    "faamatala mai e le avefeau. O le pusa sa taatitia ai i totonu sa faia i "
    "le faapipii faatasi o ni maa i se ituaiga o simā. I le ta'ele o le "
    "pusa sa faataatitia faafelavasai ai ni maa se lua, ma o luga o ia maa "
    "sa taatitia ai papatusi ma isi mea sa tuufaatasi ai."
    "\n\n"
    "“Sa ou faia se taumafaiga e aumai i fafo ia mea, peitai sa faasaina "
    "a'u e le avefeau, ma ia toe faailoa mai ia te a'u, e lei o'o i le taimi "
    "e aumai ai, ma e le tu'uina mai lava, sei o'o i le fa o tausaga mai le "
    "taimi lena; ae sa fetalai mai o ia ia te a'u ia ou sau i le mea lena i "
    "le taimi tonu lava e atoa i ai le tausaga mai le taimi lena, ma o le a "
    "ia feiloai ai ma a'u iina, ma ia faapea lava ona ou faia se'ia o'o i le "
    "taimi mo le mauaina o papatusi."
    "\n\n"
    "“Sa faapea lava, e pei ona poloaiina ai a'u, ona ou alu i le faaiuga o "
    "tausaga taitasi, ma o taimi taitasi uma na ou alu atu ai na ou maua ai "
    "lea lava avefeau iina, ma maua mai ia te ia faatonuga ma le malamalama "
    "i taimi taitasi o a ma talanoaga, e faatatau i mea o le a faia e le "
    "Alii, ma le ala ma le auala e taitai ai lona malo i aso e gata ai. …"
    "\n\n"
    "“Sa o'o ina o'o mai le taimi mo le mauaina mai o papatusi, le Urima ma "
    "le Tumena, ma le ufifatafata. O le aso luasefulu-lua o Setema, i le "
    "tausaga e tasi le afe valu selau luasefulu ma le fitu, ina ua ou alu "
    "atu e pei ona masani ai i le faaiuga o se isi tausaga i le mea sa teu "
    "ai papatusi, na tuu mai ai ia te a'u e lea lava avefeau faalelagi ia "
    "mea ma le poloaiga lenei: ua ia te a'u le tausiga o ia mea; ma afai ou "
    "te tuusolo ma le faatalalē ia mea, po o so'u faatamala i ai, o le a "
    "vavaeeseina a'u; ae afai ou te faaaoga a'u taumafaiga uma e faasaoina "
    "ia mea, se'ia o'o ina sau o ia, le avefeau lea, mo ia mea, o le a "
    "puipuia lava i latou."
    "\n\n"
    "“Sa vave ona ou iloa le pogai na ou maua ai poloaiga patino ia ou "
    "tausi saogalemu ia mea, ma le pogai na fetalai mai ai le avefeau a uma "
    "ona ou faataunuuina o le galuega ua tuu mai i o'u lima, o le a sau o ia "
    "mo i latou. Ona e lei pine ona iloa ua ia te a'u ia mea, ae faaaoga e "
    "tagata taumafaiga malolosi e faoeseina ai mai ia te a'u. Sa faaaoga soo "
    "se togafiti sa mafai ona faia mo lena faamoemoe. Sa o'o ina sili atu le "
    "matuitui ma le tiga o sauaga nai lo le taimi muamua, ma sa mata'i pea "
    "lava pea e motu o tagata avanoa latou te fao ai ia mea mai ia te a'u pe "
    "a mafai. Peitai ona o le poto o le Atua, sa saogalemu pea ia mea i o'u "
    "lima, seia o'o ina mae'a ona ou faataunuuina o le galuega sa manaomia "
    "mai lo'u lima. Ma ina ua mae'a e tusa ai ma tuutuuga, sa toe afio mai "
    "le avefeau, mo ia mea, ma sa ou tuu atu ai ia te ia; ma ua i ai ia te "
    "ia ia mea i lana vaaiga e o'o mai i le aso nei, le aso lua lea o Me, o "
    "le tasi le afe valu selau tolusefulu ma le valu.”"
    "\n\n"
    "Mo se tala atoa, tagai i le Iosefa Samita—Talafaasolopito i le Penina "
    "Tau Tele."
    "\n\n"
    "O le talafaamaumau mai anamua sa faapea ona aumai mai le eleele e pei o "
    "le leo o se nuu ua tautala mai i le efuefu, ma faaliliuina i le gagana "
    "o ona po nei e ala i le meaalofa ma le mana o le Atua e pei ona "
    "faamaonia i se faamaoniga Paia, sa muai lomia ma faasalalauina i le "
    "lalolagi i le gagana Peretania i le tausaga e 1830, The Book of Mormon "
    "(O LE TUSI A MAMONA)."
)

JS_CELLS = [
    # — Attribution line —
    ("O upu nei", "These are the words"),
    ("a le Perofeta", "of the Prophet"),
    ("o Iosefa Samita", "Joseph Smith"),
    ("lava ia,", "his own,"),
    ("e uiga i", "about"),
    ("le o'o mai", "the coming forth"),
    ("o le Tusi a Mamona:", "of the Book of Mormon:"),
    # — P1 —
    ("“O le po o le …", "“On the evening of the …"),
    ("aso luasefulu-tasi", "twenty-first"),
    ("o Setema [1823] …", "of September [1823] …"),
    ("na ou tatalo", "I betook myself to prayer"),
    ("ma aioi atu ai", "and supplication"),
    ("i le Atua", "unto God"),
    ("Malosi Aoao. …", "the Almighty. …"),
    # — P2 —
    ("“A o faapea", "“While I was thus"),
    ("ona ou valaau atu", "in the act of calling"),
    ("i le Atua,", "upon God,"),
    ("sa ou vaaia", "I discovered"),
    ("se malamalama", "a light"),
    ("ua o'o mai i lo'u potu,", "appearing in my room,"),
    ("sa faaauau pea ona faateleina", "which continued to increase"),
    ("seia o'o ina sili atu", "until was lighter"),
    ("le malamalama", "the light"),
    ("o le potu", "of the room"),
    ("nai lo le aoauli,", "than at noonday,"),
    ("ae faafuasei loa", "when immediately"),
    ("ona faaali mai", "appeared"),
    ("o se tagata", "a personage"),
    ("i tafatafa o lo'u moega,", "at my bedside,"),
    ("ua tulai i le 'ea,", "standing in the air,"),
    ("ona sa lē papa'i", "for did not touch"),
    ("ona vae", "his feet"),
    ("i le fola.", "the floor."),
    # — P3 —
    ("“Sa ofu o ia", "“He had on"),
    ("i se ofu talaloa", "a loose robe"),
    ("sa matuā pa'epa'e lava.", "of most exquisite whiteness."),
    ("O se pa'epa'e", "It was a whiteness"),
    ("sa silisili atu", "beyond"),
    ("nai lo", "than"),
    ("soo se mea faalelalolagi", "anything earthly"),
    ("ua ou vaai i ai;", "I had ever seen;"),
    ("pe ou te talitonu foi", "nor do I believe"),
    ("e mafai ona faia", "could be made"),
    ("o se mea faalelalolagi", "that any earthly thing"),
    ("ia foliga mai faapea", "to appear so"),
    ("lona pa'epa'e tele ma iila.", "exceedingly white and brilliant."),
    ("Sa aliali mai ona lima,", "His hands were naked,"),
    ("ma ona ogalima foi,", "and his arms also,"),
    ("i luga a'e teisi", "a little above"),
    ("o le tapulima;", "the wrist;"),
    ("sa faapea foi,", "so, also,"),
    ("ona aliali mai", "were naked"),
    ("o ona vae,", "his feet,"),
    ("faapea ma ona ogavae,", "as were his legs,"),
    ("i luga a'e teisi", "a little above"),
    ("o tapuvae.", "the ankles."),
    ("Sa lē ufitia foi", "were also bare"),
    ("lona ao ma lona ua.", "his head and neck."),
    ("Sa mafai ona ou iloaina,", "I could discover,"),
    ("sa leai se isi", "that he had no other"),
    ("ona ofu sa ofuina", "clothing on"),
    ("ae na o", "but only"),
    ("lea ofu talaloa,", "this robe,"),
    ("ona sa matala", "as it was open,"),
    ("sa mafai ai", "so that I could"),
    ("ona ou vaai atu", "see"),
    ("i lona fatafata.", "into his bosom."),
    # — P4 —
    ("“Sa le gata ina", "“Not only was"),
    ("matuā pa'epa'e tele", "exceedingly white"),
    ("lona ofu talaloa,", "his robe,"),
    ("ae sa matuā mamalu tele", "but was glorious"),
    ("lona tagata atoa", "his whole person"),
    ("e le mafai ona faamatalaina,", "beyond description,"),
    ("ma o ona fofoga", "and his countenance"),
    ("sa pei moni lava", "truly like"),
    ("o le uilaemo.", "lightning."),
    ("Sa matuā malamalama lava", "was exceedingly light"),
    ("le potu,", "the room,"),
    ("ae sa le sili atu", "but not so very bright"),
    ("le susulu", "the brightness"),
    ("e pei o lea", "as"),
    ("na siomia ai", "immediately around"),
    ("lona tagata.", "his person."),
    ("O le taimi muamua lava", "When first"),
    ("na ou vaai atu ai", "I looked"),
    ("ia te ia,", "upon him,"),
    ("sa ou fefe;", "I was afraid;"),
    ("peitai sa vave", "but soon"),
    ("ona tea ese atu", "departed"),
    ("o le fefe", "the fear"),
    ("mai ia te a'u.", "from me."),
    # — P5 —
    ("“Sa ia fetalai mai", "“He spake"),
    ("ia te a'u", "unto me"),
    ("i lo'u igoa,", "by my name,"),
    ("ma fai mai ia te a'u", "and said unto me"),
    ("o ia o se avefeau", "that he was a messenger"),
    ("na auina mai", "sent"),
    ("i le afioaga", "from the presence"),
    ("o le Atua", "of God"),
    ("ia te a'u,", "to me,"),
    ("ma o lona igoa", "and his name"),
    ("o Moronae;", "was Moroni;"),
    ("ma o loo i ai", "that there was"),
    ("i le Atua", "with God"),
    ("se galuega mo a'u", "a work for me"),
    ("ou te faia;", "to do;"),
    ("ma o le a tauleleia", "and shall be spoken of for good"),
    ("ma tauleagaina", "and evil"),
    ("lo'u igoa", "my name"),
    ("i atunuu uma,", "among all nations,"),
    ("ituaiga, ma gagana,", "kindreds, and tongues,"),
    ("pe o le a tauleleia", "or shall be spoken well"),
    ("ma tauleagaina", "and ill of"),
    ("i totonu o tagata uma.", "among all people."),
    # — P6 —
    ("“Sa ia fetalai mai", "“He said"),
    ("o loo i ai se tusi", "there was a book"),
    ("ua teuina,", "deposited,"),
    ("ua tusia", "written"),
    ("i luga o papatusi auro,", "upon gold plates,"),
    ("o loo tuuina mai ai", "giving"),
    ("se tala", "an account"),
    ("o tagata muamua", "of the former inhabitants"),
    ("sa nonofo", "who dwelt"),
    ("i le konetineta lenei,", "on this continent,"),
    ("ma le mea", "and the source"),
    ("na latou tupuga mai ai.", "whence they sprang."),
    ("Sa fetalai mai foi o ia", "He also said"),
    ("o loo i ai i totonu", "was contained in it"),
    ("le atoatoaga", "that the fulness"),
    ("o le Talalelei", "of the Gospel"),
    ("tumau e faavavau,", "everlasting,"),
    ("e pei ona tuuina atu", "as delivered"),
    ("e le Faaola", "by the Savior"),
    ("i tagata anamua;", "to the ancient inhabitants;"),
    # — P7 —
    ("“Faapea foi,", "“Also,"),
    ("sa i ai", "that there were"),
    ("ni maa se lua", "two stones"),
    ("ua i totonu o", "in"),
    ("ni faavaa siliva—", "silver bows—"),
    ("ma o ia maa,", "and these stones,"),
    ("sa faapipii i se ufifatafata,", "fastened to a breastplate,"),
    ("ua ta'ua o", "constituted what is called"),
    ("le Urima ma le Tumena—", "the Urim and Thummim—"),
    ("ua teu faatasi ma papatusi;", "deposited with the plates;"),
    ("ma o le umia", "and the possession"),
    ("ma le faaaogaina", "and use"),
    ("o ia maa", "of these stones"),
    ("sa tā'ua ai", "were what constituted"),
    ("tagata anamua po o taimi muamua", "in ancient or former times"),
    ("o 'tagatavāai';", "‘seers’;"),
    ("ma ua saunia e le Atua", "and God had prepared"),
    ("ia maa", "these stones"),
    ("mo le faamoemoe", "for the purpose"),
    ("o le faaliliuina", "of translating"),
    ("o le tusi. …", "the book. …"),
    # — P8 —
    ("“Sa toe fetalai mai o ia", "“Again, he told"),
    ("ia te ā'u,", "me,"),
    ("a 'ou mauaina ia papatusi", "that when I got those plates"),
    ("ua fetalai i ai o ia—", "of which he had spoken—"),
    ("ona e le i o'o", "for was not yet come"),
    ("i le taimi", "the time"),
    ("e tatau ona", "that should"),
    ("maua mai ai—", "be obtained—"),
    ("ia aua ne'i", "I should not"),
    ("ou faaalia atu", "show them"),
    ("i se tasi;", "to any person;"),
    ("po o le ufifatafata", "neither the breastplate"),
    ("ma le Urima", "with the Urim"),
    ("ma le Tumena;", "and Thummim;"),
    ("ae ia tau lava", "only"),
    ("o i latou", "to those"),
    ("o le a poloaiina ai a'u", "to whom I should be commanded"),
    ("ia faaali atu i ai;", "to show them;"),
    ("afai ou te faaalia atu", "if I did show them"),
    ("i soo se tasi,", "to any one,"),
    ("o le a faaumatia a'u.", "I should be destroyed."),
    ("A o fetalai mai o ia", "While he was conversing"),
    ("ia te a'u", "with me"),
    ("e uiga i papatusi,", "about the plates,"),
    ("sa tatala mai se faaaliga", "the vision was opened"),
    ("i lo'u mafaufau", "to my mind"),
    ("sa mafai ai", "that I could"),
    ("ona ou vaai", "see"),
    ("i le mea", "the place"),
    ("sa teu ai papatusi,", "where the plates were deposited,"),
    ("ma sa matua manino", "and so clearly"),
    ("ma malamalama lelei", "and distinctly"),
    ("le faaaliga vaaia", "the vision"),
    ("sa ou toe iloa lelei ai", "that I knew again"),
    ("lea mea", "the place"),
    ("ina ua ou asiasi atu", "when I visited"),
    ("i ai.", "it."),
    # — P9 —
    ("“Ina ua mavae lenei fesootaiga,", "“After this communication,"),
    ("sa ou vaai atu", "I saw"),
    ("i le malamalama", "the light"),
    ("sa i totonu o le potu", "in the room"),
    ("ua amata ona faapotopoto", "begin to gather"),
    ("vave ane", "immediately"),
    ("faataamilo", "around"),
    ("i le tino o le tagata", "the person of him"),
    ("sa fetalai mai ia te a'u,", "who had been speaking to me,"),
    ("ma sa faapea lava", "and it continued"),
    ("ona faia", "to do so"),
    ("se'ia o'o ina toe tuua", "until again was left"),
    ("le potu", "the room"),
    ("i le pogisa,", "dark,"),
    ("vagana ai", "except"),
    ("le faataamilo latalata ane", "just around"),
    ("ia te ia;", "him;"),
    ("ae faafuasei loa,", "when, instantly"),
    ("ona ou vaai,", "I saw,"),
    ("i le taimi lava lea,", "as it were,"),
    ("i se avanoa faaniutu", "a conduit"),
    ("ua matala sa'o a'e lava", "open right up"),
    ("i le lagi", "into heaven,"),
    ("ma", "and"),
    ("sa afio a'e o ia", "he ascended"),
    ("se'ia o'o lava ina", "till"),
    ("mou ese atu atoa o ia,", "he entirely disappeared,"),
    ("ma tuua ai le potu", "and the room was left"),
    ("e pei ona sa i ai", "as it had been"),
    ("ae lei o'o mai", "before had made its appearance"),
    ("lea malamalama mai le lagi.", "this heavenly light."),
    # — P10 —
    ("“Sa ou taoto ma mafaufau", "“I lay musing"),
    ("i le uiga ese", "on the singularity"),
    ("o lenei mea", "of this thing"),
    ("na ou vaaia,", "I had seen,"),
    ("ma le ofo tele", "and marveling greatly"),
    ("i mea na ta'u mai", "at what was told"),
    ("ia te a'u", "to me"),
    ("e lenei avefeau uiga ese;", "by this extraordinary messenger;"),
    ("ae, a o ou mafaufau loloto", "when, in my deep meditation"),
    ("i ia mea,", "on these things,"),
    ("sa faafuasei ona ou iloa", "I suddenly discovered"),
    ("ua amata ona toe malamalama", "was again beginning to lighten"),
    ("lo'u potu,", "my room,"),
    ("ma sa le'i pine,", "and in an instant,"),
    ("i lea lava taimi,", "as it were,"),
    ("ae toe tu mai", "was again standing"),
    ("lea lava avefeau", "the same messenger"),
    ("mai le lagi", "from heaven"),
    ("i tafatafa o lo'u moega.", "by my bedside."),
    # — P11 —
    ("“Sa ia amata,", "“He commenced,"),
    ("ma toe faamatala mai", "and again related"),
    ("mea lava ia e tasi", "the very same things"),
    ("na ia faia", "which he had done"),
    ("i lana asiasiga muamua,", "at his first visit,"),
    ("e aunoa ma se eseesega tele;", "without the least variation;"),
    ("ina ua uma,", "which having done,"),
    ("sa ia ta'u mai", "he informed"),
    ("ia te a'u", "me"),
    ("e uiga i faamasinoga matautia", "of great judgments"),
    ("o le a o'o mai", "which were coming"),
    ("i luga o le lalolagi,", "upon the earth,"),
    ("ma faafanoga tetele", "with great desolations"),
    ("e ala mai i", "by"),
    ("oge, le pelu, ma faama'i;", "famine, sword, and pestilence;"),
    ("ma o nei faamasinoga mamafa", "and that these grievous judgments"),
    ("o le a o'o mai", "would come"),
    ("i luga o le lalolagi", "on the earth"),
    ("i le tupulaga lenei.", "in this generation."),
    ("Ina ua uma", "Having"),
    ("ona ia faamatala mai", "related"),
    ("o nei mea,", "these things,"),
    ("sa toe afio a'e o ia", "he again ascended"),
    ("e pei ona ia faia muamua.", "as he had done before."),
    # — P12 —
    ("“E o'o mai", "“By"),
    ("i lea taimi,", "this time,"),
    ("sa matua loloto lava uunaiga", "so deep were the impressions"),
    ("sa o'o mai i lo'u mafaufau,", "made on my mind,"),
    ("sa sola ese le fia moe", "that sleep had fled"),
    ("mai i o'u mata,", "from my eyes,"),
    ("ma sa ou taoto", "and I lay"),
    ("ma le lofituina", "overwhelmed"),
    ("i le maofa tele", "in astonishment"),
    ("i mea na ou vaaia", "at what I had seen"),
    ("ma faalogoina.", "and heard."),
    ("Ae sa ou ofo,", "But what was my surprise"),
    ("ina ua ou toe vaaia", "when again I beheld"),
    ("lea lava avefeau e tasi", "the same messenger"),
    ("i tafatafa o lo'u moega,", "at my bedside,"),
    ("ma faalogo atu ia te ia", "and heard him"),
    ("ua toe faamatala", "rehearse"),
    ("pe ua toe ta'u mai", "or repeat over again"),
    ("ia te a'u", "to me"),
    ("mea uma lava ia", "the same things"),
    ("e pei o taimi muamua;", "as before;"),
    ("ma faaopoopo mai se lapataiga", "and added a caution"),
    ("ia te a'u,", "to me,"),
    ("ua fetalai mai ia te a'u", "telling me"),
    ("o le a taumafai Satani", "that Satan would try"),
    ("e faaosooso a'u", "to tempt me"),
    ("(ona o le tulaga mativa", "(in consequence of the indigent circumstances"),
    ("o le aiga", "of the family"),
    ("o lo'u tamā),", "of my father),"),
    ("ia ou aumai papatusi", "to get the plates"),
    ("mo le faamoemoe", "for the purpose"),
    ("ia ou mauoa ai.", "of getting rich."),
    ("O lenei mea", "This"),
    ("sa faasa mai e ia", "he forbade"),
    ("ia te a'u,", "me,"),
    ("fai mai", "saying"),
    ("ia aua ne'i i ai", "that I must have none"),
    ("ia te a'u", "to me"),
    ("se isi lava faamoemoe", "no other object in view"),
    ("mo le mauaina mai", "in getting"),
    ("o papatusi", "the plates"),
    ("tau lava mo le viiga", "but only to glorify"),
    ("o le Atua,", "God,"),
    ("ma ia aua lava ne'i", "and must not"),
    ("tosina a'u", "be influenced"),
    ("i se isi lava manatu", "by any other motive"),
    ("nai lo le faatuina", "than the building"),
    ("o lona malo;", "of his kingdom;"),
    ("a leai", "otherwise"),
    ("e lē mafai ona ou mauaina", "I could not get"),
    ("papatusi.", "them."),
    # — P13 —
    ("“Ina ua mavae", "“After"),
    ("lenei asiasiga lona tolu,", "this third visit,"),
    ("sa toe afio a'e o ia", "he again ascended"),
    ("i le lagi", "into heaven"),
    ("e pei o taimi muamua,", "as before,"),
    ("ma toe tuu ai a'u", "and I was again left"),
    ("ou te mafaufau loloto", "to ponder"),
    ("i le uiga ese o mea", "on the strangeness"),
    ("na faatoa o'o mai nei", "of what I had just experienced"),
    ("ia te a'u;", "to me;"),
    ("ae le'i umi lava", "when almost immediately"),
    ("ona mavae", "after"),
    ("le afio a'e", "had ascended"),
    ("o le avefeau faalelagi", "the heavenly messenger"),
    ("mai ia te a'u", "from me"),
    ("mo le taimi", "for the time"),
    ("lona tolu lea,", "the third,"),
    ("ae vivini loa moa,", "the cock crowed,"),
    ("ma ou iloa ai", "and I found"),
    ("ua lata mai le ao,", "that day was approaching,"),
    ("o lona uiga", "so that"),
    ("o a ma talanoaga", "our interviews"),
    ("atonu na alu ai", "must have occupied"),
    ("lena po atoa.", "that whole night."),
    # — P14 —
    ("“Sa lei umi", "“I shortly"),
    ("ona mavae lena", "after that"),
    ("ae ou tu a'e", "arose"),
    ("mai lo'u moega,", "from my bed,"),
    ("ma,", "and,"),
    ("e pei ona masani ai,", "as usual,"),
    ("sa ou alu atu", "went"),
    ("i galuega tatau ai", "to the necessary labors"),
    ("o le aso;", "of the day;"),
    ("peitai, a'o ou taumafai", "but, in attempting"),
    ("e galue", "to work"),
    ("e pei o i isi taimi,", "as at other times,"),
    ("sa ou iloa", "I found"),
    ("ua matuā leai lava", "so exhausted was"),
    ("so'u malosi", "my strength"),
    ("sa lē mafai ona ou faia", "as to render me unable"),
    ("o se mea.", "to do anything."),
    ("O lo'u tamā,", "My father,"),
    ("o lē", "who"),
    ("sa ma galulue faatasi,", "was laboring with me,"),
    ("sa ia iloa mai", "discovered"),
    ("e i ai se mea", "something"),
    ("ua faaletonu ia te a'u,", "to be wrong with me,"),
    ("ma sa fai mai", "and told"),
    ("ia te a'u", "me"),
    ("ou te alu i le fale.", "to go home."),
    ("Sa ou amata loa", "I started"),
    ("ma le faamoemoe", "with the intention"),
    ("ou te alu i le fale;", "of going to the house;"),
    ("peitai, a'o ou taumafai", "but, in attempting"),
    ("e sopoia le pa", "to cross the fence"),
    ("ou te alu ese atu ai", "to go out"),
    ("mai le fanua", "from the field"),
    ("sa ma i ai,", "where we were,"),
    ("sa matuā leai lava so'u malosi,", "my strength entirely failed me,"),
    ("ma sa ou pa'ū ifo", "and I fell down"),
    ("i le eleele,", "on the ground,"),
    ("ma sa ou lē iloa ai", "and knew nothing"),
    ("se mea", "of anything"),
    ("mo se taimi.", "for a time."),
    # — P15 —
    ("“O le mea muamua lava", "“The first thing"),
    ("e mafai ona ou manatua", "that I can recollect"),
    ("o se leo", "was a voice"),
    ("na fetalai mai ia te a'u,", "speaking unto me,"),
    ("ua fetalai mai ia te a'u", "calling me"),
    ("i lo'u igoa.", "by name."),
    ("Sa ou tepa a'e i luga,", "I looked up,"),
    ("ma ou vaai atu", "and beheld"),
    ("i lea lava avefeau e tasi", "the same messenger"),
    ("o tulai mai", "standing"),
    ("i luga a'e o lo'u ulu,", "over my head,"),
    ("ua siomia i le malamalama", "surrounded by light"),
    ("e pei o taimi muamua.", "as before."),
    ("Ona ia toe faamatala mai", "He then again related"),
    ("foi lea", "also"),
    ("ia te a'u", "unto me"),
    ("o mea uma", "all that"),
    ("sa ia faamatala mai", "he had related"),
    ("ia te a'u", "to me"),
    ("i le po ua mavae,", "the previous night,"),
    ("ma poloai mai ia te a'u", "and commanded me"),
    ("ia ou alu i lo'u tamā", "to go to my father"),
    ("ma faamatala atu ia te ia", "and tell him"),
    ("e uiga i le faaaliga vaaia", "of the vision"),
    ("ma poloaiga", "and commandments"),
    ("na ou mauaina.", "which I had received."),
    # — P16 —
    ("“Sa ou usitai;", "“I obeyed;"),
    ("sa ou foi atu", "I returned"),
    ("i lo'u tamā", "to my father"),
    ("i le fanua,", "in the field,"),
    ("ma faamatala atu ia te ia", "and rehearsed to him"),
    ("le mea atoa.", "the whole matter."),
    ("Sa tali mai o ia", "He replied"),
    ("ia te a'u", "to me"),
    ("o se mea", "that it was a thing"),
    ("ua mai i le Atua,", "of God,"),
    ("ma fai mai ia te a'u", "and told me"),
    ("ou te alu", "to go"),
    ("ma fai", "and do"),
    ("e pei ona faatonuina ai", "as commanded"),
    ("e le avefeau.", "by the messenger."),
    ("Sa ou tuua loa le fanua,", "I left the field,"),
    ("ma ou alu i le mea", "and went to the place"),
    ("na ta'u mai e le avefeau", "where the messenger had told"),
    ("ia te a'u", "me"),
    ("o loo teu ai papatusi;", "the plates were deposited;"),
    ("ma ona o le manino lelei", "and owing to the distinctness"),
    ("o le faaaliga vaaia", "of the vision"),
    ("na o'o mai ia te a'u", "which I had had"),
    ("e uiga i lenei mea,", "concerning it,"),
    ("sa ou iloa lelei lava", "I well knew"),
    ("le nofoaga", "the place"),
    ("i le taimi lava", "the instant"),
    ("na ou taunuu i ai.", "that I arrived there."),
    # — P17 —
    ("“E latalata i", "“Convenient to"),
    ("le nuu o Manaseta,", "the village of Manchester,"),
    ("i le itumalo o Onatario,", "Ontario county,"),
    ("i Niu Ioka,", "New York,"),
    ("o loo tu ai", "stands"),
    ("se maupu'epu'e telē lava,", "a hill of considerable size,"),
    ("ma ua sili ona maualuga", "and the most elevated"),
    ("i soo se maupu'epu'e", "of any hill"),
    ("i lena vaiaai.", "in that neighborhood."),
    ("I le itu i sisifo", "On the west side"),
    ("o lenei maupu'epu'e,", "of this hill,"),
    ("e le mamao mai", "not far from"),
    ("le tumutumu,", "the top,"),
    ("i lalo o", "under"),
    ("se maa telē lava,", "a stone of considerable size,"),
    ("sa taatitia ai papatusi,", "lay the plates,"),
    ("sa teuina", "deposited"),
    ("i totonu o se pusa maa.", "in a stone box."),
    ("O lenei maa", "This stone"),
    ("sa mafiafia ma lapotopoto", "was thick and rounding"),
    ("i le ogatotonu", "in the middle"),
    ("i le itu i luga,", "on the upper side,"),
    ("ma manifinifi", "and thinner"),
    ("i le faasolo atu i pito,", "towards the edges,"),
    ("ma aliali ai lona ogatotonu", "so that the middle part of it was visible"),
    ("i luga o le eleele,", "above the ground,"),
    ("ae o pito uma faataamilo", "but the edge all around"),
    ("sa ufitia i le eleele.", "was covered with earth."),
    # — P18 —
    ("“Ina ua uma", "“Having"),
    ("ona ou eli ese", "removed"),
    ("o le eleele,", "the earth,"),
    ("sa ou aveane se laau,", "I obtained a lever,"),
    ("ma ou sulu le isi pito", "which I got fixed"),
    ("i lalo o autafa", "under the edge"),
    ("o le maa,", "of the stone,"),
    ("ma laga i luga", "and raised it up"),
    ("i sina uunaiga itiiti.", "with a little exertion."),
    ("Sa ou tilotilo i totonu,", "I looked in,"),
    ("ma o iina moni lava", "and there indeed"),
    ("sa ou vaai ai", "did I behold"),
    ("i papatusi,", "the plates,"),
    ("le Urima ma le Tumena,", "the Urim and Thummim,"),
    ("ma le ufifatafata,", "and the breastplate,"),
    ("e pei ona faamatala mai", "as stated"),
    ("e le avefeau.", "by the messenger."),
    ("O le pusa", "The box"),
    ("sa taatitia ai i totonu", "in which they lay"),
    ("sa faia", "was formed"),
    ("i le faapipii faatasi", "by laying together"),
    ("o ni maa", "stones"),
    ("i se ituaiga o simā.", "in some kind of cement."),
    ("I le ta'ele o le pusa", "In the bottom of the box"),
    ("sa faataatitia faafelavasai ai", "were laid crossways"),
    ("ni maa se lua,", "two stones,"),
    ("ma o luga o ia maa", "and on these stones"),
    ("sa taatitia ai papatusi", "lay the plates"),
    ("ma isi mea", "and the other things"),
    ("sa tuufaatasi ai.", "with them."),
    # — P19 —
    ("“Sa ou faia se taumafaiga", "“I made an attempt"),
    ("e aumai i fafo", "to take out"),
    ("ia mea,", "them,"),
    ("peitai sa faasaina a'u", "but was forbidden"),
    ("e le avefeau,", "by the messenger,"),
    ("ma ia toe faailoa mai", "and was again informed"),
    ("ia te a'u,", "to me,"),
    ("e lei o'o", "had not yet arrived"),
    ("i le taimi", "the time"),
    ("e aumai ai,", "for bringing them forth,"),
    ("ma e le tu'uina mai", "neither would be given"),
    ("lava,", "at all,"),
    ("sei o'o", "until"),
    ("i le fa o tausaga", "four years"),
    ("mai le taimi lena;", "from that time;"),
    ("ae sa fetalai mai o ia", "but he told"),
    ("ia te a'u", "me"),
    ("ia ou sau", "that I should come"),
    ("i le mea lena", "to that place"),
    ("i le taimi tonu lava", "precisely"),
    ("e atoa i ai le tausaga", "in one full year"),
    ("mai le taimi lena,", "from that time,"),
    ("ma", "and"),
    ("o le a ia feiloai ai", "that he would meet"),
    ("ma a'u iina,", "with me there,"),
    ("ma ia faapea lava", "and that so"),
    ("ona ou faia", "I should continue to do"),
    ("se'ia o'o i le taimi", "until the time should come"),
    ("mo le mauaina o papatusi.", "for obtaining the plates."),
    # — P20 —
    ("“Sa faapea lava,", "“Accordingly,"),
    ("e pei ona poloaiina ai", "as had been commanded"),
    ("a'u,", "me,"),
    ("ona ou alu", "I went"),
    ("i le faaiuga", "at the end"),
    ("o tausaga taitasi,", "of each year,"),
    ("ma o taimi taitasi uma", "and each time"),
    ("na ou alu atu ai", "that I went"),
    ("na ou maua ai", "I found"),
    ("lea lava avefeau iina,", "the same messenger there,"),
    ("ma maua mai ia te ia", "and received from him"),
    ("faatonuga ma le malamalama", "instruction and intelligence"),
    ("i taimi taitasi", "at each"),
    ("o a ma talanoaga,", "of our interviews,"),
    ("e faatatau i mea", "respecting what"),
    ("o le a faia", "was going to do"),
    ("e le Alii,", "the Lord,"),
    ("ma le ala ma le auala", "and how and in what manner"),
    ("e taitai ai lona malo", "his kingdom was to be conducted"),
    ("i aso e gata ai. …", "in the last days. …"),
    # — P21 —
    ("“Sa o'o ina o'o mai", "“At length arrived"),
    ("le taimi", "the time"),
    ("mo le mauaina mai", "for obtaining"),
    ("o papatusi,", "the plates,"),
    ("le Urima ma le Tumena,", "the Urim and Thummim,"),
    ("ma le ufifatafata.", "and the breastplate."),
    ("O le aso luasefulu-lua o Setema,", "On the twenty-second day of September,"),
    ("i le tausaga", "in the year"),
    ("e tasi le afe", "one thousand"),
    ("valu selau", "eight hundred"),
    ("luasefulu ma le fitu,", "and twenty-seven,"),
    ("ina ua ou alu atu", "having gone"),
    ("e pei ona masani ai", "as usual"),
    ("i le faaiuga", "at the end"),
    ("o se isi tausaga", "of another year"),
    ("i le mea", "to the place"),
    ("sa teu ai papatusi,", "where they were deposited,"),
    ("na tuu mai ai", "delivered up"),
    ("ia te a'u", "to me"),
    ("e lea lava avefeau faalelagi", "the same heavenly messenger"),
    ("ia mea", "them"),
    ("ma le poloaiga lenei:", "with this charge:"),
    ("ua ia te a'u", "that I should have"),
    ("le tausiga o ia mea;", "the keeping of them;"),
    ("ma afai", "that if"),
    ("ou te tuusolo ma le faatalalē", "I should let them go carelessly"),
    ("ia mea,", "them,"),
    ("po o so'u faatamala", "or through my neglect"),
    ("i ai,", "of them,"),
    ("o le a vavaeeseina a'u;", "I should be cut off;"),
    ("ae afai ou te faaaoga", "but that if I would use"),
    ("a'u taumafaiga uma", "all my endeavors"),
    ("e faasaoina ia mea,", "to preserve them,"),
    ("se'ia o'o ina sau o ia,", "until he should come,"),
    ("le avefeau lea,", "the messenger,"),
    ("mo ia mea,", "for them,"),
    ("o le a puipuia lava", "they should be protected"),
    ("i latou.", "them."),
    # — P22 —
    ("“Sa vave ona ou iloa", "“I soon found out"),
    ("le pogai", "the reason why"),
    ("na ou maua ai poloaiga patino", "I had received such strict charges"),
    ("ia ou tausi saogalemu", "to keep safe"),
    ("ia mea,", "them,"),
    ("ma le pogai", "and why it was"),
    ("na fetalai mai ai le avefeau", "that the messenger had said"),
    ("a uma ona ou faataunuuina", "that when I had accomplished"),
    ("o le galuega", "the work"),
    ("ua tuu mai i o'u lima,", "at my hand,"),
    ("o le a sau o ia", "he would come"),
    ("mo i latou.", "for them."),
    ("Ona e lei pine ona iloa", "For no sooner was it known"),
    ("ua ia te a'u ia mea,", "that I had them,"),
    ("ae faaaoga e tagata", "than were used"),
    ("taumafaiga malolosi", "the most strenuous exertions"),
    ("e faoeseina ai", "to take away"),
    ("mai ia te a'u.", "from me."),
    ("Sa faaaoga soo se togafiti", "Every stratagem was resorted to"),
    ("sa mafai ona faia", "that could be invented"),
    ("mo lena faamoemoe.", "for that purpose."),
    ("Sa o'o ina sili atu", "became more"),
    ("le matuitui ma le tiga", "bitter and severe"),
    ("o sauaga", "the persecution"),
    ("nai lo le taimi muamua,", "than before,"),
    ("ma sa mata'i pea lava pea", "and were on the alert continually"),
    ("e motu o tagata avanoa", "multitudes"),
    ("latou te fao ai ia mea", "to get them"),
    ("mai ia te a'u", "from me"),
    ("pe a mafai.", "if possible."),
    ("Peitai ona o le poto", "But by the wisdom"),
    ("o le Atua,", "of God,"),
    ("sa saogalemu pea ia mea", "they remained safe"),
    ("i o'u lima,", "in my hands,"),
    ("seia o'o ina mae'a", "until I had accomplished"),
    ("ona ou faataunuuina", "done"),
    ("o le galuega", "the work"),
    ("sa manaomia mai lo'u lima.", "at my hand."),
    ("Ma ina ua mae'a", "When done"),
    ("e tusa ai ma tuutuuga,", "according to arrangements,"),
    ("sa toe afio mai le avefeau,", "the messenger came,"),
    ("mo ia mea,", "for them,"),
    ("ma sa ou tuu atu ai", "I delivered them up"),
    ("ia te ia;", "to him;"),
    ("ma ua i ai", "and he has"),
    ("ia te ia", "in his keeping"),
    ("ia mea", "them"),
    ("i lana vaaiga", "in his charge"),
    ("e o'o mai", "until"),
    ("i le aso nei,", "this day,"),
    ("le aso lua lea", "being the second day"),
    ("o Me,", "of May,"),
    ("o le tasi le afe", "one thousand"),
    ("valu selau", "eight hundred"),
    ("tolusefulu ma le valu.”", "and thirty-eight.”"),
    # — Closing notes —
    ("Mo se tala atoa,", "For a more complete account,"),
    ("tagai i le Iosefa Samita—", "see Joseph Smith—"),
    ("Talafaasolopito", "History"),
    ("i le Penina Tau Tele.", "in the Pearl of Great Price."),
    ("O le talafaamaumau mai anamua", "The ancient record"),
    ("sa faapea ona aumai", "thus brought forth"),
    ("mai le eleele", "from the earth"),
    ("e pei o le leo", "as the voice"),
    ("o se nuu", "of a people"),
    ("ua tautala mai i le efuefu,", "speaking from the dust,"),
    ("ma faaliliuina", "and translated"),
    ("i le gagana", "into the language"),
    ("o ona po nei", "of these days"),
    ("e ala i le meaalofa", "by the gift"),
    ("ma le mana", "and power"),
    ("o le Atua", "of God"),
    ("e pei ona faamaonia", "as attested"),
    ("i se faamaoniga Paia,", "by Divine affirmation,"),
    ("sa muai lomia ma faasalalauina", "was first published"),
    ("i le lalolagi", "to the world"),
    ("i le gagana Peretania", "in the English language"),
    ("i le tausaga e 1830,", "in the year 1830,"),
    ("The Book of Mormon", "as The Book of Mormon"),
    ("(O LE TUSI A MAMONA).", "(THE BOOK OF MORMON)."),
]

# ---------------------------------------------------------------------------
# A Brief Explanation about the Book of Mormon
# ---------------------------------------------------------------------------

EXPL_EN = (
    "The Book of Mormon is a sacred record of peoples in ancient America and "
    "was engraved upon metal plates. Sources from which this record was "
    "compiled include the following:"
    "\n\n"
    "1. The Plates of Nephi, which were of two kinds: the small plates and "
    "the large plates. The former were more particularly devoted to "
    "spiritual matters and the ministry and teachings of the prophets, while "
    "the latter were occupied mostly by a secular history of the peoples "
    "concerned (1 Nephi 9:2–4). From the time of Mosiah, however, the large "
    "plates also included items of major spiritual importance."
    "\n\n"
    "2. The Plates of Mormon, which consist of an abridgment by Mormon from "
    "the large plates of Nephi, with many commentaries. These plates also "
    "contained a continuation of the history by Mormon and additions by his "
    "son Moroni."
    "\n\n"
    "3. The Plates of Ether, which present a history of the Jaredites. This "
    "record was abridged by Moroni, who inserted comments of his own and "
    "incorporated the record with the general history under the title “Book "
    "of Ether.”"
    "\n\n"
    "4. The Plates of Brass brought by the people of Lehi from Jerusalem in "
    "600 B.C. These contained “the five books of Moses, … and also a record "
    "of the Jews from the beginning, … down to the commencement of the reign "
    "of Zedekiah, king of Judah; and also the prophecies of the holy "
    "prophets” (1 Nephi 5:11–13). Many quotations from these plates, citing "
    "Isaiah and other biblical and nonbiblical prophets, appear in the Book "
    "of Mormon."
    "\n\n"
    "The Book of Mormon comprises fifteen main parts or divisions, known, "
    "with one exception, as books, usually designated by the name of their "
    "principal author. The first portion (the first six books, ending with "
    "Omni) is a translation from the small plates of Nephi. Between the "
    "books of Omni and Mosiah is an insert called the Words of Mormon. This "
    "insert connects the record engraved on the small plates with Mormon's "
    "abridgment of the large plates."
    "\n\n"
    "The longest portion, from Mosiah through Mormon chapter 7, is a "
    "translation of Mormon's abridgment of the large plates of Nephi. The "
    "concluding portion, from Mormon chapter 8 to the end of the volume, was "
    "engraved by Mormon's son Moroni, who, after finishing the record of his "
    "father's life, made an abridgment of the Jaredite record (as the book "
    "of Ether) and later added the parts known as the book of Moroni."
    "\n\n"
    "In or about the year A.D. 421, Moroni, the last of the Nephite "
    "prophet-historians, sealed the sacred record and hid it up unto the "
    "Lord, to be brought forth in the latter days, as predicted by the voice "
    "of God through His ancient prophets. In A.D. 1823, this same Moroni, "
    "then a resurrected personage, visited the Prophet Joseph Smith and "
    "subsequently delivered the engraved plates to him."
    "\n\n"
    "About this edition: The original title page, immediately preceding the "
    "contents page, is taken from the plates and is part of the sacred text. "
    "Introductions in a non-italic typeface, such as in 1 Nephi and "
    "immediately preceding Mosiah chapter 9, are also part of the sacred "
    "text. Introductions in italics, such as in chapter headings, are not "
    "original to the text but are study helps included for convenience in "
    "reading."
    "\n\n"
    "Some minor errors in the text have been perpetuated in past editions of "
    "the Book of Mormon. This edition contains corrections that seem "
    "appropriate to bring the material into conformity with prepublication "
    "manuscripts and early editions edited by the Prophet Joseph Smith."
)

EXPL_SM = (
    "O le Tusi a Mamona o se talafaamaumau paia o tagata Amerika anamua sa "
    "togitogia i luga o papatusi metala. O faapogai na tuufaatasia mai ai "
    "lenei talafaamaumau e aofia ai mea nei:"
    "\n\n"
    "1. O Papatusi a Nifae, e lua ituaiga: o papatusi laiti ma papatusi "
    "tetele. O papatusi laiti sa faaaoga faapitoa mo mataupu faaleagaga ma "
    "auaunaga ma aoaoga a perofeta, a o papatusi tetele, sa faatumulia tele "
    "i se talafaasolopito faaletino o tagata ua faatatau i ai (1 Nifae "
    "9:2–4). E ui i lea, mai le taimi o Mosaea, ua i ai foi i papatusi "
    "tetele ni mea taua tele faaleagaga."
    "\n\n"
    "2. O Papatusi a Mamona, e aofia ai se otootoga na faia e Mamona mai "
    "papatusi tetele a Nifae, ma le tele o ni faamatalaga. Sa i ai foi i nei "
    "papatusi se faaauauga o le talafaasolopito na tusia e Mamona ma ni "
    "faaopoopoga a lona atalii o Moronae."
    "\n\n"
    "3. O Papatusi a Eteru, ua tuu mai ai le talafaasolopito o sa Iaretō. O "
    "lenei talafaamaumau sa otootoina e Moronae, o lē sa faaopoopo i ai ni "
    "ana lava faamatalaga ma tuufaatasi le talafaamaumau ma le "
    "talafaasolopito aoao i lalo o le igoa, o le “Tusi a Eteru.”"
    "\n\n"
    "4. O Papatusi Apamemea o ni papatusi sa aumaia e le nuu o Liae mai "
    "Ierusalema i le 600 T.L.M. O nei papatusi sa aofia ai “tusi e lima a "
    "Mose, … o le talafaamaumau foi o Iutaia mai le amataga, … e oo mai i le "
    "amataga o le nofoaiga a Setekaia, le tupu o Iuta; o valoaga foi a "
    "perofeta paia” (1 Nifae 5:11–13). E tele upusii mai nei papatusi, ua "
    "sii mai ai Isaia ma isi perofeta o le tusi paia ma perofeta ua lē mai "
    "le tusi paia, ua i le Tusi a Mamona."
    "\n\n"
    "O le Tusi a Mamona ua i ai ni vaega po o ni vaevaega autu e sefulu ma "
    "le lima, ua ta'ua, vagana ai se tasi, o ni tusi, e masani ona "
    "faaigoaina i igoa o o latou tusitala autu. O le vaega muamua (o tusi "
    "muamua e ono, e gata mai i le tusi a Ominae) o le faaliliuga mai "
    "papatusi laiti a Nifae. O le va o le tusi a Ominae ma le tusi a Mosaea "
    "o loo i ai se faaopoopoga ua ta'ua o Upu a Mamona. O lenei faaopoopoga "
    "ua sosoo ai le talafaamaumau na togitogia i papatusi laiti ma le "
    "otootoga a Mamona o papatusi tetele."
    "\n\n"
    "O le vaega sili ona umi, mai le tusi a Mosaea seia oo atu i le Mamona "
    "mataupu 7, o se faaliliuga o le otootoga a Mamona o papatusi tetele a "
    "Nifae. O le vaega mulimuli, mai le Mamona mataupu 8 e oo i le faaiuga o "
    "le tusi, sa togitogia e Moronae, le atalii o Mamona, o lē, ina ua uma "
    "ona ia tusia o le talafaamaumau o le olaga o lona tamā, na faia le "
    "otootoga o le talafaamaumau o sa Iaretō (ua fai ma tusi a Eteru) ma ia "
    "faaopoopo mulimuli ane i ai vaega ua ta'ua o le tusi a Moronae."
    "\n\n"
    "Pe tusa o le tausaga e 421 T.A., na faamau ai e Moronae, le perofeta "
    "tusitalafaasolopito mulimuli o sa Nifaē le talafaamaumau paia ma natia "
    "i le Alii, ina ia aumai i aso e gata ai, e pei ona valoia e le "
    "siufofoga o le Atua e ala mai i Ana perofeta anamua. I le 1823 T.A., o "
    "Moronae lava lea, ua avea nei ma tagata toetu, sa asiasi i le Perofeta "
    "o Iosefa Samita, ma mulimuli ane tuuina atu ia te ia papatusi ua "
    "togitogia."
    "\n\n"
    "E faatatau i lenei lomiga: O le ulua'i itulau autu, o loo muamua atu i "
    "le itulau o le anotusi, ua aumaia mai papatusi ma o se vaega o le "
    "tusitusiga paia. O faatomuaga e le o taina faatusilima, e pei ona i ai "
    "i le 1 Nifae ma sosoo ai ma le mataupu 9 o le Mosaea, o vaega foi ia o "
    "le tusitusiga paia. O faatomuaga o loo faatusilima, e pei o ulutala o "
    "mataupu, e le o ni uluai tusiga ia ae o ni fesoasoaniga mo suesuega ua "
    "faaaofia ai mo le faafaigofieina o faitauga."
    "\n\n"
    "E i ai ni sese laiti i upu sa i lomiga ua mavae o le Tusi a Mamona sa "
    "faasalalauina i le gagana Peretania. O le lomiga lenei ua i ai ni "
    "faasa'oga ua manatu ua tatau ai, ina ia ogatasi upu ma itulau muai "
    "tusia mo le uluai faasalalauga ma lomiga, atoa ma lomiga sa faasa'oina "
    "e le Perofeta o Iosefa Samita."
)

EXPL_CELLS = [
    # — Intro paragraph —
    ("O le Tusi a Mamona", "The Book of Mormon"),
    ("o se talafaamaumau paia", "is a sacred record"),
    ("o tagata Amerika anamua", "of peoples in ancient America"),
    ("sa togitogia", "and was engraved"),
    ("i luga o papatusi metala.", "upon metal plates."),
    ("O faapogai", "The sources"),
    ("na tuufaatasia mai ai", "from which was compiled"),
    ("lenei talafaamaumau", "this record"),
    ("e aofia ai mea nei:", "include the following:"),
    # — 1. Plates of Nephi —
    ("1. O Papatusi a Nifae,", "1. The Plates of Nephi,"),
    ("e lua ituaiga:", "which were of two kinds:"),
    ("o papatusi laiti", "the small plates"),
    ("ma papatusi tetele.", "and the large plates."),
    ("O papatusi laiti", "The former"),
    ("sa faaaoga faapitoa", "were more particularly devoted"),
    ("mo mataupu faaleagaga", "to spiritual matters"),
    ("ma auaunaga", "and the ministry"),
    ("ma aoaoga a perofeta,", "and teachings of the prophets,"),
    ("a o papatusi tetele,", "while the latter"),
    ("sa faatumulia tele", "were occupied mostly"),
    ("i se talafaasolopito faaletino", "by a secular history"),
    ("o tagata", "of the peoples"),
    ("ua faatatau i ai", "concerned"),
    ("(1 Nifae 9:2–4).", "(1 Nephi 9:2–4)."),
    ("E ui i lea,", "however,"),
    ("mai le taimi o Mosaea,", "from the time of Mosiah,"),
    ("ua i ai foi", "also included"),
    ("i papatusi tetele", "in the large plates"),
    ("ni mea taua tele faaleagaga.", "items of major spiritual importance."),
    # — 2. Plates of Mormon —
    ("2. O Papatusi a Mamona,", "2. The Plates of Mormon,"),
    ("e aofia ai se otootoga", "which consist of an abridgment"),
    ("na faia e Mamona", "by Mormon"),
    ("mai papatusi tetele a Nifae,", "from the large plates of Nephi,"),
    ("ma le tele", "with many"),
    ("o ni faamatalaga.", "commentaries."),
    ("Sa i ai foi", "also contained"),
    ("i nei papatusi", "in these plates"),
    ("se faaauauga o le talafaasolopito", "a continuation of the history"),
    ("na tusia e Mamona", "by Mormon"),
    ("ma ni faaopoopoga", "and additions"),
    ("a lona atalii o Moronae.", "by his son Moroni."),
    # — 3. Plates of Ether —
    ("3. O Papatusi a Eteru,", "3. The Plates of Ether,"),
    ("ua tuu mai ai", "which present"),
    ("le talafaasolopito", "a history"),
    ("o sa Iaretō.", "of the Jaredites."),
    ("O lenei talafaamaumau", "This record"),
    ("sa otootoina e Moronae,", "was abridged by Moroni,"),
    ("o lē", "who"),
    ("sa faaopoopo i ai", "inserted"),
    ("ni ana lava faamatalaga", "comments of his own"),
    ("ma tuufaatasi le talafaamaumau", "and incorporated the record"),
    ("ma le talafaasolopito aoao", "with the general history"),
    ("i lalo o le igoa,", "under the title,"),
    ("o le “Tusi a Eteru.”", "“Book of Ether.”"),
    # — 4. Plates of Brass —
    ("4. O Papatusi Apamemea", "4. The Plates of Brass"),
    ("o ni papatusi sa aumaia", "brought"),
    ("e le nuu o Liae", "by the people of Lehi"),
    ("mai Ierusalema", "from Jerusalem"),
    ("i le 600 T.L.M.", "in 600 B.C."),
    ("O nei papatusi", "These"),
    ("sa aofia ai", "contained"),
    ("“tusi e lima", "“the five books"),
    ("a Mose, …", "of Moses, …"),
    ("o le talafaamaumau foi", "and also a record"),
    ("o Iutaia", "of the Jews"),
    ("mai le amataga, …", "from the beginning, …"),
    ("e oo mai", "down to"),
    ("i le amataga", "the commencement"),
    ("o le nofoaiga a Setekaia,", "of the reign of Zedekiah,"),
    ("le tupu o Iuta;", "king of Judah;"),
    ("o valoaga foi", "and also the prophecies"),
    ("a perofeta paia”", "of the holy prophets”"),
    ("(1 Nifae 5:11–13).", "(1 Nephi 5:11–13)."),
    ("E tele upusii", "Many quotations"),
    ("mai nei papatusi,", "from these plates,"),
    ("ua sii mai ai Isaia", "citing Isaiah"),
    ("ma isi perofeta", "and other prophets"),
    ("o le tusi paia", "biblical"),
    ("ma perofeta", "and prophets"),
    ("ua lē mai", "not from"),
    ("le tusi paia,", "the scriptures,"),
    ("ua i", "appear in"),
    ("le Tusi a Mamona.", "the Book of Mormon."),
    # — Fifteen divisions —
    ("O le Tusi a Mamona", "The Book of Mormon"),
    ("ua i ai", "comprises"),
    ("ni vaega", "parts"),
    ("po o ni vaevaega autu", "or main divisions"),
    ("e sefulu ma le lima,", "fifteen,"),
    ("ua ta'ua,", "known,"),
    ("vagana ai se tasi,", "with one exception,"),
    ("o ni tusi,", "as books,"),
    ("e masani ona faaigoaina", "usually designated"),
    ("i igoa", "by the name"),
    ("o o latou tusitala autu.", "of their principal author."),
    ("O le vaega muamua", "The first portion"),
    ("(o tusi muamua e ono,", "(the first six books,"),
    ("e gata mai", "ending"),
    ("i le tusi a Ominae)", "with Omni)"),
    ("o le faaliliuga", "is a translation"),
    ("mai papatusi laiti a Nifae.", "from the small plates of Nephi."),
    ("O le va", "Between"),
    ("o le tusi a Ominae", "the book of Omni"),
    ("ma le tusi a Mosaea", "and the book of Mosiah"),
    ("o loo i ai", "is"),
    ("se faaopoopoga", "an insert"),
    ("ua ta'ua", "called"),
    ("o Upu a Mamona.", "the Words of Mormon."),
    ("O lenei faaopoopoga", "This insert"),
    ("ua sosoo ai", "connects"),
    ("le talafaamaumau", "the record"),
    ("na togitogia i papatusi laiti", "engraved on the small plates"),
    ("ma le otootoga a Mamona", "with Mormon's abridgment"),
    ("o papatusi tetele.", "of the large plates."),
    # — Longest / concluding portions —
    ("O le vaega", "The portion"),
    ("sili ona umi,", "longest,"),
    ("mai le tusi a Mosaea", "from Mosiah"),
    ("seia oo atu", "through"),
    ("i le Mamona mataupu 7,", "Mormon chapter 7,"),
    ("o se faaliliuga", "is a translation"),
    ("o le otootoga a Mamona", "of Mormon's abridgment"),
    ("o papatusi tetele a Nifae.", "of the large plates of Nephi."),
    ("O le vaega mulimuli,", "The concluding portion,"),
    ("mai le Mamona mataupu 8", "from Mormon chapter 8"),
    ("e oo", "to"),
    ("i le faaiuga", "the end"),
    ("o le tusi,", "of the volume,"),
    ("sa togitogia e Moronae,", "was engraved by Moroni,"),
    ("le atalii o Mamona,", "Mormon's son,"),
    ("o lē,", "who,"),
    ("ina ua uma", "after"),
    ("ona ia tusia", "he had written"),
    ("o le talafaamaumau", "the record"),
    ("o le olaga", "of the life"),
    ("o lona tamā,", "of his father,"),
    ("na faia le otootoga", "made an abridgment"),
    ("o le talafaamaumau", "of the record"),
    ("o sa Iaretō", "of the Jaredites"),
    ("(ua fai ma", "(as"),
    ("tusi a Eteru)", "the book of Ether)"),
    ("ma ia faaopoopo", "and added"),
    ("mulimuli ane i ai", "later"),
    ("vaega ua ta'ua", "the parts known"),
    ("o le tusi a Moronae.", "as the book of Moroni."),
    # — Moroni seals the record —
    ("Pe tusa o le tausaga", "In or about the year"),
    ("e 421 T.A.,", "A.D. 421,"),
    ("na faamau ai e Moronae,", "sealed by Moroni,"),
    ("le perofeta tusitalafaasolopito mulimuli", "the last prophet-historian"),
    ("o sa Nifaē", "of the Nephites,"),
    ("le talafaamaumau paia", "the sacred record"),
    ("ma natia i le Alii,", "and hid it up unto the Lord,"),
    ("ina ia aumai", "to be brought forth"),
    ("i aso e gata ai,", "in the latter days,"),
    ("e pei ona valoia", "as predicted"),
    ("e le siufofoga", "by the voice"),
    ("o le Atua", "of God"),
    ("e ala mai", "through"),
    ("i Ana perofeta anamua.", "His ancient prophets."),
    ("I le 1823 T.A.,", "In A.D. 1823,"),
    ("o Moronae lava lea,", "this same Moroni,"),
    ("ua avea nei", "then become"),
    ("ma tagata toetu,", "a resurrected personage,"),
    ("sa asiasi", "visited"),
    ("i le Perofeta", "the Prophet"),
    ("o Iosefa Samita,", "Joseph Smith,"),
    ("ma mulimuli ane", "and subsequently"),
    ("tuuina atu ia te ia", "delivered to him"),
    ("papatusi ua togitogia.", "the engraved plates."),
    # — About this edition —
    ("E faatatau i lenei lomiga:", "About this edition:"),
    ("O le ulua'i itulau autu,", "The original title page,"),
    ("o loo muamua atu", "immediately preceding"),
    ("i le itulau", "the page"),
    ("o le anotusi,", "of contents,"),
    ("ua aumaia mai papatusi", "is taken from the plates"),
    ("ma o se vaega", "and is part"),
    ("o le tusitusiga paia.", "of the sacred text."),
    ("O faatomuaga", "Introductions"),
    ("e le o taina faatusilima,", "in a non-italic typeface,"),
    ("e pei ona i ai", "such as"),
    ("i le 1 Nifae", "in 1 Nephi"),
    ("ma sosoo ai", "and preceding"),
    ("ma le mataupu 9", "chapter 9"),
    ("o le Mosaea,", "of Mosiah,"),
    ("o vaega foi ia", "are also part"),
    ("o le tusitusiga paia.", "of the sacred text."),
    ("O faatomuaga o loo faatusilima,", "Introductions in italics,"),
    ("e pei o ulutala", "such as"),
    ("o mataupu,", "chapter headings,"),
    ("e le o", "are not"),
    ("ni uluai tusiga ia", "original writings"),
    ("ae o ni fesoasoaniga", "but are helps"),
    ("mo suesuega", "for study"),
    ("ua faaaofia ai", "included"),
    ("mo le faafaigofieina o faitauga.", "for convenience in reading."),
    # — Corrections note —
    ("E i ai", "There are"),
    ("ni sese laiti", "some minor errors"),
    ("i upu", "in the text"),
    ("sa i lomiga", "in editions"),
    ("ua mavae", "past"),
    ("o le Tusi a Mamona", "of the Book of Mormon"),
    ("sa faasalalauina", "published"),
    ("i le gagana Peretania.", "in the English language."),
    ("O le lomiga lenei", "This edition"),
    ("ua i ai ni faasa'oga", "contains corrections"),
    ("ua manatu ua tatau ai,", "that seem appropriate,"),
    ("ina ia ogatasi upu", "to bring the words into conformity"),
    ("ma itulau muai tusia", "with prepublication manuscripts"),
    ("mo le uluai faasalalauga", "for the first publication"),
    ("ma lomiga,", "and editions,"),
    ("atoa ma lomiga", "and early editions"),
    ("sa faasa'oina", "edited"),
    ("e le Perofeta", "by the Prophet"),
    ("o Iosefa Samita.", "Joseph Smith."),
]

SECTIONS.extend(
    [
        {
            "id": "three-witnesses",
            "title_en": "The Testimony of Three Witnesses",
            "title_sm": "O Le Mau a Molimau e Toatolu",
            "en": THREE_EN,
            "sm": THREE_SM,
            "cells": THREE_CELLS,
        },
        {
            "id": "eight-witnesses",
            "title_en": "The Testimony of Eight Witnesses",
            "title_sm": "O Le Mau a Molimau e Toavalu",
            "en": EIGHT_EN,
            "sm": EIGHT_SM,
            "cells": EIGHT_CELLS,
        },
        {
            "id": "js-testimony",
            "title_en": "The Testimony of the Prophet Joseph Smith",
            "title_sm": "O Le Molimau a le Perofeta o Iosefa Samita",
            "en": JS_EN,
            "sm": JS_SM,
            "cells": JS_CELLS,
        },
        {
            "id": "brief-explanation",
            "title_en": "A Brief Explanation about the Book of Mormon",
            "title_sm": "O Se Faamalamalamaga Puupuu e uiga i le Tusi a Mamona",
            "en": EXPL_EN,
            "sm": EXPL_SM,
            "cells": EXPL_CELLS,
        },
    ]
)


if __name__ == "__main__":
    main()
