import math


TAGS = [
    "Thriller", "War", "Action", "Western", "Comedy", "Fantasy",
    "Foreign", "Family", "TV Movie", "Science Fiction", "Documentary",
    "Crime", "Animation", "Romance", "Horror", "Music", "Drama",
    "Adventure", "Mystery",
]
TAG_INDEX = {tag: i for i, tag in enumerate(TAGS)}



class Question:
    def __init__(self, question, answers, weights):
        self.question = question
        self.answers = answers
        self.weights = weights

QUESTIONS = [
    Question(
        "Dans une ville inconnue, que voulez-vous découvrir ?",
        [
            "Une affaire criminelle pleine de secrets",
            "Des rues étranges peuplées de créatures",
            "Des habitants et leur quotidien",
        ],
        [
            {"Crime": 1, "Mystery": .9, "Thriller": .7},
            {"Fantasy": 1, "Horror": .6, "Mystery": .5},
            {"Drama": .8, "Documentary": .5, "Foreign": .4},
        ],
    ),

    Question(
        "Quel type de danger rend un film captivant ?",
        [
            "Une guerre imminente",
            "Une menace invisible qui se rapproche",
            "Un monde qui s'effondre à cause de la technologie",
        ],
        [
            {"War": 1, "Action": .7, "Drama": .6},
            {"Thriller": 1, "Horror": .7, "Mystery": .6},
            {"Science Fiction": 1, "Thriller": .7, "Drama": .5},
        ],
    ),

    Question(
        "Votre soirée idéale ressemble plutôt à...",
        [
            "Une comédie absurde entre amis",
            "Une aventure spectaculaire dans un monde imaginaire",
            "Une histoire d'amour compliquée",
        ],
        [
            {"Comedy": 1, "Family": .3},
            {"Adventure": 1, "Fantasy": .8, "Action": .6},
            {"Romance": 1, "Drama": .8},
        ],
    ),

    Question(
        "Quel personnage vous attire le plus ?",
        [
            "Un détective brillant mais tourmenté",
            "Un guerrier prêt à tout sacrifier",
            "Une personne ordinaire qui découvre un pouvoir extraordinaire",
        ],
        [
            {"Mystery": 1, "Crime": .8, "Drama": .5},
            {"War": .9, "Action": .9, "Drama": .7},
            {"Fantasy": .9, "Adventure": .8, "Family": .3},
        ],
    ),

    Question(
        "Vous préférez voyager...",
        [
            "Dans un pays dont vous ne connaissez pas la culture",
            "Dans une galaxie lointaine",
            "Dans l'Ouest américain du XIXe siècle",
        ],
        [
            {"Foreign": 1, "Drama": .5, "Documentary": .4},
            {"Science Fiction": 1, "Adventure": .8, "Fantasy": .5},
            {"Western": 1, "Action": .7, "Drama": .5},
        ],
    ),

    Question(
        "Quelle émotion voulez-vous ressentir après le film ?",
        [
            "Avoir ri sans pouvoir vous arrêter",
            "Avoir eu peur de regarder derrière vous",
            "Être profondément ému",
        ],
        [
            {"Comedy": 1},
            {"Horror": 1, "Thriller": .8, "Mystery": .4},
            {"Drama": 1, "Romance": .5, "War": .3},
        ],
    ),

    Question(
        "Quel décor semble le plus intéressant ?",
        [
            "Un manoir isolé pendant une tempête",
            "Une jungle remplie de ruines anciennes",
            "Une banlieue familiale en apparence parfaite",
        ],
        [
            {"Horror": .9, "Mystery": .9, "Thriller": .7},
            {"Adventure": 1, "Fantasy": .7, "Action": .5},
            {"Drama": .8, "Mystery": .7, "Crime": .5},
        ],
    ),

    Question(
        "Quel conflit vous intéresse le plus ?",
        [
            "Deux familles qui se déchirent",
            "Un héros contre une organisation puissante",
            "L'humanité contre une intelligence artificielle",
        ],
        [
            {"Drama": 1, "Romance": .6, "Crime": .4},
            {"Action": .9, "Thriller": .9, "Crime": .7},
            {"Science Fiction": 1, "Thriller": .7, "Drama": .5},
        ],
    ),

    Question(
        "Que regarderiez-vous un dimanche après-midi ?",
        [
            "Un film animé drôle et inventif",
            "Un documentaire sur un sujet fascinant",
            "Une aventure légère avec des héros attachants",
        ],
        [
            {"Animation": 1, "Comedy": .7, "Family": .7, "Fantasy": .4},
            {"Documentary": 1},
            {"Adventure": .8, "Family": .8, "Comedy": .5},
        ],
    ),

    Question(
        "Quelle relation voulez-vous suivre ?",
        [
            "Un couple qui tente de se retrouver",
            "Un groupe de survivants qui doit coopérer",
            "Une famille qui cache un lourd secret",
        ],
        [
            {"Romance": 1, "Drama": .8},
            {"Horror": .7, "Thriller": .7, "Action": .6, "Drama": .5},
            {"Drama": .9, "Mystery": .8, "Crime": .5},
        ],
    ),

    Question(
        "Quel type de héros préférez-vous ?",
        [
            "Un hors-la-loi charismatique",
            "Un scientifique qui remet le monde en question",
            "Un parent maladroit mais attachant",
        ],
        [
            {"Western": .9, "Crime": .8, "Action": .5},
            {"Science Fiction": .9, "Mystery": .6, "Drama": .4},
            {"Family": 1, "Comedy": .8, "Drama": .4},
        ],
    ),

    Question(
        "Quel film choisir pour plusieurs générations ?",
        [
            "Une aventure fantastique accessible à tous",
            "Une comédie avec des personnages décalés",
            "Un film d'animation visuellement spectaculaire",
        ],
        [
            {"Family": 1, "Fantasy": .8, "Adventure": .8},
            {"Comedy": 1, "Family": .6},
            {"Animation": 1, "Fantasy": .7, "Adventure": .6},
        ],
    ),

    Question(
        "Quel mystère vous intrigue le plus ?",
        [
            "Une disparition jamais résolue",
            "Une maison qui semble vivante",
            "Un signal venu d'une autre planète",
        ],
        [
            {"Mystery": 1, "Thriller": .8, "Crime": .7},
            {"Horror": 1, "Mystery": .8, "Fantasy": .4},
            {"Science Fiction": 1, "Mystery": .8, "Adventure": .5},
        ],
    ),

    Question(
        "Quelle bande originale vous attire ?",
        [
            "Des chansons qui font avancer l'histoire",
            "Une musique épique pendant une bataille",
            "Des chansons entraînantes dans une comédie",
        ],
        [
            {"Music": 1, "Drama": .6, "Romance": .5},
            {"War": .8, "Action": .8, "Music": .7},
            {"Music": .8, "Comedy": .9},
        ],
    ),

    Question(
        "Dans quel monde aimeriez-vous passer deux heures ?",
        [
            "Un royaume magique avec des créatures étranges",
            "Une société futuriste très contrôlée",
            "Une petite ville réaliste avec des personnages complexes",
        ],
        [
            {"Fantasy": 1, "Adventure": .8, "Animation": .3},
            {"Science Fiction": 1, "Thriller": .8, "Drama": .5},
            {"Drama": .9, "Foreign": .4, "Mystery": .4},
        ],
    ),

    Question(
        "Quel événement historique vous intéresse ?",
        [
            "Une grande bataille racontée de l'intérieur",
            "La conquête d'un territoire sauvage",
            "La vie quotidienne de personnes oubliées",
        ],
        [
            {"War": 1, "Drama": .8, "Action": .6},
            {"Western": .9, "Adventure": .8, "Drama": .5},
            {"Documentary": 1, "Drama": .6, "Foreign": .5},
        ],
    ),

    Question(
        "Quel type de tension préférez-vous ?",
        [
            "Ne pas savoir qui dit la vérité",
            "Sentir qu'une créature peut surgir à tout moment",
            "Voir deux adversaires se préparer à s'affronter",
        ],
        [
            {"Mystery": .9, "Thriller": 1, "Drama": .5},
            {"Horror": 1, "Thriller": .8},
            {"Action": 1, "War": .7, "Western": .4},
        ],
    ),

    Question(
        "Quelle histoire d'amour vous attire ?",
        [
            "Deux personnes que tout oppose",
            "Un amour impossible dans un monde fantastique",
            "Une relation drôle, chaotique et imprévisible",
        ],
        [
            {"Romance": 1, "Drama": .8},
            {"Romance": .9, "Fantasy": .8, "Drama": .6},
            {"Romance": .8, "Comedy": .9},
        ],
    ),

    Question(
        "Quel film pourrait changer votre perspective ?",
        [
            "Un documentaire sur un enjeu de société",
            "Une fiction sur une guerre vue par des civils",
            "Une histoire de science-fiction sur l'avenir de l'humanité",
        ],
        [
            {"Documentary": 1, "Drama": .5},
            {"War": .9, "Drama": 1, "Foreign": .5},
            {"Science Fiction": 1, "Drama": .7, "Mystery": .4},
        ],
    ),

    Question(
        "Quelle expérience voulez-vous vivre ?",
        [
            "Être complètement absorbé par une enquête",
            "Sortir du film avec le sourire",
            "Ne plus oser éteindre la lumière",
        ],
        [
            {"Mystery": 1, "Crime": .8, "Thriller": .8},
            {"Comedy": 1, "Family": .5, "Romance": .3},
            {"Horror": 1, "Thriller": .8, "Mystery": .6},
        ],
    ),
]


