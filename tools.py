import csv
import ast
from pathlib import Path

DATA_DIR = Path(__file__).parent

with open(DATA_DIR / "movies.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    movies = list(reader)

with open(DATA_DIR / "animes.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    animes = list(reader)

tags_raw= [line[6] for line in movies][1:]
tags_b = [i.split("|") for i in tags_raw]
tags_set = set()
for i in tags_b:
    for j in i:
        tags_set.add(j)
tags = list(tags_set)[1:]
print(tags[1:])

