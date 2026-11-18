#!/usr/bin/env python3
"""Réels SANS SON du 18 nov. 2026 : midi, après-midi et soir, des produits différents selon l'heure et l'audience (demande d'Alex).
Message commercial : aubaines flash, Vendredi fou (27 nov.) et le chercheur de rabais du site (barre de recherche).
- Midi (pause dîner, femmes 45+) : Levi's, Oral-B, BISSELL.
- Après-midi (grands-parents qui magasinent pour les petits-enfants) : LEGO, Magna-Tiles, Oral-B Kids, Ninja CREAMi.
- Soir (couples, cadeaux pour lui et la maison) : Bose, Ninja, Shark, JBL, SAXX.
Leçons des stats : 1re image = produit + prix + accroche, réel court, adresse du site visible en permanence en bas.
Prix : suivi/deals_chrome.json (Keepa 8 h 35, pages Amazon envoyées par Alex 8 h 41 à 8 h 49).
Photos officielles des marques et grands détaillants (photos.yml), jamais Amazon.
Sorties : docs/pack-du-jour/reel-18nov-{midi,pm,soir}-sans-son.mp4"""
import json, pathlib, tempfile, subprocess, html as H, sys, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pack
from verdict import verdict, eco, eco_txt, SIGNATURE
from playwright.sync_api import sync_playwright
e = H.escape
ROOT = pathlib.Path(__file__).parent
ALL = json.load(open(ROOT / "suivi/deals_chrome.json"))
SRC = {x["asin"]: x for x in ALL}
money = lambda v: (f"{v:,.2f}".replace(",", " ").replace(".", ",")).replace(",00", "") + " $"
JOURS_VF = 9  # 18 nov. -> Vendredi fou le 27 nov.

REELS = {
    "midi": dict(hook="TA PAUSE DÎNER<br>VAUT <b>DE L'OR</b> 👇", recherche="jean",
                 deals=[("B0DLLGG2Z8", "Oral-B", "Brosse à dents iO2"),
                        ("B01CO66W4A", "Levi's", "Jean 315 bootcut galbant"),
                        ("B0GN4L93SM", "BISSELL", "Aspirateur balai PowerClean")]),
    "pm": dict(hook="GRANDS-PARENTS :<br>LES CADEAUX DES <b>PETITS</b> 🎁", recherche="LEGO",
               deals=[("B0FLKLY8LQ", "Oral-B", "Brosse iO Kids Spider-Man"),
                      ("B0DF81PBXK", "LEGO", "Fortnite Autobus de combat"),
                      ("B000CBSNRY", "Magna-Tiles", "Clear Colors 100 pièces"),
                      ("B0CHBNXJ24", "Ninja", "CREAMi XL Deluxe")]),
    "soir": dict(hook="CE SOIR, ON SE <b>GÂTE</b>.<br>À PRIX FLASH 🔥", recherche="casque",
                 deals=[("B0CCZ26B5V", "Bose", "Casque QuietComfort"),
                        ("B08LQY2XF5", "Ninja", "Four Foodi XL Pro 10 en 1"),
                        ("B08DJ8Z3WH", "Shark", "Aspirateur Navigator Swivel Pro"),
                        ("B0DN45YMP6", "JBL", "Écouteurs Vibe Beam 2"),
                        ("B0CYM8XGLM", "SAXX", "Boxers, lot de 3")]),
}

