from cassandra.cluster import Cluster
import asyncore
import sys

# 1. Connexion au Cluster (via le port 9042 exposé sur Windows)
print("Connexion au cluster...")
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('gamesales')

# 2. Préparation des requêtes d'insertion
insert_year = session.prepare("""
    INSERT INTO games_by_year (year, global_sales, name, platform, genre, publisher)
    VALUES (?, ?, ?, ?, ?, ?)
""")

insert_platform = session.prepare("""
    INSERT INTO sales_by_platform (platform, name, na_sales, eu_sales, jp_sales, other_sales, year)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""")

insert_publisher = session.prepare("""
    INSERT INTO sales_by_publisher (publisher, year, global_sales)
    VALUES (?, ?, ?)
""")

insert_genre = session.prepare("""
    INSERT INTO games_by_genre_year (year, genre, name, platform, publisher)
    VALUES (?, ?, ?, ?, ?)
""")

# 3. Lecture des données brutes
print("Lecture des données brutes...")
rows = session.execute("SELECT * FROM game_sales_raw")

count = 0
print("Démarrage de la migration... (Cela peut prendre quelques minutes)")

for row in rows:
    # Mini pipeline de nettoyage et validation des données au cas où.
    # Gestion de l'année : Si c'est "N/A", on ignore la ligne ou on met une valeur par défaut
    # Ici, on ignore les lignes sans année valide car c'est une clé de partition
    if row.year == 'N/A' or row.year is None:
        continue
        
    try:
        year_int = int(row.year)
    except ValueError:
        continue # Si l'année n'est pas un nombre, on passe

    # INSERTION DANS LES 4 TABLE
    
    # Table 1 : games_by_year
    session.execute(insert_year, (year_int, row.global_sales, row.name, row.platform, row.genre, row.publisher))
    
    # Table 2 : sales_by_platform
    session.execute(insert_platform, (row.platform, row.name, row.na_sales, row.eu_sales, row.jp_sales, row.other_sales, year_int))
    
    # Table 3 : sales_by_publisher
    session.execute(insert_publisher, (row.publisher, year_int, row.global_sales))
    
    # Table 4 : games_by_genre_year
    session.execute(insert_genre, (year_int, row.genre, row.name, row.platform, row.publisher))

    count += 1
    if count % 1000 == 0:
        print(f"{count} lignes migrées...")

print(f"Tout est bon! {count} lignes insérées avec succès.")
cluster.shutdown()