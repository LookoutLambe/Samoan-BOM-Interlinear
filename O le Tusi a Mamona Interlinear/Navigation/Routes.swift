import Foundation

/// A pushable reference to a specific chapter, resolved through `ScriptureLibrary`.
struct ChapterRef: Hashable {
    let bookId: String
    let chapterNum: Int
}

/// A pushable reference to a front-matter section (Title Page, Introduction,
/// testimonies, …), resolved through `ScriptureLibrary`.
struct FrontMatterRef: Hashable {
    let id: String
}

/// One page in the continuous reader — either a front-matter section or a
/// chapter. Lets the front matter and the scripture share a single horizontal
/// pager, so a swipe can carry straight from the last front-matter page into
/// 1 Nephi 1.
enum ReadingItem: Hashable, Identifiable {
    case front(String)
    case chapter(ChapterRef)

    var id: String {
        switch self {
        case .front(let sectionId): return "fm:\(sectionId)"
        case .chapter(let ref): return "ch:\(ref.bookId):\(ref.chapterNum)"
        }
    }
}
