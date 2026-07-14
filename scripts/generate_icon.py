#!/usr/bin/env python3
"""Generate the 1024x1024 app icon for the Samoan BoM Interlinear app.
Mirrors the Spanish app's icon style: navy gradient background + gold
Times New Roman text. Writes directly into the Xcode AppIcon.appiconset.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
SAFE_MARGIN = 96   # keep all art within this margin (Apple icon safe area)
NAVY_TOP = (13, 26, 46)      # #0d1a2e
NAVY_BOT = (22, 39, 68)      # #162744
GOLD = (200, 168, 78)        # #c8a84e

FONT_REG    = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
FONT_BOLD   = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"

OUT = (
    Path(__file__).resolve().parent.parent
    / "O le Tusi a Mamona Interlinear"
    / "Assets.xcassets"
    / "AppIcon.appiconset"
    / "AppIcon-1024.png"
)
OUT.parent.mkdir(parents=True, exist_ok=True)


def gradient_bg() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), NAVY_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / (SIZE - 1)
        r = int(NAVY_TOP[0] + (NAVY_BOT[0] - NAVY_TOP[0]) * t)
        g = int(NAVY_TOP[1] + (NAVY_BOT[1] - NAVY_TOP[1]) * t)
        b = int(NAVY_TOP[2] + (NAVY_BOT[2] - NAVY_TOP[2]) * t)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b))
    return img


def measure(draw, text, font, letter_spacing=0):
    if letter_spacing == 0:
        bb = draw.textbbox((0, 0), text, font=font)
        return bb[2] - bb[0], bb[3] - bb[1], bb
    widths = [draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0]
              for ch in text]
    bb_full = draw.textbbox((0, 0), text, font=font)
    return sum(widths) + letter_spacing * (len(text) - 1), bb_full[3] - bb_full[1], bb_full


def draw_centered(draw, text, font, cy, fill, letter_spacing=0):
    """Draw text horizontally centered at SIZE/2, vertically centered on cy."""
    if letter_spacing == 0:
        bb = draw.textbbox((0, 0), text, font=font)
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        x = (SIZE - w) / 2 - bb[0]
        y = cy - h / 2 - bb[1]
        draw.text((x, y), text, font=font, fill=fill)
        return

    widths = []
    bboxes = []
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=font)
        bboxes.append(bb)
        widths.append(bb[2] - bb[0])
    total_w = sum(widths) + letter_spacing * (len(text) - 1)
    bb_full = draw.textbbox((0, 0), text, font=font)
    h = bb_full[3] - bb_full[1]
    x = (SIZE - total_w) / 2
    base_y = cy - h / 2 - bb_full[1]
    for ch, w, bb in zip(text, widths, bboxes):
        draw.text((x - bb[0], base_y), ch, font=font, fill=fill)
        x += w + letter_spacing


def fit_font(draw, text, font_path, max_width, start_size, letter_spacing=0):
    """Largest size at which text fits within max_width."""
    size = start_size
    while size > 20:
        font = ImageFont.truetype(font_path, size)
        w, _, _ = measure(draw, text, font, letter_spacing=letter_spacing)
        if w <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(font_path, size)


def main():
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    avail = SIZE - 2 * SAFE_MARGIN  # 832

    # Top eyebrow — "O LE TUSI A" (Samoan for "The Book of"), small caps tracked
    f_top = fit_font(draw, "O LE TUSI A", FONT_REG, max_width=avail * 0.78,
                     start_size=130, letter_spacing=22)
    # Main word
    f_main = fit_font(draw, "MAMONA", FONT_BOLD, max_width=avail,
                      start_size=240, letter_spacing=4)
    # Subtitle
    f_sub = fit_font(draw, "Interlinear", FONT_ITALIC, max_width=avail * 0.72,
                     start_size=150)

    # Vertical layout — visually centered, with rule between main and subtitle
    eyebrow_cy = SIZE * 0.30
    main_cy    = SIZE * 0.50
    rule_cy    = SIZE * 0.68
    sub_cy     = SIZE * 0.78

    draw_centered(draw, "O LE TUSI A", f_top, eyebrow_cy, GOLD, letter_spacing=22)
    draw_centered(draw, "MAMONA",      f_main, main_cy,   GOLD, letter_spacing=4)

    # Decorative rule between main and subtitle
    rule_w = 320
    rule_h = 3
    draw.rectangle(
        [(SIZE - rule_w) // 2, int(rule_cy), (SIZE + rule_w) // 2, int(rule_cy) + rule_h],
        fill=GOLD,
    )

    draw_centered(draw, "Interlinear", f_sub, sub_cy, GOLD)

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}")

    # Generate Mac sizes (downscaled, high-quality)
    mac_sizes = [16, 32, 64, 128, 256, 512, 1024]
    for px in mac_sizes:
        if px == 1024:
            continue  # already saved
        scaled = img.resize((px, px), Image.LANCZOS)
        path = OUT.parent / f"AppIcon-mac-{px}.png"
        scaled.save(path, "PNG", optimize=True)
        print(f"  + {path.name}")


if __name__ == "__main__":
    main()
