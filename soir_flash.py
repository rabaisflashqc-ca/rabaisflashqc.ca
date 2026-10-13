#!/usr/bin/env python3
"""Image du post de 19 h 30 : 2 offres éclair, % seulement."""
import pathlib, tempfile, html as H, json
import pack, build
from playwright.sync_api import sync_playwright
e = H.escape
CSS = """*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;background:#C1121F;color:#fff;position:relative;overflow:hidden}
.top{display:flex;align-items:center;gap:14px;padding:46px 56px 0;font-size:40px;letter-spacing:2px;font-weight:700}.top b{color:#FFC72C}
h1{padding:30px 56px 0;font-size:96px;line-height:1.08;color:#FFC72C}h2{padding:14px 56px 0;font-size:44px;font-weight:700}
.foot{position:absolute;left:0;right:0;bottom:0;background:#FFC72C;color:#8E0B16;padding:26px 56px 30px;text-align:center}.foot .u{font-size:58px}.foot .s{font-size:24px;font-weight:700;margin-top:6px}
.card{background:#fff;color:#1A1A1A;border-radius:30px;padding:40px 34px;display:flex;align-items:center;gap:26px;margin-bottom:30px}
.bd{background:#FFC72C;color:#8E0B16;border-radius:22px;padding:14px 22px;font-family:Anton,Impact,sans-serif;font-size:84px;flex:none}"""
D=[d for d in build.data["deals"] if d.get("asin") in ("B0FF9Y16LK","B0GKD3FNDQ")]
rows="".join(f'<div class="card"><div style="flex:1"><div style="font-size:32px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(d["brand"])}</div><div style="font-size:46px;font-weight:700;line-height:1.1">{e({"B0FF9Y16LK":"Crème rétinol et collagène","B0GKD3FNDQ":"Spray solaire sport FPS 50"}[d["asin"]])}</div><div style="font-size:30px;margin-top:10px">⏳ Offre éclair, à durée limitée</div></div><div class="bd">{e(pack.pct_txt(d))}</div></div>' for d in D)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an">OFFRES ÉCLAIR<br>CE SOIR ⚡</h1><h2>Ça part vite, vérifie le prix final sur Amazon.ca</h2><div style="padding:50px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Rabais Flash : peut changer à tout moment, durée non garantie</div></div></body></html>'
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"soir-eclair")
    pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"soir-eclair.png")); ctx.close(); br.close()
print([d["name"] for d in D])
