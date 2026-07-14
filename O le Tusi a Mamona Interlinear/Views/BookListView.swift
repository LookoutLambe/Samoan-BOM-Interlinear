import SwiftUI

struct BookListView: View {
    @Environment(ScriptureLibrary.self) private var library

    private let columns = [
        GridItem(.flexible(), spacing: 24),
        GridItem(.flexible(), spacing: 24),
    ]

    var body: some View {
        ScrollView {
            if let error = library.loadError {
                ContentUnavailableView(
                    "E lē mafai ona uta",
                    systemImage: "exclamationmark.triangle",
                    description: Text(error)
                )
                .padding()
            } else {
                VStack(spacing: 0) {
                    LandingHeader()
                    LazyVGrid(columns: columns, spacing: 32) {
                        ForEach(library.books) { book in
                            NavigationLink(value: book) {
                                BookCard(book: book)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal, 16)
                    .padding(.bottom, 32)
                }
                .frame(maxWidth: 560)
                .frame(maxWidth: .infinity, alignment: .center)
            }
        }
        .background(Theme.pageBg)
        .navigationTitle("O Tusi Pa\u{2019}ia")
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
        .libraryToolbar()
    }
}

// MARK: - Header

private struct LandingHeader: View {
    var body: some View {
        VStack(spacing: 6) {
            Text("O le Tusi a Mamona")
                .font(SerifFont.tnr(size: 32, weight: .bold))
                .foregroundStyle(Theme.headerBg)
                .tracking(1.2)
                .multilineTextAlignment(.center)
            Text("The Book of Mormon")
                .font(SerifFont.tnr(size: 15))
                .foregroundStyle(Theme.inkLight)
                .tracking(1.0)
            Text("\u{2767} \u{2767} \u{2767}")
                .font(SerifFont.tnr(size: 18))
                .foregroundStyle(Theme.accent)
                .tracking(8)
                .padding(.top, 6)
            Text("Samoa ma Faauigaga Faa-Igilisi")
                .font(SerifFont.tnr(size: 13, italic: true))
                .foregroundStyle(Theme.inkLight)
                .padding(.top, 4)
        }
        .padding(.vertical, 24)
        .frame(maxWidth: .infinity)
    }
}

// MARK: - Book card (navy gradient cover + label below)

private struct BookCard: View {
    let book: Book

    var body: some View {
        VStack(spacing: 10) {
            cover
            VStack(spacing: 2) {
                Text(book.nameEn)
                    .font(SerifFont.tnr(size: 13, weight: .semibold))
                    .foregroundStyle(Theme.ink)
                Text(book.nameSm)
                    .font(SerifFont.tnr(size: 12, italic: true))
                    .foregroundStyle(Theme.inkLight)
            }
        }
    }

    private var cover: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 6, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            Color(red: 0.051, green: 0.102, blue: 0.180),
                            Color(red: 0.086, green: 0.153, blue: 0.267),
                        ],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                )
            RoundedRectangle(cornerRadius: 6, style: .continuous)
                .strokeBorder(Color(red: 0.165, green: 0.251, blue: 0.376), lineWidth: 1)

            VStack(spacing: 10) {
                Rectangle()
                    .fill(Theme.accent.opacity(0.55))
                    .frame(height: 1)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 24)
                Text(book.nameSm.uppercased())
                    .font(SerifFont.tnr(size: 17, weight: .semibold))
                    .foregroundStyle(Theme.accent)
                    .tracking(2)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
                    .minimumScaleFactor(0.7)
                    .padding(.horizontal, 8)
                Rectangle()
                    .fill(Theme.accent.opacity(0.55))
                    .frame(height: 1)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 24)
            }
            .padding(.vertical, 18)
        }
        .aspectRatio(3.0 / 4.0, contentMode: .fit)
        .shadow(color: .black.opacity(0.18), radius: 10, x: 0, y: 4)
    }
}
