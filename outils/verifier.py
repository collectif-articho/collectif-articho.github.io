#!/usr/bin/env python3
"""Contrôles du site construit (D9), à lancer après `hugo` depuis la racine :

    python3 outils/verifier.py

1. Aucun lien interne mort : chaque href/src commençant par « / » dans public/
   doit désigner un fichier construit ou un fichier de static/.
2. Si l'ancien site est à côté (../collectif-articho), chacune de ses pages a
   son équivalent, et chaque titre de son drive/ apparaît dans le site.

Bibliothèque standard seulement. Code de sortie 1 s'il y a un problème.
"""

import html
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

PUBLIC = Path("public")
ANCIEN = Path("../collectif-articho")
# Pages de l'ancien site qui n'ont pas vocation à être reprises.
IGNOREES = {"/pages/default_projet.html", "/pages/default_projets.html",
            "/pages/default_mobiliers.html"}


def nfc(texte):
    return unicodedata.normalize("NFC", texte)


def existe(chemin):
    cible = PUBLIC / unquote(chemin.split("#")[0].split("?")[0]).lstrip("/")
    return cible.is_file() or (cible / "index.html").is_file() or cible.with_suffix(".html").is_file()


def main():
    if not PUBLIC.is_dir():
        sys.exit("public/ absent : lancer `hugo` d'abord.")
    problemes = []

    pages = sorted(PUBLIC.rglob("*.html"))
    textes = {}
    morts = {}
    for page in pages:
        contenu = page.read_text(encoding="utf-8")
        textes[page] = nfc(html.unescape(contenu))
        for lien in set(re.findall(r'(?:href|src)="(/[^"]*)"', contenu)):
            if not lien.startswith("//") and not existe(html.unescape(lien)):
                morts.setdefault(lien, []).append(f"/{page.relative_to(PUBLIC)}")
    for lien, ou in sorted(morts.items()):
        exemple = ou[0] + (f" et {len(ou) - 1} autres pages" if len(ou) > 1 else "")
        problemes.append(f"lien mort : {lien} (dans {exemple})")

    if ANCIEN.is_dir():
        for ancienne in sorted([ANCIEN / "index.html", *(ANCIEN / "pages").rglob("*.html")]):
            url = "/" + str(ancienne.relative_to(ANCIEN))
            if url not in IGNOREES and not existe(url):
                problemes.append(f"page de l'ancien site absente : {url}")
        tout = "\n".join(textes.values())
        for titre in sorted((ANCIEN / "drive").rglob("titre.txt")):
            t = nfc(titre.read_text(encoding="utf-8").strip())
            if t and html.escape(t, quote=False) not in tout and t not in tout:
                problemes.append(f"titre du drive absent du site : {t}")

    print(f"{len(pages)} pages vérifiées.")
    print("\n".join(problemes) or "Aucun problème.")
    sys.exit(1 if problemes else 0)


if __name__ == "__main__":
    main()
