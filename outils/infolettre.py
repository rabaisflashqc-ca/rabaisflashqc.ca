#!/usr/bin/env python3
"""Infolettre « offres du jour » : courriel HTML par thème, avec photos, à partir de suivi/deals_chrome.json (prix lus il y a moins de 24 h).
Usage : python3 outils/infolettre.py [--direct] > fichier.html
Par défaut, chaque deal pointe vers sa carte sur rabaisflashqc.ca (règle absolue : aucun lien Amazon dans les courriels).
--direct : liens Amazon avec le tag (contraire à la règle et aux conditions des Associés Amazon; seulement si Alex le décide)."""
import json, sys, datetime, html, pathlib
from zoneinfo import ZoneInfo
ROOT = pathlib.Path(__file__).resolve().parent.parent
TAG = "coupdecoeurqc-20"; SITE = "https://rabaisflashqc.ca"
DIRECT = "--direct" in sys.argv
PAGE = {"beaute": "beaute", "maison": "maison", "tech": "tech", "enfants": "enfants", "jouets": "enfants", "animaux": "animaux", "plein-air": "plein-air", "homme": "mode", "femme": "mode"}
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juill.", "août", "sept.", "oct.", "nov.", "déc."]
e = html.escape
def money(v): return f"{v:,.2f}".replace(",", " ").replace(".", ",") + " $"
now = datetime.datetime.now(datetime.timezone.utc)
D = [x for x in json.loads((ROOT / "suivi/deals_chrome.json").read_text())
     if x.get("img_url") and (now - datetime.datetime.fromisoformat(x["seen"])).total_seconds() < 24 * 3600 and 15 <= x["pct"] <= 85]
D.sort(key=lambda x: -x["pct"])
jour = max(datetime.datetime.fromisoformat(x["seen"]) for x in D).astimezone(ZoneInfo("America/Toronto"))
jour_txt = f'{"1er" if jour.day == 1 else jour.day} {MOIS[jour.month - 1]}'
def url(x):
    if DIRECT: return f'https://www.amazon.ca/dp/{x["asin"]}?tag={TAG}'
    return f'{SITE}/{"vendredi-fou" if x.get("vf") else PAGE[x["cat"]]}/?utm_source=infolettre#{x["asin"]}'
pris = set()
def take(f, n):
    out = [x for x in D if x["asin"] not in pris and f(x)][:n]; pris.update(x["asin"] for x in out); return out
noel = lambda x: "Noël" in x["title"]
THEMES = [
 ("🔥 Les offres pré-Vendredi fou", "Les premiers rabais du Vendredi fou sont déjà sortis. Pas besoin d'attendre le 27!", lambda x: x.get("vf") and not noel(x), 6, "vendredi-fou"),
 ("🎧 Tech et son", "Écouteurs, casques, haut-parleurs : le cadeau qui fait toujours plaisir.", lambda x: x["cat"] == "tech", 4, "tech"),
 ("🏠 Maison et cuisine", "Pour recevoir aux Fêtes sans se ruiner.", lambda x: x["cat"] == "maison" and not noel(x), 6, "maison"),
 ("🎄 Sapins et décos de Noël", "Le sapin à rabais, c'est maintenant, pas le 20 décembre.", noel, 4, "maison"),
 ("💄 Beauté et coiffure", "Des petits prix parfaits pour le bas de Noël.", lambda x: x["cat"] == "beaute", 4, "beaute"),
 ("🧸 Enfants et jouets", "LEGO, Play-Doh, Crayola : la liste au père Noël à rabais.", lambda x: x["cat"] in ("jouets", "enfants"), 6, "enfants"),
 ("👕 Mode pour elle et lui", "Columbia, Carhartt, Levi's, Skechers, adidas : du chaud et du confortable.", lambda x: x["cat"] in ("homme", "femme"), 6, "mode"),
 ("🐾 Animaux et plein air", "Pitou, minou et les sportifs ne sont pas oubliés.", lambda x: x["cat"] in ("animaux", "plein-air"), 4, "animaux"),
]
def card(x):
    return (f'<td width="50%" valign="top" style="padding:6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eadfd2;border-radius:12px;background:#ffffff"><tr><td align="center" style="padding:12px 10px 4px">'
            f'<a href="{e(url(x))}" target="_blank"><img src="{e(x["img_url"])}" alt="{e(x["title"])}" width="150" height="150" style="display:block;width:150px;height:150px;object-fit:contain;border:0"></a></td></tr>'
            f'<tr><td style="padding:4px 12px 12px;font-family:Arial,Helvetica,sans-serif;text-align:center">'
            f'<span style="display:inline-block;background:#c1121f;color:#ffffff;font-weight:bold;font-size:14px;padding:3px 9px;border-radius:20px">-{x["pct"]} %</span>'
            f'<p style="margin:8px 0 6px;font-size:14px;line-height:19px;color:#222222;font-weight:bold"><a href="{e(url(x))}" target="_blank" style="color:#222222;text-decoration:none">{e(x["title"])}</a></p>'
            f'<p style="margin:0 0 10px;font-size:13px;color:#777777"><s>{money(x["was"])}</s> <b style="font-size:19px;color:#c1121f">{money(x["price"])}</b></p>'
            f'<a href="{e(url(x))}" target="_blank" style="display:inline-block;background:#ffc629;color:#222222;font-weight:bold;font-size:14px;text-decoration:none;padding:9px 16px;border-radius:24px">Voir le deal 👉</a>'
            f'</td></tr></table></td>')
