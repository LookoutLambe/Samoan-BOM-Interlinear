import Foundation
import Observation

/// Loads bundled Book of Mormon data on first access and exposes
/// it to the view layer. English text and crossrefs are loaded lazily.
@MainActor
@Observable
final class ScriptureLibrary {
    private(set) var books: [Book] = []
    private(set) var loadError: String?

    private var englishVerses: [String: String]?
    private var crossRefs: [String: [CrossRef]]?
    private var headings: [String: HeadingSection]?
    private var colophons: [String: HeadingSection]?
    private var frontMatterSections: [FrontMatterSection]?
    private var searchRows: [SearchRow]?
    private var diacritics: DiacriticMarks?
    private var diacriticsLoadAttempted = false

    init() {
        loadBooks()
    }

    // MARK: Verses (eager)

    private func loadBooks() {
        guard let url = Bundle.main.url(forResource: "bom_books", withExtension: "json") else {
            loadError = "bom_books.json not found in bundle"
            return
        }
        do {
            let data = try Data(contentsOf: url)
            let decoded = try JSONDecoder().decode(BookOfMormon.self, from: data)
            books = decoded.books
            applyGlossOverrides()
        } catch {
            loadError = "Failed to decode bom_books.json: \(error.localizedDescription)"
        }
    }

