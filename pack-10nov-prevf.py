#!/usr/bin/env python3
"""Packs « pré-Vendredi fou » du 10 nov. (soir) et du 11 nov. (matin) : réel 9:16 SANS SON + image Facebook 1080x1350.
Photos officielles des marques ou grands détaillants (jamais Amazon), via suivi/photos_sources.json + photos.yml.
Prix : deals_chrome.json, lus le 10 nov. à 19 h 46 (Keepa) et 19 h 55 (page Vendredi fou d'Amazon envoyée par Alex).
Usage : python3 pack-10nov-prevf.py"""
import pathlib, tempfile, subprocess, json, html as H
import pack
from playwright.sync_api import sync_playwright
e = H.escape
CSS = open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS += (".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:26px 56px;padding:40px 44px;text-align:center}"
        ".big{font-family:Anton,Impact,sans-serif;font-size:190px;color:#C1121F;line-height:1}"
        ".pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:8px 30px;font-family:Anton,Impact,sans-serif;font-size:100px;margin:16px 0}")
SRC = {x["asin"]: x for x in json.load(open("suivi/deals_chrome.json"))}
PACKS = {
    "soir": dict(titre="LES OFFRES<br>PRÉ-VENDREDI FOU<br>SONT LÀ 🔥", sous="5 rabais jusqu’à -55 %",
                 deals=[("Sony", "Casque à réduction de bruit WH-CH720N", "B0BS1QCFHX"), ("JBL", "Écouteurs sans fil Vibe Beam", "B0BQPNMXQV"),
                        ("adidas", "Bas coussinés pour homme, 6 paires", "B008YA0Z44"), ("JBL", "Écouteurs sport Endurance Race 2", "B0DVTGBCBL"),
                        ("Ninja", "Four grille-pain rabattable et friteuse à air", "B0DBNTYL27")]),
    "matin": dict(titre="5 CADEAUX<br>À RABAIS AVANT<br>LE VENDREDI FOU 🎁", sous="Jusqu’à -51 % ce matin",
                  deals=[("Sony", "Casque sans fil WH-CH520", "B0BS1RT9S2"), ("JBL", "Haut-parleur Bluetooth Clip 5", "B0CTP56C5R"),
                         ("Conair", "Fer à friser double céramique", "B07ZL9MXKN"), ("JBL", "Casque à réduction de bruit Tune 770NC", "B0CTB8GKM2"),
                         ("MyPet", "Barrière portative pour chien", "B0746RGRL3")]),
}
OB = "10 nov."
def fr(v): return f"{v:,.2f}".replace(",", " ").replace(".", ",") + " $"
def img(a): return (pathlib.Path("docs/img/p") / f"marque-{a}.jpg").resolve().as_uri()
def page(inner, w=1080, h=1920, foot=True, top=80):
    f = ('<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">rabaisflashqc point ca</div>'
         f'<div class="s">Prix observés le {OB} · vérifie le prix final sur le site</div></div>') if foot else ""
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head>'
            f'<body style="width:{w}px;height:{h}px;position:relative"><div class="top" style="padding-top:{top}px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}{f}</body></html>')
BPM = 124; B = 60 / BPM
tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for nom, P in PACKS.items():
        D = [(m, t, a, SRC[a]) for m, t, a in P["deals"]]
        # Image Facebook / Instagram 1080x1350
        cards = "".join(
            f'<div style="background:#fff;border-radius:26px;display:flex;align-items:center;gap:20px;padding:8px 18px;margin:0 0 12px">'
            f'<img src="{img(a)}" style="width:124px;height:124px;object-fit:contain"><div style="flex:1;color:#1A1A1A">'
            f'<div style="font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(m)}</div><div style="font-size:28px;font-weight:700;line-height:1.12">{e(t)}</div>'
            f'<div style="font-size:26px;margin-top:4px"><s>{fr(s["was"])}</s> <b style="font-family:Anton,Impact,sans-serif;font-size:42px;color:#C1121F">{fr(s["price"])}</b></div></div>'
            f'<div style="font-family:Anton,Impact,sans-serif;font-size:54px;background:#FFC72C;color:#8E0B16;border-radius:18px;padding:6px 14px">-{s["pct"]}%</div></div>'
            for m, t, a, s in D)
        h = page(f'<h1 class="an" style="font-size:58px;line-height:1.05;margin:6px 40px 0;text-align:center">{P["titre"].replace("<br>", " ")}</h1>'
                 f'<div style="margin:16px 46px 0">{cards}</div>', 1080, 1350, top=40)
        br, ctx, pg = pack.render(pw, h, (1080, 1350), tmp, f"i{nom}"); pg.wait_for_timeout(700)
        pg.screenshot(path=str(pack.OUT / f"image-prevf-{nom}-{'10' if nom == 'soir' else '11'}nov.png")); ctx.close(); br.close()
        # Réel 9:16 sans son
        slides = [(page(f'<h1 class="an" style="font-size:118px;line-height:1.05;margin-top:250px;text-align:center">{P["titre"]}</h1><h2 style="font-size:62px;text-align:center">{P["sous"]}</h2>'), 5)]
        for m, t, a, s in D:
            slides.append((page(f'<div style="margin:60px auto 0;width:640px;height:540px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center">'
                                f'<img src="{img(a)}" style="max-width:580px;max-height:500px;object-fit:contain"></div><div class="c">'
                                f'<div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(m)}</div><div style="font-size:50px;font-weight:700;margin:8px 0 18px">{e(t)}</div>'
                                f'<div class="big">{fr(s["price"])}</div><div class="pc">-{s["pct"]} %</div><div style="font-size:44px">avant : <s>{fr(s["was"])}</s></div></div>'), 5))
        slides.append((page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:300px;text-align:center">VENDREDI FOU<br>LE 27 NOV. ⏳</h1>'
                            '<h2 style="font-size:58px;text-align:center">Enregistre et partage<br>à quelqu’un qui magasine 🎄</h2>'), 5))
        slides.append((page('<h1 class="an" style="font-size:112px;line-height:1.1;margin-top:300px;text-align:center">TOUS LES DEALS<br>SUR LE SITE 👇</h1><h2 style="font-size:66px;text-align:center">rabaisflashqc.ca</h2>'
                            '<p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>', foot=False), 6))
        fr_ = []
        for i, (hh, _) in enumerate(slides):
            br, ctx, pg = pack.render(pw, hh, (1080, 1920), tmp, f"{nom}{i}"); pg.wait_for_timeout(500)
            p = tmp / f"{nom}{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr_.append(p)
        durs = [n * B for _, n in slides]; total = sum(durs)
        out = pack.OUT / f"reel-prevf-{nom}-{'10' if nom == 'soir' else '11'}nov-sans-son.mp4"
        inp, flt = [], []
        for i, (p, d) in enumerate(zip(fr_, durs)):
            inp += ["-loop", "1", "-t", f"{d:.4f}", "-i", str(p)]; flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
        n = len(fr_); flt.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
        subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-t", f"{total:.3f}", "-an", "-r", "30",
                        "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
        print(out, round(total, 1))
