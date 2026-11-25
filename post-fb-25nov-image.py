#!/usr/bin/env python3
"""Image FB 25 nov : 9 produits de themes differents. -> docs/pack-du-jour/fb-25nov-60-rabais.png"""
import json, pathlib, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
deals = {d["asin"]: d for d in json.load(open(ROOT / "suivi/deals_chrome.json"))}
e = H.escape
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"
EX = [("B0DN45YMP6","JBL","Vibe Beam 2"),("B0CHBNXJ24","Ninja","CREAMi XL"),("B0DLLGG2Z8","Oral-B","iO2"),
      ("B0G2SYJSJ4","LEGO","Stitch"),("B0GT28CSYM","Dyson","V8 Cyclone"),("B0DN1NFKQW","Hot Wheels","Mario Kart"),
      ("B0764BZBQW","Magic Bullet","Mélangeur"),("B0BWWZP49F","Blink","Mini 2"),("B08DJ8Z3WH","Shark","Navigator Pro")]
cards = ""
for i, (a, b, t) in enumerate(EX, 1):
    d = deals[a]; img = (ROOT / f"docs/img/p/marque-{a}.jpg").resolve().as_uri()
    cards += (f'<div class="c"><div class="p"><img src="{img}"><span class="b">-{d["pct"]} %</span></div>'
              f'<div class="t">{e(b)} · {e(t)}</div><div class="pr">{money(d["price"])}</div></div>')
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;color:#1A1A1A;overflow:hidden}
.top{text-align:center;padding:20px 30px 0}.top .k{font-size:40px;color:#fff;letter-spacing:2px}
.top .h{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:90px;line-height:.95;color:#FFC21A;text-shadow:6px 6px 0 #8E0B16}
.top .s{font-size:46px;color:#fff;margin-top:6px}
.g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;padding:14px 36px 4px}
.c{background:#FFF7E8;border-radius:26px;padding:12px;text-align:center;box-shadow:0 5px 0 #8E0B16}
.p{background:#fff;border-radius:18px;height:138px;display:flex;align-items:center;justify-content:center;position:relative}
.p img{max-width:230px;max-height:124px;object-fit:contain}.b{position:absolute;top:-8px;right:-8px;background:#FFC21A;color:#8E0B16;border-radius:14px;padding:0 12px;font-family:Anton;font-size:42px;transform:rotate(4deg)}
.t{font-size:27px;margin-top:8px;color:#3D0A10}.pr{font-family:Anton;font-size:48px;color:#C1121F;line-height:1.1}
.th{text-align:center;color:#fff;font-size:33px;padding:8px 30px 0}.th b{color:#FFC21A}
.f{text-align:center;color:#fff;font-size:40px;padding:4px 30px 0}.f b{color:#FFC21A}
.u{margin:8px auto 0;background:#FFC21A;color:#3D0A10;border-radius:40px;width:760px;text-align:center;font-family:Anton;font-size:60px;padding:8px}"""
html = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class="top"><div class="k">VENDREDI FOU · ON A FAIT LE TRI</div><div class="h">60 RABAIS<br>POUR TOUS</div>'
        f'<div class="s">Jusqu\'à -70 % · 9 thèmes</div></div><div class="g">{cards}</div>'
        f'<div class="th">Maison · Tech · Beauté · Elle · Lui · Jouets · Sport · Animaux · Enfants</div>'
        f'<div class="f">Les 60 liens sont en <b>commentaire 👇</b></div><div class="u">rabaisflashqc.ca</div></body>')
p = ROOT / "docs/pack-du-jour/fb-25nov-60-rabais.html"; p.write_text(html)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
    pg.screenshot(path=str(ROOT / "docs/pack-du-jour/fb-25nov-60-rabais.png")); br.close()
p.unlink(); print("ok")
