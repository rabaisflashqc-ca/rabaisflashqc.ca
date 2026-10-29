#!/usr/bin/env python3
"""Image du post du matin 29 oct (version prix) : 5 deals du Top 5."""
import pathlib, tempfile, html as H
import pack, build
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:28px;padding:16px 28px;display:flex;align-items:center;gap:22px;margin-bottom:14px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:20px;padding:10px 20px;font-family:Anton,Impact,sans-serif;font-size:64px;flex:none}"
pick=[("Organika","NAC, 180 gélules","💊","23,98 $","42,39 $",43),("Bedsure","Couverture en peluche côtelée","🛋️","24,68 $","34,99 $",29),("CLOUDWINGS","Trousse de maquillage, initiale","👜","30,69 $","38,38 $",20),("Jack Black","Clean Break, crème hydratante","🧴","41,00 $","49,95 $",18),("Enesco","Figurine Le Roi Lion, Jim Shore","🦁","120,00 $","env. 152 $",21)]
rows="".join(f'<div class="row"><div style="font-size:52px">{ic}</div><div style="flex:1"><div style="font-size:26px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:30px;font-weight:700;line-height:1.1">{e(t)}</div><div style="font-size:30px"><b>{p}</b> <s style="color:#777;font-size:24px">{o}</s></div></div><div class="bd2" style="font-size:54px">-{pc} %</div></div>' for a,t,ic,p,o,pc in pick)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:76px;line-height:1.05">LES RABAIS<br>DU MATIN ⚡</h1><h2>Prix observés les 26 et 27 oct.</h2><div style="padding:22px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Les prix bougent vite, fonce!</div></div></body></html>'
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"matin-29oct-prix")
    pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"matin-29oct-prix.png")); ctx.close(); br.close()
