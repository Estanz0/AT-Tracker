DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- Static --
-- Stops
CREATE TABLE Stops (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_code NUMERIC(10),
    stop_name VARCHAR(100),
    stop_desc VARCHAR(50),
    stop_lat NUMERIC(12),
    stop_lon NUMERIC(12),
    zone_id VARCHAR(12),
    parent_station VARCHAR(50), -- FK stops
    location_type VARCHAR(100)
);

-- Trips
CREATE TABLE Trips (
    trip_id VARCHAR(50) PRIMARY KEY,
    route_id VARCHAR(50), -- FK Routes
    block_id NUMERIC(5),
    direction_id NUMERIC(1),
    trip_headsign VARCHAR(50),
    shape_id VARCHAR(50), -- FK Shapes
    service_id VARCHAR(50) -- FK ??
);

-- Routes
CREATE TABLE Routes (
    route_id VARCHAR(50) PRIMARY KEY,  
    route_long_name VARCHAR(100),                     
    route_type NUMERIC(2), 
    route_text_color VARCHAR(1),   
    agency_id VARCHAR(10),                       
    route_color NUMERIC(1),    
    route_short_name VARCHAR(10)
);
-- Shapes (dim)
CREATE TABLE Shapes (
    shape_id VARCHAR(50),
    shape_pt_lat NUMERIC(12),
    shape_pt_lon NUMERIC(12),
    shape_pt_sequence NUMERIC(5),
    shape_dist_traveled NUMERIC(10),
    PRIMARY KEY (shape_id, shape_pt_sequence)
);

-- Stop times
CREATE TABLE Stop_times (
    trip_id VARCHAR(50),
    arrival_time VARCHAR(10),
    departure_time VARCHAR(10),
    stop_id VARCHAR(50), -- FK Stops
    stop_sequence INTEGER,
    stop_headsign VARCHAR(20),
    pickup_type INTEGER,
    drop_off_type INTEGER,
    shape_dist_traveled NUMERIC(10),
    PRIMARY KEY (trip_id, stop_sequence)
);

-- Realtime --

CREATE TABLE Vehicle_locations (
    id NUMERIC(6) PRIMARY KEY,
    latitude VARCHAR(10),
    longitude VARCHAR(10),
    bearing INTEGER,
    odometer NUMERIC(10),
    speed NUMERIC(5),
    timestamp VARCHAR(30),
    trip_id VARCHAR(50), -- FK Trips
    route_id VARCHAR(50) -- FK Routes
)
