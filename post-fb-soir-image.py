#!/usr/bin/env python3
import json, pathlib, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
D = {x["asin"]: x for x in json.load(open(ROOT/"suivi/deals_chrome.json"))}
lots = json.load(open("/tmp/lots.json"))
TH = [("maison","🏠","MAISON"),("tech","💻","TECH"),("beaute","✨","BEAUTÉ"),("femme","👗","POUR ELLE"),("homme","🧔","POUR LUI"),("jouets","🧸","JOUETS"),("plein-air","🏕️","SPORT"),("animaux","🐶","ANIMAUX"),("enfants","👶","ENFANTS")]
HEAD = {"1": ("VENDREDI FOU", "RABAIS POUR TOUS", "Tous les budgets · 9 thèmes"), "2": ("IDÉES CADEAUX", "RABAIS À PIGER", "Pour Noël ou pour toi · 9 thèmes")}
e = H.escape
for n, lot in lots.items():
    k, h, s = HEAD[n]; N = len(lot); cells = ""
    for c, em, lab in TH:
        L = [D[a] for cc, a in lot if cc == c]
        if not L: continue
        mx = max(x["pct"] for x in L); mn = min(x["price"] for x in L)
        cells += f'<div class="c"><div class="em">{em}</div><div class="l">{lab}</div><div class="n">{len(L)} deals</div><div class="b">jusqu\'à -{mx} %</div><div class="p">dès {int(mn)} $</div></div>'
    CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;color:#1A1A1A;overflow:hidden}
.top{text-align:center;padding:22px 30px 0}.k{font-size:46px;color:#fff;letter-spacing:3px}.h{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:104px;line-height:.92;color:#FFC21A;text-shadow:7px 7px 0 #8E0B16}.h2{font-family:Anton,Impact,sans-serif;font-size:70px;color:#fff;line-height:1;margin-top:6px}.s{font-size:46px;color:#fff;margin-top:10px}
.g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;padding:16px 40px 0}.c{background:#FFF7E8;border-radius:28px;padding:8px 8px;text-align:center;box-shadow:0 6px 0 #8E0B16}
.em{font-size:56px;line-height:1.05}.l{font-family:Anton;font-size:44px;color:#3D0A10}.n{font-size:30px;color:#6b2a30}.b{font-family:Anton;font-size:40px;color:#C1121F;margin-top:4px}.p{font-size:30px;color:#3D0A10}
.f{text-align:center;color:#fff;font-size:46px;padding:16px 30px 0}.f b{color:#FFC21A}.u{margin:12px auto 0;background:#FFC21A;color:#3D0A10;border-radius:44px;width:780px;text-align:center;font-family:Anton;font-size:60px;padding:6px}"""
    html = f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class="top"><div class="k">{k}</div><div class="h">{N}</div><div class="h2">{h}</div><div class="s">{s}</div></div><div class="g">{cells}</div><div class="f">Les {N} liens sont en <b>commentaire 👇</b></div><div class="u">rabaisflashqc.ca</div></body>'
    p = ROOT/f"docs/pack-du-jour/fb-soir{n}.html"; p.write_text(html)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width":1080,"height":1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(600)
        pg.screenshot(path=str(ROOT/f"docs/pack-du-jour/fb-soir{n}.png")); br.close()
    p.unlink(); print(n, N)
