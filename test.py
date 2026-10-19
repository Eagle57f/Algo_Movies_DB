import csv

with open("tmdb-movies.csv", "r", encoding="utf-8") as fichier:
    reader = csv.reader(fichier)
    data = list(reader)

print(data[1:4])



