# Guide du site, pour les membres de la SCOP

`guide-du-site.pdf` : une affiche A3 paysage (vue d'ensemble : ce qui se fait
dans l'administration, ce qui ne s'y fait pas) et trois fiches A4 paysage (le
jeton, ajouter un projet, modifier et réparer). C'est ce qu'on envoie aux
membres et qu'on imprime ; l'affiche peut aussi s'imprimer en A4, elle reste
lisible. Décision D17 de `ROADMAP.md`.

Sources : `guide.html` (le texte, une `<section>` par page), `guide.css` (la
charte du site : couleurs, polices Faune, dessins de `static/resources/`),
captures dans `images/`. L'adresse donnée aux membres est celle d'après la
bascule, `collectifarticho.com/admin`.

## Réimprimer le PDF après une modification

Depuis la racine du dépôt (le serveur local sert les polices de
`static/resources/fonts/` ; chromium, installé en snap, n'écrit pas dans
`/tmp`) :

```sh
python3 -m http.server 8004 &
chromium --headless=new --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf=$HOME/snap/chromium/common/guide.pdf \
  http://localhost:8004/docs/guide/guide.html
mv $HOME/snap/chromium/common/guide.pdf docs/guide/guide-du-site.pdf
```

Les formats de page (A3 puis A4) sont donnés par `@page` dans `guide.css`.

## Refaire les captures

Prises le 2026-10-03 avec Sveltia 0.221.1, sans jeton : Sveltia a un dépôt de
test intégré au navigateur. Dans une copie de `static/admin/config.yml`,
remplacer le bloc `backend` par `backend: { name: test-repo }`, servir cette
copie en local, cliquer sur « Travailler avec un dépôt de test », puis y
déposer les fichiers de `content/` (ils vivent dans le stockage du navigateur,
rien n'est envoyé à GitHub). Fenêtre de 1280 × 800, écran en double densité.
L'écran de connexion vient de la vraie page `/admin/`, servie depuis `public/`.

Les repères numérotés sont placés en pourcentage de chaque image, dans
`guide.html` : les recaler si une capture change de cadrage.
