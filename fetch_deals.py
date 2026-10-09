#!/usr/bin/env python3
"""Va chercher les deals sur l'API Creators d'Amazon et les ajoute à data.json.

Lit les identifiants dans les variables d'environnement AMZ_CLIENT_ID et
AMZ_CLIENT_SECRET (Secrets GitHub). Ne touche pas aux deals ajoutés à la main :
seuls les deals marqués "source": "api" sont remplacés à chaque passage.
"""
import json, os, sys, datetime, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).parent
TAG = "coupdecoeurqc-20"
MARKET = "www.amazon.ca"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
API = "https://creatorsapi.amazon/catalog/v1"
MIN_SAVING = 20      # rabais minimum par défaut (%)
PER_SEARCH = 10      # produits par recherche
MAX_TOTAL = 80       # plafond de deals automatiques sur le site
QUOTA = {"luxe": 35, "volume": 45}   # équilibre : grosses commissions + gros volume

# STRATÉGIE
# luxe   : forte commission (beauté de luxe, mode, bijoux, montres, bagages) et panier élevé.
#          Le luxe est rarement soldé à 40 %, donc seuil plus bas (15 %).
# volume : petits prix, achat impulsif, forte conversion. Seuil plus haut (25 %+)
#          pour que le rabais saute aux yeux.
# Format : (niveau, catégorie du site, mots-clés, rabais minimum, badge)
BASE = [
    # LUXE · beauté (la catégorie la plus payante)
    ("luxe", "beaute", "Clarins", 15, ""), ("luxe", "beaute", "Lancôme", 15, ""),
    ("luxe", "beaute", "Kiehl's", 15, ""), ("luxe", "beaute", "Clinique", 15, ""),
    ("luxe", "beaute", "Estée Lauder", 15, ""), ("luxe", "beaute", "Kérastase", 15, ""),
    ("luxe", "beaute", "Elemis", 15, ""), ("luxe", "beaute", "Laneige", 15, ""),
    ("luxe", "beaute", "Shiseido", 15, ""), ("luxe", "beaute", "parfum femme", 20, ""),
    ("luxe", "beaute", "parfum homme", 20, ""), ("luxe", "beaute", "T3 fer à friser", 15, ""),
    # LUXE · mode, montres, bijoux, bagages (commission élevée, gros panier)
    ("luxe", "femme", "Michael Kors sac", 20, ""), ("luxe", "femme", "Coach sac à main", 20, ""),
    ("luxe", "femme", "Kate Spade", 20, ""), ("luxe", "femme", "UGG femme", 20, ""),
    ("luxe", "femme", "Sorel bottes femme", 20, "canada"), ("luxe", "femme", "bijoux argent sterling femme", 25, ""),
    ("luxe", "homme", "montre Fossil homme", 20, ""), ("luxe", "homme", "Tommy Hilfiger homme", 25, ""),
    ("luxe", "homme", "Columbia manteau homme", 25, ""), ("luxe", "maison", "Samsonite valise", 20, ""),
    ("luxe", "maison", "Dyson", 15, ""), ("luxe", "maison", "Le Creuset", 15, ""),
    # VOLUME · beauté pharmacie (achat récurrent, prix bas)
    ("volume", "beaute", "CeraVe", 20, ""), ("volume", "beaute", "La Roche-Posay", 20, ""),
    ("volume", "beaute", "L'Oréal Paris", 25, ""), ("volume", "beaute", "Maybelline", 25, ""),
    ("volume", "beaute", "Oral-B iO", 25, ""),
    # VOLUME · maison et cuisine (best-sellers)
    ("volume", "maison", "Ninja", 25, ""), ("volume", "maison", "Nespresso", 25, ""),
    ("volume", "maison", "Keurig", 25, ""), ("volume", "maison", "Shark aspirateur", 25, ""),
    ("volume", "maison", "Stanley gobelet", 20, ""), ("volume", "maison", "Yankee Candle", 25, ""),
    # VOLUME · tech populaire (commission plus basse, mais ça vend)
    ("volume", "tech", "Fire TV Stick", 25, ""), ("volume", "tech", "Echo Dot", 25, ""),
    ("volume", "tech", "JBL", 30, ""), ("volume", "tech", "Anker chargeur", 30, ""),
    # VOLUME · enfants, épicerie, animaux
    ("volume", "jouets", "LEGO", 20, ""), ("volume", "jouets", "Hot Wheels", 30, ""),
    ("volume", "jouets", "Squishmallows", 25, ""), ("volume", "jouets", "Melissa & Doug", 30, ""),
    ("volume", "epicerie", "Yupik", 20, "local"), ("volume", "epicerie", "café en grains", 25, ""),
    ("volume", "animaux", "jouet chien", 30, ""), ("volume", "animaux", "litière chat", 25, ""),
]

