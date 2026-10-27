#!/usr/bin/env python3
"""Génère le site statique rabaisflashqc.ca à partir de data.json."""
import re, json, html, os, datetime, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
DOMAIN = "https://rabaisflashqc.ca"
TAG = "coupdecoeurqc-20"
FB = "https://www.facebook.com/rabaisflashqc"
MS = "https://m.me/61566039092981"
NEWSLETTER_ACTION = ""  # URL du formulaire MailerLite, à remplir
DISCLOSURE = "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises."

data = json.loads((ROOT / "data.json").read_text())
DEALS, STORES, LUXE = data["deals"], data["stores"], set(data["luxe"])
STORE_CAT = data.get("store_cat", {})
HOME_STORES = ["Clarins","Lancôme","Kérastase","Ninja","Nespresso","Shark","Apple","Sony","Bose","LEGO","Yupik","La Roche-Posay"]
_today = datetime.date.today()
def _age(d):
    try: return (_today - datetime.date.fromisoformat(d.get("added", ""))).days
    except ValueError: return 0
_keep = []
for _d in DEALS:
    if _d.get("until") and datetime.datetime.fromisoformat(_d["until"].replace("Z", "+00:00")) < datetime.datetime.now(datetime.timezone.utc):
        continue  # offre éclair terminée
    if _age(_d) > 7:
        continue  # plus de 7 jours : retiré
    if _age(_d) > 5 and _d.get("live"):
        _d = {k: v for k, v in _d.items() if k not in ("live", "pct", "amzPct", "flag", "vsAvg")}  # rabais non revérifié : coup de cœur
    _keep.append(_d)
DEALS = _keep
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
TODAY = f"{NOW.day} {MOIS[NOW.month-1]} {NOW.year}"
e = html.escape


HWFLOAT = '<div class="fl" aria-hidden="true">' + "".join(f'<i style="left:{l};top:{t};animation-delay:{d}">{e_}</i>' for e_,l,t,d in [("🦇","6%","12%","0s"),("👻","86%","14%","-2s"),("🕸️","92%","62%","-4s"),("🎃","3%","70%","-6s"),("🦇","60%","6%","-3s"),("🍬","72%","80%","-5s")]) + '</div>'
HWCOUNT = '<div class="hwcount" id="hwc"></div><script>(function(){var d=Math.ceil((Date.parse("2026-10-31T04:00:00Z")-Date.now())/864e5),el=document.getElementById("hwc");el.innerHTML=d>1?"Plus que <b>"+d+"</b> jours avant l\'Halloween":d===1?"C\'est <b>demain</b>! 👻":d===0?"C\'est <b>aujourd\'hui</b>! 🎃":"À l\'an prochain! 🎃";})();</script>'
HWT = "&tag=" + TAG
HWTILES = [("👻","Déguisements","Enfants et adultes, livrés avec Prime","https://www.amazon.ca/s?k=halloween+d%C3%A9guisement&rh=p_85%3A5690392011"+HWT),
("🦇","Déco d'Halloween","Gonflables, toiles, lumières","https://www.amazon.ca/-/fr/s?k=halloween+decor&rh=p_85%3A5690392011"+HWT),
("🍬","Bonbons","Pour les petits monstres","https://www.amazon.ca/s?k=halloween+bonbons&rh=p_85%3A5690392011"+HWT),
("💄","Maquillage","Faux sang, peinture, faux cils","https://www.amazon.ca/-/fr/s?k=halloween+maquillage&rh=p_85%3A5690392011"+HWT),
("👕","Vêtements d'Halloween","Chandails, pyjamas, bas","https://www.amazon.ca/s?k=halloween+vetement"+HWT),
("🐶","Costumes pour chien","Le plus cute du quartier","https://www.amazon.ca/s?k=costume+halloween+chien"+HWT),
("🎃","Sculpter sa citrouille","Kits, pochoirs, lumières","https://www.amazon.ca/s?k=kit+sculpture+citrouille"+HWT),
("⚜️","Bonbons Yupik","Une entreprise d'ici","https://www.amazon.ca/stores/page/57352AFD-8FA7-4764-9A8F-E1C0C8CC4E3C/deals?linkCode=ll2"+HWT)]

PRIME = "p_85%3A5690392011"
def sp(q, hi=None, lo=None):
    """Recherche Amazon.ca avec Prime et, au besoin, une fourchette de prix (en dollars)."""
    rh = PRIME
    if hi or lo: rh += f"%2Cp_36%3A{int((lo or 0)*100) if lo else ''}-{int(hi*100) if hi else ''}"
    return f"https://www.amazon.ca/s?k={urllib.parse.quote_plus(q)}&rh={rh}&tag={TAG}"

