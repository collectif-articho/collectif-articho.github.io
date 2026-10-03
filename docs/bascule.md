# Bascule du domaine : pas à pas

`collectifarticho.com` passe de l'ancien dépôt (`lou-heraut/collectif-articho`) au
nouveau (`collectif-articho/collectif-articho.github.io`). Étape 5 de
`ROADMAP.md`, décision D15.

| qui | quoi | durée |
|---|---|---|
| Louis, compte `lou-heraut` | retirer le domaine de l'ancien dépôt | 2 min |
| un membre, compte `collectif-articho` | poser le domaine sur le nouveau, créer le jeton, ménage | 10 min |
| un membre, accès Squarespace | corriger la ligne `www` du DNS, si besoin | 5 min |
| Louis | vérifier, scanner le QR code, archiver l'ancien dépôt | 15 min |

Le site ne change pas d'aspect. Seul risque : pendant quelques minutes, voire
quelques heures, `https://collectifarticho.com` peut afficher une alerte de
certificat, le temps que GitHub en délivre un pour le nouveau dépôt. Choisir un
moment calme.

Les écrans de GitHub sont en anglais : les noms de boutons sont donnés tels
quels, **en gras**.

## Avant

- **Louis** : vérifier que le dernier déploiement du nouveau site est vert
  (`gh run list -R collectif-articho/collectif-articho.github.io`).
- **Demander à la SCOP** qui a les identifiants de **Squarespace** (le DNS du
  domaine) : utile seulement si la ligne `www` pose problème (étape 4).

## 1. Retirer le domaine de l'ancien site (Louis)

1. Ouvrir https://github.com/lou-heraut/collectif-articho/settings/pages
2. Sous *Custom domain*, cliquer **Remove**.

À partir de là, `collectifarticho.com` ne répond plus (erreur 404 de GitHub)
jusqu'à l'étape 2 : enchaîner sans attendre. Ne pas dépublier l'ancien site tout
de suite : c'est ce qui permet de revenir en arrière.

## 2. Poser le domaine sur le nouveau site (membre, compte de la SCOP)

1. Se connecter à https://github.com avec le compte **collectif-articho**.
2. Ouvrir https://github.com/collectif-articho/collectif-articho.github.io/settings/pages
3. Sous *Custom domain*, taper `collectifarticho.com` et cliquer **Save**.
4. Attendre le message vert *DNS check successful* (recharger la page au bout
   d'une minute).
5. Cocher **Enforce HTTPS**. Si la case est grisée, GitHub prépare le
   certificat (jusqu'à 24 h) : revenir la cocher plus tard, c'est la seule chose
   à refaire. L'ancien site l'avait ; sans elle, les visiteurs qui tapent
   `http://` ne sont pas redirigés vers `https://`.

Le reste de la page (*Build and deployment*, *Source : GitHub Actions*) ne se
touche pas.

## 3. Pendant que le compte est ouvert (même membre)

**Le jeton du CMS** (c'est lui qu'on colle sur la page d'administration) :

1. En haut à droite, la photo du compte, puis **Settings**.
2. Tout en bas de la colonne de gauche : **Developer settings**.
3. **Personal access tokens**, puis **Fine-grained tokens**, puis
   **Generate new token**.
4. *Token name* : `CMS du site`. *Expiration* : **No expiration** (D19 : le
   jeton ne sert qu'à ce dépôt et ne peut que modifier son contenu ; s'il fuit,
   on le supprime et on en crée un autre, comme ici).
5. *Repository access* : **Only select repositories**, puis choisir
   `collectif-articho.github.io` dans la liste.
6. Sous *Permissions*, trouver **Contents** (dans *Repository permissions*, ou
   par **Add permissions**) et choisir **Read and write**. *Metadata* passe
   tout seul en lecture, c'est normal. Ne rien ajouter d'autre.
7. **Generate token**, copier le jeton (il commence par `github_pat_`) et le
   ranger aussitôt dans le gestionnaire de mots de passe de la SCOP. GitHub ne
   le montre qu'une fois.

**Ménage** : désinstaller Pages CMS, le premier CMS essayé puis écarté.
**Settings**, **Applications**, ligne *Pages CMS*, **Configure**, tout en bas
**Uninstall**. S'il n'apparaît pas, il est déjà parti : rien à faire.

Tout le reste des réglages du compte peut être ignoré.

## 4. Vérifier (Louis)

- https://collectifarticho.com/ et une fiche projet s'affichent ;
- https://collectifarticho.com/pages/mobiliers/agencements/tpmobile.html mène à
  la fiche du TPMob, puis **scanner le QR code papier** ;
- https://collectifarticho.com/admin/ : se connecter avec le nouveau jeton ;
- https://www.collectifarticho.com/ redirige vers https://collectifarticho.com/.

**Si `www` ne redirige pas, ou affiche une alerte de certificat** : la ligne
`www` du DNS pointe encore vers le compte de Louis (`lou-heraut.github.io`,
relevé le 2026-10-03), et GitHub demande qu'elle pointe vers le compte qui
publie. Chez Squarespace, dans le DNS de `collectifarticho.com`, modifier
**uniquement** l'enregistrement `CNAME` de `www` : valeur
`collectif-articho.github.io`. Ne toucher à aucune autre ligne, surtout pas les
`MX` (le mail de la SCOP).

## 5. Après (Louis)

1. Un commit sur le nouveau dépôt : `baseURL` de `hugo.toml` et `site_url` de
   `static/admin/config.yml` passent à `https://collectifarticho.com` (le guide
   donne déjà cette adresse) ; `ROADMAP.md` et `CHANGELOG.md` (`v1.0`).
3. Envoyer aux membres le guide, `docs/guide/guide-du-site.pdf`, avec le jeton.
2. Ancien dépôt, une fois tout vérifié :
   https://github.com/lou-heraut/collectif-articho/settings/pages, *Branch* :
   **None**, **Save** (il n'est plus publié nulle part) ; puis *Settings*,
   *General*, tout en bas, **Archive this repository**. Il reste lisible, avec
   son historique et les photos originales.

## Revenir en arrière

Sur le nouveau dépôt (compte de la SCOP), *Custom domain*, **Remove** ; sur
l'ancien (compte de Louis), remettre `collectifarticho.com` et **Save**. Le DNS
n'a pas bougé, il n'y a rien d'autre à défaire.
