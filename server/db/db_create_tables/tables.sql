DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

CREATE TABLE stop (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    latitude VARCHAR(10),
    longitude VARCHAR(10)
);

CREATE TABLE vehicle_locations (
    id NUMERIC(6) PRIMARY KEY,
    latitude VARCHAR(10),
    longitude VARCHAR(10),
    bearing NUMERIC(3),
    odometer NUMERIC(10),
    speed NUMERIC(5),
    timestamp TIMESTAMP,
    trip VARCHAR(50),
    route VARCHAR(50)
)

-- INSERT INTO stop (id, name, latitude, longitude) VALUES 
-- ('0097-20220620114222_v101.37', 'Papakura Train Station', -37.06429, 174.94611), 
-- ('0098-20220620114222_v101.37', 'Manurewa Train Station', -37.02327, 174.89617);