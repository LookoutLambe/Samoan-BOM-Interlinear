import Foundation
import SwiftUI
import Observation

/// Shared navigation state: drives the root `NavigationStack` path and
/// the presentation of the library drawer sheet from any screen.
@Observable
final class Navigator {
    var path = NavigationPath()
    var libraryOpen = false

    func openHome() {
        path = NavigationPath()
        libraryOpen = false
    }

    func openBook(_ book: Book) {
        var p = NavigationPath()
        p.append(book)
        path = p
        libraryOpen = false
    }

    func openChapter(book: Book, chapterNum: Int) {
        var p = NavigationPath()
        p.append(book)
        p.append(ChapterRef(bookId: book.id, chapterNum: chapterNum))
        path = p
        libraryOpen = false
    }

    func replaceTopChapter(with ref: ChapterRef) {
        if !path.isEmpty {
            path.removeLast()
        }
        path.append(ref)
    }
}
