from io import BytesIO
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from urllib.error import URLError
from urllib.request import urlopen

import get_infos
from PIL import Image, ImageTk

class SimpleApp:
    PHOTO_WIDTH = 320
    PHOTO_HEIGHT = 420
    RATING_VALUES = ("g", "pg", "pg_13", "r", "r+", "rx")

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Recherche de films et d'animés")
        self.root.geometry("1000x760")
        self.root.minsize(900, 720)

        self.movies = get_infos.Movies(get_infos.movies)
        self.animes = get_infos.Animes(get_infos.animes)
        self.current_results = []
        self.image_cache = {}
        self.selected_item = None

        self.media_type = tk.StringVar(value="Films")
        self.operation = tk.StringVar(value="Plusieurs critères")
        self.criteria_title = tk.StringVar()
        self.criteria_genre = tk.StringVar()
        self.criteria_studio = tk.StringVar()
        self.criteria_min_note = tk.StringVar()
        self.criteria_max_note = tk.StringVar()
        self.criteria_min_year = tk.StringVar()
        self.criteria_max_year = tk.StringVar()
        self.criteria_min_rating = tk.StringVar(value=self.RATING_VALUES[0])
        self.criteria_max_rating = tk.StringVar(value=self.RATING_VALUES[-1])

        self.create_widgets()
        self.update_operations()
        self.run_search()

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        ttk.Label(
            main,
            text="Movies & Anime DB",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            main,
            text="Combinez plusieurs critères pour trouver un film ou un animé.",
        ).grid(row=1, column=0, sticky="w", pady=(2, 12))

        controls = ttk.LabelFrame(main, text="Recherche", padding=10)
        controls.grid(row=2, column=0, sticky="new")
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)

        ttk.Label(controls, text="Type :").grid(row=0, column=0, sticky="w")
        media = ttk.Combobox(
            controls,
            textvariable=self.media_type,
            values=("Films", "Animés"),
            state="readonly",
            width=18,
        )
        media.grid(row=0, column=1, sticky="ew", padx=(8, 20))
        media.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.change_media_type(),
        )

        ttk.Label(controls, text="Fonction :").grid(row=0, column=2, sticky="w")
        self.operation_box = ttk.Combobox(
            controls,
            textvariable=self.operation,
            state="readonly",
            width=32,
        )
        self.operation_box.grid(row=0, column=3, sticky="ew", padx=(8, 0))
        self.operation_box.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.update_inputs(),
        )

        self.input_frame = ttk.Frame(controls)
        self.input_frame.grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=(4, 0)
        )
        self.input_frame.columnconfigure(1, weight=1)
        self.input_frame.columnconfigure(3, weight=1)

        ttk.Button(
            controls,
            text="Rechercher",
            command=self.run_search,
        ).grid(row=1, column=3, padx=(10, 0), pady=(4, 0))



        results_frame = ttk.LabelFrame(main, text="Résultats", padding=8)
        results_frame.grid(row=3, column=0, sticky="nsew")
        main.rowconfigure(3, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=0)
        results_frame.columnconfigure(2, weight=0, minsize=0)
        results_frame.rowconfigure(0, weight=1)

        self.results = tk.Listbox(results_frame, activestyle="dotbox")
        self.results.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.results.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results.configure(yscrollcommand=scrollbar.set)
        self.results.bind("<<ListboxSelect>>", self.show_selected)

        self.details = tk.Text(
            results_frame,
            height=8,
            state="disabled",
            wrap="word",
        )
        self.details.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(8, 0),
        )

        image_frame = ttk.LabelFrame(
            results_frame,
            text="Photo de l'animé",
            width=self.PHOTO_WIDTH,
            height=self.PHOTO_HEIGHT,
            padding=8,
        )
        image_frame.grid(
            row=0,
            column=2,
            rowspan=2,
            sticky="n",
            padx=(12, 0),
        )
        image_frame.grid_propagate(False)
        image_frame.pack_propagate(False)
        self.image_frame = image_frame
        self.image_label = ttk.Label(
            image_frame,
            text="Sélectionnez un animé",
            anchor="center",
            justify="center",
        )
        self.image_label.pack(fill="both", expand=True)
        self.image_frame.grid_remove()

    def update_operations(self):
        showing_animes = self.media_type.get() == "Animés"
        if showing_animes:
            self.image_frame.grid()
            self.image_frame.master.columnconfigure(
                2,
                weight=0,
                minsize=self.PHOTO_WIDTH,
            )
        else:
            self.image_frame.grid_remove()
            self.image_frame.master.columnconfigure(2, weight=0, minsize=0)
            self.selected_item = None
            self.image_label.configure(image="", text="")

        operations = ("Plusieurs critères",)
        self.operation_box["values"] = operations
        self.operation.set("Plusieurs critères")
        self.update_inputs()

    def change_media_type(self):
        self.update_operations()
        self.run_search()

    def update_inputs(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        criteria = (
            ("Titre :", self.criteria_title),
            ("Genre :", self.criteria_genre),
            ("Studio :", self.criteria_studio),
            ("Note min. :", self.criteria_min_note),
            ("Note max. :", self.criteria_max_note),
            ("Année min. :", self.criteria_min_year),
            ("Année max. :", self.criteria_max_year),
        )
        if self.media_type.get() == "Animés":
            criteria += (
                ("Rating min. :", self.criteria_min_rating),
                ("Rating max. :", self.criteria_max_rating),
            )
        for index, (label, variable) in enumerate(criteria):
            row, pair = divmod(index, 2)
            column = pair * 2
            ttk.Label(self.input_frame, text=label).grid(
                row=row,
                column=column,
                sticky="w",
                padx=(0 if column == 0 else 10, 4),
                pady=2,
            )
            if "Rating" in label:
                entry = ttk.Combobox(
                    self.input_frame,
                    textvariable=variable,
                    values=("",) + self.RATING_VALUES,
                    state="readonly",
                    width=12,
                )
            else:
                entry = ttk.Entry(
                    self.input_frame,
                    textvariable=variable,
                    width=12,
                )
            entry.grid(
                row=row,
                column=column + 1,
                sticky="ew",
                pady=2,
            )

    def get_collection(self):
        if self.media_type.get() == "Films":
            return self.movies
        return self.animes

    def run_search(self):
        try:
            collection = self.get_collection()
            criteria = dict(
                title=self.criteria_title.get().strip(),
                genres=self.criteria_genre.get().strip() or None,
                studios=self.criteria_studio.get().strip() or None,
                min_vote_average=(
                    float(self.criteria_min_note.get())
                    if self.criteria_min_note.get().strip()
                    else None
                ),
                max_vote_average=(
                    float(self.criteria_max_note.get())
                    if self.criteria_max_note.get().strip()
                    else None
                ),
                min_release_year=(
                    int(self.criteria_min_year.get())
                    if self.criteria_min_year.get().strip()
                    else None
                ),
                max_release_year=(
                    int(self.criteria_max_year.get())
                    if self.criteria_max_year.get().strip()
                    else None
                ),
            )
            if self.media_type.get() == "Animés":
                criteria["min_rating"] = (
                    self.criteria_min_rating.get().strip() or None
                )
                criteria["max_rating"] = (
                    self.criteria_max_rating.get().strip() or None
                )
            results = collection.get_by_criteria(**criteria)

            self.current_results = results
            self.results.delete(0, tk.END)
            for item in results:
                self.results.insert(
                    tk.END,
                    f"{item.title} ({item.release_year}) - "
                    f"note : {item.vote_average}",
                )
            self.clear_details()
        except (ValueError, SyntaxError) as error:
            messagebox.showerror("Recherche invalide", str(error))

    def show_selected(self, _event):
        selection = self.results.curselection()
        if not selection:
            return
        item = self.current_results[selection[0]]
        self.selected_item = item
        details = "\n".join(
            f"{label} : {value}"
            for label, value in vars(item).items()
        )
        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert("1.0", details)
        self.details.configure(state="disabled")
        self.image_label.configure(image="", text="")

        if isinstance(item, get_infos.Anime):
            cached_image = self.image_cache.get(item.picture)
            if cached_image is not None:
                self.image_label.configure(image=cached_image)
            else:
                self.image_label.configure(text="Chargement de l'image...")
                threading.Thread(
                    target=self.load_anime_image,
                    args=(item,),
                    daemon=True,
                ).start()

    def load_anime_image(self, item):
        try:
            with urlopen(item.picture, timeout=10) as response:
                image = Image.open(BytesIO(response.read()))
                image.load()
                image.thumbnail((280, 380))
        except (OSError, URLError) as error:
            self.root.after(
                0,
                lambda item=item, error=str(error): self.show_image_error(
                    item, error
                ),
            )
            return

        self.root.after(
            0,
            lambda item=item, image=image: self.display_anime_image(
                item, image
            ),
        )

    def display_anime_image(self, item, image):
        if self.selected_item is not item:
            return
        photo = ImageTk.PhotoImage(image)
        self.image_cache[item.picture] = photo
        self.image_label.configure(image=photo, text="")

    def show_image_error(self, item, error):
        if self.selected_item is item:
            self.image_label.configure(
                text=f"Image indisponible : {error}"
            )

    def clear_details(self):
        self.selected_item = None
        self.image_label.configure(image="", text="")
        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    SimpleApp(root)
    root.mainloop()
