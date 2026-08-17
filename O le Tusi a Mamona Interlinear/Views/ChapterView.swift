import SwiftUI
#if canImport(UIKit)
import UIKit
#elseif canImport(AppKit)
import AppKit
#endif

/// The reading view. One continuous horizontal pager over the whole book —
/// every front-matter section followed by every chapter — so the user can flip
/// like the Gospel Library app and swipe straight from the last front-matter
/// page into 1 Nephi 1. Instead of a paged `TabView` (which materializes every
/// child eagerly — 240+ heavy interlinear pages — and choked swiping), it uses
/// a horizontal paging `ScrollView` over a `LazyHStack`, so only the visible
/// and immediately-adjacent pages are ever built, and nothing is rebuilt during
/// the swipe. `scrolledItem` tracks the settled page and drives the title. A
/// fixed bottom `ReaderControlBar` switches display modes (Interlinear / Samoa
/// / Tutusa).
struct ReaderView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(AppSettings.self) private var settings
    @State private var scrolledItem: ReadingItem?
    @State private var didInitialScroll = false
    @State private var showFontSize = false
    @State private var noteEditorTarget: NoteEditorTarget?
    @State private var selection = WordSelectionModel()

    private let initialItem: ReadingItem

    init(item: ReadingItem) {
        self.initialItem = item
        self._scrolledItem = State(initialValue: item)
    }

    var body: some View {
        // The reading pager and the bottom banner are laid out as siblings in a
        // VStack (rather than the pager full-bleeding with the control bar added
        // as a `safeAreaInset`). This way the `GeometryReader` reports the exact
        // reading region — the space between the navigation bar and the control
        // bar — and each page is sized to it, so no verse line can slip behind
        // either banner.
        VStack(spacing: 0) {
            GeometryReader { geo in
                ScrollViewReader { proxy in
                    ScrollView(.horizontal) {
                        LazyHStack(spacing: 0) {
                            ForEach(library.allReadingItems) { item in
                                page(for: item)
                                    .frame(width: geo.size.width, height: geo.size.height)
                                    .id(item.id)
                            }
                        }
                        .scrollTargetLayout()
                    }
                    .scrollTargetBehavior(.paging)
                    .scrollPosition(id: $scrolledItem)
                    .scrollIndicators(.hidden)
                    // A LazyHStack won't honor an initial `scrollPosition` that
                    // points at a not-yet-built page (e.g. a chapter after the 6
                    // front-matter pages), so it parks on page 0. Jump explicitly
                    // once the geometry has a real width — `initial: true` fires
                    // on appear, and again if width resolves from 0 afterward.
                    .onChange(of: geo.size.width, initial: true) { _, width in
                        guard width > 0, !didInitialScroll else { return }
                        didInitialScroll = true
                        proxy.scrollTo(initialItem.id, anchor: .center)
                    }
                    .onChange(of: scrolledItem, initial: true) { _, item in
                        // Remember the furthest chapter reached for the landing
                        // page's "Continue reading" shortcut.
                        if case .chapter(let ref)? = item,
                           let order = library.allChapterRefs.firstIndex(of: ref) {
                            settings.noteChapterRead(
                                bookId: ref.bookId, chapter: ref.chapterNum, order: order
                            )
                        }
                    }
                }
            }

            VStack(spacing: 0) {
                if !selection.isEmpty {
                    WordActionBar(noteEditorTarget: $noteEditorTarget)
                        .transition(.move(edge: .bottom).combined(with: .opacity))
                }
                ReaderControlBar()
            }
            .animation(.easeInOut(duration: 0.2), value: selection.isEmpty)
        }
        .background(Theme.pageBg.ignoresSafeArea())
        .environment(\.scriptureFontScale, settings.fontScale)
        .environment(\.scriptureShowDiacritics, settings.showDiacritics)
        .navigationTitle(navTitle)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarBackground(Theme.headerBg, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
        #endif
        .toolbar {
            if #available(iOS 26.0, macOS 26.0, visionOS 26.0, *) {
                fontSizeItem.sharedBackgroundVisibility(.hidden)
            } else {
                fontSizeItem
            }
        }
        .libraryToolbar()
        .sheet(isPresented: $showFontSize) {
            FontSizeSheet()
        }
        .sheet(item: $noteEditorTarget) { target in
            NoteEditorSheet(
                verseKey: target.verseKey,
                referenceLabel: target.referenceLabel,
                samoanPreview: target.samoanPreview
            )
        }
        // Injected as the outermost modifier so both the scroll content *and*
        // the bottom `safeAreaInset` word-action bar are descendants that can
        // read the selection model.
        .environment(selection)
    }

    private var fontSizeItem: some ToolbarContent {
        ToolbarItem(placement: .primaryAction) {
            Button {
                showFontSize = true
            } label: {
                Image(systemName: "textformat.size")
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(Theme.headerText)
                    .accessibilityLabel("Lapo\u{2019}a o le Tusitusiga")
            }
        }
    }

    @ViewBuilder
    private func page(for item: ReadingItem) -> some View {
        switch item {
        case .front(let id):
            if let section = library.frontMatterSection(id: id) {
                FrontMatterPage(section: section, mode: settings.readerMode)
            } else {
                ContentUnavailableView("E lē maua", systemImage: "questionmark.folder")
            }
        case .chapter(let ref):
            ChapterPageView(ref: ref, noteEditorTarget: $noteEditorTarget)
        }
    }

    private var navTitle: String {
        switch scrolledItem ?? initialItem {
        case .front(let id):
            return library.frontMatterSection(id: id)?.titleEn ?? ""
        case .chapter(let ref):
            guard let book = library.book(id: ref.bookId) else { return "" }
            return "\(book.nameEn) \(ref.chapterNum)"
        }
    }
}

