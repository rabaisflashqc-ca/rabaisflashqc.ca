#!/usr/bin/env python3
"""4 réels Black Friday (27-30 nov.). SANS SON, 9:16 : les produits les plus populaires en rabais (prix et popularité vérifiés sur les fiches produit le 26 nov.), photos officielles de marque.
Sortie : docs/pack-du-jour/reel-bf-*.mp4"""
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

def doc(inner, bg="#FFF7E8", foot='rabaisflashqc.ca · <b>lien dans la bio</b>', q="🔎 Tape ton produit ici"):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>'
            f'<div class="url"><b>RABAISFLASHQC.CA</b><div class="sb"><span>{q}</span><i>Trouve-moi un deal</i></div></div>'
            f'<div class="body">{inner}</div><div class="foot">{foot}</div></body></html>')

def card(a, brand, titre, p, w, tag, preuve):
    pct = round((w - p) / w * 100)
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
def hook(l1, l2, l3="", bg="#C1121F"):
    return doc(f'<div style="text-align:center"><div class="big y" style="font-size:150px;line-height:1.02">{l1}</div>'
               f'<div class="big" style="font-size:96px;color:#fff;margin-top:36px;line-height:1.05">{l2}</div>'
               f'<div style="font-size:60px;color:#FFE4B0;margin-top:40px">{l3}</div></div>', bg=bg, foot='Vendredi fou · <b>27 au 30 nov.</b>')
DISC = '<div style="font-size:30px;color:#fff;opacity:.85;margin-top:40px;padding:0 40px;line-height:1.1">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.</div>'
def cta(l1, l2):
    return doc(f'<div style="text-align:center;margin-top:30px"><div class="big y" style="font-size:132px;line-height:1.02">{l1}</div>'
          f'<div style="font-size:66px;color:#fff;margin-top:44px">{l2}</div>'
          '<div class="big" style="display:inline-block;background:#FFC21A;color:#3D0A10;border-radius:40px;padding:26px 60px;font-size:92px;margin-top:44px;white-space:nowrap">rabaisflashqc.ca</div>'
          '<div style="font-size:54px;color:#FFE4B0;margin-top:36px">Lien dans la bio 👆</div>'+DISC+'</div>', bg="#C1121F", foot='Le site québécois des <b>aubaines</b>')
def search(q, msg, sub=""):
    return doc(f'<div style="text-align:center"><div class="big" style="font-size:118px;line-height:1.04;color:#C1121F">{msg}</div><div style="font-size:60px;margin-top:40px;color:#3D0A10">{sub}</div></div>', q="🔎 "+q)

R = {}
R["1-maison"] = [(hook("4 RABAIS<br>À -40 %", "que les gens<br>achètent vraiment", "Regarde jusqu'au bout 👇"), 2.4),
 (card("B0GN4L93SM","BISSELL","PowerClean, aspirateur balai",107.98,179.99,"🏠 MÉNAGE EXPRESS","Plus de 1 000 achetés le mois dernier"), 2.5),
 (card("B0B38KRTV6","De'Longhi","Magnifica Evo, machine à espresso",599.98,999.99,"☕ BARISTA À LA MAISON","Plus de 1 000 achetés le mois dernier"), 2.5),
 (card("B01MRX9US8","Crest","3D Whitestrips, blanchiment",19.97,34.99,"😁 SOURIRE DES FÊTES","Plus de 10 000 achetés le mois dernier"), 2.5),
 (card("B006W6YHYQ","Greenies","Gâteries dentaires pour chien",31.39,51.99,"🐶 POUR TOUTOU","Plus de 7 000 achetés le mois dernier"), 2.5),
 (cta("TON PRODUIT<br>EST DANS<br>LA BARRE", "Tape-le sur le site et vois<br>s'il est en rabais."), 3.2)]
