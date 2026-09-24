# Feuille de route

Contexte technique dans `CLAUDE.md`. Ce qui est fait part dans `CHANGELOG.md`.

> **État au 2026-09-24** : cadrage écrit, **décision de la SCOP en attente** entre
> WordPress et la solution intermédiaire recommandée ici (option B). Rien n'est
> implémenté. Une présentation destinée aux membres compare les options.

---

# 1. Le besoin

## Pourquoi changer

Toute mise à jour du site passe aujourd'hui par Louis :

| étape | qui | ce qui bloque |
|---|---|---|
| saisie | la SCOP, fichiers `.txt` dans le Drive | format implicite, aucun retour en cas d'erreur, jugé trop compliqué |
| Drive vers dépôt | Louis, copie à la main | personne d'autre ne sait le faire |
| génération | Louis, `Rscript` sur son poste | R installé, script connu de lui seul |
| mise en ligne | Louis, `git push` | dépôt sur son compte GitHub personnel |
| pages fixes, navigation | Louis, HTML à la main | aucun membre ne fait de HTML ni de CSS |

Les membres ont proposé WordPress. Le rythme réel : environ **5 vagues de mises à
jour en deux ans** (historique git). L'outil sera donc ouvert deux ou trois fois par
an, par des gens qui auront oublié entre deux fois. Il doit être évident sans
formation.

## Cahier des besoins (validé par Louis le 2026-09-24)

| | besoin |
|---|---|
| B1 | Les membres **ajoutent, modifient, suppriment** projets, meubles et ateliers seul·es, sans compétence HTML ni CSS. Des formulaires plutôt que des fichiers ; du Markdown simple reste acceptable. |
| B2 | Les **pages fixes** (accueil, à propos, contact, offre…) sont modifiables aussi. Il s'agit de corriger du texte, ajouter ou changer des photos, **pas** de restructurer. |
| B3 | **Publication directe**, personne ne relit. On doit pouvoir **corriger ou annuler** après coup. |
| B4 | **Louis n'intervient plus** pour les mises à jour courantes. |
| B5 | **Aucun abonnement ni hébergement payant.** GitHub Pages, gratuit, convient. |
| B6 | **Aucune ressaisie** du contenu existant. |
| B7 | **Le rendu actuel est conservé.** Le CSS est très travaillé ; un nettoyage du code est bienvenu mais ne doit rien changer au rendu, et c'est vérifié par outil, pas à l'œil. |
| B8 | **Sobre et pérenne** : peu de dépendances, code lisible, reprenable par un tiers. |
| B9 | L'**URL du QR code imprimé** continue de fonctionner. |

---

# 2. Ce qu'est un CMS, et pourquoi la question du compte GitHub

Un **CMS** (système de gestion de contenu) est l'**interface d'administration** où
l'on remplit des formulaires pour modifier un site. Deux familles, qui ne rangent
pas le contenu au même endroit :

**CMS classique (WordPress).** Interface, base de données et serveur forment un
tout. Le contenu vit dans une base de données MySQL, et un serveur PHP fabrique
chaque page à chaque visite. Il faut donc un hébergement qui fait tourner PHP et
MySQL, payant, et quelqu'un qui le met à jour.

**CMS « git » (Pages CMS, Sveltia CMS, Decap CMS).** Seulement une interface. Le
contenu reste des **fichiers** (Markdown et photos) rangés dans le dépôt GitHub.
Quand un membre clique sur « Enregistrer », le CMS écrit ces fichiers dans le dépôt
(un *commit*). GitHub reconstruit alors le site et le publie. Pas de base, pas de
serveur à entretenir, et l'hébergement reste gratuit.

**D'où la question du compte GitHub.** Pour écrire dans le dépôt, le CMS doit avoir
le droit de le faire. Le plus simple pour ces outils est que chaque personne se
connecte avec **son** compte GitHub. Ce n'est pas une fatalité, trois façons de
l'éviter :

1. **Invitation par e-mail (Pages CMS).** Le propriétaire du dépôt invite des
   collaborateur·ices par adresse e-mail ; iels se connectent par un lien reçu par
   mail, **sans compte GitHub**, et Pages CMS écrit dans le dépôt en leur nom.
   ⚠️ À confirmer en pratique au prototype : c'est le **point bloquant n°1**.
2. **Un service d'authentification par e-mail** placé devant Decap ou Sveltia
   (par exemple DecapBridge). Un service tiers de plus, à évaluer.
3. **Un compte GitHub partagé** au nom de la SCOP, dont tout le monde a le mot de
   passe. Fonctionne, mais GitHub impose la double authentification aux comptes qui
   écrivent dans un dépôt, ce qui complique le partage. Solution de repli.

---

# 3. Les options

## A. WordPress

Faisable, mais c'est **un transfert de charge, pas une suppression**.

