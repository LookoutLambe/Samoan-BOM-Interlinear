import SwiftUI

extension EnvironmentValues {
    /// Multiplier applied to interlinear typography in the chapter reader.
    /// Injected at the ChapterView root from `AppSettings.fontScale`.
    @Entry var scriptureFontScale: Double = 1.0
}
