"""Graphiques des genres de films et d'animes par annee."""

import matplotlib.pyplot as plt

import analysis
import get_infos


def afficher_genres_par_annee(
    elements,
    nombre=10,
    annee_min=analysis.ANNEE_MIN_DEFAUT,
    annee_max=analysis.ANNEE_MAX_DEFAUT,
    type_media="animes",
):
    """Affiche les genres les plus utilises par annee."""
    if not elements:
        raise ValueError("La liste des elements est vide.")
    if nombre < 1:
        raise ValueError("Le nombre de genres doit etre superieur a 0.")

    plt.figure(figsize=(14, 8))

    genres_par_annee = analysis.genres_par_annee(
        elements,
        nombre=nombre,
        annee_min=annee_min,
        annee_max=annee_max,
    )
    annees = sorted(genres_par_annee)
    genres_a_afficher = set()

    for annee in annees:
        for resultat in genres_par_annee[annee]:
            genres_a_afficher.add(resultat["genre"])

    genres_a_afficher = sorted(genres_a_afficher)
    positions = range(len(annees))
    hauteur_actuelle = [0] * len(annees)

    for numero, genre in enumerate(genres_a_afficher, start=1):
        valeurs = []
        for annee in annees:
            genre_resultat = next(
                (
                    resultat
                    for resultat in genres_par_annee[annee]
                    if resultat["genre"] == genre
                ),
                None,
            )
            valeurs.append(genre_resultat["nombre"] if genre_resultat else 0)

        plt.bar(
            list(positions),
            valeurs,
            bottom=hauteur_actuelle,
            width=0.8,
            label=str(numero) + " - " + genre,
        )
        for position, valeur, hauteur in zip(
            positions,
            valeurs,
            hauteur_actuelle,
        ):
            if valeur > 0:
                plt.text(
                    position,
                    hauteur + valeur / 2,
                    str(numero),
                    ha="center",
                    va="center",
                    fontsize=8,
                )
        hauteur_actuelle = [
            hauteur + valeur
            for hauteur, valeur in zip(hauteur_actuelle, valeurs)
        ]

    plt.xticks(list(positions), annees, rotation=45)
    plt.title(
        "Genres de " + type_media + " les plus utilises par annee "
        "(top par annee)"
    )
    plt.xlabel("Annee de publication")
    plt.ylabel("Nombre de " + type_media)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def afficher_genres_films_par_annee(
    films,
    nombre=10,
    annee_min=analysis.ANNEE_MIN_DEFAUT,
    annee_max=analysis.ANNEE_MAX_DEFAUT,
):
    """Affiche les genres de films les plus utilises par annee."""
    afficher_genres_par_annee(
        films,
        nombre,
        annee_min,
        annee_max,
        "films",
    )


if __name__ == "__main__":
    animes = get_infos.Animes(get_infos.animes).list
    afficher_genres_par_annee(animes)
    films = get_infos.Movies(get_infos.movies).list
    afficher_genres_films_par_annee(films)