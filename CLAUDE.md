# collectif-articho-v2 : contexte projet

Refonte du **mécanisme de mise à jour** du site vitrine du collectif ARTI/CHÔ
(`collectifarticho.com`), une SCOP d'artisan·es designers constructeur·ices. Le but
n'est pas de refaire le site : c'est de permettre aux membres de le mettre à jour
**seul·es**, sans passer par Louis, en gardant le rendu actuel.

Ce dossier est **autonome** : tout le contexte utile est écrit ici, sans supposer
de mémoire d'une session précédente. Les besoins, les décisions et le plan d'attaque
sont dans `ROADMAP.md`. Ce qui est fait part dans `CHANGELOG.md`.

## Reprendre le travail

1. Lire le bandeau **État** en tête de `ROADMAP.md` : il dit où on en est et quelle
   est la prochaine action.
2. Lire le journal des décisions (`ROADMAP.md`, § 2). Ne pas rouvrir une décision
   sans élément nouveau.
3. Lire les dernières entrées de `CHANGELOG.md` et `git log --oneline | head`.
4. Travailler étape par étape du plan d'attaque (§ 4) ; chaque étape a un critère
   de fin, ne pas passer à la suivante tant qu'il n'est pas atteint.
5. Lire plus bas **Travailler avec Louis** et **Le nouveau site** : ce qui a été
   appris en séance et n'est pas déductible du code.

**Tenir la traçabilité à chaque étape franchie**, dans le même commit que le code :
entrée au `CHANGELOG.md` (quoi, pourquoi, écarts constatés), bandeau État de
`ROADMAP.md` mis à jour, nouvelle décision ajoutée au § 2 si un arbitrage a été
fait avec Louis. Un fait qui n'est écrit que dans une conversation est perdu.

## Conventions de rédaction

**Ne pas utiliser le tiret cadratin (`—`)**, ni dans les fichiers, ni dans les
messages de commit, ni dans les réponses. C'est un marqueur de texte écrit par une
IA et ça agace les gens qui lisent. Reformuler la phrase (deux-points, virgule,
parenthèse ou point) plutôt que de substituer un autre signe. Le demi-cadratin
(`–`) et le trait d'union sont libres.

Tout est rédigé en français.

## Relation avec le site actuel

Le site en production vit dans le dossier voisin **`../collectif-articho/`**
(dépôt `git@github.com:lou-heraut/collectif-articho.git`, branche `main`, publié
par GitHub Pages). **Ne pas modifier ce dossier** depuis ici : il sert de
**référence**, à la fois comme source du contenu à migrer et comme étalon du rendu
à reproduire. Sa propre documentation (`CLAUDE.md`, `ROADMAP.md`, `CHANGELOG.md`)
décrit en détail son fonctionnement ; l'essentiel est résumé ci-dessous.

### Comment fonctionne l'ancien site

```
../collectif-articho/drive/<NN_Onglet>/<NN_SousOnglet>/<NN_Projet>/
    titre.txt  soustitre.txt  info.txt  text.txt  1.jpg 2.jpg …
            │
            ▼  Rscript make_projet.R  (lancé à la main par Louis)
    pages/<onglet>/<sous-onglet>/<slug>.html     page de détail par projet
    pages/<onglet>/<sous-onglet>.html            listing en vignettes
    pages/projets.html                           listing de tout l'onglet Projets
    resources/images/<onglet>/<sous-onglet>/<slug>/*   copie des photos
```

- `drive/` est la copie d'un dossier Google Drive de l'association, synchronisé
  depuis un Mac. Louis le recopie à la main dans le dépôt, lance le script, relit,
  pousse. **C'est ce circuit que la v2 remplace.**
- 3 onglets, 8 sous-onglets, 59 dossiers : 53 pages projet, plus 5 meubles de la
  « Ligne de mobilier » rendus sur **une seule page** en carrousel (prix,
  modalités, dimensions, matériaux), sans page de détail par meuble.
- `info.txt` est une suite de lignes `clé : valeur`. Pour les meubles, certaines
  valeurs sont des listes séparées par ` - ` (`Dimensions : - Longueur 100 cm -
  Largeur 60 cm`). `text.txt` donne un `<p>` par ligne non vide.
- Gabarits `pages/default_projet.html`, `default_projets.html`,
  `default_mobiliers.html`, remplis par `gsub()` sur des jetons `$NOM$`.
- **Pages écrites à la main** : `index.html` (diaporama de 9 photos, textes,
  articles de presse, logos des soutiens), `pages/a-propos.html`, `contact.html`,
  `notre-offre.html`, `mentions-legales.html`, `conditions-generales.html`,
  `ateliers.html`, `mobiliers.html`.
