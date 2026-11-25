#!/usr/bin/env python3
"""3 visuels de pub sans prix ni offre precise (Vendredi fou, fin de semaine, Cyber lundi). -> docs/pack-du-jour/pub-bfcm-*.png"""
import json, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
idx = json.load(open(ROOT/"docs/recherche.json")); N = f"{len(idx):,}".replace(",", " ")
PH = [("B0DN45YMP6","JBL"),("B0CHBNXJ24","Ninja"),("B0DLLGG2Z8","Oral-B"),("B0G2SYJSJ4","LEGO"),("B0GT28CSYM","Dyson"),("B0DN1NFKQW","Hot Wheels")]
cards = "".join(f'<div class="c"><img src="{(ROOT/f"docs/img/p/marque-{a}.jpg").resolve().as_uri()}"><div class="n">{n}</div></div>' for a, n in PH)
V = {"vendredi-fou": ("VENDREDI FOU · 27 NOV.", "TRIÉS POUR TOI, À TOUS LES BUDGETS"),
     "fin-de-semaine": ("TOUTE LA FIN DE SEMAINE", "DE NOUVEAUX DEALS CHAQUE JOUR"),
     "cyber-lundi": ("CYBER LUNDI · 30 NOV.", "LES AUBAINES DE NOËL, DÉJÀ TRIÉES")}
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow',Arial Narrow,Arial,sans-serif;font-weight:700;text-align:center;position:relative;overflow:hidden}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}
.c{background:#fff;border-radius:28px;width:320px;height:230px;box-shadow:0 8px 0 #8E0B16;padding:12px}.c img{width:270px;height:160px;object-fit:contain}.n{font-size:32px;color:#3D0A10}
.g{display:grid;grid-template-columns:repeat(3,320px);gap:26px 22px;justify-content:center;margin-top:24px}
.chips{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;padding:0 40px}.chips span{background:#FFF7E8;color:#8E0B16;border-radius:30px;padding:2px 20px;font-size:34px}"""
for key, (k, s) in V.items():
    h = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style><div style="padding-top:28px"><div class="an" style="font-size:56px;color:#FFE4B0;letter-spacing:1px">{k}</div>'
         f'<div class="an" style="font-size:190px;color:#FFC21A;line-height:1;text-shadow:6px 6px 0 #8E0B16">6 000+ DEALS</div>'
         f'<div class="an" style="font-size:54px;color:#fff;line-height:1.1">{s}</div>'
         f'<div class="an" style="font-size:44px;color:#FFC21A;margin-top:8px">JUSQU\'À -70 %</div>'
         f'<div style="width:900px;margin:16px auto 0;background:#fff;border:6px solid #FFC21A;border-radius:60px;padding:12px 34px;font-size:42px;color:#3D0A10;text-align:left">🔎 Tape ton produit ici</div>'
         f'<div class="g">{cards}</div>'
         f'<div class="chips"><span>Maison</span><span>Tech</span><span>Beauté</span><span>Elle</span><span>Lui</span><span>Jouets</span><span>Sport</span><span>Animaux</span><span>Enfants</span></div></div>'
         f'<div style="position:absolute;left:0;right:0;bottom:0;height:140px;background:#3D0A10;color:#fff;padding-top:12px"><div class="an" style="font-size:66px;color:#FFC21A">rabaisflashqc.ca</div><div style="font-size:28px">Les rabais qui valent vraiment le clic</div></div>')
    p = ROOT/f"docs/pack-du-jour/pub-bfcm-{key}.html"; p.write_text(h)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
        pg.screenshot(path=str(ROOT/f"docs/pack-du-jour/pub-bfcm-{key}.png")); b.close()
    p.unlink()
print("ok")
