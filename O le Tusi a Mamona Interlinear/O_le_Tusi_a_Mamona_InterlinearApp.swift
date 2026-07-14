import SwiftUI

@main
struct O_le_Tusi_a_Mamona_InterlinearApp: App {
    @State private var library = ScriptureLibrary()
    @State private var navigator = Navigator()
    @State private var settings = AppSettings()
    @State private var highlights = HighlightStore()
    @State private var notes = NoteStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(library)
                .environment(navigator)
                .environment(settings)
                .environment(highlights)
                .environment(notes)
        }
    }
}
