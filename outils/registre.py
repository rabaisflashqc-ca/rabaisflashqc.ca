#!/usr/bin/env python3
"""Registre des produits déjà publiés : pause de 30 jours (plan du 19 nov. 2026, point 3).

Règle : un produit (ASIN) publié en vedette ne revient pas pendant PAUSE_JOURS jours, SAUF si son prix a baissé d'au moins
BAISSE_MIN (3 %) sous le dernier prix publié : la baisse est alors la nouvelle. Dans une sélection (Top 3, Top 5), au plus
TOLERE_SELECTION produit déjà publié est toléré.

Usage :
  python3 outils/registre.py amorcer                       # (re)construit suivi/publies.json depuis suivi/posts/*.md
  python3 outils/registre.py verifier ASIN PRIX [AAAA-MM-JJ]   # LIBRE / PAUSE / LEVEE
  python3 outils/registre.py enregistrer suivi/posts/FICHIER.md  # après la publication (ligne « Publié : » présente)
  python3 outils/registre.py liste
Utilisé par verifier_pack.py (verrou), pack_du_jour.py et pack_un_deal.py.
"""
import json, pathlib, re, sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
FICHIER = ROOT / "suivi" / "publies.json"
PAUSE_JOURS = 30
BAISSE_MIN = 0.03
TOLERE_SELECTION = 1
QC = ZoneInfo("America/Toronto")


def charger():
    try:
        return json.loads(FICHIER.read_text(encoding="utf-8"))
    except Exception:
        return {"asins": {}}


def sauver(reg):
    FICHIER.parent.mkdir(exist_ok=True)
    FICHIER.write_text(json.dumps(reg, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def aujourdhui():
    return datetime.now(QC).date()


def etat(asin, prix, jour=None, pack=None, reg=None):
    """('libre'|'pause'|'levee', explication). `pack` = nom du fichier en cours de vérification : ses propres lignes sont ignorées."""
    reg = reg or charger()
    jour = jour or aujourdhui()
    if isinstance(jour, str):
        jour = date.fromisoformat(jour)
    vus = [x for x in reg.get("asins", {}).get(asin, []) if x.get("pack") != pack]
    if not vus:
        return "libre", "jamais publié"
    dernier = max(vus, key=lambda x: x["date"])
    d = date.fromisoformat(dernier["date"])
    age = (jour - d).days
    if age >= PAUSE_JOURS:
        return "libre", f"dernière publication il y a {age} jours (pause de {PAUSE_JOURS} jours terminée)"
    p0 = dernier.get("price")
    if p0 and prix is not None and prix <= p0 * (1 - BAISSE_MIN):
        return "levee", f"déjà publié le {d} à {p0:.2f} $, mais le prix a baissé à {prix:.2f} $ (au moins {BAISSE_MIN:.0%} de moins)"
    return "pause", f"déjà publié le {d} à {p0 if p0 is not None else '?'} $ ({PAUSE_JOURS - age} jours de pause restants, prix pas plus bas)"


def donnees(md):
    m = re.search(r"##\s+Données \(ne pas publier\)\s*```json\s*(.+?)```", md, re.S)
    return json.loads(m.group(1)) if m else []


def date_fichier(nom):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", nom)
    return m.group(1) if m else None


def ajouter(reg, asin, jour, prix, pack, nom=""):
    L = reg.setdefault("asins", {}).setdefault(asin, [])
    if not any(x.get("pack") == pack for x in L):
        L.append({"date": jour, "price": prix, "pack": pack, "nom": nom})


def enregistrer(chemin, exiger_publie=True):
    p = pathlib.Path(chemin)
    md = p.read_text(encoding="utf-8")
    publie = [l for l in md.splitlines() if l.startswith("Publié :")]
    if exiger_publie and not publie:
        print("Pas de ligne « Publié : » dans le fichier : rien d'enregistré (ajoute-la d'abord).")
        return 1
    if publie and re.search(r"annul", publie[-1], re.I):
        print("Pack annulé : rien d'enregistré.")
        return 0
    jour = date_fichier(p.name)
    if not jour:
        print("Nom de fichier sans date AAAA-MM-JJ : rien d'enregistré.")
        return 1
    reg = charger()
    n = 0
    for d in donnees(md):
        if d.get("asin"):
            ajouter(reg, d["asin"], jour, d.get("price"), p.name, d.get("nom", ""))
            n += 1
    sauver(reg)
    print(f"{n} produit(s) enregistré(s) depuis {p.name}.")
    return 0


def amorcer():
    """Reprend les packs déjà préparés (sauf ceux marqués annulés) pour ne pas republier ce qui est déjà sorti."""
    reg = {"asins": {}}
    for p in sorted((ROOT / "suivi" / "posts").glob("*.md")):
        md = p.read_text(encoding="utf-8")
        if any(l.startswith("Publié :") and re.search(r"annul", l, re.I) for l in md.splitlines()):
            continue
        jour = date_fichier(p.name)
        try:
            ds = donnees(md)
        except Exception:
            continue
        for d in ds:
            if jour and d.get("asin"):
                ajouter(reg, d["asin"], jour, d.get("price"), p.name, d.get("nom", ""))
    sauver(reg)
    print(f"Registre amorcé : {len(reg['asins'])} produits.")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    if a[0] == "amorcer":
        amorcer()
    elif a[0] == "verifier":
        st, why = etat(a[1], float(a[2]), a[3] if len(a) > 3 else None)
        print(f"{st.upper()} : {why}")
        sys.exit(1 if st == "pause" else 0)
    elif a[0] == "enregistrer":
        sys.exit(enregistrer(a[1]))
    elif a[0] == "liste":
        for k, v in sorted(charger()["asins"].items()):
            print(k, " | ".join(f'{x["date"]} {x.get("price")}' for x in v), "|", v[-1].get("nom", ""))


if __name__ == "__main__":
    main()