def ask_get():
    responses = []
    for i in range(len(QUESTIONS)):
        print(str(i+1) + ". " + QUESTIONS[i].question)
        for j in range(0,3):
            print("  " + str(j+1) + " - " + QUESTIONS[i].answers[j])
        response = input("Votre choix : ")
        while response not in ["1", "2", "3"]:
            print("Mauvaise saisie. Répondez par 1, 2 ou 3.")
            response = input("Votre choix : ")
        responses.append(int(response))
    return responses




def responses_to_weight_dict(responses):
    responses_weights_dict = {}
    for i in range(len(responses)):
        r_weights = QUESTIONS[i].weights[responses[i]-1]
        for key, value in r_weights.items():
            if key not in responses_weights_dict.keys():
                responses_weights_dict[key] = [value]
            else:
                responses_weights_dict[key].append(value)

    return responses_weights_dict


def user_vector(answers:dict, tau=2.0):
    """Construit un vecteur utilisateur normalisé entre 0 et 1.

    Le score combine :
      - la moyenne des valeurs du tag ;
      - le nombre d'observations du tag.

    tau contrôle l'influence du nombre d'observations.
    Plus tau est petit, plus quelques observations suffisent à obtenir
    une confiance élevée.
    """
    raw_scores = {}

    for tag in TAGS:
        values = answers.get(tag, [])

        if not values:
            raw_scores[tag] = 0.0
            continue # On passe à l'itération suivante de la boucle for sans terminer les calculs de l'itération actuelle.

        average = sum(values) / len(values)

        # La confiance augmente avec le nombre de réponses.
        confidence = 1.0 - math.exp(-len(values) / tau)
        score = average * confidence

        raw_scores[tag] = score

    # Normalisation : le meilleur tag vaut 1.0.
    maximum = max(raw_scores.values())

    profile = {tag: round(score / maximum, 4) for tag, score in raw_scores.items()}

    return profile
        

def ask_user():
    return user_vector(responses_to_weight_dict(ask_get()))



from by_attributes import Movie, Movies, movies


movies_list = Movies(movies)
def movies_vectors():
    movies_tags = {}
    for film in movies_list.list:
        movies_tags[film.title] = {}
        for tag in film.genres:
            movies_tags[film.title][tag] = 1
    
    return movies_tags





def knn_movies(movies_vectors, user_vector, k=10):
    distances = {}

    for movie_name, movie_vector in movies_vectors.items():
        distance = 0.0

        for tag, user_score in user_vector.items():
            movie_score = movie_vector.get(tag, 0.0)

            distance += (user_score - movie_score) ** 2

        distances[movie_name] = math.sqrt(distance)

    # Tri par distance croissante
    sorted_distances = sorted(
        distances.items(),
        key=lambda item: item[1]
    )

    # Conservation des k films les plus proches
    return dict(sorted_distances[:k])




def display_best():
    mv = movies_vectors()
    au = ask_user()
    print("Les films qui vous correspondent le mieux :")
    for film in knn_movies(mv, au).keys():
        print(film)