/// Identifies the verse whose note is being edited. `Identifiable` so it can
/// drive a `.sheet(item:)` presentation from anywhere on the page.
struct NoteEditorTarget: Identifiable, Hashable {
    let verseKey: String
    let referenceLabel: String
    let samoanPreview: String
    var id: String { verseKey }
}

// MARK: - One chapter's page

struct ChapterPageView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(AppSettings.self) private var settings
    @Environment(Navigator.self) private var nav
    let ref: ChapterRef
    @Binding var noteEditorTarget: NoteEditorTarget?

    /// The verse currently flashing to draw the eye after a jump-to-verse. Set
    /// when a matching `Navigator.verseTarget` is consumed, then cleared after a
    /// beat so the highlight fades on its own.
    @State private var flashVerse: Int?

    var body: some View {
        if let book = library.book(id: ref.bookId),
           let chapter = book.chapters.first(where: { $0.num == ref.chapterNum }) {
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .center, spacing: 0) {
                        BookHeader(book: book, chapter: chapter)
                        ColophonView(book: book, chapter: chapter, mode: settings.readerMode)
                        ChapterHeadingView(book: book, chapter: chapter, mode: settings.readerMode)
                        VStack(spacing: 0) {
                            ForEach(chapter.verses) { verse in
                                VerseRow(
                                    book: book,
                                    chapter: chapter,
                                    verse: verse,
                                    mode: settings.readerMode,
                                    flashing: flashVerse == verse.num,
                                    noteEditorTarget: $noteEditorTarget
                                )
                                .id("verse-\(verse.num)")
                            }
                        }
                    }
                    .frame(maxWidth: 900, alignment: .center)
                    .padding(.horizontal, 20)
                    .padding(.top, 16)
                    .padding(.bottom, 24)
                    .frame(maxWidth: .infinity, alignment: .center)
                }
                .background(Theme.pageBg)
                // Handle a jump-to-verse both when this page first appears (the
                // search-result case: target is set before the page is built)
                // and when the target changes while the page is already showing.
                .onAppear { consumeVerseTarget(proxy) }
                .onChange(of: nav.verseTarget) { consumeVerseTarget(proxy) }
            }
        } else {
            ContentUnavailableView("E lē maua le Mataupu", systemImage: "questionmark.folder")
        }
    }

    /// If a pending verse target names this chapter, scroll to it and flash it,
    /// then clear the request so it fires once.
    private func consumeVerseTarget(_ proxy: ScrollViewProxy) {
        guard let target = nav.verseTarget, target.ref == ref else { return }
        nav.verseTarget = nil
        Task { @MainActor in
            // Let the horizontal pager settle on this chapter before scrolling.
            try? await Task.sleep(nanoseconds: 350_000_000)
            withAnimation(.easeInOut(duration: 0.35)) {
                proxy.scrollTo("verse-\(target.verse)", anchor: .top)
            }
            withAnimation(.easeInOut(duration: 0.25)) { flashVerse = target.verse }
            try? await Task.sleep(nanoseconds: 1_600_000_000)
            withAnimation(.easeOut(duration: 0.6)) { flashVerse = nil }
        }
    }
}

