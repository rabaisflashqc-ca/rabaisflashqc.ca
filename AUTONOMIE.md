# Rabais Flash QC : guide d'autonomie de Claude

Ce fichier est la référence pour toutes les sessions de Claude (tâches planifiées dans le nuage et sessions Cowork avec Chrome sur l'ordinateur d'Alex). Lis-le au début de chaque session. Plan d'affaires complet : doc « Plan d'affaires Rabais Flash QC, jusqu'au 15 janvier ».

## Objectifs (jusqu'au 15 janvier 2027)

- Abonnés : point de départ le 30 oct. 2026 = 223 Facebook + 1 Instagram. Cible 500 au total, puis 800 au 15 janv. TikTok ouvert le 30 oct.
- Commissions Amazon Associés : 14 $ cumulés au 30 oct. Paliers pour décembre : 150 $ (plancher), 500 $ (bon mois), 2 000 $ par mois (étirement, demandé par Alex).
- Budget pub : 5 $ par jour. Test du 31 oct. au 6 nov. : pub A « Suivre la page » 3 $/jour, pub B « Trafic vers le site » 2 $/jour. Alex lance les pubs lui-même.

## Rôle de Claude

Marketeur viral et vendeur, autonome. Liberté totale sur le contenu, le rythme, les formats et le site. **Toute dépense d'argent demande la validation d'Alex.** Tout changement de stratégie majeur (budget, audience, nouveau canal payant) aussi.

## Routine quotidienne

| Heure (Québec) | Où | Quoi |
| --- | --- | --- |
| 7 h 07 | Nuage | Vérifier éclaireur + mises à jour, build, préparer le pack du matin (posts FB/IG/TikTok, image, réel avec musique) |
| 8 h 30 environ | Ordinateur d'Alex (Chrome) | Publier le pack du matin sur Facebook, Instagram et TikTok |
| 16 h 40 environ | Nuage | Préparer le pack du soir |
| 18 h 30 environ | Ordinateur d'Alex (Chrome) | Publier le pack du soir |
| Dimanche 19 h | Nuage | Bilan de la semaine et recommandations |

## Où sont les fichiers d'un pack

- Textes prêts à publier : `suivi/posts/AAAA-MM-JJ-matin.md` et `suivi/posts/AAAA-MM-JJ-soir.md` (sections `## Facebook`, `## Premier commentaire Facebook`, `## Instagram`, `## TikTok`, et `Image:` / `Réel:` avec le nom du fichier).
- Images et réels : `docs/pack-du-jour/` (servis aussi sur https://rabaisflashqc.ca/pack-du-jour/NOM).
- Une fois publié, ajouter en bas du fichier de textes : `Publié : Facebook HH h MM, Instagram HH h MM, TikTok HH h MM` (ou la raison d'un échec), puis commit et push.

## Recettes de contenu viral

- Réel : 15 à 25 s, format 9:16, accroche texte dans les 2 premières secondes (« 5 deals qui partent vite », « Le deal de 14 h », « Sous 25 $ »), un deal par écran, musique. Gabarit : `reel-matin30-musique.py` + `music.py` (musique originale libre de droits). Sur Instagram et TikTok, ajouter un son tendance de la bibliothèque de l'app si possible, volume de notre piste à zéro.
- Séries fixes : « Le deal de 14 h », « Top 3 sous 25 $ », guides cadeaux par personne, compte à rebours du Black Friday (27 nov. 2026) et du Cyber Monday (30 nov.).
- Chaque post Facebook invite aussi à suivre Instagram @rabaisflashqc et TikTok (Instagram part de 1 abonné). Le site a déjà les boutons « J'aime la page » et « Suis-nous @rabaisflashqc ».
- Canaux gratuits : groupes Facebook québécois de rabais, seulement là où les règles du groupe permettent de partager, et jamais en rafale.

## Règles absolues

- Chaque post finit par : « En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. »
- Chaque deal affiche nouveau prix, % et ancien prix (champ `was`, sinon « environ ») et « prix observé le [date] » (avec l'heure quand elle est connue). Ne jamais inventer d'heure.
- Jamais de faux rabais, faux avis, faux manque (« plus que 2 en stock ») ni « partenaire officiel d'Amazon ». Léa (avatar) ne dit jamais avoir essayé un produit.
- Ne jamais mentionner RedFlagDeals (ni votes, ni communauté) sur le site, les posts ou les images. Les rapports de l'éclaireur restent dans `suivi/`.
- Tag `coupdecoeurqc-20` partout. Aucun lien de vitrine sur le site. Aucun lien Amazon dans les courriels ou infolettres. Les pubs pointent vers rabaisflashqc.ca, jamais directement vers Amazon.
- Pas de scraping d'Amazon, pas de photos tirées d'Amazon.
- Dans Chrome : aucune action de masse (abonnements, commentaires ou messages automatiques en rafale), ne jamais toucher aux paramètres de paiement, de pub ou de sécurité des comptes, ne jamais saisir de mot de passe. Si une connexion est demandée ou si Meta/TikTok affiche un avertissement, arrêter et prévenir Alex.
- Le NAS d'Alex est confidentiel. Ne jamais demander de clés API ou d'informations bancaires dans le clavardage.
- Si quelque chose bloque, l'expliquer clairement à Alex au lieu de s'arrêter en silence.
