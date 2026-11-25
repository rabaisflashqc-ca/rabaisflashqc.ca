#!/usr/bin/env python3
"""Visuel de pub unique, generique, du Vendredi fou au Cyber lundi. -> docs/pack-du-jour/pub-bfcm-generique.png"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
PH = ["B0DN45YMP6","B0CHBNXJ24","B0DLLGG2Z8","B0G2SYJSJ4","B0GT28CSYM","B0DN1NFKQW"]
imgs = "".join(f'<div class="c"><img src="{(ROOT/f"docs/img/p/marque-{a}.jpg").resolve().as_uri()}"></div>' for a in PH)
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow',Arial Narrow,Arial,sans-serif;font-weight:700;text-align:center;position:relative;overflow:hidden}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}
.c{background:#fff;border-radius:22px;width:320px;height:150px;box-shadow:0 6px 0 #8E0B16;display:flex;align-items:center;justify-content:center}.c img{max-width:270px;max-height:125px;object-fit:contain}
.row{display:grid;grid-template-columns:repeat(3,320px);gap:18px 22px;justify-content:center;margin-top:26px}"""
h = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style>'
     '<div style="background:#3D0A10;padding:20px 0 14px"><div class="an" style="font-size:78px;color:#FFC21A;letter-spacing:1px">⚡ RABAIS FLASH QC</div></div>'
     '<div class="an" style="font-size:54px;color:#FFE4B0;margin-top:26px;letter-spacing:1px">DU VENDREDI FOU AU CYBER LUNDI</div>'
     '<div class="an" style="font-size:200px;color:#FFC21A;line-height:1;text-shadow:6px 6px 0 #8E0B16;margin-top:4px">6 000+</div>'
     '<div class="an" style="font-size:84px;color:#fff;line-height:1.05">RABAIS TRIÉS ET VALIDÉS</div>'
     '<div style="width:920px;margin:34px auto 0;background:#fff;border:8px solid #FFC21A;border-radius:70px;padding:20px 40px;font-size:54px;color:#3D0A10;text-align:left">🔎 Trouve ton produit ici</div>'
     '<div style="font-size:48px;color:#fff;margin-top:22px">Il est en rabais? <span style="color:#FFC21A">Tu le vois tout de suite.</span></div>'
     f'<div class="row">{imgs}</div>'
     '<div style="position:absolute;left:0;right:0;bottom:0;height:190px;background:#FFC21A;padding-top:10px"><div class="an" style="font-size:92px;color:#3D0A10">rabaisflashqc.ca</div><div style="font-size:34px;color:#3D0A10;margin-top:0">Les rabais qui valent vraiment le clic</div></div>')
p = ROOT/"docs/pack-du-jour/pub-bfcm-generique.html"; p.write_text(h)
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
    pg.screenshot(path=str(ROOT/"docs/pack-du-jour/pub-bfcm-generique.png")); b.close()
p.unlink(); print("ok")