// MARK: - Chapter header

private struct BookHeader: View {
    @Environment(\.scriptureFontScale) private var scale
    let book: Book
    let chapter: Chapter

    var body: some View {
        VStack(spacing: 6) {
            Text(book.nameSm)
                .font(SerifFont.tnr(size: 34 * scale, weight: .bold))
                .foregroundStyle(Theme.headerBg)
                .tracking(1.2)
                .multilineTextAlignment(.center)
            Text(book.nameEn)
                .font(SerifFont.tnr(size: 17 * scale))
                .foregroundStyle(Theme.inkLight)
                .tracking(1.0)
                .padding(.bottom, 4)
            Text("\u{2767} \u{2767} \u{2767}")
                .font(SerifFont.tnr(size: 17 * scale))
                .foregroundStyle(Theme.accent)
                .tracking(8)
                .padding(.bottom, 4)
            Text("Mataupu \(chapter.num)")
                .font(SerifFont.tnr(size: 24 * scale, weight: .bold))
                .foregroundStyle(Theme.ink)
                .tracking(1.4)
            Text("Chapter \(chapter.num)")
                .font(SerifFont.tnr(size: 14 * scale))
                .foregroundStyle(Theme.accent)
                .tracking(1.4)
                .textCase(.uppercase)
                .padding(.top, 2)
            Rectangle()
                .fill(Theme.rule)
                .frame(height: 2)
                .padding(.top, 16)
        }
        .padding(.top, 16)
        .padding(.bottom, 16)
        .frame(maxWidth: .infinity)
    }
}

// MARK: - Record-keeper colophon (mode-aware)

/// The sub-record preface (colophon) shown above the chapter summary on the
/// chapter where it appears — e.g. "The commandments of Alma to his son
/// Helaman. Comprising chapters 36 and 37." Centered and italic to read as an
/// editorial preface, distinct from the chapter summary below it.
private struct ColophonView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(\.scriptureFontScale) private var scale
    let book: Book
    let chapter: Chapter
    let mode: ReaderMode

    var body: some View {
        if let colophon = library.colophon(bookId: book.id, chapter: chapter.num) {
            content(colophon)
                .padding(.horizontal, 14)
                .padding(.top, 6)
                .padding(.bottom, 10)
                .frame(maxWidth: .infinity)
                .overlay(alignment: .bottom) {
                    Rectangle().fill(Theme.rule.opacity(0.5)).frame(height: 1)
                        .padding(.horizontal, 48)
                }
                .padding(.bottom, 8)
        }
    }

    @ViewBuilder
    private func content(_ colophon: HeadingSection) -> some View {
        switch mode {
        case .interlinear:
            if let words = colophon.words, !words.isEmpty {
                FlowLayout(horizontalSpacing: 6, verticalSpacing: 4) {
                    ForEach(groupIdiomSpans(words)) { item in
                        switch item {
                        case .single(_, let pair):
                            HeadingCell(sm: pair.sm, en: pair.en)
                        case .span(_, let samoanWords, let gloss):
                            HeadingCell(sm: samoanWords.joined(separator: " "), en: gloss)
                        }
                    }
                }
                .frame(maxWidth: .infinity, alignment: .center)
            } else {
                prose(colophon.sm)
            }
        case .samoan:
            prose(colophon.sm)
        case .dual:
            VStack(spacing: 4) {
                prose(colophon.sm)
                Text(colophon.en)
                    .font(SerifFont.tnr(size: 13 * scale, italic: true))
                    .foregroundStyle(Theme.inkLight)
                    .multilineTextAlignment(.center)
            }
        }
    }

    private func prose(_ text: String) -> some View {
        Text(text)
            .font(SerifFont.tnr(size: 14 * scale, italic: true))
            .foregroundStyle(Theme.inkLight)
            .multilineTextAlignment(.center)
            .frame(maxWidth: .infinity)
    }
}

