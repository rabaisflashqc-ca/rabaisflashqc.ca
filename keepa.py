#!/usr/bin/env python3
"""Scan Keepa (Amazon.ca) : deals du jour + vérification des prix affichés sur le site.

Besoin du secret GitHub KEEPA_KEY (forfait API Keepa). Sans clé, le script ne fait rien.
Budget de jetons (forfait Starter, 20 jetons/min, environ 28 800/jour) :
  - deals : 5 jetons par page de 150 deals, on lit 4 pages par passage = 20 jetons
  - prix : 1 jeton par produit, environ 100 produits par passage = 100 jetons
  Un passage par heure coûte environ 120 jetons, soit 10 % du forfait.
Sorties : suivi/deals_keepa.json (deals du jour) et suivi/prix_verifies.json (prix vérifiés).
"""
import os, json, gzip, datetime, pathlib, urllib.request, urllib.parse
ROOT = pathlib.Path(__file__).parent
KEY = os.environ.get("KEEPA_KEY", "").strip()
DOMAIN = 6  # amazon.ca
API = "https://api.keepa.com"
KEEPA_EPOCH = datetime.datetime(2011, 1, 1, tzinfo=datetime.timezone.utc)

def call(path, params=None, body=None):
    q = urllib.parse.urlencode({"key": KEY, **(params or {})})
    req = urllib.request.Request(f"{API}/{path}?{q}", data=(json.dumps(body).encode() if body else None),
                                 headers={"Accept-Encoding": "gzip", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
    j = json.loads(raw)
    print(f"{path} : {j.get('tokensLeft')} jetons restants, {j.get('tokensConsumed')} consommés")
    return j

def img_url(x):
    """Nom de fichier de l'image principale (Keepa : liste de codes de caractères ou chaîne CSV)."""
    im = x.get("image") or x.get("imagesCSV") or ""
    if isinstance(im, list): im = "".join(map(chr, im))
    im = im.split(",")[0].strip()
    return f"https://m.media-amazon.com/images/I/{im}" if im else None

CATS = [("beaute", "beauty|skin|hair|makeup|fragrance|personal care|health"), ("enfants", "toy|baby|kids|game"),
        ("tech", "electronic|computer|camera|phone|video game|headphone|tv"), ("mode", "clothing|shoe|fashion|jewel|watch|luggage"),
        ("animaux", "pet"), ("plein-air", "sport|outdoor|tool|automotive|garden"), ("epicerie", "grocery|gourmet")]
def categorie(path):
    p = (path or "").lower()
    for c, pat in CATS:
        if any(w in p for w in pat.split("|")): return c
    return "maison"

def deals(now):
    """Baisses de prix des dernières 24 h sur amazon.ca, vendues par Amazon, 20 à 85 % de rabais, 10 $ à 300 $."""
    out = []
    for page in range(4):
        sel = {"page": page, "domainId": DOMAIN, "priceTypes": [0], "dateRange": 0,
               "deltaPercentRange": [20, 85], "currentRange": [1000, 30000], "isRangeEnabled": True,
               "isFilterEnabled": True, "hasReviews": True, "filterErotic": True, "singleVariation": True,
               "sortType": 4, "salesRankRange": [1, 100000]}
        try: j = call("deal", body=sel)
        except Exception as ex: print("deal page", page, ex); break
        dr = (j.get("deals") or {}).get("dr") or []
        for x in dr:
            try:
                cur = x["current"][0]
                if not cur or cur <= 0: continue
                d = x["delta"][0][0] if isinstance(x["delta"][0], list) else x["delta"][0]
                was = cur - d if d < 0 else None
                if not was or was <= cur: continue
                pct = round((1 - cur / was) * 100)
                seen = (KEEPA_EPOCH + datetime.timedelta(minutes=x.get("lastUpdate") or 0)) if x.get("lastUpdate") else now
                if (now - seen).total_seconds() > 24 * 3600: continue
                s = seen.astimezone(datetime.timezone(datetime.timedelta(hours=-5))).isoformat(timespec="minutes")
                out.append({"asin": x["asin"], "title": x.get("title", "")[:140], "cat": categorie(" ".join(map(str, x.get("categoryTree") or x.get("rootCat") and [x["rootCat"]] or []))),
                            "price": cur / 100, "was": round(was / 100, 2), "pct": pct, "posted": s, "seen": s,
                            "until": (seen + datetime.timedelta(days=7)).isoformat(timespec="minutes"),
                            "votes": None, "img_url": img_url(x), "source": "keepa"})
            except Exception: continue
        if len(dr) < 150: break
    return out

def verifier(asins, now):
    """Prix actuel (Amazon, sinon neuf) et disponibilité de chaque produit affiché sur le site."""
    v = {}
    for i in range(0, len(asins), 100):
        lot = asins[i:i + 100]
        try: j = call("product", {"domain": DOMAIN, "asin": ",".join(lot), "stats": 1})
        except Exception as ex: print("product", ex); continue
        for p in j.get("products") or []:
            st = p.get("stats") or {}
            cur = (st.get("current") or [-1, -1])
            price = cur[0] if cur[0] and cur[0] > 0 else (cur[1] if len(cur) > 1 and cur[1] and cur[1] > 0 else None)
            avg = (st.get("avg90") or [-1])[0]
            lst = cur[4] if len(cur) > 4 and cur[4] and cur[4] > 0 else None  # prix de liste
            was = lst if lst and price and lst > price else (avg if avg and price and avg > price else None)
            v[p["asin"]] = {"price": round(price / 100, 2) if price else None, "was": round(was / 100, 2) if was else None,
                            "dispo": bool(price), "seen": now.astimezone(datetime.timezone(datetime.timedelta(hours=-5))).isoformat(timespec="minutes"),
                            "img_url": img_url(p), "source": "keepa"}
    return v

def main():
    if not KEY: print("Pas de clé KEEPA_KEY : rien à faire."); return
    now = datetime.datetime.now(datetime.timezone.utc)
    dl = deals(now)
    (ROOT / "suivi" / "deals_keepa.json").write_text(json.dumps(dl, ensure_ascii=False, indent=1))
    print(len(dl), "deals du jour")
    try: aff = [x["asin"] for x in json.loads((ROOT / "suivi" / "a_verifier.json").read_text())["produits"]]
    except Exception: aff = []
    aff = list(dict.fromkeys(aff))[:300]
    v = verifier(aff, now)
    for x in dl:  # les deals Keepa sont vérifiés par définition
        v[x["asin"]] = {"price": x["price"], "was": x["was"], "dispo": True, "seen": x["seen"], "img_url": x.get("img_url"), "source": "keepa"}
    (ROOT / "suivi" / "prix_verifies.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print(len(v), "prix vérifiés")

if __name__ == "__main__":
    main()
