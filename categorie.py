import requests
from bs4 import BeautifulSoup

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
print(liens)
