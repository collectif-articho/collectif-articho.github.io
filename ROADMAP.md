# Feuille de route

Contexte technique et règles de travail dans `CLAUDE.md`. Ce qui est fait part dans
`CHANGELOG.md`.

> **État au 2026-09-25** : cadrage terminé, décisions D1 à D7 prises (§ 2), une
> question ouverte (Q1). **Aucun code écrit.** Prochaine action : **étape 1** du
> plan d'attaque (§ 4), outillage local. Rien n'attend Louis avant l'étape 5, qui
> demande le compte GitHub `collectif-articho` (§ 2, D3).

**Tenir ce bandeau à jour** à chaque étape franchie : c'est le point d'entrée d'une
reprise de travail.

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
jour en deux ans** (historique git). L'outil sera ouvert deux ou trois fois par an,
par des gens qui auront oublié entre deux fois. Il doit être évident sans formation.

## Cahier des besoins (validé par Louis le 2026-09-24)

| | besoin |
|---|---|
| B1 | Les membres **ajoutent, modifient, suppriment** projets, meubles et ateliers seul·es, sans compétence HTML ni CSS. Des formulaires plutôt que des fichiers ; du Markdown simple reste acceptable. |
| B2 | Les **pages fixes** (accueil, à propos, contact, offre…) sont modifiables aussi. Il s'agit de corriger du texte, ajouter ou changer des photos, **pas** de restructurer. |
| B3 | **Publication directe**, personne ne relit. On doit pouvoir **corriger ou annuler** après coup. |
| B4 | **Louis n'intervient plus** pour les mises à jour courantes. |
| B5 | **Aucun abonnement ni hébergement payant.** GitHub Pages, gratuit, convient. |
| B6 | **Aucune ressaisie** du contenu existant. |
| B7 | **Le rendu actuel est conservé.** Le CSS est très travaillé ; un nettoyage du code est bienvenu mais ne doit rien changer au rendu. |
| B8 | **Sobre et pérenne** : peu de dépendances, code lisible, reprenable par un tiers. |
| B9 | L'**URL du QR code imprimé** continue de fonctionner. |

---

# 2. Décisions

Journal des arbitrages, du plus ancien au plus récent. Ne pas rouvrir une décision
sans élément nouveau ; si c'est le cas, ajouter une entrée plutôt que réécrire.

**D1. Option B : CMS « git » et générateur statique, pas WordPress** (2026-09-25,
Louis, après présentation informelle à la SCOP). Raisons : 0 €, pas de serveur à
entretenir, design conservé, contenu en fichiers portables. Comparaison au § 3.

**D2. Générateur : Hugo ; outillage : Python ; R abandonné** (2026-09-25). Hugo
est un exécutable Go unique, sans pip ni dépendances : on épingle sa version dans
`.hugo-version`, un script l'installe dans `.bin/` du projet (ignoré par git, rôle
équivalent d'un venv), et le workflow CI lit le même fichier. Il apporte sans code à
écrire : redimensionnement d'images, sections imbriquées, URL en `.html`, sitemap.
Écrire notre propre générateur en Python (Jinja2, PyYAML, Markdown, Pillow) a été
envisagé : templates plus lisibles, mais quelques centaines de lignes de moteur à
maintenir, c'est-à-dire refaire proprement ce qu'était `make_projet.R`. Pelican
(générateur Python) est taillé pour les blogs et se plierait mal aux sections
imbriquées. Python sert en revanche à **tout l'outillage** (migration, comparaison
HTML, captures), dans un venv avec `requirements.txt` épinglé. **R n'est pas
conservé**, sous aucune forme.

**D3. Accès : compte GitHub `collectif-articho` pour la SCOP, Louis collaborateur**
(2026-09-25). Pas d'invitation par e-mail ni de service d'authentification tiers,
pas d'organisation.

- **Compte** : `collectif-articho` (libre au 2026-09-25 ; `articho` et `arti-cho`
  sont pris). Cohérent avec le domaine, l'Instagram `collectif.articho` et l'ancien
  dépôt. Créé par la SCOP avec l'adresse `contact@collectifarticho.com` ;
  identifiants, double authentification et codes de secours gardés par elle.
