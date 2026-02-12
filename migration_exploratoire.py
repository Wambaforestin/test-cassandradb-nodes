import asyncore
import sys
from cassandra.cluster import Cluster

# Hack pour la compatibilité Python 3.12
sys.modules["asyncore"] = asyncore

# 1. Connexion au Cluster
print("Connexion au cluster...")
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('gamesales')

# 2. Préparation de la requête pour la nouvelle table
insert_genre_plat = session.prepare("""
    INSERT INTO genres_by_platform (platform, genre, name)
    VALUES (?, ?, ?)
""")

# 3. Lecture de la table brute
print("Récupération des données depuis game_sales_raw...")
rows = session.execute("SELECT platform, genre, name FROM game_sales_raw")

# 4. Insertion
count = 0
print("Remplissage de la table genres_by_platform...")

for row in rows:
    # On insère uniquement si les données essentielles sont présentes
    if row.platform and row.genre and row.name:
        session.execute(insert_genre_plat, (row.platform, row.genre, row.name))
        count += 1
        
        if count % 2000 == 0:
            print(f"{count} lignes traitées...")

print(f"Terminé ! {count} lignes insérées dans 'genres_by_platform'.")
cluster.shutdown()