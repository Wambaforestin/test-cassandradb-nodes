-- 1. Création du Keyspace
CREATE KEYSPACE gamesales 
WITH REPLICATION = { 
    'class': 'SimpleStrategy', 
    'replication_factor': 1 
};

-- Sélection du Keyspace pour la suite
USE gamesales;

-- 2. Création de la table brute (game_sales_raw)
-- text pour les chaînes et decimal pour les ventes
CREATE TABLE game_sales_raw (
    Rank int,
    Name text,
    Platform text,
    Year text,
    Genre text,
    Publisher text,
    NA_Sales decimal,
    EU_Sales decimal,
    JP_Sales decimal,
    Other_Sales decimal,
    Global_Sales decimal,
    PRIMARY KEY (Rank)
);