def grid(xs):
    rows = ""
    for i in range(0, len(xs), 2):
        pair = xs[i:i + 2]
        rows += "<tr>" + "".join(card(x) for x in pair) + ('<td width="50%"></td>' if len(pair) == 1 else "") + "</tr>"
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{rows}</table>'
body = ""; total = 0
for titre, sous, f, n, slug in THEMES:
    xs = take(f, n)
    if len(xs) < 2: continue
    if len(xs) % 2: pris.discard(xs.pop()["asin"])
    total += len(xs)
    body += (f'<tr><td style="padding:22px 14px 2px;font-family:Arial,Helvetica,sans-serif"><h2 style="margin:0;font-size:21px;color:#c1121f">{titre}</h2>'
             f'<p style="margin:4px 0 6px;font-size:14px;color:#555555">{sous}</p></td></tr><tr><td style="padding:0 8px">{grid(xs)}</td></tr>'
             f'<tr><td align="center" style="padding:6px 14px 4px;font-family:Arial,Helvetica,sans-serif"><a href="{SITE}/{slug}/?utm_source=infolettre" target="_blank" style="font-size:14px;color:#c1121f;font-weight:bold">Voir tous les deals de cette section →</a></td></tr>')
vedette = D[0]
pre = f'{vedette["title"].split(",")[0]} à {money(vedette["price"])} (-{vedette["pct"]} %) et {total - 1} autres rabais triés pour toi.'
print(f'''<!DOCTYPE html><html lang="fr-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Les offres du jour · Rabais Flash QC</title></head>
<body style="margin:0;padding:0;background:#f6efe6">
<div style="display:none;max-height:0;overflow:hidden;font-size:1px;color:#f6efe6">{e(pre)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6efe6"><tr><td align="center" style="padding:14px 6px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#fffaf3;border-radius:14px;overflow:hidden">
<tr><td style="background:#c1121f;padding:22px 18px;font-family:Arial,Helvetica,sans-serif;text-align:center">
<a href="{SITE}/?utm_source=infolettre" target="_blank" style="color:#ffffff;text-decoration:none;font-size:15px;letter-spacing:2px">⚡ RABAIS <b style="color:#ffc629">FLASH</b> QC</a>
<h1 style="margin:10px 0 6px;color:#ffc629;font-size:26px;line-height:31px">Les {total} meilleurs deals du jour, déjà triés pour toi</h1>
<p style="margin:0;color:#ffffff;font-size:15px;line-height:21px">Les offres pré-Vendredi fou viennent de sortir, et on a fait le tour pour toi : marques connues, vrais rabais, jusqu'à -{vedette["pct"]} %. Les meilleures partent vite, fais ton tour avant ce soir!</p></td></tr>
<tr><td style="padding:16px 14px 0;font-family:Arial,Helvetica,sans-serif"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#fff3c9;border:2px dashed #c1121f;border-radius:12px"><tr>
<td width="120" align="center" style="padding:10px"><a href="{e(url(vedette))}" target="_blank"><img src="{e(vedette["img_url"])}" alt="{e(vedette["title"])}" width="110" height="110" style="display:block;width:110px;height:110px;object-fit:contain;border:0"></a></td>
<td style="padding:10px 12px 10px 0;font-family:Arial,Helvetica,sans-serif"><p style="margin:0;font-size:12px;font-weight:bold;color:#c1121f;letter-spacing:1px">LE COUP DE CŒUR DU JOUR</p>
<p style="margin:4px 0;font-size:16px;line-height:21px;font-weight:bold;color:#222222">{e(vedette["title"])}</p>
<p style="margin:0 0 8px;font-size:14px;color:#777777"><s>{money(vedette["was"])}</s> <b style="font-size:21px;color:#c1121f">{money(vedette["price"])}</b> <b style="color:#c1121f">(-{vedette["pct"]} %)</b></p>
<a href="{e(url(vedette))}" target="_blank" style="display:inline-block;background:#c1121f;color:#ffffff;font-weight:bold;font-size:14px;text-decoration:none;padding:9px 16px;border-radius:24px">J'en profite 👉</a></td></tr></table></td></tr>
{body}
<tr><td align="center" style="padding:24px 18px 8px;font-family:Arial,Helvetica,sans-serif"><p style="margin:0 0 10px;font-size:17px;font-weight:bold;color:#222222">Lequel tu prends en premier? 👀</p>
<a href="{SITE}/?utm_source=infolettre" target="_blank" style="display:inline-block;background:#c1121f;color:#ffffff;font-weight:bold;font-size:16px;text-decoration:none;padding:13px 26px;border-radius:28px">Voir tous les deals sur rabaisflashqc.ca</a>
<p style="margin:14px 0 0;font-size:14px;color:#555555">Tu connais quelqu'un qui magasine ses cadeaux? Transfère-lui ce courriel, il va te remercier. 🎁</p></td></tr>
<tr><td style="padding:16px 18px 22px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:17px;color:#888888;text-align:center">
Prix observés le {jour_txt}. Les prix et la disponibilité changent vite : vérifie le prix final avant d'acheter.<br>
En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.<br>
Tu reçois ce courriel parce que tu es inscrit aux deals de Rabais Flash QC.</td></tr>
</table></td></tr></table></body></html>''')
print(f"deals: {total} | objet: voir suivi/infolettres", file=sys.stderr)
