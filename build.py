#!/usr/bin/env python3
"""Génère le site statique rabaisflashqc.ca à partir de data.json."""
import json, html, os, datetime, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
DOMAIN = "https://rabaisflashqc.ca"
TAG = "coupdecoeurqc-20"
FB = "https://www.facebook.com/profile.php?id=61566039092981"
MS = "https://m.me/61566039092981"
DISCLOSURE = "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises."

data = json.loads((ROOT / "data.json").read_text())
DEALS, STORES, LUXE = data["deals"], data["stores"], set(data["luxe"])
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
TODAY = f"{NOW.day} {MOIS[NOW.month-1]} {NOW.year}"
e = html.escape

def link(d):
    if d.get("url"): return d["url"]
    if d.get("q"): return f"https://www.amazon.ca/s?k={urllib.parse.quote_plus(d['q'])}&tag={TAG}"
    return f"https://www.amazon.ca/dp/{d['asin']}?tag={TAG}"

def search(q): return f"https://www.amazon.ca/s?k={urllib.parse.quote_plus(q)}&tag={TAG}"

ICON = {"tech":"🎧","maison":"🏠","beaute":"💄","femme":"👗","homme":"👔","enfants":"🧸","jouets":"🧱","animaux":"🐾","halloween":"🎃","epicerie":"🛒"}

PAGES = [
  # slug, titre <title>, H1, intro, filtre, recherches de secours
  ("", "Rabais Flash QC · Les meilleurs rabais Amazon au Québec, triés pour toi",
   "Les meilleurs rabais d'Amazon, triés pour toi",
   "Tout coûte plus cher. Ici, on fait le tri pour toi : cadeaux, beauté, mode, enfants, épicerie. Les meilleurs rabais d'Amazon.ca, classés par thème sur une seule page, mis à jour souvent. Pas besoin de chercher pendant des heures.",
   lambda d: True, []),
  ("vendredi-fou", "Vendredi fou 2026 sur Amazon.ca · Les meilleurs deals triés | Rabais Flash QC",
   "Vendredi fou 2026 : les meilleurs deals d'Amazon.ca",
   "Le Vendredi fou tombe le 27 novembre 2026, et les premières offres d'Amazon.ca commencent souvent quelques jours avant. On trie les vrais rabais pour toi : cadeaux de Noël, beauté, maison, jouets, tech. Abonne-toi à notre page Facebook pour être averti dès que les deals sortent.",
   lambda d: d.get("live") and d.get("badge") == "gift", [("Offres du jour Amazon.ca","offres du jour")]),
  ("idees-cadeaux", "Idées cadeaux de Noël 2026 en rabais sur Amazon.ca | Rabais Flash QC",
   "Idées cadeaux de Noël 2026, à prix réduit",
   "Pour elle, pour lui, pour les enfants ou pour quelqu'un qui a déjà tout : nos idées cadeaux préférées, en rabais sur Amazon.ca. On choisit des marques connues, avec de bons avis, faciles à offrir.",
   lambda d: d.get("badge") == "gift", [("Cadeaux pour elle","cadeau pour femme"),("Cadeaux pour lui","cadeau pour homme"),("Cadeaux pour enfants","cadeau enfant")]),
  ("beaute", "Rabais beauté et beauté de luxe sur Amazon.ca | Rabais Flash QC",
   "Rabais beauté : maquillage, soins et beauté de luxe",
   "Maybelline, L'Oréal, Clarins, Kérastase, First Aid Beauty… Les meilleurs rabais beauté d'Amazon.ca, du maquillage de tous les jours aux soins de luxe. Les grandes marques de beauté baissent rarement leurs prix : quand c'est le cas, on te le montre ici.",
   lambda d: d["cat"] == "beaute" or d["brand"] in LUXE, [("Beauté de luxe","beauté de luxe")]),
  ("mode", "Rabais mode femme et homme sur Amazon.ca | Rabais Flash QC",
   "Rabais mode : femme et homme",
   "Bottes d'hiver, sacs, bijoux, montres, vêtements de tous les jours : nos coups de cœur mode en rabais sur Amazon.ca, avec une attention spéciale aux marques canadiennes et québécoises.",
   lambda d: d["cat"] in ("femme","homme"), [("Mode femme","vêtements femme"),("Mode homme","vêtements homme")]),
  ("enfants", "Rabais jouets, LEGO et articles pour enfants sur Amazon.ca | Rabais Flash QC",
   "Rabais jouets et articles pour enfants",
   "LEGO, jeux, jouets et essentiels pour les enfants, en rabais sur Amazon.ca. Parfait pour préparer Noël et les anniversaires sans faire exploser le budget.",
   lambda d: d["cat"] in ("enfants","jouets"), [("Meilleures ventes jouets","jouets")]),
  ("epicerie", "Rabais épicerie et essentiels sur Amazon.ca | Rabais Flash QC",
   "Épicerie et essentiels en rabais",
   "Le panier coûte cher? Voici les essentiels d'épicerie et du quotidien en rabais sur Amazon.ca : gros formats, collations, produits ménagers et marques d'ici. Astuce : Amazon offre souvent 5 % de plus quand tu prends 5 articles admissibles, et jusqu'à 15 % avec « Abonnez-vous et économisez ».",
   lambda d: d["cat"] == "epicerie", [("Meilleures ventes épicerie","épicerie")]),
  ("maison", "Rabais maison et cuisine sur Amazon.ca | Rabais Flash QC",
   "Rabais maison et cuisine",
   "Aspirateurs, friteuses à air, machines à café, mélangeurs : les meilleurs rabais maison et cuisine d'Amazon.ca, triés pour toi.",
   lambda d: d["cat"] == "maison", [("Meilleures ventes cuisine","cuisine")]),
  ("tech", "Rabais tech et audio sur Amazon.ca | Rabais Flash QC",
   "Rabais tech et audio",
   "Casques, écouteurs, haut-parleurs, accessoires : les meilleurs rabais tech d'Amazon.ca, de marques connues comme Sony, JBL, Bose et Logitech.",
   lambda d: d["cat"] == "tech", [("Meilleures ventes électronique","électronique")]),
  ("animaux", "Rabais animaux : chiens et chats sur Amazon.ca | Rabais Flash QC",
   "Rabais pour chiens et chats",
   "Jouets, griffoirs, litière, gâteries : les essentiels pour tes animaux, en rabais sur Amazon.ca.",
   lambda d: d["cat"] == "animaux", [("Meilleures ventes animaux","animaux")]),
  ("halloween", "Halloween 2026 : costumes, déco et bonbons en rabais | Rabais Flash QC",
   "Halloween 2026 : costumes, déco et bonbons",
   "Tout pour être prêt le 31 octobre : costumes pour enfants et adultes, décorations, maquillage et bonbons en vrac, livrés vite avec Prime. Commande tôt, les tailles populaires partent vite!",
   lambda d: d["cat"] == "halloween" or d["brand"] == "Yupik", [("Déguisements","halloween déguisement"),("Déco d'Halloween","halloween decor"),("Bonbons d'Halloween","halloween bonbons"),("Maquillage d'Halloween","halloween maquillage")]),
]
NAV = [("", "Accueil"), ("vendredi-fou","Vendredi fou"), ("idees-cadeaux","Cadeaux"), ("beaute","Beauté"), ("mode","Mode"), ("enfants","Enfants"), ("epicerie","Épicerie"), ("maison","Maison"), ("tech","Tech"), ("animaux","Animaux"), ("halloween","Halloween")]

