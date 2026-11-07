#!/usr/bin/env python3
"""Réels « punchy » SANS SON (son tendance ajouté dans l'app), demande d'Alex du 6 nov. au soir.
- Vraies photos officielles des marques ou de grands détaillants (docs/img/p/marque-ASIN.jpg), jamais Amazon.
- rabaisflashqc.ca visible EN TOUT TEMPS (bandeau jaune en haut de chaque image).
- Coupes rapides (~1,6 s), léger zoom continu pour donner du mouvement.
Sorties : reel-punchy-JOUR.mp4 (Facebook/Instagram, 6 deals) + tiktok-punchy-N-JOUR.mp4 (1 deal chacun)."""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e = H.escape
JOUR = "2026-11-06"
OB = "6 nov. à 19 h 21"
# (asin, marque, produit, ancien, nouveau, %, accroche courte)
DEALS = [
    ("B0DVTGBCBL", "JBL", "Écouteurs sport Endurance Race 2", "95,43 $", "39,98 $", 58, "DES JBL À 40 $?!"),
    ("B08P55W5DW", "Levi's", "Jeans 505 coupe régulière, homme", "79,07 $", "37,03 $", 53, "DES LEVI'S À 37 $"),
    ("B0CTB8GKM2", "JBL", "Casque à réduction de bruit Tune 770NC", "157,59 $", "79,98 $", 49, "MOITIÉ PRIX 🤯"),
    ("B091MJ24TL", "Wilson", "Ballon de basket NBA Chicago Bulls", "43,83 $", "22,99 $", 48, "CADEAU À 23 $ 🏀"),
    ("B0D9R45FMH", "Sony", "Écouteurs sans fil WF-C510", "95,62 $", "58,00 $", 39, "DES SONY À 58 $"),
    ("B0CCPRDH3T", "Crayola", "Coffret d'art Pokémon", "32,24 $", "19,98 $", 38, "FAN DE PIKACHU? ⚡"),
]
TIKTOK = [1, 0, 3]  # Levi's, JBL Race 2, Wilson
FPS = 30
CSS = ("*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1920px;background:#C1121F;color:#fff;"
       "font-family:Inter,sans-serif;font-weight:700;position:relative;overflow:hidden;display:flow-root}"
       ".an{font-family:Anton,Inter,sans-serif;font-weight:900;letter-spacing:-2px}"
       ".bar{position:absolute;top:0;left:0;right:0;height:190px;background:#FFC72C;color:#8E0B16;display:flex;align-items:center;justify-content:center;gap:22px;padding-top:40px}"
       ".bar span{font-family:Anton,Inter,sans-serif;font-weight:900;font-size:84px;letter-spacing:-2px}"
       ".bot{position:absolute;bottom:0;left:0;right:0;background:#8E0B16;text-align:center;padding:26px 30px 90px}"
       ".bot b{display:block;font-family:Anton,Inter,sans-serif;font-weight:900;font-size:78px;color:#FFC72C}"
       ".bot i{font-style:normal;font-size:30px;color:#fff}"
       ".ph{margin:290px auto 0;width:900px;height:880px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center;position:relative}"
       ".ph img{max-width:840px;max-height:820px;object-fit:contain}"
       ".pc{position:absolute;top:-30px;right:-34px;background:#FFC72C;color:#8E0B16;font-family:Anton,Inter,sans-serif;font-weight:900;font-size:120px;border-radius:30px;padding:6px 30px;transform:rotate(6deg);box-shadow:0 10px 0 #8E0B16}"
       ".br{text-align:center;font-size:44px;font-weight:700;text-transform:uppercase;color:#FFC72C;margin-top:34px}"
       ".pr{text-align:center;font-family:Anton,Inter,sans-serif;font-weight:900;font-size:220px;line-height:1}"
       ".av{text-align:center;font-size:52px}")


