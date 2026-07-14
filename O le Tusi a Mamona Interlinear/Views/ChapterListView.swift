import SwiftUI

struct ChapterListView: View {
    let book: Book

    private let columns = [GridItem(.adaptive(minimum: 60, maximum: 80), spacing: 10)]

    var body: some View {
        ScrollView {
            VStack(spacing: 0) {
                ChapterListHeader(book: book)

                LazyVGrid(columns: columns, spacing: 10) {
                    ForEach(book.chapters) { chapter in
                        NavigationLink(value: ChapterRef(bookId: book.id, chapterNum: chapter.num)) {
                            ChapterBrick(num: chapter.num)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 24)
                .padding(.bottom, 40)
            }
            .frame(maxWidth: 800)
            .frame(maxWidth: .infinity, alignment: .center)
        }
        .background(Theme.pageBg)
        .navigationTitle(book.nameEn)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
        .libraryToolbar()
    }
}

private struct ChapterListHeader: View {
    let book: Book

    var body: some View {
        VStack(spacing: 6) {
            Text(book.nameSm)
                .font(SerifFont.tnr(size: 32, weight: .bold))
                .foregroundStyle(Theme.headerBg)
                .tracking(1.2)
                .multilineTextAlignment(.center)
            Text(book.nameEn)
                .font(SerifFont.tnr(size: 15))
                .foregroundStyle(Theme.inkLight)
                .tracking(1.0)
            Text("\u{2767} \u{2767} \u{2767}")
                .font(SerifFont.tnr(size: 18))
                .foregroundStyle(Theme.accent)
                .tracking(8)
                .padding(.top, 6)
            Text("Mataupu · Chapters")
                .font(SerifFont.tnr(size: 13, italic: true))
                .foregroundStyle(Theme.inkLight)
                .tracking(1.2)
                .padding(.top, 4)
            Rectangle()
                .fill(Theme.rule)
                .frame(height: 2)
                .padding(.horizontal, 24)
                .padding(.top, 14)
        }
        .padding(.vertical, 24)
        .frame(maxWidth: .infinity)
    }
}

private struct ChapterBrick: View {
    let num: Int

    var body: some View {
        Text("\(num)")
            .font(SerifFont.tnr(size: 20, weight: .semibold))
            .foregroundStyle(Theme.headerBg)
            .frame(minWidth: 56, minHeight: 56)
            .padding(6)
            .background(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(Theme.rowAlt)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .strokeBorder(Theme.accent.opacity(0.5), lineWidth: 1)
            )
    }
}
