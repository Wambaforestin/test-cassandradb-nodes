# Analyse des ventes de jeux vidéo avec Apache Cassandra

## Objectif

Dand le cadre de mon apprentissage du Data Enginneering j'ai voulu tester et met    n œuvre une base de données NoSQL distribuée à l'aide d'Apache Cassandra afin d'analyser les données relatives aux ventes de jeux vidéo. Le travail se concentre sur les principes de conception Query-First, la migration des données en utilisant Python et les tests de haute disponibilité des clusters pour voir et comprendre comment les noeuds réagissent en cas de défaillance.

## Architecture & Configuration

### Lancement du cluster (3 nœuds)

```bash
docker-compose up -d
docker exec -it cassandra-node1 nodetool status
```

### Import des données

```sql
USE gamesales;
```

#### Étape 1 : Place le fichier
Mets le fichier `video-game-sales.csv` dans ton dossier `projet_cassandra`.

#### Étape 2 : Copie le fichier DANS le conteneur
Tu dois utiliser la commande `docker cp` pour envoyer le fichier de ton Windows vers le conteneur `cassandra-node1`.

Ouvre ton terminal (PowerShell) dans le dossier du projet et lance cette commande :

```powershell
docker cp video-game-sales.csv cassandra-node1:/tmp/video-game-sales.csv
```

**Explication de la commande :**
- `docker cp` : Copier un fichier
- `video-game-sales.csv` : Le fichier source (sur ton Windows)
- `cassandra-node1:/tmp/...` : La destination (dans le conteneur, dossier temporaire `/tmp`)

#### Étape 3 : Vérifie que le fichier est bien arrivé
Pour être sûr que le fichier est bien accessible par Cassandra, lance cette petite commande de vérification :

```powershell
docker exec cassandra-node1 ls -l /tmp/video-game-sales.csv
```

Si tu vois le nom du fichier s'afficher avec des droits (ex: `-rwxr-xr-x ...`), c'est gagné ! ✅

#### Étape 4 : Import dans Cassandra (commande COPY)
Quand tu lanceras la commande d'import COPY dans cqlsh, tu devras indiquer le chemin interne du conteneur :

```sql
COPY gamesales.game_sales_raw (Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales) 
FROM '/tmp/video-game-sales.csv' 
WITH DELIMITER = ',' AND HEADER = TRUE;
```

**Note** : Utilise bien `/tmp/video-game-sales.csv` (chemin du conteneur) et non un chemin Windows.

## Migration des données (Python)

```bash
# rassure-toi d'avoir Python 3.12+ et uv installé
# si tu réutilises un environnement virtuel, active-le d'abord
uv sync 

# si tu crée un nouvel environnement virtuel, utilise :
uv init
uv add "cassandra-driver>=3.29.1" pyasyncore
uv run migration.py
```

**Note** : Shim asyncore intégré pour compatibilité Python 3.12+

##  Modélisation des données orientée requêtes

| Table | Partition Key | Clustering Key | Objectif |
|-------|---|---|---|
| `games_by_year` | année | global_sales | Top 10 ventes/année |
| `sales_by_platform` | plateforme | nom | Jeux par console |
| `sales_by_publisher` | éditeur | année | Chronologie éditeur |
| `games_by_genre_year` | (année, genre) | nom | Analyse genre-année |
| `genres_by_platform` | plateforme | genre, nom | Catalogue par console |

## Haute disponibilité

Résultats après arrêt d'un nœud (`docker stop cassandra-node3`) :

| Niveau | Statut | Remarques |
|--------|--------|----------|
| ONE | ✅ | 1 nœud suffit |
| QUORUM | ✅ | 2/3 respecté |
| ALL | ❌ | Nécessite tous les nœuds |

## Points clés retenus

- **Query-First Design** : Modeler selon les requêtes, pas de jointures
- **Réplication** : NetworkTopologyStrategy avec RF=3 indispensable
- **Scalabilité** : Performance constante en lecture/écriture

**Source** : [ValdisW/datasets](https://raw.githubusercontent.com/ValdisW/datasets/master/video-game-sales.csv)
