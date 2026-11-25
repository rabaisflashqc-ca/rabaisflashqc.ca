#!/usr/bin/env python3
"""7 images Facebook (un produit chacune, photo officielle de marque) pour la programmation 19 h 30 à 21 h du 24 nov. + textes/commentaires -> suivi/posts/2026-11-24-fb-programme-soir2.json"""
import json, pathlib, html as H
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent
deals = {d["asin"]: d for d in json.load(open(ROOT / "suivi/deals_chrome.json"))}
e = H.escape
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"
# (heure, ASIN, nom court, accroche image, accroche texte, ligne produit)
P = [("21:05","B08DJ8Z3WH","Shark Navigator Pro, aspirateur vertical","MOITIÉ PRIX SUR UN SHARK","🦈 Un aspirateur Shark à moitié prix, c'est rare. Celui-là est à -50 %!","Aspirateur vertical Navigator Pro, pratique pour les poils et les saletés de tous les jours."),
     ("21:06","B0DN45YMP6","JBL Vibe Beam 2, écouteurs sans fil","LA MUSIQUE SANS FIL À 49,98 $","🎧 Des écouteurs sans fil JBL à 49,98 $, ça te tente?","Les JBL Vibe Beam 2, un bon cadeau de Noël pour les ados et les grands."),
     ("21:07","B0CHBNXJ24","Ninja CREAMi XL, machine à glace 11 en 1","DE LA CRÈME GLACÉE MAISON","🍦 Ninja CREAMi XL : de la crème glacée maison, des sorbets et des laits fouettés. -43 %!","Machine 11 en 1, une idée cadeau originale pour toute la famille."),
     ("21:08","B0B38KRTV6","De'Longhi Magnifica Evo, machine à espresso","LE CAFÉ DE CAFÉ, CHEZ TOI","☕ Une machine à espresso De'Longhi à -40 %, ton café du matin vient de monter de niveau!","Machine automatique Magnifica Evo : tu choisis, elle moud et prépare ton espresso."),
     ("21:09","B0G2STSGW3","LEGO Star Wars AT-AT en pain d'épice","LE LEGO DES FÊTES","🎄 Un AT-AT en pain d'épice version LEGO Star Wars : -29 %!","Un cadeau de Noël parfait pour les fans de Star Wars, petits et grands."),
     ("21:10","B0DCCJZC9F","Oral-B iO Série 7, brosse à dents électrique","UN SOURIRE À -45 %","🪥 Oral-B iO Série 7 à 164,99 $ au lieu de 299,99 $ : tu l'aurais payée combien?","Brosse à dents électrique rechargeable, avec capteur de pression et étui de voyage."),
     ("21:11","B0HDVVDGZW","Dyson Airwrap i.d., multi-styler","LE DYSON AIRWRAP À -200 $","💇‍♀️ Le multi-styler Dyson Airwrap i.d. avec 200 $ de moins, pour les Fêtes!","Droit et ondulé en un seul outil. Une idée cadeau qui fait toujours son effet."),
     ("21:12","B01MRX9US8","Crest 3D Whitestrips Vivid White, kit de blanchiment","TON SOURIRE POUR LES FÊTES","😁 Prépare ton sourire pour les photos des Fêtes avec les Crest 3D Whitestrips à 19,97 $!","Kit de blanchiment des dents, pratique et à petit prix."),
     ("21:13","B0FJMCRKWD","Cosori, bouilloire électrique en verre 1500 W","THÉ, CAFÉ, CHOCO CHAUD","🍵 Une bouilloire électrique en verre Cosori à 37,99 $ : parfaite pour les matins froids!","Chauffe l'eau en quelques minutes, idéale pour le thé, le café et le chocolat chaud."),
     ("21:14","B0BN15NTGG","Hot Wheels City Ultimate Garage, grand garage et pistes","LE CADEAU QUI FAIT TOUJOURS HIT","🚗 Le grand garage Hot Wheels City : un cadeau de Noël qui fait vraiment plaisir aux enfants.","Garage et pistes à plusieurs niveaux, avec voitures incluses.")]
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;color:#1A1A1A;overflow:hidden;text-align:center}
.h{font-family:Anton,Impact,sans-serif;font-weight:400;color:#FFC21A;font-size:84px;line-height:1.02;padding:40px 50px 0;text-shadow:5px 5px 0 #8E0B16}
.card{margin:56px auto 0;width:860px;height:560px;background:#fff;border-radius:48px;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 10px 0 #8E0B16}
.card img{max-width:780px;max-height:500px;object-fit:contain}.b{position:absolute;top:-30px;right:-26px;background:#FFC21A;color:#8E0B16;border-radius:34px;padding:8px 36px;font-family:Anton;font-size:128px;transform:rotate(5deg);box-shadow:0 6px 0 #8E0B16}
.n{color:#fff;font-size:46px;margin-top:26px;padding:0 60px;line-height:1.05}.p{font-family:Anton;font-size:170px;color:#FFC21A;line-height:1.05;text-shadow:5px 5px 0 #8E0B16}
.w{color:#FFE4B0;font-size:46px}.u{margin:14px auto 0;background:#FFC21A;color:#3D0A10;border-radius:44px;width:820px;font-family:Anton;font-size:54px;padding:12px}.u small{display:block;font-family:'Liberation Sans Narrow';font-weight:700;font-size:34px}"""
out = []; tmp = ROOT / "docs/pack-du-jour"
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for i, (h, a, nm, hook, ht, ligne) in enumerate(P, 1):
        d = deals[a]; ref = bool(d.get("ref")); src = ROOT / f"docs/img/p/marque-{a}.jpg"
        im = Image.open(src).convert("RGB")
        if a == "NONE": im = im.crop((int(im.width * .2), 0, im.width, im.height))   # bande noire parasite à gauche
        crop = tmp / f"_c{i}.jpg"; im.save(crop)
        avant = f'prix conseillé : <s>{money(d["was"])}</s>' if ref else f'avant : <s>{money(d["was"])}</s>'
        page = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class="h">{e(hook)}</div>'
                f'<div class="card"><img src="{crop.resolve().as_uri()}"><div class="b">-{d["pct"]} %</div></div>'
                f'<div class="n">{e(nm)}</div><div class="p">{money(d["price"])}</div><div class="w">{avant}</div>'
                f'<div class="u">Lien en commentaire 👇<small>rabaisflashqc.ca</small></div></body>')
        hp = tmp / "_p.html"; hp.write_text(page)
        pg = br.new_page(viewport={"width": 1080, "height": 1350}); pg.goto(hp.as_uri()); pg.wait_for_timeout(400)
        f = f"fb-24nov-soir2-{i}-{a}.png"; pg.screenshot(path=str(tmp / f)); pg.close(); crop.unlink(); hp.unlink()
        av = f"prix conseillé {money(d['was'])}" if ref else f"au lieu de {money(d['was'])}"
        texte = (f"{ht}\n\n{nm} : {money(d['price'])} ({av}, -{d['pct']} %)\n{ligne}\n\nLe lien du produit est juste en commentaire 👇\n\n"
                 f"Plus de 2 900 autres deals triés sur rabaisflashqc point ca.\n⚡ Les rabais qui valent vraiment le clic.\n\n"
                 "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.")
        out.append({"heure": h, "asin": a, "image": f, "texte": texte,
                    "commentaire1": f"👉 {nm} : {money(d['price'])} (-{d['pct']} %)\nhttps://www.amazon.ca/dp/{a}?tag=coupdecoeurqc-20",
                    "commentaire2": "🔎 Tous nos deals triés par type et par prix, avec la barre de recherche :\nhttps://rabaisflashqc.ca"})
    br.close()
json.dump(out, open(ROOT / "suivi/posts/2026-11-24-fb-programme-soir2.json", "w"), ensure_ascii=False, indent=1)
from PIL import Image as I
W = I.new("RGB", (270 * 10, 338), "white")
for i, o in enumerate(out): W.paste(I.open(tmp / o["image"]).resize((270, 338)), (i * 270, 0))
W.save("/tmp/planche_fb10.png"); print("ok", len(out))
