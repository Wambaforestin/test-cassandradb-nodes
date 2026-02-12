# Analyse des ventes de jeux vidéo avec Apache Cassandra

## 🎯 Objectif

Implémentation d'une base de données NoSQL distribuée avec Apache Cassandra (v4.x) pour analyser un dataset de 16 000+ ventes de jeux vidéo. Application des principes Query-First, automatisation ETL en Python, et validation de la haute disponibilité du cluster.

## 🏗️ Architecture & Configuration

### Lancement du cluster (3 nœuds)

```bash
docker-compose up -d
docker exec -it cassandra-node1 nodetool status
```

### Import des données

```bash
# Copie du dataset
docker cp vgsales.csv cassandra-node1:/tmp/vgsales.csv

# Chargement via CQLSH
COPY gamesales.game_sales_raw (rank, name, platform, year, genre, publisher, na_sales, eu_sales, jp_sales, other_sales, global_sales) 
FROM '/tmp/vgsales.csv' WITH HEADER = TRUE;
```

## 🚀 Migration ETL (Python)

```bash
uv add "cassandra-driver>=3.29.1" pyasyncore
uv run migration.py
```

**Note** : Shim asyncore intégré pour compatibilité Python 3.12+

## 📊 Modélisation des données

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
