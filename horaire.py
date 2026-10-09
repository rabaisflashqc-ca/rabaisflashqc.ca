#!/usr/bin/env python3
"""Décide si la mise à jour doit rouler maintenant (heure du Québec, été comme hiver).

GitHub ne connaît que l'heure UTC. Chaque heure du Québec est donc programmée deux fois
(heure d'été et heure normale) et ce script garde seulement la bonne.
"""
import datetime, os, sys
from zoneinfo import ZoneInfo

# Heure de mise à jour : 30 min avant chaque publication Facebook
TOUS_LES_JOURS = ["06:30", "11:30", "19:30"]        # posts 7 h, 12 h (bonus), 20 h
FIN_DE_SEMAINE = ["08:30"]                           # post 9 h samedi et dimanche
EVENEMENTS = ["09:30", "15:30", "21:30"]             # semaine du Vendredi fou et Boxing Day
PERIODES = [((11, 20), (12, 2)), ((12, 24), (12, 28))]
FENETRE = 40  # minutes de retard tolérées (GitHub démarre parfois en retard)

def prevues(now):
    h = list(TOUS_LES_JOURS)
    if now.weekday() >= 5: h += FIN_DE_SEMAINE
    if any((a <= (now.month, now.day) <= b) for a, b in PERIODES): h += EVENEMENTS
    return h

def tranche(h):
    """matin avant 11 h, midi avant 17 h, sinon soir."""
    return "matin" if h < 11 else "midi" if h < 17 else "soir"

def main():
    now = datetime.datetime.now(ZoneInfo("America/Toronto"))
    out = os.environ.get("GITHUB_OUTPUT", os.devnull)
    open(out, "a").write(f"slot={tranche(now.hour)}\n")
    if os.environ.get("GITHUB_EVENT_NAME") != "schedule":
        print("Lancement manuel : on roule."); open(out, "a").write("go=1\n"); return 0
    for hm in prevues(now):
        t = now.replace(hour=int(hm[:2]), minute=int(hm[3:]), second=0, microsecond=0)
        if 0 <= (now - t).total_seconds() / 60 <= FENETRE:
            print(f"Mise à jour de {hm} (il est {now:%H:%M} au Québec)."); 
            open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a").write("go=1\n"); return 0
    print(f"Il est {now:%H:%M} au Québec : pas une heure prévue, on saute.")
    open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a").write("go=0\n"); return 0

if __name__ == "__main__":
    sys.exit(main())