- **Ressaisie** : pas un vrai obstacle, un script peut importer les 59 projets.
- **Structure** : il faut un type de contenu « Projet » avec des champs (extension
  ACF ou équivalent) et un **thème sur mesure en PHP** pour reproduire le design.
  C'est un vrai projet de développement, et le CSS actuel serait à réintégrer dans
  la logique de thème WordPress.
- **Entretien** : mises à jour du cœur, des extensions et du thème, sécurité
  (WordPress est la cible la plus attaquée du web), sauvegardes. Quelqu'un doit
  s'en charger, donc très probablement Louis.
- **Coût** : hébergement mutualisé de l'ordre de 5 à 10 € par mois, ou formule
  WordPress.com autorisant les extensions, de l'ordre de plusieurs dizaines d'euros
  par mois. Ordres de grandeur à revérifier. Aujourd'hui : 0 €.
- **Points forts réels** : éditeur visuel très connu, historique des révisions page
  par page, prestataires faciles à trouver.

Pertinent pour un site fait de nombreuses pages libres ou d'un blog. Ce site-ci est
l'inverse : une soixantaine de fiches très structurées, une dizaine de pages fixes,
des mises à jour rares.

## B. CMS git + générateur de site statique ✅ recommandée

```
membre de la SCOP                  GitHub (gratuit)                       visiteur
┌─────────────────────┐  commit  ┌──────────────────────────────┐  ┌─────────────────────┐
│ Pages CMS (web)     │────────> │ content/projets/…/index.md   │  │ collectifarticho.com│
│ formulaire « Projet »│         │ + photos                     │  │ GitHub Pages        │
│  titre, sous-titre  │          │            │                 │  └─────────────────────┘
│  catégorie (liste)  │          │  GitHub Actions : Hugo       │            ▲
│  infos, texte       │          │  + réduction des photos ─────┼────────────┘
│  photos             │          └──────────────────────────────┘  en ligne en 1 à 2 min
└─────────────────────┘
```

- **Saisie** : formulaires web définis par nous (titre, sous-titre, catégorie en
  liste déroulante, infos, texte, photos). Structure imposée par construction.
- **Pages fixes** : chaque page devient un fichier Markdown avec quelques champs
  (textes, photos du diaporama, articles de presse). La mise en page reste dans les
  gabarits, les membres ne touchent qu'au contenu. C'est exactement B2.
- **Publication** : directe, chaque enregistrement part en ligne en une à deux
  minutes.
- **Annuler** : corriger se fait en rouvrant la fiche. Chaque enregistrement est un
  commit, donc **tout l'historique est conservé** et toute version passée est
  récupérable ; mais le retour arrière se fait depuis GitHub, pas depuis le CMS.
  C'est le point faible face aux révisions de WordPress, à regarder au prototype.
- **Coût** : 0 €. GitHub Pages, GitHub Actions (dépôt public) et Pages CMS sont
  gratuits.
- **Entretien** : rien côté serveur. Reste, rarement, une évolution de gabarit.
- **Portabilité** : le contenu est fait de fichiers ordinaires. Si Pages CMS
  disparaît, Sveltia ou Decap lisent les mêmes fichiers avec une autre
  configuration. Aucun enfermement.

### Choix du générateur

| | B1 : garder R | B2 : Hugo ✅ |
|---|---|---|
| travail | adapter `make_projet.R` pour lire du Markdown, le lancer dans GitHub Actions | porter 3 gabarits et les pages fixes |
| dépendances | R + paquets (`yaml`, `magick`) dans le CI | **un seul exécutable**, version épinglée, rien d'autre |
| photos | à coder avec `magick` | redimensionnement **natif** |
| navigation | reste codée à la main en 3 endroits | générée depuis le contenu |
| reprise par un tiers | R est rare pour ce genre de travail | Hugo est un standard documenté |

**Recommandation : Hugo.** Plus sobre en dépendances que R en CI, et il règle au
passage une bonne partie de l'ancien backlog (voir § 5). Pas de Node, pas de
`node_modules`, pas de framework JavaScript.

### Choix du CMS

| | Pages CMS ✅ | Sveltia CMS | Decap CMS |
|---|---|---|---|
| où il tourne | application hébergée par l'éditeur | page `/admin` du site | page `/admin` du site |
| connexion sans compte GitHub | **invitation par e-mail** | via un service tiers | via un service tiers |
| installation | un fichier `.pages.yml` | fichier de config, plus une passerelle d'authentification à héberger | idem |
| photos | envoyées telles quelles | **redimensionnées à l'envoi** | envoyées telles quelles |
| maturité | projet jeune, petite équipe | jeune, successeur de Decap | ancien, évolue peu |

**Recommandation : Pages CMS**, pour la connexion par e-mail et l'installation
réduite à un fichier. Le redimensionnement se fait de toute façon à la construction
par Hugo.

