#!/usr/bin/env python3
"""Réel du 22 nov. au soir, SANS SON, 9:16, ~21 s : « plus de 1 500 rabais à saisir ce soir ».
Objectif : attirer des clients vers le site dès les 5 premières secondes (accroche + preuve), adresse du site toujours en haut,
4 exemples avec photos officielles de marque (jamais de photo Amazon dans un réel), démo de la barre de recherche, appel à l'action.
Prix = suivi/deals_chrome.json (lus dans Keepa et sur la page Vendredi fou le 22 nov.). Nombre de rabais = docs/recherche.json.
Usage : python3 reel-22nov-1500-deals.py   ->  docs/pack-du-jour/reel-25nov-2900-intelligent.mp4 (+ planche PNG des écrans)"""
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

EX = [("B08DJ8Z3WH","Shark","Navigator Swivel Pro, aspirateur"),("B0CHBNXJ24","Ninja","CREAMi XL, machine à glace 11 en 1"),
      ("B0B38KRTV6","De'Longhi","Magnifica Evo, machine à espresso"),("B0DN45YMP6","JBL","Vibe Beam 2, écouteurs sans fil"),
      ("B0DCCJZC9F","Oral-B","iO Série 7, brosse à dents électrique"),("B0G2STSGW3","LEGO","Star Wars, AT-AT en pain d'épice"),
      ("B0BWWZP49F","Blink","Mini 2, caméra de surveillance")]
for a,*_ in EX: assert (ROOT/f"docs/img/p/marque-{a}.jpg").exists(), a
N = len(idx); NTXT = f"{N:,}".replace(",", " ")

res = sorted([x for x in idx if re.search(r"\bJBL\b", x["t"]) and x["p"] < 100], key=lambda x: -x["r"])
rows = res[:3]; nres = len(res)
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

s1 = doc(f'<div style="text-align:center"><div class="big" style="font-size:100px;color:#FFE4B0;line-height:1">PLUS DE</div><div class="big y" style="font-size:300px;text-shadow:6px 6px 0 #8E0B16;line-height:1">{NRND}</div>'
         f'<div class="big" style="font-size:150px;color:#fff;line-height:1.02">DEALS TRIÉS</div>'
         f'<div style="font-size:64px;color:#fff;margin-top:40px">+ une barre de recherche<br><span class="y">intelligente</span></div></div>', bg="#C1121F")
s2 = doc(f'<div style="text-align:center"><div class="big r" style="font-size:130px;line-height:1.02">VENDREDI FOU :<br>TU NE RATERAS<br>RIEN</div>'
         f'<div style="font-size:66px;margin-top:56px;color:#3D0A10">On trie, on compare,<br>tu trouves ton deal en 1 seconde 👇</div></div>')
s_why = doc(f'<div style="text-align:center"><div class="big" style="font-size:118px;line-height:1.04">SI ÇA VAUT<br>VRAIMENT<br><span class="r">LE CLIC,</span><br>ON TE LE DIT</div>'
            f'<div style="font-size:60px;margin-top:50px;color:#3D0A10">Les vrais rabais, sans le bruit.</div></div>')

# --- exemples ---
def ex(k, a, brand, titre):
    d = deals[a]; ref = bool(d.get("ref")); eco = int(d["was"] - d["price"])
    img = (ROOT / f"docs/img/p/marque-{a}.jpg").resolve().as_uri()
    avant = (f'prix conseillé : <s>{money(d["was"])}</s>' if ref else f'avant : <s>{money(d["was"])}</s>')
    badge = (f'Tu sauves {eco} $ sous le prix conseillé' if ref else f'Tu économises {eco} $')
    return doc(f'<div style="text-align:center"><div style="margin:0 auto;width:760px;height:560px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 8px 0 #E8D9BC">'
               f'<img src="{img}" style="max-width:690px;max-height:500px;object-fit:contain">'
               f'<div class="big" style="position:absolute;top:-34px;right:-24px;background:#FFC21A;color:#8E0B16;border-radius:30px;padding:10px 30px;font-size:110px;transform:rotate(4deg)">-{d["pct"]} %</div></div>'
               f'<div style="font-size:38px;color:#C1121F;text-transform:uppercase;margin-top:34px">{e(brand)}</div>'
               f'<div style="font-size:54px;margin:4px 0 8px">{e(titre)}</div>'
               f'<div class="big r" style="font-size:180px">{money(d["price"])}</div>'
               f'<div style="font-size:48px;margin-top:4px">{avant}</div>'
               f'<div style="display:inline-block;background:#1B7F3B;color:#fff;border-radius:22px;padding:8px 28px;font-size:46px;margin-top:16px">{badge}</div></div>')
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
s_cta = doc(f'<div style="text-align:center;margin-top:30px"><div class="big y" style="font-size:150px;line-height:1.02">{NTXT} DEALS<br>T’ATTENDENT</div>'
            f'<div style="font-size:70px;color:#fff;margin-top:44px">Tape ce que tu veux dans la barre de recherche<br>et saisis ton rabais avec le Vendredi fou.</div>'
            f'<div class="big" style="display:inline-block;background:#FFC21A;color:#3D0A10;border-radius:40px;padding:26px 60px;font-size:92px;margin-top:44px;white-space:nowrap">rabaisflashqc.ca</div>'
            f'<div style="font-size:54px;color:#FFE4B0;margin-top:36px">Lien dans la bio 👆 Partage-le à qui magasine</div>'
            f'<div style="font-size:30px;color:#fff;opacity:.85;margin-top:40px;padding:0 40px;line-height:1.1">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.</div></div>',
            bg="#C1121F", foot='Les rabais qui valent vraiment le <b>clic</b>')

slides = [(s1, 2.6), (s2, 2.4), (s_search1, 2.6), (s_search2, 3.0), (s_why, 2.4)] + [(h, 1.9) for h in exs[:4]] + [(s_cta, 3.2)]
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
out = OUT / "reel-25nov-2900-intelligent.mp4"
subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-t", f"{tot}", "-an", "-r", "30", "-preset", "veryfast",
                "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
# planche de contrôle (pas publiée)
subprocess.run(["python3", "-c", "from PIL import Image;import sys;fs=sys.argv[2:];ims=[Image.open(f).resize((270,480)) for f in fs];W=Image.new('RGB',(270*5,480*3),'white')\n"
                "for i,im in enumerate(ims):W.paste(im,((i%5)*270,(i//5)*480))\nW.save(sys.argv[1])", "/tmp/planche_reel5.png", *map(str, fr)], check=True)
print(out, tot, "s", "| N =", N, "| arrondi", NRND, "| résultats JBL", nres)
