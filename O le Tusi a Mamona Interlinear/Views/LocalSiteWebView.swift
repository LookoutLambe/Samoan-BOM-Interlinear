import SwiftUI
import WebKit

/// THE APP MIRRORS THE WEBSITE (2026-09-08).
///
/// The user: *"i just want it to mirror the website"*. It could not, because
/// it was a second reader: `docs/app.js` drew one layout for the web and the
/// SwiftUI views drew another for the phone, so every change had to be made
/// twice and the two drifted between makings. The Hebrew app has never had
/// that problem — it is a `WKWebView` over a bundled copy of its own site, so
/// its phone layout *is* its web layout.
///
/// This is that, for `docs/`. The target bundles `docs/` itself as a folder
/// reference, so what runs here is the very same HTML, CSS and JavaScript that
/// samoanbominterlinear.org serves. There is one reader now.
///
/// Why a scheme handler rather than `loadFileURL`, which is all the Hebrew app
/// needs: that reader loads its data by injecting `<script>` tags, which a
/// `file://` page may do. This one calls `fetch('data/…json')`, and a `file://`
/// page has an opaque origin — every fetch would fail and `localStorage`, where
/// the highlights, notes and per-volume bookmarks live, would be unreliable.
/// Serving the same bundled files over a registered custom scheme gives the
/// page a real, stable origin, so fetch and storage behave as they do on the web.
private let siteScheme = "tusi"
private let siteHost = "local"

struct LocalSiteWebView: UIViewRepresentable {
    /// The bundled copy of `docs/` — the site.
    let wwwDirectoryURL: URL

    func makeCoordinator() -> Coordinator { Coordinator(root: wwwDirectoryURL) }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.defaultWebpagePreferences.preferredContentMode = .mobile
        config.setURLSchemeHandler(context.coordinator, forURLScheme: siteScheme)

        // A double-tap on a word must open its card, not zoom the page out
        // from under the tap that opened it.
        config.userContentController.addUserScript(WKUserScript(
            source: "document.documentElement.style.touchAction = 'manipulation';",
            injectionTime: .atDocumentStart,
            forMainFrameOnly: false))

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.isOpaque = true
        webView.backgroundColor = .clear
        webView.scrollView.backgroundColor = .clear
        // The page's own CSS pads for the notch and the home indicator with
        // env(safe-area-inset-*) under viewport-fit=cover, so neither SwiftUI
        // nor the scroll view may inset it again.
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        webView.scrollView.minimumZoomScale = 1.0
        webView.scrollView.maximumZoomScale = 1.0
        webView.allowsBackForwardNavigationGestures = true

        var start = URLComponents()
        start.scheme = siteScheme
        start.host = siteHost
        start.path = "/index.html"
        if let url = start.url {
            webView.load(URLRequest(url: url))
        }
        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {}

    /// Serves the bundled site over `tusi://local/…`.
    final class Coordinator: NSObject, WKURLSchemeHandler, WKNavigationDelegate {
        private let root: URL

        init(root: URL) {
            // Resolved once: every request is checked against it, so a crafted
            // path cannot escape the bundle.
            self.root = root.standardizedFileURL
        }

        func webView(_ webView: WKWebView, start task: WKURLSchemeTask) {
            // Answered synchronously. The files are local, and a task that has
            // already been stopped can then never be written to afterwards —
            // which is the one way this API crashes.
            guard let url = task.request.url else {
                task.didFailWithError(URLError(.badURL))
                return
            }
            var path = url.path
            if path.isEmpty || path == "/" { path = "/index.html" }
            let file = root.appendingPathComponent(String(path.dropFirst())).standardizedFileURL
            guard file.path == root.path || file.path.hasPrefix(root.path + "/"),
                  let data = try? Data(contentsOf: file, options: .mappedIfSafe) else {
                task.didFailWithError(URLError(.fileDoesNotExist))
                return
            }
            // AN HTTP RESPONSE, NOT A BARE ONE. `fetch()` reads `status` off
            // the response, and a plain `URLResponse` carries none: every
            // `res.ok` came back false and the reader reported that it could
            // not find the book, with the shell around it drawn perfectly.
            let response = HTTPURLResponse(
                url: url,
                statusCode: 200,
                httpVersion: "HTTP/1.1",
                headerFields: [
                    "Content-Type": Self.mimeType(for: file.pathExtension),
                    "Content-Length": String(data.count),
                    "Access-Control-Allow-Origin": "*",
                ]
            ) ?? URLResponse(url: url,
                             mimeType: Self.mimeType(for: file.pathExtension),
                             expectedContentLength: data.count,
                             textEncodingName: "utf-8")
            task.didReceive(response)
            task.didReceive(data)
            task.didFinish()
        }

        func webView(_ webView: WKWebView, stop task: WKURLSchemeTask) {}

        /// The App Store link, the privacy policy and anything else off the
        /// bundle open in Safari rather than replacing the reader.
        func webView(_ webView: WKWebView,
                     decidePolicyFor navigationAction: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            if let url = navigationAction.request.url,
               url.scheme != siteScheme,
               navigationAction.navigationType == .linkActivated {
                UIApplication.shared.open(url)
                decisionHandler(.cancel)
                return
            }
            decisionHandler(.allow)
        }

        private static func mimeType(for ext: String) -> String {
            switch ext.lowercased() {
            case "html", "htm":  return "text/html"
            case "js", "mjs":    return "text/javascript"
            case "css":          return "text/css"
            case "json":         return "application/json"
            case "webmanifest":  return "application/manifest+json"
            case "svg":          return "image/svg+xml"
            case "png":          return "image/png"
            case "jpg", "jpeg":  return "image/jpeg"
            case "ico":          return "image/x-icon"
            case "woff2":        return "font/woff2"
            case "woff":         return "font/woff"
            case "ttf":          return "font/ttf"
            case "txt", "md":    return "text/plain"
            default:             return "application/octet-stream"
            }
        }
    }
}
