# Tâche « Rabais Flash QC : prix du jour dans Chrome »

À créer dans l'app Claude sur l'ordinateur d'Alex (Cowork, avec Claude in Chrome), en tâche planifiée tous les jours vers 6 h 45 et 16 h 15, avec « Exiger cet ordinateur » activé. Copier le texte ci-dessous comme consigne.

---

Tu travailles pour Alex, qui gère Rabais Flash QC (site rabaisflashqc.ca, tag Amazon Associés coupdecoeurqc-20). Tu roules sur son ordinateur avec Chrome (Claude in Chrome). Réponds en français québécois, sans tirets longs.

BUT : que chaque prix du site soit celui du jour, pour garder la confiance des abonnés.

1. Lis la liste des produits affichés sur le site : https://raw.githubusercontent.com/rabaisflashqc-ca/rabaisflashqc.ca/main/suivi/a_verifier.json
2. Pour chaque produit, ouvre https://www.amazon.ca/dp/ASIN?tag=coupdecoeurqc-20 dans Chrome, un onglet à la fois, une seule visite par produit, au rythme d'une personne. Note : le prix affiché maintenant (price), le prix barré ou « Prix courant » s'il y en a un (was, sinon null), et si le produit est disponible (dispo). Ne télécharge aucune image.
3. Va sur https://www.amazon.ca/deals (Offres du jour) et choisis jusqu'à 20 offres qui collent à notre audience (Québécois de 25 à 55 ans : maison, cuisine, beauté, enfants, cadeaux, hiver, tech grand public), avec au moins 20 % de rabais affiché. Pour chacune, ouvre la fiche et note l'ASIN, un titre court en français, price, was, le % de rabais et une catégorie parmi : maison, beaute, enfants, tech, mode, animaux, plein-air, epicerie.
4. Écris dans le dépôt GitHub rabaisflashqc-ca/rabaisflashqc.ca (branche main), avec les outils GitHub disponibles :
   - suivi/prix_verifies.json : {"ASIN": {"price": 25.99, "was": 35.99, "dispo": true, "seen": "AAAA-MM-JJTHH:MM-05:00"}, ...} pour tous les produits vérifiés à l'étape 2 et 3 (heure réelle de la vérification, heure du Québec).
   - suivi/deals_chrome.json : [{"asin": "...", "title": "...", "cat": "...", "price": 0, "was": 0, "pct": 0, "posted": "<heure de la vérification>", "seen": "<même heure>", "until": "<même heure + 24 h>", "votes": null}, ...] pour les offres de l'étape 3.
5. Lance le workflow eclaireur.yml (workflow_dispatch, ref main) pour reconstruire le site.
6. Envoie à Alex une ligne : combien de prix vérifiés, combien de deals du jour ajoutés, combien de produits retirés (prix changé, plus de rabais ou indisponible).

LIMITES : aucune action de masse, aucun achat, aucun ajout au panier, ne touche jamais aux paramètres du compte Amazon ni aux paiements, ne saisis jamais de mot de passe. Si Amazon demande une connexion, un captcha ou affiche un avertissement, arrête-toi et préviens Alex.
