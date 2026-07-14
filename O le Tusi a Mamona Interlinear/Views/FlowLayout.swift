import SwiftUI

/// Arranges subviews left-to-right, wrapping to the next row when the
/// container's width is exceeded. Each row is sized to the tallest subview
/// in that row, so stacked word-units (Samoan over English gloss) stay
/// vertically aligned.
///
/// Subviews are measured with the container width as the proposal so that
/// nested wrapping layouts (e.g. an `IdiomSpanView` whose Samoan tokens are
/// themselves in a `FlowLayout`) can break onto multiple lines at large font
/// scales instead of overflowing.
struct FlowLayout: Layout {
    var horizontalSpacing: CGFloat = 6
    var verticalSpacing: CGFloat = 4

    struct Cache {
        var rows: [[Int]] = []
        var rowHeights: [CGFloat] = []
        var subviewSizes: [CGSize] = []
        var totalSize: CGSize = .zero
        var widthMeasured: CGFloat = -1
    }

    func makeCache(subviews: Subviews) -> Cache { Cache() }

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache) -> CGSize {
        let width = proposal.width ?? .infinity
        layoutRows(width: width, subviews: subviews, cache: &cache)
        return cache.totalSize
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache) {
        layoutRows(width: bounds.width, subviews: subviews, cache: &cache)
        var y = bounds.minY
        for (rowIdx, indices) in cache.rows.enumerated() {
            var x = bounds.minX
            let rowHeight = cache.rowHeights[rowIdx]
            for i in indices {
                let size = cache.subviewSizes[i]
                subviews[i].place(
                    at: CGPoint(x: x, y: y),
                    anchor: .topLeading,
                    proposal: ProposedViewSize(width: size.width, height: size.height)
                )
                x += size.width + horizontalSpacing
            }
            y += rowHeight + verticalSpacing
        }
    }

    private func layoutRows(width: CGFloat, subviews: Subviews, cache: inout Cache) {
        if cache.widthMeasured == width && !cache.rows.isEmpty { return }
        cache.rows.removeAll(keepingCapacity: true)
        cache.rowHeights.removeAll(keepingCapacity: true)
        cache.subviewSizes.removeAll(keepingCapacity: true)

        // Two-pass measurement: first ask each subview for its natural size at
        // unspecified width. If that natural size overflows the container, only
        // then re-measure constrained so wrap-capable subviews (Text with
        // `.fixedSize(horizontal: false)`) can break onto multiple lines.
        // This keeps short word-units at their compact natural width.
        for sub in subviews {
            var size = sub.sizeThatFits(.unspecified)
            if width.isFinite, size.width > width {
                size = sub.sizeThatFits(ProposedViewSize(width: width, height: nil))
            }
            cache.subviewSizes.append(size)
        }

        var currentRow: [Int] = []
        var currentRowWidth: CGFloat = 0
        var currentRowHeight: CGFloat = 0
        var maxRowWidth: CGFloat = 0

        for idx in subviews.indices {
            let size = cache.subviewSizes[idx]
            let needsSpace = currentRow.isEmpty ? size.width : (currentRowWidth + horizontalSpacing + size.width)
            if !currentRow.isEmpty && needsSpace > width {
                cache.rows.append(currentRow)
                cache.rowHeights.append(currentRowHeight)
                maxRowWidth = max(maxRowWidth, currentRowWidth)
                currentRow = [idx]
                currentRowWidth = size.width
                currentRowHeight = size.height
            } else {
                if !currentRow.isEmpty { currentRowWidth += horizontalSpacing }
                currentRow.append(idx)
                currentRowWidth += size.width
                currentRowHeight = max(currentRowHeight, size.height)
            }
        }
        if !currentRow.isEmpty {
            cache.rows.append(currentRow)
            cache.rowHeights.append(currentRowHeight)
            maxRowWidth = max(maxRowWidth, currentRowWidth)
        }

        let totalHeight = cache.rowHeights.reduce(0, +)
            + CGFloat(max(0, cache.rowHeights.count - 1)) * verticalSpacing
        cache.totalSize = CGSize(width: maxRowWidth, height: totalHeight)
        cache.widthMeasured = width
    }
}
