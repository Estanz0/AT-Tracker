-- Static --
-- Stops
CREATE TABLE Stops (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_code NUMERIC(10),
    stop_name VARCHAR(100),
    stop_desc VARCHAR(50),
    stop_lat NUMERIC(20),
    stop_lon NUMERIC(20),
    zone_id VARCHAR(12),
    parent_station VARCHAR(50), -- FK stops
    location_type VARCHAR(100)
);
ALTER TABLE Stops 
    ADD CONSTRAINT fk_stops_stops
    FOREIGN KEY (parent_station) 
    REFERENCES Stops (stop_id);

-- Shapes (dim)
CREATE TABLE Shapes (
    shape_id VARCHAR(50),
    shape_pt_lat NUMERIC(20),
    shape_pt_lon NUMERIC(20),
    shape_pt_sequence NUMERIC(5),
    shape_dist_traveled NUMERIC(10),
    PRIMARY KEY (shape_id, shape_pt_sequence)
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

-- Trips
CREATE TABLE Trips (
    trip_id VARCHAR(50) PRIMARY KEY,
    route_id VARCHAR(50) , -- FK Routes
    block_id NUMERIC(5),
    direction_id NUMERIC(10),
    trip_headsign VARCHAR(50),
    shape_id VARCHAR(50), -- FK Shapes ??
    service_id VARCHAR(50) -- FK ??
);
ALTER TABLE Trips 
    ADD CONSTRAINT fk_trips_routes
    FOREIGN KEY (route_id) 
    REFERENCES Routes (route_id);
ALTER TABLE Trips 
    ADD CONSTRAINT fk_trips_shapes
    FOREIGN KEY (shape_id) 
    REFERENCES Shapes (shape_id);

-- Stop times
CREATE TABLE Stop_times (
    trip_id VARCHAR(50),
    arrival_time TIMESTAMP,
    departure_time TIMESTAMP,
    stop_id VARCHAR(50), -- FK Stops
    stop_sequence INTEGER,
    stop_headsign VARCHAR(20),
    pickup_type INTEGER,
    drop_off_type INTEGER,
    shape_dist_traveled NUMERIC(10),
    PRIMARY KEY (trip_id, stop_sequence)
);
ALTER TABLE Stop_times 
    ADD CONSTRAINT fk_stop_times_stops
    FOREIGN KEY (stop_id) 
    REFERENCES Stops (stop_id);

-- Realtime --
CREATE TABLE Vehicle_locations (
    id VARCHAR(20) PRIMARY KEY,
    latitude NUMERIC(20),
    longitude NUMERIC(20),
    bearing NUMERIC(20),
    odometer NUMERIC(20),
    speed NUMERIC(20),
    timestamp TIMESTAMP,
    trip_id VARCHAR(50), -- FK Trips
    route_id VARCHAR(50) -- FK Routes
);
ALTER TABLE Vehicle_locations 
    ADD CONSTRAINT fk_Vehicle_locations_trips
    FOREIGN KEY (trip_id) 
    REFERENCES Trips (trip_id);
ALTER TABLE Vehicle_locations 
    ADD CONSTRAINT fk_Vehicle_locations_routes
    FOREIGN KEY (route_id) 
    REFERENCES Routes (route_id);

-- Roles
CREATE ROLE postgres WITH PASSWORD 'postgres' LOGIN;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO postgres;
GRANT CONNECT ON DATABASE buses_db TO postgres;