# Guides cadeaux : (slug, <title>, H1, intro, tuiles [(emoji, idée, pourquoi, recherche, prix max)], filtre deals, marques)
GUIDES = [
 ("pour-elle", "Idées cadeaux pour elle 2026 : femme, maman, amie | Rabais Flash QC",
  "Idées cadeaux pour elle",
  "Pour ta blonde, ta mère, ta sœur ou une amie : des idées qui font plaisir à coup sûr, de la petite attention à 25 $ au cadeau qui impressionne. Des marques connues, livrées vite avec Prime.",
  [("💄","Coffret beauté de luxe","Clarins, Lancôme, Kiehl's : déjà emballé","coffret cadeau beauté luxe",None),
   ("🌸","Parfum","Le classique qui ne déçoit jamais","parfum femme",None),
   ("👜","Sac à main","Michael Kors, Coach, Kate Spade","sac à main femme Michael Kors Coach",None),
   ("🕯️","Bougie parfumée","Yankee Candle et compagnie","bougie parfumée cadeau",40),
   ("💍","Bijoux","Argent sterling, simples et élégants","bijoux argent sterling femme",80),
   ("🧣","Pyjama ou robe de chambre","Le confort du dimanche matin","pyjama femme doux",60),
   ("☕","Pour l'amatrice de café","Nespresso, tasses, mousseur","cadeau amateur café",None),
   ("🧖‍♀️","Soirée spa à la maison","Masques, sels de bain, peignoir","coffret spa femme",50)],
  lambda d: d["cat"] in ("beaute","femme") and (d.get("badge") == "gift" or d["brand"] in LUXE),
  ["Clarins","Lancôme","Kiehl's","Estée Lauder","Michael Kors","Coach","Kate Spade","UGG"]),
 ("pour-lui", "Idées cadeaux pour lui 2026 : homme, papa, chum | Rabais Flash QC",
  "Idées cadeaux pour lui",
  "Pour ton chum, ton père, ton frère ou un collègue : des cadeaux pratiques et des valeurs sûres, du gadget à 30 $ à la montre qui fait de l'effet.",
  [("⌚","Montre","Fossil, Timex, Casio","montre homme Fossil",None),
   ("🎧","Écouteurs ou casque","Sony, Bose, JBL","écouteurs sans fil Sony Bose",None),
   ("🧴","Coffret rasage et soins","Pour la barbe et la peau","coffret rasage homme",60),
   ("🍖","Pour le roi du BBQ","Thermomètre, outils, sauces","accessoires BBQ cadeau homme",60),
   ("🔧","Outils et gadgets","Le cadeau qu'il va vraiment utiliser","gadget outil cadeau homme",50),
   ("🧥","Manteau ou tuque d'hiver","Columbia, The North Face","manteau hiver homme Columbia",None),
   ("🥃","Ensemble à whisky","Verres et pierres à refroidir","ensemble verres whisky",50),
   ("🎮","Pour le gamer","Manettes, casques, cartes-cadeaux jeux","accessoires gamer cadeau",None)],
  lambda d: d["cat"] in ("homme","tech","plein-air") or d.get("for") == "lui",
  ["Sony","Bose","Apple","Samsung","Columbia","Fossil","adidas"]),
 ("ado", "Idées cadeaux pour ado 2026 : 12 à 17 ans, gars et filles | Rabais Flash QC",
  "Idées cadeaux pour ado (12 à 17 ans)",
  "Trouver un cadeau pour un ado, c'est un sport extrême. Voici les valeurs sûres de cette année : tech, soins de la peau, sport et déco de chambre.",
  [("🎧","Écouteurs sans fil","Le cadeau qu'ils réclament tous","écouteurs sans fil ado",None),
   ("💡","Lumières DEL pour la chambre","Bandes DEL et lampes d'ambiance","lumières DEL chambre",40),
   ("🧴","Soins de la peau","CeraVe, La Roche-Posay : la routine des ados","CeraVe coffret",50),
   ("🥤","Gourde tendance","Stanley, Owala","gourde Stanley Owala",60),
   ("📸","Appareil photo instantané","Instax : souvenirs à coller partout","Instax mini",None),
   ("🎮","Gaming","Manettes, casques, accessoires","accessoires gaming ado",None),
   ("🔊","Haut-parleur portable","JBL, pour la musique partout","JBL haut-parleur",None),
   ("🧸","Squishmallows","Même les grands en veulent","Squishmallows",40)],
  lambda d: d["cat"] == "tech" or d["brand"] in ("CeraVe","Stanley","JBL","Squishmallows"),
  ["Apple","JBL","Sony","CeraVe","La Roche-Posay","Stanley","Squishmallows","Skullcandy"]),
 ("enfants", "Idées cadeaux pour enfants 2026 : jouets par âge | Rabais Flash QC",
  "Idées cadeaux pour enfants",
  "Des jouets qui vont servir plus que deux jours : LEGO, jeux de société, bricolage et jouets éducatifs, classés pour te simplifier la vie.",
  [("🧱","LEGO","Le cadeau qui ne se démode pas","LEGO",None),
   ("🎲","Jeux de société famille","Pour les soirées sans écran","jeu de société famille",50),
   ("🎨","Bricolage et art","Pâte à modeler, peinture, perles","bricolage enfant",40),
   ("🔬","Jouets éducatifs","Science, robots, STEM","jouet éducatif STEM",None),
   ("🚗","Hot Wheels","Pistes et voitures","Hot Wheels piste",None),
   ("👶","Pour les tout-petits","Melissa & Doug, Fisher-Price","jouet bébé Melissa Doug",50),
   ("📚","Livres en français","Pour aimer lire","livre enfant français",30),
   ("🛷","Jouer dehors l'hiver","Traîneaux, jeux de neige","traîneau enfant",None)],
  lambda d: d["cat"] in ("enfants","jouets"),
  ["LEGO","Squishmallows"]),
 ("moins-de-25", "Cadeaux à moins de 25 $ sur Amazon.ca : 2026 | Rabais Flash QC",
  "Cadeaux à moins de 25 $",
  "Échange de cadeaux au bureau, voisin, prof, cadeau de dernière minute : de bonnes idées à moins de 25 $, qui ont l'air d'en valoir le double.",
  [("🕯️","Bougies","Petit prix, gros effet","bougie parfumée",25),
   ("🧦","Bas drôles","Le classique des échanges","bas drôles cadeau",25),
   ("☕","Tasse ou café","Pour le collègue accro","tasse cadeau drôle",25),
   ("🍫","Gourmandises","Chocolats et bonbons","coffret chocolat cadeau",25),
   ("🧴","Crème mains et baume","Burt's Bees, L'Occitane","coffret crème mains",25),
   ("🔌","Gadget tech","Chargeurs, supports, câbles","gadget tech cadeau",25),
   ("🎲","Petit jeu","Cartes, casse-têtes","jeu de cartes party",25),
   ("🧸","Jouet","Pour les petits","jouet enfant",25)],
  lambda d: d.get("price") and d["price"] <= 25,
  ["Yupik","NIVEA","e.l.f.","Maybelline"]),
 ("moins-de-50", "Cadeaux à moins de 50 $ sur Amazon.ca : 2026 | Rabais Flash QC",
  "Cadeaux à moins de 50 $",
  "Le budget parfait pour faire plaisir sans se ruiner : beauté, cuisine, tech et jouets, des marques connues entre 25 $ et 50 $.",
  [("💄","Coffret beauté","Des marques connues","coffret beauté",50),
   ("🎧","Écouteurs","Bons et pas chers","écouteurs sans fil",50),
   ("🥤","Gourde ou thermos","Stanley et compagnie","gourde isotherme",50),
   ("🧱","LEGO","Petits ensembles","LEGO",50),
   ("🍳","Cuisine","Gadgets et ustensiles","gadget cuisine cadeau",50),
   ("🕯️","Déco douillette","Couverture, bougies","couverture douce",50),
   ("🎲","Jeu de société","Pour toute la famille","jeu de société",50),
   ("🐾","Pour l'animal","Jouets et gâteries","jouet chien",50)],
  lambda d: d.get("price") and 25 < d["price"] <= 50,
  ["La Roche-Posay","CeraVe","Stanley","LEGO","JBL"]),
 ("bas-de-noel", "Idées pour le bas de Noël 2026 : petits cadeaux | Rabais Flash QC",
  "Idées pour le bas de Noël",
  "Les petites surprises qui remplissent le bas de Noël, pour les enfants comme pour les grands, presque toutes à moins de 15 $.",
  [("🍬","Bonbons et chocolats","L'incontournable","bonbons Noël",15),
   ("💋","Baume à lèvres et petits soins","Burt's Bees, Nivea","baume à lèvres coffret",15),
   ("🧦","Bas et mitaines","Doux et pratiques","bas Noël",15),
   ("🔋","Piles!","Pour que les jouets marchent le matin de Noël","piles AA",20),
   ("🎨","Petits bricolages","Autocollants, crayons","autocollants enfant",15),
   ("🧸","Mini peluches","Squishmallows format bas","Squishmallows mini",15),
   ("🔑","Porte-clés et gadgets","Le petit fun","porte-clés drôle",15),
   ("🎴","Cartes Pokémon","Les jeunes adorent","cartes Pokémon",20)],
  lambda d: d.get("price") and d["price"] <= 15,
  ["Yupik","NIVEA","Squishmallows"]),
 ("homme-qui-a-tout", "Cadeau pour un homme qui a tout : 2026 | Rabais Flash QC",
  "Cadeau pour quelqu'un qui a déjà tout",
  "Ton père, ton beau-frère, ton patron : il a déjà tout et ne veut rien. Voici des idées originales qui vont quand même le surprendre.",
  [("🧊","Pierres à whisky","Le petit luxe utile","pierres à whisky",50),
   ("🔥","Foyer de table","Ambiance instantanée","foyer de table",None),
   ("🌡️","Thermomètre à viande intelligent","Pour le BBQ parfait","thermomètre viande sans fil",None),
   ("🔦","Lampe frontale rechargeable","Il va s'en servir tout le temps","lampe frontale rechargeable",50),
   ("🎒","Sac de qualité","Pour le gym ou le voyage","sac de voyage homme",None),
   ("🧤","Gants chauffants","Le cadeau de l'hiver québécois","gants chauffants",None),
   ("🧩","Casse-tête 1000 morceaux","Pour décrocher","casse-tête 1000 morceaux",30),
   ("📷","Cadre photo numérique","Les photos de la famille","cadre photo numérique",None)],
  lambda d: d["cat"] in ("homme","maison","tech","plein-air") and d.get("badge") == "gift",
  ["Dyson","Ninja","Bose","Sony","Samsonite"]),
]

MSKEY = {"beaute":("BEAUTÉ","beauté"),"mode":("MODE","mode"),"enfants":("ENFANTS","jouets et enfants"),"epicerie":("ÉPICERIE","épicerie"),
         "maison":("MAISON","maison et cuisine"),"tech":("TECH","tech"),"animaux":("ANIMAUX","animaux"),"plein-air":("PLEINAIR","plein air et outils"),"halloween":("HALLOWEEN","Halloween"),
         "idees-cadeaux":("CADEAUX","idées cadeaux"),"vendredi-fou":("VENDREDI FOU","Vendredi fou"),"":("DEALS","meilleurs deals")}
def msbtn(slug):
    k = MSKEY.get(slug.split("/")[0], MSKEY[""])
    return f'<a class="msa" href="{MS}?ref={slug.split('/')[0] or 'deals'}" target="_blank" rel="noopener">💬 Reçois les alertes {e(k[1])} : écris {e(k[0])} sur Messenger</a>'

BUDGET = """<div class="bud" role="group" aria-label="Filtrer par budget"><button aria-pressed="true" data-b="0-1e9">Tous les prix</button><button aria-pressed="false" data-b="0-25">Moins de 25 $</button><button aria-pressed="false" data-b="0-50">Moins de 50 $</button><button aria-pressed="false" data-b="50-100">50 à 100 $</button><button aria-pressed="false" data-b="100-1e9">100 $ et plus</button></div>
<script>document.addEventListener("click",function(ev){var b=ev.target.closest(".bud button");if(!b)return;var r=b.dataset.b.split("-").map(Number);b.parentNode.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed",x===b)});document.querySelectorAll("ul.deals>li").forEach(function(li){var p=parseFloat(li.dataset.price);li.hidden=r[0]===0&&r[1]>1e8?false:!(p>=r[0]&&p<=r[1]);});});</script>"""

def club():
    if NEWSLETTER_ACTION:
        form = (f'<form action="{NEWSLETTER_ACTION}" method="post" target="_blank"><label class="sr" for="em" hidden>Ton courriel</label>'
                '<input type="email" id="em" name="fields[email]" placeholder="Ton courriel" required autocomplete="email">'
                '<button type="submit">Je veux les alertes</button>'
                '<label class="ok"><input type="checkbox" name="consent" required> J\'accepte de recevoir les courriels de Rabais Flash QC. Je peux me désabonner en tout temps.</label></form>')
    else:
        form = '<p class="soon">📬 Inscriptions à l\'infolettre très bientôt. En attendant, active les alertes Messenger 👇</p>'
    return ('<section class="club" aria-label="Rejoins la gang"><h2>🔔 Ne paie plus jamais le gros prix</h2>'
            '<p>Rejoins la gang et reçois <b>gratuitement</b> les meilleures aubaines avant tout le monde :</p>'
            '<ul><li>🔥 Les deals du <b>Vendredi fou</b> en primeur</li><li>🎁 Le <b>Guide cadeaux</b> de Noël par budget</li><li>⚡ Les offres éclair avant qu\'elles disparaissent</li></ul>'
            + form +
            f'<div class="social"><a href="{FB}" target="_blank" rel="noopener"><b>👍</b>Aime la page</a>'
            f'<a href="{FB}" target="_blank" rel="noopener"><b>🔔</b>Active les notifs</a>'
            f'<a class="ms" href="{MS}" target="_blank" rel="noopener"><b>💬</b>Alertes Messenger</a></div>'
            '<p class="small">Pour les notifications : sur notre page Facebook, touche « Suivre », puis la cloche, et choisis « Toutes les publications ». Zéro pourriel, promis.</p></section>')

