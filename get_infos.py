import csv
import ast
from pathlib import Path

DATA_DIR = Path(__file__).parent

with open(DATA_DIR / "movies.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    movies = list(reader)

with open(DATA_DIR / "animes.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    animes = list(reader)





class Universal_Getters:
    def get_list(self):
        return self.list

    def get_by_name(self, name):
        for i in self.list:
            if i.title == name:
                return i
        return None

    def get_by_genres(self, genres: list):
        if isinstance(genres, str):
            genres = [genres]
        return [i for i in self.list if all(genre in i.genres for genre in genres)]

    def get_by_studios(self, studios: list):
        if isinstance(studios, str):
            studios = [studios]
        return [i for i in self.list if all(studio in i.studios for studio in studios)]

    def get_by_vote_average(self, min_vote_average: float, max_vote_average: float = 10):
        return [i for i in self.list if i.vote_average >= min_vote_average and i.vote_average <= max_vote_average]

    def get_by_release_year(self, min_release_year: int, max_release_year: int = 2024):
        return [i for i in self.list if i.release_year >= min_release_year and i.release_year <= max_release_year]

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

        return [
            item for item in self.list
            if (not title or title.lower() in item.title.lower())
            and (not genres or all(genre in item.genres for genre in genres))
            and (not studios or all(studio in item.studios for studio in studios))
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





class Movie:
    def __init__(self, line:list):
        self.popularity = float(line[0])
        self.title = line[1]
        self.cast=line[2].split("|")
        self.directors=line[3].split("|")   ##
        self.keywords=line[4].split("|")
        self.runtime=int(line[5])
        self.genres=line[6].split("|")      #
        self.studios=line[7].split("|")     #
        self.vote_count=int(line[8])
        self.vote_average=float(line[9])    #
        self.release_year=int(line[10])     #

class Movies(Universal_Getters):
    def __init__(self, data):
        self.list = [Movie(line) for line in data[1:]]

    def get_most_popular(self):
        return max(self.list, key=lambda movie: movie.popularity)

    def get_movies_by_director(self, director_name):
        return [movie for movie in self.list if director_name in movie.directors]

    def get_movies_by_directors(self, director_names):
        if isinstance(director_names, str):
            director_names = [director_names]
        return [movie for movie in self.list if all(director in movie.directors for director in director_names)]


class Anime:
    def __init__(self, line:list):
        self.title=line[0]                  #
        self.status=line[1]
        self.media_type=line[2]
        self.num_episodes=int(line[3])
        self.vote_average=float(line[4])    #
        self.source=line[5]
        self.rating=line[6]
        self.release_year=int(line[7])      #
        self.genres = ast.literal_eval(line[8])
        self.studios = ast.literal_eval(line[9])
        self.picture=line[10]


class Animes(Universal_Getters):
    def __init__(self, data):
        self.list = [Anime(line) for line in data[1:] if len(line) == 11]

    pass
