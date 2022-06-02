# OpenClassRooms - Python - Projet 2 : Books to Scrape

Ce projet consiste à extraire toutes les données et l'image de couverture de tous les livres de la bibliothèque http://books.toscrape.com/ 
Ce travail est à faire en plusieurs étapes :
	- extraire les données d'un livre,
	- extraire les données de tous les livres d'une catégorie,
	- extraire les données de tous les livres de toutes les catégories,
	- télécharger les images de couverture de tous les livres.

## Application du script

A partir du terminal, se placer dans le répertoire souhaité

### 1. Récupérer le repository GitHub

Cloner le repository GitHub :
```bash
git clone https://github.com/Jennifer789C/Projet_2.git
```
Puis se placer dans le répertoire du projet :
```bash
cd Projet_2
```

### 2. Créer un environnement virtuel et l'activer

*Pour ma part, je travaille sous Windows et avec l'IDE PyCharm, la création d'un environnement virtuel se fait via les paramètres de l'IDE*

Depuis un terminal sous Windows :
```bash
python -m venv env
env/Scripts/activate
```

Depuis un terminal sous Linux ou Mac :
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Installer et lancer le script

Installer les packages du requirements.txt :
```bash
pip install -r requirements.txt
```
Lancer le script python :

Depuis un terminal sous Windows :
```bash
python script.py
```

Depuis un terminal sous Linux ou Mac :
```bash
python3 script.py
```

## Résultat

La bibliothèque http://books.toscrape.com/ rassemble 1000 livres répartis dans 50 catégories.
En exécutant le script, nous obtenons un dossier data contenant un sous-dossier par catégorie.
Dans chaque dossier catégorie, nous y retrouvons le fichier CSV contenant toutes les données des livres, ainsi que les images de couverture de chaque livre.

