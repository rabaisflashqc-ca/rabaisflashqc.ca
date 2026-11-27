#!/usr/bin/env python3
"""Image FB 26 nov (sans photos produits, reseau bloque) -> docs/pack-du-jour/fb-26nov-60-rabais.png"""
import json, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"
T = [("🏠","Couteaux NutriChef","B08HZB5LPP"),("📷","Caméra Blink XR","B0DV4W9ZS3"),("🎧","JBL Endurance","B0DVTDJ7TH"),
     ("🪥","Philips Sonicare","B09LD7WRVS"),("👟","Skechers Go Walk","B07N13MDKH"),("👞","Cole Haan","B08CB4JTVG"),
     ("🧸","LEGO DUPLO Peppa","B0F2JC33YS"),("🎒","Sac Herschel","B0C3B6DJC2"),("👧","Hoodie PUMA","B0887VQHKC")]
it = {x["asin"]: x for x in json.load(open(ROOT/"suivi/posts/2026-11-26-fb-items.json"))}
cards = "".join(f'<div class="c"><div class="e">{e}</div><span class="b">-{it[a]["pct"]} %</span><div class="t">{t}</div><div class="pr">{money(it[a]["price"])}</div></div>' for e,t,a in T)
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;color:#1A1A1A;overflow:hidden}
.top{text-align:center;padding:26px 30px 0}.top .k{font-size:42px;color:#fff;letter-spacing:2px}
.top .h{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:100px;line-height:.95;color:#FFC21A;text-shadow:6px 6px 0 #8E0B16;margin-top:6px}
.top .s{font-size:48px;color:#fff;margin-top:10px}
.g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;padding:20px 36px 4px}
.c{background:#FFF7E8;border-radius:26px;padding:16px 10px 14px;text-align:center;box-shadow:0 6px 0 #8E0B16;position:relative}
.e{font-size:76px;line-height:1.1}.b{position:absolute;top:-10px;right:-8px;background:#FFC21A;color:#8E0B16;border-radius:14px;padding:0 14px;font-family:Anton;font-size:46px;transform:rotate(4deg)}
.t{font-size:31px;margin-top:6px;color:#3D0A10}.pr{font-family:Anton;font-size:56px;color:#C1121F;line-height:1.15}
.th{text-align:center;color:#fff;font-size:33px;padding:14px 30px 0}
.f{text-align:center;color:#fff;font-size:46px;padding:10px 30px 0}.f b{color:#FFC21A}
.u{margin:10px auto 0;background:#FFC21A;color:#3D0A10;border-radius:40px;width:780px;text-align:center;font-family:Anton;font-size:64px;padding:10px}"""
html = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class="top"><div class="k">VEILLE DU VENDREDI FOU · NOUVELLE SÉLECTION</div><div class="h">60 NOUVEAUX<br>RABAIS</div>'
        f'<div class="s">Jusqu\'à -70 % · dès 19 $</div></div><div class="g">{cards}</div>'
        f'<div class="th">Maison · Tech · Beauté · Elle · Lui · Jouets · Sport · Animaux · Enfants</div>'
        f'<div class="f">Les 60 liens sont en <b>commentaire 👇</b></div><div class="u">rabaisflashqc.ca</div></body>')
p = ROOT/"docs/pack-du-jour/fb-26nov-60-rabais.html"; p.write_text(html)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width":1080,"height":1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
    pg.screenshot(path=str(ROOT/"docs/pack-du-jour/fb-26nov-60-rabais.png")); br.close()
p.unlink(); print("ok")
