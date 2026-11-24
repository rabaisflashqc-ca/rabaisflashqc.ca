#!/usr/bin/env python3
"""7 images Facebook (un produit chacune, photo officielle de marque) pour la programmation 19 h 30 à 21 h du 24 nov. + textes/commentaires -> suivi/posts/2026-11-24-fb-programme-soir.json"""
import json, pathlib, html as H
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent
deals = {d["asin"]: d for d in json.load(open(ROOT / "suivi/deals_chrome.json"))}
e = H.escape
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"
# (heure, ASIN, nom court, accroche image, accroche texte, ligne produit)
P = [("19:30","B0BWWZP49F","Blink Mini 2, caméra de surveillance","19,99 $. OUI, TU AS BIEN LU.","🚨 19,99 $ pour une caméra Blink! Oui, tu as bien lu.","Petite caméra intelligente câblée, pratique pour le salon, la chambre de bébé ou l'entrée."),
     ("19:45","B0764BZBQW","Magic Bullet, mélangeur et mini-robot","-58 % : FILE LE PRENDRE","🥤 Un Magic Bullet à moitié prix et des poussières, ça se passe de commentaires.","Smoothies, sauces, salsas : prêt en quelques secondes, et ça se lave en deux temps trois mouvements."),
     ("20:00","B0FLKLY8LQ","Oral-B iO Kids Spider-Man, brosse à dents électrique","LE CADEAU QUI DONNE ENVIE DE SE BROSSER","🕷️ Spider-Man + brosse à dents électrique Oral-B iO : tes enfants vont VOULOIR se brosser les dents.","Édition limitée à -50 %, un cadeau malin pour Noël ou pour le bas de Noël."),
     ("20:15","B00NAW56MC","Mini sapin de Noël de 2 pi pré-éclairé, effet neige","-50 % POUR UN COIN DE NOËL","🎄 Un sapin de Noël pré-éclairé à 39,99 $, c'est le moment de l'ajouter à ton décor!","Idéal pour un coin de salon, un comptoir, un bureau ou un petit logement."),
     ("20:30","B0DBNTYL27","Ninja, four grille-pain rabattable et friteuse à air","FOUR + FRITEUSE À AIR EN 1","🍟 Four, grille-pain et friteuse à air dans un seul appareil Ninja : -40 %!","Il se rabat pour sauver de l'espace sur le comptoir. Parfait avant le temps des Fêtes."),
     ("20:45","B0GT28CSYM","Dyson V8 Cyclone, aspirateur sans fil","UN DYSON À CE PRIX-LÀ?","🌀 Un Dyson V8 sans fil à 349,99 $. Tu l'aurais payé combien?","Sans fil, léger, facile à sortir pour les poils d'animaux et les miettes de tous les jours."),
     ("21:00","B000CBSNRY","Magna-Tiles, lot de 100 pièces","LE CADEAU DE NOËL QUI FAIT TOUJOURS HIT","🧲 Magna-Tiles, le jouet magnétique que les enfants ne lâchent plus : -30 %!","Lot de 100 pièces, idée cadeau pour Noël et pour les journées d'hiver à la maison.")]
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
        if a == "B0GT28CSYM": im = im.crop((int(im.width * .2), 0, im.width, im.height))   # bande noire parasite à gauche
        crop = tmp / f"_c{i}.jpg"; im.save(crop)
        avant = f'prix conseillé : <s>{money(d["was"])}</s>' if ref else f'avant : <s>{money(d["was"])}</s>'
        page = (f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class="h">{e(hook)}</div>'
                f'<div class="card"><img src="{crop.resolve().as_uri()}"><div class="b">-{d["pct"]} %</div></div>'
                f'<div class="n">{e(nm)}</div><div class="p">{money(d["price"])}</div><div class="w">{avant}</div>'
                f'<div class="u">Lien en commentaire 👇<small>rabaisflashqc.ca</small></div></body>')
        hp = tmp / "_p.html"; hp.write_text(page)
        pg = br.new_page(viewport={"width": 1080, "height": 1350}); pg.goto(hp.as_uri()); pg.wait_for_timeout(400)
        f = f"fb-24nov-soir-{i}-{a}.png"; pg.screenshot(path=str(tmp / f)); pg.close(); crop.unlink(); hp.unlink()
        av = f"prix conseillé {money(d['was'])}" if ref else f"au lieu de {money(d['was'])}"
        texte = (f"{ht}\n\n{nm} : {money(d['price'])} ({av}, -{d['pct']} %)\n{ligne}\n\nLe lien du produit est juste en commentaire 👇\n\n"
                 f"Plus de 2 900 autres deals triés sur rabaisflashqc point ca.\n⚡ Les rabais qui valent vraiment le clic.\n\n"
                 "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.")
        out.append({"heure": h, "asin": a, "image": f, "texte": texte,
                    "commentaire1": f"👉 {nm} : {money(d['price'])} (-{d['pct']} %)\nhttps://www.amazon.ca/dp/{a}?tag=coupdecoeurqc-20",
                    "commentaire2": "🔎 Tous nos deals triés par type et par prix, avec la barre de recherche :\nhttps://rabaisflashqc.ca"})
    br.close()
json.dump(out, open(ROOT / "suivi/posts/2026-11-24-fb-programme-soir.json", "w"), ensure_ascii=False, indent=1)
from PIL import Image as I
W = I.new("RGB", (270 * 7, 338), "white")
for i, o in enumerate(out): W.paste(I.open(tmp / o["image"]).resize((270, 338)), (i * 270, 0))
W.save("/tmp/planche_fb7.png"); print("ok", len(out))
