import SwiftUI

struct BookListView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(Navigator.self) private var nav

    var body: some View {
        ScrollView {
            if let error = library.loadError {
                ContentUnavailableView(
                    "E lē mafai ona uta",
                    systemImage: "exclamationmark.triangle",
                    description: Text(error)
                )
                .padding()
            } else {
                VStack(spacing: 0) {
                    // The cover itself is the way in — tap it to open the book's
                    // table of contents (front matter + all chapters).
                    Button { nav.libraryOpen = true } label: {
                        BookCover()
                    }
                    .buttonStyle(.plain)
                    .padding(.horizontal, 48)
                    .padding(.top, 24)
                    .accessibilityLabel("Tatala le tusi")

                    ContinueReadingButton()
                        .padding(.top, 24)

                    DisclaimerNotice()
                        .padding(.top, 36)
                }
                .frame(maxWidth: 560)
                .frame(maxWidth: .infinity, alignment: .center)
            }
        }
        .background(Theme.pageBg)
        .navigationTitle("O le Tusi a Mamona")
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarBackground(Theme.headerBg, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
        #endif
        .libraryToolbar()
    }
}

// MARK: - Continue-reading button

/// Jumps straight to the furthest chapter the reader has reached (or the very
/// first chapter if nothing has been read yet).
private struct ContinueReadingButton: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(AppSettings.self) private var settings
    @Environment(Navigator.self) private var nav

    /// The chapter to resume at: the stored furthest chapter, else chapter 1.
    private var target: ChapterRef? {
        if let bookId = settings.furthestBookId, settings.furthestChapter > 0 {
            return ChapterRef(bookId: bookId, chapterNum: settings.furthestChapter)
        }
        return library.allChapterRefs.first
    }

    private var chapterLabel: String {
        guard let ref = target, let book = library.book(id: ref.bookId) else { return "" }
        return "\(book.nameEn) \(ref.chapterNum)"
    }

    var body: some View {
        if let ref = target {
            Button {
                nav.openChapter(ref)
            } label: {
                VStack(spacing: 3) {
                    HStack(spacing: 8) {
                        Image(systemName: "book")
                            .font(.footnote.weight(.semibold))
                        Text("Fa\u{2019}aauau le Faitau \u{00B7} Continue reading from")
                            .font(SerifFont.tnr(size: 12, weight: .semibold))
                            .textCase(.uppercase)
                            .tracking(0.5)
                    }
                    .foregroundStyle(Theme.accent)
                    Text(chapterLabel)
                        .font(SerifFont.tnr(size: 18, weight: .bold))
                        .foregroundStyle(Theme.headerText)
                }
                .padding(.horizontal, 24)
                .padding(.vertical, 12)
                .background(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(Theme.headerBg)
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .strokeBorder(Theme.accent.opacity(0.6), lineWidth: 1)
                )
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Continue reading from \(chapterLabel)")
        }
    }
}

// MARK: - Required disclaimer (Intellectual Reserve, Inc. license)

/// Notice required by the Standard Scripture License Agreement, shown at the top
/// of the app's landing page in the app's three registers: the verbatim English
/// (required wording), the official Samoan, and a word-by-word interlinear.
private struct DisclaimerNotice: View {
    private let english = """
    This product offered by Chris Lambe is neither made, provided, approved, nor \
    endorsed by, Intellectual Reserve, Inc. or The Church of Jesus Christ of \
    Latter-day Saints. Any content or opinions expressed, implied, or included in \
    or with the product offered by Chris Lambe are solely those of Chris Lambe and \
    not those of Intellectual Reserve, Inc. or The Church of Jesus Christ of \
    Latter-day Saints.
    """

