#!/usr/bin/env python3
"""Posts FB du soir 25 nov (16h30 et 18h30): 2 lots de ~50 produits verifies en direct, 9 themes. Sorties suivi/posts/2026-11-25-fb-soir{1,2}-*"""
import json, re, pathlib, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
D = {x["asin"]: x for x in json.load(open(ROOT/"suivi/deals_chrome.json"))}
OK = set(json.load(open("/tmp/ok.json")))
cands = json.load(open("/tmp/cands.json"))
exec(open(ROOT/"post-fb-25nov-themes.py").read().split("out = {}")[0].split("D = json.load")[0].replace('ROOT = pathlib.Path(__file__).resolve().parent',''))
src = open(ROOT/"post-fb-25nov-themes.py").read()
ns = {}
exec(src.split("out = {}")[0].replace("__file__", repr(str(ROOT/"x.py"))), ns)
clean, money, THEMES, TAG = ns["clean"], ns["money"], ns["THEMES"], ns["TAG"]
EMO = {c: l.split()[0] for c, l in THEMES}
def img_path(a):
    for n in (f"marque-{a}.jpg", f"{a}.jpg"):
        p = ROOT/"docs/img/p"/n
        if p.exists(): return p
lots = {1: [], 2: []}
for cat, label in THEMES:
    ok = [a for a, p in cands[cat] if a in OK]
    for i, a in enumerate(ok): lots[1 if i % 2 == 0 else 2].append((cat, a))
for n, lot in lots.items():
    lines = [f"{EMO[c]} {clean(D[a]['title'])} : {ns['money'](D[a]['price'])} (-{D[a]['pct']} %)\n👉 https://www.amazon.ca/dp/{a}?tag={TAG}" for c, a in lot]
    json.dump(lines, open(ROOT/f"suivi/posts/2026-11-25-fb-soir{n}-commentaires.json", "w"), ensure_ascii=False, indent=1)
    tiles = []
    seen = set()
    for c, a in lot:
        if c in seen or not img_path(a): continue
        seen.add(c); tiles.append((c, a))
    print(n, len(lot), "tuiles", len(tiles), "avec photo")
json.dump({str(n): lot for n, lot in lots.items()}, open("/tmp/lots.json", "w"))
