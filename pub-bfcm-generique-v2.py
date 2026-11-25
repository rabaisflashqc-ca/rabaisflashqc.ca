#!/usr/bin/env python3
"""Visuel de pub generique v2 (4:5 et 9:16). -> docs/pack-du-jour/pub-bfcm-generique-v2-{4x5,9x16}.png"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
T = [("🏠","Maison"),("💻","Tech"),("✨","Beauté"),("👗","Elle"),("🧔","Lui"),("🧸","Jouets"),("🏕️","Sport"),("🐶","Animaux"),("👶","Enfants")]
tiles = "".join(f'<div class="t"><span>{e}</span>{n}</div>' for e, n in T)
def page(H, top, bot, gap):
    css = f"""*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1080px;height:{H}px;background:#C1121F;font-family:'Liberation Sans Narrow',Arial Narrow,Arial,sans-serif;font-weight:700;text-align:center;position:relative;overflow:hidden}}
.an{{font-family:Anton,Impact,sans-serif;font-weight:400}}
.g{{display:grid;grid-template-columns:repeat(3,320px);gap:16px 22px;justify-content:center;margin-top:{gap}px}}
.t{{background:#FFF7E8;color:#8E0B16;border-radius:26px;height:92px;font-size:42px;display:flex;align-items:center;justify-content:center;gap:12px;box-shadow:0 6px 0 #8E0B16}}.t span{{font-size:46px}}"""
    return (f'<!doctype html><meta charset=utf-8><style>{css}</style><div style="height:{top}px"></div>'
     '<div style="background:#3D0A10;padding:18px 0 12px"><div class="an" style="font-size:80px;color:#FFC21A;letter-spacing:1px">⚡ RABAIS FLASH QC</div></div>'
     '<div class="an" style="font-size:56px;color:#FFE4B0;margin-top:24px;letter-spacing:1px">DU VENDREDI FOU AU CYBER LUNDI</div>'
     '<div class="an" style="font-size:46px;color:#fff">27 AU 30 NOVEMBRE</div>'
     '<div class="an" style="font-size:176px;color:#FFC21A;line-height:1;text-shadow:6px 6px 0 #8E0B16;margin-top:2px">6 000+</div>'
     '<div class="an" style="font-size:74px;color:#fff;line-height:1.05">RABAIS TRIÉS POUR LE QUÉBEC</div>'
     '<div style="width:920px;margin:22px auto 0;background:#fff;border:8px solid #FFC21A;border-radius:70px;padding:18px 40px;font-size:54px;color:#3D0A10;text-align:left">🔎 Tape ton produit ici</div>'
     '<div style="font-size:46px;color:#fff;margin-top:16px">On te dit <span style="color:#FFC21A">s\'il est en rabais.</span></div>'
     f'<div class="g">{tiles}</div>'
     f'<div style="position:absolute;left:0;right:0;bottom:{bot}px;height:176px;background:#FFC21A;padding-top:6px"><div class="an" style="font-size:88px;color:#3D0A10">rabaisflashqc.ca</div><div style="font-size:34px;color:#3D0A10">Les rabais qui valent vraiment le clic</div></div>')
for name, H, top, bot, gap in (("4x5", 1350, 0, 0, 24), ("9x16", 1920, 190, 250, 40)):
    p = ROOT/f"docs/pack-du-jour/_v2-{name}.html"; p.write_text(page(H, top, bot, gap))
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":H}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
        pg.screenshot(path=str(ROOT/f"docs/pack-du-jour/pub-bfcm-generique-v2-{name}.png")); b.close()
    p.unlink()
print("ok")