- **Dépôt** : `collectif-articho.github.io`, public. Ce nom est imposé par GitHub
  pour qu'un site soit servi **à la racine** (`https://collectif-articho.github.io/`)
  avant la bascule du domaine ; tout autre nom serait servi sous `/<dépôt>/` et
  casserait les chemins absolus du site.
- **Louis** : collaborateur avec son compte `lou-heraut`. Vérifié dans la doc
  GitHub, un collaborateur d'un dépôt personnel peut pousser, fusionner, publier
  des releases, mais **pas** toucher aux réglages (Pages, Actions, domaine,
  collaborateurs, applications installées). Ces réglages ne se font qu'une fois :
  activer Pages par Actions, installer l'application Pages CMS, poser le domaine à
  la bascule. Ils se font **connecté au compte de la SCOP**, avec un membre.
- Une organisation (deux propriétaires, pas de mot de passe partagé) a été
  envisagée et écartée : un concept de plus pour la SCOP, pour des réglages qui ne
  servent qu'une ou deux fois. Revenir dessus si ces réglages deviennent fréquents.

**D4. CMS : Pages CMS.** Avec une connexion par compte GitHub (D3), il n'y a rien à
héberger : l'application tourne chez l'éditeur, on installe son application GitHub
sur le dépôt et on décrit les formulaires dans `.pages.yml`. Sveltia et Decap
demanderaient une passerelle OAuth à héberger. Le contenu restant des fichiers
ordinaires, changer de CMS plus tard ne coûte qu'une configuration.

**D5. Pages fixes : gabarit HTML et champs de contenu séparés** (2026-09-25). La
mise en page, parfois technique (accueil surtout), reste dans des gabarits HTML
écrits à la main. Les membres n'éditent que des « emplacements » : textes, photos,
listes. Détail au § 4, étape 4.

**D6. Tests visuels : libres, sans obstination** (2026-09-25). Claude peut utiliser
Chromium headless et ImageMagick pour tester et régler le CSS. Si un réglage ne
converge pas après deux ou trois essais, revenir vers Louis avec une question
précise plutôt que d'insister. Voir `CLAUDE.md`, § Principes de travail.

**D7. Photos : masters plafonnés à 3 000 px dans le dépôt** (2026-09-25). À la
migration, chaque photo est réduite à 3 000 px sur le plus grand côté, JPEG
qualité 88. Mesuré sur un échantillon de 24 photos (surtout des 4 032 × 3 024 de
téléphone) : 78 Mo à l'origine, 30 Mo après, soit environ **460 Mo** pour les
291 photos actuelles (1,2 Go). 3 000 px couvre un affichage pleine largeur sur
écran haute densité ; au-delà, rien sur le web ne s'en sert.

Ce n'est pas destructif : **les originaux restent** dans le Drive de la SCOP et
dans l'ancien dépôt, archivé avec tout son historique (étape 7). Les tailles
servies aux visiteurs (page, vignette) sont calculées par Hugo à la construction,
jamais commitées. Plafonner après coup, par une action GitHub, ne servirait à
rien : l'original resterait dans l'historique git. Le plafonnement doit donc se
faire **avant** le commit : à la migration, puis à l'envoi depuis le CMS (Q1).

## Questions ouvertes

**Q1. Le CMS réduit-il les photos à l'envoi ?** Les membres enverront des photos
de téléphone de 3 à 20 Mo. Sans plafonnement à l'envoi, le dépôt grossit de
l'ordre de 100 à 250 Mo par an au rythme actuel (estimation : 2 à 3 vagues, quelques
projets de 5 à 10 photos), pour toujours. Pages CMS : capacité non vérifiée. Sveltia
CMS sait le faire, mais demande une connexion par jeton ou une passerelle OAuth.
**À trancher à l'étape 6**, avant d'ouvrir le CMS aux membres. Repli acceptable :
accepter la croissance quelques années, GitHub ne pose de limite dure qu'à 100 Mo
par fichier et recommande de rester sous quelques Go par dépôt.

---