CSS = """
:root{--red:#C1121F;--deep:#8E0B16;--yel:#FFC72C;--ink:#1A1A1A;--muted:#5C5C5C;--line:#ECD7D9;--paper:#fff}
*{box-sizing:border-box}body{margin:0;font-family:'Barlow Semi Condensed','Helvetica Neue',Arial,sans-serif;font-size:18px;line-height:1.45;color:var(--ink);background:var(--paper)}
a{color:inherit}.wrap{max-width:760px;margin:0 auto;padding:0 18px}
header{background:var(--red);color:#fff;padding:16px 0 22px}
.logo{display:flex;align-items:center;gap:8px;font-family:Anton,Impact,sans-serif;font-size:22px;letter-spacing:1px;text-decoration:none;color:#fff}.logo b{color:var(--yel);font-weight:400}
h1{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:clamp(34px,8vw,54px);line-height:1;margin:14px 0 10px;color:var(--yel)}
.intro{margin:0;font-size:18px;max-width:40em}.upd{font-size:14px;opacity:.85;margin-top:8px}
nav{display:flex;gap:8px;overflow-x:auto;padding:12px 0;scrollbar-width:none;border-bottom:1px solid var(--line)}nav::-webkit-scrollbar{display:none}
nav a{flex:none;text-decoration:none;font-weight:700;font-size:16px;padding:7px 14px;border-radius:999px;border:2px solid var(--red);color:var(--deep)}
nav a[aria-current]{background:var(--red);color:#fff}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.btn{display:inline-block;text-decoration:none;font-weight:700;padding:10px 18px;border-radius:999px;background:var(--yel);color:var(--deep)}
.btn.alt{background:#fff;border:2px solid var(--deep)}
ul.deals{list-style:none;padding:0;margin:8px 0}
.deal{display:grid;grid-template-columns:84px 1fr;gap:16px;padding:18px 0;border-bottom:1px solid var(--line)}
.tag{width:84px;height:84px;border-radius:14px;background:var(--yel);color:var(--deep);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Anton,Impact,sans-serif;font-size:30px;line-height:1}
.tag small{font-family:inherit;font-size:12px;font-weight:700;margin-top:4px}
.brand{margin:0;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--red)}
.deal h3{margin:2px 0 6px;font-size:20px;line-height:1.2}.why{margin:0 0 8px;color:var(--muted)}
.badges span{display:inline-block;font-size:13px;font-weight:700;background:#FFF3D1;color:var(--deep);border-radius:6px;padding:2px 8px;margin:0 6px 6px 0}
.go{display:inline-block;text-decoration:none;font-weight:700;background:var(--red);color:#fff;padding:9px 16px;border-radius:10px}
h2{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:28px;color:var(--red);margin:28px 0 8px}
.more{display:flex;flex-wrap:wrap;gap:8px}.more a{text-decoration:none;font-weight:700;padding:8px 14px;border-radius:999px;background:#FFF3D1;color:var(--deep)}
.gang{background:var(--yel);color:#4A0610;border-radius:18px;padding:18px;margin:28px 0}.gang h2{color:#4A0610;margin-top:0}
.gang .cta .btn{background:#fff}
footer{margin:30px 0 40px;font-size:15px;color:var(--muted)}footer a{margin-right:12px}
.empty{padding:20px 0;color:var(--muted)}
@media (max-width:420px){.deal{grid-template-columns:70px 1fr}.tag{width:70px;height:70px;font-size:24px}}
"""