def link(d):
    if d.get("url"): return d["url"]
    if d.get("q"): return f"https://www.amazon.ca/s?k={urllib.parse.quote_plus(d['q'])}&tag={TAG}"
    return f"https://www.amazon.ca/dp/{d['asin']}?tag={TAG}"

def search(q): return f"https://www.amazon.ca/s?k={urllib.parse.quote_plus(q)}&tag={TAG}"

ICON = {"tech":"🎧","maison":"🏠","beaute":"💄","femme":"👗","homme":"👔","enfants":"🧸","jouets":"🧱","animaux":"🐾","plein-air":"🏕️","halloween":"🎃","epicerie":"🛒"}

PAGES = [
  # slug, titre <title>, H1, intro, filtre, recherches de secours
  ("", "Rabais Flash QC · Les meilleurs rabais Amazon au Québec, triés pour toi",
   "Les meilleurs rabais d'Amazon, triés pour toi",
   "Tout coûte plus cher. Ici, on fait le tri pour toi : les meilleurs rabais d'Amazon.ca, mis à jour chaque jour, sans chercher pendant des heures.",
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
  ("plein-air", "Rabais plein air, outils et jardin sur Amazon.ca | Rabais Flash QC",
   "Rabais plein air, outils et jardin",
   "Batteries d'outils, filtres à eau, bouteilles isothermes, souffleurs à feuilles : le matériel qui sert dehors, au chalet et dans le garage, en rabais sur Amazon.ca.",
   lambda d: d["cat"] == "plein-air", [("Meilleures ventes outils","outils"),("Camping et randonnée","camping randonnée")]),
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
   lambda d: d["cat"] == "halloween" or d.get("hw"), [("Déguisements","halloween déguisement"),("Déco d'Halloween","halloween decor"),("Bonbons d'Halloween","halloween bonbons"),("Maquillage d'Halloween","halloween maquillage")]),
]
NAV = [("", "Accueil"), ("vendredi-fou","Vendredi fou"), ("idees-cadeaux","Cadeaux"), ("beaute","Beauté"), ("mode","Mode"), ("enfants","Enfants"), ("epicerie","Épicerie"), ("maison","Maison"), ("plein-air","Plein air"), ("tech","Tech"), ("animaux","Animaux")]

