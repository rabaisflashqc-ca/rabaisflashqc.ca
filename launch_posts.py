#!/usr/bin/env python3
"""Images de lancement Instagram/Facebook (1080x1350). Pas de prix, seulement des %."""
import pathlib, tempfile, html as H
import pack, build
from playwright.sync_api import sync_playwright
OUT = pack.OUT; e = H.escape
LEA = (pathlib.Path(__file__).parent / "docs" / "lea.jpg").as_uri()
CSS = """*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;background:#C1121F;color:#fff;position:relative;overflow:hidden}
.top{display:flex;align-items:center;gap:14px;padding:46px 56px 0;font-size:40px;letter-spacing:2px;font-weight:700}.top b{color:#FFC72C}
h1{padding:30px 56px 0;font-size:104px;line-height:.98;color:#FFC72C}h2{padding:14px 56px 0;font-size:44px;font-weight:700;line-height:1.15}
.foot{position:absolute;left:0;right:0;bottom:0;background:#FFC72C;color:#8E0B16;padding:26px 56px 30px;text-align:center}.foot .u{font-size:58px}.foot .s{font-size:24px;font-weight:700;margin-top:6px}
.card{background:#fff;color:#1A1A1A;border-radius:28px;padding:26px 30px;display:flex;align-items:center;gap:24px}.card .t{font-size:40px;font-weight:700;line-height:1.1}
.ph{width:380px;height:380px;border-radius:50%;border:10px solid #FFC72C;object-fit:cover;display:block;margin:30px auto 0}
.n{width:78px;height:78px;border-radius:50%;background:#C1121F;color:#fff;display:flex;align-items:center;justify-content:center;font-size:46px;flex:none}"""
def page(body): return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{body}<div class="foot"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">rabaisflashqc.ca · Rabais Flash : peut changer à tout moment, durée non garantie</div></div></body></html>'
b1 = f'<h1 class="an">BIENVENUE!</h1><h2>Les meilleurs rabais d\'Amazon.ca, triés pour toi 🍁</h2><img class="ph" src="{LEA}"><div style="padding:34px 56px 0;display:flex;flex-direction:column;gap:16px"><div class="card" style="padding:34px 30px"><span style="font-size:60px">⚡</span><div class="t" style="font-size:44px">Mis à jour plusieurs fois par jour</div></div><div class="card" style="padding:34px 30px"><span style="font-size:60px">🍁</span><div class="t" style="font-size:44px">Une page faite au Québec</div></div></div>'
picks, _ = build.top5()
rows = "".join(f'<div class="card" style="margin-bottom:12px;padding:18px 26px"><div class="n an">{i}</div><div style="flex:1;min-width:0"><div style="font-size:26px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(d["brand"])}</div><div style="font-size:33px;font-weight:700;line-height:1.1">{e(pack.short(d["name"],40))}</div></div><div style="background:#FFC72C;color:#8E0B16;border-radius:18px;padding:10px 16px;font-family:Anton,Impact,sans-serif;font-size:42px">{e(pack.pct_txt(d))}</div></div>' for i, d in enumerate(picks, 1))
b2 = f'<h1 class="an" style="font-size:88px">LE TOP 5 DU JOUR ⭐</h1><h2>Nos coups de cœur du moment</h2><div style="padding:30px 56px 0">{rows}</div>'
steps = [("1","On repère les rabais sur Amazon.ca","🔎"),("2","On les trie par thème pour toi","📂"),("3","Tu cliques et tu vérifies le prix final sur Amazon.ca","✅")]
c = "".join(f'<div class="card" style="margin-bottom:22px;padding:34px 30px"><div class="n an">{n}</div><div class="t">{e(t)}</div><span style="font-size:60px;margin-left:auto">{i}</span></div>' for n,t,i in steps)
b3 = f'<h1 class="an">COMMENT<br>ÇA MARCHE?</h1><h2>Simple, gratuit, sans inscription</h2><div style="padding:34px 56px 0">{c}<p style="font-size:28px;font-weight:700;line-height:1.25;margin-top:6px">{e(build.DISCLOSURE)} Ça ne change rien au prix que tu paies.</p></div>'
tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for name, body in (("lancement-1-bienvenue", b1), ("lancement-2-top5", b2), ("lancement-3-comment", b3)):
        br, ctx, pg = pack.render(pw, page(body).replace("—", ","), (1080, 1350), tmp, name)
        pg.wait_for_timeout(700); pg.screenshot(path=str(OUT / f"{name}.png")); ctx.close(); br.close()
print("ok")
