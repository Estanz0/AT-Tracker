from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Stops
@app.post("/stops/", response_model=schemas.Stop)
def create_stop(stop: schemas.StopCreate, db: Session = Depends(get_db)):
    db_stop = crud.get_stop_by_code(db=db, stop_code=stop.stop_code)
    if db_stop:
        # raise HTTPException(status_code=404, detail="Stop already exists")
        return crud.update_stop(db=db, stop=stop)
    return crud.create_stop(db=db, stop=stop)


@app.get("/stops/", response_model=List[schemas.Stop])
def read_stops(db: Session = Depends(get_db)):
    stops = crud.get_stops(db=db)
    return stops


@app.get("/stops/{stop_id}", response_model=schemas.Stop)
def read_stop(stop_id: str, db: Session = Depends(get_db)):
    db_stop = crud.get_stop(db=db, stop_id=stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return db_stop

@app.delete("/stops/{stop_code}")
def delete_stop(stop_code: str, db: Session = Depends(get_db)):
    db_stop = crud.get_stop_by_code(db=db, stop_code=stop_code)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.delete_stop(db=db, stop=db_stop)
    

# Stop times
@app.post("/stoptimes/", response_model=schemas.StopTimeCreate)
def create_stop_time(stop_time: schemas.StopTimeCreate, db: Session = Depends(get_db)):
    return crud.create_stop_time(db=db, stop_time=stop_time)


@app.get("/stops/{stop_id}/stoptimes/", response_model=List[schemas.StopTime])
def read_stop_times(stop_id: str, db: Session = Depends(get_db)):
    stop_times = crud.get_stop_times_by_stop(db=db, stop_id=stop_id)
    return stop_times


# Routes
@app.get("/routes/", response_model=List[schemas.Route])
def read_routes(db: Session = Depends(get_db)):
    routes = crud.get_routes(db=db)
    return routes

@app.get("/routes/{route_id}", response_model=schemas.Route)
def read_route(route_id: str, db: Session = Depends(get_db)):
    db_route = crud.get_route(db=db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route

@app.post("/routes/", response_model=schemas.Route)
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = crud.get_route(db=db, route_id=route.route_id)
    if db_route:
        # raise HTTPException(status_code=404, detail="Stop already exists")
        return crud.update_route(db=db, route=route)
    return crud.create_route(db=db, route=route)

@app.delete("/routes/{route_id}")
def delete_route(route_id: str, db: Session = Depends(get_db)):
    db_route = crud.get_route(db=db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return crud.delete_route(db=db, route=db_route)


# Trips
@app.get("/trips/", response_model=List[schemas.Trip])
def read_trips(db: Session = Depends(get_db)):
    trips = crud.get_trips(db=db)
    return trips

@app.get("/trips/{trip_id}", response_model=schemas.Trip)
def read_trip(trip_id: str, db: Session = Depends(get_db)):
    db_trip = crud.get_trip(db=db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

@app.post("/trips/", response_model=schemas.Trip)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    db_trip = crud.get_trip(db=db, trip_id=trip.trip_id)
    if db_trip:
        raise HTTPException(status_code=404, detail="Trip already exists")
        # return crud.update_trip(db=db, trip=trip)
    return crud.create_trip(db=db, trip=trip)

@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: str, db: Session = Depends(get_db)):
    db_trip = crud.get_trip(db=db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return crud.delete_trip(db=db, trip=db_trip)


# Vehicle Positions
@app.get("/vehicle_positions/", response_model=List[schemas.VehiclePosition])
def read_vehicle_positions(db: Session = Depends(get_db)):
    vehicle_positions = crud.get_vehicle_positions(db=db)
    return vehicle_positions

@app.get("/vehicle_positions/{vehicle_id}", response_model=schemas.VehiclePosition)
def read_vehicle_position(vehicle_id: str, db: Session = Depends(get_db)):
    db_vehicle_position = crud.get_vehicle_position(db=db, vehicle_id=vehicle_id)
    if db_vehicle_position is None:
        raise HTTPException(status_code=404, detail="Vehicle Position not found")
    return db_vehicle_position

@app.post("/vehicle_positions/", response_model=schemas.VehiclePosition)
def create_vehicle_position(vehicle_position: schemas.VehiclePositionCreate, db: Session = Depends(get_db)):
    db_vehicle_position = crud.get_vehicle_position(db=db, vehicle_id=vehicle_position.vehicle_id)
    if db_vehicle_position:
        return crud.update_vehicle_position(db=db, vehicle_position=vehicle_position)
    return crud.create_vehicle_position(db=db, vehicle_position=vehicle_position)

@app.delete("/vehicle_positions/{vehicle_id}")
def delete_vehicle_position(vehicle_id: str, db: Session = Depends(get_db)):
    db_vehicle_position = crud.get_vehicle_position(db=db, vehicle_id=vehicle_id)
    if db_vehicle_position is None:
        raise HTTPException(status_code=404, detail="Vehicle Position not found")
    return crud.delete_vehicle_position(db=db, vehicle_position=db_vehicle_position)


