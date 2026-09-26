#!/usr/bin/env python3
"""Migration unique du contenu de l'ancien site vers le nouveau (étape 2).

Lit ../collectif-articho/drive/ et les pages qu'il publie, écrit les fiches dans
content/ et leurs photos dans assets/photos/. Bibliothèque standard seulement ;
les photos sont réduites par `mogrify` (ImageMagick).

    python3 migration/migrer.py        # depuis la racine du dépôt

Relançable : les fiches et dossiers de photos migrés sont réécrits, les
_index.md des rubriques ne sont jamais touchés. Rapport en fin d'exécution.
"""

import html
import json
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

ANCIEN = Path("../collectif-articho")
DRIVE = ANCIEN / "drive"
CONTENT = Path("content")
PHOTOS = Path("assets/photos")

IMAGES = {".jpg", ".jpeg", ".png"}
MOGRIFY = ["mogrify", "-auto-orient", "-strip", "-resize", "3000x3000>", "-quality", "88"]

# Intitulés d'information ramenés aux champs nommés de la fiche (D13).
CHAMPS = {
    "commanditaire": "commanditaire",
    "date": "date_projet",
    "localisation": "localisation",
    "localisations": "localisation",
    "intervention": "intervention",
    "materiaux reemployes": "materiaux_reemployes",
    "materiaux de reemploi": "materiaux_reemployes",
    "materiaux neufs": "materiaux_neufs",
    "materiaux neuf": "materiaux_neufs",
}

rapport = []


def nfc(texte):
    return unicodedata.normalize("NFC", texte)


def sans_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    return "".join(c for c in texte if not unicodedata.combining(c))


