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
categories = {"nom": "lien"}
for categorie in navigation:
    nom = categorie.find("a").string
    nom = nom.replace("\n                            \n                                ","")
    nom = nom.replace("\n                            \n                        ","")
    lien = categorie.find("a")["href"]
    lien = url + lien
    categories[nom] = lien

print(categories)