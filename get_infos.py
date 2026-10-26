import csv

with open("tmdb-movies_full.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    data = list(reader)



def get_genres_list(genres_str):
    return genres_str.split("|")


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


def get_movies_list():
    return [line_to_movie(line) for line in data[1:]]


def get_movie_by_name(movies: list[Movie], name):
    for movie in movies:
        if movie.original_title == name:
            return movie
    return None

def get_movies_by_tags(movies, tags):
    return [movie for movie in movies if all(tag in movie.keywords for tag in tags)]

def get_most_popular_movie(movies):
    return max(movies, key=lambda movie: movie.popularity)


def get_movies_by_director(movies, director_name):
    return [movie for movie in movies if director_name in movie.directors]


def get_movies_by_directors(movies, director_names):
    if isinstance(director_names, str):
        director_names = [director_names]
        
        
    return [movie for movie in movies if all(director in movie.directors for director in director_names)]
