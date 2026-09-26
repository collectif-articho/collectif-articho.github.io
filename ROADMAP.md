# Feuille de route

Contexte technique et règles de travail dans `CLAUDE.md`. Ce qui est fait part dans
`CHANGELOG.md`.

> **État au 2026-09-26** : **`v0.4`** : étapes 0 à 3 faites. Le nouveau site
> reproduit l'ancien page par page (vérifié à l'œil et par
> `python3 outils/verifier.py`), avec toutes les fiches migrées et les pages fixes
> en contenu éditable. **En cours : étape 4**, formulaires Sveltia des pages fixes
> et mode d'emploi. Louis a donné carte blanche pour avancer en autonomie
> (« keep it clean, keep it simple »), retours d'ergonomie ensuite.
> **Reste côté SCOP**, à caser dans une séance : désinstaller l'application Pages
> CMS (compte `collectif-articho`, *Settings*, *Applications*), créer le jeton
> fine-grained définitif (Q2).

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

**D2. Générateur : Hugo ; outillage : Python ; R abandonné** (2026-09-25 ; outillage révisé par D9). Hugo
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
(2026-09-25 ; nom du dépôt révisé par D7). Pas d'invitation par e-mail ni de service d'authentification tiers,
pas d'organisation.

- **Compte** : `collectif-articho` (libre au 2026-09-25 ; `articho` et `arti-cho`
  sont pris). Cohérent avec le domaine, l'Instagram `collectif.articho` et l'ancien
  dépôt. Créé par la SCOP avec l'adresse `contact@collectifarticho.com` ;
  identifiants, double authentification et codes de secours gardés par elle.
- **Dépôt** : `collectif-articho/website`, public. Le nom du dépôt n'a aucune
  importance pour le site : en ligne, seul compte le domaine. Pendant les tests,
  GitHub sert le site à une adresse provisoire
  (`https://collectif-articho.github.io/website/`) ; ce qui la rend utilisable,
  c'est que **le site ne suppose pas d'être à la racine** (étape 3, chemins).
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

**D6. Photos : masters plafonnés à 3 000 px dans le dépôt** (2026-09-25). À la
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

**D7. Dépôt `collectif-articho.github.io`, site servi à la racine** (2026-09-25,
révise la partie « dépôt » de D3). GitHub publie un dépôt nommé `website` dans un
sous-dossier (`collectif-articho.github.io/website/`), ce qui cassait tous les
chemins absolus de l'ancien site (`/resources/…`) et obligeait à passer chaque
chemin par `relURL` et à réécrire les `url()` du CSS. Un dépôt nommé
`<compte>.github.io` est publié **à la racine** de `https://<compte>.github.io/` :
les chemins absolus marchent tels quels, en test comme sur le domaine. C'est la
convention GitHub pour « le site de ce compte ». Le reste de D3 est confirmé :
**un seul compte `collectif-articho`** tenu par la SCOP, pas d'organisation, pas
d'invitations par e-mail. Les conditions de GitHub interdisent le partage d'un
identifiant entre plusieurs personnes ; choix assumé par Louis, en pratique une
ou deux personnes font les modifications, et c'est ce que la SCOP sait gérer.

**D8. Photos dans un dossier média commun, pas dans le dossier de la fiche**
(2026-09-25). Vérifié dans la doc de Pages CMS : ses dossiers média sont des
chemins fixes du dépôt, sans notion de chemin relatif à la fiche. Les « page
bundles » de Hugo (`le-lopin/index.md` + `le-lopin/1.jpg`) ne sont donc pas
alimentables depuis le CMS. Les photos vont dans `assets/photos/`, rangées par
fiche à la migration ; la fiche liste leurs chemins ; les gabarits les
redimensionnent avec `resources.Get`. Même doc : **Pages CMS ne réduit pas les
photos à l'envoi**, ce qui tranche Q1 (voir D10).

