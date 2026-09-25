/* THE PHONE SHELL — the app, on a phone's browser, the installed PWA and the
 * iPhone app (a WKWebView over this same site).
 *
 * The Hebrew edition's iPhone app is the reference (2026-09-25, "look at
 * navigation on the web, PWA, and iPhone ... apply the best to the samoan").
 * Its chrome no longer sits in three full-width bars: it FLOATS as glass
 * capsules over the text — the header (home · where you are · ⋯), the chapter
 * row (‹ previous · this chapter ▾ · next ›, with the target chapters named),
 * and the icon row — so the page reads edge to edge. Text size, theme and the
 * reading layout are one sheet behind ⋯ instead of three controls in three
 * places; Notes is a sheet over the reader, not a page instead of it; Search
 * is a whole page, because a keyboard covers a short sheet.
 *
 * Nothing is rebuilt. Every control drives the page's own: the drawer
 * (#nav-label), the search sheet, #font-scale, #toggle-diacritics, the theme
 * button, the mode buttons and the dock's arrows (kept in the DOM, hidden),
 * so what is next, what theme is on and what is stored stay the page's
 * decisions and the website is the same program. No Listen: this reader has
 * no read-aloud ("i never did that"). Five icons, not the Hebrew app's seven:
 * a bottom row holds five at most, so Bookmark lives in the ⋯ sheet — where
 * the Hebrew app also has it — and bookmarks are listed in Notes.
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
  var FULLSCREEN_KEY = 'sw-app-fullscreen';
  try { if (localStorage.getItem(FULLSCREEN_KEY) === '1') html.classList.add('sw-app-fullscreen'); } catch (e) {}
  var bootedAt = Date.now();
  document.write('<link rel="stylesheet" href="' + BASE + 'shell.css?v=3">');

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
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function onChapter() { return /^#\/(b|front)\//.test(location.hash || ''); }
  function onBook() { return /^#\/b\/[^/]+\/\d+/.test(location.hash || ''); }
  function shown(id) { var e = $(id); return !!(e && !e.hidden); }
  function click(id) { var e = $(id); if (e) e.click(); }
  function cssEsc(s) { s = String(s); return (window.CSS && CSS.escape) ? CSS.escape(s) : s.replace(/["\\]/g, '\\$&'); }
  function store(key) { try { return JSON.parse(localStorage.getItem(key) || '{}') || {}; } catch (e) { return {}; } }
  function button(cls, label, inner) {
    var b = el('button', cls); b.type = 'button';
    if (label) b.setAttribute('aria-label', label);
    if (inner != null) b.innerHTML = inner;
    return b;
  }

  var ICON = {
    library: '<path d="M4 3.5h4v17H4zM10 3.5h4v17h-4zM15.6 4.6l3.9-1 3.4 15.5-3.9 1z"/>',
    read:    '<path d="M12 6.5C10 5 7 4.6 3 5.2v13.3c4-.6 7 0 9 1.5 2-1.5 5-2.1 9-1.5V5.2c-4-.6-7-.2-9 1.3z"/><path d="M12 6.5v13.5"/>',
    search:  '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3 21 21"/>',
    notes:   '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4"/>',
    settings:'<path fill="currentColor" stroke="none" d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94L14.4 2.81c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41L9.25 5.35c-.59.24-1.13.57-1.62.94L5.24 5.33c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>',
    more:    '<circle fill="currentColor" stroke="none" cx="5.5" cy="12" r="1.9"/><circle fill="currentColor" stroke="none" cx="12" cy="12" r="1.9"/><circle fill="currentColor" stroke="none" cx="18.5" cy="12" r="1.9"/>',
    close:   '<path d="M6 6l12 12M18 6 6 18"/>',
    prev:    '<path d="M14.5 5.5 8 12l6.5 6.5"/>',
    next:    '<path d="M9.5 5.5 16 12l-6.5 6.5"/>',
    bookmark:'<path d="M7 3.5h10v17l-5-3.8-5 3.8z"/>',
    marked:  '<path fill="currentColor" d="M7 3.5h10v17l-5-3.8-5 3.8z"/>',
    marker:  '<path d="M4 20h16M6.5 16l8-8 3.5 3.5-8 8H6.5z"/>',
    underline: '<path d="M7 4v7a5 5 0 0 0 10 0V4M5 20h14"/>'
  };
  function svg(name, size) {
    return '<svg viewBox="0 0 24 24" width="' + (size || 24) + '" height="' + (size || 24) + '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + '</svg>';
  }

  /* ── THE CHROME ──────────────────────────────────────────────────────── */
  var row, title, chapterRow, capPrev, capHere, capNext, sheet, sheetScrim, sheetBody, sheetTitle;
  var sheetKind = null;                       // 'display' | 'notes' | null
  var ITEMS = [
    { id: 'library', name: 'Tusi · Library' }, { id: 'read', name: 'Faitau · Read' }, { id: 'search', name: 'Suʻe · Search' },
    { id: 'notes', name: 'Manatu · Notes' }, { id: 'settings', name: 'Faʻaaliga · Display' }
  ];

  function build() {
    if ($('sw-app-row')) return;

    /* Chrome under the clock, for the installed web app only: its clock is
       always white (black-translucent), and the header is a floating capsule
       now, so the paper would otherwise run up behind it. The iPhone app's
       clock follows what is under it, and a browser tab has its own bar, so
       shell.css shows this strip in standalone display mode alone. */
    var strip = el('div'); strip.id = 'sw-app-statusbar'; document.body.appendChild(strip);

    /* THE HEADER CAPSULE: home · where you are · ⋯. The page's own bar is
       re-dressed by shell.css; the pill's place is taken by a plain title,
       because the chapter row below is where "open the contents" lives now,
       and the ⋯ stands for text size, theme and layout together. */
    var top = document.querySelector('.controls-top');
    if (top) {
      title = el('div', 'sw-app-title-text');
      title.id = 'sw-app-title';
      var pill = $('nav-label');
      if (pill && pill.parentNode) pill.parentNode.insertBefore(title, pill);
      var right = top.querySelector('.bar-right') || top;
      var more = button('sw-app-more', 'Faʻaaliga · Display options', svg('more', 24));
      more.id = 'sw-app-more';
      more.addEventListener('click', function () { tap('settings'); });
      right.appendChild(more);
    }

    /* THE CHAPTER ROW: the dock's arrows, in reach of a thumb and naming
       where they go; the chapter between them opens the contents. */
    chapterRow = el('nav'); chapterRow.id = 'sw-app-chapter-row'; chapterRow.setAttribute('aria-label', 'Mataupu · Chapter');
    capPrev = button('sw-app-cap sw-app-cap-prev', 'Mataupu muʻa · Previous chapter', svg('prev', 20) + '<span class="sw-app-cap-n"></span>');
    capHere = button('sw-app-cap sw-app-cap-here', 'Tatala le lisi · Open the contents', '<span class="sw-app-cap-label"></span><span class="sw-app-caret" aria-hidden="true">▾</span>');
    capNext = button('sw-app-cap sw-app-cap-next', 'Mataupu sosoo · Next chapter', '<span class="sw-app-cap-n"></span>' + svg('next', 20));
    capPrev.addEventListener('click', function () { turn('prev'); });
    capNext.addEventListener('click', function () { turn('next'); });
    capHere.addEventListener('click', function () { tap('library'); });
    chapterRow.appendChild(capPrev); chapterRow.appendChild(capHere); chapterRow.appendChild(capNext);
    document.body.appendChild(chapterRow);

    /* THE ICON ROW */
    row = el('nav'); row.id = 'sw-app-row'; row.setAttribute('aria-label', 'App');
    ITEMS.forEach(function (it) {
      var b = button('', it.name, svg(it.id, 26)); b.dataset.id = it.id;
      b.addEventListener('click', function () { tap(it.id); });
      row.appendChild(b);
    });
    document.body.appendChild(row);

    /* ONE SHEET, two jobs: Display and Notes. It rises over the reader and
       leaves it in view; the handle takes it to full height and back. */
    sheetScrim = el('div'); sheetScrim.id = 'sw-app-sheet-scrim';
    sheetScrim.addEventListener('click', closeSheet);
    sheet = el('section'); sheet.id = 'sw-app-sheet';
    sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'false'); sheet.setAttribute('aria-labelledby', 'sw-app-sheet-title');
    var grab = button('sw-app-grab', 'Faʻalautele · Expand', '<span></span>');
    grab.addEventListener('click', function () { sheet.classList.toggle('large'); grab.setAttribute('aria-label', sheet.classList.contains('large') ? 'Faʻaitiitia · Shrink' : 'Faʻalautele · Expand'); });
    var head = el('div', 'sw-app-sheet-head');
    sheetTitle = el('h2', 'sw-app-sheet-title'); sheetTitle.id = 'sw-app-sheet-title';
    var x = button('sw-app-x', 'Tapuni · Close', svg('close', 20));
    x.addEventListener('click', closeSheet);
    head.appendChild(sheetTitle); head.appendChild(x);
    sheetBody = el('div', 'sw-app-scroll');
    sheet.appendChild(grab); sheet.appendChild(head); sheet.appendChild(sheetBody);
    document.body.appendChild(sheetScrim); document.body.appendChild(sheet);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheetKind) closeSheet(); });

    /* The shell follows the page: its drawer and sheets opening and closing,
       the dock's arrows changing target, the reference changing. */
    var obs = new MutationObserver(function () { syncChrome(); markRow(); });
    ['drawer', 'search', 'settings', 'dock'].forEach(function (id) { var e = $(id); if (e) obs.observe(e, { attributes: true, attributeFilter: ['hidden'] }); });
    ['dock-prev', 'dock-next'].forEach(function (id) { var e = $(id); if (e) obs.observe(e, { attributes: true, attributeFilter: ['disabled', 'title', 'aria-label'] }); });
    var lab = $('nav-label'); if (lab) obs.observe(lab, { childList: true, characterData: true, subtree: true });
    window.addEventListener('hashchange', function () { if (sheetKind === 'notes') closeSheet(); syncChrome(); markRow(); });

    syncChrome();
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

  /* The header title and the chapter row read the page's own state. */
  function hereLabel() {
    var lab = $('nav-label');
    return lab ? lab.textContent.replace(/\s*▾\s*$/, '').trim() : '';
  }
  function bookName(ref) { var m = /^(.*\S)\s+\d+$/.exec(ref || ''); return m ? m[1] : ref; }
  function targetOf(id) {
    var b = $(id);
    if (!b || b.disabled) return '';
    return (b.getAttribute('title') || '').trim();
  }
  function shortTarget(target, here) {
    // the same book: only its chapter number; another book: its name as well
    if (!target) return '';
    return bookName(target) === bookName(here) ? target.slice(bookName(target).length).trim() : target;
  }
  function syncChrome() {
    var here = hereLabel();
    if (title) title.textContent = here || 'O le Tusi a Mamona';
    /* THE ROW IS FOR THE BOOKS. On the landing the covers are the way in and
       the page stands alone, as the Hebrew app's landing does on an iPhone
       (user, 2026-09-25: "does NOT show the footer on the landing pages...
       only in the books"). */
    html.classList.toggle('sw-app-in-book', onChapter());
    if (!chapterRow) return;
    var dock = $('dock');
    var live = !!(dock && !dock.hidden) && onChapter();
    html.classList.toggle('sw-app-has-chapter', live);
    if (!live) return;
    capHere.querySelector('.sw-app-cap-label').textContent = here;
    capHere.setAttribute('aria-label', here + ' · Tatala le lisi · Open the contents');
    [['dock-prev', capPrev], ['dock-next', capNext]].forEach(function (pair) {
      var t = targetOf(pair[0]), b = pair[1];
      b.disabled = !t;
      b.querySelector('.sw-app-cap-n').textContent = shortTarget(t, here);
      b.setAttribute('aria-label', (pair[0] === 'dock-prev' ? 'Mataupu muʻa · Previous: ' : 'Mataupu sosoo · Next: ') + (t || '—'));
    });
  }

  function selectedId() {
    if (sheetKind === 'notes') return 'notes';
    if (sheetKind === 'display') return 'settings';
    if (shown('drawer')) return 'library';
    if (shown('search')) return 'search';
    return onChapter() ? 'read' : null;
  }
  function markRow() {
    if (!row) return;
    var sel = selectedId();
    Array.prototype.forEach.call(row.children, function (b) {
      if (b.dataset.id === sel) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
    });
  }

  /* Close whatever is open, then open the one thing asked for. */
  function closeAll(except) {
    if (except !== 'library' && shown('drawer')) click('btn-drawer-close');
    if (except !== 'search' && shown('search')) click('btn-search-close');
    if (shown('settings')) click('btn-settings-close');
    if (except !== 'notes' && except !== 'settings') closeSheet();
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
    else if (id === 'search') { click('btn-search'); setTimeout(function () { var i = $('search-input'); if (i) try { i.focus(); } catch (e) {} }, 80); }
    else if (id === 'settings') openSheet('display');
    else if (id === 'notes') openSheet('notes');
    markRow();
  }

  /* ── THE SHEET ───────────────────────────────────────────────────────── */
  var sheetOpener = null;
  function openSheet(kind) {
    if (!sheetKind) sheetOpener = document.activeElement;
    sheetKind = kind;
    sheet.classList.remove('large');
    sheetBody.innerHTML = '';
    sheetTitle.textContent = kind === 'display' ? 'Faʻaaliga · Display' : 'Manatu · Notes';
    if (kind === 'display') renderDisplay(); else renderNotes();
    html.classList.add('sw-app-sheet-open');
    sheet.classList.add('open'); sheetScrim.classList.add('open');
    markRow();
    setTimeout(function () { var x = sheet.querySelector('.sw-app-x'); if (x) try { x.focus({ preventScroll: true }); } catch (e) {} }, 60);
  }
  function closeSheet() {
    if (!sheetKind) return;
    sheetKind = null;
    sheet.classList.remove('open', 'large'); sheetScrim.classList.remove('open');
    html.classList.remove('sw-app-sheet-open');
    sheetBody.innerHTML = '';
    markRow();
    var back = sheetOpener; sheetOpener = null;
    var now = document.activeElement;
    if (back && back !== document.body && document.contains(back) && (!now || now === document.body || sheet.contains(now))) try { back.focus({ preventScroll: true }); } catch (e) {}
  }
  function section(text) { var h = el('div', 'sw-app-h', text); sheetBody.appendChild(h); var c = el('div', 'sw-app-card'); sheetBody.appendChild(c); return c; }
  function rowIn(c, inner, onClick) { var r = button('sw-app-r', null, inner); r.addEventListener('click', onClick); c.appendChild(r); return r; }

  /* DISPLAY: the page's own controls, gathered. */
  function currentTheme() { return html.getAttribute('data-theme') || 'light'; }
  function setTheme(id) {
    // the page's button cycles light → sepia → dark and remembers the choice
    for (var i = 0; i < 3 && currentTheme() !== id; i++) click('btn-theme');
  }
  function modeButtons() { var m = $('modebar'); return m ? Array.prototype.slice.call(m.querySelectorAll('.mode-btn')) : []; }
  function renderDisplay() {
    /* text size */
    var size = section('Lapoʻa o mataitusi · Text size');
    var fs = $('font-scale');
    var sizeRow = el('div', 'sw-app-slider');
    sizeRow.innerHTML = '<span class="sw-app-a sw-app-a-small" aria-hidden="true">A</span>';
    var range = el('input'); range.type = 'range'; range.min = fs ? fs.min : '0.8'; range.max = fs ? fs.max : '2.0'; range.step = fs ? fs.step : '0.1';
    range.value = fs ? fs.value : '1'; range.setAttribute('aria-label', 'Lapoʻa o mataitusi · Text size');
    range.addEventListener('input', function () { if (!fs) return; fs.value = range.value; fs.dispatchEvent(new Event('input', { bubbles: true })); });
    sizeRow.appendChild(range);
    sizeRow.insertAdjacentHTML('beforeend', '<span class="sw-app-a sw-app-a-big" aria-hidden="true">A</span>');
    size.appendChild(sizeRow);

    /* theme */
    var themes = section('Lanu · Theme');
    var sw = el('div', 'sw-app-swatches'); sw.setAttribute('role', 'radiogroup'); sw.setAttribute('aria-label', 'Lanu · Theme');
    [['light', 'Malamalama', 'Light'], ['sepia', 'Sepia', 'Sepia'], ['dark', 'Pogisa', 'Dark']].forEach(function (t) {
      var b = button('sw-app-swatch sw-app-swatch-' + t[0], t[1] + ' · ' + t[2], '<span class="sw-app-chip" aria-hidden="true"><i></i><i></i><i></i></span><span class="sw-app-swatch-name">' + esc(t[2]) + '</span>');
      b.setAttribute('role', 'radio');
      b.setAttribute('aria-checked', String(currentTheme() === t[0]));
      b.addEventListener('click', function () {
        setTheme(t[0]);
        Array.prototype.forEach.call(sw.children, function (s) { s.setAttribute('aria-checked', 'false'); });
        b.setAttribute('aria-checked', 'true');
      });
      sw.appendChild(b);
    });
    themes.appendChild(sw);

    /* reading layout + the marked register */
    var reading = section('Faitau · Reading');
    var seg = el('div', 'sw-app-seg'); seg.setAttribute('role', 'radiogroup'); seg.setAttribute('aria-label', 'Faitau · Reading layout');
    function drawSeg() {
      seg.innerHTML = '';
      modeButtons().forEach(function (mb, i) {
        var s = button('sw-app-seg-b', mb.textContent, esc(mb.textContent));
        s.setAttribute('role', 'radio');
        s.setAttribute('aria-checked', String(mb.classList.contains('active')));
        s.addEventListener('click', function () { var live = modeButtons()[i]; if (live) live.click(); setTimeout(drawSeg, 0); });
        seg.appendChild(s);
      });
    }
    drawSeg();
    reading.appendChild(seg);
    var dia = $('toggle-diacritics');
    if (dia) reading.appendChild(toggleRow('Faʻailoga leo · Diacritics', dia.checked, function (on) { dia.checked = on; dia.dispatchEvent(new Event('change', { bubbles: true })); }));
    reading.appendChild(toggleRow('Mata atoa pe a faitau · Full screen on scroll', html.classList.contains('sw-app-fullscreen'), function (on) {
      html.classList.toggle('sw-app-fullscreen', on);
      try { localStorage.setItem(FULLSCREEN_KEY, on ? '1' : '0'); } catch (e) {}
    }));

    /* this chapter */
    if (onBook()) {
      var ch = section('Lenei mataupu · This chapter');
      var saved = isBookmarked();
      var bm = rowIn(ch, '<span class="sw-app-ic sw-app-here">' + svg(saved ? 'marked' : 'bookmark', 22) + '</span><span class="sw-app-t sw-app-grow">' + (saved ? 'Ua faʻailogaina · Bookmarked' : 'Faʻailoga lenei mataupu · Bookmark this chapter') + '</span>', function () {
        var now = toggleBookmark();
        bm.querySelector('.sw-app-ic').innerHTML = svg(now ? 'marked' : 'bookmark', 22);
        bm.querySelector('.sw-app-t').textContent = now ? 'Ua faʻailogaina · Bookmarked' : 'Faʻailoga lenei mataupu · Bookmark this chapter';
        bm.setAttribute('aria-pressed', String(now));
      });
      bm.setAttribute('aria-pressed', String(saved));
    }

    /* offline, as the page reports it */
    var off = $('offline-state');
    if (off && off.textContent.trim() && off.textContent.trim() !== '…') {
      var oc = section('Initaneti · Offline');
      var o = el('div', 'sw-app-r sw-app-static');
      o.innerHTML = '<span class="sw-app-t sw-app-grow">' + esc(off.textContent.trim()) + '</span>';
      oc.appendChild(o);
    }
  }
  function toggleRow(label, on, change) {
    var r = el('label', 'sw-app-r sw-app-toggle');
    var t = el('span', 'sw-app-t sw-app-grow', label);
    var i = el('input'); i.type = 'checkbox'; i.checked = !!on; i.setAttribute('role', 'switch');
    i.addEventListener('change', function () { change(i.checked); });
    r.appendChild(t); r.appendChild(i);
    return r;
  }

  /* ── BOOKMARKS: a chapter, kept for later ────────────────────────────── */
  var BM_KEY = 'bom.bookmarks.v1';
  function bookmarks() { try { var a = JSON.parse(localStorage.getItem(BM_KEY) || '[]'); return Array.isArray(a) ? a : []; } catch (e) { return []; } }
  function chapterHash() { var m = /^#\/b\/[^/]+\/\d+/.exec(location.hash || ''); return m ? m[0] : ''; }
  function isBookmarked() { var h = chapterHash(); return !!h && bookmarks().some(function (b) { return b.hash === h; }); }
  function toggleBookmark() {
    var h = chapterHash(); if (!h) return false;
    var list = bookmarks().filter(function (b) { return b.hash !== h; });
    var on = list.length === bookmarks().length;
    if (on) list.unshift({ hash: h, ts: Date.now() });
    try { localStorage.setItem(BM_KEY, JSON.stringify(list)); } catch (e) {}
    return on;
  }

  /* ── NOTES: the reader's own marks, from the page's stores ───────────── */
  var index = null;
  function loadIndex(done) {
    if (index) { done(index); return; }
    fetch(BASE + 'data/index.json').then(function (r) { return r.json(); }).then(function (j) { index = j; done(j); }, function () { done(null); });
  }
  function bookOf(id) { if (!index) return null; for (var i = 0; i < index.books.length; i++) if (index.books[i].id === id) return index.books[i]; return null; }
  function refLabel(verseKey) {
    var p = String(verseKey).split('|'), b = bookOf(p[0]);
    return (b ? b.nameSm : p[0]) + ' ' + p[1] + (p[2] ? ':' + p[2] : '');
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
    if (!p[2]) return;
    var tries = 0;
    (function find() {
      var elv = document.querySelector('.verse[data-key="' + cssEsc(verseKey) + '"]');
      if (elv) { elv.scrollIntoView({ block: 'center' }); elv.classList.add('sw-app-flash'); setTimeout(function () { elv.classList.remove('sw-app-flash'); }, 2400); return; }
      if (++tries < 40) setTimeout(find, 100);
    })();
  }
  function renderNotes() {
    sheetBody.appendChild(el('div', 'sw-app-hint', 'Reading your marks…'));
    loadIndex(function () {
      if (sheetKind !== 'notes') return;
      sheetBody.innerHTML = '';
      var notes = store('bom.notes.v1'), hl = store('bom.highlights.v1'), ul = store('bom.underlines.v1');
      var bms = bookmarks();
      var noteKeys = sortKeys(Object.keys(notes).filter(function (k) { return notes[k] && String(notes[k]).trim(); }));
      var byVerse = function (o) { var m = {}; Object.keys(o).forEach(function (k) { if (!o[k]) return; var v = k.split('|').slice(0, 3).join('|'); m[v] = (m[v] || 0) + 1; }); return m; };
      var hlV = byVerse(hl), ulV = byVerse(ul);
      var hlKeys = sortKeys(Object.keys(hlV)), ulKeys = sortKeys(Object.keys(ulV));
      if (!bms.length && !noteKeys.length && !hlKeys.length && !ulKeys.length) {
        var e = el('div', 'sw-app-empty');
        e.innerHTML = '<span class="sw-app-ic">' + svg('notes', 44) + '</span><div class="sw-app-t sw-app-bold">E leai se faʻailoga · Nothing marked yet</div><div class="sw-app-sub">Tap a word or a verse number in the reader to highlight, underline or add a note. Bookmark a chapter from ⋯.</div>';
        sheetBody.appendChild(e); return;
      }
      if (bms.length) {
        var cb = section('Faʻailoga tusi · Bookmarks');
        bms.forEach(function (b) {
          var m = /^#\/b\/([^/]+)\/(\d+)/.exec(b.hash || ''); if (!m) return;
          rowIn(cb, '<span class="sw-app-ic sw-app-here">' + svg('marked', 22) + '</span><span class="sw-app-t sw-app-grow">' + esc(refLabel(m[1] + '|' + m[2])) + '</span>', function () { closeAll(); location.hash = b.hash; });
        });
      }
      if (noteKeys.length) {
        var cn = section('Manatu · Notes');
        noteKeys.forEach(function (k) { var v = k.split('#')[0]; rowIn(cn, '<span class="sw-app-grow"><span class="sw-app-ref">' + esc(refLabel(v)) + '</span><span class="sw-app-t sw-app-clamp4">' + esc(notes[k]) + '</span></span>', function () { goToVerse(v); }); });
      }
      if (hlKeys.length) {
        var ch = section('Faʻailoga · Highlights');
        hlKeys.forEach(function (v) { rowIn(ch, '<span class="sw-app-ic sw-app-here">' + svg('marker', 22) + '</span><span class="sw-app-t sw-app-grow">' + esc(refLabel(v)) + '</span><span class="sw-app-n">' + hlV[v] + (hlV[v] === 1 ? ' word' : ' words') + '</span>', function () { goToVerse(v); }); });
      }
      if (ulKeys.length) {
        var cu = section('Vase i lalo · Underlines');
        ulKeys.forEach(function (v) { rowIn(cu, '<span class="sw-app-ic sw-app-here">' + svg('underline', 22) + '</span><span class="sw-app-t sw-app-grow">' + esc(refLabel(v)) + '</span><span class="sw-app-n">' + ulV[v] + (ulV[v] === 1 ? ' word' : ' words') + '</span>', function () { goToVerse(v); }); });
      }
    });
  }

  /* ── READING FOLDS THE CHAPTER ROW: a finger's drag down, and up (or the
     top of the page) brings it back. The icon row stays; with "Full screen
     on scroll" the header capsule goes too. ── */
  function watchScroll() {
    var lastY = window.scrollY || 0, dragging = false, lastDrag = 0;
    document.addEventListener('touchmove', function () { dragging = true; lastDrag = Date.now(); }, { passive: true });
    document.addEventListener('touchend', function () { dragging = false; }, { passive: true });
    document.addEventListener('touchcancel', function () { dragging = false; }, { passive: true });
    window.addEventListener('scroll', function () {
      var y = window.scrollY || 0, dy = y - lastY; lastY = y;
      if (y <= 40) { html.classList.remove('sw-app-reading'); return; }
      if (sheetKind) return;
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
  function topClear() {
    var h = document.querySelector('.controls-top');
    return h ? Math.max(0, h.getBoundingClientRect().bottom) : 56;
  }
  function watchVerse() {
    var timer = null;
    window.addEventListener('scroll', function () {
      if (timer) return;
      timer = setTimeout(function () {
        timer = null;
        if (!onChapter()) return;
        var rows = document.querySelectorAll('.verse[data-key]'), edge = topClear() + 12;
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
      var elv = document.querySelector('.verse[data-key="' + cssEsc(v) + '"]');
      if (elv) { window.scrollTo(0, elv.getBoundingClientRect().top + window.scrollY - topClear() - 8); return; }
      if (++tries < 40) setTimeout(find, 100);
    })();
  }

  /* ── A SWIPE TURNS THE CHAPTER, as it does in the Hebrew reader: through the
     dock's own arrows, so what is next and what is previous stays the page's
     decision. Left to right is a book in Samoan, so a swipe LEFT goes on.
     Nothing turns while a sheet, the drawer or the search is up, or from a
     touch that began on the chrome. ── */
  function turn(dir) {
    var b = $(dir === 'next' ? 'dock-next' : 'dock-prev');
    if (!b || b.disabled || b.getAttribute('aria-disabled') === 'true') return;
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
      fromBar = !!(e.target && e.target.closest && e.target.closest('#sw-app-row, #sw-app-chapter-row, #sw-app-sheet, .controls-bottom, .controls-top, #actionbar, .sheet, .drawer'));
    }, { passive: true });
    document.addEventListener('touchend', function (e) {
      if (!live) return; live = false;
      if (fromBar || Date.now() - t0 > 700) return;
      var t = e.changedTouches && e.changedTouches[0]; if (!t) return;
      var dx = t.clientX - x0, dy = t.clientY - y0;
      if (Math.abs(dx) < 70 || Math.abs(dy) > 50) return;
      if (!onChapter() || sheetKind || shown('drawer') || shown('search') || shown('settings') || shown('note-sheet')) return;
      turn(dx < 0 ? 'next' : 'prev');
    }, { passive: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