CSS = """
:root{--red:#C1121F;--deep:#8E0B16;--yel:#FFC72C;--ink:#1A1A1A;--muted:#5C5C5C;--line:#ECD7D9;--paper:#fff}
*{box-sizing:border-box}body{margin:0;font-family:'Barlow Semi Condensed','Helvetica Neue',Arial,sans-serif;font-size:18px;line-height:1.45;color:var(--ink);background:var(--paper)}
a{color:inherit}.wrap{max-width:760px;margin:0 auto;padding:0 18px}
header{background:var(--red);color:#fff;padding:16px 0 22px}
.logo{display:flex;align-items:center;gap:8px;font-family:Anton,Impact,sans-serif;font-size:22px;letter-spacing:1px;text-decoration:none;color:#fff}.logo b{color:var(--yel);font-weight:400}
h1{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:clamp(34px,8vw,54px);line-height:1;margin:14px 0 10px;color:var(--yel)}
.intro{margin:0;font-size:18px;max-width:40em}.upd{font-size:14px;opacity:.85;margin-top:8px}
nav{display:flex;flex-wrap:wrap;gap:8px;padding:12px 0;border-bottom:1px solid var(--line)}@media (max-width:600px){nav{gap:6px}nav a{font-size:14px!important;padding:6px 11px!important}}
nav a{flex:none;text-decoration:none;font-weight:700;font-size:16px;padding:7px 14px;border-radius:999px;border:2px solid var(--red);color:var(--deep)}
nav a[aria-current]{background:var(--red);color:#fff}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.btn{display:inline-block;text-decoration:none;font-weight:700;padding:10px 18px;border-radius:999px;background:var(--yel);color:var(--deep)}
.btn.alt{background:#fff;border:2px solid var(--deep)}
ul.deals{list-style:none;padding:0;margin:8px 0}
.deal{display:grid;grid-template-columns:84px 1fr;gap:16px;padding:18px 0;border-bottom:1px solid var(--line)}
.tag{width:84px;height:84px;border-radius:14px;background:var(--yel);color:var(--deep);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Anton,Impact,sans-serif;font-size:30px;line-height:1}
.tag small{font-family:inherit;font-size:12px;font-weight:700;margin-top:4px}
.pic{position:relative;width:84px;height:84px;border-radius:14px;background:#fff;border:1px solid var(--line);overflow:hidden}.pic img{width:100%;height:100%;object-fit:contain}.pic b{position:absolute;left:4px;top:4px;background:var(--yel);color:var(--deep);font-family:Anton,Impact,sans-serif;font-weight:400;font-size:17px;padding:1px 6px;border-radius:8px}
.brand{margin:0;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--red)}
.idg{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:14px 0}@media (min-width:760px){.idg{grid-template-columns:repeat(4,1fr)}}.idg a{display:flex;flex-direction:column;gap:4px;padding:14px;border-radius:16px;text-decoration:none;color:var(--ink);background:#FFF8E1;border:2px solid var(--yel);min-height:96px}.idg a:hover{background:#FFEFC2}.idg b{font-size:30px;line-height:1}.idg span{font-weight:700;color:var(--deep)}.idg small{font-size:14px;color:var(--muted)}.bud{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.bud button{font:inherit;font-weight:700;padding:8px 14px;border-radius:999px;border:2px solid var(--red);background:#fff;color:var(--red);cursor:pointer}.bud button[aria-pressed=true]{background:var(--red);color:#fff}.msa{display:inline-block;margin:6px 0 14px;padding:10px 16px;border-radius:999px;background:#0084FF;color:#fff;font-weight:700;text-decoration:none}@media (max-width:600px){header{padding-top:10px!important;padding-bottom:12px!important}header h1{font-size:30px!important;margin:6px 0 4px!important;line-height:1.05!important}header .intro{font-size:15px!important;margin:0 0 4px!important}header .upd{display:none}.hwcta strong,.seas strong{font-size:19px!important}.hwcta,.seas{padding:10px 14px!important;margin:8px 0!important}.hwcta span,.seas span{font-size:14px!important}.hwcta em,.seas em{font-size:28px!important}nav{padding:8px 0!important}}.clubbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:#FFF7DD;border:2px solid var(--yel);border-radius:14px;padding:8px 12px;margin:10px 0;font-weight:700;color:var(--deep);font-size:16px}.clubbar a{text-decoration:none;background:#fff;border:2px solid var(--deep);color:var(--deep);border-radius:999px;padding:5px 12px;font-size:15px}.seas{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:12px 0;padding:14px 16px;border-radius:16px;text-decoration:none;color:#fff;background:linear-gradient(120deg,#8E0B16,#C1121F);border:2px solid var(--yel)}.seas strong{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:24px;line-height:1;color:var(--yel);display:block}.seas span{font-weight:600;font-size:16px}.seas em{font-style:normal;font-size:36px}.chiph{margin:14px 0 6px;font-weight:700;color:var(--deep)}.topbox{background:#FFFDF5;border:2px solid var(--yel);border-radius:18px;padding:16px 16px 4px;margin:18px 0}.topbox h2{margin:0 0 4px;color:var(--deep);font-size:28px}.topsub{margin:0 0 6px;color:var(--muted)}.top5{counter-reset:t;list-style:none;margin:0;padding:0}.top5 .deal{counter-increment:t;position:relative}.top5 .deal::before{content:counter(t);position:absolute;left:-6px;top:8px;z-index:1;background:var(--red);color:#fff;font-weight:800;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-size:16px}.top5 .deal:last-child{border-bottom:none}.note{font-size:15px;color:var(--muted);background:#F7F3EE;border-radius:10px;padding:10px 12px;margin:10px 0}.shop{background:#FFF8E1;border-radius:12px;padding-left:12px;padding-right:12px}.deal h3{margin:2px 0 6px;font-size:20px;line-height:1.2}.why{margin:0 0 8px;color:var(--muted)}
.badges span{display:inline-block;font-size:13px;font-weight:700;background:#FFF3D1;color:var(--deep);border-radius:6px;padding:2px 8px;margin:0 6px 6px 0}
.lea{display:flex;gap:18px;align-items:center;background:linear-gradient(135deg,#fff8e1,#ffe9a8);border:3px solid #C1121F;border-radius:20px;padding:18px;margin:16px 0;box-shadow:0 6px 18px rgba(193,18,31,.18)}.lea .ph{position:relative;flex:none}.lea img{width:132px;height:132px;border-radius:50%;object-fit:cover;display:block;border:4px solid #C1121F;box-shadow:0 4px 12px rgba(0,0,0,.25)}.lea .ia{position:absolute;left:50%;bottom:-8px;transform:translateX(-50%);background:#C1121F;color:#fff;font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;white-space:nowrap}.lea p{margin:0 0 8px;line-height:1.35;font-size:17px}.lea p b{font-size:20px;display:block;margin-bottom:4px}.lea a{display:inline-block;background:#C1121F;color:#fff;text-decoration:none;font-weight:700;padding:9px 14px;border-radius:10px;font-size:15px}@media (min-width:700px){.lea img{width:160px;height:160px}.lea p{font-size:19px}.lea p b{font-size:24px}}@media (max-width:380px){.lea{flex-direction:column;text-align:center}}
.cd{display:inline-block;margin:0 0 6px;padding:3px 10px;border-radius:999px;background:#FFE3E6;color:#8E0B16;font-weight:700;font-size:14px}.share{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:4px 0 12px;font-weight:700;color:var(--deep)}.share a,.share button{font:inherit;font-size:15px;font-weight:700;text-decoration:none;border-radius:999px;padding:6px 14px;border:2px solid var(--deep);background:#fff;color:var(--deep);cursor:pointer}
.art{list-style:none;margin:0;padding:0}.art .deal{display:block}
.follow{position:relative;margin:12px 0 14px;padding:14px 14px 10px;border-radius:20px;background:linear-gradient(135deg,#FFF3C4,#FFE08A);border:3px dashed #C1121F;text-align:center}.follow .fh{margin:0;font-family:Anton,Impact,sans-serif;font-size:24px;line-height:1.05;color:#8E0B16}.follow .fs{margin:4px 0 10px;font-weight:600;font-size:16px;color:#5a2a00}.fbtn{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.stk{display:flex;align-items:center;gap:10px;min-width:150px;flex:1 1 150px;max-width:260px;padding:12px 12px;border-radius:16px;color:#fff;text-decoration:none;text-align:left;box-shadow:0 4px 0 rgba(0,0,0,.25),0 8px 18px rgba(0,0,0,.18);transition:transform .15s}.stk svg{flex:none;width:30px;height:30px}.stk b{display:block;font-size:18px;line-height:1.05;white-space:nowrap}.stk small{display:block;font-size:13px;opacity:.95;font-weight:600}.stk.fb{background:#1877F2;transform:rotate(-2deg)}.stk.ig{background:linear-gradient(45deg,#F58529,#DD2A7B 45%,#8134AF 75%,#515BD4);transform:rotate(2deg)}.stk:hover,.stk:focus{transform:rotate(0) scale(1.05)}@media (prefers-reduced-motion:no-preference){.stk.fb{animation:wob 3.5s ease-in-out infinite}.stk.ig{animation:wob2 3.5s 1.7s ease-in-out infinite}}@keyframes wob{0%,85%,100%{transform:rotate(-2deg)}90%{transform:rotate(-2deg) scale(1.07)}}@keyframes wob2{0%,85%,100%{transform:rotate(2deg)}90%{transform:rotate(2deg) scale(1.07)}}@media (max-width:420px){.stk{padding:11px 10px;gap:8px}.stk b{font-size:15.5px}.stk svg{width:26px;height:26px}}.shopb{display:block;width:fit-content;margin:12px auto 0;padding:8px 16px;border-radius:999px;background:#232F3E;color:#fff;font-weight:700;font-size:15px;text-decoration:none;border-bottom:3px solid #FF9900}.fms{display:block;margin-top:10px;font-weight:700;font-size:14px;color:#0067d6}
.brands{margin:18px 0;padding:16px;border-radius:20px;background:linear-gradient(135deg,#FFF0F5,#FFF7E0);border:2px solid #F7B6C8}.brands h2{margin:0 0 4px;color:#8E0B16}.btg{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:10px}@media (max-width:420px){.bt span{font-size:13px;padding:4px 9px}.bt b{font-size:16px}}@media (min-width:760px){.btg{grid-template-columns:repeat(4,1fr)}}.bt{position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;padding:14px 8px;border-radius:16px;background:#fff;text-decoration:none;color:var(--ink);box-shadow:0 3px 0 rgba(193,18,31,.18);border:2px solid #fff;transition:transform .15s,border-color .15s}.bt:hover,.bt:focus{transform:translateY(-3px);border-color:var(--red)}.bt i{font-style:normal;font-size:34px;line-height:1}.bt b{font-size:18px;text-align:center}.bt span{white-space:nowrap;margin-top:6px;font-size:14px;font-weight:700;color:#fff;background:var(--red);border-radius:999px;padding:4px 12px}.bt::after{content:'OFFRES';position:absolute;top:-8px;right:4px;background:#FFC72C;color:#8E0B16;font-size:11px;font-weight:800;padding:2px 7px;border-radius:999px;transform:rotate(8deg)}
.px{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:2px 0 6px}.px s{color:#8a8a8a;font-size:16px}.px b{color:var(--red);font-size:24px;font-weight:800}.px span{background:#FFC72C;color:#8E0B16;font-weight:800;border-radius:8px;padding:1px 8px;font-size:15px}.px small{flex-basis:100%;color:var(--muted);font-size:13px}
.go{display:inline-block;text-decoration:none;font-weight:700;background:var(--red);color:#fff;padding:9px 16px;border-radius:10px}@media (max-width:600px){.go{display:block;text-align:center;font-size:18px;padding:14px 16px;margin-top:6px;box-shadow:0 2px 0 rgba(0,0,0,.18)}}
h2{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:28px;color:var(--red);margin:28px 0 8px}
.more{display:flex;flex-wrap:wrap;gap:8px}.more a{text-decoration:none;font-weight:700;padding:8px 14px;border-radius:999px;background:#FFF3D1;color:var(--deep)}
.gang{background:var(--yel);color:#4A0610;border-radius:18px;padding:18px;margin:28px 0}.gang h2{color:#4A0610;margin-top:0}
.gang .cta .btn{background:#fff}
footer{margin:30px 0 40px;font-size:15px;color:var(--muted)}footer a{margin-right:12px}
.empty{padding:20px 0;color:var(--muted)}

body.hw{--paper:#140A1F;--ink:#F4ECFF;--muted:#CDBBE6;--line:#3B2356;--red:#FF7518;--deep:#3B1260;--yel:#FF9A3D;background:#140A1F}
body.hw header{position:relative;overflow:hidden;background:radial-gradient(120% 90% at 50% 0%,#5B1A8C 0%,#2A0F45 55%,#140A1F 100%)}
body.hw h1{color:#FF9A3D;text-shadow:0 0 18px rgba(255,117,24,.55)}
body.hw nav a{color:#FFD9B8;border-color:#FF7518}body.hw nav a[aria-current]{background:#FF7518;color:#1A0A28}
body.hw .tag{background:#FF7518;color:#1A0A28}body.hw .go{background:#FF7518;color:#1A0A28}
body.hw .badges span{background:#3B1260;color:#FFD9B8}body.hw .brand{color:#FF9A3D}body.hw h2{color:#FF9A3D}
body.hw .gang{background:linear-gradient(135deg,#FF7518,#FF9A3D);color:#1A0A28}body.hw .gang h2{color:#1A0A28}
body.hw .more a{background:#3B1260;color:#FFD9B8}body.hw footer{color:#CDBBE6}
.hwcta{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:18px 0 6px;padding:16px 18px;border-radius:18px;text-decoration:none;color:#fff;background:linear-gradient(120deg,#2A0F45 0%,#5B1A8C 55%,#FF7518 130%);border:2px solid #FF7518}.hwcta strong{display:block;font-family:Anton,Impact,sans-serif;font-weight:400;font-size:26px;color:#FF9A3D;line-height:1}.hwcta span{font-weight:700}.hwcta em{font-style:normal;font-size:40px}

.club{background:#FFF7DD;border:2px solid var(--yel);border-radius:18px;padding:18px;margin:18px 0 6px;color:#3A0A10}
.club h2{margin:0 0 4px;color:var(--deep);font-size:28px}.club p{margin:0 0 12px}
.club ul{margin:0 0 12px;padding-left:20px}.club li{margin:2px 0}
.club form{display:flex;flex-wrap:wrap;gap:8px}.club input[type=email]{flex:1 1 220px;min-width:0;font:inherit;padding:11px 14px;border-radius:12px;border:2px solid var(--deep)}
.club button{font:inherit;font-weight:700;padding:11px 18px;border-radius:12px;border:none;background:var(--red);color:#fff;cursor:pointer}
.club .ok{display:flex;gap:8px;align-items:flex-start;font-size:14px;margin-top:8px;width:100%}
.club .soon{font-weight:700;color:var(--deep)}
.social{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
.social a{display:flex;flex-direction:column;align-items:center;text-align:center;gap:2px;text-decoration:none;font-weight:700;font-size:15px;line-height:1.15;padding:10px 6px;border-radius:14px;background:#fff;border:2px solid var(--deep);color:var(--deep)}
.social a b{font-size:24px}.social a.ms{background:var(--deep);color:#fff}
.small{font-size:13px;color:#6A4A4E;margin-top:8px}
body.hw .club{background:#24123A;border-color:#FF7518;color:#F4ECFF}body.hw .club h2{color:#FF9A3D}body.hw .club .soon{color:#FF9A3D}
body.hw .social a{background:#140A1F;color:#FFD9B8;border-color:#FF7518}body.hw .social a.ms{background:#FF7518;color:#1A0A28}body.hw .small{color:#CDBBE6}
.fl i{position:absolute;font-style:normal;font-size:30px;opacity:.5;animation:fly 9s linear infinite;pointer-events:none}
@keyframes fly{0%,100%{transform:translate(0,20px) rotate(-10deg)}50%{transform:translate(16px,-12px) rotate(10deg)}}
.hwcount{display:inline-block;background:#FF7518;color:#1A0A28;border-radius:14px;padding:6px 14px;font-weight:700;margin-top:10px;transform:rotate(-2deg)}
.hwcount b{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:30px}
.hwgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:18px 0}@media(min-width:600px){.hwgrid{grid-template-columns:repeat(4,1fr)}}
.hwgrid a{display:flex;flex-direction:column;gap:4px;padding:14px;border-radius:16px;text-decoration:none;color:#fff;background:rgba(255,255,255,.07);border:2px solid rgba(255,154,61,.55);min-height:96px}
.hwgrid a:hover{background:rgba(255,117,24,.18)}.hwgrid b{font-size:32px;line-height:1}.hwgrid span{font-weight:700}.hwgrid small{font-size:14px;color:#E6D6FA}
@media (prefers-reduced-motion:reduce){.fl i{animation:none}}
@media (max-width:420px){.deal{grid-template-columns:70px 1fr}.tag{width:70px;height:70px;font-size:24px}}
"""

