import SwiftUI

/// One interlinear word-unit: Samoan surface form stacked above its English gloss.
/// Honors `\.scriptureFontScale` so the user's reader-size preference applies.
/// If the gloss is empty (not yet curated), the bottom row collapses cleanly.
///
/// Tappable: tapping toggles the word in the reader's selection, which the
/// bottom action bar then highlights or annotates. A saved highlight tints the
/// word; a saved note shows a small dot.
struct WordUnitView: View {
    @Environment(\.scriptureFontScale) private var scale
    @Environment(HighlightStore.self) private var highlights
    @Environment(NoteStore.self) private var notes
    @Environment(WordSelectionModel.self) private var selection
    let pair: WordPair
    let wordKey: String
    let verseKey: String

    var body: some View {
        Button {
            selection.toggle(key: wordKey, text: pair.sm, verseKey: verseKey)
        } label: {
            VStack(alignment: .center, spacing: 2) {
                Text(pair.sm)
                    .font(SerifFont.tnr(size: 22 * scale, weight: .medium))
                    .foregroundStyle(Theme.hwInk)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
                if !pair.en.isEmpty {
                    Text(pair.en)
                        .font(SerifFont.tnr(size: 12 * scale, italic: true))
                        .foregroundStyle(Theme.glossInk)
                        .multilineTextAlignment(.center)
                        .fixedSize(horizontal: false, vertical: true)
                        .frame(maxWidth: 120 * scale)
                }
            }
            .wordUnitDecoration(
                highlight: highlights.color(for: wordKey),
                selected: selection.isSelected(wordKey),
                hasNote: notes.hasNote(for: wordKey)
            )
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }
}

/// Shared background/selection/note chrome for a tappable word-unit.
struct WordUnitDecoration: ViewModifier {
    let highlight: HighlightColor?
    let selected: Bool
    let hasNote: Bool

    func body(content: Content) -> some View {
        content
            .padding(.horizontal, 4)
            .padding(.vertical, 2)
            .background {
                if let highlight {
                    RoundedRectangle(cornerRadius: 4, style: .continuous)
                        .fill(highlight.tint)
                }
            }
            .overlay {
                RoundedRectangle(cornerRadius: 4, style: .continuous)
                    .strokeBorder(Theme.accent, lineWidth: selected ? 2 : 0)
            }
            .overlay(alignment: .topTrailing) {
                if hasNote {
                    Circle()
                        .fill(Theme.accent)
                        .frame(width: 6, height: 6)
                        .offset(x: -1, y: 1)
                }
            }
    }
}

extension View {
    func wordUnitDecoration(highlight: HighlightColor?, selected: Bool, hasNote: Bool) -> some View {
        modifier(WordUnitDecoration(highlight: highlight, selected: selected, hasNote: hasNote))
    }
}

/// Multi-word TAM-phrase span: the Samoan words joined into a single Text so
/// they wrap naturally at large font scales, with one English gloss centered
/// beneath. Used for things like "sa oo ina → it came to pass" so the English
/// isn't fragmented with `·` cells.
struct IdiomSpanView: View {
    @Environment(\.scriptureFontScale) private var scale
    @Environment(HighlightStore.self) private var highlights
    @Environment(NoteStore.self) private var notes
    @Environment(WordSelectionModel.self) private var selection
    let samoanWords: [String]
    let englishGloss: String
    let wordKey: String
    let verseKey: String

    private var joined: String { samoanWords.joined(separator: " ") }

    var body: some View {
        Button {
            selection.toggle(key: wordKey, text: joined, verseKey: verseKey)
        } label: {
            VStack(alignment: .center, spacing: 2) {
                Text(joined)
                    .font(SerifFont.tnr(size: 22 * scale, weight: .medium))
                    .foregroundStyle(Theme.hwInk)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
                if !englishGloss.isEmpty {
                    Text(englishGloss)
                        .font(SerifFont.tnr(size: 12 * scale, italic: true))
                        .foregroundStyle(Theme.glossInk)
                        .multilineTextAlignment(.center)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            .wordUnitDecoration(
                highlight: highlights.color(for: wordKey),
                selected: selection.isSelected(wordKey),
                hasNote: notes.hasNote(for: wordKey)
            )
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }
}

// MARK: - TAM-phrase span grouping
//
// The `·` (middle dot) gloss is a marker meaning "this Samoan word's English
// continues to the next word". A run of `·` cells followed by a real English
// cell forms one TAM-phrase span — rendered visually as the Samoan words on
// one line with the single English meaning centered below all of them.

enum VerseFlowItem: Identifiable {
    case single(index: Int, pair: WordPair)
    case span(index: Int, samoanWords: [String], englishGloss: String)

    var id: Int {
        switch self {
        case .single(let i, _): return i
        case .span(let i, _, _): return i
        }
    }
}

func groupIdiomSpans(_ words: [WordPair]) -> [VerseFlowItem] {
    var result: [VerseFlowItem] = []
    var i = 0
    while i < words.count {
        if words[i].en == "·" {
            var end = i
            while end < words.count && words[end].en == "·" {
                end += 1
            }
            if end < words.count {
                let samoanWords = (i...end).map { words[$0].sm }
                let englishGloss = words[end].en
                result.append(.span(index: i, samoanWords: samoanWords, englishGloss: englishGloss))
                i = end + 1
                continue
            }
        }
        result.append(.single(index: i, pair: words[i]))
        i += 1
    }
    return result
}