// MARK: - Chapter heading / summary (mode-aware)

/// The editorial chapter summary shown above verse 1. Follows the active
/// reader mode: interlinear (Samoan stacked over gloss), Samoan-only, or dual
/// Samoan | English. Renders nothing when no heading has been curated yet.
private struct ChapterHeadingView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(\.scriptureFontScale) private var scale
    let book: Book
    let chapter: Chapter
    let mode: ReaderMode

    var body: some View {
        if let heading = library.heading(bookId: book.id, chapter: chapter.num) {
            content(heading)
                .padding(.horizontal, 14)
                .padding(.vertical, 12)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Theme.rowAlt)
                .overlay(alignment: .bottom) {
                    Rectangle().fill(Theme.rule).frame(height: 1)
                }
                .padding(.bottom, 10)
        }
    }

    @ViewBuilder
    private func content(_ heading: HeadingSection) -> some View {
        switch mode {
        case .interlinear:
            if let words = heading.words, !words.isEmpty {
                FlowLayout(horizontalSpacing: 6, verticalSpacing: 4) {
                    ForEach(groupIdiomSpans(words)) { item in
                        switch item {
                        case .single(_, let pair):
                            HeadingCell(sm: pair.sm, en: pair.en)
                        case .span(_, let samoanWords, let gloss):
                            HeadingCell(sm: samoanWords.joined(separator: " "), en: gloss)
                        }
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            } else {
                samoanProse(heading.sm)
            }
        case .samoan:
            samoanProse(heading.sm)
        case .dual:
            HStack(alignment: .top, spacing: 14) {
                samoanProse(heading.sm)
                Rectangle().fill(Theme.rule).frame(width: 1)
                Text(heading.en)
                    .font(SerifFont.tnr(size: 15 * scale, italic: true))
                    .foregroundStyle(Theme.hwInk)
                    .lineSpacing(3)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
    }

    private func samoanProse(_ text: String) -> some View {
        Text(text)
            .font(SerifFont.tnr(size: 16 * scale, italic: true))
            .foregroundStyle(Theme.hwInk)
            .lineSpacing(3)
            .frame(maxWidth: .infinity, alignment: .leading)
    }
}

/// A static (non-interactive) interlinear cell for chapter headings: the Samoan
/// surface form stacked over its English gloss. Headings are editorial, so
/// unlike verse words these are not selectable/highlightable.
private struct HeadingCell: View {
    @Environment(\.scriptureFontScale) private var scale
    let sm: String
    let en: String

    var body: some View {
        VStack(alignment: .center, spacing: 1) {
            Text(sm)
                .font(SerifFont.tnr(size: 17 * scale, weight: .medium))
                .foregroundStyle(Theme.hwInk)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
            if !en.isEmpty {
                Text(en)
                    .font(SerifFont.tnr(size: 10 * scale, italic: true))
                    .foregroundStyle(Theme.glossInk)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}

// MARK: - Verse row (mode-aware)

private struct VerseRow: View {
    @Environment(\.scriptureFontScale) private var scale
    @Environment(\.scriptureShowDiacritics) private var showDiacritics
    @Environment(ScriptureLibrary.self) private var library
    @Environment(HighlightStore.self) private var highlights
    @Environment(WordSelectionModel.self) private var selection
    let book: Book
    let chapter: Chapter
    let verse: Verse
    let mode: ReaderMode
    /// Briefly tints the row to draw the eye after a jump-to-verse.
    var flashing: Bool = false
    @Binding var noteEditorTarget: NoteEditorTarget?

    private var verseKey: String {
        "\(book.id)|\(chapter.num)|\(verse.num)"
    }

    /// A highlight saved against the whole verse (as opposed to a single word).
    private var verseHighlight: HighlightColor? { highlights.color(for: verseKey) }
    private var verseSelected: Bool { selection.isVerseSelected(verseKey) }

    /// Prose Samoan for the Samoan-only and dual modes. Marked per token using
    /// the same `wordKey` the interlinear mode uses, so a context-dependent
    /// exception resolves identically in all three modes.
    ///
    /// Share and selection deliberately keep `verse.samoanText` — what leaves
    /// the app stays in the published orthography.
    private var displaySamoanText: String {
        guard showDiacritics else { return verse.samoanText }
        return verse.words.enumerated()
            .map { library.markedSamoan($1.sm, wordKey: "\(verseKey)|\($0)") }
            .joined(separator: " ")
    }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            verseNumberColumn
            verseContent
        }
        .padding(.vertical, 10)
        .padding(.horizontal, 4)
        .background {
            // The flash tint sits over the row color but behind the text, so a
            // jumped-to verse briefly glows without hurting legibility.
            Theme.rowAlt
            if flashing {
                Theme.accent.opacity(0.22)
            }
        }
    }

    /// Selecting a whole verse. Tapping the number toggles it in every mode.
    private func toggleVerse() {
        selection.toggleVerse(verseKey: verseKey, text: verse.samoanText)
    }

    @ViewBuilder
    private var verseNumberColumn: some View {
        Text("\(verse.num)")
            .font(SerifFont.tnr(size: 17 * scale, weight: .bold))
            .foregroundStyle(Theme.verseNum)
            .frame(width: 32 * scale, alignment: .center)
            .padding(.top, 8)
            .contentShape(Rectangle())
            .onTapGesture(perform: toggleVerse)
            .accessibilityAddTraits(.isButton)
            .accessibilityLabel("Faailoga le fuaiupu atoa")
    }

    @ViewBuilder
    private var verseContent: some View {
        switch mode {
        case .interlinear:
            interlinearContent
        case .samoan:
            samoanOnlyContent
        case .dual:
            dualContent
        }
    }

    private var interlinearContent: some View {
        FlowLayout(horizontalSpacing: 6, verticalSpacing: 6) {
            ForEach(groupIdiomSpans(verse.words)) { item in
                switch item {
                case .single(let idx, let pair):
                    WordUnitView(
                        pair: pair,
                        wordKey: "\(verseKey)|\(idx)",
                        verseKey: verseKey
                    )
                case .span(let idx, let samoanWords, let englishGloss):
                    IdiomSpanView(
                        samoanWords: samoanWords,
                        englishGloss: englishGloss,
                        wordKey: "\(verseKey)|\(idx)",
                        verseKey: verseKey,
                        startIndex: idx
                    )
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .verseHighlight(color: verseHighlight, selected: verseSelected)
    }

    private var samoanOnlyContent: some View {
        Text(displaySamoanText)
            .font(SerifFont.tnr(size: 19 * scale))
            .foregroundStyle(Theme.hwInk)
            .lineSpacing(4)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.top, 6)
            .verseHighlight(color: verseHighlight, selected: verseSelected)
            .contentShape(Rectangle())
            .onTapGesture(perform: toggleVerse)
    }

    private var dualContent: some View {
        HStack(alignment: .top, spacing: 14) {
            Text(displaySamoanText)
                .font(SerifFont.tnr(size: 17 * scale))
                .foregroundStyle(Theme.hwInk)
                .lineSpacing(3)
                .frame(maxWidth: .infinity, alignment: .leading)
                .verseHighlight(color: verseHighlight, selected: verseSelected)
                .contentShape(Rectangle())
                .onTapGesture(perform: toggleVerse)
            Rectangle()
                .fill(Theme.rule)
                .frame(width: 1)
            Text(library.englishText(for: ScriptureKey(
                bookEn: book.nameEn,
                chapter: chapter.num,
                verse: verse.num
            )) ?? "—")
                .font(SerifFont.tnr(size: 17 * scale))
                .foregroundStyle(Theme.hwInk)
                .lineSpacing(3)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.top, 6)
    }
}

/// Background tint + selection ring for a whole-verse highlight, applied to the
/// Samoan portion of a verse in any reader mode.
private struct VerseHighlightBackground: ViewModifier {
    let color: HighlightColor?
    let selected: Bool

    func body(content: Content) -> some View {
        content
            .padding(.horizontal, 6)
            .padding(.vertical, 4)
            .background {
                if let color {
                    RoundedRectangle(cornerRadius: 6, style: .continuous)
                        .fill(color.tint)
                }
            }
            .overlay {
                RoundedRectangle(cornerRadius: 6, style: .continuous)
                    .strokeBorder(Theme.accent, lineWidth: selected ? 2 : 0)
            }
    }
}

private extension View {
    func verseHighlight(color: HighlightColor?, selected: Bool) -> some View {
        modifier(VerseHighlightBackground(color: color, selected: selected))
    }
}

// MARK: - Word selection action bar

/// The contextual toolbar that slides up while one or more Samoan words are
/// selected. Offers the five highlight colors, an eraser, a note button, and
/// copy — each applied to the current selection. Modeled on the Gospel Library
/// / Standard Works word-selection toolbar.
private struct WordActionBar: View {
    @Environment(HighlightStore.self) private var highlights
    @Environment(WordSelectionModel.self) private var selection
    @Environment(ScriptureLibrary.self) private var library
    @Binding var noteEditorTarget: NoteEditorTarget?

    var body: some View {
        HStack(spacing: 12) {
            ForEach(HighlightColor.allCases, id: \.self) { c in
                Button {
                    applyColor(c)
                } label: {
                    Circle()
                        .fill(c.tint)
                        .frame(width: 28, height: 28)
                        .overlay(Circle().strokeBorder(.white.opacity(0.5), lineWidth: 1))
                }
                .buttonStyle(.plain)
                .accessibilityLabel(c.label)
            }

            Button {
                applyColor(nil)
            } label: {
                Image(systemName: "eraser")
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundStyle(Theme.headerText)
                    .frame(width: 28, height: 28)
                    .overlay(Circle().strokeBorder(.white.opacity(0.4), lineWidth: 1))
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Aveese le Faailoga")

            Divider().frame(height: 24).overlay(.white.opacity(0.3))

            Button(action: openNote) {
                Image(systemName: "square.and.pencil")
                    .font(.system(size: 17, weight: .semibold))
                    .foregroundStyle(Theme.headerText)
            }
            .accessibilityLabel("Manatu")

            Button(action: copySelection) {
                Image(systemName: "doc.on.doc")
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundStyle(Theme.headerText)
            }
            .accessibilityLabel("Kopi")

            ShareLink(item: shareText) {
                Image(systemName: "square.and.arrow.up")
                    .font(.system(size: 17, weight: .semibold))
                    .foregroundStyle(Theme.headerText)
            }
            .accessibilityLabel("Fa\u{2019}asoa")

            Spacer(minLength: 0)

            Button {
                selection.clear()
            } label: {
                Image(systemName: "xmark")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundStyle(Theme.headerText)
            }
            .accessibilityLabel("Faaleaoga")
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 10)
        .frame(maxWidth: .infinity)
        .background(Theme.headerBg)
    }

    private func applyColor(_ color: HighlightColor?) {
        if let verseKey = selection.wholeVerseKey {
            highlights.set(color, for: verseKey)
        } else {
            for key in selection.selected {
                highlights.set(color, for: key)
            }
        }
        selection.clear()
    }

    private func copySelection() {
        let text = selection.isWholeVerse ? selection.wholeVerseText : selection.joinedText
        copyToPasteboard(text)
        selection.clear()
    }

    private func openNote() {
        if let verseKey = selection.wholeVerseKey {
            noteEditorTarget = NoteEditorTarget(
                verseKey: verseKey,
                referenceLabel: referenceLabel(for: verseKey),
                samoanPreview: selection.wholeVerseText
            )
            selection.clear()
            return
        }
        guard let anchor = selection.anchorKey, let vk = selection.verseKey else { return }
        noteEditorTarget = NoteEditorTarget(
            verseKey: anchor,
            referenceLabel: referenceLabel(for: vk),
            samoanPreview: selection.joinedText
        )
        selection.clear()
    }

    private func referenceLabel(for verseKey: String) -> String {
        let parts = verseKey.split(separator: "|")
        guard parts.count == 3, let book = library.book(id: String(parts[0])) else { return "" }
        return "\(book.nameSm) \(parts[1]):\(parts[2])"
    }

    /// The text placed on the share sheet: the reference and Samoan text, plus
    /// the official English when a whole verse is selected.
    private var shareText: String {
        if let verseKey = selection.wholeVerseKey {
            var parts = [referenceLabel(for: verseKey), selection.wholeVerseText]
            if let en = englishText(for: verseKey), !en.isEmpty {
                parts.append(en)
            }
            return parts.joined(separator: "\n\n")
        }
        if let verseKey = selection.verseKey {
            return "\(referenceLabel(for: verseKey))\n\n\(selection.joinedText)"
        }
        return selection.joinedText
    }

    private func englishText(for verseKey: String) -> String? {
        let parts = verseKey.split(separator: "|")
        guard parts.count == 3,
              let book = library.book(id: String(parts[0])),
              let chapter = Int(parts[1]),
              let verse = Int(parts[2]) else { return nil }
        return library.englishText(for: ScriptureKey(
            bookEn: book.nameEn, chapter: chapter, verse: verse
        ))
    }
}

/// Cross-platform clipboard write.
private func copyToPasteboard(_ text: String) {
    #if canImport(UIKit)
    UIPasteboard.general.string = text
    #elseif canImport(AppKit)
    NSPasteboard.general.clearContents()
    NSPasteboard.general.setString(text, forType: .string)
    #endif
}

// MARK: - Reader control bar (footer)

struct ReaderControlBar: View {
    @Environment(AppSettings.self) private var settings

    var body: some View {
        @Bindable var settings = settings
        HStack(spacing: 10) {
            ForEach(ReaderMode.allCases, id: \.self) { mode in
                Button {
                    settings.readerMode = mode
                } label: {
                    Text(mode.label)
                        .font(SerifFont.tnr(size: 14, weight: .semibold))
                        .padding(.horizontal, 14)
                        .padding(.vertical, 7)
                        .foregroundStyle(
                            settings.readerMode == mode ? Theme.headerBg : Theme.accent
                        )
                        .background(
                            RoundedRectangle(cornerRadius: 4, style: .continuous)
                                .fill(settings.readerMode == mode ? Theme.accent : Color.clear)
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 4, style: .continuous)
                                .strokeBorder(
                                    settings.readerMode == mode ? Theme.accent : Theme.buttonBorder,
                                    lineWidth: 1
                                )
                        )
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 16)
        .padding(.top, 8)
        .padding(.bottom, 10)
        .frame(maxWidth: .infinity)
        .background(Theme.headerBg.ignoresSafeArea(edges: .bottom))
    }
}
