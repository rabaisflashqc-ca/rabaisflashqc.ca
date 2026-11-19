"""Verdict Rabais Flash QC (positionnement du 16 nov. 2026) : une seule règle pour le site, les posts, les réels et l'infolettre.
Règle publiée sur rabaisflashqc.ca/a-propos/#choix. Ne pas baisser les seuils pour avoir plus de « Ça vaut le clic » : il doit rester rare (environ 1 deal sur 4)."""
SIGNATURE = "Les rabais qui valent vraiment le clic."
ACCROCHE = "Avant d'acheter sur Amazon, regarde ici."

def eco(x):
    """Économie en dollars (prix d'avant moins prix actuel)."""
    try: return max(float(x["was"]) - float(x["price"]), 0)
    except Exception: return 0

def eco_txt(v):
    """Arrondi vers le bas : jamais plus que la vraie économie."""
    return f"{int(v + 0.005)} $" if v >= 10 else f"{v:.2f} $".replace(".", ",")

def verdict(x):
    """Retourne (texte, classe CSS). Record Keepa = « Plus bas prix jamais vu »; 40 % et plus ET au moins 20 $ de moins = « Ça vaut le clic »;
    Offre à durée limitée (champ limite, minuterie ou « Offre à durée limitée » sur Amazon) à 30 % et plus ET au moins 15 $ de moins = « Ça vaut le clic » aussi.
    20 % et plus = « Bon rabais ». Sinon, pas de verdict.
    Champ ref = "conseille" (rabais calculé sur le prix conseillé du fabricant, pas sur un ancien prix réel) : pas de verdict fort, sauf offre à durée limitée (règle ci-dessus)."""
    pct, v = x.get("pct") or 0, eco(x)
    if x.get("record"): return "📉 Plus bas prix jamais vu", "v rec"
    if pct >= 40 and v >= 20 and x.get("ref") != "conseille": return "🔥 Ça vaut le clic", "v hot"  # pas de verdict fort quand le rabais se compare au prix conseillé (souvent gonflé)
    if x.get("limite") and pct >= 30 and v >= 15: return "🔥 Ça vaut le clic", "v hot"  # demande d'Alex du 18 nov. : offre à durée limitée (minuterie Amazon) à 30 % et plus et 15 $ de moins = à saisir
    if pct >= 20: return "👍 Bon rabais", "v"
    return "", ""