R["2-enfants"] = [(hook("CADEAUX<br>D'ENFANTS", "avant que<br>ça parte", "Les rabais qui font sourire 🎁"), 2.4),
 (card("B0DN1NFKQW","Hot Wheels","Mario Kart, château de Bowser",47.47,79.38,"🏎️ LE PLUS WOW","Plus de 700 achetés le mois dernier"), 2.5),
 (card("B0CD311Q6J","ZURU","5 Surprise Mini Brands (lot de 2)",15.11,22.99,"🎁 PETIT PRIX","Plus de 3 000 achetés le mois dernier"), 2.5),
 (card("B0FLKLY8LQ","Oral-B","iO Kids, brosse à dents électrique",59.99,119.99,"🪥 MOITIÉ PRIX","Plus de 700 achetés le mois dernier"), 2.5),
 (card("B0G2SYJSJ4","LEGO","Disney Stitch & Scrump",75.78,99.99,"🧱 FAN DE STITCH","Plus de 800 achetés le mois dernier"), 2.5),
 (cta("TROUVE LE<br>CADEAU EN<br>10 SECONDES", "Tape le jouet dans la barre<br>de recherche du site."), 3.2)]
R["3-techno-soins"] = [(hook("-55 %<br>SUR DU TOP<br>VENTES", "Écouteurs, soins, beauté", "Tu vas vouloir ça avant minuit 👇"), 2.4),
 (card("B0BQPNMXQV","JBL","Vibe Beam, écouteurs sans fil",44.98,99.98,"🔥 -55 % : À GRAB","Plus de 5 000 achetés le mois dernier"), 2.5),
 (card("B0DCCJZC9F","Oral-B","iO Series 7, brosse électrique",164.99,299.99,"⭐ HAUT DE GAMME","Plus de 1 000 achetés le mois dernier"), 2.5),
 (card("B07ZHZMXMV","Conair","Fer à lisser double céramique",20.98,29.99,"✨ IDÉE CADEAU","Plus de 3 000 achetés le mois dernier"), 2.5),
 (search("écouteurs sans fil","TAPE TON PRODUIT.<br>VOIS LE RABAIS.","Pas besoin de fouiller 40 pages"), 2.6),
 (cta("RECHERCHE.<br>COMPARE.<br>ÉCONOMISE.", "Le site québécois de référence<br>pour les aubaines."), 3.2)]
# réel général sans produit (5h30, 6h30, 7h30, 9h30)
R["4-general"] = [(hook("BLACK FRIDAY :<br>STOP AU<br>SCROLL", "Tu perds du temps<br>à chercher les rabais?", "Il y a plus simple 👇"), 2.4),
 (search("lave-vaisselle","1 BARRE.<br>TOUS LES DEALS.","Tape ce que tu cherches"), 2.2),
 (search("jouets Lego","TAPE.<br>TROUVE.<br>ÉCONOMISE.","Ça prend 5 secondes"), 2.2),
 (hook("27 · 28<br>29 · 30 NOV.", "Vendredi fou, fin de semaine,<br>Cyber lundi", "Un seul site à garder en tête", bg="#3D0A10"), 2.6),
 (cta("LE SITE QUÉBÉCOIS<br>DE RÉFÉRENCE<br>DES AUBAINES", "Du 27 au 30 nov.<br>Utilise la barre de recherche."), 3.4)]
tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name, slides in R.items():
        fr = []
        for i, (h, _) in enumerate(slides):
            p = tmp / f"{name}-{i}.html"; p.write_text(h)
            pg = br.new_page(viewport={"width": 1080, "height": 1920}); pg.goto(p.as_uri()); pg.wait_for_timeout(300)
            png = tmp / f"{name}-{i}.png"; pg.screenshot(path=str(png)); pg.close(); fr.append(png)
        inp, flt = [], []
        for i, (p, (_, dur)) in enumerate(zip(fr, slides)):
            inp += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]; flt.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30[v{i}]")
        tot = sum(d for _, d in slides)
        flt.append("".join(f"[v{i}]" for i in range(len(fr))) + f"concat=n={len(fr)}:v=1:a=0,format=yuv420p[o]")
        out = OUT / f"reel-bf-{name}.mp4"
        subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-t", f"{tot}", "-an", "-r", "30", "-preset", "veryfast",
                        "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
        subprocess.run(["python3", "-c", "from PIL import Image;import sys;fs=sys.argv[2:];ims=[Image.open(f).resize((300,533)) for f in fs];W=Image.new('RGB',(300*len(ims),533),'white')\nfor i,im in enumerate(ims):W.paste(im,(i*300,0))\nW.save(sys.argv[1])", f"/tmp/planche-{name}.png", *map(str, fr)], check=True)
        print(out.name, tot, "s")
    br.close()