# 3. Options étudiées (pour mémoire)

La présentation montrée à la SCOP est archivée dans `docs/presentation-scop/`.

| | A. WordPress | **B. CMS git + Hugo** ✅ | C. Kirby/Grav | D. Drive automatisé | E. Wix, Webflow… |
|---|---|---|---|---|---|
| saisie | éditeur visuel | formulaires | formulaires | fichiers `.txt` | éditeur visuel |
| structure imposée | avec extensions (ACF) | oui | oui | non | selon l'outil |
| pages fixes | tout, mise en page comprise | textes et photos | oui | non | tout |
| annuler | révisions intégrées | historique git, depuis GitHub | selon config | historique Drive | intégré |
| coût mensuel | hébergement (≈ 5 à 10 €, plus en formule gérée) | 0 € | hébergement PHP (+ licence Kirby) | 0 € | abonnement |
| entretien | élevé (mises à jour, sécurité) | quasi nul | moyen | moyen | nul |
| design actuel | à reconstruire en thème PHP | porté tel quel | à porter | tel quel | à refaire |
| Louis nécessaire | pour l'entretien | pour le design seulement | pour l'entretien | non | non |

Sur A : la ressaisie n'est pas un argument (un script importe les projets) ; ses
vrais coûts sont le thème sur mesure, l'hébergement et l'entretien de sécurité, qui
retomberaient sur Louis. Sur D : Louis sort de la boucle, mais les membres gardent
les fichiers texte qu'iels trouvent trop compliqués.

---

# 4. Plan d'attaque

Chaque étape a un **critère de fin vérifiable**. Le site actuel reste en ligne,
intact, jusqu'à l'étape 7. Les étapes 1 à 4 se font entièrement en local.

## Architecture cible

```
collectif-articho-v2/
├── hugo.toml                  config : URL, permalinks, version minimale de Hugo
├── content/                   TOUT ce que la SCOP édite, et rien d'autre
│   ├── _index.md              accueil : champs seulement (voir étape 4)
│   ├── a-propos.md  mentions-legales.md  conditions-generales.md   texte Markdown
│   ├── contact.md  notre-offre.md                                  champs + texte
│   ├── projets/
│   │   ├── _index.md          onglet
│   │   └── amenagements/
│   │       ├── _index.md      sous-onglet : titre, ordre
│   │       └── le-lopin/
│   │           ├── index.md   fiche : champs + texte
│   │           └── 1.jpg …    photos de la fiche
│   ├── mobiliers/  (agencements/, ligne-de-mobilier/)
│   └── ateliers/   (ateliers-sur-mesures/)
├── layouts/                   gabarits HTML, jamais touchés par la SCOP
│   ├── _default/baseof.html   squelette commun (<head>, en-tête, pied)
│   ├── index.html             accueil
│   ├── projets/…              fiche, listing
│   └── partials/              header, footer, barres d'onglets
├── static/resources/          css, fonts, statics, js : recopiés de l'ancien site
├── .pages.yml                 formulaires du CMS
├── .github/workflows/         construction et publication
├── migration/                 script de migration, exécuté une fois
├── outils/                    comparaison HTML, captures
└── docs/                      mode d'emploi pour la SCOP, archives
```

**Règle de séparation** : la SCOP ne touche qu'à `content/`. Tout le reste est du
code. C'est ce qui garantit le rendu quoi que saisissent les membres.

## Étape 1. Outillage local

1. Hugo (D2) : version épinglée dans `.hugo-version` ; `outils/installer-hugo.sh`
   télécharge le binaire officiel de cette version depuis les releases GitHub,
   **vérifie sa somme de contrôle**, l'installe dans `.bin/` (ignoré par git).
   Jamais de snap ni de paquet de distribution. Édition standard ou *extended*
   (WebP) : trancher en lisant les notes de version au moment d'épingler.
2. Python : `python3 -m venv .venv`, `requirements.txt` épinglé (Pillow, et le
   strict nécessaire), `.venv/` ignoré par git.
3. Squelette : `hugo.toml`, `layouts/_default/baseof.html`, `static/`,
   `.gitignore` (`.bin/`, `.venv/`, `public/`, `resources/_gen/`).
