import customtkinter as ctk
import csv

ctk.set_appearance_mode("dark")

def get_tag_list():
    with open("tmdb-movies.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        tag_list = {tag for row in reader for tag in row[13].split("|") if tag != ""}
    return tag_list

class TagSelector(ctk.CTkFrame):
    def __init__(self, master, tags):
        super().__init__(master)

        self.tags = tags
        self.selected_tags = set()
        self.checkboxes = {}

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Rechercher un genre..."
        )
        self.search_entry.pack(fill="x", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_tags)

        self.tags_frame = ctk.CTkScrollableFrame(self, height=180)
        self.tags_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.selected_label = ctk.CTkLabel(
            self,
            text="Tags sélectionnés :"
        )
        self.selected_label.pack(anchor="w", padx=10)

        self.selected_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", height=50)
        self.selected_frame.pack(fill="x", padx=10, pady=10)

        self.display_tags(self.tags)

    def display_tags(self, tags):
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        for tag in tags:
            variable = ctk.BooleanVar(
                value=tag in self.selected_tags
            )

            checkbox = ctk.CTkCheckBox(
                self.tags_frame,
                text=tag,
                variable=variable,
                command=lambda t=tag, v=variable:
                    self.toggle_tag(t, v)
            )
            checkbox.pack(anchor="w", pady=3)
            self.checkboxes[tag] = checkbox

    def filter_tags(self, event=None):
        search = self.search_entry.get().lower()

        filtered_tags = [
            tag for tag in self.tags
            if search in tag.lower()
        ]

        self.display_tags(filtered_tags)

    def toggle_tag(self, tag, variable):
        if variable.get():
            self.selected_tags.add(tag)
        else:
            self.selected_tags.discard(tag)

        self.update_selected_tags()

    def update_selected_tags(self):
        for widget in self.selected_frame.winfo_children():
            widget.destroy()

        for tag in self.selected_tags:
            button = ctk.CTkButton(
                self.selected_frame,
                text=f"{tag} ×",
                width=100,
                command=lambda t=tag: self.remove_tag(t)
            )
            button.pack(side="left", padx=3, pady=3)

    def remove_tag(self, tag):
        self.selected_tags.remove(tag)
        self.display_tags(self.tags)
        self.update_selected_tags()

    def get_selected_tags(self):
        return list(self.selected_tags)


app = ctk.CTk()
app.geometry("400x500")

selector = TagSelector(
    app,
    get_tag_list()
)
selector.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()