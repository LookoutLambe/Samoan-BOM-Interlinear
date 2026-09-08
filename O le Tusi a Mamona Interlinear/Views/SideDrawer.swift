import SwiftUI

/// THE DRAWER CONTRACT — stated once, here, and nowhere else.
///
/// The Hebrew reader states it once in `nav_engine.css`: a side panel is a
/// full-height overlay pinned to one edge, closed by transform and opened to
/// `translateX(0)` over 0.28s, behind a half-black scrim; on a phone it is
/// 90vw, on a wide screen 360px. This is that panel for SwiftUI.
///
/// It replaces `.sheet`, which is the wrong shape for a library: a sheet is a
/// bottom card, inset from the top, with the page it came from still showing
/// behind it — nothing like the panel the same library is on the web.
struct SideDrawerModifier<Panel: View>: ViewModifier {
    @Binding var isOpen: Bool
    let edge: Edge
    let title: String
    @ViewBuilder var panel: () -> Panel

    /// How far the panel has been dragged toward its closed position.
    @State private var drag: CGFloat = 0

    /// The Hebrew's two widths: 90vw on a phone, 360 where there is room.
    private func width(for container: CGFloat) -> CGFloat {
        min(container * 0.9, 360)
    }

    private var alignment: Alignment { edge == .leading ? .leading : .trailing }

    func body(content: Content) -> some View {
        content.overlay {
            ZStack(alignment: alignment) {
                if isOpen {
                    // The scrim dims the reader and is itself the way out —
                    // tapping beside a drawer closes it on every platform.
                    Color.black.opacity(0.5)
                        .ignoresSafeArea()
                        .transition(.opacity)
                        .onTapGesture { isOpen = false }
                        .accessibilityLabel("Tapuni le faletusi \u{00B7} Close the library")
                        .accessibilityAddTraits(.isButton)

                    drawer
                        .transition(.move(edge: edge))
                }
            }
            .animation(.timingCurve(0.4, 0, 0.2, 1, duration: 0.28), value: isOpen)
        }
    }

    private var drawer: some View {
        VStack(spacing: 0) {
            header
            panel()
        }
        // The content keeps clear of the notch and the home indicator; only
        // the panel's own surface runs to the edges of the screen.
        .frame(maxHeight: .infinity, alignment: .top)
        .containerRelativeFrame(.horizontal) { length, _ in width(for: length) }
        .background(Theme.pageBg.ignoresSafeArea())
        .overlay(alignment: edge == .leading ? .trailing : .leading) {
            Rectangle()
                .fill(Theme.rule)
                .frame(width: 1)
                .ignoresSafeArea()
        }
        .offset(x: drag)
        .gesture(
            // A drawer that cannot be swiped away does not feel like a drawer.
            DragGesture(minimumDistance: 12)
                .onChanged { value in
                    let d = value.translation.width
                    drag = edge == .leading ? min(0, d) : max(0, d)
                }
                .onEnded { value in
                    let d = value.translation.width
                    let past = edge == .leading ? d < -60 : d > 60
                    withAnimation(.timingCurve(0.4, 0, 0.2, 1, duration: 0.28)) {
                        drag = 0
                        if past { isOpen = false }
                    }
                }
        )
    }

    /// Title on the reading side, a 44pt close target on the outside — the
    /// Hebrew drawer's own header, which the sheet's navigation bar was
    /// standing in for.
    private var header: some View {
        HStack(spacing: 8) {
            Text(title)
                .font(SerifFont.tnr(size: 17, weight: .semibold))
                .foregroundStyle(Theme.headerText)
                .lineLimit(1)
                .minimumScaleFactor(0.8)
            Spacer(minLength: 8)
            Button {
                isOpen = false
            } label: {
                Image(systemName: "xmark")
                    .font(.body.weight(.semibold))
                    .foregroundStyle(Theme.accent)
                    .frame(width: 44, height: 44)          // iOS touch minimum
                    .contentShape(Rectangle())
            }
            .accessibilityLabel("Tapuni \u{00B7} Close")
        }
        .padding(.leading, 16)
        .padding(.trailing, 2)
        .frame(height: 52)
        .background(Theme.headerBg)
    }
}

extension View {
    /// Present `panel` as a full-height side drawer. See `SideDrawerModifier`.
    func sideDrawer<Panel: View>(isOpen: Binding<Bool>,
                                 edge: Edge = .leading,
                                 title: String,
                                 @ViewBuilder panel: @escaping () -> Panel) -> some View {
        modifier(SideDrawerModifier(isOpen: isOpen, edge: edge, title: title, panel: panel))
    }
}
