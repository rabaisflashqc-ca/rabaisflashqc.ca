#!/usr/bin/env python3
"""Journée du 19 nov. 2026 (demande d'Alex) : 3 posts texte + image et 3 réels sans son + texte, JAMAIS le même produit deux fois dans la journée.
Chaque contenu dit combien de produits en rabais sont référencés sur le site et pousse la barre de recherche (rabaisflashqc.ca/recherche/).
Prix : suivi/deals_chrome.json (Keepa 8 h 03 et pages Amazon envoyées par Alex, lues de 8 h 10 à 8 h 25). Photos officielles des marques
et grands détaillants (photos.yml, docs/img/p/marque-ASIN.jpg), jamais Amazon.
Sorties : docs/pack-du-jour/post-19nov-{1,2,3}.png (1080x1350) et reel-19nov-{1,2,3}-sans-son.mp4 (1080x1920)."""
import json, pathlib, sys, importlib.util, html as H, tempfile
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("r18", ROOT / "reels-18nov-midi-pm-soir.py"); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
import pack
from verdict import verdict, eco, eco_txt, SIGNATURE
from playwright.sync_api import sync_playwright
e = H.escape
SRC = R.SRC; money = R.money; doc = R.doc
TOTAL = len(json.load(open(ROOT / "docs/recherche.json")))  # produits en rabais référencés (vérifiés et affichables) au moment du build
JOURS_VF = 8  # 19 nov. -> 27 nov.

POSTS = {
    "1": dict(titre="POUR <span>ELLE</span>", sous="3 cadeaux qu'elle va adorer", deals=[
        ("B0HDVVDGZW", "Dyson", "Airwrap i.d."), ("B0DJWLDHCL", "Levi's", "Jean Cinch Baggy"), ("B0DQY6LSWL", "Stanley", "Quencher 20 oz")]),
    "2": dict(titre="POUR LES <span>KIDS</span>", sous="Le sapin va être content", deals=[
        ("B0BLJTJ38M", "Barbie", "Maison de rêve"), ("B07ZS7J192", "Tonka", "Camion benne en acier"), ("B0G2STSGW3", "LEGO", "AT-AT en pain d'épices")]),
    "3": dict(titre="LA <span>MAISON</span>", sous="Le gros électro à prix flash", deals=[
        ("B0B38KRTV6", "De'Longhi", "Magnifica Evo"), ("B0GT28CSYM", "Dyson", "V8 Cyclone"), ("B08LQY2XF5", "Ninja", "Four Foodi XL Pro")]),
}
REELS = {
    "1": dict(hook="4 DEALS<br><b>SOUS 50 $</b> 👇", recherche="sous 50 $", deals=[
        ("B0F3BJMLKJ", "Blink", "Caméra Mini 2K+"), ("B0764BZBQW", "Magic Bullet", "Mélangeur 11 pièces"),
        ("B006W6YHYQ", "Greenies", "Gâteries dentaires Teenie"), ("B0C7K6C39H", "Crocs", "Sabots Classic")]),
    "2": dict(hook="LE SILENCE,<br>ÇA S'OFFRE <b>EN SOLDE</b> 🎧", recherche="casque", deals=[
        ("B0CCZ26B5V", "Bose", "Casque QuietComfort"), ("B0HF9V25FZ", "Sony", "Casque WH-1000XM4"),
        ("B0D1JG8CRC", "JBL", "Haut-parleur Go 4"), ("B0DVTGBCBL", "JBL", "Écouteurs Endurance Race 2")]),
    "3": dict(hook="LES JEUNES<br>VONT <b>CRIER</b> 🎁", recherche="jouet", deals=[
        ("B0CTP56C5R", "JBL", "Haut-parleur Clip 5"), ("B0BN15NTGG", "Hot Wheels", "Garage City Ultimate"),
        ("B0CD311Q6J", "5 Surprise", "My Mini Baby, lot de 2")]),
}

def recherche(q):
    return doc(f'<div class="big"><h1 style="margin-top:250px;font-size:104px"><b>{TOTAL}</b> PRODUITS<br>EN RABAIS<br>SUR LE SITE.</h1></div>'
               f'<div class="sb"><div class="t">🔎 Tape ce que tu cherches</div><div class="in">{e(q)}<i></i></div>'
               f'<div class="go">TROUVE-MOI UN DEAL</div><div class="res">✅ Trouvé en 1 seconde</div></div>')

def vendredi_fou():
    return doc(f'<div class="big"><h1>LE <b>VENDREDI FOU</b><br>ARRIVE.</h1><div class="cd">{JOURS_VF} JOURS<small>avant le 27 novembre</small></div>'
               f'<div class="sub">Les prix flash sont <b>déjà là</b>.</div></div>')

def fin(total):
    return doc(f'<div class="end"><h1>ÇA VAUT LE CLIC?<br><b>T\'ES À LA BONNE PLACE.</b> 👇</h1><div class="site"><span>rabaisflashqc.ca</span></div>'
               f'<div class="sig">⚡ {SIGNATURE}</div><div class="sub" style="font-size:50px">{total.replace(" ", chr(160))} à sauver dans cette vidéo</div></div>'
               f'<div class="leg">Prix observés le 19 nov., ils peuvent changer.<br>En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</div>', url=False)

