import requests
from bs4 import BeautifulSoup
import csv
import os
import re


def scraper_livre(url_livre):
    # définition de la fonction scraper_livre pour obtenir toutes les données de ce livre

    donnees_livre = {}  # création de la variable de retour
    page = requests.get(url_livre)  # extraction du code HTML du livre
    donnees_livre["product_page_url"] = url_livre
    soup = BeautifulSoup(page.content, "html.parser")  # transformation du code HTML du livre en objet soup

    # extraction de toutes les données du livre
    tds = soup.findAll("td")
    ths = soup.findAll("th")
    info = {}
    for th, td in zip(ths, tds):
        info[th.string] = td.string

    donnees_livre["universal_product_code"] = info["UPC"]

    titre = soup.find("h1")
    donnees_livre["title"] = titre.string

    donnees_livre["price_including_tax"] = info["Price (incl. tax)"]
    donnees_livre["price_excluding_tax"] = info["Price (excl. tax)"]
    donnees_livre["number_available"] = info["Availability"]

    description = soup.find("div", class_="sub-header").findNext("p")
    donnees_livre["product_description"] = description.string

    categorie = soup.find("ul", class_="breadcrumb").findChildren("a")
    donnees_livre["category"] = categorie[2].text

    donnees_livre["review_rating"] = info["Number of reviews"]

    img = soup.find("div", class_="item active").find("img")
    lien_img = img["src"]
    lien_img = lien_img.replace("../../", "http://books.toscrape.com/")
    donnees_livre["image_url"] = lien_img

    return donnees_livre


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


def scraper_site(url_site):
    # définition de la fonction scraper_site pour obtenir le dictionnaire des catégories

    page = requests.get(url_site)  # extraction du code HTML du site
    soup = BeautifulSoup(page.content, "html.parser")  # transformation du code HTML en objet soup

    # extraction des url de chaque catégorie
    navigation = soup.find("ul", class_="nav nav-list").find("ul").findAll("li")
    categories = {}
    for categorie in navigation:
        nom_cat = categorie.find("a").string
        nom_cat = nom_cat.replace("\n                            \n                                ", "")
        nom_cat = nom_cat.replace("\n                            \n                        ", "")
        url_cat = categorie.find("a")["href"]
        url_cat = url_site + url_cat
        categories[nom_cat] = url_cat

    return categories


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


# création d'un dossier data
chemin = os.getcwd()
os.mkdir("data")
chemin = os.path.join(chemin, "data")
os.chdir(chemin)

# extraction des données des livres pour chaque catégorie
for categorie, url_categorie in scraper_site("http://books.toscrape.com/").items():
    livres_cat = scraper_categorie(url_categorie)
    print("Dans la catégorie " + categorie + ", il y a " + str(len(livres_cat)) + " livres")

    # création d'un dossier pour la catégorie
    os.mkdir(categorie)
    path = os.path.join(chemin, categorie)
    os.chdir(path)

    # chargement des donnees dans un fichier CSV
    print("Création du fichier csv contenant les données de chaque livre")
    donnees = {"product_page_url": 0, "universal_product_code": 0, "title": 0, "price_including_tax": 0, "price_excluding_tax": 0,
               "number_available": 0, "product_description": 0, "category": 0, "review_rating": 0, "image_url": 0}
    with open(categorie + ".csv", "w", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.DictWriter(fichier_csv, donnees)
        writer.writeheader()
        for url in livres_cat:
            writer.writerow(scraper_livre(url))

    # extraction des images de couverture
    print("Extraction des images de couverture")
    for url in livres_cat:
        telecharger_images(url)

    os.chdir(chemin)
    print("passage à la catégorie suivante")
