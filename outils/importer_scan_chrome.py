#!/usr/bin/env python3
"""Importe un scan Chrome (Keepa Affaires + page Vendredi fou d'amazon.ca) dans suivi/deals_chrome.json.

Usage : python3 outils/importer_scan_chrome.py KEEPA.json AMAZON.json [--max-keepa N] [--max-amazon N]

KEEPA.json  : {"scanned": ISO, "items": [{a, t, p, w, n, f, i}]}   (a = ASIN, p = % de baisse, w = moyenne, n = prix actuel, f = âge, i = id d'image)
AMAZON.json : {"scanned": ISO, "grid": [...], "shelves": [...]}     (prix, ancien prix, titre, image lus sur la page Vendredi fou)

Règles du site (AUTONOMIE.md) : photo Amazon en lien direct (img_url), prix = lecture réelle (seen), visible 72 h (until),
vf = true dès 30 % et photo, ref = "conseille" quand l'ancien prix est un « Prix conseillé », pas d'épicerie ni de livres.
"""
import json, re, sys, datetime, pathlib, argparse, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
TZ = datetime.timezone(datetime.timedelta(hours=-5))  # Québec, heure normale (nov.)

ap = argparse.ArgumentParser()
ap.add_argument("keepa"); ap.add_argument("amazon")
ap.add_argument("--max-keepa", type=int, default=650)
ap.add_argument("--max-amazon", type=int, default=900)
args = ap.parse_args()

def iso(ts):
    d = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)
    return d.strftime("%Y-%m-%dT%H:%M%z")[:-2] + ":" + d.strftime("%z")[-2:]

def num(s):
    s = (s or "").replace(" ", " ").replace("\xa0", " ")
    m = re.search(r"(\d[\d ]*(?:[.,]\d{1,2})?)", s)
    if not m: return 0.0
    v = m.group(1).replace(" ", "")
    if "," in v and "." in v: v = v.replace(",", "")
    else: v = v.replace(",", ".")
    try: return float(v)
    except ValueError: return 0.0

def img_url(src):
    m = re.search(r"/images/I/([A-Za-z0-9+_-]{8,})\.", src or "")
    return f"https://m.media-amazon.com/images/I/{m.group(1)}._AC_SL500_.jpg" if m else None

# --- exclusions : pas pour notre audience, pas de produits dangereux ou sensibles, pas d'épicerie ni de livres ---
EXCL = re.compile(r"brake|rotor|caliper|oil filter|spark plug|wiper|motor oil|windshield|tire |tires|lug nut|battery tender|car seat cover|"
                  r"plaquette|filtre à huile|essuie-glace|pneu|bougie d'allumage|"
                  r"toner|ink cartridge|cartouche d'encre|"
                  r"\(xsx\)|\(ps[45]\)|nintendo switch|xbox|playstation|gaming|gamer|gpu|graphics card|ssd|nvme|motherboard|server|raspberry|"
                  r"condom|lubricant|vibrator|sex|adult toy|lingerie sexy|"
                  r"cbd|vape|e-cig|cigarette|"
                  r"gun|firearm|ammo|airsoft|taser|pepper spray|switchblade|"
                  r"prime video|gift card|carte-cadeau|subscription|abonnement|"
                  r"pool |piscine|paddle ?board|weed ?burner|snow ?blower|"
                  r"coffee beans|grains de café|protein powder|poudre de protéine|snack|chocolate|candy|vitamin|vitamine|supplement|supplément", re.I)

