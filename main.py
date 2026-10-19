import csv

fichier = open("tmdb-movies.csv", "r", encoding="utf-8")

reader = csv.reader(fichier)

print(list(reader)[1][5])