import Foundation
import Observation

/// Per-verse note text, persisted to UserDefaults. Keys are scripture refs
/// in `bookId|chapter|verse` form. Empty/whitespace-only text deletes the note.
@Observable
final class NoteStore {
    private static let defaultsKey = "scriptureNotes.v1"
    private(set) var notes: [String: String] = [:]

    init() { load() }

    func note(for verseKey: String) -> String? {
        notes[verseKey]
    }

    func hasNote(for verseKey: String) -> Bool {
        guard let text = notes[verseKey] else { return false }
        return !text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }

    func setNote(_ text: String, for verseKey: String) {
        let trimmed = text.trimmingCharacters(in: .whitespacesAndNewlines)
        if trimmed.isEmpty {
            notes.removeValue(forKey: verseKey)
        } else {
            notes[verseKey] = text
        }
        persist()
    }

    func deleteNote(for verseKey: String) {
        notes.removeValue(forKey: verseKey)
        persist()
    }

    private func load() {
        guard let data = UserDefaults.standard.data(forKey: Self.defaultsKey),
              let decoded = try? JSONDecoder().decode([String: String].self, from: data)
        else { return }
        notes = decoded
    }

    private func persist() {
        if let data = try? JSONEncoder().encode(notes) {
            UserDefaults.standard.set(data, forKey: Self.defaultsKey)
        }
    }
}
