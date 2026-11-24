import csv

with open("tmdb-movies.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    data = list(reader)

# Afficher les 3 premiers films

print(data[1:4])

# Afficher le titre du 2ème film

print(data[2][1])

# Afficher le titre des 3 premiers films

print([data[i][1] for i in range(1, 4)])

# Afficher les genres du 2ème film

print(data[2][6])

# On remarque que les genres sont séparés par le caractère "|".
# En utilisant split(), afficher les genres du 2ème film sous forme de liste.

print(data[2][6].split("|"))

# Ecrire une fonction qui prend en paramètre un string d'éléments séparés par le caractère "|" et qui retourne une liste de ces éléments.

def get_genres_list(genres_str):
    return genres_str.split("|")


# Créer une classe Movie avec les attributs : 
# popularity (float),
# original_title (str),
# cast (list),
# director (list),
# keywords (list),
# runtime (int),
# genres (list),
# production_companies (list),
# vote_count (int),
# vote_average (float),
# release_year (int)

class Movie:
    def __init__(self,
                 popularity:float,
                 original_title:str,
                 cast:list,
                 directors:list,
                 keywords:list,
                 runtime:int,
                 genres:list,
                 production_companies:list,
                 vote_count:int,
                 vote_average:float,
                 release_year:int):
        self.popularity = popularity
        self.original_title = original_title
        self.cast = cast
        self.directors = directors
        self.keywords = keywords
        self.runtime = runtime
        self.genres = genres
        self.production_companies = production_companies
        self.vote_count = vote_count
        self.vote_average = vote_average
        self.release_year = release_year
        

# Créer une fonction qui prend en paramètre une ligne du fichier CSV et qui retourne un objet Movie correspondant à cette ligne,
# en transformant les chaînes de caractères en types appropriés.

def line_to_movie(line):
    return Movie(
        popularity=float(line[0]),
        original_title=line[1],
        cast=line[2].split("|"),
        directors=line[3].split("|"),
        keywords=line[4].split("|"),
        runtime=int(line[5]),
        genres=line[6].split("|"),
        production_companies=line[7].split("|"),
        vote_count=int(line[8]),
        vote_average=float(line[9]),
        release_year=int(line[10])
    )

print(line_to_movie(data[1]).__dict__) # __dict__ permet d'afficher tout les attributs d'un objet et leurs valeurs, sous forme de dictionnaire.


# Créer une fonction qui retourne une liste d'objets Movie, à partir des données du fichier tmdb-movies.csv.

def get_movies_list():
    return [line_to_movie(line) for line in data[1:]]

# Créer une fonction qui prend en paramètres une liste d'objets Movie et un nom de film, et qui renvoie l'objet Movie ayant ce nom.

def get_movie_by_name(movies: list[Movie], name):
    for movie in movies:
        if movie.original_title == name:
            return movie
    return None

# Créer une fonction qui prend en paramètre une liste d'objets Movie et qui retourne l'objet Movie correspondant au film le plus populaire
# (celui avec la plus grande valeur de l'attribut popularity).

def get_most_popular_movie(movies):
    return max(movies, key=lambda movie: movie.popularity) # key permet de spécifier la fonction à utiliser pour comparer les éléments de
                                                           # la liste. Ici, on compare les objets Movie selon leur attribut popularity.

print(get_most_popular_movie(get_movies_list()))
print(get_most_popular_movie(get_movies_list()).original_title) # Pour afficher le titre pour vérifier

# Créer une fonction qui prend en paramètre une liste d'objets Movie et le nom d'un réalisateurs (str), et qui retourne la liste des films
# de ce réalisateurs et leur nombre.

def get_movies_by_director(movies, director_name):
    return [movie for movie in movies if director_name in movie.directors]

# Créer une fonction qui prend en paramètre une liste d'objets Movie et les noms d'un ou plusieurs réalisateurs (str ou list),
# et qui retourne la liste des films de ces réalisateurs et leur nombre.
# Si on donne plusieurs réalisateurs, il faut seulement retourner les films qui ont été réalisés par tous ces réalisateurs en même temps.

print(get_movies_by_director(get_movies_list(), "Christopher Ray"))


def get_movies_by_directors(movies, director_names):
    if isinstance(director_names, str): # isinstance() permet de vérifier le type d'une variable. Ici, on vérifie si director_names est une
                                        # chaîne de caractères (str).
        director_names = [director_names] # Si c'est le cas, on le transforme en liste contenant un seul élément, pour pouvoir utiliser la
                                          # même logique que pour une liste de plusieurs réalisateurs.

    return [movie for movie in movies if all(director in movie.directors for director in director_names)] # all() permet de vérifier si tout
                                        # les éléments d'un itérable (ici, la liste des réalisateurs du film) satisfont une condition
                                        # (ici, être dans la liste des réalisateurs recherchés). Si c'est le cas, le film est ajouté à la
                                        # liste retournée.
                                        
print(get_movies_by_directors(get_movies_list(), ["Obin Olson", "Amariah Olson"]))
print([movie.original_title for movie in get_movies_by_directors(get_movies_list(), ["Obin Olson", "Amariah Olson"])]) # Pour afficher les titres des films pour vérifier
                                        
