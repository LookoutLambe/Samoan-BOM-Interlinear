/* THE PHONE SHELL — the app, on a phone's browser, the installed PWA and the
 * iPhone app (a WKWebView over this same site).
 *
 * The Hebrew edition's apps frame their reader with a row of icons along the
 * bottom and native pages behind them; its website gives a phone the same
 * frame (app-shell/pwa_shell.js there). This is that frame for this reader,
 * fitted to the parts it already has: the library drawer, the search and
 * settings sheets, the notes, highlights and underlines in localStorage, the
 * dock of chapter arrows and reading modes, the theme button. Nothing is
 * rebuilt; the row opens what the page already draws, and one new panel
 * lists the reader's marks. No Listen: this reader has no read-aloud.
 *
 * COMPUTERS ARE UNTOUCHED. The gate is the pointer: a phone or tablet has a
 * coarse pointer and no hover, a Mac or PC has a mouse and gets the website
 * exactly as it was. The iPhone app always gets the shell: it serves the site
 * over tusi://local, which is how the shell knows it is inside the app.
 * Testing on a computer: ?shell=1 forces the shell on (?shell=0 off).
 */
(function () {
  'use strict';

  /* ── 1. THE GATE ─────────────────────────────────────────────────────── */
  var inApp = location.protocol === 'tusi:';
  var phone, force = /(^|[?&])shell=([01])(&|$)/.exec(location.search || '');
  try {
    if (force) { phone = force[2] === '1'; localStorage.setItem('sw-shell-force', force[2]); }
    else { var f = localStorage.getItem('sw-shell-force'); if (f === '1' || f === '0') phone = f === '1'; }
  } catch (e) {}
  if (phone === undefined) {
    try { phone = window.matchMedia('(pointer: coarse) and (hover: none)').matches; } catch (e) { phone = false; }
  }
  if (!phone && !inApp) return;

  var me = document.currentScript;
  var BASE = (me && me.src) ? me.src.replace(/shell\.js.*$/, '') : '';
  var html = document.documentElement;
  html.classList.add('sw-web-shell', 'sw-app-booting');
  if (inApp) html.classList.add('sw-in-app');
  var bootedAt = Date.now();
  document.write('<link rel="stylesheet" href="' + BASE + 'shell.css?v=1">');

  /* OPEN IN THE BOOK. The installed app (start_url carries ?boot=1) and the
     iPhone app open where the reader left off, from the page's own bom.last;
     a browser tab opens on the shelf, as the website does. The page routes
     on the hash it finds at load, so setting it here is enough. */
  var booted = false;
  if ((inApp || /(^|[?&])boot=1(&|$)/.test(location.search || '')) && (!location.hash || location.hash === '#/')) {
    try { var last = localStorage.getItem('bom.last'); if (last && /^#\/b\/[^/]+\/\d+/.test(last)) { location.hash = last; booted = true; } } catch (e) {}
  }

  /* ── helpers ─────────────────────────────────────────────────────────── */
  function $(id) { return document.getElementById(id); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function onChapter() { return /^#\/(b|front)\//.test(location.hash || ''); }
  function shown(id) { var e = $(id); return !!(e && !e.hidden); }
  function click(id) { var e = $(id); if (e) e.click(); }

  var ICON = {
    library: '<path d="M4 3.5h4v17H4zM10 3.5h4v17h-4zM15.6 4.6l3.9-1 3.4 15.5-3.9 1z"/>',
    read:    '<path d="M12 6.5C10 5 7 4.6 3 5.2v13.3c4-.6 7 0 9 1.5 2-1.5 5-2.1 9-1.5V5.2c-4-.6-7-.2-9 1.3z"/><path d="M12 6.5v13.5"/>',
    search:  '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3 21 21"/>',
    notes:   '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4"/>',
    settings:'<path fill="currentColor" stroke="none" d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94L14.4 2.81c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41L9.25 5.35c-.59.24-1.13.57-1.62.94L5.24 5.33c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>',
    marker:  '<path d="M4 20h16M6.5 16l8-8 3.5 3.5-8 8H6.5z"/>',
    underline: '<path d="M7 4v7a5 5 0 0 0 10 0V4M5 20h14"/>'
  };
  function svg(name, size) {
    return '<svg viewBox="0 0 24 24" width="' + (size || 24) + '" height="' + (size || 24) + '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + '</svg>';
  }

  /* ── THE ROW AND THE NOTES PANEL ─────────────────────────────────────── */
  var row, panel, notesOpen = false;
  var ITEMS = [
    { id: 'library', name: 'Tusi · Library' }, { id: 'read', name: 'Faitau · Read' }, { id: 'search', name: 'Suʻe · Search' },
    { id: 'notes', name: 'Manatu · Notes' }, { id: 'settings', name: 'Faʻaaliga · Settings' }
  ];

  function build() {
    if ($('sw-app-row')) return;
    row = el('nav'); row.id = 'sw-app-row'; row.setAttribute('aria-label', 'App');
    ITEMS.forEach(function (it) {
      var b = el('button'); b.type = 'button'; b.setAttribute('aria-label', it.name); b.dataset.id = it.id;
      b.innerHTML = svg(it.id, 26);
      b.addEventListener('click', function () { tap(it.id); });
      row.appendChild(b);
    });
    panel = el('div'); panel.id = 'sw-app-panel'; panel.setAttribute('role', 'dialog');
    document.body.appendChild(row); document.body.appendChild(panel);
    /* the row follows the page's own sheets and drawer as they open and close */
    var obs = new MutationObserver(markRow);
    ['drawer', 'search', 'settings'].forEach(function (id) { var e = $(id); if (e) obs.observe(e, { attributes: true, attributeFilter: ['hidden'] }); });
    window.addEventListener('hashchange', function () { closeNotes(); markRow(); });
    markRow();
    watchScroll();
    watchSwipe();
    watchVerse();
    if (booted) restoreVerse();
    var done = false;
    function unboot() { if (done) return; done = true; html.classList.remove('sw-app-booting'); }
    function ready() { var left = 900 - (Date.now() - bootedAt); setTimeout(unboot, left > 0 ? left : 0); }
    if (document.readyState === 'complete') ready(); else window.addEventListener('load', ready);
    setTimeout(unboot, 4500 - (Date.now() - bootedAt));
  }

  function selectedId() {
    if (notesOpen) return 'notes';
    if (shown('drawer')) return 'library';
    if (shown('search')) return 'search';
    if (shown('settings')) return 'settings';
    return onChapter() ? 'read' : null;
  }
  function markRow() {
    if (!row) return;
    var sel = selectedId();
    Array.prototype.forEach.call(row.children, function (b) {
      if (b.dataset.id === sel) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
    });
  }

  /* Close whatever the page has open, then open the one thing asked for. */
  function closeAll(except) {
    if (except !== 'library' && shown('drawer')) click('btn-drawer-close');
    if (except !== 'search' && shown('search')) click('btn-search-close');
    if (except !== 'settings' && shown('settings')) click('btn-settings-close');
    if (except !== 'notes') closeNotes();
  }
  function tap(id) {
    var was = selectedId();
    if (id === 'read') {
      closeAll();
      if (!onChapter()) {
        var last = null; try { last = localStorage.getItem('bom.last'); } catch (e) {}
        location.hash = (last && /^#\/b\//.test(last)) ? last : '#/b/1nephi/1';
        restoreVerse();
      }
      markRow(); return;
    }
    if (was === id) { closeAll(); markRow(); return; }
    closeAll(id);
    if (id === 'library') click('nav-label');
    else if (id === 'search') { click('btn-search'); setTimeout(function () { var i = $('search-input'); if (i) try { i.focus(); } catch (e) {} }, 60); }
    else if (id === 'settings') click('btn-settings');
    else if (id === 'notes') openNotes();
    markRow();
  }

  /* ── NOTES: the reader's own marks, from the page's stores. ──────────── */
  var index = null;
  function loadIndex(done) {
    if (index) { done(index); return; }
    fetch(BASE + 'data/index.json').then(function (r) { return r.json(); }).then(function (j) { index = j; done(j); }, function () { done(null); });
  }
  function store(key) { try { return JSON.parse(localStorage.getItem(key) || '{}') || {}; } catch (e) { return {}; } }
  function bookOf(id) { if (!index) return null; for (var i = 0; i < index.books.length; i++) if (index.books[i].id === id) return index.books[i]; return null; }
  function refLabel(verseKey) {
    var p = String(verseKey).split('|'), b = bookOf(p[0]);
    return (b ? b.nameSm : p[0]) + ' ' + p[1] + ':' + p[2];
  }
  function bookOrder() { var o = {}; if (index) index.books.forEach(function (b, i) { o[b.id] = i; }); return o; }
  function sortKeys(keys) {
    var o = bookOrder();
    return keys.sort(function (a, b) {
      var A = a.split('|'), B = b.split('|');
      return (o[A[0]] - o[B[0]]) || (+A[1] - +B[1]) || (+A[2] - +B[2]);
    });
  }
  function goToVerse(verseKey) {
    var p = String(verseKey).split('|');
    closeAll();
    location.hash = '#/b/' + p[0] + '/' + p[1];
    var tries = 0;
    (function find() {
      var elv = document.querySelector('.verse[data-key="' + verseKey + '"]');
      if (elv) { elv.scrollIntoView({ block: 'center' }); elv.classList.add('sw-app-flash'); setTimeout(function () { elv.classList.remove('sw-app-flash'); }, 2400); return; }
      if (++tries < 40) setTimeout(find, 100);
    })();
  }
  function card(parent) { var c = el('div', 'sw-app-card'); parent.appendChild(c); return c; }
  function header(parent, text) { parent.appendChild(el('div', 'sw-app-h', text)); }
  function rowIn(c, inner, onClick) { var r = el('button', 'sw-app-r'); r.type = 'button'; r.innerHTML = inner; r.addEventListener('click', onClick); c.appendChild(r); return r; }
  function openNotes() {
    notesOpen = true; panel.innerHTML = ''; panel.classList.add('open');
    var bar = el('div', 'sw-app-bar'); bar.appendChild(el('div', 'sw-app-title', 'Manatu · Notes'));
    var scroll = el('div', 'sw-app-scroll'); panel.appendChild(bar); panel.appendChild(scroll);
    scroll.appendChild(el('div', 'sw-app-hint', 'Reading your marks…'));
    loadIndex(function () {
      if (!notesOpen) return;
      scroll.innerHTML = '';
      var notes = store('bom.notes.v1'), hl = store('bom.highlights.v1'), ul = store('bom.underlines.v1');
      var noteKeys = sortKeys(Object.keys(notes).filter(function (k) { return notes[k] && String(notes[k]).trim(); }));
      var byVerse = function (o) { var m = {}; Object.keys(o).forEach(function (k) { if (!o[k]) return; var v = k.split('|').slice(0, 3).join('|'); m[v] = (m[v] || 0) + 1; }); return m; };
      var hlV = byVerse(hl), ulV = byVerse(ul);
      var hlKeys = sortKeys(Object.keys(hlV)), ulKeys = sortKeys(Object.keys(ulV));
      if (!noteKeys.length && !hlKeys.length && !ulKeys.length) {
        var e = el('div', 'sw-app-empty');
        e.innerHTML = '<span class="sw-app-ic">' + svg('notes', 48) + '</span><div class="sw-app-t sw-app-bold">E leai se faʻailoga · Nothing marked yet</div><div class="sw-app-sub">Tap a word or a verse number in the reader to highlight, underline or add a note.</div>';
        scroll.appendChild(e); return;
      }
      if (noteKeys.length) {
        header(scroll, 'Manatu · Notes'); var cn = card(scroll);
        noteKeys.forEach(function (k) { var v = k.split('#')[0]; rowIn(cn, '<span class="sw-app-grow"><span class="sw-app-ref">' + esc(refLabel(v)) + '</span><span class="sw-app-t sw-app-clamp4">' + esc(notes[k]) + '</span></span>', function () { goToVerse(v); }); });
        scroll.appendChild(el('div', 'sw-app-gap'));
      }
      if (hlKeys.length) {
        header(scroll, 'Faʻailoga · Highlights'); var ch = card(scroll);
        hlKeys.forEach(function (v) { rowIn(ch, '<span class="sw-app-ic sw-app-here">' + svg('marker', 22) + '</span><span class="sw-app-t sw-app-grow">' + esc(refLabel(v)) + '</span><span class="sw-app-n">' + hlV[v] + (hlV[v] === 1 ? ' word' : ' words') + '</span>', function () { goToVerse(v); }); });
        scroll.appendChild(el('div', 'sw-app-gap'));
      }
      if (ulKeys.length) {
        header(scroll, 'Vase i lalo · Underlines'); var cu = card(scroll);
        ulKeys.forEach(function (v) { rowIn(cu, '<span class="sw-app-ic sw-app-here">' + svg('underline', 22) + '</span><span class="sw-app-t sw-app-grow">' + esc(refLabel(v)) + '</span><span class="sw-app-n">' + ulV[v] + (ulV[v] === 1 ? ' word' : ' words') + '</span>', function () { goToVerse(v); }); });
      }
    });
  }
  function closeNotes() { if (!notesOpen) return; notesOpen = false; panel.classList.remove('open'); panel.innerHTML = ''; }

  /* ── READING FOLDS THE DOCK: a finger's drag down, and up brings it back. ── */
  function watchScroll() {
    var lastY = window.scrollY || 0, dragging = false, lastDrag = 0;
    document.addEventListener('touchmove', function () { dragging = true; lastDrag = Date.now(); }, { passive: true });
    document.addEventListener('touchend', function () { dragging = false; }, { passive: true });
    document.addEventListener('touchcancel', function () { dragging = false; }, { passive: true });
    window.addEventListener('scroll', function () {
      var y = window.scrollY || 0, dy = y - lastY; lastY = y;
      if (y <= 40) { html.classList.remove('sw-app-reading'); return; }
      if (!dragging && Date.now() - lastDrag > 1500) return;
      if (Math.abs(dy) < 6) return;
      html.classList.toggle('sw-app-reading', dy > 0);
    }, { passive: true });
  }

  /* ── THE VERSE, NOT JUST THE CHAPTER. The page records the chapter in
     bom.last; the shell also records the verse at the top of the screen as
     the reader scrolls, and on a reopen (the app, the installed app, the
     Read icon from the shelf) scrolls back to it once the chapter is up. ── */
  var VERSE_KEY = 'bom.lastVerse';
  function topBar() { var h = document.querySelector('.controls-top'); return (h && h.offsetHeight) || 56; }
  function watchVerse() {
    var timer = null;
    window.addEventListener('scroll', function () {
      if (timer) return;
      timer = setTimeout(function () {
        timer = null;
        if (!onChapter()) return;
        var rows = document.querySelectorAll('.verse[data-key]'), edge = topBar() + 12;
        for (var i = 0; i < rows.length; i++) {
          if (rows[i].getBoundingClientRect().bottom > edge) { try { localStorage.setItem(VERSE_KEY, rows[i].dataset.key); } catch (e) {} break; }
        }
      }, 250);
    }, { passive: true });
  }
  function restoreVerse() {
    var v = null; try { v = localStorage.getItem(VERSE_KEY); } catch (e) {}
    if (!v) return;
    var p = v.split('|');
    if ((location.hash || '').replace(/\/$/, '') !== '#/b/' + p[0] + '/' + p[1]) return;
    var tries = 0;
    (function find() {
      var elv = document.querySelector('.verse[data-key="' + v + '"]');
      if (elv) { window.scrollTo(0, elv.getBoundingClientRect().top + window.scrollY - topBar() - 8); return; }
      if (++tries < 40) setTimeout(find, 100);
    })();
  }

  /* ── A SWIPE TURNS THE CHAPTER, as it does in the Hebrew reader: through the
     dock's own arrows, so what is next and what is previous stays the page's
     decision. Left to right is a book in Samoan, so a swipe LEFT goes on.
     Nothing turns while a sheet, the drawer or the notes are up, or from a
     touch that began on the bars. ── */
  function turn(dir) {
    var b = $(dir === 'next' ? 'dock-next' : 'dock-prev');
    if (!b || b.disabled || b.getAttribute('aria-disabled') === 'true' || b.hidden) return;
    var v = $('view');
    if (v) {
      v.classList.remove('sw-app-turn-next', 'sw-app-turn-prev');
      void v.offsetWidth;
      v.classList.add(dir === 'next' ? 'sw-app-turn-next' : 'sw-app-turn-prev');
      setTimeout(function () { v.classList.remove('sw-app-turn-next', 'sw-app-turn-prev'); }, 360);
    }
    b.click();
  }
  function watchSwipe() {
    var x0 = 0, y0 = 0, t0 = 0, live = false, fromBar = false;
    document.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) { live = false; return; }
      var t = e.touches[0]; x0 = t.clientX; y0 = t.clientY; t0 = Date.now(); live = true;
      fromBar = !!(e.target && e.target.closest && e.target.closest('#sw-app-row, .controls-bottom, .controls-top, #actionbar, #sw-app-panel, .sheet, .drawer'));
    }, { passive: true });
    document.addEventListener('touchend', function (e) {
      if (!live) return; live = false;
      if (fromBar || Date.now() - t0 > 700) return;
      var t = e.changedTouches && e.changedTouches[0]; if (!t) return;
      var dx = t.clientX - x0, dy = t.clientY - y0;
      if (Math.abs(dx) < 70 || Math.abs(dy) > 50) return;
      if (!onChapter() || notesOpen || shown('drawer') || shown('search') || shown('settings') || shown('note-sheet')) return;
      turn(dx < 0 ? 'next' : 'prev');
    }, { passive: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
