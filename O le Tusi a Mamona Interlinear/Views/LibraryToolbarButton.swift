import SwiftUI

/// Applied via `.libraryToolbar()` on any screen. Adds the hamburger button
/// to the trailing edge of the navigation bar; tapping it opens the
/// `LibraryDrawer` sheet via the shared `Navigator`.
struct LibraryToolbarModifier: ViewModifier {
    @Environment(Navigator.self) private var nav

    func body(content: Content) -> some View {
        content.toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    nav.libraryOpen = true
                } label: {
                    Image(systemName: "line.3.horizontal")
                        .font(.title3.weight(.semibold))
                        .foregroundStyle(Theme.accent)
                        .accessibilityLabel("Faleoloa")
                }
            }
        }
    }
}

extension View {
    func libraryToolbar() -> some View {
        modifier(LibraryToolbarModifier())
    }
}
