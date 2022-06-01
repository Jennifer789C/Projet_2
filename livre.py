import requests
from bs4 import BeautifulSoup
import csv


def scraper_livre(url_livre):
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


# chargement des donnees du livre dans un fichier CSV
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
with open("donnees_livre.csv", "w", newline="") as fichier_csv:
    writer = csv.DictWriter(fichier_csv, scraper_livre(url))
    writer.writeheader()
    writer.writerow(scraper_livre(url))