    /// Merges hand-curated TAM-phrase gloss corrections from `bom_overrides.json`
    /// on top of the bundled source data. An override only replaces a verse's
    /// `words` array if the word count matches the source; mismatches are
    /// silently skipped to keep the reader robust against stale overrides.
    private func applyGlossOverrides() {
        guard let url = Bundle.main.url(forResource: "bom_overrides", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let payload = try? JSONDecoder().decode(GlossOverrides.self, from: data)
        else { return }

        books = books.map { book in
            let newChapters = book.chapters.map { chapter in
                let newVerses = chapter.verses.map { verse in
                    let key = "\(book.id)|\(chapter.num)|\(verse.num)"
                    if let newWords = payload.verses[key], newWords.count == verse.words.count {
                        return Verse(num: verse.num, words: newWords)
                    }
                    return verse
                }
                return Chapter(num: chapter.num, verses: newVerses)
            }
            return Book(id: book.id, nameSm: book.nameSm, nameEn: book.nameEn, chapters: newChapters)
        }
    }

    func book(id: String) -> Book? {
        books.first { $0.id == id }
    }

    /// Flat ordered list of every chapter ref in the BoM, used by the
    /// page-paged reader so swipes can fall through book boundaries.
    var allChapterRefs: [ChapterRef] {
        books.flatMap { book in
            book.chapters.map { ChapterRef(bookId: book.id, chapterNum: $0.num) }
        }
    }

    /// The whole book as one continuous run of pages: every front-matter
    /// section in order, then every chapter. Drives the unified reader so a
    /// swipe carries from the last front-matter page into 1 Nephi 1.
    var allReadingItems: [ReadingItem] {
        frontMatter().map { .front($0.id) } + allChapterRefs.map { .chapter($0) }
    }

    // MARK: Linear chapter navigation

    func nextChapter(after ref: ChapterRef) -> ChapterRef? {
        guard let bookIdx = books.firstIndex(where: { $0.id == ref.bookId }) else { return nil }
        let book = books[bookIdx]
        if ref.chapterNum < book.chapters.count {
            return ChapterRef(bookId: book.id, chapterNum: ref.chapterNum + 1)
        }
        let nextIdx = bookIdx + 1
        guard nextIdx < books.count else { return nil }
        return ChapterRef(bookId: books[nextIdx].id, chapterNum: 1)
    }

    func previousChapter(before ref: ChapterRef) -> ChapterRef? {
        guard let bookIdx = books.firstIndex(where: { $0.id == ref.bookId }) else { return nil }
        if ref.chapterNum > 1 {
            return ChapterRef(bookId: ref.bookId, chapterNum: ref.chapterNum - 1)
        }
        let prevIdx = bookIdx - 1
        guard prevIdx >= 0 else { return nil }
        let prevBook = books[prevIdx]
        return ChapterRef(bookId: prevBook.id, chapterNum: prevBook.chapters.count)
    }

    // MARK: English (lazy)

    func englishText(for key: ScriptureKey) -> String? {
        ensureEnglishLoaded()
        return englishVerses?[key.raw]
    }

    private func ensureEnglishLoaded() {
        guard englishVerses == nil,
              let url = Bundle.main.url(forResource: "bom_english", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode([String: String].self, from: data)
        else { return }
        englishVerses = decoded
    }

    // MARK: Diacritics (lazy)
    //
    // The bundled text follows the published unmarked orthography. When the
    // reader turns pronunciation marks on, tokens are rewritten through this
    // layer at render time — the underlying text is never modified.

    /// Restores macrons and glottal stops on a single Samoan token, preserving
    /// its leading/trailing punctuation and capitalization.
    ///
    /// `wordKey` (`"bookId|chapter|verse|tokenIndex"`) lets a context-dependent
    /// word override the type-level mapping — `mai` "from" vs `ma’i` "sick".
    /// Returns the token unchanged when the word hasn't been curated yet.
    func markedSamoan(_ token: String, wordKey: String? = nil) -> String {
        ensureDiacriticsLoaded()
        guard let diacritics else { return token }

        let (prefix, core, suffix) = Self.splitAffixes(token)
        guard !core.isEmpty else { return token }

        let replacement: String?
        if let wordKey, let exception = diacritics.exceptions[wordKey] {
            replacement = exception
        } else {
            replacement = diacritics.types[core.lowercased()]
        }
        guard let replacement else { return token }

        return prefix + Self.matchingCapitalization(of: core, applyingTo: replacement) + suffix
    }

    /// Splits a token into (leading punctuation, word core, trailing punctuation).
    /// The glottal `’` and hyphen are treated as intra-word, so `a’u,` splits as
    /// `("", "a’u", ",")`. Mirrors `normalize` in `scripts/build_diacritics.py`.
    static func splitAffixes(_ token: String) -> (String, String, String) {
        let isWordChar: (Character) -> Bool = { ch in
            ch.isLetter || ch.isNumber || ch == "\u{2019}" || ch == "-"
        }
        guard let first = token.firstIndex(where: isWordChar),
              let last = token.lastIndex(where: isWordChar)
        else { return ("", "", token) }
        return (
            String(token[token.startIndex..<first]),
            String(token[first...last]),
            String(token[token.index(after: last)...])
        )
    }

    /// Reapplies `original`'s capitalization to a lowercase marked form, so a
    /// sentence-initial `Faauta` doesn't come back as `fa’auta`.
    private static func matchingCapitalization(of original: String, applyingTo marked: String) -> String {
        guard let firstOriginal = original.first, firstOriginal.isUppercase else { return marked }
        return marked.prefix(1).uppercased() + marked.dropFirst()
    }

    private func ensureDiacriticsLoaded() {
        guard !diacriticsLoadAttempted else { return }
        diacriticsLoadAttempted = true
        guard let url = Bundle.main.url(forResource: "bom_diacritics", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode(DiacriticMarks.self, from: data)
        else { return }
        diacritics = decoded
    }

    // MARK: Cross-references (lazy)

    func crossRefs(for key: ScriptureKey) -> [CrossRef] {
        ensureCrossRefsLoaded()
        return crossRefs?[key.raw] ?? []
    }

    private func ensureCrossRefsLoaded() {
        guard crossRefs == nil,
              let url = Bundle.main.url(forResource: "bom_crossrefs", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode([String: [CrossRef]].self, from: data)
        else { return }
        crossRefs = decoded
    }

    // MARK: Chapter headings (lazy)

    /// The editorial chapter summary for a chapter, if one has been curated.
    func heading(bookId: String, chapter: Int) -> HeadingSection? {
        ensureHeadingsLoaded()
        return headings?["\(bookId)|\(chapter)"]
    }

    private func ensureHeadingsLoaded() {
        guard headings == nil,
              let url = Bundle.main.url(forResource: "bom_headings", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode(ChapterHeadings.self, from: data)
        else { return }
        headings = decoded.headings
    }

    // MARK: Record-keeper colophons (lazy)

    /// The sub-record colophon that precedes a chapter, if one exists.
    func colophon(bookId: String, chapter: Int) -> HeadingSection? {
        ensureColophonsLoaded()
        return colophons?["\(bookId)|\(chapter)"]
    }

    private func ensureColophonsLoaded() {
        guard colophons == nil,
              let url = Bundle.main.url(forResource: "bom_colophons", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode(Colophons.self, from: data)
        else { return }
        colophons = decoded.colophons
    }

    // MARK: Front matter (lazy)

    /// The Book of Mormon front matter sections, in display order.
    func frontMatter() -> [FrontMatterSection] {
        ensureFrontMatterLoaded()
        return frontMatterSections ?? []
    }

    func frontMatterSection(id: String) -> FrontMatterSection? {
        frontMatter().first { $0.id == id }
    }

    private func ensureFrontMatterLoaded() {
        guard frontMatterSections == nil,
              let url = Bundle.main.url(forResource: "bom_frontmatter", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode(FrontMatter.self, from: data)
        else { return }
        frontMatterSections = decoded.sections
    }

    // MARK: Full-text search (Samoan + English)

    /// A verse hit for the search screen.
    struct SearchResult: Identifiable, Hashable {
        let ref: ChapterRef
        let verse: Int
        let reference: String   // "1 Nephi 1:1"
        let snippet: String     // the Samoan verse text
        var id: String { "\(ref.bookId)|\(ref.chapterNum)|\(verse)" }
    }

    private struct SearchRow {
        let ref: ChapterRef
        let verse: Int
        let reference: String
        let snippet: String
        let haystack: String    // normalized Samoan + English, for matching
    }

    /// Case- and diacritic-insensitive search across every verse's Samoan text
    /// and official English. Matches whole substrings; returns up to `limit`
    /// hits in scripture order.
    func search(_ raw: String, limit: Int = 300) -> [SearchResult] {
        let q = Self.normalizeForSearch(raw)
        guard q.count >= 2 else { return [] }
        ensureSearchIndex()
        var out: [SearchResult] = []
        for row in searchRows ?? [] where row.haystack.contains(q) {
            out.append(SearchResult(
                ref: row.ref, verse: row.verse,
                reference: row.reference, snippet: row.snippet
            ))
            if out.count >= limit { break }
        }
        return out
    }

    private func ensureSearchIndex() {
        guard searchRows == nil else { return }
        ensureEnglishLoaded()
        var rows: [SearchRow] = []
        rows.reserveCapacity(6800)
        for book in books {
            for chapter in book.chapters {
                for verse in chapter.verses {
                    let sm = verse.samoanText
                    let en = englishVerses?["\(book.nameEn)|\(chapter.num)|\(verse.num)"] ?? ""
                    rows.append(SearchRow(
                        ref: ChapterRef(bookId: book.id, chapterNum: chapter.num),
                        verse: verse.num,
                        reference: "\(book.nameEn) \(chapter.num):\(verse.num)",
                        snippet: sm,
                        haystack: Self.normalizeForSearch(sm + " " + en)
                    ))
                }
            }
        }
        searchRows = rows
    }

    /// Fold case + diacritics and drop glottal-stop apostrophes so a query like
    /// "faatuatua" matches "fa'atuatua"/"faatuatua" and "Nephi" matches "Nifae"'s
    /// English side.
    private static func normalizeForSearch(_ s: String) -> String {
        s.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
            .replacingOccurrences(of: "\u{02bc}", with: "")
            .replacingOccurrences(of: "\u{2019}", with: "")
            .replacingOccurrences(of: "'", with: "")
    }
}
