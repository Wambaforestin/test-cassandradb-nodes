USE gamesales;

-- 1. Table games_by_year
-- Objectif : Top 10 des jeux par année
-- Partition Key: year | Clustering Key: global_sales (DESC)
CREATE TABLE games_by_year (
    year int,
    global_sales decimal,
    name text,
    platform text,
    genre text,
    publisher text,
    PRIMARY KEY ((year), global_sales)
) WITH CLUSTERING ORDER BY (global_sales DESC);

-- 2. Table sales_by_platform
-- Objectif : Répartition des ventes par plateforme
-- Partition Key: platform | Clustering Key: name
CREATE TABLE sales_by_platform (
    platform text,
    name text,
    na_sales decimal,
    eu_sales decimal,
    jp_sales decimal,
    other_sales decimal,
    year int,
    PRIMARY KEY ((platform), name)
);

-- 3. Table sales_by_publisher
-- Objectif : Ventes globales par éditeur
-- Partition Key: publisher | Clustering Key: year
CREATE TABLE sales_by_publisher (
    publisher text,
    year int,
    global_sales decimal,
    PRIMARY KEY ((publisher), year)
);

-- 4. Table games_by_genre_year
-- Objectif : Volume des jeux par genre et année
-- Partition Key: (year, genre) | Clustering Key: name 
CREATE TABLE games_by_genre_year (
    year int,
    genre text,
    name text,
    platform text,
    publisher text,
    PRIMARY KEY ((year, genre), name)
);