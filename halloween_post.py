#!/usr/bin/env python3
"""Image post Halloween 14 oct : % seulement pour les gros rabais."""
import pathlib, tempfile, html as H
import pack, build
from playwright.sync_api import sync_playwright
e=H.escape
CSS="""*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;background:linear-gradient(160deg,#2B0A3D,#12041C);color:#fff;position:relative;overflow:hidden}
.top{display:flex;align-items:center;gap:14px;padding:46px 56px 0;font-size:40px;letter-spacing:2px;font-weight:700}.top b{color:#FF8A1F}
h1{padding:30px 56px 0;font-size:100px;line-height:1.05;color:#FF8A1F}h2{padding:14px 56px 0;font-size:42px;font-weight:700}
.row{background:#fff;color:#1A1A1A;border-radius:28px;padding:30px;display:flex;align-items:center;gap:24px;margin-bottom:26px}
.bd{background:#FF8A1F;color:#2B0A3D;border-radius:20px;padding:12px 22px;font-family:Anton,Impact,sans-serif;font-size:68px;flex:none}
.foot{position:absolute;left:0;right:0;bottom:0;background:#FF8A1F;color:#2B0A3D;padding:26px 56px 30px;text-align:center}.foot .u{font-size:58px}.foot .s{font-size:24px;font-weight:700;margin-top:6px}"""
D={d["asin"]:d for d in build.data["deals"] if d.get("asin")}
pick=[("B0C5D8TXZW","Tentacules gonflables lumineux","🐙","-26 %"),("B0D89PD7HK","Squelettes articulés, lot de 2","💀","-23 %"),("B08XX3R4VM","Lumières orange et violettes","🎃","4,4 ★")]
rows="".join(f'<div class="row"><div style="font-size:70px">{ic}</div><div style="flex:1"><div style="font-size:28px;font-weight:700;color:#7A2BB5;text-transform:uppercase">{e(D[a]["brand"])}</div><div style="font-size:40px;font-weight:700;line-height:1.1">{e(t)}</div></div><div class="bd">{b}</div></div>' for a,t,ic,b in pick)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an">HALLOWEEN 🎃<br>C\'EST PARTI</h1><h2>Décos qui font peur (et pas ton budget)</h2><div style="padding:40px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Rabais Flash : peut changer à tout moment, durée non garantie</div></div></body></html>'
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"halloween-14oct")
    pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"halloween-14oct.png")); ctx.close(); br.close()
