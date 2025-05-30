-- Full table definition and data insert

DROP TABLE IF EXISTS celestial_objects;

CREATE TABLE celestial_objects (
   id               SERIAL PRIMARY KEY,
   object_type      VARCHAR(30),
   object_name      VARCHAR(30),
   constellation    VARCHAR(30),
   beauty           BOOLEAN
);

INSERT INTO celestial_objects (object_type, object_name, constellation, beauty)
VALUES
('binary system', 'Sirius', 'Canis Major', 'YES'),
('white dwarf', 'Sirius A', 'Canis Major', 'YES'),
('white dwarf', 'Sirius B', 'Canis Major', 'YES'),
('stellar system', 'Keid', 'Eridanus', NULL),
('white dwarf', '40 Eridani B', 'Eridanus', 'NO'),
('red dwarf', '40 Eridani C', 'Eridanus', 'NO'),
('binary system', 'Procryn', 'Canis Minor', 'YES'),
('star', 'Procryn A', 'Canis Minor', 'YES'),
('white dwarf', 'Procryn B', 'Canis Minor', 'YES'),
('white dwarf', 'Van Maanen 2', 'Pisces', 'YES'),
('stellar system', 'PSR B1620 26', 'Scorpius', 'NO'),
('pulsar', 'PSR B1620 26 A', 'Scorpius', 'NO'),
('white dwarf', 'WD B162026', 'Scorpius', 'NO'),
('exoplanet', 'PSR B1620 26 B', 'Scorpius', 'NO'),
('globular cluster', 'Messier 4', 'Scorpius', 'YES'),
('white dwarf', 'WD 1145+017', 'Virgo', NULL),
('exoasteroid', 'WD 1145+017 b', 'Virgo', NULL),
('white dwarf', 'SDSS J1228+1040', 'Virgo', NULL),
('planetismal', 'SDSS J1228+1040 b', 'Virgo', NULL),
('binary system', 'AR Scorpii', 'Scorpius', 'YES'),
('white dwarf/pulsar', 'AR Scorpii A', 'Scorpius', 'YES'),
('red dwarf', 'AR Scorpii B', 'Scorpius', 'YES'),
('binary system', 'AE Aquarii', 'Aquarius', 'YES'),
('white dwarf/pulsar', 'AE Aquarii A', 'Aquarius', 'YES'),
('red dwarf', 'AE Aquarii B', 'Aquarius', 'YES'),
('open star cluster', 'Pleiades', 'Taurus', 'YES'),
('stellar system', 'Alcyone', 'Taurus', 'YES'),
('star', 'Alcyone A', 'Taurus', 'YES'),
('star', 'Alcyone B', 'Taurus', 'YES'),
('star', 'Alcyone C', 'Taurus', 'YES'),
('star', 'Alcyone D', 'Taurus', 'YES'),
('star system', 'Maia', 'Taurus', 'YES'),
('star', 'Maia A', 'Taurus', 'YES'),
('binary system', 'Electra', 'Taurus', 'YES'),
('star', 'Electra A', 'Taurus', 'YES'),
('star', 'Electra B', 'Taurus', 'YES'),
('binary system', 'Taygeta', 'Taurus', 'YES'),
('star', 'Taygeta A', 'Taurus', 'YES'),
('star', 'Taygeta B', 'Taurus', 'YES'),
('star system', 'Celaeno', 'Taurus', 'YES'),
('star', 'Celaeno A', 'Taurus', 'YES'),
('binary system', 'Asterope', 'Taurus', 'YES'),
('star', 'Asterope 1', 'Taurus', 'YES'),
('star', 'Asterope 2', 'Taurus', 'YES'),
('nebula', 'Merope Nebula', 'Taurus', 'YES'),
('star system', 'Merope', 'Taurus', 'YES'),
('star', 'Merope A', 'Taurus', 'YES'),
('stellar system', 'Atlas', 'Taurus', 'YES'),
('star', 'Atlas A', 'Taurus', 'YES'),
('star', 'Atlas B', 'Taurus', 'YES'),
('star', 'Atlas C', 'Taurus', 'YES'),
('binary system', 'Pleione', 'Taurus', 'YES'),
('star', 'Pleione A', 'Taurus', 'YES'),
('star', 'Pleione B', 'Taurus', 'YES'),
('white dwarf', 'Janus', 'Cygnus', 'YES'),
('white dwarf', 'ZZ Piscium', 'Pisces', 'YES'),
('white dwarf', 'LSPM J0207+3331', 'Orion', 'YES'),
('dwarf planet/asteroid', 'Ceres', NULL, 'YES'),
('minor planet/asteroid', 'Vesta', NULL, 'NO'),
('minor planet/asteroid', 'Pallas', NULL, 'NO'),
('asteroid', 'Psyche', NULL, 'NO'),
('solar system','The Solar System', NULL, 'YES'),
('star', 'Sun', NULL, 'YES'),
('planet', 'Mercury', NULL, 'YES'),
('planet', 'Venus', NULL, 'YES'),
('planet', 'Mars', NULL, 'NO'),
('planet', 'Earth', NULL, 'NO'),
('planet', 'Jupiter', NULL, 'YES'),
('planet', 'Saturn', NULL, 'YES'),
('planet', 'Uranus', NULL, 'YES'),
('planet', 'Neptune', NULL, 'YES'),
('dwarf planet', 'Pluto', NULL, 'NO'),
('stellar system', 'Alpha Centauri', 'Centaurus', 'YES'),
('star', 'Alpha Centauri A', 'Centaurus', 'YES'),
('orange dwarf', 'Alpha Centauri B', 'Centaurus', 'YES'),
('red dwarf', 'Proxima Centauri', 'Centaurus', NULL),
('open star cluster', 'NGC 5617', 'Centaurus', 'YES'),
('star', 'Betelgeuse', 'Orion', 'YES'),
('subcluster', 'Virgo A', 'Virgo', 'YES'),
('subcluster', 'Virgo B', 'Virgo', 'YES'),
('subcluster', 'Virgo C', 'Virgo', 'YES'),
('galaxy', 'M87', 'Virgo', 'YES');

