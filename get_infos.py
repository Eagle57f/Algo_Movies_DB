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


class Anime:
    def __init__(self, line: list):
        self.title = line[0]
        self.status = line[1]
        self.media_type = line[2]
        self.num_episodes = int(line[3])
        self.vote_average = float(line[4])
        self.source = line[5]
        self.rating = line[6]
        self.release_year = int(line[7])
        self.genres = ast.literal_eval(line[8])
        self.studios = ast.literal_eval(line[9])
        self.picture = line[10]


class Animes:
    RATING_ORDER = ("g", "pg", "pg_13", "r", "r+", "rx")

    def __init__(self, data):
        self.list = [Anime(line) for line in data[1:] if len(line) == 11]

    def get_by_criteria(
        self,
        title: str = "",
        genres=None,
        studios=None,
        min_vote_average=None,
        max_vote_average=None,
        min_release_year=None,
        max_release_year=None,
        min_rating=None,
        max_rating=None,
    ):
        if isinstance(genres, str):
            genres = [genres]
        if isinstance(studios, str):
            studios = [studios]
        min_rating_index = (
            self.RATING_ORDER.index(min_rating)
            if min_rating in self.RATING_ORDER
            else None
        )
        max_rating_index = (
            self.RATING_ORDER.index(max_rating)
            if max_rating in self.RATING_ORDER
            else None
        )

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
            and (
                min_rating_index is None
                or (
                    item.rating in self.RATING_ORDER
                    and self.RATING_ORDER.index(item.rating)
                    >= min_rating_index
                )
            )
            and (
                max_rating_index is None
                or (
                    item.rating in self.RATING_ORDER
                    and self.RATING_ORDER.index(item.rating)
                    <= max_rating_index
                )
            )
        ]
