import SwiftUI

/// The app is the website (user, 2026-09-08: *"i just want it to mirror the
/// website"*). The target copies `docs/` — the site itself, the one served at
/// samoanbominterlinear.org — into the bundle as a folder reference, and shows
/// it below. Nothing is duplicated: the app and the site are the same files.
///
/// The native reader has NOT been deleted — `BookListView`, `ReaderView`, the
/// library drawer and the rest still build, and their own layout fixes are in.
/// Flipping this one constant brings them back.
private let useWebReader = true

struct ContentView: View {
    var body: some View {
        if useWebReader {
            WebReader()
        } else {
            NativeReader()
        }
    }

    /// The bundled site, edge to edge: its own CSS pads for the notch and the
    /// home indicator with `env(safe-area-inset-*)`, so SwiftUI must not.
    private struct WebReader: View {
        var body: some View {
            if let www = Bundle.main.url(forResource: "docs", withExtension: nil),
               FileManager.default.fileExists(atPath: www.appendingPathComponent("index.html").path) {
                LocalSiteWebView(wwwDirectoryURL: www)
                    .ignoresSafeArea()
            } else {
                MissingSiteView()
            }
        }
    }

    private struct NativeReader: View {
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
            // The library is a full-height side panel, not a bottom card —
            // the shape it has on the web. See SideDrawer.swift.
            .sideDrawer(isOpen: $nav.libraryOpen,
                        edge: .leading,
                        title: "Faletusi \u{00B7} Library") {
                LibraryDrawer()
            }
            .fullScreenCover(isPresented: $nav.searchOpen) {
                SearchView()
            }
        }
    }
}

/// Shown when the target was built without the mirror.
private struct MissingSiteView: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("O le Tusi a Mamona")
                .font(SerifFont.tnr(size: 22, weight: .bold))
                .foregroundStyle(Theme.headerBg)
            Text("The site is not in the app bundle. In Xcode, check that the blue docs folder is in the target's Copy Bundle Resources phase, then build again.")
                .multilineTextAlignment(.center)
                .foregroundStyle(Theme.inkLight)
                .padding(.horizontal, 32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Theme.pageBg)
    }
}