## C. CMS « à plat » en PHP (Kirby, Grav)

Même philosophie que le Drive actuel (un dossier par page, du texte et des photos),
avec une vraie interface d'administration. Mais il faut un **hébergement PHP
payant** et le tenir à jour, et Kirby demande une licence payante. Intéressant si
l'on quittait GitHub Pages, ce qui n'est pas le cas.

## D. Garder le Drive et automatiser

Une action GitHub récupère le dossier Drive (ou une feuille Google Sheets, une ligne
par projet) et reconstruit le site. Louis sort de la boucle, mais **les membres
gardent les fichiers texte**, précisément ce qu'iels trouvent trop compliqué. Et
l'accès automatisé au Drive demande un compte de service Google à configurer. Repli
seulement.

## E. Constructeurs de sites (Webflow, Squarespace, Wix)

Aucun entretien, mais un abonnement, un design à refaire dans leur outil et un
contenu enfermé chez eux. Écarté par B5 et B7.

## Synthèse

| | A. WordPress | **B. CMS git + Hugo** | C. Kirby/Grav | D. Drive automatisé |
|---|---|---|---|---|
| saisie par les membres | éditeur visuel | **formulaires** | formulaires | fichiers `.txt` |
| structure imposée | avec extensions | **oui** | oui | non |
| pages fixes modifiables | oui, librement | **oui, le contenu** | oui | non |
| annuler | révisions intégrées | historique git | selon config | historique Drive |
| coût mensuel | hébergement | **0 €** | hébergement | 0 € |
| entretien | élevé | **très faible** | moyen | moyen |
| rendu actuel conservé | à reconstruire en thème | **porté tel quel** | à porter | tel quel |
| Louis encore nécessaire | pour l'entretien | **non, sauf design** | pour l'entretien | non |

---

# 4. Plan d'implémentation (option B)

Chaque phase est livrable et vérifiable seule. Le site actuel reste en ligne,
intact, jusqu'à la bascule de la phase 5.

## Phase 0. Décision et accès

1. Présenter les options aux membres, obtenir la décision.
2. Lister les personnes qui éditeront et leurs adresses e-mail.
3. Créer une **organisation GitHub de la SCOP** (gratuite), avec au moins deux
   administrateur·ices dont Louis. Le nouveau dépôt y vivra, pour que le site ne
   dépende plus d'un compte personnel.

## Phase 1. Prototype de démonstration

Petit, rapide, jetable si la décision est négative.

1. Squelette Hugo minimal, 3 ou 4 projets migrés, gabarit projet porté.
2. Pages CMS branché dessus avec le formulaire « Projet ».
3. **Vérifier le point bloquant** : un membre invité par e-mail, sans compte
   GitHub, crée une fiche, ajoute des photos, publie, corrige.
4. Vérifier aussi l'annulation depuis l'interface.

Si l'invitation par e-mail ne fonctionne pas comme attendu, réévaluer entre les
solutions du § 2 avant d'aller plus loin.

## Phase 2. Migration du contenu, portage à l'identique

**Objectif : le nouveau site produit exactement le même HTML que l'ancien.** Tant
que c'est vrai, le rendu est identique par construction, sans rien avoir à regarder.

1. **Script de migration** (`migration/`, exécuté une fois) : lit
   `../collectif-articho/drive/` et écrit `content/<onglet>/<sous-onglet>/<slug>/`
   avec un `index.md` (champs structurés en tête, texte en dessous) et les photos.
   Il reprend les règles de l'ancien script : NFD, `trim`, `clé : valeur`, listes
   séparées par ` - `. Il assainit les noms de photos.
2. **Photos réduites à la migration** : les originaux restent dans l'ancien dépôt et
   dans le Drive ; le nouveau dépôt ne garde que des versions plafonnées (de l'ordre
   de 2 500 px de large). Le dépôt passe d'environ 1,4 Go à quelques centaines de Mo
   au plus, sans perte visible.
3. **Gabarits Hugo** reproduisant `default_projet.html`, `default_projets.html`,
   `default_mobiliers.html` et la page d'onglet Projets.
4. **Mêmes URL qu'aujourd'hui** (`/pages/projets/amenagements/le-lopin.html`) :
   aucune redirection nouvelle, et le stub du QR code est repris tel quel.
5. **Test d'égalité** : un script compare, page par page, le HTML de l'ancien site
   et celui du nouveau, après normalisation des blancs. Sortie attendue : aucune
   différence, ou une liste d'écarts expliqués un par un.

Les ressources statiques (`resources/css`, `fonts`, `statics`, `js`, `components`)
sont recopiées **sans modification** à cette étape.

## Phase 3. Pages fixes éditables

