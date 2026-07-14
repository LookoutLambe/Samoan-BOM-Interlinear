import SwiftUI

/// The reading view. Hosts a paged `TabView` so the user can flip between
/// chapters like in the Gospel Library app. Rather than materializing every
/// chapter at once (240+ heavy interlinear pages, which swamps the pager and
/// kills swiping), it keeps a lightweight sliding window of just the previous,
/// current, and next chapters, re-centered whenever `currentRef` changes. A
/// fixed bottom `ReaderControlBar` switches display modes (Interlinear / Samoa
/// / Tutusa).
struct ChapterView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(AppSettings.self) private var settings
    @State private var currentRef: ChapterRef
    @State private var showFontSize = false
    @State private var noteEditorTarget: NoteEditorTarget?

    init(ref: ChapterRef) {
        self._currentRef = State(initialValue: ref)
    }

    /// The 3-page sliding window `[previous, current, next]`. Ends are trimmed
    /// at the first/last chapter of the whole Book of Mormon. `currentRef` is
    /// both the window's center and the `TabView` selection, so swiping to an
    /// adjacent page updates the selection, which re-centers the window here.
    private var windowRefs: [ChapterRef] {
        var refs: [ChapterRef] = []
        if let prev = library.previousChapter(before: currentRef) { refs.append(prev) }
        refs.append(currentRef)
        if let next = library.nextChapter(after: currentRef) { refs.append(next) }
        return refs
    }

    var body: some View {
        TabView(selection: $currentRef) {
            ForEach(windowRefs, id: \.self) { ref in
                ChapterPageView(ref: ref, noteEditorTarget: $noteEditorTarget)
                    .tag(ref)
            }
        }
        #if os(iOS)
        .tabViewStyle(.page(indexDisplayMode: .never))
        #endif
        .background(Theme.pageBg.ignoresSafeArea())
        .environment(\.scriptureFontScale, settings.fontScale)
        .navigationTitle(navTitle)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarBackground(Theme.headerBg, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
        #endif
        .toolbar {
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
        .libraryToolbar()
        .safeAreaInset(edge: .bottom, spacing: 0) {
            ReaderControlBar()
        }
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
    }

    private var navTitle: String {
        guard let book = library.book(id: currentRef.bookId) else { return "" }
        return "\(book.nameEn) \(currentRef.chapterNum)"
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
    let ref: ChapterRef
    @Binding var noteEditorTarget: NoteEditorTarget?

    var body: some View {
        if let book = library.book(id: ref.bookId),
           let chapter = book.chapters.first(where: { $0.num == ref.chapterNum }) {
            ScrollView {
                VStack(alignment: .center, spacing: 0) {
                    BookHeader(book: book, chapter: chapter)
                    VStack(spacing: 0) {
                        ForEach(chapter.verses) { verse in
                            VerseRow(
                                book: book,
                                chapter: chapter,
                                verse: verse,
                                mode: settings.readerMode,
                                noteEditorTarget: $noteEditorTarget
                            )
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
        } else {
            ContentUnavailableView("E lē maua le Mataupu", systemImage: "questionmark.folder")
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

// MARK: - Verse row (mode-aware)

private struct VerseRow: View {
    @Environment(\.scriptureFontScale) private var scale
    @Environment(ScriptureLibrary.self) private var library
    @Environment(HighlightStore.self) private var highlights
    @Environment(NoteStore.self) private var notes
    let book: Book
    let chapter: Chapter
    let verse: Verse
    let mode: ReaderMode
    @Binding var noteEditorTarget: NoteEditorTarget?

    private var verseKey: String {
        "\(book.id)|\(chapter.num)|\(verse.num)"
    }
    private var highlightColor: HighlightColor? {
        highlights.color(for: verseKey)
    }
    private var hasNote: Bool {
        notes.hasNote(for: verseKey)
    }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            verseNumberColumn
            verseContent
        }
        .padding(.vertical, 10)
        .padding(.horizontal, 4)
        .background(highlightColor?.tint ?? Theme.rowAlt)
        .contextMenu { verseMenu }
    }

    @ViewBuilder
    private var verseNumberColumn: some View {
        VStack(spacing: 4) {
            Text("\(verse.num)")
                .font(SerifFont.tnr(size: 17 * scale, weight: .bold))
                .foregroundStyle(Theme.verseNum)
            if hasNote {
                Image(systemName: "note.text")
                    .font(.system(size: 11 * scale, weight: .medium))
                    .foregroundStyle(Theme.accent)
            }
        }
        .frame(width: 32 * scale, alignment: .center)
        .padding(.top, 8)
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
                case .single(_, let pair):
                    WordUnitView(pair: pair)
                case .span(_, let samoanWords, let englishGloss):
                    IdiomSpanView(samoanWords: samoanWords, englishGloss: englishGloss)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var samoanOnlyContent: some View {
        Text(verse.samoanText)
            .font(SerifFont.tnr(size: 19 * scale))
            .foregroundStyle(Theme.hwInk)
            .lineSpacing(4)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.top, 6)
    }

    private var dualContent: some View {
        HStack(alignment: .top, spacing: 14) {
            Text(verse.samoanText)
                .font(SerifFont.tnr(size: 17 * scale))
                .foregroundStyle(Theme.hwInk)
                .lineSpacing(3)
                .frame(maxWidth: .infinity, alignment: .leading)
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

    @ViewBuilder
    private var verseMenu: some View {
        Section("Faailoga") {
            ForEach(HighlightColor.allCases, id: \.self) { c in
                Button {
                    highlights.set(highlightColor == c ? nil : c, for: verseKey)
                } label: {
                    Label(c.label, systemImage: highlightColor == c ? "checkmark.circle.fill" : "circle.fill")
                        .foregroundStyle(c.tint)
                }
            }
            if highlightColor != nil {
                Button(role: .destructive) {
                    highlights.set(nil, for: verseKey)
                } label: {
                    Label("Aveese le Faailoga", systemImage: "xmark.circle")
                }
            }
        }
        Section("Manatu") {
            Button {
                noteEditorTarget = NoteEditorTarget(
                    verseKey: verseKey,
                    referenceLabel: "\(book.nameSm) \(chapter.num):\(verse.num)",
                    samoanPreview: verse.samoanText
                )
            } label: {
                Label(hasNote ? "Faasa\u{2019}o le Manatu" : "Faaopoopo se Manatu", systemImage: "square.and.pencil")
            }
        }
    }
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
