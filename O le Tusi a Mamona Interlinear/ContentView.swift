import SwiftUI

struct ContentView: View {
    @Environment(Navigator.self) private var nav

    var body: some View {
        @Bindable var nav = nav
        NavigationStack(path: $nav.path) {
            BookListView()
                .navigationDestination(for: Book.self) { book in
                    ChapterListView(book: book)
                }
                .navigationDestination(for: ChapterRef.self) { ref in
                    ChapterView(ref: ref)
                }
        }
        .sheet(isPresented: $nav.libraryOpen) {
            LibraryDrawer()
        }
    }
}
