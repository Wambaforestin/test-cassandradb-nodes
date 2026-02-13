ALTER KEYSPACE gamesales 
WITH REPLICATION = { 
    'class': 'NetworkTopologyStrategy', 
    'datacenter1': 3 
};

-- Pour vérifier le niveau cohérence
CONSISTENCY

-- Pour changer le niveau de cohérence
CONSISTENCY QUORUM;
CONSISTENCY ALL;
CONSISTENCY ONE;