BOLT = '<svg width="16" height="26" viewBox="0 0 100 160" aria-hidden="true"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFC72C"/></svg>'

def store_html(b):
    off = "/deals" in STORES[b]
    return (f'<li class="deal shop"><div class="tag" aria-hidden="true">🏷️<small>boutique</small></div><div><p class="badges"><span>Boutique officielle</span></p>'
            f'<p class="brand">{e(b)}</p><h3>{"Tous les rabais " + e(b) + " en ce moment" if off else "Toute la collection " + e(b) + " sur Amazon.ca"}</h3>'
            f'<a class="go" href="{e(STORES[b])}" target="_blank" rel="sponsored nofollow noopener">{"Voir les rabais " + e(b) if off else "Voir la boutique " + e(b)}</a></div></li>')

def mix(items, brands, every=3):
    out, bi = [], 0
    for i, d in enumerate(items, 1):
        out.append(deal_html(d))
        if i % every == 0 and bi < len(brands):
            out.append(store_html(brands[bi])); bi += 1
    out += [store_html(b) for b in brands[bi:]]
    return "".join(out)

_MO = ["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."]
def _jour(iso):
    try: t = datetime.date.fromisoformat(iso); return f"{t.day} {_MO[t.month-1]}"
    except Exception: return "récemment"
def _money(v): return f"{v:,.2f} $".replace(",", " ").replace(".", ",")
def _old_price(price, pct):
    """Prix d'avant recalculé depuis le prix et le % affichés par Amazon, arrondi au prix rond le plus proche (x,99 ou x,95)."""
    raw = price / (1 - pct / 100)
    for c in (0.99, 0.95, 0.98, 0.00):
        cand = int(raw) + c if c else round(raw)
        for k in (cand, cand - 1, cand + 1):
            if k > price and abs(k - raw) <= max(0.35, raw * 0.006): return round(k, 2)
    return round(raw, 2)

def deal_html(d):
    pct = d.get("amzPct") or d.get("pct")
    if d.get("live") and pct:
        tag = f'<div class="tag">-{pct}%<small>sur Amazon</small></div>'
    else:
        tag = f'<div class="tag" aria-hidden="true">{ICON.get(d["cat"],"⭐")}</div>'
    if d.get("img"):
        lbl = f'<b>-{pct}%</b>' if d.get("live") and pct else ""
        tag = f'<div class="pic"><img src="{e(d["img"])}" alt="" loading="lazy" width="84" height="84">{lbl}</div>'
    badges = []
    if d.get("live") and d.get("flag"): badges.append(d["flag"])
    if d.get("badge") == "gift": badges.append("Idée cadeau")
    if d.get("badge") == "local": badges.append("⚜️ Marque d'ici")
    if d.get("badge") == "canada": badges.append("🍁 Marque canadienne")
    b = f'<p class="badges">{"".join(f"<span>{e(x)}</span>" for x in badges)}</p>' if badges else ""
    why = f'<p class="why">{e(d["why"])}</p>' if d.get("why") else ""
    prix = ""
    if d.get("live") and pct and d.get("price"):
        avant = _money(d["was"]) if d.get("was") else "env. " + f'{round(d["price"] / (1 - pct / 100)):,} $'.replace(",", " ")
        prix = (f'<p class="px"><s>{avant}</s> <b>{_money(d["price"])}</b>'
                f'<span>-{pct} %</span><small>prix observé le {_jour(d.get("added"))}</small></p>')
    why = prix + why
    until = f' data-until="{d["until"]}"' if d.get("until") else ""
    if d.get("price"): until += f' data-price="{d["price"]}"'
    return (f'<li class="deal"{until}>{tag}<div>{b}<p class="brand">{e(d["brand"])}</p><h3>{e(d["name"])}</h3>{why}'
            f'<a class="go" href="{e(link(d))}" target="_blank" rel="sponsored nofollow noopener">Voir le prix sur Amazon.ca</a></div></li>')

IG = "https://www.instagram.com/rabaisflashqc/"
SHOP = "https://www.amazon.ca/shop/coupdecoeurqc"
def clubbar():
    return ('<section class="follow" aria-label="Suis Rabais Flash QC"><p class="fh">🔥 Les offres éclair partent en quelques heures</p>'
            '<p class="fs">Abonne-toi et sois le premier averti. C\'est gratuit, et ça te fait économiser pour vrai.</p><div class="fbtn">'
            f'<a class="stk fb" href="{FB}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path fill="#fff" d="M14 8h3V4h-3c-2.8 0-4.5 1.8-4.5 4.6V11H7v4h2.5v9h4v-9h3l.5-4h-3.5V9c0-.6.4-1 1-1z"/></svg><span><b>J\'aime la page</b><small>sur Facebook</small></span></a>'
            f'<a class="stk ig" href="{IG}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="17.4" cy="6.6" r="1.4" fill="#fff"/></svg><span><b>Suis-nous</b><small>@rabaisflashqc</small></span></a>'
            f'</div>'
            f'<a class="fms" href="{MS}" target="_blank" rel="noopener">💬 ou reçois les alertes sur Messenger</a></section>')

def season_banner(t=None):
    t = t or datetime.date.today(); m, d = t.month, t.day
    if (m == 11 and d >= 20) or (m == 12 and d <= 2):
        a = ("/vendredi-fou/", "C'EST LE VENDREDI FOU", "Les meilleurs deals du moment, au même endroit", "🔥")
    elif m in (10, 11):
        a = ("/idees-cadeaux/", "NOËL APPROCHE", "Nos guides cadeaux par personne et par budget", "🎁")
    elif m == 12 and d <= 23:
        a = ("/idees-cadeaux/", "CADEAUX DE DERNIÈRE MINUTE", "Des idées livrées vite avec Prime", "🎁")
    else:
        return ""
    return f'<a class="seas" href="{a[0]}"><div><strong>{a[1]}</strong><span>{a[2]}</span></div><em aria-hidden="true">{a[3]}</em></a>'

def gift_chips():
    lab = {"pour-elle": "👩 Elle", "pour-lui": "👨 Lui", "ado": "🎮 Ado", "enfants": "🧸 Enfants", "moins-de-25": "💵 Moins de 25 $", "moins-de-50": "💰 Moins de 50 $"}
    return '<p class="chiph">🎁 Je cherche un cadeau pour…</p><p class="more">' + "".join(f'<a href="/idees-cadeaux/{k}/">{v}</a>' for k, v in lab.items()) + '</p>'

# Barème officiel des Associés Amazon.ca (page « Calendrier des commissions standard », vérifié le 2026-10-12) :
# Luxe 10 %, animaux 9 %, bagages et bijoux 7 %, accueil / beauté / chaussures / vêtements / plein air 6 %,
# électroménagers / bébé / bureau 5 %, cuisine et articles ménagers / électronique / montres 4 %,
# jeux et jouets / santé et soins personnels 3 %, ordinateurs et consoles 1 %, autres 2 %.
RATES = {"animaux": 0.09, "beaute": 0.06, "femme": 0.06, "homme": 0.06, "maison": 0.05, "tech": 0.04,
         "jouets": 0.03, "enfants": 0.04, "plein-air": 0.06, "halloween": 0.04}

def rate(d):
    """Taux de commission Amazon.ca estimé selon la catégorie du site (maison = moyenne accueil 6 % et cuisine 4 %)."""
    if d["cat"] == "epicerie" or d.get("brand") in ("Yupik", "Coach"): return 0.0
    if d["cat"] == "beaute" and d.get("tier") == "luxe": return 0.10
    if d.get("rate") is not None: return d["rate"]
    return RATES.get(d["cat"], 0.02)

def gain(d):
    """Commission estimée par vente : prix x taux. Sert à départager, jamais à gonfler un rabais."""
    return (d.get("price") or 0) * rate(d)

def _regular(d):
    return (d.get("price") or 0) / (1 - d["pct"] / 100) if d.get("pct") and d["pct"] < 100 else 0

def savings(d):
    """Économie en dollars calculée à partir du prix affiché et du rabais affiché."""
    return round(_regular(d) - (d.get("price") or 0))