BOLT = '<svg width="16" height="26" viewBox="0 0 100 160" aria-hidden="true"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFC72C"/></svg>'

def deal_html(d):
    pct = d.get("amzPct") or d.get("pct")
    if d.get("live") and pct:
        tag = f'<div class="tag">-{pct}%<small>{"sous la moy." if d.get("vsAvg") else "sur Amazon"}</small></div>'
    else:
        tag = f'<div class="tag" aria-hidden="true">{ICON.get(d["cat"],"⭐")}</div>'
    badges = []
    if d.get("live") and d.get("flag"): badges.append(d["flag"])
    if d.get("badge") == "gift": badges.append("Idée cadeau")
    if d.get("badge") == "local": badges.append("⚜️ Marque d'ici")
    if d.get("badge") == "canada": badges.append("🍁 Marque canadienne")
    b = f'<p class="badges">{"".join(f"<span>{e(x)}</span>" for x in badges)}</p>' if badges else ""
    why = f'<p class="why">{e(d["why"])}</p>' if d.get("why") else ""
    until = f' data-until="{d["until"]}"' if d.get("until") else ""
    return (f'<li class="deal"{until}>{tag}<div>{b}<p class="brand">{e(d["brand"])}</p><h3>{e(d["name"])}</h3>{why}'
            f'<a class="go" href="{e(link(d))}" target="_blank" rel="sponsored nofollow noopener">Voir le prix sur Amazon.ca</a></div></li>')

def order(items):
    return sorted(items, key=lambda d: (0 if d.get("live") else 1, -(d.get("amzPct") or d.get("pct") or 0), d["r"]))

def page(slug, title, h1, intro, items, extra="", after=""):
    url = f"{DOMAIN}/{slug + '/' if slug else ''}"
    nav = "".join(f'<a href="/{s + "/" if s else ""}"{" aria-current=\"page\"" if s == slug else ""}>{e(n)}</a>' for s, n in NAV)
    ld = {"@context":"https://schema.org","@type":"WebPage","name":title,"url":url,"inLanguage":"fr-CA",
          "isPartOf":{"@type":"WebSite","name":"Rabais Flash QC","url":DOMAIN+"/"},
          "publisher":{"@type":"Organization","name":"Rabais Flash QC","url":DOMAIN+"/","sameAs":[FB]}}
    lst = "".join(deal_html(d) for d in items) or '<li class="empty">On est en train de dénicher les prochains deals pour cette section. Reviens bientôt!</li>'
    return f"""<!doctype html>
<html lang="fr-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(intro[:155])}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(intro[:155])}">
<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="fr_CA">
<meta property="og:image" content="{DOMAIN}/couverture.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 160'%3E%3Cpath d='M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z' fill='%23C1121F'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Semi+Condensed:wght@500;700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body><header><div class="wrap"><a class="logo" href="/">{BOLT} RABAIS <b>FLASH</b> QC</a>
<h1>{e(h1)}</h1><p class="intro">{e(intro)}</p><p class="upd">Mis à jour le {TODAY}</p></div></header>
<main class="wrap"><nav aria-label="Thèmes">{nav}</nav>
{extra}
<ul class="deals">{lst}</ul>
{after}
<section class="gang"><h2>Rejoins la gang 🔔</h2><p>Les meilleurs deals du Vendredi fou et du Boxing Day sortent d'abord pour ceux qui nous suivent. C'est gratuit.</p>
<div class="cta"><a class="btn" href="{FB}" target="_blank" rel="noopener">👍 Suivre sur Facebook</a><a class="btn" href="{MS}" target="_blank" rel="noopener">💬 Alertes Messenger</a></div></section>
<footer><p>Les prix sur Amazon changent souvent. Vérifie toujours le prix actuel sur Amazon.ca avant d'acheter.</p>
<p>{DISCLOSURE}</p><p><a href="/a-propos/">À propos</a><a href="/confidentialite/">Confidentialité</a><a href="{FB}" rel="noopener">Facebook</a></p></footer>
</main><script>document.querySelectorAll('[data-until]').forEach(function(li){{if(Date.now()>Date.parse(li.dataset.until))li.remove();}});</script></body></html>"""

