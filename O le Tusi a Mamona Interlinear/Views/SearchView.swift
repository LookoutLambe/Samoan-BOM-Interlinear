import SwiftUI

/// Full-text search across the whole Book of Mormon — Samoan surface text and
/// the official English — presented as a sheet. Tapping a result opens that
/// chapter in the reader. Matching is case- and diacritic-insensitive and
/// ignores glottal-stop apostrophes (see `ScriptureLibrary.search`).
struct SearchView: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(Navigator.self) private var nav
    @Environment(\.dismiss) private var dismiss

    @State private var query = ""
    @State private var results: [ScriptureLibrary.SearchResult] = []

    var body: some View {
        NavigationStack {
            Group {
                if query.trimmingCharacters(in: .whitespaces).count < 2 {
                    ContentUnavailableView(
                        "Su\u{2019}e i le Tusi a Mamona",
                        systemImage: "magnifyingglass",
                        description: Text("Search the Samoan text and the English translation.")
                    )
                } else if results.isEmpty {
                    ContentUnavailableView.search(text: query)
                } else {
                    List(results) { result in
                        Button { open(result) } label: { row(result) }
                            .listRowBackground(Theme.pageBg)
                    }
                    .listStyle(.plain)
                    .safeAreaInset(edge: .top) {
                        Text("\(results.count) fuaiupu \u{00B7} verses")
                            .font(SerifFont.tnr(size: 13, italic: true))
                            .foregroundStyle(Theme.inkLight)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.horizontal, 20)
                            .padding(.vertical, 6)
                            .background(Theme.pageBgDeep)
                    }
                }
            }
            .background(Theme.pageBg)
            .navigationTitle("Su\u{2019}e \u{00B7} Search")
            #if os(iOS)
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Theme.headerBg, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            #endif
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Fa\u{2019}amae\u{2019}a") { dismiss() }
                        .foregroundStyle(Theme.accent)
                }
            }
            .searchable(
                text: $query,
                placement: searchPlacement,
                prompt: "Su\u{2019}e upu Samoa po o le Igilisi"
            )
            .task(id: query) {
                // Debounce a touch so typing doesn't scan on every keystroke.
                try? await Task.sleep(nanoseconds: 180_000_000)
                guard !Task.isCancelled else { return }
                results = library.search(query)
            }
        }
    }

    /// The drawer placement keeps the field permanently visible on iOS, but it
    /// doesn't exist on macOS — fall back to the system default there.
    private var searchPlacement: SearchFieldPlacement {
        #if os(iOS)
        .navigationBarDrawer(displayMode: .always)
        #else
        .automatic
        #endif
    }

    private func row(_ result: ScriptureLibrary.SearchResult) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(result.reference)
                .font(SerifFont.tnr(size: 15, weight: .bold))
                .foregroundStyle(Theme.headerBg)
            Text(result.snippet)
                .font(SerifFont.tnr(size: 15))
                .foregroundStyle(Theme.hwInk)
                .lineLimit(3)
                .multilineTextAlignment(.leading)
        }
        .padding(.vertical, 4)
        .frame(maxWidth: .infinity, alignment: .leading)
        .contentShape(Rectangle())
    }

    private func open(_ result: ScriptureLibrary.SearchResult) {
        dismiss()
        nav.openChapter(result.ref, verse: result.verse)
    }
}
