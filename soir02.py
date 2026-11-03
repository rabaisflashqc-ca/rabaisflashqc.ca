#!/usr/bin/env python3
"""Image du soir 2 nov : 5 plus gros rabais de la passe Keepa de 19 h 16."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".row{background:#fff;color:#1A1A1A;border-radius:28px;padding:10px 28px;display:flex;align-items:center;gap:22px;margin-bottom:10px}.bd2{background:#FFC72C;color:#8E0B16;border-radius:22px;padding:12px 22px;font-family:Anton,Impact,sans-serif;font-size:54px;flex:none}"
OB="2 nov. à 19 h 16"
PICK=[("Sony","Casque sans fil WH-CH520","🎧","48,00 $","93,96 $",49,OB),("CMF by Nothing","Écouteurs sans fil Buds 2","🎵","37,99 $","70,70 $",46,OB),("Sony","Haut-parleur ULT Field 1, étanche","🔊","98,00 $","174,27 $",44,OB),("DEWALT","Perceuse sans balais 20V MAX, ensemble","🛠️","118,00 $","199,94 $",41,OB),("EXIT","Jeu d’évasion La maison des énigmes","🧩","17,95 $","30,62 $",41,OB)]
rows="".join(f'<div class="row"><div style="font-size:52px">{ic}</div><div style="flex:1"><div style="font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:29px;font-weight:700;line-height:1.1">{e(t)}</div><div style="font-size:32px"><b>{p}</b> <s style="color:#777;font-size:24px">{o}</s></div><div style="font-size:20px;color:#555">prix observé le {ob}</div></div><div class="bd2">-{pc} %</div></div>' for a,t,ic,p,o,pc,ob in PICK)
html=f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:80px;line-height:1.05">LES 5 PLUS GROS RABAIS DU SOIR ⚡</h1><h2>Jusqu’à -49 %, prix vus ce soir à 19 h 16</h2><div style="padding:14px 56px 0">{rows}</div><div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">Vérifie le prix final sur rabaisflashqc.ca</div></div></body></html>'
if __name__=="__main__":
    tmp=pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"soir-02nov-prix")
        pg.wait_for_timeout(700); pg.screenshot(path=str(pack.OUT/"soir-02nov-prix.png")); ctx.close(); br.close()
    print(pack.OUT/"soir-02nov-prix.png")
