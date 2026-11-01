#!/usr/bin/env python3
"""Télécharge les photos listées dans suivi/photos_sources.json vers docs/img/p/ASIN.jpg (converties en JPEG 600 px)."""
import json, pathlib, urllib.request, io
from PIL import Image
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs" / "img" / "p"; OUT.mkdir(parents=True, exist_ok=True)
src = json.loads((ROOT / "suivi" / "photos_sources.json").read_text())["sources"]
for stem, url in src.items():
    dest = OUT / f"{stem}.jpg"
    if dest.exists(): continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (RabaisFlashQC photos)"})
        with urllib.request.urlopen(req, timeout=30) as r: data = r.read()
        im = Image.open(io.BytesIO(data))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert("RGB"); im.thumbnail((600, 600)); im.save(dest, "JPEG", quality=85)
        print("ok", stem)
    except Exception as ex: print("échec", stem, ex)
