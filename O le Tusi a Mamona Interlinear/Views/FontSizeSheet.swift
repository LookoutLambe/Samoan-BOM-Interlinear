import SwiftUI

/// Reader font-size adjuster: slider with a live word-unit preview.
struct FontSizeSheet: View {
    @Environment(AppSettings.self) private var settings
    @Environment(\.dismiss) private var dismiss

    private let range: ClosedRange<Double> = 0.75...1.75
    private let step: Double = 0.05

    var body: some View {
        @Bindable var settings = settings
        NavigationStack {
            VStack(spacing: 24) {
                Text("Lapo\u{2019}a o le Tusitusiga")
                    .font(SerifFont.tnr(size: 18, weight: .semibold))
                    .foregroundStyle(Theme.headerBg)
                    .padding(.top, 8)

                VStack(spacing: 8) {
                    FlowLayout(horizontalSpacing: 6, verticalSpacing: 6) {
                        SampleWordUnit(sm: "O", en: "·")
                        SampleWordUnit(sm: "a\u{2019}u,", en: "I")
                        SampleWordUnit(sm: "o", en: "·")
                        SampleWordUnit(sm: "Nifae,", en: "Nephi")
                        SampleWordUnit(sm: "na", en: "·")
                        SampleWordUnit(sm: "fanaua", en: "was born")
                    }
                    .environment(\.scriptureFontScale, settings.fontScale)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding(.vertical, 18)
                    .padding(.horizontal, 12)
                    .background(
                        RoundedRectangle(cornerRadius: 14, style: .continuous)
                            .fill(Theme.rowAlt)
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 14, style: .continuous)
                            .strokeBorder(Theme.rule, lineWidth: 1)
                    )
                }
                .padding(.horizontal, 16)

                HStack(spacing: 14) {
                    Button {
                        settings.fontScale = max(range.lowerBound, settings.fontScale - step)
                    } label: {
                        Text("A")
                            .font(SerifFont.tnr(size: 14, weight: .semibold))
                            .foregroundStyle(Theme.headerBg)
                            .frame(width: 28, height: 28)
                    }
                    .buttonStyle(.plain)

                    Slider(value: $settings.fontScale, in: range, step: step)
                        .tint(Theme.accent)

                    Button {
                        settings.fontScale = min(range.upperBound, settings.fontScale + step)
                    } label: {
                        Text("A")
                            .font(SerifFont.tnr(size: 26, weight: .semibold))
                            .foregroundStyle(Theme.headerBg)
                            .frame(width: 36, height: 36)
                    }
                    .buttonStyle(.plain)
                }
                .padding(.horizontal, 16)

                Text("\(Int((settings.fontScale * 100).rounded()))%")
                    .font(SerifFont.tnr(size: 14, italic: true))
                    .foregroundStyle(Theme.inkLight)

                Button("Toe Faafoi") { settings.fontScale = 1.0 }
                    .font(SerifFont.tnr(size: 15))
                    .foregroundStyle(Theme.accent)

                Spacer(minLength: 0)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(Theme.pageBg)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Ua Mae\u{2019}a") { dismiss() }
                        .tint(Theme.headerBg)
                }
            }
        }
        .presentationDetents([.medium])
        .presentationDragIndicator(.visible)
    }
}

/// A non-interactive interlinear word-unit used only for the font-size preview.
private struct SampleWordUnit: View {
    @Environment(\.scriptureFontScale) private var scale
    let sm: String
    let en: String

    var body: some View {
        VStack(alignment: .center, spacing: 2) {
            Text(sm)
                .font(SerifFont.tnr(size: 22 * scale, weight: .medium))
                .foregroundStyle(Theme.hwInk)
            if !en.isEmpty {
                Text(en)
                    .font(SerifFont.tnr(size: 12 * scale, italic: true))
                    .foregroundStyle(Theme.glossInk)
            }
        }
        .padding(.horizontal, 4)
        .padding(.vertical, 2)
    }
}
