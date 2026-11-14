#!/usr/bin/env python3
"""14 nov. : nouveau format demandé par Alex (après 142 clics et 0 commande ce mois-ci).
UN deal par publication : 1 image (1080x1350, Facebook et Instagram) + 1 réel SANS SON (9:16, environ 8 s, Facebook et TikTok).
Accroche claire « pour qui ». Prix lus le 14 nov. à 8 h 40 sur les pages Amazon envoyées par Alex.
Photos officielles (Walmart pour adidas et Krups, LEGO.com pour Stitch), jamais Amazon."""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e = H.escape
CSS = open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS += ("h1,h2{text-align:center}.c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:40px 44px;text-align:center}"
        ".big{font-family:Anton,Impact,sans-serif;font-size:200px;color:#C1121F;line-height:1}"
        ".pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:8px 30px;font-family:Anton,Impact,sans-serif;font-size:100px;margin:16px 0}"
        ".hk{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:28px;padding:16px 36px;font-family:Anton,Impact,sans-serif;line-height:1.08}")
OB = "14 nov."
# (clé, marque, produit, asin, ancien, nouveau, %, accroche)
DEALS = [
    ("midi", "adidas", "Bas invisibles pour femme (6 paires)", "B0BZR2T4VT", "28,00 $", "14,00 $", 50, "LE BAS DE NOËL<br>À 14 $ 🧦"),
    ("16h", "Krups", "Gaufrier belge 4 gaufres", "B01FYIAQA6", "136,40 $", "76,99 $", 44, "POUR LES BRUNCHS<br>DU DIMANCHE 🧇"),
    ("soir", "LEGO", "Disney Stitch et Scrump", "B0G2SYJSJ4", "99,99 $", "75,79 $", 24, "POUR LE FAN<br>DE STITCH 💙"),
]


def img(asin):
    p = (pathlib.Path('docs/img/p') / f'marque-{asin}.jpg').resolve()
    assert p.exists(), p
    return p.as_uri()


def doc(inner, w, h, foot):
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head>'
            f'<body style="width:{w}px;height:{h}px;position:relative"><div class="top" style="padding-top:{70 if h > 1500 else 30}px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}'
            f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">{foot}</div></div></body></html>')


def carte(a, t, asin, av, pr, pc, hk, hauteur_photo, taille_hk, bs=200):
    return (f'<div style="margin:24px 56px 0;text-align:center"><span class="hk" style="font-size:{taille_hk}px">{hk}</span></div>'
            f'<div style="margin:26px auto 0;width:640px;height:{hauteur_photo}px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center">'
            f'<img src="{img(asin)}" style="max-width:580px;max-height:{hauteur_photo - 40}px;object-fit:contain"></div>'
            f'<div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div>'
            f'<div style="font-size:46px;font-weight:700;margin:8px 0 18px">{e(t)}</div>'
            f'<div class="big" style="font-size:{bs}px">{pr}</div><div class="pc" style="font-size:{bs//2}px">-{pc} %</div><div style="font-size:42px">avant : <s>{av}</s></div>'
            f'<div style="font-size:28px;color:#555;margin-top:14px">prix observé le {OB}</div></div>')


def fin():
    return doc('<h1 class="an" style="font-size:120px;line-height:1.08;margin-top:260px">LE LIEN EST<br>SUR LE SITE 👇</h1>'
               '<div style="margin:50px 56px 0;text-align:center"><span style="display:inline-block;background:#fff;color:#C1121F;border-radius:30px;padding:24px 44px;font-family:Anton,Impact,sans-serif;font-size:104px">rabaisflashqc.ca</span></div>'
               '<h2 style="font-size:54px;margin-top:50px">Vendredi fou dans 13 jours ⏳</h2>'
               '<p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:50px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>',
               1080, 1920, f"Prix observé le {OB}, il peut changer")


def shot(pw, html, size, tmp, nom):
    br, ctx, pg = pack.render(pw, html, size, tmp, nom)
    pg.wait_for_timeout(700)
    p = tmp / f"{nom}.png"
    pg.screenshot(path=str(p)); ctx.close(); br.close()
    return p


tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    pf = shot(pw, fin(), (1080, 1920), tmp, "fin")
    for cle, a, t, asin, av, pr, pc, hk in DEALS:
        # Image du post (1080x1350)
        im = shot(pw, doc(carte(a, t, asin, av, pr, pc, hk, 330, 60, 130), 1080, 1350,
                          f"Prix observé le {OB}, il peut changer · vérifie le prix final sur le site"), (1080, 1350), tmp, f"im-{cle}")
        out_im = pack.OUT / f"post-14nov-{cle}.png"
        out_im.write_bytes(im.read_bytes()); print(out_im)
        # Réel sans son (9:16) : le deal 5 s, puis l'écran du site 3 s
        pd = shot(pw, doc(carte(a, t, asin, av, pr, pc, hk, 620, 84), 1080, 1920, "Tous les deals avec photos sur le site"), (1080, 1920), tmp, f"r-{cle}")
        (pathlib.Path('/tmp') / f"r-{cle}.png").write_bytes(pd.read_bytes())
        out = pack.OUT / f"reel-14nov-{cle}-sans-son.mp4"
        inp = ["-loop", "1", "-t", "5", "-i", str(pd), "-loop", "1", "-t", "3", "-i", str(pf)]
        flt = "[0:v]scale=1080:1920,fps=30,setsar=1[v0];[1:v]scale=1080:1920,fps=30,setsar=1[v1];[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[o]"
        subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", flt, "-map", "[o]", "-an", "-r", "30", "-preset", "veryfast",
                        "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
        print(out)
