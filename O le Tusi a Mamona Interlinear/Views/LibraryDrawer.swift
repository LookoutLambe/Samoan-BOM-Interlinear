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
                        let front = library.frontMatter()
                        if !front.isEmpty {
                            sectionLabel("Faatomuaga · Front Matter")
                            ForEach(front) { section in
                                frontMatterRow(section)
                                Divider().background(Theme.rule.opacity(0.5))
                            }
                            sectionLabel("Tusi · Books")
                        }
                        ForEach(library.books) { book in
                            bookRow(book)
                            Divider().background(Theme.rule.opacity(0.5))
                        }
                    }
                    .padding(.horizontal, 12)

                    privacyLink
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

    /// A reachable-in-app link to the hosted privacy policy — App Store
    /// reviewers like to see it available inside the app, not only in metadata.
    private var privacyLink: some View {
        Link(destination: URL(string: "https://lookoutlambe.github.io/tusi-a-mamona-privacy/")!) {
            HStack(spacing: 6) {
                Image(systemName: "lock.shield")
                    .font(.footnote.weight(.semibold))
                Text("Faiga fa\u{2019}alilolilo \u{00B7} Privacy Policy")
                    .font(SerifFont.tnr(size: 13))
            }
            .foregroundStyle(Theme.accent)
            .frame(maxWidth: .infinity, alignment: .center)
            .padding(.top, 20)
            .padding(.bottom, 4)
            .contentShape(Rectangle())
        }
    }

    private func sectionLabel(_ text: String) -> some View {
        Text(text)
            .font(SerifFont.tnr(size: 12, weight: .semibold))
            .foregroundStyle(Theme.accent)
            .tracking(1.2)
            .textCase(.uppercase)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 6)
            .padding(.top, 16)
            .padding(.bottom, 6)
    }

    private func frontMatterRow(_ section: FrontMatterSection) -> some View {
        Button {
            nav.openFrontMatter(id: section.id)
        } label: {
            VStack(alignment: .leading, spacing: 2) {
                Text(section.titleSm)
                    .font(SerifFont.tnr(size: 17, weight: .semibold))
                    .foregroundStyle(Theme.ink)
                Text(section.titleEn)
                    .font(SerifFont.tnr(size: 12, italic: true))
                    .foregroundStyle(Theme.inkLight)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.vertical, 12)
            .padding(.horizontal, 6)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
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
