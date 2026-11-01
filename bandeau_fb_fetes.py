#!/usr/bin/env python3
"""Bandeau (photo de couverture) Facebook, Vendredi fou et Noël 2026.
1640 x 924 : le texte important reste dans la bande centrale (y 170 à 750),
visible sur ordinateur (recadré en 2,63:1) comme sur cellulaire."""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs" / "pack-du-jour" / "bandeau-facebook-fetes.png"
FONT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/fnt/package/files/anton-latin-400-normal.woff2")
anton = base64.b64encode(FONT.read_bytes()).decode()
BOLT = '<svg width="34" height="54" viewBox="0 0 100 160"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFC72C"/></svg>'

flakes = "".join(
    f'<div class="fl" style="left:{x}px;top:{y}px;font-size:{s}px;opacity:{o}">❄</div>'
    for x, y, s, o in [(60, 40, 46, .35), (300, 110, 28, .25), (1500, 60, 40, .3), (1330, 160, 26, .25),
                       (1580, 420, 30, .25), (40, 470, 34, .25), (220, 820, 30, .25), (1420, 840, 36, .3),
                       (760, 30, 24, .2), (980, 870, 26, .2)])

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url(data:font/woff2;base64,{anton}) format('woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1640px;height:924px;overflow:hidden;font-family:Inter,"DejaVu Sans",sans-serif;
 background:radial-gradient(ellipse at 50% 45%,#D7192A 0%,#A50F1E 55%,#5E0812 100%);position:relative;color:#fff}}
.an{{font-family:Anton,Impact,sans-serif;font-weight:400;letter-spacing:1px}}
.fl{{position:absolute;color:#fff}}
.bolt{{position:absolute;left:-60px;top:40px;width:520px;height:900px;opacity:.10}}
.wrap{{position:absolute;left:0;right:0;top:168px;text-align:center}}
.brand{{display:inline-flex;align-items:center;gap:14px;font-size:34px;font-weight:800;letter-spacing:4px}}
.brand b{{color:#FFC72C}}
.join{{display:inline-block;margin-top:22px;background:#fff;color:#A50F1E;border-radius:60px;padding:12px 40px;font-size:40px;font-weight:800}}
h1{{font-size:100px;line-height:1.02;color:#FFC72C;margin-top:18px;text-shadow:0 6px 0 #6E0A15}}
h1 span{{color:#fff}}
.chips{{margin-top:30px;display:flex;justify-content:center;gap:18px}}
.chip{{background:rgba(255,255,255,.14);border:3px solid rgba(255,255,255,.5);border-radius:40px;padding:10px 24px;font-size:27px;font-weight:700;white-space:nowrap}}
.chip.y{{background:#FFC72C;border-color:#FFC72C;color:#7A0A16}}
.cta{{position:absolute;left:0;right:0;top:695px;text-align:center;font-size:32px;font-weight:700}}
.cta b{{color:#FFC72C}}
.deco{{position:absolute;font-size:96px}}
</style></head><body>
<svg class="bolt" viewBox="0 0 100 160"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#fff"/></svg>
{flakes}
<div class="deco" style="left:40px;top:330px">🎄</div>
<div class="deco" style="right:40px;top:330px">🎁</div>
<div class="wrap">
 <div class="brand">{BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><br>
 <div class="join">👋 Rejoins la gang des chasseurs de deals!</div>
 <h1 class="an">SAUVE GROS AU <span>VENDREDI FOU</span><br>ET À <span>NOËL</span></h1>
 <div class="chips">
  <div class="chip y">🔥 Vendredi fou · 27 nov.</div>
  <div class="chip">💻 Cyber lundi · 30 nov.</div>
  <div class="chip">🎁 Idées cadeaux</div>
  <div class="chip">⚡ Nouveaux deals chaque jour</div>
 </div>
</div>
<div class="cta">👍 Abonne-toi à la page et active les notifications · Tous les deals sur <b>rabaisflashqc.ca</b></div>
</body></html>"""

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 1640, "height": 924})
    pg.set_content(html); pg.wait_for_timeout(600)
    pg.screenshot(path=str(OUT)); br.close()
print(OUT)
