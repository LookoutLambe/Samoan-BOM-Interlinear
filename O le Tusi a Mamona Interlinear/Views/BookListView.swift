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
                    // One cover card per volume — the Book of Mormon, D&C, Pearl of
                    // Great Price, Old and New Testament — each the way into its
                    // books: tapping opens the library at that volume.
                    VolumeCovers()
                        .padding(.horizontal, 20)
                        .padding(.top, 24)

                    ContinueReadingButton()
                        .padding(.top, 24)

                    DisclaimerNotice()
                        .padding(.top, 36)

                    SourceNotice()
                        .padding(.top, 12)
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
        NoticeBlock(english: english, samoan: samoan, gloss: gloss)
    }
}

/// Where the Old and New Testament text comes from, under the license notice
/// in the same three registers. The Samoan Bible in the app is O le Tusi Paia,
/// the London Missionary Society translation, which is in the public domain;
/// the copy used is the Church's own printing of that text (user, 2026-09-05).
/// build_web_data.py lifts these strings for the web landing too.
private struct SourceNotice: View {
    private let english = """
    The Old and New Testament in this app are O le Tusi Paia, the Samoan Bible \
    translated by the London Missionary Society. That translation is in the \
    public domain. The text used here is the 1887 printing by the British and \
    Foreign Bible Society, the same London Missionary Society text that The \
    Church of Jesus Christ of Latter-day Saints distributes and sells. The \
    English beside it is the King James Version, also in the public domain.
    """

    private let samoan = """
    O le Feagaiga Tuai ma le Feagaiga Fou i lenei polokalama, o le Tusi Paia lea \
    na fa\u{02bb}aliliuina e le London Missionary Society. O lena fa\u{02bb}aliliuga \
    e leai sona puletaofia. O le tusitusiga o lo\u{02bb}o fa\u{02bb}aaog\u{0101}ina i \
    lenei mea, o le lomiga lea i le 1887 e le British and Foreign Bible Society, o \
    le tusitusiga lava lea a le London Missionary Society e tufatufaina ma \
    fa\u{02bb}atauina atu e Le Ekalesia a Iesu Keriso o le Au Paia o Aso e Gata Ai. \
    O le fa\u{02bb}aPeretania i ona tafatafa o le King James Version, e leai \
    fo\u{02bb}i sona puletaofia.
    """

    // Word-by-word interlinear (Samoan surface phrase, concise English gloss).
    private let gloss: [(String, String)] = [
        ("O le Feagaiga Tuai", "The Old Testament"),
        ("ma le Feagaiga Fou", "and the New Testament"),
        ("i lenei polokalama,", "in this app,"),
        ("o le Tusi Paia lea", "are the Holy Bible"),
        ("na fa\u{02bb}aliliuina", "translated"),
        ("e le London Missionary Society.", "by the London Missionary Society."),
        ("O lena fa\u{02bb}aliliuga", "That translation"),
        ("e leai sona puletaofia.", "has no copyright: public domain."),
        ("O le tusitusiga", "The text"),
        ("o lo\u{02bb}o fa\u{02bb}aaog\u{0101}ina", "used"),
        ("i lenei mea,", "here,"),
        ("o le lomiga lea", "is the printing"),
        ("i le 1887", "of 1887"),
        ("e le British and Foreign Bible Society,", "by the British and Foreign Bible Society,"),
        ("o le tusitusiga lava lea", "the same text"),
        ("a le London Missionary Society", "of the London Missionary Society"),
        ("e tufatufaina", "distributed"),
        ("ma fa\u{02bb}atauina atu", "and sold"),
        ("e Le Ekalesia a Iesu Keriso", "by The Church of Jesus Christ"),
        ("o le Au Paia o Aso e Gata Ai.", "of Latter-day Saints."),
        ("O le fa\u{02bb}aPeretania", "The English"),
        ("i ona tafatafa", "beside it"),
        ("o le King James Version,", "is the King James Version,"),
        ("e leai fo\u{02bb}i sona puletaofia.", "also with no copyright."),
    ]

    var body: some View {
        NoticeBlock(english: english, samoan: samoan, gloss: gloss)
    }
}

