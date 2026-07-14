import Foundation

// MARK: - Data Model
//
// The bundled `bom_books.json` decodes directly into `BookOfMormon`.
// English verses and crossrefs are loaded lazily by `ScriptureLibrary`
// from their own JSON files.

struct BookOfMormon: Codable, Sendable {
    let books: [Book]
}

struct Book: Codable, Identifiable, Hashable, Sendable {
    let id: String          // e.g. "1nephi", "alma"
    let nameSm: String      // "1 Nifae"
    let nameEn: String      // "1 Nephi"
    let chapters: [Chapter]
}

struct Chapter: Codable, Identifiable, Hashable, Sendable {
    let num: Int
    let verses: [Verse]

    var id: Int { num }
}

struct Verse: Codable, Identifiable, Hashable, Sendable {
    let num: Int
    let words: [WordPair]

    var id: Int { num }

    /// Samoan-only prose, reconstructed by joining word tokens with spaces.
    var samoanText: String {
        words.map(\.sm).joined(separator: " ")
    }
}

struct WordPair: Codable, Hashable, Sendable {
    let sm: String   // Samoan surface form (may include trailing punctuation)
    let en: String   // English gloss — "·" marks "this word continues into the next" for TAM phrases
}

// MARK: - Cross-reference key & entry
//
// Keys in bom_english.json and bom_crossrefs.json look like "1 Nephi|1|1"
// (English book name | chapter | verse).

struct ScriptureKey: Hashable, Sendable {
    let bookEn: String
    let chapter: Int
    let verse: Int

    var raw: String { "\(bookEn)|\(chapter)|\(verse)" }
}

struct CrossRef: Codable, Hashable, Sendable {
    let marker: String     // "a", "b", "c"...
    let text: String       // anchor word
    let refs: [String]     // ["TG Time", "Mosiah 4:2", ...]
    let category: String   // "tg" | "cross-ref" | "trn"
}

// MARK: - Override payload
//
// `bom_overrides.json` is a sparse map of corrected glosses keyed by
// "bookId|chapterNum|verseNum" → full replacement word array.
struct GlossOverrides: Codable, Sendable {
    let version: Int
    let verses: [String: [WordPair]]
}
