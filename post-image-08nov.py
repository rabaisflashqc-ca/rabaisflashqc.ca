#!/usr/bin/env python3
"""Image Facebook du 8 nov. (1080x1350) : 6 cadeaux, photos officielles des marques, prix observés le 7 nov. à 19 h 34."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=(".g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;padding:30px 30px 0}"
 ".k{background:#fff;color:#1A1A1A;border-radius:28px;padding:14px 12px 16px;text-align:center;position:relative}"
 ".k img{width:100%;height:185px;object-fit:contain}"
 ".b{font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase}.t{font-size:26px;font-weight:700;line-height:1.08;height:58px}"
 ".p{font-family:Anton,Impact,sans-serif;font-size:60px;color:#C1121F;line-height:1.05}.a{font-size:24px}"
 ".r{position:absolute;top:10px;right:10px;background:#FFC72C;color:#8E0B16;border-radius:16px;padding:4px 14px;font-family:Anton,Impact,sans-serif;font-size:38px}")
P=[("Levi's","Jeans 505 pour homme","B08P55W5DW","72,40 $","37,03 $",49),
   ("JBL","Casque Tune 770NC","B0CTB8GKM2","153,14 $","79,98 $",48),
   ("Nespresso","Vertuo Pop+ Deluxe","B0D712DKKD","159,78 $","94,00 $",41),
   ("Sony","Écouteurs WF-C510","B0DDV8V6FM","90,07 $","58,00 $",36),
   ("Braun","Mélangeur à main MQ505","B01EA5ZI2U","68,35 $","44,99 $",34),
   ("Philips","Friteuse à air 2000","B0D8QN4C9X","146,09 $","99,99 $",32)]
cards="".join(f'<div class="k"><div class="r">-{pc}%</div><img src="{(pathlib.Path("docs/img/p")/("marque-"+a+".jpg")).resolve().as_uri()}"><div class="b">{i+1}. {e(b)}</div><div class="t">{e(t)}</div><div class="p">{pr}</div><div class="a">avant : <s>{av}</s></div></div>' for i,(b,t,a,av,pr,pc) in enumerate(P))
html=(f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1350px;position:relative">'
 f'<div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
 f'<h1 class="an" style="font-size:72px;line-height:1.02;margin-top:-10px">6 CADEAUX DES FÊTES<br>JUSQU’À -49 % 🎁</h1>'
 f'<div class="g">{cards}</div>'
 f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">Prix observés le 7 nov. à 19 h 34 · peuvent changer · vérifie le prix final sur le site</div></div></body></html>')
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"img08")
    pg.wait_for_timeout(800); out=pack.OUT/"post-08nov-facebook.png"; pg.screenshot(path=str(out)); ctx.close(); br.close()
print(out)
