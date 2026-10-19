import csv

with open("tmdb-movies.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    data = list(reader)

# Afficher les 3 premiers films

print(data[1:4])

# Afficher le titre du 2ème film



# Afficher le titre des 3 premiers films



# Afficher les genres du 2ème film



# On remarque que les genres sont séparés par le caractère "|".
# En utilisant split(), afficher les genres du 2ème film sous forme de liste.



# Ecrire une fonction qui prend en paramètre un string d'éléments séparés par le caractère "|" et qui retourne une liste de ces éléments.



# Créer une classe Movie avec les attributs : 
# popularity (float),
# original_title (str),
# cast (list),
# director (list),
# keywords (str),
# runtime (int),
# genres (list),
# production_companies (list),
# vote_count (int),
# vote_average (float),
# release_year (int)



# Créer une fonction qui prend en paramètre une ligne du fichier CSV et qui retourne un objet Movie correspondant à cette ligne,
# en transformant les chaînes de caractères en types appropriés.



# Créer une fonction qui retourne une liste d'objets Movie, à partir des données du fichier tmdb-movies.csv.



# Créer une fonction qui prend en paramètre une liste d'objets Movie et qui retourne l'objet Movie correspondant au film le plus populaire
# (celui avec la plus grande valeur de l'attribut popularity).


# Créer une fonction qui prend en paramètre une liste d'objets Movie et le nom d'un réalisateurs (str), et qui retourne la liste des films
# de ce réalisateurs et leur nombre.



# Créer une fonction qui prend en paramètre une liste d'objets Movie et les noms d'un ou plusieurs réalisateurs (str ou list),
# et qui retourne la liste des films de ces réalisateurs et leur nombre.
# Si on donne plusieurs réalisateurs, il faut seulement retourner les films qui ont été réalisés par tous ces réalisateurs en même temps.


