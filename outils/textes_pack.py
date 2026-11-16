#!/usr/bin/env python3
"""Textes d'un pack dans le positionnement du 16 nov. 2026 : chaque deal reçoit son verdict, l'accroche parle en dollars, la signature ferme le post.
Usage : python3 outils/textes_pack.py suivi/posts/FICHIER.md "ACCROCHE" "#mot1 #mot2"
Réécrit les sections Facebook, Premier commentaire Facebook, Instagram et TikTok à partir du bloc « Données (ne pas publier) ». Le reste du fichier ne bouge pas.
Lancer ensuite le verrou outils/verifier_pack.py."""
import sys, re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from verdict import verdict, eco, eco_txt, SIGNATURE, ACCROCHE
MENTION = "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises."
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juill.", "août", "sept.", "oct.", "nov.", "déc."]
NUM = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
money = lambda v: f"{v:,.2f}".replace(",", " ").replace(".", ",") + " $"

def main():
    fichier, accroche, tags = pathlib.Path(sys.argv[1]), sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "")
    md = fichier.read_text()
    deals = json.loads(re.search(r"## Données \(ne pas publier\)\s*```json\s*(.+?)```", md, re.S).group(1))
    j, m = int(deals[0]["price_verified_at"][8:10]), int(deals[0]["price_verified_at"][5:7])
    jour = f'{"1er" if j == 1 else j} {MOIS[m - 1]}'
    v = lambda d: verdict(d)[0] or "👍 Bon rabais"
    lignes = "\n".join(f'{NUM[i]} {d["nom"]} : {money(d["price"])} au lieu de {money(d["was"])} (-{d["pct"]} %)\n     {eco_txt(eco(d))} de moins. Verdict : {v(d)}' for i, d in enumerate(deals))
    mx = eco_txt(max(eco(d) for d in deals)); n = len(deals)
    choix = "Lequel tu prends? " + (", ".join(str(i + 1) for i in range(n - 1)) + f" ou {n}?" if n > 1 else "Oui ou non?") + " 👇"
    fb = (f"{accroche}\n\nOn a fait le tri. Jusqu'à {mx} de moins, avec notre verdict sur chacun :\n\n{lignes}\n\n{choix}\n\n"
          f"{ACCROCHE[:-1]} 👉 rabaisflashqc point ca (bouton « Voir le site » de la page).\n⚡ {SIGNATURE}\n\nPrix observés le {jour.rstrip(".")}.\n{MENTION}")
    com = f"👉 Tape rabaisflashqc point ca dans ton navigateur. {SIGNATURE}"
    ig = (f"{accroche}\n\nJusqu'à {mx} de moins, avec notre verdict sur chacun :\n\n{lignes}\n\n{choix}\n{ACCROCHE[:-1]} 👉 rabaisflashqc.ca, lien dans la bio.\n⚡ {SIGNATURE}\n\n"
          f"Prix observés le {jour.rstrip('.')}.\n{MENTION}\n\n{tags} #rabaisqc #quebec #dealsqc".strip())
    court = " ".join(f'{d["nom"]} {money(d["price"])} (-{d["pct"]} %), {v(d).split(" ", 1)[1].lower()}.' for d in deals)
    tt = (f"{accroche} {court} T'es d'accord avec nos verdicts? 👇 {SIGNATURE} Liens sur rabaisflashqc.ca\n{MENTION}\n{tags} #rabaisqc #quebec".strip()
          + "\n\nCommentaire à épingler : Avant d'acheter, regarde sur rabaisflashqc.ca 👈 tape-le dans ton navigateur!")
    tete = md[:md.index("## Facebook")]; queue = md[md.index("## Données (ne pas publier)"):]
    fichier.write_text(f"{tete}## Facebook\n\n{fb}\n\n## Premier commentaire Facebook\n\n{com}\n\n## Instagram\n\n{ig}\n\n## TikTok\n\n{tt}\n\n{queue}")
    print(fichier)
main()