- **Navigation injectée côté navigateur** : `resources/js/script.js` charge
  `components/header.html`, `footer.html` et les `*_tab.html` par `fetch()`, puis
  `checkURL()` surligne l'onglet actif via une chaîne de `else if` sur des slugs en
  dur. Dépendances CDN : jQuery 3.7.1 et Material Icons (Google Fonts).
- CSS : 7 feuilles dans `resources/css/` (environ 1 650 lignes), polices Faune en
  local dans `resources/fonts/`. **Le style est très travaillé et ajusté à la
  main, c'est un actif à préserver.**

### Pièges connus, à ne pas redécouvrir

- **Unicode mélangé.** Le Drive macOS livre les accents en NFD (décomposés) pour
  23 noms de dossiers sur 25, et en NFC ailleurs. Tout slug dérivé d'un texte doit
  retirer les marques combinantes (`[̀-ͯ]`) avant translittération.
- **Espaces parasites** en fin de `titre.txt` (4 cas). Toujours `trim`.
- **Noms de fichiers d'images** avec espaces, accents ou `©` (15 cas). La migration
  est le bon moment pour les assainir.
- **Photos lourdes** : 110 fichiers au-dessus de 5 Mo, jusqu'à 20,7 Mo, servies
  telles quelles, y compris comme vignettes. `resources/images` pèse 1,4 Go.
- **URL du QR code imprimé** : `/pages/mobiliers/agencements/tpmobile.html` doit
  toujours rediriger vers la page du TPMob
  (`/pages/mobiliers/agencements/tpmob-theatre-public-mobile.html`). Ne jamais
  casser cette URL.
- **Fichiers au niveau onglet utilisés par les pages manuelles** :
  `resources/images/{mobiliers,ateliers}/{1,2}.jpg`,
  `resources/images/mobiliers/ligne-de-mobilier-intro.jpg`,
  `resources/images/ateliers/plaquette_ARTICHO.pdf`.

## Charte graphique

