"""Build the Dual-view data for O le Tusi Paia (Samoan Bible) from the segmented verses.

Mirrors the Spanish iOS app's structure: one book_<id>.json per book with volume "ot" | "nt",
verses as {"num", "words": [{"sm", "en": ""}]} (glosses come later), one English map keyed
"Book|chapter|verse" (the KJV column, KJV versification), and an index of volumes and books.
Output: corpus/tusi_paia/dual/. Nothing here is wired into the app bundle yet.
"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent.parent / 'corpus' / 'tusi_paia'
OUT = D / 'dual'; OUT.mkdir(exist_ok=True)
V = json.load(open(D / 'tusi_paia_verses.json', encoding='utf8'))['verses']
K = json.load(open(D / 'english_ot_nt.json', encoding='utf8')); KV = K['verses']; KC = K['counts']
OT = [('Genesis','Kenese'),('Exodus','Esoto'),('Leviticus','Levitiko'),('Numbers','Numera'),('Deuteronomy','Teuteronome'),('Joshua','Iosua'),('Judges','Faamasino'),('Ruth','Ruta'),('1 Samuel','1 Samuelu'),('2 Samuel','2 Samuelu'),('1 Kings','1 Tupu'),('2 Kings','2 Tupu'),('1 Chronicles','1 Nofoaiga a Tupu'),('2 Chronicles','2 Nofoaiga a Tupu'),('Ezra','Esera'),('Nehemiah','Neemia'),('Esther','Eseta'),('Job','Iopu'),('Psalms','Salamo'),('Proverbs','Faataoto'),('Ecclesiastes','Failauga'),('Song of Solomon','Pese a Solomona'),('Isaiah','Isaia'),('Jeremiah','Ieremia'),('Lamentations','Auega'),('Ezekiel','Esekielu'),('Daniel','Tanielu'),('Hosea','Hosea'),('Joel','Ioelu'),('Amos','Amosa'),('Obadiah','Opetaia'),('Jonah','Iona'),('Micah','Mika'),('Nahum','Nauma'),('Habakkuk','Sapakuka'),('Zephaniah','Sefanaia'),('Haggai','Hakai'),('Zechariah','Sakaria'),('Malachi','Malaki')]
NT = [('Matthew','Mataio'),('Mark','Mareko'),('Luke','Luka'),('John','Ioane'),('Acts','Galuega'),('Romans','Roma'),('1 Corinthians','1 Korinito'),('2 Corinthians','2 Korinito'),('Galatians','Kalatia'),('Ephesians','Efeso'),('Philippians','Filipi'),('Colossians','Kolose'),('1 Thessalonians','1 Tesalonia'),('2 Thessalonians','2 Tesalonia'),('1 Timothy','1 Timoteo'),('2 Timothy','2 Timoteo'),('Titus','Tito'),('Philemon','Filemoni'),('Hebrews','Eperu'),('James','Iakopo'),('1 Peter','1 Peteru'),('2 Peter','2 Peteru'),('1 John','1 Ioane'),('2 John','2 Ioane'),('3 John','3 Ioane'),('Jude','Iuta'),('Revelation','Faaaliga')]
index = {'volumes': [{'id': 'ot', 'nameSm': 'O le Feagaiga Tuai', 'nameEn': 'Old Testament'},
                     {'id': 'nt', 'nameSm': 'O le Feagaiga Fou', 'nameEn': 'New Testament'}],
         'books': [], 'estimated': [], 'missing': [],
         'source': 'corpus/tusi_paia: archive.org samoan-bible OCR segmented by scripts/segment_tusi_paia.py; English = KJV (KJV versification) from the Spanish app'}
# hand-curated verses (tusi_paia_hand.json): their Samoan is the corrected text
hand_path = Path(__file__).resolve().parent.parent / 'O le Tusi a Mamona Interlinear' / 'Resources' / 'tusi_paia_hand.json'
HAND = json.load(open(hand_path, encoding='utf8'))['verses'] if hand_path.exists() else {}
english = {}
tot_v = tot_w = 0
for vol, books in (('ot', OT), ('nt', NT)):
    for en, sm in books:
        bid = en.lower().replace(' ', '')
        book = {'id': bid, 'volume': vol, 'nameSm': sm, 'nameEn': en, 'chapters': []}
        for c in sorted(int(x) for x in KC[en]):
            verses = []
            for v in range(1, KC[en][str(c)] + 1):
                key = f'{en}|{c}|{v}'; english[key] = KV[key]
                rec = V.get(key)
                hkey = f'{bid}|{c}|{v}'
                if hkey in HAND:
                    rec = {'sm': ' '.join(w['sm'] for w in HAND[hkey]['words']), 'est': False}
                if rec is None or not rec['sm'].strip():
                    index['missing'].append(key); words = [{'sm': '—', 'en': ''}]
                else:
                    words = [{'sm': w, 'en': ''} for w in rec['sm'].split() if w.strip('|')]
                    if rec['est']: index['estimated'].append(key)
                verses.append({'num': v, 'words': words}); tot_v += 1; tot_w += len(words)
            book['chapters'].append({'num': c, 'verses': verses})
        json.dump(book, open(OUT / f'book_{bid}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
        index['books'].append({'id': bid, 'nameSm': sm, 'nameEn': en, 'volume': vol, 'chapters': len(book['chapters'])})
json.dump(english, open(OUT / 'tusi_paia_english.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
json.dump(index, open(OUT / 'tusi_paia_index.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'books {len(index["books"])}  verses {tot_v}  words {tot_w}  estimated {len(index["estimated"])}  missing {len(index["missing"])} {index["missing"]}')