def _num(pat, t):
    m = re.search(pat, t or "")
    return int(re.sub(r"\D", "", m.group(1))) if m else 0

def _bought(x): return _num(r"[Pp]lus de ([\d\s ]+?)\s*achet", x.get("why"))
def _reviews(x): return _num(r"\(([\d\s ]+) avis\)", x.get("why"))

def top5():
    """Top 5 stratégique, recalculé à chaque mise à jour :
    3 produits de VOLUME (petit prix, beaucoup d'acheteurs : faciles à vendre, déposent le cookie)
    + 2 produits à FORTE COMMISSION (commission estimée la plus élevée, rabais réel, bien notés).
    Une carte `top` posée à la main dans data.json garde la priorité."""
    live = [x for x in DEALS if x.get("live") and x.get("pct") and x.get("why") and x.get("price")
            and x["cat"] not in ("halloween", "epicerie") and x["pct"] >= 15]
    def pick(pool, n, key, cats):
        out = []
        for x in sorted(pool, key=key):
            if x["cat"] in cats: continue
            out.append(x); cats.add(x["cat"])
            if len(out) == n: break
        return out
    cats = set()
    volume = pick([x for x in live if x["price"] <= 60 and (_bought(x) >= 100 or _reviews(x) >= 1000)], 3,
                  lambda x: (-_bought(x), -_reviews(x), -x["pct"]), cats)
    ids = {id(x) for x in volume}
    comm = pick([x for x in live if id(x) not in ids and x["pct"] >= 20 and (_reviews(x) >= 100 or _bought(x) >= 50)], 2,
                lambda x: -(x["price"] * rate(x)), cats)
    picks = [volume[0]] if volume else []
    rest_v, rest_c = volume[1:], comm[:]
    while rest_v or rest_c:
        if rest_c: picks.append(rest_c.pop(0))
        if rest_v: picks.append(rest_v.pop(0))
    # sélection à la main : `top` = rang (1 à 5), valable jusqu'à `top_until` (UTC), peu importe le prix
    _now = datetime.datetime.now(datetime.timezone.utc)
    manual = sorted([x for x in live if isinstance(x.get("top"), int) and x.get("top_until")
                     and datetime.datetime.fromisoformat(x["top_until"].replace("Z", "+00:00")) > _now], key=lambda x: x["top"])[:5]
    if manual:
        mids = {id(x) for x in manual}
        picks = manual + [x for x in picks if id(x) not in mids]
        picks = picks[:5]
    if len(picks) < 5:  # secours : les plus gros rabais vérifiés
        have = {id(x) for x in picks}
        picks += sorted([x for x in live if id(x) not in have and rate(x) > 0], key=lambda x: (-x["pct"], -gain(x)))[:5 - len(picks)]
    def card(x, i):
        why = x.get("story") or x.get("why", "")
        if i >= 2 and savings(x) >= 5:
            why = f"{why} Tu économises environ {savings(x)} $."
        return deal_html({**x, "why": why})
    cards = "".join(card(x, i) for i, x in enumerate(picks))
    return picks, ('<section class="topbox" aria-label="Le Top 5 du jour"><h2>⭐ Le Top 5 du jour</h2>'
                   '<p class="topsub">Nos coups de cœur du moment, choisis un par un. Les rabais peuvent changer à tout moment : clique vite!</p>'
                   f'<ol class="top5">{cards}</ol>'
                   '<div class="share">📣 Partage le Top 5 : '
                   '<a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Frabaisflashqc.ca%2F" target="_blank" rel="noopener">Facebook</a>'
                   '<a href="https://wa.me/?text=Les%20meilleurs%20rabais%20Amazon.ca%20du%20jour%20%F0%9F%91%89%20https%3A%2F%2Frabaisflashqc.ca%2F" target="_blank" rel="noopener">WhatsApp</a>'
                   '<button type="button" onclick="navigator.clipboard&&navigator.clipboard.writeText(\'https://rabaisflashqc.ca/\');this.textContent=\'Lien copié ✓\'">Copier le lien</button></div></section>')

LEA = ('<aside class="lea"><div class="ph"><img src="/lea.jpg" alt="Léa de Rabais Flash QC" width="132" height="132"></div>'
       '<div><p><b>Salut, moi c\'est Léa de Rabais Flash QC!</b>Chaque jour, on te montre les rabais Amazon.ca qui valent le coup, triés par thème.</p>'
       '<a href="/a-propos/#choix">Comment on choisit nos deals →</a></div></aside>')

def _attrait(d):
    """Score pour attirer le clic : gros rabais, offre éclair (urgence), volume d'acheteurs, avis, commission."""
    pct = d.get("amzPct") or d.get("pct") or 0
    score = pct if d.get("live") else 0
    score += 20 if d.get("until") else 0
    score += min(_bought(d) / 100, 30) + min(_reviews(d) / 2000, 15)
    score += min((d.get("price") or 0) * rate(d) * 1.5, 30)
    return score

def _vary(items):
    """Évite deux fois la même marque de suite (et trois fois la même catégorie) dans une même journée d'ajout."""
    out, pool = [], list(items)
    while pool:
        last = out[-1] if out else None
        prev2 = out[-2:] if len(out) >= 2 else []
        for i, d in enumerate(pool):
            if d.get("added") != pool[0].get("added"): i = 0; break
            if last and d["brand"] == last["brand"]: continue
            if len(prev2) == 2 and all(p["cat"] == d["cat"] for p in prev2): continue
            break
        else:
            i = 0
        out.append(pool.pop(i))
    return out

def order(items):
    """Les plus récents d'abord (dernières mises à jour), puis le plus attrayant en premier dans chaque journée.
    Les coups de cœur sans rabais vérifié passent après les deals avec rabais."""
    return _vary(sorted(items, key=lambda d: (0 if d.get("live") and (d.get("amzPct") or d.get("pct")) else 1,
                                        "".join(chr(255 - ord(c)) for c in d.get("added", "0000-00-00")),
                                        -_attrait(d), d["r"])))

def page(slug, title, h1, intro, items, extra="", after="", brands=()):
    url = f"{DOMAIN}/{slug + '/' if slug else ''}"
    nav = "".join(f'<a href="/{s + "/" if s else ""}"{" aria-current=\"page\"" if s == slug else ""}>{e(n)}</a>' for s, n in NAV)
    ld = {"@context":"https://schema.org","@type":"WebPage","name":title,"url":url,"inLanguage":"fr-CA",
          "isPartOf":{"@type":"WebSite","name":"Rabais Flash QC","url":DOMAIN+"/"},
          "publisher":{"@type":"Organization","name":"Rabais Flash QC","url":DOMAIN+"/","sameAs":[FB]}}
    bud = BUDGET if sum(1 for d in items if d.get("price")) >= 4 else ""
    lst = mix(items, [b for b in brands if b in STORES]) or '<li class="empty">On est en train de dénicher les prochains deals pour cette section. Reviens bientôt!</li>'
    return f"""<!doctype html>
<html lang="fr-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(intro[:155])}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(intro[:155])}">
<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="fr_CA">
<meta property="og:image" content="{DOMAIN}/couverture.jpg"><meta property="og:image:width" content="1640"><meta property="og:image:height" content="924"><meta property="og:site_name" content="Rabais Flash QC"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#C1121F">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 160'%3E%3Cpath d='M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z' fill='%23C1121F'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Semi+Condensed:wght@500;700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body{" class=\"hw\"" if slug == "halloween" else ""}><header>{HWFLOAT if slug == "halloween" else ""}<div class="wrap" style="position:relative"><a class="logo" href="/">{BOLT} RABAIS <b>FLASH</b> QC</a>
<h1>{e(h1)}</h1><p class="intro">{e(intro)}</p><p class="upd">Mis à jour le {TODAY}</p>{HWCOUNT if slug == "halloween" else ""}</div></header>
<main class="wrap"><nav aria-label="Thèmes">{nav}</nav>
{clubbar()}
{msbtn(slug) if slug else ""}
{extra}
{bud}
<p class="note">⚡ Y'a une raison si on s'appelle <b>Flash</b> : certains rabais durent très peu de temps. Amazon et les marques peuvent les modifier ou y mettre fin à tout moment, et on ne peut pas le garantir. Si le prix a bougé quand tu arrives, c'est que l'offre a changé. Clique vite quand un deal te tente!</p>
<ul class="deals">{lst}</ul>
{after}
{club()}
<footer><p>Les rabais sont fixés par Amazon et par les marques, qui peuvent les modifier ou y mettre fin à tout moment, sans préavis. Leur durée n'est jamais garantie. Vérifie toujours le prix actuel sur Amazon.ca avant d'acheter.</p>
<p>{DISCLOSURE}</p><p><a href="/a-propos/">À propos</a><a href="/confidentialite/">Confidentialité</a><a href="{FB}" rel="noopener">Facebook</a></p></footer>
</main><script>(function(){{function t(){{document.querySelectorAll('[data-until]').forEach(function(li){{var m=Date.parse(li.dataset.until)-Date.now();if(m<=0){{li.remove();return;}}var c=li.querySelector('.cd');if(!c){{c=document.createElement('p');c.className='cd';var h=li.querySelector('h3');h.parentNode.insertBefore(c,h);}}var hh=Math.floor(m/36e5),mm=Math.floor(m%36e5/6e4);c.textContent='⏳ Offre éclair : finit dans '+(hh?hh+' h ':'')+mm+' min';}});}}t();setInterval(t,30000);}})();</script></body></html>"""

