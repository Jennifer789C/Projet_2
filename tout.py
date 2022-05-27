import requests
from bs4 import BeautifulSoup
import csv

# extraction du code HTML de la page d'accueil du site
url = "http://books.toscrape.com/"
page = requests.get(url)

# transformation du code HTML en objet BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")

# extraction des url des pages Categories
navigation = soup.find("ul", class_="nav nav-list").find("ul").findAll("li")
categories = {}
for categorie in navigation:
    nom = categorie.find("a").string
    nom = nom.replace("\n                            \n                                ","")
    nom = nom.replace("\n                            \n                        ","")
    lien = categorie.find("a")["href"]
    lien = url + lien
    categories[nom] = lien

# etl des donnees pour chaque categorie
donnees = {"product_page_url":0, "universal_product_code":0, "title":0, "price_including_tax":0, "price_excluding_tax":0, "number_available":0, "product_description":0, "category":0, "review_rating":0, "image_url":0}
for categorie, lien_categorie in categories.items():
    page = requests.get(lien_categorie)
    soup = BeautifulSoup(page.content, "html.parser")

    # extraction des url des pages Produits de la première page
    livres = soup.findAll("h3")
    liens_livres = []
    for livre in livres:
        lien = livre.find("a")["href"]
        lien = lien.replace("../../../", "http://books.toscrape.com/catalogue/")
        liens_livres.append(lien)

    # extraction des url des pages Produits des pages suivantes
    url = lien_categorie
    page_suivante = soup.find("li", class_="next")
    page_precedente = "index.html"

    while page_suivante:
        lien_page_suivante = page_suivante.find("a")["href"]
        url = url.replace(page_precedente, lien_page_suivante)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        page_suivante = soup.find("li", class_="next")  # recherche dans cette page s'il y en existe une autre
        page_precedente = lien_page_suivante

        livres = soup.findAll("h3")
        for livre in livres:
            lien = livre.find("a")["href"]
            lien = lien.replace("../../../", "http://books.toscrape.com/catalogue/")
            liens_livres.append(lien)

    print("Dans la catégorie " + categorie + ", il y a " + str(len(liens_livres)) + " livres")
