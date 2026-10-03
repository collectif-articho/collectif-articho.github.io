# Journal des modifications

Du plus récent au plus ancien. Ce qui reste à faire est dans `ROADMAP.md`.

## v0.5 (en cours), 2026-10-03

Étape 4, finitions avant la bascule. Arbitrages de Lou consignés en D15 à D19
(`ROADMAP.md`) : bascule sans démonstration préalable, retour du fond de carte
CARTO, guide en fiches PDF, jeton sans expiration ; `srcset` et prix des meubles
abandonnés.

- **Page 404** (`layouts/404.html`), servie par GitHub Pages pour toute adresse
  inconnue : artichaut et liens vers l'accueil, les projets et le contact, dans
  le style des offres de l'accueil. Le gabarit commun gagne un bloc `title`.
- **CSS rangé**, rendu inchangé : en-tête de commentaire par feuille (ce qu'elle
  stylise, quels gabarits la chargent) et sections. Retirés : règles sans élément
  dans aucune page (`.sep`, `.notif`, `.title`, `.overlay h1`,
  `.material-icons`, `-round`, `#header_tab_projets:hover`, l'élément `it` des
  partenaires), préfixes `-webkit-`/`-moz-`/`-ms-`/`-o-` des rotations de
  l'accueil, déclarations écrasées dans la même règle, `background-color: none`
  (invalide), blocs en commentaire et `@media` vide. Vérifié par un diff des
  déclarations et par 20 captures (10 pages, ordinateur et téléphone) identiques
  au pixel avant et après.
- **Mentions légales** : l'hébergeur est GitHub, Inc. (et non « le serveur de
  Louis Héraut ») ; le directeur de publication passe dans sa propre section. Le
  reste attend les réponses de la SCOP (Q3).
- **Fiche de bascule** `docs/bascule.md` : qui fait quoi, clic par clic, retour
  en arrière. Trouvé en la préparant : `www.collectifarticho.com` pointe vers
  `lou-heraut.github.io` (à tester après la bascule, voir étape 5) ; le fichier
  `CNAME` est inutile avec une publication par Actions.
- Constaté : sans clé, CARTO ne sert plus qu'une tuile « API KEY REQUIRED » ;
  clé gratuite demandée par Lou (D16).
- **Écran de connexion du CMS** : seule la connexion par jeton est proposée
  (`auth_methods: [token]`) ; le bouton « Se connecter avec GitHub » qu'on
  voyait jusque-là ne pouvait pas marcher sans service d'authentification.
  Artichaut du collectif et titre « Site d'ARTI/CHÔ » à la place du logo et du
  nom de Sveltia. Aides des champs Photos alignées sur l'interface réelle
  (flèches ↑ ↓, pas de glisser).
- **Enregistrement depuis le CMS vérifié** sans jeton, avec le dépôt de test
  intégré à Sveltia (`backend: test-repo`, rempli avec nos fichiers dans le
  navigateur) : chaque page fixe et une fiche enregistrées, puis le site
  construit avec les fichiers réécrits par Sveltia. **HTML identique**, fichier
  pour fichier. Sveltia reformate le YAML (ordre des champs, guillemets, `|-`,
  `_italique_`, `lien: ''` pour un lien vide) sans effet sur le rendu ; il garde
  `cascade`, `url` et `layout`. L'accueil, les textes de la Ligne de mobilier et
  les mentions légales sont repris dans ce format : sans cela, le bouton
  « Enregistrer » y était actif dès l'ouverture.
- **Guide des membres** (D17), `docs/guide/` : une affiche A3 paysage (vue
  d'ensemble : l'adresse, le circuit, ce qui se fait dans le CMS et ce qui ne
  s'y fait pas) et trois fiches A4 paysage (le jeton et comment en refaire un,
  ajouter un projet en huit étapes, modifier, supprimer, réparer). Charte du
  site, captures de la vraie interface (dépôt de test de Sveltia) avec repères
  numérotés, PDF imprimé par chromium (`guide-du-site.pdf`, moins de 1 Mo).
  Remplace `docs/mode-emploi.md` et son PDF, retirés pour ne pas avoir deux
  documents qui divergent. Vérifié en passant : l'interface de Sveltia marche
  sur téléphone (le bouton « Nouveau » y devient un crayon rond).
- **Guide validé par Lou** (« c'est parfait ») ; seule demande : « Lou » et non
  « Louis », corrigé dans le guide (PDF réimprimé), dans toute la doc et dans
  l'aide du formulaire Contact. « Louis » ne reste que dans les citations de
  l'ancien site (mentions légales) et pour un partenaire cité dans une fiche ;
  les diapositives archivées de la présentation sont laissées telles quelles.
- **Mise à plat de la doc pour une reprise propre** : bandeau de `ROADMAP.md`
  (ce qu'on attend, ce que fait Claude à la reprise) ; étape 5 : Lou fait la
  bascule lui-même avec les identifiants de la SCOP ; renvois à l'ancien mode
  d'emploi et à une « étape 7 » corrigés, D10 complétée, Q3 explique SCOP et
  SARL. `docs/bascule.md` : double authentification, fenêtre privée, liste
  « Après » renumérotée. `CLAUDE.md` : prénom, ligne `www` du DNS, jeton sans
  expiration, outils vérifiés, pièges « Sveltia reformate » et « Tester le CMS
  sans jeton ni commit » (la méthode n'existait jusque-là que dans des scripts de
  session).

## v0.5 (suite), 2026-09-26

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
  jeton). Captures d'écran à ajouter après le test de Lou.
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
  Lou sur l'essai : champs d'information nommés avec exemples, aide sous chaque
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
- Second essai de CMS (Q2), avec l'accord de Lou : Sveltia CMS 0.221.1 servi
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
  pendant l'essai et une section « Travailler avec Lou ». Q2 détaillée dans
  `ROADMAP.md` avec le constat complet du test de Pages CMS et le second essai
  prêt à dérouler.

## v0.1 (suite), 2026-09-25

- Compte GitHub `collectif-articho` et dépôt `collectif-articho.github.io` créés
  par la SCOP ; Pages sur « GitHub Actions », Pages CMS installé, Lou
  collaborateur.
- Essai Hugo : fiche du Lopin aux mêmes URL que l'ancien site, gabarit repris de
  `default_projet.html`, CSS et polices recopiés tels quels, trois photos
  plafonnées à 3 000 px (7,1 Mo devenus 2,2 Mo ; servies à environ 700 Ko après
  redimensionnement par Hugo, masters non publiés). Workflow de publication,
  Hugo 0.166.0 épinglé. Publié et vérifié en ligne.
- Écart constaté : `uglyURLs` ne s'applique pas aux sections
  (`amenagements/index.html` au lieu de `amenagements.html`), à traiter à
  l'étape 1.
- Test de Pages CMS par Lou avec son compte collaborateur : l'envoi d'une
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
  `collectif-articho` avec dépôt `website` et Lou collaborateur, Pages CMS,
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
