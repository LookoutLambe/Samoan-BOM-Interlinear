import SwiftUI

struct ContentView: View {
    @Environment(Navigator.self) private var nav

    var body: some View {
        @Bindable var nav = nav
        NavigationStack(path: $nav.path) {
            BookListView()
                .navigationDestination(for: ChapterRef.self) { ref in
                    ReaderView(item: .chapter(ref))
                }
                .navigationDestination(for: FrontMatterRef.self) { ref in
                    ReaderView(item: .front(ref.id))
                }
        }
        .sheet(isPresented: $nav.libraryOpen) {
            LibraryDrawer()
        }
        .sheet(isPresented: $nav.searchOpen) {
            SearchView()
        }
    }
}
