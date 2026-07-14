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
}