Relevée dans `resources/css/` de l'ancien site, reprise pour la présentation à la
SCOP, à réutiliser pour tout document destiné aux membres (mode d'emploi…).

| rôle | valeur |
|---|---|
| bleu (titres, fonds forts) | `#213589` |
| orange (accents) | `#FEC37E`, `#FEA945` |
| crème (fond clair) | `#FFF7ED` |
| quasi-noir (texte) | `#151206` |
| polices | Faune, en local : `faune.display-black.otf` (titres), `faune.text-regular.otf`, `faune.text-bold.otf`, plus italiques et thin |

## Hébergement et comptes

| | |
|---|---|
| hébergeur | **GitHub Pages**, gratuit, à conserver |
| ancien site | dépôt `lou-heraut/collectif-articho` (compte perso de Louis), sert `collectifarticho.com` jusqu'à la bascule |
| nouveau site | compte utilisateur **`collectif-articho`** tenu par la SCOP (créé le 2026-09-25, e-mail `contact@collectifarticho.com`, identifiants gardés par la SCOP) ; dépôt public **`collectif-articho/collectif-articho.github.io`**, branche `main`, servi à la racine de https://collectif-articho.github.io/ (D3, D7) ; Pages réglé sur « GitHub Actions » ; `lou-heraut` collaborateur (peut pousser, pas toucher aux réglages) ; CMS : **Sveltia**, page `/admin/` du site, connexion par jeton GitHub (D12) ; l'application Pages CMS, essayée puis écartée, reste à désinstaller côté SCOP |
| remote local | `origin` = `git@github.com:collectif-articho/collectif-articho.github.io.git` |
| domaine | `collectifarticho.com`, enregistré chez Google Domains, **repris par Squarespace** ; payé par la SCOP |
| DNS | serveurs `ns-cloud-d{1..4}.googledomains.com` ; A vers `185.199.10{8,9,10,11}.153` (GitHub Pages) |
| mail | MX vers `aspmx.l.google.com` : **Google Workspace**, adresse de la SCOP sur ce domaine |

GitHub Pages ne fait ni réécriture ni redirection HTTP : une redirection est un
fichier HTML (`meta refresh` plus `link canonical`). Il sert les URL sans extension
(`/pages/contact` rend 200).

Le **domaine et le mail** sont un sujet séparé, hors du périmètre de cette refonte
(voir `ROADMAP.md`, chantier annexe). Ne pas toucher au DNS sans décision explicite :
une erreur sur les MX coupe le mail de la SCOP.

## Principes de travail

- **Sobriété.** Pas d'usine à gaz. Le moins de dépendances possible, chacune
  justifiée, versions épinglées. Le site doit pouvoir être repris dans cinq ans par
  quelqu'un qui ne connaît pas l'histoire.
- **Rendu conservé.** Le CSS de l'ancien site est repris tel quel, chemins
  absolus compris. On vérifie **le rendu, pas le HTML** : pages types à l'œil côte
  à côte avec l'ancien site, plus aucun lien mort (D9). L'identité du HTML au
  caractère près n'est pas un objectif.
- **La SCOP ne touche qu'à `content/` et `assets/photos/`.** Tout le reste (gabarits, CSS, config) est
  du code. Un champ saisi par un membre ne doit jamais pouvoir casser la mise en
  page.
- **Le contenu appartient à la SCOP.** Il doit rester sous forme de fichiers
  lisibles (Markdown, YAML, images) dans le dépôt, sans base de données ni format
  propriétaire, pour qu'on puisse changer d'outil d'édition sans rien perdre.
- **Outillage minimal** (D9) : Python **sans dépendance** (bibliothèque standard),
  ImageMagick pour les photos, Hugo épinglé dans le workflow et n'importe quel Hugo
  récent en local. Ni venv, ni script d'installation. **Pas de R.**
- **Photos : jamais d'original perdu.** Le dépôt ne garde que des masters
  plafonnés (D6) ; les originaux vivent dans le Drive et l'ancien dépôt archivé.
- **Aucune ressaisie.** Le contenu existant est migré par script depuis
  `../collectif-articho/drive/`.
- **Commits** en français, message au présent, sans cadratin.

## Outils disponibles sur le poste de Louis (vérifié le 2026-09-26)

`Rscript`, `python3`, `node`, `chromium` (snap, utilisable en headless), ImageMagick
(`mogrify`, `identify`, `compare`), `dig`, `gh` (CLI GitHub). Pas de `whois`, pas de
Playwright.

**Hugo n'est pas installé sur le système**, et c'est voulu (D9). Pour construire en
local, télécharger dans le dossier temporaire de la session la même version que le
workflow (`HUGO_VERSION` dans `.github/workflows/publier.yml`), somme de contrôle
vérifiée :

```sh
V=0.166.0   # celle du workflow
curl -sLO https://github.com/gohugoio/hugo/releases/download/v$V/hugo_extended_${V}_linux-amd64.tar.gz
curl -sL https://github.com/gohugoio/hugo/releases/download/v$V/hugo_${V}_checksums.txt \
  | grep "hugo_extended_${V}_linux-amd64.tar.gz" | sha256sum -c
tar -xzf hugo_extended_${V}_linux-amd64.tar.gz hugo
./hugo --gc -s <chemin du dépôt>     # construit dans public/
./hugo server -s <chemin du dépôt>   # aperçu sur http://localhost:1313
```

## Travailler avec Louis

Appris en séance, à respecter sans le lui redemander :

- **Pas de widget de questions à choix** (`AskUserQuestion`) : exposer les options
  en texte, avec une recommandation, et le laisser répondre en prose. Tableaux et
  schémas ASCII bienvenus.
- **Commiter et pousser ce dépôt au fil de l'eau** sans demander, la doc
  (`ROADMAP.md`, `CHANGELOG.md`) dans le même commit. Le dépôt est public : signaler
  seulement ce qui serait risqué à publier.
- Il tient au **process ROADMAP / CHANGELOG versionné / CLAUDE.md** : c'est ce qui
  permet de reprendre. Ne pas proposer de l'alléger.
- Ce qui l'agace, c'est la **sur-ingénierie technique** (exemple vécu : vouloir
  comparer le HTML au caractère près avec l'ancien site, avec normalisation des
  chemins). Chercher la solution la plus simple qui tient, et le dire quand un
  choix du plan en ajoute sans nécessité.
- Arbitrages à ne pas rouvrir : **compte unique** de la SCOP (D3, il sait que les
  conditions de GitHub interdisent le partage d'identifiant et l'assume) ; **accueil
  éditable** gardé dans le périmètre avant la démonstration à la SCOP (c'est
  l'argument contre un retour de WordPress).
- Les réglages sur le compte de la SCOP se font **en séance avec un membre** :
  préparer des consignes pas à pas, clic par clic, et dire ce qui peut être ignoré.
- Louis peut faire les tests d'édition avec son propre compte `lou-heraut`
  (collaborateur), sans attendre la SCOP.

## Le nouveau site : état technique et pièges constatés

Ce qui existe au 2026-09-26 (`v0.4`) :

```
hugo.toml                  URL (/pages/…, uglyURLs), MENU PRINCIPAL (en-tête et
                             barres d'onglets en sont tirés), hardWraps
content/<onglet>/<rubrique>/
    _index.md              la rubrique : titre, ordre, url: /pages/….html
    <slug>.md              une fiche (format : ROADMAP, étape 2 ; champs D13)
content/mobiliers/ligne-de-mobilier/_index.md
                           textes de la page et `cascade` : pas de page par meuble
content/_index.md          accueil : tous ses textes et listes en champs (D5)
content/contact.md  notre-offre.md  a-propos.md  mentions-legales.md
    conditions-generales.md        pages fixes : `url:` et `layout:` en tête
content/{mobiliers,ateliers}/_index.md   pages d'onglet : `cartes`
assets/photos/<onglet>/<rubrique>/<slug>/   photos d'une fiche (D8)
assets/photos/pages/       photos des pages fixes (accueil, onglets)
static/documents/          plaquette PDF
layouts/baseof.html        squelette : <head>, #header, #footer
layouts/page.html          fiche ; section.html : listings ; home.html : accueil
layouts/ligne-de-mobilier.html  onglet.html  offre.html  texte.html  contact.html
                           un gabarit par type de page fixe, choisi par `layout:`
layouts/_partials/         header, footer, tab_bar (menus), actif (onglet actif),
                           photo (redimensionne, erreur si absente), vignette
static/resources/          css, fonts, statics, js repris de l'ancien site
static/pages/…/tpmobile.html   redirection du QR code (D14)
static/admin/              Sveltia CMS : index.html (version épinglée), config.yml
migration/migrer.py        migration unique depuis ../collectif-articho (relançable)
outils/verifier.py         liens morts, pages et titres de l'ancien site absents
```

Pièges déjà rencontrés :

- **NFD du drive** : `cp "drive/01_Projets/01_Aménagements/…"` échoue parce que le
  `é` du disque est décomposé. Passer par `find`, ou `unicodedata` en Python.
- **Sections** : un `_index.md` est obligatoire par dossier, sinon Hugo ne voit
  pas la section et l'URL perd un niveau. `uglyURLs` ne s'y applique pas, d'où
  `url:` dans chaque `_index.md` (un permalink finissant par `.html` crée un
  dossier `amenagements.html/`).
- **`cascade`** s'applique aussi à la section elle-même : le `build: render:
  never` des meubles est limité par `target: kind: page`.
- **Une fiche ne contient que des champs décrits dans `static/admin/config.yml`**
  (D14) : un CMS peut retirer à l'enregistrement les champs inconnus. Tout champ
  ajouté aux gabarits s'ajoute aussi au formulaire, dans le même commit.
- `date` est réservé par Hugo (date de la page) : l'information « Date » est
  `date_projet`. `languageCode` est déprécié : `locale`.
- Les photos de `assets/` ne sont publiées **que dans les tailles demandées** par
  les gabarits, jamais le master. Le partial `photo.html` arrête la construction
  si une photo listée est absente.
- Le langage de gabarit de Hugo aplatit les `slice` imbriquées avec `append` :
  préférer une `slice` de `dict`.
- **`projets.css` ne se charge pas partout** : sa règle `p { max-width: 50vw }`
  change les paragraphes. Chaque gabarit déclare ses feuilles dans son bloc
  `head` ; l'accueil, le contact et les pages texte ne la chargent pas.
- Le Markdown produit `strong`/`em`, l'ancien HTML `b`/`i` : le CSS les traite
  ensemble (polices Faune Bold et Italic). Les blocs de texte Markdown sont en
  `display: contents`, pour que leurs enfants restent des enfants directs de
  `.container` (colonne flex centrée).
- **Sveltia conserve les champs qu'il ne connaît pas** à l'enregistrement
  (vérifié dans son code, `serialize.js`). Des champs de structure (`url`,
  `layout`, `cascade`) peuvent donc vivre à côté des champs éditables.
- Le workflow met en cache les images redimensionnées ; en local, le premier
  `hugo` complet prend environ 30 s, les suivants 3 s.
- **Captures d'écran** : `chromium` est un snap, il ne peut pas écrire dans
  `/tmp`. Écrire dans `~/snap/chromium/common/`, puis déplacer :

  ```sh
  chromium --headless=new --hide-scrollbars --virtual-time-budget=8000 \
    --window-size=1400,2000 --screenshot=$HOME/snap/chromium/common/x.png URL
  ```

  Servir l'ancien site (`python3 -m http.server 8001` dans `../collectif-articho`)
  et le nouveau (`python3 -m http.server 8002` dans `public/`) pour comparer.
  Relancer le second après un `rm -rf public`. L'accueil a des blocs en hauteur
  d'écran (`vh`) : une fenêtre très haute les étire au lieu de montrer le bas de
  page, et une ancre (`#…`) donne une capture blanche ; comparer alors le HTML
  normalisé de ces sections.
- `pkill -f motif` ou `pgrep -f motif` dans une commande Bash se trouvent
  eux-mêmes (le motif est dans la ligne de commande) : écrire `http.serve[r]`.

Vérifier une publication : le workflow dure moins d'une minute ; suivre avec
`gh run list -R collectif-articho/collectif-articho.github.io`, puis `curl -I`
sur les pages. Si le push est refusé (`fetch first`), c'est que le CMS a commité
entre-temps : `git pull --rebase`, puis lire ce qu'il a écrit.