def img(asin):
    return (pathlib.Path("docs/img/p") / f"marque-{asin}.jpg").resolve().as_uri()


def page(inner, bot=f"Prix observé le {OB} · vérifie le prix final sur le site"):
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body>'
            f'<div class="bar">{pack.BOLT}<span>RABAISFLASHQC.CA</span></div>{inner}'
            f'<div class="bot"><b>👉 rabaisflashqc.ca</b><i>{e(bot)}</i></div></body></html>')


def hook(txt, sub):
    return page(f'<h1 class="an" style="font-size:190px;line-height:1;text-align:center;margin-top:420px">{txt}</h1>'
                f'<h2 class="an" style="font-size:96px;text-align:center;margin-top:50px;color:#FFC72C">{sub}</h2>')


def deal(d, n=None):
    a, m, t, av, pr, pc, _ = d
    num = f'<div class="an" style="position:absolute;top:240px;left:40px;font-size:90px;color:#FFC72C;z-index:2">#{n}</div>' if n else ''
    return page(f'{num}<div class="ph"><img src="{img(a)}"><div class="pc">-{pc} %</div></div>'
                f'<div class="br">{e(m)} · {e(t)}</div><div class="pr">{pr.replace(" ","&nbsp;")}</div><div class="av">au lieu de <s>{av}</s></div>')


def shock(d):
    a, m, t, av, pr, pc, acc = d
    return page(f'<h1 class="an" style="font-size:132px;line-height:1;text-align:center;margin-top:280px;padding:0 30px">{e(acc).replace(" $","&nbsp;$")}</h1>'
                f'<div class="ph" style="margin-top:60px;height:820px"><img src="{img(a)}"><div class="pc">-{pc} %</div></div>')


def cta(big="TOUS LES DEALS<br>SONT LÀ 👇"):
    return page(f'<h1 class="an" style="font-size:140px;line-height:1.05;text-align:center;margin-top:360px">{big}</h1>'
                f'<h2 class="an" style="font-size:98px;text-align:center;margin-top:60px;color:#FFC72C">RABAISFLASHQC.CA</h2>'
                f'<p style="font-size:32px;text-align:center;padding:0 80px;margin-top:70px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>',
                bot="Abonne-toi pour les deals de chaque jour")


def render(slides, out):
    tmp = pathlib.Path(tempfile.mkdtemp()); fr = []
    with sync_playwright() as pw:
        for i, (h, _) in enumerate(slides):
            br, ctx, pg = pack.render(pw, h, (1080, 1920), tmp, f"s{i}"); pg.wait_for_timeout(400)
            p = tmp / f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
    inp, flt = [], []
    for i, (p, (_, d)) in enumerate(zip(fr, slides)):
        nf = round(d * FPS)
        inp += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(p)]
        # léger zoom avant continu (mouvement), le bandeau du site reste lisible
        flt.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0016*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1080x1920:fps={FPS},setsar=1,trim=end_frame={nf}[v{i}]")
    n = len(fr); flt.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
    subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-an", "-r", str(FPS),
                    "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
    return fr


if __name__ == "__main__":
    best = max(d[5] for d in DEALS)
    s = [(hook(f"JUSQU'À<br>-{best} % 🤯", "6 DEALS QUI<br>PARTENT VITE"), 1.4)]
    s += [(deal(d, i + 1), 1.7) for i, d in enumerate(DEALS)]
    s += [(cta(), 2.2)]
    out = pack.OUT / f"reel-punchy-{JOUR}.mp4"; fr = render(s, out); print(out, sum(x for _, x in s))
    for k, j in enumerate(TIKTOK, 1):
        d = DEALS[j]
        s = [(shock(d), 1.6), (deal(d), 2.4), (cta("TAPE ÇA<br>DANS GOOGLE 👇"), 1.6)]
        o = pack.OUT / f"tiktok-punchy-{k}-{JOUR}.mp4"; render(s, o); print(o)
