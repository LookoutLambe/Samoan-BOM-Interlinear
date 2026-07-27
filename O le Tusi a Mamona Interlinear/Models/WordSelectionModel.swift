import Foundation
import Observation

/// Tracks which Samoan word-units are currently selected in the reader, so the
/// user can tap words to build up a selection and then highlight or annotate
/// them — mirroring the per-word (`data-wid`) model of the Gospel Library /
/// Standard Works reader. Selection is scoped to a single verse at a time:
/// tapping a word in a different verse starts a fresh selection.
///
/// Word keys are `bookId|chapter|verse|wordIndex`; verse keys are the same
/// string without the trailing `|wordIndex`.
@Observable
final class WordSelectionModel {
    private(set) var selected: Set<String> = []
    private(set) var texts: [String: String] = [:]
    private(set) var verseKey: String?

    /// Whole-verse selection — distinct from the per-word `selected` set. When
    /// set, the action bar operates on the verse as a single unit and the
    /// highlight/note is stored under the 3-part verse key (`bookId|chapter|verse`).
    /// This is the granularity used in the Samoa / Tutusa modes and via the
    /// verse-number tap in every mode.
    private(set) var wholeVerseKey: String?
    private(set) var wholeVerseText: String = ""

    var isEmpty: Bool { selected.isEmpty && wholeVerseKey == nil }
    var isWholeVerse: Bool { wholeVerseKey != nil }

    func isSelected(_ key: String) -> Bool { selected.contains(key) }
    func isVerseSelected(_ verseKey: String) -> Bool { wholeVerseKey == verseKey }

    /// Toggle a word in/out of the selection. Switching verses resets first.
    /// Starting a per-word selection clears any whole-verse selection.
    func toggle(key: String, text: String, verseKey: String) {
        wholeVerseKey = nil
        wholeVerseText = ""
        if self.verseKey != verseKey {
            selected.removeAll()
            texts.removeAll()
            self.verseKey = verseKey
        }
        if selected.contains(key) {
            selected.remove(key)
            texts.removeValue(forKey: key)
        } else {
            selected.insert(key)
            texts[key] = text
        }
        if selected.isEmpty { self.verseKey = nil }
    }

    /// Toggle a whole verse in/out of selection. Clears any per-word selection
    /// first, so word- and verse-level selections never coexist.
    func toggleVerse(verseKey: String, text: String) {
        selected.removeAll()
        texts.removeAll()
        self.verseKey = nil
        if wholeVerseKey == verseKey {
            wholeVerseKey = nil
            wholeVerseText = ""
        } else {
            wholeVerseKey = verseKey
            wholeVerseText = text
        }
    }

    func clear() {
        selected.removeAll()
        texts.removeAll()
        verseKey = nil
        wholeVerseKey = nil
        wholeVerseText = ""
    }

    /// Selected keys ordered by their word index within the verse.
    var sortedKeys: [String] {
        selected.sorted { (index(of: $0) ?? 0) < (index(of: $1) ?? 0) }
    }

    /// The lowest-index selected word — where a note for the selection anchors.
    var anchorKey: String? { sortedKeys.first }

    /// The selected Samoan words joined in reading order.
    var joinedText: String {
        sortedKeys.compactMap { texts[$0] }.joined(separator: " ")
    }

    private func index(of key: String) -> Int? {
        Int(key.split(separator: "|").last ?? "")
    }
}
