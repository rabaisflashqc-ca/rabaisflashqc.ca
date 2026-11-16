#!/usr/bin/env python3
"""Réels SANS SON « Ça vaut le clic? » du 16 nov. 2026 (nouveau positionnement : on rend un verdict, on fait gagner).
Mécanique : pour chaque deal, 1) la question « Ça vaut le clic? » avec la photo et le prix, 2) le verdict tombe comme un sceau,
avec l'économie en dollars en gros (le moment « j'ai gagné »). Fin : total des économies + « Passe ici avant d'acheter sur Amazon ».
Leçon des stats Facebook du 11 nov. : la 1re image montre tout de suite un produit et son prix, vidéo courte.
Prix : suivi/deals_chrome.json (Keepa 11 h 55, page Amazon envoyée par Alex 11 h 59). Photos officielles via Best Buy et marques (photos.yml), jamais Amazon.
Sorties : docs/pack-du-jour/reel-16nov-ca-vaut-le-clic-sans-son.mp4 (Facebook, Instagram) et tiktok-16nov-ca-vaut-le-clic-bose-sans-son.mp4 (TikTok, 1 deal)."""
import json, pathlib, tempfile, subprocess, html as H, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pack
from verdict import verdict, eco, eco_txt, SIGNATURE
from playwright.sync_api import sync_playwright
e = H.escape
ROOT = pathlib.Path(__file__).parent
SRC = {x["asin"]: x for x in json.load(open(ROOT / "suivi/deals_chrome.json"))}
money = lambda v: (f"{v:,.2f}".replace(",", "\u202f").replace(".", ",")).replace(",00", "") + "\u00a0$"

# (ASIN, marque, nom court affiché)
DEALS = [("B0F2LCBKVN", "Bose", "Casque antibruit QuietComfort"),
         ("B0DDQKXDZF", "Beats", "Casque Studio Pro"),
         ("B08DJ8Z3WH", "Shark", "Aspirateur Navigator"),
         ("B0GN4L93SM", "BISSELL", "Aspirateur sans fil PowerClean")]

CSS = """*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;overflow:hidden;font-family:'Barlow Semi Condensed',Arial,sans-serif;
background:radial-gradient(120% 80% at 50% 0,#E01E2F 0,#C1121F 40%,#7A0A16 100%);color:#fff;position:relative}
.top{display:flex;align-items:center;justify-content:center;gap:14px;padding-top:86px;font-family:Anton,Impact,sans-serif;font-size:46px;letter-spacing:3px}.top b{color:#FFC72C;font-weight:400}
.q{margin:110px 56px 0;text-align:center;font-family:Anton,Impact,sans-serif;font-size:118px;line-height:1;color:#FFC72C;text-shadow:0 6px 0 rgba(0,0,0,.25)}
.card{position:relative;margin:50px auto 0;width:900px;background:#fff;border-radius:48px;padding:36px 40px 40px;color:#1A1A1A;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.ph{height:640px;display:flex;align-items:center;justify-content:center}.ph img{max-width:700px;max-height:640px;object-fit:contain}
.br{font-size:40px;font-weight:700;color:#C1121F;letter-spacing:2px;text-transform:uppercase;margin-top:6px}.nm{font-size:52px;font-weight:700;line-height:1.1;margin-top:4px}
.px{margin-top:18px;display:flex;align-items:baseline;justify-content:center;gap:24px}.px s{font-size:56px;color:#8a8a8a}.px{white-space:nowrap}.px b{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:136px;color:#C1121F;line-height:1}
.stamp{position:absolute;right:-30px;top:430px;transform:rotate(8deg);background:#1A1A1A;color:#FFC72C;border:8px solid #FFC72C;border-radius:30px;padding:18px 30px;font-family:Anton,Impact,sans-serif;font-size:70px;line-height:1.02;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.4)}
.stamp.bon{background:#fff;color:#8E0B16;border-color:#8E0B16}
.sv{margin:56px 56px 0;white-space:nowrap;text-align:center}.sv span{display:inline-block;background:#0F7A3D;color:#fff;border-radius:34px;padding:20px 46px;font-family:Anton,Impact,sans-serif;font-size:104px;line-height:1;box-shadow:0 10px 0 rgba(0,0,0,.2)}
.n{position:absolute;left:56px;top:80px;font-family:Anton,Impact,sans-serif;font-size:44px;background:#FFC72C;color:#8E0B16;border-radius:999px;padding:4px 24px}
.foot{position:absolute;left:0;right:0;bottom:170px;text-align:center;font-family:Anton,Impact,sans-serif;font-size:62px;color:#fff}.foot small{display:block;font-family:'Barlow Semi Condensed',Arial;font-size:30px;font-weight:500;opacity:.85;margin-top:8px}
.end{text-align:center;margin:0 56px}.end h1{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:112px;line-height:1.05;color:#fff;margin-top:230px}
.tot{margin-top:70px}.tot span{display:inline-block;background:#0F7A3D;border-radius:34px;padding:18px 40px;font-family:Anton,Impact,sans-serif;font-size:92px;line-height:1.05}
.site{margin-top:80px}.site span{display:inline-block;background:#fff;color:#C1121F;border-radius:30px;padding:26px 44px;font-family:Anton,Impact,sans-serif;font-size:100px}
.sig{margin-top:36px;font-size:54px;font-weight:700;color:#FFC72C}.leg{position:absolute;left:70px;right:70px;bottom:90px;text-align:center;font-size:27px;line-height:1.35;opacity:.9}"""

