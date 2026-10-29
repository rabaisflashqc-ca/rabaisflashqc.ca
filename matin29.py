#!/usr/bin/env python3
"""Image du post du matin 29 oct : 5 deals, % seulement."""
import pathlib, tempfile, html as H
import pack, build
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:28px;padding:16px 28px;display:flex;align-items:center;gap:22px;margin-bottom:14px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:20px;padding:10px 20px;font-family:Anton,Impact,sans-serif;font-size:64px;flex:none}"
pick=[("ThermoMaven","Thermomètre à viande Bluetooth G2","🥩",50),("Russell Athletic","Chandail pullover pour homme","👕",56),("Cottonelle","Papier de toilette, 144 rouleaux","🧻",50),("The North Face","Gants Etip recyclés","🧤",42),("Skechers","Go Run Consistent 2.0, espadrilles","👟",28)]
rows="".join(f'<div class="row"><div style="font-size:58px">{ic}</div><div style="flex:1"><div style="font-size:28px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:34px;font-weight:700;line-height:1.1">{e(t)}</div></div><div class="bd2">-{ic2} %</div></div>' for a,t,ic,ic2 in pick)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:76px;line-height:1.05">LES RABAIS<br>DU MATIN ⚡</h1><h2>Cuisine, mode et maison</h2><div style="padding:22px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Les prix bougent vite, fonce!</div></div></body></html>'
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"matin-29oct")
    pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"matin-29oct.png")); ctx.close(); br.close()
