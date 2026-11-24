#!/usr/bin/env python3
"""Image Facebook du 24 nov. : 6 deals avec photos officielles de marque, liens en commentaire. -> docs/pack-du-jour/fb-24nov-vendredi-fou.png"""
import json, pathlib, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
deals = {d["asin"]: d for d in json.load(open(ROOT / "suivi/deals_chrome.json"))}
e = H.escape
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"
EX = [("B08DJ8Z3WH","Shark","Navigator Pro"),("B0DN45YMP6","JBL","Vibe Beam 2"),("B0CHBNXJ24","Ninja","CREAMi XL"),
      ("B0B38KRTV6","De'Longhi","Magnifica Evo"),("B0G2STSGW3","LEGO","Star Wars AT-AT"),("B0BWWZP49F","Blink","Mini 2")]
cards = ""
for i, (a, b, t) in enumerate(EX, 1):
    d = deals[a]; img = (ROOT / f"docs/img/p/marque-{a}.jpg").resolve().as_uri()
    cards += (f'<div class="c"><div class="n">{i}</div><div class="p"><img src="{img}"><span class="b">-{d["pct"]} %</span></div>'
              f'<div class="t">{e(b)} · {e(t)}</div><div class="pr">{money(d["price"])}</div></div>')
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;color:#1A1A1A;overflow:hidden}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}.top{text-align:center;padding:28px 30px 4px}
.top .h{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:92px;line-height:1;color:#FFC21A;text-shadow:5px 5px 0 #8E0B16}
.top .s{font-size:50px;color:#fff;margin-top:8px}
.g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;padding:20px 40px}
.c{background:#FFF7E8;border-radius:30px;padding:16px;text-align:center;position:relative;box-shadow:0 6px 0 #8E0B16}
.n{position:absolute;top:-10px;left:-10px;background:#1A1A1A;color:#FFC21A;width:54px;height:54px;border-radius:50%;font-family:Anton;font-size:34px;line-height:54px;z-index:2}
.p{background:#fff;border-radius:20px;height:215px;display:flex;align-items:center;justify-content:center;position:relative}
.p img{max-width:270px;max-height:195px;object-fit:contain}.b{position:absolute;top:-8px;right:-8px;background:#FFC21A;color:#8E0B16;border-radius:16px;padding:2px 14px;font-family:Anton;font-size:46px;transform:rotate(4deg)}
.t{font-size:28px;margin-top:10px;min-height:32px;color:#3D0A10}.pr{font-family:Anton;font-size:62px;color:#C1121F;line-height:1.1}
.f{text-align:center;color:#fff;font-size:44px;padding:6px 30px}.f b{color:#FFC21A}
.u{margin:6px auto 0;background:#FFC21A;color:#3D0A10;border-radius:40px;width:760px;text-align:center;font-family:Anton;font-size:64px;padding:12px}"""
html = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class="top"><div class="h">VENDREDI FOU<br>APPROCHE 🔥</div>'
        f'<div class="s">6 rabais à saisir tout de suite</div></div><div class="g">{cards}</div>'
        f'<div class="f">Les liens de chaque produit sont en <b>commentaire 👇</b></div><div class="u">rabaisflashqc.ca</div></body>')
p = ROOT / "docs/pack-du-jour/fb-24nov-vendredi-fou.html"; p.write_text(html)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
    pg.screenshot(path=str(ROOT / "docs/pack-du-jour/fb-24nov-vendredi-fou.png")); br.close()
p.unlink(); print("ok")
