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

    init() {
        let storedScale = UserDefaults.standard.double(forKey: Self.fontScaleKey)
        self.fontScale = (storedScale >= 0.6 && storedScale <= 2.0) ? storedScale : 1.0

        if let raw = UserDefaults.standard.string(forKey: Self.readerModeKey),
           let mode = ReaderMode(rawValue: raw) {
            self.readerMode = mode
        } else {
            self.readerMode = .interlinear
        }
    }
}
