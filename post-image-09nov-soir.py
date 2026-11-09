#!/usr/bin/env python3
"""Image Facebook/Instagram du 9 nov. soir (1080x1350) : un cadeau pour chaque membre de la famille, photos officielles des marques, prix Keepa du 9 nov. à 8 h 11."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=(".g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;padding:26px 30px 0}"
 ".k{background:#fff;color:#1A1A1A;border-radius:28px;padding:12px 12px 16px;text-align:center;position:relative}"
 ".k img{width:100%;height:180px;object-fit:contain}"
 ".w{display:inline-block;background:#8E0B16;color:#FFC72C;border-radius:12px;padding:3px 12px;font-size:23px;font-weight:800;text-transform:uppercase;margin-bottom:4px}"
 ".t{font-size:25px;font-weight:700;line-height:1.08;height:56px}"
 ".p{font-family:Anton,Impact,sans-serif;font-size:58px;color:#C1121F;line-height:1.05}.a{font-size:23px}"
 ".r{position:absolute;top:10px;right:10px;background:#FFC72C;color:#8E0B16;border-radius:16px;padding:4px 14px;font-family:Anton,Impact,sans-serif;font-size:36px}")
P=[("Pour lui","Levi's 505 pour homme","B08P55W5DW","62,31 $","37,03 $",41),
   ("Pour l'ado","Casque JBL Tune 770NC","B0CTB8GKM2","132,17 $","79,98 $",39),
   ("Pour maman","Nespresso Vertuo Pop+","B0D712DKKD","141,67 $","94,00 $",34),
   ("Pour le sportif","Écouteurs Sony WF-C510","B0D9R45FMH","82,95 $","58,00 $",30),
   ("Pour les enfants","Coffret d'art Crayola Pokémon","B0CCPRDH3T","27,48 $","19,98 $",27),
   ("Pour la cuisine","Friteuse à air Philips 2000","B0D8QN4C9X","127,03 $","99,99 $",21)]
cards="".join(f'<div class="k"><div class="r">-{pc}%</div><img src="{(pathlib.Path("docs/img/p")/("marque-"+a+".jpg")).resolve().as_uri()}"><div class="w">{e(w)}</div><div class="t">{e(t)}</div><div class="p">{pr}</div><div class="a">avant : <s>{av}</s></div></div>' for (w,t,a,av,pr,pc) in P)
html=(f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1350px;position:relative">'
 f'<div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
 f'<h1 class="an" style="font-size:68px;line-height:1.02;margin-top:-10px">UN CADEAU POUR CHACUN<br>JUSQU’À -41 % 🎁</h1>'
 f'<div class="g">{cards}</div>'
 f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">Prix observés le 9 nov. · peuvent changer · vérifie le prix final sur le site</div></div></body></html>')
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"img09s")
    pg.wait_for_timeout(800); out=pack.OUT/"post-09nov-soir-famille.png"; pg.screenshot(path=str(out)); ctx.close(); br.close()
print(out)