# Saisons : ajoutées automatiquement selon le mois
SEASON = {
    10: [("volume", "halloween", "costume halloween enfant", 25, ""), ("volume", "halloween", "décoration halloween", 30, ""),
         ("luxe", "beaute", "coffret cadeau beauté", 20, "gift"), ("luxe", "homme", "coffret cadeau homme", 20, "gift")],
    11: [("luxe", "beaute", "coffret cadeau beauté", 20, "gift"), ("luxe", "beaute", "calendrier de l'Avent beauté", 15, "gift"),
         ("luxe", "homme", "coffret cadeau homme", 20, "gift"), ("volume", "jouets", "calendrier de l'Avent LEGO", 15, "gift"),
         ("volume", "maison", "cadeau Noël femme", 30, "gift")],
    12: [("volume", "maison", "bas de Noël idées", 30, "gift"), ("luxe", "beaute", "coffret cadeau beauté", 20, "gift"),
         ("luxe", "homme", "coffret cadeau homme", 20, "gift"), ("volume", "jouets", "jeu de société famille", 25, "gift")],
    1: [("luxe", "femme", "manteau hiver femme", 30, ""), ("volume", "maison", "rangement organisation", 30, ""),
        ("volume", "maison", "équipement entraînement maison", 30, "")],
    2: [("luxe", "beaute", "coffret parfum femme", 20, "gift"), ("luxe", "femme", "bijoux femme Saint-Valentin", 25, "gift")],
}


def searches(month):
    return BASE + SEASON.get(month, [])


RESOURCES = ["itemInfo.title", "itemInfo.byLineInfo", "images.primary.large", "offersV2.listings.price",
             "offersV2.listings.dealDetails", "offersV2.listings.availability", "offersV2.listings.isBuyBoxWinner"]


def post(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def token():
    r = post(TOKEN_URL, {"grant_type": "client_credentials", "client_id": os.environ["AMZ_CLIENT_ID"],
                         "client_secret": os.environ["AMZ_CLIENT_SECRET"], "scope": "creatorsapi::default"}, {})
    return r["access_token"]


def dig(o, *path):
    for p in path:
        if isinstance(o, list):
            o = o[0] if o else None
        if not isinstance(o, dict):
            return None
        o = o.get(p)
    return o


def to_deal(item, cat, today, tier="volume", minpct=MIN_SAVING, badge=""):
    listing = dig(item, "offersV2", "listings")
    listing = listing[0] if isinstance(listing, list) and listing else (listing or {})
    pct = dig(listing, "price", "savings", "percentage") or dig(listing, "price", "savingBasis", "percentage")
    try:
        pct = int(round(float(pct)))
    except (TypeError, ValueError):
        return None
    if pct < minpct:
        return None
    title = dig(item, "itemInfo", "title", "displayValue")
    if not title or not item.get("asin"):
        return None
    brand = dig(item, "itemInfo", "byLineInfo", "brand", "displayValue") or ""
    flag = dig(listing, "dealDetails", "badge") or "Rabais affiché sur Amazon"
    return {"r": 0.5, "cat": cat, "asin": item["asin"], "pct": pct, "amzPct": pct, "flag": flag,
            "brand": brand, "name": title[:110], "why": "", "badge": badge, "tier": tier,
            "img": dig(item, "images", "primary", "large", "url") or "",
            "live": True, "added": today, "source": "api"}


def main():
    if not os.environ.get("AMZ_CLIENT_ID") or not os.environ.get("AMZ_CLIENT_SECRET"):
        print("Identifiants Amazon absents : aucune recherche automatique.")
        return
    try:
        bearer = token()
    except urllib.error.HTTPError as e:
        print("Échec de l'authentification Amazon :", e.code, e.read()[:300]); return
    headers = {"Authorization": f"Bearer {bearer}", "x-marketplace": MARKET}
    today = datetime.date.today().isoformat()
    found, seen, ok = [], set(), 0
    for tier, cat, kw, minpct, badge in searches(datetime.date.today().month):
        body = {"partnerTag": TAG, "marketplace": MARKET, "keywords": kw, "itemCount": PER_SEARCH,
                "minSavingPercent": minpct, "resources": RESOURCES}
        try:
            res = post(f"{API}/searchItems", body, headers)
        except urllib.error.HTTPError as e:
            msg = e.read()[:300]
            if b"AssociateNotEligible" in msg:
                print("Compte pas encore admissible a l'API (10 ventes qualifiees sur 30 jours requises). Deals du site inchanges.")
                return
            print(f"[{kw}] erreur {e.code} :", msg); continue
        except Exception as e:
            print(f"[{kw}] erreur :", e); continue
        ok += 1
        for it in dig(res, "searchResult", "items") or []:
            d = to_deal(it, cat, today, tier, minpct, badge)
            if d and d["asin"] not in seen:
                seen.add(d["asin"]); found.append(d)
    if ok == 0:
        print("Aucune recherche n'a fonctionne : deals du site inchanges.")
        return
    # Chaque niveau garde ses meilleurs rabais, avec un maximum de 8 par catégorie pour garder le site varié
    keep = []
    for tier, n in QUOTA.items():
        per_cat = {}
        for d in sorted((d for d in found if d["tier"] == tier), key=lambda d: -d["pct"]):
            if per_cat.get(d["cat"], 0) < 8 and len([k for k in keep if k["tier"] == tier]) < n:
                per_cat[d["cat"]] = per_cat.get(d["cat"], 0) + 1; keep.append(d)
    found = keep[:MAX_TOTAL]
    data = json.loads((ROOT / "data.json").read_text())
    manual = [d for d in data["deals"] if d.get("source") != "api"]
    manual_asins = {d.get("asin") for d in manual}
    data["deals"] = manual + [d for d in found if d["asin"] not in manual_asins]
    (ROOT / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"{len(found)} deals automatiques trouvés.")


if __name__ == "__main__":
    sys.exit(main())
