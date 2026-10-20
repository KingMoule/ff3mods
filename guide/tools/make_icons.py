"""Génère les icônes de la PWA (nécessite Pillow, uniquement pour cette étape).
Usage : python -I guide/tools/make_icons.py"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons")
os.makedirs(OUT, exist_ok=True)


def icon(size, pad=0.0):
    im = Image.new("RGB", (size, size), (20, 23, 43))
    d = ImageDraw.Draw(im)
    m = int(size * (0.12 + pad))
    # cristal stylisé
    cx = size / 2
    top, bot = m, size - m
    mid = size * 0.38
    pts = [(cx, top), (size - m * 1.5, mid), (cx, bot), (m * 1.5, mid)]
    d.polygon(pts, fill=(96, 176, 255), outline=(210, 235, 255))
    d.polygon([(cx, top), (size - m * 1.5, mid), (cx, mid)], fill=(150, 210, 255))
    d.line([(m * 1.5, mid), (size - m * 1.5, mid)], fill=(210, 235, 255), width=max(2, size // 100))
    d.line([(cx, top), (cx, bot)], fill=(210, 235, 255), width=max(2, size // 100))
    return im


icon(180).save(os.path.join(OUT, "apple-touch-icon.png"))
icon(192).save(os.path.join(OUT, "icon-192.png"))
icon(512).save(os.path.join(OUT, "icon-512.png"))
icon(512, pad=0.08).save(os.path.join(OUT, "icon-maskable-512.png"))
print("icônes écrites dans", os.path.normpath(OUT))
