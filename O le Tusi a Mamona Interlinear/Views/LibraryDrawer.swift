import SwiftUI

/// The "cheeseburger" drawer: every book of every volume listed — the Book of
/// Mormon, D&C and Pearl of Great Price, then O le Tusi Paia's Old and New
/// Testament — each expandable to a grid of chapter bricks. Tapping a chapter
/// jumps the main NavigationStack directly to that chapter view. Bible rows
/// are drawn from the index, so no Bible book is decoded until it is opened.
struct LibraryDrawer: View {
    @Environment(ScriptureLibrary.self) private var library
    @Environment(Navigator.self) private var nav
    @State private var expandedBookId: String?

    private let chapterColumns = [GridItem(.adaptive(minimum: 44, maximum: 64), spacing: 8)]

    // The panel's chrome — its title, its close button and its edge — belongs
    // to SideDrawer, which states it once for every panel in the app. What is
    // left here is the library itself.
    var body: some View {
        ScrollViewReader { proxy in
                ScrollView {
                    VStack(spacing: 0) {
                        LazyVStack(spacing: 0) {
                            let front = library.frontMatter()
                            if !front.isEmpty {
                                sectionLabel("Faatomuaga · Front Matter")
                                ForEach(front) { section in
                                    frontMatterRow(section)
                                    Divider().background(Theme.rule.opacity(0.5))
                                }
                            }
                            // Grouped by volume, each section anchored so a landing
                            // card can open the drawer at its own books.
                            ForEach(library.allVolumes) { volume in
                                sectionLabel("\(volume.nameSm) \u{00B7} \(volume.nameEn)")
                                    .id("vol-\(volume.id)")
                                ForEach(library.books(in: volume.id)) { book in
                                    bookRow(id: book.id, nameSm: book.nameSm, nameEn: book.nameEn,
                                            chapterNums: book.chapters.map(\.num))
                                    Divider().background(Theme.rule.opacity(0.5))
                                }
                                ForEach(library.bibleBooks(in: volume.id)) { meta in
                                    bookRow(id: meta.id, nameSm: meta.nameSm, nameEn: meta.nameEn,
                                            chapterNums: Array(1...max(meta.chapters, 1)))
                                    Divider().background(Theme.rule.opacity(0.5))
                                }
                            }
                        }
                        .padding(.horizontal, 12)

                        privacyLink
                            .padding(.bottom, 24)
                    }
                }
                .onAppear {
                    if let volume = nav.libraryFocusVolume {
                        proxy.scrollTo("vol-\(volume)", anchor: .top)
                        nav.libraryFocusVolume = nil
                    }
                }
            }
        .background(Theme.pageBg)
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

    /// One book row: its two names, and when expanded a grid of chapter bricks.
    /// Takes plain values rather than a `Book` so a Bible book can be listed from
    /// its index entry without decoding its text.
    private func bookRow(id: String, nameSm: String, nameEn: String, chapterNums: [Int]) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            Button {
                withAnimation(.snappy(duration: 0.2)) {
                    expandedBookId = expandedBookId == id ? nil : id
                }
            } label: {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(nameSm)
                            .font(SerifFont.tnr(size: 18, weight: .semibold))
                            .foregroundStyle(Theme.ink)
                        Text(nameEn)
                            .font(SerifFont.tnr(size: 12, italic: true))
                            .foregroundStyle(Theme.inkLight)
                    }
                    Spacer()
                    Image(systemName: expandedBookId == id ? "chevron.up" : "chevron.down")
                        .font(.callout.weight(.semibold))
                        .foregroundStyle(Theme.accent)
                }
                .padding(.vertical, 12)
                .padding(.horizontal, 6)
                .contentShape(Rectangle())
            }
            .buttonStyle(.plain)

            if expandedBookId == id {
                LazyVGrid(columns: chapterColumns, spacing: 8) {
                    ForEach(chapterNums, id: \.self) { num in
                        Button {
                            nav.openChapter(ChapterRef(bookId: id, chapterNum: num))
                        } label: {
                            Text("\(num)")
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
