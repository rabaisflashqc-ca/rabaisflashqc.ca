#!/usr/bin/env python3
"""Réel 26 nov. SANS SON, 9:16 : les produits les plus populaires en rabais (prix et popularité vérifiés sur les fiches produit le 26 nov.), photos officielles de marque.
Sortie : docs/pack-du-jour/reel-26nov-top-ventes.mp4"""
import pathlib, tempfile, subprocess, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "docs" / "pack-du-jour"; OUT.mkdir(parents=True, exist_ok=True)
e = H.escape
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;background:#FFF7E8;color:#1A1A1A;position:relative}
.an{font-family:Anton,Impact,'Arial Narrow Bold',sans-serif;font-weight:400}
.url{position:absolute;top:0;left:0;right:0;height:410px;background:#C1121F;text-align:center;padding-top:96px;border-bottom:10px solid #FFC21A}
.sb{margin:22px auto 0;width:900px;background:#fff;border:6px solid #FFC21A;border-radius:60px;padding:14px 34px;font-size:46px;color:#3D0A10;text-align:left;display:flex;justify-content:space-between;align-items:center}.url .sb span{display:inline;color:#3D0A10;font-size:40px;margin:0;letter-spacing:0;white-space:nowrap}.sb{white-space:nowrap}.sb i{white-space:nowrap;font-style:normal;background:#FFC21A;color:#3D0A10;border-radius:40px;padding:6px 26px;font-size:40px}
.url b{display:block;font-family:Anton,Impact,sans-serif;font-weight:400;font-size:112px;color:#FFC21A;letter-spacing:2px;line-height:1}
.url span{display:block;color:#fff;font-size:34px;margin-top:10px;letter-spacing:1px}
.body{position:absolute;top:420px;left:0;right:0;bottom:150px;padding:30px 56px;display:flex;flex-direction:column;justify-content:center}
.foot{position:absolute;left:0;right:0;bottom:0;height:150px;background:#3D0A10;color:#fff;text-align:center;padding-top:34px;font-size:38px}
.foot b{color:#FFC21A}
.big{font-family:Anton,Impact,sans-serif;font-weight:400;line-height:1}
.y{color:#FFC21A}.r{color:#C1121F}
"""

def doc(inner, bg="#FFF7E8", foot='rabaisflashqc.ca · <b>lien dans la bio</b>'):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>'
            f'<div class="url"><b>RABAISFLASHQC.CA</b><div class="sb"><span>🔎 Tape ton produit ici</span><i>Trouve-moi un deal</i></div></div>'
            f'<div class="body">{inner}</div><div class="foot">{foot}</div></body></html>')
# (asin, marque, titre, prix, conseillé, tag, preuve)
P = [("B0764BZBQW","Magic Bullet","Mélangeur 17 pièces",24.99,59.99,"🏆 #1 DES VENTES","Plus de 4 000 achetés le mois dernier"),
     ("B0BWWZP49F","Blink","Mini 2, caméra de surveillance",14.99,54.99,"🔥 -73 % : PRIX FOU","Plus de 1 000 achetés le mois dernier"),
     ("B0DLLGG2Z8","Oral-B","iO2, brosse à dents électrique",59.99,119.99,"🏆 #1 DES VENTES","Plus de 4 000 achetés le mois dernier"),
     ("B0DN45YMP6","JBL","Vibe Beam 2, écouteurs sans fil",49.98,99.98,"⭐ TOP POPULAIRE","Plus de 5 000 achetés le mois dernier"),
     ("B0GT28CSYM","Dyson","V8 Cyclone, aspirateur sans fil",349.99,549.99,"⭐ TOP POPULAIRE","Plus de 3 000 achetés le mois dernier")]
def card(a, brand, titre, p, w, tag, preuve):
    pct = round((w - p) / w * 100); eco = int(w - p)
    img = (ROOT / f"docs/img/p/marque-{a}.jpg").resolve().as_uri()
    return doc(f'<div style="text-align:center"><div style="display:inline-block;background:#1A1A1A;color:#FFC21A;border-radius:40px;padding:10px 40px;font-size:62px;margin-bottom:34px" class="an">{tag}</div>'
               f'<div style="margin:0 auto;width:760px;height:520px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 8px 0 #E8D9BC">'
               f'<img src="{img}" style="max-width:690px;max-height:470px;object-fit:contain">'
               f'<div class="big" style="position:absolute;top:-34px;right:-24px;background:#FFC21A;color:#8E0B16;border-radius:30px;padding:10px 30px;font-size:110px;transform:rotate(4deg)">-{pct} %</div></div>'
               f'<div style="font-size:38px;color:#C1121F;text-transform:uppercase;margin-top:30px">{e(brand)}</div>'
               f'<div style="font-size:52px;margin:4px 0 6px">{e(titre)}</div>'
               f'<div class="big r" style="font-size:176px">{money(p)}</div>'
               f'<div style="font-size:46px;margin-top:2px">prix conseillé : <s>{money(w)}</s></div>'
               f'<div style="display:inline-block;background:#1B7F3B;color:#fff;border-radius:22px;padding:8px 28px;font-size:44px;margin-top:14px">{preuve}</div></div>')
cta = doc('<div style="text-align:center;margin-top:30px"><div class="big y" style="font-size:132px;line-height:1.02">LES DEALS<br>QUE TOUT LE<br>MONDE VEUT</div>'
          '<div style="font-size:68px;color:#fff;margin-top:44px">Tape ton produit dans la barre de recherche<br>et trouve ton rabais.</div>'
          '<div class="big" style="display:inline-block;background:#FFC21A;color:#3D0A10;border-radius:40px;padding:26px 60px;font-size:92px;margin-top:44px;white-space:nowrap">rabaisflashqc.ca</div>'
          '<div style="font-size:54px;color:#FFE4B0;margin-top:36px">Lien dans la bio 👆</div>'
          '<div style="font-size:30px;color:#fff;opacity:.85;margin-top:40px;padding:0 40px;line-height:1.1">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.</div></div>',
          bg="#C1121F", foot='Les rabais qui valent vraiment le <b>clic</b>')
slides = [(card(*x), 2.3) for x in P] + [(cta, 3.0)]
tmp = pathlib.Path(tempfile.mkdtemp()); fr = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for i, (h, _) in enumerate(slides):
        p = tmp / f"s{i}.html"; p.write_text(h)
        pg = br.new_page(viewport={"width": 1080, "height": 1920}); pg.goto(p.as_uri()); pg.wait_for_timeout(400)
        png = tmp / f"s{i}.png"; pg.screenshot(path=str(png)); pg.close(); fr.append(png)
    br.close()
inp, flt = [], []
for i, (p, (_, dur)) in enumerate(zip(fr, slides)):
    inp += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]; flt.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30[v{i}]")
tot = sum(d for _, d in slides)
flt.append("".join(f"[v{i}]" for i in range(len(fr))) + f"concat=n={len(fr)}:v=1:a=0,format=yuv420p[o]")
out = OUT / "reel-26nov-top-ventes.mp4"
subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-t", f"{tot}", "-an", "-r", "30", "-preset", "veryfast",
                "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
subprocess.run(["python3", "-c", "from PIL import Image;import sys;fs=sys.argv[2:];ims=[Image.open(f).resize((360,640)) for f in fs];W=Image.new('RGB',(360*len(ims),640),'white')\n"
                "for i,im in enumerate(ims):W.paste(im,(i*360,0))\nW.save(sys.argv[1])", "/tmp/planche_reel26.png", *map(str, fr)], check=True)
print(out, tot, "s")
