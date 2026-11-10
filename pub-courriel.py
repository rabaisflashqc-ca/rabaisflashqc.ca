#!/usr/bin/env python3
"""Image de pub Facebook (1080x1080) : inscription aux deals par courriel. Aucun logo ni marque Amazon (règle Associés)."""
import pathlib, tempfile
import pack
from playwright.sync_api import sync_playwright
CSS="""*{box-sizing:border-box;margin:0}body{width:1080px;height:1080px;background:linear-gradient(160deg,#C1121F,#7A0A16);font-family:'Barlow Semi Condensed',sans-serif;color:#fff;position:relative;overflow:hidden;text-align:center}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}.br{display:flex;justify-content:center;align-items:center;gap:12px;font-size:40px;font-weight:700;letter-spacing:3px;padding-top:60px}.br b{color:#FFC72C}
.pill{display:inline-block;margin-top:34px;background:#FFC72C;color:#7A0A16;border-radius:999px;padding:10px 34px;font-size:40px;font-weight:700}
h1{font-size:88px;line-height:1.05;margin-top:30px}h1 span{color:#FFC72C}
.env{font-size:120px;line-height:1;margin-top:14px}
ul{list-style:none;padding:0;margin:14px auto 0;font-size:42px;font-weight:700;line-height:1.35}
.ft{position:absolute;left:0;right:0;bottom:0;background:#FFC72C;color:#7A0A16;padding:26px 0 24px}.ft .u{font-size:54px;line-height:1}.ft .s{font-size:30px;font-weight:700;margin-top:6px}"""
html=(f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body>'
 f'<div class="br">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
 '<div class="pill">100 % GRATUIT</div>'
 '<h1 class="an">LES DEALS DU JOUR<br><span>DANS TA BOÎTE COURRIEL</span></h1>'
 '<div class="env">📬</div>'
 '<ul><li>✅ Vrais prix, gros %, marques connues</li><li>✅ Le Vendredi fou en primeur 🔥</li></ul>'
 '<div class="ft"><div class="u an">INSCRIS-TOI EN 10 SECONDES 👇</div><div class="s">1 à 2 courriels par jour · désabonnement en tout temps</div></div></body></html>')
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1080),tmp,"pubc"); pg.wait_for_timeout(800)
    out=pack.OUT/"pub-courriel-1080.png"; pg.screenshot(path=str(out)); ctx.close(); br.close()
print(out)
