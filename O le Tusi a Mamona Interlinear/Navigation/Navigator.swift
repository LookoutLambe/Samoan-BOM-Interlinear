import Foundation
import SwiftUI
import Observation

/// Shared navigation state: drives the root `NavigationStack` path and
/// the presentation of the library drawer sheet from any screen.
@Observable
final class Navigator {
    var path = NavigationPath()
    var libraryOpen = false
    var searchOpen = false

    /// A pending request to scroll to (and briefly flash) a specific verse once
    /// its chapter page is on screen — set when a search result is tapped and
    /// consumed by the reader's chapter page. The `token` makes two requests for
    /// the same verse distinct so the reader re-triggers.
    struct VerseTarget: Equatable {
        let ref: ChapterRef
        let verse: Int
        let token: Int
    }
    var verseTarget: VerseTarget?
    private var verseTargetToken = 0

    func openHome() {
        path = NavigationPath()
        libraryOpen = false
    }

    func openChapter(book: Book, chapterNum: Int) {
        openChapter(ChapterRef(bookId: book.id, chapterNum: chapterNum))
    }

    /// Open the reader directly at a chapter (used by the landing page's
    /// "Continue reading" shortcut).
    func openChapter(_ ref: ChapterRef) {
        var p = NavigationPath()
        p.append(ref)
        path = p
        libraryOpen = false
    }

    /// Open the reader at a chapter and request a scroll to a specific verse
    /// (used when a search result is tapped).
    func openChapter(_ ref: ChapterRef, verse: Int) {
        verseTargetToken += 1
        verseTarget = VerseTarget(ref: ref, verse: verse, token: verseTargetToken)
        openChapter(ref)
    }

    func openFrontMatter(id: String) {
        var p = NavigationPath()
        p.append(FrontMatterRef(id: id))
        path = p
        libraryOpen = false
    }
}