def simple(slug, title, h1, body):
    return page(slug, title, h1, "", [], extra=body).replace('<ul class="deals"><li class="empty">On est en train de dénicher les prochains deals pour cette section. Reviens bientôt!</li></ul>', "").replace('<p class="intro"></p>', "")

def write(slug, content):
    p = OUT / slug / "index.html" if slug else OUT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)

def main():
    OUT.mkdir(exist_ok=True)
    urls = []
    for slug, title, h1, intro, f, more in PAGES:
        items = order([d for d in DEALS if f(d)])
        extra = after = ""
        if more:
            after = '<h2>Plus de choix sur Amazon.ca</h2><p class="more">' + "".join(f'<a href="{e(search(q))}" target="_blank" rel="sponsored nofollow noopener">{e(n)}</a>' for n, q in more) + "</p>"
        if slug == "":
            extra = ('<h2>Les offres de tes marques préférées</h2><p class="more">' +
                     "".join(f'<a href="{e(u)}" target="_blank" rel="sponsored nofollow noopener">{e(n)}</a>' for n, u in STORES.items()) + "</p><h2>Les deals du moment</h2>")
        write(slug, page(slug, title, h1, intro, items, extra, after)); urls.append(slug)
    write("a-propos", simple("a-propos", "À propos de Rabais Flash QC", "À propos",
        "<h2>Qui on est</h2><p>Rabais Flash QC est un projet québécois, né à Saint-Bruno-de-Montarville. Tout coûte plus cher, alors on fait le tri des aubaines d'Amazon.ca pour te faire gagner du temps et de l'argent.</p>"
        "<h2>Comment on choisit</h2><p>On garde surtout des rabais affichés par Amazon sur des marques connues, avec de bons avis. On classe tout par thème et on retire les offres expirées. Les prix changent souvent : vérifie toujours le prix final sur Amazon.ca.</p>"
        f"<h2>Transparence</h2><p>{DISCLOSURE} Ça ne change rien au prix que tu paies.</p>"
        f'<h2>Nous joindre</h2><p>Écris-nous sur <a href="{MS}">Messenger</a> ou sur notre <a href="{FB}">page Facebook</a>.</p>')); urls.append("a-propos")
    write("confidentialite", simple("confidentialite", "Politique de confidentialité | Rabais Flash QC", "Politique de confidentialité",
        "<p>Ce site ne te demande aucune information personnelle pour consulter les deals. Il n'utilise pas de témoins publicitaires qui lui sont propres.</p>"
        "<p>Quand tu cliques sur un lien vers Amazon.ca, Amazon peut utiliser des témoins pour attribuer l'achat, selon sa propre politique de confidentialité.</p>"
        "<p>Si tu t'inscris à notre infolettre, ton adresse courriel sert seulement à t'envoyer nos aubaines. Tu peux te désabonner en tout temps avec le lien présent dans chaque courriel. Pour toute question sur tes renseignements personnels, écris-nous sur Messenger.</p>"
        f"<p>Dernière mise à jour : {TODAY}.</p>")); urls.append("confidentialite")
    (OUT / "CNAME").write_text("rabaisflashqc.ca\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<url><loc>{DOMAIN}/{u + '/' if u else ''}</loc><lastmod>{NOW.date()}</lastmod></url>" for u in urls) + "</urlset>\n")
    print("pages:", len(urls))

if __name__ == "__main__":
    main()
