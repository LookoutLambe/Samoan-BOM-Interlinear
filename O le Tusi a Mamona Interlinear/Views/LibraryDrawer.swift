import SwiftUI

/// The "cheeseburger" drawer: all 15 books listed, each expandable to a grid
/// of chapter bricks. Tapping a chapter jumps the main NavigationStack
/// directly to that chapter view.
struct LibraryDrawer: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(Navigator.self) private var nav
    @State private var expandedBookId: String?

    private let chapterColumns = [GridItem(.adaptive(minimum: 44, maximum: 64), spacing: 8)]

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 0) {
                    drawerHeader
                    LazyVStack(spacing: 0) {
                        ForEach(library.books) { book in
                            bookRow(book)
                            Divider().background(Theme.rule.opacity(0.5))
                        }
                    }
                    .padding(.horizontal, 12)
                    .padding(.bottom, 24)
                }
            }
            .background(Theme.pageBg)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Tapuni") { nav.libraryOpen = false }
                        .tint(Theme.headerBg)
                }
            }
            #if os(iOS)
            .toolbarBackground(Theme.headerBg, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            #endif
        }
    }

    private var drawerHeader: some View {
        VStack(spacing: 4) {
            Text("O le Tusi a Mamona")
                .font(SerifFont.tnr(size: 24, weight: .bold))
                .foregroundStyle(Theme.headerBg)
                .tracking(1.0)
            Text("\u{2767} \u{2767} \u{2767}")
                .font(SerifFont.tnr(size: 15))
                .foregroundStyle(Theme.accent)
                .tracking(6)
                .padding(.top, 2)
        }
        .padding(.top, 12)
        .padding(.bottom, 18)
        .frame(maxWidth: .infinity)
    }

    private func bookRow(_ book: Book) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            Button {
                withAnimation(.snappy(duration: 0.2)) {
                    expandedBookId = expandedBookId == book.id ? nil : book.id
                }
            } label: {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(book.nameSm)
                            .font(SerifFont.tnr(size: 18, weight: .semibold))
                            .foregroundStyle(Theme.ink)
                        Text(book.nameEn)
                            .font(SerifFont.tnr(size: 12, italic: true))
                            .foregroundStyle(Theme.inkLight)
                    }
                    Spacer()
                    Image(systemName: expandedBookId == book.id ? "chevron.up" : "chevron.down")
                        .font(.callout.weight(.semibold))
                        .foregroundStyle(Theme.accent)
                }
                .padding(.vertical, 12)
                .padding(.horizontal, 6)
                .contentShape(Rectangle())
            }
            .buttonStyle(.plain)

            if expandedBookId == book.id {
                LazyVGrid(columns: chapterColumns, spacing: 8) {
                    ForEach(book.chapters) { ch in
                        Button {
                            nav.openChapter(book: book, chapterNum: ch.num)
                        } label: {
                            Text("\(ch.num)")
                                .font(SerifFont.tnr(size: 16, weight: .semibold))
                                .foregroundStyle(Theme.headerBg)
                                .frame(minWidth: 40, minHeight: 40)
                                .background(
                                    RoundedRectangle(cornerRadius: 6, style: .continuous)
                                        .fill(Theme.rowAlt)
                                )
                                .overlay(
                                    RoundedRectangle(cornerRadius: 6, style: .continuous)
                                        .strokeBorder(Theme.accent.opacity(0.5), lineWidth: 1)
                                )
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 6)
                .padding(.bottom, 12)
                .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
    }
}