1. `index.html` et les pages de `pages/` deviennent des fichiers de contenu, avec
   des gabarits dédiés. Les textes libres passent en Markdown, les listes (photos
   du diaporama, articles de presse, logos) en champs répétables.
2. Même test d'égalité HTML qu'en phase 2. Les rares écarts inévitables (blancs,
   ordre d'attributs) sont justifiés ou validés par la comparaison visuelle de la
   phase 6.

## Phase 4. Formulaires du CMS

Un fichier `.pages.yml` décrit les formulaires, avec des champs obligatoires, ce qui
remplace toute validation à la main (ancien P2.2) :

| formulaire | champs |
|---|---|
| Projet | titre, sous-titre, catégorie (liste fixe), infos (liste clé/valeur), texte, photos (la 1ʳᵉ est la principale) |
| Meuble | nom, modalité, dimensions (liste), matériaux (liste), photos |
| Atelier | comme Projet |
| Accueil | textes, photos du diaporama, articles de presse, soutiens |
| Page fixe | titre, texte, photos |

**Adresses stables.** L'adresse d'une page est fixée à sa création (nom du dossier)
et ne suit plus les changements de titre. Le problème permanent de l'ancien site,
où chaque renommage de titre cassait l'URL, disparaît.

Écrire aussi un **mode d'emploi d'une page** pour les membres, avec captures.

## Phase 5. Mise en ligne et bascule

1. **GitHub Actions** : construction par Hugo (version épinglée) et publication sur
   GitHub Pages à chaque commit. Environ une à deux minutes.
2. Le nouveau dépôt reprend le domaine (`CNAME`), l'ancien est **archivé** en
   lecture seule, avec son historique complet.
3. Vérifications en ligne : toutes les pages rendent 200, le stub du QR code
   redirige, aucun lien interne mort (le script de l'ancien `CLAUDE.md` se réutilise
   tel quel).
4. **Scanner le QR code papier.**

## Phase 6. Nettoyage du code, sous contrôle visuel

Seulement après la bascule, quand le site tourne. Rien n'y est obligatoire.

**Outil de comparaison visuelle**, à écrire avant de toucher au moindre style :
Chromium headless capture chaque page de l'ancien et du nouveau site à trois
largeurs (390, 768 et 1 440 px), ImageMagick (`compare`) calcule l'écart pixel à
pixel et produit une image de différence pour chaque page qui bouge. Animations
figées, diaporama arrêté sur la même image. Les deux outils sont déjà sur le poste
de Louis. **C'est Louis qui valide chaque écart signalé**, pas Claude.

Chantiers possibles, un commit chacun, chacun validé par l'outil :

- en-tête, pied de page et barres d'onglets inclus à la construction au lieu d'être
  chargés par `fetch()`, onglet actif calculé par Hugo : `checkURL()` et jQuery
  disparaissent ;
- dédoublonnage et rangement du CSS, suppression des règles mortes ;
- styles en ligne (`style="…"`) de `index.html` rapatriés dans le CSS ;
- vignettes et photos servies en taille adaptée (`srcset`).

## Chantier annexe, hors périmètre : domaine et mail

Le domaine est chez Squarespace (ex-Google Domains) et le mail de la SCOP passe par
Google Workspace (MX `aspmx.l.google.com`). Les deux sont jugés trop chers. Migrer
vers un registraire et un hébergeur de mail plus simples (français de préférence)
est possible, mais c'est un **sujet séparé** : il faut transférer le domaine,
recréer les boîtes mail, déplacer les messages, et surtout ne jamais couper les MX
pendant l'opération. À traiter **après** la bascule du site, jamais en même temps.

---

# 5. Ce que devient le backlog de l'ancien site

Référence : `../collectif-articho/ROADMAP.md`.

| ancien point | avec l'option B |
|---|---|
| P1.2 métadonnées des pages projet | une ligne dans le gabarit Hugo |
| P1.3 page 404 maison | `layouts/404.html`, natif |
| P1.5 photos pleine résolution | réduction à la migration, puis par Hugo |
| P2.2 validation du contenu entrant | champs obligatoires du CMS |
| P2.3 titres injectés sans échappement | Hugo échappe par défaut |
| P2.4 noms de photos non assainis | assainis à la migration |
| P2.5 carrousel à une seule photo | corrigé dans le gabarit |
| P3.1 `sitemap.xml`, `robots.txt` | natifs dans Hugo |
| P3.2 slugs dupliqués en 3 endroits | navigation générée (phase 6) |
| P3.3 1,4 Go d'images dans git | nouveau dépôt avec photos réduites |
| P3.4 hygiène dépôt | nouveau dépôt propre |
| P3.5 fichiers inutilisés dans `resources/` | à trier au moment de la copie |

Tant que la décision n'est pas prise, ne rien investir de plus dans
`make_projet.R`, sauf urgence en production.