CSS = """*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;overflow:hidden;font-family:'Barlow Semi Condensed',Arial,sans-serif;
background:radial-gradient(120% 80% at 50% 0,#E01E2F 0,#C1121F 40%,#7A0A16 100%);color:#fff;position:relative}
.top{display:flex;align-items:center;justify-content:center;gap:14px;padding-top:80px;font-family:Anton,Impact,sans-serif;font-size:46px;letter-spacing:3px}.top b{color:#FFC72C;font-weight:400}
.flash{position:absolute;right:40px;top:70px;background:#FFC72C;color:#8E0B16;font-family:Anton,Impact,sans-serif;font-size:38px;padding:6px 22px;border-radius:999px;transform:rotate(4deg)}
.hook{margin:46px 40px 0;text-align:center;font-family:Anton,Impact,sans-serif;font-size:96px;line-height:1.02}.hook b{color:#FFC72C;font-weight:400}.hk .ph{height:640px}.hk .ph img{max-height:640px}
.q{margin:60px 56px 0;text-align:center;font-family:Anton,Impact,sans-serif;font-size:96px;line-height:1;color:#FFC72C;text-shadow:0 6px 0 rgba(0,0,0,.25)}
.card{position:relative;margin:70px auto 0;width:900px;background:#fff;border-radius:48px;padding:30px 40px 36px;color:#1A1A1A;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.ph{height:800px;display:flex;align-items:center;justify-content:center}.ph img{max-width:820px;max-height:800px;object-fit:contain}
.br{font-size:40px;font-weight:700;color:#C1121F;letter-spacing:2px;text-transform:uppercase;margin-top:6px}.nm{font-size:50px;font-weight:700;line-height:1.1;margin-top:4px}
.px{margin-top:14px;display:flex;align-items:baseline;justify-content:center;gap:24px;white-space:nowrap}.px s{font-size:54px;color:#8a8a8a}.px b{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:130px;color:#C1121F;line-height:1}
.pct{position:absolute;left:-26px;top:-26px;background:#FFC72C;color:#8E0B16;font-family:Anton,Impact,sans-serif;font-size:84px;padding:10px 30px;border-radius:30px;transform:rotate(-6deg);box-shadow:0 10px 24px rgba(0,0,0,.35)}
.stamp{position:absolute;right:-30px;top:560px;transform:rotate(8deg);background:#1A1A1A;color:#FFC72C;border:8px solid #FFC72C;border-radius:30px;padding:16px 28px;font-family:Anton,Impact,sans-serif;font-size:66px;line-height:1.02;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.4)}
.stamp.bon{background:#fff;color:#8E0B16;border-color:#8E0B16}
.sv{margin:70px 56px 0;white-space:nowrap;text-align:center}.sv span{display:inline-block;background:#0F7A3D;color:#fff;border-radius:34px;padding:18px 44px;font-family:Anton,Impact,sans-serif;font-size:96px;line-height:1;box-shadow:0 10px 0 rgba(0,0,0,.2)}
.n{position:absolute;left:56px;top:150px;font-family:Anton,Impact,sans-serif;font-size:44px;background:#FFC72C;color:#8E0B16;border-radius:999px;padding:4px 24px}
.url{position:absolute;left:0;right:0;bottom:120px;text-align:center}.url span{display:inline-block;background:#fff;color:#C1121F;border-radius:24px;padding:12px 36px;font-family:Anton,Impact,sans-serif;font-size:62px;box-shadow:0 8px 0 rgba(0,0,0,.2)}
.big{text-align:center;margin:0 50px}.big h1{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:130px;line-height:1.02;margin-top:300px}.big h1 b{color:#FFC72C;font-weight:400}
.cd{margin:60px auto 0;display:inline-block;background:#1A1A1A;color:#FFC72C;border:8px solid #FFC72C;border-radius:36px;padding:20px 50px;font-family:Anton,Impact,sans-serif;font-size:150px;line-height:1}
.cd small{display:block;font-size:56px;color:#fff;margin-top:8px}.sub{margin-top:56px;font-size:60px;font-weight:700;line-height:1.2}.sub b{color:#FFC72C}
.sb{margin:90px 50px 0;background:#fff;border:8px solid #FFC72C;border-radius:40px;padding:30px;color:#1A1A1A;text-align:left;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.sb .t{font-size:44px;font-weight:700;color:#C1121F}.sb .in{margin-top:18px;border:5px solid #C1121F;background:#FFF8E1;border-radius:24px;padding:22px 26px;font-size:66px;font-weight:700}
.sb .in i{display:inline-block;width:6px;height:64px;background:#C1121F;vertical-align:middle;margin-left:4px}
.sb .go{margin-top:18px;background:#FFC72C;color:#7A0A16;border-radius:24px;padding:22px;text-align:center;font-family:Anton,Impact,sans-serif;font-size:64px}
.sb .res{margin-top:20px;text-align:center;font-size:50px;font-weight:700;color:#0F7A3D}
.end{text-align:center;margin:0 56px}.end h1{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:112px;line-height:1.05;margin-top:380px}.end h1 b{color:#FFC72C;font-weight:400}
.site{margin-top:70px}.site span{display:inline-block;background:#fff;color:#C1121F;border-radius:30px;padding:26px 44px;font-family:Anton,Impact,sans-serif;font-size:100px}
.sig{margin-top:36px;font-size:54px;font-weight:700;color:#FFC72C}.leg{position:absolute;left:70px;right:70px;bottom:70px;text-align:center;font-size:27px;line-height:1.35;opacity:.9}"""

