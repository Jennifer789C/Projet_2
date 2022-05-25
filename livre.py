import requests
from bs4 import BeautifulSoup
import csv

donnees = {}

# extraction du code HTML du livre "Holidays on Ice" categorie Humour
url = "http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html"
page = requests.get(url)
donnees["product_page_url"] = url

# transformation du code HTML en objet BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")

tds = soup.findAll("td")
ths = soup.findAll("th")
info = {}
for th, td in zip (ths, tds):
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
donnees["image_url"] = ("http://books.toscrape.com/" + image["src"])

# chargement des donnees dans un fichier CSV
with open("donnees_livre.csv", "w", newline="") as fichier_csv:
    writer = csv.DictWriter(fichier_csv, donnees)
    writer.writeheader()
    writer.writerow(donnees)