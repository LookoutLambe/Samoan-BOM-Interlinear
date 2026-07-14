import Foundation

/// A pushable reference to a specific chapter, resolved through `ScriptureLibrary`.
struct ChapterRef: Hashable {
    let bookId: String
    let chapterNum: Int
}
