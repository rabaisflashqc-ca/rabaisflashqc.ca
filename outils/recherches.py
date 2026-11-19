#!/usr/bin/env python3
"""Journal des recherches du site : quoi chercher en priorité (plan du 19 nov. 2026, point 2).

Usage : python3 outils/recherches.py suivi/recherches.csv [--jours 7]
Le CSV est l'export de la feuille de réponses du formulaire Google qui reçoit les mots cherchés
(colonnes : Horodateur, Mot cherché, Résultats, Canal). Aucune donnée personnelle : seulement le mot, le nombre
de résultats et le canal d'arrivée.
Écrit suivi/recherches.md (à lire avant la passe Keepa de 8 h 03) et suivi/cibles_recherche.json (mots à chercher en priorité).
"""
import csv, json, pathlib, re, sys, unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMATS = ("%Y/%m/%d %I:%M:%S %p", "%Y/%m/%d %H:%M:%S", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S")


def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9$ ]+", " ", s)).strip()


def date(s):
    s = re.sub(r"\s+[A-Z]{2,4}$", "", (s or "").strip())  # « EST » à la fin
    for f in FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None


def lire(chemin):
    with open(chemin, encoding="utf-8-sig", newline="") as fh:
        rd = csv.reader(fh)
        tete = [norm(c) for c in next(rd, [])]
        def col(*mots):
            for i, c in enumerate(tete):
                if any(m in c for m in mots):
                    return i
            return None
        iq, ir, ic, it = col("mot", "recherche", "terme"), col("resultat"), col("canal", "source"), col("horodateur", "date", "timestamp")
        if iq is None:
            iq, ir, ic, it = 1, 2, 3, 0
        out = []
        for row in rd:
            try:
                q = norm(row[iq])
                n = int(re.sub(r"\D", "", row[ir]) or 0) if ir is not None and ir < len(row) else 0
            except Exception:
                continue
            if len(q) < 3:
                continue
            can = (row[ic].strip().lower() if ic is not None and ic < len(row) else "") or "direct"
            d = date(row[it]) if it is not None and it < len(row) else None
            out.append({"q": q, "n": n, "canal": can, "date": d})
        return out


def main():
    args = sys.argv[1:]
    jours = 7
    if "--jours" in args:
        i = args.index("--jours"); jours = int(args[i + 1]); del args[i:i + 2]
    src = pathlib.Path(args[0]) if args else ROOT / "suivi/recherches.csv"
    L = lire(src)
    dates = [x["date"] for x in L if x["date"]]
    fin = max(dates) if dates else None
    if fin:
        L = [x for x in L if x["date"] is None or x["date"] >= fin - timedelta(days=jours)]
    tot, zero, bas, canal, pires = Counter(), Counter(), Counter(), Counter(), defaultdict(list)
    for x in L:
        tot[x["q"]] += 1
        canal[x["canal"]] += 1
        pires[x["q"]].append(x["n"])
        if x["n"] == 0:
            zero[x["q"]] += 1
        elif x["n"] <= 2:
            bas[x["q"]] += 1
    out = [f"# Recherches du site, {jours} derniers jours", "",
           f"{len(L)} recherches, {len(tot)} mots différents" + (f", jusqu'au {fin:%Y-%m-%d}" if fin else "") + ".", "",
           "## À chercher en priorité (aucun résultat sur le site)", ""]
    out += [f"- **{q}** : {c} fois" for q, c in zero.most_common(15)] or ["- Rien pour l'instant."]
    out += ["", "## À renforcer (1 ou 2 résultats seulement)", ""]
    out += [f"- {q} : {c} fois" for q, c in bas.most_common(10)] or ["- Rien pour l'instant."]
    out += ["", "## Les plus cherchés", ""]
    out += [f"- {q} : {c} fois (résultats habituels : {sorted(pires[q])[len(pires[q]) // 2]})" for q, c in tot.most_common(15)]
    out += ["", "## Par canal d'arrivée", ""] + [f"- {c} : {n}" for c, n in canal.most_common()]
    out += ["", "Règle : un mot cherché au moins 3 fois sans résultat devient une cible de la passe Keepa du lendemain matin (suivi/cibles_recherche.json).", ""]
    (ROOT / "suivi/recherches.md").write_text("\n".join(out), encoding="utf-8")
    cibles = [{"mot": q, "fois": c} for q, c in (zero + bas).most_common(20) if c >= 3 or zero[q] >= 3]
    (ROOT / "suivi/cibles_recherche.json").write_text(json.dumps({"jours": jours, "cibles": cibles}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(L)} recherches lues, {len(zero)} mots sans résultat, {len(cibles)} cibles pour le scan.")


if __name__ == "__main__":
    main()
