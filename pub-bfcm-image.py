#!/usr/bin/env python3
"""Visuel pub payante Vendredi fou -> Cyber lundi : hybride « chiffre choc » + « panier ». 4:5 (1080x1350) et 9:16 (1080x1920)."""
import json, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
N = len(json.load(open(ROOT/"docs/recherche.json")))
big = f"{(N//100)*100:,}".replace(",", "&nbsp;") + "+"   # arrondi à la centaine sous le nombre réel
CART = '<svg viewBox="0 0 64 64" width="{s}" height="{s}" fill="none" stroke="#FFC21A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8h9l7 31h28l6-22H19"/><circle cx="27" cy="52" r="4" fill="#FFC21A"/><circle cx="46" cy="52" r="4" fill="#FFC21A"/></svg>'
def html(h, tall):
    cs = 120 if tall else 90
    return f"""<!doctype html><meta charset=utf-8><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1080px;height:{h}px;background:#3D0A10;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;color:#fff;display:flex;flex-direction:column;overflow:hidden;padding:{'210px 0 270px' if tall else '0'}}}
.s{{background:#FFC21A;color:#3D0A10;text-align:center;font-size:44px;padding:20px 10px;letter-spacing:3px}}
.m{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 50px}}
.n{{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:{280 if tall else 200}px;line-height:1;color:#FFC21A}}
.t{{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:{96 if tall else 76}px;line-height:1.02;margin-top:6px}}
.sub{{font-size:46px;color:#F6D9DC;margin-top:{26 if tall else 18}px;font-weight:500}}
.q{{margin-top:{44 if tall else 30}px;width:920px;box-sizing:border-box;background:#fff;border:6px solid #FFC21A;border-radius:28px;display:flex;align-items:center;gap:18px;padding:12px 12px 12px 26px}}
.q svg{{flex:none}}.q span{{flex:1;text-align:left;font-size:{44 if tall else 40}px;color:#8a8a85;font-weight:500;white-space:nowrap}}.q em{{font-style:normal;background:#FFC21A;color:#3D0A10;font-size:{46 if tall else 42}px;padding:{22 if tall else 18}px 28px;border-radius:18px}}
.lbl{{margin-top:{40 if tall else 26}px;font-family:Anton,Impact,sans-serif;font-weight:400;font-size:{56 if tall else 56}px;color:#fff;letter-spacing:1px;white-space:nowrap}}.lbl b{{color:#FFC21A;font-weight:400}}
.p{{margin-top:{40 if tall else 24}px;background:#C1121F;border-radius:44px;padding:{34 if tall else 26}px 54px;display:flex;align-items:center;gap:30px;text-align:left}}
.p div{{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:{66 if tall else 54}px;line-height:1.04}}.p b{{color:#FFC21A;font-weight:400}}
.f{{background:#C1121F;text-align:center;font-size:58px;padding:{40 if tall else 28}px 10px;letter-spacing:1px}}.f b{{color:#FFC21A}}
</style><body><div class="s">VENDREDI FOU ➔ CYBER LUNDI · JUSQU'AU 30 NOV.</div>
<div class="m"><div class="n">{big}</div><div class="t">RABAIS DÉJÀ TRIÉS</div><div class="sub">Les grandes marques · tous les besoins</div>
<div class="lbl">TROUVE TON DEAL, <b>SANS PERDRE DE TEMPS</b></div>
<div class="q"><svg viewBox="0 0 24 24" width="56" height="56" fill="none" stroke="#5F5E5A" stroke-width="2.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M16 16l5 5"/></svg><span>Cherche un produit ou une marque</span><em>Trouver</em></div>
<div class="p">{CART.format(s=cs)}<div>AJOUTE AU PANIER.<br><b>NE RATE RIEN.</b></div></div></div>
<div class="f">rabaisflashqc<b>.ca</b> · On a déjà fait le tri</div></body>"""
out = ROOT/"docs/pack-du-jour"
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name, h, tall in (("pub-bfcm-4x5", 1350, False), ("pub-bfcm-9x16", 1920, True)):
        p = out/f"{name}.html"; p.write_text(html(h, tall))
        pg = br.new_page(viewport={"width":1080,"height":h}); pg.goto(p.as_uri()); pg.wait_for_timeout(600)
        pg.screenshot(path=str(out/f"{name}.png")); pg.close(); p.unlink()
    br.close()
print(big)