/// The three-register notice block both landing notices share: the English,
/// a hairline, the Samoan, a hairline, then the word-by-word interlinear.
private struct NoticeBlock: View {
    let english: String
    let samoan: String
    let gloss: [(String, String)]

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

/// The interlinear breakdown of each volume's title, curated per
/// GLOSSING_RULES.md: the glosses read cell by cell in Samoan order, as the
/// reader itself does. Keyed by volume id; the drawer supplies the volumes.
private enum TitleGloss {
    struct Spec { let titles: [InterlinearTitle.Cell]; let subtitles: [InterlinearTitle.Cell] }
    static let specs: [String: Spec] = [
        "bom": Spec(
            titles: [.init(sm: "O LE TUSI", en: "The Book"), .init(sm: "A MAMONA", en: "of Mormon")],
            subtitles: [.init(sm: "O se tasi molimau", en: "Another testimony"),
                        .init(sm: "a Iesu Keriso", en: "of Jesus Christ")]),
        "dc": Spec(
            titles: [.init(sm: "MATAUPU FAAVAE", en: "Doctrine"), .init(sm: "MA FEAGAIGA", en: "and Covenants")],
            subtitles: [.init(sm: "a le Ekalesia a Iesu Keriso", en: "of the Church of Jesus Christ"),
                        .init(sm: "o le Au Paia o Aso e Gata Ai", en: "of Latter-day Saints")]),
        "pgp": Spec(
            titles: [.init(sm: "LE PENINA", en: "The Pearl"), .init(sm: "SILISILI ONA TAUA", en: "of Great Price")],
            subtitles: [.init(sm: "Faaaliga ma faaliliuga", en: "Revelations and translations"),
                        .init(sm: "a Iosefa Samita", en: "of Joseph Smith")]),
        "ot": Spec(
            titles: [.init(sm: "O LE FEAGAIGA", en: "The Testament"), .init(sm: "TUAI", en: "Old")],
            subtitles: [.init(sm: "O le Tusi Paia", en: "The Holy Bible"),
                        .init(sm: "Kenese \u{2013} Malaki", en: "Genesis \u{2013} Malachi")]),
        "nt": Spec(
            titles: [.init(sm: "O LE FEAGAIGA", en: "The Testament"), .init(sm: "FOU", en: "New")],
            subtitles: [.init(sm: "O le Tusi Paia", en: "The Holy Bible"),
                        .init(sm: "Mataio \u{2013} Faaaliga", en: "Matthew \u{2013} Revelation")]),
    ]
}

// MARK: - Volume covers (navy gradient plates)

/// The landing page's cards: one plate per volume, two across, in reading
/// order. Each opens the library drawer scrolled to that volume's books.
private struct VolumeCovers: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(Navigator.self) private var nav

    private let columns = [GridItem(.adaptive(minimum: 150, maximum: 260), spacing: 16)]

    var body: some View {
        LazyVGrid(columns: columns, spacing: 16) {
            ForEach(library.allVolumes) { volume in
                let spec = TitleGloss.specs[volume.id]
                    ?? TitleGloss.Spec(titles: [.init(sm: volume.nameSm.uppercased(), en: volume.nameEn)], subtitles: [])
                Button { nav.openLibrary(volume: volume.id) } label: {
                    CoverPlate(titles: spec.titles, subtitles: spec.subtitles)
                }
                .buttonStyle(.plain)
                .accessibilityLabel("Tatala: \(volume.nameSm)")
            }
        }
    }
}

/// One cover plate: interlinear title cells over interlinear subtitle cells,
/// between two gold rules, on the navy gradient. Gold on navy is the bright
/// accent (Theme.accent here is the Hebrew app's gold), never a paper mark.
private struct CoverPlate: View {
    let titles: [InterlinearTitle.Cell]
    let subtitles: [InterlinearTitle.Cell]

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
                    cells: titles,
                    smSize: 17,
                    enSize: 9.5,
                    smColor: Theme.accent,
                    enColor: Theme.accent.opacity(0.85),
                    smWeight: .semibold,
                    tracking: 1.2,
                    spacing: 10
                )
                .padding(.horizontal, 10)
                .minimumScaleFactor(0.8)
                InterlinearTitle(
                    cells: subtitles,
                    smSize: 11,
                    enSize: 8.5,
                    smColor: Theme.accent.opacity(0.9),
                    enColor: Theme.accent.opacity(0.8),
                    smWeight: .regular,
                    tracking: 0.4,
                    spacing: 5
                )
                .padding(.horizontal, 10)
                .minimumScaleFactor(0.8)
                Rectangle()
                    .fill(Theme.accent.opacity(0.55))
                    .frame(height: 1)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 28)
            }
            .padding(.vertical, 20)
        }
        .aspectRatio(3.0 / 4.0, contentMode: .fit)
        .shadow(color: .black.opacity(0.18), radius: 10, x: 0, y: 4)
    }
}
