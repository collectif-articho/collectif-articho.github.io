# collectif-articho-v2 : contexte projet

Refonte du **mécanisme de mise à jour** du site vitrine du collectif ARTI/CHÔ
(`collectifarticho.com`), une SCOP d'artisan·es designers constructeur·ices. Le but
n'est pas de refaire le site : c'est de permettre aux membres de le mettre à jour
**seul·es**, sans passer par Louis, en gardant le rendu actuel.

Ce dossier est **autonome** : tout le contexte utile est écrit ici, sans supposer
de mémoire d'une session précédente. Les besoins, les options étudiées, la décision
et le plan d'implémentation sont dans `ROADMAP.md`. Ce qui est fait part dans
`CHANGELOG.md`.

## Conventions de rédaction

**Ne pas utiliser le tiret cadratin (`—`)**, ni dans les fichiers, ni dans les
messages de commit, ni dans les réponses. C'est un marqueur de texte écrit par une
IA et ça agace les gens qui lisent. Reformuler la phrase (deux-points, virgule,
parenthèse ou point) plutôt que de substituer un autre signe. Le demi-cadratin
(`–`) et le trait d'union sont libres.

Tout est rédigé en français. Quand un arbitrage revient à Louis, exposer les options
en prose avec une recommandation claire, pas sous forme de questions à choix figés.

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

## Hébergement et comptes

| | |
|---|---|
| hébergeur | **GitHub Pages**, gratuit, à conserver |
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
- **Le style ne se touche pas sans Louis.** Claude voit mal un rendu et gère mal
  les retouches fines de CSS ; Louis l'a constaté et ne compte que modestement sur
  les captures d'écran automatiques (Chromium headless et ImageMagick, lentes et peu
  fiables pour du réglage précis). Règle : **toute modification de style est
  d'abord proposée à Louis en prose** (quoi, où, pourquoi, effet attendu), et c'est
  lui qui valide ou fait. Le vrai garde-fou est l'**égalité du HTML produit** avec
  l'ancien site : tant qu'elle tient et que le CSS est recopié tel quel, le rendu
  est identique par construction. Les captures ne servent qu'à un contrôle
  ponctuel, jamais à piloter un réglage.
- **Le contenu appartient à la SCOP.** Il doit rester sous forme de fichiers
  lisibles (Markdown, YAML, images) dans le dépôt, sans base de données ni format
  propriétaire, pour qu'on puisse changer d'outil d'édition sans rien perdre.
- **Aucune ressaisie.** Le contenu existant est migré par script depuis
  `../collectif-articho/drive/`.
- **Commits** en français, message au présent, sans cadratin.

## Outils disponibles sur le poste de Louis (vérifié le 2026-09-24)

`Rscript`, `python3`, `node`, `chromium` (snap, utilisable en headless), ImageMagick
(`compare`, `convert`), `dig`. **Hugo n'est pas installé.** Pas de `whois`, pas de
Playwright.
