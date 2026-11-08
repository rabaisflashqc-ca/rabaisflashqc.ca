#!/usr/bin/env python3
"""Mini réels TikTok de 5 s (matin, midi, soir), SANS SON (son tendance ajouté dans l'app).
Pour l'audience qui regarde 3 à 5 s et ne peut pas cliquer : TOUT est visible dès la 1re image
(photo officielle de la marque, prix, %, et rabaisflashqc.ca en gros en haut, en permanence).
0 à 2,6 s : le deal. 2,6 à 5 s : « Tape rabaisflashqc.ca » + question qui fait commenter. Boucle propre.
Usage : modifier JOUR, OB et DEALS puis python3 tiktok_mini.py"""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e = H.escape
JOUR = "2026-11-08"
OB = "7 nov. à 19 h 34"
# (créneau, marque, produit, ASIN, ancien prix, nouveau prix, %)
DEALS = [
    ("matin", "Levi's", "Jeans 505 coupe régulière pour homme", "B08P55W5DW", "72,40 $", "37,03 $", 49),
    ("midi", "JBL", "Casque à réduction de bruit Tune 770NC", "B0CTB8GKM2", "153,14 $", "79,98 $", 48),
    ("soir", "Nespresso", "Machine à café Vertuo Pop+ Deluxe", "B0D712DKKD", "159,78 $", "94,00 $", 41),
]
FPS = 30
CSS = ("*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;background:#C1121F;color:#fff;position:relative;overflow:hidden;"
       "font-family:'Barlow Semi Condensed',sans-serif;text-align:center}.an{font-family:Anton,Impact,sans-serif}"
       ".site{background:#FFC72C;color:#8E0B16;font-family:Anton,Impact,sans-serif;font-size:92px;padding:150px 0 26px;letter-spacing:1px}"
       ".ph{margin:50px auto 0;width:880px;height:760px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center}"
       ".ph img{width:800px;height:700px;object-fit:contain}"
       ".pc{position:absolute;top:230px;right:20px;background:#FFC72C;color:#8E0B16;border-radius:50%;width:300px;height:300px;"
       "display:flex;align-items:center;justify-content:center;font-family:Anton,Impact,sans-serif;font-size:118px;transform:rotate(-10deg);box-shadow:0 10px 30px rgba(0,0,0,.35)}"
       ".big{font-family:Anton,Impact,sans-serif;font-size:270px;line-height:1;margin-top:50px;color:#fff;text-shadow:0 8px 0 #8E0B16}"
       ".av{font-size:62px;font-weight:700;margin-top:6px}.nm{font-size:56px;font-weight:700;margin-top:24px;padding:0 60px;line-height:1.1}"
       ".ob{position:absolute;bottom:60px;left:0;right:0;font-size:30px;font-weight:600;opacity:.9}")


def page(inner, ob=True):
    o = f'<div class="ob">Prix observé le {OB} · peut changer · vérifie le prix final sur le site</div>' if ob else ''
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head>'
            f'<body><div class="site">rabaisflashqc.ca</div>{inner}{o}</body></html>')


def slides_for(slot, a, t, asin, av, pr, pc):
    img = (pathlib.Path('docs/img/p') / f'marque-{asin}.jpg').resolve().as_uri()
    s1 = page(f'<div class="ph"><img src="{img}"></div><div class="pc">-{pc}%</div>'
              f'<div class="big">{pr}</div><div class="av">au lieu de <s>{av}</s></div>'
              f'<div class="nm">{e(a.upper())} · {e(t)}</div>')
    s2 = page(f'<div class="ph" style="height:600px"><img src="{img}" style="height:540px"></div><div class="pc">-{pc}%</div>'
              f'<h1 class="an" style="font-size:110px;line-height:1.1;margin-top:60px;color:#FFC72C">TAPE 🔎<br>rabaisflashqc.ca</h1>'
              f'<div style="font-size:70px;font-weight:700;margin-top:40px">{pr} au lieu de {av}</div>'
              f'<div style="font-size:70px;font-weight:700;margin-top:34px">Tu l’aurais payé combien? 👇</div>'
              f'<div style="font-size:28px;margin-top:40px;padding:0 80px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</div>')
    return [(s1, 2.6), (s2, 2.4)]


tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for d in DEALS:
        slot = d[0]
        sl = slides_for(*d)
        fr = []
        for i, (h, _) in enumerate(sl):
            br, ctx, pg = pack.render(pw, h, (1080, 1920), tmp, f"{slot}{i}")
            pg.wait_for_timeout(500)
            p = tmp / f"{slot}{i}.png"
            pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
        inp, flt = [], []
        for i, (p, (_, du)) in enumerate(zip(fr, sl)):
            inp += ["-loop", "1", "-t", f"{du:.3f}", "-i", str(p)]
            flt.append(f"[{i}:v]scale=1080:1920,fps={FPS},setsar=1[v{i}]")
        k = len(fr)
        flt.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0,format=yuv420p[o]")
        out = pack.OUT / f"tiktok-mini-{slot}-{JOUR}.mp4"
        subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-an", "-r", str(FPS),
                        "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)],
                       check=True, capture_output=True)
        print(out, sum(x for _, x in sl))
