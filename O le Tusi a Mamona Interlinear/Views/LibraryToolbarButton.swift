import SwiftUI

/// Applied via `.libraryToolbar()` on any screen. Adds the hamburger button
/// to the trailing edge of the navigation bar; tapping it opens the
/// `LibraryDrawer` sheet via the shared `Navigator`.
struct LibraryToolbarModifier: ViewModifier {
    @Environment(Navigator.self) private var nav

    func body(content: Content) -> some View {
        content.toolbar {
            // Hiding the shared background keeps each button on its own, rather
            // than letting them share one glass capsule — but that's 26.0+, so
            // fall back to the default grouping on older systems.
            if #available(iOS 26.0, macOS 26.0, visionOS 26.0, *) {
                searchItem.sharedBackgroundVisibility(.hidden)
                libraryItem.sharedBackgroundVisibility(.hidden)
            } else {
                searchItem
                libraryItem
            }
        }
    }

    private var searchItem: some ToolbarContent {
        ToolbarItem(placement: .primaryAction) {
            Button {
                nav.searchOpen = true
            } label: {
                Image(systemName: "magnifyingglass")
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(Theme.accent)
                    .accessibilityLabel("Su\u{2019}e")
            }
        }
    }

    private var libraryItem: some ToolbarContent {
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

extension View {
    func libraryToolbar() -> some View {
        modifier(LibraryToolbarModifier())
    }
}