APP = re.compile(r"\b(jeans?|bras?|leggings?|dress(es)?|shirts?|t-shirts?|tees?|pants?|jackets?|coats?|boots?|booties|shoes?|sneakers?|sandals?|loafers?|mary jane|cardigan|underwire|sweaters?|hoodies?|socks?|slippers?|joggers?|shorts|boxers?|briefs|vests?|parkas?|gloves?|mittens?|beanies?|hats?|scarf|scarves|skirts?|blouses?|pajamas?|slip-?ons?|clogs?|flats?|heels?|pumps?|wedges?|bikini|tank|polo|pullover|sweatshirts?|trunks|chaussures?|bottes?|espadrilles?|pantoufles?|manteau|veste|chandail|pantalon|robe|jupe|sandales?)\b", re.I)
def cat_de(t, pill=""):
    s = t.lower()
    app = bool(APP.search(s))
    if not app and re.search(r"\b(dog|dogs|puppy|cat|cats|kitten|pet|pets|aquarium|litter|leash|chien|chat|chiots?|laisse|litière|animaux)\b", s): return "animaux"
    if pill in ("Beauté", "Santé"): return "beaute"
    if pill == "Jeux et jouets": return "jouets"
    if pill == "Sport et plein air": return "plein-air"
    if pill in ("Outils", "Pelouse"): return "plein-air"
    if pill == "Appareils Amazon": return "tech"
    if pill in ("Maison et cuisine", "Meubles"):
        return "tech" if re.search(r"\b(tv|télé|echo|alexa|speaker|haut-parleur|camera|caméra|thermostat|smart plug|prise intelligente|wifi|wi-fi)\b", s) else "maison"
    # Mode (ou Keepa sans catégorie) : jouets stricts, puis vêtements, puis beauté, tech
    if re.search(r"\b(lego|puzzle|barbie|hot wheels|playset|board game|nerf|play-doh|action figure|dollhouse|doll|jouet|jeu de société|peluche|building set|magna-tiles|fisher-price|playmobil)\b", s) and not app: return "jouets"
    if app:
        if re.search(r"\b(baby|toddler|infant|newborn|bébé|bebe|nourrisson|boys?'?s?|girls?'?s?|kids?|children|youth|garçons?|filles?|enfants?)\b", s): return "enfants"
        if re.search(r"\bwomen'?s?\b|\bwomens\b|\bladies\b|\bfemmes?\b|\bdress|\bbras?\b|underwire|legging|skirt|jupe|blouse|bikini|mary jane|heels?|pumps?|wedges?|\bflats\b|cardigan", s): return "femme"
        return "homme"
    if re.search(r"\bsoap and lotion\b|dispenser|air conditioner|blower|hvac|\bcover\b", s): return "maison"
    if re.search(r"shampoo|conditioner|\bskin(care)?\b|serum|moistur|makeup|mascara|lipstick|perfume|fragrance|eau de|razor|toothbrush|oral-b|\bhair|\bcream|\blotion|nail polish|deodorant|sunscreen|cerave|neutrogena|maybelline|l'or[eé]al|revlon|essie|brosse à dents|rasoir|épilat|crème|maquillage|parfum|shampo|\bsoins?\b|cosmetic|\bpalette\b|foundation spf|makeup brush|blow ?dry|flat iron|curling iron|hair straightener|sèche-cheveux", s): return "beaute"
    if re.search(r"\b(headphones?|earbuds?|earphones?|speaker|charger|charging|usb|camera|echo|fire tv|fire stick|kindle|laptop|tablet|iphone|smartphone|smart ?watch|bluetooth|router|monitor|wifi|wi-fi|garmin|casque|écouteurs|haut-parleur|chargeur|caméra|ordinateur|power bank|batterie externe|airpods|tv|television|projector|soundbar|webcam|keyboard|clavier|drone|gopro|ring doorbell|blink|eufy|tapo|kasa|govee)\b", s): return "tech"
    if re.search(r"women'?s?|womens|ladies|femmes?|pour elle|maternity|maternité|handbag|sac à main|purse", s): return "femme"
    if re.search(r"\bmen'?s?\b|\bmens\b|\bhommes?\b|pour lui", s): return "homme"
    if re.search(r"\b(tent|camping|hiking|fishing|bike|cycling|outdoor|grill|bbq|drill|dewalt|milwaukee|makita|yoga|dumbbell|golf|ski|soccer|basketball|backpack|cooler|kayak|fitness|treadmill|tente|randonnée|pêche|vélo|barbecue|perceuse|haltère)\b", s): return "plein-air"
    return "maison"

def comm_de(t, cat):
    s = t.lower()
    if re.search(r"luggage|suitcase|valise|bagage|carry-?on", s): return 7
    if re.search(r"jewel|bijou|necklace|bracelet|earring|collier|boucles d'oreilles|\bring\b.*(gold|silver|diamond)", s): return 7
    if re.search(r"air fryer|friteuse|coffee maker|cafetière|blender|mélangeur|toaster|grille-pain|vacuum|aspirateur|instant pot|slow cooker|mijoteuse|espresso|kettle|bouilloire|microwave|micro-ondes|dishwasher|refrigerator|dryer|washer", s): return 5
    if re.search(r"water bottle|tumbler|mug|cookware|pan\b|pot\b|knife|couteau|bouteille|gobelet|poêle|casserole|ustensile|kitchen|cuisine", s): return 4
    if re.search(r"\bwatch\b|montre", s): return 4
    if cat in ("femme", "homme") and re.search(r"shoe|sneaker|boot|sandal|slipper|clog|chaussure|espadrille|botte|pantoufle|crocs", s): return 6
    return None

