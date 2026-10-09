# Round the corners, draw a border, and save lossless WebP (README illustrations). Needs Pillow: uvx --from pillow python -I assets/source/finish.py ...
"""Round the corners, draw a border, and save lossless WebP.
usage: finish.py <theme> <dst.webp> <src.png> [crop x,y,w,h]
"""
import sys
from PIL import Image, ImageChops, ImageDraw

theme, dst, src = sys.argv[1:4]
img = Image.open(src).convert("RGB")
if len(sys.argv) > 4:
    x, y, w, h = map(int, sys.argv[4].split(","))
    img = img.crop((x, y, x + w, y + h))
W, H = img.size
R, B, S = 24, 3, 4
line = {"light": (191, 211, 227), "dark": (44, 74, 102)}[theme]


def mask(inset, radius):
    m = Image.new("L", (W * S, H * S), 0)
    ImageDraw.Draw(m).rounded_rectangle(
        (inset * S, inset * S, (W - inset) * S - 1, (H - inset) * S - 1), radius=radius * S, fill=255)
    return m.resize((W, H), Image.LANCZOS)


outer, inner = mask(0, R), mask(B, R - B)
border = ImageChops.subtract(outer, inner)
out = img.convert("RGBA")
out.paste(Image.new("RGBA", (W, H), line + (255,)), (0, 0), border)
out.putalpha(outer)
out.save(dst, "WEBP", lossless=True, method=6)
print(dst, W, H)
