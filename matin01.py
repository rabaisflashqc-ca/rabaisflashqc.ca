#!/usr/bin/env python3
"""Image du matin 1er nov : 5 deals sous 75 $, prix scannés le 1er nov. à 7 h 09."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:28px;padding:10px 28px;display:flex;align-items:center;gap:22px;margin-bottom:10px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:22px;padding:12px 22px;font-family:Anton,Impact,sans-serif;font-size:54px;flex:none}"
OB="1er nov. à 7 h 10"
PICK=[("Amazon Fire TV","Fire TV Stick 4K Max","📺","64,99 $","129,98 $",50,OB),("INIU","Station de recharge 3 en 1 MagSafe Qi2","🔌","20,39 $","39,99 $",49,OB),("Ferrero Rocher","Boîte cadeau de 48 chocolats","🍫","21,49 $","40,00 $",46,OB),("ThermoMaven","Thermomètre à viande WiFi G1","🍗","39,99 $","69,99 $",43,OB),("Anker soundcore","Écouteurs ouverts V20i, 36 h","🎧","35,99 $","59,99 $",40,OB)]
rows="".join(f'<div class="row"><div style="font-size:52px">{ic}</div><div style="flex:1"><div style="font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:29px;font-weight:700;line-height:1.1">{e(t)}</div><div style="font-size:32px"><b>{p}</b> <s style="color:#777;font-size:24px">{o}</s></div><div style="font-size:20px;color:#555">prix observé le {ob}</div></div><div class="bd2">-{pc} %</div></div>' for a,t,ic,p,o,pc,ob in PICK)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:80px;line-height:1.05">5 IDÉES CADEAUX EN RABAIS 🎁</h1><h2>Idées cadeaux des Fêtes, prix vus ce matin</h2><div style="padding:14px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">Vérifie le prix final sur rabaisflashqc.ca</div></div></body></html>'
if __name__=="__main__":
    tmp=pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"matin-01nov-prix")
        pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"matin-01nov-prix.png")); ctx.close(); br.close()
    print(pack.OUT/"matin-01nov-prix.png")
