/* O le Tusi a Mamona — Interlinear (web reader / PWA)
 *
 * A browser port of the SwiftUI reader. Chapter data is fetched one file at a
 * time from docs/data/ch/, so the initial paint doesn't wait on the whole
 * corpus; the service worker separately precaches all of it for offline use.
 *
 * Routing is hash-based because GitHub Pages serves static files only and can't
 * rewrite deep paths to index.html.
 */
(() => {
  'use strict';

  const BASE = new URL('.', location.href).href;
  const $ = (id) => document.getElementById(id);

  const view = $('view');

  /* The app's three reader modes (ReaderMode in AppSettings.swift). */
  const MODES = [
    { id: 'interlinear', label: 'Interlinear' },
    { id: 'samoan', label: 'Samoa' },
    { id: 'dual', label: 'Tutusa' },
  ];

  /* Five highlight colors, matching HighlightColor in HighlightStore.swift. */
  const COLORS = [
    { id: 'yellow', tint: '#fff08c', label: 'Samasama' },
    { id: 'pink', tint: '#ffc7d9', label: 'Piniki' },
    { id: 'blue', tint: '#a8d9fc', label: 'Lanumoana' },
    { id: 'green', tint: '#bdeba6', label: 'Lanumeamata' },
    { id: 'purple', tint: '#d9bff2', label: 'Viole' },
  ];

  const state = {
    index: null,
    diacritics: null,
    chapterCache: new Map(),
    settings: loadSettings(),
    // key -> color id. Keys are `bookId|chapter|verse|wordIndex` for a word
    // and `bookId|chapter|verse` for a whole verse, as in the app.
    highlights: loadJSON('bom.highlights.v1', {}),
    notes: loadJSON('bom.notes.v1', {}),
  };

  /* Which word-units are selected. Scoped to one verse: tapping a word in a
     different verse starts fresh, and word- and verse-level selections never
     coexist (WordSelectionModel.swift). */
  const selection = {
    words: new Set(),
    texts: {},
    verseKey: null,
    wholeVerseKey: null,
    wholeVerseText: '',

    get isEmpty() {
      return this.words.size === 0 && !this.wholeVerseKey;
    },
    get isWholeVerse() {
      return !!this.wholeVerseKey;
    },
    /* Selected keys in reading order — they carry their word index. */
    get sortedKeys() {
      const idx = (k) => Number(k.split('|').pop()) || 0;
      return [...this.words].sort((a, b) => idx(a) - idx(b));
    },
    get joinedText() {
      return this.sortedKeys.map((k) => this.texts[k]).filter(Boolean).join(' ');
    },
    get anchorVerseKey() {
      return this.wholeVerseKey || this.verseKey;
    },

    toggleWord(key, text, verseKey) {
      this.wholeVerseKey = null;
      this.wholeVerseText = '';
      if (this.verseKey !== verseKey) {
        this.words.clear();
        this.texts = {};
        this.verseKey = verseKey;
      }
      if (this.words.has(key)) {
        this.words.delete(key);
        delete this.texts[key];
      } else {
        this.words.add(key);
        this.texts[key] = text;
      }
      if (!this.words.size) this.verseKey = null;
    },

    toggleVerse(verseKey, text) {
      this.words.clear();
      this.texts = {};
      this.verseKey = null;
      if (this.wholeVerseKey === verseKey) {
        this.wholeVerseKey = null;
        this.wholeVerseText = '';
      } else {
        this.wholeVerseKey = verseKey;
        this.wholeVerseText = text;
      }
    },

    clear() {
      this.words.clear();
      this.texts = {};
      this.verseKey = null;
      this.wholeVerseKey = null;
      this.wholeVerseText = '';
    },
  };

  const saveHighlights = () =>
    localStorage.setItem('bom.highlights.v1', JSON.stringify(state.highlights));
  const saveNotes = () => localStorage.setItem('bom.notes.v1', JSON.stringify(state.notes));

  // ---------------------------------------------------------------- settings

  function loadJSON(key, fallback) {
    try {
      return JSON.parse(localStorage.getItem(key)) ?? fallback;
    } catch {
      return fallback;
    }
  }

  function loadSettings() {
    const s = loadJSON('bom.settings', {});
    return {
      scale: typeof s.scale === 'number' ? s.scale : 1,
      diacritics: !!s.diacritics,
      mode: MODES.some((m) => m.id === s.mode) ? s.mode : 'interlinear',
    };
  }

  function saveSettings() {
    localStorage.setItem('bom.settings', JSON.stringify(state.settings));
    applySettings();
  }

  function applySettings() {
    document.documentElement.style.setProperty('--scale', state.settings.scale);
    $('font-scale').value = state.settings.scale;
    $('toggle-diacritics').checked = state.settings.diacritics;
  }

  /* The footer mode bar. Active pill = gold fill with navy text, inactive =
     outlined gold on navy, matching ReaderControlBar. */
  function buildModeBar() {
    const bar = $('modebar');
    bar.replaceChildren();
    for (const mode of MODES) {
      const btn = el('button', 'mode-btn', mode.label);
      btn.classList.toggle('active', state.settings.mode === mode.id);
      btn.addEventListener('click', () => {
        if (state.settings.mode === mode.id) return;
        state.settings.mode = mode.id;
        saveSettings();
        buildModeBar();
        route();
      });
      bar.append(btn);
    }
  }

  // ------------------------------------------------------------------ diacritics

  /* Ports ScriptureLibrary.splitAffixes: the glottal ’ and hyphen count as
     intra-word, so `a’u,` splits to ("", "a’u", ","). */
  const WORD_CHAR = /[\p{L}\p{N}’-]/u;

  function splitAffixes(token) {
    const chars = [...token];
    let first = -1;
    let last = -1;
    chars.forEach((ch, i) => {
      if (WORD_CHAR.test(ch)) {
        if (first === -1) first = i;
        last = i;
      }
    });
    if (first === -1) return ['', '', token];
    return [
      chars.slice(0, first).join(''),
      chars.slice(first, last + 1).join(''),
      chars.slice(last + 1).join(''),
    ];
  }

  function matchCapitalization(original, marked) {
    const head = [...original][0];
    if (!head || head !== head.toUpperCase() || head === head.toLowerCase()) return marked;
    return marked.charAt(0).toUpperCase() + marked.slice(1);
  }

  function markedSamoan(token, wordKey) {
    const d = state.diacritics;
    if (!d) return token;
    const [prefix, core, suffix] = splitAffixes(token);
    if (!core) return token;
    const replacement =
      (wordKey && d.exceptions[wordKey]) || d.types[core.toLowerCase()];
    if (!replacement) return token;
    return prefix + matchCapitalization(core, replacement) + suffix;
  }

  function displaySm(token, wordKey) {
    return state.settings.diacritics ? markedSamoan(token, wordKey) : token;
  }

  // ------------------------------------------------------------------ grouping

  /* Direct port of groupIdiomSpans in WordUnitView.swift. A `·` gloss means
     "this word's English continues into the next word", so a run of dots plus
     the following real gloss renders as one cell. */
  function groupIdiomSpans(words) {
    const out = [];
    let i = 0;
    while (i < words.length) {
      if (words[i].en === '·') {
        let end = i;
        while (end < words.length && words[end].en === '·') end += 1;
        if (end < words.length) {
          out.push({
            index: i,
            sm: words.slice(i, end + 1).map((w) => w.sm),
            en: words[end].en,
          });
          i = end + 1;
          continue;
        }
      }
      out.push({ index: i, sm: [words[i].sm], en: words[i].en });
      i += 1;
    }
    return out;
  }

  // ------------------------------------------------------------------- data

  async function getJSON(path) {
    const res = await fetch(new URL(path, BASE));
    if (!res.ok) throw new Error(`${res.status} ${path}`);
    return res.json();
  }

  async function getChapter(bookId, num) {
    const key = `${bookId}-${num}`;
    if (!state.chapterCache.has(key)) {
      state.chapterCache.set(key, getJSON(`data/ch/${key}.json`));
    }
    return state.chapterCache.get(key);
  }

  const bookById = (id) => state.index.books.find((b) => b.id === id);

  // ----------------------------------------------------------------- render

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function renderUnit(item, verseKey) {
    const wordKey = `${verseKey}|${item.index}`;
    const unit = el('span', 'unit');
    unit.dataset.key = wordKey;

    const sm = el('span', 'sm');
    const text = item.sm
      .map((word, offset) => displaySm(word, `${verseKey}|${item.index + offset}`))
      .join(' ');
    sm.textContent = text;
    unit.append(sm);

    if (item.en) unit.append(el('span', 'en', item.en));
    paintUnit(unit, wordKey);

    // Tapping builds up a selection; the toolbar then acts on it. Highlighting
    // is never applied by the tap itself, matching the app.
    unit.addEventListener('click', () => {
      selection.toggleWord(wordKey, item.sm.join(' '), verseKey);
      refreshSelectionUI();
    });
    return unit;
  }

  /* Highlight tint, selection ring and note dot for one word-unit. */
  function paintUnit(unit, wordKey) {
    const color = state.highlights[wordKey];
    unit.classList.toggle('hl', !!color);
    unit.dataset.hl = color || '';
    unit.classList.toggle('selected', selection.words.has(wordKey));
  }

  /* Notes are stored per verse, so the marker belongs on the verse row — one
     dot per annotated verse. Putting it on every word of the verse would stamp
     a row of identical dots across the whole passage. */
  function noteFor(verseKey) {
    const text = state.notes[verseKey];
    return text && text.trim() ? text : null;
  }

  /* Repaint highlight/selection state in place, without rebuilding the
     chapter — a full re-render would lose scroll position mid-selection. */
  function refreshSelectionUI() {
    for (const unit of document.querySelectorAll('.unit')) {
      paintUnit(unit, unit.dataset.key);
    }
    for (const row of document.querySelectorAll('.verse')) {
      const key = row.dataset.key;
      if (!key) continue;
      const color = state.highlights[key];
      row.classList.toggle('hl', !!color);
      row.dataset.hl = color || '';
      row.classList.toggle('selected', selection.wholeVerseKey === key);
      row.classList.toggle('has-note', !!noteFor(key));
    }
    $('actionbar').hidden = selection.isEmpty;
  }

  /* Samoan prose for the samoan/dual modes. Marked per token with the same
     wordKey the interlinear mode uses, so a context-dependent exception
     resolves identically in every mode (see VerseView.displaySamoanText). */
  function samoanProse(verse, verseKey) {
    if (!state.settings.diacritics) {
      return verse.sm || verse.w.map((w) => w.sm).join(' ');
    }
    return verse.w.map((w, i) => markedSamoan(w.sm, `${verseKey}|${i}`)).join(' ');
  }

  function renderVerse(verse, bookId, num) {
    const verseKey = `${bookId}|${num}|${verse.n}`;
    const prose = samoanProse(verse, verseKey);
    const row = el('div', `verse mode-${state.settings.mode}`);
    row.dataset.key = verseKey;

    // Tapping the number selects the whole verse, in every mode.
    const numCell = el('span', 'verse-num', String(verse.n));
    numCell.addEventListener('click', () => {
      selection.toggleVerse(verseKey, prose);
      refreshSelectionUI();
    });
    row.append(numCell);

    if (state.settings.mode === 'samoan') {
      const p = el('p', 'prose', prose);
      p.addEventListener('click', () => {
        selection.toggleVerse(verseKey, prose);
        refreshSelectionUI();
      });
      row.append(p);
      row.append(noteMarker(verseKey, prose));
      return row;
    }

    if (state.settings.mode === 'dual') {
      const cols = el('div', 'dual-cols');
      const sm = el('p', 'prose sm-col', prose);
      sm.addEventListener('click', () => {
        selection.toggleVerse(verseKey, prose);
        refreshSelectionUI();
      });
      cols.append(sm);
      cols.append(el('div', 'dual-rule'));
      cols.append(el('p', 'prose en-col', verse.en || '—'));
      row.append(cols);
      row.append(noteMarker(verseKey, prose));
      return row;
    }

    const flow = el('div', 'flow');
    for (const item of groupIdiomSpans(verse.w)) flow.append(renderUnit(item, verseKey));
    row.append(flow);
    row.append(noteMarker(verseKey, prose));
    return row;
  }

  /* The margin notepad, as on the Church's own reader: an annotated verse gets
     a notepad in the right gutter, and clicking it reopens the note. Always
     rendered; CSS reveals it only when the row carries a note. */
  function noteMarker(verseKey, preview) {
    const btn = el('button', 'note-marker');
    btn.setAttribute('aria-label', `Manatu — ${referenceLabel(verseKey)}`);
    btn.title = 'Manatu';
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true">' +
      '<path d="M5 3h11l3 3v15a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" ' +
      'fill="currentColor" opacity=".18"/>' +
      '<path d="M5 3h11l3 3v15a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" ' +
      'fill="none" stroke="currentColor" stroke-width="1.6"/>' +
      '<path d="M15.5 3.2V6.5h3.3M7.5 11h9M7.5 14.5h9M7.5 18h5.5" ' +
      'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>' +
      '</svg>';
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      openNote(verseKey, preview);
    });
    return btn;
  }

  /* The chapter title block from BookHeader: Samoan book name, English name,
     the ❧ ❧ ❧ ornament, then Mataupu N over CHAPTER N. */
  function bookHeader(book, num) {
    const head = el('div', 'book-header');
    head.append(el('h2', 'bh-sm', book.nameSm));
    head.append(el('p', 'bh-en', book.nameEn));
    head.append(el('p', 'bh-orn', '❧ ❧ ❧'));
    head.append(el('p', 'bh-ch-sm', `Mataupu ${num}`));
    head.append(el('p', 'bh-ch-en', `Chapter ${num}`));
    return head;
  }

  /* Headings and colophons carry their own interlinear word arrays and follow
     the same three-mode branching as verses (ChapterHeadingView.content). */
  function renderBlock(block, className, keyPrefix) {
    const wrap = el('div', `${className} mode-${state.settings.mode}`);
    const mode = state.settings.mode;

    if (mode === 'samoan') {
      wrap.append(el('p', 'prose', block.sm || ''));
      return wrap;
    }
    if (mode === 'dual') {
      const cols = el('div', 'dual-cols');
      cols.append(el('p', 'prose sm-col', block.sm || ''));
      cols.append(el('div', 'dual-rule'));
      cols.append(el('p', 'prose en-col', block.en || '—'));
      wrap.append(cols);
      return wrap;
    }

    const words = block.words || [];
    if (!words.length) {
      wrap.append(el('p', 'prose', block.sm || ''));
      return wrap;
    }
    const flow = el('div', 'flow');
    for (const item of groupIdiomSpans(words)) flow.append(renderUnit(item, keyPrefix));
    wrap.append(flow);
    return wrap;
  }

  /* Chapter-to-chapter navigation. The app relies on its library sheet for
     this; on the web a pair of links at the end of the text keeps sequential
     reading possible without adding chrome the app doesn't have. */
  function chapterNav(book, num) {
    const all = flatChapters();
    const at = all.findIndex((c) => c.id === book.id && c.num === num);
    const nav = el('nav', 'chapter-nav');

    const make = (target, label, cls) => {
      if (!target) return el('span', 'nav-spacer');
      const b = bookById(target.id);
      const btn = el('button', `nav-btn ${cls}`);
      btn.append(el('span', 'nav-dir', label));
      btn.append(el('span', 'nav-ref', `${b.nameSm} ${target.num}`));
      btn.addEventListener('click', () => {
        location.hash = `#/b/${target.id}/${target.num}`;
      });
      return btn;
    };

    nav.append(make(all[at - 1], '‹ Mu’a', 'prev'));
    nav.append(make(all[at + 1], 'Sosoo ›', 'next'));
    return nav;
  }

  /* The notice required by the Standard Scripture License Agreement, in the same
     three registers the app's landing page uses: the verbatim English (the
     wording the license prescribes), the official Samoan, and a word-by-word
     interlinear. The strings come from data/index.json, which build_web_data.py
     lifts straight out of BookListView.swift so the two can't diverge. */
  function disclaimer() {
    const source = state.index && state.index.disclaimer;
    const wrap = el('div', 'disclaimer');
    if (!source) return wrap;

    wrap.append(el('p', 'disclaimer-en', source.english));
    wrap.append(el('div', 'hairline'));
    wrap.append(el('p', 'disclaimer-sm', source.samoan));
    wrap.append(el('div', 'hairline'));

    const flow = el('div', 'disclaimer-gloss');
    for (const [sm, en] of source.gloss) {
      const cell = el('span', 'gloss-cell');
      cell.append(el('span', 'sm', sm));
      cell.append(el('span', 'en', en));
      flow.append(cell);
    }
    wrap.append(flow);
    return wrap;
  }

  /* The navy cover plate from BookListView.BookCover — tapping it opens the
     library, exactly as in the app. */
  function bookCover() {
    const titles = [
      ['O LE TUSI', 'The Book'],
      ['A MAMONA', 'of Mormon'],
    ];
    const subtitles = [
      ['O se tasi molimau', 'Another testimony'],
      ['a Iesu Keriso', 'of Jesus Christ'],
    ];

    const cover = el('button', 'cover');
    cover.setAttribute('aria-label', 'Tatala le tusi');
    cover.append(el('div', 'cover-rule'));

    const title = el('div', 'cover-title');
    for (const [sm, en] of titles) {
      const cell = el('div', 'cover-cell');
      cell.append(el('span', 'sm', sm));
      cell.append(el('span', 'en', en));
      title.append(cell);
    }
    cover.append(title);

    const sub = el('div', 'cover-sub');
    for (const [sm, en] of subtitles) {
      const cell = el('div', 'cover-cell');
      cell.append(el('span', 'sm', sm));
      cell.append(el('span', 'en', en));
      sub.append(cell);
    }
    cover.append(sub);
    cover.append(el('div', 'cover-rule'));

    cover.addEventListener('click', () => toggleDrawer(true));
    return cover;
  }

  /* Link to the iOS/iPadOS/macOS build on the App Store. An inline SVG mark
     rather than the  glyph, which is a private-use character and renders as
     tofu everywhere except Apple platforms — this button matters most to the
     readers who are not on one yet. */
  function appStoreButton() {
    const link = document.createElement('a');
    link.className = 'appstore';
    link.href = 'https://apps.apple.com/us/app/o-le-tusi-a-m-a-interlinear/id6783359106';
    link.target = '_blank';
    link.rel = 'noopener';

    link.innerHTML =
      '<svg class="appstore-mark" viewBox="0 0 24 24" aria-hidden="true">' +
      '<path fill="currentColor" d="M17.05 12.04c-.02-2.2 1.8-3.26 1.88-3.31-1.02-1.5-2.62-1.7-3.18-1.72' +
      '-1.35-.14-2.64.79-3.33.79-.69 0-1.75-.77-2.87-.75-1.48.02-2.84.86-3.6 2.18-1.54 2.67-.39 6.62 1.1 8.79' +
      '.73 1.06 1.6 2.25 2.74 2.21 1.1-.04 1.52-.71 2.85-.71 1.33 0 1.7.71 2.87.69 1.18-.02 1.93-1.08 2.65-2.14' +
      '.83-1.22 1.18-2.41 1.2-2.47-.03-.01-2.3-.88-2.32-3.5z"/>' +
      '<path fill="currentColor" d="M14.9 5.6c.6-.73 1.01-1.75.9-2.76-.87.04-1.92.58-2.55 1.31-.56.64-1.05 1.68' +
      '-.92 2.67.97.08 1.96-.49 2.57-1.22z"/>' +
      '</svg>';

    const text = el('span', 'appstore-text');
    text.append(el('span', 'appstore-main', 'Download the Apple App'));
    text.append(el('span', 'appstore-sub', 'E Leai se Totogi \u00b7 Free of Charge'));
    link.append(text);
    return link;
  }

  /* Resumes at the furthest chapter reached, or the first chapter if the reader
     hasn't started. Mirrors ContinueReadingButton. */
  function continueButton() {
    const last = localStorage.getItem('bom.last');
    const match = last && last.match(/^#\/b\/([^/]+)\/(\d+)/);
    let bookId = state.index.books[0].id;
    let num = state.index.books[0].chapters[0];
    if (match && bookById(match[1])) {
      bookId = match[1];
      num = Number(match[2]);
    }

    const btn = el('button', 'continue');
    btn.append(el('span', 'continue-kicker', "Fa’aauau le Faitau · Continue reading from"));
    btn.append(el('span', 'continue-ref', `${bookById(bookId).nameEn} ${num}`));
    btn.addEventListener('click', () => {
      location.hash = `#/b/${bookId}/${num}`;
    });
    return btn;
  }

  async function showChapter(bookId, num) {
    const book = bookById(bookId);
    if (!book) return showHome();

    view.replaceChildren(el('p', 'loading', 'O loo utaina…'));
    let chapter;
    try {
      chapter = await getChapter(bookId, num);
    } catch {
      view.replaceChildren(el('p', 'loading', 'Le mafai ona maua le mataupu.'));
      return;
    }

    $('title').textContent = `${book.nameSm} ${num}`;
    document.title = `${book.nameSm} ${num} — O le Tusi a Mamona`;

    const frag = document.createDocumentFragment();
    frag.append(bookHeader(book, num));

    if (chapter.colophon) {
      frag.append(renderBlock(chapter.colophon, 'colophon', `${bookId}|${num}|colophon`));
    }
    if (chapter.heading) {
      frag.append(renderBlock(chapter.heading, 'heading', `${bookId}|${num}|heading`));
    }
    for (const verse of chapter.verses) frag.append(renderVerse(verse, bookId, num));
    frag.append(chapterNav(book, num));

    view.replaceChildren(frag);
    window.scrollTo(0, 0);
    $('modebar').hidden = false;
    refreshSelectionUI();
    localStorage.setItem('bom.last', `#/b/${bookId}/${num}`);
  }

  async function showFront(id) {
    view.replaceChildren(el('p', 'loading', 'O loo utaina…'));
    let section;
    try {
      section = await getJSON(`data/front/${id}.json`);
    } catch {
      return showHome();
    }
    $('title').textContent = section.titleSm;
    document.title = `${section.titleSm} — O le Tusi a Mamona`;

    const frag = document.createDocumentFragment();
    frag.append(el('h2', 'book-title', section.titleSm));
    frag.append(el('div', 'front-body', section.sm || ''));
    if (section.en) frag.append(el('div', 'front-body en', section.en));
    view.replaceChildren(frag);
    window.scrollTo(0, 0);
    $('modebar').hidden = true;
    selection.clear();
    $('actionbar').hidden = true;
  }

  /* Matches BookListView: the cover is the way in, a continue-reading button
     under it, and the license notice below. No book list here — that lives in
     the library drawer, as it does in the app. */
  function showHome() {
    $('title').textContent = 'O le Tusi a Mamona';
    document.title = 'O le Tusi a Mamona — Interlinear';
    $('modebar').hidden = true;
    selection.clear();
    $('actionbar').hidden = true;

    const frag = document.createDocumentFragment();
    const home = el('div', 'home');
    home.append(bookCover());
    home.append(continueButton());
    home.append(appStoreButton());
    home.append(disclaimer());
    frag.append(home);
    view.replaceChildren(frag);
    window.scrollTo(0, 0);
  }

  // ----------------------------------------------------------------- pager

  function flatChapters() {
    const out = [];
    for (const book of state.index.books) {
      for (const num of book.chapters) out.push({ id: book.id, num });
    }
    return out;
  }

  // ----------------------------------------------------------------- drawer

  function buildDrawer() {
    const body = $('drawer-body');
    body.replaceChildren();

    for (const section of state.index.frontmatter) {
      const btn = el('button', 'drawer-book', section.titleSm);
      btn.addEventListener('click', () => {
        location.hash = `#/front/${section.id}`;
        toggleDrawer(false);
      });
      body.append(btn);
    }

    for (const book of state.index.books) {
      const group = el('div', 'drawer-body-group');
      const btn = el('button', 'drawer-book');
      btn.append(document.createTextNode(book.nameSm));
      btn.append(document.createElement('br'));
      btn.append(el('span', 'en', book.nameEn));

      const grid = el('div', 'chapter-grid');
      grid.hidden = true;
      for (const num of book.chapters) {
        const chip = el('button', 'chapter-chip', String(num));
        chip.addEventListener('click', () => {
          location.hash = `#/b/${book.id}/${num}`;
          toggleDrawer(false);
        });
        grid.append(chip);
      }
      btn.addEventListener('click', () => {
        grid.hidden = !grid.hidden;
      });
      group.append(btn, grid);
      body.append(group);
    }
  }

  function toggleDrawer(open) {
    $('drawer').hidden = !open;
    $('drawer-scrim').hidden = !open;
  }

  // ----------------------------------------------------------------- search

  /* Searches every chapter file. After the service worker's precache completes
     these all come from the cache, so it stays fast and works offline; before
     that it streams over the network with a progress line. */
  let searchToken = 0;

  async function runSearch(query) {
    const token = ++searchToken;
    const needle = query.trim().toLowerCase();
    const results = $('search-results');
    const note = $('search-note');
    results.replaceChildren();
    if (needle.length < 2) {
      note.textContent = "Sa'ili i upu Samoa ma fa'aliliuga fa'aPeretania.";
      return;
    }

    const all = flatChapters();
    let hits = 0;
    let scanned = 0;

    for (const { id, num } of all) {
      if (token !== searchToken) return;
      let chapter;
      try {
        chapter = await getChapter(id, num);
      } catch {
        continue;
      }
      scanned += 1;
      if (scanned % 10 === 0) {
        note.textContent = `O loo su'e… ${scanned}/${all.length} — ${hits} maua`;
      }

      for (const verse of chapter.verses) {
        const sm = verse.w.map((w) => w.sm).join(' ');
        const en = verse.w.map((w) => w.en).filter((g) => g && g !== '·').join(' ');
        if (!sm.toLowerCase().includes(needle) && !en.toLowerCase().includes(needle)) {
          continue;
        }
        hits += 1;
        results.append(searchResult(id, num, verse, sm, needle));
        if (hits >= 200) {
          note.textContent = `200+ maua — fa'apitoa lau su'esu'ega.`;
          return;
        }
      }
    }
    if (token === searchToken) {
      note.textContent = hits ? `${hits} maua` : 'Leai se mea na maua.';
    }
  }

  function searchResult(bookId, num, verse, sm, needle) {
    const book = bookById(bookId);
    const btn = el('button', 'result');
    btn.append(el('span', 'ref', `${book.nameSm} ${num}:${verse.n}`));

    const snip = el('span', 'snip');
    const at = sm.toLowerCase().indexOf(needle);
    if (at === -1) {
      snip.textContent = sm.slice(0, 120);
    } else {
      const from = Math.max(0, at - 40);
      snip.append(document.createTextNode((from ? '…' : '') + sm.slice(from, at)));
      const mark = document.createElement('mark');
      mark.textContent = sm.slice(at, at + needle.length);
      snip.append(mark);
      snip.append(document.createTextNode(sm.slice(at + needle.length, at + needle.length + 60) + '…'));
    }
    btn.append(snip);
    btn.addEventListener('click', () => {
      $('search').hidden = true;
      location.hash = `#/b/${bookId}/${num}`;
    });
    return btn;
  }

  // ------------------------------------------------- selection toolbar + notes

  /* Applies a color to the current selection, or clears it when `color` is
     null (the eraser). Mirrors WordActionBar.applyColor. */
  function applyColor(color) {
    const keys = selection.isWholeVerse ? [selection.wholeVerseKey] : [...selection.words];
    for (const key of keys) {
      if (color) state.highlights[key] = color;
      else delete state.highlights[key];
    }
    saveHighlights();
    selection.clear();
    refreshSelectionUI();
  }

  function selectionText() {
    return selection.isWholeVerse ? selection.wholeVerseText : selection.joinedText;
  }

  /* Human reference for the note sheet — "1 Nifae 1:1". */
  function referenceLabel(verseKey) {
    const [bookId, chapter, verse] = verseKey.split('|');
    const book = bookById(bookId);
    return `${book ? book.nameSm : bookId} ${chapter}:${verse}`;
  }

  /* `verseKey` is passed when opening from a margin marker; otherwise the note
     belongs to whatever is currently selected. */
  function openNote(verseKey, preview) {
    if (!verseKey) verseKey = selection.anchorVerseKey;
    if (!verseKey) return;
    const existing = state.notes[verseKey] || '';

    $('note-ref').textContent = referenceLabel(verseKey);
    $('note-preview').textContent = preview || selectionText();
    $('note-text').value = existing;
    $('btn-note-delete').hidden = !existing;
    $('note-sheet').hidden = false;
    $('note-sheet').dataset.key = verseKey;
    $('note-text').focus();
  }

  function saveNote() {
    const verseKey = $('note-sheet').dataset.key;
    const text = $('note-text').value;
    if (text.trim()) state.notes[verseKey] = text;
    else delete state.notes[verseKey];
    saveNotes();
    $('note-sheet').hidden = true;
    selection.clear();
    refreshSelectionUI();
  }

  function deleteNote() {
    delete state.notes[$('note-sheet').dataset.key];
    saveNotes();
    $('note-sheet').hidden = true;
    selection.clear();
    refreshSelectionUI();
  }

  function buildSwatches() {
    const wrap = $('swatches');
    wrap.replaceChildren();
    for (const c of COLORS) {
      const btn = el('button', 'swatch');
      btn.style.background = c.tint;
      btn.title = c.label;
      btn.setAttribute('aria-label', c.label);
      btn.addEventListener('click', () => applyColor(c.id));
      wrap.append(btn);
    }
  }

  async function copySelection() {
    const text = selectionText();
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      // Clipboard API needs a secure context and permission; fall back to a
      // hidden textarea so copy still works where it isn't available.
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.append(ta);
      ta.select();
      try {
        document.execCommand('copy');
      } catch {
        /* nothing more to try */
      }
      ta.remove();
    }
    selection.clear();
    refreshSelectionUI();
  }

  // ------------------------------------------------------------------ router

  function route() {
    const hash = location.hash || '#/';
    const chapter = hash.match(/^#\/b\/([^/]+)\/(\d+)/);
    const front = hash.match(/^#\/front\/(.+)/);
    $('btn-back').hidden = hash === '#/';

    if (chapter) return showChapter(chapter[1], Number(chapter[2]));
    if (front) return showFront(decodeURIComponent(front[1]));
    return showHome();
  }

  // ------------------------------------------------------------- offline SW

  function registerServiceWorker() {
    const stateEl = $('offline-state');
    const noteEl = $('offline-note');
    if (!('serviceWorker' in navigator)) {
      stateEl.textContent = 'N/A';
      noteEl.textContent = 'Offline storage needs a browser with service workers.';
      return;
    }

    navigator.serviceWorker
      .register(new URL('sw.js', BASE))
      .then(() => {
        stateEl.textContent = 'O loo utaina…';
        noteEl.textContent =
          'Downloading all 239 chapters for offline reading. Keep this tab open until it finishes — about 10 MB.';
      })
      .catch(() => {
        stateEl.textContent = 'Failed';
        noteEl.textContent = 'Service worker registration failed.';
      });

    navigator.serviceWorker.addEventListener('message', (event) => {
      const data = event.data || {};
      if (data.type === 'precache-progress') {
        stateEl.textContent = `${data.done}/${data.total}`;
      } else if (data.type === 'precache-done') {
        stateEl.textContent = 'Ua sauni';
        noteEl.textContent =
          'All chapters are stored on this device. The reader now works with no connection.';
      }
    });
  }

  // -------------------------------------------------------------------- init

  function wireUI() {
    buildSwatches();
    $('btn-erase').addEventListener('click', () => applyColor(null));
    $('btn-note').addEventListener('click', openNote);
    $('btn-copy').addEventListener('click', copySelection);
    $('btn-clear-sel').addEventListener('click', () => {
      selection.clear();
      refreshSelectionUI();
    });
    $('btn-note-save').addEventListener('click', saveNote);
    $('btn-note-delete').addEventListener('click', deleteNote);
    $('btn-note-close').addEventListener('click', () => {
      $('note-sheet').hidden = true;
    });
    $('note-sheet').addEventListener('click', (e) => {
      if (e.target === $('note-sheet')) $('note-sheet').hidden = true;
    });

    $('btn-library').addEventListener('click', () => toggleDrawer(true));
    $('drawer-scrim').addEventListener('click', () => toggleDrawer(false));
    $('btn-back').addEventListener('click', () => {
      location.hash = '#/';
    });

    $('btn-settings').addEventListener('click', () => {
      $('settings').hidden = false;
    });
    $('btn-settings-close').addEventListener('click', () => {
      $('settings').hidden = true;
    });
    $('settings').addEventListener('click', (e) => {
      if (e.target === $('settings')) $('settings').hidden = true;
    });

    $('font-scale').addEventListener('input', (e) => {
      state.settings.scale = Number(e.target.value);
      saveSettings();
    });
    $('toggle-diacritics').addEventListener('change', async (e) => {
      state.settings.diacritics = e.target.checked;
      if (state.settings.diacritics && !state.diacritics) {
        try {
          state.diacritics = await getJSON('data/diacritics.json');
        } catch {
          state.diacritics = null;
        }
      }
      saveSettings();
      route();
    });

    $('btn-search').addEventListener('click', () => {
      $('search').hidden = false;
      $('search-input').focus();
    });
    $('btn-search-close').addEventListener('click', () => {
      $('search').hidden = true;
    });
    $('search').addEventListener('click', (e) => {
      if (e.target === $('search')) $('search').hidden = true;
    });

    let debounce;
    $('search-input').addEventListener('input', (e) => {
      clearTimeout(debounce);
      const value = e.target.value;
      debounce = setTimeout(() => runSearch(value), 250);
    });

    window.addEventListener('hashchange', route);
  }

  async function init() {
    applySettings();
    wireUI();
    registerServiceWorker();

    try {
      state.index = await getJSON('data/index.json');
    } catch {
      view.replaceChildren(el('p', 'loading', 'Le mafai ona maua le tusi.'));
      return;
    }
    if (state.settings.diacritics) {
      try {
        state.diacritics = await getJSON('data/diacritics.json');
      } catch {
        state.diacritics = null;
      }
    }

    buildDrawer();
    buildModeBar();
    // No auto-resume to the last chapter: the app opens on its landing page, and
    // that page carries the license notice. Returning readers get there in one
    // tap via the continue button instead.
    route();
  }

  init();
})();
