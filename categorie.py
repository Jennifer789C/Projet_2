import requests
from bs4 import BeautifulSoup
import csv

# extraction du code HTML de la categorie Humour
url = "http://books.toscrape.com/catalogue/category/books/humor_30/index.html"
page = requests.get(url)

# transformation du code HTML en objet BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")

# extraction de toutes les url des pages Produits de la categorie Humour (seulement 10 livres = 1 page)
livres = soup.findAll("h3")
liens = []
for livre in livres:
    lien = livre.find("a")["href"]
    lien = lien.replace("../../../", "http://books.toscrape.com/catalogue/")
    liens.append(lien)

# chargement des donnees dans un fichier CSV
donnees = {"product_page_url":0, "universal_product_code":0, "title":0, "price_including_tax":0, "price_excluding_tax":0, "number_available":0, "product_description":0, "category":0, "review_rating":0, "image_url":0}
with open("donnees_categorie.csv", "w", newline="") as fichier_csv:
    writer = csv.DictWriter(fichier_csv, donnees)
    writer.writeheader()

# etl de chaque page Produit de la categorie Humour
    for url in liens:
        page = requests.get(url)
        donnees["product_page_url"] = url

        soup = BeautifulSoup(page.content, "html.parser")

        tds = soup.findAll("td")
        ths = soup.findAll("th")
        info = {}
        for th, td in zip(ths, tds):
            info[th.string] = td.string

        donnees["universal_product_code"] = info["UPC"]

        titre = soup.find("h1")
        donnees["title"] = titre.string

        donnees["price_including_tax"] = info["Price (incl. tax)"]
        donnees["price_excluding_tax"] = info["Price (excl. tax)"]
        donnees["number_available"] = info["Availability"]

        description = soup.find("div", class_="sub-header").findNext("p")
        donnees["product_description"] = description.string

        categorie = soup.find("ul", class_="breadcrumb").findChildren("a")
        donnees["category"] = categorie[2].text

        donnees["review_rating"] = info["Number of reviews"]

        image = soup.find("div", class_="item active").find("img")
        lien = image["src"]
        lien = lien.replace("../../", "http://books.toscrape.com/")
        donnees["image_url"] = lien

        writer.writerow(donnees)
