import get_infos
import tkinter as tk
from tkinter import ttk

movies = get_infos.get_movies_list()
matching_movies = []
tag_matching_movies = []


def format_movie(movie):
    return (
        f"Titre original : {movie.original_title}\n"
        f"Popularité : {movie.popularity}\n"
        f"Acteurs : {', '.join(movie.cast)}\n"
        f"Réalisateurs : {', '.join(movie.directors)}\n"
        f"Mots-clés : {', '.join(movie.keywords)}\n"
        f"Durée : {movie.runtime} minutes\n"
        f"Genres : {', '.join(movie.genres)}\n"
        f"Sociétés de production : {', '.join(movie.production_companies)}\n"
        f"Nombre de votes : {movie.vote_count}\n"
        f"Moyenne des votes : {movie.vote_average}\n"
        f"Année de sortie : {movie.release_year}"
    )


def show_selected_movie(_event=None):
    selection = movie_list.curselection()
    if not selection:
        return

    movie = matching_movies[selection[0]]
    movie_info.delete("1.0", tk.END)
    movie_info.insert(tk.END, format_movie(movie))


def search_movies():
    global matching_movies

    search = name_entry.get().strip().lower()
    matching_movies = [
        movie for movie in movies
        if search in movie.original_title.lower()
    ]

    movie_list.delete(0, tk.END)
    movie_info.delete("1.0", tk.END)

    if not matching_movies:
        result_label.config(
            text=f"Aucun film trouvé pour « {search} ».",
            fg="red",
        )
        return

    result_label.config(
        text=f"{len(matching_movies)} film(s) trouvé(s).",
        fg="black",
    )
    for movie in matching_movies:
        movie_list.insert(tk.END, movie.original_title)
    if len(matching_movies) == 1:
        movie_info.insert(tk.END, format_movie(matching_movies[0]))


def show_selected_tag_movie(_event=None):
    selection = tag_movie_list.curselection()
    if not selection:
        return

    movie = tag_matching_movies[selection[0]]
    tag_movie_info.delete("1.0", tk.END)
    tag_movie_info.insert(tk.END, format_movie(movie))


def search_by_tag():
    global tag_matching_movies

    searches = [
        tag.strip().lower()
        for tag in tag_entry.get().split(",")
        if tag.strip()
    ]
    tag_matching_movies = (
        [
            movie
            for movie in movies
            if all(
                any(tag in keyword.lower() for keyword in movie.keywords)
                for tag in searches
            )
        ]
        if searches
        else []
    )

    tag_movie_list.delete(0, tk.END)
    tag_movie_info.delete("1.0", tk.END)

    if not tag_matching_movies:
        search_text = ", ".join(searches)
        tag_result_label.config(
            text=f"Aucun film trouvé pour les tags « {search_text} ».",
            fg="red",
        )
        return

    tag_result_label.config(
        text=f"{len(tag_matching_movies)} film(s) trouvé(s).",
        fg="black",
    )
    for movie in tag_matching_movies:
        tag_movie_list.insert(tk.END, movie.original_title)
    if len(tag_matching_movies) == 1:
        tag_movie_info.insert(tk.END, format_movie(tag_matching_movies[0]))


window = tk.Tk()
window.title("Recherche d'un film")
window.geometry("700x500")

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)

title_search_tab = ttk.Frame(notebook)
notebook.add(title_search_tab, text="Recherche par titre")

tk.Label(title_search_tab, text="Nom du film :").pack(pady=(15, 5))
name_entry = tk.Entry(title_search_tab, width=50)
name_entry.pack()
name_entry.bind("<Return>", lambda _event: search_movies())

tk.Button(title_search_tab, text="Rechercher", command=search_movies).pack(pady=10)
result_label = tk.Label(title_search_tab)
result_label.pack()

movie_list = tk.Listbox(title_search_tab, width=80, height=8)
movie_list.pack(padx=15, pady=10)
movie_list.bind("<<ListboxSelect>>", show_selected_movie)

movie_info = tk.Text(title_search_tab, wrap="word", width=80, height=20)
movie_info.pack(fill="both", expand=True, padx=15, pady=10)

tag_search_tab = ttk.Frame(notebook)
notebook.add(tag_search_tab, text="Recherche par tags")

tk.Label(tag_search_tab, text="Tag recherché :").pack(pady=(15, 5))
tag_entry = tk.Entry(tag_search_tab, width=50)
tag_entry.pack()
tag_entry.bind("<Return>", lambda _event: search_by_tag())

tk.Button(
    tag_search_tab,
    text="Rechercher",
    command=search_by_tag,
).pack(pady=10)
tag_result_label = tk.Label(tag_search_tab)
tag_result_label.pack()

tag_movie_list = tk.Listbox(tag_search_tab, width=80, height=8)
tag_movie_list.pack(padx=15, pady=10)
tag_movie_list.bind("<<ListboxSelect>>", show_selected_tag_movie)

tag_movie_info = tk.Text(tag_search_tab, wrap="word", width=80, height=20)
tag_movie_info.pack(fill="both", expand=True, padx=15, pady=10)

window.mainloop()
