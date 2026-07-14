import SwiftUI

/// Per-verse note editor. Saves on Done; deletes on empty text.
struct NoteEditorSheet: View {
    @Environment(NoteStore.self) private var notes
    @Environment(\.dismiss) private var dismiss

    let verseKey: String
    let referenceLabel: String   // e.g. "1 Nifae 1:1"
    let samoanPreview: String

    @State private var text: String = ""

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 12) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(referenceLabel)
                        .font(SerifFont.tnr(size: 17, weight: .semibold))
                        .foregroundStyle(Theme.headerBg)
                    Text(samoanPreview)
                        .font(SerifFont.tnr(size: 14, italic: true))
                        .foregroundStyle(Theme.inkLight)
                        .lineLimit(3)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal, 4)

                Divider().background(Theme.rule)

                TextEditor(text: $text)
                    .font(SerifFont.tnr(size: 17))
                    .foregroundStyle(Theme.ink)
                    .scrollContentBackground(.hidden)
                    .background(Theme.rowAlt)
                    .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                    .overlay(
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .strokeBorder(Theme.rule, lineWidth: 1)
                    )
                    .frame(minHeight: 160)

                if !text.isEmpty {
                    Button(role: .destructive) {
                        notes.deleteNote(for: verseKey)
                        dismiss()
                    } label: {
                        Label("Tapeina le Manatu", systemImage: "trash")
                    }
                    .padding(.top, 4)
                }

                Spacer(minLength: 0)
            }
            .padding(16)
            .background(Theme.pageBg)
            .navigationTitle("Manatu")
            #if os(iOS)
            .navigationBarTitleDisplayMode(.inline)
            #endif
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Faaleaoga") { dismiss() }
                        .tint(Theme.inkLight)
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Ua Mae\u{2019}a") {
                        notes.setNote(text, for: verseKey)
                        dismiss()
                    }
                    .tint(Theme.headerBg)
                    .fontWeight(.semibold)
                }
            }
        }
        .presentationDetents([.medium, .large])
        .onAppear {
            text = notes.note(for: verseKey) ?? ""
        }
    }
}