4. Recopier **sans modification** depuis `../collectif-articho/` : `resources/css`,
   `resources/fonts`, `resources/statics`, `resources/js`, `components/`, les images
   des pages fixes (`resources/images/{slideshow,articles,thumbnail}`,
   `accueil.JPEG`, `team.jpg`, les fichiers au niveau onglet listés dans
   `CLAUDE.md`), `CNAME`. Les `resources/images/<onglet>/<sous-onglet>/` ne sont
   **pas** recopiées : elles viendront de la migration. Trier au passage les
   fichiers inutilisés (ancien P3.5).
5. `outils/compare_html.py` : construit le site, puis compare page par page avec
   `../collectif-articho/` après normalisation (blancs, ordre des attributs,
   chemins d'images ramenés au nom de fichier). Sortie : pages identiques,
   différentes, manquantes, en trop.

**Fin** : `hugo` construit sans erreur ; `outils/compare_html.py` tourne et liste
toutes les pages comme manquantes.

## Étape 2. Migration du contenu

`migration/migrer.py`, Python dans le venv (Pillow pour les photos). Exécuté une
fois, gardé pour la traçabilité.

1. Parcourt `../collectif-articho/drive/`. Reprend les règles de l'ancien script
   (`CLAUDE.md`, § Pièges) : NFD, `trim`, `clé : valeur`, listes ` - ` des meubles.
2. Écrit une fiche par dossier. Format retenu :

   ```yaml
   ---
   title: "LE LOPIN"
   sous_titre: "Aménagement extérieur de l'école du CEPROC"
   weight: 5                    # ordre, tiré du préfixe NN_ du dossier drive
   infos:
     - { cle: "Commanditaire", valeur: "Croque Ta Ville" }
     - { cle: "Date", valeur: "2022" }
   photos: [1.jpg, 2.jpg, 3.jpg]  # ordre d'affichage, la 1re est la principale
   ---
   Dans le cadre de l'appel à projet des Pariculteurs, …

   Deuxième paragraphe…
   ```

   Meubles : `modalite`, `dimensions` (liste), `materiaux` (liste), `photos`.
3. Nom du dossier de fiche = slug actuel (`to_link()` de l'ancien script), pour
   garder les mêmes URL.
4. Photos (D7) : noms assainis, orientation EXIF appliquée, plafond 3 000 px,
   JPEG qualité 88, métadonnées de localisation GPS retirées. Les originaux
   restent dans l'ancien dépôt et dans le Drive.
5. Rapport en fin d'exécution : fiches écrites, champs manquants, photos renommées,
   anomalies.

**Fin** : 53 fiches projet et 5 meubles dans `content/`, rapport sans anomalie non
expliquée, `content/` autour de 460 Mo.

## Étape 3. Gabarits générés, à l'identique

1. Gabarits Hugo pour : fiche projet (`default_projet.html`), listing de
   sous-onglet (`default_projets.html`), listing de l'onglet Projets, page Ligne de
   mobilier (`default_mobiliers.html`, carrousel compris).
2. **Mêmes URL** : `uglyURLs = true` et permalinks préfixés par `/pages/`, donc
   `/pages/projets/amenagements/le-lopin.html`. Le stub du QR code devient un
   contenu avec un gabarit « redirection ».
3. En-tête, pied de page et `script.js` **inchangés** à cette étape : le HTML des
   pages reste celui de l'ancien site, `fetch()` compris.
4. Photos : servies depuis le dossier de la fiche, redimensionnées par Hugo (une
   taille pour la page, une pour les vignettes). C'est le seul écart assumé avec
   l'ancien HTML, neutralisé par la normalisation des chemins dans la comparaison.

**Fin** : `outils/compare_html.py` ne signale **aucune différence** sur les 62 pages
générées (53 fiches, 8 listings, Ligne de mobilier), hors écarts listés et
expliqués un par un dans le `CHANGELOG`.

## Étape 4. Pages fixes éditables

Principe (D5) : **le gabarit porte la mise en page, le fichier de contenu porte
les emplacements.** Trois cas selon la page :

| page | modèle | ce que la SCOP édite |
|---|---|---|
| **accueil** | gabarit dédié, champs seulement | diaporama (liste de photos) ; accroche ; 4 valeurs ; 3 offres (titre, sous-titre, lien) ; blocs de texte en Markdown ; photo d'accueil, photo d'équipe ; presse (nom, image, lien) ; soutiens (logo, lien) ; partenaires (groupes de noms) |
| **contact** | gabarit dédié, champs | e-mail, réseaux (nom, lien, icône), adresses (nom, adresse) ; la carte reste dans le gabarit |
| **notre-offre** | gabarit, champs et texte | plaquette PDF, texte |
| **ateliers**, **mobiliers** | gabarit de page d'onglet | 2 cartes (titre, sous-titre, image, lien) |
| **à propos**, **mentions légales**, **conditions générales** | gabarit « texte », corps en Markdown | le texte, avec gras et italique |

Concrètement, pour l'accueil, le gabarit `layouts/index.html` contient tout le HTML
actuel, et à la place de chaque contenu une boucle ou un champ :

```html
<div id="slideshow">
  {{ range .Params.diaporama }}
  <figure><img loading="lazy" src="{{ . }}"></figure>
  {{ end }}
</div>
…
<div id="container_article">
  {{ range .Params.presse }}
  <a class="article" href="{{ .lien }}" target="_blank">
    <div class="circle"></div>
    <img loading="lazy" src="{{ .image }}">
    <h4>{{ .nom }}</h4>
  </a>
  {{ end }}
</div>
```

Un champ de texte long passe par `markdownify` et s'insère au bon endroit. Les
membres écrivent `**gras**`, jamais de HTML ; le CSS et la structure ne dépendent
jamais de ce qu'iels saisissent.

Points connus à traiter :

- les styles en ligne des pages texte (`style="margin-top: 0rem;"` sur chaque
  `<p>`) ne survivent pas au Markdown : les remplacer par une règle CSS de la
  page. Écart de HTML voulu, vérifié par capture (D6) ;
- partenaires : certains noms contiennent un `/` (« Mission Locale Saint-Denis /
  Pierrefitte »), donc une liste de noms par groupe, pas un texte à découper ; la
  balise `<it>` actuelle n'existe pas en HTML, le rôle devient un champ ;
- soutiens : les deux derniers logos sont empilés verticalement, prévoir un champ
  de regroupement ou un cas dans le gabarit ;
- pied de page : année `2025` écrite en dur, à calculer à la construction.

**Fin** : toutes les pages de l'ancien site existent dans le nouveau ; pages à
champs identiques au sens de `compare-html` ; pages Markdown validées par capture.

## Étape 5. Mise en ligne de test

**Demande le compte `collectif-articho` (D3).** Séance de réglages avec un membre,
connecté au compte de la SCOP : créer le dépôt `collectif-articho.github.io`
(public, GitHub Pages gratuit l'exige), inviter `lou-heraut` en collaborateur,
régler Pages sur « GitHub Actions ».

1. Pousser ce dossier vers le dépôt.
2. Workflow `.github/workflows/publier.yml` : Hugo à version épinglée, construction,
   publication Pages. Rien d'autre.
3. Vérifier en ligne : toutes les pages rendent 200, aucun lien interne mort.

**Fin** : le nouveau site est consultable à l'adresse de test, identique à
l'ancien.

## Étape 6. Formulaires du CMS

1. Trancher Q1 (réduction des photos à l'envoi). Installer l'application Pages
   CMS sur le dépôt (connecté au compte de la SCOP) ; écrire `.pages.yml` :

   | formulaire | champs |
   |---|---|
   | Projet (un par sous-onglet) | titre, sous-titre, infos (liste clé/valeur), texte, photos ; champs obligatoires marqués |
   | Meuble | nom, modalité, dimensions (liste), matériaux (liste), photos |
   | Accueil, Contact, Offre, pages d'onglet | les champs de l'étape 4 |
   | Pages texte | titre, texte |

2. Vérifier avec le compte de la SCOP : créer une fiche, ajouter et réordonner des
   photos, publier, corriger, supprimer. Mesurer le délai jusqu'à la mise en ligne.
3. Vérifier ce que l'interface permet pour **annuler** ; si c'est insuffisant,
   documenter la procédure de retour arrière depuis GitHub.
4. Écrire `docs/mode-emploi.md` pour les membres : une page, avec captures.

**Adresses stables** : l'URL d'une fiche est le nom de son dossier, fixé à la
création. Renommer un titre ne la change plus, contrairement à l'ancien site.

**Fin** : un membre de la SCOP fait une modification complète seul, avec le mode
d'emploi.

## Étape 7. Bascule

1. Retirer le domaine de l'ancien dépôt, l'ajouter au nouveau (`CNAME` et
   réglage Pages). Les enregistrements DNS ne changent pas : ils pointent déjà vers
   GitHub Pages.
2. Vérifier en ligne : pages, images, stub du QR code, liens internes.
3. **Scanner le QR code papier.**
4. Transférer l'ancien dépôt `lou-heraut/collectif-articho` au compte
   `collectif-articho` et l'**archiver** (lecture seule, historique complet et
   photos originales conservés).

**Fin** : `collectifarticho.com` est servi par le nouveau dépôt, le QR code
fonctionne.

## Étape 8. Nettoyage et améliorations

Après la bascule, un commit par sujet, chacun vérifié (D6) :

- en-tête, pied de page et barres d'onglets en partials Hugo au lieu de `fetch()`,
  onglet actif calculé à la construction : `checkURL()` et jQuery disparaissent ;
- métadonnées par page (`<title>`, description, Open Graph avec image absolue),
  `404.html`, `sitemap.xml` (natif) ;
- Leaflet de la page contact : chargé depuis `unpkg.com` **sans version**, donc à
  la merci d'une version majeure ; épingler ou héberger ;
- CSS : règles mortes, doublons, styles en ligne de `index.html` rapatriés ;
- `srcset` pour servir la bonne taille d'image selon l'écran.

## Hors périmètre : domaine et mail

Le domaine est chez Squarespace (ex-Google Domains), le mail passe par Google
Workspace (MX `aspmx.l.google.com`). Les deux sont jugés trop chers. Migrer vers
un registraire et un hébergeur de mail plus simples est un **sujet séparé** :
transfert du domaine, recréation des boîtes, déplacement des messages, sans jamais
couper les MX. À traiter **après** la bascule, jamais en même temps.

## À signaler à la SCOP (contenu, pas code)

- **Mentions légales périmées** : elles disent le site « hébergé bénévolement sur
  le serveur de Louis Héraut », alors qu'il est chez GitHub (GitHub Inc., à
  nommer comme hébergeur, c'est une obligation légale) ; elles parlent encore de
  CAVAPU qui « se transforme en SCOP ».
- Page d'accueil : la transformation en SCOP est racontée dans deux paragraphes
  successifs qui se recoupent.

---

# 5. Ce que devient le backlog de l'ancien site

Référence : `../collectif-articho/ROADMAP.md`.

| ancien point | dans la v2 |
|---|---|
| P1.2 métadonnées des pages projet | étape 8, une ligne de gabarit |
| P1.3 page 404 maison | étape 8, natif |
| P1.5 photos pleine résolution | étapes 2 et 3, D7 |
| P2.2 validation du contenu entrant | étape 6, champs obligatoires |
| P2.3 titres injectés sans échappement | Hugo échappe par défaut |
| P2.4 noms de photos non assainis | étape 2 |
| P2.5 carrousel à une seule photo | étape 3, dans le gabarit |
| P3.1 `sitemap.xml`, `robots.txt` | étape 8, natif |
| P3.2 slugs dupliqués en 3 endroits | étape 8, navigation générée |
| P3.3 1,4 Go d'images dans git | nouveau dépôt, photos plafonnées |
| P3.4 hygiène dépôt | nouveau dépôt propre |
| P3.5 fichiers inutilisés dans `resources/` | étape 1, à la copie |

Ne rien investir de plus dans `make_projet.R`, sauf urgence en production.
