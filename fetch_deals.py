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
MIN_SAVING = 20      # rabais minimum affiché par Amazon (%)
PER_SEARCH = 10      # produits par recherche
MAX_TOTAL = 80       # plafond de deals automatiques sur le site

# (catégorie du site, mots-clés) : les thèmes qui rapportent le plus en premier
SEARCHES = [
    ("beaute", "Clarins"), ("beaute", "Lancôme"), ("beaute", "Kérastase"), ("beaute", "L'Oréal Paris"),
    ("beaute", "Maybelline"), ("beaute", "First Aid Beauty"), ("beaute", "Shark séchoir"), ("beaute", "Oral-B iO"),
    ("femme", "bottes hiver femme"), ("femme", "sac à main femme"), ("femme", "bijoux femme"),
    ("homme", "montre homme"), ("homme", "manteau homme hiver"),
    ("maison", "Ninja"), ("maison", "Nespresso"), ("maison", "Keurig"), ("maison", "Shark aspirateur"),
    ("maison", "Dyson"), ("maison", "Yankee Candle"), ("maison", "Stanley gobelet"),
    ("tech", "Sony casque"), ("tech", "JBL"), ("tech", "Bose"), ("tech", "Apple AirPods"), ("tech", "Fire TV Stick"),
    ("jouets", "LEGO"), ("jouets", "Hot Wheels"), ("jouets", "Barbie"), ("enfants", "jouet bébé"),
    ("epicerie", "Yupik"), ("epicerie", "café en grains"), ("epicerie", "Clover Leaf"),
    ("animaux", "jouet chien"), ("animaux", "chat griffoir"),
    ("halloween", "costume halloween enfant"), ("halloween", "décoration halloween"),
]
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


def to_deal(item, cat, today):
    listing = dig(item, "offersV2", "listings")
    listing = listing[0] if isinstance(listing, list) and listing else (listing or {})
    pct = dig(listing, "price", "savings", "percentage") or dig(listing, "price", "savingBasis", "percentage")
    try:
        pct = int(round(float(pct)))
    except (TypeError, ValueError):
        return None
    if pct < MIN_SAVING:
        return None
    title = dig(item, "itemInfo", "title", "displayValue")
    if not title or not item.get("asin"):
        return None
    brand = dig(item, "itemInfo", "byLineInfo", "brand", "displayValue") or ""
    flag = dig(listing, "dealDetails", "badge") or "Rabais affiché sur Amazon"
    return {"r": 0.5, "cat": cat, "asin": item["asin"], "pct": pct, "amzPct": pct, "flag": flag,
            "brand": brand, "name": title[:110], "why": "", "badge": "",
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
    for cat, kw in SEARCHES:
        body = {"partnerTag": TAG, "marketplace": MARKET, "keywords": kw, "itemCount": PER_SEARCH,
                "minSavingPercent": MIN_SAVING, "resources": RESOURCES}
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
            d = to_deal(it, cat, today)
            if d and d["asin"] not in seen:
                seen.add(d["asin"]); found.append(d)
    if ok == 0:
        print("Aucune recherche n'a fonctionne : deals du site inchanges.")
        return
    found.sort(key=lambda d: -d["pct"])
    found = found[:MAX_TOTAL]
    data = json.loads((ROOT / "data.json").read_text())
    manual = [d for d in data["deals"] if d.get("source") != "api"]
    manual_asins = {d.get("asin") for d in manual}
    data["deals"] = manual + [d for d in found if d["asin"] not in manual_asins]
    (ROOT / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"{len(found)} deals automatiques trouvés.")


if __name__ == "__main__":
    sys.exit(main())
