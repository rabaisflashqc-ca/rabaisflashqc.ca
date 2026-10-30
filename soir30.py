#!/usr/bin/env python3
"""Image du soir 30 oct : 4 deals aux prix observés dans les 12 dernières heures."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:32px;padding:14px 28px;display:flex;align-items:center;gap:22px;margin-bottom:12px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:22px;padding:12px 22px;font-family:Anton,Impact,sans-serif;font-size:54px;flex:none}"
PICK=[("Mise en forme","Kit Pilates : anneau, ballon, bandes","🧘","16,99 $","35,99 $",53,"30 oct. à 8 h 29"),("AstroAI","Balai à neige et grattoir 2 en 1, 27 po","❄️","16,99 $","29,99 $",43,"30 oct. à 9 h 29"),("ThermoMaven","Thermomètre à viande WiFi G1","🍖","39,99 $","69,99 $",43,"30 oct. à 10 h 08"),("VIOFO","Caméra de tableau de bord A119 Mini 2","🚗","135,99 $","169,99 $",20,"30 oct. à 15 h 42")]
rows="".join(f'<div class="row"><div style="font-size:52px">{ic}</div><div style="flex:1"><div style="font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:29px;font-weight:700;line-height:1.1">{e(t)}</div><div style="font-size:32px"><b>{p}</b> <s style="color:#777;font-size:24px">{o}</s></div><div style="font-size:20px;color:#555">prix observé le {ob}</div></div><div class="bd2">-{pc} %</div></div>' for a,t,ic,p,o,pc,ob in PICK)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:72px;line-height:1.05">PAS BESOIN D\'ATTENDRE<br>LE BLACK FRIDAY ⏳</h1><h2>4 deals aux prix vus aujourd\'hui</h2><div style="padding:18px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Vérifie le prix final sur Amazon.ca</div></div></body></html>'
if __name__=="__main__":
    tmp=pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"soir-30oct")
        pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"soir-30oct.png")); ctx.close(); br.close()
    print(pack.OUT/"soir-30oct.png")
