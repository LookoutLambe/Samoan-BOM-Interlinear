import SwiftUI
#if canImport(UIKit)
import UIKit
#elseif canImport(AppKit)
import AppKit
#endif

/// The reading view. Lets the user flip between chapters like in the Gospel
/// Library app. Instead of a paged `TabView` (which materializes every child
/// eagerly — 240+ heavy interlinear pages — and choked swiping), it uses a
/// horizontal paging `ScrollView` over a `LazyHStack`, so only the visible and
/// immediately-adjacent chapters are ever built, and nothing is rebuilt during
/// the swipe. `scrolledRef` tracks the settled page and drives the title. A
/// fixed bottom `ReaderControlBar` switches display modes (Interlinear / Samoa
/// / Tutusa).
struct ChapterView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(AppSettings.self) private var settings
    @State private var scrolledRef: ChapterRef?
    @State private var showFontSize = false
    @State private var noteEditorTarget: NoteEditorTarget?
    @State private var selection = WordSelectionModel()

    private let initialRef: ChapterRef

    init(ref: ChapterRef) {
        self.initialRef = ref
        self._scrolledRef = State(initialValue: ref)
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
                ScrollView(.horizontal) {
                    LazyHStack(spacing: 0) {
                        ForEach(library.allChapterRefs, id: \.self) { ref in
                            ChapterPageView(ref: ref, noteEditorTarget: $noteEditorTarget)
                                .frame(width: geo.size.width, height: geo.size.height)
                        }
                    }
                    .scrollTargetLayout()
                }
                .scrollTargetBehavior(.paging)
                .scrollPosition(id: $scrolledRef)
                .scrollIndicators(.hidden)
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

    private var navTitle: String {
        let ref = scrolledRef ?? initialRef
        guard let book = library.book(id: ref.bookId) else { return "" }
        return "\(book.nameEn) \(ref.chapterNum)"
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
    @Environment(WordSelectionModel.self) private var selection
    let book: Book
    let chapter: Chapter
    let verse: Verse
    let mode: ReaderMode
    @Binding var noteEditorTarget: NoteEditorTarget?

    private var verseKey: String {
        "\(book.id)|\(chapter.num)|\(verse.num)"
    }

    /// A highlight saved against the whole verse (as opposed to a single word).
    private var verseHighlight: HighlightColor? { highlights.color(for: verseKey) }
    private var verseSelected: Bool { selection.isVerseSelected(verseKey) }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            verseNumberColumn
            verseContent
        }
        .padding(.vertical, 10)
        .padding(.horizontal, 4)
        .background(Theme.rowAlt)
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
                        verseKey: verseKey
                    )
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .verseHighlight(color: verseHighlight, selected: verseSelected)
    }

    private var samoanOnlyContent: some View {
        Text(verse.samoanText)
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
            Text(verse.samoanText)
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
