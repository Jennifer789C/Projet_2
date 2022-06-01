import requests
from bs4 import BeautifulSoup
import re


def telecharger_images(url_livre):
    # définition de la fonction telecharger_images pour télécharger toutes les images de couverture des livres d'une catégorie

    page = requests.get(url_livre)  # extraction du code HTML du livre
    soup = BeautifulSoup(page.content, "html.parser")  # transformation du code HTML en objet soup

    # extraction du titre
    titre = soup.find("h1")
    titre = titre.string
    titre = re.sub(r"[^a-zA-Z0-9 ]", "", titre)  # suppression des caractères spéciaux

    # extraction de l'image
    img = soup.find("div", class_="item active").find("img")
    lien_img = img["src"]
    lien_img = lien_img.replace("../../", "http://books.toscrape.com/")
    image = requests.get(lien_img).content

    with open(titre + ".jpg", "wb") as file:
        file.write(image)


def scraper_categorie(url_categorie):
    # définition de la fonction scraper_categorie pour obtenir la liste de toutes les url des livres de cette catégorie

    page = requests.get(url_categorie)  # extraction du code HTML de la catégorie
    soup = BeautifulSoup(page.content, "html.parser")  # transformation du code HTML en objet soup

    # extraction des url des livres de la première page
    livres = soup.findAll("h3")
    url_livres = []
    for livre in livres:
        lien_livre = livre.find("a")["href"]
        lien_livre = lien_livre.replace("../../../", "http://books.toscrape.com/catalogue/")
        url_livres.append(lien_livre)

    # extraction des url des livres des pages suivantes
    page_suivante = soup.find("li", class_="next")
    page_precedente = "index.html"

    while page_suivante:
        lien_page_suivante = page_suivante.find("a")["href"]
        url_categorie = url_categorie.replace(page_precedente, lien_page_suivante)
        page = requests.get(url_categorie)
        soup = BeautifulSoup(page.content, "html.parser")

        page_suivante = soup.find("li", class_="next")  # recherche dans cette page s'il en existe une autre
        page_precedente = lien_page_suivante

        livres = soup.findAll("h3")
        for livre in livres:
            lien_livre = livre.find("a")["href"]
            lien_livre = lien_livre.replace("../../../", "http://books.toscrape.com/catalogue/")
            url_livres.append(lien_livre)

    return url_livres


# extraction des images d'une catégorie
for url in scraper_categorie("http://books.toscrape.com/catalogue/category/books/travel_2/index.html"):
    telecharger_images(url)
