from __future__ import annotations

from typing import Dict, List, Mapping, Sequence

import numpy as np
import pandas as pd

import by_attributes

TAGS = [
    "Thriller", "War", "Action", "Western", "Comedy", "Fantasy",
    "Foreign", "Family", "TV Movie", "Science Fiction", "Documentary",
    "Crime", "Animation", "Romance", "Horror", "Music", "Drama",
    "Adventure", "Mystery",
]
TAG_INDEX = {tag: i for i, tag in enumerate(TAGS)}


def weights(**values: float) -> Dict[str, float]:
    """Crée une réponse lisible: weights(Comedy=1, Family=.4)."""
    return {tag: float(value) for tag, value in values.items()}


QUESTIONS = [
    {
        "question": "Dans une ville inconnue, que voulez-vous découvrir ?",
        "answers": [
            weights(Crime=1, Mystery=.9, Thriller=.7),
            weights(Fantasy=1, Horror=.6, Mystery=.5),
            weights(Drama=.8, Documentary=.5, Foreign=.4),
        ],
    },
    {
        "question": "Quel type de danger rend un film captivant ?",
        "answers": [weights(War=1, Action=.7, Drama=.6),
                    weights(Thriller=1, Horror=.7, Mystery=.6),
                    weights(**{"Science Fiction": 1, "Thriller": .7, "Drama": .5})],
    },
    {
        "question": "Votre soirée idéale ressemble plutôt à...",
        "answers": [weights(Comedy=1, Family=.3),
                    weights(Adventure=1, Fantasy=.8, Action=.6),
                    weights(Romance=1, Drama=.8)],
    },
    {
        "question": "Quel personnage vous attire le plus ?",
        "answers": [weights(Mystery=1, Crime=.8, Drama=.5),
                    weights(War=.9, Action=.9, Drama=.7),
                    weights(Fantasy=.9, Adventure=.8, Family=.3)],
    },
    {
        "question": "Vous préférez voyager...",
        "answers": [weights(Foreign=1, Drama=.5, Documentary=.4),
                    weights(**{"Science Fiction": 1, "Adventure": .8, "Fantasy": .5}),
                    weights(Western=1, Action=.7, Drama=.5)],
    },
    {
        "question": "Quelle émotion voulez-vous ressentir après le film ?",
        "answers": [weights(Comedy=1), weights(Horror=1, Thriller=.8, Mystery=.4),
                    weights(Drama=1, Romance=.5, War=.3)],
    },
    {
        "question": "Quel décor semble le plus intéressant ?",
        "answers": [weights(Horror=.9, Mystery=.9, Thriller=.7),
                    weights(Adventure=1, Fantasy=.7, Action=.5),
                    weights(Drama=.8, Mystery=.7, Crime=.5)],
    },
    {
        "question": "Quel conflit vous intéresse le plus ?",
        "answers": [weights(Drama=1, Romance=.6, Crime=.4),
                    weights(Action=.9, Thriller=.9, Crime=.7),
                    weights(**{"Science Fiction": 1, "Thriller": .7, "Drama": .5})],
    },
    {
        "question": "Que regarderiez-vous un dimanche après-midi ?",
        "answers": [weights(Animation=1, Comedy=.7, Family=.7, Fantasy=.4),
                    weights(Documentary=1),
                    weights(Adventure=.8, Family=.8, Comedy=.5)],
    },
    {
        "question": "Quelle relation voulez-vous suivre ?",
        "answers": [weights(Romance=1, Drama=.8),
                    weights(Horror=.7, Thriller=.7, Action=.6, Drama=.5),
                    weights(Drama=.9, Mystery=.8, Crime=.5)],
    },
    {
        "question": "Quel type de héros préférez-vous ?",
        "answers": [weights(Western=.9, Crime=.8, Action=.5),
                    weights(**{"Science Fiction": .9, "Mystery": .6, "Drama": .4}),
                    weights(Family=1, Comedy=.8, Drama=.4)],
    },
    {
        "question": "Quel film choisir pour plusieurs générations ?",
        "answers": [weights(Family=1, Fantasy=.8, Adventure=.8),
                    weights(Comedy=1, Family=.6),
                    weights(Animation=1, Fantasy=.7, Adventure=.6)],
    },
    {
        "question": "Quel mystère vous intrigue le plus ?",
        "answers": [weights(Mystery=1, Thriller=.8, Crime=.7),
                    weights(Horror=1, Mystery=.8, Fantasy=.4),
                    weights(**{"Science Fiction": 1, "Mystery": .8, "Adventure": .5})],
    },
    {
        "question": "Quelle bande originale vous attire ?",
        "answers": [weights(Music=1, Drama=.6, Romance=.5),
                    weights(War=.8, Action=.8, Music=.7),
                    weights(Music=.8, Comedy=.9)],
    },
    {
        "question": "Dans quel monde aimeriez-vous passer deux heures ?",
        "answers": [weights(Fantasy=1, Adventure=.8, Animation=.3),
                    weights(**{"Science Fiction": 1, "Thriller": .8, "Drama": .5}),
                    weights(Drama=.9, Foreign=.4, Mystery=.4)],
    },
    {
        "question": "Quel événement historique vous intéresse ?",
        "answers": [weights(War=1, Drama=.8, Action=.6),
                    weights(Western=.9, Adventure=.8, Drama=.5),
                    weights(Documentary=1, Drama=.6, Foreign=.5)],
    },
    {
        "question": "Quel type de tension préférez-vous ?",
        "answers": [weights(Mystery=.9, Thriller=1, Drama=.5),
                    weights(Horror=1, Thriller=.8),
                    weights(Action=1, War=.7, Western=.4)],
    },
    {
        "question": "Quelle histoire d'amour vous attire ?",
        "answers": [weights(Romance=1, Drama=.8),
                    weights(Romance=.9, Fantasy=.8, Drama=.6),
                    weights(Romance=.8, Comedy=.9)],
    },
    {
        "question": "Quel film pourrait changer votre perspective ?",
        "answers": [weights(Documentary=1, Drama=.5),
                    weights(War=.9, Drama=1, Foreign=.5),
                    weights(**{"Science Fiction": 1, "Drama": .7, "Mystery": .4})],
    },
    {
        "question": "Quelle expérience voulez-vous vivre ?",
        "answers": [weights(Mystery=1, Crime=.8, Thriller=.8),
                    weights(Comedy=1, Family=.5, Romance=.3),
                    weights(Horror=1, Thriller=.8, Mystery=.6)],
    },
]

