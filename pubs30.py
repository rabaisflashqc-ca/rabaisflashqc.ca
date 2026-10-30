#!/usr/bin/env python3
"""Visuels des 2 pubs test (31 oct au 6 nov) : Suivre la page + Trafic vers le site."""
import pathlib, tempfile
import pack
from playwright.sync_api import sync_playwright
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".pt{background:#fff;color:#1A1A1A;border-radius:28px;margin:16px 56px;padding:22px 30px;font-size:38px;font-weight:700;display:flex;gap:20px;align-items:center}"
def page(inner,foot,sub):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot"><div class="u an">{foot}</div><div class="s">{sub}</div></div></body></html>'
pts=lambda L:"".join(f'<div class="pt"><span style="font-size:52px">{i}</span><span>{t}</span></div>' for i,t in L)
A=page('<h1 class="an" style="font-size:96px;line-height:1.05">LES RABAIS AMAZON.CA<br>DU QUÉBEC, CHAQUE JOUR ⚡</h1><div style="padding-top:20px">'+pts([("🔎","On trie les vraies baisses de prix pour toi"),("⏰","Deals du matin et du soir"),("🎁","Black Friday et idées cadeaux de Noël"),("🇨🇦","En français, pour le Québec")])+'</div>',"👉 ABONNE-TOI","Gratuit · Facebook et Instagram")
B=page('<h1 class="an" style="font-size:104px;line-height:1.05">BLACK FRIDAY<br>COMMENCE ICI 🔥</h1><h2>Les vraies baisses de prix sur Amazon.ca</h2><div style="padding-top:20px">'+pts([("💸","Prix, ancien prix et % affichés"),("📅","Date d\'observation sur chaque deal"),("🎄","Guides cadeaux : pour elle, pour lui, moins de 25 $")])+'</div>',"👉 RABAISFLASHQC.CA","Les prix bougent vite, vérifie le prix final sur Amazon.ca")
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for n,h in (("pub-suivre-30oct",A),("pub-site-30oct",B)):
        br,ctx,pg=pack.render(pw,h,(1080,1350),tmp,n); pg.wait_for_timeout(600)
        pg.screenshot(path=str(pack.OUT/f"{n}.png")); ctx.close(); br.close(); print(n)