def simple(slug, title, h1, body):
    return page(slug, title, h1, "", [], extra=body).replace('<ul class="deals"><li class="empty">On est en train de dénicher les prochains deals pour cette section. Reviens bientôt!</li></ul>', "").replace('<p class="intro"></p>', "")

from articles import ARTICLES
_ALL = {x.get("asin"): x for x in data["deals"] if x.get("asin")}
_LIVE = {x.get("asin"): x for x in DEALS if x.get("asin")}

def article(a):
    cards, n = "", 0
    for h2, sub, picks in a["sections"]:
        cards += f'<h2>{e(h2)}</h2><p class="topsub">Idéal {e(sub)}.</p><ol class="art" start="{n+1}">'
        for asin, txt in picks:
            d = _ALL.get(asin)
            if not d: continue
            n += 1
            live = _LIVE.get(asin)
            pct = f'<span class="cd">-{live["pct"]} % au moment de notre vérification</span>' if live and live.get("live") and live.get("pct") else ""
            cards += (f'<li class="deal"><div><p class="brand">{e(d["brand"])}</p><h3>{e(d["name"])}</h3>{pct}<p>{e(txt)}</p>'
                      f'<a class="go" href="{e(link(d))}" target="_blank" rel="sponsored nofollow noopener">Voir le prix sur Amazon.ca</a></div></li>')
        cards += '</ol>'
    intro = "".join(f"<p>{e(x)}</p>" for x in a["intro"])
    tips = '<h2>Nos conseils avant de commander</h2><ul>' + "".join(f"<li>{e(t)}</li>" for t in a["tips"]) + '</ul>'
    faq = '<h2>Questions fréquentes</h2>' + "".join(f"<h3>{e(q)}</h3><p>{e(r)}</p>" for q, r in a["faq"])
    links = '<h2>À voir aussi</h2><p class="more">' + "".join(f'<a href="{u}">{e(t)}</a>' for u, t in a["links"]) + '</p>'
    ld = [{"@context":"https://schema.org","@type":"Article","headline":a["h1"],"description":a["desc"],"datePublished":a["date"],"dateModified":str(NOW.date()),
           "inLanguage":"fr-CA","mainEntityOfPage":f'{DOMAIN}/{a["slug"]}/',"author":{"@type":"Organization","name":"Rabais Flash QC","url":DOMAIN+"/"},
           "publisher":{"@type":"Organization","name":"Rabais Flash QC","url":DOMAIN+"/"},"image":DOMAIN+"/couverture.jpg"},
          {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":r}} for q, r in a["faq"]]},
          {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Idées cadeaux","item":DOMAIN+"/idees-cadeaux/"},{"@type":"ListItem","position":3,"name":a["h1"],"item":f'{DOMAIN}/{a["slug"]}/'}]}]
    body = (f'<p class="small"><a href="/">Accueil</a> › <a href="/idees-cadeaux/">Idées cadeaux</a> › Guide</p>'
            f'<p class="note">{e(DISCLOSURE)} Les rabais changent souvent : vérifie toujours le prix final sur Amazon.ca.</p>{intro}{cards}{tips}{faq}{links}')
    html = page(a["slug"], a["title"], a["h1"], a["desc"], [], extra=body)
    html = html.replace('<ul class="deals"><li class="empty">On est en train de dénicher les prochains deals pour cette section. Reviens bientôt!</li></ul>', "")
    html = html.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    return html.replace('</head>', "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld) + '</head>', 1)

# Marques chouchous : liens vers « Toutes les remises » d'Amazon.ca (mis à jour par Amazon en continu)
_T = "&tag=" + TAG
BRANDS = [
 ("💄","L'Oréal Paris","beaute","https://www.amazon.ca/-/fr/s?k=l%27or%C3%A9al&rh=p_n_deal_type%3A23565508011%2Cp_85%3A5690392011%2Cp_123%3A665212"+_T),
 ("💋","Maybelline","beaute","https://www.amazon.ca/s?k=Maybelline&rh=p_n_deal_type%3A23565508011"+_T),
 ("🌿","Garnier","beaute","https://www.amazon.ca/s?k=Garnier&rh=p_85%3A5690392011%2Cp_n_deal_type%3A23565508011"+_T),
 ("✨","e.l.f.","beaute",STORES.get("e.l.f.","https://www.amazon.ca/-/fr/s?k=elf&rh=p_85%3A5690392011%2Cp_n_deal_type%3A23565508011"+_T)),
 ("🌹","Lancôme","beaute",STORES["Lancôme"]),
 ("🤍","Clarins","beaute",STORES["Clarins"]),
 ("🧴","La Roche-Posay","beaute",STORES["La Roche-Posay"]),
 ("🌟","Laura Geller","beaute","https://www.amazon.ca/stores/page/027C192F-9D65-42BE-B3DB-16E3EB33EB17?tag="+TAG),
 ("💧","Neutrogena","beaute","https://www.amazon.ca/-/fr/s?k=Neutrogena&rh=p_n_deal_type%3A23565508011%2Cp_72%3A11192170011"+_T),
 ("🌸","Olay","beaute","https://www.amazon.ca/-/fr/s?k=Olay&rh=p_85%3A5690392011%2Cp_72%3A11192170011%2Cp_123%3A195696%2Cp_n_deal_type%3A23565508011"+_T),
 ("🍳","Ninja","maison","https://www.amazon.ca/-/fr/s?k=ninja&rh=p_n_deal_type%3A23565508011%2Cp_123%3A391646%2Cp_85%3A5690392011"+_T),
 ("🦈","Shark","maison",STORES.get("Shark","https://www.amazon.ca/-/fr/s?k=shark&rh=p_n_deal_type%3A23565508011%2Cp_85%3A5690392011"+_T)),
 ("🌀","Dyson","maison","https://www.amazon.ca/-/fr/s?k=Dyson&rh=p_n_deal_type%3A23565508011%2Cp_85%3A5690392011"+_T),
 ("☕","Nespresso","maison",STORES.get("Nespresso","https://www.amazon.ca/s?k=Nespresso&rh=p_n_deal_type%3A23565508011"+_T)),
 ("🧥","Columbia","mode","https://www.amazon.ca/s?k=Columbia&rh=p_n_deal_type%3A23565508011%2Cp_85%3A5690392011%2Cp_123%3A232621"+_T),
 ("🏔️","The North Face","mode","https://www.amazon.ca/s?k=The+North+Face&rh=p_85%3A5690392011%2Cp_n_deal_type%3A23565508011%2Cp_123%3A196635"+_T),
 ("👟","Skechers","mode","https://www.amazon.ca/-/fr/s?k=Skechers&rh=p_n_deal_type%3A23565508011"+_T),
]
def brand_block(only=None, title="💖 Les marques chouchous des Québécoises"):
    items = [b for b in BRANDS if only is None or b[2] in only]
    tiles = "".join(f'<a class="bt" href="{e(u)}" target="_blank" rel="sponsored nofollow noopener"><i>{ic}</i><b>{e(n)}</b><span>Voir les rabais →</span></a>' for ic, n, _, u in items)
    return (f'<section class="brands"><h2>{title}</h2><p class="topsub">Un clic et tu vois <b>toutes leurs offres du moment</b> sur Amazon.ca, mises à jour par Amazon en continu.</p>'
            f'<div class="btg">{tiles}</div></section>')

def rfd_block():
    try: L = json.loads((ROOT / "rfd.json").read_text())
    except Exception: return ""
    now = datetime.datetime.now(datetime.timezone.utc)
    L = [x for x in L if datetime.datetime.fromisoformat(x["until"]) > now and x.get("title")]
    if not L: return ""
    MO = ["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."]
    def card(x):
        tag = f'<div class="tag">-{x["pct"]}%<small>signalé</small></div>' if x.get("pct") else '<div class="tag" aria-hidden="true">🔥</div>'
        s = datetime.datetime.fromisoformat(x["seen"])
        when = f'{s.day} {MO[s.month-1]} à {s.hour} h {s.minute:02d}'
        pr = (f'{x["price"]:,.2f} $'.replace(",", " ").replace(".", ",")) if x.get("price") else ""
        obs = f'<p class="why"><b>{"Prix signalé : " + pr + " · " if pr else ""}</b>observé sur RedFlagDeals le {when}. Les prix bougent vite : vérifie le prix final sur Amazon.ca.</p>'
        return (f'<li class="deal" data-until="{x["until"]}">{tag}<div><p class="badges"><span>🔥 {x.get("votes") or ""} votes de la communauté</span></p>'
                f'<h3>{e(x["title"])}</h3>{obs}'
                f'<a class="go" href="https://www.amazon.ca/dp/{e(x["asin"])}?tag={TAG}" target="_blank" rel="sponsored nofollow noopener">Voir le prix sur Amazon.ca</a></div></li>')
    li = "".join(card(x) for x in L[:8])
    return ('<section class="topbox" aria-label="Repérés par la communauté"><h2>⚡ Les deals à saisir maintenant</h2>'
            '<p class="topsub">Les aubaines Amazon.ca les plus votées par les chasseurs de deals canadiens. Elles partent vite!</p>'
            f'<ul class="deals">{li}</ul></section>')

def write(slug, content):
    p = OUT / slug / "index.html" if slug else OUT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)

def main():
    OUT.mkdir(exist_ok=True)
    urls = []
    for slug, title, h1, intro, f, more in PAGES:
        items = order([d for d in DEALS if f(d)])
        extra = after = ""
        topblock = ""
        if slug == "":
            tpicks, topblock = top5()
            tids = {id(x) for x in tpicks}
            items = [x for x in items if id(x) not in tids]
        if more:
            after = '<h2>Plus de choix sur Amazon.ca</h2><p class="more">' + "".join(f'<a href="{e(search(q))}" target="_blank" rel="sponsored nofollow noopener">{e(n)}</a>' for n, q in more) + "</p>"
        brands = [b for b in STORE_CAT.get(slug, []) if b in STORES]
        if brands:
            extra = '<h2>Les boutiques de tes marques préférées</h2><p class="more">' + "".join(f'<a href="{e(STORES[b])}" target="_blank" rel="sponsored nofollow noopener">{e(b)}</a>' for b in brands) + "</p><h2>Les deals du moment</h2>"
        if slug in ("beaute", "maison", "mode"):
            extra = brand_block({slug}, "💖 Les rabais de tes marques préférées") + extra
        if slug == "epicerie":
            _u = "https://www.amazon.ca/-/fr/deals?discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257B%255C%2522departments%255C%2522%253A%255B%255C%25226967216011%255C%2522%255D%257D%252C%255C%2522rangeRefinementFilters%255C%2522%253A%257B%255C%2522percentOff%255C%2522%253A%257B%255C%2522min%255C%2522%253A20%252C%255C%2522max%255C%2522%253A40%257D%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522&tag=" + TAG
            extra = '<h2>🛒 Les rabais épicerie du moment</h2><p class="more"><a href="' + e(_u) + '" target="_blank" rel="sponsored nofollow noopener">Voir tous les deals épicerie de 20 % à 40 %</a></p>' + extra
        if slug == "idees-cadeaux":
            extra = ('<h2>🎁 Trouve le cadeau parfait</h2><div class="idg">' + "".join(f'<a href="/idees-cadeaux/{x[0]}/"><b>{x[4][0][0]}</b><span>{e(x[2])}</span><small>{len(x[4])} idées + les rabais du moment</small></a>' for x in GUIDES)
                     + '</div><h2>📖 Nos guides d\'achat</h2><p class="more">' + "".join(f'<a href="/{a["slug"]}/">{e(a["h1"])}</a>' for a in ARTICLES) + '</p><h2>Par budget, directement sur Amazon.ca</h2><div class="idg">'
                     + "".join(f'<a href="{e(sp("cadeau", hi, lo))}" target="_blank" rel="sponsored nofollow noopener"><b>{i}</b><span>{t}</span><small>Livraison Prime</small></a>' for i,t,lo,hi in [("💵","Moins de 25 $",None,25),("💰","25 $ à 50 $",25,50),("💎","50 $ à 100 $",50,100),("👑","100 $ et plus",100,None)])
                     + '</div>' + extra)
        if slug == "halloween":
            extra = '<h2>🎃 Choisis ton univers</h2><div class="hwgrid">' + "".join(f'<a href="{e(u)}" target="_blank" rel="sponsored nofollow noopener"><b>{i}</b><span>{e(t)}</span><small>{e(sub)}</small></a>' for i,t,sub,u in HWTILES) + '</div><p>⏰ Conseil : commande tôt, les tailles populaires partent vite!</p><h2>👻 Nos trouvailles épeurantes</h2>'
            after = ""
        if slug == "":
            pills = "".join(f'<a href="{e(STORES[b])}" target="_blank" rel="sponsored nofollow noopener">{e(b)}</a>' for b in HOME_STORES if b in STORES)
            hw = sorted([x for x in DEALS if x["cat"] == "halloween" and id(x) not in tids and x.get("live") and x.get("pct") and x.get("why")], key=lambda x: -x["pct"])[:4]
            hwblock = ""
            if False:
                hwblock = ('<h2>🎃 Halloween : les meilleurs rabais du moment</h2><ul class="deals">' + "".join(deal_html(x) for x in hw) + '</ul>'
                           '<p class="more"><a href="/halloween/">Voir tous les rabais Halloween →</a></p>')
            extra = (LEA + season_banner() + topblock + rfd_block() + brand_block() + hwblock + gift_chips() + '<h2>Plus de deals</h2>')
            items = [x for x in items if x["cat"] != "halloween"][:12]
            after = ('<h2>Les offres de tes marques préférées</h2><p class="more">' + pills + '</p>'
                     '<h2>📖 Nos guides d\'achat</h2><p class="more">' + "".join(f'<a href="/{a["slug"]}/">{e(a["h1"])}</a>' for a in ARTICLES) + '</p>'
                     '<h2>Voir tous les deals par thème</h2><p class="more">' + "".join(f'<a href="/{sl}/">{e(n)}</a>' for sl, n in NAV if sl and sl not in ("vendredi-fou",)) + '</p>')
        write(slug, page(slug, title, h1, intro, items, extra, after, [] if slug == "" else STORE_CAT.get(slug, []))); urls.append(slug)
    for g, title, h1, intro, tiles, f, brands in GUIDES:
        slug = f"idees-cadeaux/{g}"
        _arts = [a for a in ARTICLES if any(u == f"/idees-cadeaux/{g}/" for u, _ in a["links"])]
        extra = ("".join(f'<p class="seas" style="display:block"><a href="/{a["slug"]}/" style="color:#fff;font-weight:700">📖 Notre guide : {e(a["h1"])} →</a></p>' for a in _arts) + '<h2>Nos idées</h2><div class="idg">' + "".join(f'<a href="{e(sp(q, hi))}" target="_blank" rel="sponsored nofollow noopener"><b>{i}</b><span>{e(t)}</span><small>{e(w)}</small></a>' for i,t,w,q,hi in tiles)
                 + '</div><p class="small">Les liens ouvrent une recherche Amazon.ca avec livraison Prime' + (", filtrée par prix" if any(t[4] for t in tiles) else "") + '.</p>'
                 + '<h2>Les autres guides</h2><p class="more">' + "".join(f'<a href="/idees-cadeaux/{x[0]}/">{e(x[2])}</a>' for x in GUIDES if x[0] != g) + '</p><h2>Les rabais du moment pour ce guide</h2>')
        items = order([d for d in DEALS if f(d)])
        write(slug, page(slug, title, h1, intro, items, extra, "", brands)); urls.append(slug)
    write("a-propos", simple("a-propos", "À propos de Rabais Flash QC", "À propos",
        "<h2>Qui on est</h2><p>Rabais Flash QC, c'est un entrepreneur du Québec, pour le Québec. Tout coûte plus cher, alors on fait le tri des aubaines d'Amazon.ca pour te faire gagner du temps et de l'argent.</p>"
        "<h2>Pourquoi « Flash »?</h2><p>Parce que les meilleurs rabais ne durent pas. Certains disparaissent en quelques heures, et Amazon ou la marque peut changer le prix ou arrêter l'offre à tout moment, sans nous prévenir. On ne peut donc pas garantir qu'un rabais sera encore là quand tu cliques. C'est pour ça qu'on met le site à jour plusieurs fois par jour, et qu'on te conseille de ne pas trop attendre.</p>"
        "<h2 id=\"choix\">Comment on choisit</h2><p>On garde surtout des rabais affichés par Amazon sur des marques connues, avec de bons avis. On classe tout par thème et on retire les offres expirées. Les prix changent souvent : vérifie toujours le prix final sur Amazon.ca.</p>"
        f"<h2>Transparence</h2><p>{DISCLOSURE} Ça ne change rien au prix que tu paies.</p>"
        f'<h2>Nous joindre</h2><p>Écris-nous sur <a href="{MS}">Messenger</a> ou sur notre <a href="{FB}">page Facebook</a>.</p>')); urls.append("a-propos")
    write("confidentialite", simple("confidentialite", "Politique de confidentialité | Rabais Flash QC", "Politique de confidentialité",
        "<p>Ce site ne te demande aucune information personnelle pour consulter les deals. Il n'utilise pas de témoins publicitaires qui lui sont propres.</p>"
        "<p>Quand tu cliques sur un lien vers Amazon.ca, Amazon peut utiliser des témoins pour attribuer l'achat, selon sa propre politique de confidentialité.</p>"
        "<p>Si tu t'inscris à notre infolettre, ton adresse courriel sert seulement à t'envoyer nos aubaines. Tu peux te désabonner en tout temps avec le lien présent dans chaque courriel. Pour toute question sur tes renseignements personnels, écris-nous sur Messenger.</p>"
        f"<p>Dernière mise à jour : {TODAY}.</p>")); urls.append("confidentialite")
    for a in ARTICLES:
        write(a["slug"], article(a)); urls.append(a["slug"])
    (OUT / "CNAME").write_text("rabaisflashqc.ca\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<url><loc>{DOMAIN}/{u + '/' if u else ''}</loc><lastmod>{NOW.date()}</lastmod></url>" for u in urls) + "</urlset>\n")
    print("pages:", len(urls))

if __name__ == "__main__":
    main()
