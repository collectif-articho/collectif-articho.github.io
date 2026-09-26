# Modifier le site d'ARTI/CHÔ : mode d'emploi

Tout se fait depuis un navigateur, à cette adresse :

**https://collectif-articho.github.io/admin/**
(elle deviendra **https://collectifarticho.com/admin/** quand le nouveau site
remplacera l'ancien)

Chaque enregistrement est publié tout seul : la modification apparaît sur le site
**une à deux minutes** plus tard. Il n'y a pas de relecture, mais rien n'est
jamais perdu (voir « En cas d'erreur »).

## Se connecter

La première fois sur un ordinateur ou un téléphone :

1. Ouvrir l'adresse ci-dessus.
2. Cliquer sur **« Se connecter avec un jeton d'accès »**.
3. Coller le **jeton** du collectif : une longue suite de caractères qui commence
   par `github_pat_`, rangée avec les mots de passe de la SCOP.

Le navigateur s'en souvient ensuite. Sur un ordinateur partagé, se déconnecter à
la fin (menu en haut à droite).

## Ajouter un projet

1. Dans la colonne de gauche, choisir la rubrique (par exemple **Projets ·
   Aménagements**).
2. Cliquer sur **Nouvelle fiche**.
3. Remplir le **titre** (en majuscules, comme les autres) et le **sous-titre**.
4. Remplir les **informations** utiles (Commanditaire, Date, Localisation…) ;
   laisser vides celles qui ne servent pas. Pour une information qui n'est pas
   dans la liste (Collaboration, Partenaires…), utiliser **Autres informations**.
5. Ajouter les **photos**. La première est la grande photo de la fiche et sa
   vignette dans les listes ; glisser les photos pour changer l'ordre.
6. Écrire le **texte**.
7. **Enregistrer**.

L'adresse de la fiche est tirée du titre au moment de la création, puis ne change
plus, même si le titre change ensuite. Choisir donc un titre juste dès le départ.

**Ordre dans la rubrique** : 1 pour placer la fiche en premier, 2 en deuxième…
Laisser vide pour la placer en fin de liste.

## Les photos

- Les photos du téléphone vont très bien telles quelles : elles sont réduites
  automatiquement avant l'envoi.
- **Sur une connexion lente** (train, 4G faible), ajouter **2 ou 3 photos à la
  fois** et enregistrer entre chaque ajout. Un message « NetworkError » veut dire
  que l'envoi a pris trop de temps : réessayer avec moins de photos d'un coup.

## Mettre en forme un texte

La barre d'outils du texte propose le **gras**, l'*italique*, les listes et les
liens. Un retour à la ligne reste un retour à la ligne ; une ligne vide sépare
deux paragraphes.

## Modifier ou supprimer une fiche

Ouvrir la rubrique, cliquer sur la fiche, modifier, enregistrer. Pour la
supprimer : bouton de suppression dans la fiche ouverte (menu en haut à droite).

## Les pages du site

Dans **Pages du site** : l'accueil (diaporama, textes, boutons, presse, soutiens,
partenaires), le contact, notre offre, les pages Mobiliers et Ateliers, les
textes de la Ligne de mobilier, À propos, les mentions légales et les conditions
générales. On y change textes, photos et listes ; la mise en page, elle, ne bouge
pas.

## En cas d'erreur

Chaque enregistrement est gardé dans l'historique du site : rien n'est perdu,
même une fiche supprimée. Le plus simple est de corriger en modifiant à nouveau.
Pour retrouver une ancienne version, demander à Louis.

## Ce qui ne se fait pas ici

Ajouter ou renommer une rubrique ou un onglet, changer la mise en page ou les
couleurs, déplacer un point de la carte du contact : demander à Louis.

## Renouveler le jeton

Le jeton expire au bout d'un an (la date est notée avec lui). Pour en créer un
nouveau, connecté à GitHub avec le compte **collectif-articho** : *Settings*,
*Developer settings*, *Personal access tokens*, *Fine-grained tokens*,
*Generate new token* ; *Repository access* : seulement
`collectif-articho.github.io` ; *Permissions*, *Contents* : **Read and write**.
Remplacer l'ancien jeton dans les mots de passe de la SCOP, puis se reconnecter
sur chaque appareil avec le nouveau.
