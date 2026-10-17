#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph social preview for 高性价比人生指南 (how-to-live-better).

Single-file offline reader for the 《高性价比人生指南》 book: every advice item
tagged with cost, benefit, evidence grade (A/B/C), and source links.

Design: clean editorial card matching the site's brand palette
(--brand-1 #3451b2 / --brand-2 #3a5ccc), dark navy gradient background,
white Chinese headline, evidence-grade accent chips, and a subtle
"evidence-based" signal. Original logo: none exists, so the card uses the
brand color + typography only (matches the site itself).

Requires: Pillow + a CJK font (WenQuanYi Zen Hei / Noto Sans CJK).
Usage: python3 make-og-image.py [--out path]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630

# Site brand palette (from index.html :root)
BRAND_1 = (52, 81, 178)      # #3451b2
BRAND_2 = (58, 92, 204)      # #3a5ccc
NAVY_TOP = (28, 34, 62)
NAVY_BOTTOM = (13, 18, 34)
WHITE = (255, 255, 255)
SOFT_BLUE = (168, 190, 240)
GREY = (196, 205, 224)
GOLD = (241, 196, 15)
GREEN = (24, 121, 78)


def find_cjk_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for p in candidates:
        if Path(p).is_file():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def vertical_gradient(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return base.convert("RGBA")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    out_path = Path(args.out).resolve() if args.out else Path("og-image.png").resolve()

    img = vertical_gradient((WIDTH, HEIGHT), NAVY_TOP, NAVY_BOTTOM)
    draw = ImageDraw.Draw(img, "RGBA")

    # Decorative: soft brand glow top-left, subtle ring bottom-right
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy, cr = 180, 160, 320
    for r in range(cr, 0, -8):
        alpha = int(26 * (1 - r / cr))
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BRAND_2 + (alpha,))
    img.alpha_composite(glow)

    # Top accent bar
    draw.rectangle((0, 0, WIDTH, 8), fill=BRAND_2)

    # Small eyebrow
    f_eyebrow = find_cjk_font(34)
    draw.text((80, 96), "高性价比人生指南", font=f_eyebrow, fill=SOFT_BLUE)

    # Headline
    f_head = find_cjk_font(104)
    draw.text((80, 170), "用最少的钱、时间", font=f_head, fill=WHITE)
    draw.text((80, 300), "换回寿命、金钱与自由", font=f_head, fill=WHITE)

    # Sub-line
    f_sub = find_cjk_font(40)
    draw.text((80, 460), "完备的证据等级 · 成本与收益标注 · 原始文献链接", font=f_sub, fill=GREY)

    # Evidence chips
    chip_y = 536
    chip_h = 46
    chips = [("A 级 · 期刊/官方", GREEN), ("B 级 · 综述/专著", BRAND_1), ("C 级 · 参考", (146, 89, 48))]
    x = 80
    for label, color in chips:
        f_chip = find_cjk_font(28)
        bbox = draw.textbbox((0, 0), label, font=f_chip)
        w = bbox[2] - bbox[0] + 48
        draw.rounded_rectangle((x, chip_y, x + w, chip_y + chip_h), radius=23,
                               fill=color + (230,), outline=WHITE + (120,), width=2)
        draw.text((x + 24, chip_y + 9), label, font=f_chip, fill=WHITE)
        x += w + 24

    # Footer
    f_foot = find_cjk_font(26)
    draw.text((80, HEIGHT - 56), "cdyforever.github.io/how-to-live-better", font=f_foot,
              fill=(150, 162, 190))

    img.convert("RGB").save(out_path, optimize=True)
    print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()