from sqlalchemy.orm import Session

import models, schemas

# Stops
def get_stop(db: Session, stop_id: int):
    return db.query(models.Stop).filter(models.Stop.stop_id == stop_id).first()

def get_stop_by_code(db: Session, stop_code: int):
    return db.query(models.Stop).filter(models.Stop.stop_code == stop_code).first()

def get_stops(db: Session):
    return db.query(models.Stop).all()

def create_stop(db: Session, stop: schemas.StopCreate):
    db_route = db.query(models.Route).filter(models.Route.route_id == stop.route_id).first()
    stop_dict = stop.dict()
    stop_dict.pop('route_id', None)
    db_stop = models.Stop(**stop_dict)
    if db_route is not None:
        db_stop.routes.append(db_route)
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop

def update_stop(db: Session, stop: schemas.StopCreate):
    db_route = db.query(models.Route).filter(models.Route.route_id == stop.route_id).first()
    db_route_stop = db.query(models.route_stop).filter(models.route_stop.c.route_id == stop.route_id, models.route_stop.c.stop_id == stop.stop_id).first()
    db_stop = db.query(models.Stop).filter(models.Stop.stop_code == stop.stop_code).one()
    if db_route is not None and db_route_stop is None:
        db_stop.routes.append(db_route)
    db_stop.stop_id = stop.stop_id
    db.add(db_stop)
    db.commit()
    return db_stop

def delete_stop(db: Session, stop: schemas.Stop):
    db.delete(stop)
    db.commit()
    return {"ok": True}

# Stop times
def get_stop_times_by_stop(db: Session, stop_id: str):
    return db.query(models.StopTime).filter(models.StopTime.stop_id == stop_id).all()

def create_stop_time(db: Session, stop_time: schemas.StopTimeCreate):
    db_stop_time = models.StopTime(**stop_time.dict())
    db.add(db_stop_time)
    db.commit()
    db.refresh(db_stop_time)
    return db_stop_time

# Routes
def get_route(db: Session, route_id: int):
    return db.query(models.Route).filter(models.Route.route_id == route_id).first()

def get_routes(db: Session):
    return db.query(models.Route).all()

def create_route(db: Session, route: schemas.RouteCreate):
    db_stop = db.query(models.Stop).filter(models.Stop.stop_id == route.stop_id).first()
    route_dict = route.dict()
    route_dict.pop('stop_id', None)
    db_route = models.Route(**route_dict)
    if db_stop is not None:
        db_route.stops.append(db_stop)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def update_route(db: Session, route: schemas.RouteCreate):
    db_route = db.query(models.Route).filter(models.Route.route_id == route.route_id).first()
    db_stop = db.query(models.Stop).filter(models.Stop.stop_id == route.stop_id).first()
    if db_stop is not None and route.stop_id not in db_route.stops:
        db_route.stops.append(db_stop)
    db.add(db_route)
    db.commit()
    return db_route

def delete_route(db: Session, route: schemas.Route):
    db.delete(route)
    db.commit()
    return {"ok": True}

    
# Trip
def get_trip(db: Session, trip_id: int):
    return db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()

def get_trips(db: Session):
    return db.query(models.Trip).all()

def create_trip(db: Session, trip: schemas.TripCreate):
    db_trip = db.query(models.Trip).filter(models.Trip.trip_id == trip.trip_id).first()
    trip_dict = trip.dict()
    db_trip = models.Trip(**trip_dict)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

# def update_trip(db: Session, trip: schemas.TripCreate):
#     db_trip = db.query(models.Trip).filter_by(trip_id=trip.trip_id).one()
#     db.add(db_trip)
#     db.commit()
#     return db_trip

def delete_trip(db: Session, trip: schemas.Trip):
    db.delete(trip)
    db.commit()
    return {"ok": True}


# VehiclePosition
def get_vehicle_position(db: Session, vehicle_id: str):
    return db.query(models.VehiclePosition).filter(models.VehiclePosition.vehicle_id == vehicle_id).first()

def get_vehicle_positions(db: Session):
    return db.query(models.VehiclePosition).all()

def create_vehicle_position(db: Session, vehicle_position: schemas.VehiclePositionCreate):
    db_vehicle_position = db.query(models.VehiclePosition).filter(models.VehiclePosition.vehicle_id == vehicle_position.vehicle_id).first()
    vehicle_position_dict = vehicle_position.dict()
    db_vehicle_position = models.VehiclePosition(**vehicle_position_dict)
    db.add(db_vehicle_position)
    db.commit()
    db.refresh(db_vehicle_position)
    return db_vehicle_position

def update_vehicle_position(db: Session, vehicle_position: schemas.VehiclePositionCreate):
     db_vehicle_position = db.query(models.VehiclePosition).filter_by(vehicle_id=vehicle_position.vehicle_id).one()
     db_vehicle_position.vehicle_lat = vehicle_position.vehicle_lat
     db_vehicle_position.vehicle_lon = vehicle_position.vehicle_lon
     db_vehicle_position.vehicle_bearing = vehicle_position.vehicle_bearing
     db_vehicle_position.vehicle_speed = vehicle_position.vehicle_speed
     db_vehicle_position.vehicle_timestamp = vehicle_position.vehicle_timestamp
     db.add(db_vehicle_position)
     db.commit()
     return db_vehicle_position

def delete_vehicle_position(db: Session, vehicle_position: schemas.VehiclePosition):
    db.delete(vehicle_position)
    db.commit()
    return {"ok": True}

