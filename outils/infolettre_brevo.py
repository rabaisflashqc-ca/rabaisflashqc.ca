#!/usr/bin/env python3
"""Infolettre pour Brevo (« Code HTML personnalisé ») : style texte, sans image, par thème, liens Amazon taggés.
Permis par les règles Amazon.ca Associés pour des abonnés inscrits (opt-in). Prix = deals_chrome.json lus il y a moins de 24 h.
Usage : python3 outils/infolettre_brevo.py > fichier.html"""
import json, datetime, html, pathlib, sys
from zoneinfo import ZoneInfo
ROOT = pathlib.Path(__file__).resolve().parent.parent
TAG = "coupdecoeurqc-20"; SITE = "https://rabaisflashqc.ca/offres-du-jour/?utm_source=brevo"
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juill.", "août", "sept.", "oct.", "nov.", "déc."]
e = html.escape
m = lambda v: (f"{v:,.2f}".replace(",", " ").replace(".", ",")).replace(",00", "") + " $"
now = datetime.datetime.now(datetime.timezone.utc)
D = [x for x in json.loads((ROOT / "suivi/deals_chrome.json").read_text())
     if (now - datetime.datetime.fromisoformat(x["seen"])).total_seconds() < 24 * 3600 and 15 <= x["pct"] <= 85 and x["price"] <= 300]
D.sort(key=lambda x: -x["pct"])
jour = max(datetime.datetime.fromisoformat(x["seen"]) for x in D).astimezone(ZoneInfo("America/Toronto"))
jt = f'{"1er" if jour.day == 1 else jour.day} {MOIS[jour.month-1]}'
noel = lambda x: "Noël" in x["title"]
T = [("🔥 Pré-Vendredi fou", lambda x: x.get("vf") and not noel(x), 6), ("🎧 Tech et son", lambda x: x["cat"] == "tech", 5),
     ("🏠 Maison et cuisine", lambda x: x["cat"] == "maison" and not noel(x), 5), ("🎄 Sapins et décos de Noël", noel, 4),
     ("💄 Beauté et coiffure", lambda x: x["cat"] == "beaute", 5), ("🧸 Enfants et jouets", lambda x: x["cat"] in ("jouets", "enfants"), 5),
     ("👕 Mode pour elle et lui", lambda x: x["cat"] in ("homme", "femme"), 6), ("🐾 Animaux et plein air", lambda x: x["cat"] in ("animaux", "plein-air"), 5)]
P = 'style="margin:0 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;color:#222222"'
pris = set(); body = ""; n = 0
for t, f, k in T:
    xs = [x for x in D if x["asin"] not in pris and f(x)][:k]
    if not xs: continue
    pris.update(x["asin"] for x in xs); n += len(xs)
    body += f'<p style="margin:22px 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:18px;font-weight:bold;color:#c1121f">{t}</p>'
    for x in xs:
        u = f'https://www.amazon.ca/dp/{x["asin"]}?tag={TAG}'
        body += (f'<p style="margin:0 0 10px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:22px;color:#222222">'
                 f'• <a href="{u}" style="color:#1a56b3">{e(x["title"])}</a> : <b>{m(x["price"])}</b> au lieu de {m(x["was"])} <b style="color:#c1121f">(-{x["pct"]} %)</b></p>')
top = D[0]
print(f'''<!DOCTYPE html><html lang="fr-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Les offres du jour</title></head>
<body style="margin:0;padding:0;background:#ffffff">
<div style="display:none;max-height:0;overflow:hidden">{e(top["title"].split(",")[0])} à {m(top["price"])} et {n - 1} autres rabais triés par thème.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:20px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px"><tr><td>
<p {P}>Salut!</p>
<p {P}>Les premières offres du Vendredi fou sont déjà sorties, et on a fait le tri pour toi : {n} deals de marques connues, classés par thème. Clique sur un produit pour le voir.</p>
{body}
<p style="margin:24px 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;color:#222222">Tous les deals du jour, avec photos et filtres par budget :<br><a href="{SITE}" style="color:#c1121f;font-weight:bold">rabaisflashqc.ca/offres-du-jour</a></p>
<p {P}>Lequel tu prends en premier? Réponds à ce courriel, je lis tout.</p>
<p {P}>Alex, Rabais Flash QC</p>
<p style="margin:20px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#888888">Prix observés le {jt}, ils peuvent changer vite : vérifie le prix final avant d'acheter. En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.<br>Tu reçois ce courriel parce que tu t'es inscrit aux deals de Rabais Flash QC. <a href="{{{{ unsubscribe }}}}" style="color:#888888">Se désinscrire</a></p>
</td></tr></table></td></tr></table></body></html>''')
print(f"{n} deals", file=sys.stderr)