**D9. Outillage minimal, vérification à l'œil** (2026-09-25). Le rendu se vérifie
visuellement sur 5 pages types côte à côte avec l'ancien site (une fiche, un
listing, la Ligne de mobilier, l'accueil, une page texte), plus deux contrôles
scriptés : aucun lien interne mort, et chaque titre du drive présent dans le site.
62 pages sortent de 4 gabarits : si une fiche est juste, toutes le sont. Donc
**pas de `compare_html.py`**, et l'identité au caractère près du HTML n'est pas un
objectif. Dans le même esprit : migration en Python **sans dépendance** (bibliothèque
standard) et photos traitées par `mogrify` (ImageMagick, déjà sur le poste), donc
ni venv ni `requirements.txt` ; version de Hugo épinglée dans le workflow (méthode
officielle de GitHub), sans script d'installation ni `.bin/`, n'importe quel Hugo
récent en local. Révise les parties correspondantes de D2.

**D10. Croissance du dépôt acceptée** (2026-09-25, tranche Q1). Les photos
envoyées depuis le CMS entrent en pleine taille : de l'ordre de 100 à 250 Mo par
an au rythme actuel. Acceptable plusieurs années (GitHub ne bloque qu'à 100 Mo par
fichier). Le site publié reste léger : Hugo ne publie que les tailles réduites. Le
mode d'emploi demandera d'envoyer des photos « taille moyenne » depuis le
téléphone quand c'est possible. À réévaluer si le dépôt dépasse 2 Go.

**D11. Une version par étape franchie** (2026-09-25). Chaque étape du plan (§ 4)
franchie donne une version : `v0.1` à l'étape 0, jusqu'à `v1.0` à la bascule. Le
`CHANGELOG.md` est titré par version et date, et le commit qui la clôt porte une
étiquette git du même nom.

