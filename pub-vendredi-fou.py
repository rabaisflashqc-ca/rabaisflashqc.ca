#!/usr/bin/env python3
"""Pub « Trafic vers le site » : pré-deals + Vendredi fou (27 nov.) + Cyber lundi (30 nov.).
Aucun prix sur l'image (la pub roule plusieurs jours), photos officielles des marques, « les prix peuvent changer à tout moment »."""
import pathlib, tempfile
import pack
from playwright.sync_api import sync_playwright
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=(".tl{display:flex;gap:16px;padding:0 44px;margin-top:26px}"
 ".ev{flex:1;background:#fff;color:#1A1A1A;border-radius:26px;padding:20px 10px;text-align:center}"
 ".ev .d{font-family:Anton,Impact,sans-serif;font-size:44px;color:#C1121F;line-height:1.05}.ev .w{font-size:28px;font-weight:700;margin-top:6px}"
 ".ev.on{background:#FFC72C}.ev.on .d{color:#8E0B16}"
 ".ph{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:0 44px;margin-top:26px}"
 ".ph div{background:#fff;border-radius:22px;height:H px;display:flex;align-items:center;justify-content:center}"
 ".ph img{max-width:88%;max-height:88%;object-fit:contain}")
A="B08P55W5DW B0CTB8GKM2 B0D712DKKD B0DDV8V6FM B0CCPRDH3T B0D8QN4C9X".split()
imgs="".join(f'<div><img src="{(pathlib.Path("docs/img/p")/("marque-"+a+".jpg")).resolve().as_uri()}"></div>' for a in A)
TL=('<div class="tl"><div class="ev on"><div class="d">DÈS<br>MAINTENANT</div><div class="w">Pré-deals</div></div>'
    '<div class="ev"><div class="d">27<br>NOV.</div><div class="w">Vendredi fou</div></div>'
    '<div class="ev"><div class="d">30<br>NOV.</div><div class="w">Cyber lundi</div></div></div>')
def page(w,h,ph,title,mt):
    css=CSS.replace("height:H px",f"height:{ph}px")
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{css}</style></head>'
     f'<body style="width:{w}px;height:{h}px;position:relative"><div class="top" style="padding-top:{mt}px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
     f'<h1 class="an" style="font-size:{title}px;line-height:1.04">VENDREDI FOU<br>ET CYBER LUNDI 🔥</h1>'
     f'<h2 style="font-size:44px">Les meilleurs deals Amazon triés pour le Québec</h2>{TL}<div class="ph">{imgs}</div>'
     f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 VOIS LES DEALS SUR RABAISFLASHQC.CA</div>'
     f'<div class="s">Les prix peuvent changer à tout moment · vérifie le prix final avant d’acheter</div></div></body></html>')
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for n,(w,h,ph,t,mt) in {"pub-vendredi-fou-fil":(1080,1350,190,92,40),"pub-vendredi-fou-story":(1080,1920,260,98,170)}.items():
        br,ctx,pg=pack.render(pw,page(w,h,ph,t,mt),(w,h),tmp,n); pg.wait_for_timeout(800)
        pg.screenshot(path=str(pack.OUT/f"{n}.png")); ctx.close(); br.close(); print(n)
