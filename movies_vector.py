from get_infos import Movie, Movies, movies


movies_list = Movies(movies)
def movies_vectors():
    movies_tags = {}
    for film in movies_list.list:
        movies_tags[film.title] = {}
        for tag in film.genres:
            movies_tags[film.title][tag] = 1
    
    return movies_tags

