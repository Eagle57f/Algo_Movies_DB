import csv
import ast
from pathlib import Path

DATA_DIR = Path(__file__).parent

with open(DATA_DIR / "movies.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    movies = list(reader)





class Movie:
    def __init__(self, line: list):
        self.popularity = float(line[0])
        self.title = line[1]
        self.cast = line[2].split("|")
        self.directors = line[3].split("|")
        self.keywords = line[4].split("|")
        self.runtime = int(line[5])
        self.genres = line[6].split("|")
        self.studios = line[7].split("|")
        self.vote_count = int(line[8])
        self.vote_average = float(line[9])
        self.release_year = int(line[10])


class Movies:
    def __init__(self, data):
        self.list = [Movie(line) for line in data[1:]]

    def get_by_criteria(
        self,
        title: str = "",
        genres=None,
        studios=None,
        min_vote_average=None,
        max_vote_average=None,
        min_release_year=None,
        max_release_year=None,
    ):
        if isinstance(genres, str):
            genres = [genres]
        if isinstance(studios, str):
            studios = [studios]
        genres_lowered = [genre.lower() for genre in genres] if genres else []
        studios_lowered = [studio.lower() for studio in studios] if studios else []
        return [
            item for item in self.list
            if (not title or title.lower() in item.title.lower())
            and (not genres or all(genre.lower() in genres_lowered for genre in genres))
            and (not studios or all(studio.lower() in studios_lowered for studio in studios))
            and (
                min_vote_average is None
                or item.vote_average >= min_vote_average
            )
            and (
                max_vote_average is None
                or item.vote_average <= max_vote_average
            )
            and (
                min_release_year is None
                or item.release_year >= min_release_year
            )
            and (
                max_release_year is None
                or item.release_year <= max_release_year
            )
        ]



def by_attributes():
    movie_list = Movies(movies)
    
    print("Pour chaque question, appuyez sur Enter pour passer.")

    title_input = input("Quel est le titre de votre film ?\nVotre réponse : ")
    title = title_input if title_input != "" else None
    
    genres_input = input("Donnez un ou plusieurs genres de votre film. Séparez les genres par '|'.\nVotre réponse : ")
    genres = genres_input.split('|') if genres_input != "" else None
    
    studio_input = input("Quel est le studio de votre film ?\nVotre réponse : ")
    studio = studio_input if studio_input != "" else None

    while True:
        min_vote_average_input = input("Quel est le vote moyen minimum de votre film ?\nVotre réponse : ")
        if min_vote_average_input == "":
            min_vote_average = None
            break
        try:
            min_vote_average = float(min_vote_average_input)
            if 0 <= min_vote_average <= 10:
                break
            print("La note doit être comprise entre 0 et 10.")
        except ValueError:
            print("Veuillez entrer une note comprise entre 0 et 10.")

    while True:
        max_vote_average_input = input("Quel est le vote moyen maximum de votre film ?\nVotre réponse : ")
        if max_vote_average_input == "":
            max_vote_average = None
            break
        try:
            max_vote_average = float(max_vote_average_input)
            if 0 <= max_vote_average <= 10:
                break
            print("La note doit être comprise entre 0 et 10.")
        except ValueError:
            print("Veuillez entrer une note comprise entre 0 et 10.")

    while True:
        min_release_year_input = input("Quel est l'année de sortie minimum de votre film ?\nVotre réponse : ")
        if min_release_year_input == "":
            min_release_year = None
            break
        try:
            min_release_year = int(min_release_year_input)
            if len(min_release_year_input) == 4:
                break
            print("Veuillez entrer une année valide à quatre chiffres.")
        except ValueError:
            print("Veuillez entrer une année valide à quatre chiffres.")

    while True:
        max_release_year_input = input("Quel est l'année de sortie maximum de votre film ?\nVotre réponse : ")
        if max_release_year_input == "":
            max_release_year = None
            break
        try:
            max_release_year = int(max_release_year_input)
            if len(max_release_year_input) == 4:
                break
            print("Veuillez entrer une année valide à quatre chiffres.")
        except ValueError:
            print("Veuillez entrer une année valide à quatre chiffres.")
    
    

    
    returned_movies = movie_list.get_by_criteria(
        title=title,
        genres=genres,
        studios=studio,
        min_vote_average=min_vote_average,
        max_vote_average=max_vote_average,
        min_release_year=min_release_year,
        max_release_year=max_release_year,
    )

    if len(returned_movies) == 0:
        print("Aucun film ne correspond à vos critères.")

    elif len(returned_movies) > 20:
        print(f"{len(returned_movies)} films correspondent à vos critères. Voici les 20 premiers :")
        for i in returned_movies[:20]:
            print(i.title)
        print("Voulez vous préciser vos critères ? (oui/non)")
        user_input = input("Votre réponse : ")
        while user_input not in ["oui", "non"]:
            print("Réponse non valide. Veuillez répondre par 'oui' ou 'non'.")
            user_input = input("Votre réponse : ")
        if user_input == "oui":
            by_attributes()
    else:
        print(f"{len(returned_movies)} films correspondent à vos critères. Voici la liste :")
        for i in returned_movies:
            print(i.title)
        print("Si vous voulez avoir des informations sur un film, tapez son titre. Sinon, appuyez sur Enter pour quitter.")

        user_input = input("Votre réponse : ")

        while user_input != "":
            found = False
            for movie in movie_list.list:
                if movie.title.lower() == user_input.lower():
                    found = True
                    break
            if found:
                print(movie.title)
                print("Genres : " + ", ".join(movie.genres))
                print("Réalisateurs : " + ", ".join(movie.directors))
                print("Année de sortie : " + str(movie.release_year))
                print("Durée : " + str(movie.runtime) + " minutes")
                print("Vote moyen : " + str(movie.vote_average))
            else:
                print("Film non trouvé. Veuillez vérifier l'orthographe ou appuyez sur Enter pour quitter.")
            user_input = input("Votre réponse : ")