    private let samoan = """
    O le oloa lenei o loo ofoina atu e Chris Lambe, e le\u{02bb}i faia, e le\u{02bb}i \
    saunia, e le\u{02bb}i fa\u{02bb}amaonia, pe lagolagoina fo\u{02bb}i e le \
    Intellectual Reserve, Inc. po o Le Ekalesia a Iesu Keriso o le Au Paia o Aso \
    e Gata Ai. O so o se mataupu po o ni manatu o loo fa\u{02bb}aalia, o loo \
    fa\u{02bb}ailoa mai, po o loo aofia i totonu po o fa\u{02bb}atasi ma le oloa o \
    loo ofoina atu e Chris Lambe, e na\u{02bb}o manatu tonu lava ia o Chris Lambe, \
    ae l\u{0113} o ni manatu o le Intellectual Reserve, Inc. po o Le Ekalesia a Iesu \
    Keriso o le Au Paia o Aso e Gata Ai.
    """

    // Word-by-word interlinear (Samoan surface phrase, concise English gloss).
    private let gloss: [(String, String)] = [
        ("O le oloa lenei", "This product"),
        ("o loo ofoina atu", "offered"),
        ("e Chris Lambe,", "by Chris Lambe,"),
        ("e le\u{02bb}i faia,", "is not made,"),
        ("e le\u{02bb}i saunia,", "not provided,"),
        ("e le\u{02bb}i fa\u{02bb}amaonia,", "not approved,"),
        ("pe lagolagoina fo\u{02bb}i", "nor endorsed"),
        ("e le", "by"),
        ("Intellectual Reserve, Inc.", "Intellectual Reserve, Inc."),
        ("po o", "or"),
        ("Le Ekalesia", "The Church"),
        ("a Iesu Keriso", "of Jesus Christ"),
        ("o le Au Paia", "of the Saints"),
        ("o Aso e Gata Ai.", "of the Last Days."),
        ("O so o se mataupu", "Any content"),
        ("po o ni manatu", "or opinions"),
        ("o loo fa\u{02bb}aalia,", "expressed,"),
        ("o loo fa\u{02bb}ailoa mai,", "implied,"),
        ("po o loo aofia", "or included"),
        ("i totonu", "in"),
        ("po o fa\u{02bb}atasi ma", "or with"),
        ("le oloa", "the product"),
        ("o loo ofoina atu", "offered"),
        ("e Chris Lambe,", "by Chris Lambe,"),
        ("e na\u{02bb}o", "are solely"),
        ("manatu tonu lava ia", "those very opinions"),
        ("o Chris Lambe,", "of Chris Lambe,"),
        ("ae l\u{0113}", "and not"),
        ("o ni manatu", "the opinions"),
        ("o le", "of"),
        ("Intellectual Reserve, Inc.", "Intellectual Reserve, Inc."),
        ("po o", "or"),
        ("Le Ekalesia", "The Church"),
        ("a Iesu Keriso", "of Jesus Christ"),
        ("o le Au Paia", "of the Saints"),
        ("o Aso e Gata Ai.", "of the Last Days."),
    ]

