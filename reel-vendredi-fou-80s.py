#!/usr/bin/env python3
"""(base) 4 réels Black Friday (27-30 nov.). SANS SON, 9:16 : les produits les plus populaires en rabais (prix et popularité vérifiés sur les fiches produit le 26 nov.), photos officielles de marque.
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


import json, base64
IMG = json.load(open("/mnt/user-data/uploads/Downloads/IMG-vendredi-fou.json"))
ITEMS = json.load(open("/tmp/vsel.json"))
TAG = {"tech":"💻 TECHNO","beaute":"✨ BEAUTÉ","jouets":"🧸 JOUETS","maison":"🏠 MAISON","enfants":"👶 BÉBÉ","plein-air":"🏕️ SPORT","animaux":"🐶 ANIMAUX","homme":"🧔 HOMME","femme":"👗 FEMME"}
def short(t, n=46):
    t = t.split(" : ")[0].strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"
def pcard(x):
    img = IMG[x["asin"]]; p = x["price"]; w = x["was"]; pct = x["pct"]
    brand = x["title"].split(" ")[0]
    b = x.get("bought") or 0
    preuve = f"Plus de {b:,} achetés le mois dernier".replace(",", " ") if b >= 1000 else "Rabais vérifié sur Amazon.ca"
    return doc(f'<div style="text-align:center"><div style="display:inline-block;background:#1A1A1A;color:#FFC21A;border-radius:40px;padding:10px 40px;font-size:62px;margin-bottom:34px" class="an">{TAG[x["cat"]]}</div>'
               f'<div style="margin:0 auto;width:760px;height:520px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 8px 0 #E8D9BC">'
               f'<img src="{img}" style="max-width:690px;max-height:470px;object-fit:contain">'
               f'<div class="big" style="position:absolute;top:-34px;right:-24px;background:#FFC21A;color:#8E0B16;border-radius:30px;padding:10px 30px;font-size:110px;transform:rotate(4deg)">-{pct} %</div></div>'
               f'<div style="font-size:50px;margin:30px 0 6px;line-height:1.05">{e(short(x["title"]))}</div>'
               f'<div class="big r" style="font-size:176px">{money(p)}</div>'
               f'<div style="font-size:46px;margin-top:2px">avant : <s>{money(w)}</s></div>'
               f'<div style="display:inline-block;background:#1B7F3B;color:#fff;border-radius:22px;padding:8px 28px;font-size:42px;margin-top:14px">{preuve}</div></div>')
def search(q, msg, sub=""):
    return doc(f'<div style="text-align:center"><div class="big" style="font-size:118px;line-height:1.04;color:#C1121F">{msg}</div><div style="font-size:60px;margin-top:40px;color:#3D0A10">{sub}</div></div>', q="🔎 "+q)
def counter():
    return doc('<div style="text-align:center"><div class="big y" style="font-size:330px;line-height:1;text-shadow:0 8px 0 #8E0B16">+ 7 000</div>'
               '<div class="big" style="font-size:150px;color:#fff;line-height:1.02;margin-top:10px">DEALS</div>'
               '<div style="font-size:64px;color:#FFE4B0;margin-top:44px;line-height:1.12">à portée de main.<br>Une seule barre pour tous les trouver.</div></div>', bg="#C1121F", foot='Vendredi fou · <b>27 au 30 nov.</b>')
def cta2():
    return doc('<div style="text-align:center;margin-top:10px"><div class="big y" style="font-size:118px;line-height:1.02">LE SITE QUÉBÉCOIS<br>DE RÉFÉRENCE<br>EN AUBAINES</div>'
          '<div class="big" style="font-size:96px;color:#fff;margin-top:40px">VIENS ÉCONOMISER !</div>'
          '<div class="big" style="display:inline-block;background:#FFC21A;color:#3D0A10;border-radius:40px;padding:26px 60px;font-size:92px;margin-top:44px;white-space:nowrap">rabaisflashqc.ca</div>'
          '<div style="font-size:54px;color:#FFE4B0;margin-top:34px">Tape ton produit dans la barre 🔎 · Lien dans la bio 👆</div>'+DISC+'</div>', bg="#C1121F", foot='Le site québécois des <b>aubaines</b>')
slides = [(hook("VENDREDI FOU<br>LES DEALS<br>SONT LÀ", "Un seul site à garder en tête", "Regarde jusqu'au bout 👇"), 3.6),
          (counter(), 4.2),
          (search("écouteurs sans fil", "TAPE TON PRODUIT.<br>VOIS LE RABAIS.", "La barre de recherche, c'est notre force"), 3.6)]
Q = ["lave-vaisselle", "LEGO", "souliers de course", "cadeau pour bébé"]
M = ["1 BARRE.<br>+ 7 000 DEALS.", "TAPE.<br>TROUVE.<br>ÉCONOMISE.", "FINI DE FOUILLER<br>40 PAGES", "TON PRODUIT<br>EST DANS<br>LA BARRE"]
S = ["Ça prend 5 secondes", "Vendredi fou jusqu'au 30 nov.", "Tape, compare, clique", "Essaie-la sur rabaisflashqc.ca"]
si = 0
for i, x in enumerate(ITEMS):
    slides.append((pcard(x), 2.45))
    if i in (5, 10, 15, 20) and si < 4:
        slides.append((search(Q[si], M[si], S[si]), 3.0)); si += 1
fixed = sum(d for _, d in slides)
slides.append((cta2(), round(80 - fixed, 2)))
tmp = pathlib.Path(tempfile.mkdtemp())
name = "vendredi-fou-80s"
with sync_playwright() as pw:
    br = pw.chromium.launch(); fr = []
    for i, (h, _) in enumerate(slides):
        p = tmp / f"{i}.html"; p.write_text(h)
        pg = br.new_page(viewport={"width": 1080, "height": 1920}); pg.goto(p.as_uri()); pg.wait_for_timeout(300)
        png = tmp / f"{i}.png"; pg.screenshot(path=str(png)); pg.close(); fr.append(png)
    br.close()
inp, flt = [], []
for i, (p, (_, dur)) in enumerate(zip(fr, slides)):
    inp += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]; flt.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30[v{i}]")
flt.append("".join(f"[v{i}]" for i in range(len(fr))) + f"concat=n={len(fr)}:v=1:a=0,format=yuv420p[o]")
out = OUT / f"reel-{name}.mp4"
subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-an", "-r", "30", "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
print(out, sum(d for _, d in slides), "s", len(slides), "slides")
import shutil
for i in (0, 1, 3, 9, len(fr) - 1): shutil.copy(fr[i], f"/tmp/vf-{i}.png")
