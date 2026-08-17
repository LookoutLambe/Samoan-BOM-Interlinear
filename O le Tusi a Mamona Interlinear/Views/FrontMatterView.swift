import SwiftUI

/// One front-matter section (Title Page, Introduction, testimonies, …) as a
/// single scrollable page: a bilingual title header + the body in the active
/// reader mode. Paging across sections — and onward into the scripture — is
/// owned by the unified `ReaderView`.
struct FrontMatterPage: View {
    let section: FrontMatterSection
    let mode: ReaderMode

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 0) {
                FrontMatterHeader(section: section)
                FrontMatterBody(section: section, mode: mode)
                    .padding(.horizontal, 20)
                    .padding(.bottom, 28)
            }
            .frame(maxWidth: 900)
            .frame(maxWidth: .infinity, alignment: .center)
        }
        .background(Theme.pageBg)
    }
}

private struct FrontMatterHeader: View {
    @Environment(\.scriptureFontScale) private var scale
    let section: FrontMatterSection

    var body: some View {
        VStack(spacing: 6) {
            Text(section.titleSm)
                .font(SerifFont.tnr(size: 30 * scale, weight: .bold))
                .foregroundStyle(Theme.ink)
                .tracking(1.0)
                .multilineTextAlignment(.center)
            Text(section.titleEn)
                .font(SerifFont.tnr(size: 15 * scale))
                .foregroundStyle(Theme.accent)
                .tracking(1.0)
                .textCase(.uppercase)
                .multilineTextAlignment(.center)
            Text("\u{2767} \u{2767} \u{2767}")
                .font(SerifFont.tnr(size: 16 * scale))
                .foregroundStyle(Theme.accent)
                .tracking(8)
                .padding(.top, 4)
            Rectangle()
                .fill(Theme.rule)
                .frame(height: 2)
                .padding(.top, 14)
        }
        .padding(.top, 20)
        .padding(.bottom, 16)
        .padding(.horizontal, 20)
        .frame(maxWidth: .infinity)
    }
}

private struct FrontMatterBody: View {
    @Environment(\.scriptureFontScale) private var scale
    let section: FrontMatterSection
    let mode: ReaderMode

    var body: some View {
        switch mode {
        case .interlinear:
            if let words = section.words, !words.isEmpty {
                // Render one flowing block per source paragraph so the section's
                // structure survives, instead of collapsing every word into a
                // single wall of cells.
                VStack(alignment: .leading, spacing: 18) {
                    ForEach(Array(paragraphs(of: words).enumerated()), id: \.offset) { _, para in
                        FlowLayout(horizontalSpacing: 6, verticalSpacing: 4) {
                            ForEach(groupIdiomSpans(para)) { item in
                                switch item {
                                case .single(_, let pair):
                                    FrontMatterGlossCell(sm: pair.sm, en: pair.en)
                                case .span(_, let samoanWords, let gloss):
                                    FrontMatterGlossCell(sm: samoanWords.joined(separator: " "), en: gloss)
                                }
                            }
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            } else {
                prose(section.sm)
            }
        case .samoan:
            prose(section.sm)
        case .dual:
            HStack(alignment: .top, spacing: 16) {
                prose(section.sm)
                Rectangle().fill(Theme.rule).frame(width: 1)
                Text(section.en)
                    .font(SerifFont.tnr(size: 17 * scale))
                    .foregroundStyle(Theme.hwInk)
                    .lineSpacing(4)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
    }

    private func prose(_ text: String) -> some View {
        Text(text)
            .font(SerifFont.tnr(size: 18 * scale))
            .foregroundStyle(Theme.hwInk)
            .lineSpacing(5)
            .frame(maxWidth: .infinity, alignment: .leading)
    }

    /// Slice the flat interlinear word stream back into paragraphs, matching
    /// the `\n\n` breaks in the Samoan source by token count. Falls back to a
    /// single paragraph if the counts don't line up.
    private func paragraphs(of words: [WordPair]) -> [[WordPair]] {
        let paraTexts = section.sm.components(separatedBy: "\n\n")
        guard paraTexts.count > 1 else { return [words] }
        var result: [[WordPair]] = []
        var idx = 0
        for para in paraTexts {
            let count = tokenCount(para)
            guard count > 0 else { continue }
            let end = min(idx + count, words.count)
            if idx >= end { break }
            result.append(Array(words[idx..<end]))
            idx = end
        }
        if idx < words.count {
            if result.isEmpty {
                result.append(words)
            } else {
                result[result.count - 1].append(contentsOf: words[idx...])
            }
        }
        return result.isEmpty ? [words] : result
    }

    /// Count tokens the same way the builder does: split on whitespace, and
    /// split `X—Y` (em-dash followed by a non-space) into two tokens.
    private func tokenCount(_ text: String) -> Int {
        var spaced = ""
        let chars = Array(text)
        for (i, c) in chars.enumerated() {
            spaced.append(c)
            if c == "\u{2014}" {
                let next: Character = i + 1 < chars.count ? chars[i + 1] : " "
                if !next.isWhitespace { spaced.append(" ") }
            }
        }
        return spaced.split(whereSeparator: { $0.isWhitespace }).count
    }
}

/// Static (non-interactive) interlinear cell for front matter.
private struct FrontMatterGlossCell: View {
    @Environment(\.scriptureFontScale) private var scale
    let sm: String
    let en: String

    var body: some View {
        // Both lines size to their natural single-line width (no fixed maxWidth
        // cap). FlowLayout measures each cell at that width, so the gloss never
        // renders taller than it was measured — which is what made a capped
        // gloss wrap and spill onto the next Samoan row.
        VStack(alignment: .center, spacing: 1) {
            Text(sm)
                .font(SerifFont.tnr(size: 18 * scale, weight: .medium))
                .foregroundStyle(Theme.hwInk)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
            if !en.isEmpty {
                Text(en)
                    .font(SerifFont.tnr(size: 11 * scale, italic: true))
                    .foregroundStyle(Theme.glossInk)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}
