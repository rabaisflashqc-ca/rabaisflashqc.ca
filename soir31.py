#!/usr/bin/env python3
"""Image du soir 31 oct : Top 5 sous 25 $, prix scannés le 31 oct. à 15 h 58."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:28px;padding:10px 28px;display:flex;align-items:center;gap:22px;margin-bottom:10px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:22px;padding:12px 22px;font-family:Anton,Impact,sans-serif;font-size:54px;flex:none}"
OB="31 oct. à 15 h 58"
PICK=[("BlackCanyon Outfitters","Gants de conduite en cuir de vache (L)","🧤","17,00 $","69,50 $",76,OB),
      ("Pilates","Kit d'exercice : anneau, ballon, bandes","🧘","16,99 $","35,99 $",53,OB),
      ("AstroAI","Balai à neige et grattoir 2 en 1 (27 po)","❄️","16,99 $","29,99 $",43,OB),
      ("ORICO","Hub USB 3.0 à 7 ports","💻","13,79 $","22,98 $",40,OB),
      ("Splendor Kids","Jeu de société pour enfants","🎲","22,42 $","34,44 $",35,OB)]
rows="".join(f'<div class="row"><div style="font-size:52px">{ic}</div><div style="flex:1"><div style="font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:29px;font-weight:700;line-height:1.1">{e(t)}</div><div style="font-size:32px"><b>{p}</b> <s style="color:#777;font-size:24px">{o}</s></div><div style="font-size:20px;color:#555">prix observé le {ob}</div></div><div class="bd2">-{pc} %</div></div>' for a,t,ic,p,o,pc,ob in PICK)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:84px;line-height:1.05">TOP 5 SOUS 25 $ 🔥</h1><h2>Prêts pour l\'hiver et les Fêtes · prix vus cet après-midi</h2><div style="padding:14px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Vérifie le prix final sur rabaisflashqc.ca</div></div></body></html>'
if __name__=="__main__":
    tmp=pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"soir-31oct")
        pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"soir-31oct.png")); ctx.close(); br.close()
    print(pack.OUT/"soir-31oct.png")