PCSS = """*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;overflow:hidden;font-family:'Barlow Semi Condensed',Arial,sans-serif;background:#C1121F;color:#fff}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}.top{display:flex;align-items:center;justify-content:center;gap:12px;padding-top:30px;font-size:36px;letter-spacing:3px}.top b{color:#FFD23F;font-weight:400}
h1{text-align:center;font-size:110px;line-height:1;margin-top:14px}h1 span{color:#FFD23F}.sub{text-align:center;font-size:40px;font-weight:700;margin-top:4px}
.g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:26px 30px 0}
.c{position:relative;background:#FFF7E8;border-radius:26px;color:#1A1A1A;text-align:center;padding:16px 12px 16px;height:700px;display:flex;flex-direction:column;align-items:center;box-shadow:0 14px 30px rgba(80,0,8,.35)}
.ph{width:100%;height:300px;background:#fff;border-radius:18px;display:flex;align-items:center;justify-content:center}.ph img{max-height:280px;max-width:92%;object-fit:contain}
.pc{position:absolute;top:-14px;left:-10px;background:#FFC21A;color:#5A0A10;border-radius:16px;padding:4px 14px;font-size:44px;transform:rotate(-5deg)}
.b{font-size:26px;font-weight:700;color:#C1121F;letter-spacing:2px;margin-top:12px;text-transform:uppercase}.n{font-size:34px;line-height:1.05;margin-top:2px;font-weight:700}
.p{font-size:64px;color:#C1121F;line-height:1.05;margin-top:8px}.w{font-size:28px;font-weight:600;color:#6B6560;text-decoration:line-through}
.s{margin-top:auto;background:#146C34;color:#fff;border-radius:14px;padding:6px 14px;font-size:32px;white-space:nowrap}
.sr{margin:30px 60px 0;background:#fff;border-radius:22px;padding:16px 22px;display:flex;align-items:center;gap:16px;color:#1A1A1A;box-shadow:0 10px 24px rgba(80,0,8,.35)}
.sr .i{flex:1;white-space:nowrap;border:4px solid #C1121F;border-radius:14px;padding:10px 16px;font-size:34px;font-weight:700;color:#5A534D}.sr .k{background:#FFC21A;color:#2A0508;border-radius:14px;padding:12px 18px;font-size:34px}
.f{text-align:center;margin-top:22px}.f .u{display:inline-block;background:#FFC21A;color:#2A0508;border-radius:999px;padding:8px 36px;font-size:48px}.f small{display:block;font-size:26px;font-weight:700;margin-top:10px}"""

def post_html(cfg):
    tiles = "".join(f'<div class="c"><div class="pc an">-{SRC[a]["pct"]}&nbsp;%</div><div class="ph"><img src="{R.photo(a)}"></div><div class="b">{e(m)}</div>'
                    f'<div class="n">{e(n)}</div><div class="p an">{money(SRC[a]["price"])}</div><div class="w">{money(SRC[a]["was"])}</div>'
                    f'<div class="s an">TU SAUVES {eco_txt(eco(SRC[a])).replace(" ", chr(160))}</div></div>' for a, m, n in cfg["deals"])
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{PCSS}</style></head><body><div class="top an">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
            f'<h1 class="an">{cfg["titre"]}</h1><div class="sub">{e(cfg["sous"])}</div><div class="g">{tiles}</div>'
            f'<div class="sr"><span style="font-size:40px">🔎</span><div class="i">{TOTAL} rabais : tape ce que tu cherches</div><div class="k an">GO</div></div>'
            f'<div class="f"><span class="u an">rabaisflashqc.ca</span><small>⚡ {SIGNATURE} · Prix observés le 19 nov.</small></div></body></html>')

def render_post(cle, cfg):
    tmp = pathlib.Path(tempfile.mkdtemp()); out = pack.OUT / f"post-19nov-{cle}.png"
    with sync_playwright() as pw:
        br, ctx, pg = pack.render(pw, post_html(cfg), (1080, 1350), tmp, "p"); pg.wait_for_timeout(600)
        pg.screenshot(path=str(out)); ctx.close(); br.close()
    print(out)

if __name__ == "__main__":
    vus = [a for c in list(POSTS.values()) + list(REELS.values()) for a, _, _ in c["deals"]]
    assert len(vus) == len(set(vus)), "Un produit revient deux fois dans la journée"
    pack.OUT.mkdir(parents=True, exist_ok=True)
    quoi = sys.argv[1:] or ["posts", "reels"]
    if "posts" in quoi:
        for k, c in POSTS.items(): render_post(k, c)
    if "reels" in quoi:
        for k, cfg in REELS.items():
            D = cfg["deals"]; total = eco_txt(sum(int(eco(SRC[a])) for a, _, _ in D))
            s = [(R.hook(cfg), 2.0)] + [(R.scene(a, m, nm, i, len(D)), 1.9) for i, (a, m, nm) in enumerate(D, 1)]
            s += [(vendredi_fou(), 2.0), (recherche(cfg["recherche"]), 2.6), (fin(total), 3.0)]
            R.render(f"reel-19nov-{k}-sans-son.mp4", s)
