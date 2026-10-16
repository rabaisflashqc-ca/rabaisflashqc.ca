#!/usr/bin/env python3
"""Image du post du matin 14 oct : 4 deals, % seulement."""
import pathlib, tempfile, html as H
import pack, build
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:28px;padding:26px 30px;display:flex;align-items:center;gap:22px;margin-bottom:22px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:20px;padding:10px 20px;font-family:Anton,Impact,sans-serif;font-size:64px;flex:none}"
pick=[("B0CT9SBWC9","Tune 670NC, casque antibruit","🎧"),("B0CTB8GKM2","Tune 770NC, casque antibruit","🎧"),("B0BQPNMXQV","Vibe Beam, écouteurs sans fil","🎵"),("B0711FGWN9","Trousse solaire The Getaway","☀️")]
D={d["asin"]:d for d in build.data["deals"] if d.get("asin")}
rows="".join(f'<div class="row"><div style="font-size:58px">{ic}</div><div style="flex:1"><div style="font-size:28px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(D[a]["brand"])}</div><div style="font-size:38px;font-weight:700;line-height:1.1">{e(t)}</div></div><div class="bd2">{e(pack.pct_txt(D[a]))}</div></div>' for a,t,ic in pick)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:92px;line-height:1.08">LES PLUS GROS<br>RABAIS DU SOIR ⚡</h1><h2>Du son et du solaire à gros rabais</h2><div style="padding:36px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Rabais Flash : peut changer à tout moment, durée non garantie</div></div></body></html>'
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"soir-16oct")
    pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"soir-16oct.png")); ctx.close(); br.close()
