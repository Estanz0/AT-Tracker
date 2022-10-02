CREATE TABLE "routes" (
  "route_id" string(50),
  "route_short_name" string(50),
  "route_long_name" string(50),
  "route_type" integer(2),
  "route_text_color" string(10),
  "agency_id" string(50),
  "route_color" string(10),
  PRIMARY KEY ("route_id")
);

CREATE TABLE "shapes" (
  "shape_id" string(50),
  "shape_pt_lat" latitude(20),
  "shape_pt_lon" longitude(20),
  "shape_pt_sequence" integer(20),
  "shape_dist_traveled" float(20),
  PRIMARY KEY ("shape_id")
);

CREATE TABLE "trips" (
  "trip_id" string(50),
  "trip_headsign" string(50),
  "route_id" string(50),
  "block_id" string(50),
  "direction_id" integer(1),
  "shape_id" string(50),
  "service_id" string(50),
  PRIMARY KEY ("trip_id"),
  CONSTRAINT "FK_trips.route_id"
    FOREIGN KEY ("route_id")
      REFERENCES "routes"("route_id"),
  CONSTRAINT "FK_trips.shape_id"
    FOREIGN KEY ("shape_id")
      REFERENCES "shapes"("shape_id")
);

CREATE TABLE "stops" (
  "stop_id" string(50),
  "stop_code" string(50),
  "stop_name" string(50),
  "stop_desc" string(50),
  "stop_lat" latitude(20),
  "stop_lon" longitude(20),
  "parent_station" string(50),
  "location_type" integer(1),
  "zone_id" string(50),
  PRIMARY KEY ("stop_id"),
  CONSTRAINT "FK_stops.parent_station"
    FOREIGN KEY ("parent_station")
      REFERENCES "stops"("stop_id"),
  CONSTRAINT "FK_stops.parent_station"
    FOREIGN KEY ("parent_station")
      REFERENCES "stops"("stop_id")
);

CREATE TABLE "stop_times" (
  "trip_id" string(50),
  "stop_id" string(50),
  "arrival_time" datetime(50),
  "departure_time" datetime(50),
  "stop_sequence" integer(10),
  "stop_headsign" string(50),
  "pickup_type" integer(1),
  "drop_off_type" integer(1),
  "shape_dist_traveled" float(20),
  CONSTRAINT "FK_stop_times.trip_id"
    FOREIGN KEY ("trip_id")
      REFERENCES "trips"("trip_id"),
  CONSTRAINT "FK_stop_times.stop_id"
    FOREIGN KEY ("stop_id")
      REFERENCES "stops"("stop_id")
);

