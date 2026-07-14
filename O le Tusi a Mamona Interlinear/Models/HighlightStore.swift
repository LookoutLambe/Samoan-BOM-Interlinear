import Foundation
import SwiftUI
import Observation

/// Five highlight colors, modeled after the Gospel Library reader.
enum HighlightColor: String, CaseIterable, Codable, Sendable, Hashable {
    case yellow, pink, blue, green, purple

    var tint: Color {
        switch self {
        case .yellow: return Color(red: 1.00, green: 0.94, blue: 0.55)
        case .pink:   return Color(red: 1.00, green: 0.78, blue: 0.85)
        case .blue:   return Color(red: 0.66, green: 0.85, blue: 0.99)
        case .green:  return Color(red: 0.74, green: 0.92, blue: 0.65)
        case .purple: return Color(red: 0.85, green: 0.75, blue: 0.95)
        }
    }

    var label: String {
        switch self {
        case .yellow: return "Samasama"
        case .pink:   return "Piniki"
        case .blue:   return "Lanumoana"
        case .green:  return "Lanumeamata"
        case .purple: return "Viole"
        }
    }
}

/// Per-verse highlight color, persisted to UserDefaults as JSON.
@Observable
final class HighlightStore {
    private static let defaultsKey = "scriptureHighlights.v1"
    private(set) var highlights: [String: HighlightColor] = [:]

    init() { load() }

    func color(for verseKey: String) -> HighlightColor? {
        highlights[verseKey]
    }

    func set(_ color: HighlightColor?, for verseKey: String) {
        if let color {
            highlights[verseKey] = color
        } else {
            highlights.removeValue(forKey: verseKey)
        }
        persist()
    }

    private func load() {
        guard let data = UserDefaults.standard.data(forKey: Self.defaultsKey),
              let decoded = try? JSONDecoder().decode([String: HighlightColor].self, from: data)
        else { return }
        highlights = decoded
    }

    private func persist() {
        if let data = try? JSONEncoder().encode(highlights) {
            UserDefaults.standard.set(data, forKey: Self.defaultsKey)
        }
    }
}