def doc(inner):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}</body></html>'

def photo(asin):
    p = (ROOT / "docs/img/p" / f"marque-{asin}.jpg").resolve()
    if not p.exists(): sys.exit(f"Photo officielle manquante : {p.name} (lancer photos.yml)")
    return p.as_uri()

def scene(asin, marque, nom, k, n, revele):
    d = SRC[asin]; vt, vc = verdict(d)
    stamp = ""
    if revele:
        cls = "stamp" if "hot" in vc else "stamp bon"
        stamp = f'<div class="{cls}">{"ÇA VAUT<br>LE CLIC 🔥" if "hot" in vc else e(vt.split(" ", 1)[1].upper())}</div>'
    bas = (f'<div class="sv"><span>TU SAUVES {eco_txt(eco(d)).replace(" ", "\u00a0")}</span></div>' if revele
           else '<div class="foot">Le verdict dans 1 seconde…</div>')
    num = f'<div class="n">{k}/{n}</div>' if n > 1 else ""
    return doc(f'{num}<div class="q">ÇA VAUT LE CLIC?</div><div class="card">{stamp}<div class="ph"><img src="{photo(asin)}"></div>'
               f'<div class="br">{e(marque)}</div><div class="nm">{e(nom)}</div><div class="px"><s>{money(d["was"])}</s><b>{money(d["price"])}</b></div></div>{bas}')

def fin(total, n):
    tot = f'<div class="tot"><span>{total.replace(' ', chr(160))} D\'ÉCONOMIES<br>SUR {n} DEALS</span></div>' if n > 1 else ""
    return doc(f'<div class="end"><h1>PASSE ICI AVANT<br>D\'ACHETER SUR AMAZON 👇</h1>{tot}<div class="site"><span>rabaisflashqc.ca</span></div>'
               f'<div class="sig">⚡ {SIGNATURE}</div></div><div class="leg">Prix observés le 16 nov., ils peuvent changer.<br>En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</div>')

def render(nom, slides):
    tmp = pathlib.Path(tempfile.mkdtemp()); fr = []
    with sync_playwright() as pw:
        for i, (h, _) in enumerate(slides):
            br, ctx, pg = pack.render(pw, h, (1080, 1920), tmp, f"s{i}"); pg.wait_for_timeout(500)
            p = tmp / f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
            (pathlib.Path("/tmp") / f"{nom}-{i}.png").write_bytes(p.read_bytes())
    durs = [d for _, d in slides]; out = pack.OUT / nom; inp, flt = [], []
    for i, (p, d) in enumerate(zip(fr, durs)):
        inp += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(p)]
        z = "zoompan=z='min(1+0.0009*on,1.04)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30," if i % 2 == 1 or i == len(fr) - 1 else ""
        flt.append(f"[{i}:v]scale=1080:1920,setsar=1,{z}fps=30[v{i}]")
    n = len(fr); flt.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
    subprocess.run(["ffmpeg", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-t", f"{sum(durs):.3f}", "-an", "-r", "30",
                    "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
    print(out, round(sum(durs), 1), "s")

if __name__ == "__main__":
    pack.OUT.mkdir(parents=True, exist_ok=True)
    total = eco_txt(sum(int(eco(SRC[a])) for a, _, _ in DEALS))
    s = []
    for k, (a, m, nm) in enumerate(DEALS, 1):
        s += [(scene(a, m, nm, k, len(DEALS), False), 1.5), (scene(a, m, nm, k, len(DEALS), True), 2.2)]
    render("reel-16nov-ca-vaut-le-clic-sans-son.mp4", s + [(fin(total, len(DEALS)), 3.5)])
    a, m, nm = DEALS[0]
    render("tiktok-16nov-ca-vaut-le-clic-bose-sans-son.mp4", [(scene(a, m, nm, 1, 1, False), 1.8), (scene(a, m, nm, 1, 1, True), 3.2), (fin(total, 1), 3.0)])
