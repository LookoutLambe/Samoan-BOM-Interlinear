import SwiftUI

/// Color & font palette pulled from the Spanish-app sibling, which in turn
/// mirrors the Hebrew "Sefer Mormon" app's CSS root vars: brighter gold
/// (`#dbb958`) and dark-navy chrome (`#1e2233`).
enum Theme {
    // Backgrounds
    static let pageBg     = Color(red: 0.980, green: 0.973, blue: 0.949)   // #faf8f2
    static let pageBgDeep = Color(red: 0.941, green: 0.925, blue: 0.878)   // #f0ece0
    static let rowAlt     = Color(red: 0.992, green: 0.973, blue: 0.922)   // #fdf8eb

    // Inks
    static let ink      = Color(red: 0.102, green: 0.102, blue: 0.102)     // #1a1a1a
    static let inkLight = Color(red: 0.267, green: 0.267, blue: 0.267)     // #444

    // Interlinear
    static let hwInk    = Color(red: 0.102, green: 0.153, blue: 0.267)     // #1a2744 — Samoan word
    static let glossInk = Color(red: 0.353, green: 0.416, blue: 0.541)     // #5a6a8a — English gloss

    // Accents and rules
    static let accent      = Color(red: 0.859, green: 0.725, blue: 0.345)  // #dbb958 — Hebrew-app gold
    static let accentLight = Color(red: 0.910, green: 0.800, blue: 0.471)  // #e8cc78
    static let rule        = Color(red: 0.839, green: 0.808, blue: 0.722)  // #d6ceb8
    static let ruleLight   = Color(red: 0.910, green: 0.886, blue: 0.831)  // #e8e2d4
    static let verseNum    = Color(red: 0.498, green: 0.702, blue: 0.827)  // #7fb3d3

    // Chrome (top/bottom bars)
    static let headerBg     = Color(red: 0.118, green: 0.133, blue: 0.200) // #1e2233
    static let headerHover  = Color(red: 0.165, green: 0.184, blue: 0.267) // #2a2f44
    static let headerText   = Color(red: 0.859, green: 0.725, blue: 0.345) // #dbb958
    static let buttonBorder = Color(red: 0.227, green: 0.247, blue: 0.333) // #3a3f55
}

/// Times New Roman with graceful fallback to the system serif design.
enum SerifFont {
    static func tnr(size: CGFloat, weight: Font.Weight = .regular, italic: Bool = false) -> Font {
        var f = Font.custom("TimesNewRomanPSMT", size: size).weight(weight)
        if italic { f = Font.custom("TimesNewRomanPS-ItalicMT", size: size).weight(weight) }
        return f
    }
}
