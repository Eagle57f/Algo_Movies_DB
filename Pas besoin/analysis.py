import get_infos

ANNEE_MIN_DEFAUT = 1960
ANNEE_MAX_DEFAUT = 2022


def filtrer_par_annee(
    elements,
    annee_min=ANNEE_MIN_DEFAUT,
    annee_max=ANNEE_MAX_DEFAUT,
):
    """Garde les elements compris entre deux annees incluses."""
    if annee_min > annee_max:
        raise ValueError("annee_min doit etre inferieure ou egale a annee_max")

    return [
        element for element in elements
        if annee_min <= element.release_year <= annee_max
    ]


def compter_genres(elements):
    compteurs = {}

    for element in elements:
        for genre in element.genres:
            if genre not in compteurs:
                compteurs[genre] = 0
            compteurs[genre] += 1

    return compteurs


def genres_les_plus_presents(elements, nombre=None):
    if not elements:
        return []

    compteurs = compter_genres(elements)
    genres_tries = sorted(
        compteurs.items(),
        key=lambda genre_et_compte: (-genre_et_compte[1], genre_et_compte[0]),
    )

    resultat = []
    for genre, compte in genres_tries:
        resultat.append(
            {
                "genre": genre,
                "nombre": compte,
                "pourcentage": round(100 * compte / len(elements), 2),
            }
        )

    if nombre is not None:
        return resultat[:nombre]
    return resultat


def genres_par_ranking(
    animes,
    ranking=None,
    nombre=None,
    annee_min=ANNEE_MIN_DEFAUT,
    annee_max=ANNEE_MAX_DEFAUT,
):
    animes = filtrer_par_annee(animes, annee_min, annee_max)
    ratings = get_infos.Animes.RATING_ORDER
    if ranking is None:
        ratings_a_analyser = ratings
    elif isinstance(ranking, str):
        ratings_a_analyser = [ranking]
    else:
        ratings_a_analyser = ranking

    resultat = {}
    for rating in ratings_a_analyser:
        rating = "pg_13" if rating == "pg13" else rating
        if rating not in ratings:
            raise ValueError("Ranking inconnu : " + rating)

        groupe = [
            anime for anime in animes
            if anime.rating == rating
        ]
        resultat[rating] = genres_les_plus_presents(groupe, nombre)

    return resultat


def regrouper_par(elements, attribut):
    groupes = {}

    for element in elements:
        valeurs = getattr(element, attribut)
        if not isinstance(valeurs, list):
            valeurs = [valeurs]

        for valeur in valeurs:
            if valeur not in groupes:
                groupes[valeur] = []
            groupes[valeur].append(element)

    return groupes


def genres_par_directeur(
    films,
    directeur=None,
    nombre=None,
    annee_min=ANNEE_MIN_DEFAUT,
    annee_max=ANNEE_MAX_DEFAUT,
):
    films = filtrer_par_annee(films, annee_min, annee_max)
    groupes = regrouper_par(films, "directors")

    if directeur is not None:
        if directeur not in groupes:
            return []
        return genres_les_plus_presents(groupes[directeur], nombre)

    resultat = {}

    for directeur in sorted(groupes):
        resultat[directeur] = genres_les_plus_presents(
            groupes[directeur],
            nombre,
        )

    return resultat


def genres_par_annee(
    elements,
    annee=None,
    nombre=None,
    annee_min=ANNEE_MIN_DEFAUT,
    annee_max=ANNEE_MAX_DEFAUT,
):
    elements = filtrer_par_annee(elements, annee_min, annee_max)
    groupes = regrouper_par(elements, "release_year")

    if annee is not None:
        if annee not in groupes:
            return []
        return genres_les_plus_presents(groupes[annee], nombre)

    resultat = {}

    for annee in sorted(groupes):
        resultat[annee] = genres_les_plus_presents(groupes[annee], nombre)

    return resultat


def afficher_genres(resultat):
    if isinstance(resultat, list):
        for genre in resultat:
            print(
                genre["genre"],
                "-",
                genre["nombre"],
                "elements (",
                genre["pourcentage"],
                "%)",
            )
        return

    for groupe, genres in resultat.items():
        print("\n" + str(groupe) + " :")
        afficher_genres(genres)





animes = get_infos.Animes(get_infos.animes).list
films = get_infos.Movies(get_infos.movies).list

# afficher_genres(genres_par_ranking(animes, "r", nombre=5))
# afficher_genres(
#     genres_par_directeur(films, directeur="Christopher Nolan", nombre=3)
# )
# afficher_genres(genres_par_annee(animes, annee=2010, nombre=1))