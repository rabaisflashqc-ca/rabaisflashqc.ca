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

## Top 5 du site

- Le Top 5 de l'accueil est recalculé à chaque build, sans verrou (demande d'Alex du 2 nov.) : dès qu'un meilleur deal plus récent arrive, il entre. Source : deals de moins de 12 h (éclaireur et Keepa dans Chrome). Classement `_score()` dans build.py : % de rabais + petit bonus de votes (10 max) − 1 point par heure depuis la lecture du prix, un deal par catégorie d'abord. S'il y a moins de 3 deals frais, le site revient au Top 5 du catalogue.
- L'éclaireur roule aussi juste avant le pack du matin et la publication du soir.
- Vérité des prix : un deal repéré affiche « prix repéré le [date de publication du deal] », jamais l'heure du scan comme si le prix avait été vérifié. Les fils où une des 5 dernières réponses parle de deal mort ou de prix remonté sont écartés. Les prix du catalogue de plus de 3 jours sont cachés. Aucun compte à rebours inventé.
- Prix du jour (demande impérative d'Alex) : source = Keepa (keepa.py, workflow keepa.yml chaque heure, secret KEEPA_KEY). Keepa fournit les deals du jour d'amazon.ca et vérifie tous les prix affichés. Dès qu'une vérification de moins de 36 h existe, le site ne garde que les deals vérifiés; les deals restent au maximum 7 jours. Budget : forfait Starter, environ 10 % des jetons utilisés.
- Plan B gratuit (à l'essai, idée d'Alex du 2 nov.) : tant qu'aucune clé d'API (Keepa ou Logimu) n'existe, une session Cowork sur l'ordi d'Alex, avec Claude dans Chrome, fait une passe par jour dans Keepa Affaires (keepa.com/#!deals, compte d'Alex déjà connecté, jamais de mot de passe) et écrit les meilleurs deals dans suivi/deals_chrome.json (format de rfd.json, avec img_url : voir Photos). Cible : 30 à 45 deals de qualité par passe (marques connues, familles du Québec, Fêtes), cat parmi beaute, maison, tech, enfants, jouets, animaux, plein-air, homme, femme (jouets va sur la page Enfants, homme et femme sur Mode). Éviter les mots du filtre hors saison (piscine, pool…) dans les titres. Accueil et pages de catégorie trient tous par `_score()` (meilleur et plus récent). Une seule passe, pas de lecture massive. Les prix des deals affichés se revérifient sur les fiches Keepa, pas sur Amazon. Les trouvailles qu'Alex envoie (liens et captures) passent en priorité.
- Photos : l'éclaireur copie la photo principale de chaque deal dans docs/img/p/, mais elle n'apparaît que si son ASIN est dans suivi/photos.json « ok ». À chaque pack, regarde les nouvelles photos (Read) et classe-les : ok = vraie photo du produit, non = capture d'écran, graphique, mème ou visuel publicitaire (supprime alors le fichier).
- Photos des deals Keepa (décision d'Alex du 2 nov. : « plus vendeur ») : champ img_url = https://images-na.ssl-images-amazon.com/images/P/ASIN.01.L.jpg, affiché en lien direct depuis Amazon, jamais téléchargé. Tester chaque image dans Chrome (une image 1x1 = pas de photo : ne pas mettre img_url) et vérifier à l'oeil sur une planche que c'est le bon produit.
- Photos du catalogue (produits ajoutés à data.json) : trouve une photo officielle sur le site de la marque ou d'un grand détaillant (jamais Amazon), ajoute l'URL dans suivi/photos_sources.json, lance le workflow photos.yml, vérifie la photo à l'oeil puis ajoute l'ASIN à suivi/photos.json « ok ».
- Les packs pour les réseaux reprennent la même règle : « prix repéré le [date] ».

## Plan pour battre les grosses pages de deals (nov.-déc. 2026)

- Ton : énergique, complice, québécois. Moins d'avertissements, plus d'émotion. Les prix restent datés en petit (« prix du 29 oct. ») : Amazon l'exige pour les prix qui ne sont pas mis à jour en continu, sinon le compte Associés est à risque.
- Site : boutons « Voir le deal 👉 », Top 5 avec photos en haut, nouveau Top matin et soir pour donner une raison de revenir.
- Réseaux, chaque jour : 1 réel (accroche choc dans la 1re seconde : le plus gros % ou le plus petit prix), 1 carrousel ou image « Top 5 », 1 story avec sondage (« Tu le prends? Oui / Non »). Séries fixes : « Le deal à moins de 20 $ », « Cadeau pour… (maman, ado, chum) », compte à rebours Vendredi fou (27 nov.).
- Engagement : toujours une question en fin de post (« Lequel tu prends? 1, 2 ou 3? »), répondre à chaque commentaire, inviter à identifier quelqu'un.
- Communauté : pas de groupe Facebook (décision d'Alex, 1er nov.). On mise sur la page, Instagram, TikTok et le site.
- Objectif de commissions : 500 $ en décembre demande environ 12 000 $ de ventes (à environ 4 % de commission), soit autour de 4 000 clics vers Amazon dans le mois. 2 000 $ demande environ 4 fois plus. Suivre clics et ventes chaque dimanche dans le bilan.

## Règles absolues

- Chaque post finit par : « En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. »
- Chaque deal affiche nouveau prix, % et ancien prix (champ `was`, sinon « environ ») et « prix observé le [date] » (avec l'heure quand elle est connue). Ne jamais inventer d'heure.
- Jamais de faux rabais, faux avis, faux manque (« plus que 2 en stock ») ni « partenaire officiel d'Amazon ». Léa (avatar) ne dit jamais avoir essayé un produit.
- Ne jamais mentionner RedFlagDeals (ni votes, ni communauté) sur le site, les posts ou les images. Les rapports de l'éclaireur restent dans `suivi/`.
- Tag `coupdecoeurqc-20` partout. Aucun lien de vitrine sur le site. Aucun lien Amazon dans les courriels ou infolettres. Les pubs pointent vers rabaisflashqc.ca, jamais directement vers Amazon.
- Pas de scraping d'Amazon. Photos Amazon : seulement en lien direct (img_url), jamais copiées sur notre serveur (décision d'Alex du 2 nov., il assume le risque pour le compte Associés).
- Dans Chrome : aucune action de masse (abonnements, commentaires ou messages automatiques en rafale), ne jamais toucher aux paramètres de paiement, de pub ou de sécurité des comptes, ne jamais saisir de mot de passe. Si une connexion est demandée ou si Meta/TikTok affiche un avertissement, arrêter et prévenir Alex.
- Le NAS d'Alex est confidentiel. Ne jamais demander de clés API ou d'informations bancaires dans le clavardage.
- Si quelque chose bloque, l'expliquer clairement à Alex au lieu de s'arrêter en silence.
