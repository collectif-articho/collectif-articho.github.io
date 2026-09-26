# Journal des modifications

Du plus récent au plus ancien. Ce qui reste à faire est dans `ROADMAP.md`.

## v0.5 (en cours), 2026-09-26

Étape 4, formulaires du CMS et mode d'emploi.

- Collection Sveltia « Pages du site » : un formulaire par page fixe (accueil,
  contact, notre offre, onglets Mobiliers et Ateliers, textes de la Ligne de
  mobilier, pages texte), avec une aide sous les champs qui en ont besoin.
- Insertion d'images désactivée dans les textes Markdown (`editor_components:
  []`) : une image glissée dans un texte ne serait ni réduite ni rangée ; les
  photos passent par les champs Photos.
- Config chargée sans erreur par Sveltia (écran de connexion en local) ; les
  formulaires restent à essayer une fois connecté.
- `docs/mode-emploi.md` : une page pour les membres (connexion par jeton, ajouter
  une fiche, photos sur connexion lente, pages du site, erreurs, renouvellement du
  jeton). Captures d'écran à ajouter après le test de Louis.
- Passage de relais consigné : `ROADMAP.md` § 4 réécrit (étapes faites résumées,
  reste détaillé, à faire à la bascule), D14 complétée (Sveltia conserve les
  champs inconnus) ; `CLAUDE.md` gagne le format des contenus et les commandes
  courantes ; `migration/migrer.py` refuse désormais de tourner sans
  `--ecraser-le-contenu`, puisqu'il effacerait les modifications faites depuis
  le CMS.

## v0.4, 2026-09-26

Étape 3, pages fixes éditables (D5) : la mise en page reste dans les gabarits,
le contenu passe dans des fichiers de `content/`, transcrits une fois à la main
depuis le HTML de l'ancien site.

- **Accueil** (`content/_index.md`) : diaporama, titre et accroche, 4 valeurs,
  3 offres, trois blocs de texte en Markdown, photo d'accueil et d'équipe,
  presse, soutiens (dont les deux logos empilés), partenaires (un groupe = un
  texte, un nom par ligne, rôle entre parenthèses). Métadonnées reprises, image
  de partage en URL absolue.
- **Contact** : e-mail, réseaux, adresses. Le pied de page lit ses réseaux sur
  cette page (une seule source). Leaflet épinglé en 1.9.4.
- **Notre offre** : plaquette PDF (`static/documents/`) et texte.
- **Onglets Mobiliers et Ateliers** : cartes (titre, sous-titre, image, lien).
- **Pages texte** (À propos, Mentions légales, Conditions générales) : Markdown.
- Images des pages fixes dans `assets/photos/pages/` : 30 Mo au lieu d'environ
  85 (vignettes de presse de 3 040 px et 9 Mo ramenées à 1 200 px).
- `projets.css` n'est plus chargé partout : l'accueil, le contact et les pages
  texte ne le chargeaient pas, et sa règle `p { max-width: 50vw }` changeait
  leurs paragraphes.
- CSS : `strong`/`em` (produits par le Markdown) reçoivent les polices de `b`/`i`
  (Faune Bold et Italic), faute de quoi le gras était simulé ; blocs de texte en
  `display: contents` pour garder la disposition de `.container` ; phrase
  d'annonce de la liste de Notre offre alignée sur la liste.
- **Carte du contact réparée** : les fonds CARTO exigent désormais une clé d'API
  et l'ancien site n'affiche plus que « API KEY REQUIRED » (constaté en
  production). Fonds OpenStreetMap, sans clé ; rendu plus coloré qu'avant.
- Écarts voulus, relevés en comparant le HTML : noms d'images assainis, lien
  HORIZONS direct au lieu d'une redirection Google, logos de soutiens sans lien
  qui ne rouvrent plus l'accueil dans un onglet, apostrophes typographiques.
- Vérifié à l'œil (accueil, contact, notre offre, à propos, mentions légales,
  onglets) et par `outils/verifier.py` : aucun lien mort, toutes les pages de
  l'ancien site présentes.

## v0.3, 2026-09-26

Étape 2, migration du contenu, par `migration/migrer.py` (bibliothèque standard
et `mogrify`, relançable).

- 53 fiches projet et 5 meubles migrés depuis `../collectif-articho/drive/`. Les
  59 titres du drive sont présents sur le site, et chaque URL de l'ancien site a
  sa fiche (nom de fichier repris de `urls.tsv`, pas recalculé).
- 292 photos, plafonnées à 3 000 px (D6) : 398 Mo au lieu de 1,2 Go. L'ordre des
  photos, photo principale comprise, est relevé **dans les pages publiées** de
  l'ancien site plutôt que recalculé. Noms assainis (espaces, accents, `©`,
  majuscules), extensions `.jpeg` ramenées à `.jpg`.
- Informations en champs nommés (D13) ; variantes ramenées à leur champ :
  « Matériaux de réemploi » (2 fiches), « Matériaux neuf », « Localisations ».
- Textes : un paragraphe par ligne comme avant ; les lignes « - … » deviennent de
  vraies listes à puces ; les lignes « > … » sont échappées (affichées telles
  quelles, pas en citation) ; le lien HTML de la fiche TPMob devient un lien
  Markdown (Hugo retire le HTML brut).
- Prix des meubles **non migrés** : présents dans le drive (285 € HT, 350 €…),
  jamais affichés par l'ancien site (« Prix sur demande »). Voir ROADMAP, « À
  signaler à la SCOP ».
- Redirection du QR code : fichier fixe `static/pages/mobiliers/agencements/tpmobile.html`
  (D14), vérifié en local.
- Formulaires Sveltia pour les 8 rubriques au format D13, avec les retours de
  Louis sur l'essai : champs d'information nommés avec exemples, aide sous chaque
  champ, aperçu retiré. Nécessaire tout de suite : un CMS peut retirer à
  l'enregistrement les champs qu'il ne connaît pas.

## v0.2, 2026-09-26

Étape 1, squelette et gabarits.

- En-tête, pied de page et barres d'onglets en partials Hugo, tirés d'un seul
  menu déclaré dans `hugo.toml` : les slugs ne sont plus écrits qu'à un endroit
  (ancien P3.2). L'onglet actif est calculé à la construction : `checkURL()`,
  jQuery et les `fetch()` de `components/` disparaissent ; `script.js` ne garde
  que les menus déroulants et le survol des icônes.
- Gabarits : fiche (informations en champs nommés, D13), listing d'onglet et de
  rubrique, page Ligne de mobilier (carrousel sans points de navigation quand un
  meuble n'a qu'une photo, ancien P2.5 ; Material Icons chargé sur cette page
  seulement). Les meubles n'ont pas de page à eux (`cascade` limité aux pages).
- Mêmes URL : chaque rubrique fixe la sienne par `url:` dans son `_index.md`,
  puisque `uglyURLs` ne s'applique pas aux sections.
- Photos redimensionnées à la construction : 2 000 px pour les pages, 1 000 px
  pour les vignettes.
- Retouches CSS, les seules : listes du texte des fiches alignées sur les
  paragraphes (`projets.css`), marge du texte d'introduction de la Ligne de
  mobilier (`mobiliers.css`). Retour à la ligne saisi = retour à la ligne
  (`hardWraps`). Année du pied de page calculée.
- `outils/verifier.py` : liens internes morts, pages et titres de l'ancien site
  absents (D9).
- Vérifié à l'œil contre l'ancien site, captures côte à côte : fiche, listing
  « Tout », listing de rubrique, Ligne de mobilier, page courte avec pied de
  page, fiche sur téléphone (390 px). Identiques, sauf l'année et les listes.

## v0.1, 2026-09-26

- Étape 0 close : chaîne complète validée (Hugo, GitHub Actions, Sveltia CMS).
  Décisions D12 (Sveltia plutôt que Pages CMS) et D13 (informations d'une fiche
  en champs nommés). Ménage : `.pages.yml`, photo `3.jpeg` et fiche `test`
  retirés.
- Second essai de CMS (Q2), avec l'accord de Louis : Sveltia CMS 0.221.1 servi
  sous `/admin/` (`static/admin/`). Photos rangées par fiche grâce au
  `media_folder` de collection avec `{{filename}}`, réduites dans le navigateur
  en WebP 3 000 px avant l'envoi ; nom de fichier des nouvelles fiches en ASCII
  sans accents, figé à la création. Pages CMS reste branché pour comparer.
- Premier test de Sveltia depuis un train : échec d'enregistrement d'une photo de
  8,9 Mo pourtant réduite en WebP. Mesuré : l'API GraphQL de GitHub coupe les
  envois au-delà d'environ 5 s (HTTP 499), l'API REST non. Réduction abaissée de
  3 000 à 2 000 px (environ 1 Mo par photo). Test à refaire sur une connexion
  ordinaire.
- Second essai réussi : photo de téléphone de 8,9 Mo enregistrée depuis Sveltia
  (WebP 1 500 × 2 000, 1,3 Mo) dans le dossier de sa fiche, nouvelle fiche
  créée au format prévu, publiée en moins de 30 s.
- Passage de relais consigné : `CLAUDE.md` gagne l'état des comptes et du dépôt,
  la façon de construire en local sans installer Hugo, les pièges constatés
  pendant l'essai et une section « Travailler avec Louis ». Q2 détaillée dans
  `ROADMAP.md` avec le constat complet du test de Pages CMS et le second essai
  prêt à dérouler.

## v0.1 (suite), 2026-09-25

- Compte GitHub `collectif-articho` et dépôt `collectif-articho.github.io` créés
  par la SCOP ; Pages sur « GitHub Actions », Pages CMS installé, Louis
  collaborateur.
- Essai Hugo : fiche du Lopin aux mêmes URL que l'ancien site, gabarit repris de
  `default_projet.html`, CSS et polices recopiés tels quels, trois photos
  plafonnées à 3 000 px (7,1 Mo devenus 2,2 Mo ; servies à environ 700 Ko après
  redimensionnement par Hugo, masters non publiés). Workflow de publication,
  Hugo 0.166.0 épinglé. Publié et vérifié en ligne.
- Écart constaté : `uglyURLs` ne s'applique pas aux sections
  (`amenagements/index.html` au lieu de `amenagements.html`), à traiter à
  l'étape 1.
- Test de Pages CMS par Louis avec son compte collaborateur : l'envoi d'une
  photo lourde échoue en `413`. Cause : limite de 4,5 Mo par requête des
  fonctions Vercel qui hébergent Pages CMS. Question Q2 ouverte dans
  `ROADMAP.md` (passage à Sveltia CMS).

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