def to_link(texte):
    """Même slug que to_link() de l'ancien make_projet.R."""
    s = re.sub(r"[‘’ʼ´`']", "-", texte)
    s = sans_accents(s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def libelle(dossier):
    """Nom affiché d'un dossier drive : sans le préfixe NN_, _ en espaces."""
    return nfc(re.sub(r"^\d+_", "", dossier.name).replace("_", " "))


def rang(dossier):
    m = re.match(r"^(\d+)_", dossier.name)
    return int(m.group(1)) if m else 0


def lire(chemin):
    if not chemin.exists():
        return []
    return [nfc(l.strip()) for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]


def yaml(valeur, retrait=0):
    """Sérialise en YAML : chaînes entre guillemets (JSON est du YAML valide)."""
    pad = " " * retrait
    if isinstance(valeur, list):
        lignes = []
        for v in valeur:
            if isinstance(v, dict):
                items = list(v.items())
                lignes.append(f"{pad}- {items[0][0]}: {json.dumps(items[0][1], ensure_ascii=False)}")
                lignes += [f"{pad}  {k}: {json.dumps(x, ensure_ascii=False)}" for k, x in items[1:]]
            else:
                lignes.append(f"{pad}- {json.dumps(v, ensure_ascii=False)}")
        return "\n" + "\n".join(lignes)
    return " " + json.dumps(valeur, ensure_ascii=False)


def ecrire_fiche(chemin, champs, corps=""):
    lignes = ["---"]
    for cle, valeur in champs.items():
        if valeur not in (None, "", []):
            lignes.append(f"{cle}:{yaml(valeur)}")
    lignes.append("---")
    chemin.write_text("\n".join(lignes) + "\n" + (f"\n{corps}\n" if corps else ""), encoding="utf-8")


def texte_markdown(lignes):
    """Un paragraphe par ligne, comme l'ancien site ; HTML brut converti."""
    sortie = []
    for l in lignes:
        l = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", l)
        if "<" in l:
            rapport.append(f"HTML restant dans un texte : {l[:80]}")
        if l.startswith(">"):
            l = "\\" + l  # pas une citation : le « > » était affiché tel quel
        sortie.append(l)
    return "\n\n".join(sortie)


def ordre_publie(page_html, fichiers):
    """Ordre des photos tel que publié par l'ancien site, sinon ordre alphabétique."""
    par_nom = {nfc(f.name): f for f in fichiers}
    ordre = []
    if page_html and page_html.exists():
        for src in re.findall(r'<img[^>]*src="([^"]+)"', page_html.read_text(encoding="utf-8")):
            f = par_nom.get(nfc(html.unescape(src.rsplit("/", 1)[-1])))
            if f and f not in ordre:
                ordre.append(f)
    if len(ordre) != len(fichiers):
        if page_html:
            rapport.append(f"ordre des photos non retrouvé en entier : {page_html}")
        ordre += sorted((f for f in fichiers if f not in ordre), key=lambda f: nfc(f.name))
    return ordre


def migrer_photos(dossier, cible_rel, page_html=None, ordre=None):
    """Copie, renomme et réduit les photos ; renvoie leurs chemins /photos/…"""
    fichiers = [f for f in dossier.iterdir() if f.suffix.lower() in IMAGES]
    fichiers = ordre or ordre_publie(page_html, fichiers)
    cible = PHOTOS / cible_rel
    shutil.rmtree(cible, ignore_errors=True)
    cible.mkdir(parents=True)
    chemins = []
    for f in fichiers:
        ext = ".png" if f.suffix.lower() == ".png" else ".jpg"
        nom = (to_link(f.stem) or "photo") + ext
        base, n = nom, 2
        while (cible / nom).exists():
            nom = base.replace(ext, f"-{n}{ext}")
            n += 1
        if Path(nom).stem != f.stem.lower():
            rapport.append(f"photo renommée : {nfc(f.name)} -> {nom}")
        shutil.copyfile(f, cible / nom)
        chemins.append(f"/photos/{cible_rel}/{nom}")
    if fichiers:
        subprocess.run(MOGRIFY + [str(p) for p in cible.iterdir()], check=True)
    return chemins


def migrer_projet(dossier, rubrique, urls):
    titre = lire(dossier / "titre.txt")
    if not titre:
        rapport.append(f"sans titre, ignoré : {dossier}")
        return
    titre = titre[0]
    url = urls.get(nfc(str(dossier.relative_to(DRIVE))))
    # Le nom de la fiche fait son URL : on reprend celle publiée par l'ancien site.
    slug = url.rsplit("/", 1)[-1].removesuffix(".html") if url else to_link(titre)
    if slug != to_link(titre):
        rapport.append(f"slug repris de l'URL publiée : {slug} (calculé : {to_link(titre)})")
    page_html = ANCIEN / url.lstrip("/") if url else None

    champs = {"title": titre, "sous_titre": (lire(dossier / "soustitre.txt") or [""])[0],
              "weight": rang(dossier)}
    autres = []
    for ligne in lire(dossier / "info.txt"):
        cle, _, valeur = ligne.partition(":")
        cle, valeur = cle.strip(), valeur.strip()
        champ = CHAMPS.get(sans_accents(cle).lower())
        if champ and champ not in champs:
            if sans_accents(cle).lower() not in ("commanditaire", "date", "localisation",
                                                 "intervention", "materiaux reemployes",
                                                 "materiaux neufs"):
                rapport.append(f"intitulé ramené à son champ : « {cle} » ({titre})")
            champs[champ] = valeur
        else:
            autres.append({"intitule": cle, "valeur": valeur})
    if autres:
        champs["autres_infos"] = autres
    champs["photos"] = migrer_photos(dossier, f"{rubrique}/{slug}", page_html)
    ecrire_fiche(CONTENT / rubrique / f"{slug}.md", champs, texte_markdown(lire(dossier / "text.txt")))
    return f"/pages/{rubrique}/{slug}.html"


def ecrire_redirection(ancienne, nouvelle):
    stub = Path("static") / ancienne.lstrip("/")
    stub.parent.mkdir(parents=True, exist_ok=True)
    stub.write_text(f"""<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url={nouvelle}">
        <link rel="canonical" href="{nouvelle}">
        <meta name="robots" content="noindex, follow">
        <title>ARTI/CHÔ</title>
        <script>location.replace("{nouvelle}");</script>
    </head>
    <body><p>Cette page a déménagé : <a href="{nouvelle}">{nouvelle}</a></p></body>
</html>
""", encoding="utf-8")
    rapport.append(f"redirection : {ancienne} -> {nouvelle}")


def liste(valeur):
    """« - a - b » ou « a » en liste ; un tiret collé à un mot n'est pas un séparateur."""
    return [v.strip() for v in re.split(r"(?:^|\s)-\s+", valeur) if v.strip()]


def migrer_meuble(dossier, rubrique, ordre_html):
    titre = lire(dossier / "titre.txt")[0]
    slug = to_link(titre)
    champs = {"title": titre, "weight": rang(dossier)}
    for ligne in lire(dossier / "info.txt"):
        # « Clé : valeur » ou, sans deux-points, « Clé - a - b ».
        m = re.match(r"([^:-]+?)\s*(?::|(?=\s-))\s*(.*)", ligne)
        cle, valeur = sans_accents(m.group(1)).lower(), m.group(2)
        if cle.startswith("modalite"):
            champs["modalite"] = liste(valeur)
        elif cle.startswith("dimensions"):
            champs["dimensions"] = liste(valeur)
        elif cle.startswith("materiaux"):
            champs["materiaux"] = liste(valeur)
        elif cle.startswith("prix"):
            rapport.append(f"prix non migré, non affiché par le site : {titre} ({valeur})")
        else:
            rapport.append(f"information de meuble ignorée : {ligne} ({titre})")
    fichiers = [f for f in dossier.iterdir() if f.suffix.lower() in IMAGES]
    par_nom = {nfc(f.name): f for f in fichiers}
    ordre = [par_nom[n] for n in ordre_html.get(titre, []) if n in par_nom]
    if len(ordre) != len(fichiers):
        rapport.append(f"ordre des photos non retrouvé en entier : meuble {titre}")
        ordre = None
    champs["photos"] = migrer_photos(dossier, f"{rubrique}/{slug}", ordre=ordre or
                                     sorted(fichiers, key=lambda f: nfc(f.name)))
    ecrire_fiche(CONTENT / rubrique / f"{slug}.md", champs)


def ordre_meubles():
    """Photos de chaque meuble dans l'ordre de la page Ligne de mobilier publiée."""
    page = (ANCIEN / "pages/mobiliers/ligne-de-mobilier.html").read_text(encoding="utf-8")
    ordre = {}
    for bloc in page.split('<div class="mobilier">')[1:]:
        titre = nfc(html.unescape(re.search(r"<h2>(.*?)</h2>", bloc).group(1)).strip())
        ordre[titre] = [nfc(html.unescape(s.rsplit("/", 1)[-1]))
                        for s in re.findall(r'class="image active" src="([^"]+)"', bloc)]
    return ordre


def main():
    urls = {}
    for ligne in (ANCIEN / "urls.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        dossier, url = ligne.split("\t")
        urls[nfc(dossier)] = url
    # Redirections (QR code imprimé) : fichiers fixes dans static/, hors de
    # portée du CMS, qui pourrait retirer un champ `aliases` qu'il ne connaît pas.
    for ligne in (ANCIEN / "redirects.txt").read_text(encoding="utf-8").splitlines():
        if ligne.strip() and not ligne.lstrip().startswith("#"):
            ancienne, nouvelle = [c.strip() for c in ligne.split("\t")]
            ecrire_redirection(ancienne, nouvelle)
    meubles = ordre_meubles()

    publiees = []
    for onglet in sorted(p for p in DRIVE.iterdir() if p.is_dir()):
        for sous_onglet in sorted(p for p in onglet.iterdir() if p.is_dir()):
            rubrique = f"{to_link(libelle(onglet))}/{to_link(libelle(sous_onglet))}"
            if not (CONTENT / rubrique / "_index.md").exists():
                rapport.append(f"rubrique sans _index.md, ignorée : {rubrique}")
                continue
            for ancien in (CONTENT / rubrique).glob("*.md"):
                if ancien.name != "_index.md":
                    ancien.unlink()
            for dossier in sorted(p for p in sous_onglet.iterdir() if p.is_dir()):
                if rubrique == "mobiliers/ligne-de-mobilier":
                    migrer_meuble(dossier, rubrique, meubles)
                else:
                    publiees.append(migrer_projet(dossier, rubrique, urls))

    anciennes = set(urls.values())
    for url in sorted(anciennes - set(publiees)):
        rapport.append(f"URL de l'ancien site sans fiche : {url}")
    print(f"{len([p for p in publiees if p])} fiches projet, "
          f"{len(meubles)} meubles attendus.")
    print("\n".join(rapport) or "Rapport vide.")


if __name__ == "__main__":
    main()
