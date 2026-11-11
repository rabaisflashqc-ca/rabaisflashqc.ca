#!/usr/bin/env python3
"""Verrou de publication Rabais Flash QC : PASS ou BLOCK.

Usage : python3 outils/verifier_pack.py suivi/posts/AAAA-MM-JJ-matin.md suivi/deals_chrome.json [--max-heures 24] [--maintenant ISO]
Sortie : une ligne par contrôle, puis « RESULTAT: PASS » (code 0) ou « RESULTAT: BLOCK » (code 1).

Le pack doit contenir une section « ## Données (ne pas publier) » avec un bloc ```json``` :
[{"asin": "...", "nom": "...", "price": 25.99, "was": 35.99, "pct": 28,
  "price_verified_at": "2026-11-03T08:12-05:00", "price_source": "keepa", "discovered_at": "..."}]
price_verified_at = heure réelle où le prix a été lu (champ seen de deals_chrome.json), jamais l'heure d'un scan
qui n'a pas lu le prix. discovered_at = moment où l'offre a été repérée (information seulement).
"""
import json, re, sys
from datetime import datetime, timezone, timedelta

MENTION = "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises."
SOURCES_OK = {"keepa", "amazon"}  # "amazon" : page de deals amazon.ca envoyée par Alex et lue en une passe (exception du 7 nov., AUTONOMIE.md)
TEXTES = ["Facebook", "Premier commentaire Facebook", "Instagram", "TikTok"]
from zoneinfo import ZoneInfo
QC = ZoneInfo("America/Toronto")


def iso(s):
    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def sections(md):
    out, cur = {}, None
    for ligne in md.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", ligne)
        if ligne.startswith("Publié :"):
            cur = None
        elif m:
            cur = m.group(1)
            out[cur] = []
        elif cur:
            out[cur].append(ligne)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def prix_fr(v):
    return f"{v:,.2f}".replace(",", " ").replace(".", ",") + " $"


def main():
    args = sys.argv[1:]
    max_h = 24.0
    now = datetime.now(timezone.utc)
    if "--max-heures" in args:
        i = args.index("--max-heures"); max_h = float(args[i + 1]); del args[i:i + 2]
    if "--maintenant" in args:
        i = args.index("--maintenant"); now = iso(args[i + 1]); del args[i:i + 2]
    pack_path, source_path = args[0], args[1]
    md = open(pack_path, encoding="utf-8").read()
    sec = sections(md)
    erreurs, ok = [], []

    def check(cond, msg):
        (ok if cond else erreurs).append(msg)
        return cond

    # 1. Textes présents, mention, pas de mentions interdites
    for nom in TEXTES:
        if not check(nom in sec and sec[nom], f"section « {nom} » présente"):
            continue
        t = sec[nom]
        if nom != "Premier commentaire Facebook":
            check(MENTION in t, f"{nom} : mention Partenaire Amazon")
        sans_hashtags = re.sub(r"#\w+", "", t)
        check(not re.search(r"amazon\.ca", sans_hashtags, re.I), f"{nom} : aucun « Amazon.ca » cliquable")
        check(not re.search(r"redflag|\brfd\b", t, re.I), f"{nom} : aucune mention du forum source")
        check(not re.search(r"partenaire officiel", t, re.I), f"{nom} : pas de « partenaire officiel »")
        check(not re.search(r"plus que \d+ en stock|derni[eè]res? unit", t, re.I), f"{nom} : pas de faux manque")
    if "Premier commentaire Facebook" in sec:
        check(re.search(r"rabaisflashqc(\.ca| point ca)", sec["Premier commentaire Facebook"]), "premier commentaire : adresse du site (« rabaisflashqc point ca » depuis la limite de liens Facebook du 9 nov.)")

    # 2. Données des deals
    data = sec.get("Données (ne pas publier)", "")
    m = re.search(r"```json\s*(.+?)```", data, re.S)
    if not check(bool(m), "bloc JSON des deals présent (section « Données (ne pas publier) »)"):
        return fin(ok, erreurs)
    try:
        deals = json.loads(m.group(1))
    except Exception as e:
        check(False, f"bloc JSON lisible ({e})")
        return fin(ok, erreurs)
    check(isinstance(deals, list) and len(deals) >= 1, "au moins 1 deal")
    src = {}
    try:
        for d in json.load(open(source_path, encoding="utf-8")):
            src[d.get("asin")] = d
    except Exception as e:
        check(False, f"source des prix lisible ({source_path} : {e})")

    heures_ok = set()
    tous = "\n".join(sec.get(n, "") for n in TEXTES)
    for d in deals:
        n = d.get("nom") or d.get("asin")
        for champ in ("asin", "price", "was", "pct", "price_verified_at", "price_source"):
            check(d.get(champ) not in (None, ""), f"{n} : champ {champ}")
        if not d.get("price_verified_at"):
            continue
        check(d.get("price_source") in SOURCES_OK, f"{n} : source de prix autorisée ({d.get('price_source')})")
        v = iso(d["price_verified_at"])
        age = (now - v).total_seconds() / 3600
        check(-0.25 <= age <= max_h, f"{n} : prix vérifié il y a {age:.1f} h (max {max_h:g} h)")
        s = src.get(d.get("asin"))
        if check(s is not None, f"{n} : ASIN présent dans la source vérifiée"):
            check(abs(float(s.get("price", -1)) - float(d["price"])) < 0.005, f"{n} : prix identique à la source ({s.get('price')})")
            check(s.get("seen") and iso(s["seen"]) == v, f"{n} : heure de vérification = seen de la source ({s.get('seen')})")
        p = prix_fr(float(d["price"]))
        check(p in sec.get("Facebook", ""), f"{n} : prix {p} écrit tel quel dans le texte Facebook")
        try:
            pct = round((1 - float(d["price"]) / float(d["was"])) * 100)
            check(abs(pct - int(d["pct"])) <= 1, f"{n} : % cohérent avec prix et ancien prix ({pct} %)")
        except Exception:
            check(False, f"{n} : % calculable")
        lv = v.astimezone(QC)
        heures_ok.add(f"{lv.hour} h {lv.minute:02d}")
    # 3. Aucune heure inventée : chaque « à H h MM » des textes doit être une heure de vérification réelle
    for h in set(re.findall(r"à (\d{1,2} h \d{2})", tous)):
        check(h in heures_ok, f"heure « {h} » des textes = une vraie heure de vérification")
    return fin(ok, erreurs)


def fin(ok, erreurs):
    for m in ok:
        print("OK    " + m)
    for m in erreurs:
        print("BLOCK " + m)
    print("RESULTAT: " + ("PASS" if not erreurs else "BLOCK"))
    sys.exit(0 if not erreurs else 1)


if __name__ == "__main__":
    main()
