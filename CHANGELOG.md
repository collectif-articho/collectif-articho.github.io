# Journal des modifications

Du plus récent au plus ancien. Ce qui reste à faire est dans `ROADMAP.md`.

## 2026-09-25, revue du plan

- Revue du plan pour l'alléger, décisions D7 à D11 dans `ROADMAP.md` :
  - D7 : dépôt `collectif-articho.github.io`, publié à la racine, donc les chemins
    absolus de l'ancien site marchent tels quels. Supprime la réécriture des
    chemins par `relURL` et des `url()` du CSS. Compte unique de la SCOP confirmé.
  - D8 : photos dans `assets/photos/`, car Pages CMS ne sait pas écrire dans le
    dossier d'une fiche (vérifié dans sa doc).
  - D9 : vérification du rendu à l'œil et par liens morts, abandon de
    `compare_html.py` ; Python sans dépendance, ImageMagick, Hugo épinglé dans le
    workflow.
  - D10 : Pages CMS ne réduit pas les photos (vérifié), croissance du dépôt
    acceptée ; tranche Q1.
  - D11 : une version par étape, `v1.0` à la bascule.
- Plan réécrit en 7 étapes (0 à 6) : l'essai de bout en bout passe en premier,
  car il fixe le format de migration. Pages fixes éditables, accueil compris,
  gardées avant la démonstration à la SCOP. Stub du QR code par `aliases` Hugo.

## 2026-09-25, cadrage

- Décisions D1 à D6 consignées dans `ROADMAP.md` : option B (CMS git et Hugo),
  outillage en Python dans un venv et abandon de R, compte GitHub
  `collectif-articho` avec dépôt `website` et Louis collaborateur, Pages CMS,
  pages fixes en gabarit plus champs, photos plafonnées à 3 000 px (originaux
  conservés dans le Drive et l'ancien dépôt). Question ouverte Q1 : réduction des
  photos à l'envoi depuis le CMS.
- Plan d'attaque en 8 étapes à critères de fin ; inventaire des emplacements
  éditables des pages fixes ; points de contenu à signaler à la SCOP.
- Chemins du site relatifs à la `baseURL` (étape 3) : le site fonctionne à
  l'adresse provisoire de GitHub comme sur le domaine.
- `CLAUDE.md` : procédure de reprise, charte graphique. Présentation à la SCOP
  archivée dans `docs/presentation-scop/`.

## 2026-09-24

- Création du dossier. Cadrage écrit : besoins de la SCOP, explication des CMS,
  comparaison de cinq options (WordPress, CMS git avec Hugo, CMS à plat en PHP,
  Drive automatisé, constructeurs de sites), plan d'implémentation en six phases
  pour l'option recommandée, chantier annexe domaine et mail.
