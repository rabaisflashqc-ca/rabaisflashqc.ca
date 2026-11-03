#!/usr/bin/env python3
"""Réels TikTok « Deal du jour #N » : UN deal, ~9 s, 9:16, SANS SON (son tendance ajouté dans l'app).
Stratégie TikTok approuvée par Alex le 3 nov. (voir AUTONOMIE.md).
0 à 1,9 s : prix choc + % (accroche, prix exact) / 1,9 à 6,6 s : fiche du deal / 6,6 à 9,4 s : série + rabaisflashqc.ca.
Usage : modifier DEALS puis python3 reel_deal_du_jour.py"""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e = H.escape
CSS = open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS += (".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}"
        ".big{font-family:Anton,Impact,sans-serif;font-size:230px;color:#C1121F;line-height:1}"
        ".pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:120px;margin:20px 0}"
        ".site{font-family:Anton,Impact,sans-serif;font-size:96px;color:#FFC72C;text-align:center;margin-top:40px}")
JOUR = "2026-11-03"
OB = "3 nov. à 8 h 15"
# (numéro, marque, produit, émoji, ancien prix, nouveau prix, prix court pour l'accroche, %)
DEALS = [
    (1, "JBL", "Écouteurs sans fil Vibe Beam", "🎧", "63,91 $", "44,98 $", "44,98 $", 30),
    (2, "Crayola", "Scribble Scrubbie, animaux à colorier et laver", "🎨", "22,37 $", "15,99 $", "15,99 $", 29),
    (3, "Arlo", "Caméra de sécurité sans fil Essential", "📹", "96,91 $", "69,99 $", "69,99 $", 28),
]
FPS = 30


def page(inner, foot=True):
    f = ('<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">rabaisflashqc.ca</div>'
         '<div class="s">Prix observé le ' + OB + ' · vérifie le prix final sur le site</div></div>') if foot else ''
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head>'
            f'<body style="width:1080px;height:1920px;position:relative">{inner}{f}</body></html>')


def slides_for(n, a, t, ic, av, pr, court, pc):
    s1 = page(f'<div style="font-size:260px;text-align:center;margin-top:260px">{ic}</div>'
              f'<h1 class="an" style="font-size:170px;line-height:1;margin-top:40px;text-align:center">{e(court)} ?! 🤯</h1>'
              f'<h2 style="font-size:84px;text-align:center">{e(a.upper())} · -{pc} %</h2>')
    s2 = page(f'<div class="top" style="padding-top:90px">{pack.BOLT}<span>DEAL DU JOUR <b>#{n}</b></span></div>'
              f'<div style="font-size:180px;text-align:center;margin-top:60px">{ic}</div>'
              f'<div class="c"><div style="font-size:38px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div>'
              f'<div style="font-size:54px;font-weight:700;margin:10px 0 24px">{e(t)}</div>'
              f'<div class="big">{pr}</div><div class="pc">-{pc} %</div>'
              f'<div style="font-size:46px">avant : <s>{av}</s></div>'
              f'<div style="font-size:30px;color:#555;margin-top:18px">prix observé le {OB}</div></div>')
    s3 = page(f'<h1 class="an" style="font-size:118px;line-height:1.1;margin-top:300px">TU L’AURAIS PAYÉ<br>COMBIEN? 👇</h1>'
              f'<h2 style="font-size:62px">Abonne-toi pour le<br>Deal du jour #{n + 1} 🔔</h2>'
              f'<div class="site">rabaisflashqc.ca</div>'
              f'<p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:50px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>', foot=False)
    return [(s1, 1.9), (s2, 4.7), (s3, 2.8)]


tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for d in DEALS:
        n = d[0]
        fr = []
        sl = slides_for(*d)
        for i, (h, _) in enumerate(sl):
            br, ctx, pg = pack.render(pw, h, (1080, 1920), tmp, f"d{n}s{i}")
            pg.wait_for_timeout(500)
            p = tmp / f"d{n}s{i}.png"
            pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
        durs = [x for _, x in sl]
        inp, flt = [], []
        for i, (p, du) in enumerate(zip(fr, durs)):
            inp += ["-loop", "1", "-t", f"{du:.3f}", "-i", str(p)]
            flt.append(f"[{i}:v]scale=1080:1920,fps={FPS},setsar=1[v{i}]")
        k = len(fr)
        flt.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0,format=yuv420p[o]")
        out = pack.OUT / f"tiktok-deal{n}-{JOUR}.mp4"
        subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-an", "-r", str(FPS),
                        "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)],
                       check=True, capture_output=True)
        print(out, round(sum(durs), 1))