ANSWER_TEXTS = [
    ["Une affaire criminelle pleine de secrets", "Des rues étranges peuplées de créatures", "Des habitants et leur quotidien"],
    ["Une guerre imminente", "Une menace invisible qui se rapproche", "Un monde qui s'effondre à cause de la technologie"],
    ["Une comédie absurde entre amis", "Une aventure spectaculaire dans un monde imaginaire", "Une histoire d'amour compliquée"],
    ["Un détective brillant mais tourmenté", "Un guerrier prêt à tout sacrifier", "Une personne ordinaire qui découvre un pouvoir extraordinaire"],
    ["Dans un pays dont vous ne connaissez pas la culture", "Dans une galaxie lointaine", "Dans l'Ouest américain du XIXe siècle"],
    ["Avoir ri sans pouvoir vous arrêter", "Avoir eu peur de regarder derrière vous", "Être profondément ému"],
    ["Un manoir isolé pendant une tempête", "Une jungle remplie de ruines anciennes", "Une banlieue familiale en apparence parfaite"],
    ["Deux familles qui se déchirent", "Un héros contre une organisation puissante", "L'humanité contre une intelligence artificielle"],
    ["Un film animé drôle et inventif", "Un documentaire sur un sujet fascinant", "Une aventure légère avec des héros attachants"],
    ["Un couple qui tente de se retrouver", "Un groupe de survivants qui doit coopérer", "Une famille qui cache un lourd secret"],
    ["Un hors-la-loi charismatique", "Un scientifique qui remet le monde en question", "Un parent maladroit mais attachant"],
    ["Une aventure fantastique accessible à tous", "Une comédie avec des personnages décalés", "Un film d'animation visuellement spectaculaire"],
    ["Une disparition jamais résolue", "Une maison qui semble vivante", "Un signal venu d'une autre planète"],
    ["Des chansons qui font avancer l'histoire", "Une musique épique pendant une bataille", "Des chansons entraînantes dans une comédie"],
    ["Un royaume magique avec des créatures étranges", "Une société futuriste très contrôlée", "Une petite ville réaliste avec des personnages complexes"],
    ["Une grande bataille racontée de l'intérieur", "La conquête d'un territoire sauvage", "La vie quotidienne de personnes oubliées"],
    ["Ne pas savoir qui dit la vérité", "Sentir qu'une créature peut surgir à tout moment", "Voir deux adversaires se préparer à s'affronter"],
    ["Deux personnes que tout oppose", "Un amour impossible dans un monde fantastique", "Une relation drôle, chaotique et imprévisible"],
    ["Un documentaire sur un enjeu de société", "Une fiction sur une guerre vue par des civils", "Une histoire de science-fiction sur l'avenir de l'humanité"],
    ["Être complètement absorbé par une enquête", "Sortir du film avec le sourire", "Ne plus oser éteindre la lumière"],
]

