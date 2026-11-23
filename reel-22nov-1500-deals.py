#!/usr/bin/env python3
"""Réel du 22 nov. au soir, SANS SON, 9:16, ~21 s : « plus de 1 500 rabais à saisir ce soir ».
Objectif : attirer des clients vers le site dès les 5 premières secondes (accroche + preuve), adresse du site toujours en haut,
4 exemples avec photos officielles de marque (jamais de photo Amazon dans un réel), démo de la barre de recherche, appel à l'action.
Prix = suivi/deals_chrome.json (lus dans Keepa et sur la page Vendredi fou le 22 nov.). Nombre de rabais = docs/recherche.json.
Usage : python3 reel-22nov-1500-deals.py   ->  docs/pack-du-jour/reel-22nov-1500-deals.mp4 (+ planche PNG des écrans)"""
import json, re, pathlib, tempfile, subprocess, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "docs" / "pack-du-jour"; OUT.mkdir(parents=True, exist_ok=True)
e = H.escape
deals = {d["asin"]: d for d in json.load(open(ROOT / "suivi/deals_chrome.json"))}
idx = json.load(open(ROOT / "docs/recherche.json"))
N = len(idx); NTXT = f"{N:,}".replace(",", " ")
NRND = f"{(N // 100) * 100:,}".replace(",", " ")          # « 1 500 » : arrondi vers le bas, jamais plus que la réalité
MAXP = max(x["r"] for x in idx)
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"

# 4 exemples : vrais anciens prix (pas de « prix conseillé »), photo officielle de marque déjà approuvée (docs/img/p/marque-ASIN.jpg)
EX = [("B0DDQKXDZF", "Beats", "Studio Pro, casque antibruit"), ("B0DCCJZC9F", "Oral-B", "iO Série 7, brosse à dents électrique"),
      ("B0DN45YMP6", "JBL", "Vibe Beam 2, écouteurs sans fil"), ("B0764BZBQW", "Magic Bullet", "Mélangeur et mixeur")]
for a, _, _ in EX:
    d = deals[a]; assert not d.get("ref") and (ROOT / f"docs/img/p/marque-{a}.jpg").exists(), a

