// Menus déroulants de l'en-tête et survol des icônes du pied de page.
// L'en-tête, le pied de page et l'onglet actif sont produits par Hugo.

function showMenu(menuId) {
    var menu = document.getElementById(menuId);
    if (menu) {
        menu.style.display = 'block';
    }
}

function hideMenu(menuId) {
    var menu = document.getElementById(menuId);
    if (menu) {
        menu.style.display = 'none';
    }
}

function changeImage(img, suffix) {
    var originalSrc = img.src;
    var dotIndex = originalSrc.lastIndexOf('.');
    var path = originalSrc.substring(0, dotIndex);
    var extension = originalSrc.substring(dotIndex);
    img.src = path + suffix + extension;
}

function restoreImage(img, suffix) {
    img.src = img.src.replace(suffix, '');
}
