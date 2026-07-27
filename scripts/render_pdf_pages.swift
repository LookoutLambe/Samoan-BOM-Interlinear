// Render specific pages of a PDF to PNG using PDFKit.
// usage: swift render_pdf_pages.swift <pdf> <outdir> <page1> <page2> ...
import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
guard args.count >= 4, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    FileHandle.standardError.write("bad args or pdf\n".data(using: .utf8)!)
    exit(1)
}
let outdir = args[2]
let scale: CGFloat = 4.0
for s in args[3...] {
    guard let p = Int(s), let page = doc.page(at: p - 1) else { continue }
    let r = page.bounds(for: .mediaBox)
    let size = NSSize(width: r.width * scale, height: r.height * scale)
    let img = page.thumbnail(of: size, for: .mediaBox)
    guard let tiff = img.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let png = rep.representation(using: .png, properties: [:]) else { continue }
    let out = "\(outdir)/page-\(p).png"
    try? png.write(to: URL(fileURLWithPath: out))
    print(out)
}