URL = '<div class="url"><span>rabaisflashqc.ca</span></div>'

def doc(inner, url=True):
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body>'
            f'<div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}{URL if url else ""}</body></html>')

def photo(asin):
    p = (ROOT / "docs/img/p" / f"marque-{asin}.jpg").resolve()
    if not p.exists(): sys.exit(f"Photo officielle manquante : {p.name} (lancer photos.yml)")
    return p.as_uri()

def carte(d, asin, marque, nom, stamp="", pct=False):
    badge = f'<div class="pct">-{d["pct"]}&nbsp;%</div>' if pct else ""
    return (f'<div class="card">{badge}{stamp}<div class="ph"><img src="{photo(asin)}"></div><div class="br">{e(marque)}</div>'
            f'<div class="nm">{e(nom)}</div><div class="px"><s>{money(d["was"])}</s><b>{money(d["price"])}</b></div></div>')

def hook(cfg):
    a, m, nm = cfg["deals"][0]; d = SRC[a]
    return doc(f'<div class="flash">FLASH ⚡</div><div class="hook">{cfg["hook"]}</div><div class="hk">{carte(d, a, m, nm, pct=True)}</div>')

def scene(asin, marque, nom, k, n):
    d = SRC[asin]; vt, vc = verdict(d)
    cls = "stamp" if "hot" in vc else "stamp bon"
    stamp = f'<div class="{cls}">{"ÇA VAUT<br>LE CLIC 🔥" if "hot" in vc else e(vt.split(" ", 1)[1].upper())}</div>'
    return doc(f'<div class="n">{k}/{n}</div>{carte(d, asin, marque, nom, stamp)}'
               f'<div class="sv"><span>TU SAUVES {eco_txt(eco(d)).replace(" ", " ")}</span></div>')

def vendredi_fou():
    n = len(ALL)
    return doc(f'<div class="big"><h1>LE <b>VENDREDI FOU</b><br>ARRIVE.</h1><div class="cd">{JOURS_VF} JOURS<small>avant le 27 novembre</small></div>'
               f'<div class="sub">Les prix flash sont <b>déjà là</b>.<br>{n} aubaines triées pour toi.</div></div>')

def recherche(q):
    n = sum(1 for x in ALL if re.search(rf"\b{re.escape(q)}", x["title"], re.I))
    return doc(f'<div class="big"><h1 style="margin-top:280px;font-size:110px">TU CHERCHES<br>QUELQUE CHOSE?<br><b style="white-space:nowrap">TAPE-LE.</b></h1></div>'
               f'<div class="sb"><div class="t">🔎 Le chercheur de rabais</div><div class="in">{e(q)}<i></i></div>'
               f'<div class="go">TROUVE-MOI UN DEAL</div><div class="res">✅ {n} deals {e(q)} trouvés en 1 seconde</div></div>')

def fin(total):
    return doc(f'<div class="end"><h1>ÇA VAUT LE CLIC?<br><b>T\'ES À LA BONNE PLACE.</b> 👇</h1><div class="site"><span>rabaisflashqc.ca</span></div>'
               f'<div class="sig">⚡ {SIGNATURE}</div><div class="sub" style="font-size:50px">{total.replace(" ", chr(160))} à sauver dans cette vidéo</div></div>'
               f'<div class="leg">Prix observés le 18 nov., ils peuvent changer.<br>En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</div>', url=False)

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
    for cle in (sys.argv[1:] or REELS):
        cfg = REELS[cle]; D = cfg["deals"]
        total = eco_txt(sum(int(eco(SRC[a])) for a, _, _ in D))
        s = [(hook(cfg), 2.0)] + [(scene(a, m, nm, k, len(D)), 1.9) for k, (a, m, nm) in enumerate(D, 1)]
        s += [(vendredi_fou(), 2.2), (recherche(cfg["recherche"]), 2.6), (fin(total), 3.0)]
        render(f"reel-18nov-{cle}-sans-son.mp4", s)