def clean_en(t):
    t = html.unescape(t).replace("\xa0", " ")
    t = re.sub(r"\s+", " ", t).strip()
    # coupe aux virgules : on garde le nom du produit, pas les couleurs ni les tailles
    parts = [p.strip() for p in t.split(",")]
    keep = [parts[0]]
    for p in parts[1:]:
        if len(" ".join(keep)) + len(p) > 78: break
        if re.fullmatch(r"(size |taille )?(x{0,3}[sl]|medium|large|small|\d{1,2}(\.\d)?|\d+(\.\d+)?\s?(oz|ml|g|lb|pack|count|ct|inch|in|cm|mm))( .*)?", p, re.I): break
        if re.fullmatch(r"[A-Za-z/ &-]{2,24}", p) and len(keep) >= 1 and re.search(r"black|white|blue|red|grey|gray|green|pink|navy|brown|beige|tan|olive|burgundy|purple|yellow|orange|silver|gold|charcoal|heather|multi|natural|cream|noir|blanc|bleu|rouge|gris|vert|rose", p, re.I): break
        keep.append(p)
    t = ", ".join(keep)
    t = re.sub(r"\s*[-–]\s*(Size|Color|Colour)\b.*$", "", t, flags=re.I)
    t = re.sub(r"\s+(for|pour) (Men|Women|Boys|Girls|Kids)\b.*$", r" \1 \2", t, flags=re.I) if False else t
    return t[:90].rstrip(" ,-–:")

AUD = [(r"\bwomen'?s\b|\bwomens\b|\bladies'?\b", "pour femme"), (r"\bmen'?s\b|\bmens\b", "pour homme"),
       (r"\bboys?'?s?\b", "pour garçon"), (r"\bgirls?'?s?\b", "pour fille"), (r"\b(kids?|children|youth|toddler)'?s?\b", "pour enfants"),
       (r"\bbaby\b|\binfant\b", "pour bébé")]