def vector_from_weights(values: Mapping[str, float]):
    vector = np.zeros(len(TAGS), dtype=float)
    for tag, value in values.items():
        vector[TAG_INDEX[tag]] = np.clip(value, 0, 1)
    return vector


def user_vector(answer_indexes: Sequence[int]):
    return np.mean([
        vector_from_weights(QUESTIONS[i]["answers"][choice])
        for i, choice in enumerate(answer_indexes)
    ], axis=0)


def parse_tags(value: object) -> List[str]:
    if isinstance(value, list):
        return value
    return value.split("|")


def movie_matrix(movies: pd.DataFrame, tags_column: str = "genres"):
    matrix = np.zeros((len(movies), len(TAGS)), dtype=float)
    for row, tags in enumerate(movies[tags_column].map(parse_tags)):
        for tag in tags:
            if tag in TAG_INDEX:
                matrix[row, TAG_INDEX[tag]] = 1.0
    return matrix


def load_movies() -> pd.DataFrame:
    loaded_movies = by_attributes.Movies(by_attributes.movies).list
    return pd.DataFrame(
        {
            "title": [movie.title for movie in loaded_movies],
            "genres": [movie.genres for movie in loaded_movies],
        }
    )


def recommend(
    movies: pd.DataFrame,
    answers: Sequence[int],
    n: int = 10,
    tags_column: str = "genres",
) -> pd.DataFrame:

    profile = user_vector(answers)
    matrix = movie_matrix(movies, tags_column)

    # Distance cosinus:
    # d(a, b) = 1 - (a . b) / (||a|| * ||b||)
    profile_norm = np.linalg.norm(profile)
    movie_norms = np.linalg.norm(matrix, axis=1)
    denominators = movie_norms * profile_norm
    similarities = np.zeros(len(matrix), dtype=float)
    valid = denominators > 0
    similarities[valid] = (matrix[valid] @ profile) / denominators[valid]
    distances = 1.0 - similarities


    k = min(n, len(movies))
    indices = np.argsort(distances)[:k]

    result = movies.iloc[indices].copy()
    result["distance"] = distances[indices]
    result["score"] = similarities[indices]
    return result.reset_index(drop=True)


def ask_user() -> List[int]:
    answers = []
    for number, item in enumerate(QUESTIONS, start=1):
        print(f"\n{number}. {item['question']}")
        for choice_number, answer_text in enumerate(ANSWER_TEXTS[number - 1], start=1):
            print(f"  {choice_number} - {answer_text}")
        answers.append(int(input("Votre choix: ")) - 1)
    return answers


def main() -> None:
    movies = load_movies()
    recommendations = recommend(movies, ask_user())
    print("\n=== Films recommandés ===")
    for number, movie in recommendations.iterrows():
        print(f"{number + 1}. {movie['title']} (score : {movie['score']:.3f})")


if __name__ == "__main__":
    main()