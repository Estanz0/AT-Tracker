from typing import List, Union
from datetime import datetime
from pydantic import BaseModel



# StopTimes
class StopTimeBase(BaseModel):
    trip_id: str
    arrival_time: datetime = None
    departure_time: datetime
    stop_id: str
    stop_sequence: int = None
    stop_headsign: str = None
    pickup_type: int = None
    drop_off_type: int = None
    shape_dist_traveled: int = None

    class Config:
        orm_mode = True
    

class StopTimeCreate(StopTimeBase):
    pass


class StopTime(StopTimeBase):
    pass

# Stops
class StopBase(BaseModel):
    stop_id: str
    stop_code: str 
    stop_name: str = None
    stop_desc: str = None
    stop_lat: float = None
    stop_lon: float = None

    class Config:
        orm_mode = True

class StopCreate(StopBase):
    route_id: str = None


class Stop(StopBase):
    stop_times: List[StopTime] = []
    # routes: List[Route] = []

# Trips
class TripBase(BaseModel):
    trip_id: str
    route_id: str = None
    service_id: str = None
    trip_headsign: str = None
    direction_id: int = None
    shape_id: str

    class Config:
        orm_mode = True

class TripCreate(TripBase):
    pass


class Trip(TripBase):
    pass


# Routes
class RouteBase(BaseModel):
    route_id: str
    route_long_name: str
    route_short_name: str

    class Config:
        orm_mode = True

class RouteCreate(RouteBase):
    stop_id: str = None


class Route(RouteBase):
    stops: List[Stop] = []
    trips: List[Trip] = []


# Vehicle Positions
class VehiclePositionBase(BaseModel):
    vehicle_id: str
    vehicle_lat: float
    vehicle_lon: float
    vehicle_bearing: float = None
    vehicle_speed: float = None
    vehicle_timestamp: datetime
    trip_id: str = None
    route_id: str = None
    direction_id: int = None

    class Config:
        orm_mode = True

class VehiclePositionCreate(VehiclePositionBase):
    pass

class VehiclePosition(VehiclePositionBase):
    pass
    # route: Route = None