def fr_titre(t):
    """Titre Keepa (anglais) : on retire « Men's / Women's… » et on ajoute le public en français à la fin."""
    t = clean_en(t); suf = ""
    for pat, fr in AUD:
        if re.search(pat, t, re.I):
            t = re.sub(pat + r"\s*", "", t, count=1, flags=re.I).strip(" ,-"); suf = " " + fr; break
    t = re.sub(r"\s+'(?=\s|$)", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    return (t + suf)[:100]

def clean_fr(t):
    t = html.unescape(t).replace("\xa0", " ")
    t = t.split(" | ")[0]
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > 88:
        cut = max(t.rfind(", ", 40, 88), t.rfind(" - ", 40, 88), t.rfind(" : ", 40, 88), t.rfind(" avec ", 40, 88))
        t = t[:cut] if cut > 0 else t[:88].rsplit(" ", 1)[0]
    return t.rstrip(" ,-–:|")

def keywords_key(t):
    return " ".join(re.split(r"[\s,]+", t.lower())[:4])

kj = json.load(open(args.keepa)); aj = json.load(open(args.amazon))
seen_k = iso(kj["scanned"]); seen_a = iso(aj["scanned"])
until = lambda s: (datetime.datetime.fromisoformat(s) + datetime.timedelta(hours=72)).strftime("%Y-%m-%dT%H:%M%z")[:-2] + ":" + datetime.datetime.fromisoformat(s).strftime("%z")[-2:]

# ---------- Amazon : page Vendredi fou ----------
amz, vus = [], set()
for x in aj.get("grid", []) + aj.get("shelves", []):
    asin = x.get("asin") or ""
    if asin in vus or not re.fullmatch(r"B[A-Z0-9]{9}", asin): continue
    price = num(x.get("price")); old = num(x.get("old") or x.get("kind"))
    if not price or not old or old <= price: continue
    pct = round((1 - price / old) * 100)
    if pct < 16 or pct > 70 or price < 8: continue
    rate = num((x.get("rate") or "").split("sur")[0]) if x.get("rate") else 0
    if x.get("rate") and rate and rate < 4.0: continue
    img = img_url(x.get("img")); title_raw = x.get("t") or ""
    if not img or not title_raw or EXCL.search(title_raw): continue
    vus.add(asin)
    kind = (x.get("old") or x.get("kind") or "")
    PILL = {"jouets": "Jeux et jouets", "plein-air": "Sport et plein air", "beaute": "Beauté", "maison": "Maison et cuisine"}
    t = clean_fr(title_raw); cat = "enfants" if x.get("c") == "enfants" else cat_de(title_raw, x.get("pill") or PILL.get(x.get("c"), ""))
    e = {"asin": asin, "title": t, "cat": cat, "price": round(price, 2), "was": round(old, 2), "pct": pct, "seen": seen_a, "until": until(seen_a),
         "source": "amazon", "img_url": img}
    if "conseill" in kind.lower(): e["ref"] = "conseille"
    c = comm_de(title_raw, cat)
    if c: e["comm"] = c
    if re.search(r"éclair|durée limitée|se termine", (x.get("msg") or "") + " " + (x.get("badge") or ""), re.I): e["limite"] = True
    if pct >= 30: e["vf"] = True
    amz.append(e)
# tri : vrais anciens prix d'abord (pas de « conseillé »), puis gros %, avec un plafond par catégorie pour la variété
amz.sort(key=lambda e: (1 if e.get("ref") else 0, -e["pct"]))
def cap(L, n, per_cat):
    out, c = [], {}
    for e in L:
        if len(out) >= n: break
        if c.get(e["cat"], 0) >= per_cat: continue
        c[e["cat"]] = c.get(e["cat"], 0) + 1; out.append(e)
    return out
amz_pick = cap(amz, args.max_amazon, int(args.max_amazon * 0.32))

# ---------- Keepa Affaires ----------
kp, seen_t, asins_amz = [], set(), {e["asin"] for e in amz_pick}
for x in kj["items"]:
    asin = x.get("a") or ""
    if not re.fullmatch(r"B[A-Z0-9]{9}", asin) or asin in asins_amz: continue   # pas de livres (ISBN), pas de doublon avec Amazon
    n, w = float(x["n"]), float(x["w"])
    if not (w > n > 0): continue
    pct = round((1 - n / w) * 100)
    if pct < 16 or pct > 70 or not (10 <= n <= 600): continue
    if not re.search(r"minute|heure|1 jour|2 jours", x.get("f", "")): continue
    t_raw = html.unescape(x["t"])
    if EXCL.search(t_raw): continue
    k = keywords_key(t_raw)
    if k in seen_t: continue
    seen_t.add(k)
    if not x.get("i"): continue
    cat = cat_de(t_raw)
    e = {"asin": asin, "title": fr_titre(t_raw), "cat": cat, "price": round(n, 2), "was": round(w, 2), "pct": pct, "seen": seen_k, "until": until(seen_k),
         "source": "keepa", "img_url": f"https://m.media-amazon.com/images/I/{x['i']}._AC_SL500_.jpg"}
    c = comm_de(t_raw, cat)
    if c: e["comm"] = c
    if pct >= 30: e["vf"] = True
    kp.append(e)
kp.sort(key=lambda e: -e["pct"])
# viser ~40 % mode (homme/femme/enfants), 15 % beauté, le reste maison/tech/jouets/plein-air/animaux (règle d'Alex)
mode = [e for e in kp if e["cat"] in ("homme", "femme", "enfants")]; autres = [e for e in kp if e["cat"] not in ("homme", "femme", "enfants")]
kp_pick = sorted(mode[:int(args.max_keepa * 0.4)] + autres[:args.max_keepa - min(len(mode), int(args.max_keepa * 0.4))], key=lambda e: -e["pct"])[:args.max_keepa]

# ---------- fusion avec l'existant (les nouveaux écrasent, les anciens non expirés restent) ----------
path = ROOT / "suivi" / "deals_chrome.json"
old = json.loads(path.read_text()) if path.exists() else []
now = datetime.datetime.now(datetime.timezone.utc)
neuf = {e["asin"]: e for e in amz_pick + kp_pick}
garde = []
for e in old:
    try:
        if e["asin"] in neuf or datetime.datetime.fromisoformat(e["until"]) < now: continue
    except Exception: continue
    garde.append(e)
out = list(neuf.values()) + garde
path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
import collections
print("Amazon retenus :", len(amz_pick), "| Keepa retenus :", len(kp_pick), "| anciens gardés :", len(garde), "| total :", len(out))
print("catégories :", dict(collections.Counter(e["cat"] for e in out)))
print("vf :", sum(1 for e in out if e.get("vf")), "| avec photo :", sum(1 for e in out if e.get("img_url")))