**D12. CMS : Sveltia CMS, pas Pages CMS** (2026-09-26, révise D4, tranche Q2).
Pages CMS refuse tout envoi de plus de 4,5 Mo (limite de son hébergeur Vercel),
donc la plupart des photos de téléphone. Sveltia, servi par le site sous `/admin/`,
réduit les photos dans le navigateur (WebP, 2 000 px) et écrit directement dans
GitHub : essai réussi avec une photo de 8,9 Mo. Connexion par jeton GitHub.
Limite connue : l'API qu'il utilise coupe un enregistrement de plus d'environ 5 s,
donc sur une connexion lente on ajoute les photos quelques-unes à la fois (mode
d'emploi). Louis trouve l'interface moins soignée que Pages CMS : ergonomie à
travailler à l'étape 4, puis retours de la SCOP.

**D13. Informations d'une fiche : champs nommés, plus une liste libre**
(2026-09-26, remarque de Louis après l'essai). Demander aux membres d'écrire
l'intitulé *et* la valeur de chaque information les laisse sans repère, alors que
les intitulés se répètent. Relevé sur les 53 fiches : Date (53), Commanditaire
(52), Intervention (51), Localisation (49), Matériaux réemployés (44, plus 2
« Matériaux de réemploi »), Matériaux neufs (29, plus 1 « Matériaux neuf »). Ces
six deviennent des champs du formulaire, affichés dans cet ordre quand ils sont
remplis ; les intitulés rares (Type de projet 6, Collaboration 6, Implication,
Partenaires, Équipage complet) vont dans une liste libre « Autres informations »,
affichée après. Les variantes d'orthographe sont ramenées aux six intitulés à la
migration. Clé `date_projet` et non `date`, que Hugo réserve à la date de la page.

**D14. Redirections en fichiers fixes, hors du CMS** (2026-09-26). L'ancienne URL
du QR code imprimé (`/pages/mobiliers/agencements/tpmobile.html`) est un fichier
HTML dans `static/`, pas un champ `aliases` de la fiche TPMob : un CMS peut
retirer à l'enregistrement les champs que son formulaire ne décrit pas, et une
simple correction de la fiche casserait le QR code. Règle générale : **une fiche
ne contient que des champs décrits dans `static/admin/config.yml`.**

## Questions ouvertes

Aucune au 2026-09-26. Q1 est tranchée par D8 et D10, Q2 par D12.

**Q2. Garder Pages CMS ou passer à Sveltia CMS ?** (ouverte le 2026-09-25,
**tranchée le 2026-09-26 par D12**, conservée pour mémoire).

*Constat de l'essai (2026-09-25, Louis avec son compte `lou-heraut`)* :

| test | résultat |
|---|---|
| photo lourde (> 4 Mo) | ❌ `Failed to upload file: 413` |
| photo de 2,9 Mo (2 896 × 2 896) | ✅ passée, commit `1aca82b` signé du nom de Louis |
| dossier d'arrivée | `assets/photos/projets/amenagements/`, le `path` par défaut du champ, **pas** le dossier de la fiche |
| nom du fichier | gardé tel quel (`3.jpeg`) malgré `rename: safe` : deux projets avec un `3.jpeg` entreraient en collision |
| fiche | non modifiée (aucun commit sur `le-lopin.md`), donc format d'écriture du CMS **non observé** |
| nouvelle fiche, nom de fichier | **non testé** |

Cause du 413, vérifiée : app.pagescms.org tourne sur Vercel (`server: Vercel`,
`x-powered-by: Next.js`) et les envois passent par ses fonctions, limitées à
**4,5 Mo** par requête (doc Vercel, erreur `FUNCTION_PAYLOAD_TOO_LARGE`). Ticket
ouvert chez Pages CMS (#284, juillet 2025), sans réponse. Les photos de téléphone
font 3 à 20 Mo : bloque B1.

*Options présentées à Louis* : A. garder Pages CMS et faire réduire les photos par
les membres (ils ne le feront pas) ; **B. Sveltia CMS, recommandé** ; C. héberger
Pages CMS nous-mêmes (exclu par B5).

*Sveltia CMS, vérifié dans sa doc* : application d'une page chargée depuis un CDN,
servie par notre site sous `/admin/`, compatible avec la config de Decap CMS. Avec
la connexion par jeton, elle parle **directement à l'API GitHub depuis le
navigateur**, sans serveur. Elle **réduit les images avant l'envoi** :

```yaml
media_libraries:
  default:
    config:
      transformations:
        raster_image: { format: webp, quality: 85, width: 2048, height: 2048 }
```

WebP est le seul format de sortie : les photos envoyées par le CMS seront en WebP,
les photos migrées restent en JPEG ; Hugo lit les deux. Règle aussi D10.

*Connexion* : bouton « Sign In with Token », jeton stocké dans le navigateur.
Rien à installer côté GitHub. Pour l'essai, Louis crée un jeton **classic** sur
`lou-heraut`, permission `repo`, expiration 7 jours (un jeton fine-grained ne peut
pas viser un dépôt dont on est seulement collaborateur). En production, un jeton
**fine-grained** sur le compte `collectif-articho`, limité au dépôt, permission
*Contents : Read and write* seule, collé une fois par appareil, renouvelé à
expiration (procédure dans le mode d'emploi). Alternative plus confortable mais
à héberger : « Sign in with GitHub » via `sveltia-cms-auth` sur Cloudflare
Workers (gratuit).

*Second essai, constat du 2026-09-26* (Louis, depuis un train) : la photo de
téléphone (JPEG 8,9 Mo, 3 072 × 4 096) est bien convertie en WebP dans le
navigateur, mais l'enregistrement échoue en « NetworkError when attempting to
fetch resource ». Mesures rejouées depuis le poste de Louis avec la même requête
que Sveltia (`createCommitOnBranch` GraphQL, branche jetable supprimée) :

| envoi | GraphQL (Sveltia) | REST `git/blobs` |
|---|---|---|
| 100 à 800 Ko | ✅ 1,7 à 3,5 s | |
| 996 Ko (WebP 2 000 px) | 4 sur 5, échecs à ~5,5 s | ✅ 7,5 s |
| 1,2 à 2 Mo | aléatoire, échecs à ~5,3 s (HTTP 499) | ✅ 5,8 s (1,9 Mo) |
| 8,9 Mo (brut) | ❌ | ✅ 27 s |

Conclusion : pas un seuil de taille mais un **délai d'environ 5 s** côté GraphQL,
atteint selon le débit montant (180 à 450 Ko/s dans le train). Les photos d'un
même enregistrement s'additionnent (une seule mutation, cf. ticket Sveltia
#1012). Réduction abaissée à 2 000 px (la plus grande taille servie par les
gabarits), soit environ 1 Mo par photo. **À refaire depuis une connexion
ordinaire** (fibre, 4G) avant de conclure.

*Second essai réussi le 2026-09-26* (même train, photos réduites à 2 000 px) :

| vérification | résultat |
|---|---|
| photo de téléphone 8,9 Mo ajoutée à LE LOPIN | ✅ enregistrée en WebP 1 500 × 2 000, 1,3 Mo, dans `le-lopin/` |
| nouvelle fiche « TEST » | ✅ `content/projets/amenagements/test.md`, photo dans `test/`, URL `/pages/projets/amenagements/test.html` |
| format de la fiche | identique à celui prévu (`title`, `sous_titre`, `infos` en liste `cle`/`valeur`, `photos` en liste de chemins `/photos/…`, corps Markdown) ; un champ vide est écrit `weight: null` |
| nom des photos | nom d'origine gardé (`IMG20240618165007.webp`), sans risque de collision puisque chaque fiche a son dossier |
| commits | signés du nom de l'utilisateur, publication en 25 à 30 s |
| effet de bord | le premier essai échoué a laissé un commit sans photo (`692c9f5`, simple ligne vide ajoutée), comme décrit dans le ticket #1012 |

Retour de Louis : ça marche, mais le formulaire de création paraît moins clair
que celui de Pages CMS. La config de l'essai est brute (pas d'aide sur les
champs, aperçu à côté du formulaire) ; l'interface existe en français
(`fr.yaml` dans les sources de Sveltia). À soigner à l'étape 4.

*Second essai proposé, si Louis dit oui* :

1. `static/admin/index.html` qui charge Sveltia depuis le CDN **à version
   épinglée** (lire la doc d'installation, sveltiacms.app/en/docs/start), et
   `static/admin/config.yml` : backend `github`, `repo:
   collectif-articho/collectif-articho.github.io`, `branch: main`.
2. Collection « Projets · Aménagements » sur `content/projets/amenagements`,
   mêmes champs que `.pages.yml` (titre, sous-titre, ordre, infos en liste
   clé/valeur, photos en liste, corps Markdown), format YAML front matter.
3. **Photos rangées par fiche et noms uniques** : chercher dans la doc si le
   `media_folder` d'une collection accepte un gabarit du genre
   `assets/photos/projets/amenagements/{{slug}}` avec `public_folder`
   correspondant `/photos/…`. Sinon, prévoir un nommage unique (préfixe du slug).
4. Transformations d'images comme ci-dessus.
5. Pousser ; Louis se connecte sur https://collectif-articho.github.io/admin/
   avec son jeton de test, modifie LE LOPIN, envoie une **photo de téléphone
   lourde prise en portrait** (teste le poids et l'orientation EXIF : si elle
   s'affiche couchée, ajouter la rotation dans le gabarit), crée une fiche
   « Fiche d'essai ». Puis `git pull` et lire ce que le CMS a écrit : chemin et
   nom de la photo, format de la fiche, nom du fichier de la nouvelle fiche.
6. Si concluant : réviser D4 (nouvelle décision D12), retirer `.pages.yml`,
   supprimer `assets/photos/projets/amenagements/3.jpeg` et la fiche d'essai,
   faire désinstaller l'application Pages CMS du compte de la SCOP, clore `v0.1`.

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

Chaque étape a un **critère de fin vérifiable** et donne une version (D11). Le site
actuel reste en ligne, intact, jusqu'à la bascule (étape 5).

| étape | version | contenu | attend |
|---|---|---|---|
| 0 | v0.1 | essai de bout en bout : compte, dépôt, une fiche, Pages CMS | le compte `collectif-articho` |
| 1 | v0.2 | squelette Hugo, CSS repris, gabarits générés | |
| 2 | v0.3 | migration du contenu | |
| 3 | v0.4 | pages fixes éditables, accueil compris | |
| 4 | v0.5 | formulaires du CMS, mode d'emploi, démonstration à la SCOP | un membre |
| 5 | v1.0 | bascule du domaine | un membre, pour les réglages |
| 6 | v1.x | améliorations, un sujet par version | |

## Architecture cible

```
collectif-articho.github.io/
├── hugo.toml                  config : URL, permalinks
├── content/                   textes : TOUT ce que la SCOP édite, avec assets/photos
│   ├── _index.md              accueil : champs (étape 3)
│   ├── a-propos.md  mentions-legales.md  conditions-generales.md   texte Markdown
│   ├── contact.md  notre-offre.md                                  champs + texte
│   ├── projets/
│   │   ├── _index.md          onglet
│   │   └── amenagements/
│   │       ├── _index.md      sous-onglet : titre, ordre
│   │       └── le-lopin.md    fiche : champs + texte
│   ├── mobiliers/  (agencements/, ligne-de-mobilier/)
│   └── ateliers/   (ateliers-sur-mesures/)
├── assets/photos/             photos des fiches, rangées par fiche (D8)
├── layouts/                   gabarits HTML, jamais touchés par la SCOP
│   ├── _default/baseof.html   squelette commun (<head>, en-tête, pied)
│   ├── index.html             accueil
│   ├── projets/…              fiche, listing
│   └── partials/              header, footer, barres d'onglets
├── static/resources/          css, fonts, statics, js : recopiés de l'ancien site
├── .pages.yml                 formulaires du CMS
├── .github/workflows/         construction et publication, Hugo épinglé ici
├── migration/                 script de migration, exécuté une fois
└── docs/                      mode d'emploi pour la SCOP, archives
```

**Règle de séparation** : la SCOP ne touche qu'à `content/` et `assets/photos/`.
Tout le reste est du code. C'est ce qui garantit le rendu quoi que saisissent les
membres.

## Étape 0. Essai de bout en bout (v0.1)

> Points 1 à 3 faits et publiés le 2026-09-25. Points 4 et 5 bloqués par le 413 de
> Pages CMS : voir Q2 (§ 2), qui décrit le second essai avec Sveltia CMS.

But : valider toute la chaîne sur **une seule fiche** avant d'investir, parce que
c'est elle qui fixe le format de migration (D8).

**Demande le compte `collectif-articho` (D3, D7).** Séance de réglages avec un
membre, connecté au compte de la SCOP : créer le dépôt `collectif-articho.github.io`
(public, GitHub Pages gratuit l'exige), inviter `lou-heraut` en collaborateur,
régler Pages sur « GitHub Actions », installer l'application Pages CMS sur le dépôt.

1. `git init` dans ce dossier, premier push vers le dépôt.
2. Hugo minimal : `hugo.toml`, un gabarit de fiche brut, **une** fiche écrite à la
   main (`le-lopin.md`) avec 3 photos dans `assets/photos/`.
3. Workflow `.github/workflows/publier.yml` sur le modèle officiel de GitHub pour
   Hugo, version épinglée : construction, publication Pages. Rien d'autre.
4. `.pages.yml` minimal : une collection « Projets » et son dossier média.
5. Depuis Pages CMS, connecté au compte de la SCOP : modifier la fiche, ajouter une
   photo, publier. Noter où atterrit la photo, ce qu'écrit le CMS dans la fiche, et
   le délai jusqu'à la mise en ligne.

**Fin** : une modification faite dans Pages CMS apparaît sur
`https://collectif-articho.github.io/` avec sa photo redimensionnée. Le format de
fiche et de chemin de photo de l'étape 2 est fixé d'après ce qu'écrit le CMS.

## Étape 1. Squelette et gabarits générés (v0.2)

1. Recopier **sans modification** depuis `../collectif-articho/` : `resources/css`,
   `resources/fonts`, `resources/statics`, `resources/js`, les images des pages
   fixes (`resources/images/{slideshow,articles,thumbnail}`, `accueil.JPEG`,
   `team.jpg`, les fichiers au niveau onglet listés dans `CLAUDE.md`), `CNAME`
   (retiré tant que le domaine n'a pas basculé). Trier au passage les fichiers
   inutilisés (ancien P3.5). Les chemins absolus (`/resources/…`) restent tels
   quels (D7).
2. `components/*.html` devient des partials Hugo (`header`, `footer`, barres
   d'onglets), au lieu d'être chargés par `fetch()`. **L'onglet actif est calculé
   dans le partial** : `checkURL()` et jQuery disparaissent ici.
3. Gabarits pour : fiche projet (`default_projet.html`), listing de sous-onglet
   (`default_projets.html`), listing de l'onglet Projets, page Ligne de mobilier
   (`default_mobiliers.html`, carrousel compris, cas d'une seule photo traité).
4. **Mêmes URL** : `uglyURLs = true` et permalinks préfixés par `/pages/`, donc
   `/pages/projets/amenagements/le-lopin.html`. Constaté à l'étape 0 : `uglyURLs`
   ne s'applique pas aux sections, qui sortent en `amenagements/index.html` au lieu
   de `amenagements.html`. Un permalink finissant par `.html` crée un dossier
   `amenagements.html/`, donc à écarter ; piste à essayer : `url:` dans le
   `_index.md` de chaque section.
5. Photos redimensionnées par Hugo : une taille pour la page, une pour les
   vignettes. Seules ces tailles sont publiées.

**Fin** : `hugo` construit sans erreur sur les fiches de l'étape 0 et quelques
fiches ajoutées à la main, une par gabarit.

## Étape 2. Migration du contenu (v0.3)

`migration/migrer.py`, Python sans dépendance, plus `mogrify` pour les photos
(D9). Exécuté une fois, gardé pour la traçabilité.

1. Parcourt `../collectif-articho/drive/`. Reprend les règles de l'ancien script
   (`CLAUDE.md`, § Pièges) : NFD, `trim`, `clé : valeur`, listes ` - ` des meubles.
2. Écrit une fiche par dossier. Format réel (D13, photos par fiche) :

   ```yaml
   ---
   title: "LE LOPIN"
   sous_titre: "Aménagement extérieur de l’école du CEPROC"
   weight: 5                    # ordre, tiré du préfixe NN_ du dossier drive
   commanditaire: "Croque Ta Ville"
   date_projet: "2022"          # pas `date`, réservé par Hugo
   localisation: "Paris 19e arrondissement (75)"
   intervention: "conception et réalisation"
   materiaux_reemployes: "bois d’ossature"
   materiaux_neufs: "polycarbonate alvéolaire"
   autres_infos:                # intitulés rares seulement
     - intitule: "Collaboration"
       valeur: "…"
   photos:                      # ordre d'affichage, la 1re est la principale
     - "/photos/projets/amenagements/le-lopin/1.jpg"
   ---
   Dans le cadre de l’appel à projet des Pariculteurs, …
   ```

   Meubles : `modalite`, `dimensions` (liste), `materiaux` (liste), `photos`.
3. Nom du fichier de fiche = slug de l'URL publiée (`urls.tsv`), pour garder les
   mêmes URL. Redirection du QR code en fichier fixe dans `static/` (D14).
4. Photos (D6) : noms assainis, `mogrify -auto-orient -strip -resize '3000x3000>'
   -quality 88` (orientation appliquée, métadonnées GPS retirées, plafond 3 000 px).
   Les originaux restent dans l'ancien dépôt et dans le Drive.
5. Rapport en fin d'exécution : fiches écrites, champs manquants, photos renommées,
   anomalies.

**Fin** : 53 fiches projet et 5 meubles dans `content/`, rapport sans anomalie non
expliquée, `assets/photos/` autour de 460 Mo. Les deux contrôles de D9 passent
(aucun lien mort, chaque titre du drive présent) et les pages types sont vérifiées
à l'œil contre l'ancien site.

## Étape 3. Pages fixes éditables (v0.4)

C'est l'argument qui compte pour la SCOP face à WordPress : **tout le site se
modifie depuis les formulaires**, accueil compris, sans que personne puisse casser
la mise en page.

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
  page ;
- partenaires : certains noms contiennent un `/` (« Mission Locale Saint-Denis /
  Pierrefitte »), donc une liste de noms par groupe, pas un texte à découper ; la
  balise `<it>` actuelle n'existe pas en HTML, le rôle devient un champ ;
- soutiens : les deux derniers logos sont empilés verticalement, prévoir un champ
  de regroupement ou un cas dans le gabarit ;
- pied de page : année `2025` écrite en dur, à calculer à la construction.

**Fin** : toutes les pages de l'ancien site existent dans le nouveau, vérifiées à
l'œil côte à côte ; aucun lien mort.

## Étape 4. Formulaires du CMS et démonstration (v0.5)

1. Compléter `.pages.yml` :

   | formulaire | champs |
   |---|---|
   | Projet (un par sous-onglet) | titre, sous-titre, infos (liste clé/valeur), texte, photos ; champs obligatoires marqués |
   | Meuble | nom, modalité, dimensions (liste), matériaux (liste), photos |
   | Accueil, Contact, Offre, pages d'onglet | les champs de l'étape 3 |
   | Pages texte | titre, texte |

2. Vérifier avec le compte de la SCOP : créer une fiche, ajouter et réordonner des
   photos, publier, corriger, supprimer, modifier l'accueil.
3. Vérifier ce que l'interface permet pour **annuler** ; si c'est insuffisant,
   documenter la procédure de retour arrière depuis GitHub.
4. Écrire `docs/mode-emploi.md` pour les membres : une page, avec captures, dont
   la consigne sur la taille des photos (D10).
5. Démonstration à la SCOP sur l'adresse de test.

**Adresses stables** : l'URL d'une fiche est le nom de son fichier, fixé à la
création. Renommer un titre ne la change plus, contrairement à l'ancien site.

**Fin** : un membre de la SCOP fait une modification complète seul, avec le mode
d'emploi.

## Étape 5. Bascule (v1.0)

1. Retirer le domaine de l'ancien dépôt, l'ajouter au nouveau (`CNAME` et
   réglage Pages, connecté au compte de la SCOP). Les enregistrements DNS ne
   changent pas : ils pointent déjà vers GitHub Pages.
2. Vérifier en ligne : pages, images, stub du QR code, liens internes.
3. **Scanner le QR code papier.**
4. Transférer l'ancien dépôt `lou-heraut/collectif-articho` au compte
   `collectif-articho` et l'**archiver** (lecture seule, historique complet et
   photos originales conservés).

**Fin** : `collectifarticho.com` est servi par le nouveau dépôt, le QR code
fonctionne.

## Étape 6. Améliorations (v1.x)

Après la bascule, une version par sujet, chacune vérifiée contre le rendu :

- métadonnées par page (`<title>`, description, Open Graph avec image absolue),
  `404.html`, `sitemap.xml` (natif) ;
- ~~Leaflet de la page contact sans version~~ : épinglé en 1.9.4 à l'étape 3 ;
- fond de carte du contact : OpenStreetMap depuis l'étape 3 (CARTO exige une clé).
  Si le rendu coloré ne plaît pas, un filtre CSS (niveaux de gris) suffit ;
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
- **La carte de la page Contact est cassée sur le site actuel** (« API KEY
  REQUIRED » : le fournisseur CARTO exige désormais une clé). Réparé dans le
  nouveau site ; l'ancien reste tel quel jusqu'à la bascule, sauf si Louis
  préfère le corriger avant (une ligne dans `pages/contact.html`).
- **Prix des meubles** : le drive en contient (Tabouret tapissé 285 € HT,
  Luminaire 350 €, Tabouret 265 € HT, les tables « sur demande ») mais l'ancien
  site ne les a jamais affichés (« Prix sur demande » partout) et ils n'ont pas
  été migrés. Si la SCOP veut les afficher, c'est un champ à ajouter.

---

# 5. Ce que devient le backlog de l'ancien site

Référence : `../collectif-articho/ROADMAP.md`.

| ancien point | dans la v2 |
|---|---|
| P1.2 métadonnées des pages projet | étape 6, une ligne de gabarit |
| P1.3 page 404 maison | étape 6, natif |
| P1.5 photos pleine résolution | étapes 1 et 2, D6 |
| P2.2 validation du contenu entrant | étape 4, champs obligatoires |
| P2.3 titres injectés sans échappement | Hugo échappe par défaut |
| P2.4 noms de photos non assainis | étape 2 |
| P2.5 carrousel à une seule photo | étape 1, dans le gabarit |
| P3.1 `sitemap.xml`, `robots.txt` | étape 6, natif |
| P3.2 slugs dupliqués en 3 endroits | étape 1, navigation en partials |
| P3.3 1,4 Go d'images dans git | nouveau dépôt, photos plafonnées |
| P3.4 hygiène dépôt | nouveau dépôt propre |
| P3.5 fichiers inutilisés dans `resources/` | étape 1, à la copie |

Ne rien investir de plus dans `make_projet.R`, sauf urgence en production.