# démo de recherche : « JBL sous 100 $ » = vraie requête du chercheur du site, vrais résultats
res = sorted([x for x in idx if re.search(r"\bJBL\b", x["t"]) and x["p"] < 100], key=lambda x: -x["r"])
rows = res[:3]; nres = len(res)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;background:#FFF7E8;color:#1A1A1A;position:relative}
.an{font-family:Anton,Impact,'Arial Narrow Bold',sans-serif;font-weight:400}
.url{position:absolute;top:0;left:0;right:0;height:300px;background:#C1121F;text-align:center;padding-top:120px;border-bottom:10px solid #FFC21A}
.url b{display:block;font-family:Anton,Impact,sans-serif;font-weight:400;font-size:112px;color:#FFC21A;letter-spacing:2px;line-height:1}
.url span{display:block;color:#fff;font-size:34px;margin-top:10px;letter-spacing:1px}
.body{position:absolute;top:310px;left:0;right:0;bottom:150px;padding:30px 56px;display:flex;flex-direction:column;justify-content:center}
.foot{position:absolute;left:0;right:0;bottom:0;height:150px;background:#3D0A10;color:#fff;text-align:center;padding-top:34px;font-size:38px}
.foot b{color:#FFC21A}
.big{font-family:Anton,Impact,sans-serif;font-weight:400;line-height:1}
.y{color:#FFC21A}.r{color:#C1121F}
"""
def doc(inner, bg="#FFF7E8", foot='Les liens sont sur le site · <b>lien dans la bio</b>'):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>'
            f'<div class="url"><b>RABAISFLASHQC.CA</b><span>⚡ RABAIS FLASH QC · LES RABAIS QUI VALENT VRAIMENT LE CLIC</span></div>'
            f'<div class="body">{inner}</div><div class="foot">{foot}</div></body></html>')

# --- 0 à 5 s : accroche + preuve ---
s1 = doc(f'<div style="text-align:center;margin-top:0"><div class="big y" style="font-size:330px;text-shadow:6px 6px 0 #8E0B16">+{NRND}</div>'
         f'<div class="big" style="font-size:150px;color:#fff;line-height:1.02;margin-top:10px">RABAIS À SAISIR<br>CE SOIR</div>'
         f'<div style="font-size:76px;color:#fff;margin-top:50px">Jusqu’à <span class="y">-{MAXP} %</span> 🔥</div>'
         f'<div style="font-size:54px;color:#FFE4B0;margin-top:30px">Déjà triés pour toi, avec photos</div></div>', bg="#C1121F")
chips = ["MODE", "MAISON", "TECH", "BEAUTÉ", "JOUETS", "PLEIN AIR", "ANIMAUX"]
s2 = doc(f'<div style="text-align:center;margin-top:20px"><div class="big r" style="font-size:300px">{NTXT}</div>'
         f'<div class="big" style="font-size:96px;line-height:1.05;margin-top:6px">RABAIS TRIÉS<br>PAR TYPE ET PAR PRIX</div>'
         f'<div style="margin-top:50px;display:flex;flex-wrap:wrap;gap:18px;justify-content:center">'
         + "".join(f'<span style="background:#fff;border:5px solid #C1121F;border-radius:60px;padding:14px 34px;font-size:50px;color:#C1121F">{c}</span>' for c in chips)
         + '</div><div style="font-size:62px;margin-top:56px;color:#3D0A10">Tu vois le prix, le rabais et ce que tu sauves.</div></div>')

# --- exemples ---
def ex(k, a, brand, titre):
    d = deals[a]; eco = int(d["was"] - d["price"])
    img = (ROOT / f"docs/img/p/marque-{a}.jpg").resolve().as_uri()
    return doc(f'<div style="text-align:center"><div class="big r" style="font-size:64px;margin-bottom:46px">EXEMPLE {k}/4 ⚡</div>'
               f'<div style="margin:0 auto;width:700px;height:560px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 8px 0 #E8D9BC">'
               f'<img src="{img}" style="max-width:620px;max-height:500px;object-fit:contain">'
               f'<div class="big" style="position:absolute;top:-34px;right:-24px;background:#FFC21A;color:#8E0B16;border-radius:30px;padding:10px 30px;font-size:104px;transform:rotate(4deg)">-{d["pct"]} %</div></div>'
               f'<div style="font-size:36px;color:#C1121F;text-transform:uppercase;margin-top:34px">{e(brand)}</div>'
               f'<div style="font-size:56px;margin:4px 0 14px">{e(titre)}</div>'
               f'<div class="big r" style="font-size:190px">{money(d["price"])}</div>'
               f'<div style="font-size:50px;margin-top:6px">avant : <s>{money(d["was"])}</s></div>'
               f'<div style="display:inline-block;background:#1B7F3B;color:#fff;border-radius:22px;padding:8px 30px;font-size:54px;margin-top:20px">Tu économises {eco} $</div></div>')
exs = [ex(i + 1, *x) for i, x in enumerate(EX)]

# --- démo de la barre de recherche (même chercheur que sur le site) ---
bar = lambda txt, cur: (f'<div style="background:#fff;border-radius:34px;padding:34px 36px;box-shadow:0 8px 0 #E8D9BC;text-align:left">'
                        f'<div style="font-size:34px;color:#1B7F3B">🔎 Le chercheur de rabais · {NTXT} deals à fouiller</div>'
                        f'<div style="border:5px solid #FFC21A;border-radius:24px;padding:26px 28px;font-size:66px;margin-top:18px;min-height:122px;color:{"#1A1A1A" if txt else "#9a9a9a"}">'
                        f'{e(txt) if txt else "Ex. : casque Sony, LEGO sous 50 $"}{"<span style=color:#C1121F>|</span>" if cur else ""}</div>'
                        f'<div style="background:#FFC21A;color:#3D0A10;border-radius:24px;text-align:center;font-size:60px;padding:20px;margin-top:18px">Trouve-moi un deal 👉</div></div>')
s_search1 = doc(f'<div style="text-align:center"><div class="big" style="font-size:124px;line-height:1.02;margin-bottom:34px">UTILISE LA<br><span class="r">BARRE DE RECHERCHE</span></div>'
                f'{bar("", True)}<div style="font-size:54px;margin-top:40px;color:#3D0A10">Une marque, un produit, un budget : tape-le.</div>'
                f'<div style="margin-top:26px;display:flex;flex-wrap:wrap;gap:16px;justify-content:center">'
                + "".join(f'<span style="background:#fff;border:4px solid #C1121F;border-radius:50px;padding:10px 28px;font-size:44px;color:#C1121F">{c}</span>' for c in ["Dyson", "LEGO", "Sony", "JBL", "Levi’s", "sous 50 $"])
                + '</div></div>')
rws = "".join(f'<div style="background:#fff;border-radius:26px;padding:20px 26px;margin-top:16px;display:flex;justify-content:space-between;align-items:center;text-align:left;box-shadow:0 6px 0 #E8D9BC">'
              f'<div style="font-size:42px;width:560px;line-height:1.05">{e(re.sub(chr(32)+"-"+chr(32)+".*$", "", x["t"])[:44])}</div>'
              f'<div style="text-align:right"><div class="big r" style="font-size:78px">{money(x["p"])}</div><div style="font-size:34px;color:#1B7F3B">-{x["r"]} % · tu sauves {x["e"]} $</div></div></div>' for x in rows)
s_search2 = doc(f'<div style="text-align:center"><div class="big" style="font-size:124px;line-height:1.02;margin-bottom:34px">EN 1 SECONDE,<br><span class="r">TOUT EST TRIÉ</span></div>'
                f'{bar("JBL sous 100 $", False)}<div style="font-size:50px;margin-top:26px;color:#3D0A10">{nres} rabais trouvés. Voici les 3 plus forts :</div>{rws}</div>')

# --- appel à l'action ---
s_cta = doc(f'<div style="text-align:center;margin-top:30px"><div class="big y" style="font-size:150px;line-height:1.02">CE SOIR,<br>LES {NRND}+ RABAIS<br>SONT LÀ</div>'
            f'<div style="font-size:70px;color:#fff;margin-top:44px">Entre sur le site, tape ce que tu veux,<br>et saisis ton rabais avant que le prix remonte.</div>'
            f'<div class="big" style="display:inline-block;background:#FFC21A;color:#3D0A10;border-radius:40px;padding:26px 60px;font-size:92px;margin-top:44px;white-space:nowrap">rabaisflashqc.ca</div>'
            f'<div style="font-size:54px;color:#FFE4B0;margin-top:36px">Lien dans la bio 👆 Partage-le à qui magasine</div>'
            f'<div style="font-size:30px;color:#fff;opacity:.85;margin-top:40px;padding:0 40px;line-height:1.1">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.</div></div>',
            bg="#C1121F", foot='Les rabais qui valent vraiment le <b>clic</b>')

slides = [(s1, 2.6), (s2, 2.6)] + [(h, 2.1) for h in exs] + [(s_search1, 2.4), (s_search2, 3.2), (s_cta, 3.0)]
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
out = OUT / "reel-22nov-1500-deals.mp4"
subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-t", f"{tot}", "-an", "-r", "30", "-preset", "veryfast",
                "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
# planche de contrôle (pas publiée)
subprocess.run(["python3", "-c", "from PIL import Image;import sys;fs=sys.argv[2:];ims=[Image.open(f).resize((270,480)) for f in fs];W=Image.new('RGB',(270*5,480*2),'white')\n"
                "for i,im in enumerate(ims):W.paste(im,((i%5)*270,(i//5)*480))\nW.save(sys.argv[1])", "/tmp/planche_reel.png", *map(str, fr)], check=True)
print(out, tot, "s", "| N =", N, "| arrondi", NRND, "| résultats JBL", nres)
