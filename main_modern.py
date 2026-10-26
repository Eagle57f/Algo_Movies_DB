import tkinter as tk
from tkinter import ttk

import sv_ttk

import get_infos


class MovieApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.movies = get_infos.get_movies_list()
        self.title_matches = []
        self.tag_matches = []
        self.sort_state = {
            "title": {"column": None, "reverse": False},
            "tag": {"column": None, "reverse": False},
        }

        self.root.title("Movies DB")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        sv_ttk.set_theme("light")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        ttk.Label(
            main_frame,
            text="Movies DB",
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            main_frame,
            text="Recherchez un film par son titre ou par ses tags.",
        ).grid(row=1, column=0, sticky="w", pady=(2, 12))

        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, sticky="nsew")

        title_tab = ttk.Frame(notebook, padding=12)
        tag_tab = ttk.Frame(notebook, padding=12)
        notebook.add(title_tab, text="Recherche par titre")
        notebook.add(tag_tab, text="Recherche par tags")

        self.create_search_tab(
            title_tab,
            "Titre à rechercher :",
            self.search_by_title,
            "title",
        )
        self.create_search_tab(
            tag_tab,
            "Tags à rechercher (séparés par des virgules) :",
            self.search_by_tag,
            "tag",
        )

    def create_search_tab(self, parent, label_text, command, search_type):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        search_frame = ttk.Frame(parent)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text=label_text).grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        entry = ttk.Entry(search_frame)
        entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        entry.bind("<Return>", lambda _event: command())
        ttk.Button(search_frame, text="Rechercher", command=command).grid(
            row=0, column=2
        )

        result_label = ttk.Label(parent)
        result_label.grid(row=1, column=0, sticky="w", pady=(0, 8))

        content = ttk.PanedWindow(parent, orient="vertical")
        content.grid(row=2, column=0, sticky="nsew")

        results_frame = ttk.Frame(content, padding=4)
        details_frame = ttk.LabelFrame(
            content,
            text="Informations du film",
            padding=12,
        )
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(1, weight=1)
        content.add(results_frame, weight=3)
        content.add(details_frame, weight=2)

        tree = ttk.Treeview(
            results_frame,
            columns=("title", "year", "rating"),
            show="headings",
            selectmode="browse",
            height=3,
        )
        tree.heading(
            "title",
            text="Titre",
            command=lambda: self.sort_results(search_type, "title"),
        )
        tree.heading(
            "year",
            text="Année",
            command=lambda: self.sort_results(search_type, "year"),
        )
        tree.heading(
            "rating",
            text="Note",
            command=lambda: self.sort_results(search_type, "rating"),
        )
        tree.column("title", anchor="w", width=520)
        tree.column("year", anchor="center", width=100)
        tree.column("rating", anchor="center", width=100)
        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)

        selected_label = ttk.Label(
            details_frame,
            text="Aucun film sélectionné",
            font=("Segoe UI", 11, "bold"),
        )
        selected_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 10),
        )

        details_canvas = tk.Canvas(
            details_frame,
            highlightthickness=0,
            borderwidth=0,
        )
        details_canvas.grid(row=1, column=0, sticky="nsew")
        details_scrollbar = ttk.Scrollbar(
            details_frame,
            orient="vertical",
            command=details_canvas.yview,
        )
        details_scrollbar.grid(row=1, column=1, sticky="ns")
        details_canvas.configure(yscrollcommand=details_scrollbar.set)

        details = ttk.Frame(details_canvas, padding=(0, 0, 8, 0))
        details_window = details_canvas.create_window(
            (0, 0),
            window=details,
            anchor="nw",
        )
        details.bind(
            "<Configure>",
            lambda _event: details_canvas.configure(
                scrollregion=details_canvas.bbox("all")
            ),
        )
        details_canvas.bind(
            "<Configure>",
            lambda event: details_canvas.itemconfigure(
                details_window,
                width=event.width,
            ),
        )
        details_canvas.bind(
            "<Enter>",
            lambda _event: details_canvas.bind_all(
                "<MouseWheel>",
                lambda event: details_canvas.yview_scroll(
                    int(-event.delta / 120),
                    "units",
                ),
            ),
        )
        details_canvas.bind(
            "<Leave>",
            lambda _event: details_canvas.unbind_all("<MouseWheel>"),
        )

        details.columnconfigure(0, weight=1)
        details.columnconfigure(1, weight=1)

        general_frame = ttk.LabelFrame(
            details,
            text="Informations générales",
            padding=8,
        )
        general_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 8),
        )
        general_frame.columnconfigure(1, weight=1)
        general_frame.columnconfigure(3, weight=1)

        general_values = {}
        general_fields = (
            ("Année", "release_year"),
            ("Durée", "runtime"),
            ("Popularité", "popularity"),
            ("Note moyenne", "vote_average"),
            ("Nombre de votes", "vote_count"),
        )
        for index, (label, attribute) in enumerate(general_fields):
            row = index // 2
            column = (index % 2) * 2
            ttk.Label(
                general_frame,
                text=f"{label} :",
                font=("Segoe UI", 9, "bold"),
            ).grid(row=row, column=column, sticky="w", padx=(0, 6), pady=2)
            value = ttk.Label(general_frame, text="-")
            value.grid(
                row=row,
                column=column + 1,
                sticky="w",
                padx=(0, 18),
                pady=2,
            )
            general_values[attribute] = value

        category_values = {}
        categories = (
            ("Genres", "genres"),
            ("Réalisateurs", "directors"),
            ("Acteurs", "cast"),
            ("Mots-clés", "keywords"),
            ("Sociétés de production", "production_companies"),
        )
        for index, (title, attribute) in enumerate(categories):
            row = index // 2 + 1
            column = index % 2
            category = ttk.LabelFrame(details, text=title, padding=8)
            category.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=(0, 4) if column == 0 else (4, 0),
                pady=(0, 8),
            )
            value = ttk.Label(
                category,
                text="-",
                anchor="w",
                justify="left",
                wraplength=360,
            )
            value.pack(fill="both", expand=True)
            category_values[attribute] = value

        details.general_values = general_values
        details.category_values = category_values

        tree.bind(
            "<<TreeviewSelect>>",
            lambda _event: self.show_selected(
                search_type, tree, details, selected_label
            ),
        )

        setattr(self, f"{search_type}_entry", entry)
        setattr(self, f"{search_type}_label", result_label)
        setattr(self, f"{search_type}_tree", tree)
        setattr(self, f"{search_type}_details", details)
        setattr(self, f"{search_type}_selected", selected_label)

    def search_by_title(self):
        search = self.title_entry.get().strip().lower()
        self.title_matches = [
            movie for movie in self.movies
            if search and search in movie.original_title.lower()
        ]
        self.update_results("title", self.title_matches, search, "titre")

    def search_by_tag(self):
        tags = [
            tag.strip().lower()
            for tag in self.tag_entry.get().split(",")
            if tag.strip()
        ]
        self.tag_matches = [
            movie for movie in self.movies
            if tags and all(
                any(tag in keyword.lower() for keyword in movie.keywords)
                for tag in tags
            )
        ]
        self.update_results("tag", self.tag_matches, ", ".join(tags), "tags")

    def update_results(self, search_type, matches, search, search_kind):
        tree = getattr(self, f"{search_type}_tree")
        details = getattr(self, f"{search_type}_details")
        selected_label = getattr(self, f"{search_type}_selected")
        result_label = getattr(self, f"{search_type}_label")
        self.sort_state[search_type] = {"column": None, "reverse": False}
        self.update_heading_labels(search_type)

        for item in tree.get_children():
            tree.delete(item)
        self.clear_details(details)
        selected_label.configure(text="Aucun film sélectionné")

        if not matches:
            result_label.configure(
                text=f"Aucun film trouvé pour les {search_kind} « {search} »."
            )
            return

        result_label.configure(text=f"{len(matches)} film(s) trouvé(s).")
        for index, movie in enumerate(matches):
            tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    movie.original_title,
                    movie.release_year,
                    f"{movie.vote_average:.1f}",
                ),
            )

        if len(matches) == 1:
            tree.selection_set("0")
            self.show_selected(
                search_type, tree, details, selected_label
            )

    def sort_results(self, search_type, column):
        matches = (
            self.title_matches if search_type == "title" else self.tag_matches
        )
        if not matches:
            return

        tree = getattr(self, f"{search_type}_tree")
        selected = tree.selection()
        selected_movie = (
            matches[int(selected[0])]
            if selected
            else None
        )
        state = self.sort_state[search_type]
        if state["column"] == column:
            state["reverse"] = not state["reverse"]
        else:
            state["column"] = column
            state["reverse"] = False

        key_functions = {
            "title": lambda movie: movie.original_title.casefold(),
            "year": lambda movie: movie.release_year,
            "rating": lambda movie: movie.vote_average,
        }
        matches.sort(
            key=key_functions[column],
            reverse=state["reverse"],
        )

        for item in tree.get_children():
            tree.delete(item)
        for index, movie in enumerate(matches):
            tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    movie.original_title,
                    movie.release_year,
                    f"{movie.vote_average:.1f}",
                ),
            )

        self.update_heading_labels(search_type)
        if selected_movie is not None:
            selected_index = matches.index(selected_movie)
            tree.selection_set(str(selected_index))
            self.show_selected(
                search_type,
                tree,
                getattr(self, f"{search_type}_details"),
                getattr(self, f"{search_type}_selected"),
            )

    def update_heading_labels(self, search_type):
        tree = getattr(self, f"{search_type}_tree")
        state = self.sort_state[search_type]
        labels = {
            "title": "Titre",
            "year": "Année",
            "rating": "Note",
        }
        for column, label in labels.items():
            if state["column"] == column:
                arrow = " ▼" if state["reverse"] else " ▲"
                label += arrow
            tree.heading(column, text=label)

    def show_selected(self, search_type, tree, details, selected_label):
        selection = tree.selection()
        if not selection:
            return

        matches = (
            self.title_matches if search_type == "title" else self.tag_matches
        )
        movie = matches[int(selection[0])]
        selected_label.configure(
            text=f"Film sélectionné : {movie.original_title}"
        )
        self.update_details(details, movie)

    @staticmethod
    def clear_details(details):
        for value in details.general_values.values():
            value.configure(text="-")
        for value in details.category_values.values():
            value.configure(text="-")

    @staticmethod
    def update_details(details, movie):
        general_values = {
            "release_year": movie.release_year,
            "runtime": f"{movie.runtime} minutes",
            "popularity": movie.popularity,
            "vote_average": movie.vote_average,
            "vote_count": movie.vote_count,
        }
        for attribute, value in general_values.items():
            details.general_values[attribute].configure(text=value)
        for attribute, value in details.category_values.items():
            value.configure(text=", ".join(getattr(movie, attribute)))


if __name__ == "__main__":
    root = tk.Tk()
    MovieApp(root)
    root.mainloop()
