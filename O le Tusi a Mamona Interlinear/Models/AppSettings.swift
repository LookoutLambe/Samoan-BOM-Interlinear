import Foundation
import Observation

/// Reader display modes, matching the Hebrew app's bottom control bar.
enum ReaderMode: String, Codable, CaseIterable, Sendable {
    case interlinear   // Samoan TAM phrase + English gloss stacked beneath
    case samoan        // Samoan-only, glosses hidden, prose flow
    case dual          // Samoan verse | Official English verse, side-by-side

    var label: String {
        switch self {
        case .interlinear: return "Interlinear"
        case .samoan:      return "Samoa"
        case .dual:        return "Tutusa"
        }
    }
}

/// User-tunable reading preferences, persisted to UserDefaults.
@Observable
final class AppSettings {
    private static let fontScaleKey  = "scriptureFontScale"
    private static let readerModeKey = "scriptureReaderMode"
    private static let showDiacriticsKey = "scriptureShowDiacritics"
    private static let furthestBookKey    = "furthestReadBookId"
    private static let furthestChapterKey = "furthestReadChapter"
    private static let furthestOrderKey   = "furthestReadOrder"

    /// Multiplier applied to interlinear typography. Default 1.0; clamped 0.7…1.8 by the UI.
    var fontScale: Double {
        didSet {
            UserDefaults.standard.set(fontScale, forKey: Self.fontScaleKey)
        }
    }

    /// Selected reader display mode.
    var readerMode: ReaderMode {
        didSet {
            UserDefaults.standard.set(readerMode.rawValue, forKey: Self.readerModeKey)
        }
    }

    /// Show macrons and glottal stops on the Samoan text. Off by default, so the
    /// reader sees the published orthography unless they ask for the marked
    /// register. See `ScriptureLibrary.markedSamoan(_:wordKey:)`.
    var showDiacritics: Bool {
        didSet {
            UserDefaults.standard.set(showDiacritics, forKey: Self.showDiacriticsKey)
        }
    }

    /// The furthest chapter the reader has reached, for the landing page's
    /// "Continue reading" shortcut. `furthestOrder` is the chapter's index in
    /// `library.allChapterRefs` (−1 when nothing has been read yet), used to
    /// decide whether a newly-viewed chapter is deeper than the stored one.
    private(set) var furthestBookId: String?
    private(set) var furthestChapter: Int
    private(set) var furthestOrder: Int

    /// Record that a chapter was read. Only advances the marker when `order`
    /// is deeper than what's stored, so paging backward never rewinds it.
    func noteChapterRead(bookId: String, chapter: Int, order: Int) {
        guard order > furthestOrder else { return }
        furthestOrder = order
        furthestBookId = bookId
        furthestChapter = chapter
        UserDefaults.standard.set(bookId, forKey: Self.furthestBookKey)
        UserDefaults.standard.set(chapter, forKey: Self.furthestChapterKey)
        UserDefaults.standard.set(order, forKey: Self.furthestOrderKey)
    }

    init() {
        let storedScale = UserDefaults.standard.double(forKey: Self.fontScaleKey)
        self.fontScale = (storedScale >= 0.6 && storedScale <= 2.0) ? storedScale : 1.0

        if let raw = UserDefaults.standard.string(forKey: Self.readerModeKey),
           let mode = ReaderMode(rawValue: raw) {
            self.readerMode = mode
        } else {
            self.readerMode = .interlinear
        }

        self.showDiacritics = UserDefaults.standard.bool(forKey: Self.showDiacriticsKey)

        self.furthestBookId = UserDefaults.standard.string(forKey: Self.furthestBookKey)
        self.furthestChapter = UserDefaults.standard.integer(forKey: Self.furthestChapterKey)
        self.furthestOrder = UserDefaults.standard.object(forKey: Self.furthestOrderKey) as? Int ?? -1
    }
}