    var body: some View {
        VStack(spacing: 12) {
            Text(english)
                .font(SerifFont.tnr(size: 10.5))
                .foregroundStyle(Theme.inkLight)
                .multilineTextAlignment(.center)
                .lineSpacing(2)
                .fixedSize(horizontal: false, vertical: true)

            hairline

            Text(samoan)
                .font(SerifFont.tnr(size: 10.5, italic: true))
                .foregroundStyle(Theme.inkLight)
                .multilineTextAlignment(.center)
                .lineSpacing(2)
                .fixedSize(horizontal: false, vertical: true)

            hairline

            FlowLayout(horizontalSpacing: 8, verticalSpacing: 6) {
                ForEach(gloss.indices, id: \.self) { i in
                    GlossCell(sm: gloss[i].0, en: gloss[i].1)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal, 18)
        .padding(.vertical, 14)
        .frame(maxWidth: .infinity)
        .background(Theme.rowAlt)
        .overlay(alignment: .bottom) {
            Rectangle().fill(Theme.rule).frame(height: 1)
        }
    }

    private var hairline: some View {
        Rectangle()
            .fill(Theme.rule.opacity(0.6))
            .frame(height: 1)
            .padding(.horizontal, 40)
    }
}

/// A static (non-interactive) interlinear cell: Samoan phrase over its gloss.
private struct GlossCell: View {
    let sm: String
    let en: String

    var body: some View {
        VStack(alignment: .center, spacing: 1) {
            Text(sm)
                .font(SerifFont.tnr(size: 12, weight: .medium))
                .foregroundStyle(Theme.hwInk)
            Text(en)
                .font(SerifFont.tnr(size: 8, italic: true))
                .foregroundStyle(Theme.glossInk)
        }
        .fixedSize()
    }
}

// MARK: - Interlinear title

/// The book title rendered interlinear: each Samoan phrase stacked above its
/// English gloss, like the reader itself. Units are stacked vertically and
/// centered so a multi-word title reads as a clean title block rather than
/// drifting across the page.
private struct InterlinearTitle: View {
    struct Cell: Identifiable {
        let id = UUID()
        let sm: String
        let en: String
    }

    let cells: [Cell]
    var smSize: CGFloat
    var enSize: CGFloat
    var smColor: Color
    var enColor: Color
    var smWeight: Font.Weight = .bold
    var tracking: CGFloat = 0
    var spacing: CGFloat = 10   // gap between interlinear units

    var body: some View {
        VStack(spacing: spacing) {
            ForEach(cells) { cell in
                VStack(spacing: 1) {
                    Text(cell.sm)
                        .font(SerifFont.tnr(size: smSize, weight: smWeight))
                        .foregroundStyle(smColor)
                        .tracking(tracking)
                    Text(cell.en)
                        .font(SerifFont.tnr(size: enSize, italic: true))
                        .foregroundStyle(enColor)
                }
            }
        }
        .multilineTextAlignment(.center)
    }
}

/// The interlinear breakdown of the title, curated per GLOSSING_RULES.md.
private enum TitleGloss {
    static let cover: [InterlinearTitle.Cell] = [
        .init(sm: "O LE TUSI", en: "The Book"),
        .init(sm: "A MAMONA", en: "of Mormon"),
    ]
    static let subtitle: [InterlinearTitle.Cell] = [
        .init(sm: "O se tasi molimau", en: "Another testimony"),
        .init(sm: "a Iesu Keriso", en: "of Jesus Christ"),
    ]
}

// MARK: - Single book cover (navy gradient plate)

/// The one cover on the landing page — the Book of Mormon as a single volume.
private struct BookCover: View {
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            Color(red: 0.051, green: 0.102, blue: 0.180),
                            Color(red: 0.086, green: 0.153, blue: 0.267),
                        ],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                )
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .strokeBorder(Color(red: 0.165, green: 0.251, blue: 0.376), lineWidth: 1)

            VStack(spacing: 14) {
                Rectangle()
                    .fill(Theme.accent.opacity(0.55))
                    .frame(height: 1)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 28)
                InterlinearTitle(
                    cells: TitleGloss.cover,
                    smSize: 24,
                    enSize: 11,
                    smColor: Theme.accent,
                    enColor: Theme.accent.opacity(0.8),
                    smWeight: .semibold,
                    tracking: 1.5,
                    spacing: 14
                )
                .padding(.horizontal, 12)
                InterlinearTitle(
                    cells: TitleGloss.subtitle,
                    smSize: 13,
                    enSize: 9,
                    smColor: Theme.accent.opacity(0.9),
                    enColor: Theme.accent.opacity(0.7),
                    smWeight: .regular,
                    tracking: 0.5,
                    spacing: 6
                )
                Rectangle()
                    .fill(Theme.accent.opacity(0.55))
                    .frame(height: 1)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 28)
            }
            .padding(.vertical, 28)
        }
        .aspectRatio(3.0 / 4.0, contentMode: .fit)
        .shadow(color: .black.opacity(0.18), radius: 10, x: 0, y: 4)
    }
}
