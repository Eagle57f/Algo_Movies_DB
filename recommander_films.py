"""Recommande des films a partir des preferences saisies dans le terminal."""

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Film:
    titre: str
    genres: list[str]
    duree: int
    note: float
    annee: int
    popularite: float


def charger_films(chemin: Path | None = None) -> list[Film]:
    """Charge les films du fichier CSV du projet."""
    chemin = chemin or Path(__file__).with_name("movies.csv")
    films = []

    with chemin.open("r", encoding="utf-8", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            try:
                films.append(
                    Film(
                        titre=ligne["original_title"],
                        genres=ligne["genres"].split("|"),
                        duree=int(ligne["runtime"]),
                        note=float(ligne["vote_average"]),
                        annee=int(ligne["release_year"]),
                        popularite=float(ligne["popularity"]),
                    )
                )
            except (KeyError, TypeError, ValueError):
                # Une ligne incomplete ne doit pas empecher les autres films
                # d'etre proposes.
                continue

    return films


def genres_disponibles(films: list[Film], nombre: int = 8) -> list[str]:
    """Retourne les genres les plus frequents, tries alphabetiquement."""
    compteurs: dict[str, int] = {}
    for film in films:
        for genre in film.genres:
            compteurs[genre] = compteurs.get(genre, 0) + 1

    genres_populaires = sorted(
        compteurs,
        key=lambda genre: (-compteurs[genre], genre),
    )
    return sorted(genres_populaires[:nombre])


def demander_choix(message: str, choix: list[str]) -> int:
    """Demande un numero jusqu'a obtenir un choix valide."""
    while True:
        try:
            numero = int(input(message))
            if 1 <= numero <= len(choix):
                return numero - 1
        except ValueError:
            pass
        print("Reponse invalide : choisissez un numero dans la liste.")


def demander_genres(genres: list[str]) -> list[str]:
    """Permet de selectionner plusieurs genres, un par un."""
    selectionnes = []
    choix = genres + ["Terminer"]

    while True:
        print("\nChoisissez un genre (ou 'Terminer').")
        for numero, genre in enumerate(choix, start=1):
            marque = " (deja choisi)" if genre in selectionnes else ""
            print(f"{numero}. {genre}{marque}")

        choix_index = demander_choix("> ", choix)
        genre = choix[choix_index]
        if genre == "Terminer":
            if selectionnes:
                return selectionnes
            print("Choisissez au moins un genre.")
        elif genre not in selectionnes:
            selectionnes.append(genre)
        else:
            print("Ce genre est deja dans votre selection.")


def recommander_films(
    films: list[Film],
    genres_preferes: list[str],
    nouveaute: str,
    confiance: str,
    ambiance: str,
    public: str,
    nombre: int,
) -> list[Film]:
    """Classe les films selon le profil de la seance, puis les renvoie."""
    def score(film: Film) -> tuple[float, float, float, float]:
        score_genre = sum(genre in film.genres for genre in genres_preferes)
        score_ambiance = sum(genre in film.genres for genre in ambiance)
        score_public = sum(genre in film.genres for genre in public)
        score_total = score_genre * 5 + score_ambiance * 2 + score_public

        if nouveaute == "recent" and film.annee >= 2010:
            score_total += 2
        elif nouveaute == "classique" and film.annee < 2010:
            score_total += 2
        if confiance == "valeur_sure":
            score_total += min(film.note, 10) + film.popularite / 10
        else:
            score_total += film.annee / 1000

        return score_total, film.note, film.popularite, film.annee

    return sorted(films, key=score, reverse=True)[:nombre]


def poser_questions(
    films: list[Film],
) -> tuple[list[str], str, str, list[str], list[str], int]:
    """Pose des questions de contexte plutot que des filtres techniques."""
    genres = genres_disponibles(films)
    print("\n1. Quelle ambiance recherchez-vous ?")
    ambiances = {
        "Me divertir": ["Comedy", "Adventure", "Animation"],
        "Avoir des frissons": ["Horror", "Thriller", "Mystery"],
        "Etre emu": ["Drama", "Romance", "Family"],
        "M evader": ["Fantasy", "Adventure", "Science Fiction"],
    }
    ambiance_choisie = list(ambiances)
    for numero, reponse in enumerate(ambiance_choisie, start=1):
        print(f"{numero}. {reponse}")
    ambiance = ambiances[ambiance_choisie[demander_choix("> ", ambiance_choisie)]]

    print("\n2. Avec qui allez-vous regarder ce film ?")
    publics = {
        "Seul": ["Drama", "Mystery", "Science Fiction"],
        "En couple": ["Romance", "Drama", "Comedy"],
        "Avec des amis": ["Comedy", "Action", "Adventure"],
        "En famille": ["Family", "Animation", "Adventure"],
    }
    public_choisi = list(publics)
    for numero, reponse in enumerate(public_choisi, start=1):
        print(f"{numero}. {reponse}")
    public = publics[public_choisi[demander_choix("> ", public_choisi)]]

    print("\n3. Preferez-vous une valeur sure ou une decouverte ?")
    confiances = ["Une valeur sure", "Une decouverte"]
    for numero, reponse in enumerate(confiances, start=1):
        print(f"{numero}. {reponse}")
    confiance = ["valeur_sure", "decouverte"][
        demander_choix("> ", confiances)
    ]

    print("\n4. Avez-vous envie de voir quelque chose de recent ?")
    nouveautes = ["Oui, plutot recent", "Non, un classique me va aussi"]
    for numero, reponse in enumerate(nouveautes, start=1):
        print(f"{numero}. {reponse}")
    nouveaute = ["recent", "classique"][demander_choix("> ", nouveautes)]

    print("\n5. Quels genres vous attirent aujourd'hui ?")
    genres_choisis = demander_genres(genres)

    nombre = 3
    return genres_choisis, nouveaute, confiance, ambiance, public, nombre


def main() -> None:
    films = charger_films()
    if not films:
        print("Aucun film exploitable n'a ete trouve dans movies.csv.")
        return

    print("=== Recommandateur de films ===")
    preferences = poser_questions(films)
    recommandations = recommander_films(films, *preferences)

    print("\n=== Films recommandes ===")
    for numero, film in enumerate(recommandations, start=1):
        print(
            f"{numero}. {film.titre} ({film.annee}) - "
            f"{film.note:.1f}/10, {film.duree} min - "
            f"{', '.join(film.genres)}"
        )


if __name__ == "__main__":
    main()