-- Add any queries you'd like below this line

-- View all data
SELECT * FROM celestial_objects;

-- Count total objects
SELECT COUNT(*) AS total_objects FROM celestial_objects;

-- Count beautiful objects per constellation
SELECT constellation, COUNT(*) AS beautiful_objects
FROM celestial_objects
WHERE beauty = 'YES'
GROUP BY constellation;

-- Count objects by type
SELECT object_type, COUNT(*) AS count
FROM celestial_objects
GROUP BY object_type;

-- First 10 objects alphabetically
SELECT object_name, object_type FROM celestial_objects
ORDER BY object_name ASC
LIMIT 10;

-- Count unique constellations
SELECT COUNT(DISTINCT constellation) AS unique_constellations 
FROM celestial_objects;

-- Sorted by constellation and type
SELECT object_name, constellation, object_type FROM celestial_objects
ORDER BY constellation ASC, object_type DESC
LIMIT 10;

-- Alphabetical extremes
SELECT MIN(object_name) AS first_alphabetically,
       MAX(object_name) AS last_alphabetically
FROM celestial_objects;

-- Case formatting example
SELECT UPPER(object_name) AS upper_name, 
       LOWER(constellation) AS lower_const
FROM celestial_objects
LIMIT 5;

-- Longest object names
SELECT object_name, LENGTH(object_name) AS name_length
FROM celestial_objects
ORDER BY name_length DESC
LIMIT 5;

-- Name prefixes
SELECT object_name, SUBSTRING(object_name, 1, 3) AS name_prefix
FROM celestial_objects
LIMIT 5;

-- Concatenated location
SELECT CONCAT(object_name, ' in ', constellation) AS location
FROM celestial_objects
WHERE constellation IS NOT NULL
LIMIT 5;

-- Beauty case label
SELECT object_name, 
       CASE 
           WHEN beauty = 'YES' THEN 'Beautiful'
           WHEN beauty = 'NO' THEN 'Not Beautiful'
           ELSE 'Unknown Beauty'
       END AS beauty_description
FROM celestial_objects
LIMIT 20;

-- Constellation null fallback
SELECT object_name, COALESCE(constellation, 'No Constellation') AS const
FROM celestial_objects
WHERE constellation IS NULL
LIMIT 5;

-- Parent-child object relationships
SELECT c1.object_name AS parent_object, c2.object_name AS child_object
FROM celestial_objects c1
INNER JOIN celestial_objects c2 ON c2.object_name LIKE CONCAT(c1.object_name, ' %')
WHERE c1.object_type IN ('binary system', 'stellar system', 'star system');

-- Objects in same constellations as white dwarfs
SELECT object_name, object_type
FROM celestial_objects
WHERE constellation IN (
    SELECT DISTINCT constellation
    FROM celestial_objects
    WHERE object_type = 'white dwarf'
)
LIMIT 12;

-- Performance check
EXPLAIN ANALYZE
SELECT * FROM celestial_objects
WHERE constellation = 'Taurus' AND object_type = 'star';